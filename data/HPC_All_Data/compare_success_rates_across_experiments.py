#!/usr/bin/env python
"""
Compare classification success rates across all 4 experiments:
- ANOVA_L_2_Random vs ANOVA_L_6_Random
- PCA_L_2_Random vs PCA_L_6_Random
- ANOVA vs PCA (for same L value)
- L=2 vs L=6 (for same transformation)

For the same model×HP combination to ensure fair comparison.
"""

import pandas as pd
from pathlib import Path
from collections import defaultdict
import json
import random
import math
import statistics
import re
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
MAX_TEST_GROUPS = 15

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

def load_all_subject_accuracies(results_dir, model_name):
    """Load all subject accuracies for a model across all folds."""
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

def calculate_success_rate_for_combination(fold_names, subject_accuracies_cache):
    """Calculate success rate for a combination of folds."""
    all_subject_success = []
    
    for fold_name in fold_names:
        if fold_name in subject_accuracies_cache:
            for subject_id, accuracy in subject_accuracies_cache[fold_name].items():
                success = 1 if accuracy > CLASSIFICATION_THRESHOLD else 0
                all_subject_success.append(success)
    
    if len(all_subject_success) == 0:
        return None
    
    return statistics.mean(all_subject_success)

def calculate_success_rate_by_groups(subject_accuracies_cache, fold_names):
    """Calculate success rate statistics for each number of test groups."""
    total_folds = len(fold_names)
    if total_folds == 0:
        return {}
    
    subjects_per_group = count_subjects_in_fold(fold_names[0]) if fold_names else 0
    results = {}
    max_groups = min(MAX_TEST_GROUPS, total_folds)
    
    for num_groups in range(1, max_groups + 1):
        total_combinations = math.comb(total_folds, num_groups)
        sample_size = min(RANDOM_SAMPLE_SIZE, total_combinations)
        
        sampled_combos = set()
        while len(sampled_combos) < sample_size:
            combo = tuple(sorted(random.sample(fold_names, num_groups)))
            sampled_combos.add(combo)
        combinations = list(sampled_combos)
        
        success_rates = []
        for combo in combinations:
            success_rate = calculate_success_rate_for_combination(combo, subject_accuracies_cache)
            if success_rate is not None:
                success_rates.append(success_rate)
        
        if success_rates:
            results[num_groups] = {
                'mean_success_rate': statistics.mean(success_rates),
                'std_success_rate': statistics.stdev(success_rates) if len(success_rates) > 1 else 0.0,
                'subjects_included': num_groups * subjects_per_group
            }
    
    return results

def extract_model_type(model_hp_key):
    """Extract model type from model×HP key (e.g., 'KNN', 'MLP', 'SVM', 'XGBoost')."""
    if model_hp_key.startswith('KNN'):
        return 'KNN'
    elif model_hp_key.startswith('MLP'):
        return 'MLP'
    elif model_hp_key.startswith('SVM'):
        return 'SVM'
    elif model_hp_key.startswith('XGBoost'):
        return 'XGBoost'
    return None

def normalize_hyperparams(hyperparams):
    """Normalize hyperparameters for comparison (sort keys, handle lists)."""
    if not hyperparams:
        return {}
    normalized = {}
    for k, v in sorted(hyperparams.items()):
        if isinstance(v, list):
            normalized[k] = tuple(sorted(v))
        else:
            normalized[k] = v
    return normalized

def extract_hyperparams_from_key(model_hp_key):
    """Extract hyperparameters dict from model×HP key string."""
    # Parse string like "KNN (metric=euclidean, n_neighbors=7, weights=uniform)"
    # or "MLP (activation=tanh, alpha=0.1, hidden_layer_sizes=[150, 50])"
    match = re.search(r'\((.+)\)', model_hp_key)
    if not match:
        return {}
    
    params_str = match.group(1)
    hyperparams = {}
    
    # Handle lists in the string (e.g., "[150, 50]")
    # Split by commas, but be careful with lists
    i = 0
    current_key = None
    current_value = ""
    in_list = False
    
    while i < len(params_str):
        char = params_str[i]
        
        if char == '[':
            in_list = True
            current_value += char
        elif char == ']':
            in_list = False
            current_value += char
        elif char == '=' and not in_list:
            # End of key, start of value
            if current_key:
                # Save previous key-value pair
                if current_value:
                    v = parse_value(current_value.strip())
                    hyperparams[current_key.strip()] = v
            current_key = current_value
            current_value = ""
        elif char == ',' and not in_list:
            # End of current parameter
            if current_key and current_value:
                v = parse_value(current_value.strip())
                hyperparams[current_key.strip()] = v
            current_key = None
            current_value = ""
        else:
            current_value += char
        
        i += 1
    
    # Handle last parameter
    if current_key and current_value:
        v = parse_value(current_value.strip())
        hyperparams[current_key.strip()] = v
    
    return normalize_hyperparams(hyperparams)

def parse_value(v_str):
    """Parse a value string into appropriate Python type."""
    v_str = v_str.strip()
    
    # Handle lists
    if v_str.startswith('[') and v_str.endswith(']'):
        list_str = v_str[1:-1]
        items = [parse_value(item.strip()) for item in list_str.split(',') if item.strip()]
        return items
    
    # Try to convert to appropriate type
    try:
        if v_str.isdigit():
            return int(v_str)
        elif '.' in v_str and v_str.replace('.', '').replace('-', '').isdigit():
            return float(v_str)
        elif v_str.lower() == 'true':
            return True
        elif v_str.lower() == 'false':
            return False
    except:
        pass
    
    return v_str

def find_exact_matching_hyperparams(all_experiment_data):
    """Find model×HP combinations with EXACT same hyperparameters across all 4 experiments."""
    # Group by model type first
    models_by_type = defaultdict(lambda: defaultdict(list))
    
    for exp_name, exp_data in all_experiment_data.items():
        for model_hp_key, info in exp_data.items():
            model_type = extract_model_type(model_hp_key)
            if model_type:
                # Use stored hyperparams dict instead of parsing from string
                hyperparams = info.get('hyperparams', {})
                models_by_type[model_type][exp_name].append({
                    'model_hp_key': model_hp_key,
                    'hyperparams': hyperparams,
                    'data': info.get('data', {}),
                    'model_name': info.get('model_name', '')
                })
    
    # Find exact matches
    exact_matches = []
    hyperparam_variations = defaultdict(lambda: defaultdict(list))
    
    for model_type, exp_models in models_by_type.items():
        if len(exp_models) != 4:  # Not in all 4 experiments
            continue
        
        # Get all unique hyperparameter sets for this model type
        all_hp_sets = set()
        for exp_name, models in exp_models.items():
            for model_info in models:
                hp_tuple = tuple(sorted(model_info['hyperparams'].items()))
                all_hp_sets.add(hp_tuple)
        
        # Check if any hyperparameter set appears in all 4 experiments
        for hp_tuple in all_hp_sets:
            hp_dict = dict(hp_tuple)
            matching_exps = []
            matching_keys = {}
            
            for exp_name, models in exp_models.items():
                for model_info in models:
                    model_hp_dict = model_info['hyperparams']
                    if normalize_hyperparams(model_hp_dict) == normalize_hyperparams(hp_dict):
                        matching_exps.append(exp_name)
                        matching_keys[exp_name] = model_info['model_hp_key']
                        break
            
            if len(matching_exps) == 4:
                # Exact match across all 4 experiments!
                exact_matches.append({
                    'model_type': model_type,
                    'hyperparams': hp_dict,
                    'model_hp_keys': matching_keys,
                    'data': {exp: all_experiment_data[exp][matching_keys[exp]]['data'] 
                            for exp in matching_exps}
                })
            else:
                # Record variation
                for exp_name in matching_exps:
                    if exp_name not in hyperparam_variations[model_type]:
                        hyperparam_variations[model_type][exp_name] = []
                    # Avoid duplicates
                    existing = [v['hyperparams'] for v in hyperparam_variations[model_type][exp_name]]
                    if hp_dict not in existing:
                        hyperparam_variations[model_type][exp_name].append({
                            'hyperparams': hp_dict,
                            'model_hp_key': matching_keys[exp_name]
                        })
    
    return exact_matches, hyperparam_variations

def plot_comparison(all_experiment_data, model_hp_key, output_dir):
    """Create comparison plots across all 4 experiments."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: ANOVA L=2 vs L=6
    ax1 = axes[0, 0]
    if "ANOVA_L_2_Random" in all_experiment_data and model_hp_key in all_experiment_data["ANOVA_L_2_Random"]:
        data_l2 = all_experiment_data["ANOVA_L_2_Random"][model_hp_key]
        groups_l2 = sorted(data_l2.keys())
        rates_l2 = [data_l2[g]['mean_success_rate'] for g in groups_l2]
        subjects_l2 = [data_l2[g]['subjects_included'] for g in groups_l2]
        ax1.plot(subjects_l2, rates_l2, marker='o', label='ANOVA L=2', linewidth=2, markersize=6)
    
    if "ANOVA_L_6_Random" in all_experiment_data and model_hp_key in all_experiment_data["ANOVA_L_6_Random"]:
        data_l6 = all_experiment_data["ANOVA_L_6_Random"][model_hp_key]
        groups_l6 = sorted(data_l6.keys())
        rates_l6 = [data_l6[g]['mean_success_rate'] for g in groups_l6]
        subjects_l6 = [data_l6[g]['subjects_included'] for g in groups_l6]
        ax1.plot(subjects_l6, rates_l6, marker='s', label='ANOVA L=6', linewidth=2, markersize=6)
    
    ax1.set_xlabel('Number of Subjects', fontweight='bold')
    ax1.set_ylabel('Success Rate (Proportion >50%)', fontweight='bold')
    ax1.set_title('ANOVA: L=2 vs L=6', fontweight='bold', fontsize=13)
    ax1.set_ylim(0, 1.05)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
    
    # Plot 2: PCA L=2 vs L=6
    ax2 = axes[0, 1]
    if "PCA_L_2_Random" in all_experiment_data and model_hp_key in all_experiment_data["PCA_L_2_Random"]:
        data_l2 = all_experiment_data["PCA_L_2_Random"][model_hp_key]
        groups_l2 = sorted(data_l2.keys())
        rates_l2 = [data_l2[g]['mean_success_rate'] for g in groups_l2]
        subjects_l2 = [data_l2[g]['subjects_included'] for g in groups_l2]
        ax2.plot(subjects_l2, rates_l2, marker='o', label='PCA L=2', linewidth=2, markersize=6)
    
    if "PCA_L_6_Random" in all_experiment_data and model_hp_key in all_experiment_data["PCA_L_6_Random"]:
        data_l6 = all_experiment_data["PCA_L_6_Random"][model_hp_key]
        groups_l6 = sorted(data_l6.keys())
        rates_l6 = [data_l6[g]['mean_success_rate'] for g in groups_l6]
        subjects_l6 = [data_l6[g]['subjects_included'] for g in groups_l6]
        ax2.plot(subjects_l6, rates_l6, marker='s', label='PCA L=6', linewidth=2, markersize=6)
    
    ax2.set_xlabel('Number of Subjects', fontweight='bold')
    ax2.set_ylabel('Success Rate (Proportion >50%)', fontweight='bold')
    ax2.set_title('PCA: L=2 vs L=6', fontweight='bold', fontsize=13)
    ax2.set_ylim(0, 1.05)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
    
    # Plot 3: L=2: ANOVA vs PCA
    ax3 = axes[1, 0]
    if "ANOVA_L_2_Random" in all_experiment_data and model_hp_key in all_experiment_data["ANOVA_L_2_Random"]:
        data_anova = all_experiment_data["ANOVA_L_2_Random"][model_hp_key]
        groups = sorted(data_anova.keys())
        rates = [data_anova[g]['mean_success_rate'] for g in groups]
        subjects = [data_anova[g]['subjects_included'] for g in groups]
        ax3.plot(subjects, rates, marker='o', label='ANOVA', linewidth=2, markersize=6)
    
    if "PCA_L_2_Random" in all_experiment_data and model_hp_key in all_experiment_data["PCA_L_2_Random"]:
        data_pca = all_experiment_data["PCA_L_2_Random"][model_hp_key]
        groups = sorted(data_pca.keys())
        rates = [data_pca[g]['mean_success_rate'] for g in groups]
        subjects = [data_pca[g]['subjects_included'] for g in groups]
        ax3.plot(subjects, rates, marker='s', label='PCA', linewidth=2, markersize=6)
    
    ax3.set_xlabel('Number of Subjects', fontweight='bold')
    ax3.set_ylabel('Success Rate (Proportion >50%)', fontweight='bold')
    ax3.set_title('L=2: ANOVA vs PCA', fontweight='bold', fontsize=13)
    ax3.set_ylim(0, 1.05)
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    ax3.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
    
    # Plot 4: L=6: ANOVA vs PCA
    ax4 = axes[1, 1]
    if "ANOVA_L_6_Random" in all_experiment_data and model_hp_key in all_experiment_data["ANOVA_L_6_Random"]:
        data_anova = all_experiment_data["ANOVA_L_6_Random"][model_hp_key]
        groups = sorted(data_anova.keys())
        rates = [data_anova[g]['mean_success_rate'] for g in groups]
        subjects = [data_anova[g]['subjects_included'] for g in groups]
        ax4.plot(subjects, rates, marker='o', label='ANOVA', linewidth=2, markersize=6)
    
    if "PCA_L_6_Random" in all_experiment_data and model_hp_key in all_experiment_data["PCA_L_6_Random"]:
        data_pca = all_experiment_data["PCA_L_6_Random"][model_hp_key]
        groups = sorted(data_pca.keys())
        rates = [data_pca[g]['mean_success_rate'] for g in groups]
        subjects = [data_pca[g]['subjects_included'] for g in groups]
        ax4.plot(subjects, rates, marker='s', label='PCA', linewidth=2, markersize=6)
    
    ax4.set_xlabel('Number of Subjects', fontweight='bold')
    ax4.set_ylabel('Success Rate (Proportion >50%)', fontweight='bold')
    ax4.set_title('L=6: ANOVA vs PCA', fontweight='bold', fontsize=13)
    ax4.set_ylim(0, 1.05)
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    ax4.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
    
    plt.suptitle(f'Success Rate Comparison: {model_hp_key[:60]}...', 
                fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    # Sanitize filename
    safe_model_hp = re.sub(r'[^\w\s-]', '_', model_hp_key)
    safe_model_hp = re.sub(r'_+', '_', safe_model_hp).strip('_')
    output_file = output_dir / f'SUCCESS_RATE_COMPARISON_{safe_model_hp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved comparison plot: {output_file.name}")

def generate_comparison_report(all_experiment_data, model_hp_key, output_file):
    """Generate comparison report."""
    import re
    
    report = []
    report.append("# Classification Success Rate Comparison Across Experiments\n")
    report.append("## Methods\n")
    report.append("This analysis compares classification success rates (>50% accuracy) across 4 experiments:\n")
    report.append("- **ANOVA_L_2_Random**: ANOVA transformation, 2 subjects per test group\n")
    report.append("- **ANOVA_L_6_Random**: ANOVA transformation, 6 subjects per test group\n")
    report.append("- **PCA_L_2_Random**: PCA transformation, 2 subjects per test group\n")
    report.append("- **PCA_L_6_Random**: PCA transformation, 6 subjects per test group\n")
    report.append("\n**Model Analyzed**: " + model_hp_key + "\n")
    report.append("\n## Comparison Tables\n")
    
    # Table 1: All 4 experiments side by side
    report.append("### Success Rates by Number of Subjects (All Experiments)\n")
    report.append("| Subjects | ANOVA L=2 | ANOVA L=6 | PCA L=2 | PCA L=6 |")
    report.append("|---------|-----------|-----------|---------|---------|")
    
    # Get all subject counts
    all_subject_counts = set()
    for exp_name, exp_data in all_experiment_data.items():
        if model_hp_key in exp_data:
            for ng, stats in exp_data[model_hp_key].items():
                all_subject_counts.add(stats['subjects_included'])
    
    for subjects in sorted(all_subject_counts):
        row = [str(subjects)]
        for exp_name in ["ANOVA_L_2_Random", "ANOVA_L_6_Random", "PCA_L_2_Random", "PCA_L_6_Random"]:
            if exp_name in all_experiment_data and model_hp_key in all_experiment_data[exp_name]:
                data = all_experiment_data[exp_name][model_hp_key]
                # Find group with this subject count
                found = False
                for ng, stats in data.items():
                    if stats['subjects_included'] == subjects:
                        row.append(f"{stats['mean_success_rate']:.1%}")
                        found = True
                        break
                if not found:
                    row.append("-")
            else:
                row.append("-")
        report.append("|".join(row))
    
    report.append("\n## Key Comparisons\n")
    
    # ANOVA L=2 vs L=6
    if "ANOVA_L_2_Random" in all_experiment_data and "ANOVA_L_6_Random" in all_experiment_data:
        if model_hp_key in all_experiment_data["ANOVA_L_2_Random"] and model_hp_key in all_experiment_data["ANOVA_L_6_Random"]:
            data_l2 = all_experiment_data["ANOVA_L_2_Random"][model_hp_key]
            data_l6 = all_experiment_data["ANOVA_L_6_Random"][model_hp_key]
            
            # Compare at similar subject counts
            report.append("### ANOVA: L=2 vs L=6\n")
            report.append("| Subjects | L=2 Success Rate | L=6 Success Rate | Difference |")
            report.append("|----------|------------------|------------------|------------|")
            
            # Compare at 6, 12, 18, 24 subjects (multiples that work for both)
            for target_subjects in [6, 12, 18, 24, 30]:
                l2_rate = None
                l6_rate = None
                
                for ng, stats in data_l2.items():
                    if stats['subjects_included'] == target_subjects:
                        l2_rate = stats['mean_success_rate']
                        break
                
                for ng, stats in data_l6.items():
                    if stats['subjects_included'] == target_subjects:
                        l6_rate = stats['mean_success_rate']
                        break
                
                if l2_rate is not None and l6_rate is not None:
                    diff = l6_rate - l2_rate
                    report.append(f"| {target_subjects} | {l2_rate:.1%} | {l6_rate:.1%} | {diff:+.1%} |")
    
    # PCA L=2 vs L=6
    if "PCA_L_2_Random" in all_experiment_data and "PCA_L_6_Random" in all_experiment_data:
        if model_hp_key in all_experiment_data["PCA_L_2_Random"] and model_hp_key in all_experiment_data["PCA_L_6_Random"]:
            data_l2 = all_experiment_data["PCA_L_2_Random"][model_hp_key]
            data_l6 = all_experiment_data["PCA_L_6_Random"][model_hp_key]
            
            report.append("\n### PCA: L=2 vs L=6\n")
            report.append("| Subjects | L=2 Success Rate | L=6 Success Rate | Difference |")
            report.append("|----------|------------------|------------------|------------|")
            
            for target_subjects in [6, 12, 18, 24, 30]:
                l2_rate = None
                l6_rate = None
                
                for ng, stats in data_l2.items():
                    if stats['subjects_included'] == target_subjects:
                        l2_rate = stats['mean_success_rate']
                        break
                
                for ng, stats in data_l6.items():
                    if stats['subjects_included'] == target_subjects:
                        l6_rate = stats['mean_success_rate']
                        break
                
                if l2_rate is not None and l6_rate is not None:
                    diff = l6_rate - l2_rate
                    report.append(f"| {target_subjects} | {l2_rate:.1%} | {l6_rate:.1%} | {diff:+.1%} |")
    
    # ANOVA vs PCA for L=2
    if "ANOVA_L_2_Random" in all_experiment_data and "PCA_L_2_Random" in all_experiment_data:
        if model_hp_key in all_experiment_data["ANOVA_L_2_Random"] and model_hp_key in all_experiment_data["PCA_L_2_Random"]:
            data_anova = all_experiment_data["ANOVA_L_2_Random"][model_hp_key]
            data_pca = all_experiment_data["PCA_L_2_Random"][model_hp_key]
            
            report.append("\n### L=2: ANOVA vs PCA\n")
            report.append("| Subjects | ANOVA Success Rate | PCA Success Rate | Difference |")
            report.append("|----------|---------------------|------------------|------------|")
            
            for target_subjects in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
                anova_rate = None
                pca_rate = None
                
                for ng, stats in data_anova.items():
                    if stats['subjects_included'] == target_subjects:
                        anova_rate = stats['mean_success_rate']
                        break
                
                for ng, stats in data_pca.items():
                    if stats['subjects_included'] == target_subjects:
                        pca_rate = stats['mean_success_rate']
                        break
                
                if anova_rate is not None and pca_rate is not None:
                    diff = pca_rate - anova_rate
                    report.append(f"| {target_subjects} | {anova_rate:.1%} | {pca_rate:.1%} | {diff:+.1%} |")
    
    # ANOVA vs PCA for L=6
    if "ANOVA_L_6_Random" in all_experiment_data and "PCA_L_6_Random" in all_experiment_data:
        if model_hp_key in all_experiment_data["ANOVA_L_6_Random"] and model_hp_key in all_experiment_data["PCA_L_6_Random"]:
            data_anova = all_experiment_data["ANOVA_L_6_Random"][model_hp_key]
            data_pca = all_experiment_data["PCA_L_6_Random"][model_hp_key]
            
            report.append("\n### L=6: ANOVA vs PCA\n")
            report.append("| Subjects | ANOVA Success Rate | PCA Success Rate | Difference |")
            report.append("|----------|---------------------|------------------|------------|")
            
            for target_subjects in [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]:
                anova_rate = None
                pca_rate = None
                
                for ng, stats in data_anova.items():
                    if stats['subjects_included'] == target_subjects:
                        anova_rate = stats['mean_success_rate']
                        break
                
                for ng, stats in data_pca.items():
                    if stats['subjects_included'] == target_subjects:
                        pca_rate = stats['mean_success_rate']
                        break
                
                if anova_rate is not None and pca_rate is not None:
                    diff = pca_rate - anova_rate
                    report.append(f"| {target_subjects} | {anova_rate:.1%} | {pca_rate:.1%} | {diff:+.1%} |")
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"✅ Comparison report saved to: {output_file}")

def main():
    """Main function."""
    import re
    
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    print("🔬 Starting cross-experiment comparison...\n")
    
    all_experiment_data = {}
    
    # Process all experiments
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"📊 Processing {exp_name}...")
        
        results_path = results_dir / "ml_results_grid_search"
        if not results_path.exists():
            results_path = results_dir
        
        # Get fold names
        fold_names = set()
        for model_dir in results_path.iterdir():
            if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
                continue
            for fold_dir in model_dir.iterdir():
                if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
                    fold_names.add(fold_dir.name)
        
        fold_names = sorted(list(fold_names))
        
        # Process each model
        exp_results = {}
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
                hyperparams = {}
                model_hp_key = model_name
            
            print(f"   Processing: {model_hp_key[:50]}...")
            
            # Load subject accuracies
            subject_accuracies_cache = load_all_subject_accuracies(results_path, model_name)
            
            if not subject_accuracies_cache:
                continue
            
            # Calculate success rates
            success_rate_data = calculate_success_rate_by_groups(subject_accuracies_cache, fold_names)
            
            if success_rate_data:
                # Store both the string key and the actual hyperparams dict
                exp_results[model_hp_key] = {
                    'data': success_rate_data,
                    'hyperparams': normalize_hyperparams(hyperparams),
                    'model_name': model_name
                }
        
        all_experiment_data[exp_name] = exp_results
    
    # Find exact matching hyperparameters across all experiments
    exact_matches, hyperparam_variations = find_exact_matching_hyperparams(all_experiment_data)
    
    if not exact_matches:
        print("\n⚠️  No model×HP combinations with EXACT same hyperparameters found across all 4 experiments")
        print("\n📋 Hyperparameter variations by model type:")
        
        # Generate variation report
        variation_report = []
        variation_report.append("# Hyperparameter Variations Across Experiments\n")
        variation_report.append("## Summary\n")
        variation_report.append("No model×HP combinations with identical hyperparameters were found across all 4 experiments.\n")
        variation_report.append("Below are the hyperparameters found for each model type in each experiment:\n\n")
        
        for model_type, exp_variations in hyperparam_variations.items():
            variation_report.append(f"## {model_type}\n\n")
            
            # Create a comparison table
            variation_report.append("| Experiment | Hyperparameters |\n")
            variation_report.append("|------------|----------------|\n")
            
            for exp_name in ["ANOVA_L_2_Random", "ANOVA_L_6_Random", "PCA_L_2_Random", "PCA_L_6_Random"]:
                if exp_name in exp_variations and exp_variations[exp_name]:
                    var = exp_variations[exp_name][0]  # Take first variation
                    hp_str = ", ".join([f"{k}={v}" for k, v in sorted(var['hyperparams'].items())])
                    variation_report.append(f"| {exp_name} | {hp_str} |\n")
                else:
                    variation_report.append(f"| {exp_name} | *Not found* |\n")
            
            variation_report.append("\n")
        
        variation_file = output_dir / "HYPERPARAMETER_VARIATIONS.md"
        with open(variation_file, 'w') as f:
            f.write('\n'.join(variation_report))
        
        print(f"   📝 Detailed variations saved to: {variation_file.name}")
        
        # Also print summary
        for model_type, exp_variations in hyperparam_variations.items():
            print(f"\n   {model_type}:")
            for exp_name, variations in exp_variations.items():
                print(f"      {exp_name}: {len(variations)} unique hyperparameter combination(s)")
        
        return
    
    print(f"\n✅ Found {len(exact_matches)} model×HP combination(s) with identical hyperparameters across all 4 experiments")
    
    # Create comparison for each exact match
    for match in exact_matches:
        model_type = match['model_type']
        model_hp_key = match['model_hp_keys'][list(match['model_hp_keys'].keys())[0]]  # Use first one as label
        
        print(f"\n📊 Creating comparison for {model_type}...")
        print(f"   Hyperparameters: {', '.join([f'{k}={v}' for k, v in sorted(match['hyperparams'].items())])}")
        
        # Create comparison plot
        plot_comparison(match['data'], model_hp_key, output_dir)
        
        # Generate report
        report_file = output_dir / f"SUCCESS_RATE_COMPARISON_{model_type}_{re.sub(r'[^\w\s-]', '_', str(match['hyperparams']))[:50]}.md"
        generate_comparison_report(match['data'], model_hp_key, report_file)
    
    print("\n✅ Comparison complete!")

if __name__ == "__main__":
    main()

