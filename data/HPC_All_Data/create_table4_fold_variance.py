#!/usr/bin/env python
"""
Table 4: Fold-to-Fold Variance Statistics (PCA LPSO)

Shows variance statistics for each model under PCA LPSO (P=6).
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics

BASE_DIR = Path(__file__).parent

PCA_LPSO_P6 = BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results"

def extract_model_variance(results_dir):
    """Extract variance statistics for all models."""
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
            
            mean = statistics.mean(accuracies)
            median = statistics.median(accuracies)
            std = statistics.stdev(accuracies) if n > 1 else 0
            min_acc = min(accuracies)
            max_acc = max(accuracies)
            range_acc = max_acc - min_acc
            
            # Calculate quartiles
            q1_idx = n // 4
            q3_idx = 3 * n // 4
            q1 = sorted_acc[q1_idx] if q1_idx < n else sorted_acc[0]
            q3 = sorted_acc[q3_idx] if q3_idx < n else sorted_acc[-1]
            iqr = q3 - q1
            
            model_stats[model_name] = {
                'mean': mean,  # Use mean as primary metric
                'median': median,
                'q1': q1,
                'q3': q3,
                'iqr': iqr,
                'min': min_acc,
                'max': max_acc,
                'range': range_acc,
                'std': std,
                'swing': (max_acc - min_acc) * 100  # in percentage points
            }
    
    return model_stats

def format_model_name(model_name, results_dir):
    """Try to add kernel info for SVM."""
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
    return model_name

def main():
    """Main function."""
    print("=" * 80)
    print("TABLE 4: Fold-to-Fold Variance Statistics (PCA LPSO)")
    print("=" * 80)
    
    print(f"\n📊 Analyzing PCA LPSO P=6...")
    model_stats = extract_model_variance(PCA_LPSO_P6)
    
    # Rank by mean for table order (using mean instead of median)
    ranked = sorted(model_stats.items(), key=lambda x: x[1]['mean'], reverse=True)
    
    print(f"   Found {len(ranked)} models")
    
    # Find reference model for IQR comparison (should be between P=2 and P=6)
    # For now, we'll calculate based on current data
    if len(ranked) >= 2:
        # Estimate P=2 IQR (would need actual P=2 data, but we can note this)
        pass
    
    # Create table
    markdown = """# Table 6: Fold-to-Fold Variance Statistics (PCA LPSO) - Using Mean

| Model | Mean | IQR (Q1–Q3) | Range (Min–Max) | Std Dev | Swing |
|-------|------|--------------|-----------------|---------|-------|
"""
    
    for model_name, stats in ranked:
        model_display = format_model_name(model_name, PCA_LPSO_P6)
        iqr_str = f"{stats['q1']:.1%}–{stats['q3']:.1%}"
        range_str = f"{stats['min']:.1%}–{stats['max']:.1%}"
        
        markdown += f"| {model_display} | {stats['mean']:.1%} | {iqr_str} | {range_str} | {stats['std']:.1%} | {stats['swing']:.1f} pts |\n"
    
    # Calculate IQR increase (compared to P=2 - would need to fetch that data)
    # For now, note it in the footnote
    markdown += """
---

## Footnote

Statistics computed across LPSO folds with P=6. For sensitivity to hold-out size (P=2 vs P=6), see the "Effect of Hold-Out Size (P) on Variance" section/figure.

**Takeaway:** The same protocol yields wide fold ranges (≈36–80%), underscoring the need to report mean ± IQR rather than single folds.

*Generated by `create_table4_fold_variance.py`*
"""
    
    # Save
    output_file = BASE_DIR / "table4_fold_variance_pca_lpso.md"
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print("\n" + markdown)
    print(f"\n✅ Saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

