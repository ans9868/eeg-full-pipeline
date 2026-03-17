#!/usr/bin/env python3
"""
Subject-Level Classification Threshold Analysis

Analyzes optimal threshold for classifying subjects as AD vs Control based on
the percentage of their epochs predicted as AD.

Current: If >50% epochs are AD, classify subject as AD
Question: Should this match the 60/40 training distribution?
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
    print(f"🔍 Loading subject-level predictions from {experiment_dir}")
    
    results_dir = Path(experiment_dir)
    parquet_files = list(results_dir.rglob("test_predictions.parquet"))
    
    print(f"📊 Found {len(parquet_files)} prediction files")
    
    if len(parquet_files) > max_folds * 4:
        import random
        parquet_files = random.sample(parquet_files, max_folds * 4)
        print(f"📊 Sampling {len(parquet_files)} files")
    
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
                true_label = subject_df['label'].iloc[0]
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
    
    if not subject_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(subject_data)
    print(f"✅ Loaded {len(df)} subject observations")
    return df

def test_thresholds(data):
    """Test different thresholds for subject classification"""
    print("\n🎯 TESTING THRESHOLDS")
    print("=" * 50)
    
    # Aggregate by subject (average across folds/models)
    subject_agg = data.groupby(['subject_id', 'true_group']).agg({
        'ad_ratio': 'mean'
    }).reset_index()
    
    subject_agg['true_label'] = (subject_agg['true_group'] == 'cntrl').astype(int)
    
    print(f"📊 {len(subject_agg)} unique subjects")
    
    thresholds = [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7]
    results = []
    
    for threshold in thresholds:
        # If ad_ratio >= threshold, predict AD (0), else Control (1)
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
    
    results_df = pd.DataFrame(results)
    
    print("\nThreshold Performance:")
    print("-" * 80)
    print(f"{'Threshold':<10} {'Accuracy':<10} {'Balanced':<10} {'AD Recall':<12} {'Pred AD%':<10}")
    print("-" * 80)
    for _, row in results_df.iterrows():
        print(f"{row['threshold']:<10.2f} {row['accuracy']:<10.3f} {row['balanced_accuracy']:<10.3f} "
              f"{row['ad_recall']:<12.3f} {row['predicted_ad_pct']:<10.1f}")
    
    return results_df, subject_agg

def analyze_distribution(data):
    """Analyze training distribution"""
    print("\n📊 DISTRIBUTION ANALYSIS")
    print("=" * 50)
    
    total = len(data)
    ad_count = (data['true_group'] == 'alz').sum()
    ad_pct = ad_count / total * 100
    
    print(f"AD: {ad_count:,} ({ad_pct:.1f}%)")
    print(f"Control: {total - ad_count:,} ({100 - ad_pct:.1f}%)")
    
    return ad_pct

def create_visualizations(results_df, subject_agg, true_ad_pct, output_dir="visualizations"):
    """Create visualizations"""
    print(f"\n📊 Creating visualizations...")
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Performance vs Threshold
    ax = axes[0, 0]
    ax.plot(results_df['threshold'], results_df['accuracy'], 'o-', label='Accuracy', linewidth=2)
    ax.plot(results_df['threshold'], results_df['balanced_accuracy'], 's-', label='Balanced', linewidth=2)
    ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='Current (0.5)')
    ax.axvline(x=true_ad_pct/100, color='green', linestyle='--', alpha=0.5, label=f'Training ({true_ad_pct:.0f}%)')
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Performance')
    ax.set_title('Performance vs Threshold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Predicted Distribution
    ax = axes[0, 1]
    ax.plot(results_df['threshold'], results_df['predicted_ad_pct'], 'o-', linewidth=2)
    ax.axhline(y=true_ad_pct, color='green', linestyle='--', label=f'True ({true_ad_pct:.1f}%)')
    ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Predicted AD %')
    ax.set_title('Predicted Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Recall by Class
    ax = axes[1, 0]
    ax.plot(results_df['threshold'], results_df['ad_recall'], 'o-', label='AD Recall', linewidth=2)
    ax.plot(results_df['threshold'], results_df['cntrl_recall'], 's-', label='Control Recall', linewidth=2)
    ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Recall')
    ax.set_title('Recall by Class')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Subject AD Ratio Distribution
    ax = axes[1, 1]
    ad_subjects = subject_agg[subject_agg['true_group'] == 'alz']['ad_ratio']
    cntrl_subjects = subject_agg[subject_agg['true_group'] == 'cntrl']['ad_ratio']
    ax.hist(ad_subjects, bins=30, alpha=0.7, label='True AD', color='#FF6B6B', density=True)
    ax.hist(cntrl_subjects, bins=30, alpha=0.7, label='True Control', color='#4ECDC4', density=True)
    ax.axvline(x=0.5, color='red', linestyle='--', linewidth=2, label='Current (0.5)')
    ax.set_xlabel('AD Prediction Ratio')
    ax.set_ylabel('Density')
    ax.set_title('Subject AD Ratio Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/subject_threshold_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved visualization")

def main():
    print("🧠 Subject-Level Threshold Analysis")
    print("=" * 60)
    
    experiment_dir = "grid_50_random_folds/Anova_L_2_incomplete_ml_results"
    data = load_subject_predictions(experiment_dir, max_folds=50)
    
    if data.empty:
        print("❌ No data")
        return
    
    true_ad_pct = analyze_distribution(data)
    results_df, subject_agg = test_thresholds(data)
    
    # Find best threshold
    best = results_df.loc[results_df['balanced_accuracy'].idxmax()]
    
    create_visualizations(results_df, subject_agg, true_ad_pct)
    
    # Create report
    summary = f"""# Subject-Level Classification Threshold Analysis

## Question
Should the 0.5 threshold be adjusted to match 60/40 training distribution?

## Findings

**Training Distribution**: {true_ad_pct:.1f}% AD, {100-true_ad_pct:.1f}% Control

**Optimal Threshold**: {best['threshold']:.2f}
- Accuracy: {best['accuracy']:.3f}
- Balanced Accuracy: {best['balanced_accuracy']:.3f}
- AD Recall: {best['ad_recall']:.3f}
- Predicted AD%: {best['predicted_ad_pct']:.1f}%

**Current (0.5) Performance**:
- Accuracy: {results_df[results_df['threshold']==0.5]['accuracy'].iloc[0]:.3f}
- Balanced: {results_df[results_df['threshold']==0.5]['balanced_accuracy'].iloc[0]:.3f}

## Recommendation

{'**YES - Adjust threshold to ' + str(best['threshold']) + '**' if abs(best['threshold'] - 0.5) > 0.05 else '**0.5 threshold is close to optimal**'}

---
*Analysis completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    with open('subject_threshold_report.md', 'w') as f:
        f.write(summary)
    
    print(f"\n🎉 COMPLETE!")
    print(f"📊 Optimal threshold: {best['threshold']:.2f}")
    print(f"📁 Check subject_threshold_report.md")

if __name__ == "__main__":
    main()




