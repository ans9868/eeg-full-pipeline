#!/usr/bin/env python
"""
Compare Within-Subject vs LPSO (P=6) for PCA and ANOVA.

Creates Table 2 showing:
- Within-Subject (best)
- LPSO Best
- Drop (points)
- LPSO Mean ± SD
- LPSO Best Model
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
import statistics

# Set up paths
BASE_DIR = Path(__file__).parent

# Define experiments
WITHIN_SUBJECT_EXPERIMENTS = {
    "ANOVA": BASE_DIR / "grid_12_folds/ANOVA_W_C/ml_results_grid_search",
    "PCA": BASE_DIR / "grid_12_folds/PCA_W_C-3/ml_results_grid_search",
}

LPSO_P6_EXPERIMENTS = {
    "ANOVA": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "PCA": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

def extract_best_performance(ml_results_dir, exp_type="within"):
    """Extract best model performance from results directory."""
    if not ml_results_dir.exists():
        print(f"⚠️  Directory not found: {ml_results_dir}")
        return None, None
    
    # For within-subject, look in within_subject_split folder
    if exp_type == "within":
        results_path = ml_results_dir
        # Look for within_subject_split in each model directory
        model_dirs = [d for d in results_path.iterdir() 
                      if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    else:
        # For LPSO, try ml_results_grid_search first
        results_path = ml_results_dir / "ml_results_grid_search"
        if not results_path.exists():
            results_path = ml_results_dir
        
        model_dirs = [d for d in results_path.iterdir() 
                      if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    if not model_dirs:
        return None, None
    
    best_performance = -1
    best_model = None
    best_stats = None
    
    # Collect all model performances
    model_performances = {}
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        
        # Find results.json files
        if exp_type == "within":
            # Look specifically in within_subject_split subdirectory
            within_dir = model_dir / "within_subject_split"
            if not within_dir.exists():
                continue
            results_files = list(within_dir.rglob("results.json"))
        else:
            # For LPSO, get all results.json files in model directory
            results_files = list(model_dir.rglob("results.json"))
        
        if not results_files:
            continue
        
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
            if exp_type == "within":
                # For within-subject, take the best single performance
                best_acc = max(accuracies)
                if best_acc > best_performance:
                    best_performance = best_acc
                    best_model = model_name
                    best_stats = {'best': best_acc}
            else:
                # For LPSO, calculate statistics across all folds
                mean_acc = statistics.mean(accuracies)
                median_acc = statistics.median(accuracies)
                std_acc = statistics.stdev(accuracies) if len(accuracies) > 1 else 0
                max_acc = max(accuracies)
                
                model_performances[model_name] = {
                    'mean': mean_acc,
                    'median': median_acc,
                    'std': std_acc,
                    'max': max_acc,
                    'accuracies': accuracies
                }
    
    if exp_type == "within":
        return best_model, best_stats
    else:
        # Find best model by median (or mean if median not available)
        if model_performances:
            best_model = max(model_performances.items(), key=lambda x: x[1]['median'])
            return best_model[0], {
                'mean': best_model[1]['mean'],
                'median': best_model[1]['median'],
                'std': best_model[1]['std'],
                'best': best_model[1]['max'],
                'accuracies': best_model[1]['accuracies']
            }
    
    return None, None

def format_model_name(model_name):
    """Format model name for display (e.g., add kernel info if SVM)."""
    # Check if we can find kernel info from results
    return model_name

def main():
    """Main function."""
    print("=" * 80)
    print("COMPARING WITHIN-SUBJECT vs LPSO (P=6)")
    print("=" * 80)
    
    results = {}
    
    # Analyze within-subject experiments
    print("\n📊 Analyzing Within-Subject Experiments...")
    for feature_set, ws_dir in WITHIN_SUBJECT_EXPERIMENTS.items():
        print(f"   {feature_set}...")
        best_model, stats = extract_best_performance(ws_dir, exp_type="within")
        
        if best_model and stats:
            print(f"      ✅ Best: {best_model} ({stats['best']:.2%})")
            results[feature_set] = {
                'within': {
                    'model': best_model,
                    'best': stats['best']
                }
            }
        else:
            print(f"      ⚠️  No results found")
    
    # Analyze LPSO P=6 experiments
    print("\n📊 Analyzing LPSO P=6 Experiments...")
    for feature_set, lpso_dir in LPSO_P6_EXPERIMENTS.items():
        print(f"   {feature_set}...")
        best_model, stats = extract_best_performance(lpso_dir, exp_type="lpso")
        
        if best_model and stats:
            print(f"      ✅ Best Model: {best_model}")
            print(f"         Median: {stats['median']:.2%}")
            print(f"         Mean: {stats['mean']:.2%} ± {stats['std']:.2%}")
            print(f"         Best: {stats['best']:.2%}")
            
            if feature_set in results:
                results[feature_set]['lpso'] = {
                    'model': best_model,
                    'mean': stats['mean'],
                    'std': stats['std'],
                    'median': stats['median'],
                    'best': stats['best']
                }
            else:
                results[feature_set] = {
                    'lpso': {
                        'model': best_model,
                        'mean': stats['mean'],
                        'std': stats['std'],
                        'median': stats['median'],
                        'best': stats['best']
                    }
                }
        else:
            print(f"      ⚠️  No results found")
    
    # Create comparison table
    print("\n" + "=" * 80)
    print("TABLE 2: Within-Subject vs LPSO (P=6)")
    print("=" * 80)
    
    table_rows = []
    
    for feature_set in ["PCA", "ANOVA"]:
        if feature_set not in results:
            continue
        
        row = {}
        row['feature_set'] = feature_set
        
        # Within-subject best
        if 'within' in results[feature_set]:
            within_best = results[feature_set]['within']['best']
            row['within_best'] = within_best
            row['within_model'] = results[feature_set]['within']['model']
        else:
            row['within_best'] = None
            row['within_model'] = "N/A"
        
        # LPSO best
        if 'lpso' in results[feature_set]:
            lpso_best = results[feature_set]['lpso']['best']
            lpso_mean = results[feature_set]['lpso']['mean']
            lpso_std = results[feature_set]['lpso']['std']
            lpso_model = results[feature_set]['lpso']['model']
            
            row['lpso_best'] = lpso_best
            row['lpso_mean'] = lpso_mean
            row['lpso_std'] = lpso_std
            row['lpso_model'] = lpso_model
            
            # Calculate drop in percentage points (not ratio)
            if row['within_best']:
                drop = (lpso_best - within_best) * 100  # Convert to percentage points
                row['drop'] = drop
            else:
                row['drop'] = None
        else:
            row['lpso_best'] = None
            row['lpso_mean'] = None
            row['lpso_std'] = None
            row['lpso_model'] = "N/A"
            row['drop'] = None
        
        table_rows.append(row)
    
    # Print markdown table
    print("\n```markdown")
    print("| Feature Set | Within-Subject (best) | LPSO Best | Drop (pts) | LPSO Mean ± SD | LPSO Best Model |")
    print("|-------------|----------------------|-----------|------------|----------------|-----------------|")
    
    for row in table_rows:
        within_str = f"{row['within_best']:.2%}" if row['within_best'] else "N/A"
        lpso_best_str = f"{row['lpso_best']:.2%}" if row['lpso_best'] else "N/A"
        drop_str = f"{row['drop']:.1f}" if row['drop'] is not None else "N/A"
        lpso_mean_str = f"{row['lpso_mean']:.2%} ± {row['lpso_std']:.2%}" if row['lpso_mean'] is not None else "N/A"
        
        print(f"| {row['feature_set']} | {within_str} | {lpso_best_str} | {drop_str} | {lpso_mean_str} | {row['lpso_model']} |")
    
    # Calculate delta row (ANOVA - PCA)
    print()
    if len(table_rows) == 2:
        pca_row = next((r for r in table_rows if r['feature_set'] == 'PCA'), None)
        anova_row = next((r for r in table_rows if r['feature_set'] == 'ANOVA'), None)
        
        if pca_row and anova_row:
            delta_within = None
            delta_lpso_best = None
            delta_drop = None
            delta_mean = None
            
            if pca_row['within_best'] and anova_row['within_best']:
                delta_within = anova_row['within_best'] - pca_row['within_best']
            
            if pca_row['lpso_best'] and anova_row['lpso_best']:
                delta_lpso_best = anova_row['lpso_best'] - pca_row['lpso_best']
            
            if pca_row['drop'] is not None and anova_row['drop'] is not None:
                delta_drop = anova_row['drop'] - pca_row['drop']
            
            if pca_row['lpso_mean'] and anova_row['lpso_mean']:
                delta_mean = anova_row['lpso_mean'] - pca_row['lpso_mean']
            
            delta_within_str = f"{delta_within:.1f}" if delta_within is not None else "N/A"
            delta_lpso_str = f"{delta_lpso_best:.1f}" if delta_lpso_best is not None else "N/A"
            delta_drop_str = f"{delta_drop:.1f}" if delta_drop is not None else "N/A"
            delta_mean_str = f"{delta_mean:.1f}" if delta_mean is not None else "N/A"
            
            print(f"| Δ (ANOVA−PCA) | {delta_within_str} | {delta_lpso_str} | {delta_drop_str} | {delta_mean_str} | — |")
    
    print("```")
    
    # Create markdown file
    markdown_content = """# Table 2: Within-Subject vs LPSO (P=6)

This table compares within-subject performance (where the same subjects appear in both train and test) with LPSO (Leave-6-Subjects-Out) performance, which uses different subjects for training and testing.

---

| Feature Set | Within-Subject (best) | LPSO Best | Drop (pts) | LPSO Mean ± SD | LPSO Best Model |
|-------------|----------------------|-----------|------------|----------------|-----------------|
"""
    
    for row in table_rows:
        within_str = f"{row['within_best']:.2%}" if row['within_best'] else "N/A"
        lpso_best_str = f"{row['lpso_best']:.2%}" if row['lpso_best'] else "N/A"
        drop_str = f"{row['drop']:.1f}" if row['drop'] is not None else "N/A"
        lpso_mean_str = f"{row['lpso_mean']:.2%} ± {row['lpso_std']:.2%}" if row['lpso_mean'] is not None else "N/A"
        
        markdown_content += f"| {row['feature_set']} | {within_str} | {lpso_best_str} | {drop_str} | {lpso_mean_str} | {row['lpso_model']} |\n"
    
    # Delta row
    if len(table_rows) == 2:
        pca_row = next((r for r in table_rows if r['feature_set'] == 'PCA'), None)
        anova_row = next((r for r in table_rows if r['feature_set'] == 'ANOVA'), None)
        
        if pca_row and anova_row:
            delta_within = None
            delta_lpso_best = None
            delta_drop = None
            delta_mean = None
            
            if pca_row['within_best'] and anova_row['within_best']:
                delta_within = anova_row['within_best'] - pca_row['within_best']
            
            if pca_row['lpso_best'] and anova_row['lpso_best']:
                delta_lpso_best = anova_row['lpso_best'] - pca_row['lpso_best']
            
            if pca_row['drop'] is not None and anova_row['drop'] is not None:
                delta_drop = anova_row['drop'] - pca_row['drop']
            
            if pca_row['lpso_mean'] and anova_row['lpso_mean']:
                delta_mean = anova_row['lpso_mean'] - pca_row['lpso_mean']
            
            delta_within_str = f"{delta_within:.1f}" if delta_within is not None else "N/A"
            delta_lpso_str = f"{delta_lpso_best:.1f}" if delta_lpso_best is not None else "N/A"
            delta_drop_str = f"{delta_drop:.1f}" if delta_drop is not None else "N/A"
            delta_mean_str = f"{delta_mean:.1f}" if delta_mean is not None else "N/A"
            
            markdown_content += f"| Δ (ANOVA−PCA) | {delta_within_str} | {delta_lpso_str} | {delta_drop_str} | {delta_mean_str} | — |\n"
    
    markdown_content += """
---

## Interpretation

- **Within-Subject (best)**: Best model performance when same subjects appear in both training and testing (80/20 split per subject)
- **LPSO Best**: Best single-fold performance in Leave-6-Subjects-Out cross-validation
- **Drop (pts)**: Performance drop from within-subject to LPSO (negative = LPSO lower)
- **LPSO Mean ± SD**: Average performance across all LPSO folds with standard deviation
- **LPSO Best Model**: Model that achieved the best performance in LPSO

**Key Observations:**
1. Within-subject performance is typically higher because models can learn subject-specific patterns
2. LPSO performance is lower because models must generalize to unseen subjects
3. The drop shows how much performance decreases when evaluating on truly unseen subjects
4. Δ (ANOVA−PCA) shows the difference between ANOVA and PCA feature extraction methods

*Generated by `compare_within_vs_lpso_p6.py`*
"""
    
    # Save markdown
    markdown_file = BASE_DIR / "within_vs_lpso_p6_comparison.md"
    with open(markdown_file, 'w') as f:
        f.write(markdown_content)
    print(f"\n✅ Saved comparison to: {markdown_file}")
    
    # Save CSV
    csv_file = BASE_DIR / "within_vs_lpso_p6_stats.csv"
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['feature_set', 'within_best', 'within_model', 'lpso_best', 'lpso_mean', 'lpso_std', 'lpso_model', 'drop']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in table_rows:
            writer.writerow(row)
    print(f"✅ Saved detailed stats to: {csv_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

