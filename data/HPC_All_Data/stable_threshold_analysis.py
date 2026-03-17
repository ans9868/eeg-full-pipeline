#!/usr/bin/env python3
"""
Stable Threshold Analysis - Finding ONE threshold across all folds

Also clarifies threshold direction: should it lean towards AD or Control?
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
            
            # For each subject
            for subject_id in df['SubjectID'].unique():
                subject_df = df[df['SubjectID'] == subject_id]
                true_group = subject_df['Group'].iloc[0]
                true_label = subject_df['label'].iloc[0]  # 0.0 = AD, 1.0 = Control
                
                total_epochs = len(subject_df)
                ad_predictions = (subject_df['prediction'] == 0.0).sum()  # 0.0 = predicted AD
                ad_ratio = ad_predictions / total_epochs if total_epochs > 0 else 0
                
                all_data.append({
                    'subject_id': subject_id,
                    'fold': fold_info,
                    'model': model,
                    'true_group': true_group,
                    'true_label': true_label,  # 0.0 = AD, 1.0 = Control
                    'ad_ratio': ad_ratio,
                    'total_epochs': total_epochs
                })
        except Exception as e:
            continue
    
    return pd.DataFrame(all_data) if all_data else pd.DataFrame()

def analyze_threshold_direction(data):
    """Analyze threshold direction and AD/Control distribution"""
    print("\n🔍 ANALYZING THRESHOLD DIRECTION")
    print("=" * 60)
    
    # Check actual distribution
    total = len(data)
    ad_count = (data['true_group'] == 'alz').sum()
    cntrl_count = (data['true_group'] == 'cntrl').sum()
    
    print(f"True Distribution:")
    print(f"  AD: {ad_count} ({ad_count/total*100:.1f}%)")
    print(f"  Control: {cntrl_count} ({cntrl_count/total*100:.1f}%)")
    
    # Check AD ratios by true class
    ad_subjects = data[data['true_group'] == 'alz']
    cntrl_subjects = data[data['true_group'] == 'cntrl']
    
    print(f"\nAD Ratio Distribution:")
    print(f"  AD subjects - Mean AD ratio: {ad_subjects['ad_ratio'].mean():.3f}")
    print(f"  AD subjects - Median AD ratio: {ad_subjects['ad_ratio'].median():.3f}")
    print(f"  Control subjects - Mean AD ratio: {cntrl_subjects['ad_ratio'].mean():.3f}")
    print(f"  Control subjects - Median AD ratio: {cntrl_subjects['ad_ratio'].median():.3f}")
    
    # Check what threshold would give 60/40 distribution
    all_ad_ratios = data['ad_ratio'].sort_values()
    target_ad_pct = ad_count / total * 100
    
    # Find threshold that gives similar distribution
    threshold_idx = int(len(all_ad_ratios) * (1 - target_ad_pct/100))
    threshold_for_dist = all_ad_ratios.iloc[threshold_idx] if threshold_idx < len(all_ad_ratios) else 0.5
    
    print(f"\nThreshold Analysis:")
    print(f"  To match {target_ad_pct:.1f}% AD distribution, threshold should be around: {threshold_for_dist:.2f}")
    
    return {
        'ad_pct': ad_count / total * 100,
        'ad_mean_ratio': ad_subjects['ad_ratio'].mean(),
        'cntrl_mean_ratio': cntrl_subjects['ad_ratio'].mean(),
        'threshold_for_dist': threshold_for_dist
    }

def find_stable_threshold(data, model_filter=None):
    """Find ONE stable threshold across all folds"""
    print("\n🎯 FINDING STABLE THRESHOLD ACROSS ALL FOLDS")
    print("=" * 60)
    
    # Filter by model if specified
    if model_filter:
        data = data[data['model'] == model_filter]
        print(f"Filtering to {model_filter} model only")
    
    # Aggregate by subject (average across all folds/models)
    subject_agg = data.groupby(['subject_id', 'true_group']).agg({
        'ad_ratio': 'mean'
    }).reset_index()
    
    subject_agg['true_label'] = (subject_agg['true_group'] == 'cntrl').astype(int)
    
    print(f"Analyzing {len(subject_agg)} unique subjects")
    
    thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
    results = []
    
    for threshold in thresholds:
        # Classification: if ad_ratio >= threshold, predict AD (0), else Control (1)
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
            
            # Calculate predicted distribution
            predicted_ad = (y_pred == 0).sum()
            predicted_ad_pct = predicted_ad / len(y_pred) * 100
            
            results.append({
                'threshold': threshold,
                'accuracy': accuracy,
                'balanced_accuracy': balanced_acc,
                'ad_recall': ad_recall,
                'cntrl_recall': cntrl_recall,
                'predicted_ad_pct': predicted_ad_pct,
                'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp
            })
    
    results_df = pd.DataFrame(results)
    
    # Find best by balanced accuracy
    best = results_df.loc[results_df['balanced_accuracy'].idxmax()]
    
    print(f"\nResults:")
    print(f"  Best threshold (balanced accuracy): {best['threshold']:.2f}")
    print(f"  Accuracy: {best['accuracy']:.3f}")
    print(f"  Balanced accuracy: {best['balanced_accuracy']:.3f}")
    print(f"  AD Recall: {best['ad_recall']:.3f}")
    print(f"  Control Recall: {best['cntrl_recall']:.3f}")
    print(f"  Predicted AD %: {best['predicted_ad_pct']:.1f}%")
    
    return results_df, best, subject_agg

def analyze_all_experiments_stable():
    """Analyze all experiments with stable threshold"""
    print("🔍 STABLE THRESHOLD ANALYSIS - ONE Threshold Across All Folds")
    print("=" * 70)
    
    experiments = {
        'ANOVA_L_2': 'grid_50_random_folds/Anova_L_2_incomplete_ml_results',
        'ANOVA_L_6': 'grid_50_random_folds/Anova_L_6_Incomplete_ml_results',
        'PCA_L_2': 'grid_50_random_folds/PCA_L_2_ml_results',
        'PCA_L_6': 'grid_50_random_folds/PCA_L_6_ml_results'
    }
    
    all_results = {}
    
    for exp_name, exp_dir in experiments.items():
        print(f"\n{'='*70}")
        print(f"📊 {exp_name}")
        print(f"{'='*70}")
        
        data = load_all_predictions(exp_dir, max_folds=50)
        
        if data.empty:
            print(f"⚠️ No data")
            continue
        
        # Analyze distribution
        dist_info = analyze_threshold_direction(data)
        
        # Find stable threshold (all models)
        results_df, best, subject_agg = find_stable_threshold(data, model_filter=None)
        
        # Find stable threshold for KNN only
        print(f"\n🎯 KNN-Only Analysis:")
        knn_results_df, knn_best, knn_subject_agg = find_stable_threshold(data, model_filter='KNN')
        
        all_results[exp_name] = {
            'data': data,
            'dist_info': dist_info,
            'results_df': results_df,
            'best': best,
            'subject_agg': subject_agg,
            'knn_results_df': knn_results_df,
            'knn_best': knn_best,
            'knn_subject_agg': knn_subject_agg
        }
    
    return all_results

def create_stable_threshold_report(all_results):
    """Create report with stable thresholds"""
    print("\n📝 Creating stable threshold report...")
    
    report = """# 🎯 Stable Threshold Analysis - ONE Threshold Across All Folds

## Analysis Overview

This analysis finds **ONE stable threshold** that works across all folds, rather than per-fold thresholds.
It also clarifies the threshold direction and why thresholds might seem counterintuitive.

## 📊 Results by Experiment

"""
    
    for exp_name, results in all_results.items():
        dist_info = results['dist_info']
        best = results['best']
        knn_best = results['knn_best']
        
        report += f"### {exp_name}\n\n"
        report += f"**Data Distribution:**\n"
        report += f"- True AD %: {dist_info['ad_pct']:.1f}%\n"
        report += f"- True Control %: {100-dist_info['ad_pct']:.1f}%\n"
        report += f"- AD subjects mean AD ratio: {dist_info['ad_mean_ratio']:.3f}\n"
        report += f"- Control subjects mean AD ratio: {dist_info['cntrl_mean_ratio']:.3f}\n\n"
        
        report += f"**Stable Threshold (All Models):**\n"
        report += f"- Optimal threshold: **{best['threshold']:.2f}**\n"
        report += f"- Accuracy: {best['accuracy']:.3f}\n"
        report += f"- Balanced accuracy: {best['balanced_accuracy']:.3f}\n"
        report += f"- AD Recall: {best['ad_recall']:.3f}\n"
        report += f"- Control Recall: {best['cntrl_recall']:.3f}\n"
        report += f"- Predicted AD %: {best['predicted_ad_pct']:.1f}%\n\n"
        
        report += f"**🎯 KNN-Only Stable Threshold:**\n"
        report += f"- Optimal threshold: **{knn_best['threshold']:.2f}**\n"
        report += f"- Accuracy: {knn_best['accuracy']:.3f}\n"
        report += f"- Balanced accuracy: {knn_best['balanced_accuracy']:.3f}\n"
        report += f"- AD Recall: {knn_best['ad_recall']:.3f}\n"
        report += f"- Control Recall: {knn_best['cntrl_recall']:.3f}\n"
        report += f"- Predicted AD %: {knn_best['predicted_ad_pct']:.1f}%\n\n"
        
        # Threshold direction explanation
        if dist_info['ad_pct'] > 50:
            report += f"**Threshold Direction Analysis:**\n"
            report += f"- Since {dist_info['ad_pct']:.1f}% of data is AD, you'd expect threshold around {dist_info['threshold_for_dist']:.2f} to match distribution\n"
            if best['threshold'] < 0.5:
                report += f"- ⚠️ **Note**: Optimal threshold ({best['threshold']:.2f}) is LOWER than 0.5\n"
                report += f"  This means: Need LESS AD evidence to classify as AD (more lenient)\n"
                report += f"  This suggests: Models are predicting AD more often than Control\n"
            else:
                report += f"- ✅ Optimal threshold ({best['threshold']:.2f}) is HIGHER than 0.5\n"
                report += f"  This means: Need MORE AD evidence to classify as AD (more strict)\n"
            report += "\n"
        
        report += "---\n\n"
    
    report += """## 🎯 Key Findings

### Threshold Direction Clarification

**How thresholds work:**
- **Lower threshold (e.g., 0.3)**: Easier to classify as AD → More AD classifications
- **Higher threshold (e.g., 0.7)**: Harder to classify as AD → More Control classifications

**If training data is 60% AD / 40% Control:**
- You'd expect AD subjects to have higher AD ratios (more AD predictions)
- You'd expect Control subjects to have lower AD ratios (fewer AD predictions)
- **Optimal threshold should be around 0.5-0.6** to match distribution

**Why low thresholds (0.3-0.4) might be optimal:**
- If models are **over-predicting AD** (predicting AD too often)
- Then AD ratios are inflated for both AD and Control subjects
- Lower threshold compensates for this over-prediction
- OR: Models are actually good at distinguishing, but threshold needs adjustment

### Stable Threshold Recommendations

**Universal (All Models):**
- Use experiment-specific thresholds from the table above
- These work across all folds and models

**KNN-Specific:**
- Use KNN-specific thresholds for best KNN performance
- These are optimized specifically for KNN's prediction patterns

## 🔧 Implementation

```python
# Stable thresholds by experiment
stable_thresholds = {
    'ANOVA_L_2': <threshold>,
    'ANOVA_L_6': <threshold>,
    'PCA_L_2': <threshold>,
    'PCA_L_6': <threshold>
}

# KNN-specific thresholds
knn_thresholds = {
    'ANOVA_L_2': <threshold>,
    'ANOVA_L_6': <threshold>,
    'PCA_L_2': <threshold>,
    'PCA_L_6': <threshold>
}

# Use stable threshold
threshold = stable_thresholds[experiment_name]  # or knn_thresholds for KNN
if ad_ratio >= threshold:
    subject_class = "AD"
else:
    subject_class = "Control"
```

---
*Analysis completed: Stable threshold across all folds*
"""
    
    with open('stable_threshold_analysis.md', 'w') as f:
        f.write(report)
    
    print("✅ Saved report: stable_threshold_analysis.md")

def main():
    all_results = analyze_all_experiments_stable()
    
    if not all_results:
        print("❌ No results")
        return
    
    create_stable_threshold_report(all_results)
    
    print("\n🎉 STABLE THRESHOLD ANALYSIS COMPLETE!")
    print("📁 Check stable_threshold_analysis.md")

if __name__ == "__main__":
    main()




