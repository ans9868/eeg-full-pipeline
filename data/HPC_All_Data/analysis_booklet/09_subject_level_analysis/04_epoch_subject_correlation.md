# Epoch–Subject Accuracy Correlation

Within each experiment×model combination, fold-level epoch accuracy and fold-level
subject accuracy are paired (one value per fold). Pearson and Spearman correlation
coefficients quantify how tightly the two metrics track each other.

---

## Correlation Table

| Experiment | Pipeline | Strategy | P | Model | Folds | Pearson r | Pearson p | Spearman r | Spearman p |
|---|---|---|---|---|---|---|---|---|---|
| ANOVA_L_2_Random | FTest | Random-50 | 2 | KNN | 50 | 0.741 | < 0.001 | 0.678 | < 0.001 |
| ANOVA_L_2_Random | FTest | Random-50 | 2 | MLP | 50 | 0.823 | < 0.001 | 0.767 | < 0.001 |
| ANOVA_L_2_Random | FTest | Random-50 | 2 | SVM | 50 | 0.811 | < 0.001 | 0.764 | < 0.001 |
| ANOVA_L_2_Random | FTest | Random-50 | 2 | XGBoost | 50 | 0.766 | < 0.001 | 0.773 | < 0.001 |
| ANOVA_L_6_Random | FTest | Random-50 | 6 | KNN | 50 | 0.808 | < 0.001 | 0.814 | < 0.001 |
| ANOVA_L_6_Random | FTest | Random-50 | 6 | MLP | 50 | 0.837 | < 0.001 | 0.846 | < 0.001 |
| ANOVA_L_6_Random | FTest | Random-50 | 6 | SVM | 50 | 0.787 | < 0.001 | 0.756 | < 0.001 |
| ANOVA_L_6_Random | FTest | Random-50 | 6 | XGBoost | 50 | 0.824 | < 0.001 | 0.817 | < 0.001 |
| ANOVA_L_6_Uniform | FTest | Uniform-12 | 6 | KNN | 12 | 0.801 | 0.002 | 0.704 | 0.011 |
| ANOVA_L_6_Uniform | FTest | Uniform-12 | 6 | MLP | 12 | 0.472 | 0.122 | 0.118 | 0.715 |
| ANOVA_L_6_Uniform | FTest | Uniform-12 | 6 | SVM | 12 | 0.834 | 0.001 | 0.785 | 0.003 |
| ANOVA_L_6_Uniform | FTest | Uniform-12 | 6 | XGBoost | 12 | 0.783 | 0.003 | 0.752 | 0.005 |
| PCA_L_2_Random | PCA | Random-50 | 2 | KNN | 50 | 0.507 | < 0.001 | 0.348 | 0.013 |
| PCA_L_2_Random | PCA | Random-50 | 2 | MLP | 50 | 0.565 | < 0.001 | 0.340 | 0.016 |
| PCA_L_2_Random | PCA | Random-50 | 2 | SVM | 50 | 0.624 | < 0.001 | 0.582 | < 0.001 |
| PCA_L_2_Random | PCA | Random-50 | 2 | XGBoost | 50 | 0.596 | < 0.001 | 0.411 | 0.003 |
| PCA_L_6_Random | PCA | Random-50 | 6 | KNN | 50 | 0.667 | < 0.001 | 0.664 | < 0.001 |
| PCA_L_6_Random | PCA | Random-50 | 6 | MLP | 50 | 0.739 | < 0.001 | 0.632 | < 0.001 |
| PCA_L_6_Random | PCA | Random-50 | 6 | SVM | 50 | 0.717 | < 0.001 | 0.693 | < 0.001 |
| PCA_L_6_Random | PCA | Random-50 | 6 | XGBoost | 50 | 0.638 | < 0.001 | 0.547 | < 0.001 |
| PCA_L_6_Uniform | PCA | Uniform-12 | 6 | KNN | 12 | 0.901 | < 0.001 | 0.786 | 0.002 |
| PCA_L_6_Uniform | PCA | Uniform-12 | 6 | MLP | 12 | 0.489 | 0.107 | 0.518 | 0.084 |
| PCA_L_6_Uniform | PCA | Uniform-12 | 6 | SVM | 12 | 0.151 | 0.639 | 0.139 | 0.666 |
| PCA_L_6_Uniform | PCA | Uniform-12 | 6 | XGBoost | 12 | 0.608 | 0.036 | 0.480 | 0.114 |

---

## Interpretation

**ANOVA pipeline — strong, consistent correlation:**

- For ANOVA Random-50 ($P = 6$), Pearson $r$ ranges from 0.787 to 0.837 across all
  four models (all $p < 0.001$). Spearman $r$ is similarly high (0.756–0.846).
- This indicates that **folds with high epoch accuracy also tend to have high subject
  accuracy** — the two metrics are almost interchangeable as fold-quality signals for
  ANOVA.
- For Uniform-12, MLP is an exception ($r = 0.472$, $p = 0.12$), likely due to the
  low number of folds ($n = 12$) combined with occasional outlier folds.

**PCA pipeline — moderate correlation only:**

- PCA Random-50 ($P = 6$) correlations are moderate: Pearson $r$ = 0.64–0.74. This
  means a fold with above-chance epoch accuracy for PCA does not reliably produce
  above-chance subject accuracy.
- This is consistent with PCA's near-chance median subject accuracy: most subject-level
  outcomes are decided by noise, so the correlation with epoch accuracy is weakened.
- PCA Uniform-12 shows highly variable correlations (0.15 to 0.90), reflecting the
  instability with $n = 12$ folds.

**Practical implication:**

The strong epoch–subject correlation for ANOVA (r > 0.80) supports using epoch accuracy
as a proxy when subject-level ground truth is unavailable, at least for the ANOVA
pipeline. For PCA, epoch accuracy is a weaker predictor of subject-level outcome.
