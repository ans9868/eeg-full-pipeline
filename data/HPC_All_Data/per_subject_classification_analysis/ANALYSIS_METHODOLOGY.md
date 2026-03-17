# Per-Subject Accuracy Analysis: Methodology

## Overview

This document describes the methodology used to calculate per-subject accuracy from EEG classification experiments. The analysis calculates accuracy for each individual subject based on their actual predictions, rather than using aggregate fold-level statistics.

## Problem Statement

Initially, per-subject accuracy was calculated incorrectly by:
1. Using aggregate fold accuracy from `results.json` files
2. Mixing accuracies from different models for the same test set
3. Not accounting for the fact that each subject has different numbers of epochs

This approach was problematic because:
- Aggregate fold accuracy doesn't reflect individual subject performance
- Different models give different accuracies for the same test set
- Subjects with more epochs have different weight in the calculation

## Solution: Direct Calculation from Parquet Files

### Step 1: Locate Test Prediction Files

For each experiment, we scan the directory structure:
```
{experiment_dir}/
  ml_results_grid_search/
    {model_name}/
      {fold_name}/  (e.g., "sub-2_sub-39")
        task_{model}_{hyperparams}/
          test_predictions.parquet  ← This is what we read
```

### Step 2: Read Test Predictions

Each `test_predictions.parquet` file contains:
- **SubjectID**: Integer subject identifier (e.g., 2, 39)
- **EpochID**: Epoch number within the subject
- **Group**: Group label ("alz" or "cntrl")
- **label**: True label (0.0 or 1.0)
- **prediction**: Predicted label (0.0 or 1.0)

**Example structure:**
```
SubjectID  EpochID  Group  label  prediction
39         0        cntrl  1.0    1.0
39         1        cntrl  1.0    1.0
2          0        alz    0.0    0.0
...
```

### Step 3: Calculate Per-Subject Accuracy

For each subject in each fold×model combination:

```python
# Filter data for this subject
subject_data = test_df[test_df['SubjectID'] == subject_id]

# Calculate accuracy
correct = (subject_data['label'] == subject_data['prediction']).sum()
total = len(subject_data)
accuracy = correct / total if total > 0 else 0.0
```

**Example:**
- Subject 39 in fold "sub-2_sub-39" with model "KNN":
  - 541 correct predictions out of 561 total epochs
  - Accuracy = 541/561 = 96.43%

### Step 4: Aggregate Across Folds and Models

For each subject, we collect all accuracies from:
- All folds where the subject appears in the test set
- All model×hyperparameter combinations

**Example for sub-1 in ANOVA_L_6_Uniform:**
- Appears in 1 fold: "sub-1_sub-2_sub-3_sub-37_sub-38_sub-39"
- Has 12 model×HP combinations (KNN, XGBoost, SVM, MLP with different hyperparameters)
- Collects 12 accuracy values: [96.08%, 91.91%, 94.52%, ...]
- Median = 96.08%, Mean = 93.10%

### Step 5: Generate Statistics

For each subject, we calculate:
- **Median Accuracy**: Robust to outliers
- **Mean Accuracy**: Average performance
- **N Folds**: Number of unique folds (indicates how many times subject was tested)
- **N Observations**: Total fold×model combinations (indicates data richness)

## Advantages of This Method

1. **Accuracy**: Uses actual predictions, not aggregate statistics
2. **Subject-Specific**: Each subject's accuracy is calculated independently
3. **Transparent**: Can trace back to exact predictions
4. **Comprehensive**: Captures all fold×model combinations
5. **Robust**: Median provides stable measure even with outliers

## Data Flow

```
test_predictions.parquet files
    ↓
Read parquet for each fold×model
    ↓
Filter by SubjectID
    ↓
Calculate: (label == prediction).sum() / len(subject_data)
    ↓
Collect all accuracies for each subject
    ↓
Calculate median, mean, N folds, N observations
    ↓
Generate reports (markdown + CSV)
```

## Validation

We validated the method by:
1. Manually checking a specific subject in a specific fold
2. Comparing calculated accuracy with direct parquet inspection
3. Verifying that all subjects are accounted for (1-65)
4. Confirming fold counts match expected values

**Validation Example:**
- Checked sub-1 in ANOVA_L_6_Uniform, fold "sub-1_sub-2_sub-3_sub-37_sub-38_sub-39"
- Manual calculation: 352/383 = 91.91%
- Script output: Matches across all model×HP combinations

## Implementation

The analysis is implemented in:
- **Script**: `calculate_per_subject_accuracy_from_parquet.py`
- **Location**: `/data/HPC_All_Data/`

## Output Files

For each experiment, we generate:
1. **Summary Markdown** (`*_per_subject_summary.md`): Human-readable report
2. **Summary CSV** (`*_per_subject_summary.csv`): Machine-readable summary
3. **Detailed CSV** (`*_per_subject_detailed.csv`): Complete breakdown by fold×model

## Future Improvements

Potential enhancements:
- Add confidence intervals for accuracy estimates
- Calculate per-epoch accuracy distributions
- Analyze accuracy by group (alz vs cntrl)
- Compare accuracy across different hyperparameter settings
- Visualize accuracy distributions


