#!/usr/bin/env python
"""
Create a per-subject summary showing:
- Subject ID (1-65)
- Median accuracy across all folds and model×HP combinations
- Number of times observed in a fold
- NA if subject not in data
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

def load_per_subject_accuracies(exp_name, results_dir):
    """Load all accuracies for each subject across all folds and model×HP."""
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {subject: [accuracies from all folds and model×HP]}
    subject_accuracies = defaultdict(list)
    
    # Iterate through all model directories
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
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
                        # Add this accuracy to all subjects in this fold
                        for subject_id in subject_ids:
                            subject_accuracies[subject_id].append(acc)
                except Exception as e:
                    continue
    
    return subject_accuracies

def create_per_subject_summary():
    """Create per-subject summary for all experiments."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    all_reports = []
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        # Load per-subject accuracies
        subject_accuracies = load_per_subject_accuracies(exp_name, results_dir)
        
        if not subject_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        # Create report
        report = []
        report.append(f"# Per-Subject Summary: {exp_name}")
        report.append("=" * 80)
        report.append("")
        report.append("For each subject (1-65), shows:")
        report.append("- **Median Accuracy**: Median accuracy across all folds and model×HP combinations")
        report.append("- **N Folds Observed**: Number of times the subject appeared in a test fold")
        report.append("- **NA**: Subject not observed in any test fold")
        report.append("")
        report.append("| Subject | Median Accuracy | N Folds Observed |")
        report.append("|---------|----------------|------------------|")
        
        # Process all subjects 1-65
        for subject_num in range(1, 66):
            subject_id = f"sub-{subject_num}"
            accuracies = subject_accuracies.get(subject_id, [])
            
            if accuracies:
                median_acc = statistics.median(accuracies)
                n_folds = len(accuracies)
                report.append(f"| {subject_id} | {median_acc:.2%} | {n_folds} |")
            else:
                report.append(f"| {subject_id} | N/A | 0 |")
        
        report.append("")
        report.append("## Summary Statistics")
        report.append("")
        
        # Calculate summary stats for subjects with data
        subjects_with_data = {k: v for k, v in subject_accuracies.items() if v}
        if subjects_with_data:
            all_medians = [statistics.median(accs) for accs in subjects_with_data.values()]
            all_n_folds = [len(accs) for accs in subjects_with_data.values()]
            
            report.append(f"- **Subjects with test data**: {len(subjects_with_data)}")
            report.append(f"- **Subjects without test data**: {65 - len(subjects_with_data)}")
            report.append(f"- **Median accuracy (across subjects)**: {statistics.median(all_medians):.2%}")
            report.append(f"- **Mean accuracy (across subjects)**: {statistics.mean(all_medians):.2%}")
            report.append(f"- **Min accuracy**: {min(all_medians):.2%}")
            report.append(f"- **Max accuracy**: {max(all_medians):.2%}")
            report.append(f"- **Mean N folds per subject**: {statistics.mean(all_n_folds):.1f}")
            report.append(f"- **Median N folds per subject**: {statistics.median(all_n_folds):.0f}")
            report.append(f"- **Min N folds**: {min(all_n_folds)}")
            report.append(f"- **Max N folds**: {max(all_n_folds)}")
        
        report_text = "\n".join(report)
        all_reports.append(report_text)
        
        # Save individual report
        output_file = output_dir / f"{exp_name}_per_subject_summary.md"
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"   ✅ Saved: {output_file.name}")
        
        # Also save as CSV
        csv_file = output_dir / f"{exp_name}_per_subject_summary.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject', 'Median_Accuracy', 'N_Folds_Observed'])
            for subject_num in range(1, 66):
                subject_id = f"sub-{subject_num}"
                accuracies = subject_accuracies.get(subject_id, [])
                if accuracies:
                    median_acc = statistics.median(accuracies)
                    n_folds = len(accuracies)
                    writer.writerow([subject_id, f"{median_acc:.4f}", n_folds])
                else:
                    writer.writerow([subject_id, "N/A", 0])
        print(f"   ✅ Saved: {csv_file.name}")
    
    # Create combined report
    combined_report = []
    combined_report.append("# Per-Subject Summary: All Experiments")
    combined_report.append("=" * 80)
    combined_report.append("")
    combined_report.append("\n\n".join(all_reports))
    
    output_file = output_dir / "per_subject_summary_all_experiments.md"
    with open(output_file, 'w') as f:
        f.write("\n".join(combined_report))
    print(f"\n✅ Saved combined report: {output_file.name}")

if __name__ == "__main__":
    create_per_subject_summary()

