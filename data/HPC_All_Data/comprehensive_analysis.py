#!/usr/bin/env python
"""
Comprehensive analysis of grid_12_folds and grid_50_random_folds experiments.

This script:
1. Analyzes grid_12_folds experiments
2. Analyzes grid_50_random_folds experiments
3. Performs combined comparison analysis
"""

import sys
from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)


def load_all_results_from_dir(results_dir: Path) -> pd.DataFrame:
    """Load all results.json files from a directory recursively."""
    results = []
    results_files = list(results_dir.rglob("results.json"))
    
    for results_file in results_files:
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            result = {
                'experiment_group': None,  # Will be filled based on parent directory
                'config_name': None,  # Will be filled based on parent directory
                'task_id': data.get('task_id'),
                'model_name': data.get('model_name'),
                'fold_id': str(data.get('fold_id', '')),
                'test_accuracy': data.get('test_accuracy', data.get('test_results', {}).get('accuracy')),
                'train_accuracy': data.get('train_accuracy', data.get('train_results', {}).get('accuracy')),
                'test_f1': data.get('test_results', {}).get('f1'),
                'test_precision': data.get('test_results', {}).get('precision'),
                'test_recall': data.get('test_results', {}).get('recall'),
                'hyperparams': json.dumps(data.get('hyperparams', {}), sort_keys=True),
            }
            
            # Extract fold name and experiment info from path
            fold_path = Path(results_file).parent
            if fold_path.name.startswith('sub-'):
                result['fold_name'] = fold_path.name
            elif fold_path.parent.name.startswith('sub-'):
                result['fold_name'] = fold_path.parent.name
            else:
                result['fold_name'] = str(result['fold_id'])
            
            # Extract config name and experiment group from path
            path_str = str(results_file)
            path_parts = Path(results_file).parts
            
            # Determine experiment group
            if 'grid_12_folds' in path_str:
                result['experiment_group'] = 'grid_12_folds'
                # Find the parent directory of ml_results (this is the config name)
                for i, part in enumerate(path_parts):
                    if 'ml_results' in part and i > 0:
                        # Go up two levels: ml_results -> config_name
                        result['config_name'] = path_parts[i-1] if i > 0 else 'unknown'
                        break
            elif 'grid_50_random_folds' in path_str:
                result['experiment_group'] = 'grid_50_random_folds'
                # For grid_50_random_folds, the config name is the ml_results directory name itself
                for i, part in enumerate(path_parts):
                    if 'ml_results' in part:
                        # The config name is the ml_results directory name (without _ml_results suffix)
                        ml_results_name = part.replace('_ml_results', '').replace('ml_results', '')
                        if ml_results_name:
                            result['config_name'] = ml_results_name
                        else:
                            # Fallback: use parent directory
                            result['config_name'] = path_parts[i-1] if i > 0 else 'unknown'
                        break
            
            results.append(result)
        except Exception as e:
            continue
    
    df = pd.DataFrame(results)
    return df


def analyze_experiment_group(df: pd.DataFrame, group_name: str) -> Dict[str, Any]:
    """Analyze all experiments in a group."""
    print(f"\n{'='*70}")
    print(f"ANALYZING: {group_name}")
    print('='*70)
    
    if df.empty:
        print(f"   ⚠️ No data found for {group_name}")
        return {}
    
    print(f"   📊 Total results: {len(df)}")
    print(f"   📊 Configurations: {df['config_name'].nunique()}")
    print(f"   📊 Models: {df['model_name'].nunique()}")
    
    # Overall statistics
    stats = {
        'group_name': group_name,
        'total_results': len(df),
        'num_configs': df['config_name'].nunique(),
        'num_models': df['model_name'].nunique(),
        'num_folds': df['fold_name'].nunique() if 'fold_name' in df.columns else 0,
        'overall_mean_accuracy': float(df['test_accuracy'].mean()),
        'overall_median_accuracy': float(df['test_accuracy'].median()),
        'overall_std_accuracy': float(df['test_accuracy'].std()),
        'overall_min_accuracy': float(df['test_accuracy'].min()),
        'overall_max_accuracy': float(df['test_accuracy'].max()),
    }
    
    # Per-config analysis
    print(f"\n   📊 Per-Configuration Analysis:")
    print("-"*70)
    stats['per_config'] = {}
    
    for config_name in sorted(df['config_name'].unique()):
        config_df = df[df['config_name'] == config_name]
        config_stats = {
            'total_results': len(config_df),
            'num_models': config_df['model_name'].nunique(),
            'num_folds': config_df['fold_name'].nunique() if 'fold_name' in config_df.columns else 0,
            'mean_accuracy': float(config_df['test_accuracy'].mean()),
            'median_accuracy': float(config_df['test_accuracy'].median()),
            'std_accuracy': float(config_df['test_accuracy'].std()),
        }
        stats['per_config'][config_name] = config_stats
        
        print(f"      {config_name:40} | Accuracy: {config_stats['mean_accuracy']:.4f} ± {config_stats['std_accuracy']:.4f} | "
              f"Results: {config_stats['total_results']} | Folds: {config_stats['num_folds']}")
    
    # Per-model analysis
    print(f"\n   📊 Per-Model Analysis:")
    print("-"*70)
    stats['per_model'] = {}
    
    for model_name in sorted(df['model_name'].unique()):
        model_df = df[df['model_name'] == model_name]
        model_stats = {
            'total_results': len(model_df),
            'num_configs': model_df['config_name'].nunique(),
            'mean_accuracy': float(model_df['test_accuracy'].mean()),
            'median_accuracy': float(model_df['test_accuracy'].median()),
            'std_accuracy': float(model_df['test_accuracy'].std()),
        }
        stats['per_model'][model_name] = model_stats
        
        print(f"      {model_name:25} | Accuracy: {model_stats['mean_accuracy']:.4f} ± {model_stats['std_accuracy']:.4f} | "
              f"Results: {model_stats['total_results']}")
    
    return stats


def compare_experiment_groups(stats_12: Dict, stats_50: Dict) -> Dict[str, Any]:
    """Compare grid_12_folds vs grid_50_random_folds."""
    print(f"\n{'='*70}")
    print("COMBINED COMPARISON: grid_12_folds vs grid_50_random_folds")
    print('='*70)
    
    comparison = {
        'overall_comparison': {},
        'model_comparison': {},
    }
    
    # Overall comparison
    print("\n📊 Overall Performance Comparison:")
    print("-"*70)
    
    overall_12 = stats_12.get('overall_mean_accuracy', 0)
    overall_50 = stats_50.get('overall_mean_accuracy', 0)
    diff = overall_50 - overall_12
    pct_diff = (diff / overall_12 * 100) if overall_12 > 0 else 0
    
    comparison['overall_comparison'] = {
        'grid_12_folds': overall_12,
        'grid_50_random_folds': overall_50,
        'difference': diff,
        'percent_change': pct_diff,
    }
    
    print(f"   grid_12_folds:          {overall_12:.4f} ± {stats_12.get('overall_std_accuracy', 0):.4f}")
    print(f"   grid_50_random_folds:   {overall_50:.4f} ± {stats_50.get('overall_std_accuracy', 0):.4f}")
    print(f"   Difference:             {diff:+.4f} ({pct_diff:+.2f}%)")
    
    # Model comparison
    print("\n📊 Per-Model Comparison:")
    print("-"*70)
    
    models_12 = stats_12.get('per_model', {})
    models_50 = stats_50.get('per_model', {})
    
    all_models = set(list(models_12.keys()) + list(models_50.keys()))
    
    for model_name in sorted(all_models):
        model_12 = models_12.get(model_name, {})
        model_50 = models_50.get(model_name, {})
        
        acc_12 = model_12.get('mean_accuracy', 0)
        acc_50 = model_50.get('mean_accuracy', 0)
        diff = acc_50 - acc_12
        pct_diff = (diff / acc_12 * 100) if acc_12 > 0 else 0
        
        comparison['model_comparison'][model_name] = {
            'grid_12_folds': acc_12,
            'grid_50_random_folds': acc_50,
            'difference': diff,
            'percent_change': pct_diff,
        }
        
        print(f"   {model_name:25} | 12_folds: {acc_12:.4f} | 50_random: {acc_50:.4f} | "
              f"Diff: {diff:+.4f} ({pct_diff:+.2f}%)")
    
    return comparison


def generate_visualizations(df_12: pd.DataFrame, df_50: pd.DataFrame, output_dir: Path):
    """Generate comprehensive comparison visualizations."""
    print(f"\n{'='*70}")
    print("GENERATING COMPARISON VISUALIZATIONS")
    print('='*70)
    
    graphs_dir = output_dir / 'graphs'
    graphs_dir.mkdir(exist_ok=True)
    
    # Combine dataframes for comparison
    df_combined = pd.concat([
        df_12.assign(experiment_type='12_folds'),
        df_50.assign(experiment_type='50_random_folds')
    ], ignore_index=True)
    
    # 1. Overall Comparison
    print("   1. Overall comparison...")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    data_12 = df_12['test_accuracy'].values if not df_12.empty else []
    data_50 = df_50['test_accuracy'].values if not df_50.empty else []
    
    if len(data_12) > 0 and len(data_50) > 0:
        bp = ax.boxplot([data_12, data_50], tick_labels=['12 Folds', '50 Random Folds'], 
                       patch_artist=True)
        colors = ['#3498db', '#e74c3c']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        ax.set_ylabel('Test Accuracy', fontsize=12, fontweight='bold')
        ax.set_title('Overall Performance: 12 Folds vs 50 Random Folds', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim([0, 1])
        
        # Add mean lines
        mean_12 = np.mean(data_12)
        mean_50 = np.mean(data_50)
        ax.axhline(y=mean_12, color='blue', linestyle='--', alpha=0.7, 
                  label=f'12 Folds Mean: {mean_12:.3f}')
        ax.axhline(y=mean_50, color='red', linestyle='--', alpha=0.7, 
                  label=f'50 Random Mean: {mean_50:.3f}')
        ax.legend()
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'overall_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. Model-by-Model Comparison
    print("   2. Model-by-model comparison...")
    models = sorted(set(df_12['model_name'].unique()) | set(df_50['model_name'].unique()))
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    axes = axes.flatten()
    
    for idx, model_name in enumerate(models[:4]):
        if idx < len(axes):
            ax = axes[idx]
            
            model_12 = df_12[df_12['model_name'] == model_name]['test_accuracy'].values if not df_12.empty else []
            model_50 = df_50[df_50['model_name'] == model_name]['test_accuracy'].values if not df_50.empty else []
            
            if len(model_12) > 0 and len(model_50) > 0:
                bp = ax.boxplot([model_12, model_50], 
                               tick_labels=['12 Folds', '50 Random'], 
                               patch_artist=True)
                colors = ['#3498db', '#e74c3c']
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                
                ax.set_ylabel('Test Accuracy', fontsize=11)
                ax.set_title(f'{model_name}\n12 Folds vs 50 Random Folds', 
                           fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='y')
                ax.set_ylim([0, 1])
            else:
                ax.text(0.5, 0.5, f'No data for {model_name}', 
                       ha='center', va='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'model_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. Configuration Comparison
    print("   3. Configuration comparison...")
    if 'config_name' in df_combined.columns:
        config_stats = df_combined.groupby(['experiment_type', 'config_name'])['test_accuracy'].agg(['mean', 'std', 'count']).reset_index()
        
        # Get unique configs
        all_configs = sorted(set(config_stats['config_name'].unique()))
        
        if all_configs:
            fig, ax = plt.subplots(figsize=(18, 10))
            
            x = np.arange(len(all_configs))
            width = 0.35
            
            means_12 = []
            means_50 = []
            stds_12 = []
            stds_50 = []
            
            for config in all_configs:
                config_12 = config_stats[(config_stats['experiment_type'] == '12_folds') & 
                                        (config_stats['config_name'] == config)]
                config_50 = config_stats[(config_stats['experiment_type'] == '50_random_folds') & 
                                        (config_stats['config_name'] == config)]
                
                means_12.append(config_12['mean'].values[0] if not config_12.empty else 0)
                means_50.append(config_50['mean'].values[0] if not config_50.empty else 0)
                stds_12.append(config_12['std'].values[0] if not config_12.empty else 0)
                stds_50.append(config_50['std'].values[0] if not config_50.empty else 0)
            
            bars1 = ax.bar(x - width/2, means_12, width, yerr=stds_12, 
                          label='12 Folds', capsize=5, alpha=0.8, color='#3498db')
            bars2 = ax.bar(x + width/2, means_50, width, yerr=stds_50, 
                          label='50 Random Folds', capsize=5, alpha=0.8, color='#e74c3c')
            
            ax.set_xlabel('Configuration', fontsize=12, fontweight='bold')
            ax.set_ylabel('Mean Test Accuracy', fontsize=12, fontweight='bold')
            ax.set_title('Performance by Configuration: 12 Folds vs 50 Random Folds', 
                        fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(all_configs, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_ylim([0, 1])
            
            plt.tight_layout()
            plt.savefig(graphs_dir / 'configuration_comparison.png', dpi=150, bbox_inches='tight')
            plt.close()
    
    print(f"   ✅ Graphs saved to: {graphs_dir}")


def save_analysis_report(stats_12: Dict, stats_50: Dict, comparison: Dict, output_dir: Path):
    """Save comprehensive analysis report."""
    print(f"\n{'='*70}")
    print("GENERATING ANALYSIS REPORT")
    print('='*70)
    
    report_file = output_dir / 'comprehensive_analysis_report.md'
    
    with open(report_file, 'w') as f:
        f.write("# Comprehensive Analysis Report\n\n")
        f.write("## Executive Summary\n\n")
        f.write("This report compares experiments from:\n")
        f.write("- **grid_12_folds**: Systematic 12-fold LPSO experiments\n")
        f.write("- **grid_50_random_folds**: Random 50-fold LPSO experiments\n\n")
        
        # Grid 12 Folds Analysis
        f.write("## 1. Grid 12 Folds Analysis\n\n")
        if stats_12:
            f.write(f"### Overall Statistics\n\n")
            f.write(f"- Total Results: {stats_12.get('total_results', 0)}\n")
            f.write(f"- Configurations: {stats_12.get('num_configs', 0)}\n")
            f.write(f"- Models: {stats_12.get('num_models', 0)}\n")
            f.write(f"- Mean Accuracy: {stats_12.get('overall_mean_accuracy', 0):.4f} ± {stats_12.get('overall_std_accuracy', 0):.4f}\n")
            f.write(f"- Range: [{stats_12.get('overall_min_accuracy', 0):.4f}, {stats_12.get('overall_max_accuracy', 0):.4f}]\n\n")
            
            f.write("### Per-Configuration Performance\n\n")
            f.write("| Configuration | Mean Accuracy | Std Dev | Total Results | Folds |\n")
            f.write("|---------------|---------------|---------|---------------|-------|\n")
            
            for config_name, config_stats in sorted(stats_12.get('per_config', {}).items()):
                f.write(f"| {config_name} | {config_stats['mean_accuracy']:.4f} | "
                       f"{config_stats['std_accuracy']:.4f} | {config_stats['total_results']} | "
                       f"{config_stats['num_folds']} |\n")
            
            f.write("\n### Per-Model Performance\n\n")
            f.write("| Model | Mean Accuracy | Std Dev | Total Results |\n")
            f.write("|-------|---------------|---------|---------------|\n")
            
            for model_name, model_stats in sorted(stats_12.get('per_model', {}).items()):
                f.write(f"| {model_name} | {model_stats['mean_accuracy']:.4f} | "
                       f"{model_stats['std_accuracy']:.4f} | {model_stats['total_results']} |\n")
        
        # Grid 50 Random Folds Analysis
        f.write("\n## 2. Grid 50 Random Folds Analysis\n\n")
        if stats_50:
            f.write(f"### Overall Statistics\n\n")
            f.write(f"- Total Results: {stats_50.get('total_results', 0)}\n")
            f.write(f"- Configurations: {stats_50.get('num_configs', 0)}\n")
            f.write(f"- Models: {stats_50.get('num_models', 0)}\n")
            f.write(f"- Mean Accuracy: {stats_50.get('overall_mean_accuracy', 0):.4f} ± {stats_50.get('overall_std_accuracy', 0):.4f}\n")
            f.write(f"- Range: [{stats_50.get('overall_min_accuracy', 0):.4f}, {stats_50.get('overall_max_accuracy', 0):.4f}]\n\n")
            
            f.write("### Per-Configuration Performance\n\n")
            f.write("| Configuration | Mean Accuracy | Std Dev | Total Results | Folds |\n")
            f.write("|---------------|---------------|---------|---------------|-------|\n")
            
            for config_name, config_stats in sorted(stats_50.get('per_config', {}).items()):
                f.write(f"| {config_name} | {config_stats['mean_accuracy']:.4f} | "
                       f"{config_stats['std_accuracy']:.4f} | {config_stats['total_results']} | "
                       f"{config_stats['num_folds']} |\n")
            
            f.write("\n### Per-Model Performance\n\n")
            f.write("| Model | Mean Accuracy | Std Dev | Total Results |\n")
            f.write("|-------|---------------|---------|---------------|\n")
            
            for model_name, model_stats in sorted(stats_50.get('per_model', {}).items()):
                f.write(f"| {model_name} | {model_stats['mean_accuracy']:.4f} | "
                       f"{model_stats['std_accuracy']:.4f} | {model_stats['total_results']} |\n")
        
        # Comparison
        f.write("\n## 3. Combined Comparison\n\n")
        if comparison:
            overall = comparison.get('overall_comparison', {})
            f.write("### Overall Performance Comparison\n\n")
            f.write(f"- **12 Folds**: {overall.get('grid_12_folds', 0):.4f}\n")
            f.write(f"- **50 Random Folds**: {overall.get('grid_50_random_folds', 0):.4f}\n")
            f.write(f"- **Difference**: {overall.get('difference', 0):+.4f} ({overall.get('percent_change', 0):+.2f}%)\n\n")
            
            f.write("### Per-Model Comparison\n\n")
            f.write("| Model | 12 Folds | 50 Random | Difference | % Change |\n")
            f.write("|-------|----------|-----------|------------|----------|\n")
            
            for model_name, model_comp in sorted(comparison.get('model_comparison', {}).items()):
                f.write(f"| {model_name} | {model_comp['grid_12_folds']:.4f} | "
                       f"{model_comp['grid_50_random_folds']:.4f} | "
                       f"{model_comp['difference']:+.4f} | {model_comp['percent_change']:+.2f}% |\n")
    
    print(f"   ✅ Saved: {report_file}")


def main():
    """Main function."""
    print("="*70)
    print("COMPREHENSIVE ANALYSIS: grid_12_folds vs grid_50_random_folds")
    print("="*70)
    
    base_dir = Path("/Users/user/projects/eeg-full-pipeline/data/HPC_All_Data")
    
    # Load data
    print("\n📊 Loading data from grid_12_folds...")
    grid_12_dir = base_dir / "grid_12_folds"
    df_12 = load_all_results_from_dir(grid_12_dir)
    print(f"   ✅ Loaded {len(df_12)} results from grid_12_folds")
    
    print("\n📊 Loading data from grid_50_random_folds...")
    grid_50_dir = base_dir / "grid_50_random_folds"
    df_50 = load_all_results_from_dir(grid_50_dir)
    print(f"   ✅ Loaded {len(df_50)} results from grid_50_random_folds")
    
    # Analyze each group
    stats_12 = analyze_experiment_group(df_12, "grid_12_folds") if not df_12.empty else {}
    stats_50 = analyze_experiment_group(df_50, "grid_50_random_folds") if not df_50.empty else {}
    
    # Compare
    comparison = compare_experiment_groups(stats_12, stats_50)
    
    # Generate visualizations
    generate_visualizations(df_12, df_50, base_dir)
    
    # Save report
    save_analysis_report(stats_12, stats_50, comparison, base_dir)
    
    # Save statistics as JSON
    stats_file = base_dir / 'comprehensive_analysis_stats.json'
    with open(stats_file, 'w') as f:
        json.dump({
            'grid_12_folds': stats_12,
            'grid_50_random_folds': stats_50,
            'comparison': comparison,
        }, f, indent=2)
    print(f"   ✅ Saved: {stats_file}")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\n📁 Generated files in: {base_dir}")
    print("   • comprehensive_analysis_report.md")
    print("   • comprehensive_analysis_stats.json")
    print("   • graphs/overall_comparison.png")
    print("   • graphs/model_comparison.png")
    print("   • graphs/configuration_comparison.png")
    print("="*70)


if __name__ == '__main__':
    main()

