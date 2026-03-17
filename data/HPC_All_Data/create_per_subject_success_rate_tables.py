#!/usr/bin/env python
"""
Create tables showing per-subject success rate and mean accuracy.

For each experiment, creates tables showing:
1. Success Rate (% of fold×model combinations where accuracy > 50%)
2. Mean Accuracy (average accuracy across all fold×model combinations)
"""

import pandas as pd
import json
from pathlib import Path
from collections import defaultdict
import statistics
import re

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

def load_per_subject_accuracies(exp_name, results_dir):
    """
    Load per-subject accuracies from parquet files.
    
    Returns: {subject_id: [list of accuracies from all fold×model combinations]}
    """
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {subject_id: [accuracies from all fold×model combinations]}
    subject_accuracies = defaultdict(list)
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            
            # Find task directories
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
                        
                except Exception as e:
                    continue
    
    return subject_accuracies

def calculate_success_rate(accuracies):
    """Calculate success rate: % of fold×model combinations where accuracy > 50%."""
    if not accuracies:
        return 0.0
    
    successful_folds = sum(1 for acc in accuracies if acc > 0.50)
    total_folds = len(accuracies)
    
    return (successful_folds / total_folds) * 100 if total_folds > 0 else 0.0

def calculate_mean_accuracy(accuracies):
    """Calculate mean accuracy: average of all fold×model accuracies."""
    if not accuracies:
        return 0.0
    
    return statistics.mean(accuracies) * 100

def create_tables(exp_name, subject_accuracies, output_file):
    """Create markdown tables for success rate and mean accuracy."""
    
    # Calculate metrics for each subject
    subject_data = []
    
    for subject_num in range(1, 66):
        subject_id = f"sub-{subject_num}"
        accuracies = subject_accuracies.get(subject_id, [])
        
        if accuracies:
            success_rate = calculate_success_rate(accuracies)
            mean_acc = calculate_mean_accuracy(accuracies)
            n_observations = len(accuracies)
        else:
            success_rate = None
            mean_acc = None
            n_observations = 0
        
        subject_data.append({
            'Subject': subject_id,
            'Success_Rate_%': success_rate,
            'Mean_Accuracy_%': mean_acc,
            'N_Observations': n_observations
        })
    
    # Create markdown content
    report = []
    report.append(f"# Per-Subject Success Rate and Mean Accuracy: {exp_name}")
    report.append("=" * 80)
    report.append("")
    report.append("## Table 1: Per-Subject Classification Success Rate")
    report.append("")
    report.append("**Definition**: Percentage of fold×model combinations where accuracy > 50%")
    report.append("")
    report.append("| Subject | Success Rate (%) | N Observations |")
    report.append("|---------|------------------|----------------|")
    
    # Sort by success rate (descending), then by subject number
    sorted_data = sorted(subject_data, key=lambda x: (x['Success_Rate_%'] if x['Success_Rate_%'] is not None else -1, int(x['Subject'].split('-')[1])), reverse=True)
    
    for row in sorted_data:
        if row['Success_Rate_%'] is not None:
            report.append(f"| {row['Subject']} | {row['Success_Rate_%']:.2f}% | {row['N_Observations']} |")
        else:
            report.append(f"| {row['Subject']} | N/A | 0 |")
    
    report.append("")
    report.append("## Table 2: Per-Subject Mean Accuracy")
    report.append("")
    report.append("**Definition**: Average accuracy across all fold×model combinations")
    report.append("")
    report.append("| Subject | Mean Accuracy (%) | N Observations |")
    report.append("|---------|-------------------|----------------|")
    
    # Sort by mean accuracy (descending), then by subject number
    sorted_data_mean = sorted(subject_data, key=lambda x: (x['Mean_Accuracy_%'] if x['Mean_Accuracy_%'] is not None else -1, int(x['Subject'].split('-')[1])), reverse=True)
    
    for row in sorted_data_mean:
        if row['Mean_Accuracy_%'] is not None:
            report.append(f"| {row['Subject']} | {row['Mean_Accuracy_%']:.2f}% | {row['N_Observations']} |")
        else:
            report.append(f"| {row['Subject']} | N/A | 0 |")
    
    report.append("")
    report.append("## Summary Statistics")
    report.append("")
    
    # Calculate summary stats
    subjects_with_data = [s for s in subject_data if s['Success_Rate_%'] is not None]
    
    if subjects_with_data:
        success_rates = [s['Success_Rate_%'] for s in subjects_with_data]
        mean_accs = [s['Mean_Accuracy_%'] for s in subjects_with_data]
        n_obs = [s['N_Observations'] for s in subjects_with_data]
        
        report.append(f"- **Subjects with test data**: {len(subjects_with_data)}")
        report.append(f"- **Subjects without test data**: {65 - len(subjects_with_data)}")
        report.append("")
        report.append("### Success Rate Statistics")
        report.append(f"- **Mean**: {statistics.mean(success_rates):.2f}%")
        report.append(f"- **Median**: {statistics.median(success_rates):.2f}%")
        report.append(f"- **Min**: {min(success_rates):.2f}%")
        report.append(f"- **Max**: {max(success_rates):.2f}%")
        report.append("")
        report.append("### Mean Accuracy Statistics")
        report.append(f"- **Mean**: {statistics.mean(mean_accs):.2f}%")
        report.append(f"- **Median**: {statistics.median(mean_accs):.2f}%")
        report.append(f"- **Min**: {min(mean_accs):.2f}%")
        report.append(f"- **Max**: {max(mean_accs):.2f}%")
        report.append("")
        report.append("### Observation Statistics")
        report.append(f"- **Mean N observations per subject**: {statistics.mean(n_obs):.1f}")
        report.append(f"- **Median N observations per subject**: {statistics.median(n_obs):.0f}")
        report.append(f"- **Min**: {min(n_obs)}")
        report.append(f"- **Max**: {max(n_obs)}")
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write("\n".join(report))
    
    print(f"   ✅ Saved: {output_file.name}")

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    all_reports = []
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        # Load per-subject accuracies from parquet files
        subject_accuracies = load_per_subject_accuracies(exp_name, results_dir)
        
        if not subject_accuracies:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found {len(subject_accuracies)} subjects with data")
        
        # Create individual table file
        output_file = output_dir / f"{exp_name}_per_subject_tables.md"
        create_tables(exp_name, subject_accuracies, output_file)
        
        # Also collect for combined report
        all_reports.append(f"## {exp_name}\n\nSee: `{exp_name}_per_subject_tables.md`\n")
    
    # Create combined report
    combined_report = []
    combined_report.append("# Per-Subject Success Rate and Mean Accuracy: All Experiments")
    combined_report.append("=" * 80)
    combined_report.append("")
    combined_report.append("This document provides links to individual experiment tables.")
    combined_report.append("")
    combined_report.append("\n".join(all_reports))
    
    output_file = output_dir / "per_subject_tables_all_experiments.md"
    with open(output_file, 'w') as f:
        f.write("\n".join(combined_report))
    
    print(f"\n✅ Saved combined report: {output_file.name}")

if __name__ == "__main__":
    main()


