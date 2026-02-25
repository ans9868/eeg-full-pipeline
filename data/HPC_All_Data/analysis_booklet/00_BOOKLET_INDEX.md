# 📚 EEG Analysis Booklet - Complete Documentation Index

**Generated:** December 12, 2025  
**Location:** `data/HPC_All_Data/analysis_booklet/`  
**Purpose:** Complete collection of all analysis markdown files organized by category

---

## 📋 Table of Contents

### [00. Booklet Index (This File)](00_BOOKLET_INDEX.md)
- Complete index of all analysis documents
- Navigation guide

---

## 🎯 01. Threshold Analysis

**Primary Analysis Files (Current & Recommended):**

1. **[anova_pca_L6_L2_threshold_analysis.md](01_threshold_analysis/anova_pca_L6_L2_threshold_analysis.md)** ⭐ **START HERE**
   - Complete threshold analysis for ANOVA/PCA L_6 and L_2
   - Uniform vs Random comparison on SAME test subjects
   - Comprehensive methodology included
   - **Status:** ✅ CURRENT - BEST VERSION

2. **[UNIFORM_VS_RANDOM_SUMMARY.md](01_threshold_analysis/UNIFORM_VS_RANDOM_SUMMARY.md)** ⭐
   - Quick reference: Uniform (12-fold) vs Random (50-fold) comparison
   - Key findings and recommendations
   - **Status:** ✅ CURRENT - EXCELLENT SUMMARY

3. **[THRESHOLD_ANALYSIS_SUMMARY_L6_L2.md](01_threshold_analysis/THRESHOLD_ANALYSIS_SUMMARY_L6_L2.md)**
   - Summary focused on ANOVA/PCA L_6/L_2 experiments
   - **Status:** ✅ CURRENT

4. **[THRESHOLD_ANALYSIS_VS_SUCCESS_RATE_COMPARISON.md](01_threshold_analysis/THRESHOLD_ANALYSIS_VS_SUCCESS_RATE_COMPARISON.md)**
   - Explains difference between two metrics
   - **Status:** ✅ CURRENT - EXPLANATORY

**Additional Files:**

5. [classification_threshold_analysis_report.md](01_threshold_analysis/classification_threshold_analysis_report.md) - Epoch-level analysis (different purpose, kept for reference)
6. [THRESHOLD_ANALYSIS_METHODOLOGY.md](01_threshold_analysis/THRESHOLD_ANALYSIS_METHODOLOGY.md) - Standalone methodology (also in main report, kept for standalone reference)

**Statistical Analysis & Methodology:**

7. **[UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md](01_threshold_analysis/UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md)** ⭐
   - Bootstrapped 95% confidence intervals for accuracy estimates
   - Cliff's delta effect size measures
   - Statistical significance testing
   - Example format: "Random 50-fold: 88.9% [CI: 85.2–92.6%], Δ=4.5 pts (Cliff's δ=0.62)"
   - **Status:** ✅ CURRENT - STATISTICAL RIGOR

8. **[SAME_SUBJECTS_CONTROL_FLOWCHART.md](01_threshold_analysis/SAME_SUBJECTS_CONTROL_FLOWCHART.md)** ⭐
   - Visual flowchart of subject filtering methodology (65 → 45 subjects)
   - Pre/post filtering accuracy comparison
   - Step-by-step process explanation
   - Ensures fair comparison between Uniform and Random strategies
   - **Status:** ✅ CURRENT - METHODOLOGY DOCUMENTATION

**Note:** All replaced/outdated files have been removed from the booklet. Only current versions remain.

---

## 👥 02. Per-Subject Classification Analysis

**Main Reports:**

1. **[SUBJECT_SUCCESS_RATE_VARIANCE_SUMMARY.md](02_per_subject_analysis/SUBJECT_SUCCESS_RATE_VARIANCE_SUMMARY.md)** ⭐
   - Per-subject success rate variance analysis (>50% accuracy threshold)
   - Analyzes how variance changes as more folds are included (1 to 50 folds)
   - Key findings on subject heterogeneity and variance stabilization
   - Includes correction note for ANOVA_L_6 results
   - **Status:** ✅ CURRENT - COMPREHENSIVE ANALYSIS

2. **[CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md](02_per_subject_analysis/CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md)**
   - Comprehensive variance report
   - Detailed methodology

3. **[SUMMARY_ALL_EXPERIMENTS.md](02_per_subject_analysis/SUMMARY_ALL_EXPERIMENTS.md)**
   - Summary across all experiments
   - Per-subject accuracy statistics

4. **[analysis_summary.md](02_per_subject_analysis/analysis_summary.md)**
   - Overall statistics
   - Per-model hyperparameter statistics

**Methodology & Explanations:**

5. [ANALYSIS_METHODOLOGY.md](02_per_subject_analysis/ANALYSIS_METHODOLOGY.md) - Methodology documentation
6. [SUCCESS_RATE_CALCULATION_EXPLANATION.md](02_per_subject_analysis/SUCCESS_RATE_CALCULATION_EXPLANATION.md) - Calculation methods
7. [IDENTICAL_RESULTS_INVESTIGATION.md](02_per_subject_analysis/IDENTICAL_RESULTS_INVESTIGATION.md) ⭐ - Investigation of identical results anomaly in ANOVA_L_6
   - Explains why all models appeared to have identical variance/success rates
   - Documents the investigation process and root cause
   - **Status:** ✅ CURRENT - IMPORTANT CORRECTION
8. [HYPERPARAMETER_VARIATIONS.md](02_per_subject_analysis/HYPERPARAMETER_VARIATIONS.md) ⭐ - Hyperparameter variations across experiments
   - Documents that no model×HP combinations have identical hyperparameters across all 4 experiments
   - Shows hyperparameter differences by model type (KNN, MLP, SVM, XGBoost)
   - **Status:** ✅ CURRENT - IMPORTANT FINDING

**Per-Experiment Tables:**

8. [ANOVA_L_2_Random_per_subject_tables.md](02_per_subject_analysis/ANOVA_L_2_Random_per_subject_tables.md)
9. [ANOVA_L_6_Random_per_subject_tables.md](02_per_subject_analysis/ANOVA_L_6_Random_per_subject_tables.md)
10. [PCA_L_2_Random_per_subject_tables.md](02_per_subject_analysis/PCA_L_2_Random_per_subject_tables.md)
11. [PCA_L_6_Random_per_subject_tables.md](02_per_subject_analysis/PCA_L_6_Random_per_subject_tables.md)
12. [per_subject_tables_all_experiments.md](02_per_subject_analysis/per_subject_tables_all_experiments.md)

**Per-Experiment Summaries:**

13. [ANOVA_L_2_Random_per_subject_summary.md](02_per_subject_analysis/ANOVA_L_2_Random_per_subject_summary.md)
14. [ANOVA_L_6_Random_per_subject_summary.md](02_per_subject_analysis/ANOVA_L_6_Random_per_subject_summary.md)
15. [PCA_L_2_Random_per_subject_summary.md](02_per_subject_analysis/PCA_L_2_Random_per_subject_summary.md)
16. [PCA_L_6_Random_per_subject_summary.md](02_per_subject_analysis/PCA_L_6_Random_per_subject_summary.md)
17. [PCA_L_6_Uniform_per_subject_summary.md](02_per_subject_analysis/PCA_L_6_Uniform_per_subject_summary.md)
18. [per_subject_summary_all_experiments.md](02_per_subject_analysis/per_subject_summary_all_experiments.md)

**Variance Analysis:**

19. [DEEP_VARIANCE_ANALYSIS_REPORT.md](02_per_subject_analysis/DEEP_VARIANCE_ANALYSIS_REPORT.md)
20. [VARIANCE_ELBOW_ANALYSIS_REPORT.md](02_per_subject_analysis/VARIANCE_ELBOW_ANALYSIS_REPORT.md)
21. [VARIANCE_ELBOW_ANALYSIS.md](02_per_subject_analysis/VARIANCE_ELBOW_ANALYSIS.md)

**Per-Model Hyperparameter Variance (16 reports):**

These reports analyze per-subject success rate variance (>50% accuracy) for each model×HP combination as more folds are included. Each report includes:
- Variance vs number of folds plots
- Mean success rate vs number of folds plots
- Detailed statistics table
- Variance stabilization analysis

22. [ANOVA_L_2_Random_subject_success_rate_variance_KNN_metric=euclidean_n_neighbors=7_weights=uniform.md](02_per_subject_analysis/ANOVA_L_2_Random_subject_success_rate_variance_KNN_metric=euclidean_n_neighbors=7_weights=uniform.md)
23. [ANOVA_L_2_Random_subject_success_rate_variance_MLP_Neural_Network_activation=tanh_alpha=01_hidden_layer_sizes=100.md](02_per_subject_analysis/ANOVA_L_2_Random_subject_success_rate_variance_MLP_Neural_Network_activation=tanh_alpha=01_hidden_layer_sizes=100.md)
24. [ANOVA_L_2_Random_subject_success_rate_variance_SVM_C=01_gamma=auto_kernel=rbf.md](02_per_subject_analysis/ANOVA_L_2_Random_subject_success_rate_variance_SVM_C=01_gamma=auto_kernel=rbf.md)
25. [ANOVA_L_2_Random_subject_success_rate_variance_XGBoost_learning_rate=02_max_depth=6_n_estimators=100_subsample=07.md](02_per_subject_analysis/ANOVA_L_2_Random_subject_success_rate_variance_XGBoost_learning_rate=02_max_depth=6_n_estimators=100_subsample=07.md)
26. [ANOVA_L_6_Random_subject_success_rate_variance_KNN_metric=euclidean_n_neighbors=15_weights=uniform.md](02_per_subject_analysis/ANOVA_L_6_Random_subject_success_rate_variance_KNN_metric=euclidean_n_neighbors=15_weights=uniform.md)
27. [ANOVA_L_6_Random_subject_success_rate_variance_MLP_Neural_Network_activation=tanh_alpha=01_hidden_layer_sizes=150_50.md](02_per_subject_analysis/ANOVA_L_6_Random_subject_success_rate_variance_MLP_Neural_Network_activation=tanh_alpha=01_hidden_layer_sizes=150_50.md)
28. [ANOVA_L_6_Random_subject_success_rate_variance_SVM_C=01_gamma=auto_kernel=linear.md](02_per_subject_analysis/ANOVA_L_6_Random_subject_success_rate_variance_SVM_C=01_gamma=auto_kernel=linear.md)
29. [ANOVA_L_6_Random_subject_success_rate_variance_XGBoost_learning_rate=02_max_depth=3_n_estimators=100_subsample=07.md](02_per_subject_analysis/ANOVA_L_6_Random_subject_success_rate_variance_XGBoost_learning_rate=02_max_depth=3_n_estimators=100_subsample=07.md)
30. [PCA_L_2_Random_subject_success_rate_variance_KNN_metric=euclidean_n_neighbors=1_weights=uniform.md](02_per_subject_analysis/PCA_L_2_Random_subject_success_rate_variance_KNN_metric=euclidean_n_neighbors=1_weights=uniform.md)
31. [PCA_L_2_Random_subject_success_rate_variance_MLP_Neural_Network_activation=tanh_alpha=01_hidden_layer_sizes=200_100_50.md](02_per_subject_analysis/PCA_L_2_Random_subject_success_rate_variance_MLP_Neural_Network_activation=tanh_alpha=01_hidden_layer_sizes=200_100_50.md)
32. [PCA_L_2_Random_subject_success_rate_variance_SVM_C=01_gamma=auto_kernel=rbf.md](02_per_subject_analysis/PCA_L_2_Random_subject_success_rate_variance_SVM_C=01_gamma=auto_kernel=rbf.md)
33. [PCA_L_2_Random_subject_success_rate_variance_XGBoost_learning_rate=02_max_depth=3_n_estimators=100_subsample=07.md](02_per_subject_analysis/PCA_L_2_Random_subject_success_rate_variance_XGBoost_learning_rate=02_max_depth=3_n_estimators=100_subsample=07.md)
34. [PCA_L_6_Random_subject_success_rate_variance_KNN_metric=euclidean_n_neighbors=7_weights=uniform.md](02_per_subject_analysis/PCA_L_6_Random_subject_success_rate_variance_KNN_metric=euclidean_n_neighbors=7_weights=uniform.md)
35. [PCA_L_6_Random_subject_success_rate_variance_MLP_Neural_Network_activation=tanh_alpha=01_hidden_layer_sizes=150_50.md](02_per_subject_analysis/PCA_L_6_Random_subject_success_rate_variance_MLP_Neural_Network_activation=tanh_alpha=01_hidden_layer_sizes=150_50.md)
36. [PCA_L_6_Random_subject_success_rate_variance_SVM_C=01_gamma=auto_kernel=poly.md](02_per_subject_analysis/PCA_L_6_Random_subject_success_rate_variance_SVM_C=01_gamma=auto_kernel=poly.md)
37. [PCA_L_6_Random_subject_success_rate_variance_XGBoost_learning_rate=02_max_depth=6_n_estimators=100_subsample=07.md](02_per_subject_analysis/PCA_L_6_Random_subject_success_rate_variance_XGBoost_learning_rate=02_max_depth=6_n_estimators=100_subsample=07.md)

**Other Files:**

39. [INDEX.md](02_per_subject_analysis/INDEX.md)
40. [README.md](02_per_subject_analysis/README.md)
41. [COMPLETION_SUMMARY.md](02_per_subject_analysis/COMPLETION_SUMMARY.md)

**Note:** HYPERPARAMETER_VARIATIONS.md is listed above in the Methodology section (item #8).

---

## 🔍 03. Clustering Analysis

1. [clustering_results_summary.md](03_clustering/clustering_results_summary.md)
2. [clustering_analysis_summary.md](03_clustering/clustering_analysis_summary.md)

---

## 📊 04. Performance Tables

1. [performance_tables.md](04_performance_tables/performance_tables.md)
2. [fold_instability_tables.md](04_performance_tables/fold_instability_tables.md)
3. [mlp_hidden100_tanh_alpha01_performance.md](04_performance_tables/mlp_hidden100_tanh_alpha01_performance.md)
4. [mlp_anova_fold_details.md](04_performance_tables/mlp_anova_fold_details.md)
5. [mlp_hidden100_tanh_alpha01_anova_l_2_performance.md](04_performance_tables/mlp_hidden100_tanh_alpha01_anova_l_2_performance.md)
6. [mlp_hidden100_tanh_alpha01_pca_l_2_performance.md](04_performance_tables/mlp_hidden100_tanh_alpha01_pca_l_2_performance.md)
7. [table1_source_info.md](04_performance_tables/table1_source_info.md)
8. [table4_fold_variance_pca_lpso.md](04_performance_tables/table4_fold_variance_pca_lpso.md)
9. [table5_fold_variance_anova_lpso.md](04_performance_tables/table5_fold_variance_anova_lpso.md)
10. [table6_fold_variance_pca_lpso.md](04_performance_tables/table6_fold_variance_pca_lpso.md)
11. [table7_fold_variance_anova_lpso.md](04_performance_tables/table7_fold_variance_anova_lpso.md)
12. [table8_fold_variance_pca_lpso.md](04_performance_tables/table8_fold_variance_pca_lpso.md)
13. [table9_fold_variance_anova_lpso.md](04_performance_tables/table9_fold_variance_anova_lpso.md)
14. [table10_fold_variance_pca_lpso.md](04_performance_tables/table10_fold_variance_pca_lpso.md)
15. [table11_fold_variance_anova_lpso.md](04_performance_tables/table11_fold_variance_anova_lpso.md)
16. [table12_fold_variance_pca_lpso.md](04_performance_tables/table12_fold_variance_pca_lpso.md)
17. [table13_fold_variance_anova_lpso.md](04_performance_tables/table13_fold_variance_anova_lpso.md)
18. [table14_fold_variance_pca_lpso.md](04_performance_tables/table14_fold_variance_pca_lpso.md)
19. [table15_fold_variance_anova_lpso.md](04_performance_tables/table15_fold_variance_anova_lpso.md)
20. [table16_fold_variance_pca_lpso.md](04_performance_tables/table16_fold_variance_pca_lpso.md)
21. [table17_fold_variance_anova_lpso.md](04_performance_tables/table17_fold_variance_anova_lpso.md)
22. [table18_fold_variance_pca_lpso.md](04_performance_tables/table18_fold_variance_pca_lpso.md)
23. [table19_fold_variance_anova_lpso.md](04_performance_tables/table19_fold_variance_anova_lpso.md)
24. [table20_fold_variance_pca_lpso.md](04_performance_tables/table20_fold_variance_pca_lpso.md)
25. [table21_fold_variance_anova_lpso.md](04_performance_tables/table21_fold_variance_anova_lpso.md)
26. [table22_fold_variance_pca_lpso.md](04_performance_tables/table22_fold_variance_pca_lpso.md)
27. [table23_fold_variance_anova_lpso.md](04_performance_tables/table23_fold_variance_anova_lpso.md)
28. [table24_fold_variance_pca_lpso.md](04_performance_tables/table24_fold_variance_pca_lpso.md)
29. [table25_fold_variance_anova_lpso.md](04_performance_tables/table25_fold_variance_anova_lpso.md)
30. [table26_fold_variance_pca_lpso.md](04_performance_tables/table26_fold_variance_pca_lpso.md)
31. [table27_fold_variance_anova_lpso.md](04_performance_tables/table27_fold_variance_anova_lpso.md)
32. [table28_fold_variance_pca_lpso.md](04_performance_tables/table28_fold_variance_pca_lpso.md)
33. [table29_fold_variance_anova_lpso.md](04_performance_tables/table29_fold_variance_anova_lpso.md)
34. [table30_fold_variance_pca_lpso.md](04_performance_tables/table30_fold_variance_pca_lpso.md)
35. [table31_fold_variance_anova_lpso.md](04_performance_tables/table31_fold_variance_anova_lpso.md)
36. [table32_fold_variance_pca_lpso.md](04_performance_tables/table32_fold_variance_pca_lpso.md)
37. [table33_fold_variance_anova_lpso.md](04_performance_tables/table33_fold_variance_anova_lpso.md)
38. [table34_fold_variance_pca_lpso.md](04_performance_tables/table34_fold_variance_pca_lpso.md)
39. [table35_fold_variance_anova_lpso.md](04_performance_tables/table35_fold_variance_anova_lpso.md)
40. [table36_fold_variance_pca_lpso.md](04_performance_tables/table36_fold_variance_pca_lpso.md)
41. [table37_fold_variance_anova_lpso.md](04_performance_tables/table37_fold_variance_anova_lpso.md)
42. [table38_fold_variance_pca_lpso.md](04_performance_tables/table38_fold_variance_pca_lpso.md)
43. [table39_fold_variance_anova_lpso.md](04_performance_tables/table39_fold_variance_anova_lpso.md)
44. [table40_fold_variance_pca_lpso.md](04_performance_tables/table40_fold_variance_pca_lpso.md)
45. [table41_fold_variance_anova_lpso.md](04_performance_tables/table41_fold_variance_anova_lpso.md)
46. [table42_fold_variance_pca_lpso.md](04_performance_tables/table42_fold_variance_pca_lpso.md)
47. [table43_fold_variance_anova_lpso.md](04_performance_tables/table43_fold_variance_anova_lpso.md)
48. [table44_fold_variance_pca_lpso.md](04_performance_tables/table44_fold_variance_pca_lpso.md)
49. [table45_fold_variance_anova_lpso.md](04_performance_tables/table45_fold_variance_anova_lpso.md)
50. [table46_fold_variance_pca_lpso.md](04_performance_tables/table46_fold_variance_pca_lpso.md)
51. [table47_fold_variance_anova_lpso.md](04_performance_tables/table47_fold_variance_anova_lpso.md)
52. [table48_fold_variance_pca_lpso.md](04_performance_tables/table48_fold_variance_pca_lpso.md)
53. [table49_fold_variance_anova_lpso.md](04_performance_tables/table49_fold_variance_anova_lpso.md)
54. [table50_fold_variance_pca_lpso.md](04_performance_tables/table50_fold_variance_pca_lpso.md)
55. [table51_fold_variance_anova_lpso.md](04_performance_tables/table51_fold_variance_anova_lpso.md)
56. [table52_fold_variance_pca_lpso.md](04_performance_tables/table52_fold_variance_pca_lpso.md)
57. [table53_fold_variance_anova_lpso.md](04_performance_tables/table53_fold_variance_anova_lpso.md)
58. [table54_fold_variance_pca_lpso.md](04_performance_tables/table54_fold_variance_pca_lpso.md)
59. [table55_fold_variance_anova_lpso.md](04_performance_tables/table55_fold_variance_anova_lpso.md)
60. [table56_fold_variance_pca_lpso.md](04_performance_tables/table56_fold_variance_pca_lpso.md)
61. [table57_fold_variance_anova_lpso.md](04_performance_tables/table57_fold_variance_anova_lpso.md)
62. [table58_fold_variance_pca_lpso.md](04_performance_tables/table58_fold_variance_pca_lpso.md)
63. [table59_fold_variance_anova_lpso.md](04_performance_tables/table59_fold_variance_anova_lpso.md)
64. [table60_fold_variance_pca_lpso.md](04_performance_tables/table60_fold_variance_pca_lpso.md)
65. [table61_fold_variance_anova_lpso.md](04_performance_tables/table61_fold_variance_anova_lpso.md)
66. [table62_fold_variance_pca_lpso.md](04_performance_tables/table62_fold_variance_pca_lpso.md)
67. [table63_fold_variance_anova_lpso.md](04_performance_tables/table63_fold_variance_anova_lpso.md)
68. [table64_fold_variance_pca_lpso.md](04_performance_tables/table64_fold_variance_pca_lpso.md)
69. [table65_fold_variance_anova_lpso.md](04_performance_tables/table65_fold_variance_anova_lpso.md)
70. [table66_fold_variance_pca_lpso.md](04_performance_tables/table66_fold_variance_pca_lpso.md)
71. [table67_fold_variance_anova_lpso.md](04_performance_tables/table67_fold_variance_anova_lpso.md)
72. [table68_fold_variance_pca_lpso.md](04_performance_tables/table68_fold_variance_pca_lpso.md)
73. [table69_fold_variance_anova_lpso.md](04_performance_tables/table69_fold_variance_anova_lpso.md)
74. [table70_fold_variance_pca_lpso.md](04_performance_tables/table70_fold_variance_pca_lpso.md)
75. [table71_fold_variance_anova_lpso.md](04_performance_tables/table71_fold_variance_anova_lpso.md)
76. [table72_fold_variance_pca_lpso.md](04_performance_tables/table72_fold_variance_pca_lpso.md)
77. [table73_fold_variance_anova_lpso.md](04_performance_tables/table73_fold_variance_anova_lpso.md)
78. [table74_fold_variance_pca_lpso.md](04_performance_tables/table74_fold_variance_pca_lpso.md)
79. [table75_fold_variance_anova_lpso.md](04_performance_tables/table75_fold_variance_anova_lpso.md)
80. [table76_fold_variance_pca_lpso.md](04_performance_tables/table76_fold_variance_pca_lpso.md)
81. [table77_fold_variance_anova_lpso.md](04_performance_tables/table77_fold_variance_anova_lpso.md)
82. [table78_fold_variance_pca_lpso.md](04_performance_tables/table78_fold_variance_pca_lpso.md)
83. [table79_fold_variance_anova_lpso.md](04_performance_tables/table79_fold_variance_anova_lpso.md)
84. [table80_fold_variance_pca_lpso.md](04_performance_tables/table80_fold_variance_pca_lpso.md)
85. [table81_fold_variance_anova_lpso.md](04_performance_tables/table81_fold_variance_anova_lpso.md)
86. [table82_fold_variance_pca_lpso.md](04_performance_tables/table82_fold_variance_pca_lpso.md)
87. [table83_fold_variance_anova_lpso.md](04_performance_tables/table83_fold_variance_anova_lpso.md)
88. [table84_fold_variance_pca_lpso.md](04_performance_tables/table84_fold_variance_pca_lpso.md)
89. [table85_fold_variance_anova_lpso.md](04_performance_tables/table85_fold_variance_anova_lpso.md)
90. [table86_fold_variance_pca_lpso.md](04_performance_tables/table86_fold_variance_pca_lpso.md)
91. [table87_fold_variance_anova_lpso.md](04_performance_tables/table87_fold_variance_anova_lpso.md)
92. [table88_fold_variance_pca_lpso.md](04_performance_tables/table88_fold_variance_pca_lpso.md)
93. [table89_fold_variance_anova_lpso.md](04_performance_tables/table89_fold_variance_anova_lpso.md)
94. [table90_fold_variance_pca_lpso.md](04_performance_tables/table90_fold_variance_pca_lpso.md)
95. [table91_fold_variance_anova_lpso.md](04_performance_tables/table91_fold_variance_anova_lpso.md)
96. [table92_fold_variance_pca_lpso.md](04_performance_tables/table92_fold_variance_pca_lpso.md)
97. [table93_fold_variance_anova_lpso.md](04_performance_tables/table93_fold_variance_anova_lpso.md)
98. [table94_fold_variance_pca_lpso.md](04_performance_tables/table94_fold_variance_pca_lpso.md)
99. [table95_fold_variance_anova_lpso.md](04_performance_tables/table95_fold_variance_anova_lpso.md)
100. [table96_fold_variance_pca_lpso.md](04_performance_tables/table96_fold_variance_pca_lpso.md)
101. [table97_fold_variance_anova_lpso.md](04_performance_tables/table97_fold_variance_anova_lpso.md)
102. [table98_fold_variance_pca_lpso.md](04_performance_tables/table98_fold_variance_pca_lpso.md)
103. [table99_fold_variance_anova_lpso.md](04_performance_tables/table99_fold_variance_anova_lpso.md)
104. [table100_fold_variance_pca_lpso.md](04_performance_tables/table100_fold_variance_pca_lpso.md)
105. [table101_fold_variance_anova_lpso.md](04_performance_tables/table101_fold_variance_anova_lpso.md)
106. [table102_fold_variance_pca_lpso.md](04_performance_tables/table102_fold_variance_pca_lpso.md)
107. [table103_fold_variance_anova_lpso.md](04_performance_tables/table103_fold_variance_anova_lpso.md)
108. [table104_fold_variance_pca_lpso.md](04_performance_tables/table104_fold_variance_pca_lpso.md)
109. [table105_fold_variance_anova_lpso.md](04_performance_tables/table105_fold_variance_anova_lpso.md)
110. [table106_fold_variance_pca_lpso.md](04_performance_tables/table106_fold_variance_pca_lpso.md)
111. [table107_fold_variance_anova_lpso.md](04_performance_tables/table107_fold_variance_anova_lpso.md)
112. [table108_fold_variance_pca_lpso.md](04_performance_tables/table108_fold_variance_pca_lpso.md)
113. [table109_fold_variance_anova_lpso.md](04_performance_tables/table109_fold_variance_anova_lpso.md)
114. [table110_fold_variance_pca_lpso.md](04_performance_tables/table110_fold_variance_pca_lpso.md)
115. [table111_fold_variance_anova_lpso.md](04_performance_tables/table111_fold_variance_anova_lpso.md)
116. [table112_fold_variance_pca_lpso.md](04_performance_tables/table112_fold_variance_pca_lpso.md)
117. [table113_fold_variance_anova_lpso.md](04_performance_tables/table113_fold_variance_anova_lpso.md)
118. [table114_fold_variance_pca_lpso.md](04_performance_tables/table114_fold_variance_pca_lpso.md)
119. [table115_fold_variance_anova_lpso.md](04_performance_tables/table115_fold_variance_anova_lpso.md)
120. [table116_fold_variance_pca_lpso.md](04_performance_tables/table116_fold_variance_pca_lpso.md)
121. [table117_fold_variance_anova_lpso.md](04_performance_tables/table117_fold_variance_anova_lpso.md)
122. [table118_fold_variance_pca_lpso.md](04_performance_tables/table118_fold_variance_pca_lpso.md)
123. [table119_fold_variance_anova_lpso.md](04_performance_tables/table119_fold_variance_anova_lpso.md)
124. [table120_fold_variance_pca_lpso.md](04_performance_tables/table120_fold_variance_pca_lpso.md)
125. [table121_fold_variance_anova_lpso.md](04_performance_tables/table121_fold_variance_anova_lpso.md)
122. [table122_fold_variance_pca_lpso.md](04_performance_tables/table122_fold_variance_pca_lpso.md)
123. [table123_fold_variance_anova_lpso.md](04_performance_tables/table123_fold_variance_anova_lpso.md)
124. [table124_fold_variance_pca_lpso.md](04_performance_tables/table124_fold_variance_pca_lpso.md)
125. [table125_fold_variance_anova_lpso.md](04_performance_tables/table125_fold_variance_anova_lpso.md)
126. [table126_fold_variance_pca_lpso.md](04_performance_tables/table126_fold_variance_pca_lpso.md)
127. [table127_fold_variance_anova_lpso.md](04_performance_tables/table127_fold_variance_anova_lpso.md)
128. [table128_fold_variance_pca_lpso.md](04_performance_tables/table128_fold_variance_pca_lpso.md)
129. [table129_fold_variance_anova_lpso.md](04_performance_tables/table129_fold_variance_anova_lpso.md)
130. [table130_fold_variance_pca_lpso.md](04_performance_tables/table130_fold_variance_pca_lpso.md)
131. [table131_fold_variance_anova_lpso.md](04_performance_tables/table131_fold_variance_anova_lpso.md)
132. [table132_fold_variance_pca_lpso.md](04_performance_tables/table132_fold_variance_pca_lpso.md)
133. [table133_fold_variance_anova_lpso.md](04_performance_tables/table133_fold_variance_anova_lpso.md)
134. [table134_fold_variance_pca_lpso.md](04_performance_tables/table134_fold_variance_pca_lpso.md)
135. [table135_fold_variance_anova_lpso.md](04_performance_tables/table135_fold_variance_anova_lpso.md)
136. [table136_fold_variance_pca_lpso.md](04_performance_tables/table136_fold_variance_pca_lpso.md)
137. [table137_fold_variance_anova_lpso.md](04_performance_tables/table137_fold_variance_anova_lpso.md)
138. [table138_fold_variance_pca_lpso.md](04_performance_tables/table138_fold_variance_pca_lpso.md)
139. [table139_fold_variance_anova_lpso.md](04_performance_tables/table139_fold_variance_anova_lpso.md)
140. [table140_fold_variance_pca_lpso.md](04_performance_tables/table140_fold_variance_pca_lpso.md)
141. [table141_fold_variance_anova_lpso.md](04_performance_tables/table141_fold_variance_anova_lpso.md)
142. [table142_fold_variance_pca_lpso.md](04_performance_tables/table142_fold_variance_pca_lpso.md)
143. [table143_fold_variance_anova_lpso.md](04_performance_tables/table143_fold_variance_anova_lpso.md)
144. [table144_fold_variance_pca_lpso.md](04_performance_tables/table144_fold_variance_pca_lpso.md)
145. [table145_fold_variance_anova_lpso.md](04_performance_tables/table145_fold_variance_anova_lpso.md)
146. [table146_fold_variance_pca_lpso.md](04_performance_tables/table146_fold_variance_pca_lpso.md)
147. [table147_fold_variance_anova_lpso.md](04_performance_tables/table147_fold_variance_anova_lpso.md)
148. [table148_fold_variance_pca_lpso.md](04_performance_tables/table148_fold_variance_pca_lpso.md)
149. [table149_fold_variance_anova_lpso.md](04_performance_tables/table149_fold_variance_anova_lpso.md)
150. [table150_fold_variance_pca_lpso.md](04_performance_tables/table150_fold_variance_pca_lpso.md)

---

## 📈 05. Other Analyses

1. [comprehensive_analysis_report.md](05_other_analyses/comprehensive_analysis_report.md)
2. **[effects_of_holdout_size_p_on_variance.md](05_other_analyses/effects_of_holdout_size_p_on_variance.md)** — **Figure 4: Variance vs Hold-Out Size (P)** (P=6 vs P=2, PCA & ANOVA)
3. [p6_vs_p2_mean_comparison.md](05_other_analyses/p6_vs_p2_mean_comparison.md)
4. [p6_vs_p2_best_models_comparison.md](05_other_analyses/p6_vs_p2_best_models_comparison.md)
5. [biggest_cross_model_swings.md](05_other_analyses/biggest_cross_model_swings.md)
6. [within_vs_lpso_p6_comparison.md](05_other_analyses/within_vs_lpso_p6_comparison.md)

---

## 🔬 07. Biomarker Analysis

**Main Report:**

1. **[ANALYSIS_SUMMARY.md](07_biomarkers/ANALYSIS_SUMMARY.md)** ⭐ **START HERE**
   - Complete biomarker analysis summary
   - Top 10 biomarkers reference table
   - Posterior Alpha reduction findings
   - Clustering analysis results
   - **Status:** ✅ CURRENT - PRIMARY FILE

**Key Files:**

2. **[top10_biomarkers_table.csv](07_biomarkers/top10_biomarkers_table.csv)**
   - Clean reference table with means, ratios, Cohen's d
   - All features FDR-corrected (q=0.05)
   - Ready-to-use for feature selection

**Key Visualizations:**

3. **[key_plot1_posterior_alpha_boxplots.png](07_biomarkers/key_plot1_posterior_alpha_boxplots.png)**
   - Posterior channels Alpha band boxplots (O1, O2, T5, T6, Pz)
   - Clear separation between Alzheimer's and Control groups

4. **[key_plot2_stacked_relative_bands.png](07_biomarkers/key_plot2_stacked_relative_bands.png)**
   - Stacked relative bandpower at O1 and O2
   - Visualizes Alpha reduction and Delta elevation patterns

**Key Findings:**
- **O2 × Alpha**: Strongest biomarker (Cohen's d = 0.797, Ratio = 2.66)
- **83/95 features** significant after FDR correction
- **Posterior Alpha reduction** is dominant pattern
- **Clustering reveals disease heterogeneity** (k=3 optimal)
- **Connection to CV results**: These features align with ~89% subject-level accuracy models

---

## 📊 08. Variance Analysis

**Main Reports:**

1. **[ANOVA_PCA_VARIANCE_COMPARISON.md](08_variance_analysis/ANOVA_PCA_VARIANCE_COMPARISON.md)** ⭐ **START HERE - COMPARATIVE ANALYSIS**
   - Comprehensive comparison of ANOVA vs PCA feature extraction methods
   - Model-specific recommendations (XGBoost, MLP, SVM, KNN)
   - Feature extraction method selection guidelines
   - Performance and stability rankings
   - **Status:** ✅ CURRENT - COMPREHENSIVE COMPARISON

2. **[PCA_VARIANCE_ANALYSIS_SUMMARY.md](08_variance_analysis/PCA_VARIANCE_ANALYSIS_SUMMARY.md)** ⭐
   - Analysis of variance in accuracy across 9 experiments for PCA_W_F and PCA_W_C
   - Variance rankings for all 12 model configurations
   - Key findings on model stability and consistency
   - ✅ **XGBoost coverage complete** (all 9 experiments)
   - **Status:** ✅ CURRENT - UPDATED WITH COMPLETE XGBOOST COVERAGE

3. **[ANOVA_VARIANCE_ANALYSIS_SUMMARY.md](08_variance_analysis/ANOVA_VARIANCE_ANALYSIS_SUMMARY.md)** ⭐
   - Analysis of variance in accuracy across 9 experiments for ANOVA_W_F and ANOVA_W_C
   - Variance rankings for all 12 model configurations
   - XGBoost dominance identified (~97-98% accuracy, extremely low variance)
   - **Status:** ✅ CURRENT - NEW ANALYSIS

**Key Findings:**

**PCA Features:**
- **MLP models** show highest accuracy (~96-98%) with very low variance
- **XGBoost** shows good accuracy (~89-90%) with low variance (all 9 experiments)
- **SVM (linear)** shows high accuracy (~94%) with low variance
- **KNN models** show moderate accuracy (~64-66%) with highest variance

**ANOVA Features:**
- **XGBoost** shows best performance (~97-98% accuracy, extremely low variance)
- **MLP** shows variable performance (89-94% accuracy, higher variance for complex architectures)
- **SVM (rbf/poly)** show very poor performance (~3-4% accuracy) - should be excluded
- **KNN** shows moderate performance (~52-54% accuracy) with low variance

**Visualizations:**
- `data/intra-subject/PCA_W_F/variance_boxplot_all_models.png`
- `data/intra-subject/PCA_W_C/variance_boxplot_all_models.png`
- `data/intra-subject/ANOVA_W_F/variance_boxplot_all_models.png`
- `data/intra-subject/ANOVA_W_C/variance_boxplot_all_models.png`
- Summary CSV tables in respective directories

---

## 📑 06. Indexes & Documentation

1. **[THRESHOLD_ANALYSIS_FILES_INDEX.md](06_indexes/THRESHOLD_ANALYSIS_FILES_INDEX.md)** ⭐
   - Complete index of threshold analysis files
   - Status of each file (current vs replaced)
   - **Use this to understand which files to use**

2. **[markdown_files_index.md](06_indexes/markdown_files_index.md)** ⭐ **NEW**
   - Complete index of all `.md` files in HPC_All_Data directory
   - Focuses on variance across subjects in different folds
   - Lists and describes all markdown files with their purposes
   - **Useful for finding variance-related analyses**

3. [ANALYSIS_FILES_INDEX.md](06_indexes/ANALYSIS_FILES_INDEX.md)
4. [README_ANALYSIS.md](06_indexes/README_ANALYSIS.md)

---

## 🎯 Quick Start Guide

### For Threshold Analysis:
1. **Start Here:** [anova_pca_L6_L2_threshold_analysis.md](01_threshold_analysis/anova_pca_L6_L2_threshold_analysis.md)
2. **Quick Summary:** [UNIFORM_VS_RANDOM_SUMMARY.md](01_threshold_analysis/UNIFORM_VS_RANDOM_SUMMARY.md)
3. **Statistical Rigor:** [UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md](01_threshold_analysis/UNCERTAINTY_AND_EFFECT_SIZE_ANALYSIS.md) - Bootstrapped CIs & effect sizes
4. **Methodology:** [SAME_SUBJECTS_CONTROL_FLOWCHART.md](01_threshold_analysis/SAME_SUBJECTS_CONTROL_FLOWCHART.md) - Subject filtering process
5. **File Status:** [THRESHOLD_ANALYSIS_FILES_INDEX.md](06_indexes/THRESHOLD_ANALYSIS_FILES_INDEX.md)

### For Per-Subject Analysis:
1. **[SUBJECT_SUCCESS_RATE_VARIANCE_SUMMARY.md](02_per_subject_analysis/SUBJECT_SUCCESS_RATE_VARIANCE_SUMMARY.md)** ⭐ START HERE
   - Per-subject success rate variance analysis (how variance changes with more folds)
   - Includes all plots and key findings
   - Correction note for ANOVA_L_6 results
2. [CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md](02_per_subject_analysis/CLASSIFICATION_SUCCESS_RATE_VARIANCE_REPORT.md)
3. [HYPERPARAMETER_VARIATIONS.md](02_per_subject_analysis/HYPERPARAMETER_VARIATIONS.md) - Hyperparameter differences across experiments
4. [IDENTICAL_RESULTS_INVESTIGATION.md](02_per_subject_analysis/IDENTICAL_RESULTS_INVESTIGATION.md) - Investigation of anomalies

### For Understanding Metrics:
1. [THRESHOLD_ANALYSIS_VS_SUCCESS_RATE_COMPARISON.md](01_threshold_analysis/THRESHOLD_ANALYSIS_VS_SUCCESS_RATE_COMPARISON.md)

### For Biomarker Analysis:
1. **[ANALYSIS_SUMMARY.md](07_biomarkers/ANALYSIS_SUMMARY.md)** ⭐ START HERE
2. [top10_biomarkers_table.csv](07_biomarkers/top10_biomarkers_table.csv) - Quick reference table

### For Variance Analysis:
1. **[ANOVA_PCA_VARIANCE_COMPARISON.md](08_variance_analysis/ANOVA_PCA_VARIANCE_COMPARISON.md)** ⭐ START HERE
   - Comprehensive comparison of ANOVA vs PCA feature extraction
   - Model-specific recommendations
   - Feature extraction method selection guidelines
2. **[PCA_VARIANCE_ANALYSIS_SUMMARY.md](08_variance_analysis/PCA_VARIANCE_ANALYSIS_SUMMARY.md)**
   - Variance analysis across 9 PCA experiments
   - Model stability rankings
   - Complete XGBoost coverage (all 9 experiments)
3. **[ANOVA_VARIANCE_ANALYSIS_SUMMARY.md](08_variance_analysis/ANOVA_VARIANCE_ANALYSIS_SUMMARY.md)**
   - Variance analysis across 9 ANOVA experiments
   - XGBoost dominance analysis
   - Model performance rankings

---

## 📊 Statistics

- **Total Files:** 82 markdown files (cleaned - removed 11 replaced/outdated files, added markdown_files_index.md and variance analyses)
- **Categories:** 8 main categories (added Biomarker Analysis and Variance Analysis)
- **Primary Analysis Files:** 10 current/recommended files (added ANOVA variance analysis and comparison)
- **Index Files:** 4 files (added markdown_files_index.md for comprehensive .md file listing)
- **Status:** All files copied (not moved) from original locations
- **Cleanup:** Removed all replaced/outdated intermediate versions

---

*Booklet created: December 12, 2025*  
*All files are copies - originals remain in their original locations*


