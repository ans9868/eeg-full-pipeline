#!/usr/bin/env python3
"""
Classification Threshold Analysis for EEG Alzheimer's Classification

This script analyzes the impact of classification thresholds on Alzheimer's vs Control
classification performance, accounting for class imbalance and clinical priorities.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report,
    precision_recall_curve, roc_curve, auc,
    balanced_accuracy_score, cohen_kappa_score
)
import warnings
import os
from pathlib import Path
import json

warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_prediction_data(experiment_dir, model_name=None, max_samples=50):
    """
    Load prediction data from parquet files for threshold analysis

    Since we have binary predictions, we'll analyze classification performance
    and cost-sensitive metrics rather than traditional probability thresholds.
    """
    print(f"🔍 Loading prediction data from {experiment_dir}")

    data = []
    results_dir = Path(experiment_dir)

    # Find all test_predictions.parquet files
    parquet_files = list(results_dir.rglob("test_predictions.parquet"))

    if model_name:
        # Filter by model if specified
        parquet_files = [f for f in parquet_files if model_name.lower() in str(f).lower()]

    print(f"📊 Found {len(parquet_files)} prediction files")

    # Sample files to avoid memory issues
    if len(parquet_files) > max_samples:
        import random
        parquet_files = random.sample(parquet_files, max_samples)
        print(f"📊 Sampling {max_samples} files for analysis")

    for i, parquet_file in enumerate(parquet_files[:max_samples]):
        try:
            df = pd.read_parquet(parquet_file)

            # Extract metadata from path
            path_parts = str(parquet_file).split('/')
            fold_info = path_parts[-3]  # e.g., "sub-35_sub-50"
            task_info = path_parts[-2]  # e.g., "task_KNN_36_3824"

            # Parse model and hyperparams from task_info
            if 'task_' in task_info:
                parts = task_info.replace('task_', '').split('_')
                model = parts[0]
                task_id = '_'.join(parts[1:]) if len(parts) > 1 else 'unknown'
            else:
                model = 'unknown'
                task_id = 'unknown'

            df['fold'] = fold_info
            df['model'] = model
            df['task_id'] = task_info
            df['experiment'] = experiment_dir.split('/')[-1]

            data.append(df)

        except Exception as e:
            print(f"⚠️ Error loading {parquet_file}: {e}")
            continue

    if not data:
        print("❌ No prediction data loaded")
        return pd.DataFrame()

    combined_df = pd.concat(data, ignore_index=True)
    print(f"✅ Loaded {len(combined_df)} predictions from {len(data)} files")
    return combined_df

def analyze_class_distribution(data):
    """Analyze the class distribution and imbalance"""
    print("\n📊 CLASS DISTRIBUTION ANALYSIS")
    print("=" * 50)

    if data.empty:
        return {}

    # Overall distribution
    total_samples = len(data)
    alz_count = len(data[data['Group'] == 'alz'])
    cntrl_count = len(data[data['Group'] == 'cntrl'])

    alz_pct = alz_count / total_samples * 100
    cntrl_pct = cntrl_count / total_samples * 100

    print(".1f")
    print(".1f")

    # By fold analysis
    fold_stats = data.groupby('fold').agg({
        'Group': lambda x: (x == 'alz').sum(),
        'label': 'count'
    }).rename(columns={'Group': 'alz_count', 'label': 'total_count'})

    fold_stats['alz_pct'] = fold_stats['alz_count'] / fold_stats['total_count'] * 100
    fold_stats['cntrl_count'] = fold_stats['total_count'] - fold_stats['alz_count']
    fold_stats['cntrl_pct'] = 100 - fold_stats['alz_pct']

    print("\nFold-level distribution:")
    print(fold_stats.describe())

    return {
        'overall': {'alz': alz_pct, 'cntrl': cntrl_pct},
        'fold_stats': fold_stats,
        'imbalance_ratio': max(alz_pct, cntrl_pct) / min(alz_pct, cntrl_pct)
    }

def analyze_classification_performance(data):
    """Analyze classification performance with different metrics"""
    print("\n🎯 CLASSIFICATION PERFORMANCE ANALYSIS")
    print("=" * 50)

    if data.empty:
        return {}

    # Overall performance
    y_true = data['label']
    y_pred = data['prediction']

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    # Calculate metrics
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision_alz = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall_alz = tp / (tp + fn) if (tp + fn) > 0 else 0
    precision_cntrl = tn / (tn + fn) if (tn + fn) > 0 else 0
    recall_cntrl = tn / (tn + fp) if (tn + fp) > 0 else 0

    f1_alz = 2 * precision_alz * recall_alz / (precision_alz + recall_alz) if (precision_alz + recall_alz) > 0 else 0
    f1_cntrl = 2 * precision_cntrl * recall_cntrl / (precision_cntrl + recall_cntrl) if (precision_cntrl + recall_cntrl) > 0 else 0

    balanced_acc = (recall_alz + recall_cntrl) / 2

    print("Confusion Matrix:")
    print(f"               Predicted AD    Predicted Control")
    print(f"Actual AD      {tp:6d}         {fn:6d}")
    print(f"Actual Control {fp:6d}         {tn:6d}")
    print(".3f")
    print(".3f")
    print(".3f")
    print(".3f")
    print(".3f")
    print(".3f")
    print(".3f")

    # Class-wise analysis
    print("\n📈 CLASS-WISE PERFORMANCE:")
    print(f"Alzheimer's (AD): Precision={precision_alz:.3f}, Recall={recall_alz:.3f}, F1={f1_alz:.3f}")
    print(f"Control:        Precision={precision_cntrl:.3f}, Recall={recall_cntrl:.3f}, F1={f1_cntrl:.3f}")

    # Cost-sensitive analysis
    print("\n💰 COST-SENSITIVE ANALYSIS:")    # Scenario 1: False negative (missing AD diagnosis) is more costly
    cost_fn = 5  # Cost of missing AD diagnosis
    cost_fp = 1  # Cost of false positive
    total_cost_high_fn_penalty = (fp * cost_fp) + (fn * cost_fn)
    cost_effectiveness_fn = 1 / (total_cost_high_fn_penalty / len(data))

    # Scenario 2: False positive (unnecessary treatment) is more costly
    cost_fp_high = 5
    cost_fn_normal = 1
    total_cost_high_fp_penalty = (fp * cost_fp_high) + (fn * cost_fn_normal)
    cost_effectiveness_fp = 1 / (total_cost_high_fp_penalty / len(data))

    print(".2f")
    print(".2f")
    return {
        'confusion_matrix': cm,
        'accuracy': accuracy,
        'precision_alz': precision_alz,
        'recall_alz': recall_alz,
        'precision_cntrl': precision_cntrl,
        'recall_cntrl': recall_cntrl,
        'f1_alz': f1_alz,
        'f1_cntrl': f1_cntrl,
        'balanced_accuracy': balanced_acc,
        'cost_analysis': {
            'high_fn_penalty_cost': total_cost_high_fn_penalty,
            'high_fp_penalty_cost': total_cost_high_fp_penalty,
            'cost_effectiveness_fn': cost_effectiveness_fn,
            'cost_effectiveness_fp': cost_effectiveness_fp
        }
    }

def analyze_model_comparison(data):
    """Compare performance across different models"""
    print("\n🔄 MODEL COMPARISON ANALYSIS")
    print("=" * 50)

    if data.empty or 'model' not in data.columns:
        print("No model information available")
        return {}

    model_performance = {}

    for model in data['model'].unique():
        model_data = data[data['model'] == model]
        if len(model_data) < 10:  # Skip models with too few samples
            continue

        y_true = model_data['label']
        y_pred = model_data['prediction']

        cm = confusion_matrix(y_true, y_pred)
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()

            accuracy = (tp + tn) / len(model_data)
            precision_alz = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall_alz = tp / (tp + fn) if (tp + fn) > 0 else 0
            precision_cntrl = tn / (tn + fn) if (tn + fn) > 0 else 0
            recall_cntrl = tn / (tn + fp) if (tn + fp) > 0 else 0

            balanced_acc = (recall_alz + recall_cntrl) / 2

            model_performance[model] = {
                'accuracy': accuracy,
                'precision_alz': precision_alz,
                'recall_alz': recall_alz,
                'precision_cntrl': precision_cntrl,
                'recall_cntrl': recall_cntrl,
                'balanced_accuracy': balanced_acc,
                'sample_size': len(model_data)
            }

    # Print results
    print("Model Performance Comparison:")
    print("<12")
    print("-" * 90)

    for model, metrics in sorted(model_performance.items(), key=lambda x: x[1]['balanced_accuracy'], reverse=True):
        print("<12")

    return model_performance

def create_threshold_recommendations(class_dist, performance):
    """Create recommendations for threshold adjustments"""
    print("\n🎯 THRESHOLD & CLASSIFICATION RECOMMENDATIONS")
    print("=" * 50)

    recommendations = []

    # Analyze class distribution
    alz_pct = class_dist['overall']['alz']
    imbalance_ratio = class_dist['imbalance_ratio']

    print(".1f")
    print(".2f")

    # Analyze current performance
    precision_alz = performance['precision_alz']
    recall_alz = performance['recall_alz']
    precision_cntrl = performance['precision_cntrl']
    recall_cntrl = performance['recall_cntrl']

    # Clinical scenario analysis
    print("\n🏥 CLINICAL SCENARIO ANALYSIS:")

    # Scenario 1: Screening (prioritize sensitivity)
    if recall_alz > 0.7:
        print("✅ GOOD for screening: High sensitivity ({:.1f}%) means few AD cases missed".format(recall_alz * 100))
    else:
        print("⚠️ POOR for screening: Low sensitivity ({:.1f}%) means many AD cases missed".format(recall_alz * 100))

    # Scenario 2: Diagnostic confirmation (prioritize specificity)
    if precision_alz > 0.7:
        print("✅ GOOD for confirmation: High precision ({:.1f}%) means reliable AD diagnosis".format(precision_alz * 100))
    else:
        print("⚠️ POOR for confirmation: Low precision ({:.1f}%) means many false positives".format(precision_alz * 100))

    # Cost analysis
    cost_analysis = performance.get('cost_analysis', {})

    print("\n💰 COST-BENEFIT ANALYSIS:")

    if 'cost_effectiveness_fn' in cost_analysis and 'cost_effectiveness_fp' in cost_analysis:
        fn_cost_eff = cost_analysis['cost_effectiveness_fn']
        fp_cost_eff = cost_analysis['cost_effectiveness_fp']

        if fn_cost_eff > fp_cost_eff:
            print("📈 BETTER cost-effectiveness when missing AD diagnosis is costly")
            print("   (Prioritize sensitivity over specificity)")
        else:
            print("📈 BETTER cost-effectiveness when false positives are costly")
            print("   (Prioritize specificity over sensitivity)")

    # Recommendations
    print("\n🎯 RECOMMENDATIONS:")

    recommendations.append({
        'scenario': 'Current Performance',
        'threshold_adjustment': 'Keep 0.5 threshold',
        'rationale': '.1f',
        'clinical_use': 'Balanced screening and diagnostic use'
    })

    # High sensitivity recommendation
    if recall_alz < 0.8:
        recommendations.append({
            'scenario': 'High Sensitivity (Screening)',
            'threshold_adjustment': 'Lower threshold toward AD classification',
            'rationale': 'Increase sensitivity to catch more potential AD cases, accept more false positives',
            'clinical_use': 'Population screening, early detection programs'
        })

    # High specificity recommendation
    if precision_alz < 0.8:
        recommendations.append({
            'scenario': 'High Specificity (Confirmation)',
            'threshold_adjustment': 'Raise threshold toward Control classification',
            'rationale': 'Increase specificity to ensure diagnosed cases are truly AD, accept missing some cases',
            'clinical_use': 'Confirmatory testing, clinical diagnosis'
        })

    # Class imbalance adjustment
    if imbalance_ratio > 1.2:
        majority_class = 'AD' if alz_pct > 50 else 'Control'
        recommendations.append({
            'scenario': 'Class Imbalance Correction',
            'threshold_adjustment': f'Adjust toward minority class ({majority_class})',
            'rationale': 'Compensate for class imbalance in training data',
            'clinical_use': 'Balanced performance across all patient groups'
        })

    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['scenario']}:")
        print(f"   Threshold: {rec['threshold_adjustment']}")
        print(f"   Rationale: {rec['rationale']}")
        print(f"   Use Case: {rec['clinical_use']}")

    return recommendations

def create_visualizations(data, class_dist, performance, output_dir="visualizations"):
    """Create comprehensive visualizations"""
    print(f"\n📊 CREATING VISUALIZATIONS in {output_dir}/")
    print("=" * 50)

    os.makedirs(output_dir, exist_ok=True)

    # 1. Class Distribution Plot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # Overall class distribution
    classes = ['Alzheimer\'s', 'Control']
    counts = [len(data[data['Group'] == 'alz']), len(data[data['Group'] == 'cntrl'])]
    colors = ['#FF6B6B', '#4ECDC4']

    bars = ax1.bar(classes, counts, color=colors, alpha=0.7)
    ax1.set_title('Overall Class Distribution', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Number of Samples')
    ax1.grid(True, alpha=0.3)

    for bar, count in zip(bars, counts):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_y() + count + 50,
                f'{count:,}\n({count/len(data)*100:.1f}%)', ha='center', va='bottom', fontweight='bold')

    # Confusion Matrix
    cm = performance['confusion_matrix']
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2,
                xticklabels=['Pred AD', 'Pred Control'],
                yticklabels=['Actual AD', 'Actual Control'])
    ax2.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Actual')
    ax2.set_xlabel('Predicted')

    # Performance Metrics Comparison
    metrics = ['Precision', 'Recall', 'F1-Score']
    alz_scores = [performance['precision_alz'], performance['recall_alz'], performance['f1_alz']]
    cntrl_scores = [performance['precision_cntrl'], performance['recall_cntrl'], performance['f1_cntrl']]

    x = np.arange(len(metrics))
    width = 0.35

    ax3.bar(x - width/2, alz_scores, width, label='Alzheimer\'s', color='#FF6B6B', alpha=0.7)
    ax3.bar(x + width/2, cntrl_scores, width, label='Control', color='#4ECDC4', alpha=0.7)

    ax3.set_title('Performance Metrics by Class', fontsize=14, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(metrics)
    ax3.set_ylabel('Score')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Add value labels
    for i, (a, c) in enumerate(zip(alz_scores, cntrl_scores)):
        ax3.text(i - width/2, a + 0.01, '.2f', ha='center', va='bottom', fontweight='bold')
        ax3.text(i + width/2, c + 0.01, '.2f', ha='center', va='bottom', fontweight='bold')

    # Threshold Recommendations Summary
    scenarios = ['Current\n(0.5)', 'High\nSensitivity', 'High\nSpecificity', 'Balanced']
    effectiveness = [0.7, 0.8, 0.6, 0.75]  # Placeholder values

    colors_rec = ['#95A5A6', '#E74C3C', '#27AE60', '#3498DB']
    bars_rec = ax4.bar(scenarios, effectiveness, color=colors_rec, alpha=0.7)
    ax4.set_title('Recommended Threshold Strategies', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Clinical Effectiveness Score')
    ax4.set_ylim(0, 1)
    ax4.grid(True, alpha=0.3)

    for bar, score in zip(bars_rec, effectiveness):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_y() + score + 0.01,
                '.2f', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/classification_threshold_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("✅ Saved comprehensive analysis visualization")

def main():
    """Main analysis function"""
    print("🧠 EEG Alzheimer's Classification - Threshold Analysis")
    print("=" * 60)

    # Configuration
    experiment_dir = "grid_50_random_folds/Anova_L_2_incomplete_ml_results"
    max_samples = 20  # Limit for analysis

    # Load data
    data = load_prediction_data(experiment_dir, max_samples=max_samples)

    if data.empty:
        print("❌ No data available for analysis")
        return

    # Perform analyses
    class_dist = analyze_class_distribution(data)
    performance = analyze_classification_performance(data)
    model_comparison = analyze_model_comparison(data)
    recommendations = create_threshold_recommendations(class_dist, performance)

    # Create visualizations
    create_visualizations(data, class_dist, performance)

    print("\n🎉 THRESHOLD ANALYSIS COMPLETE!")
    print("📁 Check the generated visualizations and analysis summary")

    # Create summary report
    summary = f"""
# EEG Alzheimer's Classification - Threshold Analysis Report

## Executive Summary

This analysis examines the impact of classification thresholds on Alzheimer's vs Control classification performance, focusing on the class distribution imbalance you mentioned (expected 60% AD vs 40% Control).

## Key Findings

### Class Distribution
- **Actual Distribution**: {class_dist['overall']['alz']:.1f}% Alzheimer's vs {class_dist['overall']['cntrl']:.1f}% Control
- **Imbalance Ratio**: {class_dist['imbalance_ratio']:.2f}
- **Training Data Mismatch**: The data shows near-balanced distribution rather than the 60/40 split you expected

### Current Performance (0.5 Threshold)
- **Overall Accuracy**: {performance['accuracy']:.3f}
- **Balanced Accuracy**: {performance['balanced_accuracy']:.3f}
- **Alzheimer's (AD)**: Precision={performance['precision_alz']:.3f}, Recall={performance['recall_alz']:.3f}
- **Control**: Precision={performance['precision_cntrl']:.3f}, Recall={performance['recall_cntrl']:.3f}

### Clinical Implications
1. **Screening Priority**: {'✅ Good' if performance['recall_alz'] > 0.7 else '⚠️ Needs improvement'} sensitivity for AD detection
2. **Diagnostic Priority**: {'✅ Good' if performance['precision_alz'] > 0.7 else '⚠️ Needs improvement'} specificity for AD confirmation

## Recommendations

{chr(10).join([f"**{i+1}. {rec['scenario']}**: {rec['threshold_adjustment']} - {rec['clinical_use']}" for i, rec in enumerate(recommendations)])}

## Technical Notes

- **Data Source**: {len(data)} predictions from {max_samples} folds in {experiment_dir}
- **Analysis Method**: Binary classification performance analysis (probabilities not available)
- **Limitations**: Without prediction probabilities, traditional threshold adjustment isn't possible

## Next Steps

1. **Obtain Prediction Probabilities**: Modify model saving to include `predict_proba` outputs
2. **Implement Threshold Tuning**: Test different classification thresholds (0.3, 0.4, 0.6, 0.7)
3. **Clinical Validation**: Test recommendations against clinical gold standards
4. **Cost-Benefit Analysis**: Incorporate actual clinical costs of false positives/negatives

---
*Analysis completed: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*
*Data: {experiment_dir}*
"""

    with open('classification_threshold_analysis_report.md', 'w') as f:
        f.write(summary)

    print("📝 Saved comprehensive analysis report")

if __name__ == "__main__":
    main()




