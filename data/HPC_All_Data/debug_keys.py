#!/usr/bin/env python
"""Debug: List all available model×HP keys."""

import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/Users/user/projects/eeg-full-pipeline/data/HPC_All_Data")

EXPERIMENTS = {
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

def load_per_subject_accuracies_by_model_hp(exp_name, results_dir):
    """Load per-subject accuracies grouped by model×HP combination."""
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    model_hp_subject_accuracies = defaultdict(lambda: defaultdict(list))
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        model_name = model_dir.name
        
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            
            task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
            
            for task_dir in task_dirs:
                results_file = task_dir / "results.json"
                if not results_file.exists():
                    continue
                
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                    
                    accuracy = data.get('accuracy', 0.0)
                    hyperparams = data.get('hyperparams', {})
                    model_hp_key = f"{model_name}_({', '.join([f'{k}={v}' for k, v in sorted(hyperparams.items())])})"
                    model_hp_subject_accuracies[model_hp_key][fold_name].append(accuracy)
                except:
                    pass
    
    return model_hp_subject_accuracies

for exp_name, results_dir in EXPERIMENTS.items():
    print(f"\n{exp_name}:")
    data = load_per_subject_accuracies_by_model_hp(exp_name, results_dir)
    for key in sorted(data.keys()):
        print(f"  {key}")
