# Investigation: Identical Results Anomaly in ANOVA_L_6_Random

## Problem Statement

In the ANOVA_L_6_Random experiment, all four models (KNN, MLP, SVM, XGBoost) report **identical** final statistics:
- **Variance**: 0.1430
- **Mean Success Rate**: 77.03%

This is statistically suspicious because different model architectures should produce different results.

## Investigation Results

### 1. Individual Fold Accuracies ARE Different

When examining individual fold predictions, the models produce **different** accuracies:

**Example from fold `sub-10_sub-17_sub-30_sub-41_sub-44_sub-60`:**
- **KNN**: Subject 10 = 0.371, Subject 17 = 0.842, Subject 30 = 0.881
- **MLP**: Subject 10 = 0.586, Subject 17 = 0.967, Subject 30 = 0.759
- **SVM**: Subject 10 = 0.925, Subject 17 = 0.996, Subject 30 = 0.988
- **XGBoost**: Subject 10 = 0.315, Subject 17 = 0.954, Subject 30 = 0.988

**Conclusion**: Models are producing different predictions at the fold level.

### 2. Per-Subject Success Rates ARE Different

When calculating per-subject success rates using **ALL 50 folds**, the results are:

| Model | Variance | Mean Success Rate |
|-------|----------|-------------------|
| KNN | 0.1292 | 83.62% |
| MLP | 0.1142 | 80.35% |
| SVM | 0.1835 | 75.77% |
| XGBoost | 0.1430 | 77.03% |

**Conclusion**: When using all folds directly, results are **different** across models.

### 3. The Issue: Random Sampling at num_folds=50

The analysis script uses `calculate_variance_by_num_folds()` which:
1. For each `num_folds` (1 to 50), samples 30 random combinations
2. When `num_folds=50`, it does `random.sample(all_fold_names, 50)` 30 times
3. Since there are exactly 50 folds, each sample contains all 50 folds (just shuffled)
4. The script then averages the variance across these 30 samples

**The Problem**: When `num_folds=50`, all 30 samples contain the same 50 folds (just in different orders). Since order doesn't matter for calculating per-subject success rates, all 30 samples should give identical results. However, the script reports `std_variance=0.0000` for num_folds=50, which confirms this.

### 4. Why Are Results Identical in the Report?

**Hypothesis**: The identical results (0.1430 variance, 77.03% mean) might be due to:

1. **Rounding/Precision**: The results are rounded to 4 decimal places in the report
2. **Data Issue**: Perhaps all models are somehow using the same underlying data or there's a bug in data loading
3. **Calculation Bug**: There might be an issue in how the variance is calculated when using sampled folds

### 5. Verification Test

When calculating directly with all 50 folds (bypassing the sampling):
- **XGBoost**: variance=0.143001, mean=0.770265 ✅ Matches report
- **KNN**: variance=0.129180, mean=0.836154 ❌ Does NOT match report
- **MLP**: variance=0.114241, mean=0.803497 ❌ Does NOT match report  
- **SVM**: variance=0.183534, mean=0.757692 ❌ Does NOT match report

**Conclusion**: Only XGBoost matches the reported values. The other models should have different values.

## Root Cause Analysis

### Most Likely Explanation

The identical results in the report are likely due to one of these issues:

1. **Bug in Data Loading**: The script might be loading the same model's data for all models, or there's a caching issue
2. **Incorrect Model Directory**: The script might be pointing to the wrong directories
3. **Data Corruption**: The parquet files might have been overwritten or corrupted
4. **Calculation Error**: There might be a bug in how subject success rates are calculated when using sampled folds

### Recommended Actions

1. **Verify Data Loading**: Check that each model loads from its own directory
2. **Check File Integrity**: Verify that parquet files contain different predictions for different models
3. **Re-run Analysis**: Re-run the analysis script with additional debugging to track which data is being used
4. **Compare with Direct Calculation**: Use the direct calculation (all folds) as the ground truth

## Correct Values (Using All 50 Folds)

Based on direct calculation using all 50 folds:

| Model | Variance | Mean Success Rate |
|-------|----------|-------------------|
| KNN | 0.1292 | 83.62% |
| MLP | 0.1142 | 80.35% |
| SVM | 0.1835 | 75.77% |
| XGBoost | 0.1430 | 77.03% |

**Note**: These values are different, which is expected for different model architectures.

## Next Steps

1. Fix the analysis script to ensure correct data loading per model
2. Re-run the analysis to get correct per-model statistics
3. Update the summary report with corrected values
4. Investigate why the original script produced identical results

---

*Investigation Date: 2024-12-04*
*Script Used: `investigate_identical_results.py`*




