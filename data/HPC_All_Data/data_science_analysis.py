#!/usr/bin/env python
"""
Comprehensive Data Science Analysis for ML Results

This script performs statistical analysis and clearly distinguishes between:
- Average performance (across all hyperparameters)
- Best model performance (best hyperparameter configuration)
"""

import sys
from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)


def load_all_results(ml_results_dir: Path) -> pd.DataFrame:
    """Load all results.json files from directory."""
    print(f"📊 Loading results from: {ml_results_dir}")
    
    results = []
    results_files = list(ml_results_dir.rglob("results.json"))
    
    print(f"   Found {len(results_files)} results.json files")
    
    for results_file in results_files:
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            result = {
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
            
            # Extract fold name from path
            fold_path = Path(results_file).parent
            if fold_path.name.startswith('sub-'):
                result['fold_name'] = fold_path.name
            elif fold_path.parent.name.startswith('sub-'):
                result['fold_name'] = fold_path.parent.name
            else:
                result['fold_name'] = str(result['fold_id'])
            
            results.append(result)
        except Exception as e:
            print(f"   ⚠️ Error loading {results_file}: {e}")
            continue
    
    df = pd.DataFrame(results)
    print(f"   ✅ Loaded {len(df)} results")
    return df


def analyze_average_performance(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze AVERAGE performance across all hyperparameters."""
    print("\n📊 ANALYZING AVERAGE PERFORMANCE (All Hyperparameters)")
    print("="*70)
    
    stats = {}
    
    for model_name in df['model_name'].unique():
        model_df = df[df['model_name'] == model_name]
        
        # Calculate statistics for ALL hyperparameter combinations (average)
        stats[model_name] = {
            'type': 'AVERAGE',
            'total_tasks': len(model_df),
            'num_hyperparam_configs': model_df['hyperparams'].nunique(),
            'num_folds': model_df['fold_name'].nunique(),
            
            # Accuracy metrics (AVERAGE)
            'mean_test_accuracy': float(model_df['test_accuracy'].mean()),
            'median_test_accuracy': float(model_df['test_accuracy'].median()),
            'std_test_accuracy': float(model_df['test_accuracy'].std()),
            'min_test_accuracy': float(model_df['test_accuracy'].min()),
            'max_test_accuracy': float(model_df['test_accuracy'].max()),
            'q25_test_accuracy': float(model_df['test_accuracy'].quantile(0.25)),
            'q75_test_accuracy': float(model_df['test_accuracy'].quantile(0.75)),
            
            # Other metrics (AVERAGE)
            'mean_test_f1': float(model_df['test_f1'].mean()) if 'test_f1' in model_df.columns else None,
            'mean_test_precision': float(model_df['test_precision'].mean()) if 'test_precision' in model_df.columns else None,
            'mean_test_recall': float(model_df['test_recall'].mean()) if 'test_recall' in model_df.columns else None,
            'mean_train_accuracy': float(model_df['train_accuracy'].mean()) if 'train_accuracy' in model_df.columns else None,
        }
        
        print(f"\n   {model_name} (AVERAGE):")
        print(f"      Tasks: {stats[model_name]['total_tasks']}, "
              f"Hyperparam Configs: {stats[model_name]['num_hyperparam_configs']}, "
              f"Folds: {stats[model_name]['num_folds']}")
        print(f"      Mean Accuracy: {stats[model_name]['mean_test_accuracy']:.4f} ± {stats[model_name]['std_test_accuracy']:.4f}")
        print(f"      Median: {stats[model_name]['median_test_accuracy']:.4f}, "
              f"Range: [{stats[model_name]['min_test_accuracy']:.4f}, {stats[model_name]['max_test_accuracy']:.4f}]")
    
    return stats


def analyze_best_model_performance(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze BEST MODEL performance (best hyperparameter configuration)."""
    print("\n📊 ANALYZING BEST MODEL PERFORMANCE (Best Hyperparameters)")
    print("="*70)
    
    stats = {}
    
    for model_name in df['model_name'].unique():
        model_df = df[df['model_name'] == model_name]
        
        # Find best hyperparameters (highest mean test accuracy per hyperparam config)
        best_hyperparams = None
        best_mean_accuracy = 0
        best_results = []
        
        for hyperparams in model_df['hyperparams'].unique():
            hp_df = model_df[model_df['hyperparams'] == hyperparams]
            mean_acc = hp_df['test_accuracy'].mean()
            
            if mean_acc > best_mean_accuracy:
                best_mean_accuracy = mean_acc
                best_hyperparams = hyperparams
                best_results = hp_df.to_dict('records')
        
        # Calculate statistics for BEST hyperparameter configuration
        best_df = pd.DataFrame(best_results)
        
        stats[model_name] = {
            'type': 'BEST MODEL',
            'best_hyperparams': json.loads(best_hyperparams) if best_hyperparams else {},
            'total_tasks': len(best_df),
            'num_folds': best_df['fold_name'].nunique(),
            
            # Accuracy metrics (BEST)
            'mean_test_accuracy': float(best_df['test_accuracy'].mean()),
            'median_test_accuracy': float(best_df['test_accuracy'].median()),
            'std_test_accuracy': float(best_df['test_accuracy'].std()),
            'min_test_accuracy': float(best_df['test_accuracy'].min()),
            'max_test_accuracy': float(best_df['test_accuracy'].max()),
            'q25_test_accuracy': float(best_df['test_accuracy'].quantile(0.25)),
            'q75_test_accuracy': float(best_df['test_accuracy'].quantile(0.75)),
            
            # Other metrics (BEST)
            'mean_test_f1': float(best_df['test_f1'].mean()) if 'test_f1' in best_df.columns else None,
            'mean_test_precision': float(best_df['test_precision'].mean()) if 'test_precision' in best_df.columns else None,
            'mean_test_recall': float(best_df['test_recall'].mean()) if 'test_recall' in best_df.columns else None,
            'mean_train_accuracy': float(best_df['train_accuracy'].mean()) if 'train_accuracy' in best_df.columns else None,
        }
        
        print(f"\n   {model_name} (BEST MODEL):")
        print(f"      Best Hyperparams: {stats[model_name]['best_hyperparams']}")
        print(f"      Tasks: {stats[model_name]['total_tasks']}, "
              f"Folds: {stats[model_name]['num_folds']}")
        print(f"      Mean Accuracy: {stats[model_name]['mean_test_accuracy']:.4f} ± {stats[model_name]['std_test_accuracy']:.4f}")
        print(f"      Median: {stats[model_name]['median_test_accuracy']:.4f}, "
              f"Range: [{stats[model_name]['min_test_accuracy']:.4f}, {stats[model_name]['max_test_accuracy']:.4f}]")
    
    return stats


def statistical_tests(df: pd.DataFrame, average_stats: Dict, best_stats: Dict) -> Dict[str, Any]:
    """Perform statistical tests between models."""
    print("\n📊 STATISTICAL TESTS")
    print("="*70)
    
    tests = {}
    models = sorted(df['model_name'].unique())
    
    # Pairwise comparisons for BEST models
    print("\n   BEST MODEL Comparisons (Pairwise t-tests):")
    print("-"*70)
    
    best_tests = {}
    for i, model1 in enumerate(models):
        for model2 in models[i+1:]:
            model1_best = df[df['model_name'] == model1]
            model2_best = df[df['model_name'] == model2]
            
            # Get best hyperparam results for each
            best_hp1 = None
            best_hp2 = None
            best_mean1 = 0
            best_mean2 = 0
            
            for hp in model1_best['hyperparams'].unique():
                hp_df = model1_best[model1_best['hyperparams'] == hp]
                if hp_df['test_accuracy'].mean() > best_mean1:
                    best_mean1 = hp_df['test_accuracy'].mean()
                    best_hp1 = hp
            
            for hp in model2_best['hyperparams'].unique():
                hp_df = model2_best[model2_best['hyperparams'] == hp]
                if hp_df['test_accuracy'].mean() > best_mean2:
                    best_mean2 = hp_df['test_accuracy'].mean()
                    best_hp2 = hp
            
            if best_hp1 and best_hp2:
                data1 = model1_best[model1_best['hyperparams'] == best_hp1]['test_accuracy'].values
                data2 = model2_best[model2_best['hyperparams'] == best_hp2]['test_accuracy'].values
                
                t_stat, p_value = stats.ttest_ind(data1, data2)
                
                best_tests[f"{model1} vs {model2}"] = {
                    't_statistic': float(t_stat),
                    'p_value': float(p_value),
                    'mean1': float(data1.mean()),
                    'mean2': float(data2.mean()),
                    'significant': p_value < 0.05,
                }
                
                significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
                print(f"      {model1:25} vs {model2:25}")
                print(f"         Mean: {data1.mean():.4f} vs {data2.mean():.4f}, "
                      f"p={p_value:.4f} {significance}")
    
    tests['best_model_pairwise'] = best_tests
    
    # Pairwise comparisons for AVERAGE models
    print("\n   AVERAGE MODEL Comparisons (Pairwise t-tests):")
    print("-"*70)
    
    avg_tests = {}
    for i, model1 in enumerate(models):
        for model2 in models[i+1:]:
            data1 = df[df['model_name'] == model1]['test_accuracy'].values
            data2 = df[df['model_name'] == model2]['test_accuracy'].values
            
            t_stat, p_value = stats.ttest_ind(data1, data2)
            
            avg_tests[f"{model1} vs {model2}"] = {
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'mean1': float(data1.mean()),
                'mean2': float(data2.mean()),
                'significant': p_value < 0.05,
            }
            
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
            print(f"      {model1:25} vs {model2:25}")
            print(f"         Mean: {data1.mean():.4f} vs {data2.mean():.4f}, "
                  f"p={p_value:.4f} {significance}")
    
    tests['average_pairwise'] = avg_tests
    
    return tests


def generate_comparison_csv(average_stats: Dict, best_stats: Dict, output_dir: Path):
    """Generate CSV comparing AVERAGE vs BEST model performance."""
    print("\n📊 GENERATING COMPARISON CSV")
    print("="*70)
    
    rows = []
    
    # AVERAGE performance
    for model_name in sorted(average_stats.keys()):
        avg = average_stats[model_name]
        row = {
            'model_name': model_name,
            'performance_type': 'AVERAGE',
            'mean_test_accuracy': avg['mean_test_accuracy'],
            'std_test_accuracy': avg['std_test_accuracy'],
            'median_test_accuracy': avg['median_test_accuracy'],
            'min_test_accuracy': avg['min_test_accuracy'],
            'max_test_accuracy': avg['max_test_accuracy'],
            'q25_test_accuracy': avg['q25_test_accuracy'],
            'q75_test_accuracy': avg['q75_test_accuracy'],
            'mean_test_f1': avg.get('mean_test_f1'),
            'mean_test_precision': avg.get('mean_test_precision'),
            'mean_test_recall': avg.get('mean_test_recall'),
            'num_hyperparam_configs': avg['num_hyperparam_configs'],
            'num_folds': avg['num_folds'],
            'total_tasks': avg['total_tasks'],
            'best_hyperparams': 'N/A (Average)',
        }
        rows.append(row)
    
    # BEST MODEL performance
    for model_name in sorted(best_stats.keys()):
        best = best_stats[model_name]
        row = {
            'model_name': model_name,
            'performance_type': 'BEST MODEL',
            'mean_test_accuracy': best['mean_test_accuracy'],
            'std_test_accuracy': best['std_test_accuracy'],
            'median_test_accuracy': best['median_test_accuracy'],
            'min_test_accuracy': best['min_test_accuracy'],
            'max_test_accuracy': best['max_test_accuracy'],
            'q25_test_accuracy': best['q25_test_accuracy'],
            'q75_test_accuracy': best['q75_test_accuracy'],
            'mean_test_f1': best.get('mean_test_f1'),
            'mean_test_precision': best.get('mean_test_precision'),
            'mean_test_recall': best.get('mean_test_recall'),
            'num_hyperparam_configs': 1,  # Only best hyperparams
            'num_folds': best['num_folds'],
            'total_tasks': best['total_tasks'],
            'best_hyperparams': str(best['best_hyperparams']),
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df = df.sort_values(['model_name', 'performance_type'])
    
    csv_file = output_dir / 'model_comparison_AVERAGE_vs_BEST.csv'
    df.to_csv(csv_file, index=False)
    print(f"   ✅ Saved: {csv_file}")
    
    return df


def generate_visualizations(df: pd.DataFrame, average_stats: Dict, best_stats: Dict, output_dir: Path):
    """Generate comprehensive visualizations clearly labeled as AVERAGE vs BEST."""
    print("\n📊 GENERATING VISUALIZATIONS")
    print("="*70)
    
    graphs_dir = output_dir / 'graphs'
    graphs_dir.mkdir(exist_ok=True)
    
    models = sorted(df['model_name'].unique())
    
    # 1. AVERAGE vs BEST Comparison Bar Chart
    print("   1. Average vs Best Model Comparison...")
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(models))
    width = 0.35
    
    avg_means = [average_stats[m]['mean_test_accuracy'] for m in models]
    avg_stds = [average_stats[m]['std_test_accuracy'] for m in models]
    best_means = [best_stats[m]['mean_test_accuracy'] for m in models]
    best_stds = [best_stats[m]['std_test_accuracy'] for m in models]
    
    bars1 = ax.bar(x - width/2, avg_means, width, yerr=avg_stds, 
                   label='AVERAGE (All Hyperparams)', capsize=5, alpha=0.8, color='#3498db')
    bars2 = ax.bar(x + width/2, best_means, width, yerr=best_stds, 
                   label='BEST MODEL (Best Hyperparams)', capsize=5, alpha=0.8, color='#e74c3c')
    
    ax.set_xlabel('Model', fontsize=12, fontweight='bold')
    ax.set_ylabel('Test Accuracy', fontsize=12, fontweight='bold')
    ax.set_title('AVERAGE vs BEST MODEL Performance Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0, 1])
    
    # Add value labels on bars
    for bars, means, stds in [(bars1, avg_means, avg_stds), (bars2, best_means, best_stds)]:
        for bar, mean, std in zip(bars, means, stds):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + std,
                   f'{mean:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'AVERAGE_vs_BEST_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. AVERAGE Performance Distribution
    print("   2. Average Performance Distribution...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, model_name in enumerate(models):
        if idx < len(axes):
            ax = axes[idx]
            model_df = df[df['model_name'] == model_name]
            
            ax.hist(model_df['test_accuracy'], bins=30, alpha=0.7, edgecolor='black', color='#3498db')
            ax.axvline(average_stats[model_name]['mean_test_accuracy'], color='red', linestyle='--', 
                      linewidth=2, label=f"Mean: {average_stats[model_name]['mean_test_accuracy']:.3f} (AVERAGE)")
            ax.axvline(average_stats[model_name]['median_test_accuracy'], color='blue', linestyle='--', 
                      linewidth=2, label=f"Median: {average_stats[model_name]['median_test_accuracy']:.3f}")
            
            ax.set_xlabel('Test Accuracy', fontsize=11)
            ax.set_ylabel('Frequency', fontsize=11)
            ax.set_title(f'{model_name}\nAVERAGE Performance (All Hyperparams)\nn={len(model_df)}', 
                        fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_xlim([0, 1])
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'AVERAGE_performance_distributions.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. BEST MODEL Performance Distribution
    print("   3. Best Model Performance Distribution...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, model_name in enumerate(models):
        if idx < len(axes):
            ax = axes[idx]
            
            # Get best hyperparam results
            model_df = df[df['model_name'] == model_name]
            best_hp = None
            best_mean = 0
            
            for hp in model_df['hyperparams'].unique():
                hp_df = model_df[model_df['hyperparams'] == hp]
                if hp_df['test_accuracy'].mean() > best_mean:
                    best_mean = hp_df['test_accuracy'].mean()
                    best_hp = hp
            
            best_df = model_df[model_df['hyperparams'] == best_hp]
            
            ax.hist(best_df['test_accuracy'], bins=30, alpha=0.7, edgecolor='black', color='#e74c3c')
            ax.axvline(best_stats[model_name]['mean_test_accuracy'], color='red', linestyle='--', 
                      linewidth=2, label=f"Mean: {best_stats[model_name]['mean_test_accuracy']:.3f} (BEST MODEL)")
            ax.axvline(best_stats[model_name]['median_test_accuracy'], color='blue', linestyle='--', 
                      linewidth=2, label=f"Median: {best_stats[model_name]['median_test_accuracy']:.3f}")
            
            ax.set_xlabel('Test Accuracy', fontsize=11)
            ax.set_ylabel('Frequency', fontsize=11)
            ax.set_title(f'{model_name}\nBEST MODEL Performance (Best Hyperparams)\nn={len(best_df)}', 
                        fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_xlim([0, 1])
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'BEST_MODEL_performance_distributions.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 4. Box Plot Comparison
    print("   4. Box Plot Comparison (Average vs Best)...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # AVERAGE box plot
    data_avg = [df[df['model_name'] == m]['test_accuracy'].values for m in models]
    bp1 = ax1.boxplot(data_avg, labels=models, patch_artist=True)
    colors = plt.cm.Set3(np.linspace(0, 1, len(models)))
    for patch, color in zip(bp1['boxes'], colors):
        patch.set_facecolor(color)
    
    ax1.set_ylabel('Test Accuracy', fontsize=12, fontweight='bold')
    ax1.set_title('AVERAGE Performance\n(All Hyperparameters)', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_ylim([0, 1])
    
    # BEST box plot
    data_best = []
    for m in models:
        model_df = df[df['model_name'] == m]
        best_hp = None
        best_mean = 0
        
        for hp in model_df['hyperparams'].unique():
            hp_df = model_df[model_df['hyperparams'] == hp]
            if hp_df['test_accuracy'].mean() > best_mean:
                best_mean = hp_df['test_accuracy'].mean()
                best_hp = hp
        
        best_df = model_df[model_df['hyperparams'] == best_hp]
        data_best.append(best_df['test_accuracy'].values)
    
    bp2 = ax2.boxplot(data_best, labels=models, patch_artist=True)
    for patch, color in zip(bp2['boxes'], colors):
        patch.set_facecolor(color)
    
    ax2.set_ylabel('Test Accuracy', fontsize=12, fontweight='bold')
    ax2.set_title('BEST MODEL Performance\n(Best Hyperparameters)', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim([0, 1])
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'AVERAGE_vs_BEST_boxplots.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Graphs saved to: {graphs_dir}")


def generate_statistical_report(average_stats: Dict, best_stats: Dict, tests: Dict, output_dir: Path):
    """Generate comprehensive statistical report."""
    print("\n📊 GENERATING STATISTICAL REPORT")
    print("="*70)
    
    report_file = output_dir / 'data_science_analysis_report.md'
    
    with open(report_file, 'w') as f:
        f.write("# Data Science Analysis Report\n\n")
        f.write("## Executive Summary\n\n")
        f.write("This report provides comprehensive statistical analysis distinguishing between:\n")
        f.write("- **AVERAGE Performance**: Performance across ALL hyperparameter configurations\n")
        f.write("- **BEST MODEL Performance**: Performance of the BEST hyperparameter configuration\n\n")
        
        # AVERAGE Performance Summary
        f.write("## 1. AVERAGE Performance (All Hyperparameters)\n\n")
        f.write("### Summary Statistics\n\n")
        f.write("| Model | Mean Accuracy | Std Dev | Median | Min | Max | Folds | Hyperparam Configs |\n")
        f.write("|-------|---------------|---------|--------|-----|-----|-------|-------------------|\n")
        
        for model_name in sorted(average_stats.keys()):
            stats = average_stats[model_name]
            f.write(f"| {model_name} | {stats['mean_test_accuracy']:.4f} | "
                   f"{stats['std_test_accuracy']:.4f} | {stats['median_test_accuracy']:.4f} | "
                   f"{stats['min_test_accuracy']:.4f} | {stats['max_test_accuracy']:.4f} | "
                   f"{stats['num_folds']} | {stats['num_hyperparam_configs']} |\n")
        
        # BEST MODEL Performance Summary
        f.write("\n## 2. BEST MODEL Performance (Best Hyperparameters)\n\n")
        f.write("### Summary Statistics\n\n")
        f.write("| Model | Mean Accuracy | Std Dev | Median | Min | Max | Folds | Best Hyperparams |\n")
        f.write("|-------|---------------|---------|--------|-----|-----|-------|------------------|\n")
        
        for model_name in sorted(best_stats.keys()):
            stats = best_stats[model_name]
            best_hp_str = str(stats['best_hyperparams'])[:50] + "..." if len(str(stats['best_hyperparams'])) > 50 else str(stats['best_hyperparams'])
            f.write(f"| {model_name} | {stats['mean_test_accuracy']:.4f} | "
                   f"{stats['std_test_accuracy']:.4f} | {stats['median_test_accuracy']:.4f} | "
                   f"{stats['min_test_accuracy']:.4f} | {stats['max_test_accuracy']:.4f} | "
                   f"{stats['num_folds']} | {best_hp_str} |\n")
        
        # Statistical Tests
        f.write("\n## 3. Statistical Tests\n\n")
        f.write("### BEST MODEL Pairwise Comparisons (t-tests)\n\n")
        f.write("| Comparison | Mean 1 | Mean 2 | t-statistic | p-value | Significant? |\n")
        f.write("|------------|--------|--------|-------------|---------|--------------|\n")
        
        for comparison, test_results in tests.get('best_model_pairwise', {}).items():
            sig = "Yes (p<0.05)" if test_results['significant'] else "No"
            f.write(f"| {comparison} | {test_results['mean1']:.4f} | {test_results['mean2']:.4f} | "
                   f"{test_results['t_statistic']:.4f} | {test_results['p_value']:.4f} | {sig} |\n")
        
        f.write("\n### AVERAGE MODEL Pairwise Comparisons (t-tests)\n\n")
        f.write("| Comparison | Mean 1 | Mean 2 | t-statistic | p-value | Significant? |\n")
        f.write("|------------|--------|--------|-------------|---------|--------------|\n")
        
        for comparison, test_results in tests.get('average_pairwise', {}).items():
            sig = "Yes (p<0.05)" if test_results['significant'] else "No"
            f.write(f"| {comparison} | {test_results['mean1']:.4f} | {test_results['mean2']:.4f} | "
                   f"{test_results['t_statistic']:.4f} | {test_results['p_value']:.4f} | {sig} |\n")
        
        # Key Insights
        f.write("\n## 4. Key Insights\n\n")
        
        # Find best average model
        best_avg_model = max(average_stats.items(), key=lambda x: x[1]['mean_test_accuracy'])
        f.write(f"### Best AVERAGE Model: {best_avg_model[0]}\n")
        f.write(f"- Mean Accuracy: {best_avg_model[1]['mean_test_accuracy']:.4f} ± {best_avg_model[1]['std_test_accuracy']:.4f}\n")
        f.write(f"- This represents performance across ALL hyperparameter configurations\n\n")
        
        # Find best model
        best_model = max(best_stats.items(), key=lambda x: x[1]['mean_test_accuracy'])
        f.write(f"### Best MODEL Overall: {best_model[0]}\n")
        f.write(f"- Mean Accuracy: {best_model[1]['mean_test_accuracy']:.4f} ± {best_model[1]['std_test_accuracy']:.4f}\n")
        f.write(f"- This represents performance of the BEST hyperparameter configuration\n")
        f.write(f"- Best Hyperparams: {best_model[1]['best_hyperparams']}\n\n")
        
        # Performance gap
        avg_best_acc = best_avg_model[1]['mean_test_accuracy']
        best_best_acc = best_model[1]['mean_test_accuracy']
        gap = best_best_acc - avg_best_acc
        
        f.write(f"### Performance Gap: AVERAGE vs BEST\n")
        f.write(f"- Average Best Model: {best_avg_model[0]} ({avg_best_acc:.4f})\n")
        f.write(f"- Best Model Overall: {best_model[0]} ({best_best_acc:.4f})\n")
        f.write(f"- Gap: {gap:.4f} ({gap/avg_best_acc*100:.2f}% improvement)\n\n")
    
    print(f"   ✅ Saved: {report_file}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Comprehensive Data Science Analysis')
    parser.add_argument('ml_results_dir', type=str, help='Path to ml_results directory')
    
    args = parser.parse_args()
    
    ml_results_dir = Path(args.ml_results_dir).resolve()
    
    if not ml_results_dir.exists():
        print(f"❌ ML results directory not found: {ml_results_dir}")
        sys.exit(1)
    
    print("="*70)
    print("COMPREHENSIVE DATA SCIENCE ANALYSIS")
    print("="*70)
    print(f"📁 ML Results Directory: {ml_results_dir}")
    print("\n⚠️  IMPORTANT: This analysis distinguishes between:")
    print("   - AVERAGE: Performance across ALL hyperparameter configurations")
    print("   - BEST MODEL: Performance of the BEST hyperparameter configuration")
    
    # Load all results
    df = load_all_results(ml_results_dir)
    
    if df.empty:
        print("❌ No results found")
        sys.exit(1)
    
    # Analyze
    average_stats = analyze_average_performance(df)
    best_stats = analyze_best_model_performance(df)
    
    # Statistical tests
    tests = statistical_tests(df, average_stats, best_stats)
    
    # Generate outputs
    comparison_df = generate_comparison_csv(average_stats, best_stats, ml_results_dir)
    generate_visualizations(df, average_stats, best_stats, ml_results_dir)
    generate_statistical_report(average_stats, best_stats, tests, ml_results_dir)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\n📁 Generated files in: {ml_results_dir}")
    print("   • model_comparison_AVERAGE_vs_BEST.csv")
    print("   • graphs/AVERAGE_vs_BEST_comparison.png")
    print("   • graphs/AVERAGE_performance_distributions.png")
    print("   • graphs/BEST_MODEL_performance_distributions.png")
    print("   • graphs/AVERAGE_vs_BEST_boxplots.png")
    print("   • data_science_analysis_report.md")
    print("="*70)


if __name__ == '__main__':
    main()


