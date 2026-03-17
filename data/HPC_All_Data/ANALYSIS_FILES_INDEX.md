# Analysis Files Index

This document lists all analysis files generated for per-subject accuracy analysis.

## Per-Subject Accuracy Analysis Files

### 1. Per-Subject Accuracy (Best Model Only)
- **File:** `per_subject_accuracy_analysis.md`
- **Size:** ~21KB
- **Description:** Detailed per-subject statistics using only the best model (by median) for each experiment
- **Location:** `/Users/user/projects/eeg-full-pipeline/data/HPC_All_Data/per_subject_accuracy_analysis.md`

### 2. Per-Subject Accuracy by Model × Hyperparameter
- **File:** `per_subject_accuracy_by_model_hyperparam.md`
- **Size:** ~85KB
- **Description:** Detailed breakdown showing per-subject accuracy for EACH model×hyperparameter combination
- **Includes:**
  - Cross-model×hyperparameter swings (biggest variance across all combinations)
  - Detailed breakdown per subject showing all model×hyperparam combinations
- **Location:** `/Users/user/projects/eeg-full-pipeline/data/HPC_All_Data/per_subject_accuracy_by_model_hyperparam.md`

### 3. Biggest Cross-Model Swings Summary
- **File:** `biggest_cross_model_swings.md`
- **Size:** ~2.4KB
- **Description:** Top 30 subjects with largest accuracy swings across different model×hyperparameter combinations
- **Location:** `/Users/user/projects/eeg-full-pipeline/data/HPC_All_Data/biggest_cross_model_swings.md`

### 4. Per-Subject Accuracy Summary
- **File:** `per_subject_accuracy_summary.md`
- **Size:** ~100 lines
- **Description:** Summary report with key findings and top swings
- **Location:** `/Users/user/projects/eeg-full-pipeline/data/HPC_All_Data/per_subject_accuracy_summary.md`

## Quick Access

To view any file, use:
```bash
# In terminal:
cd /Users/user/projects/eeg-full-pipeline/data/HPC_All_Data
cat biggest_cross_model_swings.md
cat per_subject_accuracy_summary.md
# etc.
```

Or open in your editor:
- `data/HPC_All_Data/biggest_cross_model_swings.md`
- `data/HPC_All_Data/per_subject_accuracy_by_model_hyperparam.md`
- `data/HPC_All_Data/per_subject_accuracy_analysis.md`
- `data/HPC_All_Data/per_subject_accuracy_summary.md`

## Key Findings Files

1. **biggest_cross_model_swings.md** - Quick reference for top 30 subjects with largest swings
2. **per_subject_accuracy_summary.md** - Executive summary with key findings

## Detailed Analysis Files

1. **per_subject_accuracy_analysis.md** - Best model only (simpler view)
2. **per_subject_accuracy_by_model_hyperparam.md** - All models×hyperparams (comprehensive view)

---

*Generated: November 4, 2025*


