# 🔍 Detailed Per-Subject, Per-Fold, Per-Model Threshold Analysis

## Analysis Overview

This report provides **granular threshold analysis** at multiple levels:
- **Per Model** (aggregated across folds)
- **Per Fold** (aggregated across models)  
- **Per Model×Fold** (most granular)
- **KNN-Specific** (detailed analysis for KNN model)

## 📊 Summary by Experiment

### ANOVA_L_2

**Per-Model Optimal Thresholds:**

| Model | Optimal Threshold | Accuracy | Balanced Accuracy | AD Recall | N Subjects |
|-------|-------------------|----------|-------------------|----------|------------|
| KNN | 0.50 | 0.907 | 0.912 | 0.880 | 43 |
| MLP | 0.60 | 0.889 | 0.900 | 0.800 | 36 |
| SVM | 0.45 | 0.778 | 0.853 | 0.706 | 45 |
| XGBoost | 0.55 | 0.905 | 0.907 | 0.864 | 42 |

**Per-Fold Analysis:**
- Number of folds analyzed: 50
- Threshold range: 0.30 - 0.70
- Mean threshold: 0.37
- Median threshold: 0.30
- Std deviation: 0.12
- Mean accuracy: 0.900

**🎯 KNN-Specific Analysis:**
- KNN folds analyzed: 39
- KNN threshold range: 0.30 - 0.70
- KNN mean threshold: 0.37
- KNN median threshold: 0.30
- KNN std deviation: 0.13
- KNN mean accuracy: 0.949
- KNN mean balanced accuracy: 0.923

**KNN Threshold Distribution:**
- Threshold 0.30: 25 folds (64.1%)
- Threshold 0.40: 7 folds (17.9%)
- Threshold 0.45: 2 folds (5.1%)
- Threshold 0.50: 1 folds (2.6%)
- Threshold 0.70: 4 folds (10.3%)

---

### ANOVA_L_6

**Per-Model Optimal Thresholds:**

| Model | Optimal Threshold | Accuracy | Balanced Accuracy | AD Recall | N Subjects |
|-------|-------------------|----------|-------------------|----------|------------|
| KNN | 0.55 | 0.846 | 0.844 | 0.882 | 65 |
| MLP | 0.45 | 0.810 | 0.831 | 0.757 | 58 |
| SVM | 0.60 | 0.800 | 0.828 | 0.756 | 65 |
| XGBoost | 0.50 | 0.806 | 0.807 | 0.806 | 62 |

**Per-Fold Analysis:**
- Number of folds analyzed: 50
- Threshold range: 0.30 - 0.70
- Mean threshold: 0.50
- Median threshold: 0.50
- Std deviation: 0.12
- Mean accuracy: 0.867

**🎯 KNN-Specific Analysis:**
- KNN folds analyzed: 37
- KNN threshold range: 0.30 - 0.70
- KNN mean threshold: 0.45
- KNN median threshold: 0.45
- KNN std deviation: 0.13
- KNN mean accuracy: 0.914
- KNN mean balanced accuracy: 0.936

**KNN Threshold Distribution:**
- Threshold 0.30: 10 folds (27.0%)
- Threshold 0.40: 7 folds (18.9%)
- Threshold 0.45: 5 folds (13.5%)
- Threshold 0.50: 4 folds (10.8%)
- Threshold 0.55: 5 folds (13.5%)
- Threshold 0.60: 2 folds (5.4%)
- Threshold 0.70: 4 folds (10.8%)

---

### PCA_L_2

**Per-Model Optimal Thresholds:**

| Model | Optimal Threshold | Accuracy | Balanced Accuracy | AD Recall | N Subjects |
|-------|-------------------|----------|-------------------|----------|------------|
| KNN | 0.30 | 0.659 | 0.739 | 0.857 | 44 |
| MLP | 0.45 | 0.571 | 0.615 | 0.564 | 42 |
| SVM | 0.70 | 0.543 | 0.761 | 0.523 | 46 |
| XGBoost | 0.30 | 0.532 | 0.761 | 0.522 | 47 |

**Per-Fold Analysis:**
- Number of folds analyzed: 49
- Threshold range: 0.30 - 0.70
- Mean threshold: 0.42
- Median threshold: 0.30
- Std deviation: 0.16
- Mean accuracy: 0.714

**🎯 KNN-Specific Analysis:**
- KNN folds analyzed: 34
- KNN threshold range: 0.30 - 0.30
- KNN mean threshold: 0.30
- KNN median threshold: 0.30
- KNN std deviation: 0.00
- KNN mean accuracy: 0.632
- KNN mean balanced accuracy: 0.449

**KNN Threshold Distribution:**
- Threshold 0.30: 34 folds (100.0%)

---

### PCA_L_6

**Per-Model Optimal Thresholds:**

| Model | Optimal Threshold | Accuracy | Balanced Accuracy | AD Recall | N Subjects |
|-------|-------------------|----------|-------------------|----------|------------|
| KNN | 0.60 | 0.508 | 0.737 | 1.000 | 61 |
| MLP | 0.70 | 0.631 | 0.654 | 0.615 | 65 |
| SVM | 0.70 | 0.587 | 0.787 | 0.574 | 63 |
| XGBoost | 0.50 | 0.569 | 0.781 | 0.562 | 65 |

**Per-Fold Analysis:**
- Number of folds analyzed: 47
- Threshold range: 0.30 - 0.70
- Mean threshold: 0.49
- Median threshold: 0.50
- Std deviation: 0.17
- Mean accuracy: 0.631

**🎯 KNN-Specific Analysis:**
- KNN folds analyzed: 32
- KNN threshold range: 0.30 - 0.70
- KNN mean threshold: 0.34
- KNN median threshold: 0.30
- KNN std deviation: 0.11
- KNN mean accuracy: 0.589
- KNN mean balanced accuracy: 0.478

**KNN Threshold Distribution:**
- Threshold 0.30: 26 folds (81.2%)
- Threshold 0.40: 2 folds (6.2%)
- Threshold 0.45: 1 folds (3.1%)
- Threshold 0.50: 1 folds (3.1%)
- Threshold 0.70: 2 folds (6.2%)

---

## 🎯 Overall KNN Summary Across All Experiments

**Across all experiments:**
- Total KNN fold analyses: 142
- Overall threshold range: 0.30 - 0.70
- Overall mean threshold: 0.37
- Overall median threshold: 0.30
- Overall mean accuracy: 0.783

## 📋 Key Findings

1. **Threshold variability**: Optimal thresholds vary significantly across folds and models
2. **KNN performance**: KNN shows consistent patterns but threshold varies by fold
3. **Experiment differences**: ANOVA vs PCA experiments show different threshold patterns
4. **Granularity matters**: Per-fold analysis reveals more variability than aggregated analysis

## 🔧 Recommendations

1. **Use fold-specific thresholds** for best performance (if fold information available)
2. **Use model-specific thresholds** as a compromise (better than universal)
3. **KNN-specific thresholds** can be optimized separately from other models
4. **Consider ensemble approach**: Use different thresholds for different models

---
*Analysis completed: 2025-12-08 15:46*
*Granularity: Per model, per fold, per model×fold combinations*
