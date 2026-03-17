#!/usr/bin/env python
"""
Plot fold-by-fold accuracy for each model×hyperparameter combination.

For PCA_L_6_Random (or any experiment), shows:
- X-axis: Fold number (1-50)
- Y-axis: Accuracy (average of correct predictions)
- One line per model×HP combination
"""

import json
import pandas as pd
from pathlib import Path
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import re

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "ANOVA_L_6_Uniform": BASE_DIR / "grid_12_folds/ANOVA_L_6_C_Resource_Boosted",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
    "PCA_L_6_Uniform": BASE_DIR / "grid_12_folds/PCA_L_6_C-3",
}

def extract_hyperparams(results_file):
    """Extract hyperparameters from results.json file."""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        return data.get('hyperparams', {})
    except:
        return {}

def format_model_hp_label(model_name, hyperparams):
    """Format model×hyperparameter label."""
    if hyperparams:
        sorted_keys = sorted(hyperparams.keys())
        param_str = ", ".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
        return f"{model_name} ({param_str})"
    else:
        return f"{model_name} (default)"

def load_fold_accuracies(exp_name, results_dir):
    """
    Load accuracy for each fold×model×HP combination.
    
    Returns:
        {model_hp_key: [(fold_num, accuracy)]}
    """
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {model_hp_key: [(fold_name, accuracy)]}
    model_hp_fold_accuracies = defaultdict(list)
    
    # Get all fold names to sort them
    all_fold_names = set()
    
    # First pass: collect all fold names
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        for fold_dir in model_dir.iterdir():
            if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
                all_fold_names.add(fold_dir.name)
    
    # Sort fold names (they should be consistent across models)
    sorted_fold_names = sorted(all_fold_names)
    
    # Second pass: collect accuracies
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        model_name = model_dir.name
        
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            
            # Find results.json
            results_files = list(fold_dir.rglob("results.json"))
            if not results_files:
                task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
                for task_dir in task_dirs:
                    results_file = task_dir / "results.json"
                    if results_file.exists():
                        results_files.append(results_file)
                        break
            
            if results_files:
                try:
                    with open(results_files[0], 'r') as f:
                        data = json.load(f)
                    accuracy = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                    if accuracy is not None:
                        acc = float(accuracy)
                        hyperparams = extract_hyperparams(results_files[0])
                        
                        # Create model×HP key
                        model_hp_key = format_model_hp_label(model_name, hyperparams)
                        
                        # Store fold number (index in sorted list + 1)
                        fold_num = sorted_fold_names.index(fold_name) + 1
                        model_hp_fold_accuracies[model_hp_key].append((fold_num, acc))
                except Exception as e:
                    continue
    
    # Sort by fold number for each model×HP
    for model_hp_key in model_hp_fold_accuracies:
        model_hp_fold_accuracies[model_hp_key].sort(key=lambda x: x[0])
    
    return model_hp_fold_accuracies

def plot_fold_by_fold_accuracy(exp_name, model_hp_fold_accuracies, output_dir):
    """Create plot showing fold-by-fold accuracy for each model×HP."""
    if not model_hp_fold_accuracies:
        return False
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Colors for different model×HP combinations
    colors = plt.cm.tab20(range(len(model_hp_fold_accuracies)))
    
    for idx, (model_hp_key, fold_accs) in enumerate(sorted(model_hp_fold_accuracies.items())):
        if not fold_accs:
            continue
        
        fold_nums = [x[0] for x in fold_accs]
        accuracies = [x[1] for x in fold_accs]
        
        # Truncate label if too long
        label = model_hp_key[:50] + "..." if len(model_hp_key) > 50 else model_hp_key
        
        ax.plot(fold_nums, accuracies, marker='o', label=label, 
                color=colors[idx], alpha=0.7, linewidth=1.5, markersize=3)
    
    # Add 50% threshold line
    ax.axhline(y=0.5, color='red', linestyle='--', linewidth=2, 
               label='50% Threshold (Correct Classification)', alpha=0.7)
    
    ax.set_xlabel('Fold Number', fontsize=13, fontweight='bold')
    ax.set_ylabel('Accuracy (Average of Correct Predictions)', fontsize=13, fontweight='bold')
    ax.set_title(f'{exp_name}\nFold-by-Fold Accuracy for Each Model×Hyperparameter Combination',
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 51)
    ax.set_ylim(0, 1.05)
    
    # Legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    
    plt.tight_layout()
    output_file = output_dir / f'{exp_name}_fold_by_fold_accuracy.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        # Load fold-by-fold accuracies
        model_hp_fold_accuracies = load_fold_accuracies(exp_name, results_dir)
        
        if not model_hp_fold_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found {len(model_hp_fold_accuracies)} model×HP combinations")
        
        # Create plot
        plot_fold_by_fold_accuracy(exp_name, model_hp_fold_accuracies, output_dir)
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

