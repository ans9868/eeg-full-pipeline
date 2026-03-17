#!/usr/bin/env python
"""
Create per-subject success rate plots with explanatory blurbs.

Two graphs:
1. Top: Per-Subject Classification Success Rate (% of folds where accuracy > 50%)
2. Bottom: Per-Subject Mean Accuracy Across All Folds
"""

import pandas as pd
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from collections import defaultdict
import statistics
import re

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
}

def extract_hyperparams(results_file):
    """Extract hyperparameters from results.json file."""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        return data.get('hyperparams', {})
    except:
        return {}

def load_per_subject_accuracies(exp_name, results_dir):
    """
    Load per-subject accuracies from parquet files.
    
    Returns: {subject_id: [list of accuracies from all fold×model combinations]}
    """
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {subject_id: [accuracies from all fold×model combinations]}
    subject_accuracies = defaultdict(list)
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            
            # Find task directories
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
                        
                        # Filter data for this subject
                        subject_data = test_df[test_df['SubjectID'] == subject_id_num]
                        
                        # Calculate accuracy: (label == prediction).sum() / len(subject_data)
                        correct = (subject_data['label'] == subject_data['prediction']).sum()
                        total = len(subject_data)
                        accuracy = correct / total if total > 0 else 0.0
                        
                        # Store accuracy
                        subject_accuracies[subject_id].append(accuracy)
                        
                except Exception as e:
                    continue
    
    return subject_accuracies

def calculate_success_rate(accuracies):
    """
    Calculate success rate: % of fold×model combinations where accuracy > 50%.
    
    Pseudocode:
        successful_folds = 0
        total_folds = length(accuracies)
        
        for accuracy in accuracies:
            if accuracy > 0.50:
                successful_folds = successful_folds + 1
        
        if total_folds == 0:
            return 0
        else:
            return (successful_folds / total_folds) * 100
    """
    if not accuracies:
        return 0.0
    
    successful_folds = sum(1 for acc in accuracies if acc > 0.50)
    total_folds = len(accuracies)
    
    return (successful_folds / total_folds) * 100 if total_folds > 0 else 0.0

def calculate_mean_accuracy(accuracies):
    """
    Calculate mean accuracy: average of all fold×model accuracies.
    
    Pseudocode:
        total_accuracy_sum = 0
        total_folds = length(accuracies)
        
        for accuracy in accuracies:
            total_accuracy_sum = total_accuracy_sum + accuracy
        
        if total_folds == 0:
            return 0
        else:
            return (total_accuracy_sum / total_folds) * 100
    """
    if not accuracies:
        return 0.0
    
    return statistics.mean(accuracies) * 100


def display_experiment_name(exp_name):
    """Human-readable experiment label for plot titles."""
    return exp_name.replace('ANOVA', 'F-test')


def success_rate_color(sr):
    """Color by success category: 100% (green), partial (yellow), 0% (red)."""
    if sr >= 99.999:
        return '#90EE90'  # 100% Success
    if sr <= 0.001:
        return '#FFB6C1'  # 0% Success
    return '#FFD700'      # Partial Success


def create_per_subject_success_rate_plot(exp_name, subject_accuracies, output_dir):
    """Create bar plot showing per-subject classification success rate."""
    exp_disp = display_experiment_name(exp_name)
    if not subject_accuracies:
        return False
    
    # Calculate metrics for each subject
    subjects = []
    success_rates = []
    mean_accs = []
    
    for subject_id in sorted(subject_accuracies.keys(), key=lambda x: int(x.split('-')[1])):
        accuracies = subject_accuracies[subject_id]
        if accuracies:
            success_rate = calculate_success_rate(accuracies)
            mean_acc = calculate_mean_accuracy(accuracies)
            subjects.append(subject_id)
            success_rates.append(success_rate)
            mean_accs.append(mean_acc)
    
    # Sort by success rate (descending)
    sorted_data = sorted(zip(subjects, success_rates, mean_accs), key=lambda x: x[1], reverse=True)
    subjects, success_rates, mean_accs = zip(*sorted_data) if sorted_data else ([], [], [])
    
    if not subjects:
        return False
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12))
    
    # Color coding: 100% success = green, partial = yellow, 0% success = red
    colors = [success_rate_color(sr) for sr in success_rates]
    
    # Plot 1: Success Rate
    bars1 = ax1.bar(range(len(subjects)), success_rates, color=colors, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('% Correctly Classified', fontsize=13, fontweight='bold')
    ax1.set_title(f'{exp_disp}\nPer-Subject Classification Success Rate\n(% of folds where accuracy > 50%)',
                 fontsize=15, fontweight='bold', pad=20)
    ax1.set_xticks(range(len(subjects)))
    ax1.set_xticklabels(subjects, rotation=45, ha='right', fontsize=9)
    ax1.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_ylim(0, 105)
    
    # Legend for top plot
    legend_elements = [
        mpatches.Patch(facecolor='#90EE90', alpha=0.7, edgecolor='black', label='100% Success'),
        mpatches.Patch(facecolor='#FFD700', alpha=0.7, edgecolor='black', label='Partial Success'),
        mpatches.Patch(facecolor='#FFB6C1', alpha=0.7, edgecolor='black', label='0% Success'),
    ]
    ax1.legend(handles=legend_elements + [plt.Line2D([0], [0], color='red', linestyle='--', label='50% Threshold')],
              loc='upper right', fontsize=10)
    
    # Plot 2: Mean Accuracy
    bars2 = ax2.bar(range(len(subjects)), mean_accs, color=colors, edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Mean Accuracy (%)', fontsize=13, fontweight='bold')
    ax2.set_title(f'{exp_disp}\nPer-Subject Mean Accuracy Across All Folds',
                 fontsize=15, fontweight='bold', pad=20)
    ax2.set_xticks(range(len(subjects)))
    ax2.set_xticklabels(subjects, rotation=45, ha='right', fontsize=9)
    ax2.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend(fontsize=11)
    ax2.set_ylim(0, 105)
    
    plt.tight_layout()
    output_file = output_dir / f'{exp_name}_per_subject_success_rate.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis" / "success_rate_plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        # Load per-subject accuracies from parquet files
        subject_accuracies = load_per_subject_accuracies(exp_name, results_dir)
        
        if not subject_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found {len(subject_accuracies)} subjects with data")
        
        # Create plot
        create_per_subject_success_rate_plot(exp_name, subject_accuracies, output_dir)
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

