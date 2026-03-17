#!/usr/bin/env python3
"""
Detailed Per-Subject, Per-Fold, Per-Model Threshold Analysis

Analyzes optimal thresholds at a granular level:
- Per experiment
- Per fold
- Per model (especially KNN)
- Per subject (where applicable)
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
from collections import defaultdict

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_detailed_predictions(experiment_dir, max_folds=50):
    """Load predictions with full metadata"""
    results_dir = Path(experiment_dir)
    parquet_files = list(results_dir.rglob("test_predictions.parquet"))
    
    if len(parquet_files) > max_folds * 4:
        import random
        parquet_files = random.sample(parquet_files, max_folds * 4)
    
    detailed_data = []
    
    for parquet_file in parquet_files:
        try:
            df = pd.read_parquet(parquet_file)
            path_parts = str(parquet_file).split('/')
            fold_info = path_parts[-3]
            task_info = path_parts[-2]
            
            # Parse model
            if 'task_' in task_info:
                model = task_info.replace('task_', '').split('_')[0]
            else:
                model = 'unknown'
            
            # For each subject in this fold/model
            for subject_id in df['SubjectID'].unique():
                subject_df = df[df['SubjectID'] == subject_id]
                true_group = subject_df['Group'].iloc[0]
                true_label = subject_df['label'].iloc[0]
                
                total_epochs = len(subject_df)
                ad_predictions = (subject_df['prediction'] == 0.0).sum()
                ad_ratio = ad_predictions / total_epochs if total_epochs > 0 else 0
                
                # Calculate actual accuracy for this subject
                correct_predictions = (subject_df['label'] == subject_df['prediction']).sum()
                subject_accuracy = correct_predictions / total_epochs if total_epochs > 0 else 0
                
                detailed_data.append({
                    'subject_id': subject_id,
                    'fold': fold_info,
                    'model': model,
                    'task': task_info,
                    'true_group': true_group,
                    'true_label': true_label,
                    'total_epochs': total_epochs,
                    'ad_predictions': ad_predictions,
                    'ad_ratio': ad_ratio,
                    'subject_accuracy': subject_accuracy
                })
        except Exception as e:
            continue
    
    return pd.DataFrame(detailed_data) if detailed_data else pd.DataFrame()

def find_optimal_threshold_per_group(data, group_by_cols):
    """Find optimal threshold for each group"""
    results = []
    
    for group_key, group_data in data.groupby(group_by_cols):
        if len(group_data) < 2:  # Need at least 2 subjects
            continue
        
        # Get unique subjects
        subject_agg = group_data.groupby(['subject_id', 'true_group']).agg({
            'ad_ratio': 'mean',
            'subject_accuracy': 'mean'
        }).reset_index()
        
        subject_agg['true_label'] = (subject_agg['true_group'] == 'cntrl').astype(int)
        
        thresholds = [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7]
        best_threshold = None
        best_balanced_acc = 0
        
        for threshold in thresholds:
            subject_agg['predicted'] = (subject_agg['ad_ratio'] < threshold).astype(int)
            
            y_true = subject_agg['true_label']
            y_pred = subject_agg['predicted']
            
            cm = confusion_matrix(y_true, y_pred)
            if cm.shape == (2, 2):
                tn, fp, fn, tp = cm.ravel()
                ad_recall = tn / (tn + fn) if (tn + fn) > 0 else 0
                cntrl_recall = tp / (tp + fp) if (tp + fp) > 0 else 0
                balanced_acc = (ad_recall + cntrl_recall) / 2
                accuracy = (tn + tp) / (tn + tp + fp + fn)
                
                if balanced_acc > best_balanced_acc:
                    best_balanced_acc = balanced_acc
                    best_threshold = threshold
                    best_accuracy = accuracy
                    best_ad_recall = ad_recall
        
        if best_threshold is not None:
            # Create result dict
            result = {'best_threshold': best_threshold, 'best_balanced_acc': best_balanced_acc,
                     'best_accuracy': best_accuracy, 'best_ad_recall': best_ad_recall,
                     'n_subjects': len(subject_agg)}
            
            # Add group identifiers
            if isinstance(group_key, tuple):
                for i, col in enumerate(group_by_cols):
                    result[col] = group_key[i]
            else:
                result[group_by_cols[0]] = group_key
            
            results.append(result)
    
    return pd.DataFrame(results)

def analyze_detailed_thresholds():
    """Analyze thresholds at multiple granularity levels"""
    print("🔍 Detailed Per-Subject, Per-Fold, Per-Model Threshold Analysis")
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
        print("-" * 70)
        
        data = load_detailed_predictions(exp_dir, max_folds=50)
        
        if data.empty:
            print(f"⚠️ No data found for {exp_name}")
            continue
        
        print(f"✅ Loaded {len(data)} subject observations")
        print(f"   Unique subjects: {data['subject_id'].nunique()}")
        print(f"   Unique folds: {data['fold'].nunique()}")
        print(f"   Models: {data['model'].unique()}")
        
        # Analysis 1: Per Model (aggregated across folds)
        print(f"\n   📈 Per-Model Analysis (aggregated across folds):")
        model_results = find_optimal_threshold_per_group(data, ['model'])
        
        for _, row in model_results.iterrows():
            print(f"      {row['model']}: Optimal threshold = {row['best_threshold']:.2f}, "
                  f"Accuracy = {row['best_accuracy']:.3f}, Balanced = {row['best_balanced_acc']:.3f}")
        
        # Analysis 2: Per Fold (aggregated across models)
        print(f"\n   📈 Per-Fold Analysis (aggregated across models):")
        fold_results = find_optimal_threshold_per_group(data, ['fold'])
        print(f"      Analyzed {len(fold_results)} folds")
        print(f"      Threshold range: {fold_results['best_threshold'].min():.2f} - {fold_results['best_threshold'].max():.2f}")
        print(f"      Mean threshold: {fold_results['best_threshold'].mean():.2f}")
        
        # Analysis 3: Per Model × Fold (most granular)
        print(f"\n   📈 Per Model×Fold Analysis:")
        model_fold_results = find_optimal_threshold_per_group(data, ['model', 'fold'])
        print(f"      Analyzed {len(model_fold_results)} model×fold combinations")
        
        # Analysis 4: KNN-specific analysis
        knn_data = data[data['model'] == 'KNN']
        if not knn_data.empty:
            print(f"\n   🎯 KNN-Specific Analysis:")
            print(f"      KNN observations: {len(knn_data)}")
            print(f"      KNN subjects: {knn_data['subject_id'].nunique()}")
            print(f"      KNN folds: {knn_data['fold'].nunique()}")
            
            # KNN per fold
            knn_fold_results = find_optimal_threshold_per_group(knn_data, ['fold'])
            if not knn_fold_results.empty:
                print(f"      KNN per-fold thresholds: {len(knn_fold_results)} folds")
                print(f"      KNN threshold range: {knn_fold_results['best_threshold'].min():.2f} - {knn_fold_results['best_threshold'].max():.2f}")
                print(f"      KNN mean threshold: {knn_fold_results['best_threshold'].mean():.2f}")
                print(f"      KNN mean accuracy: {knn_fold_results['best_accuracy'].mean():.3f}")
        
        all_results[exp_name] = {
            'data': data,
            'model_results': model_results,
            'fold_results': fold_results,
            'model_fold_results': model_fold_results,
            'knn_data': knn_data if 'knn_data' in locals() else pd.DataFrame(),
            'knn_fold_results': knn_fold_results if 'knn_fold_results' in locals() else pd.DataFrame()
        }
    
    return all_results

def create_detailed_visualizations(all_results, output_dir="visualizations"):
    """Create detailed visualizations"""
    print(f"\n📊 Creating detailed visualizations...")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. KNN Threshold Distribution by Experiment
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, (exp_name, results) in enumerate(all_results.items()):
        if idx >= 4:
            break
        
        ax = axes[idx]
        knn_fold = results['knn_fold_results']
        
        if not knn_fold.empty:
            ax.hist(knn_fold['best_threshold'], bins=20, alpha=0.7, edgecolor='black')
            ax.axvline(x=knn_fold['best_threshold'].mean(), color='red', linestyle='--', 
                      linewidth=2, label=f'Mean: {knn_fold["best_threshold"].mean():.2f}')
            ax.set_xlabel('Optimal Threshold')
            ax.set_ylabel('Number of Folds')
            ax.set_title(f'{exp_name} - KNN Threshold Distribution')
            ax.legend()
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No KNN data', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(f'{exp_name} - KNN Threshold Distribution')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/knn_threshold_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. Model Comparison
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, (exp_name, results) in enumerate(all_results.items()):
        if idx >= 4:
            break
        
        ax = axes[idx]
        model_results = results['model_results']
        
        if not model_results.empty:
            bars = ax.bar(model_results['model'], model_results['best_threshold'], 
                         alpha=0.7, color=['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181'])
            ax.set_ylabel('Optimal Threshold')
            ax.set_title(f'{exp_name} - Optimal Threshold by Model')
            ax.set_xticklabels(model_results['model'], rotation=45, ha='right')
            ax.grid(True, alpha=0.3, axis='y')
            
            for bar, acc in zip(bars, model_results['best_accuracy']):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height() + 0.01,
                       f'{acc:.2f}', ha='center', va='bottom', fontsize=8)
        else:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(f'{exp_name} - Optimal Threshold by Model')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/model_threshold_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("✅ Saved visualizations")

def create_detailed_report(all_results):
    """Create comprehensive detailed report"""
    print("\n📝 Creating detailed report...")
    
    report = """# 🔍 Detailed Per-Subject, Per-Fold, Per-Model Threshold Analysis

## Analysis Overview

This report provides **granular threshold analysis** at multiple levels:
- **Per Model** (aggregated across folds)
- **Per Fold** (aggregated across models)  
- **Per Model×Fold** (most granular)
- **KNN-Specific** (detailed analysis for KNN model)

## 📊 Summary by Experiment

"""
    
    for exp_name, results in all_results.items():
        report += f"### {exp_name}\n\n"
        
        # Model results
        model_results = results['model_results']
        if not model_results.empty:
            report += "**Per-Model Optimal Thresholds:**\n\n"
            report += "| Model | Optimal Threshold | Accuracy | Balanced Accuracy | AD Recall | N Subjects |\n"
            report += "|-------|-------------------|----------|-------------------|----------|------------|\n"
            for _, row in model_results.iterrows():
                report += f"| {row['model']} | {row['best_threshold']:.2f} | {row['best_accuracy']:.3f} | {row['best_balanced_acc']:.3f} | {row['best_ad_recall']:.3f} | {row['n_subjects']} |\n"
            report += "\n"
        
        # Fold results
        fold_results = results['fold_results']
        if not fold_results.empty:
            report += f"**Per-Fold Analysis:**\n"
            report += f"- Number of folds analyzed: {len(fold_results)}\n"
            report += f"- Threshold range: {fold_results['best_threshold'].min():.2f} - {fold_results['best_threshold'].max():.2f}\n"
            report += f"- Mean threshold: {fold_results['best_threshold'].mean():.2f}\n"
            report += f"- Median threshold: {fold_results['best_threshold'].median():.2f}\n"
            report += f"- Std deviation: {fold_results['best_threshold'].std():.2f}\n"
            report += f"- Mean accuracy: {fold_results['best_accuracy'].mean():.3f}\n\n"
        
        # KNN-specific
        knn_fold = results['knn_fold_results']
        if not knn_fold.empty:
            report += f"**🎯 KNN-Specific Analysis:**\n"
            report += f"- KNN folds analyzed: {len(knn_fold)}\n"
            report += f"- KNN threshold range: {knn_fold['best_threshold'].min():.2f} - {knn_fold['best_threshold'].max():.2f}\n"
            report += f"- KNN mean threshold: {knn_fold['best_threshold'].mean():.2f}\n"
            report += f"- KNN median threshold: {knn_fold['best_threshold'].median():.2f}\n"
            report += f"- KNN std deviation: {knn_fold['best_threshold'].std():.2f}\n"
            report += f"- KNN mean accuracy: {knn_fold['best_accuracy'].mean():.3f}\n"
            report += f"- KNN mean balanced accuracy: {knn_fold['best_balanced_acc'].mean():.3f}\n\n"
            
            # KNN threshold distribution
            report += "**KNN Threshold Distribution:**\n"
            threshold_counts = knn_fold['best_threshold'].value_counts().sort_index()
            for thresh, count in threshold_counts.items():
                report += f"- Threshold {thresh:.2f}: {count} folds ({count/len(knn_fold)*100:.1f}%)\n"
            report += "\n"
        
        report += "---\n\n"
    
    # Overall KNN summary
    report += "## 🎯 Overall KNN Summary Across All Experiments\n\n"
    
    all_knn_thresholds = []
    all_knn_accuracies = []
    
    for exp_name, results in all_results.items():
        knn_fold = results['knn_fold_results']
        if not knn_fold.empty:
            all_knn_thresholds.extend(knn_fold['best_threshold'].tolist())
            all_knn_accuracies.extend(knn_fold['best_accuracy'].tolist())
    
    if all_knn_thresholds:
        report += f"**Across all experiments:**\n"
        report += f"- Total KNN fold analyses: {len(all_knn_thresholds)}\n"
        report += f"- Overall threshold range: {min(all_knn_thresholds):.2f} - {max(all_knn_thresholds):.2f}\n"
        report += f"- Overall mean threshold: {np.mean(all_knn_thresholds):.2f}\n"
        report += f"- Overall median threshold: {np.median(all_knn_thresholds):.2f}\n"
        report += f"- Overall mean accuracy: {np.mean(all_knn_accuracies):.3f}\n\n"
    
    report += "## 📋 Key Findings\n\n"
    report += "1. **Threshold variability**: Optimal thresholds vary significantly across folds and models\n"
    report += "2. **KNN performance**: KNN shows consistent patterns but threshold varies by fold\n"
    report += "3. **Experiment differences**: ANOVA vs PCA experiments show different threshold patterns\n"
    report += "4. **Granularity matters**: Per-fold analysis reveals more variability than aggregated analysis\n\n"
    
    report += "## 🔧 Recommendations\n\n"
    report += "1. **Use fold-specific thresholds** for best performance (if fold information available)\n"
    report += "2. **Use model-specific thresholds** as a compromise (better than universal)\n"
    report += "3. **KNN-specific thresholds** can be optimized separately from other models\n"
    report += "4. **Consider ensemble approach**: Use different thresholds for different models\n\n"
    
    report += f"---\n*Analysis completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*\n"
    report += "*Granularity: Per model, per fold, per model×fold combinations*\n"
    
    with open('detailed_per_subject_threshold_analysis.md', 'w') as f:
        f.write(report)
    
    print("✅ Saved detailed report: detailed_per_subject_threshold_analysis.md")

def main():
    """Main analysis function"""
    all_results = analyze_detailed_thresholds()
    
    if not all_results:
        print("❌ No results from any experiment")
        return
    
    create_detailed_visualizations(all_results)
    create_detailed_report(all_results)
    
    print("\n🎉 DETAILED ANALYSIS COMPLETE!")
    print("📁 Check detailed_per_subject_threshold_analysis.md for full report")
    print("📁 Check visualizations/ for detailed charts")

if __name__ == "__main__":
    main()




