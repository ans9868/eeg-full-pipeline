#!/usr/bin/env python3
"""
Visualize top biomarkers and their distributions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Set style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def load_data():
    """Load the exploration results."""
    data_dir = Path(__file__).parent
    df = pd.read_csv(data_dir / 'full_data_with_features.csv')
    interesting = pd.read_csv(data_dir / 'interesting_features_mapped.csv')
    feature_mapping = pd.read_csv(data_dir / 'feature_mapping.csv')
    return df, interesting, feature_mapping

def get_feature_name(feature_col, feature_mapping_df):
    """Get actual feature name (channel×band) from feature column name."""
    # Extract feature index from column name like "feature_38"
    if feature_col.startswith('feature_'):
        feat_idx = int(feature_col.split('_')[1])
        mapping = feature_mapping_df[feature_mapping_df['feature_index'] == feat_idx]
        if len(mapping) > 0:
            row = mapping.iloc[0]
            if row['feature_type'] == 'relative_band_power':
                return f"{row['channel_name']} × {row['band_name']}"
            elif row['feature_type'] == 'band_power':
                return f"{row['channel_name']} (all bands)"
            else:
                return f"{row['channel_name']} × {row['band_name']}"
    return feature_col

def plot_top_biomarkers(df, interesting_df, feature_mapping_df, n_top=10):
    """Plot distributions of top biomarkers."""
    top_features = interesting_df.head(n_top)['feature'].tolist()
    
    fig, axes = plt.subplots(2, 5, figsize=(20, 10))
    axes = axes.flatten()
    
    for idx, feature in enumerate(top_features):
        ax = axes[idx]
        
        # Get stats
        stats = interesting_df[interesting_df['feature'] == feature].iloc[0]
        
        # Get actual feature name
        feature_name = get_feature_name(feature, feature_mapping_df)
        
        # Plot distributions
        alz_data = df[df['Group'] == 'alz'][feature]
        cntrl_data = df[df['Group'] == 'cntrl'][feature]
        
        ax.hist(alz_data, bins=50, alpha=0.6, label='Alzheimer\'s', color='red', density=True)
        ax.hist(cntrl_data, bins=50, alpha=0.6, label='Control', color='blue', density=True)
        
        # Add means
        ax.axvline(stats['group1_mean'], color='red', linestyle='--', linewidth=2, label=f"Alz mean: {stats['group1_mean']:.3f}")
        ax.axvline(stats['group2_mean'], color='blue', linestyle='--', linewidth=2, label=f"Cntrl mean: {stats['group2_mean']:.3f}")
        
        ax.set_title(f"{feature_name}\nCohen's d={stats['cohens_d']:.3f}, Rel diff={stats['rel_diff_pct']:.1f}%", 
                    fontsize=10, fontweight='bold')
        ax.set_xlabel('Feature Value')
        ax.set_ylabel('Density')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle(f'Top {n_top} Biomarkers: Distribution Comparison', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig

def plot_effect_sizes(interesting_df, feature_mapping_df, n_top=20):
    """Plot effect sizes (Cohen's d) for top features."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    top_n = interesting_df.head(n_top)
    
    colors = ['red' if row['group1_mean'] < row['group2_mean'] else 'green' 
              for _, row in top_n.iterrows()]
    
    # Get actual feature names
    feature_names = [get_feature_name(f, feature_mapping_df) for f in top_n['feature']]
    
    y_pos = np.arange(len(top_n))
    bars = ax.barh(y_pos, top_n['cohens_d'], color=colors, alpha=0.7)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(feature_names, fontsize=10)
    ax.set_xlabel("Cohen's d (Effect Size)", fontsize=12, fontweight='bold')
    ax.set_title(f'Top {n_top} Biomarkers by Effect Size', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (idx, row) in enumerate(top_n.iterrows()):
        ax.text(row['cohens_d'] + 0.01, i, f"{row['cohens_d']:.3f}", 
               va='center', fontsize=9)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.7, label='Reduced in Alzheimer\'s'),
        Patch(facecolor='green', alpha=0.7, label='Elevated in Alzheimer\'s')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    return fig

def plot_feature_correlation_heatmap(df, interesting_df, feature_mapping_df, n_top=15):
    """Plot correlation heatmap of top biomarkers."""
    top_features = interesting_df.head(n_top)['feature'].tolist()
    
    # Get actual feature names
    feature_names = [get_feature_name(f, feature_mapping_df) for f in top_features]
    
    # Calculate correlation
    corr = df[top_features].corr()
    
    fig, ax = plt.subplots(figsize=(14, 12))
    im = ax.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Correlation', fontsize=10)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(top_features)))
    ax.set_yticks(np.arange(len(top_features)))
    ax.set_xticklabels(feature_names, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(feature_names, fontsize=9)
    
    # Add text annotations
    for i in range(len(top_features)):
        for j in range(len(top_features)):
            text = ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=7)
    
    ax.set_title(f'Correlation Matrix: Top {n_top} Biomarkers', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_group_comparison_boxplot(df, interesting_df, feature_mapping_df, n_top=10):
    """Plot boxplots comparing groups for top biomarkers."""
    top_features = interesting_df.head(n_top)['feature'].tolist()
    
    # Get actual feature names
    feature_names = [get_feature_name(f, feature_mapping_df) for f in top_features]
    
    # Prepare data for plotting
    plot_data = []
    for feature in top_features:
        for group in ['alz', 'cntrl']:
            values = df[df['Group'] == group][feature]
            for val in values.sample(min(1000, len(values))):  # Sample for performance
                plot_data.append({'feature': feature, 'group': group, 'value': val})
    
    plot_df = pd.DataFrame(plot_data)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create boxplot manually
    positions = np.arange(len(top_features))
    width = 0.35
    
    for i, feature in enumerate(top_features):
        alz_data = plot_df[(plot_df['feature'] == feature) & (plot_df['group'] == 'alz')]['value']
        cntrl_data = plot_df[(plot_df['feature'] == feature) & (plot_df['group'] == 'cntrl')]['value']
        
        bp1 = ax.boxplot([alz_data], positions=[i - width/2], widths=width, 
                        patch_artist=True, labels=[''] if i > 0 else ['Alz'])
        bp2 = ax.boxplot([cntrl_data], positions=[i + width/2], widths=width,
                        patch_artist=True, labels=[''] if i > 0 else ['Cntrl'])
        
        for patch in bp1['boxes']:
            patch.set_facecolor('red')
            patch.set_alpha(0.7)
        for patch in bp2['boxes']:
            patch.set_facecolor('blue')
            patch.set_alpha(0.7)
    
    ax.set_xticks(positions)
    ax.set_xticklabels(feature_names, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Feature Value', fontsize=12)
    ax.set_title(f'Top {n_top} Biomarkers: Group Comparison (Boxplots)', fontsize=14, fontweight='bold')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.7, label='Alzheimer\'s'),
        Patch(facecolor='blue', alpha=0.7, label='Control')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    return fig

def main():
    """Generate all visualizations."""
    print("📊 Loading data...")
    df, interesting_df, feature_mapping_df = load_data()
    
    output_dir = Path(__file__).parent
    print(f"💾 Saving visualizations to {output_dir}...")
    
    # Plot 1: Top biomarkers distributions
    print("   Creating distribution plots...")
    fig1 = plot_top_biomarkers(df, interesting_df, feature_mapping_df, n_top=10)
    fig1.savefig(output_dir / 'top_10_biomarkers_distributions.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved top_10_biomarkers_distributions.png")
    
    # Plot 2: Effect sizes
    print("   Creating effect size plot...")
    fig2 = plot_effect_sizes(interesting_df, feature_mapping_df, n_top=20)
    fig2.savefig(output_dir / 'biomarker_effect_sizes.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved biomarker_effect_sizes.png")
    
    # Plot 3: Correlation heatmap
    print("   Creating correlation heatmap...")
    fig3 = plot_feature_correlation_heatmap(df, interesting_df, feature_mapping_df, n_top=15)
    fig3.savefig(output_dir / 'biomarker_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved biomarker_correlation_heatmap.png")
    
    # Plot 4: Boxplots
    print("   Creating boxplots...")
    fig4 = plot_group_comparison_boxplot(df, interesting_df, feature_mapping_df, n_top=10)
    fig4.savefig(output_dir / 'biomarker_boxplots.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved biomarker_boxplots.png")
    
    print("\n✅ All visualizations complete!")

if __name__ == '__main__':
    main()

