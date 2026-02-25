# Variance Elbow Analysis: Optimal Number of Test Subjects

## Methods

### Data Source

**Aggregate Fold Accuracies**: This analysis uses aggregate fold-level accuracies from `results.json` files. Each fold (test group) has a single accuracy value representing the overall performance on that fold's test subjects.

**Calculation Method**:
1. For each model×hyperparameter combination:
   - Extract `test_accuracy` from `results.json` for each fold
   - Structure: `{fold_name: accuracy}` mapping

2. For each number of test groups (1 to MAX_TEST_GROUPS):
   - Generate all possible combinations of that many test groups
   - For each combination, collect the accuracies from those folds
   - Calculate variance: `variance([accuracy1, accuracy2, ...])`
   - This measures variance of **fold-level accuracies** (group means)

### Variance Calculation

**Variance Formula**: For a combination of N test groups with accuracies [a₁, a₂, ..., aₙ]:
```
variance = Σ(aᵢ - mean)² / (N - 1)
```
Where `mean = (a₁ + a₂ + ... + aₙ) / N` (sample variance with Bessel's correction)

### Combination Generation

For k test groups from n total folds:
- **Total combinations**: C(n,k) = n! / (k! × (n-k)!)
- **Example**: C(50,10) = 10,272,278,170 combinations
- **Sampling**: When combinations exceed 10,000, we randomly sample 10,000 unique combinations

### Elbow Detection Algorithm

**Gradual Stabilization Detection**:
1. Calculate variance for each number of test groups (1-15)
2. For each point, check if variance change is <5% (stability threshold)
3. Require at least 2 consecutive stable points to confirm stabilization
4. Record the first point where stability is achieved

**Elbow Point Detection** (for sharp drops):
1. Find maximum variance (usually at start)
2. Calculate percentage drops between consecutive points
3. Identify first drop >10% as potential elbow
4. Check if variance stabilizes after elbow point

### Experiments Analyzed

- **ANOVA_L_2_Random**: 50 random folds, 2 subjects per fold
- **ANOVA_L_6_Random**: 50 random folds, 6 subjects per fold
- **PCA_L_2_Random**: 50 random folds, 2 subjects per fold
- **PCA_L_6_Random**: 50 random folds, 6 subjects per fold

**Total**: 48 model×hyperparameter combinations across 4 experiments

## Executive Summary

- **Total Model×HP Combinations Analyzed**: 48
- **Clear Elbow Detected**: 0 (0.0%)
- **Gradual Stabilization Detected**: 48 (100.0%)
- **No Clear Pattern**: 0 (0.0%)

- **Median Stability Point**: 12.0 subjects
- **Mean Stability Point**: 12.0 subjects

### Overall Conclusion

**For models with gradual stabilization (48 models):**

**Key Finding:** All models show a consistent pattern where variance stabilizes at **3 test groups**, regardless of the number of subjects per group.

- **For L_2 experiments (2 subjects per test group):** Stability reached at **3 groups = 6 subjects**
- **For L_6 experiments (6 subjects per test group):** Stability reached at **3 groups = 18 subjects**

**Recommendation:**
- **3 test groups is sufficient** for stable variance estimates
- The absolute number of subjects depends on the experimental design (2 vs 6 subjects per group)
- This suggests that **test group diversity** (number of groups) is more important than total subject count for variance stabilization

## Detailed Results by Experiment

### ANOVA_L_2_Random

#### Models with Gradual Stabilization

| Model×HP | Stability Point (Groups) | Subjects |
|----------|--------------------------|----------|
| KNN (metric=euclidean, n_neighbors=1, weights=uniform)... | 3 | 6 |
| KNN (metric=euclidean, n_neighbors=15, weights=uniform)... | 3 | 6 |
| KNN (metric=euclidean, n_neighbors=7, weights=uniform)... | 3 | 6 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 6 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 6 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 6 |
| SVM (C=0.1, gamma=auto, kernel=linear)... | 3 | 6 |
| SVM (C=0.1, gamma=auto, kernel=poly)... | 3 | 6 |
| SVM (C=0.1, gamma=auto, kernel=rbf)... | 3 | 6 |
| XGBoost (learning_rate=0.2, max_depth=3, n_estimators=100, s... | 3 | 6 |
| XGBoost (learning_rate=0.2, max_depth=6, n_estimators=100, s... | 3 | 6 |
| XGBoost (learning_rate=0.2, max_depth=9, n_estimators=100, s... | 3 | 6 |

### ANOVA_L_6_Random

#### Models with Gradual Stabilization

| Model×HP | Stability Point (Groups) | Subjects |
|----------|--------------------------|----------|
| KNN (metric=euclidean, n_neighbors=1, weights=uniform)... | 3 | 18 |
| KNN (metric=euclidean, n_neighbors=15, weights=uniform)... | 3 | 18 |
| KNN (metric=euclidean, n_neighbors=7, weights=uniform)... | 3 | 18 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 18 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 18 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 18 |
| SVM (C=0.1, gamma=auto, kernel=linear)... | 3 | 18 |
| SVM (C=0.1, gamma=auto, kernel=poly)... | 3 | 18 |
| SVM (C=0.1, gamma=auto, kernel=rbf)... | 3 | 18 |
| XGBoost (learning_rate=0.2, max_depth=3, n_estimators=100, s... | 3 | 18 |
| XGBoost (learning_rate=0.2, max_depth=6, n_estimators=100, s... | 3 | 18 |
| XGBoost (learning_rate=0.2, max_depth=9, n_estimators=100, s... | 3 | 18 |

### PCA_L_2_Random

#### Models with Gradual Stabilization

| Model×HP | Stability Point (Groups) | Subjects |
|----------|--------------------------|----------|
| KNN (metric=euclidean, n_neighbors=1, weights=uniform)... | 3 | 6 |
| KNN (metric=euclidean, n_neighbors=15, weights=uniform)... | 3 | 6 |
| KNN (metric=euclidean, n_neighbors=7, weights=uniform)... | 3 | 6 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 6 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 6 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 6 |
| SVM (C=0.1, gamma=auto, kernel=linear)... | 3 | 6 |
| SVM (C=0.1, gamma=auto, kernel=poly)... | 3 | 6 |
| SVM (C=0.1, gamma=auto, kernel=rbf)... | 3 | 6 |
| XGBoost (learning_rate=0.2, max_depth=3, n_estimators=100, s... | 3 | 6 |
| XGBoost (learning_rate=0.2, max_depth=6, n_estimators=100, s... | 3 | 6 |
| XGBoost (learning_rate=0.2, max_depth=9, n_estimators=100, s... | 3 | 6 |

### PCA_L_6_Random

#### Models with Gradual Stabilization

| Model×HP | Stability Point (Groups) | Subjects |
|----------|--------------------------|----------|
| KNN (metric=euclidean, n_neighbors=1, weights=uniform)... | 3 | 18 |
| KNN (metric=euclidean, n_neighbors=15, weights=uniform)... | 3 | 18 |
| KNN (metric=euclidean, n_neighbors=7, weights=uniform)... | 3 | 18 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 18 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 18 |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_lay... | 3 | 18 |
| SVM (C=0.1, gamma=auto, kernel=linear)... | 3 | 18 |
| SVM (C=0.1, gamma=auto, kernel=poly)... | 3 | 18 |
| SVM (C=0.1, gamma=auto, kernel=rbf)... | 3 | 18 |
| XGBoost (learning_rate=0.2, max_depth=3, n_estimators=100, s... | 3 | 18 |
| XGBoost (learning_rate=0.2, max_depth=6, n_estimators=100, s... | 3 | 18 |
| XGBoost (learning_rate=0.2, max_depth=9, n_estimators=100, s... | 3 | 18 |
