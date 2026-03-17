#!/usr/bin/env python
"""
Create CSV showing median accuracy for each subject.
Shows how accuracy is calculated per subject.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
import statistics

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "ANOVA_L_6_Uniform": BASE_DIR / "grid_12_folds/ANOVA_L_6_C_Resource_Boosted",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
    "PCA_L_6_Uniform": BASE_DIR / "grid_12_folds/PCA_L_6_C-3",
}

def extract_subject_ids_from_fold(fold_name):
    """Extract subject IDs from fold name."""
    import re
    return re.findall(r'sub-\d+', fold_name)

def load_subject_accuracies_detailed(exp_name, results_dir):
    """Load accuracies with detailed breakdown."""
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {subject: {fold: {model: accuracy}}}
    subject_fold_model_acc = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    # Also keep simple list for current calculation
    subject_all_accuracies = defaultdict(list)
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        model_name = model_dir.name
        
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            subject_ids = extract_subject_ids_from_fold(fold_name)
            
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
                        for subject_id in subject_ids:
                            subject_fold_model_acc[subject_id][fold_name][model_name] = acc
                            subject_all_accuracies[subject_id].append(acc)
                except:
                    continue
    
    return subject_fold_model_acc, subject_all_accuracies

def create_csv():
    """Create CSV for all experiments."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        subject_fold_model_acc, subject_all_accuracies = load_subject_accuracies_detailed(exp_name, results_dir)
        
        if not subject_all_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        # Create CSV
        csv_file = output_dir / f"{exp_name}_subject_median_accuracy.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Subject', 
                'Median_Accuracy_Current_Method', 
                'N_Folds', 
                'N_Model_Observations',
                'Calculation_Method',
                'Note'
            ])
            
            for subject_num in range(1, 66):
                subject_id = f"sub-{subject_num}"
                all_accs = subject_all_accuracies.get(subject_id, [])
                
                if all_accs:
                    median_acc = statistics.median(all_accs)
                    n_folds = len(subject_fold_model_acc.get(subject_id, {}))
                    n_obs = len(all_accs)
                    
                    # Calculate what the method actually does
                    method = f"Median of {n_obs} accuracies (across {n_folds} folds × multiple models)"
                    note = f"Mixed: {n_obs} accuracies from {n_folds} fold(s) and multiple models"
                    
                    writer.writerow([
                        subject_id,
                        f"{median_acc:.4f}",
                        n_folds,
                        n_obs,
                        method,
                        note
                    ])
                else:
                    writer.writerow([subject_id, "N/A", 0, 0, "No data", "Subject not in test folds"])
        
        print(f"   ✅ Saved: {csv_file.name}")
        
        # Also create detailed breakdown CSV
        detailed_csv = output_dir / f"{exp_name}_subject_accuracy_detailed.csv"
        with open(detailed_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject', 'Fold', 'Model', 'Accuracy'])
            
            for subject_num in range(1, 66):
                subject_id = f"sub-{subject_num}"
                if subject_id in subject_fold_model_acc:
                    for fold_name, models in subject_fold_model_acc[subject_id].items():
                        for model_name, acc in models.items():
                            writer.writerow([subject_id, fold_name, model_name, f"{acc:.4f}"])
        
        print(f"   ✅ Saved: {detailed_csv.name}")

if __name__ == "__main__":
    create_csv()


