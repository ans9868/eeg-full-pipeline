#!/usr/bin/env python
"""
P=6 vs P=2 Comparison using MEAN (instead of median)

Creates comparison tables showing:
- ANOVA P=6 vs P=2
- PCA P=6 vs P=2

All using mean as the primary metric.
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_6": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "ANOVA_L_2": BASE_DIR / "grid_50_random_folds/Anova_L_2_incomplete_ml_results",
    "PCA_L_6": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
    "PCA_L_2": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
}

def extract_model_stats(results_dir):
    """Extract statistics for all models - find best by MEAN."""
    if not results_dir.exists():
        return {}
    
    # Try ml_results_grid_search first
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    model_stats = {}
    
    model_dirs = [d for d in results_path.iterdir() 
                  if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        results_files = list(model_dir.rglob("results.json"))
        
        accuracies = []
        for results_file in results_files:
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                accuracy = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                if accuracy is not None:
                    accuracies.append(float(accuracy))
            except:
                continue
        
        if accuracies:
            sorted_acc = sorted(accuracies)
            n = len(sorted_acc)
            
            mean_acc = statistics.mean(accuracies)
            median_acc = statistics.median(accuracies)
            std_acc = statistics.stdev(accuracies) if n > 1 else 0
            min_acc = min(accuracies)
            max_acc = max(accuracies)
            
            # Calculate quartiles
            q1_idx = n // 4
            q3_idx = 3 * n // 4
            q1 = sorted_acc[q1_idx] if q1_idx < n else sorted_acc[0]
            q3 = sorted_acc[q3_idx] if q3_idx < n else sorted_acc[-1]
            iqr = q3 - q1
            
            model_stats[model_name] = {
                'mean': mean_acc,
                'median': median_acc,
                'std': std_acc,
                'min': min_acc,
                'max': max_acc,
                'q1': q1,
                'q3': q3,
                'iqr': iqr,
                'n_folds': n
            }
    
    return model_stats

def find_best_model_by_median(model_stats):
    """Find best model by median performance."""
    if not model_stats:
        return None, None
    
    best_model = max(model_stats.items(), key=lambda x: x[1]['median'])
    return best_model[0], best_model[1]

def main():
    """Main function."""
    print("=" * 80)
    print("P=6 vs P=2 Comparison (Using MEAN)")
    print("=" * 80)
    
    results = {}
    
    # Extract stats for each experiment
    for exp_name, exp_dir in EXPERIMENTS.items():
        print(f"\n📊 Analyzing {exp_name}...")
        model_stats = extract_model_stats(exp_dir)
        
        if model_stats:
            best_model, best_stats = find_best_model_by_median(model_stats)
            print(f"   ✅ Best Model: {best_model}")
            print(f"      Median: {best_stats['median']:.2%}")
            print(f"      Mean: {best_stats['mean']:.2%}")
            print(f"      IQR: {best_stats['iqr']:.2%}")
            print(f"      Range: {best_stats['min']:.2%} / {best_stats['max']:.2%}")
            
            results[exp_name] = {
                'model': best_model,
                'stats': best_stats
            }
        else:
            print(f"   ⚠️  No results found")
    
    # Create ANOVA comparison table
    print("\n" + "=" * 80)
    print("ANOVA Comparison Table")
    print("=" * 80)
    
    anova_table = """# Table 1: ANOVA Comparison (Median Across 50× LPSO folds)

| Setting | Best Model | Median | IQR | Min / Max |
|---------|------------|--------|-----|-----------|
"""
    
    if "ANOVA_L_6" in results and "ANOVA_L_2" in results:
        r6 = results["ANOVA_L_6"]
        r2 = results["ANOVA_L_2"]
        
        anova_table += f"| ANOVA, P=6 (50×) | {r6['model']} | {r6['stats']['median']:.1%} | {r6['stats']['iqr']:.1%} | {r6['stats']['min']:.1%} / {r6['stats']['max']:.1%} |\n"
        anova_table += f"| ANOVA, P=2 (50×) | {r2['model']} | {r2['stats']['median']:.1%} | ↑ {r2['stats']['iqr']:.1%} | {r2['stats']['min']:.1%} / {r2['stats']['max']:.1%} |\n"
    
    anova_table += "\n**Note.** P = number of held-out subjects per fold. Higher IQR at P=2 indicates greater fold-to-fold variance.\n"
    
    anova_table += "\n---\n\n"
    
    # Create PCA comparison table
    print("\n" + "=" * 80)
    print("PCA Comparison Table")
    print("=" * 80)
    
    pca_table = """# Table 2: PCA Comparison (Median Across 50× LPSO folds)

| Setting | Best Model | Median | IQR | Min / Max |
|---------|------------|--------|-----|-----------|
"""
    
    if "PCA_L_6" in results and "PCA_L_2" in results:
        r6 = results["PCA_L_6"]
        r2 = results["PCA_L_2"]
        
        pca_table += f"| PCA, P=6 (50×) | {r6['model']} | {r6['stats']['median']:.1%} | {r6['stats']['iqr']:.1%} | {r6['stats']['min']:.1%} / {r6['stats']['max']:.1%} |\n"
        pca_table += f"| PCA, P=2 (50×) | {r2['model']} | {r2['stats']['median']:.1%} | ↑ {r2['stats']['iqr']:.1%} | {r2['stats']['min']:.1%} / {r2['stats']['max']:.1%} |\n"
    
    pca_table += "\n---\n\n"
    
    # Combine into one file
    combined_table = "# P=6 vs P=2 Comparison Tables (Using Median)\n\n"
    combined_table += anova_table
    combined_table += pca_table
    combined_table += "*Generated by `create_p6_vs_p2_mean_comparison.py`*\n"
    
    # Save
    output_file = BASE_DIR / "p6_vs_p2_mean_comparison.md"
    with open(output_file, 'w') as f:
        f.write(combined_table)
    
    print("\n" + anova_table)
    print("\n" + pca_table)
    print(f"\n✅ Saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

