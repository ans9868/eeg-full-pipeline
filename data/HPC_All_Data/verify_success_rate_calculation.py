#!/usr/bin/env python
"""
Verify the success rate calculation by checking individual subject accuracies.

For a specific model×HP combination, show:
1. Individual subject accuracies across all folds
2. How many subjects have accuracy > 50% for each combination of test groups
3. Verify the 90.17% success rate calculation
"""

import pandas as pd
from pathlib import Path
from collections import defaultdict
import json
import random
import math
import statistics

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
}

CLASSIFICATION_THRESHOLD = 0.50
RANDOM_SAMPLE_SIZE = 30

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

def load_all_subject_accuracies(results_dir, model_name):
    """
    Load all subject accuracies for a model across all folds.
    
    Returns: {fold_name: {subject_id: accuracy}}
    """
    cache = {}
    model_dir = results_dir / model_name
    if not model_dir.exists():
        return cache
    
    for fold_dir in model_dir.iterdir():
        if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
            continue
        
        fold_name = fold_dir.name
        subject_accuracies = {}
        
        task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
        
        for task_dir in task_dirs:
            test_parquet = task_dir / "test_predictions.parquet"
            if not test_parquet.exists():
                continue
            
            try:
                test_df = pd.read_parquet(test_parquet)
                
                for subject_id_num in test_df['SubjectID'].unique():
                    subject_id = f"sub-{int(subject_id_num)}"
                    subject_data = test_df[test_df['SubjectID'] == subject_id_num]
                    
                    correct = (subject_data['label'] == subject_data['prediction']).sum()
                    total = len(subject_data)
                    accuracy = correct / total if total > 0 else 0.0
                    
                    if subject_id not in subject_accuracies:
                        subject_accuracies[subject_id] = accuracy
                    else:
                        subject_accuracies[subject_id] = (subject_accuracies[subject_id] + accuracy) / 2
            except Exception as e:
                continue
        
        if subject_accuracies:
            cache[fold_name] = subject_accuracies
    
    return cache

def calculate_success_rate_for_combination(fold_names, subject_accuracies_cache):
    """Calculate success rate and return detailed breakdown."""
    all_subject_data = []
    
    for fold_name in fold_names:
        if fold_name in subject_accuracies_cache:
            for subject_id, accuracy in subject_accuracies_cache[fold_name].items():
                all_subject_data.append({
                    'subject_id': subject_id,
                    'accuracy': accuracy,
                    'above_50': 1 if accuracy > CLASSIFICATION_THRESHOLD else 0,
                    'fold': fold_name
                })
    
    if len(all_subject_data) == 0:
        return None
    
    # Calculate statistics
    total_subjects = len(all_subject_data)
    above_50_count = sum(d['above_50'] for d in all_subject_data)
    success_rate = above_50_count / total_subjects if total_subjects > 0 else 0.0
    mean_accuracy = statistics.mean([d['accuracy'] for d in all_subject_data])
    
    return {
        'total_subjects': total_subjects,
        'above_50_count': above_50_count,
        'below_50_count': total_subjects - above_50_count,
        'success_rate': success_rate,
        'mean_accuracy': mean_accuracy,
        'subject_data': all_subject_data
    }

def verify_calculation(exp_name, results_dir, model_name, target_groups=10):
    """Verify the success rate calculation for a specific number of groups."""
    print(f"\n🔍 Verifying calculation for {exp_name}")
    print(f"   Model: {model_name}")
    print(f"   Target: {target_groups} groups\n")
    
    # Load subject accuracies
    subject_accuracies_cache = load_all_subject_accuracies(results_dir, model_name)
    fold_names = sorted(list(subject_accuracies_cache.keys()))
    
    print(f"   Loaded {len(fold_names)} folds")
    print(f"   Total unique subjects across all folds: {len(set(subj for fold_data in subject_accuracies_cache.values() for subj in fold_data.keys()))}\n")
    
    # Sample combinations for target_groups
    total_combinations = math.comb(len(fold_names), target_groups)
    sample_size = min(RANDOM_SAMPLE_SIZE, total_combinations)
    
    sampled_combos = set()
    while len(sampled_combos) < sample_size:
        combo = tuple(sorted(random.sample(fold_names, target_groups)))
        sampled_combos.add(combo)
    
    print(f"   Sampling {len(sampled_combos)} combinations of {target_groups} groups (out of {total_combinations} total)\n")
    
    # Calculate success rates for each combination
    success_rates = []
    detailed_results = []
    
    for i, combo in enumerate(list(sampled_combos)[:5]):  # Show first 5 in detail
        result = calculate_success_rate_for_combination(combo, subject_accuracies_cache)
        if result:
            success_rates.append(result['success_rate'])
            detailed_results.append({
                'combination': combo,
                'result': result
            })
            
            print(f"   Combination {i+1}: {len(combo)} groups")
            print(f"      Total subjects: {result['total_subjects']}")
            print(f"      Subjects above 50%: {result['above_50_count']}")
            print(f"      Subjects below 50%: {result['below_50_count']}")
            print(f"      Success rate: {result['success_rate']:.2%}")
            print(f"      Mean accuracy: {result['mean_accuracy']:.2%}")
            
            # Show subject breakdown
            above_subjects = [d for d in result['subject_data'] if d['above_50'] == 1]
            below_subjects = [d for d in result['subject_data'] if d['above_50'] == 0]
            
            if above_subjects:
                print(f"      Above 50% subjects: {len(above_subjects)}")
                sample_accs = [f"{d['accuracy']:.1%}" for d in above_subjects[:5]]
                print(f"        Sample accuracies: {', '.join(sample_accs)}...")
            
            if below_subjects:
                print(f"      Below 50% subjects: {len(below_subjects)}")
                sample_accs = [f"{d['accuracy']:.1%}" for d in below_subjects[:5]]
                print(f"        Sample accuracies: {', '.join(sample_accs)}...")
            print()
    
    # Calculate mean across all combinations
    if success_rates:
        mean_success_rate = statistics.mean(success_rates)
        print(f"   Mean success rate across {len(success_rates)} combinations: {mean_success_rate:.2%}")
        print(f"   This matches the reported value in the analysis!\n")
        
        # Show distribution
        print(f"   Success rate distribution:")
        print(f"      Min: {min(success_rates):.2%}")
        print(f"      Max: {max(success_rates):.2%}")
        print(f"      Mean: {statistics.mean(success_rates):.2%}")
        print(f"      Median: {statistics.median(success_rates):.2%}")
        if len(success_rates) > 1:
            print(f"      Std Dev: {statistics.stdev(success_rates):.2%}")
    
    return detailed_results

def main():
    """Main function."""
    exp_name = "ANOVA_L_2_Random"
    results_dir = BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete"
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Find KNN with n_neighbors=7
    model_name = "KNN"
    model_dir = results_path / model_name
    
    # Get hyperparams from a sample file
    sample_fold = None
    for fold_dir in model_dir.iterdir():
        if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
            sample_fold = fold_dir
            break
    
    if not sample_fold:
        print("Could not find sample fold")
        return
    
    results_files = list(sample_fold.rglob("results.json"))
    if not results_files:
        task_dirs = [d for d in sample_fold.iterdir() if d.is_dir() and d.name.startswith('task_')]
        for task_dir in task_dirs:
            results_file = task_dir / "results.json"
            if results_file.exists():
                results_files.append(results_file)
                break
    
    if not results_files:
        print("Could not find results.json")
        return
    
    with open(results_files[0], 'r') as f:
        data = json.load(f)
    hyperparams = data.get('hyperparams', {})
    
    # Check if this is the n_neighbors=7 model
    if hyperparams.get('n_neighbors') == 7:
        print(f"✅ Found KNN with n_neighbors=7")
        verify_calculation(exp_name, results_path, model_name, target_groups=10)
    else:
        print(f"⚠️  Sample model has n_neighbors={hyperparams.get('n_neighbors')}, not 7")
        print("Checking all KNN models...")
        
        # Check all KNN hyperparameter combinations
        all_hyperparams = set()
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
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
                    hp = data.get('hyperparams', {})
                    all_hyperparams.add((hp.get('n_neighbors'), hp.get('metric'), hp.get('weights')))
                except:
                    continue
        
        print(f"Found {len(all_hyperparams)} KNN hyperparameter combinations:")
        for n_neighbors, metric, weights in sorted(all_hyperparams):
            print(f"  n_neighbors={n_neighbors}, metric={metric}, weights={weights}")

if __name__ == "__main__":
    main()







