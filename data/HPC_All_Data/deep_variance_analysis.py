#!/usr/bin/env python
"""
Deep variance analysis to identify specific subject counts where variance drops significantly.

This script performs comprehensive analysis:
1. Calculates variance drops at each subject count
2. Identifies largest variance reductions
3. Finds inflection points (where rate of change changes)
4. Analyzes patterns across all models
5. Generates detailed visualizations and statistics
"""

import json
import math
import random
from pathlib import Path
from collections import defaultdict
import itertools
import statistics
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_6_complete",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

MAX_COMBINATIONS = 10000
MAX_TEST_GROUPS = 15
RANDOM_SAMPLE_SIZE = 30  # Number of random combinations to sample per number of groups

def extract_hyperparams(results_file):
    """Extract hyperparameters from results.json file."""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        return data.get('hyperparams', {})
    except:
        return {}

def format_model_hp_label(model_name, hyperparams):
    """Format model×hyperparameter label."""
    if hyperparams:
        sorted_keys = sorted(hyperparams.keys())
        param_str = ", ".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
        return f"{model_name} ({param_str})"
    else:
        return f"{model_name} (default)"

def count_subjects_in_fold(fold_name):
    """Count number of subjects in a fold name like 'sub-2_sub-39'."""
    return len(re.findall(r'sub-\d+', fold_name))

def load_fold_accuracies(exp_name, results_dir):
    """Load accuracy for each fold×model×HP combination."""
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    model_hp_fold_accuracies = defaultdict(dict)
    all_fold_names = set()
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        for fold_dir in model_dir.iterdir():
            if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
                all_fold_names.add(fold_dir.name)
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        model_name = model_dir.name
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            fold_name = fold_dir.name
            results_files = list(fold_dir.rglob("results.json"))
            if not results_files:
                task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
                for task_dir in task_dirs:
                    results_file = task_dir / "results.json"
                    if results_file.exists():
                        results_files.append(results_file)
                        break
            if results_files:
                try:
                    with open(results_files[0], 'r') as f:
                        data = json.load(f)
                    accuracy = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                    if accuracy is not None:
                        acc = float(accuracy)
                        hyperparams = extract_hyperparams(results_files[0])
                        model_hp_key = format_model_hp_label(model_name, hyperparams)
                        model_hp_fold_accuracies[model_hp_key][fold_name] = acc
                except Exception as e:
                    continue
    
    return model_hp_fold_accuracies

def load_subject_accuracies_cache(results_dir, model_name):
    """
    Pre-load all subject accuracies for a model to avoid repeated parquet reads.
    
    Returns: {fold_name: [list of subject accuracies]}
    """
    cache = {}
    model_dir = results_dir / model_name
    if not model_dir.exists():
        return cache
    
    print(f"      Loading subject accuracies for {model_name}...", end='', flush=True)
    fold_count = 0
    
    for fold_dir in model_dir.iterdir():
        if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
            continue
        
        fold_name = fold_dir.name
        fold_accuracies = []
        
        # Find all task directories in this fold
        task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
        
        for task_dir in task_dirs:
            test_parquet = task_dir / "test_predictions.parquet"
            if not test_parquet.exists():
                continue
            
            try:
                # Read test predictions
                test_df = pd.read_parquet(test_parquet)
                
                # Calculate per-subject accuracy
                for subject_id_num in test_df['SubjectID'].unique():
                    subject_data = test_df[test_df['SubjectID'] == subject_id_num]
                    
                    # Calculate accuracy: (label == prediction).sum() / len(subject_data)
                    correct = (subject_data['label'] == subject_data['prediction']).sum()
                    total = len(subject_data)
                    accuracy = correct / total if total > 0 else 0.0
                    
                    fold_accuracies.append(accuracy)
            except Exception as e:
                continue
        
        if fold_accuracies:
            cache[fold_name] = fold_accuracies
            fold_count += 1
    
    print(f" loaded {fold_count} folds")
    return cache

def calculate_variance_for_combination_from_cache(fold_names, subject_accuracies_cache):
    """
    Calculate variance of individual subject accuracies for a combination of folds.
    Uses pre-loaded cache to avoid repeated parquet reads.
    """
    all_subject_accuracies = []
    
    for fold_name in fold_names:
        if fold_name in subject_accuracies_cache:
            all_subject_accuracies.extend(subject_accuracies_cache[fold_name])
    
    if len(all_subject_accuracies) < 2:
        return 0.0
    
    return statistics.variance(all_subject_accuracies)

def calculate_variance_for_combination(fold_names, fold_accuracies):
    """Calculate variance of accuracies for a specific combination of folds (OLD METHOD - group means)."""
    accs = []
    for fold_name in fold_names:
        if fold_name in fold_accuracies:
            accs.append(fold_accuracies[fold_name])
        else:
            return None
    if len(accs) < 2:
        return 0.0
    return statistics.variance(accs)

def calculate_variance_by_test_groups(fold_accuracies, subject_accuracies_cache=None, use_individual_accuracies=False):
    """
    Calculate variance statistics for each number of test groups.
    
    If use_individual_accuracies=True, calculates variance of all individual subject accuracies
    across the selected groups (not variance of group means).
    Uses pre-loaded cache to avoid repeated parquet reads.
    """
    fold_names = list(fold_accuracies.keys())
    total_folds = len(fold_names)
    if total_folds == 0:
        return {}
    
    subjects_per_group = count_subjects_in_fold(fold_names[0])
    results = {}
    max_groups = min(MAX_TEST_GROUPS, total_folds)
    
    for num_groups in range(1, max_groups + 1):
        print(f"      Processing {num_groups} groups...", end='', flush=True)
        total_combinations = math.comb(total_folds, num_groups)
        
        # Always use random sampling for efficiency
        # Sample RANDOM_SAMPLE_SIZE combinations (or all if fewer exist)
        sample_size = min(RANDOM_SAMPLE_SIZE, total_combinations)
        sampled_combos = set()
        while len(sampled_combos) < sample_size:
            combo = tuple(sorted(random.sample(fold_names, num_groups)))
            sampled_combos.add(combo)
        combinations = list(sampled_combos)
        
        print(f" (sampling {len(combinations)}/{total_combinations} combinations)", end='', flush=True)
        
        variances = []
        for i, combo in enumerate(combinations):
            if (i + 1) % 10 == 0:
                print(f" {i+1}/{len(combinations)}", end='', flush=True)
            
            if use_individual_accuracies and subject_accuracies_cache:
                # NEW METHOD: Variance of all individual subject accuracies (from cache)
                var = calculate_variance_for_combination_from_cache(combo, subject_accuracies_cache)
            else:
                # OLD METHOD: Variance of group means
                var = calculate_variance_for_combination(combo, fold_accuracies)
            
            if var is not None:
                variances.append(var)
        
        print(f" done ({len(variances)} valid)")
        
        if variances:
            mean_var = statistics.mean(variances)
            std_var = statistics.stdev(variances) if len(variances) > 1 else 0.0
            results[num_groups] = {
                'mean_variance': mean_var,
                'std_variance': std_var,
                'num_combinations': len(variances),
                'subjects_included': num_groups * subjects_per_group
            }
    
    return results

def analyze_variance_drops(variance_data):
    """
    Analyze variance drops at each subject count.
    
    Returns detailed analysis of variance changes.
    """
    if len(variance_data) < 2:
        return {}
    
    num_groups_list = sorted(variance_data.keys())
    subjects_list = [variance_data[n]['subjects_included'] for n in num_groups_list]
    variances = [variance_data[n]['mean_variance'] for n in num_groups_list]
    
    analysis = {
        'subjects': subjects_list,
        'variances': variances,
        'absolute_drops': [],
        'percentage_drops': [],
        'drop_points': [],
        'largest_drops': []
    }
    
    # Calculate drops
    for i in range(1, len(variances)):
        prev_var = variances[i-1]
        curr_var = variances[i]
        prev_subj = subjects_list[i-1]
        curr_subj = subjects_list[i]
        
        if prev_var > 0:
            abs_drop = prev_var - curr_var
            pct_drop = (abs_drop / prev_var) * 100
            
            analysis['absolute_drops'].append(abs_drop)
            analysis['percentage_drops'].append(pct_drop)
            analysis['drop_points'].append({
                'from_subjects': prev_subj,
                'to_subjects': curr_subj,
                'from_variance': prev_var,
                'to_variance': curr_var,
                'absolute_drop': abs_drop,
                'percentage_drop': pct_drop
            })
    
    # Find largest drops
    if analysis['drop_points']:
        sorted_drops = sorted(analysis['drop_points'], 
                            key=lambda x: x['percentage_drop'], 
                            reverse=True)
        analysis['largest_drops'] = sorted_drops[:5]  # Top 5
    
    # Calculate rate of change (second derivative approximation)
    if len(variances) >= 3:
        rates_of_change = []
        for i in range(1, len(variances) - 1):
            # Rate of change: (v[i+1] - v[i]) - (v[i] - v[i-1])
            rate = (variances[i+1] - variances[i]) - (variances[i] - variances[i-1])
            rates_of_change.append({
                'subjects': subjects_list[i],
                'rate_of_change': rate,
                'variance': variances[i]
            })
        analysis['rates_of_change'] = rates_of_change
        
        # Find inflection points (where rate of change changes sign or is near zero)
        inflection_points = []
        for i in range(1, len(rates_of_change)):
            if rates_of_change[i-1]['rate_of_change'] * rates_of_change[i]['rate_of_change'] < 0:
                # Sign change - inflection point
                inflection_points.append({
                    'subjects': rates_of_change[i]['subjects'],
                    'variance': rates_of_change[i]['variance'],
                    'type': 'sign_change'
                })
        analysis['inflection_points'] = inflection_points
    
    # Find where variance first becomes "low" (below threshold)
    # Use median of all variances as threshold for "low"
    if variances:
        median_variance = statistics.median(variances)
        low_variance_threshold = median_variance * 1.1  # 10% above median
        
        first_low_point = None
        for i, (subj, var) in enumerate(zip(subjects_list, variances)):
            if var <= low_variance_threshold:
                first_low_point = {
                    'subjects': subj,
                    'variance': var,
                    'index': i
                }
                break
        
        analysis['first_low_variance'] = first_low_point
        analysis['median_variance'] = median_variance
        analysis['low_threshold'] = low_variance_threshold
    
    return analysis

def find_optimal_subject_count(all_analyses):
    """
    Find optimal subject count based on aggregate analysis.
    
    Looks for consistent patterns across all models.
    Analyzes L_2 and L_6 experiments separately to find consistent subject thresholds.
    """
    # Separate by experiment type
    l2_drop_points = []
    l6_drop_points = []
    l2_inflection_points = []
    l6_inflection_points = []
    l2_largest_drops = []
    l6_largest_drops = []
    
    # Also collect all together for overall analysis
    all_drop_points = []
    all_inflection_points = []
    all_largest_drops = []
    
    for exp_name, exp_results in all_analyses.items():
        is_l2 = 'L_2' in exp_name
        is_l6 = 'L_6' in exp_name
        
        for model_hp, data in exp_results.items():
            analysis = data.get('variance_analysis', {})
            if not analysis:
                continue
            
            # Collect drop points
            for drop in analysis.get('drop_points', []):
                drop_point = {
                    'subjects': drop['to_subjects'],
                    'percentage_drop': drop['percentage_drop'],
                    'experiment': exp_name,
                    'model': model_hp
                }
                all_drop_points.append(drop_point)
                if is_l2:
                    l2_drop_points.append(drop_point)
                elif is_l6:
                    l6_drop_points.append(drop_point)
            
            # Collect inflection points
            for inf in analysis.get('inflection_points', []):
                inf_point = {
                    'subjects': inf['subjects'],
                    'experiment': exp_name,
                    'model': model_hp
                }
                all_inflection_points.append(inf_point)
                if is_l2:
                    l2_inflection_points.append(inf_point)
                elif is_l6:
                    l6_inflection_points.append(inf_point)
            
            # Collect largest drops
            for drop in analysis.get('largest_drops', [])[:1]:  # Just the largest
                largest_drop = {
                    'subjects': drop['to_subjects'],
                    'percentage_drop': drop['percentage_drop'],
                    'experiment': exp_name,
                    'model': model_hp
                }
                all_largest_drops.append(largest_drop)
                if is_l2:
                    l2_largest_drops.append(largest_drop)
                elif is_l6:
                    l6_largest_drops.append(largest_drop)
    
    # Analyze separately for L_2 and L_6
    def analyze_subject_counts(drop_points, name):
        significant_drops = [d for d in drop_points if d['percentage_drop'] > 1.0]
        subject_drop_counts = defaultdict(list)
        for drop in significant_drops:
            subject_drop_counts[drop['subjects']].append(drop['percentage_drop'])
        
        subject_stats = {}
        for subjects, drops in subject_drop_counts.items():
            subject_stats[subjects] = {
                'count': len(drops),
                'mean_drop': statistics.mean(drops),
                'median_drop': statistics.median(drops),
                'max_drop': max(drops),
                'min_drop': min(drops)
            }
        
        sorted_subjects = sorted(subject_stats.items(), 
                               key=lambda x: (x[1]['count'], x[1]['mean_drop']), 
                               reverse=True)
        return subject_stats, sorted_subjects
    
    l2_stats, l2_top = analyze_subject_counts(l2_drop_points, 'L_2')
    l6_stats, l6_top = analyze_subject_counts(l6_drop_points, 'L_6')
    
    # Overall analysis (all together)
    significant_drops = [d for d in all_drop_points if d['percentage_drop'] > 1.0]
    subject_drop_counts = defaultdict(list)
    for drop in significant_drops:
        subject_drop_counts[drop['subjects']].append(drop['percentage_drop'])
    
    subject_stats = {}
    for subjects, drops in subject_drop_counts.items():
        subject_stats[subjects] = {
            'count': len(drops),
            'mean_drop': statistics.mean(drops),
            'median_drop': statistics.median(drops),
            'max_drop': max(drops),
            'min_drop': min(drops)
        }
    
    sorted_subjects = sorted(subject_stats.items(), 
                           key=lambda x: (x[1]['count'], x[1]['mean_drop']), 
                           reverse=True)
    
    return {
        'subject_statistics': subject_stats,
        'top_subject_counts': sorted_subjects[:10],
        'l2_statistics': l2_stats,
        'l2_top_subjects': l2_top[:10],
        'l6_statistics': l6_stats,
        'l6_top_subjects': l6_top[:10],
        'l2_drop_points': l2_drop_points,
        'l6_drop_points': l6_drop_points,
        'l2_inflection_points': l2_inflection_points,
        'l6_inflection_points': l6_inflection_points,
        'all_drop_points': all_drop_points,
        'all_inflection_points': all_inflection_points,
        'all_largest_drops': all_largest_drops
    }

def create_aggregate_visualization(aggregate_analysis, output_dir):
    """Create visualization showing variance drops across all models."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Distribution of significant drops by subject count
    ax1 = axes[0, 0]
    significant_drops = [d for d in aggregate_analysis['all_drop_points'] if d['percentage_drop'] > 1.0]
    subject_counts = [d['subjects'] for d in significant_drops]
    if subject_counts:
        ax1.hist(subject_counts, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
        ax1.set_xlabel('Number of Subjects', fontweight='bold')
        ax1.set_ylabel('Frequency of Significant Drops (>5%)', fontweight='bold')
        ax1.set_title('Distribution of Significant Variance Drops\nby Subject Count', fontweight='bold')
        ax1.grid(True, alpha=0.3)
    
    # 2. Mean drop percentage by subject count
    ax2 = axes[0, 1]
    subject_stats = aggregate_analysis['subject_statistics']
    if subject_stats:
        subjects = sorted(subject_stats.keys())
        mean_drops = [subject_stats[s]['mean_drop'] for s in subjects]
        counts = [subject_stats[s]['count'] for s in subjects]
        ax2.scatter(subjects, mean_drops, s=[c*10 for c in counts], 
                   alpha=0.6, color='crimson', edgecolors='black')
        ax2.set_xlabel('Number of Subjects', fontweight='bold')
        ax2.set_ylabel('Mean Percentage Drop (%)', fontweight='bold')
        ax2.set_title('Mean Variance Drop by Subject Count\n(Bubble size = frequency)', fontweight='bold')
        ax2.grid(True, alpha=0.3)
    
    # 3. Cumulative variance reduction
    ax3 = axes[1, 0]
    # Group by experiment type
    exp_types = {}
    for drop in aggregate_analysis['all_drop_points']:
        exp = drop['experiment']
        if 'L_2' in exp:
            exp_type = 'L_2 (2 subjects/group)'
        elif 'L_6' in exp:
            exp_type = 'L_6 (6 subjects/group)'
        else:
            exp_type = exp
        if exp_type not in exp_types:
            exp_types[exp_type] = []
        exp_types[exp_type].append(drop)
    
    for exp_type, drops in exp_types.items():
        subjects = sorted(set([d['subjects'] for d in drops]))
        cumulative_drops = []
        for s in subjects:
            relevant_drops = [d['percentage_drop'] for d in drops if d['subjects'] <= s]
            cumulative_drops.append(sum(relevant_drops))
        ax3.plot(subjects, cumulative_drops, marker='o', label=exp_type, linewidth=2)
    
    ax3.set_xlabel('Number of Subjects', fontweight='bold')
    ax3.set_ylabel('Cumulative Variance Reduction (%)', fontweight='bold')
    ax3.set_title('Cumulative Variance Reduction by Subject Count', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Top subject counts with most drops
    ax4 = axes[1, 1]
    top_subjects = aggregate_analysis['top_subject_counts'][:10]
    if top_subjects:
        subjects = [s[0] for s in top_subjects]
        counts = [s[1]['count'] for s in top_subjects]
        mean_drops = [s[1]['mean_drop'] for s in top_subjects]
        
        x = np.arange(len(subjects))
        width = 0.35
        ax4.bar(x - width/2, counts, width, label='Frequency', alpha=0.8, color='skyblue')
        ax4_twin = ax4.twinx()
        ax4_twin.bar(x + width/2, mean_drops, width, label='Mean Drop %', alpha=0.8, color='salmon')
        
        ax4.set_xlabel('Number of Subjects', fontweight='bold')
        ax4.set_ylabel('Frequency of Drops', fontweight='bold', color='steelblue')
        ax4_twin.set_ylabel('Mean Drop Percentage (%)', fontweight='bold', color='crimson')
        ax4.set_title('Top 10 Subject Counts with Most Variance Drops', fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(subjects, rotation=45, ha='right')
        ax4.grid(True, alpha=0.3, axis='y')
        ax4.legend(loc='upper left')
        ax4_twin.legend(loc='upper right')
    
    plt.tight_layout()
    output_file = output_dir / 'deep_variance_analysis_aggregate.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   ✅ Saved aggregate visualization: {output_file.name}")

def generate_detailed_report(all_analyses, aggregate_analysis, output_file):
    """Generate comprehensive markdown report."""
    report = []
    report.append("# Deep Variance Analysis: Identifying Optimal Subject Counts\n")
    report.append("## Executive Summary\n")
    
    # Key findings
    top_subjects = aggregate_analysis['top_subject_counts']
    if top_subjects:
        report.append("### Key Findings\n")
        report.append(f"**Most Common Subject Counts with Significant Variance Drops:**\n")
        for i, (subjects, stats) in enumerate(top_subjects[:5], 1):
            report.append(f"{i}. **{subjects} subjects**: {stats['count']} models show drops (mean: {stats['mean_drop']:.1f}%, max: {stats['max_drop']:.1f}%)")
        report.append("")
    
    # Overall recommendation - analyze separately
    report.append("### Overall Recommendation\n")
    
    # L_2 analysis
    l2_top = aggregate_analysis.get('l2_top_subjects', [])
    l6_top = aggregate_analysis.get('l6_top_subjects', [])
    
    report.append("#### For L_2 Experiments (2 subjects per test group)\n")
    if l2_top:
        best_subject = l2_top[0][0]
        best_stats = l2_top[0][1]
        report.append(f"**{best_subject} subjects appears to be the optimal threshold** (equivalent to {best_subject//2} test groups).")
        report.append(f"- Observed in {best_stats['count']} model×HP combinations")
        report.append(f"- Mean variance drop: {best_stats['mean_drop']:.1f}%")
        report.append(f"- Maximum variance drop: {best_stats['max_drop']:.1f}%")
    else:
        report.append("No significant variance drops detected (>1% threshold).")
    report.append("")
    
    report.append("#### For L_6 Experiments (6 subjects per test group)\n")
    if l6_top:
        best_subject = l6_top[0][0]
        best_stats = l6_top[0][1]
        report.append(f"**{best_subject} subjects appears to be the optimal threshold** (equivalent to {best_subject//6} test groups).")
        report.append(f"- Observed in {best_stats['count']} model×HP combinations")
        report.append(f"- Mean variance drop: {best_stats['mean_drop']:.1f}%")
        report.append(f"- Maximum variance drop: {best_stats['max_drop']:.1f}%")
    else:
        report.append("No significant variance drops detected (>1% threshold).")
    report.append("")
    
    # Cross-experiment consistency check
    report.append("#### Cross-Experiment Consistency Check\n")
    if l2_top and l6_top:
        l2_best = l2_top[0][0]
        l6_best = l6_top[0][0]
        l2_groups = l2_best // 2
        l6_groups = l6_best // 6
        
        if l2_groups == l6_groups:
            report.append(f"✅ **CONSISTENT PATTERN**: Both L_2 and L_6 experiments show optimal threshold at **{l2_groups} test groups**")
            report.append(f"- L_2: {l2_best} subjects = {l2_groups} groups")
            report.append(f"- L_6: {l6_best} subjects = {l6_groups} groups")
            report.append(f"- This suggests **{l2_groups} test groups** is the key threshold, regardless of subjects per group")
        else:
            report.append(f"⚠️ **INCONSISTENT PATTERN**: Different optimal thresholds detected")
            report.append(f"- L_2 optimal: {l2_best} subjects ({l2_groups} groups)")
            report.append(f"- L_6 optimal: {l6_best} subjects ({l6_groups} groups)")
            report.append("")
            report.append("**Note**: Since variance drops are very small (<2%), variance is already quite stable.")
            report.append("The inconsistent patterns suggest there may not be a single optimal subject count.")
            report.append("Instead, variance appears to stabilize early (around 3-6 test groups) regardless of total subjects.")
    report.append("")
    
    # Analyze where variance first becomes "low" (absolute levels)
    report.append("#### Analysis: Where Variance First Becomes Low\n")
    report.append("Since variance drops are small, we analyze where variance first reaches acceptably low levels.\n")
    
    l2_first_low = []
    l6_first_low = []
    
    for exp_name, exp_results in all_analyses.items():
        is_l2 = 'L_2' in exp_name
        is_l6 = 'L_6' in exp_name
        
        for model_hp, data in exp_results.items():
            analysis = data.get('variance_analysis', {})
            first_low = analysis.get('first_low_variance')
            if first_low:
                if is_l2:
                    l2_first_low.append(first_low['subjects'])
                elif is_l6:
                    l6_first_low.append(first_low['subjects'])
    
    if l2_first_low:
        report.append("**L_2 Experiments - First Low Variance Point:**")
        report.append(f"- Median: {statistics.median(l2_first_low)} subjects")
        report.append(f"- Mean: {statistics.mean(l2_first_low):.1f} subjects")
        report.append(f"- Range: {min(l2_first_low)} - {max(l2_first_low)} subjects")
        report.append("")
    
    if l6_first_low:
        report.append("**L_6 Experiments - First Low Variance Point:**")
        report.append(f"- Median: {statistics.median(l6_first_low)} subjects")
        report.append(f"- Mean: {statistics.mean(l6_first_low):.1f} subjects")
        report.append(f"- Range: {min(l6_first_low)} - {max(l6_first_low)} subjects")
        report.append("")
    
    # Check if there's a consistent absolute subject count
    all_first_low = l2_first_low + l6_first_low
    if all_first_low:
        report.append("**Overall - First Low Variance Point (All Experiments):**")
        report.append(f"- Median: {statistics.median(all_first_low)} subjects")
        report.append(f"- Mean: {statistics.mean(all_first_low):.1f} subjects")
        report.append("")
        
        # Check consistency
        if l2_first_low and l6_first_low:
            l2_median = statistics.median(l2_first_low)
            l6_median = statistics.median(l6_first_low)
            if abs(l2_median - l6_median) / max(l2_median, l6_median) < 0.3:  # Within 30%
                report.append(f"✅ **CONSISTENT**: Both experiment types show similar absolute subject counts")
                report.append(f"- Suggests there may be a consistent subject count threshold (~{int(statistics.median(all_first_low))} subjects)")
            else:
                report.append(f"⚠️ **INCONSISTENT**: Different absolute subject counts")
                report.append(f"- L_2 median: {l2_median} subjects")
                report.append(f"- L_6 median: {l6_median} subjects")
                report.append("- This suggests the threshold is based on number of groups, not absolute subjects")
    report.append("")
    
    # Detailed statistics
    report.append("## Detailed Statistics\n")
    
    # L_2 Statistics
    report.append("### L_2 Experiments: Subject Counts with Significant Drops (>1%)\n")
    report.append("| Subjects | Groups | Frequency | Mean Drop % | Median Drop % | Max Drop % | Min Drop % |")
    report.append("|----------|--------|-----------|-------------|---------------|------------|------------|")
    l2_stats = aggregate_analysis.get('l2_statistics', {})
    for subjects, stats in sorted(l2_stats.items()):
        if stats['count'] > 0:
            groups = subjects // 2
            report.append(f"| {subjects} | {groups} | {stats['count']} | {stats['mean_drop']:.2f} | {stats['median_drop']:.2f} | {stats['max_drop']:.2f} | {stats['min_drop']:.2f} |")
    report.append("")
    
    # L_6 Statistics
    report.append("### L_6 Experiments: Subject Counts with Significant Drops (>1%)\n")
    report.append("| Subjects | Groups | Frequency | Mean Drop % | Median Drop % | Max Drop % | Min Drop % |")
    report.append("|----------|--------|-----------|-------------|---------------|------------|------------|")
    l6_stats = aggregate_analysis.get('l6_statistics', {})
    for subjects, stats in sorted(l6_stats.items()):
        if stats['count'] > 0:
            groups = subjects // 6
            report.append(f"| {subjects} | {groups} | {stats['count']} | {stats['mean_drop']:.2f} | {stats['median_drop']:.2f} | {stats['max_drop']:.2f} | {stats['min_drop']:.2f} |")
    report.append("")
    
    # Overall Statistics
    report.append("### Overall: Subject Counts with Significant Drops (>1%)\n")
    report.append("| Subjects | Frequency | Mean Drop % | Median Drop % | Max Drop % | Min Drop % |")
    report.append("|----------|-----------|-------------|---------------|------------|------------|")
    for subjects, stats in sorted(aggregate_analysis['subject_statistics'].items()):
        if stats['count'] > 0:
            report.append(f"| {subjects} | {stats['count']} | {stats['mean_drop']:.2f} | {stats['median_drop']:.2f} | {stats['max_drop']:.2f} | {stats['min_drop']:.2f} |")
    report.append("")
    
    # Per-experiment analysis
    report.append("## Per-Experiment Analysis\n")
    for exp_name, exp_results in all_analyses.items():
        report.append(f"### {exp_name}\n")
        
        # Find largest drops per model
        report.append("#### Largest Variance Drops by Model\n")
        report.append("| Model×HP | Subjects | Drop % | From Variance | To Variance |")
        report.append("|----------|----------|--------|---------------|-------------|")
        
        for model_hp, data in sorted(exp_results.items()):
            analysis = data.get('variance_analysis', {})
            largest_drops = analysis.get('largest_drops', [])
            if largest_drops:
                drop = largest_drops[0]  # Largest
                model_short = model_hp[:50] + "..." if len(model_hp) > 50 else model_hp
                report.append(f"| {model_short} | {drop['to_subjects']} | {drop['percentage_drop']:.2f}% | {drop['from_variance']:.4f} | {drop['to_variance']:.4f} |")
        report.append("")
    
    # Inflection points
    report.append("## Inflection Points Analysis\n")
    inflection_by_subjects = defaultdict(list)
    for inf in aggregate_analysis['all_inflection_points']:
        inflection_by_subjects[inf['subjects']].append(inf)
    
    if inflection_by_subjects:
        report.append("### Most Common Inflection Points\n")
        report.append("| Subjects | Frequency |")
        report.append("|----------|-----------|")
        for subjects, infs in sorted(inflection_by_subjects.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            report.append(f"| {subjects} | {len(infs)} |")
        report.append("")
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"✅ Detailed report saved to: {output_file}")

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    all_analyses = {}
    
    print("🔬 Starting deep variance analysis...\n")
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"📊 Analyzing {exp_name}...")
        
        model_hp_fold_accuracies = load_fold_accuracies(exp_name, results_dir)
        if not model_hp_fold_accuracies:
            continue
        
        exp_results = {}
        for model_hp_key, fold_accuracies in sorted(model_hp_fold_accuracies.items()):
            print(f"   Processing: {model_hp_key[:50]}...")
            
            # Extract model name from model_hp_key (format: "ModelName (params)")
            model_name = model_hp_key.split(' (')[0]
            
            # Get results directory structure
            results_path = results_dir / "ml_results_grid_search"
            if not results_path.exists():
                results_path = results_dir
            
            # Pre-load subject accuracies cache (much faster than reading parquet repeatedly)
            subject_accuracies_cache = load_subject_accuracies_cache(results_path, model_name)
            
            if not subject_accuracies_cache:
                print(f"      ⚠️  No subject accuracies found, skipping")
                continue
            
            # Use individual accuracies method (NEW) with cache
            variance_data = calculate_variance_by_test_groups(
                fold_accuracies, 
                subject_accuracies_cache=subject_accuracies_cache,
                use_individual_accuracies=True
            )
            if not variance_data:
                continue
            
            variance_analysis = analyze_variance_drops(variance_data)
            exp_results[model_hp_key] = {
                'variance_data': variance_data,
                'variance_analysis': variance_analysis
            }
        
        all_analyses[exp_name] = exp_results
    
    # Aggregate analysis
    print("\n📈 Performing aggregate analysis...")
    aggregate_analysis = find_optimal_subject_count(all_analyses)
    
    # Create visualizations
    print("\n📊 Creating visualizations...")
    create_aggregate_visualization(aggregate_analysis, output_dir)
    
    # Generate report
    print("\n📝 Generating detailed report...")
    report_file = output_dir / "DEEP_VARIANCE_ANALYSIS_REPORT.md"
    generate_detailed_report(all_analyses, aggregate_analysis, report_file)
    
    print("\n✅ Deep analysis complete!")

if __name__ == "__main__":
    main()

