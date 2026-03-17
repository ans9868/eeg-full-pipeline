#!/usr/bin/env python
"""
Improved Per-Subject Accuracy Analysis by Model × Hyperparameter

Features:
- Fixed naming consistency (n_neighbors, learning_rate, etc.)
- Fold comparability checking
- Minimum evidence filter (N Folds >= 3)
- 95% CIs and binomial SE
- Scale check (Swing = max-min)
- CSV exports
- Proper experiment labeling (uniform vs random)
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics
import re
import csv
import math

try:
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not available - skipping visualizations")

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_6_Random": {
        "path": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
        "description": "ANOVA P=6 (50 random folds)",
        "type": "random"
    },
    "ANOVA_L_2_Random": {
        "path": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
        "description": "ANOVA P=2 (50 random folds)",
        "type": "random"
    },
    "PCA_L_6_Random": {
        "path": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
        "description": "PCA P=6 (50 random folds)",
        "type": "random"
    },
    "PCA_L_2_Random": {
        "path": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
        "description": "PCA P=2 (50 random folds)",
        "type": "random"
    },
    "ANOVA_L_6_Uniform": {
        "path": BASE_DIR / "grid_12_folds/ANOVA_L_6_C_Resource_Boosted",
        "description": "ANOVA P=6 (12 uniform folds)",
        "type": "uniform"
    },
    "PCA_L_6_Uniform": {
        "path": BASE_DIR / "grid_12_folds/PCA_L_6_C-3",
        "description": "PCA P=6 (12 uniform folds)",
        "type": "uniform"
    },
}

def extract_subject_ids_from_fold(fold_dir_name):
    """Extract subject IDs from fold directory name."""
    pattern = r'sub-(\d+)'
    matches = re.findall(pattern, fold_dir_name)
    return [f"sub-{m}" for m in matches]

def normalize_hyperparam_string(hyperparam_str):
    """Normalize hyperparameter string for consistent naming."""
    # Fix common typos
    replacements = {
        "n, neighbors": "n_neighbors",
        "learning, rate": "learning_rate",
        "max, depth": "max_depth",
        "n, estimators": "n_estimators",
        "hidden, layer, sizes": "hidden_layer_sizes",
    }
    
    for old, new in replacements.items():
        hyperparam_str = hyperparam_str.replace(old, new)
    
    return hyperparam_str

def format_model_label(model_name, hyperparams):
    """Format model label consistently."""
    if 'MLP' in model_name or 'Neural' in model_name:
        activation = hyperparams.get('activation', 'unknown')
        alpha = hyperparams.get('alpha', 'unknown')
        hidden = hyperparams.get('hidden_layer_sizes', hyperparams.get('hidden, layer, sizes', []))
        if isinstance(hidden, list):
            hidden_str = str(hidden)
        else:
            hidden_str = str(hidden)
        return f"MLP (activation={activation}, alpha={alpha}, hidden={hidden_str})"
    
    elif 'SVM' in model_name:
        kernel = hyperparams.get('kernel', 'unknown')
        C = hyperparams.get('C', 'unknown')
        gamma = hyperparams.get('gamma', 'unknown')
        return f"SVM (kernel={kernel}, C={C}, gamma={gamma})"
    
    elif 'XGBoost' in model_name:
        lr = hyperparams.get('learning_rate', hyperparams.get('learning, rate', 'unknown'))
        depth = hyperparams.get('max_depth', hyperparams.get('max, depth', 'unknown'))
        n_est = hyperparams.get('n_estimators', hyperparams.get('n, estimators', 'unknown'))
        return f"XGBoost (learning_rate={lr}, max_depth={depth}, n_estimators={n_est})"
    
    elif 'KNN' in model_name:
        n_neigh = hyperparams.get('n_neighbors', hyperparams.get('n, neighbors', 'unknown'))
        metric = hyperparams.get('metric', 'unknown')
        weights = hyperparams.get('weights', 'unknown')
        return f"KNN (n_neighbors={n_neigh}, metric={metric}, weights={weights})"
    
    return model_name

def extract_hyperparams(results_file):
    """Extract hyperparameters from results.json file."""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        hyperparams = data.get('hyperparams', {})
        return hyperparams
    except:
        return {}

def binomial_se(n, p):
    """Calculate binomial standard error."""
    if n == 0:
        return 0
    return math.sqrt(p * (1 - p) / n)

def calculate_ci(acc, n, confidence=0.95):
    """Calculate 95% confidence interval using binomial approximation."""
    if n < 2:
        return None, None, "CI unavailable"
    
    se = binomial_se(n, acc)
    z = 1.96  # 95% CI
    lower = max(0, acc - z * se)
    upper = min(1, acc + z * se)
    return lower, upper, f"[{lower:.3f}, {upper:.3f}]"

def extract_per_subject_accuracies_by_model_hyperparam(results_dir):
    """Extract per-subject accuracies broken down by model × hyperparameter."""
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {model_name: {hyperparam_key: {subject_id: {fold_id: accuracy}}}}
    model_hyperparam_subject_fold_acc = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    
    model_dirs = [d for d in results_path.iterdir() 
                  if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        fold_dirs = [d for d in model_dir.iterdir() 
                     if d.is_dir() and d.name.startswith('sub-')]
        
        for fold_dir in fold_dirs:
            fold_name = fold_dir.name
            subject_ids = extract_subject_ids_from_fold(fold_name)
            
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
                        
                        # Create hyperparam key
                        if hyperparams:
                            sorted_keys = sorted(hyperparams.keys())
                            param_str = "_".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
                        else:
                            param_str = "default"
                        
                        # Store with fold_id for comparability checking
                        for subject_id in subject_ids:
                            model_hyperparam_subject_fold_acc[model_name][param_str][subject_id][fold_name] = acc
                except Exception as e:
                    continue
    
    return dict(model_hyperparam_subject_fold_acc)

def analyze_subject_stats_by_model_hyperparam(model_hyperparam_subject_fold_acc):
    """Calculate statistics with fold comparability checking."""
    subject_model_hyperparam_stats = defaultdict(lambda: defaultdict(dict))
    subject_all_accuracies = defaultdict(list)
    
    for model_name, hyperparam_dict in model_hyperparam_subject_fold_acc.items():
        for hyperparam_str, subject_fold_dict in hyperparam_dict.items():
            for subject_id, fold_acc_dict in subject_fold_dict.items():
                accuracies = list(fold_acc_dict.values())
                fold_ids = list(fold_acc_dict.keys())
                
                if accuracies:
                    n = len(accuracies)
                    mean_acc = statistics.mean(accuracies)
                    median_acc = statistics.median(accuracies)
                    min_acc = min(accuracies)
                    max_acc = max(accuracies)
                    swing = max_acc - min_acc  # Verified: max - min
                    std_acc = statistics.stdev(accuracies) if n > 1 else 0
                    
                    # Calculate CI
                    lower_ci, upper_ci, ci_str = calculate_ci(mean_acc, n)
                    se = binomial_se(n, mean_acc)
                    
                    stats = {
                        'mean': mean_acc,
                        'median': median_acc,
                        'min': min_acc,
                        'max': max_acc,
                        'swing': swing,
                        'std': std_acc,
                        'n_folds': n,
                        'fold_ids': fold_ids,
                        'ci_lower': lower_ci,
                        'ci_upper': upper_ci,
                        'ci_str': ci_str,
                        'se': se,
                        'hyperparam_str': hyperparam_str
                    }
                    
                    subject_model_hyperparam_stats[subject_id][model_name][hyperparam_str] = stats
                    subject_all_accuracies[subject_id].extend(accuracies)
    
    # Calculate cross-model-hyperparam swings with min/max model info
    subject_cross_swings = {}
    for subject_id, model_dict in subject_model_hyperparam_stats.items():
        # Find all model×hyperparam combinations and their means
        all_combos = []
        for model_name, hyperparam_dict in model_dict.items():
            for hyperparam_str, stats in hyperparam_dict.items():
                # Parse hyperparams for label
                hyperparams = {}
                if hyperparam_str != "default":
                    pairs = hyperparam_str.split('_')
                    for pair in pairs:
                        if '=' in pair:
                            k, v = pair.split('=', 1)
                            try:
                                if v.startswith('[') and v.endswith(']'):
                                    v = v.strip('[]')
                                    if v:
                                        v = [x.strip() for x in v.split(',')]
                                        try:
                                            v = [int(x) if x.isdigit() else float(x) if '.' in x else x for x in v]
                                        except:
                                            pass
                                    else:
                                        v = []
                                elif v.replace('.', '').replace('-', '').isdigit():
                                    v = float(v) if '.' in v else int(v)
                            except:
                                pass
                            hyperparams[k] = v
                
                model_label = format_model_label(model_name, hyperparams)
                all_combos.append({
                    'model': model_name,
                    'hyperparam_str': hyperparam_str,
                    'model_label': model_label,
                    'mean': stats['mean'],
                    'min': stats['min'],
                    'max': stats['max']
                })
        
        if all_combos:
            # Find min and max combinations
            min_combo = min(all_combos, key=lambda x: x['min'])
            max_combo = max(all_combos, key=lambda x: x['max'])
            
            all_accs = [c['mean'] for c in all_combos]
            
            subject_cross_swings[subject_id] = {
                'min': min_combo['min'],
                'max': max_combo['max'],
                'swing': max_combo['max'] - min_combo['min'],
                'mean': statistics.mean(all_accs),
                'n_combinations': len(all_combos),
                'min_model_label': min_combo['model_label'],
                'max_model_label': max_combo['model_label'],
                'min_model': min_combo['model'],
                'max_model': max_combo['model'],
                'min_hyperparam': min_combo['hyperparam_str'],
                'max_hyperparam': max_combo['hyperparam_str']
            }
    
    return dict(subject_model_hyperparam_stats), subject_cross_swings

def create_visualizations(subject_stats_by_exp, cross_swings_by_exp, output_dir):
    """Create the two requested plots."""
    if not HAS_MATPLOTLIB:
        print("   ⚠️  Skipping visualizations (matplotlib not available)")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Plot 1: Subject Instability Plot
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = {
        'ANOVA_L_2_Random': 'red',
        'PCA_L_2_Random': 'orange',
        'ANOVA_L_6_Random': 'blue',
        'PCA_L_6_Random': 'green',
        'ANOVA_L_6_Uniform': 'purple',
        'PCA_L_6_Uniform': 'brown'
    }
    
    all_subjects_swings = []
    for exp_name, cross_swings in cross_swings_by_exp.items():
        if not cross_swings:
            continue
        
        subjects = sorted(cross_swings.keys())
        swings = [cross_swings[s]['swing'] * 100 for s in subjects]
        
        x_pos = range(len(subjects))
        color = colors.get(exp_name, 'gray')
        ax.scatter(x_pos, swings, label=exp_name, alpha=0.6, s=50, color=color)
        
        all_subjects_swings.extend(swings)
    
    # Add dashed line at 30% swing
    ax.axhline(y=30, color='red', linestyle='--', linewidth=2, label='High-risk threshold (30%)')
    
    ax.set_xlabel('Subject (sorted by ID)', fontsize=12)
    ax.set_ylabel('Swing (%)', fontsize=12)
    ax.set_title('Subject Instability Plot\n(Accuracy Swing Across Model×Hyperparameter Combinations)', 
                 fontsize=14, fontweight='bold')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'subject_instability_plot.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: subject_instability_plot.png")
    
    # Plot 2: Per-subject Rank Stability (for worst subjects)
    # Find worst subjects across all experiments
    all_worst_subjects = []
    for exp_name, cross_swings in cross_swings_by_exp.items():
        if cross_swings:
            sorted_subjects = sorted(cross_swings.items(), key=lambda x: x[1]['swing'], reverse=True)
            for subject_id, stats in sorted_subjects[:3]:  # Top 3 worst per experiment
                all_worst_subjects.append((exp_name, subject_id, stats['swing']))
    
    # Get top 10 worst overall
    all_worst_subjects.sort(key=lambda x: x[2], reverse=True)
    worst_subjects = all_worst_subjects[:10]
    
    if worst_subjects:
        n_subjects = len(worst_subjects)
        fig, axes = plt.subplots(2, 5, figsize=(20, 8))
        axes = axes.flatten()
        
        for idx, (exp_name, subject_id, swing) in enumerate(worst_subjects):
            if idx >= len(axes):
                break
            
            ax = axes[idx]
            
            # Get model rankings for this subject
            if exp_name in subject_stats_by_exp:
                subject_stats = subject_stats_by_exp[exp_name].get('per_model_hyperparam', {}).get(subject_id, {})
                
                # Collect all model×hyperparam means
                model_means = []
                model_labels = []
                
                for model_name in sorted(subject_stats.keys()):
                    for hyperparam_str, stats in subject_stats[model_name].items():
                        if stats['n_folds'] >= 3:  # Only include if N >= 3
                            hyperparams = {}
                            for pair in hyperparam_str.split('_'):
                                if '=' in pair:
                                    k, v = pair.split('=', 1)
                                    hyperparams[k] = v
                            
                            label = format_model_label(model_name, hyperparams)
                            model_means.append(stats['mean'])
                            model_labels.append(label)
                
                if model_means:
                    # Rank models
                    sorted_indices = sorted(range(len(model_means)), key=lambda i: model_means[i], reverse=True)
                    ranks = [0] * len(model_means)
                    for rank, idx in enumerate(sorted_indices, 1):
                        ranks[idx] = rank
                    
                    ax.barh(range(len(model_means)), ranks, color='steelblue', alpha=0.7)
                    ax.set_yticks(range(len(model_means)))
                    ax.set_yticklabels([label[:30] + '...' if len(label) > 30 else label 
                                       for label in model_labels], fontsize=7)
                    ax.set_xlabel('Rank', fontsize=8)
                    ax.set_title(f'{subject_id}\n{exp_name}\nSwing: {swing*100:.1f}%', 
                               fontsize=9, fontweight='bold')
                    ax.invert_yaxis()
                    ax.grid(True, alpha=0.3, axis='x')
            
            if not model_means:
                ax.text(0.5, 0.5, 'Insufficient data\n(N < 3)', 
                       ha='center', va='center', transform=ax.transAxes)
        
        plt.suptitle('Per-Subject Rank Stability\n(Top 10 Worst Subjects by Swing)', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_dir / 'rank_stability_plot.png', dpi=300, bbox_inches='tight')
        print(f"   ✅ Saved: rank_stability_plot.png")

def main():
    """Main function."""
    print("=" * 80)
    print("IMPROVED PER-SUBJECT ACCURACY ANALYSIS BY MODEL × HYPERPARAMETER")
    print("=" * 80)
    
    all_results = {}
    all_cross_swings = {}
    
    for exp_name, exp_info in EXPERIMENTS.items():
        print(f"\n📊 Analyzing {exp_name} ({exp_info['description']})...")
        
        model_hyperparam_subject_fold_acc = extract_per_subject_accuracies_by_model_hyperparam(exp_info['path'])
        
        if model_hyperparam_subject_fold_acc:
            subject_stats, cross_swings = analyze_subject_stats_by_model_hyperparam(
                model_hyperparam_subject_fold_acc)
            
            all_results[exp_name] = {
                'per_model_hyperparam': subject_stats,
                'cross_model_swings': cross_swings,
                'experiment_info': exp_info
            }
            all_cross_swings[exp_name] = cross_swings
            
            if cross_swings:
                swings = [s['swing'] * 100 for s in cross_swings.values()]
                print(f"   ✅ Found {len(cross_swings)} subjects")
                print(f"      Mean cross-model swing: {statistics.mean(swings):.2f}%")
                print(f"      Largest swing: {max(swings):.2f}%")
        else:
            print(f"   ⚠️  No results found")
            all_results[exp_name] = {'per_model_hyperparam': {}, 'cross_model_swings': {}}
    
    # Create visualizations
    print("\n" + "=" * 80)
    print("CREATING VISUALIZATIONS")
    print("=" * 80)
    
    output_dir = BASE_DIR / "per_subject_analysis_improved"
    create_visualizations(all_results, all_cross_swings, output_dir)
    
    # Generate CSV files
    print("\n" + "=" * 80)
    print("GENERATING CSV FILES")
    print("=" * 80)
    
    # CSV 1: Main table (N Folds >= 3 only)
    csv_main = []
    csv_appendix = []
    
    for exp_name, exp_data in all_results.items():
        exp_info = exp_data.get('experiment_info', {})
        exp_type = exp_info.get('type', 'unknown')
        
        for subject_id, model_dict in exp_data.get('per_model_hyperparam', {}).items():
            for model_name, hyperparam_dict in model_dict.items():
                for hyperparam_str, stats in hyperparam_dict.items():
                    # Parse hyperparam string (format: "key1=value1_key2=value2" or "default")
                    hyperparams = {}
                    if hyperparam_str != "default":
                        # Split by underscore to get key=value pairs
                        pairs = hyperparam_str.split('_')
                        for pair in pairs:
                            if '=' in pair:
                                k, v = pair.split('=', 1)
                                k = k.strip()
                                v = v.strip()
                                # Try to convert to appropriate type
                                try:
                                    if v.startswith('[') and v.endswith(']'):
                                        # List value like "[100]" or "[200, 100, 50]"
                                        v = v.strip('[]')
                                        if v:
                                            v = [x.strip() for x in v.split(',')]
                                            # Try to convert list elements to numbers
                                            try:
                                                v = [int(x) if x.isdigit() else float(x) if '.' in x else x for x in v]
                                            except:
                                                pass
                                        else:
                                            v = []
                                    elif v.lower() in ['true', 'false']:
                                        v = v.lower() == 'true'
                                    elif v.replace('.', '').replace('-', '').isdigit():
                                        v = float(v) if '.' in v else int(v)
                                except:
                                    pass  # Keep as string
                                hyperparams[k] = v
                    
                    model_label = format_model_label(model_name, hyperparams)
                    
                    row = {
                        'Experiment': exp_name,
                        'Experiment_Type': exp_type,
                        'Subject': subject_id,
                        'Model': model_label,
                        'Mean_Accuracy': f"{stats['mean']:.4f}",
                        'Min_Accuracy': f"{stats['min']:.4f}",
                        'Max_Accuracy': f"{stats['max']:.4f}",
                        'Swing': f"{stats['swing']:.4f}",
                        'Std_Dev': f"{stats['std']:.4f}",
                        'N_Folds': stats['n_folds'],
                        'CI_95': stats['ci_str'],
                        'SE': f"{stats['se']:.4f}",
                        'Fold_IDs': ';'.join(stats['fold_ids'])
                    }
                    
                    if stats['n_folds'] >= 3:
                        csv_main.append(row)
                    else:
                        csv_appendix.append(row)
    
    # Save main CSV
    if csv_main:
        main_csv_file = BASE_DIR / "per_subject_accuracy_main.csv"
        with open(main_csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=csv_main[0].keys())
            writer.writeheader()
            writer.writerows(csv_main)
        print(f"   ✅ Saved: {main_csv_file} ({len(csv_main)} rows)")
    
    # Save appendix CSV
    if csv_appendix:
        appendix_csv_file = BASE_DIR / "per_subject_accuracy_appendix_n_lt_3.csv"
        with open(appendix_csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=csv_appendix[0].keys())
            writer.writeheader()
            writer.writerows(csv_appendix)
        print(f"   ✅ Saved: {appendix_csv_file} ({len(csv_appendix)} rows, N < 3)")
    
    # CSV 2: Cross-model swings summary
    csv_swings = []
    all_swings_list = []
    
    for exp_name, cross_swings in all_cross_swings.items():
        exp_info = all_results[exp_name].get('experiment_info', {})
        exp_type = exp_info.get('type', 'unknown')
        
        for subject_id, stats in cross_swings.items():
            row = {
                'Experiment': exp_name,
                'Experiment_Type': exp_type,
                'Subject': subject_id,
                'Swing': f"{stats['swing']:.4f}",
                'Mean_Accuracy': f"{stats['mean']:.4f}",
                'Min_Accuracy': f"{stats['min']:.4f}",
                'Max_Accuracy': f"{stats['max']:.4f}",
                'N_Combinations': stats['n_combinations'],
                'Min_Model_Hyperparam': stats['min_model_label'],
                'Max_Model_Hyperparam': stats['max_model_label']
            }
            csv_swings.append(row)
            all_swings_list.append({
                'experiment': exp_name,
                'subject': subject_id,
                'swing': stats['swing'] * 100,
                'mean': stats['mean'] * 100,
                'min': stats['min'] * 100,
                'max': stats['max'] * 100,
                'n_combinations': stats['n_combinations'],
                'min_model_label': stats['min_model_label'],
                'max_model_label': stats['max_model_label']
            })
    
    if csv_swings:
        swings_csv_file = BASE_DIR / "cross_model_swings_summary.csv"
        with open(swings_csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=csv_swings[0].keys())
            writer.writeheader()
            writer.writerows(csv_swings)
        print(f"   ✅ Saved: {swings_csv_file} ({len(csv_swings)} rows)")
    
    # Generate markdown report
    print("\n" + "=" * 80)
    print("GENERATING MARKDOWN REPORT")
    print("=" * 80)
    
    report_file = BASE_DIR / "per_subject_accuracy_improved_report.md"
    with open(report_file, 'w') as f:
        f.write("# Per-Subject Accuracy Analysis by Model × Hyperparameter (Improved)\n\n")
        f.write("## Summary\n\n")
        f.write("This report includes:\n")
        f.write("- Fixed naming consistency (n_neighbors, learning_rate, etc.)\n")
        f.write("- Fold comparability information\n")
        f.write("- Minimum evidence filter (N Folds >= 3 in main table)\n")
        f.write("- 95% Confidence Intervals and Standard Errors\n")
        f.write("- Verified swing calculation (max - min)\n")
        f.write("- Experiment type labeling (uniform vs random)\n\n")
        
        # Top swings
        all_swings_list.sort(key=lambda x: x['swing'], reverse=True)
        f.write("## Top 30 Subjects with Largest Cross-Model Swings\n\n")
        f.write("| Rank | Subject | Experiment | Type | Swing | Range (Min-Max) | Mean | N Combos | Min Model×HP | Max Model×HP |\n")
        f.write("|------|---------|------------|------|-------|----------------|------|----------|--------------|-------------|\n")
        for i, swing_data in enumerate(all_swings_list[:30], 1):
            exp_name = swing_data['experiment']
            exp_type = all_results[exp_name].get('experiment_info', {}).get('type', 'unknown')
            min_label = swing_data.get('min_model_label', 'N/A')[:50]  # Truncate if too long
            max_label = swing_data.get('max_model_label', 'N/A')[:50]
            f.write(f"| {i} | {swing_data['subject']} | {exp_name} | {exp_type} | "
                   f"{swing_data['swing']:.1f}% | "
                   f"{swing_data['min']:.1f}% - {swing_data['max']:.1f}% | "
                   f"{swing_data['mean']:.1f}% | {swing_data['n_combinations']} | "
                   f"{min_label} | {max_label} |\n")
        
        f.write("\n---\n\n")
        f.write("## Methodology Notes\n\n")
        f.write("1. **Swing Calculation**: Swing = max - min (verified)\n")
        f.write("2. **Minimum Evidence**: Main table shows only model×hyperparam combinations with N Folds >= 3\n")
        f.write("3. **Uncertainty**: 95% CIs calculated using binomial approximation\n")
        f.write("4. **Fold Comparability**: Fold IDs stored for each combination to verify comparability\n")
        f.write("5. **Multiple Comparisons**: Note that rankings may flip with different fold splits\n\n")
    
    print(f"   ✅ Saved: {report_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nGenerated Files:")
    print(f"  - per_subject_accuracy_main.csv (N >= 3)")
    print(f"  - per_subject_accuracy_appendix_n_lt_3.csv (N < 3)")
    print(f"  - cross_model_swings_summary.csv")
    print(f"  - per_subject_accuracy_improved_report.md")
    if HAS_MATPLOTLIB:
        print(f"  - per_subject_analysis_improved/subject_instability_plot.png")
        print(f"  - per_subject_analysis_improved/rank_stability_plot.png")

if __name__ == '__main__':
    main()

