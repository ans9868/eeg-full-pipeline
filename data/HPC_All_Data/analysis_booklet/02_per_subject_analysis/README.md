# Per-Subject Accuracy Analysis

## Overview

This directory contains per-subject accuracy analysis calculated directly from `test_predictions.parquet` files. The analysis provides detailed accuracy metrics for each subject (1-65) across different experiments, folds, and model×hyperparameter combinations.

## Directory Structure

```
per_subject_classification_analysis/
├── README.md (this file)
├── ANALYSIS_METHODOLOGY.md (detailed methodology)
├── SUMMARY_ALL_EXPERIMENTS.md (overall summary)
│
├── Individual Experiment Reports:
│   ├── ANOVA_L_2_Random_per_subject_summary.md
│   ├── ANOVA_L_2_Random_per_subject_summary.csv
│   ├── ANOVA_L_2_Random_per_subject_detailed.csv
│   ├── ANOVA_L_6_Random_per_subject_summary.md
│   ├── ANOVA_L_6_Random_per_subject_summary.csv
│   ├── ANOVA_L_6_Random_per_subject_detailed.csv
│   ├── ANOVA_L_6_Uniform_per_subject_summary.md
│   ├── ANOVA_L_6_Uniform_per_subject_summary.csv
│   ├── ANOVA_L_6_Uniform_per_subject_detailed.csv
│   ├── PCA_L_2_Random_per_subject_summary.md
│   ├── PCA_L_2_Random_per_subject_summary.csv
│   ├── PCA_L_2_Random_per_subject_detailed.csv
│   ├── PCA_L_6_Random_per_subject_summary.md
│   ├── PCA_L_6_Random_per_subject_summary.csv
│   ├── PCA_L_6_Random_per_subject_detailed.csv
│   ├── PCA_L_6_Uniform_per_subject_summary.md
│   ├── PCA_L_6_Uniform_per_subject_summary.csv
│   ├── PCA_L_6_Uniform_per_subject_detailed.csv
│   └── subject_accuracy_per_model.csv   (all experiments, per model)
│
└── Combined Reports:
    └── per_subject_summary_all_experiments.md
```

## File Types

### Summary Files (`*_per_subject_summary.md` and `.csv`)
- **Markdown**: Human-readable report with tables and statistics
- **CSV**: Machine-readable data with columns:
  - `Subject`: Subject ID (sub-1 to sub-65)
  - `Median_Accuracy`: Median accuracy across all fold×model combinations
  - `Mean_Accuracy`: Mean accuracy across all fold×model combinations
  - `N_Folds`: Number of unique folds where subject appeared
  - `N_Observations`: Total number of fold×model combinations

### Detailed Files (`*_per_subject_detailed.csv`)
- Complete breakdown: `Subject`, `Fold`, `Model`, `Accuracy`
- One row per subject×fold×model combination
- Useful for detailed analysis and debugging

### Subject Accuracy per Model (`subject_accuracy_per_model.csv`)
- One row per (experiment, subject, model): `median_accuracy`, `mean_accuracy`, `n_folds`
- Aggregated from the detailed CSVs; see [SUBJECT_ACCURACY_PER_MODEL.md](SUBJECT_ACCURACY_PER_MODEL.md) in the booklet.

## Experiments Analyzed

1. **ANOVA_L_2_Random**: ANOVA features, P=2, 50 random folds
2. **ANOVA_L_6_Random**: ANOVA features, P=6, 50 random folds
3. **ANOVA_L_6_Uniform**: ANOVA features, P=6, 12 uniform folds
4. **PCA_L_2_Random**: PCA features, P=2, 50 random folds
5. **PCA_L_6_Random**: PCA features, P=6, 50 random folds
6. **PCA_L_6_Uniform**: PCA features, P=6, 12 uniform folds

## Quick Start

1. **For overall summary**: See `SUMMARY_ALL_EXPERIMENTS.md`
2. **For methodology**: See `ANALYSIS_METHODOLOGY.md`
3. **For specific experiment**: Open `{EXPERIMENT}_per_subject_summary.md`
4. **For detailed data**: Use `{EXPERIMENT}_per_subject_detailed.csv`

## Key Metrics

- **Median Accuracy**: Robust measure of central tendency
- **Mean Accuracy**: Average performance across all observations
- **N Folds**: How many different test folds included this subject
- **N Observations**: Total fold×model combinations (indicates data richness)

## Notes

- Subjects not appearing in any test fold are marked as "N/A"
- Accuracy is calculated as: `(label == prediction).sum() / len(subject_data)`
- All calculations are done from actual prediction parquet files, not aggregate statistics


