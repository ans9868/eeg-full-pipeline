#!/usr/bin/env python
"""
Create box plots comparing 12-fold LPSO (Systematic) vs 50-fold LPSO (Random)
for PCA_L_6 and ANOVA_L_6 experiments.

Generates:
- Individual box plots for each feature set × strategy combination
- Combined 2x2 grid plot showing all combinations
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# Set random seed for reproducible jitter
np.random.seed(42)

# Set up paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "LPSO_Box_Plots"
OUTPUT_DIR.mkdir(exist_ok=True)

# Experiment paths
EXPERIMENTS = {
    'PCA_Systematic-12': BASE_DIR / 'grid_12_folds' / 'PCA_L_6_C-3' / 'ml_results_grid_search',
    'PCA_Random-50': BASE_DIR / 'grid_50_random_folds' / 'PCA_L_6_ml_results',
    'ANOVA_Systematic-12': BASE_DIR / 'grid_12_folds' / 'ANOVA_L_6_C_Resource_Boosted' / 'ml_results_grid_search',
    'ANOVA_Random-50': BASE_DIR / 'grid_50_random_folds' / 'ANOVA_L_6_complete',
}

# Model name normalization and fixed order
MODEL_ORDER = ['MLP', 'XGBoost', 'SVM', 'KNN']
MODEL_NAME_MAP = {
    'MLP (Neural Network)': 'MLP',
    'MLP_(Neural_Network)': 'MLP',
    'XGBoost': 'XGBoost',
    'SVM': 'SVM',
    'KNN': 'KNN',
}

# Model colors (consistent with existing graphs)
MODEL_COLORS = {
    'MLP': '#1f77b4',      # Blue
    'XGBoost': '#ff7f0e',  # Orange
    'SVM': '#2ca02c',      # Green
    'KNN': '#d62728',      # Red
}


def normalize_model_name(model_name: str) -> str:
    """Normalize model name to standard format."""
    # Remove underscores and normalize
    normalized = model_name.replace('_', ' ').strip()
    return MODEL_NAME_MAP.get(normalized, normalized)


def extract_fold_performances(experiment_path: Path) -> Dict[str, List[float]]:
    """
    Extract per-fold test accuracies from experiment for each model.
    
    Returns:
        Dictionary mapping model_name -> list of fold accuracies
    """
    fold_performances = {}
    
    # Check if ml_results_grid_search subdirectory exists
    if (experiment_path / 'ml_results_grid_search').exists():
        ml_results_path = experiment_path / 'ml_results_grid_search'
    else:
        ml_results_path = experiment_path
    
    if not ml_results_path.exists():
        print(f"   ⚠️  Path does not exist: {ml_results_path}")
        return fold_performances
    
    # Get all model directories
    model_dirs = [d for d in ml_results_path.iterdir() 
                  if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    for model_dir in model_dirs:
        model_name_raw = model_dir.name
        model_name = normalize_model_name(model_name_raw)
        
        # Skip if not in our target models
        if model_name not in MODEL_ORDER:
            continue
        
        accuracies = []
        
        # Try reading from detailed_results.json first (has all fold results)
        detailed_results = model_dir / "detailed_results.json"
        
        if detailed_results.exists():
            try:
                with open(detailed_results, 'r') as f:
                    data = json.load(f)
                    
                # Look for all_hyperparameter_results with fold_results
                if 'all_hyperparameter_results' in data:
                    for hp_result in data['all_hyperparameter_results']:
                        if 'fold_results' in hp_result:
                            for fold_result in hp_result['fold_results']:
                                if 'test_results' in fold_result and 'accuracy' in fold_result['test_results']:
                                    accuracies.append(fold_result['test_results']['accuracy'])
            except Exception as e:
                print(f"   Warning: Could not read {detailed_results}: {e}")
        
        # Fallback: Get all fold directories (sub-XXX_sub-YYY pattern) and read results.json
        if not accuracies:
            fold_dirs = [d for d in model_dir.iterdir() 
                        if d.is_dir() and ("sub-" in d.name or d.name.isdigit())]
            
            for fold_dir in fold_dirs:
                # Look for results.json in fold directory
                results_json = fold_dir / "results.json"
                
                if results_json.exists():
                    try:
                        with open(results_json, 'r') as f:
                            data = json.load(f)
                            acc = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                            if acc is not None:
                                accuracies.append(float(acc))
                    except Exception as e:
                        pass
        
        # Also try loading from any subdirectory recursively
        if not accuracies:
            results_files = list(model_dir.rglob("results.json"))
            for results_file in results_files:
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                        acc = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                        if acc is not None:
                            accuracies.append(float(acc))
                except:
                    pass
        
        if accuracies:
            fold_performances[model_name] = accuracies
            print(f"   ✅ {model_name}: {len(accuracies)} folds")
        else:
            print(f"   ⚠️  {model_name}: No fold data found")
    
    return fold_performances


def create_single_box_plot(
    data: Dict[str, List[float]], 
    title: str, 
    output_path: Path,
    ylim: Tuple[float, float] = (0.0, 1.0)
) -> None:
    """
    Create a single box plot showing accuracy distributions for each model.
    
    Args:
        data: Dictionary mapping model_name -> list of fold accuracies
        title: Plot title
        output_path: Path to save the plot
        ylim: Y-axis limits
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data in fixed model order
    box_data = []
    labels = []
    positions = []
    
    for i, model in enumerate(MODEL_ORDER):
        if model in data:
            box_data.append(data[model])
            labels.append(model)
            positions.append(i)
    
    if not box_data:
        print(f"   ⚠️  No data to plot for {title}")
        plt.close(fig)
        return
    
    # Create box plot (with showfliers=False since we'll add all points manually)
    bp = ax.boxplot(
        box_data, 
        positions=positions,
        tick_labels=labels,
        patch_artist=True,
        showmeans=False,
        showfliers=False,  # We'll show all points manually
        widths=0.6
    )
    
    # Color the boxes
    for patch, model in zip(bp['boxes'], labels):
        color = MODEL_COLORS.get(model, '#666666')
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1.2)
    
    # Style the whiskers and medians
    for element in ['whiskers', 'means', 'medians', 'caps']:
        for item in bp[element]:
            item.set_color('black')
            item.set_linewidth(1.2)
    
    # Add individual data points (dots) with adaptive jitter
    for i, (model, pos) in enumerate(zip(labels, positions)):
        values = np.array(box_data[i])
        mean_val = np.mean(values)
        
        # Calculate distance from mean for each point
        distances_from_mean = np.abs(values - mean_val)
        max_distance = np.max(distances_from_mean) if len(distances_from_mean) > 0 else 1.0
        
        # Scale jitter inversely with distance from mean
        # Points near mean get more jitter, points on tails get less
        # Normalize distances to 0-1 range, then invert (closer to mean = higher scale)
        if max_distance > 0:
            normalized_distances = distances_from_mean / max_distance
            # Jitter scale: 1.0 for points at mean, decreasing as distance increases
            # Use a function like 1 / (1 + normalized_distance) to ensure tails have less jitter
            jitter_scales = 1.0 / (1.0 + 2.0 * normalized_distances)  # Tails get ~0.33x jitter, mean gets 1.0x
        else:
            jitter_scales = np.ones(len(values))
        
        # Base jitter (reduced by 40%: 0.05 * 0.6 = 0.03)
        base_jitter_std = 0.03
        jitter = np.random.normal(0, base_jitter_std, len(values)) * jitter_scales
        x_positions = pos + jitter
        # Use slightly darker version of model color for dots
        color = MODEL_COLORS.get(model, '#666666')
        ax.scatter(x_positions, values, alpha=0.5, s=20, color=color, edgecolors='black', linewidth=0.5, zorder=10)
    
    # Add horizontal baseline at 0.5
    ax.axhline(y=0.5, color='red', linestyle=':', alpha=0.5, linewidth=1, label='Baseline (0.5)')
    
    # Customize axes
    ax.set_ylabel('Accuracy', fontsize=14, fontweight='bold')
    ax.set_xlabel('Model', fontsize=14, fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylim(ylim)
    ax.set_xlim(-0.5, len(MODEL_ORDER) - 0.5)  # Set x-axis limits
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"   ✅ Saved: {output_path.name}")


def create_combined_grid_plot(
    all_data: Dict[str, Dict[str, List[float]]],
    output_path: Path,
    ylim: Tuple[float, float] = (0.0, 1.0)
) -> None:
    """
    Create a 2x2 grid plot showing all combinations.
    
    Layout:
    - Row 1: F-test (left: Systematic-12, right: Random-50)
    - Row 2: PCA (left: Systematic-12, right: Random-50)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Define subplot positions
    subplots = {
        'ANOVA_Systematic-12': axes[0, 0],
        'ANOVA_Random-50': axes[0, 1],
        'PCA_Systematic-12': axes[1, 0],
        'PCA_Random-50': axes[1, 1],
    }
    
    # Row and column labels
    row_labels = ['F-test', 'PCA']
    col_labels = ['Systematic-12', 'Random-50']
    
    for exp_key, ax in subplots.items():
        if exp_key not in all_data:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            continue
        
        data = all_data[exp_key]
        
        # Prepare data in fixed model order
        box_data = []
        labels = []
        positions = []
        
        for i, model in enumerate(MODEL_ORDER):
            if model in data:
                box_data.append(data[model])
                labels.append(model)
                positions.append(i)
        
        if box_data:
            # Create box plot (with showfliers=False since we'll add all points manually)
            bp = ax.boxplot(
                box_data,
                positions=positions,
                tick_labels=labels,
                patch_artist=True,
                showmeans=False,
                showfliers=False,  # We'll show all points manually
                widths=0.6
            )
            
            # Color the boxes
            for patch, model in zip(bp['boxes'], labels):
                color = MODEL_COLORS.get(model, '#666666')
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
                patch.set_edgecolor('black')
                patch.set_linewidth(1.2)
            
            # Style the whiskers and medians
            for element in ['whiskers', 'means', 'medians', 'caps']:
                for item in bp[element]:
                    item.set_color('black')
                    item.set_linewidth(1.2)
            
            # Add individual data points (dots) with adaptive jitter
            for i, (model, pos) in enumerate(zip(labels, positions)):
                values = np.array(box_data[i])
                mean_val = np.mean(values)
                
                # Calculate distance from mean for each point
                distances_from_mean = np.abs(values - mean_val)
                max_distance = np.max(distances_from_mean) if len(distances_from_mean) > 0 else 1.0
                
                # Scale jitter inversely with distance from mean
                # Points near mean get more jitter, points on tails get less
                # Normalize distances to 0-1 range, then invert (closer to mean = higher scale)
                if max_distance > 0:
                    normalized_distances = distances_from_mean / max_distance
                    # Jitter scale: 1.0 for points at mean, decreasing as distance increases
                    # Use a function like 1 / (1 + normalized_distance) to ensure tails have less jitter
                    jitter_scales = 1.0 / (1.0 + 2.0 * normalized_distances)  # Tails get ~0.33x jitter, mean gets 1.0x
                else:
                    jitter_scales = np.ones(len(values))
                
                # Base jitter (reduced by 40%: 0.05 * 0.6 = 0.03)
                base_jitter_std = 0.03
                jitter = np.random.normal(0, base_jitter_std, len(values)) * jitter_scales
                x_positions = pos + jitter
                # Use slightly darker version of model color for dots
                color = MODEL_COLORS.get(model, '#666666')
                ax.scatter(x_positions, values, alpha=0.5, s=15, color=color, edgecolors='black', linewidth=0.5, zorder=10)
        
        # Add horizontal baseline at 0.5
        ax.axhline(y=0.5, color='red', linestyle=':', alpha=0.5, linewidth=1)
        
        # Customize axes
        ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
        ax.set_ylim(ylim)
        ax.set_xlim(-0.5, len(MODEL_ORDER) - 0.5)  # Set x-axis limits
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Set subplot title
        feature_set = 'PCA' if 'PCA' in exp_key else 'F-test'
        strategy = 'Systematic-12' if 'Systematic' in exp_key else 'Random-50'
        ax.set_title(f'{feature_set} — {strategy}', fontsize=13, fontweight='bold', pad=10)
    
    # Add row and column labels
    fig.text(0.02, 0.5, 'Feature Set', rotation=90, ha='center', va='center', fontsize=14, fontweight='bold')
    fig.text(0.5, 0.02, 'Strategy', ha='center', va='center', fontsize=14, fontweight='bold')
    
    plt.tight_layout(rect=[0.03, 0.03, 0.97, 0.95])
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"   ✅ Saved: {output_path.name}")


def main():
    """Main function to generate all box plots."""
    print("=" * 80)
    print("LPSO BOX PLOTS: Systematic-12 vs Random-50")
    print("=" * 80)
    print()
    
    # Extract fold performances for all experiments
    all_data = {}
    
    print("Loading fold data from experiments...")
    print("-" * 80)
    
    for exp_key, exp_path in EXPERIMENTS.items():
        print(f"\n📊 {exp_key}:")
        print(f"   Path: {exp_path}")
        
        if not exp_path.exists():
            print(f"   ❌ Path does not exist!")
            continue
        
        fold_perfs = extract_fold_performances(exp_path)
        if fold_perfs:
            all_data[exp_key] = fold_perfs
            total_folds = sum(len(accs) for accs in fold_perfs.values())
            print(f"   ✅ Loaded {len(fold_perfs)} models, {total_folds} total folds")
        else:
            print(f"   ⚠️  No fold data extracted")
    
    print("\n" + "=" * 80)
    print("Generating plots...")
    print("-" * 80)
    
    # Generate individual plots
    print("\n📊 Generating individual plots...")
    for exp_key, data in all_data.items():
        # Create title
        feature_set = 'PCA' if 'PCA' in exp_key else 'F-test'
        strategy = 'Systematic-12' if 'Systematic' in exp_key else 'Random-50'
        title = f"{feature_set} — {strategy}"
        
        filename = f"{exp_key.replace('-', '_')}.png"
        output_path = OUTPUT_DIR / filename
        
        create_single_box_plot(data, title, output_path)
    
    # Generate combined grid plot
    print("\n📊 Generating combined grid plot...")
    combined_path = OUTPUT_DIR / "LPSO_Systematic_vs_Random_Combined.png"
    create_combined_grid_plot(all_data, combined_path)
    
    print("\n" + "=" * 80)
    print("✅ All plots generated successfully!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()

