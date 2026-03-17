#!/usr/bin/env python3
"""
Per-Experiment Independent Threshold Analysis

Each experiment is treated independently. A subject's performance in Experiment 1
is separate from their performance in Experiment 2. No averaging across experiments.
"""

import pandas as pd
import numpy as np
import json
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

def extract_hyperparameters(parquet_file_path):
    """Extract hyperparameters from results.json file"""
    hyperparams = {}
    results_json = parquet_file_path.parent / "results.json"
    
    if results_json.exists():
        try:
            with open(results_json, 'r') as f:
                results_data = json.load(f)
                if 'hyperparams' in results_data:
                    hyperparams = results_data['hyperparams']
                elif 'detailed_results' in results_data and 'metadata' in results_data['detailed_results']:
                    if 'hyperparams' in results_data['detailed_results']['metadata']:
                        hyperparams = results_data['detailed_results']['metadata']['hyperparams']
        except:
            pass
    
    # Create hyperparameter string
    if hyperparams:
        if 'n_neighbors' in hyperparams:
            param_str = f"n_neighbors={hyperparams['n_neighbors']}"
        elif 'max_depth' in hyperparams:
            param_str = f"max_depth={hyperparams['max_depth']}"
        elif 'kernel' in hyperparams:
            param_str = f"kernel={hyperparams['kernel']}"
        elif 'hidden_layer_sizes' in hyperparams:
            hidden = hyperparams['hidden_layer_sizes']
            if isinstance(hidden, list):
                param_str = f"hidden={'_'.join(map(str, hidden))}"
            else:
                param_str = f"hidden={hidden}"
        else:
            sorted_params = sorted(hyperparams.items())
            param_str = "_".join([f"{k}={v}" for k, v in sorted_params])
    else:
        param_str = "default"
    
    return hyperparams, param_str

def load_experiment_data(experiment_dir, max_folds=50):
    """Load data for a single experiment"""
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
            
            # Extract hyperparameters
            hyperparams, param_str = extract_hyperparameters(parquet_file)
            
            if param_str != "default":
                model_hp = f"{model}_{param_str}"
            else:
                model_hp = model
            
            for subject_id in df['SubjectID'].unique():
                subject_df = df[df['SubjectID'] == subject_id]
                true_group = subject_df['Group'].iloc[0]
                
                total_epochs = len(subject_df)
                ad_predictions = (subject_df['prediction'] == 0.0).sum()
                ad_ratio = ad_predictions / total_epochs if total_epochs > 0 else 0
                
                # Calculate per-subject accuracy in THIS experiment
                correct_epochs = (subject_df['label'] == subject_df['prediction']).sum()
                subject_accuracy = correct_epochs / total_epochs if total_epochs > 0 else 0
                
                all_data.append({
                    'subject_id': subject_id,
                    'fold': fold_info,
                    'model': model,
                    'model_hp': model_hp,
                    'hyperparams': param_str,
                    'true_group': true_group,
                    'ad_ratio': ad_ratio,
                    'subject_accuracy': subject_accuracy,
                    'total_epochs': total_epochs
                })
        except Exception as e:
            continue
    
    return pd.DataFrame(all_data) if all_data else pd.DataFrame()

def analyze_threshold_per_model_hp_independent(data, experiment_name):
    """Analyze threshold per model×hyperparameter, treating experiment independently"""
    
    results_by_model_hp = {}
    
    for model_hp in data['model_hp'].unique():
        model_hp_data = data[data['model_hp'] == model_hp]
        
        # Aggregate by subject WITHIN this experiment (average across folds only)
        # This is the key: we're NOT averaging across experiments
        subject_agg = model_hp_data.groupby(['subject_id', 'true_group']).agg({
            'ad_ratio': 'mean',  # Average across folds within this experiment
            'subject_accuracy': 'mean'  # Average accuracy across folds within this experiment
        }).reset_index()
        
        thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        model_hp_results = []
        
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
            
            model_hp_results.append({
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
        
        results_by_model_hp[model_hp] = pd.DataFrame(model_hp_results)
    
    return results_by_model_hp

def create_independent_report(all_results):
    """Create report with independent experiment analysis"""
    print("\n📝 Creating independent experiment report...")
    
    report = """# 🎯 Per-Experiment Independent Threshold Analysis

## Analysis Overview

**Key Difference**: Each experiment is treated **independently**. A subject's performance in Experiment 1 is completely separate from their performance in Experiment 2.

**Example**:
- Subject 1 in Experiment 1: 20% accuracy → Incorrectly classified
- Subject 1 in Experiment 2: 91% accuracy → Correctly classified
- Result: Subject 1 is correctly classified **1 out of 2 times** (50%), NOT averaged

**Method**:
1. For each experiment separately
2. For each model×hyperparameter combination
3. Calculate per-subject AD ratio (averaged across folds within that experiment only)
4. Apply threshold to classify subjects
5. Count correct/incorrect classifications
6. Find optimal threshold per model×experiment×hyperparameter

## 📊 Results by Experiment and Model×Hyperparameter

"""
    
    summary_rows = []
    
    for exp_name, results in all_results.items():
        report += f"## {exp_name}\n\n"
        
        # Group by base model
        models = {}
        for model_hp, model_results in results.items():
            base_model = model_hp.split('_')[0]
            if base_model not in models:
                models[base_model] = []
            models[base_model].append((model_hp, model_results))
        
        for base_model in sorted(models.keys()):
            report += f"### {base_model}\n\n"
            
            for model_hp, model_results in sorted(models[base_model]):
                if model_results.empty:
                    continue
                
                best = model_results.loc[model_results['accuracy'].idxmax()]
                hp_parts = model_hp.replace(f"{base_model}_", "")
                
                report += f"#### {base_model} ({hp_parts if hp_parts else 'default'})\n\n"
                report += f"**Optimal Threshold: {best['threshold']:.2f}**\n\n"
                
                # Show key thresholds
                key_thresholds = [0.5, 0.55, 0.6, best['threshold']]
                key_thresholds = sorted(set([t for t in key_thresholds if t in model_results['threshold'].values]))
                
                report += "| Threshold | Total | True AD | True CNTRL | Pred AD | Pred CNTRL | Correct | Correct AD | Correct CNTRL | Incorrect | Accuracy |\n"
                report += "|-----------|-------|---------|------------|---------|------------|---------|------------|---------------|-----------|----------|\n"
                
                for thresh in key_thresholds:
                    row = model_results[model_results['threshold'] == thresh]
                    if not row.empty:
                        r = row.iloc[0]
                        marker = " ⭐" if thresh == best['threshold'] else ""
                        report += f"| {thresh:.2f}{marker} | {int(r['total_subjects'])} | {int(r['true_ad'])} | {int(r['true_cntrl'])} | {int(r['predicted_ad'])} | {int(r['predicted_cntrl'])} | {int(r['correct_total'])} | {int(r['correct_ad'])} | {int(r['correct_cntrl'])} | {int(r['incorrect_total'])} | {r['accuracy']:.3f} |\n"
                
                report += f"\n**Detailed Breakdown at Optimal Threshold ({best['threshold']:.2f}):**\n\n"
                report += f"- **Total Subjects**: {int(best['total_subjects'])}\n"
                report += f"- **True AD**: {int(best['true_ad'])} | **True Control**: {int(best['true_cntrl'])}\n"
                report += f"- **Predicted as AD**: {int(best['predicted_ad'])} ({best['predicted_ad']/best['total_subjects']*100:.1f}%)\n"
                report += f"- **Predicted as Control**: {int(best['predicted_cntrl'])} ({best['predicted_cntrl']/best['total_subjects']*100:.1f}%)\n"
                report += f"- **Correctly Classified**: {int(best['correct_total'])} out of {int(best['total_subjects'])} ({best['accuracy']*100:.1f}%)\n"
                report += f"  - Correct AD: {int(best['correct_ad'])} out of {int(best['true_ad'])} ({best['correct_ad']/best['true_ad']*100:.1f}%)\n"
                report += f"  - Correct Control: {int(best['correct_cntrl'])} out of {int(best['true_cntrl'])} ({best['correct_cntrl']/best['true_cntrl']*100:.1f}%)\n"
                report += f"- **Incorrectly Classified**: {int(best['incorrect_total'])} ({best['incorrect_total']/best['total_subjects']*100:.1f}%)\n"
                report += f"  - AD → Control: {int(best['incorrect_ad_as_cntrl'])}\n"
                report += f"  - Control → AD: {int(best['incorrect_cntrl_as_ad'])}\n\n"
                
                summary_rows.append({
                    'experiment': exp_name,
                    'model_hp': model_hp,
                    'threshold': best['threshold'],
                    'total': int(best['total_subjects']),
                    'correct': int(best['correct_total']),
                    'incorrect': int(best['incorrect_total']),
                    'accuracy': best['accuracy']
                })
                
                report += "---\n\n"
    
    # Summary table
    report += "## 📋 Summary: Optimal Thresholds by Model×Hyperparameter×Experiment\n\n"
    report += "| Experiment | Model×Hyperparameters | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |\n"
    report += "|------------|------------------------|-------------------|----------------|---------|-----------|----------|\n"
    
    for row in summary_rows:
        report += f"| {row['experiment']} | {row['model_hp']} | {row['threshold']:.2f} | {row['total']} | {row['correct']} | {row['incorrect']} | {row['accuracy']:.3f} |\n"
    
    # KNN-specific summary
    report += "\n## 🎯 KNN-Specific Summary (Per Experiment)\n\n"
    knn_rows = [r for r in summary_rows if r['model_hp'].startswith('KNN')]
    if knn_rows:
        report += "| Experiment | KNN Hyperparameters | Threshold | Total | Correct | Incorrect | Accuracy |\n"
        report += "|------------|---------------------|-----------|-------|---------|-----------|----------|\n"
        for row in knn_rows:
            hp = row['model_hp'].replace('KNN_', '')
            report += f"| {row['experiment']} | {hp} | {row['threshold']:.2f} | {row['total']} | {row['correct']} | {row['incorrect']} | {row['accuracy']:.3f} |\n"
    
    report += f"\n## 🔑 Key Points\n\n"
    report += "1. **Each experiment analyzed independently** - no cross-experiment averaging\n"
    report += "2. **Per-subject performance calculated within each experiment** - averaged across folds only\n"
    report += "3. **Threshold optimization per model×experiment×hyperparameter** - each combination gets its own optimal threshold\n"
    report += "4. **Subject counts are per experiment** - same subject in different experiments counted separately\n\n"
    
    report += f"---\n*Analysis completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*\n"
    report += "*Each experiment treated independently - no cross-experiment averaging*\n"
    
    with open('per_experiment_independent_threshold_analysis.md', 'w') as f:
        f.write(report)
    
    print("✅ Saved report: per_experiment_independent_threshold_analysis.md")

def main():
    """Main analysis"""
    print("🔍 Per-Experiment Independent Threshold Analysis")
    print("=" * 70)
    print("Each experiment treated independently - no cross-experiment averaging")
    print()
    
    experiments = {
        'ANOVA_L_2': 'grid_50_random_folds/Anova_L_2_incomplete_ml_results',
        'ANOVA_L_6': 'grid_50_random_folds/Anova_L_6_Incomplete_ml_results',
        'PCA_L_2': 'grid_50_random_folds/PCA_L_2_ml_results',
        'PCA_L_6': 'grid_50_random_folds/PCA_L_6_ml_results'
    }
    
    all_results = {}
    
    for exp_name, exp_dir in experiments.items():
        print(f"\n📊 Analyzing {exp_name} (INDEPENDENTLY)...")
        print("-" * 70)
        
        # Load data for THIS experiment only
        data = load_experiment_data(exp_dir, max_folds=50)
        
        if data.empty:
            print(f"⚠️ No data")
            continue
        
        print(f"✅ Loaded {len(data)} observations for {exp_name}")
        print(f"   Subjects: {data['subject_id'].nunique()}")
        print(f"   Model×HP combinations: {data['model_hp'].nunique()}")
        
        # Analyze per model×hyperparameter WITHIN this experiment
        results_by_model_hp = analyze_threshold_per_model_hp_independent(data, exp_name)
        
        # Print summary
        for model_hp, model_results in results_by_model_hp.items():
            if not model_results.empty:
                best = model_results.loc[model_results['accuracy'].idxmax()]
                print(f"   {model_hp}: Threshold = {best['threshold']:.2f}, "
                      f"Accuracy = {best['accuracy']:.3f}, "
                      f"Correct = {int(best['correct_total'])}/{int(best['total_subjects'])}")
        
        all_results[exp_name] = results_by_model_hp
    
    create_independent_report(all_results)
    
    print("\n🎉 INDEPENDENT EXPERIMENT ANALYSIS COMPLETE!")
    print("📁 Check per_experiment_independent_threshold_analysis.md")
    print("\n🔑 Key: Each experiment analyzed separately - no averaging across experiments!")

if __name__ == "__main__":
    main()




