#!/usr/bin/env python
"""
Investigate why ANOVA_L_6_Random shows identical variance and success rates across all models.
"""

import pandas as pd
from pathlib import Path
from collections import defaultdict
import json
import random
import statistics

BASE_DIR = Path(__file__).parent
EXPERIMENTS = {
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_6_complete",
}

CLASSIFICATION_THRESHOLD = 0.50

def load_all_subject_accuracies(results_dir, model_name):
    """Load all subject accuracies for a model across all folds."""
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

def calculate_subject_success_rates(subject_accuracies_cache, fold_names):
    """For each subject, calculate the percentage of folds where accuracy > 50%."""
    subject_fold_counts = defaultdict(lambda: {'total': 0, 'above_50': 0})
    
    for fold_name in fold_names:
        if fold_name in subject_accuracies_cache:
            for subject_id, accuracy in subject_accuracies_cache[fold_name].items():
                subject_fold_counts[subject_id]['total'] += 1
                if accuracy > CLASSIFICATION_THRESHOLD:
                    subject_fold_counts[subject_id]['above_50'] += 1
    
    subject_success_rates = {}
    for subject_id, counts in subject_fold_counts.items():
        if counts['total'] > 0:
            success_rate = counts['above_50'] / counts['total']
            subject_success_rates[subject_id] = success_rate
    
    return subject_success_rates

def main():
    exp_name = "ANOVA_L_6_Random"
    results_dir = EXPERIMENTS[exp_name]
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Get all fold names (should be same for all models)
    fold_names = set()
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        for fold_dir in model_dir.iterdir():
            if fold_dir.is_dir() and fold_dir.name.startswith('sub-'):
                fold_names.add(fold_dir.name)
    
    fold_names = sorted(list(fold_names))
    print(f"Total folds: {len(fold_names)}")
    print(f"First 3 folds: {fold_names[:3]}\n")
    
    models = ['KNN', 'MLP_(Neural_Network)', 'SVM', 'XGBoost']
    all_results = {}
    
    for model_name in models:
        print(f"=== {model_name} ===")
        
        # Load subject accuracies
        subject_accuracies_cache = load_all_subject_accuracies(results_path, model_name)
        print(f"  Folds with data: {len(subject_accuracies_cache)}")
        
        if not subject_accuracies_cache:
            continue
        
        # Check which subjects appear in which folds
        all_subjects = set()
        for fold_name, subject_accs in subject_accuracies_cache.items():
            all_subjects.update(subject_accs.keys())
        
        print(f"  Total unique subjects: {len(all_subjects)}")
        print(f"  Sample subjects: {sorted(list(all_subjects))[:5]}")
        
        # Calculate success rates using ALL folds
        subject_success_rates = calculate_subject_success_rates(subject_accuracies_cache, fold_names)
        
        if subject_success_rates:
            success_rate_values = list(subject_success_rates.values())
            variance = statistics.variance(success_rate_values) if len(success_rate_values) > 1 else 0.0
            mean_rate = statistics.mean(success_rate_values)
            
            print(f"  Mean Success Rate: {mean_rate:.4f} ({mean_rate:.2%})")
            print(f"  Variance: {variance:.6f}")
            print(f"  Number of subjects: {len(success_rate_values)}")
            print(f"  Min success rate: {min(success_rate_values):.4f}")
            print(f"  Max success rate: {max(success_rate_values):.4f}")
            print(f"  Sample success rates: {sorted(success_rate_values)[:5]}")
            
            all_results[model_name] = {
                'variance': variance,
                'mean_rate': mean_rate,
                'subject_success_rates': subject_success_rates,
                'num_subjects': len(success_rate_values)
            }
        print()
    
    # Compare results
    print("=== COMPARISON ===")
    if len(all_results) > 1:
        variances = [r['variance'] for r in all_results.values()]
        mean_rates = [r['mean_rate'] for r in all_results.values()]
        
        print(f"Variances: {variances}")
        print(f"Mean Rates: {mean_rates}")
        
        if len(set([round(v, 4) for v in variances])) == 1:
            print("\n⚠️  WARNING: All variances are identical (rounded to 4 decimals)!")
        
        if len(set([round(m, 4) for m in mean_rates])) == 1:
            print("⚠️  WARNING: All mean rates are identical (rounded to 4 decimals)!")
        
        # Check if subject success rates are identical
        if len(all_results) >= 2:
            model_names = list(all_results.keys())
            subj_rates_1 = all_results[model_names[0]]['subject_success_rates']
            subj_rates_2 = all_results[model_names[1]]['subject_success_rates']
            
            common_subjects = set(subj_rates_1.keys()) & set(subj_rates_2.keys())
            if common_subjects:
                differences = []
                for subj in common_subjects:
                    diff = abs(subj_rates_1[subj] - subj_rates_2[subj])
                    differences.append(diff)
                
                print(f"\nComparing {model_names[0]} vs {model_names[1]}:")
                print(f"  Common subjects: {len(common_subjects)}")
                print(f"  Mean difference in success rates: {statistics.mean(differences):.6f}")
                print(f"  Max difference: {max(differences):.6f}")
                print(f"  Subjects with identical rates: {sum(1 for d in differences if d < 0.0001)}")
                
                # Show some examples
                print(f"\n  Sample subject comparisons:")
                for subj in sorted(list(common_subjects))[:5]:
                    print(f"    {subj}: {model_names[0]}={subj_rates_1[subj]:.4f}, {model_names[1]}={subj_rates_2[subj]:.4f}, diff={abs(subj_rates_1[subj] - subj_rates_2[subj]):.6f}")

if __name__ == "__main__":
    main()







