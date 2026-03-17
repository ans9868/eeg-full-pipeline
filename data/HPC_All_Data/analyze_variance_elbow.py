#!/usr/bin/env python
"""
Analyze variance elbow plots to determine optimal number of test subjects.

This script:
1. Calculates variance for each number of test groups
2. Identifies "elbow" points where variance drops significantly
3. Determines if there's a clear threshold where variance stabilizes
4. Generates a summary report
"""

import json
import math
import random
from pathlib import Path
from collections import defaultdict
import itertools
import statistics
import re

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_6_complete",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

# Computational limits
MAX_COMBINATIONS = 10000
MAX_TEST_GROUPS = 15

# Elbow detection parameters
VARIANCE_DROP_THRESHOLD = 0.1  # 10% drop to consider significant
STABILITY_THRESHOLD = 0.05  # 5% change to consider stable

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
    
    # First pass: collect all fold names
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        for fold_dir in model_dir.iterdir():
            if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
                all_fold_names.add(fold_dir.name)
    
    # Second pass: collect accuracies
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

def calculate_variance_for_combination(fold_names, fold_accuracies):
    """Calculate variance of accuracies for a specific combination of folds."""
    accs = []
    for fold_name in fold_names:
        if fold_name in fold_accuracies:
            accs.append(fold_accuracies[fold_name])
        else:
            return None
    if len(accs) < 2:
        return 0.0
    return statistics.variance(accs)

def calculate_variance_by_test_groups(fold_accuracies):
    """Calculate variance statistics for each number of test groups."""
    fold_names = list(fold_accuracies.keys())
    total_folds = len(fold_names)
    if total_folds == 0:
        return {}
    
    subjects_per_group = count_subjects_in_fold(fold_names[0])
    results = {}
    max_groups = min(MAX_TEST_GROUPS, total_folds)
    
    for num_groups in range(1, max_groups + 1):
        total_combinations = math.comb(total_folds, num_groups)
        if total_combinations > MAX_COMBINATIONS:
            combinations_to_use = min(MAX_COMBINATIONS, total_combinations)
            sampled_combos = set()
            while len(sampled_combos) < combinations_to_use:
                combo = tuple(sorted(random.sample(fold_names, num_groups)))
                sampled_combos.add(combo)
            combinations = list(sampled_combos)
        else:
            combinations = list(itertools.combinations(fold_names, num_groups))
        
        variances = []
        for combo in combinations:
            var = calculate_variance_for_combination(combo, fold_accuracies)
            if var is not None:
                variances.append(var)
        
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

def detect_elbow_point(variance_data):
    """
    Detect elbow point where variance stabilizes.
    
    Returns:
        {
            'elbow_detected': bool,
            'elbow_point': int (number of groups),
            'elbow_subjects': int (number of subjects),
            'variance_at_elbow': float,
            'variance_reduction': float (percentage),
            'stability_point': int (where variance becomes stable),
            'stable_subjects': int
        }
    """
    if len(variance_data) < 3:
        return {
            'elbow_detected': False,
            'reason': 'Insufficient data points'
        }
    
    num_groups_list = sorted(variance_data.keys())
    variances = [variance_data[n]['mean_variance'] for n in num_groups_list]
    
    # Find maximum variance (usually at start)
    max_var = max(variances)
    max_var_idx = variances.index(max_var)
    
    # Calculate relative drops
    drops = []
    for i in range(max_var_idx + 1, len(variances)):
        if variances[i-1] > 0:
            drop_pct = (variances[i-1] - variances[i]) / variances[i-1]
            drops.append((i, drop_pct, num_groups_list[i], variance_data[num_groups_list[i]]['subjects_included']))
    
    # Find first significant drop (>10%)
    elbow_idx = None
    for idx, drop_pct, ng, subj in drops:
        if drop_pct >= VARIANCE_DROP_THRESHOLD:
            elbow_idx = idx
            elbow_groups = ng
            elbow_subjects = subj
            variance_at_elbow = variances[idx]
            variance_reduction = drop_pct * 100
            break
    
    # If no significant drop found, check for gradual stabilization
    if elbow_idx is None:
        # Look for point where variance changes become small (<5%)
        stability_idx = None
        for i in range(1, len(variances)):
            if variances[i-1] > 0:
                change_pct = abs(variances[i] - variances[i-1]) / variances[i-1]
                if change_pct < STABILITY_THRESHOLD:
                    # Check if subsequent points are also stable
                    stable_count = 0
                    for j in range(i, min(i+3, len(variances))):
                        if variances[j-1] > 0:
                            chg = abs(variances[j] - variances[j-1]) / variances[j-1]
                            if chg < STABILITY_THRESHOLD:
                                stable_count += 1
                    if stable_count >= 2:  # At least 2 consecutive stable points
                        stability_idx = i
                        break
        
        if stability_idx:
            return {
                'elbow_detected': False,
                'stability_detected': True,
                'stability_point': num_groups_list[stability_idx],
                'stable_subjects': variance_data[num_groups_list[stability_idx]]['subjects_included'],
                'variance_at_stability': variances[stability_idx],
                'reason': 'Gradual stabilization detected'
            }
        else:
            return {
                'elbow_detected': False,
                'stability_detected': False,
                'reason': 'No clear elbow or stability point'
            }
    
    # Check if variance stabilizes after elbow
    stability_idx = None
    for i in range(elbow_idx + 1, len(variances)):
        if variances[i-1] > 0:
            change_pct = abs(variances[i] - variances[i-1]) / variances[i-1]
            if change_pct < STABILITY_THRESHOLD:
                stable_count = 0
                for j in range(i, min(i+3, len(variances))):
                    if j < len(variances) and variances[j-1] > 0:
                        chg = abs(variances[j] - variances[j-1]) / variances[j-1]
                        if chg < STABILITY_THRESHOLD:
                            stable_count += 1
                if stable_count >= 2:
                    stability_idx = i
                    break
    
    result = {
        'elbow_detected': True,
        'elbow_point': elbow_groups,
        'elbow_subjects': elbow_subjects,
        'variance_at_elbow': variance_at_elbow,
        'variance_reduction': variance_reduction,
        'initial_variance': max_var,
        'final_variance': variances[-1],
        'total_reduction': ((max_var - variances[-1]) / max_var * 100) if max_var > 0 else 0
    }
    
    if stability_idx:
        result['stability_point'] = num_groups_list[stability_idx]
        result['stable_subjects'] = variance_data[num_groups_list[stability_idx]]['subjects_included']
        result['variance_at_stability'] = variances[stability_idx]
    
    return result

def analyze_experiment(exp_name, results_dir):
    """Analyze variance elbow for an experiment."""
    print(f"\n📊 Analyzing {exp_name}...")
    
    model_hp_fold_accuracies = load_fold_accuracies(exp_name, results_dir)
    if not model_hp_fold_accuracies:
        return {}
    
    results = {}
    
    for model_hp_key, fold_accuracies in sorted(model_hp_fold_accuracies.items()):
        variance_data = calculate_variance_by_test_groups(fold_accuracies)
        if not variance_data:
            continue
        
        elbow_analysis = detect_elbow_point(variance_data)
        results[model_hp_key] = {
            'variance_data': variance_data,
            'elbow_analysis': elbow_analysis
        }
    
    return results

def generate_summary_report(all_results, output_file):
    """Generate markdown summary report."""
    report = []
    report.append("# Variance Elbow Analysis: Optimal Number of Test Subjects\n")
    report.append("## Executive Summary\n")
    
    # Aggregate statistics
    elbow_detected_count = 0
    stability_detected_count = 0
    no_clear_pattern_count = 0
    all_elbow_subjects = []
    all_stable_subjects = []
    
    for exp_name, exp_results in all_results.items():
        for model_hp, data in exp_results.items():
            analysis = data['elbow_analysis']
            if analysis.get('elbow_detected'):
                elbow_detected_count += 1
                all_elbow_subjects.append(analysis['elbow_subjects'])
            elif analysis.get('stability_detected'):
                stability_detected_count += 1
                all_stable_subjects.append(analysis['stable_subjects'])
            else:
                no_clear_pattern_count += 1
    
    total_models = elbow_detected_count + stability_detected_count + no_clear_pattern_count
    
    report.append(f"- **Total Model×HP Combinations Analyzed**: {total_models}")
    report.append(f"- **Clear Elbow Detected**: {elbow_detected_count} ({elbow_detected_count/total_models*100:.1f}%)")
    report.append(f"- **Gradual Stabilization Detected**: {stability_detected_count} ({stability_detected_count/total_models*100:.1f}%)")
    report.append(f"- **No Clear Pattern**: {no_clear_pattern_count} ({no_clear_pattern_count/total_models*100:.1f}%)")
    report.append("")
    
    if all_elbow_subjects:
        report.append(f"- **Median Elbow Point**: {statistics.median(all_elbow_subjects)} subjects")
        report.append(f"- **Mean Elbow Point**: {statistics.mean(all_elbow_subjects):.1f} subjects")
        report.append(f"- **Elbow Range**: {min(all_elbow_subjects)} - {max(all_elbow_subjects)} subjects")
        report.append("")
    
    if all_stable_subjects:
        report.append(f"- **Median Stability Point**: {statistics.median(all_stable_subjects)} subjects")
        report.append(f"- **Mean Stability Point**: {statistics.mean(all_stable_subjects):.1f} subjects")
        report.append("")
    
    # Overall conclusion
    report.append("### Overall Conclusion\n")
    
    if all_elbow_subjects:
        median_elbow = statistics.median(all_elbow_subjects)
        report.append(f"**For models with clear elbow patterns ({elbow_detected_count} models):**")
        report.append(f"- **{int(median_elbow)} subjects appears to be sufficient** for stable variance estimates")
        report.append(f"- This represents the median elbow point across all model×HP combinations")
        report.append("")
    
    if all_stable_subjects and not all_elbow_subjects:
        median_stable = statistics.median(all_stable_subjects)
        report.append(f"**For models with gradual stabilization ({stability_detected_count} models):**")
        report.append(f"- **{int(median_stable)} subjects appears to be sufficient** for stable variance estimates")
        report.append("")
    
    if no_clear_pattern_count > total_models * 0.5:
        report.append("**⚠️ CAUTION:** More than 50% of models show no clear elbow or stability pattern.")
        report.append("This suggests that variance may not stabilize at a consistent number of subjects across different models.")
        report.append("")
    
    # Detailed results by experiment
    report.append("## Detailed Results by Experiment\n")
    
    for exp_name, exp_results in all_results.items():
        report.append(f"### {exp_name}\n")
        
        # Group by detection type
        elbow_models = []
        stability_models = []
        no_pattern_models = []
        
        for model_hp, data in exp_results.items():
            analysis = data['elbow_analysis']
            if analysis.get('elbow_detected'):
                elbow_models.append((model_hp, analysis))
            elif analysis.get('stability_detected'):
                stability_models.append((model_hp, analysis))
            else:
                no_pattern_models.append((model_hp, analysis))
        
        if elbow_models:
            report.append("#### Models with Clear Elbow\n")
            report.append("| Model×HP | Elbow Point (Groups) | Subjects | Variance Reduction |")
            report.append("|----------|----------------------|----------|-------------------|")
            for model_hp, analysis in elbow_models:
                report.append(f"| {model_hp[:60]}... | {analysis['elbow_point']} | {analysis['elbow_subjects']} | {analysis['variance_reduction']:.1f}% |")
            report.append("")
        
        if stability_models:
            report.append("#### Models with Gradual Stabilization\n")
            report.append("| Model×HP | Stability Point (Groups) | Subjects |")
            report.append("|----------|--------------------------|----------|")
            for model_hp, analysis in stability_models:
                report.append(f"| {model_hp[:60]}... | {analysis['stability_point']} | {analysis['stable_subjects']} |")
            report.append("")
        
        if no_pattern_models:
            report.append(f"#### Models with No Clear Pattern ({len(no_pattern_models)} models)\n")
            for model_hp, analysis in no_pattern_models:
                report.append(f"- {model_hp}: {analysis.get('reason', 'No pattern detected')}")
            report.append("")
    
    # Write report
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"✅ Summary report saved to: {output_file}")

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    all_results = {}
    
    for exp_name, results_dir in EXPERIMENTS.items():
        results = analyze_experiment(exp_name, results_dir)
        if results:
            all_results[exp_name] = results
    
    # Generate summary report
    report_file = output_dir / "VARIANCE_ELBOW_ANALYSIS_REPORT.md"
    generate_summary_report(all_results, report_file)
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()







