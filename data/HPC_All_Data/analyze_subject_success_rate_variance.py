#!/usr/bin/env python
"""
Analyze variance of per-subject success rates (>50% accuracy) as we add more folds.

For a specific model×HP combination:
1. For each subject, calculate % of folds where accuracy > 50%
2. Calculate variance of these percentages across all subjects
3. See how variance changes as we include more folds
"""

import pandas as pd
from pathlib import Path
from collections import defaultdict
import json
import random
import math
import statistics
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

CLASSIFICATION_THRESHOLD = 0.50
RANDOM_SAMPLE_SIZE = 30
MAX_FOLDS = 50

def format_model_hp_label(model_name, hyperparams):
    """Format model×hyperparameter label."""
    if hyperparams:
        sorted_keys = sorted(hyperparams.keys())
        param_str = ", ".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
        return f"{model_name} ({param_str})"
    else:
        return f"{model_name} (default)"

def load_all_subject_accuracies(results_dir, model_name):
    """
    Load all subject accuracies for a model across all folds.
    
    Returns: {fold_name: {subject_id: accuracy}}
    """
    cache = {}
    model_dir = results_dir / model_name
    if not model_dir.exists():
        return cache
    
    for fold_dir in model_dir.iterdir():
        if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
            continue
        
        fold_name = fold_dir.name
        subject_accuracies = {}
        
        task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
        
        for task_dir in task_dirs:
            test_parquet = task_dir / "test_predictions.parquet"
            if not test_parquet.exists():
                continue
            
            try:
                test_df = pd.read_parquet(test_parquet)
                
                for subject_id_num in test_df['SubjectID'].unique():
                    subject_id = f"sub-{int(subject_id_num)}"
                    subject_data = test_df[test_df['SubjectID'] == subject_id_num]
                    
                    correct = (subject_data['label'] == subject_data['prediction']).sum()
                    total = len(subject_data)
                    accuracy = correct / total if total > 0 else 0.0
                    
                    if subject_id not in subject_accuracies:
                        subject_accuracies[subject_id] = accuracy
                    else:
                        subject_accuracies[subject_id] = (subject_accuracies[subject_id] + accuracy) / 2
            except Exception as e:
                continue
        
        if subject_accuracies:
            cache[fold_name] = subject_accuracies
    
    return cache

def calculate_subject_success_rates(subject_accuracies_cache, fold_names):
    """
    For each subject, calculate the percentage of folds where accuracy > 50%.
    
    Returns: {subject_id: success_rate_percentage}
    """
    subject_fold_counts = defaultdict(lambda: {'total': 0, 'above_50': 0})
    
    for fold_name in fold_names:
        if fold_name in subject_accuracies_cache:
            for subject_id, accuracy in subject_accuracies_cache[fold_name].items():
                subject_fold_counts[subject_id]['total'] += 1
                if accuracy > CLASSIFICATION_THRESHOLD:
                    subject_fold_counts[subject_id]['above_50'] += 1
    
    # Calculate success rate percentage for each subject
    subject_success_rates = {}
    for subject_id, counts in subject_fold_counts.items():
        if counts['total'] > 0:
            success_rate = counts['above_50'] / counts['total']
            subject_success_rates[subject_id] = success_rate
    
    return subject_success_rates

def calculate_variance_by_num_folds(subject_accuracies_cache, all_fold_names):
    """
    Calculate variance of subject success rates as we progressively add more folds.
    
    Returns: {num_folds: {'variance': float, 'mean': float, 'std': float}}
    """
    results = {}
    
    # Randomly sample different numbers of folds
    max_folds_to_test = min(MAX_FOLDS, len(all_fold_names))
    
    for num_folds in range(1, max_folds_to_test + 1):
        # Sample multiple times for each number of folds to get variance estimate
        variances = []
        means = []
        
        for _ in range(RANDOM_SAMPLE_SIZE):
            # Randomly sample num_folds folds
            sampled_folds = random.sample(all_fold_names, min(num_folds, len(all_fold_names)))
            
            # Calculate subject success rates for this sample
            subject_success_rates = calculate_subject_success_rates(subject_accuracies_cache, sampled_folds)
            
            if len(subject_success_rates) > 1:
                success_rate_values = list(subject_success_rates.values())
                variance = statistics.variance(success_rate_values) if len(success_rate_values) > 1 else 0.0
                mean_rate = statistics.mean(success_rate_values)
                
                variances.append(variance)
                means.append(mean_rate)
        
        if variances:
            results[num_folds] = {
                'mean_variance': statistics.mean(variances),
                'std_variance': statistics.stdev(variances) if len(variances) > 1 else 0.0,
                'mean_success_rate': statistics.mean(means),
                'num_subjects': len(subject_success_rates) if subject_success_rates else 0
            }
    
    return results

def plot_variance_by_folds(results, exp_name, model_hp_key, output_dir):
    """Plot variance of subject success rates vs number of folds."""
    if not results:
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Variance vs Number of Folds
    num_folds = sorted(results.keys())
    mean_variances = [results[n]['mean_variance'] for n in num_folds]
    std_variances = [results[n]['std_variance'] for n in num_folds]
    
    ax1.plot(num_folds, mean_variances, marker='o', linewidth=2, markersize=4, color='steelblue')
    ax1.fill_between(num_folds, 
                     [m - s for m, s in zip(mean_variances, std_variances)],
                     [m + s for m, s in zip(mean_variances, std_variances)],
                     alpha=0.2, color='steelblue')
    
    ax1.set_xlabel('Number of Folds Included', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Variance of Subject Success Rates', fontweight='bold', fontsize=12)
    ax1.set_title('Variance of Per-Subject Success Rates vs Number of Folds', 
                  fontweight='bold', fontsize=13)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, max(num_folds) + 1)
    
    # Plot 2: Mean Success Rate vs Number of Folds
    mean_rates = [results[n]['mean_success_rate'] for n in num_folds]
    
    ax2.plot(num_folds, mean_rates, marker='s', linewidth=2, markersize=4, color='coral')
    ax2.set_xlabel('Number of Folds Included', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Mean Subject Success Rate', fontweight='bold', fontsize=12)
    ax2.set_title('Mean Per-Subject Success Rate vs Number of Folds', 
                  fontweight='bold', fontsize=13)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.05)
    ax2.set_xlim(0, max(num_folds) + 1)
    ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='50% threshold')
    ax2.legend()
    
    plt.suptitle(f'{exp_name}: {model_hp_key[:70]}...', 
                fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # Sanitize filename
    safe_exp = exp_name.replace(' ', '_').replace('/', '_')
    safe_model_hp = model_hp_key.replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')
    safe_model_hp = ''.join(c for c in safe_model_hp if c.isalnum() or c in ('_', '-', '='))[:100]
    output_file = output_dir / f'{safe_exp}_subject_success_rate_variance_{safe_model_hp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved plot: {output_file.name}")

def generate_report(results, exp_name, model_hp_key, output_dir):
    """Generate markdown report."""
    if not results:
        return
    
    report = []
    report.append(f"# Per-Subject Success Rate Variance Analysis\n")
    report.append(f"## Experiment: {exp_name}\n")
    report.append(f"## Model×Hyperparameters: {model_hp_key}\n")
    report.append("\n## Methods\n")
    report.append("This analysis examines how the variance of per-subject success rates (>50% accuracy) ")
    report.append("changes as we include more folds in the analysis.\n\n")
    report.append("**Methodology:**\n")
    report.append("1. For each subject, calculate the percentage of folds where that subject's accuracy > 50%\n")
    report.append("2. Calculate the variance of these percentages across all subjects\n")
    report.append("3. Repeat for different numbers of folds (1 to N folds)\n")
    report.append("4. For each number of folds, sample 30 random combinations to estimate variance\n\n")
    report.append("**Key Metrics:**\n")
    report.append("- **Variance**: How much subjects differ in their success rates\n")
    report.append("- **Mean Success Rate**: Average percentage of folds where subjects exceed 50% accuracy\n\n")
    
    report.append("## Results\n\n")
    report.append("| Number of Folds | Mean Variance | Std Dev of Variance | Mean Success Rate |\n")
    report.append("|----------------|---------------|---------------------|-------------------|\n")
    
    for num_folds in sorted(results.keys()):
        stats = results[num_folds]
        report.append(f"| {num_folds} | {stats['mean_variance']:.4f} | "
                     f"{stats['std_variance']:.4f} | {stats['mean_success_rate']:.2%} |\n")
    
    report.append("\n## Interpretation\n\n")
    
    # Find where variance stabilizes
    num_folds_list = sorted(results.keys())
    if len(num_folds_list) > 5:
        recent_variances = [results[n]['mean_variance'] for n in num_folds_list[-5:]]
        if len(recent_variances) > 1:
            variance_change = abs(recent_variances[-1] - recent_variances[0])
            if variance_change < 0.01:
                report.append(f"**Variance Stabilization**: Variance appears to stabilize after ~{num_folds_list[-5]} folds ")
                report.append(f"(change < 0.01 in last 5 data points).\n\n")
    
    # Find minimum variance
    min_variance_folds = min(num_folds_list, key=lambda n: results[n]['mean_variance'])
    min_variance = results[min_variance_folds]['mean_variance']
    report.append(f"**Minimum Variance**: {min_variance:.4f} at {min_variance_folds} folds.\n\n")
    
    # Final statistics
    final_stats = results[num_folds_list[-1]]
    report.append(f"**Final Statistics** (with all {num_folds_list[-1]} folds):\n")
    report.append(f"- Mean Variance: {final_stats['mean_variance']:.4f}\n")
    report.append(f"- Mean Success Rate: {final_stats['mean_success_rate']:.2%}\n")
    
    # Sanitize filename
    safe_exp = exp_name.replace(' ', '_').replace('/', '_')
    safe_model_hp = model_hp_key.replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')
    safe_model_hp = ''.join(c for c in safe_model_hp if c.isalnum() or c in ('_', '-', '='))[:100]
    output_file = output_dir / f'{safe_exp}_subject_success_rate_variance_{safe_model_hp}.md'
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"   ✅ Saved report: {output_file.name}")

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    print("🔬 Starting per-subject success rate variance analysis...\n")
    
    # Process all experiments
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"📊 Processing {exp_name}...")
        
        results_path = results_dir / "ml_results_grid_search"
        if not results_path.exists():
            results_path = results_dir
        
        # Get all fold names
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
        model_dirs = [d for d in results_path.iterdir() 
                     if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
        
        for model_dir in sorted(model_dirs):
            model_name = model_dir.name
            
            # Get hyperparams
            sample_fold = None
            for fold_dir in model_dir.iterdir():
                if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
                    sample_fold = fold_dir
                    break
            
            if not sample_fold:
                continue
            
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
            
            print(f"   Processing: {model_hp_key[:60]}...")
            
            # Load subject accuracies
            subject_accuracies_cache = load_all_subject_accuracies(results_path, model_name)
            
            if not subject_accuracies_cache:
                print(f"      ⚠️  No subject accuracies found")
                continue
            
            # Calculate variance by number of folds
            variance_results = calculate_variance_by_num_folds(subject_accuracies_cache, fold_names)
            
            if variance_results:
                # Create plot
                plot_variance_by_folds(variance_results, exp_name, model_hp_key, output_dir)
                
                # Generate report
                generate_report(variance_results, exp_name, model_hp_key, output_dir)
            else:
                print(f"      ⚠️  No variance results calculated")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()







