#!/usr/bin/env python
"""
Comprehensive analysis for grid_50_random_folds experiments.

This script follows the same pattern as HPC_experiments and HPC_experimentsv2:
1. Loads overall_summary.json files
2. Loads model_comparison.csv files
3. Extracts fold results from detailed_results.json or individual fold directories
4. Generates comprehensive statistics and comparisons
"""

import sys
import json
import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import statistics

# Set up paths
BASE_DIR = Path(__file__).parent
GRID_50_DIR = BASE_DIR / "grid_50_random_folds"
OUTPUT_DIR = BASE_DIR
OUTPUT_DIR.mkdir(exist_ok=True)

# Define experiments in grid_50_random_folds
EXPERIMENTS_50 = {
    'Anova_L_2_incomplete': GRID_50_DIR / 'Anova_L_2_incomplete_ml_results',
    'Anova_L_6_Incomplete': GRID_50_DIR / 'Anova_L_6_Incomplete_ml_results',
    'PCA_L_2': GRID_50_DIR / 'PCA_L_2_ml_results',
    'PCA_L_6': GRID_50_DIR / 'PCA_L_6_ml_results',
}

def load_summary_json(experiment_path: Path) -> Optional[dict]:
    """Load overall_summary.json from an experiment."""
    # Try ml_results_grid_search subdirectory first
    summary_path = experiment_path / "ml_results_grid_search" / "overall_summary.json"
    if summary_path.exists():
        with open(summary_path, 'r') as f:
            return json.load(f)
    
    # Try direct path (for grid_50_random_folds structure)
    summary_path = experiment_path / "overall_summary.json"
    if summary_path.exists():
        with open(summary_path, 'r') as f:
            return json.load(f)
    
    return None

def load_model_comparison_csv(experiment_path: Path) -> Optional[pd.DataFrame]:
    """Load model_comparison.csv from an experiment."""
    # Try ml_results_grid_search subdirectory first
    csv_path = experiment_path / "ml_results_grid_search" / "model_comparison.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        df['experiment'] = experiment_path.name
        return df
    
    # Try direct path (for grid_50_random_folds structure)
    csv_path = experiment_path / "model_comparison.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        df['experiment'] = experiment_path.name
        return df
    
    return None

def extract_fold_performances(experiment_path: Path) -> Dict[str, List[float]]:
    """Extract per-fold test accuracies from experiment for each model."""
    fold_performances = {}
    
    # Try ml_results_grid_search subdirectory first
    ml_results_path = experiment_path / "ml_results_grid_search"
    if not ml_results_path.exists():
        ml_results_path = experiment_path
    
    if not ml_results_path.exists():
        return fold_performances
    
    # Get all model directories
    model_dirs = [d for d in ml_results_path.iterdir() 
                  if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        
        # Try reading from detailed_results.json first (has all fold results)
        detailed_results = model_dir / "detailed_results.json"
        
        accuracies = []
        
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
                # Look for results.json
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
    
    return fold_performances

def calculate_percentiles(values: List[float]) -> Dict[str, float]:
    """Calculate percentiles for a list of values."""
    if not values:
        return {}
    
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    
    def percentile(p: float) -> float:
        k = (n - 1) * p
        f = int(k)
        c = k - f
        if f + 1 < n:
            return sorted_vals[f] * (1 - c) + sorted_vals[f + 1] * c
        return sorted_vals[f]
    
    return {
        'min': min(values),
        'q1': percentile(0.25),
        'median': percentile(0.50),
        'q3': percentile(0.75),
        'max': max(values),
        'mean': statistics.mean(values),
        'std': statistics.stdev(values) if len(values) > 1 else 0.0,
        'iqr': percentile(0.75) - percentile(0.25)
    }

def main():
    """Run comprehensive analysis for grid_50_random_folds."""
    
    print("=" * 80)
    print("COMPREHENSIVE ANALYSIS: GRID_50_RANDOM_FOLDS")
    print("=" * 80)
    print()
    
    # Load all summaries
    summaries = {}
    model_comparisons = {}
    fold_performances_all = {}
    
    print("Loading data...")
    print("-" * 80)
    
    for exp_name, exp_path in EXPERIMENTS_50.items():
        print(f"\n📊 {exp_name}:")
        
        # Load summary
        summary = load_summary_json(exp_path)
        if summary:
            summaries[exp_name] = summary
            print(f"   ✅ Loaded overall_summary.json")
        else:
            print(f"   ⚠️  No overall_summary.json found")
        
        # Load model comparison
        model_comparison = load_model_comparison_csv(exp_path)
        if model_comparison is not None:
            model_comparisons[exp_name] = model_comparison
            print(f"   ✅ Loaded model_comparison.csv ({len(model_comparison)} models)")
        else:
            print(f"   ⚠️  No model_comparison.csv found")
        
        # Extract fold performances
        fold_perfs = extract_fold_performances(exp_path)
        if fold_perfs:
            fold_performances_all[exp_name] = fold_perfs
            total_folds = sum(len(accs) for accs in fold_perfs.values())
            print(f"   ✅ Extracted fold performances ({len(fold_perfs)} models, {total_folds} total folds)")
        else:
            print(f"   ⚠️  No fold performances extracted")
    
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    
    # Overall statistics
    print("\n1. OVERALL STATISTICS")
    print("-" * 80)
    
    all_results = []
    for exp_name in EXPERIMENTS_50.keys():
        # If we have a summary, use it; otherwise calculate from fold performances
        if exp_name in summaries:
            summary = summaries[exp_name]
            
            # Handle different summary.json formats
            # Format 1: HPC_experiments style (best_model, accuracy_statistics)
            if 'best_model' in summary and 'accuracy_statistics' in summary:
                best_model = summary.get('best_model', {})
                acc_stats = summary.get('accuracy_statistics', {})
                best_acc = best_model.get('best_test_accuracy', 0)
                mean_acc = acc_stats.get('test_accuracy_mean', 0)
                std_acc = acc_stats.get('test_accuracy_std', 0)
                best_model_name = best_model.get('model_name', 'Unknown')
            
            # Format 2: grid_50 style (overall_statistics, per_model)
            elif 'overall_statistics' in summary:
                acc_stats = summary.get('overall_statistics', {})
                mean_acc = acc_stats.get('mean_accuracy', 0)
                std_acc = acc_stats.get('std_accuracy', 0)
                # Find best model from model_comparison.csv or per_model
                if 'per_model' in summary:
                    best_acc = max([m.get('mean_accuracy', 0) for m in summary['per_model'].values()])
                    # Find which model has the best accuracy
                    best_model_name = max(summary['per_model'].items(), key=lambda x: x[1].get('mean_accuracy', 0))[0]
                else:
                    best_acc = mean_acc
                    best_model_name = 'Unknown'
            
            # Format 3: model_rankings style (like PCA_L_6)
            elif 'model_rankings' in summary:
                rankings = summary.get('model_rankings', [])
                if rankings:
                    best_model_entry = rankings[0]  # Already sorted by best_test_accuracy
                    best_acc = best_model_entry.get('best_test_accuracy', 0)
                    best_model_name = best_model_entry.get('model_name', 'Unknown')
                    mean_acc = best_model_entry.get('best_test_accuracy', 0)  # Use best as mean for now
                    std_acc = best_model_entry.get('std_test_accuracy', 0)
                else:
                    best_acc = 0
                    mean_acc = 0
                    std_acc = 0
                    best_model_name = 'Unknown'
            
            else:
                # Fallback
                best_acc = 0
                mean_acc = 0
                std_acc = 0
                best_model_name = 'Unknown'
        
        # If no summary, calculate from fold performances
        elif exp_name in fold_performances_all:
            fold_perfs = fold_performances_all[exp_name]
            
            # Calculate statistics for each model
            model_stats = {}
            for model_name, accs in fold_perfs.items():
                if accs:
                    stats = calculate_percentiles(accs)
                    model_stats[model_name] = {
                        'mean': stats['mean'],
                        'median': stats['median'],
                        'std': stats['std'],
                        'best': stats['max'],
                        'count': len(accs)
                    }
            
            if model_stats:
                # Find best model (highest mean)
                best_model_name = max(model_stats.items(), key=lambda x: x[1]['mean'])[0]
                best_stats = model_stats[best_model_name]
                
                best_acc = best_stats['best']
                mean_acc = best_stats['mean']
                std_acc = best_stats['std']
            else:
                best_acc = 0
                mean_acc = 0
                std_acc = 0
                best_model_name = 'Unknown'
        else:
            # No data available
            best_acc = 0
            mean_acc = 0
            std_acc = 0
            best_model_name = 'Unknown'
        
        all_results.append({
            'experiment': exp_name,
            'best_accuracy': best_acc,
            'mean_accuracy': mean_acc,
            'std_accuracy': std_acc,
            'best_model': best_model_name
        })
        
        # Print statistics if we have data
        if mean_acc > 0:
            print(f"\n   {exp_name}:")
            print(f"      Best Model: {best_model_name} - {best_acc:.4f}")
            print(f"      Mean Accuracy: {mean_acc:.4f} ± {std_acc:.4f}")
            
            # Show fold performance stats if available
            if exp_name in fold_performances_all:
                fold_perfs = fold_performances_all[exp_name]
                if best_model_name in fold_perfs:
                    fold_accs = fold_perfs[best_model_name]
                    fold_stats = calculate_percentiles(fold_accs)
                    print(f"      Fold Performance (best model across {len(fold_accs)} folds):")
                    print(f"         Median: {fold_stats['median']:.4f}")
                    print(f"         IQR: [{fold_stats['q1']:.4f}, {fold_stats['q3']:.4f}]")
                    print(f"         Range: [{fold_stats['min']:.4f}, {fold_stats['max']:.4f}]")
                    print(f"         Std: {fold_stats['std']:.4f}")
    
    # Calculate overall stats
    if all_results:
        df_results = pd.DataFrame(all_results)
        overall_mean = df_results['mean_accuracy'].mean()
        overall_std = df_results['mean_accuracy'].std()
        overall_best = df_results['best_accuracy'].max()
        
        print(f"\n   Overall (across all configs):")
        print(f"      Mean Accuracy: {overall_mean:.4f} ± {overall_std:.4f}")
        print(f"      Best Accuracy: {overall_best:.4f}")
        print(f"      Total Configs: {len(all_results)}")
    
    # Per-model analysis
    print("\n2. PER-MODEL ANALYSIS")
    print("-" * 80)
    
    model_stats = defaultdict(lambda: {'accuracies': [], 'configs': []})
    
    for exp_name, comparison_df in model_comparisons.items():
        for _, row in comparison_df.iterrows():
            model_name = row['model_name']
            best_acc = row['best_test_accuracy']
            model_stats[model_name]['accuracies'].append(best_acc)
            model_stats[model_name]['configs'].append(exp_name)
    
    print("\n   Best model performance across configs:")
    for model_name in sorted(model_stats.keys()):
        stats = model_stats[model_name]
        mean_acc = statistics.mean(stats['accuracies'])
        std_acc = statistics.stdev(stats['accuracies']) if len(stats['accuracies']) > 1 else 0
        print(f"      {model_name}: {mean_acc:.4f} ± {std_acc:.4f} (across {len(stats['configs'])} configs)")
    
    # ANOVA vs PCA comparison
    print("\n3. ANOVA vs PCA COMPARISON")
    print("-" * 80)
    
    anova_configs = [r for r in all_results if 'anova' in r['experiment'].lower() and r['mean_accuracy'] > 0]
    pca_configs = [r for r in all_results if 'pca' in r['experiment'].lower() and r['mean_accuracy'] > 0]
    
    if anova_configs and pca_configs:
        anova_mean = statistics.mean([r['mean_accuracy'] for r in anova_configs])
        anova_best = max([r['best_accuracy'] for r in anova_configs])
        pca_mean = statistics.mean([r['mean_accuracy'] for r in pca_configs])
        pca_best = max([r['best_accuracy'] for r in pca_configs])
        
        print(f"\n   ANOVA-based configs:")
        print(f"      Mean: {anova_mean:.4f}")
        print(f"      Best: {anova_best:.4f}")
        print(f"      Configs: {[r['experiment'] for r in anova_configs]}")
        
        print(f"\n   PCA-based configs:")
        print(f"      Mean: {pca_mean:.4f}")
        print(f"      Best: {pca_best:.4f}")
        print(f"      Configs: {[r['experiment'] for r in pca_configs]}")
        
        advantage = (anova_mean - pca_mean) * 100
        print(f"\n   ANOVA advantage: +{advantage:.2f} percentage points")
    
    # L_2 vs L_6 comparison
    print("\n4. LEAVE-2 vs LEAVE-6 COMPARISON")
    print("-" * 80)
    
    l2_configs = [r for r in all_results if 'L_2' in r['experiment'] or 'l_2' in r['experiment']]
    l6_configs = [r for r in all_results if 'L_6' in r['experiment'] or 'l_6' in r['experiment']]
    
    if l2_configs and l6_configs:
        l2_mean = statistics.mean([r['mean_accuracy'] for r in l2_configs])
        l2_best = max([r['best_accuracy'] for r in l2_configs])
        l6_mean = statistics.mean([r['mean_accuracy'] for r in l6_configs])
        l6_best = max([r['best_accuracy'] for r in l6_configs])
        
        print(f"\n   Leave-2-out configs:")
        print(f"      Mean: {l2_mean:.4f}")
        print(f"      Best: {l2_best:.4f}")
        print(f"      Configs: {[r['experiment'] for r in l2_configs]}")
        
        print(f"\n   Leave-6-out configs:")
        print(f"      Mean: {l6_mean:.4f}")
        print(f"      Best: {l6_best:.4f}")
        print(f"      Configs: {[r['experiment'] for r in l6_configs]}")
        
        difference = (l2_mean - l6_mean) * 100
        print(f"\n   L_2 vs L_6 difference: {difference:+.2f} percentage points")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    
    # Save summary statistics
    if all_results:
        summary_df = pd.DataFrame(all_results)
        summary_file = OUTPUT_DIR / "grid_50_random_folds_analysis_summary.csv"
        summary_df.to_csv(summary_file, index=False)
        print(f"\n✅ Saved summary to: {summary_file}")

if __name__ == '__main__':
    main()

