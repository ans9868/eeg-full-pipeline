# Per-Subject Accuracy Analysis by Model × Hyperparameter (Improved)

## Summary

This report includes:
- Fixed naming consistency (n_neighbors, learning_rate, etc.)
- Fold comparability information
- Minimum evidence filter (N Folds >= 3 in main table)
- 95% Confidence Intervals and Standard Errors
- Verified swing calculation (max - min)
- Experiment type labeling (uniform vs random)

## Top 30 Subjects with Largest Cross-Model Swings

| Rank | Subject | Experiment | Type | Swing | Range (Min-Max) | Mean | N Combos | Min Model×HP | Max Model×HP |
|------|---------|------------|------|-------|----------------|------|----------|--------------|-------------|
| 1 | sub-3 | ANOVA_L_2_Random | random | 74.1% | 16.9% - 90.9% | 69.0% | 5 | SVM (kernel=poly, C=0.1, gamma=auto) | XGBoost (learning_rate=unknown, max_depth=unknown, |
| 2 | sub-60 | ANOVA_L_2_Random | random | 61.1% | 16.9% - 78.0% | 55.2% | 4 | SVM (kernel=poly, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 3 | sub-11 | ANOVA_L_2_Random | random | 52.4% | 40.0% - 92.5% | 65.6% | 7 | SVM (kernel=rbf, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 4 | sub-30 | PCA_L_2_Random | random | 52.1% | 38.3% - 90.4% | 56.8% | 8 | SVM (kernel=linear, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 5 | sub-18 | PCA_L_2_Random | random | 49.6% | 37.4% - 87.0% | 54.4% | 12 | KNN (n_neighbors=unknown, metric=euclidean, weight | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 6 | sub-3 | PCA_L_2_Random | random | 47.9% | 28.3% - 76.2% | 49.4% | 8 | KNN (n_neighbors=unknown, metric=euclidean, weight | KNN (n_neighbors=unknown, metric=euclidean, weight |
| 7 | sub-18 | ANOVA_L_2_Random | random | 44.6% | 46.5% - 91.1% | 71.3% | 12 | XGBoost (learning_rate=unknown, max_depth=unknown, | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 8 | sub-49 | PCA_L_2_Random | random | 44.4% | 46.0% - 90.4% | 62.7% | 11 | SVM (kernel=poly, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 9 | sub-15 | ANOVA_L_2_Random | random | 44.3% | 48.7% - 93.1% | 65.1% | 12 | SVM (kernel=poly, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 10 | sub-15 | PCA_L_2_Random | random | 40.2% | 43.9% - 84.0% | 54.2% | 12 | KNN (n_neighbors=unknown, metric=euclidean, weight | SVM (kernel=rbf, C=0.1, gamma=auto) |
| 11 | sub-57 | PCA_L_2_Random | random | 39.5% | 47.5% - 87.0% | 62.3% | 4 | KNN (n_neighbors=unknown, metric=euclidean, weight | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 12 | sub-7 | PCA_L_2_Random | random | 38.9% | 49.0% - 87.8% | 61.7% | 11 | KNN (n_neighbors=unknown, metric=euclidean, weight | XGBoost (learning_rate=unknown, max_depth=unknown, |
| 13 | sub-49 | ANOVA_L_2_Random | random | 38.0% | 56.6% - 94.6% | 80.7% | 9 | MLP (activation=tanh, alpha=0.1, hidden=[]) | XGBoost (learning_rate=unknown, max_depth=unknown, |
| 14 | sub-54 | ANOVA_L_2_Random | random | 37.2% | 55.3% - 92.5% | 74.6% | 11 | SVM (kernel=poly, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 15 | sub-57 | ANOVA_L_6_Random | random | 37.0% | 50.1% - 87.1% | 69.2% | 11 | SVM (kernel=linear, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 16 | sub-8 | PCA_L_6_Random | random | 36.8% | 43.3% - 80.0% | 53.1% | 11 | XGBoost (learning_rate=unknown, max_depth=unknown, | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 17 | sub-42 | PCA_L_6_Random | random | 36.8% | 43.3% - 80.0% | 54.8% | 10 | XGBoost (learning_rate=unknown, max_depth=unknown, | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 18 | sub-21 | ANOVA_L_6_Random | random | 36.5% | 50.6% - 87.1% | 74.0% | 8 | SVM (kernel=rbf, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 19 | sub-23 | PCA_L_2_Random | random | 36.4% | 40.2% - 76.6% | 62.7% | 4 | KNN (n_neighbors=unknown, metric=euclidean, weight | SVM (kernel=rbf, C=0.1, gamma=auto) |
| 20 | sub-56 | PCA_L_2_Random | random | 36.4% | 40.2% - 76.6% | 60.4% | 10 | KNN (n_neighbors=unknown, metric=euclidean, weight | SVM (kernel=rbf, C=0.1, gamma=auto) |
| 21 | sub-32 | ANOVA_L_6_Random | random | 36.0% | 51.1% - 87.1% | 69.3% | 11 | KNN (n_neighbors=unknown, metric=euclidean, weight | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 22 | sub-39 | PCA_L_2_Random | random | 35.9% | 47.0% - 82.9% | 56.8% | 7 | MLP (activation=tanh, alpha=0.1, hidden=[]) | SVM (kernel=rbf, C=0.1, gamma=auto) |
| 23 | sub-60 | ANOVA_L_6_Random | random | 35.9% | 52.0% - 87.8% | 68.1% | 12 | SVM (kernel=rbf, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 24 | sub-14 | ANOVA_L_6_Random | random | 35.1% | 52.0% - 87.1% | 71.2% | 11 | SVM (kernel=rbf, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 25 | sub-65 | ANOVA_L_6_Random | random | 35.1% | 52.0% - 87.1% | 76.1% | 9 | SVM (kernel=rbf, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 26 | sub-35 | PCA_L_2_Random | random | 34.8% | 47.0% - 81.8% | 53.3% | 5 | MLP (activation=tanh, alpha=0.1, hidden=[]) | SVM (kernel=rbf, C=0.1, gamma=auto) |
| 27 | sub-28 | PCA_L_6_Random | random | 34.6% | 45.4% - 80.0% | 55.9% | 12 | SVM (kernel=linear, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |
| 28 | sub-35 | ANOVA_L_2_Random | random | 34.3% | 52.0% - 86.4% | 66.6% | 8 | MLP (activation=tanh, alpha=0.1, hidden=[]) | SVM (kernel=poly, C=0.1, gamma=auto) |
| 29 | sub-19 | ANOVA_L_2_Random | random | 34.3% | 51.9% - 86.2% | 65.9% | 5 | XGBoost (learning_rate=unknown, max_depth=unknown, | SVM (kernel=poly, C=0.1, gamma=auto) |
| 30 | sub-37 | PCA_L_6_Random | random | 34.1% | 45.9% - 80.0% | 58.7% | 10 | SVM (kernel=linear, C=0.1, gamma=auto) | MLP (activation=tanh, alpha=0.1, hidden=[]) |

---

## Methodology Notes

1. **Swing Calculation**: Swing = max - min (verified)
2. **Minimum Evidence**: Main table shows only model×hyperparam combinations with N Folds >= 3
3. **Uncertainty**: 95% CIs calculated using binomial approximation
4. **Fold Comparability**: Fold IDs are stored in the CSV files (`Fold_IDs` column in `per_subject_accuracy_main.csv` and `per_subject_accuracy_appendix_n_lt_3.csv`). Each row shows the fold directory names (e.g., `sub-2_sub-6_sub-14_sub-44_sub-53_sub-56`) used for that model×hyperparameter combination, allowing verification that the same folds are being compared across different models.
5. **Multiple Comparisons**: Note that rankings may flip with different fold splits

## CSV Files with Fold IDs

The fold IDs are included in the CSV files:

- **`per_subject_accuracy_main.csv`**: Contains `Fold_IDs` column with semicolon-separated fold directory names for each model×hyperparameter combination (N >= 3)
- **`per_subject_accuracy_appendix_n_lt_3.csv`**: Contains `Fold_IDs` column for combinations with N < 3

Example: `sub-2_sub-6_sub-14_sub-44_sub-53_sub-56;sub-2_sub-15_sub-36_sub-37_sub-44_sub-55` means this subject appeared in two folds as test data.

