#!/usr/bin/env python3
"""
Create two key plots:
1. Posterior channels alpha boxplots (O1, O2, T5, T6, Pz)
2. Stacked relative bands at O1 and O2 for both groups
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Set style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def load_data():
    """Load data and feature mapping."""
    data_dir = Path(__file__).parent
    df = pd.read_csv(data_dir / 'full_data_with_features.csv')
    feature_mapping = pd.read_csv(data_dir / 'feature_mapping.csv')
    return df, feature_mapping

def get_feature_name(channel, band, feature_mapping_df):
    """Get feature column name from channel and band."""
    mapping = feature_mapping_df[
        (feature_mapping_df['channel_name'] == channel) & 
        (feature_mapping_df['band_name'] == band) &
        (feature_mapping_df['feature_type'] == 'relative_band_power')
    ]
    if len(mapping) > 0:
        return mapping.iloc[0]['feature_name']
    return None

def plot_posterior_alpha_boxplots(df, feature_mapping_df):
    """Plot boxplots of Alpha band in posterior channels."""
    print("📊 Creating posterior Alpha boxplots...")
    
    # Get posterior channels and Alpha features
    posterior_channels = ['O1', 'O2', 'T5', 'T6', 'Pz']
    features = []
    feature_labels = []
    
    for channel in posterior_channels:
        feat_name = get_feature_name(channel, 'Alpha', feature_mapping_df)
        if feat_name:
            features.append(feat_name)
            feature_labels.append(f'{channel} × Alpha')
    
    # Prepare data
    plot_data = []
    for feature, label in zip(features, feature_labels):
        for group in ['alz', 'cntrl']:
            values = df[df['Group'] == group][feature]
            # Sample for performance if too many
            if len(values) > 5000:
                values = values.sample(5000, random_state=42)
            for val in values:
                plot_data.append({
                    'Feature': label,
                    'Group': 'Alzheimer\'s' if group == 'alz' else 'Control',
                    'Value': val
                })
    
    plot_df = pd.DataFrame(plot_data)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create boxplot
    positions = np.arange(len(feature_labels))
    width = 0.35
    
    for i, label in enumerate(feature_labels):
        alz_data = plot_df[(plot_df['Feature'] == label) & (plot_df['Group'] == 'Alzheimer\'s')]['Value']
        cntrl_data = plot_df[(plot_df['Feature'] == label) & (plot_df['Group'] == 'Control')]['Value']
        
        bp1 = ax.boxplot([alz_data], positions=[i - width/2], widths=width, 
                        patch_artist=True)
        bp2 = ax.boxplot([cntrl_data], positions=[i + width/2], widths=width,
                        patch_artist=True)
        
        for patch in bp1['boxes']:
            patch.set_facecolor('red')
            patch.set_alpha(0.7)
        for patch in bp2['boxes']:
            patch.set_facecolor('blue')
            patch.set_alpha(0.7)
    
    ax.set_xticks(positions)
    ax.set_xticklabels(feature_labels, rotation=0, fontsize=11)
    ax.set_ylabel('Relative Alpha Power', fontsize=12, fontweight='bold')
    ax.set_title('Posterior Channels: Alpha Band Relative Power', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.7, label='Alzheimer\'s'),
        Patch(facecolor='blue', alpha=0.7, label='Control')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    return fig

def plot_stacked_relative_bands(df, feature_mapping_df):
    """Plot stacked relative bandpower at O1 and O2 for both groups."""
    print("📊 Creating stacked relative bands plot...")
    
    channels = ['O1', 'O2']
    bands = ['Delta', 'Theta', 'Alpha', 'Beta']
    
    # Aggregate by subject and group
    subject_data = df.groupby(['SubjectID', 'Group']).agg({
        **{get_feature_name(ch, band, feature_mapping_df): 'mean' 
           for ch in channels for band in bands if get_feature_name(ch, band, feature_mapping_df)}
    }).reset_index()
    
    # Calculate group means
    group_means = {}
    for group in ['alz', 'cntrl']:
        group_data = subject_data[subject_data['Group'] == group]
        group_means[group] = {}
        for ch in channels:
            group_means[group][ch] = {}
            for band in bands:
                feat_name = get_feature_name(ch, band, feature_mapping_df)
                if feat_name and feat_name in group_data.columns:
                    group_means[group][ch][band] = group_data[feat_name].mean()
                else:
                    group_means[group][ch][band] = 0
    
    # Create stacked bar plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    
    band_colors = {
        'Delta': '#1f77b4',  # blue
        'Theta': '#ff7f0e',  # orange
        'Alpha': '#2ca02c',  # green
        'Beta': '#d62728'    # red
    }
    
    for idx, ch in enumerate(channels):
        ax = axes[idx]
        
        # Prepare data for stacking
        alz_values = [group_means['alz'][ch][band] for band in bands]
        cntrl_values = [group_means['cntrl'][ch][band] for band in bands]
        
        x_pos = [0, 1]
        width = 0.6
        
        # Stack bars
        bottom_alz = 0
        bottom_cntrl = 0
        
        for i, band in enumerate(bands):
            ax.bar(0, alz_values[i], width, bottom=bottom_alz, 
                  label=band if idx == 0 else '', color=band_colors[band], alpha=0.8)
            ax.bar(1, cntrl_values[i], width, bottom=bottom_cntrl,
                  color=band_colors[band], alpha=0.8)
            bottom_alz += alz_values[i]
            bottom_cntrl += cntrl_values[i]
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(['Alzheimer\'s', 'Control'], fontsize=11)
        ax.set_ylabel('Relative Power', fontsize=12, fontweight='bold')
        ax.set_title(f'{ch} Channel: Relative Band Power', fontsize=13, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        y_pos_alz = 0
        y_pos_cntrl = 0
        for i, band in enumerate(bands):
            y_pos_alz += alz_values[i] / 2
            y_pos_cntrl += cntrl_values[i] / 2
            if alz_values[i] > 0.05:
                ax.text(0, y_pos_alz, f'{alz_values[i]:.2f}', 
                       ha='center', va='center', fontsize=9, fontweight='bold', color='white')
            if cntrl_values[i] > 0.05:
                ax.text(1, y_pos_cntrl, f'{cntrl_values[i]:.2f}',
                       ha='center', va='center', fontsize=9, fontweight='bold', color='white')
            y_pos_alz += alz_values[i] / 2
            y_pos_cntrl += cntrl_values[i] / 2
    
    # Add legend
    axes[0].legend(title='Band', loc='upper right', fontsize=10)
    
    plt.suptitle('Stacked Relative Band Power: O1 and O2 Channels', 
                fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()
    
    return fig

def main():
    """Generate key plots."""
    print("="*60)
    print("📊 Creating Key Plots")
    print("="*60)
    
    # Load data
    df, feature_mapping_df = load_data()
    
    # Plot 1: Posterior Alpha boxplots
    fig1 = plot_posterior_alpha_boxplots(df, feature_mapping_df)
    
    # Plot 2: Stacked relative bands
    fig2 = plot_stacked_relative_bands(df, feature_mapping_df)
    
    # Save
    output_dir = Path(__file__).parent
    fig1.savefig(output_dir / 'key_plot1_posterior_alpha_boxplots.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved key_plot1_posterior_alpha_boxplots.png")
    
    fig2.savefig(output_dir / 'key_plot2_stacked_relative_bands.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved key_plot2_stacked_relative_bands.png")
    
    print("\n✅ Key plots complete!")

if __name__ == '__main__':
    main()




