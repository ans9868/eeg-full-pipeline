# Official Accuracy Summary (All Experiments, Verified from Combined CSV)

All statistics computed from `all_experiments_combined.csv` (2,736 verified rows, Feb 2026 audit).
No cross-experiment aggregation. Two median definitions reported side-by-side:

- **Median (all runs)**: median over all folds x all HP configs. Matches booklet Tables B/D convention.
- **Median (best/fold)**: for each fold pick the max accuracy, then take the median of those.

---

## Table A: Best Model per Experiment

| Experiment | Type | Feature | P | Best Model | Folds | Median (all) | Median (best/fold) | IQR | Min | Max |
|------------|------|---------|---|------------|-------|-------------|-------------------|-----|-----|-----|
| ANOVA_L_6_Random | Random-50 | ANOVA | 6 | MLP | 50 | 69.5% | 73.1% | 12.4% | 51.0% | 89.7% |
| ANOVA_L_2_Random | Random-50 | ANOVA | 2 | MLP | 50 | 76.6% | 80.4% | 22.0% | 36.1% | 98.3% |
| PCA_L_6_Random | Random-50 | PCA | 6 | KNN | 50 | 53.2% | 57.5% | 6.9% | 34.4% | 74.1% |
| PCA_L_2_Random | Random-50 | PCA | 2 | KNN | 50 | 54.2% | 59.1% | 10.0% | 26.0% | 78.5% |
| ANOVA_L_6_Uniform | Systematic-12 | ANOVA | 6 | MLP | 12 | 69.9% | 72.6% | 7.2% | 44.4% | 90.0% |
| PCA_L_6_Uniform | Systematic-12 | PCA | 6 | KNN | 12 | 54.1% | 56.7% | 7.3% | 45.7% | 73.8% |
| ANOVA_W_C | Within-subject | ANOVA | N/A | XGBoost | 1 | 93.8% | 94.9% | 6.3% | 88.6% | 94.9% |
| ANOVA_W_F | Within-subject | ANOVA | N/A | XGBoost | 1 | 97.6% | 97.6% | 0.2% | 97.4% | 97.6% |
| PCA_W_C | Within-subject | PCA | N/A | MLP | 1 | 97.7% | 98.2% | 2.1% | 96.0% | 98.2% |
| PCA_W_F | Within-subject | PCA | N/A | MLP | 1 | 97.5% | 98.1% | 1.9% | 96.2% | 98.1% |

---

## Table B: Per-Model Leaderboard (LPSO Experiments Only)

### ANOVA, P=6, Random-50 (primary setting)

| Model | Median (all) | Median (best/fold) | IQR | Min | Max |
|-------|-------------|-------------------|-----|-----|-----|
| MLP | 69.5% | 73.1% | 12.4% | 51.0% | 89.7% |
| KNN | 68.9% | 71.5% | 8.6% | 50.6% | 83.5% |
| XGBoost | 67.4% | 69.4% | 14.3% | 47.4% | 87.7% |
| SVM | 66.3% | 71.0% | 13.6% | 39.6% | 86.8% |

### PCA, P=6, Random-50

| Model | Median (all) | Median (best/fold) | IQR | Min | Max |
|-------|-------------|-------------------|-----|-----|-----|
| KNN | 53.2% | 57.5% | 6.9% | 34.4% | 74.1% |
| XGBoost | 53.0% | 57.8% | 8.5% | 37.9% | 76.0% |
| MLP | 52.9% | 57.2% | 8.0% | 37.3% | 80.0% |
| SVM | 51.2% | 56.5% | 6.8% | 38.5% | 74.3% |

### ANOVA, P=2, Random-50 (variance stress test)

| Model | Median (all) | Median (best/fold) | IQR | Min | Max |
|-------|-------------|-------------------|-----|-----|-----|
| MLP | 76.6% | 80.4% | 22.0% | 36.1% | 98.3% |
| SVM | 74.1% | 77.3% | 24.0% | 16.9% | 97.1% |
| XGBoost | 71.8% | 74.4% | 24.7% | 31.4% | 97.5% |
| KNN | 71.7% | 76.4% | 17.8% | 45.4% | 92.7% |

### PCA, P=2, Random-50 (variance stress test)

| Model | Median (all) | Median (best/fold) | IQR | Min | Max |
|-------|-------------|-------------------|-----|-----|-----|
| KNN | 54.2% | 59.1% | 10.0% | 26.0% | 78.5% |
| XGBoost | 53.2% | 59.4% | 9.9% | 27.1% | 87.8% |
| MLP | 52.4% | 58.1% | 9.9% | 25.6% | 90.4% |
| SVM | 51.4% | 59.7% | 9.8% | 25.6% | 84.0% |

### ANOVA, P=6, Systematic-12

| Model | Median (all) | Median (best/fold) | IQR | Min | Max |
|-------|-------------|-------------------|-----|-----|-----|
| MLP | 69.9% | 72.6% | 7.2% | 44.4% | 90.0% |
| SVM | 68.7% | 71.8% | 16.2% | 55.2% | 89.3% |
| KNN | 65.7% | 67.8% | 8.2% | 57.8% | 79.3% |
| XGBoost | 65.4% | 68.4% | 9.0% | 47.3% | 88.2% |

### PCA, P=6, Systematic-12

| Model | Median (all) | Median (best/fold) | IQR | Min | Max |
|-------|-------------|-------------------|-----|-----|-----|
| KNN | 54.1% | 56.7% | 7.3% | 45.7% | 73.8% |
| XGBoost | 53.5% | 57.5% | 8.3% | 41.7% | 70.3% |
| MLP | 53.3% | 55.9% | 11.3% | 41.5% | 66.3% |
| SVM | 52.1% | 57.6% | 6.5% | 40.6% | 68.7% |

---

## Notes

- **Source:** `data/HPC_All_Data/accuracy_summary/` contains the full CSVs at all abstraction levels (per-model, per-hyperparameter, best-model, all-models-pooled).
- **Verified:** All values cross-checked against booklet Tables B, C, D and the combined CSV integrity report.
- Within-subject experiments (W_C, W_F) have only 1 split with 3 HP configs per model, so IQR/min/max reflect HP variation, not fold variation.

*Generated from `accuracy_summary/` scripts, Feb 2026.*
