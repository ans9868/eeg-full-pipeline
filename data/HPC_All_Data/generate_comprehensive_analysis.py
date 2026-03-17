#!/usr/bin/env python
"""
Comprehensive analysis script for HPC ML results.

Generates:
- Model comparison CSV
- Detailed graphs
- Performance statistics
- Fold-by-fold analysis
"""

import sys
from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from typing import Dict, List, Any, Optional

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


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
                'hyperparams': json.dumps(data.get('hyperparams', {})),
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


def generate_model_comparison_csv(df: pd.DataFrame, output_dir: Path):
    """Generate model comparison CSV."""
    print("\n📊 Generating model comparison CSV...")
    
    rows = []
    
    for model_name in df['model_name'].unique():
        model_df = df[df['model_name'] == model_name]
        
        # Find best hyperparameters (highest mean test accuracy)
        best_hyperparams = None
        best_mean_accuracy = 0
        
        for hyperparams in model_df['hyperparams'].unique():
            hp_df = model_df[model_df['hyperparams'] == hyperparams]
            mean_acc = hp_df['test_accuracy'].mean()
            
            if mean_acc > best_mean_accuracy:
                best_mean_accuracy = mean_acc
                best_hyperparams = hyperparams
        
        # Get stats for best hyperparameters
        best_df = model_df[model_df['hyperparams'] == best_hyperparams]
        
        row = {
            'model_name': model_name,
            'best_test_accuracy': best_df['test_accuracy'].mean(),
            'std_test_accuracy': best_df['test_accuracy'].std(),
            'best_train_accuracy': best_df['train_accuracy'].mean() if 'train_accuracy' in best_df.columns else 0,
            'std_train_accuracy': best_df['train_accuracy'].std() if 'train_accuracy' in best_df.columns else 0,
            'test_f1': best_df['test_f1'].mean() if 'test_f1' in best_df.columns else 0,
            'test_precision': best_df['test_precision'].mean() if 'test_precision' in best_df.columns else 0,
            'test_recall': best_df['test_recall'].mean() if 'test_recall' in best_df.columns else 0,
            'num_folds': best_df['fold_name'].nunique(),
            'total_tasks': len(best_df),
            'best_hyperparams': best_hyperparams,
        }
        rows.append(row)
    
    if rows:
        comparison_df = pd.DataFrame(rows)
        comparison_df = comparison_df.sort_values('best_test_accuracy', ascending=False)
        
        csv_file = output_dir / 'model_comparison.csv'
        comparison_df.to_csv(csv_file, index=False)
        print(f"   ✅ Saved: {csv_file}")
        
        # Print summary
        print("\n   Model Comparison Summary:")
        print("-"*70)
        for _, row in comparison_df.iterrows():
            print(f"   {row['model_name']:25} | Accuracy: {row['best_test_accuracy']:.4f} ± {row['std_test_accuracy']:.4f} | "
                  f"Folds: {row['num_folds']} | Tasks: {row['total_tasks']}")
        
        return comparison_df
    else:
        print("   ⚠️ No results to save")
        return None


def generate_graphs(df: pd.DataFrame, output_dir: Path):
    """Generate comprehensive graphs."""
    print("\n📊 Generating graphs...")
    
    graphs_dir = output_dir / 'graphs'
    graphs_dir.mkdir(exist_ok=True)
    
    # 1. Model Comparison Box Plot
    print("   1. Model comparison box plot...")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    models = sorted(df['model_name'].unique())
    data_by_model = [df[df['model_name'] == model]['test_accuracy'].values for model in models]
    
    bp = ax.boxplot(data_by_model, labels=models, patch_artist=True)
    colors = plt.cm.Set3(np.linspace(0, 1, len(models)))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Test Accuracy')
    ax.set_title('Model Performance Comparison')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0, 1])
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'model_comparison_boxplot.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. Accuracy Distribution by Model
    print("   2. Accuracy distributions by model...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, model_name in enumerate(sorted(models)):
        if idx < len(axes):
            ax = axes[idx]
            model_df = df[df['model_name'] == model_name]
            
            ax.hist(model_df['test_accuracy'], bins=30, alpha=0.7, edgecolor='black')
            ax.axvline(model_df['test_accuracy'].mean(), color='red', linestyle='--', 
                      label=f'Mean: {model_df["test_accuracy"].mean():.3f}')
            ax.axvline(model_df['test_accuracy'].median(), color='blue', linestyle='--', 
                      label=f'Median: {model_df["test_accuracy"].median():.3f}')
            
            ax.set_xlabel('Test Accuracy')
            ax.set_ylabel('Frequency')
            ax.set_title(f'{model_name}\nAccuracy Distribution (n={len(model_df)})')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_xlim([0, 1])
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'accuracy_distributions_by_model.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. Fold Performance
    if 'fold_name' in df.columns and df['fold_name'].nunique() > 1:
        print("   3. Fold performance analysis...")
        
        fold_performance = df.groupby('fold_name')['test_accuracy'].mean().sort_values()
        
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.scatter(range(len(fold_performance)), fold_performance.values, alpha=0.6, s=50)
        ax.axhline(y=fold_performance.mean(), color='red', linestyle='--', 
                  label=f'Mean: {fold_performance.mean():.3f}')
        ax.axhline(y=fold_performance.median(), color='blue', linestyle='--', 
                  label=f'Median: {fold_performance.median():.3f}')
        
        ax.set_xlabel('Fold (sorted by accuracy)')
        ax.set_ylabel('Mean Test Accuracy')
        ax.set_title(f'Accuracy Across Folds ({len(fold_performance)} folds)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(graphs_dir / 'fold_performance.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    # 4. Model Performance Metrics Comparison
    print("   4. Model metrics comparison...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    metrics = ['test_accuracy', 'test_f1', 'test_precision', 'test_recall']
    metric_names = ['Accuracy', 'F1 Score', 'Precision', 'Recall']
    
    for idx, (metric, metric_name) in enumerate(zip(metrics, metric_names)):
        if idx < len(axes.flatten()):
            ax = axes.flatten()[idx]
            
            if metric in df.columns:
                model_stats = df.groupby('model_name')[metric].agg(['mean', 'std']).sort_values('mean', ascending=False)
                
                x_pos = np.arange(len(model_stats))
                bars = ax.bar(x_pos, model_stats['mean'], yerr=model_stats['std'], 
                             capsize=5, color=plt.cm.Set3(np.linspace(0, 1, len(model_stats))))
                
                ax.set_xticks(x_pos)
                ax.set_xticklabels(model_stats.index, rotation=45, ha='right')
                ax.set_ylabel(metric_name)
                ax.set_title(f'{metric_name} by Model')
                ax.grid(True, alpha=0.3, axis='y')
                ax.set_ylim([0, 1])
    
    plt.tight_layout()
    plt.savefig(graphs_dir / 'model_metrics_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Graphs saved to: {graphs_dir}")


def generate_detailed_statistics(df: pd.DataFrame, output_dir: Path):
    """Generate detailed statistics files."""
    print("\n📊 Generating detailed statistics...")
    
    # Overall statistics
    stats = {
        'overall': {
            'total_results': len(df),
            'total_models': df['model_name'].nunique(),
            'total_folds': df['fold_name'].nunique() if 'fold_name' in df.columns else 0,
            'mean_accuracy': float(df['test_accuracy'].mean()),
            'median_accuracy': float(df['test_accuracy'].median()),
            'std_accuracy': float(df['test_accuracy'].std()),
            'min_accuracy': float(df['test_accuracy'].min()),
            'max_accuracy': float(df['test_accuracy'].max()),
        }
    }
    
    # Per-model statistics
    stats['per_model'] = {}
    for model_name in df['model_name'].unique():
        model_df = df[df['model_name'] == model_name]
        stats['per_model'][model_name] = {
            'total_tasks': len(model_df),
            'num_folds': model_df['fold_name'].nunique() if 'fold_name' in model_df.columns else 0,
            'mean_accuracy': float(model_df['test_accuracy'].mean()),
            'median_accuracy': float(model_df['test_accuracy'].median()),
            'std_accuracy': float(model_df['test_accuracy'].std()),
            'min_accuracy': float(model_df['test_accuracy'].min()),
            'max_accuracy': float(model_df['test_accuracy'].max()),
        }
    
    # Save as JSON
    stats_file = output_dir / 'detailed_statistics.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"   ✅ Saved: {stats_file}")
    
    # Save as text summary
    summary_file = output_dir / 'detailed_summary.txt'
    with open(summary_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("DETAILED STATISTICS SUMMARY\n")
        f.write("="*70 + "\n\n")
        
        f.write("OVERALL STATISTICS:\n")
        f.write("-"*70 + "\n")
        for key, value in stats['overall'].items():
            f.write(f"  {key}: {value}\n")
        
        f.write("\n\nPER-MODEL STATISTICS:\n")
        f.write("-"*70 + "\n")
        for model_name, model_stats in stats['per_model'].items():
            f.write(f"\n{model_name}:\n")
            for key, value in model_stats.items():
                f.write(f"  {key}: {value}\n")
    
    print(f"   ✅ Saved: {summary_file}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate comprehensive analysis from ML results')
    parser.add_argument('ml_results_dir', type=str, help='Path to ml_results directory')
    
    args = parser.parse_args()
    
    ml_results_dir = Path(args.ml_results_dir).resolve()
    
    if not ml_results_dir.exists():
        print(f"❌ ML results directory not found: {ml_results_dir}")
        sys.exit(1)
    
    print("="*70)
    print("COMPREHENSIVE ML RESULTS ANALYSIS")
    print("="*70)
    print(f"📁 ML Results Directory: {ml_results_dir}")
    
    # Load all results
    df = load_all_results(ml_results_dir)
    
    if df.empty:
        print("❌ No results found")
        sys.exit(1)
    
    # Generate analysis
    generate_model_comparison_csv(df, ml_results_dir)
    generate_graphs(df, ml_results_dir)
    generate_detailed_statistics(df, ml_results_dir)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\n📁 Generated files in: {ml_results_dir}")
    print("   • model_comparison.csv")
    print("   • graphs/ (multiple PNG files)")
    print("   • detailed_statistics.json")
    print("   • detailed_summary.txt")
    print("="*70)


if __name__ == '__main__':
    main()

