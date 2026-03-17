#!/usr/bin/env python
"""
Create CSV showing per-subject accuracy for each model×hyperparameter combination.

For each model×HP, shows:
- Subject ID
- Accuracy for each fold where subject appears in test set
- Whether subject is correctly classified (>50% accuracy) in each fold
- Summary statistics (mean, median, min, max, % correctly classified)
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
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

def extract_subject_ids_from_fold(fold_name):
    """Extract subject IDs from fold name like 'sub-3_sub-60'."""
    import re
    return re.findall(r'sub-\d+', fold_name)

def extract_hyperparams(results_file):
    """Extract hyperparameters from results.json file."""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        return data.get('hyperparams', {})
    except:
        return {}

def format_model_hp_label(model_name, hyperparams):
    """Format model×hyperparameter label for CSV."""
    if hyperparams:
        sorted_keys = sorted(hyperparams.keys())
        param_str = ", ".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
        return f"{model_name} ({param_str})"
    else:
        return f"{model_name} (default)"

def load_per_subject_classification_data(exp_name, results_dir):
    """Load per-subject accuracy data for each model×HP combination."""
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {model_hp_key: {subject: [(fold_id, accuracy, correctly_classified)]}}
    model_hp_subject_data = defaultdict(lambda: defaultdict(list))
    
    # Iterate through all model directories
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        model_name = model_dir.name
        
        # Iterate through fold directories
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            subject_ids = extract_subject_ids_from_fold(fold_name)
            
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
                        correctly_classified = acc > 0.5
                        hyperparams = data.get('hyperparams', {})
                        
                        # Create model×HP key
                        if hyperparams:
                            sorted_keys = sorted(hyperparams.keys())
                            param_str = "_".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
                        else:
                            param_str = "default"
                        
                        model_hp_key = f"{model_name}__{param_str}"
                        
                        # Store for each subject in test set
                        for subject_id in subject_ids:
                            model_hp_subject_data[model_hp_key][subject_id].append({
                                'fold_id': fold_name,
                                'accuracy': acc,
                                'correctly_classified': correctly_classified
                            })
                except Exception as e:
                    pass
    
    return model_hp_subject_data

def get_all_subjects_in_dataset(exp_name):
    """Get all expected subjects (sub-1 to sub-65) for the dataset."""
    # Based on the dataset, we expect subjects sub-1 through sub-65
    # Check ANOVA_L_6_Random to see the full set
    if 'L_6' in exp_name:
        # For L_6, we can check what subjects actually exist
        return set([f'sub-{i}' for i in range(1, 66)])
    else:
        # For L_2, we still expect 65 subjects total
        return set([f'sub-{i}' for i in range(1, 66)])

def create_per_subject_classification_csv(exp_name, model_hp_subject_data, output_dir):
    """Create CSV file for per-subject classification data."""
    output_file = output_dir / f"{exp_name}_per_subject_classification.csv"
    
    # Get all expected subjects
    all_expected_subjects = get_all_subjects_in_dataset(exp_name)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'Experiment',
            'Model×Hyperparameter',
            'Subject',
            'N_Folds',
            'Mean_Accuracy',
            'Median_Accuracy',
            'Min_Accuracy',
            'Max_Accuracy',
            'Std_Dev',
            'N_Correctly_Classified',
            'Pct_Correctly_Classified',
            'Fold_Accuracies',
            'Fold_IDs'
        ])
        
        # Write data for each model×HP combination
        for model_hp_key, subject_data in sorted(model_hp_subject_data.items()):
            # Parse model×HP key
            parts = model_hp_key.split('__', 1)
            model_name = parts[0]
            if len(parts) > 1:
                # Parse hyperparams
                hyperparams = {}
                for param in parts[1].split('_'):
                    if '=' in param:
                        k, v = param.split('=', 1)
                        try:
                            # Try to convert to appropriate type
                            if v.startswith('[') and v.endswith(']'):
                                # List
                                v = eval(v)  # Safe for our use case
                            elif '.' in v:
                                v = float(v)
                            else:
                                v = int(v)
                        except:
                            pass
                        hyperparams[k] = v
            else:
                hyperparams = {}
            
            model_hp_label = format_model_hp_label(model_name, hyperparams)
            
            # Get all subjects that have data for this model×HP
            subjects_with_data = set(subject_data.keys())
            
            # Write data for each subject (including those with no test data)
            for subject_id in sorted(all_expected_subjects):
                if subject_id in subject_data:
                    # Subject has test data
                    fold_data = subject_data[subject_id]
                    
                    accuracies = [d['accuracy'] for d in fold_data]
                    correctly_classified = [d['correctly_classified'] for d in fold_data]
                    fold_ids = [d['fold_id'] for d in fold_data]
                    
                    n_folds = len(accuracies)
                    mean_acc = statistics.mean(accuracies) if accuracies else 0
                    median_acc = statistics.median(accuracies) if accuracies else 0
                    min_acc = min(accuracies) if accuracies else 0
                    max_acc = max(accuracies) if accuracies else 0
                    std_acc = statistics.stdev(accuracies) if len(accuracies) > 1 else 0
                    n_correct = sum(correctly_classified)
                    pct_correct = (n_correct / n_folds * 100) if n_folds > 0 else 0
                    
                    # Format accuracies and fold IDs as semicolon-separated
                    acc_str = ";".join([f"{acc:.4f}" for acc in accuracies])
                    fold_ids_str = ";".join(fold_ids)
                else:
                    # Subject never appeared in test set
                    n_folds = 0
                    mean_acc = 0
                    median_acc = 0
                    min_acc = 0
                    max_acc = 0
                    std_acc = 0
                    n_correct = 0
                    pct_correct = 0
                    acc_str = "N/A"
                    fold_ids_str = "No test data"
                
                writer.writerow([
                    exp_name,
                    model_hp_label,
                    subject_id,
                    n_folds,
                    f"{mean_acc:.4f}" if n_folds > 0 else "N/A",
                    f"{median_acc:.4f}" if n_folds > 0 else "N/A",
                    f"{min_acc:.4f}" if n_folds > 0 else "N/A",
                    f"{max_acc:.4f}" if n_folds > 0 else "N/A",
                    f"{std_acc:.4f}" if n_folds > 0 else "N/A",
                    n_correct,
                    f"{pct_correct:.2f}" if n_folds > 0 else "N/A",
                    acc_str,
                    fold_ids_str
                ])
    
    print(f"   ✅ Saved: {output_file.name}")
    return output_file

def main():
    """Main function."""
    print("=" * 80)
    print("CREATING PER-SUBJECT CLASSIFICATION CSV FILES")
    print("=" * 80)
    
    output_dir = BASE_DIR / "per_subject_classification_csvs"
    output_dir.mkdir(exist_ok=True)
    
    success_count = 0
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        model_hp_subject_data = load_per_subject_classification_data(exp_name, results_dir)
        
        if model_hp_subject_data:
            create_per_subject_classification_csv(exp_name, model_hp_subject_data, output_dir)
            success_count += 1
            print(f"   Found {len(model_hp_subject_data)} model×HP combinations")
        else:
            print(f"   ⚠️  No data found")
    
    print("\n" + "=" * 80)
    print("CSV GENERATION COMPLETE")
    print("=" * 80)
    print(f"\n✅ Generated {success_count} CSV files")
    print(f"\nAll CSVs saved to: {output_dir}")

if __name__ == '__main__':
    main()

