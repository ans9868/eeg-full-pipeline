#!/usr/bin/env python
"""
Create box plots showing fold-to-fold variance for specific model×hyperparameter combinations.

This shows the same type of variance as Table 1: same model×HP, different folds.
Each boxplot shows the distribution of accuracies across folds where a subject appears in the test set.
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not available")

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

def extract_subject_ids_from_fold(fold_name):
    """Extract subject IDs from fold name like 'sub-3_sub-60'."""
    import re
    return re.findall(r'sub-\d+', fold_name)

def load_fold_variance_data(exp_name, results_dir):
    """Load fold-to-fold variance data: {model×HP: {subject: [fold_accuracies]}}"""
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {model_hp_key: {subject: [accuracies]}}
    model_hp_subject_folds = defaultdict(lambda: defaultdict(list))
    
    # Iterate through all model directories
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        model_name = model_dir.name
        
        # Iterate through fold directories
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            # Extract subjects from fold name
            subject_ids = extract_subject_ids_from_fold(fold_dir.name)
            
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
                        hyperparams = data.get('hyperparams', {})
                        
                        # Create model×HP key
                        if hyperparams:
                            sorted_keys = sorted(hyperparams.keys())
                            param_str = "_".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
                        else:
                            param_str = "default"
                        
                        model_hp_key = f"{model_name}__{param_str}"
                        
                        # Store for each subject in test set
                        for subject_id in subject_ids:
                            model_hp_subject_folds[model_hp_key][subject_id].append(acc)
                except Exception as e:
                    pass
    
    return model_hp_subject_folds

def create_box_plot_fold_variance(exp_name, model_hp_key, model_hp_subject_folds, output_dir, top_n=30):
    """Create box plot showing fold-to-fold variance for a specific model×HP."""
    if not HAS_MATPLOTLIB:
        return False
    
    if model_hp_key not in model_hp_subject_folds:
        print(f"   ⚠️  Model×HP not found: {model_hp_key}")
        return False
    
    subject_folds = model_hp_subject_folds[model_hp_key]
    
    # Calculate swing (max-min) for each subject
    subject_swings = []
    for subject, accs in subject_folds.items():
        if len(accs) >= 2:  # Need at least 2 folds
            swing = max(accs) - min(accs)
            subject_swings.append((subject, swing, accs))
    
    # Sort by swing (descending) and take top N
    subject_swings.sort(key=lambda x: x[1], reverse=True)
    subject_swings = subject_swings[:top_n]
    
    if not subject_swings:
        print(f"   ⚠️  No subjects with sufficient folds")
        return False
    
    subjects = [s[0] for s in subject_swings]
    accuracies_list = [s[2] for s in subject_swings]
    swings = [s[1] * 100 for s in subject_swings]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(18, 10))
    
    # Create box plot
    positions = range(1, len(accuracies_list) + 1)
    bp = ax.boxplot(accuracies_list, positions=positions, tick_labels=subjects, vert=True, 
                    patch_artist=True, showmeans=False, meanline=False, showfliers=True,
                    widths=0.6)
    
    # Color boxes by swing magnitude
    for i, (patch, swing) in enumerate(zip(bp['boxes'], swings)):
        if swing > 30:
            color = '#ff6b6b'  # Light red
        elif swing > 20:
            color = '#ffd93d'  # Yellow/orange
        else:
            color = '#6bcf7f'  # Light green/blue
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1)
    
    # Formatting
    ax.set_xlabel('Subject (sorted by swing, descending)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Accuracy', fontsize=13, fontweight='bold')
    ax.set_title(f'{exp_name}\nFold-to-Fold Variance for {model_hp_key}\n(Box shows distribution across folds where subject appears in test set)',
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_ylim(-0.15, 1.05)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(fontsize=10)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='#ff6b6b', alpha=0.7, edgecolor='black', linewidth=1, label='High swing (>30%)'),
        mpatches.Patch(facecolor='#ffd93d', alpha=0.7, edgecolor='black', linewidth=1, label='Medium swing (20-30%)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)
    
    # Add swing values as text annotations below boxes
    for i, (subject, swing) in enumerate(zip(subjects, swings)):
        ax.text(i + 1, -0.12, f'{swing:.0f}%', rotation=90, ha='center', va='top', 
               fontsize=8, fontweight='bold', color='darkred')
    
    # Add explanation text box in top right
    explanation_text = (
        'Swing % = (Max - Min) accuracy\n'
        'across folds where this subject\n'
        'appears in the test set.\n'
        'Same model×hyperparameter,\n'
        'different fold combinations.'
    )
    ax.text(0.98, 0.98, explanation_text, transform=ax.transAxes,
           fontsize=11, verticalalignment='top', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='black', linewidth=2),
           fontweight='bold')
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0.18, 1, 0.98])
    
    # Save
    safe_key = model_hp_key.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '')
    output_file = output_dir / f'{exp_name}_fold_variance_{safe_key}_top{top_n}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    print(f"      Subjects plotted: {len(subjects)}")
    print(f"      Swing range: {min(swings):.1f}% - {max(swings):.1f}%")
    return True

def main():
    """Main function."""
    if not HAS_MATPLOTLIB:
        print("=" * 80)
        print("ERROR: matplotlib is required for visualization")
        print("=" * 80)
        return
    
    print("=" * 80)
    print("CREATING BOX PLOTS: FOLD-TO-FOLD VARIANCE (Table 1 Style)")
    print("=" * 80)
    
    output_dir = BASE_DIR / "per_subject_boxplots_fold_variance"
    output_dir.mkdir(exist_ok=True)
    
    # For each experiment, find all model×HP combinations and plot top ones
    success_count = 0
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        model_hp_subject_folds = load_fold_variance_data(exp_name, results_dir)
        
        if not model_hp_subject_folds:
            print(f"   ⚠️  No data found")
            continue
        
        # Find model×HP combinations with most subjects
        model_hp_counts = [(key, len(subjects)) for key, subjects in model_hp_subject_folds.items()]
        model_hp_counts.sort(key=lambda x: x[1], reverse=True)
        
        print(f"   Found {len(model_hp_counts)} model×HP combinations")
        
        # Plot top 3 model×HP combinations (or all if fewer)
        for model_hp_key, n_subjects in model_hp_counts[:3]:
            print(f"   Creating plot for: {model_hp_key[:80]}... ({n_subjects} subjects)")
            if create_box_plot_fold_variance(exp_name, model_hp_key, model_hp_subject_folds, output_dir):
                success_count += 1
    
    print("\n" + "=" * 80)
    print("VISUALIZATION COMPLETE")
    print("=" * 80)
    print(f"\n✅ Generated {success_count} plots")
    print(f"\nAll plots saved to: {output_dir}")

if __name__ == '__main__':
    main()

