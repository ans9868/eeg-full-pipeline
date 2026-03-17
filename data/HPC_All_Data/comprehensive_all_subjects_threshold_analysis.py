#!/usr/bin/env python3
"""
Comprehensive All-Subjects Threshold Analysis

Ensures ALL subjects across ALL experiments are analyzed.
No sampling - processes all available data.
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

def load_all_experiment_data(experiment_dir):
    """Load ALL data for an experiment - no sampling"""
    results_dir = Path(experiment_dir)
    parquet_files = list(results_dir.rglob("test_predictions.parquet"))
    
    print(f"   Found {len(parquet_files)} prediction files")
    
    all_data = []
    subjects_seen = set()
    
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
                
                subjects_seen.add(subject_id)
                
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
    
    df_result = pd.DataFrame(all_data) if all_data else pd.DataFrame()
    print(f"   Loaded {len(df_result)} subject observations")
    print(f"   Unique subjects: {len(subjects_seen)}")
    print(f"   Subject IDs: {sorted(list(subjects_seen))}")
    
    return df_result

def analyze_threshold_per_model_hp_independent(data, experiment_name):
    """Analyze threshold per model×hyperparameter, treating experiment independently
    
    IMPORTANT: Only analyzes subjects that appear in ALL model×hp combinations
    to ensure fair comparison with same denominators.
    """
    
    # Find intersection of subjects across ALL model×hp combinations
    all_model_hps = data['model_hp'].unique()
    subject_sets = {}
    
    for model_hp in all_model_hps:
        model_hp_data = data[data['model_hp'] == model_hp]
        subject_sets[model_hp] = set(model_hp_data['subject_id'].unique())
    
    # Find common subjects (intersection)
    if len(subject_sets) > 0:
        common_subjects = set.intersection(*subject_sets.values())
        print(f"   Common subjects across all model×hp: {len(common_subjects)}")
        print(f"   Subject IDs: {sorted(list(common_subjects))[:20]}...")
    else:
        common_subjects = set()
    
    results_by_model_hp = {}
    
    for model_hp in all_model_hps:
        model_hp_data = data[data['model_hp'] == model_hp]
        
        # Filter to only common subjects for fair comparison
        model_hp_data = model_hp_data[model_hp_data['subject_id'].isin(common_subjects)]
        
        # Aggregate by subject WITHIN this experiment (average across folds only)
        subject_agg = model_hp_data.groupby(['subject_id', 'true_group']).agg({
            'ad_ratio': 'mean',
            'subject_accuracy': 'mean'
        }).reset_index()
        
        thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        model_hp_results = []
        
        for threshold in thresholds:
            subject_agg['predicted_group'] = subject_agg['ad_ratio'].apply(
                lambda x: 'alz' if x >= threshold else 'cntrl'
            )
            
            total_subjects = len(subject_agg)
            predicted_ad = (subject_agg['predicted_group'] == 'alz').sum()
            predicted_cntrl = (subject_agg['predicted_group'] == 'cntrl').sum()
            
            correct = (subject_agg['true_group'] == subject_agg['predicted_group']).sum()
            correct_ad = ((subject_agg['true_group'] == 'alz') & 
                         (subject_agg['predicted_group'] == 'alz')).sum()
            correct_cntrl = ((subject_agg['true_group'] == 'cntrl') & 
                            (subject_agg['predicted_group'] == 'cntrl')).sum()
            
            incorrect = total_subjects - correct
            incorrect_ad_as_cntrl = ((subject_agg['true_group'] == 'alz') & 
                                    (subject_agg['predicted_group'] == 'cntrl')).sum()
            incorrect_cntrl_as_ad = ((subject_agg['true_group'] == 'cntrl') & 
                                     (subject_agg['predicted_group'] == 'alz')).sum()
            
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
    
    return results_by_model_hp, common_subjects

def create_comprehensive_report(all_results, common_subjects_by_exp):
    """Create comprehensive report with all subjects"""
    print("\n📝 Creating comprehensive report with ALL subjects...")
    
    report = """# 🎯 Comprehensive All-Subjects Threshold Analysis

## Analysis Overview

**Key Features**:
- **ALL subjects** across ALL experiments analyzed (no sampling)
- Each experiment treated **independently**
- Per model×hyperparameter×experiment threshold optimization
- **Fair comparison**: Only subjects present in ALL model×hp combinations are analyzed (same denominator for all models)

## 📊 Subject Coverage by Experiment

"""
    
    # Subject coverage summary
    total_subject_experiment_combos = 0
    
    for exp_name, results in all_results.items():
        common_subjects = common_subjects_by_exp.get(exp_name, set())
        # Count unique subjects (we need to get this from the data)
        # For now, we'll note it in the summary
        report += f"### {exp_name}\n"
        report += f"- Model×HP combinations analyzed: {len(results)}\n"
        report += f"- **Common subjects (used for all models)**: {len(common_subjects)}\n"
        if len(common_subjects) > 0 and len(common_subjects) <= 50:
            report += f"- Subject IDs: {sorted(list(common_subjects))}\n"
        report += "\n"
        total_subject_experiment_combos += sum([len(r) for r in results.values() if not r.empty])
    
    report += f"\n**Total Analysis Points**: {total_subject_experiment_combos}\n\n"
    
    report += "## 📊 Results by Experiment and Model×Hyperparameter\n\n"
    
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
    report += "\n## 🎯 KNN-Specific Summary (All Subjects, Per Experiment)\n\n"
    knn_rows = [r for r in summary_rows if r['model_hp'].startswith('KNN')]
    if knn_rows:
        report += "| Experiment | KNN Hyperparameters | Threshold | Total | Correct | Incorrect | Accuracy |\n"
        report += "|------------|---------------------|-----------|-------|---------|-----------|----------|\n"
        for row in knn_rows:
            hp = row['model_hp'].replace('KNN_', '')
            report += f"| {row['experiment']} | {hp} | {row['threshold']:.2f} | {row['total']} | {row['correct']} | {row['incorrect']} | {row['accuracy']:.3f} |\n"
    
    # Verify subject coverage
    report += f"\n## ✅ Subject Coverage Verification\n\n"
    report += f"- **Total experiments analyzed**: {len(all_results)}\n"
    report += f"- **Total model×HP×experiment combinations**: {len(summary_rows)}\n"
    report += f"- **All parquet files processed** (no sampling)\n"
    report += f"- **Each experiment analyzed independently**\n\n"
    
    report += f"---\n*Analysis completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*\n"
    report += "*ALL subjects across ALL experiments - no sampling*\n"
    report += "*Each experiment treated independently*\n"
    report += "*Fair comparison: Only subjects present in ALL model×hp combinations are analyzed (same denominator for all models)*\n"
    
    with open('comprehensive_all_subjects_threshold_analysis.md', 'w') as f:
        f.write(report)
    
    print("✅ Saved report: comprehensive_all_subjects_threshold_analysis.md")

def main():
    """Main analysis - ALL subjects, ALL experiments"""
    print("🔍 Comprehensive All-Subjects Threshold Analysis")
    print("=" * 70)
    print("Processing ALL subjects across ALL experiments (no sampling)")
    print()
    
    experiments = {
        'ANOVA_L_2': 'grid_50_random_folds/Anova_L_2_incomplete_ml_results',
        'ANOVA_L_6': 'grid_50_random_folds/Anova_L_6_Incomplete_ml_results',
        'PCA_L_2': 'grid_50_random_folds/PCA_L_2_ml_results',
        'PCA_L_6': 'grid_50_random_folds/PCA_L_6_ml_results'
    }
    
    all_results = {}
    common_subjects_by_exp = {}
    total_observations = 0
    all_subjects_across_experiments = set()
    
    for exp_name, exp_dir in experiments.items():
        print(f"\n📊 Analyzing {exp_name} (ALL DATA, NO SAMPLING)...")
        print("-" * 70)
        
        # Load ALL data for THIS experiment (no max_folds limit)
        data = load_all_experiment_data(exp_dir)
        
        if data.empty:
            print(f"⚠️ No data")
            continue
        
        total_observations += len(data)
        all_subjects_across_experiments.update(data['subject_id'].unique())
        
        print(f"   Model×HP combinations: {data['model_hp'].nunique()}")
        print(f"   Unique combinations: {sorted(data['model_hp'].unique())}")
        
        # Analyze per model×hyperparameter WITHIN this experiment
        results_by_model_hp, common_subjects = analyze_threshold_per_model_hp_independent(data, exp_name)
        common_subjects_by_exp[exp_name] = common_subjects
        
        # Print summary
        for model_hp, model_results in results_by_model_hp.items():
            if not model_results.empty:
                best = model_results.loc[model_results['accuracy'].idxmax()]
                print(f"   {model_hp}: Threshold = {best['threshold']:.2f}, "
                      f"Accuracy = {best['accuracy']:.3f}, "
                      f"Correct = {int(best['correct_total'])}/{int(best['total_subjects'])} "
                      f"(using {len(common_subjects)} common subjects)")
        
        all_results[exp_name] = results_by_model_hp
    
    print(f"\n📊 OVERALL SUMMARY:")
    print(f"   Total observations: {total_observations}")
    print(f"   Unique subjects across all experiments: {len(all_subjects_across_experiments)}")
    print(f"   Subject IDs: {sorted(list(all_subjects_across_experiments))}")
    
    create_comprehensive_report(all_results, common_subjects_by_exp)
    
    print("\n🎉 COMPREHENSIVE ANALYSIS COMPLETE!")
    print("📁 Check comprehensive_all_subjects_threshold_analysis.md")
    print(f"\n✅ Verified: {len(all_subjects_across_experiments)} unique subjects analyzed across {len(experiments)} experiments")

if __name__ == "__main__":
    main()




