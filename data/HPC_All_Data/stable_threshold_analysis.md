# 🎯 Stable Threshold Analysis - ONE Threshold Across All Folds

## Analysis Overview

This analysis finds **ONE stable threshold** that works across all folds, rather than per-fold thresholds.
It also clarifies the threshold direction and why thresholds might seem counterintuitive.

## 📊 Results by Experiment

### ANOVA_L_2

**Data Distribution:**
- True AD %: 50.0%
- True Control %: 50.0%
- AD subjects mean AD ratio: 0.835
- Control subjects mean AD ratio: 0.424

**Stable Threshold (All Models):**
- Optimal threshold: **0.45**
- Accuracy: 0.837
- Balanced accuracy: 0.859
- AD Recall: 0.774
- Control Recall: 0.944
- Predicted AD %: 63.3%

**🎯 KNN-Only Stable Threshold:**
- Optimal threshold: **0.45**
- Accuracy: 0.875
- Balanced accuracy: 0.878
- AD Recall: 0.852
- Control Recall: 0.905
- Predicted AD %: 56.2%

---

### ANOVA_L_6

**Data Distribution:**
- True AD %: 50.0%
- True Control %: 50.0%
- AD subjects mean AD ratio: 0.792
- Control subjects mean AD ratio: 0.435

**Stable Threshold (All Models):**
- Optimal threshold: **0.70**
- Accuracy: 0.846
- Balanced accuracy: 0.844
- AD Recall: 0.882
- Control Recall: 0.806
- Predicted AD %: 52.3%

**🎯 KNN-Only Stable Threshold:**
- Optimal threshold: **0.60**
- Accuracy: 0.859
- Balanced accuracy: 0.864
- AD Recall: 0.933
- Control Recall: 0.794
- Predicted AD %: 46.9%

---

### PCA_L_2

**Data Distribution:**
- True AD %: 50.0%
- True Control %: 50.0%
- AD subjects mean AD ratio: 0.751
- Control subjects mean AD ratio: 0.654

**Stable Threshold (All Models):**
- Optimal threshold: **0.70**
- Accuracy: 0.660
- Balanced accuracy: 0.660
- AD Recall: 0.654
- Control Recall: 0.667
- Predicted AD %: 55.3%

**🎯 KNN-Only Stable Threshold:**
- Optimal threshold: **0.35**
- Accuracy: 0.535
- Balanced accuracy: 0.631
- AD Recall: 0.750
- Control Recall: 0.513
- Predicted AD %: 9.3%

---

### PCA_L_6

**Data Distribution:**
- True AD %: 50.0%
- True Control %: 50.0%
- AD subjects mean AD ratio: 0.782
- Control subjects mean AD ratio: 0.699

**Stable Threshold (All Models):**
- Optimal threshold: **0.70**
- Accuracy: 0.723
- Balanced accuracy: 0.722
- AD Recall: 0.725
- Control Recall: 0.720
- Predicted AD %: 61.5%

**🎯 KNN-Only Stable Threshold:**
- Optimal threshold: **0.70**
- Accuracy: 0.484
- Balanced accuracy: 0.730
- AD Recall: 1.000
- Control Recall: 0.459
- Predicted AD %: 4.7%

---

## 🎯 Key Findings

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
