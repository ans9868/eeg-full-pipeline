#!/usr/bin/env python
"""
Plot variance elbow curves showing how variance changes as more test groups are included.

For each model×hyperparameter combination:
- X-axis: Number of test groups (1, 2, 3, ...)
- Y-axis: Mean variance of accuracies (with error bars showing ±std)
- For each number of groups, calculates variance across all possible combinations
- Shows "elbow" pattern as variance stabilizes with more groups
"""

import json
import math
import random
from pathlib import Path
from collections import defaultdict
import itertools
import statistics
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import re

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_6_complete",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

# Computational limits
MAX_COMBINATIONS = 10000  # Maximum combinations to calculate before sampling
MAX_TEST_GROUPS = 15  # Maximum number of test groups to analyze

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
    """
    Load accuracy for each fold×model×HP combination.
    
    Returns:
        {model_hp_key: {fold_name: accuracy}}
    """
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {model_hp_key: {fold_name: accuracy}}
    model_hp_fold_accuracies = defaultdict(dict)
    
    # First pass: collect all fold names
    all_fold_names = set()
    
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
            
            # Find results.json
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
                        
                        # Create model×HP key
                        model_hp_key = format_model_hp_label(model_name, hyperparams)
                        
                        # Store fold accuracy
                        model_hp_fold_accuracies[model_hp_key][fold_name] = acc
                except Exception as e:
                    continue
    
    return model_hp_fold_accuracies

def calculate_variance_for_combination(fold_names, fold_accuracies):
    """
    Calculate variance of accuracies for a specific combination of folds.
    
    Args:
        fold_names: List of fold names in this combination
        fold_accuracies: Dict mapping fold_name -> accuracy
    
    Returns:
        Variance of accuracies (or None if any fold missing)
    """
    accs = []
    for fold_name in fold_names:
        if fold_name in fold_accuracies:
            accs.append(fold_accuracies[fold_name])
        else:
            return None  # Missing data
    
    if len(accs) < 2:
        return 0.0  # No variance with < 2 values
    
    return statistics.variance(accs)

def calculate_variance_by_test_groups(fold_accuracies):
    """
    Calculate variance statistics for each number of test groups.
    
    Args:
        fold_accuracies: Dict mapping fold_name -> accuracy
    
    Returns:
        {
            num_groups: {
                'mean_variance': float,
                'std_variance': float,
                'num_combinations': int,
                'sampled': bool
            }
        }
    """
    fold_names = list(fold_accuracies.keys())
    total_folds = len(fold_names)
    
    if total_folds == 0:
        return {}
    
    # Determine subjects per group from first fold
    subjects_per_group = count_subjects_in_fold(fold_names[0])
    
    results = {}
    max_groups = min(MAX_TEST_GROUPS, total_folds)
    
    for num_groups in range(1, max_groups + 1):
        # Calculate number of combinations
        total_combinations = math.comb(total_folds, num_groups)
        
        # Determine if we need to sample
        if total_combinations > MAX_COMBINATIONS:
            # Sample combinations
            combinations_to_use = min(MAX_COMBINATIONS, total_combinations)
            sampled = True
            
            # Generate random sample of combinations
            # Use a set to ensure uniqueness
            sampled_combos = set()
            while len(sampled_combos) < combinations_to_use:
                combo = tuple(sorted(random.sample(fold_names, num_groups)))
                sampled_combos.add(combo)
            
            combinations = list(sampled_combos)
        else:
            # Use all combinations
            combinations = list(itertools.combinations(fold_names, num_groups))
            sampled = False
        
        # Calculate variance for each combination
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
                'total_combinations': total_combinations,
                'sampled': sampled,
                'subjects_included': num_groups * subjects_per_group
            }
    
    return results

def sanitize_filename(text):
    """Sanitize text for use in filenames."""
    # Replace problematic characters
    text = text.replace('(', '_').replace(')', '_')
    text = text.replace('[', '_').replace(']', '_')
    text = text.replace(',', '_').replace(' ', '_')
    text = text.replace('=', '_').replace('/', '_')
    # Remove multiple underscores
    text = re.sub(r'_+', '_', text)
    # Remove leading/trailing underscores
    text = text.strip('_')
    return text

def plot_variance_elbow(exp_name, model_hp_key, variance_data, output_dir):
    """Create elbow plot showing variance vs number of test groups."""
    if not variance_data:
        return False
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    num_groups_list = sorted(variance_data.keys())
    mean_vars = [variance_data[n]['mean_variance'] for n in num_groups_list]
    std_vars = [variance_data[n]['std_variance'] for n in num_groups_list]
    subjects_included = [variance_data[n]['subjects_included'] for n in num_groups_list]
    
    # Plot line with error bars
    ax.errorbar(num_groups_list, mean_vars, yerr=std_vars, 
                marker='o', linestyle='-', linewidth=2, markersize=6,
                capsize=5, capthick=2, elinewidth=1.5,
                label='Mean Variance ± Std')
    
    # Annotate with subjects included
    for i, (ng, si) in enumerate(zip(num_groups_list, subjects_included)):
        if i % 2 == 0 or i == len(num_groups_list) - 1:  # Annotate every other point or last
            ax.annotate(f'{si} subjects', 
                       xy=(ng, mean_vars[i]), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, alpha=0.7)
    
    ax.set_xlabel('Number of Test Groups', fontsize=13, fontweight='bold')
    ax.set_ylabel('Variance of Accuracies', fontsize=13, fontweight='bold')
    
    # Truncate title if too long
    title = f'{exp_name}\nVariance Elbow: {model_hp_key}'
    if len(title) > 100:
        title = f'{exp_name}\nVariance Elbow: {model_hp_key[:80]}...'
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    # Add note about sampling if applicable
    sampled_any = any(variance_data[n]['sampled'] for n in num_groups_list)
    if sampled_any:
        ax.text(0.02, 0.98, 
               f'Note: Some combinations were sampled (max {MAX_COMBINATIONS})',
               transform=ax.transAxes, fontsize=9, 
               verticalalignment='top', alpha=0.7,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Sanitize filename
    safe_model_hp = sanitize_filename(model_hp_key)
    output_file = output_dir / f'{exp_name}_variance_by_test_groups_{safe_model_hp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        # Load fold accuracies
        model_hp_fold_accuracies = load_fold_accuracies(exp_name, results_dir)
        
        if not model_hp_fold_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found {len(model_hp_fold_accuracies)} model×HP combinations")
        
        # Process each model×HP combination
        for model_hp_key, fold_accuracies in sorted(model_hp_fold_accuracies.items()):
            print(f"   Processing: {model_hp_key[:60]}...")
            
            # Calculate variance statistics
            variance_data = calculate_variance_by_test_groups(fold_accuracies)
            
            if not variance_data:
                print(f"      ⚠️  No variance data calculated")
                continue
            
            # Create plot
            plot_variance_elbow(exp_name, model_hp_key, variance_data, output_dir)
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

