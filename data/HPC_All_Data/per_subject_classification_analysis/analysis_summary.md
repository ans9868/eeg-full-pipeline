# Analysis: ANOVA_L_2_Random
================================================================================

## Overall Statistics

- Total subjects with test data: 49
- Total model×HP combinations: 12
- Total fold observations: 400

### Accuracy Distribution (Across All Folds)
- Mean accuracy: 71.22%
- Median accuracy: 73.80%
- Min accuracy: 16.86%
- Max accuracy: 96.08%
- Std Dev: 14.23%

### Per-Subject Summary
For detailed per-subject median accuracies and fold counts, see: `ANOVA_L_2_Random_per_subject_summary.md`

**Note on Classification Success Rate**: A subject is considered "correctly classified" in a fold if accuracy > 50%. The previous "Classification Success Rate" metric aggregated this across all model×HP combinations, which may be misleading. The per-subject summary provides clearer insight into individual subject performance.

## Per Model×Hyperparameter Statistics

| Model×Hyperparameter | N Subjects | Mean Acc | Median Acc | Min | Max | Std Dev |
|---------------------|------------|----------|------------|-----|-----|---------|
| KNN (metric=euclidean, neighbors=1, weights=unifor | 26 | 64.16% | 63.96% | 49.18% | 79.17% | 8.84% |
| KNN (metric=euclidean, neighbors=15, weights=unifo | 26 | 78.01% | 81.70% | 57.54% | 88.67% | 8.73% |
| KNN (metric=euclidean, neighbors=7, weights=unifor | 29 | 70.99% | 71.28% | 46.42% | 90.89% | 12.03% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 20 | 73.43% | 77.17% | 48.04% | 96.08% | 16.29% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 20 | 71.60% | 73.90% | 46.67% | 92.46% | 13.82% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 39 | 71.98% | 76.94% | 36.15% | 93.07% | 14.70% |
| SVM (C=0.1, gamma=auto, kernel=linear) | 19 | 73.91% | 72.01% | 50.92% | 92.60% | 13.14% |
| SVM (C=0.1, gamma=auto, kernel=poly) | 39 | 69.76% | 74.98% | 16.86% | 86.39% | 15.13% |
| SVM (C=0.1, gamma=auto, kernel=rbf) | 19 | 68.42% | 73.85% | 40.02% | 88.57% | 17.33% |
| XGBoost (depth=3, estimators=100, rate=0.2, subsam | 19 | 66.30% | 62.70% | 44.50% | 94.38% | 18.63% |
| XGBoost (depth=6, estimators=100, rate=0.2, subsam | 19 | 73.03% | 73.39% | 52.46% | 92.89% | 14.32% |
| XGBoost (depth=9, estimators=100, rate=0.2, subsam | 39 | 72.45% | 73.21% | 31.45% | 94.59% | 14.35% |


# Analysis: ANOVA_L_6_Random
================================================================================

## Overall Statistics

- Total subjects with test data: 65
- Total model×HP combinations: 12
- Total fold observations: 1170

### Accuracy Distribution
- Mean accuracy: 68.00%
- Median accuracy: 68.25%
- Min accuracy: 48.65%
- Max accuracy: 87.81%
- Std Dev: 8.58%

### Per-Subject Summary
For detailed per-subject median accuracies and fold counts, see: `ANOVA_L_6_Random_per_subject_summary.md`

**Note on Classification Success Rate**: A subject is considered "correctly classified" in a fold if accuracy > 50%. The previous "Classification Success Rate" metric aggregated this across all model×HP combinations, which may be misleading. The per-subject summary provides clearer insight into individual subject performance.

## Per Model×Hyperparameter Statistics

| Model×Hyperparameter | N Subjects | Mean Acc | Median Acc | Min | Max | Std Dev |
|---------------------|------------|----------|------------|-----|-----|---------|
| KNN (metric=euclidean, neighbors=1, weights=unifor | 54 | 65.33% | 65.55% | 55.13% | 70.01% | 3.46% |
| KNN (metric=euclidean, neighbors=15, weights=unifo | 53 | 71.29% | 72.59% | 55.67% | 82.64% | 6.88% |
| KNN (metric=euclidean, neighbors=7, weights=unifor | 46 | 67.17% | 68.21% | 51.12% | 77.45% | 7.59% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 61 | 70.68% | 71.96% | 52.65% | 87.81% | 8.34% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 45 | 71.44% | 72.96% | 53.84% | 87.11% | 9.98% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 27 | 68.83% | 69.21% | 56.50% | 74.82% | 6.12% |
| SVM (C=0.1, gamma=auto, kernel=linear) | 54 | 71.47% | 72.19% | 50.13% | 85.59% | 9.18% |
| SVM (C=0.1, gamma=auto, kernel=poly) | 51 | 65.73% | 65.75% | 53.33% | 83.64% | 7.94% |
| SVM (C=0.1, gamma=auto, kernel=rbf) | 47 | 61.21% | 62.82% | 49.86% | 75.96% | 7.48% |
| XGBoost (depth=3, estimators=100, rate=0.2, subsam | 45 | 72.78% | 73.66% | 57.28% | 86.08% | 9.46% |
| XGBoost (depth=6, estimators=100, rate=0.2, subsam | 37 | 65.11% | 68.55% | 52.74% | 76.30% | 8.65% |
| XGBoost (depth=9, estimators=100, rate=0.2, subsam | 61 | 65.31% | 65.20% | 48.65% | 81.32% | 7.96% |


# Analysis: PCA_L_2_Random
================================================================================

## Overall Statistics

- Total subjects with test data: 49
- Total model×HP combinations: 12
- Total fold observations: 400

### Accuracy Distribution
- Mean accuracy: 55.22%
- Median accuracy: 53.06%
- Min accuracy: 28.25%
- Max accuracy: 90.44%
- Std Dev: 9.92%

### Per-Subject Summary
For detailed per-subject median accuracies and fold counts, see: `PCA_L_2_Random_per_subject_summary.md`

**Note on Classification Success Rate**: A subject is considered "correctly classified" in a fold if accuracy > 50%. The previous "Classification Success Rate" metric aggregated this across all model×HP combinations, which may be misleading. The per-subject summary provides clearer insight into individual subject performance.

## Per Model×Hyperparameter Statistics

| Model×Hyperparameter | N Subjects | Mean Acc | Median Acc | Min | Max | Std Dev |
|---------------------|------------|----------|------------|-----|-----|---------|
| KNN (metric=euclidean, neighbors=1, weights=unifor | 40 | 52.05% | 51.98% | 37.43% | 76.20% | 6.81% |
| KNN (metric=euclidean, neighbors=15, weights=unifo | 19 | 58.38% | 55.22% | 51.24% | 71.79% | 7.23% |
| KNN (metric=euclidean, neighbors=7, weights=unifor | 21 | 55.56% | 57.26% | 28.25% | 76.83% | 11.36% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 20 | 52.48% | 51.48% | 41.18% | 68.03% | 7.33% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 18 | 53.03% | 51.26% | 30.03% | 90.44% | 14.49% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 37 | 56.75% | 52.97% | 38.46% | 87.04% | 10.05% |
| SVM (C=0.1, gamma=auto, kernel=linear) | 20 | 51.32% | 51.48% | 38.34% | 59.58% | 6.09% |
| SVM (C=0.1, gamma=auto, kernel=poly) | 24 | 47.50% | 48.82% | 30.03% | 58.10% | 6.43% |
| SVM (C=0.1, gamma=auto, kernel=rbf) | 38 | 61.25% | 59.80% | 41.45% | 84.04% | 11.51% |
| XGBoost (depth=3, estimators=100, rate=0.2, subsam | 23 | 60.07% | 57.59% | 48.69% | 87.83% | 10.57% |
| XGBoost (depth=6, estimators=100, rate=0.2, subsam | 32 | 52.99% | 51.42% | 31.07% | 69.57% | 8.24% |
| XGBoost (depth=9, estimators=100, rate=0.2, subsam | 30 | 56.38% | 56.11% | 43.44% | 69.27% | 7.57% |


# Analysis: PCA_L_6_Random
================================================================================

## Overall Statistics

- Total subjects with test data: 65
- Total model×HP combinations: 12
- Total fold observations: 1200

### Accuracy Distribution
- Mean accuracy: 54.63%
- Median accuracy: 53.30%
- Min accuracy: 37.94%
- Max accuracy: 80.04%
- Std Dev: 6.97%

### Per-Subject Summary
For detailed per-subject median accuracies and fold counts, see: `PCA_L_6_Random_per_subject_summary.md`

**Note on Classification Success Rate**: A subject is considered "correctly classified" in a fold if accuracy > 50%. The previous "Classification Success Rate" metric aggregated this across all model×HP combinations, which may be misleading. The per-subject summary provides clearer insight into individual subject performance.

## Per Model×Hyperparameter Statistics

| Model×Hyperparameter | N Subjects | Mean Acc | Median Acc | Min | Max | Std Dev |
|---------------------|------------|----------|------------|-----|-----|---------|
| KNN (metric=euclidean, neighbors=1, weights=unifor | 45 | 52.81% | 51.70% | 47.07% | 68.41% | 5.27% |
| KNN (metric=euclidean, neighbors=15, weights=unifo | 47 | 55.78% | 54.38% | 47.33% | 72.37% | 7.51% |
| KNN (metric=euclidean, neighbors=7, weights=unifor | 58 | 55.59% | 54.12% | 47.01% | 65.86% | 5.48% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 52 | 55.40% | 54.46% | 46.34% | 64.70% | 5.33% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 46 | 58.49% | 55.01% | 49.07% | 74.36% | 7.53% |
| MLP_(Neural_Network) (activation=tanh, alpha=0.1,  | 57 | 55.92% | 54.34% | 42.90% | 80.04% | 8.84% |
| SVM (C=0.1, gamma=auto, kernel=linear) | 51 | 49.36% | 49.68% | 41.12% | 58.30% | 4.34% |
| SVM (C=0.1, gamma=auto, kernel=poly) | 49 | 49.25% | 49.24% | 44.26% | 53.91% | 2.57% |
| SVM (C=0.1, gamma=auto, kernel=rbf) | 56 | 58.45% | 57.82% | 47.06% | 74.08% | 7.27% |
| XGBoost (depth=3, estimators=100, rate=0.2, subsam | 38 | 53.46% | 54.59% | 46.64% | 60.25% | 4.62% |
| XGBoost (depth=6, estimators=100, rate=0.2, subsam | 61 | 54.14% | 53.37% | 37.94% | 70.63% | 7.12% |
| XGBoost (depth=9, estimators=100, rate=0.2, subsam | 38 | 54.96% | 53.05% | 47.43% | 68.02% | 5.84% |
