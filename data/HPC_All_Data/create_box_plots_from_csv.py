#!/usr/bin/env python
"""
Create box plots from existing CSV data.

Reads the cross_model_swings_summary.csv and per_subject_accuracy_main.csv
to create box plots showing accuracy distributions for top 30 subjects per experiment.
"""

import csv
from pathlib import Path
from collections import defaultdict
import statistics

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not available")
    print("   To generate plots, install: pip install matplotlib numpy")

BASE_DIR = Path(__file__).parent

EXPERIMENTS_TO_PLOT = [
    "PCA_L_6_Random",
    "PCA_L_2_Random",
    "ANOVA_L_2_Random",
    "ANOVA_L_6_Random"
]

def extract_subject_ids_from_fold(fold_name):
    """Extract subject IDs from fold name like 'sub-3_sub-60'."""
    import re
    return re.findall(r'sub-\d+', fold_name)

def load_data_from_json():
    """Load individual fold accuracies from JSON files (not just means from CSV)."""
    import json
    
    # Map experiment names to directory paths
    exp_to_dir = {
        "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
        "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
        "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
        "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    }
    
    # Structure: {exp: {subject: [all_individual_fold_accuracies]}}
    subject_all_fold_accuracies = defaultdict(lambda: defaultdict(list))
    
    for exp_name, results_dir in exp_to_dir.items():
        if not results_dir.exists():
            print(f"⚠️  Directory not found: {results_dir}")
            continue
        
        results_path = results_dir / "ml_results_grid_search"
        if not results_path.exists():
            results_path = results_dir
        
        # Iterate through all model directories
        for model_dir in results_path.iterdir():
            if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
                continue
            
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
                            # Store individual fold accuracy for each subject in test set
                            for subject_id in subject_ids:
                                subject_all_fold_accuracies[exp_name][subject_id].append(acc)
                    except Exception as e:
                        pass
    
    return subject_all_fold_accuracies

def load_data_from_csv():
    """Load subject accuracy data from CSV files."""
    # Load cross-model swings to get top subjects
    swings_file = BASE_DIR / "cross_model_swings_summary.csv"
    if not swings_file.exists():
        print(f"❌ File not found: {swings_file}")
        return {}
    
    # Read swings to identify top subjects
    subject_swings = defaultdict(dict)
    with open(swings_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exp = row['Experiment']
            subject = row['Subject']
            swing = float(row['Swing'])
            subject_swings[exp][subject] = swing
    
    # Load individual fold accuracies from JSON (not just means from CSV)
    subject_accuracies = load_data_from_json()
    
    return subject_swings, subject_accuracies

def create_box_plot_for_experiment(exp_name, subject_swings, subject_accuracies, output_dir):
    """Create box plot for a single experiment showing top 30 subjects."""
    if not HAS_MATPLOTLIB:
        return False
    
    print(f"\n📊 Creating box plot for {exp_name}...")
    
    if exp_name not in subject_swings or exp_name not in subject_accuracies:
        print(f"   ⚠️  No data found for {exp_name}")
        return False
    
    # Get top 30 subjects by swing
    exp_swings = subject_swings[exp_name]
    sorted_subjects = sorted(exp_swings.items(), key=lambda x: x[1], reverse=True)[:30]
    
    if not sorted_subjects:
        print(f"   ⚠️  No subjects found")
        return False
    
    # Prepare data for box plot
    subjects = [s[0] for s in sorted_subjects]
    accuracies_list = []
    swings = []
    
    for subject_id, swing in sorted_subjects:
        # Get all accuracies for this subject (across all model×hyperparam combinations)
        accs = subject_accuracies[exp_name].get(subject_id, [])
        if accs:
            accuracies_list.append(accs)
            swings.append(swing * 100)
        else:
            # If no data in main CSV, skip
            continue
    
    if not accuracies_list:
        print(f"   ⚠️  No accuracy data found")
        return False
    
    # Update subjects list to match
    subjects = [subjects[i] for i in range(len(accuracies_list))]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(18, 10))
    
    # Create box plot
    positions = range(1, len(accuracies_list) + 1)
    bp = ax.boxplot(accuracies_list, positions=positions, tick_labels=subjects, vert=True, 
                    patch_artist=True, showmeans=False, meanline=False, showfliers=True,
                    widths=0.6)
    
    # Color boxes by swing magnitude
    for i, (patch, swing) in enumerate(zip(bp['boxes'], swings)):
        # Color scale: red for high swing (>30%), orange for medium (20-30%), blue for low (<20%)
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
    
    # Min/max markers removed - with small sample sizes (3-5 model×HP combinations),
    # min/max equals Q1/Q3 (IQR boundaries), so dots would be redundant with box plot
    
    # Formatting
    ax.set_xlabel('Subject (sorted by swing, descending)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Accuracy', fontsize=13, fontweight='bold')
    ax.set_title(f'{exp_name}\nTop 30 Subjects by Cross-Model×Hyperparameter Swing\n(Box shows distribution of individual fold accuracies across all model×HP combinations)',
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    # Set y-axis limit with more bottom space for labels
    ax.set_ylim(-0.15, 1.05)  # More negative space for bottom labels
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(fontsize=10)
    
    # Add legend (excluding low swing, mean, and min/max per user request)
    legend_elements = [
        mpatches.Patch(facecolor='#ff6b6b', alpha=0.7, edgecolor='black', linewidth=1, label='High swing (>30%)'),
        mpatches.Patch(facecolor='#ffd93d', alpha=0.7, edgecolor='black', linewidth=1, label='Medium swing (20-30%)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)
    
    # Add swing values as text annotations below boxes (with more space)
    for i, (subject, swing) in enumerate(zip(subjects, swings)):
        ax.text(i + 1, -0.12, f'{swing:.0f}%', rotation=90, ha='center', va='top', 
               fontsize=8, fontweight='bold', color='darkred')
    
    # Add horizontal line at 30% swing threshold (as reference)
    # Calculate max mean from accuracies for threshold line
    max_mean = max([statistics.mean(accs) for accs in accuracies_list]) if accuracies_list else 0.7
    ax.axhline(y=max_mean * 0.7, color='red', linestyle=':', linewidth=1.5, alpha=0.4, 
              label='30% threshold reference')
    
    # Add explanation text box in top right
    explanation_text = (
        'Swing % = (Max - Min) accuracy\n'
        'across all individual fold\n'
        'accuracies from all model×HP\n'
        'combinations for this subject.\n'
        'Shows cross-model×HP variance\n'
        '(different model choices).'
    )
    ax.text(0.98, 0.98, explanation_text, transform=ax.transAxes,
           fontsize=11, verticalalignment='top', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='black', linewidth=2),
           fontweight='bold')
    
    # Adjust layout with more bottom space for labels
    plt.tight_layout(rect=[0, 0.18, 1, 0.98])  # Leave 18% bottom margin for swing labels
    
    # Save
    output_file = output_dir / f'{exp_name}_top30_boxplot.png'
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
        print("\nPlease install matplotlib and numpy:")
        print("  pip install matplotlib numpy")
        print("\nOr use a conda environment:")
        print("  conda install matplotlib numpy")
        return
    
    print("=" * 80)
    print("CREATING BOX PLOTS FOR TOP 30 SUBJECTS")
    print("=" * 80)
    
    # Load data from CSV
    print("\n📂 Loading data from CSV files...")
    subject_swings, subject_accuracies = load_data_from_csv()
    
    if not subject_swings:
        print("❌ Failed to load data")
        return
    
    output_dir = BASE_DIR / "per_subject_boxplots"
    output_dir.mkdir(exist_ok=True)
    
    # Create one box plot per experiment
    success_count = 0
    for exp_name in EXPERIMENTS_TO_PLOT:
        if create_box_plot_for_experiment(exp_name, subject_swings, subject_accuracies, output_dir):
            success_count += 1
    
    print("\n" + "=" * 80)
    print("VISUALIZATION COMPLETE")
    print("=" * 80)
    print(f"\n✅ Generated {success_count} out of {len(EXPERIMENTS_TO_PLOT)} plots")
    print(f"\nAll plots saved to: {output_dir}")
    print("\nGenerated files:")
    for exp_name in EXPERIMENTS_TO_PLOT:
        print(f"  - {exp_name}_top30_boxplot.png")

if __name__ == '__main__':
    main()

