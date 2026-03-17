#!/usr/bin/env python
"""
Analyze per-subject classification data and create visualizations.

For each experiment, creates:
1. Summary statistics
2. Distribution plots
3. Per-subject classification success rates
4. Model×HP comparison plots
"""

import csv
import json
from pathlib import Path
from collections import defaultdict
import statistics

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not available")

BASE_DIR = Path(__file__).parent
CSV_DIR = BASE_DIR / "per_subject_classification_csvs"
OUTPUT_DIR = BASE_DIR / "per_subject_classification_analysis"

def load_csv_data(csv_file):
    """Load data from CSV file."""
    data = []
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Handle N/A values
            def safe_float(val):
                try:
                    return float(val) if val and val != 'N/A' else None
                except (ValueError, TypeError):
                    return None
            
            def safe_int(val):
                try:
                    return int(val) if val and val != 'N/A' else 0
                except (ValueError, TypeError):
                    return 0
            
            row['N_Folds'] = safe_int(row['N_Folds'])
            row['Mean_Accuracy'] = safe_float(row['Mean_Accuracy'])
            row['Median_Accuracy'] = safe_float(row['Median_Accuracy'])
            row['Min_Accuracy'] = safe_float(row['Min_Accuracy'])
            row['Max_Accuracy'] = safe_float(row['Max_Accuracy'])
            row['Std_Dev'] = safe_float(row['Std_Dev'])
            row['N_Correctly_Classified'] = safe_int(row['N_Correctly_Classified'])
            row['Pct_Correctly_Classified'] = safe_float(row['Pct_Correctly_Classified'])
            
            # Parse fold accuracies (skip N/A)
            if row['Fold_Accuracies'] and row['Fold_Accuracies'] != 'N/A':
                row['Fold_Accuracies_List'] = [float(x) for x in row['Fold_Accuracies'].split(';') if x]
            else:
                row['Fold_Accuracies_List'] = []
            
            # Only include rows with actual data (N_Folds > 0)
            if row['N_Folds'] > 0:
                data.append(row)
    return data

def create_summary_statistics(data, exp_name):
    """Create summary statistics report."""
    report = []
    report.append(f"# Analysis: {exp_name}")
    report.append("=" * 80)
    report.append("")
    
    # Overall statistics
    all_accuracies = []
    all_pct_correct = []
    for row in data:
        all_accuracies.extend(row['Fold_Accuracies_List'])
        if row['Pct_Correctly_Classified'] is not None:
            all_pct_correct.append(row['Pct_Correctly_Classified'])
    
    report.append("## Overall Statistics")
    report.append("")
    report.append(f"- Total subjects with test data: {len(set(r['Subject'] for r in data))}")
    report.append(f"- Total model×HP combinations: {len(set(r['Model×Hyperparameter'] for r in data))}")
    report.append(f"- Total fold observations: {len(all_accuracies)}")
    report.append("")
    report.append("### Accuracy Distribution")
    if all_accuracies:
        report.append(f"- Mean accuracy: {statistics.mean(all_accuracies):.2%}")
        report.append(f"- Median accuracy: {statistics.median(all_accuracies):.2%}")
        report.append(f"- Min accuracy: {min(all_accuracies):.2%}")
        report.append(f"- Max accuracy: {max(all_accuracies):.2%}")
        report.append(f"- Std Dev: {statistics.stdev(all_accuracies):.2%}")
    report.append("")
    report.append("### Classification Success Rate")
    if all_pct_correct:
        report.append(f"- Mean % correctly classified: {statistics.mean(all_pct_correct):.2f}%")
        report.append(f"- Median % correctly classified: {statistics.median(all_pct_correct):.2f}%")
        report.append(f"- Subjects with 100% correct: {sum(1 for p in all_pct_correct if p == 100)}")
        report.append(f"- Subjects with 0% correct: {sum(1 for p in all_pct_correct if p == 0)}")
    report.append("")
    
    # Per model×HP statistics
    report.append("## Per Model×Hyperparameter Statistics")
    report.append("")
    model_hp_stats = defaultdict(list)
    for row in data:
        model_hp_stats[row['Model×Hyperparameter']].extend(row['Fold_Accuracies_List'])
    
    report.append("| Model×Hyperparameter | N Subjects | Mean Acc | Median Acc | Min | Max | Std Dev |")
    report.append("|---------------------|------------|----------|------------|-----|-----|---------|")
    
    for model_hp, accs in sorted(model_hp_stats.items()):
        subjects = set(r['Subject'] for r in data if r['Model×Hyperparameter'] == model_hp)
        if accs:
            report.append(f"| {model_hp[:50]} | {len(subjects)} | {statistics.mean(accs):.2%} | "
                         f"{statistics.median(accs):.2%} | {min(accs):.2%} | {max(accs):.2%} | "
                         f"{statistics.stdev(accs):.2%} |")
    report.append("")
    
    return "\n".join(report)

def create_accuracy_distribution_plot(data, exp_name, output_dir):
    """Create histogram of accuracy distribution."""
    if not HAS_MATPLOTLIB:
        return False
    
    all_accuracies = []
    for row in data:
        all_accuracies.extend(row['Fold_Accuracies_List'])
    
    if not all_accuracies:
        return False
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create histogram
    n, bins, patches = ax.hist(all_accuracies, bins=50, edgecolor='black', alpha=0.7)
    
    # Color bars by accuracy threshold
    for i, (patch, bin_val) in enumerate(zip(patches, bins[:-1])):
        if bin_val >= 0.5:
            patch.set_facecolor('#90EE90')  # Light green for >50%
        else:
            patch.set_facecolor('#FFB6C1')  # Light pink for <50%
    
    # Add vertical line at 50%
    ax.axvline(x=0.5, color='red', linestyle='--', linewidth=2, label='50% Threshold (Correct Classification)')
    
    ax.set_xlabel('Accuracy', fontsize=13, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax.set_title(f'{exp_name}\nDistribution of Per-Subject Accuracies Across All Folds',
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(fontsize=11)
    
    # Add statistics text
    mean_acc = statistics.mean(all_accuracies)
    median_acc = statistics.median(all_accuracies)
    stats_text = f'Mean: {mean_acc:.2%}\nMedian: {median_acc:.2%}\nN: {len(all_accuracies)}'
    ax.text(0.98, 0.98, stats_text, transform=ax.transAxes,
           fontsize=11, verticalalignment='top', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, edgecolor='black', linewidth=2))
    
    plt.tight_layout()
    output_file = output_dir / f'{exp_name}_accuracy_distribution.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def create_per_subject_success_rate_plot(data, exp_name, output_dir):
    """Create bar plot showing per-subject classification success rate."""
    if not HAS_MATPLOTLIB:
        return False
    
    # Aggregate by subject
    subject_stats = defaultdict(lambda: {'total_folds': 0, 'correct_folds': 0, 'accuracies': []})
    for row in data:
        subject = row['Subject']
        subject_stats[subject]['total_folds'] += row['N_Folds']
        subject_stats[subject]['correct_folds'] += row['N_Correctly_Classified']
        subject_stats[subject]['accuracies'].extend(row['Fold_Accuracies_List'])
    
    # Calculate success rates
    subjects = []
    success_rates = []
    mean_accs = []
    
    for subject in sorted(subject_stats.keys()):
        stats = subject_stats[subject]
        if stats['total_folds'] > 0:
            success_rate = (stats['correct_folds'] / stats['total_folds']) * 100
            mean_acc = statistics.mean(stats['accuracies']) if stats['accuracies'] else 0
            subjects.append(subject)
            success_rates.append(success_rate)
            mean_accs.append(mean_acc)
    
    # Sort by success rate
    sorted_data = sorted(zip(subjects, success_rates, mean_accs), key=lambda x: x[1], reverse=True)
    subjects, success_rates, mean_accs = zip(*sorted_data) if sorted_data else ([], [], [])
    
    if not subjects:
        return False
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 12))
    
    # Plot 1: Success rate
    colors = ['#90EE90' if sr == 100 else '#FFB6C1' if sr == 0 else '#FFD700' for sr in success_rates]
    bars1 = ax1.bar(range(len(subjects)), success_rates, color=colors, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('% Correctly Classified', fontsize=13, fontweight='bold')
    ax1.set_title(f'{exp_name}\nPer-Subject Classification Success Rate\n(% of folds where accuracy > 50%)',
                 fontsize=15, fontweight='bold', pad=20)
    ax1.set_xticks(range(len(subjects)))
    ax1.set_xticklabels(subjects, rotation=45, ha='right', fontsize=9)
    ax1.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.legend(fontsize=11)
    ax1.set_ylim(0, 105)
    
    # Plot 2: Mean accuracy
    bars2 = ax2.bar(range(len(subjects)), [m*100 for m in mean_accs], color=colors, edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Subject (sorted by success rate)', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Mean Accuracy (%)', fontsize=13, fontweight='bold')
    ax2.set_title(f'{exp_name}\nPer-Subject Mean Accuracy Across All Folds',
                 fontsize=15, fontweight='bold', pad=20)
    ax2.set_xticks(range(len(subjects)))
    ax2.set_xticklabels(subjects, rotation=45, ha='right', fontsize=9)
    ax2.axhline(y=50, color='red', linestyle='--', linewidth=2, label='50% Threshold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend(fontsize=11)
    ax2.set_ylim(0, 105)
    
    # Add legend for colors
    legend_elements = [
        mpatches.Patch(facecolor='#90EE90', alpha=0.7, edgecolor='black', label='100% Success'),
        mpatches.Patch(facecolor='#FFD700', alpha=0.7, edgecolor='black', label='Partial Success'),
        mpatches.Patch(facecolor='#FFB6C1', alpha=0.7, edgecolor='black', label='0% Success')
    ]
    ax1.legend(handles=legend_elements + [plt.Line2D([0], [0], color='red', linestyle='--', label='50% Threshold')],
              loc='upper right', fontsize=10)
    
    plt.tight_layout()
    output_file = output_dir / f'{exp_name}_per_subject_success_rate.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def create_model_hp_comparison_plot(data, exp_name, output_dir):
    """Create box plot comparing different model×HP combinations."""
    if not HAS_MATPLOTLIB:
        return False
    
    # Group by model×HP
    model_hp_data = defaultdict(list)
    for row in data:
        model_hp_data[row['Model×Hyperparameter']].extend(row['Fold_Accuracies_List'])
    
    if not model_hp_data:
        return False
    
    # Sort by mean accuracy
    sorted_model_hps = sorted(model_hp_data.items(), 
                             key=lambda x: statistics.mean(x[1]) if x[1] else 0, 
                             reverse=True)
    
    model_hps = [mh[:40] for mh, _ in sorted_model_hps]  # Truncate long names
    accuracies_list = [accs for _, accs in sorted_model_hps]
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    positions = range(1, len(accuracies_list) + 1)
    bp = ax.boxplot(accuracies_list, positions=positions, tick_labels=model_hps, vert=True,
                    patch_artist=True, showmeans=False, meanline=False, showfliers=True,
                    widths=0.6)
    
    # Color boxes
    for patch in bp['boxes']:
        patch.set_facecolor('#87CEEB')
        patch.set_alpha(0.7)
        patch.set_edgecolor('black')
        patch.set_linewidth(1)
    
    # Add 50% threshold line
    ax.axhline(y=0.5, color='red', linestyle='--', linewidth=2, label='50% Threshold (Correct Classification)')
    
    ax.set_xlabel('Model×Hyperparameter Combination', fontsize=13, fontweight='bold')
    ax.set_ylabel('Accuracy', fontsize=13, fontweight='bold')
    ax.set_title(f'{exp_name}\nAccuracy Distribution by Model×Hyperparameter Combination',
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(fontsize=10)
    ax.legend(fontsize=11)
    ax.set_ylim(0, 1.05)
    
    plt.tight_layout()
    output_file = output_dir / f'{exp_name}_model_hp_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    if not HAS_MATPLOTLIB:
        print("=" * 80)
        print("ERROR: matplotlib is required for visualization")
        print("=" * 80)
        return
    
    print("=" * 80)
    print("ANALYZING PER-SUBJECT CLASSIFICATION DATA")
    print("=" * 80)
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    csv_files = list(CSV_DIR.glob("*_per_subject_classification.csv"))
    
    if not csv_files:
        print(f"❌ No CSV files found in {CSV_DIR}")
        return
    
    all_reports = []
    
    for csv_file in sorted(csv_files):
        exp_name = csv_file.stem.replace('_per_subject_classification', '')
        print(f"\n📊 Analyzing {exp_name}...")
        
        # Load data
        data = load_csv_data(csv_file)
        
        if not data:
            print(f"   ⚠️  No data found")
            continue
        
        # Create summary statistics
        report = create_summary_statistics(data, exp_name)
        all_reports.append(report)
        
        # Create visualizations
        create_accuracy_distribution_plot(data, exp_name, OUTPUT_DIR)
        create_per_subject_success_rate_plot(data, exp_name, OUTPUT_DIR)
        create_model_hp_comparison_plot(data, exp_name, OUTPUT_DIR)
    
    # Save combined report
    report_file = OUTPUT_DIR / "analysis_summary.md"
    with open(report_file, 'w') as f:
        f.write("\n\n".join(all_reports))
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\n✅ Generated analysis for {len(csv_files)} experiments")
    print(f"\nAll outputs saved to: {OUTPUT_DIR}")
    print(f"Summary report: {report_file.name}")

if __name__ == '__main__':
    main()

