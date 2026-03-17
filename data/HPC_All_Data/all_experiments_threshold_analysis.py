#!/usr/bin/env python3
"""
Comprehensive Threshold Analysis for ALL Experiments in HPC_All_Data

Automatically discovers and analyzes all experiment directories.
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
            
            # Find fold and task info from path
            fold_info = "unknown"
            task_info = "unknown"
            for i, part in enumerate(path_parts):
                if 'fold' in part.lower() or 'task' in part.lower():
                    fold_info = part
                    if i + 1 < len(path_parts):
                        task_info = path_parts[i + 1]
                    break
            
            if 'task_' in task_info:
                model = task_info.replace('task_', '').split('_')[0]
            else:
                # Try to infer from path
                model = task_info.split('_')[0] if task_info != "unknown" else "unknown"
            
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
    if len(subjects_seen) <= 20:
        print(f"   Subject IDs: {sorted(list(subjects_seen))}")
    else:
        print(f"   Subject IDs: {sorted(list(subjects_seen))[:20]}... (showing first 20)")
    
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
        if len(common_subjects) <= 20:
            print(f"   Subject IDs: {sorted(list(common_subjects))}")
        else:
            print(f"   Subject IDs: {sorted(list(common_subjects))[:20]}... (showing first 20)")
    else:
        common_subjects = set()
    
    results_by_model_hp = {}
    
    for model_hp in all_model_hps:
        model_hp_data = data[data['model_hp'] == model_hp]
        
        # Filter to only common subjects for fair comparison
        model_hp_data = model_hp_data[model_hp_data['subject_id'].isin(common_subjects)]
        
        if len(model_hp_data) == 0:
            continue
        
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

def discover_experiments(base_dir):
    """Discover all experiment directories with ml_results"""
    base_path = Path(base_dir)
    experiment_dirs = []
    
    # Find all directories with ml_results in the name
    for ml_results_dir in base_path.rglob("*ml_results*"):
        if ml_results_dir.is_dir():
            # Check if it contains test_predictions.parquet files
            parquet_files = list(ml_results_dir.rglob("test_predictions.parquet"))
            if len(parquet_files) > 0:
                # Create experiment name from path
                rel_path = ml_results_dir.relative_to(base_path)
                exp_name = str(rel_path).replace('/', '_').replace('ml_results_grid_search', '').replace('ml_results_ax', '').replace('ml_results', '').strip('_')
                if not exp_name:
                    exp_name = rel_path.parent.name
                experiment_dirs.append((exp_name, str(ml_results_dir)))
    
    return experiment_dirs

def create_comprehensive_report(all_results, common_subjects_by_exp, fold_type_by_exp):
    """Create comprehensive report with uniform vs random comparisons"""
    print("\n📝 Creating comprehensive report with uniform vs random comparisons...")
    
    report = """# 🎯 Threshold Analysis: ANOVA/PCA L_6 and L_2 - Uniform vs Random Comparison

## Analysis Overview

**Key Features**:
- **L_6 and L_2 experiments** analyzed (ANOVA_L_6, ANOVA_L_2, PCA_L_6, PCA_L_2)
- **Comparison of Uniform (12-fold) vs Random (50-fold)** cross-validation strategies
- **Fair comparison on SAME test subjects**: Uniform experiments filtered to only include subjects present in random experiments
- **ALL subjects** across these experiments analyzed (no sampling)
- Each experiment treated **independently**
- Per model×hyperparameter×experiment threshold optimization
- **Fair comparison**: Only subjects present in ALL model×hp combinations AND in both uniform/random are analyzed

## 📊 Experiments Analyzed

"""
    
    # List all experiments with fold type
    for exp_name in sorted(all_results.keys()):
        common_subjects = common_subjects_by_exp.get(exp_name, set())
        fold_type = fold_type_by_exp.get(exp_name, "unknown")
        results = all_results[exp_name]
        report += f"- **{exp_name}** ({fold_type}): {len(results)} model×HP combinations, {len(common_subjects)} common subjects\n"
    
    # Create uniform vs random comparison
    report += "\n## 🔄 Uniform vs Random Comparison\n\n"
    
    # Group experiments by base name (extract L_6 or L_2 and feature type)
    experiment_groups = {}
    for exp_name in all_results.keys():
        exp_name_upper = exp_name.upper()
        fold_type = fold_type_by_exp.get(exp_name, "unknown")
        
        # Extract base identifier: ANOVA_L_6, ANOVA_L_2, PCA_L_6, PCA_L_2
        base_name = None
        if 'ANOVA_L_6' in exp_name_upper:
            base_name = 'ANOVA_L_6'
        elif 'ANOVA_L_2' in exp_name_upper:
            base_name = 'ANOVA_L_2'
        elif 'PCA_L_6' in exp_name_upper:
            base_name = 'PCA_L_6'
        elif 'PCA_L_2' in exp_name_upper:
            base_name = 'PCA_L_2'
        
        if base_name:
            if base_name not in experiment_groups:
                experiment_groups[base_name] = {}
            experiment_groups[base_name][fold_type] = exp_name
    
    # Create comparison tables
    for base_name in sorted(experiment_groups.keys()):
        group = experiment_groups[base_name]
        if 'uniform' in group and 'random' in group:
            uniform_exp = group['uniform']
            random_exp = group['random']
            
            uniform_results = all_results[uniform_exp]
            random_results = all_results[random_exp]
            uniform_subjects = common_subjects_by_exp.get(uniform_exp, set())
            random_subjects = common_subjects_by_exp.get(random_exp, set())
            intersection_subjects = uniform_subjects & random_subjects
            
            report += f"### {base_name.replace('_', ' ').title()}\n\n"
            report += f"**Comparison on SAME test subjects:**\n"
            report += f"- Uniform subjects: {len(uniform_subjects)}\n"
            report += f"- Random subjects: {len(random_subjects)}\n"
            report += f"- **Intersection (used for comparison): {len(intersection_subjects)} subjects**\n"
            if len(intersection_subjects) <= 50:
                report += f"- Subject IDs: {sorted(list(intersection_subjects))}\n"
            report += f"\n"
            report += f"| Model×Hyperparameters | Uniform Threshold | Uniform Accuracy | Uniform Subjects | Random Threshold | Random Accuracy | Random Subjects | Accuracy Difference |\n"
            report += f"|------------------------|-------------------|------------------|-----------------|------------------|-----------------|-----------------|---------------------|\n"
            
            # Get all unique model×hp combinations (normalize case)
            all_model_hps = set()
            uniform_model_hps_normalized = {}
            random_model_hps_normalized = {}
            
            # Normalize uniform model names
            for model_hp in uniform_results.keys():
                normalized = model_hp.upper().replace('ANOVA_', 'ANOVA_').replace('PCA_', 'PCA_')
                uniform_model_hps_normalized[normalized] = model_hp
                all_model_hps.add(normalized)
            
            # Normalize random model names
            for model_hp in random_results.keys():
                normalized = model_hp.upper().replace('ANOVA_', 'ANOVA_').replace('PCA_', 'PCA_')
                random_model_hps_normalized[normalized] = model_hp
                all_model_hps.add(normalized)
            
            for model_hp_normalized in sorted(all_model_hps):
                uniform_model_hp = uniform_model_hps_normalized.get(model_hp_normalized, None)
                random_model_hp = random_model_hps_normalized.get(model_hp_normalized, None)
                
                uniform_data = uniform_results.get(uniform_model_hp, pd.DataFrame()) if uniform_model_hp else pd.DataFrame()
                random_data = random_results.get(random_model_hp, pd.DataFrame()) if random_model_hp else pd.DataFrame()
                
                if not uniform_data.empty:
                    uniform_best = uniform_data.loc[uniform_data['accuracy'].idxmax()]
                    uniform_acc = uniform_best['accuracy']
                    uniform_thresh = uniform_best['threshold']
                    uniform_subj = int(uniform_best['total_subjects'])
                else:
                    uniform_acc = None
                    uniform_thresh = None
                    uniform_subj = None
                
                if not random_data.empty:
                    random_best = random_data.loc[random_data['accuracy'].idxmax()]
                    random_acc = random_best['accuracy']
                    random_thresh = random_best['threshold']
                    random_subj = int(random_best['total_subjects'])
                else:
                    random_acc = None
                    random_thresh = None
                    random_subj = None
                
                # Format the row - extract hyperparameters from normalized name
                if '_' in model_hp_normalized:
                    hp_display = model_hp_normalized.split('_', 1)[1]
                else:
                    hp_display = model_hp_normalized
                uniform_thresh_str = f"{uniform_thresh:.2f}" if uniform_thresh is not None else "N/A"
                uniform_acc_str = f"{uniform_acc:.3f}" if uniform_acc is not None else "N/A"
                uniform_subj_str = f"{uniform_subj}" if uniform_subj is not None else "N/A"
                random_thresh_str = f"{random_thresh:.2f}" if random_thresh is not None else "N/A"
                random_acc_str = f"{random_acc:.3f}" if random_acc is not None else "N/A"
                random_subj_str = f"{random_subj}" if random_subj is not None else "N/A"
                
                if uniform_acc is not None and random_acc is not None:
                    diff = random_acc - uniform_acc
                    diff_str = f"{diff:+.3f}" if diff != 0 else "0.000"
                    diff_marker = "🟢" if diff > 0.01 else "🔴" if diff < -0.01 else "⚪"
                else:
                    diff_str = "N/A"
                    diff_marker = ""
                
                report += f"| {hp_display} | {uniform_thresh_str} | {uniform_acc_str} | {uniform_subj_str} | {random_thresh_str} | {random_acc_str} | {random_subj_str} | {diff_marker} {diff_str} |\n"
            
            report += "\n"
    
    report += "\n## 📊 Detailed Results by Experiment and Model×Hyperparameter\n\n"
    
    summary_rows = []
    
    for exp_name in sorted(all_results.keys()):
        results = all_results[exp_name]
        common_subjects = common_subjects_by_exp.get(exp_name, set())
        fold_type = fold_type_by_exp.get(exp_name, "unknown")
        
        report += f"## {exp_name} ({fold_type})\n\n"
        report += f"**Fold Strategy**: {fold_type.upper()}\n"
        report += f"**Common subjects (used for all models)**: {len(common_subjects)}\n"
        if len(common_subjects) > 0 and len(common_subjects) <= 50:
            report += f"Subject IDs: {sorted(list(common_subjects))}\n"
        report += "\n"
        
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
                
                fold_type = fold_type_by_exp.get(exp_name, "unknown")
                summary_rows.append({
                    'experiment': exp_name,
                    'model_hp': model_hp,
                    'threshold': best['threshold'],
                    'total': int(best['total_subjects']),
                    'correct': int(best['correct_total']),
                    'incorrect': int(best['incorrect_total']),
                    'accuracy': best['accuracy'],
                    'fold_type': fold_type
                })
                
                report += "---\n\n"
    
    # Summary table
    report += "## 📋 Summary: Optimal Thresholds by Model×Hyperparameter×Experiment\n\n"
    report += "| Experiment | Fold Type | Model×Hyperparameters | Optimal Threshold | Total Subjects | Correct | Incorrect | Accuracy |\n"
    report += "|------------|-----------|------------------------|-------------------|----------------|---------|-----------|----------|\n"
    
    for row in summary_rows:
        fold_type = row.get('fold_type', 'unknown')
        report += f"| {row['experiment']} | {fold_type} | {row['model_hp']} | {row['threshold']:.2f} | {row['total']} | {row['correct']} | {row['incorrect']} | {row['accuracy']:.3f} |\n"
    
    # KNN-specific summary
    report += "\n## 🎯 KNN-Specific Summary (All Experiments)\n\n"
    knn_rows = [r for r in summary_rows if r['model_hp'].startswith('KNN')]
    if knn_rows:
        report += "| Experiment | KNN Hyperparameters | Threshold | Total | Correct | Incorrect | Accuracy |\n"
        report += "|------------|---------------------|-----------|-------|---------|-----------|----------|\n"
        for row in knn_rows:
            hp = row['model_hp'].replace('KNN_', '')
            report += f"| {row['experiment']} | {hp} | {row['threshold']:.2f} | {row['total']} | {row['correct']} | {row['incorrect']} | {row['accuracy']:.3f} |\n"
    
    # Verify subject coverage
    report += f"\n## ✅ Analysis Verification\n\n"
    report += f"- **Total experiments analyzed**: {len(all_results)}\n"
    report += f"- **Total model×HP×experiment combinations**: {len(summary_rows)}\n"
    report += f"- **All parquet files processed** (no sampling)\n"
    report += f"- **Each experiment analyzed independently**\n"
    report += f"- **Fair comparison**: Only subjects present in ALL model×hp combinations within each experiment\n\n"
    
    report += f"---\n*Analysis completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*\n"
    report += "*Only ANOVA/PCA L_6 and L_2 experiments analyzed*\n"
    report += "*ALL subjects across these experiments - no sampling*\n"
    report += "*Each experiment treated independently*\n"
    report += "*Fair comparison: Only subjects present in ALL model×hp combinations are analyzed (same denominator for all models)*\n"
    
    with open('anova_pca_L6_L2_threshold_analysis.md', 'w') as f:
        f.write(report)
    
    print("✅ Saved report: anova_pca_L6_L2_threshold_analysis.md")

def main():
    """Main analysis - Only ANOVA/PCA L_6 and L_2 experiments"""
    print("🔍 Threshold Analysis: ANOVA/PCA L_6 and L_2 Only")
    print("=" * 70)
    print("Analyzing only: ANOVA_L_6, ANOVA_L_2, PCA_L_6, PCA_L_2")
    print()
    
    base_dir = Path(__file__).parent
    all_experiments = discover_experiments(base_dir)
    
    # Filter to L_6 and L_2 experiments, including both uniform (12-fold) and random (50-fold) variants
    experiments = []
    for exp_name, exp_dir in all_experiments:
        exp_name_upper = exp_name.upper()
        exp_dir_str = str(exp_dir)
        
        # Determine if uniform (12-fold) or random (50-fold)
        fold_type = "random"
        if "grid_12_folds" in exp_dir_str:
            fold_type = "uniform"
        elif "grid_50_random_folds" in exp_dir_str:
            fold_type = "random"
        
        # Match patterns for L_6 and L_2
        is_anova_l6 = 'ANOVA_L_6' in exp_name_upper and ('RESOURCE_BOOSTED' in exp_name_upper or 'INCOMPLETE' in exp_name_upper)
        is_anova_l2 = 'ANOVA_L_2' in exp_name_upper and 'INCOMPLETE' in exp_name_upper
        is_pca_l6 = 'PCA_L_6' in exp_name_upper and ('C-3' in exp_name_upper or ('C-3' not in exp_name_upper and 'W' not in exp_name_upper))
        is_pca_l2 = 'PCA_L_2' in exp_name_upper and 'C-3' not in exp_name_upper and 'W' not in exp_name_upper
        
        if is_anova_l6 or is_anova_l2 or is_pca_l6 or is_pca_l2:
            # Create a label that includes fold type
            if fold_type == "uniform":
                label = f"{exp_name}_uniform"
            else:
                label = f"{exp_name}_random"
            experiments.append((label, exp_dir, fold_type))
    
    print(f"📁 Filtered to {len(experiments)} target experiments:\n")
    for exp_name, _, fold_type in experiments:
        print(f"   - {exp_name} ({fold_type})")
    print()
    
    all_results = {}
    common_subjects_by_exp = {}
    fold_type_by_exp = {}  # Track fold type for each experiment
    total_observations = 0
    all_subjects_across_experiments = set()
    
    # First pass: Load random experiments to get their subjects
    print("📋 Step 1: Identifying subjects in RANDOM experiments...")
    random_subjects_by_base = {}  # e.g., {'ANOVA_L_6': set([1,2,3...]), 'PCA_L_6': set([1,2,3...])}
    
    for exp_name, exp_dir, fold_type in sorted(experiments):
        if fold_type == "random":
            print(f"   Loading {exp_name} to identify subjects...")
            data = load_all_experiment_data(exp_dir)
            if not data.empty:
                # Extract base name (ANOVA_L_6, PCA_L_6, etc.)
                exp_name_upper = exp_name.upper()
                if 'ANOVA_L_6' in exp_name_upper:
                    base = 'ANOVA_L_6'
                elif 'ANOVA_L_2' in exp_name_upper:
                    base = 'ANOVA_L_2'
                elif 'PCA_L_6' in exp_name_upper:
                    base = 'PCA_L_6'
                elif 'PCA_L_2' in exp_name_upper:
                    base = 'PCA_L_2'
                else:
                    base = None
                
                if base:
                    # Find common subjects across all model×hp in this random experiment
                    all_model_hps = data['model_hp'].unique()
                    subject_sets = {}
                    for model_hp in all_model_hps:
                        model_hp_data = data[data['model_hp'] == model_hp]
                        subject_sets[model_hp] = set(model_hp_data['subject_id'].unique())
                    
                    if len(subject_sets) > 0:
                        common_subjects = set.intersection(*subject_sets.values())
                        random_subjects_by_base[base] = common_subjects
                        print(f"      {base}: {len(common_subjects)} common subjects")
                        if len(common_subjects) <= 30:
                            print(f"      Subject IDs: {sorted(list(common_subjects))}")
    
    print(f"\n📋 Step 2: Analyzing experiments (filtering uniform to random subjects)...\n")
    
    for exp_name, exp_dir, fold_type in sorted(experiments):
        print(f"\n📊 Analyzing {exp_name}...")
        print(f"   Directory: {exp_dir}")
        print("-" * 70)
        
        # Load ALL data for THIS experiment (no max_folds limit)
        data = load_all_experiment_data(exp_dir)
        
        if data.empty:
            print(f"⚠️ No data found, skipping")
            continue
        
        total_observations += len(data)
        all_subjects_across_experiments.update(data['subject_id'].unique())
        
        print(f"   Model×HP combinations: {data['model_hp'].nunique()}")
        if data['model_hp'].nunique() <= 15:
            print(f"   Unique combinations: {sorted(data['model_hp'].unique())}")
        
        # For uniform experiments: filter to only subjects that appear in random
        if fold_type == "uniform":
            exp_name_upper = exp_name.upper()
            if 'ANOVA_L_6' in exp_name_upper:
                base = 'ANOVA_L_6'
            elif 'ANOVA_L_2' in exp_name_upper:
                base = 'ANOVA_L_2'
            elif 'PCA_L_6' in exp_name_upper:
                base = 'PCA_L_6'
            elif 'PCA_L_2' in exp_name_upper:
                base = 'PCA_L_2'
            else:
                base = None
            
            if base and base in random_subjects_by_base:
                random_subjects = random_subjects_by_base[base]
                original_count = len(data['subject_id'].unique())
                data = data[data['subject_id'].isin(random_subjects)]
                filtered_count = len(data['subject_id'].unique())
                print(f"   ⚠️ Filtered uniform to random subjects: {original_count} → {filtered_count} subjects")
                print(f"   Using only subjects present in BOTH uniform and random: {sorted(list(random_subjects))}")
        
        # Analyze per model×hyperparameter WITHIN this experiment
        results_by_model_hp, common_subjects = analyze_threshold_per_model_hp_independent(data, exp_name)
        common_subjects_by_exp[exp_name] = common_subjects
        fold_type_by_exp[exp_name] = fold_type
        
        if len(results_by_model_hp) == 0:
            print(f"⚠️ No valid results after filtering to common subjects")
            continue
        
        # Print summary
        for model_hp, model_results in sorted(results_by_model_hp.items()):
            if not model_results.empty:
                best = model_results.loc[model_results['accuracy'].idxmax()]
                print(f"   {model_hp}: Threshold = {best['threshold']:.2f}, "
                      f"Accuracy = {best['accuracy']:.3f}, "
                      f"Correct = {int(best['correct_total'])}/{int(best['total_subjects'])} "
                      f"(using {len(common_subjects)} common subjects, {fold_type})")
        
        all_results[exp_name] = results_by_model_hp
    
    print(f"\n📊 OVERALL SUMMARY:")
    print(f"   Total experiments analyzed: {len(all_results)}")
    print(f"   Total observations: {total_observations}")
    print(f"   Unique subjects across all experiments: {len(all_subjects_across_experiments)}")
    
    create_comprehensive_report(all_results, common_subjects_by_exp, fold_type_by_exp)
    
    print("\n🎉 ANALYSIS COMPLETE!")
    print("📁 Check anova_pca_L6_L2_threshold_analysis.md")
    print(f"\n✅ Analyzed {len(all_results)} L_6/L_2 experiments with fair comparison (common subjects only)")

if __name__ == "__main__":
    main()




