#!/usr/bin/env python
"""
Create Figure 4: Variance vs Hold-Out Size (P) - Multi-Model Small Multiples
2x2 grid combining PCA and ANOVA for both P=6 and P=2.

Layout:
- Top-left: PCA P=6 (Random-50 LPSO)
- Top-right: PCA P=2 (Random-50 LPSO)
- Bottom-left: ANOVA P=6 (Random-50 LPSO)
- Bottom-right: ANOVA P=2 (Random-50 LPSO)

Each panel shows 4 boxplots (one per model) + scatter dots of all folds.
Shows that variance inflation at P=2 is consistent across all models and feature sets.

Data: all_experiments_combined.csv — best-HP per model (HP with highest median
across 50 folds), giving n=50 per model per panel.  Consistent with Table 2.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

# Set random seed for reproducible jitter
np.random.seed(42)

# Set up paths
BASE_DIR   = Path(__file__).parent
DATA_CSV   = BASE_DIR / "all_experiments_combined.csv"
OUTPUT_DIR = BASE_DIR / "LPSO_Box_Plots"
OUTPUT_DIR.mkdir(exist_ok=True)

# CSV experiment name → panel key
EXPERIMENT_MAP = {
    'PCA_P6':   'PCA_L_6_Random',
    'PCA_P2':   'PCA_L_2_Random',
    'ANOVA_P6': 'ANOVA_L_6_Random',
    'ANOVA_P2': 'ANOVA_L_2_Random',
}

# Model order and colors (consistent with existing graphs)
MODEL_ORDER = ['MLP', 'XGBoost', 'SVM', 'KNN']

# Model colors (consistent with existing graphs)
MODEL_COLORS = {
    'MLP': '#1f77b4',      # Blue
    'XGBoost': '#ff7f0e',  # Orange
    'SVM': '#2ca02c',      # Green
    'KNN': '#d62728',      # Red
}


def load_best_hp_data(df_lpso: pd.DataFrame, exp_name: str) -> Dict[str, List[float]]:
    """
    For each model in the given experiment, select the HP configuration with the
    highest median test_accuracy across 50 folds, then return those 50 values.

    Returns:
        Dictionary mapping model_name -> list of 50 fold accuracies (best-HP only)
    """
    sub    = df_lpso[df_lpso["experiment"] == exp_name]
    result = {}
    for model in MODEL_ORDER:
        m = sub[sub["model"] == model]
        if m.empty:
            print(f"   ⚠️  {model}: no data")
            continue
        best_hp = m.groupby("hyperparams")["test_accuracy"].median().idxmax()
        vals    = m[m["hyperparams"] == best_hp]["test_accuracy"].tolist()
        result[model] = vals
        print(f"   ✅ {model}: n={len(vals)}  median={np.median(vals):.3f}")
    return result


def create_single_panel(
    ax,
    data: Dict[str, List[float]],
    title: str,
    ylim: Tuple[float, float] = (0.0, 1.0)
) -> None:
    """
    Create a single panel with boxplots for all models.
    
    Args:
        ax: Matplotlib axis object
        data: Dictionary mapping model_name -> list of fold accuracies
        title: Panel title
        ylim: Y-axis limits
    """
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
            if max_distance > 0:
                normalized_distances = distances_from_mean / max_distance
                jitter_scales = 1.0 / (1.0 + 2.0 * normalized_distances)
            else:
                jitter_scales = np.ones(len(values))
            
            # Base jitter (same as LPSO script)
            base_jitter_std = 0.03
            jitter = np.random.normal(0, base_jitter_std, len(values)) * jitter_scales
            x_positions = pos + jitter
            
            # Use model color for dots
            color = MODEL_COLORS.get(model, '#666666')
            ax.scatter(x_positions, values, alpha=0.5, s=15, color=color, 
                      edgecolors='black', linewidth=0.5, zorder=10)
    
    # Add horizontal baseline at 0.5
    ax.axhline(y=0.5, color='red', linestyle=':', alpha=0.5, linewidth=1)
    
    # Customize axes
    ax.set_ylabel('Subject-Level Accuracy', fontsize=11, fontweight='bold')
    ax.set_ylim(ylim)
    ax.set_xlim(-0.5, len(MODEL_ORDER) - 0.5)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Set subplot title
    ax.set_title(title, fontsize=12, fontweight='bold', pad=8)


def create_figure4_2x2_grid(
    all_data: Dict[str, Dict[str, List[float]]],
    output_path: Path,
    ylim: Tuple[float, float] = (0.0, 1.0)
) -> None:
    """
    Create Figure 4: 2x2 grid showing variance vs hold-out size (P) for both PCA and ANOVA
    
    Layout:
    - Top-left: PCA P=6
    - Top-right: PCA P=2
    - Bottom-left: ANOVA P=6
    - Bottom-right: ANOVA P=2
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Define panel positions
    panels = {
        'PCA_P6': axes[0, 0],   # Top-left
        'PCA_P2': axes[0, 1],   # Top-right
        'ANOVA_P6': axes[1, 0],  # Bottom-left
        'ANOVA_P2': axes[1, 1],  # Bottom-right
    }
    
    # Panel titles
    panel_titles = {
        'PCA_P6': 'PCA — P=6 (Random-50 LPSO)',
        'PCA_P2': 'PCA — P=2 (Random-50 LPSO)',
        'ANOVA_P6': 'F-test — P=6 (Random-50 LPSO)',
        'ANOVA_P2': 'F-test — P=2 (Random-50 LPSO)',
    }
    
    for exp_key, ax in panels.items():
        if exp_key not in all_data:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            continue
        
        data = all_data[exp_key]
        title = panel_titles.get(exp_key, exp_key)
        create_single_panel(ax, data, title, ylim)
    

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"   ✅ Saved: {output_path.name}")


def main():
    """Main function to generate Figure 4."""
    print("=" * 80)
    print("FIGURE 4: Variance vs Hold-Out Size (P) - 2x2 Grid (PCA + ANOVA)")
    print("  Data: all_experiments_combined.csv — best-HP per model (n=50 per panel)")
    print("=" * 80)
    print()

    df    = pd.read_csv(DATA_CSV)
    lpso  = df[df["experiment_type"] == "LPSO_Random_50"].copy()

    all_data = {}
    for exp_key, exp_name in EXPERIMENT_MAP.items():
        print(f"\n📊 {exp_key}  ({exp_name}):")
        data = load_best_hp_data(lpso, exp_name)
        if data:
            all_data[exp_key] = data
        else:
            print(f"   ⚠️  No data loaded")

    print("\n" + "=" * 80)
    print("Generating Figure 4 (2x2 Grid)...")
    print("-" * 80)

    figure4_path = OUTPUT_DIR / "Figure4_Variance_vs_HoldOut_Size.png"
    create_figure4_2x2_grid(all_data, figure4_path)

    print("\n" + "=" * 80)
    print("✅ Figure 4 generated successfully!")
    print(f"📁 Output: {figure4_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
