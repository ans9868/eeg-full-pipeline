# Per-Subject Accuracy Analysis: Overall Summary

## Executive Summary

This document provides a comprehensive summary of per-subject accuracy analysis across 6 experiments. The analysis calculates individual subject accuracy directly from prediction parquet files, providing a detailed view of how well each subject is classified across different experimental conditions.

## Analysis Steps

### Step 1: Problem Identification
**Initial Issue**: The original per-subject accuracy calculation was incorrect because:
- It used aggregate fold accuracy from `results.json` files
- It mixed accuracies from different models for the same test set
- It didn't account for individual subject performance

**Discovery**: When examining the data structure, we found that:
- Each fold×model combination has a `test_predictions.parquet` file
- This file contains individual predictions for each epoch of each subject
- We can calculate per-subject accuracy directly: `(label == prediction).sum() / len(subject_data)`

### Step 2: Data Structure Exploration
**Location**: `/data/HPC_All_Data/grid_50_random_folds/` and `/grid_12_folds/`

**Structure Discovered**:
```
{experiment_dir}/
  ml_results_grid_search/
    {model_name}/  (e.g., KNN, XGBoost, SVM, MLP)
      {fold_name}/  (e.g., "sub-2_sub-39")
        task_{model}_{hyperparams}/
          test_predictions.parquet  ← Key file
```

**Parquet File Structure**:
- `SubjectID`: Integer subject identifier
- `EpochID`: Epoch number
- `Group`: "alz" or "cntrl"
- `label`: True label (0.0 or 1.0)
- `prediction`: Predicted label (0.0 or 1.0)

### Step 3: Method Development
**New Calculation Method**:
1. For each experiment, scan all model directories
2. For each fold directory, find all task directories
3. Read `test_predictions.parquet` from each task directory
4. For each subject in the test set:
   - Filter: `test_df[test_df['SubjectID'] == subject_id]`
   - Calculate: `accuracy = (label == prediction).sum() / len(subject_data)`
5. Aggregate across all fold×model combinations for each subject
6. Calculate median, mean, N folds, and N observations

### Step 4: Implementation
**Script Created**: `calculate_per_subject_accuracy_from_parquet.py`

**Process**:
- Scans 6 experiments (ANOVA/PCA × L_2/L_6 × Random/Uniform)
- Processes all fold×model combinations
- Generates 3 output files per experiment:
  - Summary markdown report
  - Summary CSV
  - Detailed CSV (subject × fold × model)

### Step 5: Validation
**Validation Steps**:
1. Manually checked specific subjects in specific folds
2. Verified calculation matches direct parquet inspection
3. Confirmed all subjects (1-65) are accounted for
4. Verified fold counts match expected values

**Example Validation**:
- Checked sub-1 in ANOVA_L_6_Uniform
- Manual calculation: 352/383 = 91.91%
- Script output: Matches across all model×HP combinations

## Experiments Analyzed

### 1. ANOVA_L_2_Random
- **Features**: ANOVA
- **Fold Strategy**: P=2, 50 random folds
- **Subjects with data**: 49 (out of 65)
- **Median of medians**: 76.84%
- **Mean of medians**: 72.75%
- **Range**: 4.76% - 98.76%

### 2. ANOVA_L_6_Random
- **Features**: ANOVA
- **Fold Strategy**: P=6, 50 random folds
- **Subjects with data**: 65 (all subjects)
- **Median of medians**: 75.80%
- **Mean of medians**: 70.43%
- **Range**: 5.33% - 97.79%

### 3. ANOVA_L_6_Uniform
- **Features**: ANOVA
- **Fold Strategy**: P=6, 12 uniform folds
- **Subjects with data**: 65 (all subjects)
- **Median of medians**: 74.12%
- **Mean of medians**: 70.12%
- **Range**: 2.95% - 99.41%

### 4. PCA_L_2_Random
- **Features**: PCA
- **Fold Strategy**: P=2, 50 random folds
- **Subjects with data**: 49 (out of 65)
- **Median of medians**: 87.92%
- **Mean of medians**: 58.71%
- **Range**: 0.00% - 100.00%
- **Note**: High median but low mean suggests bimodal distribution

### 5. PCA_L_6_Random
- **Features**: PCA
- **Fold Strategy**: P=6, 50 random folds
- **Subjects with data**: 65 (all subjects)
- **Median of medians**: 85.46%
- **Mean of medians**: 60.59%
- **Range**: 0.00% - 100.00%
- **Note**: High median but low mean suggests bimodal distribution

### 6. PCA_L_6_Uniform
- **Features**: PCA
- **Fold Strategy**: P=6, 12 uniform folds
- **Subjects with data**: 65 (all subjects)
- **Median of medians**: 88.18%
- **Mean of medians**: 60.39%
- **Range**: 0.00% - 100.00%
- **Note**: High median but low mean suggests bimodal distribution

## Key Findings

### 1. Subject Coverage
- **Random folds (P=2)**: 49 subjects appear in test sets (75% coverage)
- **Random folds (P=6)**: 65 subjects appear in test sets (100% coverage)
- **Uniform folds (P=6)**: 65 subjects appear in test sets (100% coverage)

### 2. Accuracy Patterns

**ANOVA Features**:
- More consistent across subjects
- Median accuracy: 74-77%
- Mean accuracy: 70-73%
- Fewer extreme values (min: 2.95-5.33%, max: 97.79-99.41%)

**PCA Features**:
- More variable across subjects
- Median accuracy: 85-88% (higher than ANOVA)
- Mean accuracy: 58-61% (lower than ANOVA)
- More extreme values (min: 0%, max: 100%)
- **Bimodal distribution**: Many subjects with very high or very low accuracy

### 3. Fold Strategy Comparison

**P=2 vs P=6**:
- P=6 provides better subject coverage (all 65 subjects)
- P=2 has some subjects missing from test sets
- Accuracy distributions are similar between P=2 and P=6

**Random vs Uniform**:
- Both provide 100% subject coverage for P=6
- Uniform folds: Each subject appears in 1-2 folds
- Random folds: Each subject appears in variable number of folds (1-3+)
- Accuracy patterns are similar between random and uniform

### 4. Subject-Level Variability

**High Variability Subjects**:
- Some subjects show very low accuracy (2-5%) across all conditions
- Some subjects show very high accuracy (97-100%) across all conditions
- This suggests subject-specific factors influence classification performance

**Consistent Subjects**:
- Most subjects show moderate accuracy (50-90%)
- Accuracy is relatively stable across different fold×model combinations

## Methodology Advantages

1. **Accuracy**: Uses actual predictions, not aggregate statistics
2. **Subject-Specific**: Each subject's accuracy calculated independently
3. **Transparent**: Can trace back to exact predictions
4. **Comprehensive**: Captures all fold×model combinations
5. **Robust**: Median provides stable measure even with outliers

## Output Files

For each experiment:
- **`{EXPERIMENT}_per_subject_summary.md`**: Human-readable report
- **`{EXPERIMENT}_per_subject_summary.csv`**: Summary statistics (median, mean, N folds, N observations)
- **`{EXPERIMENT}_per_subject_detailed.csv`**: Complete breakdown (subject × fold × model)

## Recommendations

1. **For ANOVA features**: More consistent performance, fewer extreme cases
2. **For PCA features**: Higher median but more variable - investigate bimodal distribution
3. **Subject-specific analysis**: Some subjects consistently perform poorly - investigate why
4. **Fold strategy**: P=6 provides better coverage; random vs uniform similar performance

## Next Steps

Potential future analyses:
1. Investigate subjects with consistently low accuracy
2. Analyze accuracy by group (alz vs cntrl)
3. Compare accuracy across different hyperparameter settings
4. Visualize accuracy distributions
5. Calculate confidence intervals for accuracy estimates
6. Analyze per-epoch accuracy patterns

## Files and Documentation

- **README.md**: Directory structure and quick start guide
- **ANALYSIS_METHODOLOGY.md**: Detailed methodology explanation
- **SUMMARY_ALL_EXPERIMENTS.md**: This document
- **per_subject_summary_all_experiments.md**: Combined report with all experiments

## Technical Details

**Script**: `calculate_per_subject_accuracy_from_parquet.py`  
**Location**: `/data/HPC_All_Data/`  
**Dependencies**: pandas, pathlib, statistics  
**Processing Time**: ~2-5 minutes for all 6 experiments  
**Output Size**: ~20 files (markdown + CSV)

---

*Analysis completed: November 2025*  
*Method: Direct calculation from test_predictions.parquet files*


