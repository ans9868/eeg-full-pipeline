# Markdown Files Index: HPC_All_Data Directory

This document lists all `.md` files in the HPC_All_Data directory and describes their content, with special focus on files analyzing variance across subjects in different folds.

## Files Focused on Variance Across Subjects in Different Folds

### 1. **CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md**
   - **Location**: `per_subject_classification_analysis/`
   - **Focus**: Variance in classification success rate (proportion of subjects with >50% accuracy) across different test group combinations
   - **Key Content**:
     - Analyzes variance of classification success rates across 30 random combinations of test groups
     - Shows how variance decreases as more test groups are included (1-15 groups)
     - Reports variance drops and stabilization points for each model×hyperparameter combination
     - Covers ANOVA_L_2_Random, ANOVA_L_6_Random, PCA_L_2_Random, PCA_L_6_Random experiments
   - **Key Finding**: Mean variance of 0.0044, with variance stabilizing as more subjects are included

### 2. **VARIANCE_ELBOW_ANALYSIS_REPORT.md**
   - **Location**: `per_subject_classification_analysis/`
   - **Focus**: Optimal number of test subjects needed for stable variance estimates (elbow point detection)
   - **Key Content**:
     - Uses aggregate fold-level accuracies from results.json
     - Calculates variance of fold-level accuracies across different combinations of test groups
     - Identifies "elbow points" where variance stabilizes
     - All 48 model×HP combinations show gradual stabilization at 3 test groups
   - **Key Finding**: 3 test groups (6 subjects for L_2, 18 subjects for L_6) sufficient for stable variance

### 3. **VARIANCE_ELBOW_ANALYSIS.md**
   - **Location**: `per_subject_classification_analysis/`
   - **Focus**: Detailed methodology for variance elbow analysis using aggregate fold accuracies
   - **Key Content**:
     - Explains calculation of variance of group means (not individual subjects)
     - Describes combination generation and sampling strategy (max 10,000 combinations)
     - Documents computational optimization approaches
     - Provides interpretation guide for elbow patterns
   - **Note**: This is the methodology document; see VARIANCE_ELBOW_ANALYSIS_REPORT.md for results

### 4. **DEEP_VARIANCE_ANALYSIS_REPORT.md**
   - **Location**: `per_subject_classification_analysis/`
   - **Focus**: Variance analysis using individual subject accuracies (not aggregate fold accuracies)
   - **Key Content**:
     - Calculates variance of all individual subject accuracies from test_predictions.parquet
     - Uses 30 random combinations per number of test groups
     - Identifies significant variance drops (>1%) and inflection points
     - Shows where variance first becomes "low" (below median + 10%)
   - **Key Finding**: Variance drops are very small (<2%), suggesting variance stabilizes early (around 3-6 test groups)

### 5. **fold_instability_tables.md**
   - **Location**: Root directory
   - **Focus**: Demonstrates dramatic variance in performance across individual LPSO folds
   - **Key Content**:
     - Shows single-fold performance ranges (e.g., SVM + ANOVA L_2: 16.9% to 92.6%, span of 75.7%)
     - Top 10 most variable model+feature combinations
     - Explains why median + IQR over many folds is required
     - Compares L_2 vs L_6 variance patterns
   - **Key Finding**: Single-fold performance can vary dramatically (up to 75.7 percentage points), requiring robust reporting with median + IQR

### 6. **table4_fold_variance_pca_lpso.md**
   - **Location**: Root directory
   - **Focus**: Fold-to-fold variance statistics for PCA LPSO experiments
   - **Key Content**:
     - Mean, IQR, Range, Std Dev, and Swing statistics for each model
     - Statistics computed across LPSO folds with P=6
     - Shows wide fold ranges (≈36-80%) across models
   - **Key Finding**: Same protocol yields wide fold ranges, underscoring need for mean ± IQR reporting

### 7. **biggest_cross_model_swings.md**
   - **Location**: Root directory
   - **Focus**: Subjects with largest accuracy differences across different model×hyperparameter combinations
   - **Key Content**:
     - Top 30 subjects ranked by swing (max - min accuracy across models)
     - Shows range, mean, and number of combinations for each subject
     - Identifies subjects that are highly sensitive to model choice
   - **Key Finding**: Some subjects show swings up to 74.1% (sub-3 in ANOVA_L_2_Random: 16.9% - 90.9%)

## General Analysis Files

### 8. **comprehensive_analysis_report.md**
   - **Location**: Root directory
   - **Focus**: Comprehensive comparison of grid_12_folds vs grid_50_random_folds experiments
   - **Key Content**:
     - Overall performance statistics and variance comparisons
     - Per-configuration and per-model performance analysis
     - ANOVA vs PCA performance differences
     - Statistical significance analysis
   - **Key Finding**: Grid 50 Random Folds shows 31.1% reduction in variance compared to Grid 12 Folds

### 9. **ANALYSIS_FILES_INDEX.md**
   - **Location**: Root directory
   - **Focus**: Index of per-subject accuracy analysis files
   - **Key Content**: Lists all per-subject analysis files and their purposes

### 10. **README_ANALYSIS.md**
   - **Location**: Root directory
   - **Focus**: Documentation for analysis scripts and generated files
   - **Key Content**: Explains how to run analysis scripts and what files they generate

### 11. **performance_tables.md**
   - **Location**: Root directory
   - **Focus**: Performance tables (likely summary statistics)
   - **Note**: File not read in detail, but likely contains performance summaries

## Per-Subject Classification Analysis Files

### 12. **per_subject_classification_analysis/README.md**
   - **Focus**: Overview of per-subject accuracy analysis directory
   - **Key Content**: Directory structure, file types, experiments analyzed

### 13. **per_subject_classification_analysis/ANALYSIS_METHODOLOGY.md**
   - **Focus**: Detailed methodology for calculating per-subject accuracy from parquet files
   - **Key Content**: Step-by-step process, validation, advantages of the method

### 14. **per_subject_classification_analysis/SUMMARY_ALL_EXPERIMENTS.md**
   - **Focus**: Overall summary across all experiments
   - **Key Content**: Combined statistics and findings

### 15. **per_subject_classification_analysis/INDEX.md**
   - **Focus**: Index of files in the per_subject_classification_analysis directory

### 16. **per_subject_classification_analysis/SUCCESS_RATE_CALCULATION_EXPLANATION.md**
   - **Focus**: Explanation of classification success rate calculation method
   - **Note**: File not read in detail

### 17. **per_subject_classification_analysis/COMPLETION_SUMMARY.md**
   - **Focus**: Summary of completed analyses
   - **Note**: File not read in detail

### 18. **per_subject_classification_analysis/per_subject_summary_all_experiments.md**
   - **Focus**: Combined per-subject summary across all experiments

### 19. **per_subject_classification_analysis/per_subject_tables_all_experiments.md**
   - **Focus**: Tables showing per-subject data across all experiments

## Per-Experiment Summary Files

### 20-25. **Experiment-specific per_subject_summary.md files**
   - **Locations**: `per_subject_classification_analysis/` and `old_per_subject_accuracy/`
   - **Experiments**: 
     - ANOVA_L_2_Random
     - ANOVA_L_6_Random
     - ANOVA_L_6_Uniform
     - PCA_L_2_Random
     - PCA_L_6_Random
     - PCA_L_6_Uniform
   - **Focus**: Per-subject accuracy statistics for each specific experiment

### 26-31. **Experiment-specific per_subject_tables.md files**
   - **Locations**: `per_subject_classification_analysis/`
   - **Focus**: Detailed tables for each experiment

## Comparison and Table Files

### 32. **table1_within_subject_performance.md**
   - **Focus**: Within-subject performance table

### 33. **table2_within_vs_lpso.md**
   - **Focus**: Comparison of within-subject vs LPSO performance

### 34. **table3_model_rankings_lpso.md**
   - **Focus**: Model rankings for LPSO experiments

### 35. **table_a_within_subject_control.md**
   - **Focus**: Within-subject control table

### 36. **table_b_cross_subject_summary.md**
   - **Focus**: Cross-subject summary table

### 37. **table_c_lpso_leaderboard.md**
   - **Focus**: LPSO leaderboard table

### 38. **table_d_holdout_sensitivity.md**
   - **Focus**: Holdout sensitivity analysis

### 39. **table1_source_info.md**
   - **Focus**: Source information for table 1

### 40. **p6_vs_p2_mean_comparison.md**
   - **Focus**: Comparison of P=6 vs P=2 mean performance

### 41. **p6_vs_p2_best_models_comparison.md**
   - **Focus**: Comparison of best models for P=6 vs P=2

### 42. **within_vs_lpso_p6_comparison.md**
   - **Focus**: Within-subject vs LPSO comparison for P=6

## Model-Specific Performance Files

### 43. **mlp_hidden100_tanh_alpha01_performance.md**
   - **Focus**: MLP performance with specific hyperparameters

### 44. **mlp_hidden100_tanh_alpha01_pca_l_2_performance.md**
   - **Focus**: MLP performance with PCA L_2 configuration

### 45. **mlp_hidden100_tanh_alpha01_anova_l_2_performance.md**
   - **Focus**: MLP performance with ANOVA L_2 configuration

### 46. **mlp_anova_fold_details.md**
   - **Focus**: Detailed MLP ANOVA fold analysis

## Old Analysis Files

### 47-52. **old_per_subject_accuracy/*.md**
   - **Focus**: Older versions of per-subject accuracy analyses
   - **Note**: These may be superseded by newer analyses in `per_subject_classification_analysis/`

## Summary

**Primary Files for Variance Across Subjects in Different Folds:**
1. `CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md` - Success rate variance analysis
2. `VARIANCE_ELBOW_ANALYSIS_REPORT.md` - Optimal subject count for stable variance
3. `DEEP_VARIANCE_ANALYSIS_REPORT.md` - Individual subject variance analysis
4. `fold_instability_tables.md` - Single-fold variance demonstration
5. `table4_fold_variance_pca_lpso.md` - Fold-to-fold variance statistics
6. `biggest_cross_model_swings.md` - Cross-model variance per subject

These files collectively provide comprehensive analysis of:
- How variance changes as more test groups/subjects are included
- Optimal number of subjects needed for stable variance estimates
- Variance patterns across different folds
- Subject-specific sensitivity to model choice
- Fold-to-fold performance variability






