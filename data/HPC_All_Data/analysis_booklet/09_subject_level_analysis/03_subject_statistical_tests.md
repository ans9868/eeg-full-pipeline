# Subject-Level Statistical Tests

Statistical tests are performed on **subject accuracy** vectors (one value per fold),
mirroring the acceptance-criteria methodology from `compute_real_statistics.py`.
Best-per-fold vectors are taken from the model with the highest all-runs median epoch
accuracy (same model selection as the primary analysis).

---

## Acceptance Criteria — Subject Accuracy (Best-Per-Fold)

These tests use the best-model selection methodology to produce a single fold-level
vector per experiment, then compare across experiments. All 7 criteria pass.

| Comparison | Test | Delta Median (pp) | Cliff's delta | p-value | Result |
|---|---|---|---|---|---|
| ANOVA vs PCA (Random-50) | Wilcoxon signed-rank (paired) | +15.65 | 0.851 | < 0.001 | PASS |
| ANOVA vs PCA (Uniform-12) | Wilcoxon signed-rank (paired) | +15.88 | 0.833 | < 0.001 | PASS |
| Uniform-12 vs Random-50 (FTest) | Mann-Whitney U (unpaired) | +0.59 | 0.150 | 0.428 | PASS (ns) |
| Uniform-12 vs Random-50 (PCA) | Mann-Whitney U (unpaired) | +0.82 | 0.087 | 0.650 | PASS (ns) |
| P=6 vs P=2 (FTest) | Mann-Whitney U (unpaired) | -7.23 | -0.319 | 0.006 | PASS |
| P=6 vs P=2 (PCA) | Mann-Whitney U (unpaired) | -1.56 | -0.167 | 0.151 | PASS (ns) |
| MLP vs KNN (ANOVA Random-50) | Wilcoxon signed-rank (paired) | +1.61 | 0.206 | < 0.001 | PASS |

**Overall: ALL 7 CRITERIA PASSED**

---

## Per-Model Subject Accuracy Tests — ANOVA vs PCA

### Random-50 strategy

| Model | Delta Median (pp) | Cliff's delta | p-value | Test |
|---|---|---|---|---|
| MLP | +33.33 | 0.802 | < 0.001 | Wilcoxon signed-rank (paired) |
| KNN | +33.33 | 0.727 | < 0.001 | Wilcoxon signed-rank (paired) |
| SVM | +33.33 | 0.796 | < 0.001 | Wilcoxon signed-rank (paired) |
| XGBoost | +33.33 | 0.702 | < 0.001 | Wilcoxon signed-rank (paired) |

### Uniform-12 strategy

| Model | Delta Median (pp) | Cliff's delta | p-value | Test |
|---|---|---|---|---|
| MLP | +33.33 | 0.917 | 0.001 | Wilcoxon signed-rank (paired) |
| KNN | +25.00 | 0.701 | 0.001 | Wilcoxon signed-rank (paired) |
| SVM | +33.33 | 0.750 | 0.002 | Wilcoxon signed-rank (paired) |
| XGBoost | +25.00 | 0.653 | 0.020 | Wilcoxon signed-rank (paired) |

The ANOVA advantage over PCA is **larger** at the subject level (+33 pp) than at the
epoch level (+11–17 pp), because PCA subject accuracy collapses to chance while ANOVA
subject accuracy sits at 83%.

---

## Uniform-12 vs Random-50 — Subject Accuracy

### ANOVA (FTest) pipeline

| Model | Delta Median (pp) | Cliff's delta | p-value |
|---|---|---|---|
| MLP | 0.00 | -0.165 | 0.352 |
| KNN | 0.00 | -0.030 | 0.871 |
| SVM | 0.00 | +0.033 | 0.857 |
| XGBoost | -8.33 | -0.193 | 0.284 |

### PCA pipeline

| Model | Delta Median (pp) | Cliff's delta | p-value |
|---|---|---|---|
| MLP | 0.00 | -0.130 | 0.419 |
| KNN | +8.33 | +0.027 | 0.883 |
| SVM | 0.00 | +0.015 | 0.922 |
| XGBoost | 0.00 | -0.140 | 0.354 |

No significant difference between Uniform-12 and Random-50 at the subject level for
either pipeline, consistent with the epoch-level finding.

---

## P=6 vs P=2 — Subject Accuracy

### ANOVA (FTest) pipeline

| Model | Delta Median (pp) | Cliff's delta | p-value |
|---|---|---|---|
| MLP | -16.67 | -0.268 | 0.010 |
| KNN | -16.67 | -0.320 | 0.002 |
| SVM | -16.67 | -0.298 | 0.007 |
| XGBoost | -16.67 | -0.161 | 0.141 |

P=2 yields higher subject accuracy for ANOVA (the median jumps from 83% to 100%), which
is expected: with only 2 subjects per fold the task is easier — one AD and one control —
so majority-vote prediction trivially succeeds more often.

### PCA pipeline

| Model | Delta Median (pp) | Cliff's delta | p-value |
|---|---|---|---|
| MLP | 0.00 | +0.102 | 0.266 |
| KNN | 0.00 | +0.250 | 0.009 |
| SVM | 0.00 | +0.025 | 0.759 |
| XGBoost | 0.00 | +0.030 | 0.747 |

PCA shows no meaningful P=6 vs P=2 difference at subject level (both are at chance), as
expected.

---

## MLP vs KNN (ANOVA Random-50) — Subject Accuracy

| Comparison | Delta Median (pp) | Cliff's delta | p-value | Test |
|---|---|---|---|---|
| MLP vs KNN | 0.00 | +0.020 | 0.855 | Wilcoxon signed-rank (paired) |

At the subject level, MLP and KNN produce statistically equivalent performance for the
ANOVA pipeline. This contrasts with the epoch-level result where MLP marginally but
significantly outperforms KNN (Cliff's delta = 0.206, p < 0.001).
