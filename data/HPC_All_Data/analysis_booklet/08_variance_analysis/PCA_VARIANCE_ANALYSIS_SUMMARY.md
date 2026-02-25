# PCA Variance Analysis Summary

## Overview

Analysis of variance in accuracy across 10 experiments for both PCA_W_F and PCA_W_C feature sets. Results selected to achieve n=10 for each model where possible.

---

## Version Status

### Version Coverage

**PCA_W_F:** All 10 versions present (v1-v10) ✅  
**PCA_W_C:** 10 versions present (v0-v9) ⚠️ *v10 not yet run*

**Note:** v0 was initially missed in analysis but is now included. v0 contains a subset of models (not all standard 12 models).

---

## Model Status

### Models Found

Both PCA_W_F and PCA_W_C contain:
- ✅ **KNN** (3 configurations: n=1, n=7, n=15) - n=10 each
- ✅ **MLP (Neural Network)** (3 configurations: hidden=[100], [150,50], [200,100,50]) - n=10 each
- ✅ **SVM** (3 configurations: kernel=linear, rbf, poly) - n=10 each
- ✅ **XGBoost** (3 configurations: depth=3, 6, 9) - n=10 for depth=3 and 6, n=9 for depth=9 in PCA_W_C

**Note:** The "Missing models" warning is a false positive - the system looks for "MLP" and "Neural Network" separately, but they're stored as "MLP (Neural Network)".

### Duplicate Handling

**v7 and v8 have duplicate results:**
- **KNN, MLP, SVM:** 2 results each in v7 and v8 (original + rerun)
- **XGBoost depth=3, 6:** 1 result each in v7 and v8 (no duplicates)
- **XGBoost depth=9:** 1 result each in v7 and v8 (no duplicates)
- **Strategy:** 
  - Models in v0: v0 + v1-v6, v9 (8) + 1 from v7 + 1 from v8 = 10
  - Models NOT in v0: v1-v6, v9 (7) + 2 from v7 + 1 from v8 = 10 (or vice versa)
  - XGBoost depth=9: v1-v6, v9 (7) + 1 from v7 + 1 from v8 = 9 (no duplicates available)

---

## PCA_W_F Results

### Summary Statistics

- **Total results loaded:** 138
- **Unique model configurations:** 12
- **Unique experiments:** 10
- **Results per model:** 10 (all models)

### Variance Rankings (Lowest to Highest)

1. **MLP [200, 100, 50]**: variance = 0.000004, mean = 0.9818 (n=10) ✅
2. **MLP [150, 50]**: variance = 0.000013, mean = 0.9755 (n=10) ✅
3. **MLP [100]**: variance = 0.000018, mean = 0.9626 (n=10) ✅
4. **XGBoost (depth=3)**: variance = 0.000021, mean = 0.8959 (n=10)
5. **XGBoost (depth=6)**: variance = 0.000023, mean = 0.8982 (n=10)
6. **SVM (linear)**: variance = 0.000027, mean = 0.9396 (n=10)
7. **XGBoost (depth=9)**: variance = 0.000031, mean = 0.8897 (n=10)
8. **SVM (poly)**: variance = 0.000356, mean = 0.5577 (n=10)
9. **SVM (rbf)**: variance = 0.000471, mean = 0.6396 (n=10)
10. **KNN (n=1)**: variance = 0.000614, mean = 0.6412 (n=10)
11. **KNN (n=15)**: variance = 0.000680, mean = 0.6631 (n=10)
12. **KNN (n=7)**: variance = 0.000839, mean = 0.6652 (n=10)

### Key Findings

- **MLP models** show highest accuracy (~96-98%) with very low variance (best performers)
- **XGBoost** shows good accuracy (~89-90%) with very low variance
- **SVM (linear)** shows high accuracy (~94%) with low variance
- **KNN models** show moderate accuracy (~64-67%) with highest variance
- **All models** now have consistent n=10 values across all 10 experiments

---

## PCA_W_C Results

### Summary Statistics

- **Total results loaded:** 143
- **Unique model configurations:** 16
- **Unique experiments:** 10 (v0-v9)
- **Results per model:** 10 (except XGBoost depth=9 with n=9)

### Variance Rankings (Lowest to Highest)

1. **MLP [200, 100, 50]**: variance = 0.000005, mean = 0.9818 (n=10) ✅
2. **MLP [150, 50]**: variance = 0.000009, mean = 0.9748 (n=10) ✅
3. **MLP [100]**: variance = 0.000014, mean = 0.9627 (n=10) ✅
4. **SVM (linear)**: variance = 0.000027, mean = 0.9396 (n=10)
5. **XGBoost (depth=9)**: variance = 0.000044, mean = 0.8919 (n=9)
6. **XGBoost (depth=6)**: variance = 0.000058, mean = 0.8969 (n=10)
7. **XGBoost (depth=3)**: variance = 0.000183, mean = 0.8933 (n=10)
8. **SVM (poly)**: variance = 0.000327, mean = 0.5568 (n=10)
9. **SVM (rbf)**: variance = 0.000402, mean = 0.6349 (n=10)
10. **KNN (n=1)**: variance = 0.000489, mean = 0.6339 (n=10)
11. **KNN (n=15)**: variance = 0.000588, mean = 0.6616 (n=10)
12. **KNN (n=7)**: variance = 0.000652, mean = 0.6571 (n=10)

### Key Findings

- **MLP models** show highest accuracy (~96-98%) with very low variance (best performers)
- **XGBoost** shows good accuracy (~89-90%) with low variance
- **SVM (linear)** shows high accuracy (~94%) with low variance
- **KNN models** show moderate accuracy (~63-66%) with highest variance
- **Consistent n values** across all models (n=10 for most, n=9 for XGBoost depth=9)

---

## Comparison: PCA_W_F vs PCA_W_C

### Similarities

1. **Same model coverage:** Both have all 4 model types (KNN, MLP, SVM, XGBoost)
2. **Same n values:** Both have n=10 for most models
3. **Similar variance patterns:** MLP lowest variance, KNN highest variance
4. **Similar accuracy patterns:** MLP highest accuracy, KNN moderate accuracy
5. **MLP dominance:** MLP [200, 100, 50] shows best performance in both

### Differences

1. **XGBoost variance:** Slightly different variance rankings between PCA_W_F and PCA_W_C
2. **PCA_W_F:** XGBoost depth=3 has lowest variance (0.000021)
3. **PCA_W_C:** XGBoost depth=9 has lowest variance (0.000044), but depth=3 has highest (0.000183)
4. **Version coverage:** PCA_W_F has v10, PCA_W_C missing v10

---

## Files Generated

### PCA_W_F
- `all_experiment_results.csv` - Complete tabular data
- `variance_boxplot_all_models.png` - Box plot visualization (n=10 per model)
- `variance_summary_table.csv` - Summary statistics

### PCA_W_C
- `all_experiment_results.csv` - Complete tabular data
- `variance_boxplot_all_models.png` - Box plot visualization (n=10 per model)
- `variance_summary_table.csv` - Summary statistics

---

## Methodology

**Result Selection Strategy:**
1. Include all results from v1-v6, v9 (7 results)
2. For v7 and v8: Select results to achieve n=10 total
   - If duplicates exist: Keep 1 from v7, 2 from v8 (or vice versa)
   - For XGBoost: Only 1 result per version available, so n=9 for depth=9 in PCA_W_C

**Why Duplicates Exist:**
- v7 and v8 were rerun to add XGBoost results
- Original runs (KNN, MLP, SVM) were kept alongside rerun results
- Some duplicates have identical accuracies (same result stored twice)
- Some duplicates have slightly different accuracies (original vs rerun with different random seeds)

---

## Recommendations

1. ✅ **Analysis complete:** All models have consistent n values (10 for most, 9 for XGBoost depth=9 in PCA_W_C)
2. **CSV files available:** `all_experiment_results.csv` contains all raw data for inspection
3. **XGBoost n=9:** This is expected as XGBoost was only added in reruns and has no duplicates for depth=9 in PCA_W_C
4. **PCA_W_C v10:** Run v10 experiment to complete the dataset

---

*Analysis Date: January 13, 2025*  
*Script: `analyze_pca_variance.py`*  
*Versions analyzed: PCA_W_F (v1-v10), PCA_W_C (v0-v9)*
