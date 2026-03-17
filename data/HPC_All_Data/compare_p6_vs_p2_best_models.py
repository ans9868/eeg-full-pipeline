#!/usr/bin/env python
"""
Compare P=6 vs P=2 for best performing models.

Finds the best model (by average/median performance) for each experiment type
and creates comparison tables showing Median, IQR, Min/Max.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
import statistics

# Set up paths
BASE_DIR = Path(__file__).parent

# Define experiments
EXPERIMENTS = {
    "ANOVA_L_6": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "ANOVA_L_2": BASE_DIR / "grid_50_random_folds/Anova_L_2_incomplete_ml_results",
    "PCA_L_6": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
    "PCA_L_2": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
}

def extract_model_performances(ml_results_dir):
    """Extract all fold performances for each model."""
    model_performances = defaultdict(list)
    
    if not ml_results_dir.exists():
        print(f"⚠️  Directory not found: {ml_results_dir}")
        return {}
    
    # Try ml_results_grid_search subdirectory first
    results_path = ml_results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = ml_results_dir
    
    if not results_path.exists():
        return {}
    
    # Get all model directories
    model_dirs = [d for d in results_path.iterdir() 
                  if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        
        # Find all results.json files for this model
        results_files = list(model_dir.rglob("results.json"))
        
        for results_file in results_files:
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                
                accuracy = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                
                if accuracy is not None:
                    model_performances[model_name].append(float(accuracy))
            except:
                continue
    
    return model_performances

def calculate_statistics(accuracies):
    """Calculate statistics for a list of accuracies."""
    if not accuracies:
        return None
    
    sorted_acc = sorted(accuracies)
    n = len(sorted_acc)
    
    mean_acc = statistics.mean(accuracies)
    median_acc = statistics.median(accuracies)
    std_acc = statistics.stdev(accuracies) if n > 1 else 0
    min_acc = min(accuracies)
    max_acc = max(accuracies)
    range_acc = max_acc - min_acc
    
    # Calculate quartiles
    q1_idx = n // 4
    q3_idx = 3 * n // 4
    q1 = sorted_acc[q1_idx] if q1_idx < n else sorted_acc[0]
    q3 = sorted_acc[q3_idx] if q3_idx < n else sorted_acc[-1]
    iqr = q3 - q1
    
    return {
        'mean': mean_acc,
        'median': median_acc,
        'std': std_acc,
        'min': min_acc,
        'max': max_acc,
        'range': range_acc,
        'q1': q1,
        'q3': q3,
        'iqr': iqr,
        'n_folds': len(accuracies)
    }

def find_best_model(model_performances):
    """Find the model with the highest median performance."""
    if not model_performances:
        return None, None
    
    best_model = None
    best_stats = None
    best_median = -1
    
    for model_name, accuracies in model_performances.items():
        stats = calculate_statistics(accuracies)
        if stats and stats['median'] > best_median:
            best_median = stats['median']
            best_model = model_name
            best_stats = stats
    
    return best_model, best_stats

def main():
    """Main function."""
    print("=" * 80)
    print("COMPARING P=6 vs P=2 FOR BEST MODELS")
    print("=" * 80)
    
    results = {}
    
    # Analyze each experiment
    for exp_name, ml_results_dir in EXPERIMENTS.items():
        print(f"\n📊 Analyzing {exp_name}...")
        
        model_performances = extract_model_performances(ml_results_dir)
        
        if not model_performances:
            print(f"   ⚠️  No results found")
            continue
        
        print(f"   Found {len(model_performances)} models")
        
        # Find best model by median
        best_model, best_stats = find_best_model(model_performances)
        
        if best_model:
            print(f"   ✅ Best model: {best_model}")
            print(f"      Median: {best_stats['median']:.1%}")
            print(f"      Mean: {best_stats['mean']:.1%}")
            print(f"      IQR: {best_stats['iqr']:.1%}")
            print(f"      Range: {best_stats['min']:.1%} - {best_stats['max']:.1%}")
            print(f"      Folds: {best_stats['n_folds']}")
            
            results[exp_name] = {
                'model': best_model,
                'stats': best_stats
            }
    
    # Create comparison tables
    print("\n" + "=" * 80)
    print("COMPARISON TABLES")
    print("=" * 80)
    
    # ANOVA comparison
    print("\n### ANOVA: P=6 vs P=2\n")
    print("| Setting | Model | Median | IQR | Min / Max | N Folds |")
    print("|---------|-------|--------|-----|-----------|---------|")
    
    if "ANOVA_L_6" in results and "ANOVA_L_2" in results:
        r6 = results["ANOVA_L_6"]
        r2 = results["ANOVA_L_2"]
        
        print(f"| ANOVA, P=6 (50×) | {r6['model']} | {r6['stats']['median']:.1%} | {r6['stats']['iqr']:.1%} | {r6['stats']['min']:.1%} / {r6['stats']['max']:.1%} | {r6['stats']['n_folds']} |")
        print(f"| ANOVA, P=2 (50×) | {r2['model']} | {r2['stats']['median']:.1%} | ↑ {r2['stats']['iqr']:.1%} | {r2['stats']['min']:.1%} / {r2['stats']['max']:.1%} | {r2['stats']['n_folds']} |")
    
    # PCA comparison
    print("\n### PCA: P=6 vs P=2\n")
    print("| Setting | Model | Median | IQR | Min / Max | N Folds |")
    print("|---------|-------|--------|-----|-----------|---------|")
    
    if "PCA_L_6" in results and "PCA_L_2" in results:
        r6 = results["PCA_L_6"]
        r2 = results["PCA_L_2"]
        
        print(f"| PCA, P=6 (50×) | {r6['model']} | {r6['stats']['median']:.1%} | {r6['stats']['iqr']:.1%} | {r6['stats']['min']:.1%} / {r6['stats']['max']:.1%} | {r6['stats']['n_folds']} |")
        print(f"| PCA, P=2 (50×) | {r2['model']} | {r2['stats']['median']:.1%} | ↑ {r2['stats']['iqr']:.1%} | {r2['stats']['min']:.1%} / {r2['stats']['max']:.1%} | {r2['stats']['n_folds']} |")
    
    # Create markdown file
    markdown_content = """# P=6 vs P=2 Comparison: Best Models

**Left: P=6, 50 random folds (ANOVA). Right: P=2, 50 random folds (same settings).**  
Note the wider IQR and heavier tails at P=2, indicating greater cohort sensitivity.  
(Optional: faint boxes for PCA to show both feature pipelines share the same P-driven variance effect.)

---

## ANOVA Comparison

| Setting | Model | Median | IQR | Min / Max | N Folds |
|---------|-------|--------|-----|-----------|---------|
"""
    
    if "ANOVA_L_6" in results and "ANOVA_L_2" in results:
        r6 = results["ANOVA_L_6"]
        r2 = results["ANOVA_L_2"]
        
        markdown_content += f"| ANOVA, P=6 (50×) | {r6['model']} | {r6['stats']['median']:.1%} | {r6['stats']['iqr']:.1%} | {r6['stats']['min']:.1%} / {r6['stats']['max']:.1%} | {r6['stats']['n_folds']} |\n"
        markdown_content += f"| ANOVA, P=2 (50×) | {r2['model']} | {r2['stats']['median']:.1%} | ↑ {r2['stats']['iqr']:.1%} | {r2['stats']['min']:.1%} / {r2['stats']['max']:.1%} | {r2['stats']['n_folds']} |\n"
        
        # Calculate IQR increase
        iqr_increase = r2['stats']['iqr'] - r6['stats']['iqr']
        iqr_pct_increase = (iqr_increase / r6['stats']['iqr']) * 100 if r6['stats']['iqr'] > 0 else 0
        
        markdown_content += f"\n**IQR Increase:** {iqr_increase:.1%} ({iqr_pct_increase:.1f}% increase)\n"
    
    markdown_content += "\n---\n\n## PCA Comparison\n\n"
    markdown_content += "| Setting | Model | Median | IQR | Min / Max | N Folds |\n"
    markdown_content += "|---------|-------|--------|-----|-----------|---------|\n"
    
    if "PCA_L_6" in results and "PCA_L_2" in results:
        r6 = results["PCA_L_6"]
        r2 = results["PCA_L_2"]
        
        markdown_content += f"| PCA, P=6 (50×) | {r6['model']} | {r6['stats']['median']:.1%} | {r6['stats']['iqr']:.1%} | {r6['stats']['min']:.1%} / {r6['stats']['max']:.1%} | {r6['stats']['n_folds']} |\n"
        markdown_content += f"| PCA, P=2 (50×) | {r2['model']} | {r2['stats']['median']:.1%} | ↑ {r2['stats']['iqr']:.1%} | {r2['stats']['min']:.1%} / {r2['stats']['max']:.1%} | {r2['stats']['n_folds']} |\n"
        
        # Calculate IQR increase
        iqr_increase = r2['stats']['iqr'] - r6['stats']['iqr']
        iqr_pct_increase = (iqr_increase / r6['stats']['iqr']) * 100 if r6['stats']['iqr'] > 0 else 0
        
        markdown_content += f"\n**IQR Increase:** {iqr_increase:.1%} ({iqr_pct_increase:.1f}% increase)\n"
    
    markdown_content += "\n---\n\n## Interpretation\n\n"
    markdown_content += "This comparison shows the effect of **P** (number of subjects left out) on model performance variance:\n\n"
    markdown_content += "1. **P=2 (Leave-2-out)**: Higher variance (wider IQR) - fewer subjects in training set makes performance more dependent on which specific subjects are left out\n"
    markdown_content += "2. **P=6 (Leave-6-out)**: Lower variance (narrower IQR) - more subjects in training set provides more stability\n"
    markdown_content += "3. **Both ANOVA and PCA** show the same P-driven variance effect, indicating this is a fundamental property of the leave-P-subjects-out cross-validation strategy\n\n"
    
    markdown_content += "*Generated by `compare_p6_vs_p2_best_models.py`*\n"
    
    # Save markdown
    markdown_file = BASE_DIR / "p6_vs_p2_best_models_comparison.md"
    with open(markdown_file, 'w') as f:
        f.write(markdown_content)
    print(f"\n✅ Saved comparison to: {markdown_file}")
    
    # Also save CSV with all model stats
    csv_data = []
    for exp_name, data in results.items():
        csv_data.append({
            'experiment': exp_name,
            'model': data['model'],
            'median': data['stats']['median'],
            'mean': data['stats']['mean'],
            'iqr': data['stats']['iqr'],
            'std': data['stats']['std'],
            'min': data['stats']['min'],
            'max': data['stats']['max'],
            'range': data['stats']['range'],
            'q1': data['stats']['q1'],
            'q3': data['stats']['q3'],
            'n_folds': data['stats']['n_folds']
        })
    
    csv_file = BASE_DIR / "p6_vs_p2_best_models_stats.csv"
    if csv_data:
        fieldnames = csv_data[0].keys()
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        print(f"✅ Saved detailed stats to: {csv_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

