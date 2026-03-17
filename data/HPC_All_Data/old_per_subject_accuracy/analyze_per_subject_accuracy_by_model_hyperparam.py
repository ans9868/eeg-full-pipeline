#!/usr/bin/env python
"""
Analyze per-subject accuracy across LPSO folds, broken down by Model × Hyperparameter.

For each subject and each model×hyperparam combination, find all folds where they appear as test,
then calculate:
- Mean accuracy across all folds where subject was tested (for that model×hyperparam)
- Min/Max accuracy (swing)
- Identify subjects with biggest swings across different model/hyperparam combinations
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics
import re

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_6_Random": {
        "path": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
        "description": "ANOVA P=6 (50 random folds)"
    },
    "ANOVA_L_2_Random": {
        "path": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
        "description": "ANOVA P=2 (50 random folds)"
    },
    "PCA_L_6_Random": {
        "path": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
        "description": "PCA P=6 (50 random folds)"
    },
    "PCA_L_2_Random": {
        "path": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
        "description": "PCA P=2 (50 random folds)"
    },
}

def extract_subject_ids_from_fold(fold_dir_name):
    """Extract subject IDs from fold directory name."""
    pattern = r'sub-(\d+)'
    matches = re.findall(pattern, fold_dir_name)
    return [f"sub-{m}" for m in matches]

def extract_hyperparams(results_file):
    """Extract hyperparameters from results.json file."""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        hyperparams = data.get('hyperparams', {})
        # Create a string representation of hyperparams
        if hyperparams:
            # Sort keys for consistent representation
            sorted_keys = sorted(hyperparams.keys())
            param_str = "_".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
            return param_str, hyperparams
        return None, None
    except:
        return None, None

def extract_per_subject_accuracies_by_model_hyperparam(results_dir):
    """Extract per-subject accuracies broken down by model × hyperparameter."""
    if not results_dir.exists():
        return {}
    
    # Try ml_results_grid_search first
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {model_name: {hyperparam_str: {subject_id: [accuracies]}}}
    model_hyperparam_subject_acc = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    model_dirs = [d for d in results_path.iterdir() 
                  if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        fold_dirs = [d for d in model_dir.iterdir() 
                     if d.is_dir() and d.name.startswith('sub-')]
        
        for fold_dir in fold_dirs:
            fold_name = fold_dir.name
            subject_ids = extract_subject_ids_from_fold(fold_name)
            
            # Find results.json in this fold
            results_files = list(fold_dir.rglob("results.json"))
            if not results_files:
                # Try task directories
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
                        
                        # Extract hyperparameters
                        hyperparam_str, hyperparams = extract_hyperparams(results_files[0])
                        if hyperparam_str is None:
                            hyperparam_str = "default"
                        
                        # Add this accuracy to all subjects in this fold for this model×hyperparam
                        for subject_id in subject_ids:
                            model_hyperparam_subject_acc[model_name][hyperparam_str][subject_id].append(acc)
                except Exception as e:
                    continue
    
    return dict(model_hyperparam_subject_acc)

def analyze_subject_swings_by_model_hyperparam(model_hyperparam_subject_acc):
    """Calculate statistics for each subject across all model×hyperparam combinations."""
    # Structure: {subject_id: {model_name: {hyperparam_str: stats}}}
    subject_model_hyperparam_stats = defaultdict(lambda: defaultdict(dict))
    
    # Also track cross-model-hyperparam swings per subject
    subject_all_accuracies = defaultdict(list)  # All accuracies for a subject across all model×hyperparam
    
    for model_name, hyperparam_dict in model_hyperparam_subject_acc.items():
        for hyperparam_str, subject_acc_dict in hyperparam_dict.items():
            for subject_id, accuracies in subject_acc_dict.items():
                if accuracies:
                    stats = {
                        'mean': statistics.mean(accuracies),
                        'median': statistics.median(accuracies),
                        'min': min(accuracies),
                        'max': max(accuracies),
                        'swing': max(accuracies) - min(accuracies),
                        'std': statistics.stdev(accuracies) if len(accuracies) > 1 else 0,
                        'n_folds': len(accuracies)
                    }
                    subject_model_hyperparam_stats[subject_id][model_name][hyperparam_str] = stats
                    subject_all_accuracies[subject_id].extend(accuracies)
    
    # Calculate cross-model-hyperparam swings (biggest difference across all model×hyperparam combos)
    subject_cross_swings = {}
    for subject_id, all_accs in subject_all_accuracies.items():
        if all_accs:
            subject_cross_swings[subject_id] = {
                'min': min(all_accs),
                'max': max(all_accs),
                'swing': max(all_accs) - min(all_accs),
                'mean': statistics.mean(all_accs),
                'n_combinations': len([(m, h) for m in subject_model_hyperparam_stats[subject_id] 
                                       for h in subject_model_hyperparam_stats[subject_id][m]])
            }
    
    return dict(subject_model_hyperparam_stats), subject_cross_swings

def main():
    """Main function."""
    print("=" * 80)
    print("PER-SUBJECT ACCURACY ANALYSIS BY MODEL × HYPERPARAMETER")
    print("=" * 80)
    
    all_results = {}
    all_cross_swings = {}
    
    for exp_name, exp_info in EXPERIMENTS.items():
        print(f"\n📊 Analyzing {exp_name} ({exp_info['description']})...")
        print(f"   Path: {exp_info['path']}")
        
        model_hyperparam_subject_acc = extract_per_subject_accuracies_by_model_hyperparam(exp_info['path'])
        
        if model_hyperparam_subject_acc:
            print(f"   ✅ Found {len(model_hyperparam_subject_acc)} models")
            
            # Count total combinations
            total_combos = sum(len(hp_dict) for model_dict in model_hyperparam_subject_acc.values() 
                              for hp_dict in model_dict.values())
            print(f"   📊 Total model×hyperparam combinations: {total_combos}")
            
            subject_stats, cross_swings = analyze_subject_swings_by_model_hyperparam(model_hyperparam_subject_acc)
            all_results[exp_name] = {
                'per_model_hyperparam': subject_stats,
                'cross_model_swings': cross_swings
            }
            all_cross_swings[exp_name] = cross_swings
            
            # Show summary
            if cross_swings:
                swings = [s['swing'] * 100 for s in cross_swings.values()]
                means = [s['mean'] * 100 for s in cross_swings.values()]
                
                print(f"      Subjects analyzed: {len(cross_swings)}")
                print(f"      Mean accuracy across subjects: {statistics.mean(means):.2f}%")
                print(f"      Mean cross-model swing: {statistics.mean(swings):.2f}%")
                print(f"      Largest cross-model swing: {max(swings):.2f}%")
        else:
            print(f"   ⚠️  No results found")
            all_results[exp_name] = {'per_model_hyperparam': {}, 'cross_model_swings': {}}
    
    # Find biggest cross-model swings
    print("\n" + "=" * 80)
    print("TOP 20 SUBJECTS WITH LARGEST CROSS-MODEL×HYPERPARAM SWINGS")
    print("=" * 80)
    
    all_swings = []
    for exp_name, cross_swings in all_cross_swings.items():
        if cross_swings:
            for subject_id, stats in cross_swings.items():
                all_swings.append({
                    'experiment': exp_name,
                    'subject': subject_id,
                    'swing': stats['swing'] * 100,
                    'mean': stats['mean'] * 100,
                    'min': stats['min'] * 100,
                    'max': stats['max'] * 100,
                    'n_combinations': stats['n_combinations']
                })
    
    all_swings.sort(key=lambda x: x['swing'], reverse=True)
    
    print(f"\n{'Rank':<6} {'Subject':<10} {'Experiment':<30} {'Swing':<8} {'Range':<20} {'Mean':<8} {'N Combos':<10}")
    print("-" * 100)
    for i, swing_data in enumerate(all_swings[:20], 1):
        print(f"{i:2d}.   {swing_data['subject']:8s} | {swing_data['experiment']:28s} | "
              f"{swing_data['swing']:6.1f}% | "
              f"{swing_data['min']:5.1f}%-{swing_data['max']:5.1f}% | "
              f"{swing_data['mean']:5.1f}% | "
              f"{swing_data['n_combinations']:3d}")
    
    # Save detailed results
    print("\n" + "=" * 80)
    print("SAVING DETAILED RESULTS")
    print("=" * 80)
    
    results_file = BASE_DIR / "per_subject_accuracy_by_model_hyperparam.md"
    with open(results_file, 'w') as f:
        f.write("# Per-Subject Accuracy Analysis by Model × Hyperparameter\n\n")
        f.write("This analysis shows per-subject accuracy broken down by each model×hyperparameter combination.\n\n")
        
        # Summary of cross-model swings
        f.write("## Cross-Model×Hyperparameter Swings (Biggest Variance Across All Combinations)\n\n")
        f.write("| Rank | Subject | Experiment | Swing | Range (Min-Max) | Mean | N Combinations |\n")
        f.write("|------|---------|------------|-------|-----------------|------|----------------|\n")
        for i, swing_data in enumerate(all_swings[:30], 1):
            f.write(f"| {i} | {swing_data['subject']} | {swing_data['experiment']} | "
                   f"{swing_data['swing']:.1f}% | "
                   f"{swing_data['min']:.1f}% - {swing_data['max']:.1f}% | "
                   f"{swing_data['mean']:.1f}% | {swing_data['n_combinations']} |\n")
        
        f.write("\n---\n\n")
        
        # Detailed breakdown per experiment
        for exp_name, exp_data in all_results.items():
            if not exp_data['per_model_hyperparam']:
                continue
            
            f.write(f"## {exp_name} - Detailed Breakdown\n\n")
            
            # For each subject, show all model×hyperparam combinations
            subjects = sorted(exp_data['per_model_hyperparam'].keys())
            
            for subject_id in subjects[:20]:  # Show top 20 subjects by cross-model swing
                cross_swing = exp_data['cross_model_swings'].get(subject_id, {})
                if not cross_swing:
                    continue
                
                f.write(f"### {subject_id} (Cross-Model Swing: {cross_swing['swing']:.2%})\n\n")
                f.write("| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |\n")
                f.write("|-------|----------------|------|-----|-----|-------|---------|----------|\n")
                
                for model_name in sorted(exp_data['per_model_hyperparam'][subject_id].keys()):
                    for hyperparam_str, stats in exp_data['per_model_hyperparam'][subject_id][model_name].items():
                        # Format hyperparam string for display
                        hyperparam_display = hyperparam_str.replace("_", ", ") if hyperparam_str != "default" else "default"
                        f.write(f"| {model_name} | {hyperparam_display} | "
                               f"{stats['mean']:.2%} | {stats['min']:.2%} | {stats['max']:.2%} | "
                               f"{stats['swing']:.2%} | {stats['std']:.2%} | {stats['n_folds']} |\n")
                
                f.write("\n")
    
    print(f"   ✅ Saved: {results_file}")
    
    # Save summary of biggest swings
    swings_file = BASE_DIR / "biggest_cross_model_swings.md"
    with open(swings_file, 'w') as f:
        f.write("# Biggest Cross-Model×Hyperparameter Swings\n\n")
        f.write("Subjects with largest accuracy differences across different model×hyperparameter combinations.\n\n")
        f.write("| Rank | Subject | Experiment | Swing | Range (Min-Max) | Mean | N Combinations |\n")
        f.write("|------|---------|------------|-------|-----------------|------|----------------|\n")
        for i, swing_data in enumerate(all_swings[:30], 1):
            f.write(f"| {i} | {swing_data['subject']} | {swing_data['experiment']} | "
                   f"{swing_data['swing']:.1f}% | "
                   f"{swing_data['min']:.1f}% - {swing_data['max']:.1f}% | "
                   f"{swing_data['mean']:.1f}% | {swing_data['n_combinations']} |\n")
    
    print(f"   ✅ Saved: {swings_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

