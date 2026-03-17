#!/usr/bin/env python
"""
Calculate per-subject accuracy from test_predictions.parquet files.

For each subject, calculates accuracy as:
  accuracy = (label == prediction).sum() / len(subject_data)

Then aggregates across folds and model×HP combinations.
"""

import pandas as pd
import json
import csv
from pathlib import Path
from collections import defaultdict
import statistics
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

def extract_subject_ids_from_fold(fold_name):
    """Extract subject IDs from fold name like 'sub-2_sub-39'."""
    return re.findall(r'sub-(\d+)', fold_name)

def calculate_per_subject_accuracy_from_parquet(exp_name, results_dir):
    """
    Calculate per-subject accuracy from test_predictions.parquet files.
    
    Returns:
        subject_accuracies: {subject_id: [accuracies from all folds and model×HP]}
        subject_fold_details: {subject_id: {fold_name: {model_name: accuracy}}}
    """
    if not results_dir.exists():
        return {}, {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {subject_id: [accuracies from all folds and model×HP]}
    subject_accuracies = defaultdict(list)
    # Structure: {subject_id: {fold_name: {model_name: accuracy}}}
    subject_fold_details = defaultdict(lambda: defaultdict(dict))
    # Track unique folds per subject
    subject_unique_folds = defaultdict(set)
    
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
            
            # Find all task directories in this fold
            task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
            
            for task_dir in task_dirs:
                test_parquet = task_dir / "test_predictions.parquet"
                
                if not test_parquet.exists():
                    continue
                
                try:
                    # Read test predictions
                    test_df = pd.read_parquet(test_parquet)
                    
                    # Calculate per-subject accuracy
                    for subject_id_num in test_df['SubjectID'].unique():
                        subject_id = f"sub-{int(subject_id_num)}"
                        
                        # Filter data for this subject
                        subject_data = test_df[test_df['SubjectID'] == subject_id_num]
                        
                        # Calculate accuracy: (label == prediction).sum() / len(subject_data)
                        correct = (subject_data['label'] == subject_data['prediction']).sum()
                        total = len(subject_data)
                        accuracy = correct / total if total > 0 else 0.0
                        
                        # Store accuracy
                        subject_accuracies[subject_id].append(accuracy)
                        subject_fold_details[subject_id][fold_name][model_name] = accuracy
                        subject_unique_folds[subject_id].add(fold_name)
                        
                except Exception as e:
                    print(f"   ⚠️  Error processing {task_dir}: {e}")
                    continue
    
    return subject_accuracies, subject_fold_details, subject_unique_folds

def create_per_subject_summary():
    """Create per-subject summary for all experiments."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    all_reports = []
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        # Calculate per-subject accuracies from parquet files
        subject_accuracies, subject_fold_details, subject_unique_folds = calculate_per_subject_accuracy_from_parquet(exp_name, results_dir)
        
        if not subject_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found {len(subject_accuracies)} subjects with test data")
        
        # Create report
        report = []
        report.append(f"# Per-Subject Summary: {exp_name}")
        report.append("=" * 80)
        report.append("")
        report.append("**Calculation Method**: Per-subject accuracy calculated from `test_predictions.parquet` files.")
        report.append("For each subject in each fold×model combination:")
        report.append("- Filter predictions where `SubjectID == subject_id`")
        report.append("- Calculate: `accuracy = (label == prediction).sum() / len(subject_data)`")
        report.append("- Then aggregate across folds and model×HP combinations")
        report.append("")
        report.append("For each subject (1-65), shows:")
        report.append("- **Median Accuracy**: Median accuracy across all folds and model×HP combinations")
        report.append("- **Mean Accuracy**: Mean accuracy across all folds and model×HP combinations")
        report.append("- **N Folds Observed**: Number of unique folds where subject appeared in test set")
        report.append("- **N Observations**: Total number of fold×model combinations")
        report.append("- **NA**: Subject not observed in any test fold")
        report.append("")
        report.append("| Subject | Median Accuracy | Mean Accuracy | N Folds | N Observations |")
        report.append("|---------|----------------|---------------|---------|----------------|")
        
        # Process all subjects 1-65
        for subject_num in range(1, 66):
            subject_id = f"sub-{subject_num}"
            accuracies = subject_accuracies.get(subject_id, [])
            unique_folds = subject_unique_folds.get(subject_id, set())
            
            if accuracies:
                median_acc = statistics.median(accuracies)
                mean_acc = statistics.mean(accuracies)
                n_folds = len(unique_folds)
                n_obs = len(accuracies)
                report.append(f"| {subject_id} | {median_acc:.2%} | {mean_acc:.2%} | {n_folds} | {n_obs} |")
            else:
                report.append(f"| {subject_id} | N/A | N/A | 0 | 0 |")
        
        report.append("")
        report.append("## Summary Statistics")
        report.append("")
        
        # Calculate summary stats for subjects with data
        subjects_with_data = {k: v for k, v in subject_accuracies.items() if v}
        if subjects_with_data:
            all_medians = [statistics.median(accs) for accs in subjects_with_data.values()]
            all_means = [statistics.mean(accs) for accs in subjects_with_data.values()]
            all_n_folds = [len(subject_unique_folds.get(k, set())) for k in subjects_with_data.keys()]
            all_n_obs = [len(accs) for accs in subjects_with_data.values()]
            
            report.append(f"- **Subjects with test data**: {len(subjects_with_data)}")
            report.append(f"- **Subjects without test data**: {65 - len(subjects_with_data)}")
            report.append(f"- **Median accuracy (across subjects, median)**: {statistics.median(all_medians):.2%}")
            report.append(f"- **Mean accuracy (across subjects, mean)**: {statistics.mean(all_means):.2%}")
            report.append(f"- **Min accuracy**: {min(all_medians):.2%}")
            report.append(f"- **Max accuracy**: {max(all_medians):.2%}")
            report.append(f"- **Mean N folds per subject**: {statistics.mean(all_n_folds):.1f}")
            report.append(f"- **Median N folds per subject**: {statistics.median(all_n_folds):.0f}")
            report.append(f"- **Mean N observations per subject**: {statistics.mean(all_n_obs):.1f}")
            report.append(f"- **Median N observations per subject**: {statistics.median(all_n_obs):.0f}")
        
        report_text = "\n".join(report)
        all_reports.append(report_text)
        
        # Save individual report
        output_file = output_dir / f"{exp_name}_per_subject_summary.md"
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"   ✅ Saved: {output_file.name}")
        
        # Save as CSV
        csv_file = output_dir / f"{exp_name}_per_subject_summary.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject', 'Median_Accuracy', 'Mean_Accuracy', 'N_Folds', 'N_Observations'])
            for subject_num in range(1, 66):
                subject_id = f"sub-{subject_num}"
                accuracies = subject_accuracies.get(subject_id, [])
                unique_folds = subject_unique_folds.get(subject_id, set())
                if accuracies:
                    median_acc = statistics.median(accuracies)
                    mean_acc = statistics.mean(accuracies)
                    n_folds = len(unique_folds)
                    n_obs = len(accuracies)
                    writer.writerow([subject_id, f"{median_acc:.4f}", f"{mean_acc:.4f}", n_folds, n_obs])
                else:
                    writer.writerow([subject_id, "N/A", "N/A", 0, 0])
        print(f"   ✅ Saved: {csv_file.name}")
        
        # Save detailed breakdown (subject × fold × model)
        detailed_csv = output_dir / f"{exp_name}_per_subject_detailed.csv"
        with open(detailed_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject', 'Fold', 'Model', 'Accuracy'])
            for subject_id in sorted(subject_fold_details.keys(), key=lambda x: int(x.split('-')[1])):
                for fold_name in sorted(subject_fold_details[subject_id].keys()):
                    for model_name in sorted(subject_fold_details[subject_id][fold_name].keys()):
                        acc = subject_fold_details[subject_id][fold_name][model_name]
                        writer.writerow([subject_id, fold_name, model_name, f"{acc:.4f}"])
        print(f"   ✅ Saved: {detailed_csv.name}")
    
    # Create combined report
    combined_report = []
    combined_report.append("# Per-Subject Summary: All Experiments")
    combined_report.append("=" * 80)
    combined_report.append("")
    combined_report.append("**Note**: Accuracies calculated from `test_predictions.parquet` files.")
    combined_report.append("")
    combined_report.append("\n\n".join(all_reports))
    
    output_file = output_dir / "per_subject_summary_all_experiments.md"
    with open(output_file, 'w') as f:
        f.write("\n".join(combined_report))
    print(f"\n✅ Saved combined report: {output_file.name}")

if __name__ == "__main__":
    create_per_subject_summary()


