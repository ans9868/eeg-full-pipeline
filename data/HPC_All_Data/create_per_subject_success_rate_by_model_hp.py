#!/usr/bin/env python
"""
Create per-subject success rate plots for EACH model×hyperparameter combination.

For each experiment and each model×HP combination, creates:
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
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

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

def sanitize_filename(text):
    """Sanitize text for use in filename."""
    # Replace problematic characters
    text = text.replace('/', '_').replace('\\', '_')
    text = text.replace(':', '_').replace('*', '_').replace('?', '_')
    text = text.replace('"', '_').replace('<', '_').replace('>', '_')
    text = text.replace('|', '_').replace(' ', '_')
    return text[:100]  # Limit length


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

def load_per_subject_accuracies_by_model_hp(exp_name, results_dir):
    """
    Load per-subject accuracies grouped by model×HP combination.
    
    Returns: {model_hp_key: {subject_id: [list of accuracies from all folds]}}
    """
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {model_hp_key: {subject_id: [accuracies from all folds]}}
    model_hp_subject_accuracies = defaultdict(lambda: defaultdict(list))
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        model_name = model_dir.name
        
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            
            # Find task directories
            task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
            
            for task_dir in task_dirs:
                test_parquet = task_dir / "test_predictions.parquet"
                results_file = task_dir / "results.json"
                
                if not test_parquet.exists() or not results_file.exists():
                    continue
                
                try:
                    # Get hyperparameters
                    hyperparams = extract_hyperparams(results_file)
                    model_hp_key = format_model_hp_label(model_name, hyperparams)
                    
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
                        
                        # Store accuracy for this model×HP and subject
                        model_hp_subject_accuracies[model_hp_key][subject_id].append(accuracy)
                        
                except Exception as e:
                    continue
    
    return model_hp_subject_accuracies

def calculate_success_rate(accuracies):
    """Calculate success rate: % of fold×model combinations where accuracy > 50%."""
    if not accuracies:
        return 0.0
    
    successful_folds = sum(1 for acc in accuracies if acc > 0.50)
    total_folds = len(accuracies)
    
    return (successful_folds / total_folds) * 100 if total_folds > 0 else 0.0

def calculate_mean_accuracy(accuracies):
    """Calculate mean accuracy: average of all fold×model accuracies."""
    if not accuracies:
        return 0.0
    
    return statistics.mean(accuracies) * 100

def create_per_subject_success_rate_plot_for_model_hp(exp_name, model_hp_key, subject_accuracies, output_dir):
    """Create bar plot showing per-subject classification success rate for a specific model×HP."""
    if not subject_accuracies:
        return False
    
    # Calculate metrics for each subject
    subject_data = []
    
    for subject_num in range(1, 66):
        subject_id = f"sub-{subject_num}"
        accuracies = subject_accuracies.get(subject_id, [])
        
        if accuracies:
            success_rate = calculate_success_rate(accuracies)
            mean_acc = calculate_mean_accuracy(accuracies)
        else:
            success_rate = None
            mean_acc = None
        
        if accuracies:  # Only include subjects with data
            subject_data.append({
                'subject': subject_id,
                'success_rate': success_rate,
                'mean_acc': mean_acc
            })
    
    if not subject_data:
        return False
    
    # Sort by success rate (descending)
    sorted_data = sorted(subject_data, key=lambda x: x['success_rate'], reverse=True)
    subjects = [s['subject'] for s in sorted_data]
    success_rates = [s['success_rate'] for s in sorted_data]
    mean_accs = [s['mean_acc'] for s in sorted_data]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12))
    
    # Color coding: 100% success = green, partial = yellow, 0% success = red
    colors = [success_rate_color(sr) for sr in success_rates]
    
    exp_disp = display_experiment_name(exp_name)

    # Plot 1: Success Rate
    bars1 = ax1.bar(range(len(subjects)), success_rates, color=colors, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('% Correctly Classified', fontsize=13, fontweight='bold')
    ax1.set_title(f'{exp_disp}\n{model_hp_key}\nPer-Subject Classification Success Rate\n(% of folds where accuracy > 50%)',
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
    ax2.set_title(f'{exp_disp}\n{model_hp_key}\nPer-Subject Mean Accuracy Across All Folds',
                 fontsize=15, fontweight='bold', pad=20)
    ax2.set_xticks(range(len(subjects)))
    ax2.set_xticklabels(subjects, rotation=45, ha='right', fontsize=9)
    ax2.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend(fontsize=11)
    ax2.set_ylim(0, 105)
    
    plt.tight_layout()
    
    # Create safe filename
    safe_model_hp = sanitize_filename(model_hp_key)
    output_file = output_dir / f'{exp_name}_per_subject_success_rate_{safe_model_hp}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True


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


def create_specific_examples_combined_plot(exp_name, model_hp_subject_accuracies, output_dir):
    """
    Create a 2x2 combined figure for two illustrative model×HP examples.
    Left column: KNN n_neighbors=1
    Right column: MLP hidden_layer_sizes=[150, 50]
    """
    # Find keys robustly by substrings (exact formatting can vary slightly by source dirs)
    key_knn = next(
        (k for k in model_hp_subject_accuracies.keys()
         if k.startswith('KNN') and 'n_neighbors=1' in k and 'metric=euclidean' in k),
        None
    )
    key_mlp = next(
        (k for k in model_hp_subject_accuracies.keys()
         if 'MLP' in k and 'hidden_layer_sizes=[150, 50]' in k),
        None
    )

    if key_knn is None or key_mlp is None:
        print("   ⚠️  Could not build specific examples figure (missing KNN n=1 or MLP [150,50] key)")
        return False

    examples = [key_knn, key_mlp]
    exp_disp = display_experiment_name(exp_name)

    fig, axes = plt.subplots(2, 2, figsize=(24, 12), sharex=False)

    for ci, model_hp_key in enumerate(examples):
        subject_accuracies = model_hp_subject_accuracies[model_hp_key]
        subjects, success_rates, mean_accs, colors = _prepare_subject_series(subject_accuracies)
        if not subjects:
            continue

        ax1 = axes[0, ci]
        ax2 = axes[1, ci]

        # Top: success rate
        ax1.bar(range(len(subjects)), success_rates, color=colors, edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
        ax1.set_ylabel('% Correctly Classified', fontsize=13, fontweight='bold')
        ax1.set_title(
            f'{exp_disp}\n{model_hp_key}\nPer-Subject Classification Success Rate\n(% of folds where accuracy > 50%)',
            fontsize=15, fontweight='bold', pad=20
        )
        ax1.set_xticks(range(len(subjects)))
        ax1.set_xticklabels(subjects, rotation=45, ha='right', fontsize=9)
        ax1.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.set_ylim(0, 105)

        legend_elements = [
            mpatches.Patch(facecolor='#90EE90', alpha=0.7, edgecolor='black', label='100% Success'),
            mpatches.Patch(facecolor='#FFD700', alpha=0.7, edgecolor='black', label='Partial Success'),
            mpatches.Patch(facecolor='#FFB6C1', alpha=0.7, edgecolor='black', label='0% Success'),
        ]
        ax1.legend(
            handles=legend_elements + [plt.Line2D([0], [0], color='red', linestyle='--', label='50% Threshold')],
            loc='upper right', fontsize=10
        )

        # Bottom: mean accuracy
        ax2.bar(range(len(subjects)), mean_accs, color=colors, edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
        ax2.set_ylabel('Mean Accuracy (%)', fontsize=13, fontweight='bold')
        ax2.set_title(
            f'{exp_disp}\n{model_hp_key}\nPer-Subject Mean Accuracy Across All Folds',
            fontsize=15, fontweight='bold', pad=20
        )
        ax2.set_xticks(range(len(subjects)))
        ax2.set_xticklabels(subjects, rotation=45, ha='right', fontsize=9)
        ax2.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.legend(fontsize=11)
        ax2.set_ylim(0, 105)

    plt.tight_layout()
    output_file = output_dir / f'{exp_name}_per_subject_success_rate_specific_examples.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   ✅ Saved: {output_file.name}")
    return True

def create_ftest_vs_pca_combined_plot(model_hp_ftest, model_hp_pca, output_dir):
    """
    Create a 2x2 combined figure comparing F-test vs PCA for a specific model×HP.
    Left column: F-test
    Right column: PCA
    Rows: Success Rate (top), Mean Accuracy (bottom)
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
    print(f"   ✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis" / "success_rate_plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ftest_model_hp_data = {}
    pca_model_hp_data = {}
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        # Load per-subject accuracies grouped by model×HP
        model_hp_subject_accuracies = load_per_subject_accuracies_by_model_hp(exp_name, results_dir)
        
        if not model_hp_subject_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found {len(model_hp_subject_accuracies)} model×HP combinations")
        
        # Create plot for each model×HP combination
        for model_hp_key, subject_accuracies in sorted(model_hp_subject_accuracies.items()):
            create_per_subject_success_rate_plot_for_model_hp(
                exp_name, model_hp_key, subject_accuracies, output_dir
            )

        # Also create a combined specific-examples figure for ANOVA_L_6_Random
        if exp_name == "ANOVA_L_6_Random":
            create_specific_examples_combined_plot(
                exp_name, model_hp_subject_accuracies, output_dir
            )
            # Store for F-test vs PCA comparison
            ftest_model_hp_data = model_hp_subject_accuracies
        
        # Store PCA data for F-test vs PCA comparison
        if exp_name == "PCA_L_6_Random":
            pca_model_hp_data = model_hp_subject_accuracies
    
    # Create F-test vs PCA combined figure
    if ftest_model_hp_data and pca_model_hp_data:
        # Find KNN n_neighbors=1 keys for both experiments
        key_knn_ftest = next(
            (k for k in ftest_model_hp_data.keys()
             if k.startswith('KNN') and 'n_neighbors=1' in k and 'metric=euclidean' in k),
            None
        )
        key_knn_pca = next(
            (k for k in pca_model_hp_data.keys()
             if k.startswith('KNN') and 'n_neighbors=1' in k and 'metric=euclidean' in k),
            None
        )
        
        if key_knn_ftest and key_knn_pca:
            print(f"\n📊 Creating F-test vs PCA combined figure for L_6_Random...")
            create_ftest_vs_pca_combined_plot(
                ftest_model_hp_data[key_knn_ftest],
                pca_model_hp_data[key_knn_pca],
                output_dir
            )
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()


