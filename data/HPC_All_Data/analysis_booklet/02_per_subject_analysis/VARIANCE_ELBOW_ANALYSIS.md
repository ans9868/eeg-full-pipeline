# Variance Elbow Analysis: Test Group Combinations

## Methods

### Data Source

**Aggregate Fold Accuracies**: This analysis uses aggregate fold-level accuracies from `results.json` files. Each fold represents a test group with a single accuracy value.

**Key Limitation**: This method calculates variance of **group means**, not individual subject accuracies. For a more detailed analysis using individual subject accuracies, see `DEEP_VARIANCE_ANALYSIS_REPORT.md`.

### Variance Calculation Process

1. **Load Fold Accuracies**:
   - Extract `test_accuracy` from `results.json` for each fold×model×HP combination
   - Structure: `{fold_name: accuracy}` for each model×HP

2. **For Each Number of Test Groups (1 to MAX_TEST_GROUPS)**:
   - Generate all possible combinations of that many test groups
   - Example: For 50 folds and 2 groups, calculate C(50,2) = 1,225 combinations
   - For each combination, collect accuracies from those folds
   - Calculate variance: `variance = statistics.variance(accuracies)`

3. **Aggregate Statistics**:
   - Calculate mean variance across all combinations
   - Calculate standard deviation of variances
   - Track number of combinations analyzed

### Computational Optimization

- **Maximum Combinations**: Limited to 10,000 combinations per number of groups
- **Sampling Strategy**: If total combinations exceed 10,000, randomly sample 10,000 unique combinations
- **Maximum Test Groups**: Analyzed up to 15 test groups (to keep computation manageable)
- **Note**: When sampling is used, a note is displayed on the plot

### Visualization

**Plot Structure**:
- **X-axis**: Number of test groups (1, 2, 3, ..., up to 15)
- **Y-axis**: Mean variance of accuracies (with error bars showing ±1 standard deviation)
- **Annotations**: Number of subjects included (num_groups × subjects_per_group)

**Key Features**:
- Line plot with error bars showing mean ± std across all combinations
- Annotations showing total subjects included at key points
- Note displayed if sampling was used for any number of groups

## Overview

This analysis examines how the variance of model accuracies changes as we include more test groups (folds) in our evaluation. The goal is to understand the stability and consistency of model performance across different combinations of test groups, revealing an "elbow" pattern where variance stabilizes as more groups are included.

## Methodology

### Data Source

- **Input**: `results.json` files from each fold×model×hyperparameter combination
- **Accuracy Metric**: Aggregate fold accuracy (`test_accuracy` from results.json)
- **Experiments Analyzed**:
  - ANOVA_L_2_Random (50 random folds, 2 subjects per fold)
  - ANOVA_L_6_Random (50 random folds, 6 subjects per fold)
  - PCA_L_2_Random (50 random folds, 2 subjects per fold)
  - PCA_L_6_Random (50 random folds, 6 subjects per fold)

### Calculation Process

For each model×hyperparameter combination:

1. **Load Fold Accuracies**
   - Extract `test_accuracy` from `results.json` for each fold
   - Structure: `{fold_name: accuracy}` for each model×HP combination

2. **For Each Number of Test Groups (1 to MAX_TEST_GROUPS)**
   - Generate all possible combinations of that many test groups
   - Example: For 50 folds and 2 groups, calculate C(50,2) = 1,225 combinations
   - Example: For 50 folds and 3 groups, calculate C(50,3) = 19,600 combinations

3. **Calculate Variance for Each Combination**
   - For each combination of test groups, collect the accuracies
   - Calculate variance: `variance = statistics.variance(accuracies)`
   - This measures how spread out the accuracies are for that specific combination

4. **Aggregate Statistics**
   - Calculate mean variance across all combinations
   - Calculate standard deviation of variances
   - Track number of combinations analyzed

5. **Computational Optimization**
   - **Maximum Combinations**: Limited to 10,000 combinations per number of groups
   - **Sampling Strategy**: If total combinations exceed 10,000, randomly sample 10,000 unique combinations
   - **Maximum Test Groups**: Analyzed up to 15 test groups (to keep computation manageable)
   - **Note**: When sampling is used, a note is displayed on the plot

### Visualization

**Plot Structure**:
- **X-axis**: Number of test groups (1, 2, 3, ..., up to 15)
- **Y-axis**: Mean variance of accuracies (with error bars showing ±1 standard deviation)
- **Annotations**: Number of subjects included (num_groups × subjects_per_group)

**Key Features**:
- Line plot with error bars showing mean ± std across all combinations
- Annotations showing total subjects included at key points
- Note displayed if sampling was used for any number of groups

## Interpretation

### The "Elbow" Pattern

The plot typically shows an "elbow" pattern where:
- **Initial Phase**: Variance decreases rapidly as more test groups are included
- **Stabilization Phase**: Variance plateaus, indicating that adding more groups doesn't significantly change the variance estimate
- **Elbow Point**: The point where the curve transitions from rapid decrease to stabilization

### What This Tells Us

1. **Stability Assessment**: Lower variance indicates more consistent performance across different test group combinations
2. **Sample Size Sufficiency**: The elbow point suggests how many test groups are needed for stable variance estimates
3. **Model Comparison**: Different model×HP combinations may show different elbow patterns, revealing which models are more stable

### Example Interpretation

- **High initial variance**: Model performance varies significantly depending on which test groups are selected
- **Rapid decrease**: Adding more test groups quickly stabilizes the variance estimate
- **Low plateau**: Final variance is low, indicating consistent performance across test group combinations
- **Early elbow**: Few test groups are needed for stable estimates (efficient)
- **Late elbow**: Many test groups are needed for stable estimates (requires more data)

## Technical Details

### Variance Calculation

For a combination of N test groups with accuracies [a₁, a₂, ..., aₙ]:
```
variance = Σ(aᵢ - mean)² / (N - 1)
```

Where:
- `mean = (a₁ + a₂ + ... + aₙ) / N`
- This is the sample variance (Bessel's correction)

### Combination Generation

For k test groups from n total folds:
- **Total combinations**: C(n,k) = n! / (k! × (n-k)!)
- **Example**: C(50,10) = 10,272,278,170 combinations
- **Sampling**: When combinations exceed 10,000, we randomly sample 10,000 unique combinations

### Subjects Included

The number of subjects included is calculated as:
```
subjects_included = num_test_groups × subjects_per_fold
```

For example:
- ANOVA_L_2_Random: 1 group = 2 subjects, 5 groups = 10 subjects, 10 groups = 20 subjects
- ANOVA_L_6_Random: 1 group = 6 subjects, 5 groups = 30 subjects, 10 groups = 60 subjects

## Output Files

### Generated Plots

One PNG file per model×hyperparameter combination per experiment:
- Format: `{Experiment}_variance_by_test_groups_{Model}_{Hyperparams}.png`
- Location: `per_subject_classification_analysis/`
- Resolution: 300 DPI
- Example: `ANOVA_L_6_Random_variance_by_test_groups_MLP__activation_tanh_alpha_0_1_hidden_layer_sizes_100_.png`

### Script

- **Script**: `plot_variance_by_test_groups.py`
- **Location**: `data/HPC_All_Data/`
- **Dependencies**: `matplotlib`, `statistics`, `itertools`, `json`, `pathlib`

## Limitations and Considerations

1. **Computational Limits**: 
   - Maximum 10,000 combinations per number of groups
   - Maximum 15 test groups analyzed
   - For very large combination spaces, results are based on random sampling

2. **Variance vs. Accuracy**:
   - This analysis focuses on variance, not absolute accuracy
   - A model with low variance but low accuracy may not be desirable
   - Consider both metrics together

3. **Fold Independence**:
   - Assumes folds are independent test groups
   - In LPSO cross-validation, folds may share training data, affecting independence

4. **Subject Representation**:
   - Different combinations may include different subjects
   - The analysis doesn't account for subject-level effects beyond fold-level aggregation

## Future Enhancements

Potential improvements to this analysis:
1. **Subject-Level Analysis**: Track which subjects are included in each combination
2. **Confidence Intervals**: Add confidence intervals for variance estimates
3. **Elbow Detection**: Automatically detect and mark the elbow point
4. **Comparative Analysis**: Side-by-side comparison of multiple model×HP combinations
5. **Interactive Plots**: Create interactive visualizations for exploration

## References

- **Variance Formula**: Sample variance with Bessel's correction
- **Combination Generation**: `itertools.combinations` for exhaustive enumeration
- **Sampling**: Random sampling without replacement for large combination spaces
- **Visualization**: Matplotlib error bars for mean ± standard deviation

