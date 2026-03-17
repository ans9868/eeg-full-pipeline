#!/usr/bin/env python
"""
Table C: LPSO (P=6, 50×) Leaderboard by Transform (Medians)

Ranks models by median performance for PCA and ANOVA separately.
"""

import json
from pathlib import Path
import statistics

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "PCA": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
    "ANOVA": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
}

def extract_model_medians(results_dir):
    """Extract median performance for all models."""
    if not results_dir.exists():
        return {}
    
    # Try ml_results_grid_search first
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    model_medians = {}
    
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
            median_acc = statistics.median(accuracies)
            model_medians[model_name] = median_acc
    
    return model_medians

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
        return 'MLP'
    if 'XGBoost' in model_name:
        return 'XGBoost'
    if 'KNN' in model_name:
        return 'KNN'
    
    return model_name.replace('_', ' ')

def main():
    """Main function."""
    print("=" * 80)
    print("TABLE C: LPSO (P=6, 50×) Leaderboard by Transform (Medians)")
    print("=" * 80)
    
    all_results = {}
    
    # Extract medians for each transform
    for transform, exp_dir in EXPERIMENTS.items():
        print(f"\n📊 Analyzing {transform}...")
        model_medians = extract_model_medians(exp_dir)
        
        if model_medians:
            # Rank by median (highest first)
            ranked = sorted(model_medians.items(), key=lambda x: x[1], reverse=True)
            all_results[transform] = ranked
            
            print(f"   Found {len(ranked)} models")
            for i, (model, median) in enumerate(ranked, 1):
                print(f"   {i}. {model}: {median:.2%}")
        else:
            print(f"   ⚠️  No results found")
    
    # Create table
    print("\n" + "=" * 80)
    print("TABLE C: LPSO (P=6, 50×) Leaderboard by Transform (Medians)")
    print("=" * 80)
    
    markdown = """# Table C. LPSO (P=6, 50×) Leaderboard by Transform (Medians)

| Rank | PCA (Median) | ANOVA (Median) |
|------|--------------|----------------|
"""
    
    # Get max rank
    max_rank = max(len(all_results.get('PCA', [])), len(all_results.get('ANOVA', [])))
    
    pca_results = all_results.get('PCA', [])
    anova_results = all_results.get('ANOVA', [])
    
    # Format rows
    for rank in range(max_rank):
        rank_num = rank + 1
        
        # PCA entry
        if rank < len(pca_results):
            pca_model, pca_median = pca_results[rank]
            pca_formatted = format_model_name(pca_model, EXPERIMENTS['PCA'])
            pca_entry = f"{pca_formatted} — {pca_median:.1%}"
        else:
            pca_entry = "—"
        
        # ANOVA entry
        if rank < len(anova_results):
            anova_model, anova_median = anova_results[rank]
            anova_formatted = format_model_name(anova_model, EXPERIMENTS['ANOVA'])
            anova_entry = f"{anova_formatted} — {anova_median:.1%}"
        else:
            anova_entry = "—"
        
        markdown += f"| {rank_num} | {pca_entry} | {anova_entry} |\n"
    
    markdown += """
---

## Footnote

LPSO = Leave-P-Subjects-Out with P=6 held-out subjects per fold (balanced 3 alz + 3 cntrl). Results use 50 random folds. Medians computed across folds for each model.

*Generated by `create_table_c_lpso_leaderboard.py`*
"""
    
    # Save
    output_file = BASE_DIR / "table_c_lpso_leaderboard.md"
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print("\n" + markdown)
    print(f"\n✅ Saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()


