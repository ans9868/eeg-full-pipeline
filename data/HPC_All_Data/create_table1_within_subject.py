#!/usr/bin/env python
"""
Table 1: Within-Subject Best and Mean Accuracies by Experiment and Model

Creates Table 1 showing within-subject performance for:
- PCA_W_F (Fingerprinting)
- PCA_W_C (Classification)
- ANOVA_W_F (Fingerprinting)
- ANOVA_W_C (Classification)
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "PCA_W_F": {
        "path": BASE_DIR / "grid_12_folds/PCA_W_F-3/ml_results_grid_search",
        "task": "Fingerprinting"
    },
    "PCA_W_C": {
        "path": BASE_DIR / "grid_12_folds/PCA_W_C-3/ml_results_grid_search",
        "task": "Classification"
    },
    "ANOVA_W_F": {
        "path": BASE_DIR / "grid_12_folds/ANOVA_W_F/ml_results_grid_search",
        "task": "Fingerprinting"
    },
    "ANOVA_W_C": {
        "path": BASE_DIR / "grid_12_folds/ANOVA_W_C/ml_results_grid_search",
        "task": "Classification"
    },
}

def extract_model_results(results_dir):
    """Extract results for all models in within_subject_split."""
    model_results = {}
    
    if not results_dir.exists():
        return model_results
    
    model_dirs = [d for d in results_dir.iterdir() 
                  if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        within_dir = model_dir / "within_subject_split"
        
        if not within_dir.exists():
            continue
        
        results_files = list(within_dir.rglob("results.json"))
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
            best_acc = max(accuracies)
            mean_acc = statistics.mean(accuracies)
            model_results[model_name] = {
                'best': best_acc,
                'mean': mean_acc,
                'all': accuracies
            }
    
    return model_results

def format_model_name(model_name, model_results):
    """Format model name with hyperparameters if available."""
    # Try to get best model's hyperparams
    if model_results:
        # Look for results file to get hyperparams
        return model_name  # Simplified for now
    
    return model_name

def main():
    """Main function."""
    print("=" * 80)
    print("TABLE 1: Within-Subject Best and Mean Accuracies")
    print("=" * 80)
    
    results = {}
    
    # Extract results for each experiment
    for exp_name, exp_info in EXPERIMENTS.items():
        print(f"\n📊 Analyzing {exp_name} ({exp_info['task']})...")
        model_results = extract_model_results(exp_info['path'])
        
        if model_results:
            # Find best model by best accuracy
            best_model = max(model_results.items(), key=lambda x: x[1]['best'])
            
            results[exp_name] = {
                'task': exp_info['task'],
                'best_model': best_model[0],
                'best_acc': best_model[1]['best'],
                'mean_acc': best_model[1]['mean'],
                'all_models': model_results
            }
            
            print(f"   ✅ Best: {best_model[0]} ({best_model[1]['best']:.2%})")
            print(f"      Mean: {best_model[1]['mean']:.1%}")
        else:
            print(f"   ⚠️  No results found")
    
    # Calculate means
    pca_exps = [r for k, r in results.items() if k.startswith('PCA_')]
    anova_exps = [r for k, r in results.items() if k.startswith('ANOVA_')]
    
    pca_best_mean = statistics.mean([r['best_acc'] for r in pca_exps]) if pca_exps else 0
    pca_mean_mean = statistics.mean([r['mean_acc'] for r in pca_exps]) if pca_exps else 0
    
    anova_best_mean = statistics.mean([r['best_acc'] for r in anova_exps]) if anova_exps else 0
    anova_mean_mean = statistics.mean([r['mean_acc'] for r in anova_exps]) if anova_exps else 0
    
    # Create table
    print("\n" + "=" * 80)
    print("TABLE 1: Within-Subject Best and Mean Accuracies")
    print("=" * 80)
    
    markdown = """# Table 1: Within-Subject Best and Mean Accuracies by Experiment and Model

| Experiment | Task Type | Best Accuracy | Best Model | Mean Accuracy |
|------------|-----------|---------------|------------|---------------|
"""
    
    for exp_name in ["PCA_W_F", "PCA_W_C", "ANOVA_W_F", "ANOVA_W_C"]:
        if exp_name in results:
            r = results[exp_name]
            # Try to format model name with hyperparameters
            model_display = r['best_model']
            
            # Try to get hyperparams for display
            if r['best_model'] in r['all_models']:
                # Could add hyperparam extraction here if needed
                pass
            
            markdown += f"| {exp_name} | {r['task']} | {r['best_acc']:.2%} | {model_display} | {r['mean_acc']:.1%} |\n"
    
    # Add mean rows
    markdown += f"| PCA Mean | Both tasks | {pca_best_mean:.2%} | — | {pca_mean_mean:.1%} |\n"
    markdown += f"| ANOVA Mean | Both tasks | {anova_best_mean:.2%} | — | {anova_mean_mean:.1%} |\n"
    
    markdown += """
---

## Footnote

80/20 within-subject split (train/test from the same person). Features per experiment as labeled (PCA or ANOVA → MinMax). Best model = highest test accuracy on the single split. Values rounded to 2 decimals.

**Takeaway:** These near-ceiling within-subject scores mostly capture subject signatures, not deployable cross-person signals.

*Generated by `create_table1_within_subject.py`*
"""
    
    # Save
    output_file = BASE_DIR / "table1_within_subject_performance.md"
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print(markdown)
    print(f"\n✅ Saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

