#!/usr/bin/env python
"""
Create box plots showing accuracy distributions for top 30 subjects per experiment.

Generates 4 separate box plot graphs:
1. PCA_L_6_Random
2. PCA_L_2_Random
3. ANOVA_L_2_Random
4. ANOVA_L_6_Random

Each shows the accuracy distribution (across model×hyperparameter combinations) for the top 30 subjects by swing.
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics
import re

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not available - cannot generate plots")
    print("   Install with: pip install matplotlib numpy")

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "PCA_L_6_Random": {
        "path": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
        "description": "PCA P=6 (50 random folds)"
    },
    "PCA_L_2_Random": {
        "path": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
        "description": "PCA P=2 (50 random folds)"
    },
    "ANOVA_L_2_Random": {
        "path": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
        "description": "ANOVA P=2 (50 random folds)"
    },
    "ANOVA_L_6_Random": {
        "path": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
        "description": "ANOVA P=6 (50 random folds)"
    },
}

def extract_subject_ids_from_fold(fold_dir_name):
    """Extract subject IDs from fold directory name."""
    pattern = r'sub-(\d+)'
    matches = re.findall(pattern, fold_dir_name)
    return [f"sub-{m}" for m in matches]

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
                        hyperparams = data.get('hyperparams', {})
                        
                        # Create hyperparam key
                        if hyperparams:
                            sorted_keys = sorted(hyperparams.keys())
                            param_str = "_".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
                        else:
                            param_str = "default"
                        
                        # Store with fold_id
                        for subject_id in subject_ids:
                            model_hyperparam_subject_fold_acc[model_name][param_str][subject_id][fold_name] = acc
                except Exception as e:
                    continue
    
    return dict(model_hyperparam_subject_fold_acc)

def analyze_subject_swings(model_hyperparam_subject_fold_acc):
    """Calculate cross-model swings and collect all accuracies per subject."""
    subject_all_accuracies = defaultdict(list)
    subject_cross_swings = {}
    
    for model_name, hyperparam_dict in model_hyperparam_subject_fold_acc.items():
        for hyperparam_str, subject_fold_dict in hyperparam_dict.items():
            for subject_id, fold_acc_dict in subject_fold_dict.items():
                accuracies = list(fold_acc_dict.values())
                # Add all accuracies for this subject×model×hyperparam
                subject_all_accuracies[subject_id].extend(accuracies)
    
    # Calculate swings
    for subject_id, all_accs in subject_all_accuracies.items():
        if all_accs:
            subject_cross_swings[subject_id] = {
                'swing': max(all_accs) - min(all_accs),
                'mean': statistics.mean(all_accs),
                'min': min(all_accs),
                'max': max(all_accs),
                'all_accuracies': all_accs
            }
    
    return subject_cross_swings

def create_box_plot_for_experiment(exp_name, exp_info, output_dir):
    """Create box plot for a single experiment showing top 30 subjects."""
    if not HAS_MATPLOTLIB:
        return False
    
    print(f"\n📊 Creating box plot for {exp_name}...")
    
    # Extract data
    model_hyperparam_subject_fold_acc = extract_per_subject_accuracies_by_model_hyperparam(exp_info['path'])
    
    if not model_hyperparam_subject_fold_acc:
        print(f"   ⚠️  No data found")
        return False
    
    subject_swings = analyze_subject_swings(model_hyperparam_subject_fold_acc)
    
    if not subject_swings:
        print(f"   ⚠️  No subject data")
        return False
    
    # Get top 30 subjects by swing
    sorted_subjects = sorted(subject_swings.items(), key=lambda x: x[1]['swing'], reverse=True)[:30]
    
    if not sorted_subjects:
        return False
    
    # Prepare data for box plot
    subjects = [s[0] for s in sorted_subjects]
    accuracies_list = [s[1]['all_accuracies'] for s in sorted_subjects]
    swings = [s[1]['swing'] * 100 for s in sorted_subjects]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Create box plot
    bp = ax.boxplot(accuracies_list, labels=subjects, vert=True, patch_artist=True,
                    showmeans=True, meanline=False, showfliers=True)
    
    # Color boxes by swing magnitude
    for i, (patch, swing) in enumerate(zip(bp['boxes'], swings)):
        # Color scale: red for high swing (>30%), orange for medium (20-30%), blue for low (<20%)
        if swing > 30:
            color = 'lightcoral'
        elif swing > 20:
            color = 'wheat'
        else:
            color = 'lightblue'
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Add mean line
    means = [statistics.mean(accs) for accs in accuracies_list]
    ax.plot(range(1, len(means) + 1), means, 'ko', markersize=4, label='Mean', zorder=3)
    
    # Add 30% swing threshold line (horizontal at some reference point)
    max_mean = max(means)
    ax.axhline(y=max_mean * 0.7, color='red', linestyle='--', linewidth=1.5, alpha=0.5, label='30% swing threshold reference')
    
    # Formatting
    ax.set_xlabel('Subject (sorted by swing, descending)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
    ax.set_title(f'{exp_name}\n{exp_info["description"]}\nTop 30 Subjects by Cross-Model×Hyperparameter Swing',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 1)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=8)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='lightcoral', alpha=0.7, label='High swing (>30%)'),
        mpatches.Patch(facecolor='wheat', alpha=0.7, label='Medium swing (20-30%)'),
        mpatches.Patch(facecolor='lightblue', alpha=0.7, label='Low swing (<20%)'),
        plt.Line2D([0], [0], marker='o', color='k', linestyle='None', markersize=4, label='Mean')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Add text annotation with swing values
    for i, (subject, swing) in enumerate(zip(subjects, swings)):
        ax.text(i + 1, 0.02, f'{swing:.0f}%', rotation=90, ha='center', va='bottom', 
               fontsize=6, fontweight='bold')
    
    plt.tight_layout()
    
    # Save
    output_file = output_dir / f'{exp_name}_top30_boxplot.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    if not HAS_MATPLOTLIB:
        print("=" * 80)
        print("ERROR: matplotlib is required for visualization")
        print("=" * 80)
        print("\nPlease install matplotlib:")
        print("  pip install matplotlib numpy")
        print("\nOr use a conda environment:")
        print("  conda install matplotlib numpy")
        return
    
    print("=" * 80)
    print("CREATING BOX PLOTS FOR TOP 30 SUBJECTS")
    print("=" * 80)
    
    output_dir = BASE_DIR / "per_subject_boxplots"
    output_dir.mkdir(exist_ok=True)
    
    # Create one box plot per experiment
    for exp_name, exp_info in EXPERIMENTS.items():
        create_box_plot_for_experiment(exp_name, exp_info, output_dir)
    
    print("\n" + "=" * 80)
    print("VISUALIZATION COMPLETE")
    print("=" * 80)
    print(f"\nAll plots saved to: {output_dir}")
    print("\nGenerated files:")
    for exp_name in EXPERIMENTS.keys():
        print(f"  - {exp_name}_top30_boxplot.png")

if __name__ == '__main__':
    main()

