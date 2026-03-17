#!/usr/bin/env python
"""
Analyze variance of classification success rates (>50% accuracy) across test group combinations.

For each combination of test groups:
1. For each subject, determine if accuracy > 50% (binary: 1 if yes, 0 if no)
2. Calculate mean: avg(group1.subjects.above50percent + group2.subjects.above50percent + ...)
3. This gives the proportion of subjects correctly classified
4. Calculate variance of these proportions across all combinations

This shows how stable the classification success rate is as we include more test groups.
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

MAX_TEST_GROUPS = 15
RANDOM_SAMPLE_SIZE = 30
CLASSIFICATION_THRESHOLD = 0.50  # 50% accuracy threshold

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

def load_subject_accuracies_cache(results_dir, model_name):
    """
    Pre-load all subject accuracies for a model.
    
    Returns: {fold_name: {subject_id: accuracy}}
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
        subject_accuracies = {}
        
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
                    subject_id = f"sub-{int(subject_id_num)}"
                    subject_data = test_df[test_df['SubjectID'] == subject_id_num]
                    
                    # Calculate accuracy: (label == prediction).sum() / len(subject_data)
                    correct = (subject_data['label'] == subject_data['prediction']).sum()
                    total = len(subject_data)
                    accuracy = correct / total if total > 0 else 0.0
                    
                    # Store accuracy for this subject (may appear in multiple tasks, take first or average)
                    if subject_id not in subject_accuracies:
                        subject_accuracies[subject_id] = accuracy
                    else:
                        # Average if subject appears in multiple tasks
                        subject_accuracies[subject_id] = (subject_accuracies[subject_id] + accuracy) / 2
            except Exception as e:
                continue
        
        if subject_accuracies:
            cache[fold_name] = subject_accuracies
            fold_count += 1
    
    print(f" loaded {fold_count} folds")
    return cache

def calculate_success_rate_for_combination(fold_names, subject_accuracies_cache):
    """
    Calculate classification success rate for a combination of folds.
    
    Returns: proportion of subjects with accuracy > 50%
    """
    all_subject_success = []  # List of 1s and 0s
    
    for fold_name in fold_names:
        if fold_name in subject_accuracies_cache:
            for subject_id, accuracy in subject_accuracies_cache[fold_name].items():
                # Binary: 1 if accuracy > 50%, 0 otherwise
                success = 1 if accuracy > CLASSIFICATION_THRESHOLD else 0
                all_subject_success.append(success)
    
    if len(all_subject_success) == 0:
        return None
    
    # Calculate mean: proportion of subjects correctly classified
    success_rate = statistics.mean(all_subject_success)
    return success_rate

def calculate_success_rate_variance_by_test_groups(subject_accuracies_cache, fold_names):
    """
    Calculate variance of success rates for each number of test groups.
    """
    total_folds = len(fold_names)
    if total_folds == 0:
        return {}
    
    subjects_per_group = count_subjects_in_fold(fold_names[0]) if fold_names else 0
    results = {}
    max_groups = min(MAX_TEST_GROUPS, total_folds)
    
    for num_groups in range(1, max_groups + 1):
        print(f"      Processing {num_groups} groups...", end='', flush=True)
        total_combinations = math.comb(total_folds, num_groups)
        
        # Always use random sampling for efficiency
        sample_size = min(RANDOM_SAMPLE_SIZE, total_combinations)
        sampled_combos = set()
        while len(sampled_combos) < sample_size:
            combo = tuple(sorted(random.sample(fold_names, num_groups)))
            sampled_combos.add(combo)
        combinations = list(sampled_combos)
        
        print(f" (sampling {len(combinations)}/{total_combinations} combinations)", end='', flush=True)
        
        success_rates = []
        for i, combo in enumerate(combinations):
            if (i + 1) % 10 == 0:
                print(f" {i+1}/{len(combinations)}", end='', flush=True)
            
            success_rate = calculate_success_rate_for_combination(combo, subject_accuracies_cache)
            if success_rate is not None:
                success_rates.append(success_rate)
        
        print(f" done ({len(success_rates)} valid)")
        
        if success_rates:
            mean_success_rate = statistics.mean(success_rates)
            variance_success_rate = statistics.variance(success_rates) if len(success_rates) > 1 else 0.0
            std_success_rate = statistics.stdev(success_rates) if len(success_rates) > 1 else 0.0
            results[num_groups] = {
                'mean_success_rate': mean_success_rate,
                'variance_success_rate': variance_success_rate,
                'std_success_rate': std_success_rate,
                'num_combinations': len(success_rates),
                'subjects_included': num_groups * subjects_per_group
            }
    
    return results

def analyze_success_rate_drops(variance_data):
    """Analyze success rate variance drops at each subject count."""
    if len(variance_data) < 2:
        return {}
    
    num_groups_list = sorted(variance_data.keys())
    subjects_list = [variance_data[n]['subjects_included'] for n in num_groups_list]
    variances = [variance_data[n]['variance_success_rate'] for n in num_groups_list]
    mean_rates = [variance_data[n]['mean_success_rate'] for n in num_groups_list]
    
    analysis = {
        'subjects': subjects_list,
        'variances': variances,
        'mean_success_rates': mean_rates,
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
                'percentage_drop': pct_drop,
                'mean_success_rate': mean_rates[i]
            })
    
    # Find largest drops
    if analysis['drop_points']:
        sorted_drops = sorted(analysis['drop_points'], 
                            key=lambda x: x['percentage_drop'], 
                            reverse=True)
        analysis['largest_drops'] = sorted_drops[:5]
    
    return analysis

def plot_success_rate_variance_elbow(exp_name, model_hp_key, variance_data, output_dir):
    """Create elbow plot showing variance of success rates vs number of test groups."""
    if not variance_data:
        return False
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    num_groups_list = sorted(variance_data.keys())
    variances = [variance_data[n]['variance_success_rate'] for n in num_groups_list]
    mean_rates = [variance_data[n]['mean_success_rate'] for n in num_groups_list]
    std_vars = [variance_data[n]['std_success_rate'] for n in num_groups_list]
    subjects_included = [variance_data[n]['subjects_included'] for n in num_groups_list]
    
    # Plot 1: Variance of success rates
    ax1.errorbar(num_groups_list, variances, yerr=std_vars,
                marker='o', linestyle='-', linewidth=2, markersize=6,
                capsize=5, capthick=2, elinewidth=1.5,
                color='#2E86AB', label='Variance ± Std')
    
    ax1.set_xlabel('Number of Test Groups', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Variance of Success Rate', fontsize=12, fontweight='bold')
    ax1.set_title(f'{exp_name}\nVariance of Classification Success Rate (>50%): {model_hp_key[:60]}...',
                 fontsize=13, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Mean success rate
    ax2.plot(num_groups_list, mean_rates,
            marker='s', linestyle='-', linewidth=2, markersize=6,
            color='#A23B72', label='Mean Success Rate')
    ax2.axhline(y=0.5, color='red', linestyle='--', linewidth=1.5, 
               label='50% Threshold', alpha=0.7)
    
    ax2.set_xlabel('Number of Test Groups', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Mean Success Rate (Proportion >50%)', fontsize=12, fontweight='bold')
    ax2.set_title('Mean Classification Success Rate Across Combinations',
                 fontsize=13, fontweight='bold', pad=15)
    ax2.set_ylim(0, 1.05)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Annotate with subjects included
    for i, (ng, si) in enumerate(zip(num_groups_list, subjects_included)):
        if i == 0 or i == len(num_groups_list) - 1 or i % 3 == 0:
            ax1.annotate(f'{si} subj', 
                       xy=(ng, variances[i]), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, alpha=0.7)
    
    plt.tight_layout()
    
    # Sanitize filename
    safe_model_hp = re.sub(r'[^\w\s-]', '_', model_hp_key)
    safe_model_hp = re.sub(r'_+', '_', safe_model_hp).strip('_')
    output_file = output_dir / f'{exp_name}_success_rate_variance_{safe_model_hp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def generate_success_rate_report(all_results, output_file):
    """Generate markdown report for success rate variance analysis."""
    report = []
    report.append("# Classification Success Rate Variance Analysis\n")
    report.append("## Methods\n")
    report.append("### Calculation Method\n")
    report.append("For each combination of test groups:\n")
    report.append("1. For each subject in the selected groups, determine if accuracy > 50% (binary: 1 if yes, 0 if no)\n")
    report.append("2. Calculate mean: `avg(group1.subjects.above50percent + group2.subjects.above50percent + ...)`\n")
    report.append("3. This gives the **proportion of subjects correctly classified** (>50% accuracy)\n")
    report.append("4. Calculate variance of these proportions across all combinations\n")
    report.append("\n**Key Difference**: This analyzes variance in **classification success rate**, not variance in accuracy values.\n")
    report.append("\n### Sampling Strategy\n")
    report.append(f"- **30 random combinations** sampled per number of groups (instead of all possible combinations)\n")
    report.append(f"- **Classification Threshold**: 50% accuracy\n")
    report.append(f"- **Maximum Test Groups**: {MAX_TEST_GROUPS}\n")
    report.append("\n### Data Source\n")
    report.append("- Individual subject accuracies from `test_predictions.parquet` files\n")
    report.append("- Per-subject accuracy calculated as: `(label == prediction).sum() / total_epochs`\n")
    report.append("\n## Executive Summary\n")
    
    # Aggregate statistics
    all_variances = []
    all_mean_rates = []
    
    for exp_name, exp_results in all_results.items():
        for model_hp, data in exp_results.items():
            variance_data = data.get('variance_data', {})
            for ng, stats in variance_data.items():
                all_variances.append(stats['variance_success_rate'])
                all_mean_rates.append(stats['mean_success_rate'])
    
    if all_variances:
        report.append(f"- **Total Data Points**: {len(all_variances)}\n")
        report.append(f"- **Mean Variance**: {statistics.mean(all_variances):.4f}\n")
        report.append(f"- **Median Variance**: {statistics.median(all_variances):.4f}\n")
        report.append(f"- **Mean Success Rate**: {statistics.mean(all_mean_rates):.2%}\n")
        report.append(f"- **Median Success Rate**: {statistics.median(all_mean_rates):.2%}\n")
        report.append("")
    
    # Per-experiment analysis
    report.append("## Per-Experiment Analysis\n")
    
    for exp_name, exp_results in all_results.items():
        report.append(f"### {exp_name}\n")
        
        for model_hp, data in sorted(exp_results.items()):
            variance_data = data.get('variance_data', {})
            analysis = data.get('analysis', {})
            
            if not variance_data:
                continue
            
            report.append(f"#### {model_hp[:70]}...\n")
            report.append("| Groups | Subjects | Mean Success Rate | Variance | Std Dev |")
            report.append("|--------|----------|-------------------|----------|---------|")
            
            for ng in sorted(variance_data.keys()):
                stats = variance_data[ng]
                report.append(f"| {ng} | {stats['subjects_included']} | {stats['mean_success_rate']:.2%} | {stats['variance_success_rate']:.4f} | {stats['std_success_rate']:.4f} |")
            
            # Show largest drops
            largest_drops = analysis.get('largest_drops', [])
            if largest_drops:
                report.append("\n**Largest Variance Drops:**\n")
                for drop in largest_drops[:3]:
                    report.append(f"- {drop['to_subjects']} subjects: {drop['percentage_drop']:.1f}% drop (success rate: {drop['mean_success_rate']:.2%})\n")
            
            report.append("")
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"✅ Success rate report saved to: {output_file}")

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    all_results = {}
    
    print("🔬 Starting classification success rate variance analysis...\n")
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"📊 Analyzing {exp_name}...")
        
        # Get results directory structure
        results_path = results_dir / "ml_results_grid_search"
        if not results_path.exists():
            results_path = results_dir
        
        # Get all fold names from any model directory
        fold_names = set()
        for model_dir in results_path.iterdir():
            if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
                continue
            for fold_dir in model_dir.iterdir():
                if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
                    fold_names.add(fold_dir.name)
        
        fold_names = sorted(list(fold_names))
        print(f"   Found {len(fold_names)} folds")
        
        # Process each model
        exp_results = {}
        model_dirs = [d for d in results_path.iterdir() 
                     if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
        
        for model_dir in sorted(model_dirs):
            model_name = model_dir.name
            
            # Extract model×HP key (we'll need to get hyperparams from a sample file)
            sample_fold = None
            for fold_dir in model_dir.iterdir():
                if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
                    sample_fold = fold_dir
                    break
            
            if not sample_fold:
                continue
            
            # Get hyperparams from a sample results.json
            results_files = list(sample_fold.rglob("results.json"))
            if not results_files:
                task_dirs = [d for d in sample_fold.iterdir() if d.is_dir() and d.name.startswith('task_')]
                for task_dir in task_dirs:
                    results_file = task_dir / "results.json"
                    if results_file.exists():
                        results_files.append(results_file)
                        break
            
            if not results_files:
                continue
            
            try:
                with open(results_files[0], 'r') as f:
                    data = json.load(f)
                hyperparams = data.get('hyperparams', {})
                model_hp_key = format_model_hp_label(model_name, hyperparams)
            except:
                model_hp_key = model_name
            
            print(f"   Processing: {model_hp_key[:50]}...")
            
            # Load subject accuracies cache
            subject_accuracies_cache = load_subject_accuracies_cache(results_path, model_name)
            
            if not subject_accuracies_cache:
                print(f"      ⚠️  No subject accuracies found, skipping")
                continue
            
            # Calculate success rate variance
            variance_data = calculate_success_rate_variance_by_test_groups(
                subject_accuracies_cache, fold_names
            )
            
            if not variance_data:
                continue
            
            # Analyze drops
            analysis = analyze_success_rate_drops(variance_data)
            
            # Create plot
            plot_success_rate_variance_elbow(exp_name, model_hp_key, variance_data, output_dir)
            
            exp_results[model_hp_key] = {
                'variance_data': variance_data,
                'analysis': analysis
            }
        
        all_results[exp_name] = exp_results
    
    # Generate report
    print("\n📝 Generating report...")
    report_file = output_dir / "CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md"
    generate_success_rate_report(all_results, report_file)
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()







