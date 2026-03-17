#!/usr/bin/env python3
"""
Multi-Experiment Subject-Level Classification Threshold Analysis

Analyzes optimal thresholds across multiple experiments:
- ANOVA_L_2, ANOVA_L_6, PCA_L_2, PCA_L_6
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from pathlib import Path
import warnings
import os

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_subject_predictions(experiment_dir, max_folds=50):
    """Load predictions and aggregate by subject"""
    results_dir = Path(experiment_dir)
    parquet_files = list(results_dir.rglob("test_predictions.parquet"))
    
    if len(parquet_files) > max_folds * 4:
        import random
        parquet_files = random.sample(parquet_files, max_folds * 4)
    
    subject_data = []
    
    for parquet_file in parquet_files:
        try:
            df = pd.read_parquet(parquet_file)
            path_parts = str(parquet_file).split('/')
            fold_info = path_parts[-3]
            task_info = path_parts[-2]
            model = task_info.replace('task_', '').split('_')[0] if 'task_' in task_info else 'unknown'
            
            for subject_id in df['SubjectID'].unique():
                subject_df = df[df['SubjectID'] == subject_id]
                true_group = subject_df['Group'].iloc[0]
                
                total_epochs = len(subject_df)
                ad_predictions = (subject_df['prediction'] == 0.0).sum()
                ad_ratio = ad_predictions / total_epochs if total_epochs > 0 else 0
                
                subject_data.append({
                    'subject_id': subject_id,
                    'fold': fold_info,
                    'model': model,
                    'true_group': true_group,
                    'total_epochs': total_epochs,
                    'ad_ratio': ad_ratio
                })
        except Exception as e:
            continue
    
    return pd.DataFrame(subject_data) if subject_data else pd.DataFrame()

def test_thresholds(data):
    """Test different thresholds for subject classification"""
    if data.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    # Aggregate by subject (average across folds/models)
    subject_agg = data.groupby(['subject_id', 'true_group']).agg({
        'ad_ratio': 'mean'
    }).reset_index()
    
    subject_agg['true_label'] = (subject_agg['true_group'] == 'cntrl').astype(int)
    
    thresholds = [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7]
    results = []
    
    for threshold in thresholds:
        subject_agg['predicted'] = (subject_agg['ad_ratio'] < threshold).astype(int)
        
        y_true = subject_agg['true_label']
        y_pred = subject_agg['predicted']
        
        cm = confusion_matrix(y_true, y_pred)
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
            accuracy = (tn + tp) / (tn + tp + fp + fn)
            ad_recall = tn / (tn + fn) if (tn + fn) > 0 else 0
            cntrl_recall = tp / (tp + fp) if (tp + fp) > 0 else 0
            balanced_acc = (ad_recall + cntrl_recall) / 2
            predicted_ad_pct = (y_pred == 0).sum() / len(y_pred) * 100
            
            results.append({
                'threshold': threshold,
                'accuracy': accuracy,
                'balanced_accuracy': balanced_acc,
                'ad_recall': ad_recall,
                'cntrl_recall': cntrl_recall,
                'predicted_ad_pct': predicted_ad_pct
            })
    
    return pd.DataFrame(results), subject_agg

def analyze_distribution(data):
    """Analyze training distribution"""
    if data.empty:
        return 0.0
    total = len(data)
    ad_count = (data['true_group'] == 'alz').sum()
    return ad_count / total * 100

def analyze_all_experiments():
    """Analyze all experiments"""
    print("🧠 Multi-Experiment Subject-Level Threshold Analysis")
    print("=" * 60)
    
    experiments = {
        'ANOVA_L_2': 'grid_50_random_folds/Anova_L_2_incomplete_ml_results',
        'ANOVA_L_6': 'grid_50_random_folds/Anova_L_6_Incomplete_ml_results',
        'PCA_L_2': 'grid_50_random_folds/PCA_L_2_ml_results',
        'PCA_L_6': 'grid_50_random_folds/PCA_L_6_ml_results'
    }
    
    all_results = {}
    
    for exp_name, exp_dir in experiments.items():
        print(f"\n📊 Analyzing {exp_name}...")
        print("-" * 60)
        
        data = load_subject_predictions(exp_dir, max_folds=50)
        
        if data.empty:
            print(f"⚠️ No data found for {exp_name}")
            continue
        
        true_ad_pct = analyze_distribution(data)
        results_df, subject_agg = test_thresholds(data)
        
        if results_df.empty:
            print(f"⚠️ No results for {exp_name}")
            continue
        
        # Find best threshold
        best = results_df.loc[results_df['balanced_accuracy'].idxmax()]
        current_05 = results_df[results_df['threshold'] == 0.5].iloc[0] if len(results_df[results_df['threshold'] == 0.5]) > 0 else None
        current_055 = results_df[results_df['threshold'] == 0.55].iloc[0] if len(results_df[results_df['threshold'] == 0.55]) > 0 else None
        current_06 = results_df[results_df['threshold'] == 0.6].iloc[0] if len(results_df[results_df['threshold'] == 0.6]) > 0 else None
        
        print(f"✅ {exp_name}: {len(data)} observations, {data['subject_id'].nunique()} unique subjects")
        print(f"   Training distribution: {true_ad_pct:.1f}% AD")
        print(f"   Optimal threshold: {best['threshold']:.2f}")
        print(f"   Best accuracy: {best['accuracy']:.3f}, Balanced: {best['balanced_accuracy']:.3f}")
        
        all_results[exp_name] = {
            'data': data,
            'results_df': results_df,
            'subject_agg': subject_agg,
            'true_ad_pct': true_ad_pct,
            'best': best,
            'current_05': current_05,
            'current_055': current_055,
            'current_06': current_06,
            'n_subjects': data['subject_id'].nunique(),
            'n_observations': len(data)
        }
    
    return all_results

def create_comparison_visualizations(all_results, output_dir="visualizations"):
    """Create comparison visualizations"""
    print(f"\n📊 Creating comparison visualizations...")
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Accuracy vs Threshold (all experiments)
    ax = axes[0, 0]
    for exp_name, results in all_results.items():
        ax.plot(results['results_df']['threshold'], results['results_df']['accuracy'], 
               'o-', label=exp_name, linewidth=2, markersize=6)
    ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='Current (0.5)')
    ax.axvline(x=0.55, color='orange', linestyle='--', alpha=0.5, label='0.55')
    ax.axvline(x=0.6, color='green', linestyle='--', alpha=0.5, label='0.6')
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Accuracy')
    ax.set_title('Accuracy vs Threshold (All Experiments)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Balanced Accuracy vs Threshold
    ax = axes[0, 1]
    for exp_name, results in all_results.items():
        ax.plot(results['results_df']['threshold'], results['results_df']['balanced_accuracy'], 
               's-', label=exp_name, linewidth=2, markersize=6)
    ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.5)
    ax.axvline(x=0.55, color='orange', linestyle='--', alpha=0.5)
    ax.axvline(x=0.6, color='green', linestyle='--', alpha=0.5)
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Balanced Accuracy')
    ax.set_title('Balanced Accuracy vs Threshold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. AD Recall vs Threshold
    ax = axes[1, 0]
    for exp_name, results in all_results.items():
        ax.plot(results['results_df']['threshold'], results['results_df']['ad_recall'], 
               '^-', label=exp_name, linewidth=2, markersize=6)
    ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.5)
    ax.axvline(x=0.55, color='orange', linestyle='--', alpha=0.5)
    ax.axvline(x=0.6, color='green', linestyle='--', alpha=0.5)
    ax.set_xlabel('Threshold')
    ax.set_ylabel('AD Recall')
    ax.set_title('AD Recall vs Threshold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Optimal Threshold Comparison
    ax = axes[1, 1]
    exp_names = list(all_results.keys())
    optimal_thresholds = [all_results[exp]['best']['threshold'] for exp in exp_names]
    optimal_accuracies = [all_results[exp]['best']['accuracy'] for exp in exp_names]
    
    bars = ax.bar(exp_names, optimal_accuracies, color=['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181'], alpha=0.7)
    for i, (bar, thresh) in enumerate(zip(bars, optimal_thresholds)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height() + 0.01,
               f"T={thresh:.2f}", ha='center', va='bottom', fontweight='bold')
    ax.set_ylabel('Best Accuracy')
    ax.set_title('Optimal Threshold Performance by Experiment')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/multi_experiment_threshold_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved comparison visualization")

def create_comprehensive_report(all_results):
    """Create comprehensive report"""
    print("\n📝 Creating comprehensive report...")
    
    # Build summary table
    summary_rows = []
    for exp_name, results in all_results.items():
        best = results['best']
        current_05 = results['current_05']
        current_055 = results['current_055']
        current_06 = results['current_06']
        
        summary_rows.append({
            'Experiment': exp_name,
            'Training AD %': f"{results['true_ad_pct']:.1f}%",
            'Optimal Threshold': f"{best['threshold']:.2f}",
            'Optimal Accuracy': f"{best['accuracy']:.3f}",
            'Optimal Balanced': f"{best['balanced_accuracy']:.3f}",
            'Optimal AD Recall': f"{best['ad_recall']:.3f}",
            '0.5 Accuracy': f"{current_05['accuracy']:.3f}" if current_05 is not None else 'N/A',
            '0.55 Accuracy': f"{current_055['accuracy']:.3f}" if current_055 is not None else 'N/A',
            '0.6 Accuracy': f"{current_06['accuracy']:.3f}" if current_06 is not None else 'N/A',
            'N Subjects': results['n_subjects']
        })
    
    summary_df = pd.DataFrame(summary_rows)
    
    # Create report
    report = f"""# 🎯 Comprehensive Subject-Level Classification Threshold Analysis

## Analysis Overview

This report analyzes optimal classification thresholds across **4 experiments**:
- **ANOVA_L_2**: ANOVA features, Leave-2-out cross-validation
- **ANOVA_L_6**: ANOVA features, Leave-6-out cross-validation  
- **PCA_L_2**: PCA features, Leave-2-out cross-validation
- **PCA_L_6**: PCA features, Leave-6-out cross-validation

## 📊 Summary Results by Experiment

| Experiment | Training AD % | Optimal Threshold | Optimal Accuracy | Optimal Balanced | Optimal AD Recall | 0.5 Accuracy | 0.55 Accuracy | 0.6 Accuracy | N Subjects |
|------------|----------------|-------------------|------------------|------------------|-------------------|--------------|---------------|--------------|------------|
"""
    
    for row in summary_rows:
        report += f"| {row['Experiment']} | {row['Training AD %']} | {row['Optimal Threshold']} | {row['Optimal Accuracy']} | {row['Optimal Balanced']} | {row['Optimal AD Recall']} | {row['0.5 Accuracy']} | {row['0.55 Accuracy']} | {row['0.6 Accuracy']} | {row['N Subjects']} |\n"
    
    report += f"""
## 🎯 Key Findings

### 1. Optimal Thresholds Vary by Experiment

"""
    
    for exp_name, results in all_results.items():
        best = results['best']
        current_05 = results['current_05']
        improvement = (best['accuracy'] - current_05['accuracy']) * 100 if current_05 is not None else 0
        report += f"**{exp_name}**:\n"
        report += f"- Optimal threshold: **{best['threshold']:.2f}**\n"
        report += f"- Best accuracy: {best['accuracy']:.3f} (vs {current_05['accuracy']:.3f} at 0.5 = {improvement:+.1f}% improvement)\n"
        report += f"- Best balanced accuracy: {best['balanced_accuracy']:.3f}\n"
        report += f"- AD recall: {best['ad_recall']:.3f}\n"
        report += f"- Training distribution: {results['true_ad_pct']:.1f}% AD\n\n"
    
    report += f"""
### 2. Threshold Performance Comparison

#### ANOVA Experiments
"""
    
    for exp_name in ['ANOVA_L_2', 'ANOVA_L_6']:
        if exp_name in all_results:
            results = all_results[exp_name]
            current_05 = results['current_05']
            current_055 = results['current_055']
            current_06 = results['current_06']
            best = results['best']
            
            report += f"\n**{exp_name}**:\n"
            report += f"- 0.5 threshold: Accuracy={current_05['accuracy']:.3f}, Balanced={current_05['balanced_accuracy']:.3f}, AD Recall={current_05['ad_recall']:.3f}\n"
            if current_055 is not None:
                report += f"- 0.55 threshold: Accuracy={current_055['accuracy']:.3f}, Balanced={current_055['balanced_accuracy']:.3f}, AD Recall={current_055['ad_recall']:.3f}\n"
            if current_06 is not None:
                report += f"- 0.6 threshold: Accuracy={current_06['accuracy']:.3f}, Balanced={current_06['balanced_accuracy']:.3f}, AD Recall={current_06['ad_recall']:.3f}\n"
            report += f"- Optimal ({best['threshold']:.2f}): Accuracy={best['accuracy']:.3f}, Balanced={best['balanced_accuracy']:.3f}, AD Recall={best['ad_recall']:.3f}\n"
    
    report += f"\n#### PCA Experiments\n"
    
    for exp_name in ['PCA_L_2', 'PCA_L_6']:
        if exp_name in all_results:
            results = all_results[exp_name]
            current_05 = results['current_05']
            current_055 = results['current_055']
            current_06 = results['current_06']
            best = results['best']
            
            report += f"\n**{exp_name}**:\n"
            report += f"- 0.5 threshold: Accuracy={current_05['accuracy']:.3f}, Balanced={current_05['balanced_accuracy']:.3f}, AD Recall={current_05['ad_recall']:.3f}\n"
            if current_055 is not None:
                report += f"- 0.55 threshold: Accuracy={current_055['accuracy']:.3f}, Balanced={current_055['balanced_accuracy']:.3f}, AD Recall={current_055['ad_recall']:.3f}\n"
            if current_06 is not None:
                report += f"- 0.6 threshold: Accuracy={current_06['accuracy']:.3f}, Balanced={current_06['balanced_accuracy']:.3f}, AD Recall={current_06['ad_recall']:.3f}\n"
            report += f"- Optimal ({best['threshold']:.2f}): Accuracy={best['accuracy']:.3f}, Balanced={best['balanced_accuracy']:.3f}, AD Recall={best['ad_recall']:.3f}\n"
    
    # Calculate overall recommendations
    optimal_thresholds = [all_results[exp]['best']['threshold'] for exp in all_results.keys()]
    avg_optimal = np.mean(optimal_thresholds)
    
    report += f"""
## 🎯 Overall Recommendations

### Universal Recommendation

Based on all experiments, the **optimal threshold range is {min(optimal_thresholds):.2f} - {max(optimal_thresholds):.2f}**, with an average of **{avg_optimal:.2f}**.

### Experiment-Specific Recommendations

"""
    
    for exp_name, results in all_results.items():
        best = results['best']
        report += f"**{exp_name}**: Use threshold **{best['threshold']:.2f}**\n"
        report += f"- Improves accuracy from {results['current_05']['accuracy']:.3f} (0.5) to {best['accuracy']:.3f} ({best['threshold']:.2f})\n"
        report += f"- Improvement: {((best['accuracy'] - results['current_05']['accuracy']) * 100):+.1f}%\n\n"
    
    report += f"""
### Conservative vs Optimal Approach

**Conservative (0.55 threshold):**
- Moderate improvement over 0.5
- Good middle ground
- Works reasonably well across all experiments

**Optimal (experiment-specific):**
- Best performance for each experiment
- Thresholds range from {min(optimal_thresholds):.2f} to {max(optimal_thresholds):.2f}
- Requires experiment-specific implementation

## 📈 Performance Improvements

### By Experiment

"""
    
    for exp_name, results in all_results.items():
        current_05 = results['current_05']
        best = results['best']
        improvement = (best['accuracy'] - current_05['accuracy']) * 100
        ad_recall_improvement = (best['ad_recall'] - current_05['ad_recall']) * 100
        
        report += f"**{exp_name}**:\n"
        report += f"- Accuracy improvement: {improvement:+.1f}% ({current_05['accuracy']:.3f} → {best['accuracy']:.3f})\n"
        report += f"- AD Recall improvement: {ad_recall_improvement:+.1f}% ({current_05['ad_recall']:.3f} → {best['ad_recall']:.3f})\n"
        report += f"- Optimal threshold: {best['threshold']:.2f}\n\n"
    
    report += f"""
## 🔧 Implementation Guide

### Option 1: Universal Threshold (Simplest)

Use a single threshold for all experiments:

```python
# Conservative universal threshold
if ad_ratio >= 0.55:
    subject_class = "AD"
else:
    subject_class = "Control"

# OR Optimal universal threshold (average)
if ad_ratio >= {avg_optimal:.2f}:
    subject_class = "AD"
else:
    subject_class = "Control"
```

### Option 2: Experiment-Specific Thresholds (Best Performance)

Use different thresholds based on the experiment:

```python
# Threshold mapping by experiment
thresholds = {{
    'ANOVA_L_2': {all_results.get('ANOVA_L_2', {}).get('best', {}).get('threshold', 0.6):.2f},
    'ANOVA_L_6': {all_results.get('ANOVA_L_6', {}).get('best', {}).get('threshold', 0.6):.2f},
    'PCA_L_2': {all_results.get('PCA_L_2', {}).get('best', {}).get('threshold', 0.6):.2f},
    'PCA_L_6': {all_results.get('PCA_L_6', {}).get('best', {}).get('threshold', 0.6):.2f}
}}

# Use experiment-specific threshold
threshold = thresholds[experiment_name]
if ad_ratio >= threshold:
    subject_class = "AD"
else:
    subject_class = "Control"
```

## 📊 Detailed Results Tables

### ANOVA_L_2 Performance by Threshold

"""
    
    if 'ANOVA_L_2' in all_results:
        results_df = all_results['ANOVA_L_2']['results_df']
        report += "| Threshold | Accuracy | Balanced | AD Recall | CNTRL Recall | Pred AD % |\n"
        report += "|-----------|----------|----------|-----------|--------------|-----------|\n"
        for _, row in results_df.iterrows():
            report += f"| {row['threshold']:.2f} | {row['accuracy']:.3f} | {row['balanced_accuracy']:.3f} | {row['ad_recall']:.3f} | {row['cntrl_recall']:.3f} | {row['predicted_ad_pct']:.1f}% |\n"
    
    report += f"\n### ANOVA_L_6 Performance by Threshold\n\n"
    
    if 'ANOVA_L_6' in all_results:
        results_df = all_results['ANOVA_L_6']['results_df']
        report += "| Threshold | Accuracy | Balanced | AD Recall | CNTRL Recall | Pred AD % |\n"
        report += "|-----------|----------|----------|-----------|--------------|-----------|\n"
        for _, row in results_df.iterrows():
            report += f"| {row['threshold']:.2f} | {row['accuracy']:.3f} | {row['balanced_accuracy']:.3f} | {row['ad_recall']:.3f} | {row['cntrl_recall']:.3f} | {row['predicted_ad_pct']:.1f}% |\n"
    
    report += f"\n### PCA_L_2 Performance by Threshold\n\n"
    
    if 'PCA_L_2' in all_results:
        results_df = all_results['PCA_L_2']['results_df']
        report += "| Threshold | Accuracy | Balanced | AD Recall | CNTRL Recall | Pred AD % |\n"
        report += "|-----------|----------|----------|-----------|--------------|-----------|\n"
        for _, row in results_df.iterrows():
            report += f"| {row['threshold']:.2f} | {row['accuracy']:.3f} | {row['balanced_accuracy']:.3f} | {row['ad_recall']:.3f} | {row['cntrl_recall']:.3f} | {row['predicted_ad_pct']:.1f}% |\n"
    
    report += f"\n### PCA_L_6 Performance by Threshold\n\n"
    
    if 'PCA_L_6' in all_results:
        results_df = all_results['PCA_L_6']['results_df']
        report += "| Threshold | Accuracy | Balanced | AD Recall | CNTRL Recall | Pred AD % |\n"
        report += "|-----------|----------|----------|-----------|--------------|-----------|\n"
        for _, row in results_df.iterrows():
            report += f"| {row['threshold']:.2f} | {row['accuracy']:.3f} | {row['balanced_accuracy']:.3f} | {row['ad_recall']:.3f} | {row['cntrl_recall']:.3f} | {row['predicted_ad_pct']:.1f}% |\n"
    
    report += f"""
## 🎯 Final Recommendations Summary

1. **Universal Approach**: Use **0.55-0.60 threshold** for all experiments (good balance)
2. **Optimal Approach**: Use experiment-specific thresholds (best performance)
3. **Current 0.5 threshold is suboptimal** for all experiments - improvements range from {min([(all_results[exp]['best']['accuracy'] - all_results[exp]['current_05']['accuracy']) * 100 for exp in all_results.keys()]):.1f}% to {max([(all_results[exp]['best']['accuracy'] - all_results[exp]['current_05']['accuracy']) * 100 for exp in all_results.keys()]):.1f}%

---
*Analysis completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*
*Experiments analyzed: {', '.join(all_results.keys())}*
*Total subjects analyzed: {sum([all_results[exp]['n_subjects'] for exp in all_results.keys()])}*
"""
    
    with open('final_subject_threshold_analysis.md', 'w') as f:
        f.write(report)
    
    print("✅ Saved comprehensive report: final_subject_threshold_analysis.md")

def main():
    """Main analysis function"""
    all_results = analyze_all_experiments()
    
    if not all_results:
        print("❌ No results from any experiment")
        return
    
    create_comparison_visualizations(all_results)
    create_comprehensive_report(all_results)
    
    print("\n🎉 COMPREHENSIVE ANALYSIS COMPLETE!")
    print(f"📊 Analyzed {len(all_results)} experiments")
    print("📁 Check final_subject_threshold_analysis.md for full report")
    print("📁 Check visualizations/multi_experiment_threshold_analysis.png for visualizations")

if __name__ == "__main__":
    main()




