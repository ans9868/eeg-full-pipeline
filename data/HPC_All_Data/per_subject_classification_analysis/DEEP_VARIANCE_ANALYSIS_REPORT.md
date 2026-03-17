# Deep Variance Analysis: Identifying Optimal Subject Counts

## Methods

### Data Source and Processing

**Individual Subject Accuracies**: This analysis uses individual subject-level accuracies calculated directly from `test_predictions.parquet` files, rather than aggregate fold-level accuracies from `results.json`. This approach provides a more accurate representation of variance across subjects.

**Calculation Method**:
1. For each combination of test groups (folds), we:
   - Read `test_predictions.parquet` files for all folds in the combination
   - Calculate per-subject accuracy: `accuracy = (label == prediction).sum() / total_epochs` for each subject
   - Collect all individual subject accuracies from all selected groups
   - Calculate variance: `variance(all_subject_accuracies)` 

2. **Key Difference from Previous Method**:
   - **Previous**: `variance([group1_mean, group2_mean, ...])` - variance of group means
   - **Current**: `variance([subject1_acc, subject2_acc, subject3_acc, ...])` - variance of all individual subject accuracies

### Sampling Strategy

To make the analysis computationally feasible, we use **random sampling**:
- For each number of test groups (1-15), we sample **30 random combinations** instead of calculating all possible combinations
- Example: For 2 groups from 50 folds, instead of C(50,2) = 1,225 combinations, we sample 30
- Example: For 10 groups from 50 folds, instead of 10,272,278,170 combinations, we sample 30
- This provides statistically robust estimates while remaining computationally tractable

### Variance Drop Detection

**Significant Drop Threshold**: We identify variance drops >1% as significant (lowered from 5% since overall variance is already quite stable).

**Drop Calculation**:
- For each number of groups, calculate mean variance across all sampled combinations
- Calculate percentage drop: `(variance[i-1] - variance[i]) / variance[i-1] * 100`
- Identify largest drops and inflection points

### Elbow Point Detection

**Stability Detection**:
- Look for points where variance changes become small (<5% between consecutive points)
- Identify inflection points where the rate of change (second derivative) changes sign
- Determine where variance first becomes "low" (below median + 10%)

### Experiments Analyzed

- **ANOVA_L_2_Random**: 50 random folds, 2 subjects per fold
- **ANOVA_L_6_Random**: 50 random folds, 6 subjects per fold  
- **PCA_L_2_Random**: 50 random folds, 2 subjects per fold
- **PCA_L_6_Random**: 50 random folds, 6 subjects per fold

**Total**: 48 model×hyperparameter combinations across 4 experiments

## Executive Summary

### Key Findings

**Most Common Subject Counts with Significant Variance Drops:**

1. **18 subjects**: 1 models show drops (mean: 1.7%, max: 1.7%)
2. **20 subjects**: 1 models show drops (mean: 1.7%, max: 1.7%)
3. **8 subjects**: 1 models show drops (mean: 1.6%, max: 1.6%)
4. **48 subjects**: 1 models show drops (mean: 1.5%, max: 1.5%)
5. **30 subjects**: 1 models show drops (mean: 1.4%, max: 1.4%)

### Overall Recommendation

#### For L_2 Experiments (2 subjects per test group)

**18 subjects appears to be the optimal threshold** (equivalent to 9 test groups).
- Observed in 1 model×HP combinations
- Mean variance drop: 1.7%
- Maximum variance drop: 1.7%

#### For L_6 Experiments (6 subjects per test group)

**48 subjects appears to be the optimal threshold** (equivalent to 8 test groups).
- Observed in 1 model×HP combinations
- Mean variance drop: 1.5%
- Maximum variance drop: 1.5%

#### Cross-Experiment Consistency Check

⚠️ **INCONSISTENT PATTERN**: Different optimal thresholds detected
- L_2 optimal: 18 subjects (9 groups)
- L_6 optimal: 48 subjects (8 groups)

**Note**: Since variance drops are very small (<2%), variance is already quite stable.
The inconsistent patterns suggest there may not be a single optimal subject count.
Instead, variance appears to stabilize early (around 3-6 test groups) regardless of total subjects.

#### Analysis: Where Variance First Becomes Low

Since variance drops are small, we analyze where variance first reaches acceptably low levels.

**L_2 Experiments - First Low Variance Point:**
- Median: 2.0 subjects
- Mean: 2.0 subjects
- Range: 2 - 2 subjects

**L_6 Experiments - First Low Variance Point:**
- Median: 6.0 subjects
- Mean: 6.0 subjects
- Range: 6 - 6 subjects

**Overall - First Low Variance Point (All Experiments):**
- Median: 4.0 subjects
- Mean: 4.0 subjects

⚠️ **INCONSISTENT**: Different absolute subject counts
- L_2 median: 2.0 subjects
- L_6 median: 6.0 subjects
- This suggests the threshold is based on number of groups, not absolute subjects

## Detailed Statistics

### L_2 Experiments: Subject Counts with Significant Drops (>1%)

| Subjects | Groups | Frequency | Mean Drop % | Median Drop % | Max Drop % | Min Drop % |
|----------|--------|-----------|-------------|---------------|------------|------------|
| 8 | 4 | 1 | 1.56 | 1.56 | 1.56 | 1.56 |
| 10 | 5 | 1 | 1.25 | 1.25 | 1.25 | 1.25 |
| 12 | 6 | 1 | 1.00 | 1.00 | 1.00 | 1.00 |
| 18 | 9 | 1 | 1.74 | 1.74 | 1.74 | 1.74 |
| 20 | 10 | 1 | 1.66 | 1.66 | 1.66 | 1.66 |
| 22 | 11 | 1 | 1.23 | 1.23 | 1.23 | 1.23 |
| 26 | 13 | 1 | 1.02 | 1.02 | 1.02 | 1.02 |
| 28 | 14 | 1 | 1.35 | 1.35 | 1.35 | 1.35 |

### L_6 Experiments: Subject Counts with Significant Drops (>1%)

| Subjects | Groups | Frequency | Mean Drop % | Median Drop % | Max Drop % | Min Drop % |
|----------|--------|-----------|-------------|---------------|------------|------------|
| 24 | 4 | 1 | 1.15 | 1.15 | 1.15 | 1.15 |
| 30 | 5 | 1 | 1.38 | 1.38 | 1.38 | 1.38 |
| 48 | 8 | 1 | 1.49 | 1.49 | 1.49 | 1.49 |
| 54 | 9 | 1 | 1.01 | 1.01 | 1.01 | 1.01 |

### Overall: Subject Counts with Significant Drops (>1%)

| Subjects | Frequency | Mean Drop % | Median Drop % | Max Drop % | Min Drop % |
|----------|-----------|-------------|---------------|------------|------------|
| 8 | 1 | 1.56 | 1.56 | 1.56 | 1.56 |
| 10 | 1 | 1.25 | 1.25 | 1.25 | 1.25 |
| 12 | 1 | 1.00 | 1.00 | 1.00 | 1.00 |
| 18 | 1 | 1.74 | 1.74 | 1.74 | 1.74 |
| 20 | 1 | 1.66 | 1.66 | 1.66 | 1.66 |
| 22 | 1 | 1.23 | 1.23 | 1.23 | 1.23 |
| 24 | 1 | 1.15 | 1.15 | 1.15 | 1.15 |
| 26 | 1 | 1.02 | 1.02 | 1.02 | 1.02 |
| 28 | 1 | 1.35 | 1.35 | 1.35 | 1.35 |
| 30 | 1 | 1.38 | 1.38 | 1.38 | 1.38 |
| 48 | 1 | 1.49 | 1.49 | 1.49 | 1.49 |
| 54 | 1 | 1.01 | 1.01 | 1.01 | 1.01 |

## Per-Experiment Analysis

### ANOVA_L_2_Random

#### Largest Variance Drops by Model

| Model×HP | Subjects | Drop % | From Variance | To Variance |
|----------|----------|--------|---------------|-------------|
| KNN (metric=euclidean, n_neighbors=1, weights=unif... | 6 | 0.00% | 0.0081 | 0.0081 |
| KNN (metric=euclidean, n_neighbors=15, weights=uni... | 6 | 0.00% | 0.0079 | 0.0079 |
| KNN (metric=euclidean, n_neighbors=7, weights=unif... | 12 | 1.00% | 0.0149 | 0.0148 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 6 | 0.00% | 0.0280 | 0.0280 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 6 | 0.00% | 0.0202 | 0.0202 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 20 | 0.86% | 0.0221 | 0.0219 |
| SVM (C=0.1, gamma=auto, kernel=linear) | 6 | 0.00% | 0.0182 | 0.0182 |
| SVM (C=0.1, gamma=auto, kernel=poly) | 28 | 1.35% | 0.0234 | 0.0231 |
| SVM (C=0.1, gamma=auto, kernel=rbf) | 6 | 0.00% | 0.0317 | 0.0317 |
| XGBoost (learning_rate=0.2, max_depth=3, n_estimat... | 6 | 0.00% | 0.0366 | 0.0366 |
| XGBoost (learning_rate=0.2, max_depth=6, n_estimat... | 6 | 0.00% | 0.0217 | 0.0217 |
| XGBoost (learning_rate=0.2, max_depth=9, n_estimat... | 28 | 0.87% | 0.0210 | 0.0208 |

### ANOVA_L_6_Random

#### Largest Variance Drops by Model

| Model×HP | Subjects | Drop % | From Variance | To Variance |
|----------|----------|--------|---------------|-------------|
| KNN (metric=euclidean, n_neighbors=1, weights=unif... | 18 | 0.00% | 0.0007 | 0.0007 |
| KNN (metric=euclidean, n_neighbors=15, weights=uni... | 48 | 0.95% | 0.0057 | 0.0057 |
| KNN (metric=euclidean, n_neighbors=7, weights=unif... | 18 | 0.00% | 0.0056 | 0.0056 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 60 | 0.47% | 0.0073 | 0.0073 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 48 | 0.35% | 0.0117 | 0.0117 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 18 | 0.00% | 0.0045 | 0.0045 |
| SVM (C=0.1, gamma=auto, kernel=linear) | 24 | 1.15% | 0.0082 | 0.0081 |
| SVM (C=0.1, gamma=auto, kernel=poly) | 18 | 0.00% | 0.0051 | 0.0051 |
| SVM (C=0.1, gamma=auto, kernel=rbf) | 18 | 0.00% | 0.0072 | 0.0072 |
| XGBoost (learning_rate=0.2, max_depth=3, n_estimat... | 48 | 0.32% | 0.0127 | 0.0126 |
| XGBoost (learning_rate=0.2, max_depth=6, n_estimat... | 18 | 0.00% | 0.0049 | 0.0049 |
| XGBoost (learning_rate=0.2, max_depth=9, n_estimat... | 54 | 0.49% | 0.0062 | 0.0062 |

### PCA_L_2_Random

#### Largest Variance Drops by Model

| Model×HP | Subjects | Drop % | From Variance | To Variance |
|----------|----------|--------|---------------|-------------|
| KNN (metric=euclidean, n_neighbors=1, weights=unif... | 8 | 1.56% | 0.0047 | 0.0047 |
| KNN (metric=euclidean, n_neighbors=15, weights=uni... | 6 | 0.00% | 0.0055 | 0.0055 |
| KNN (metric=euclidean, n_neighbors=7, weights=unif... | 6 | 0.00% | 0.0135 | 0.0135 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 6 | 0.00% | 0.0056 | 0.0056 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 6 | 0.00% | 0.0222 | 0.0222 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 20 | 1.66% | 0.0103 | 0.0102 |
| SVM (C=0.1, gamma=auto, kernel=linear) | 6 | 0.00% | 0.0039 | 0.0039 |
| SVM (C=0.1, gamma=auto, kernel=poly) | 6 | 0.00% | 0.0043 | 0.0043 |
| SVM (C=0.1, gamma=auto, kernel=rbf) | 14 | 0.53% | 0.0136 | 0.0135 |
| XGBoost (learning_rate=0.2, max_depth=3, n_estimat... | 6 | 0.00% | 0.0116 | 0.0116 |
| XGBoost (learning_rate=0.2, max_depth=6, n_estimat... | 18 | 1.74% | 0.0070 | 0.0069 |
| XGBoost (learning_rate=0.2, max_depth=9, n_estimat... | 18 | 0.17% | 0.0059 | 0.0059 |

### PCA_L_6_Random

#### Largest Variance Drops by Model

| Model×HP | Subjects | Drop % | From Variance | To Variance |
|----------|----------|--------|---------------|-------------|
| KNN (metric=euclidean, n_neighbors=1, weights=unif... | 18 | 0.00% | 0.0030 | 0.0030 |
| KNN (metric=euclidean, n_neighbors=15, weights=uni... | 18 | 0.00% | 0.0060 | 0.0060 |
| KNN (metric=euclidean, n_neighbors=7, weights=unif... | 66 | 0.44% | 0.0031 | 0.0031 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 18 | 0.00% | 0.0030 | 0.0030 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 18 | 0.00% | 0.0061 | 0.0061 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, ... | 48 | 1.49% | 0.0082 | 0.0081 |
| SVM (C=0.1, gamma=auto, kernel=linear) | 18 | 0.00% | 0.0020 | 0.0020 |
| SVM (C=0.1, gamma=auto, kernel=poly) | 18 | 0.00% | 0.0007 | 0.0007 |
| SVM (C=0.1, gamma=auto, kernel=rbf) | 42 | 0.76% | 0.0055 | 0.0055 |
| XGBoost (learning_rate=0.2, max_depth=3, n_estimat... | 18 | 0.00% | 0.0023 | 0.0023 |
| XGBoost (learning_rate=0.2, max_depth=6, n_estimat... | 30 | 1.38% | 0.0053 | 0.0052 |
| XGBoost (learning_rate=0.2, max_depth=9, n_estimat... | 18 | 0.00% | 0.0037 | 0.0037 |

## Inflection Points Analysis

### Most Common Inflection Points

| Subjects | Frequency |
|----------|-----------|
| 24 | 12 |
| 18 | 9 |
| 28 | 8 |
| 42 | 8 |
| 48 | 8 |
| 54 | 8 |
| 12 | 7 |
| 16 | 7 |
| 22 | 7 |
| 30 | 7 |
