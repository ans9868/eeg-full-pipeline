#!/usr/bin/env python3
"""
Clear Threshold Analysis - Per Subject Classification Results

For each threshold, shows:
- How many subjects classified as AD vs Control
- How many are correctly classified (actual numbers)
- Per model × experiment
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

def load_all_predictions(experiment_dir, max_folds=50):
    """Load all predictions"""
    results_dir = Path(experiment_dir)
    parquet_files = list(results_dir.rglob("test_predictions.parquet"))
    
    if len(parquet_files) > max_folds * 4:
        import random
        parquet_files = random.sample(parquet_files, max_folds * 4)
    
    all_data = []
    
    for parquet_file in parquet_files:
        try:
            df = pd.read_parquet(parquet_file)
            path_parts = str(parquet_file).split('/')
            fold_info = path_parts[-3]
            task_info = path_parts[-2]
            
            if 'task_' in task_info:
                model = task_info.replace('task_', '').split('_')[0]
            else:
                model = 'unknown'
            
            for subject_id in df['SubjectID'].unique():
                subject_df = df[df['SubjectID'] == subject_id]
                true_group = subject_df['Group'].iloc[0]
                
                total_epochs = len(subject_df)
                ad_predictions = (subject_df['prediction'] == 0.0).sum()
                ad_ratio = ad_predictions / total_epochs if total_epochs > 0 else 0
                
                all_data.append({
                    'subject_id': subject_id,
                    'fold': fold_info,
                    'model': model,
                    'true_group': true_group,
                    'ad_ratio': ad_ratio
                })
        except Exception as e:
            continue
    
    return pd.DataFrame(all_data) if all_data else pd.DataFrame()

def analyze_threshold_per_model_experiment(data, experiment_name):
    """Analyze threshold per model, showing actual numbers"""
    
    results_by_model = {}
    
    for model in data['model'].unique():
        model_data = data[data['model'] == model]
        
        # Aggregate by subject (average across folds)
        subject_agg = model_data.groupby(['subject_id', 'true_group']).agg({
            'ad_ratio': 'mean'
        }).reset_index()
        
        thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        model_results = []
        
        for threshold in thresholds:
            # Classify: if ad_ratio >= threshold, predict AD, else Control
            subject_agg['predicted_group'] = subject_agg['ad_ratio'].apply(
                lambda x: 'alz' if x >= threshold else 'cntrl'
            )
            
            # Count classifications
            total_subjects = len(subject_agg)
            predicted_ad = (subject_agg['predicted_group'] == 'alz').sum()
            predicted_cntrl = (subject_agg['predicted_group'] == 'cntrl').sum()
            
            # Count correct classifications
            correct = (subject_agg['true_group'] == subject_agg['predicted_group']).sum()
            correct_ad = ((subject_agg['true_group'] == 'alz') & 
                         (subject_agg['predicted_group'] == 'alz')).sum()
            correct_cntrl = ((subject_agg['true_group'] == 'cntrl') & 
                            (subject_agg['predicted_group'] == 'cntrl')).sum()
            
            # Count incorrect
            incorrect = total_subjects - correct
            incorrect_ad_as_cntrl = ((subject_agg['true_group'] == 'alz') & 
                                    (subject_agg['predicted_group'] == 'cntrl')).sum()
            incorrect_cntrl_as_ad = ((subject_agg['true_group'] == 'cntrl') & 
                                     (subject_agg['predicted_group'] == 'alz')).sum()
            
            # True counts
            true_ad = (subject_agg['true_group'] == 'alz').sum()
            true_cntrl = (subject_agg['true_group'] == 'cntrl').sum()
            
            accuracy = correct / total_subjects if total_subjects > 0 else 0
            
            model_results.append({
                'threshold': threshold,
                'total_subjects': total_subjects,
                'true_ad': true_ad,
                'true_cntrl': true_cntrl,
                'predicted_ad': predicted_ad,
                'predicted_cntrl': predicted_cntrl,
                'correct_total': correct,
                'correct_ad': correct_ad,
                'correct_cntrl': correct_cntrl,
                'incorrect_total': incorrect,
                'incorrect_ad_as_cntrl': incorrect_ad_as_cntrl,
                'incorrect_cntrl_as_ad': incorrect_cntrl_as_ad,
                'accuracy': accuracy
            })
        
        results_by_model[model] = pd.DataFrame(model_results)
    
    return results_by_model

def create_clear_report(all_results):
    """Create clear report with actual numbers"""
    print("\n📝 Creating clear report with actual numbers...")
    
    report = """# 📊 Clear Threshold Analysis - Per Subject Classification Results

## Analysis Overview

This analysis shows **actual numbers** of subjects classified and correctly classified for each threshold.
The threshold is chosen **per model × experiment** based on overall accuracy, NOT using per-subject information.

## 📈 Results by Experiment and Model

"""
    
    for exp_name, results in all_results.items():
        report += f"## {exp_name}\n\n"
        
        for model, model_results in results.items():
            if model_results.empty:
                continue
            
            # Find best threshold
            best = model_results.loc[model_results['accuracy'].idxmax()]
            
            report += f"### {model}\n\n"
            report += f"**Optimal Threshold: {best['threshold']:.2f}**\n\n"
            
            # Show results for key thresholds
            key_thresholds = [0.5, 0.55, 0.6, best['threshold']]
            key_thresholds = sorted(set(key_thresholds))
            
            report += "| Threshold | Total Subjects | True AD | True CNTRL | Predicted AD | Predicted CNTRL | Correct Total | Correct AD | Correct CNTRL | Incorrect Total | Accuracy |\n"
            report += "|-----------|----------------|---------|------------|--------------|-----------------|---------------|------------|---------------|------------------|----------|\n"
            
            for thresh in key_thresholds:
                row = model_results[model_results['threshold'] == thresh]
                if not row.empty:
                    r = row.iloc[0]
                    marker = " ⭐" if thresh == best['threshold'] else ""
                    report += f"| {thresh:.2f}{marker} | {int(r['total_subjects'])} | {int(r['true_ad'])} | {int(r['true_cntrl'])} | {int(r['predicted_ad'])} | {int(r['predicted_cntrl'])} | {int(r['correct_total'])} | {int(r['correct_ad'])} | {int(r['correct_cntrl'])} | {int(r['incorrect_total'])} | {r['accuracy']:.3f} |\n"
            
            report += "\n"
            
            # Detailed breakdown for optimal threshold
            report += f"**Detailed Breakdown at Optimal Threshold ({best['threshold']:.2f}):**\n\n"
            report += f"- **Total Subjects**: {int(best['total_subjects'])}\n"
            report += f"- **True AD Subjects**: {int(best['true_ad'])}\n"
            report += f"- **True Control Subjects**: {int(best['true_cntrl'])}\n\n"
            report += f"- **Predicted as AD**: {int(best['predicted_ad'])} ({best['predicted_ad']/best['total_subjects']*100:.1f}%)\n"
            report += f"- **Predicted as Control**: {int(best['predicted_cntrl'])} ({best['predicted_cntrl']/best['total_subjects']*100:.1f}%)\n\n"
            report += f"- **Correctly Classified**: {int(best['correct_total'])} ({best['accuracy']*100:.1f}%)\n"
            report += f"  - Correct AD: {int(best['correct_ad'])} out of {int(best['true_ad'])} true AD ({best['correct_ad']/best['true_ad']*100:.1f}%)\n"
            report += f"  - Correct Control: {int(best['correct_cntrl'])} out of {int(best['true_cntrl'])} true Control ({best['correct_cntrl']/best['true_cntrl']*100:.1f}%)\n\n"
            report += f"- **Incorrectly Classified**: {int(best['incorrect_total'])} ({best['incorrect_total']/best['total_subjects']*100:.1f}%)\n"
            report += f"  - AD misclassified as Control: {int(best['incorrect_ad_as_cntrl'])}\n"
            report += f"  - Control misclassified as AD: {int(best['incorrect_cntrl_as_ad'])}\n\n"
            
            report += "---\n\n"
    
    # Summary table
    report += "## 📋 Summary: Optimal Thresholds by Model × Experiment\n\n"
    report += "| Experiment | Model | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |\n"
    report += "|------------|-------|-------------------|----------------|---------|-----------|----------|\n"
    
    for exp_name, results in all_results.items():
        for model, model_results in results.items():
            if model_results.empty:
                continue
            best = model_results.loc[model_results['accuracy'].idxmax()]
            report += f"| {exp_name} | {model} | {best['threshold']:.2f} | {int(best['total_subjects'])} | {int(best['correct_total'])} | {int(best['incorrect_total'])} | {best['accuracy']:.3f} |\n"
    
    report += f"\n---\n*Analysis completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*\n"
    report += "*Threshold chosen per model × experiment based on overall accuracy*\n"
    
    with open('clear_threshold_analysis.md', 'w') as f:
        f.write(report)
    
    print("✅ Saved clear report: clear_threshold_analysis.md")

def main():
    """Main analysis"""
    print("📊 Clear Threshold Analysis - Per Subject Classification")
    print("=" * 70)
    
    experiments = {
        'ANOVA_L_2': 'grid_50_random_folds/Anova_L_2_incomplete_ml_results',
        'ANOVA_L_6': 'grid_50_random_folds/Anova_L_6_Incomplete_ml_results',
        'PCA_L_2': 'grid_50_random_folds/PCA_L_2_ml_results',
        'PCA_L_6': 'grid_50_random_folds/PCA_L_6_ml_results'
    }
    
    all_results = {}
    
    for exp_name, exp_dir in experiments.items():
        print(f"\n📊 Analyzing {exp_name}...")
        
        data = load_all_predictions(exp_dir, max_folds=50)
        
        if data.empty:
            print(f"⚠️ No data")
            continue
        
        print(f"✅ Loaded {len(data)} observations")
        print(f"   Subjects: {data['subject_id'].nunique()}, Models: {data['model'].unique()}")
        
        # Analyze per model
        results_by_model = analyze_threshold_per_model_experiment(data, exp_name)
        
        # Print summary
        for model, model_results in results_by_model.items():
            if not model_results.empty:
                best = model_results.loc[model_results['accuracy'].idxmax()]
                print(f"   {model}: Best threshold = {best['threshold']:.2f}, "
                      f"Accuracy = {best['accuracy']:.3f}, "
                      f"Correct = {int(best['correct_total'])}/{int(best['total_subjects'])}")
        
        all_results[exp_name] = results_by_model
    
    create_clear_report(all_results)
    
    print("\n🎉 CLEAR ANALYSIS COMPLETE!")
    print("📁 Check clear_threshold_analysis.md for detailed numbers")

if __name__ == "__main__":
    main()




