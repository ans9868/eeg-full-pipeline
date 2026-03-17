#!/usr/bin/env python
"""
Create a 2x2 combined figure comparing F-test vs PCA for L_6_Random.
Averages success rates across ALL models and hyperparameters for each experiment.
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

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

def load_per_subject_accuracies(exp_name, results_dir):
    """
    Load per-subject accuracies from all fold×model combinations (aggregated).
    
    Returns: {subject_id: [list of accuracies from all fold×model combinations]}
    """
    if not results_dir.exists():
        print(f"   ⚠️  Directory not found: {results_dir}")
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
    """Success rate: % of folds where accuracy > 50%."""
    if not accuracies:
        return 0.0
    successful = sum(1 for acc in accuracies if acc > 0.50)
    return (successful / len(accuracies)) * 100

def calculate_mean_accuracy(accuracies):
    """Mean accuracy across all folds."""
    return statistics.mean(accuracies) * 100 if accuracies else 0.0

def success_rate_color(sr):
    """Color by success category: 100% (green), partial (yellow), 0% (red)."""
    if sr >= 99.999:
        return '#90EE90'  # 100% Success
    if sr <= 0.001:
        return '#FFB6C1'  # 0% Success
    return '#FFD700'      # Partial Success

def _prepare_subject_series(subject_accuracies):
    """Build sorted per-subject success-rate and mean-accuracy series."""
    subject_data = []
    for subject_num in range(1, 66):
        subject_id = f"sub-{subject_num}"
        accuracies = subject_accuracies.get(subject_id, [])
        if not accuracies:
            continue
        subject_data.append({
            'subject': subject_id,
            'success_rate': calculate_success_rate(accuracies),
            'mean_acc': calculate_mean_accuracy(accuracies),
        })

    if not subject_data:
        return [], [], [], []

    sorted_data = sorted(subject_data, key=lambda x: x['success_rate'], reverse=True)
    subjects = [s['subject'] for s in sorted_data]
    success_rates = [s['success_rate'] for s in sorted_data]
    mean_accs = [s['mean_acc'] for s in sorted_data]
    colors = [success_rate_color(sr) for sr in success_rates]
    return subjects, success_rates, mean_accs, colors


def create_ftest_vs_pca_combined_plot(ftest_accuracies, pca_accuracies, output_dir):
    """
    Create a 2x2 combined figure comparing F-test vs PCA (aggregate across all models).
    Left column: F-test
    Right column: PCA
    """
    exp_disp_ftest = "F-test"
    exp_disp_pca = "PCA"

    fig, axes = plt.subplots(2, 2, figsize=(24, 12), sharex=False)

    # Left column: F-test (aggregated across all models)
    subjects_ftest, success_rates_ftest, mean_accs_ftest, colors_ftest = _prepare_subject_series(
        ftest_accuracies
    )
    if subjects_ftest:
        ax1_ftest = axes[0, 0]
        ax2_ftest = axes[1, 0]

        # Top: F-test success rate
        ax1_ftest.bar(range(len(subjects_ftest)), success_rates_ftest, color=colors_ftest, edgecolor='black', alpha=0.7)
        ax1_ftest.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
        ax1_ftest.set_ylabel('% Correctly Classified', fontsize=13, fontweight='bold')
        ax1_ftest.set_title(
            f'{exp_disp_ftest} (All Models)\nPer-Subject Classification Success Rate\n(% of folds where accuracy > 50%)',
            fontsize=15, fontweight='bold', pad=20
        )
        ax1_ftest.set_xticks(range(len(subjects_ftest)))
        ax1_ftest.set_xticklabels(subjects_ftest, rotation=45, ha='right', fontsize=9)
        ax1_ftest.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
        ax1_ftest.grid(True, alpha=0.3, axis='y')
        ax1_ftest.set_ylim(0, 105)

        legend_elements = [
            mpatches.Patch(facecolor='#90EE90', alpha=0.7, edgecolor='black', label='100% Success'),
            mpatches.Patch(facecolor='#FFD700', alpha=0.7, edgecolor='black', label='Partial Success'),
            mpatches.Patch(facecolor='#FFB6C1', alpha=0.7, edgecolor='black', label='0% Success'),
        ]
        ax1_ftest.legend(
            handles=legend_elements + [plt.Line2D([0], [0], color='red', linestyle='--', label='50% Threshold')],
            loc='upper right', fontsize=10
        )

        # Bottom: F-test mean accuracy
        ax2_ftest.bar(range(len(subjects_ftest)), mean_accs_ftest, color=colors_ftest, edgecolor='black', alpha=0.7)
        ax2_ftest.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
        ax2_ftest.set_ylabel('Mean Accuracy (%)', fontsize=13, fontweight='bold')
        ax2_ftest.set_title(
            f'{exp_disp_ftest} (All Models)\nPer-Subject Mean Accuracy Across All Folds',
            fontsize=15, fontweight='bold', pad=20
        )
        ax2_ftest.set_xticks(range(len(subjects_ftest)))
        ax2_ftest.set_xticklabels(subjects_ftest, rotation=45, ha='right', fontsize=9)
        ax2_ftest.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
        ax2_ftest.grid(True, alpha=0.3, axis='y')
        ax2_ftest.legend(fontsize=11)
        ax2_ftest.set_ylim(0, 105)

    # Right column: PCA (aggregated across all models)
    subjects_pca, success_rates_pca, mean_accs_pca, colors_pca = _prepare_subject_series(pca_accuracies)
    if subjects_pca:
        ax1_pca = axes[0, 1]
        ax2_pca = axes[1, 1]

        # Top: PCA success rate
        ax1_pca.bar(range(len(subjects_pca)), success_rates_pca, color=colors_pca, edgecolor='black', alpha=0.7)
        ax1_pca.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
        ax1_pca.set_ylabel('% Correctly Classified', fontsize=13, fontweight='bold')
        ax1_pca.set_title(
            f'{exp_disp_pca} (All Models)\nPer-Subject Classification Success Rate\n(% of folds where accuracy > 50%)',
            fontsize=15, fontweight='bold', pad=20
        )
        ax1_pca.set_xticks(range(len(subjects_pca)))
        ax1_pca.set_xticklabels(subjects_pca, rotation=45, ha='right', fontsize=9)
        ax1_pca.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
        ax1_pca.grid(True, alpha=0.3, axis='y')
        ax1_pca.set_ylim(0, 105)

        legend_elements = [
            mpatches.Patch(facecolor='#90EE90', alpha=0.7, edgecolor='black', label='100% Success'),
            mpatches.Patch(facecolor='#FFD700', alpha=0.7, edgecolor='black', label='Partial Success'),
            mpatches.Patch(facecolor='#FFB6C1', alpha=0.7, edgecolor='black', label='0% Success'),
        ]
        ax1_pca.legend(
            handles=legend_elements + [plt.Line2D([0], [0], color='red', linestyle='--', label='50% Threshold')],
            loc='upper right', fontsize=10
        )

        # Bottom: PCA mean accuracy
        ax2_pca.bar(range(len(subjects_pca)), mean_accs_pca, color=colors_pca, edgecolor='black', alpha=0.7)
        ax2_pca.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
        ax2_pca.set_ylabel('Mean Accuracy (%)', fontsize=13, fontweight='bold')
        ax2_pca.set_title(
            f'{exp_disp_pca} (All Models)\nPer-Subject Mean Accuracy Across All Folds',
            fontsize=15, fontweight='bold', pad=20
        )
        ax2_pca.set_xticks(range(len(subjects_pca)))
        ax2_pca.set_xticklabels(subjects_pca, rotation=45, ha='right', fontsize=9)
        ax2_pca.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
        ax2_pca.grid(True, alpha=0.3, axis='y')
        ax2_pca.legend(fontsize=11)
        ax2_pca.set_ylim(0, 105)

    plt.tight_layout()
    output_file = output_dir / 'ANOVA_L_6_Random_vs_PCA_L_6_Random_combined_aggregate.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis" / "success_rate_plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ftest_accuracies = {}
    pca_accuracies = {}
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Loading {exp_name} (aggregating across ALL models)...")
        
        # Load per-subject accuracies (aggregated across all models)
        subject_accuracies = load_per_subject_accuracies(exp_name, results_dir)
        
        if not subject_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found data for {len(subject_accuracies)} subjects")
        print(f"   Total accuracy measurements: {sum(len(accs) for accs in subject_accuracies.values())}")
        
        # Store for F-test vs PCA comparison
        if exp_name == "ANOVA_L_6_Random":
            ftest_accuracies = subject_accuracies
        elif exp_name == "PCA_L_6_Random":
            pca_accuracies = subject_accuracies
    
    # Create F-test vs PCA combined figure
    if ftest_accuracies and pca_accuracies:
        print(f"\n📊 Creating F-test vs PCA combined figure (L_6_Random, ALL MODELS aggregated)...")
        create_ftest_vs_pca_combined_plot(
            ftest_accuracies,
            pca_accuracies,
            output_dir
        )
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
