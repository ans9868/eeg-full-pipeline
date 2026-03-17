#!/usr/bin/env python
"""
Quickly generate F-test vs PCA combined figure for L_6_Random.
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

def calculate_success_rate(accuracies):
    """Success rate: % of folds where accuracy > 50%."""
    if not accuracies:
        return 0.0
    return (sum(1 for acc in accuracies if acc > 50) / len(accuracies)) * 100

def calculate_mean_accuracy(accuracies):
    """Mean accuracy across all folds."""
    return statistics.mean(accuracies) if accuracies else 0.0

def success_rate_color(sr):
    """Color by success category: 100% (green), partial (yellow), 0% (red)."""
    if sr >= 99.999:
        return '#90EE90'  # 100% Success
    if sr <= 0.001:
        return '#FFB6C1'  # 0% Success
    return '#FFD700'      # Partial Success

def load_per_subject_accuracies_by_model_hp(exp_name, results_dir):
    """Load per-subject accuracies grouped by model×HP combination."""
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    model_hp_subject_accuracies = defaultdict(lambda: defaultdict(list))
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        model_name = model_dir.name
        
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            
            task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
            
            for task_dir in task_dirs:
                results_file = task_dir / "results.json"
                if not results_file.exists():
                    continue
                
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                    
                    accuracy = data.get('accuracy', 0.0)
                    hyperparams = data.get('hyperparams', {})
                    model_hp_key = f"{model_name}_({', '.join([f'{k}={v}' for k, v in sorted(hyperparams.items())])})"
                    model_hp_subject_accuracies[model_hp_key][fold_name].append(accuracy)
                except:
                    pass
    
    return model_hp_subject_accuracies

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


def create_ftest_vs_pca_combined_plot(model_hp_ftest, model_hp_pca, output_dir):
    """
    Create a 2x2 combined figure comparing F-test vs PCA for KNN n_neighbors=1.
    Left column: F-test
    Right column: PCA
    """
    exp_disp_ftest = "F-test"
    exp_disp_pca = "PCA"

    fig, axes = plt.subplots(2, 2, figsize=(24, 12), sharex=False)

    # Left column: F-test
    subject_accuracies_ftest = model_hp_ftest
    subjects_ftest, success_rates_ftest, mean_accs_ftest, colors_ftest = _prepare_subject_series(
        subject_accuracies_ftest
    )
    if subjects_ftest:
        ax1_ftest = axes[0, 0]
        ax2_ftest = axes[1, 0]

        # Top: F-test success rate
        ax1_ftest.bar(range(len(subjects_ftest)), success_rates_ftest, color=colors_ftest, edgecolor='black', alpha=0.7)
        ax1_ftest.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
        ax1_ftest.set_ylabel('% Correctly Classified', fontsize=13, fontweight='bold')
        ax1_ftest.set_title(
            f'{exp_disp_ftest}\nKNN (n_neighbors=1)\nPer-Subject Classification Success Rate\n(% of folds where accuracy > 50%)',
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
            f'{exp_disp_ftest}\nKNN (n_neighbors=1)\nPer-Subject Mean Accuracy Across All Folds',
            fontsize=15, fontweight='bold', pad=20
        )
        ax2_ftest.set_xticks(range(len(subjects_ftest)))
        ax2_ftest.set_xticklabels(subjects_ftest, rotation=45, ha='right', fontsize=9)
        ax2_ftest.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
        ax2_ftest.grid(True, alpha=0.3, axis='y')
        ax2_ftest.legend(fontsize=11)
        ax2_ftest.set_ylim(0, 105)

    # Right column: PCA
    subject_accuracies_pca = model_hp_pca
    subjects_pca, success_rates_pca, mean_accs_pca, colors_pca = _prepare_subject_series(subject_accuracies_pca)
    if subjects_pca:
        ax1_pca = axes[0, 1]
        ax2_pca = axes[1, 1]

        # Top: PCA success rate
        ax1_pca.bar(range(len(subjects_pca)), success_rates_pca, color=colors_pca, edgecolor='black', alpha=0.7)
        ax1_pca.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
        ax1_pca.set_ylabel('% Correctly Classified', fontsize=13, fontweight='bold')
        ax1_pca.set_title(
            f'{exp_disp_pca}\nKNN (n_neighbors=1)\nPer-Subject Classification Success Rate\n(% of folds where accuracy > 50%)',
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
            f'{exp_disp_pca}\nKNN (n_neighbors=1)\nPer-Subject Mean Accuracy Across All Folds',
            fontsize=15, fontweight='bold', pad=20
        )
        ax2_pca.set_xticks(range(len(subjects_pca)))
        ax2_pca.set_xticklabels(subjects_pca, rotation=45, ha='right', fontsize=9)
        ax2_pca.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
        ax2_pca.grid(True, alpha=0.3, axis='y')
        ax2_pca.legend(fontsize=11)
        ax2_pca.set_ylim(0, 105)

    plt.tight_layout()
    output_file = output_dir / 'ANOVA_L_6_Random_vs_PCA_L_6_Random_combined.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis" / "success_rate_plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ftest_model_hp_data = {}
    pca_model_hp_data = {}
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Loading {exp_name}...")
        
        # Load per-subject accuracies grouped by model×HP
        model_hp_subject_accuracies = load_per_subject_accuracies_by_model_hp(exp_name, results_dir)
        
        if not model_hp_subject_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found {len(model_hp_subject_accuracies)} model×HP combinations")
        
        # Store for F-test vs PCA comparison
        if exp_name == "ANOVA_L_6_Random":
            ftest_model_hp_data = model_hp_subject_accuracies
        
        # Store PCA data for F-test vs PCA comparison
        if exp_name == "PCA_L_6_Random":
            pca_model_hp_data = model_hp_subject_accuracies
    
    # Create F-test vs PCA combined figure
    if ftest_model_hp_data and pca_model_hp_data:
        # Find KNN n_neighbors=1 keys for both experiments
        key_knn_ftest = "KNN_(metric=euclidean, n_neighbors=1, weights=uniform)"
        key_knn_pca = "KNN_(metric=euclidean, n_neighbors=1, weights=uniform)"
        
        if key_knn_ftest in ftest_model_hp_data and key_knn_pca in pca_model_hp_data:
            print(f"\n📊 Creating F-test vs PCA combined figure for L_6_Random...")
            print(f"   F-test key: {key_knn_ftest}")
            print(f"   PCA key: {key_knn_pca}")
            create_ftest_vs_pca_combined_plot(
                ftest_model_hp_data[key_knn_ftest],
                pca_model_hp_data[key_knn_pca],
                output_dir
            )
        else:
            print(f"⚠️  Could not find matching KNN keys")
            print(f"   Available F-test keys: {list(ftest_model_hp_data.keys())}")
            print(f"   Available PCA keys: {list(pca_model_hp_data.keys())}")
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
