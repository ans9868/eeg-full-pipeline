#!/usr/bin/env python
"""
Table B: Cross-Subject (LPSO, P=6, 50× resamples) — Primary Summary

Shows median, IQR, Min/Max, and best model for PCA and ANOVA under LPSO P=6.
"""

import json
from pathlib import Path
import statistics

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "PCA": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
    "ANOVA": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
}

def extract_model_stats(results_dir):
    """Extract statistics for all models - find best by median."""
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
            
            median_acc = statistics.median(accuracies)
            min_acc = min(accuracies)
            max_acc = max(accuracies)
            
            # Calculate quartiles
            q1_idx = n // 4
            q3_idx = 3 * n // 4
            q1 = sorted_acc[q1_idx] if q1_idx < n else sorted_acc[0]
            q3 = sorted_acc[q3_idx] if q3_idx < n else sorted_acc[-1]
            iqr = q3 - q1
            
            model_stats[model_name] = {
                'median': median_acc,
                'q1': q1,
                'q3': q3,
                'iqr': iqr,
                'min': min_acc,
                'max': max_acc
            }
    
    return model_stats

def find_best_model_by_median(model_stats):
    """Find best model by median performance."""
    if not model_stats:
        return None, None
    
    best_model = max(model_stats.items(), key=lambda x: x[1]['median'])
    return best_model[0], best_model[1]

def format_model_name(model_name, results_dir):
    """Format model name with kernel info for SVM."""
    if 'SVM' in model_name:
        try:
            model_dir = results_dir / model_name if (results_dir / model_name).exists() else None
            if not model_dir:
                results_path = results_dir / "ml_results_grid_search"
                if results_path.exists():
                    model_dir = results_path / model_name
            
            if model_dir:
                results_files = list(model_dir.rglob("results.json"))
                if results_files:
                    with open(results_files[0], 'r') as f:
                        data = json.load(f)
                    kernel = data.get('hyperparams', {}).get('kernel', '')
                    if kernel:
                        return f"SVM ({kernel})"
        except:
            pass
    
    # Format other models
    if 'MLP' in model_name or 'Neural' in model_name:
        return 'MLP (Neural Network)'
    if 'XGBoost' in model_name:
        return 'XGBoost'
    if 'KNN' in model_name:
        return 'KNN'
    
    return model_name.replace('_', ' ')

def main():
    """Main function."""
    print("=" * 80)
    print("TABLE B: Cross-Subject (LPSO, P=6, 50× resamples) — Primary Summary")
    print("=" * 80)
    
    results = {}
    
    # Extract stats for each feature set
    for feature_set, exp_dir in EXPERIMENTS.items():
        print(f"\n📊 Analyzing {feature_set}...")
        model_stats = extract_model_stats(exp_dir)
        
        if model_stats:
            best_model, best_stats = find_best_model_by_median(model_stats)
            print(f"   ✅ Best Model: {best_model}")
            print(f"      Median: {best_stats['median']:.2%}")
            print(f"      IQR: {best_stats['iqr']:.2%}")
            print(f"      Range: {best_stats['min']:.2%} / {best_stats['max']:.2%}")
            
            results[feature_set] = {
                'model': best_model,
                'stats': best_stats
            }
        else:
            print(f"   ⚠️  No results found")
    
    # Create table
    print("\n" + "=" * 80)
    print("TABLE B: Cross-Subject (LPSO, P=6, 50× resamples) — Primary Summary")
    print("=" * 80)
    
    markdown = """# Table B. Cross-Subject (LPSO, P=6, 50× resamples) — Primary Summary

| Feature Set | Median | IQR | Min / Max | Best Model |
|-------------|--------|-----|-----------|------------|
"""
    
    for feature_set in ["PCA", "ANOVA"]:
        if feature_set in results:
            r = results[feature_set]
            model_display = format_model_name(r['model'], EXPERIMENTS[feature_set])
            
            markdown += f"| {feature_set} | {r['stats']['median']:.1%} | {r['stats']['iqr']:.1%} | {r['stats']['min']:.1%} / {r['stats']['max']:.1%} | {model_display} |\n"
    
    markdown += """
---

## Footnote

LPSO = Leave-P-Subjects-Out with P=6 held-out subjects per fold (balanced 3 alz + 3 cntrl). Results use 50 random folds. Best model selected by median performance. Median, IQR, Min/Max computed across all folds for the best model.

*Generated by `create_table_b_cross_subject_summary.py`*
"""
    
    # Save
    output_file = BASE_DIR / "table_b_cross_subject_summary.md"
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print("\n" + markdown)
    print(f"\n✅ Saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()


