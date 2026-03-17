# Per-Subject Accuracy Analysis: Index

## Quick Navigation

### 📋 Documentation
1. **[README.md](README.md)** - Start here! Overview and directory structure
2. **[SUMMARY_ALL_EXPERIMENTS.md](SUMMARY_ALL_EXPERIMENTS.md)** - Overall summary with findings and analysis steps
3. **[ANALYSIS_METHODOLOGY.md](ANALYSIS_METHODOLOGY.md)** - Detailed methodology explanation

### 📊 Experiment Reports

#### ANOVA Experiments
- **[ANOVA_L_2_Random](ANOVA_L_2_Random_per_subject_summary.md)** - ANOVA, P=2, 50 random folds
- **[ANOVA_L_6_Random](ANOVA_L_6_Random_per_subject_summary.md)** - ANOVA, P=6, 50 random folds
- **[ANOVA_L_6_Uniform](ANOVA_L_6_Uniform_per_subject_summary.md)** - ANOVA, P=6, 12 uniform folds

#### PCA Experiments
- **[PCA_L_2_Random](PCA_L_2_Random_per_subject_summary.md)** - PCA, P=2, 50 random folds
- **[PCA_L_6_Random](PCA_L_6_Random_per_subject_summary.md)** - PCA, P=6, 50 random folds
- **[PCA_L_6_Uniform](PCA_L_6_Uniform_per_subject_summary.md)** - PCA, P=6, 12 uniform folds

### 📁 Data Files

Each experiment has 3 data files:
- `*_per_subject_summary.csv` - Summary statistics (median, mean, N folds, N observations)
- `*_per_subject_detailed.csv` - Complete breakdown (subject × fold × model)
- `*_per_subject_summary.md` - Human-readable report

**Combined (all experiments, per model):**
- **[subject_accuracy_per_model.csv](SUBJECT_ACCURACY_PER_MODEL.md)** - Subject accuracy per model (experiment, subject, model, median/mean accuracy, n_folds). See [SUBJECT_ACCURACY_PER_MODEL.md](SUBJECT_ACCURACY_PER_MODEL.md).

### 🔍 Combined Reports
- **[per_subject_summary_all_experiments.md](per_subject_summary_all_experiments.md)** - All experiments in one document
- **[SUBJECT_ACCURACY_PER_MODEL.md](SUBJECT_ACCURACY_PER_MODEL.md)** - Subject accuracy per model (CSV description and usage)

## Analysis Summary

### What We Did
1. **Identified the problem**: Original method mixed aggregate accuracies incorrectly
2. **Explored data structure**: Found `test_predictions.parquet` files with individual predictions
3. **Developed new method**: Calculate per-subject accuracy directly from parquet files
4. **Implemented solution**: Created script to process all experiments
5. **Validated results**: Verified calculations match manual inspection

### Key Results
- **6 experiments** analyzed
- **65 subjects** tracked (sub-1 to sub-65)
- **ANOVA**: More consistent (median: 74-77%, mean: 70-73%)
- **PCA**: More variable (median: 85-88%, mean: 58-61%, bimodal distribution)
- **P=6**: Better subject coverage (all 65 subjects)
- **P=2**: Some subjects missing (49 subjects)

### Files Generated
- **11 markdown files**: Documentation and reports
- **12 CSV files**: Data files (6 summary + 6 detailed)
- **Total**: 35 files including visualizations

## How to Use

1. **Start with**: `SUMMARY_ALL_EXPERIMENTS.md` for overall findings
2. **Understand method**: Read `ANALYSIS_METHODOLOGY.md`
3. **Explore data**: Use CSV files for custom analysis
4. **Check specific experiment**: Open individual experiment markdown files

## File Organization

```
per_subject_classification_analysis/
├── Documentation
│   ├── INDEX.md (this file)
│   ├── README.md
│   ├── SUMMARY_ALL_EXPERIMENTS.md
│   └── ANALYSIS_METHODOLOGY.md
│
├── Experiment Reports (6 experiments × 3 files = 18 files)
│   ├── {EXPERIMENT}_per_subject_summary.md
│   ├── {EXPERIMENT}_per_subject_summary.csv
│   ├── {EXPERIMENT}_per_subject_detailed.csv
│   └── subject_accuracy_per_model.csv (all experiments × subjects × models)
│
└── Combined Reports
    ├── per_subject_summary_all_experiments.md
    └── analysis_summary.md (from previous analysis)
```

---

*Last updated: November 2025*


