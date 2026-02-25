# 📋 Threshold Analysis Files Index

This document catalogs all threshold analysis markdown files created during this analysis session, with their status and relationships.

## ✅ **CURRENT & RECOMMENDED FILES**

### 1. **Main Comprehensive Report** ⭐ **START HERE**
- **File:** [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md)
- **Status:** ✅ **CURRENT - BEST VERSION**
- **Description:** 
  - Complete threshold analysis for ANOVA/PCA L_6 and L_2 experiments
  - **Compares Uniform (12-fold) vs Random (50-fold) on SAME test subjects**
  - Includes detailed methodology section
  - Per model×hyperparameter results
  - Subject filtering to ensure fair comparison
- **Key Features:**
  - Fair comparison: Uniform filtered to match random subjects
  - ANOVA_L_6: 45 same subjects
  - PCA_L_6: 65 same subjects
  - Complete calculation methods documented

### 2. **Uniform vs Random Summary** ⭐ **QUICK REFERENCE**
- **File:** [`UNIFORM_VS_RANDOM_SUMMARY.md`](UNIFORM_VS_RANDOM_SUMMARY.md)
- **Status:** ✅ **CURRENT - EXCELLENT SUMMARY**
- **Description:**
  - Concise summary comparing uniform vs random fold strategies
  - Key findings and recommendations
  - Model-by-model comparison tables
  - Includes methodology section
- **Use When:** You want a quick overview of uniform vs random differences

### 3. **Threshold Analysis Summary (L_6/L_2)**
- **File:** [`THRESHOLD_ANALYSIS_SUMMARY_L6_L2.md`](THRESHOLD_ANALYSIS_SUMMARY_L6_L2.md)
- **Status:** ✅ **CURRENT - GOOD SUMMARY**
- **Description:**
  - Summary of threshold analysis for ANOVA/PCA L_6/L_2 only
  - Key findings and optimal thresholds
  - Includes detailed calculation methods
- **Use When:** You want a summary focused on L_6/L_2 experiments

### 4. **Threshold vs Success Rate Comparison** (Different Purpose)
- **File:** [`THRESHOLD_ANALYSIS_VS_SUCCESS_RATE_COMPARISON.md`](THRESHOLD_ANALYSIS_VS_SUCCESS_RATE_COMPARISON.md)
- **Status:** ✅ **CURRENT - EXPLANATORY DOCUMENT**
- **Description:**
  - Explains the difference between two metrics:
    - "Classification Success Rate Variance" (percentage of subjects with >50% accuracy)
    - "Subject-Level Threshold Analysis" (percentage of subjects correctly classified)
  - **Different purpose** - not a threshold analysis report
- **Use When:** You're confused about the difference between these two metrics

### 5. **Uncertainty and Effect Size Analysis** ⭐ **STATISTICAL RIGOR**
- **File:** [`UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md`](../01_threshold_analysis/UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md)
- **Status:** ✅ **CURRENT - STATISTICAL RIGOR**
- **Description:**
  - Bootstrapped 95% confidence intervals for all accuracy estimates
  - Cliff's delta effect size measures (quantifies magnitude of differences)
  - Statistical significance testing (p-values)
  - Example format: "Random 50-fold: 88.9% [CI: 85.2–92.6%], Δ=4.5 pts (Cliff's δ=0.62)"
  - Methodology for bootstrap and effect size calculations
- **Use When:** You need statistical rigor, uncertainty quantification, or effect sizes for publications

### 6. **Same Subjects Control Flowchart** ⭐ **METHODOLOGY**
- **File:** [`SAME_SUBJECTS_CONTROL_FLOWCHART.md`](../01_threshold_analysis/SAME_SUBJECTS_CONTROL_FLOWCHART.md)
- **Status:** ✅ **CURRENT - METHODOLOGY DOCUMENTATION**
- **Description:**
  - Visual flowchart (Mermaid + ASCII) showing subject filtering process (65 → 45 subjects)
  - Step-by-step explanation of how uniform experiments were filtered to match random
  - Pre/post filtering accuracy comparison tables
  - Ensures fair comparison between Uniform and Random strategies
  - Implementation code snippets
- **Use When:** You need to understand or explain the subject filtering methodology

---

## ⚠️ **REPLACED / OUTDATED FILES**

### 5. **Final Subject Threshold Analysis** ❌ **REPLACED**
- **File:** [`final_subject_threshold_analysis.md`](final_subject_threshold_analysis.md)
- **Status:** ❌ **REPLACED by `anova_pca_L6_L2_threshold_analysis.md`**
- **Why Replaced:**
  - Only analyzed 4 experiments (ANOVA_L_2, ANOVA_L_6, PCA_L_2, PCA_L_6)
  - **No uniform vs random comparison**
  - **No subject filtering** (didn't ensure same subjects for fair comparison)
  - Less comprehensive methodology
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

### 6. **Comprehensive All Subjects Threshold Analysis** ❌ **REPLACED**
- **File:** [`comprehensive_all_subjects_threshold_analysis.md`](comprehensive_all_subjects_threshold_analysis.md)
- **Status:** ❌ **REPLACED by `anova_pca_L6_L2_threshold_analysis.md`**
- **Why Replaced:**
  - Only analyzed 4 hardcoded experiments
  - **No uniform vs random comparison**
  - **No subject filtering** between uniform and random
  - Less comprehensive
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

### 7. **All Experiments Threshold Analysis** ❌ **REPLACED**
- **File:** [`all_experiments_threshold_analysis.md`](all_experiments_threshold_analysis.md)
- **Status:** ❌ **REPLACED - TOO BROAD**
- **Why Replaced:**
  - Analyzed all 11 experiments (too many, includes experiments you don't care about)
  - User specifically requested **only ANOVA/PCA L_6/L_2**
  - No uniform vs random comparison initially
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

### 8. **Threshold Analysis Summary (All Experiments)** ❌ **REPLACED**
- **File:** [`THRESHOLD_ANALYSIS_SUMMARY.md`](THRESHOLD_ANALYSIS_SUMMARY.md)
- **Status:** ❌ **REPLACED - TOO BROAD**
- **Why Replaced:**
  - Summary of all 11 experiments
  - User specifically requested **only ANOVA/PCA L_6/L_2**
- **Better Version:** Use [`THRESHOLD_ANALYSIS_SUMMARY_L6_L2.md`](THRESHOLD_ANALYSIS_SUMMARY_L6_L2.md) instead

### 9. **Hyperparameter Specific Threshold Analysis** ❌ **REPLACED**
- **File:** [`hyperparameter_specific_threshold_analysis.md`](hyperparameter_specific_threshold_analysis.md)
- **Status:** ❌ **REPLACED - OLD VERSION**
- **Why Replaced:**
  - Older version without uniform vs random comparison
  - No subject filtering for fair comparison
  - Less comprehensive methodology
- **Better Version:** The main report [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) includes per-hyperparameter analysis

### 10. **Per Experiment Independent Threshold Analysis** ❌ **REPLACED**
- **File:** [`per_experiment_independent_threshold_analysis.md`](per_experiment_independent_threshold_analysis.md)
- **Status:** ❌ **REPLACED - INTERMEDIATE VERSION**
- **Why Replaced:**
  - Intermediate version during development
  - Replaced by more comprehensive versions
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

### 11. **Detailed Per Subject Threshold Analysis** ❌ **REPLACED**
- **File:** [`detailed_per_subject_threshold_analysis.md`](detailed_per_subject_threshold_analysis.md)
- **Status:** ❌ **REPLACED - INTERMEDIATE VERSION**
- **Why Replaced:**
  - Intermediate version with different granularity
  - Replaced by more comprehensive versions
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

### 12. **Stable Threshold Analysis** ❌ **REPLACED**
- **File:** [`stable_threshold_analysis.md`](stable_threshold_analysis.md)
- **Status:** ❌ **REPLACED - INTERMEDIATE VERSION**
- **Why Replaced:**
  - Intermediate version during development
  - Replaced by more comprehensive versions
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

### 13. **Clear Threshold Analysis** ❌ **REPLACED**
- **File:** [`clear_threshold_analysis.md`](clear_threshold_analysis.md)
- **Status:** ❌ **REPLACED - INTERMEDIATE VERSION**
- **Why Replaced:**
  - Intermediate version during development
  - Replaced by more comprehensive versions
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

### 14. **Subject Threshold Report** ❌ **REPLACED**
- **File:** [`subject_threshold_report.md`](subject_threshold_report.md)
- **Status:** ❌ **REPLACED - INTERMEDIATE VERSION**
- **Why Replaced:**
  - Intermediate version during development
  - Replaced by more comprehensive versions
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

### 15. **Final Classification Threshold Analysis** ❌ **REPLACED**
- **File:** [`final_classification_threshold_analysis.md`](final_classification_threshold_analysis.md)
- **Status:** ❌ **REPLACED - INTERMEDIATE VERSION**
- **Why Replaced:**
  - Intermediate version during development
  - Replaced by more comprehensive versions
- **Better Version:** Use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) instead

---

## 🔍 **DIFFERENT PURPOSE FILES** (Not Threshold Analysis)

### 16. **Classification Threshold Analysis Report** (Epoch-Level)
- **File:** [`classification_threshold_analysis_report.md`](classification_threshold_analysis_report.md)
- **Status:** ⚠️ **DIFFERENT PURPOSE - EPOCH-LEVEL, NOT SUBJECT-LEVEL**
- **Description:**
  - Analyzes **epoch-level** classification thresholds
  - Examines overall class distribution (AD vs Control at epoch level)
  - **NOT** subject-level threshold analysis
  - Different methodology and purpose
- **Use When:** You want to understand epoch-level class distribution, not subject-level classification

### 17. **Threshold Analysis Methodology** (May Be Redundant)
- **File:** [`THRESHOLD_ANALYSIS_METHODOLOGY.md`](THRESHOLD_ANALYSIS_METHODOLOGY.md)
- **Status:** ⚠️ **MAY BE REDUNDANT**
- **Description:**
  - Standalone methodology document
  - **Note:** Methodology is now included in the main report
- **Use When:** You want methodology in a separate document (though it's in the main report too)

---

## 📊 **QUICK REFERENCE GUIDE**

### For Main Analysis:
1. **Start Here:** [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) ⭐
2. **Quick Summary:** [`UNIFORM_VS_RANDOM_SUMMARY.md`](UNIFORM_VS_RANDOM_SUMMARY.md) ⭐
3. **L_6/L_2 Summary:** [`THRESHOLD_ANALYSIS_SUMMARY_L6_L2.md`](THRESHOLD_ANALYSIS_SUMMARY_L6_L2.md)

### For Understanding Metrics:
- **Metric Comparison:** [`THRESHOLD_ANALYSIS_VS_SUCCESS_RATE_COMPARISON.md`](THRESHOLD_ANALYSIS_VS_SUCCESS_RATE_COMPARISON.md)

### Files to Ignore (Replaced):
- `final_subject_threshold_analysis.md` → Use main report instead
- `comprehensive_all_subjects_threshold_analysis.md` → Use main report instead
- `all_experiments_threshold_analysis.md` → Use main report instead
- `hyperparameter_specific_threshold_analysis.md` → Use main report instead
- All other intermediate versions → Use main report instead

---

## 🎯 **KEY DIFFERENCES: CURRENT vs REPLACED**

| Feature | Replaced Files | Current Files |
|---------|---------------|---------------|
| **Experiments** | 4 hardcoded or all 11 | ANOVA/PCA L_6/L_2 only |
| **Uniform vs Random** | ❌ No comparison | ✅ Full comparison |
| **Subject Filtering** | ❌ No filtering | ✅ Same subjects for fair comparison |
| **Methodology** | ⚠️ Basic or missing | ✅ Comprehensive |
| **Subject Count** | Different denominators | ✅ Same denominators |

---

## 📝 **RECOMMENDATIONS**

1. **Primary File:** Always use [`anova_pca_L6_L2_threshold_analysis.md`](anova_pca_L6_L2_threshold_analysis.md) for complete analysis
2. **Quick Reference:** Use [`UNIFORM_VS_RANDOM_SUMMARY.md`](UNIFORM_VS_RANDOM_SUMMARY.md) for summaries
3. **Ignore Replaced Files:** Don't use files marked as ❌ REPLACED
4. **Different Purpose:** Understand that `classification_threshold_analysis_report.md` is epoch-level, not subject-level

---

*Last Updated: 2025-12-12*
*Files created during threshold analysis session*

