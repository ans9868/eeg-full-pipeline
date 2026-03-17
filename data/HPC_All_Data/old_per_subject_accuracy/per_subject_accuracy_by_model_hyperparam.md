# Per-Subject Accuracy Analysis by Model × Hyperparameter

This analysis shows per-subject accuracy broken down by each model×hyperparameter combination.

## Cross-Model×Hyperparameter Swings (Biggest Variance Across All Combinations)

| Rank | Subject | Experiment | Swing | Range (Min-Max) | Mean | N Combinations |
|------|---------|------------|-------|-----------------|------|----------------|
| 1 | sub-3 | ANOVA_L_2_Random | 74.1% | 16.9% - 90.9% | 68.8% | 5 |
| 2 | sub-60 | ANOVA_L_2_Random | 61.1% | 16.9% - 78.0% | 55.2% | 4 |
| 3 | sub-11 | ANOVA_L_2_Random | 52.4% | 40.0% - 92.5% | 65.0% | 7 |
| 4 | sub-30 | PCA_L_2_Random | 52.1% | 38.3% - 90.4% | 56.8% | 8 |
| 5 | sub-18 | PCA_L_2_Random | 49.6% | 37.4% - 87.0% | 55.5% | 12 |
| 6 | sub-3 | PCA_L_2_Random | 47.9% | 28.3% - 76.2% | 49.4% | 8 |
| 7 | sub-18 | ANOVA_L_2_Random | 44.6% | 46.5% - 91.1% | 73.1% | 12 |
| 8 | sub-49 | PCA_L_2_Random | 44.4% | 46.0% - 90.4% | 61.6% | 11 |
| 9 | sub-15 | ANOVA_L_2_Random | 44.3% | 48.7% - 93.1% | 66.1% | 12 |
| 10 | sub-15 | PCA_L_2_Random | 40.2% | 43.9% - 84.0% | 55.1% | 12 |
| 11 | sub-57 | PCA_L_2_Random | 39.5% | 47.5% - 87.0% | 62.3% | 4 |
| 12 | sub-7 | PCA_L_2_Random | 38.9% | 49.0% - 87.8% | 62.4% | 11 |
| 13 | sub-49 | ANOVA_L_2_Random | 38.0% | 56.6% - 94.6% | 79.3% | 9 |
| 14 | sub-54 | ANOVA_L_2_Random | 37.2% | 55.3% - 92.5% | 74.0% | 11 |
| 15 | sub-57 | ANOVA_L_6_Random | 37.0% | 50.1% - 87.1% | 69.6% | 11 |
| 16 | sub-8 | PCA_L_6_Random | 36.8% | 43.3% - 80.0% | 53.5% | 11 |
| 17 | sub-42 | PCA_L_6_Random | 36.8% | 43.3% - 80.0% | 53.3% | 10 |
| 18 | sub-21 | ANOVA_L_6_Random | 36.5% | 50.6% - 87.1% | 70.5% | 8 |
| 19 | sub-23 | PCA_L_2_Random | 36.4% | 40.2% - 76.6% | 62.7% | 4 |
| 20 | sub-56 | PCA_L_2_Random | 36.4% | 40.2% - 76.6% | 61.2% | 10 |
| 21 | sub-32 | ANOVA_L_6_Random | 36.0% | 51.1% - 87.1% | 66.9% | 11 |
| 22 | sub-39 | PCA_L_2_Random | 35.9% | 47.0% - 82.9% | 58.5% | 7 |
| 23 | sub-60 | ANOVA_L_6_Random | 35.9% | 52.0% - 87.8% | 69.0% | 12 |
| 24 | sub-14 | ANOVA_L_6_Random | 35.1% | 52.0% - 87.1% | 70.7% | 11 |
| 25 | sub-65 | ANOVA_L_6_Random | 35.1% | 52.0% - 87.1% | 72.4% | 9 |
| 26 | sub-35 | PCA_L_2_Random | 34.8% | 47.0% - 81.8% | 54.2% | 5 |
| 27 | sub-28 | PCA_L_6_Random | 34.6% | 45.4% - 80.0% | 56.0% | 12 |
| 28 | sub-35 | ANOVA_L_2_Random | 34.3% | 52.0% - 86.4% | 66.6% | 8 |
| 29 | sub-19 | ANOVA_L_2_Random | 34.3% | 51.9% - 86.2% | 66.1% | 5 |
| 30 | sub-37 | PCA_L_6_Random | 34.1% | 45.9% - 80.0% | 58.7% | 10 |

---

## ANOVA_L_6_Random - Detailed Breakdown

### sub-1 (Cross-Model Swing: 19.34%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 72.59% | 72.59% | 72.59% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 62.41% | 62.41% | 62.41% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 64.89% | 64.89% | 64.89% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 56.50% | 56.50% | 56.50% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 73.10% | 73.10% | 73.10% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 68.25% | 68.25% | 68.25% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 56.10% | 56.10% | 56.10% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 53.76% | 53.76% | 53.76% | 0.00% | 0.00% | 1 |

### sub-10 (Cross-Model Swing: 17.49%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 51.12% | 51.12% | 51.12% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 65.25% | 65.25% | 65.25% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 60.85% | 53.09% | 68.61% | 15.52% | 10.97% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 59.89% | 57.39% | 62.40% | 5.01% | 3.54% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 55.85% | 51.81% | 59.90% | 8.09% | 5.72% | 2 |

### sub-11 (Cross-Model Swing: 31.87%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 70.46% | 55.67% | 75.92% | 20.25% | 7.36% | 6 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 76.86% | 74.25% | 79.47% | 5.23% | 3.70% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 77.91% | 77.91% | 77.91% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 64.88% | 56.50% | 69.21% | 12.71% | 7.25% | 3 |
| SVM | C=0.1, gamma=auto, kernel=linear | 70.25% | 50.13% | 82.00% | 31.87% | 11.96% | 5 |
| SVM | C=0.1, gamma=auto, kernel=poly | 67.43% | 67.43% | 67.43% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 79.93% | 79.33% | 80.53% | 1.20% | 0.85% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 61.95% | 53.76% | 69.61% | 15.85% | 8.30% | 4 |

### sub-12 (Cross-Model Swing: 34.03%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 77.52% | 77.52% | 77.52% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 64.56% | 64.56% | 64.56% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 77.59% | 77.59% | 77.59% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 82.68% | 82.68% | 82.68% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 58.79% | 58.79% | 58.79% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 75.58% | 75.58% | 75.58% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 48.65% | 48.65% | 48.65% | 0.00% | 0.00% | 1 |

### sub-13 (Cross-Model Swing: 26.44%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 61.91% | 61.91% | 61.91% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 73.09% | 69.53% | 76.65% | 7.12% | 5.03% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 67.78% | 65.55% | 70.01% | 4.46% | 3.15% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 70.77% | 64.68% | 75.90% | 11.22% | 4.76% | 4 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 63.64% | 63.64% | 63.64% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 65.00% | 65.00% | 65.00% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 68.06% | 63.75% | 72.38% | 8.63% | 6.10% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 65.36% | 63.25% | 67.47% | 4.23% | 2.99% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 69.60% | 64.84% | 79.18% | 14.35% | 6.51% | 4 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 52.74% | 52.74% | 52.74% | 0.00% | 0.00% | 1 |

### sub-14 (Cross-Model Swing: 35.14%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 68.47% | 61.93% | 78.91% | 16.97% | 9.13% | 3 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 77.45% | 77.45% | 77.45% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 67.66% | 67.66% | 67.66% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 75.72% | 67.14% | 84.30% | 17.16% | 12.13% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 70.47% | 53.84% | 87.11% | 33.27% | 23.53% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 71.30% | 57.75% | 85.59% | 27.84% | 13.94% | 3 |
| SVM | C=0.1, gamma=auto, kernel=poly | 83.64% | 83.64% | 83.64% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 51.96% | 51.96% | 51.96% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 66.99% | 57.28% | 86.05% | 28.77% | 16.50% | 3 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 73.25% | 73.25% | 73.25% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 76.30% | 76.30% | 76.30% | 0.00% | 0.00% | 1 |

### sub-15 (Cross-Model Swing: 30.96%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 72.68% | 63.53% | 78.74% | 15.21% | 8.06% | 3 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 65.40% | 57.57% | 70.58% | 13.01% | 5.54% | 4 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 70.21% | 56.53% | 77.44% | 20.91% | 11.86% | 3 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 79.53% | 77.51% | 81.54% | 4.03% | 2.85% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 74.34% | 74.34% | 74.34% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 76.03% | 74.14% | 77.93% | 3.79% | 2.68% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 76.08% | 76.08% | 76.08% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 60.34% | 50.58% | 66.04% | 15.46% | 6.78% | 4 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 71.21% | 64.71% | 81.04% | 16.33% | 8.66% | 3 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 70.64% | 62.65% | 81.32% | 18.66% | 8.05% | 4 |

### sub-16 (Cross-Model Swing: 20.61%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 68.56% | 68.56% | 68.56% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 66.68% | 65.55% | 67.80% | 2.25% | 1.59% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 73.64% | 64.68% | 82.60% | 17.92% | 12.67% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 65.08% | 65.08% | 65.08% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 61.99% | 61.99% | 61.99% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 65.23% | 63.25% | 67.22% | 3.97% | 2.81% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 71.60% | 64.84% | 78.36% | 13.52% | 9.56% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 62.97% | 62.97% | 62.97% | 0.00% | 0.00% | 1 |

### sub-17 (Cross-Model Swing: 28.41%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 74.57% | 69.94% | 77.52% | 7.58% | 4.06% | 3 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 66.47% | 65.25% | 67.70% | 2.45% | 1.73% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 69.48% | 68.61% | 70.33% | 1.72% | 0.86% | 3 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 77.59% | 77.59% | 77.59% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 74.82% | 74.82% | 74.82% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 76.97% | 68.37% | 82.68% | 14.31% | 7.58% | 3 |
| SVM | C=0.1, gamma=auto, kernel=poly | 54.27% | 54.27% | 54.27% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 62.40% | 62.40% | 62.40% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 74.62% | 73.66% | 75.58% | 1.92% | 1.36% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 61.99% | 59.90% | 64.09% | 4.19% | 2.96% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 74.39% | 74.39% | 74.39% | 0.00% | 0.00% | 1 |

### sub-18 (Cross-Model Swing: 10.14%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 72.48% | 71.55% | 73.42% | 1.87% | 1.32% | 2 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 73.65% | 73.65% | 73.65% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 69.51% | 69.51% | 69.51% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 72.25% | 69.44% | 74.25% | 4.81% | 2.50% | 3 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 68.41% | 68.41% | 68.41% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 71.94% | 69.14% | 74.74% | 5.61% | 3.96% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 65.49% | 64.60% | 66.38% | 1.78% | 1.26% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 65.40% | 65.40% | 65.40% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 72.97% | 72.85% | 73.09% | 0.24% | 0.17% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 69.61% | 69.61% | 69.61% | 0.00% | 0.00% | 1 |

### sub-19 (Cross-Model Swing: 19.98%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 67.90% | 66.43% | 69.38% | 2.96% | 2.09% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 65.89% | 65.89% | 65.89% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 71.96% | 71.96% | 71.96% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 69.21% | 69.21% | 69.21% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 62.63% | 62.63% | 62.63% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 76.08% | 76.08% | 76.08% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 71.23% | 71.23% | 71.23% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 71.32% | 61.33% | 81.32% | 19.98% | 14.13% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 71.81% | 71.81% | 71.81% | 0.00% | 0.00% | 1 |

### sub-2 (Cross-Model Swing: 22.14%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 65.39% | 61.91% | 71.55% | 9.64% | 4.25% | 4 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 62.51% | 62.51% | 62.51% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 71.01% | 67.14% | 74.88% | 7.74% | 5.47% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 66.03% | 63.64% | 68.41% | 4.77% | 3.37% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 74.34% | 74.34% | 74.34% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 68.23% | 65.00% | 70.55% | 5.55% | 2.88% | 3 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 58.53% | 53.75% | 63.32% | 9.56% | 6.76% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 63.52% | 57.28% | 67.89% | 10.61% | 5.55% | 3 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 69.54% | 69.54% | 69.54% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 52.74% | 52.74% | 52.74% | 0.00% | 0.00% | 1 |

### sub-20 (Cross-Model Swing: 18.85%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 69.53% | 69.53% | 69.53% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 68.91% | 67.80% | 70.01% | 2.21% | 1.56% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 76.11% | 69.85% | 82.60% | 12.75% | 6.38% | 3 |
| SVM | C=0.1, gamma=auto, kernel=poly | 68.06% | 63.75% | 72.38% | 8.63% | 6.10% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 67.22% | 67.22% | 67.22% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 74.67% | 66.47% | 79.18% | 12.72% | 7.12% | 3 |

### sub-21 (Cross-Model Swing: 36.53%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 78.91% | 78.91% | 78.91% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 62.31% | 57.57% | 67.04% | 9.48% | 6.70% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 66.60% | 56.53% | 76.67% | 20.15% | 14.25% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 87.11% | 87.11% | 87.11% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 85.59% | 85.59% | 85.59% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 58.31% | 50.58% | 66.04% | 15.46% | 10.94% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 86.05% | 86.05% | 86.05% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 67.25% | 62.65% | 71.84% | 9.19% | 6.50% | 2 |

### sub-22 (Cross-Model Swing: 23.66%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 77.45% | 77.45% | 77.45% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 63.31% | 63.31% | 63.31% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 73.82% | 64.01% | 83.64% | 19.64% | 13.89% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 59.98% | 59.98% | 59.98% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 76.30% | 76.30% | 76.30% | 0.00% | 0.00% | 1 |

### sub-23 (Cross-Model Swing: 9.22%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 69.94% | 69.94% | 69.94% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 75.74% | 75.74% | 75.74% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 73.54% | 69.49% | 77.59% | 8.09% | 5.72% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 68.37% | 68.37% | 68.37% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 70.53% | 70.53% | 70.53% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 73.66% | 73.66% | 73.66% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 71.81% | 71.81% | 71.81% | 0.00% | 0.00% | 1 |

### sub-24 (Cross-Model Swing: 12.91%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 75.78% | 75.78% | 75.78% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 75.15% | 73.65% | 76.65% | 3.00% | 2.12% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 71.05% | 69.44% | 72.67% | 3.23% | 2.28% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 77.51% | 77.51% | 77.51% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 74.14% | 74.14% | 74.14% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 64.60% | 64.60% | 64.60% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 67.47% | 67.47% | 67.47% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 64.71% | 64.71% | 64.71% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 70.39% | 67.92% | 72.85% | 4.93% | 3.49% | 2 |

### sub-25 (Cross-Model Swing: 19.06%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 55.67% | 55.67% | 55.67% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 57.80% | 57.80% | 57.80% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 64.55% | 64.55% | 64.55% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 56.96% | 52.65% | 61.27% | 8.63% | 6.10% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 68.92% | 68.92% | 68.92% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 50.13% | 50.13% | 50.13% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 65.11% | 65.11% | 65.11% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 49.86% | 49.86% | 49.86% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 58.46% | 56.49% | 60.42% | 3.92% | 2.78% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 55.86% | 55.86% | 55.86% | 0.00% | 0.00% | 1 |

### sub-26 (Cross-Model Swing: 23.10%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 77.10% | 72.88% | 82.64% | 9.76% | 5.01% | 3 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 70.01% | 70.01% | 70.01% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 81.06% | 75.90% | 87.81% | 11.92% | 6.12% | 3 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 77.51% | 77.51% | 77.51% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 74.14% | 74.14% | 74.14% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 69.69% | 67.43% | 72.38% | 4.95% | 2.50% | 3 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 76.71% | 64.71% | 86.08% | 21.37% | 10.92% | 3 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 79.18% | 79.18% | 79.18% | 0.00% | 0.00% | 1 |

### sub-27 (Cross-Model Swing: 19.55%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 73.19% | 68.56% | 78.74% | 10.18% | 5.15% | 3 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 75.74% | 75.74% | 75.74% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 77.59% | 77.59% | 77.59% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 73.31% | 65.08% | 81.54% | 16.46% | 11.64% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 69.21% | 69.21% | 69.21% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 70.40% | 61.99% | 77.93% | 15.94% | 8.00% | 3 |
| SVM | C=0.1, gamma=auto, kernel=poly | 70.53% | 70.53% | 70.53% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 81.04% | 81.04% | 81.04% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 71.81% | 71.81% | 71.81% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 65.76% | 62.97% | 68.55% | 5.58% | 3.95% | 2 |

## ANOVA_L_2_Random - Detailed Breakdown

### sub-1 (Cross-Model Swing: 27.77%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 62.55% | 57.89% | 67.20% | 9.31% | 6.58% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 48.04% | 48.04% | 48.04% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 75.81% | 75.81% | 75.81% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 53.53% | 53.53% | 53.53% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 62.69% | 62.69% | 62.69% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 55.43% | 55.43% | 55.43% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 58.39% | 58.39% | 58.39% | 0.00% | 0.00% | 1 |

### sub-11 (Cross-Model Swing: 52.44%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 60.85% | 46.42% | 75.27% | 28.84% | 20.39% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 53.58% | 53.58% | 53.58% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 92.46% | 92.46% | 92.46% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 40.02% | 40.02% | 40.02% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 86.62% | 86.62% | 86.62% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 81.10% | 81.10% | 81.10% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 44.50% | 44.50% | 44.50% | 0.00% | 0.00% | 1 |

### sub-13 (Cross-Model Swing: 21.38%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 52.83% | 52.83% | 52.83% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 36.15% | 36.15% | 36.15% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 49.57% | 49.57% | 49.57% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 31.45% | 31.45% | 31.45% | 0.00% | 0.00% | 1 |

### sub-14 (Cross-Model Swing: 29.14%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 72.65% | 72.65% | 72.65% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 68.15% | 62.39% | 73.91% | 11.51% | 8.14% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 66.40% | 53.97% | 83.11% | 29.14% | 15.03% | 3 |
| SVM | C=0.1, gamma=auto, kernel=poly | 69.53% | 59.43% | 76.23% | 16.80% | 8.90% | 3 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 64.98% | 54.42% | 81.38% | 26.96% | 14.40% | 3 |

### sub-15 (Cross-Model Swing: 44.34%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 65.98% | 62.17% | 69.78% | 7.60% | 5.38% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 49.18% | 49.18% | 49.18% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 77.72% | 77.72% | 77.72% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 76.37% | 76.37% | 76.37% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 73.89% | 54.72% | 93.07% | 38.35% | 27.12% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 60.26% | 60.26% | 60.26% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 48.79% | 48.79% | 48.79% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 65.86% | 48.73% | 82.98% | 34.25% | 24.22% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 66.87% | 66.87% | 66.87% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 62.41% | 62.41% | 62.41% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 70.64% | 56.53% | 84.74% | 28.20% | 19.94% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 63.38% | 63.38% | 63.38% | 0.00% | 0.00% | 1 |

### sub-16 (Cross-Model Swing: 19.51%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 76.57% | 76.57% | 76.57% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 96.08% | 96.08% | 96.08% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 92.60% | 92.60% | 92.60% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 89.02% | 89.02% | 89.02% | 0.00% | 0.00% | 1 |

### sub-17 (Cross-Model Swing: 12.49%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 89.97% | 89.97% | 89.97% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 77.48% | 77.48% | 77.48% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 88.57% | 88.57% | 88.57% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 82.85% | 82.85% | 82.85% | 0.00% | 0.00% | 1 |

### sub-18 (Cross-Model Swing: 44.60%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 71.21% | 57.49% | 84.93% | 27.44% | 19.41% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 75.65% | 72.13% | 79.17% | 7.04% | 4.98% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 79.46% | 74.45% | 84.47% | 10.01% | 7.08% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 83.89% | 83.89% | 83.89% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 79.14% | 68.61% | 91.09% | 22.47% | 9.28% | 4 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 46.67% | 46.67% | 46.67% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 87.89% | 87.89% | 87.89% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 67.18% | 57.90% | 75.90% | 18.00% | 8.95% | 4 |
| SVM | C=0.1, gamma=auto, kernel=linear | 50.92% | 50.92% | 50.92% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 89.63% | 89.63% | 89.63% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 77.87% | 71.34% | 84.73% | 13.39% | 6.73% | 4 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 46.49% | 46.49% | 46.49% | 0.00% | 0.00% | 1 |

### sub-19 (Cross-Model Swing: 34.29%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 56.94% | 56.94% | 56.94% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 72.95% | 72.95% | 72.95% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 65.26% | 53.69% | 76.83% | 23.14% | 16.36% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 72.15% | 58.08% | 86.22% | 28.13% | 19.89% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 61.97% | 51.93% | 72.01% | 20.07% | 14.19% | 2 |

### sub-2 (Cross-Model Swing: 14.91%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 65.85% | 64.85% | 66.86% | 2.00% | 1.42% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 77.30% | 77.30% | 77.30% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 62.92% | 62.92% | 62.92% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 73.25% | 73.25% | 73.25% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 74.07% | 74.07% | 74.07% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 65.68% | 65.68% | 65.68% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 62.39% | 62.39% | 62.39% | 0.00% | 0.00% | 1 |

### sub-21 (Cross-Model Swing: 24.69%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 63.96% | 63.96% | 63.96% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 84.12% | 84.12% | 84.12% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 59.42% | 59.42% | 59.42% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 74.87% | 74.87% | 74.87% | 0.00% | 0.00% | 1 |

### sub-22 (Cross-Model Swing: 23.12%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 75.48% | 75.48% | 75.48% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 55.68% | 55.68% | 55.68% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 78.79% | 78.79% | 78.79% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 71.56% | 71.56% | 71.56% | 0.00% | 0.00% | 1 |

### sub-23 (Cross-Model Swing: 28.12%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 56.00% | 56.00% | 56.00% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 71.06% | 71.06% | 71.06% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 84.12% | 84.12% | 84.12% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 73.53% | 73.53% | 73.53% | 0.00% | 0.00% | 1 |

### sub-24 (Cross-Model Swing: 16.45%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 87.27% | 83.66% | 90.89% | 7.24% | 5.12% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 86.97% | 86.97% | 86.97% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 92.05% | 92.05% | 92.05% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 87.63% | 87.63% | 87.63% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 84.43% | 84.43% | 84.43% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 76.98% | 76.98% | 76.98% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 76.48% | 76.48% | 76.48% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 91.86% | 91.86% | 91.86% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 84.33% | 84.33% | 84.33% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 87.54% | 87.54% | 87.54% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 92.93% | 92.93% | 92.93% | 0.00% | 0.00% | 1 |

### sub-28 (Cross-Model Swing: 30.83%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 70.36% | 70.36% | 70.36% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 81.70% | 81.70% | 81.70% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 57.19% | 50.88% | 63.50% | 12.63% | 8.93% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 67.01% | 60.94% | 73.09% | 12.15% | 8.59% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 66.34% | 52.72% | 79.96% | 27.24% | 19.26% | 2 |

### sub-3 (Cross-Model Swing: 74.07%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 57.84% | 57.84% | 57.84% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 81.99% | 81.99% | 81.99% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 79.91% | 77.96% | 81.86% | 3.91% | 2.76% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 45.71% | 16.86% | 74.56% | 57.70% | 40.80% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 79.49% | 68.05% | 90.93% | 22.88% | 16.18% | 2 |

### sub-30 (Cross-Model Swing: 19.04%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 75.44% | 75.44% | 75.44% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 86.25% | 86.25% | 86.25% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 80.67% | 75.56% | 85.78% | 10.22% | 7.23% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 79.38% | 75.41% | 83.35% | 7.95% | 5.62% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 90.06% | 85.66% | 94.45% | 8.79% | 6.21% | 2 |

### sub-33 (Cross-Model Swing: 28.43%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 59.46% | 59.46% | 59.46% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 87.89% | 87.89% | 87.89% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 82.57% | 82.57% | 82.57% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 74.04% | 74.04% | 74.04% | 0.00% | 0.00% | 1 |

### sub-35 (Cross-Model Swing: 34.34%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 59.73% | 59.73% | 59.73% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 83.55% | 83.55% | 83.55% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 52.05% | 52.05% | 52.05% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 78.26% | 78.26% | 78.26% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 54.30% | 54.30% | 54.30% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 86.39% | 86.39% | 86.39% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 52.46% | 52.46% | 52.46% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 65.97% | 65.97% | 65.97% | 0.00% | 0.00% | 1 |

### sub-36 (Cross-Model Swing: 23.53%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 56.01% | 56.01% | 56.01% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 71.99% | 71.99% | 71.99% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 65.50% | 65.50% | 65.50% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 48.46% | 48.46% | 48.46% | 0.00% | 0.00% | 1 |

## PCA_L_6_Random - Detailed Breakdown

### sub-1 (Cross-Model Swing: 20.87%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 64.62% | 64.62% | 64.62% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 55.85% | 55.85% | 55.85% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 53.99% | 53.99% | 53.99% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 46.78% | 46.78% | 46.78% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 45.41% | 45.41% | 45.41% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 66.28% | 66.28% | 66.28% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 46.06% | 46.06% | 46.06% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 47.27% | 47.27% | 47.27% | 0.00% | 0.00% | 1 |

### sub-10 (Cross-Model Swing: 16.37%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 48.51% | 48.51% | 48.51% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 47.33% | 47.33% | 47.33% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 63.70% | 63.70% | 63.70% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 60.79% | 60.79% | 60.79% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 59.57% | 58.73% | 60.40% | 1.68% | 1.18% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 57.27% | 56.46% | 58.09% | 1.62% | 1.15% | 2 |

### sub-11 (Cross-Model Swing: 28.95%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 55.11% | 49.91% | 58.23% | 8.32% | 4.54% | 3 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 49.20% | 47.07% | 51.34% | 4.27% | 3.02% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 55.85% | 55.85% | 55.85% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 66.89% | 66.89% | 66.89% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 57.22% | 57.22% | 57.22% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 53.03% | 42.90% | 66.72% | 23.82% | 10.59% | 4 |
| SVM | C=0.1, gamma=auto, kernel=poly | 46.33% | 45.18% | 47.47% | 2.28% | 1.61% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 46.45% | 41.12% | 53.31% | 12.20% | 5.06% | 4 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 51.12% | 37.94% | 63.31% | 25.36% | 10.12% | 6 |

### sub-12 (Cross-Model Swing: 19.77%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 54.56% | 54.56% | 54.56% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 69.31% | 69.31% | 69.31% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 50.90% | 50.90% | 50.90% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 54.46% | 54.46% | 54.46% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 49.69% | 49.69% | 49.69% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 50.63% | 50.63% | 50.63% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 51.77% | 49.54% | 53.99% | 4.45% | 3.15% | 2 |

### sub-13 (Cross-Model Swing: 28.44%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 56.45% | 53.60% | 59.29% | 5.69% | 4.02% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 58.10% | 47.79% | 68.41% | 20.61% | 14.58% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 51.10% | 51.10% | 51.10% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 57.74% | 48.80% | 76.23% | 27.43% | 10.95% | 5 |
| SVM | C=0.1, gamma=auto, kernel=poly | 51.31% | 50.28% | 52.34% | 2.05% | 1.45% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 49.22% | 49.22% | 49.22% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 57.02% | 54.69% | 59.36% | 4.67% | 3.30% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 56.12% | 52.76% | 59.04% | 6.29% | 3.17% | 3 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 63.85% | 59.68% | 68.02% | 8.33% | 5.89% | 2 |

### sub-14 (Cross-Model Swing: 21.01%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 51.80% | 49.91% | 53.69% | 3.78% | 2.67% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 52.78% | 51.70% | 53.86% | 2.15% | 1.52% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 50.34% | 50.34% | 50.34% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 59.27% | 49.07% | 68.08% | 19.01% | 9.58% | 3 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 51.39% | 51.39% | 51.39% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 47.07% | 47.07% | 47.07% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 51.10% | 50.77% | 51.44% | 0.67% | 0.48% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 51.38% | 49.68% | 53.08% | 3.40% | 2.40% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 48.20% | 48.20% | 48.20% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 55.91% | 51.35% | 63.60% | 12.25% | 5.32% | 4 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 52.63% | 52.63% | 52.63% | 0.00% | 0.00% | 1 |

### sub-15 (Cross-Model Swing: 26.21%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 58.70% | 53.49% | 62.60% | 9.12% | 4.70% | 3 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 51.86% | 49.24% | 57.61% | 8.37% | 3.88% | 4 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 59.28% | 59.28% | 59.28% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 58.28% | 51.85% | 64.70% | 12.85% | 9.09% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 56.45% | 47.86% | 63.18% | 15.32% | 7.63% | 4 |
| SVM | C=0.1, gamma=auto, kernel=poly | 49.10% | 49.10% | 49.10% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 52.71% | 51.28% | 54.14% | 2.87% | 2.03% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 61.68% | 52.78% | 74.08% | 21.29% | 9.62% | 4 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 57.40% | 49.49% | 63.86% | 14.37% | 7.29% | 3 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 53.61% | 53.61% | 53.61% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 51.24% | 48.52% | 53.29% | 4.76% | 2.45% | 3 |

### sub-16 (Cross-Model Swing: 27.12%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 58.60% | 50.34% | 68.41% | 18.07% | 9.13% | 3 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 60.84% | 49.11% | 76.23% | 27.12% | 13.93% | 3 |
| SVM | C=0.1, gamma=auto, kernel=poly | 53.12% | 52.34% | 53.91% | 1.57% | 1.11% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 59.09% | 59.09% | 59.09% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 55.46% | 54.35% | 56.56% | 2.20% | 1.56% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 55.80% | 55.80% | 55.80% | 0.00% | 0.00% | 1 |

### sub-17 (Cross-Model Swing: 25.09%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 57.04% | 56.00% | 58.09% | 2.09% | 1.48% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 48.51% | 48.51% | 48.51% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 70.84% | 69.31% | 72.37% | 3.06% | 2.16% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 55.88% | 50.90% | 63.70% | 12.80% | 6.86% | 3 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 47.77% | 47.77% | 47.77% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 52.33% | 52.33% | 52.33% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 48.48% | 47.28% | 49.69% | 2.41% | 1.70% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 58.30% | 58.30% | 58.30% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 57.65% | 54.89% | 60.40% | 5.51% | 3.90% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 54.62% | 48.41% | 61.46% | 13.05% | 6.55% | 3 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 56.83% | 55.57% | 58.09% | 2.51% | 1.78% | 2 |

### sub-18 (Cross-Model Swing: 15.93%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 51.64% | 50.63% | 53.07% | 2.43% | 1.27% | 3 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 51.34% | 51.34% | 51.34% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 52.11% | 46.34% | 56.27% | 9.94% | 5.16% | 3 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 55.71% | 55.71% | 55.71% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 48.36% | 47.47% | 49.24% | 1.78% | 1.26% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 50.95% | 50.95% | 50.95% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 51.61% | 51.61% | 51.61% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 54.35% | 49.65% | 62.27% | 12.62% | 6.90% | 3 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 46.64% | 46.64% | 46.64% | 0.00% | 0.00% | 1 |

### sub-19 (Cross-Model Swing: 32.31%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 62.60% | 62.60% | 62.60% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 52.60% | 52.60% | 52.60% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 61.66% | 61.66% | 61.66% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 64.70% | 64.70% | 64.70% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 67.90% | 55.76% | 80.04% | 24.28% | 17.17% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 47.73% | 47.73% | 47.73% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 67.11% | 60.15% | 74.08% | 13.93% | 9.85% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 50.53% | 50.53% | 50.53% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 53.61% | 53.61% | 53.61% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 59.55% | 59.55% | 59.55% | 0.00% | 0.00% | 1 |

### sub-2 (Cross-Model Swing: 21.02%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 50.27% | 49.91% | 50.63% | 0.72% | 0.51% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 51.33% | 47.79% | 54.87% | 7.07% | 5.00% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 49.94% | 49.94% | 49.94% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 68.08% | 68.08% | 68.08% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 56.27% | 56.27% | 56.27% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 57.09% | 53.25% | 62.58% | 9.34% | 4.88% | 3 |
| SVM | C=0.1, gamma=auto, kernel=poly | 50.86% | 50.28% | 51.44% | 1.16% | 0.82% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 52.55% | 50.95% | 54.14% | 3.19% | 2.26% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 47.06% | 47.06% | 47.06% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 57.05% | 51.14% | 63.86% | 12.72% | 5.59% | 4 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 47.43% | 47.43% | 47.43% | 0.00% | 0.00% | 1 |

### sub-20 (Cross-Model Swing: 19.22%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 56.45% | 53.60% | 59.29% | 5.69% | 4.02% | 2 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 50.34% | 50.34% | 50.34% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 49.86% | 48.80% | 51.68% | 2.88% | 1.58% | 3 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 57.71% | 54.69% | 59.36% | 4.67% | 2.62% | 3 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 61.17% | 55.80% | 68.02% | 12.21% | 6.24% | 3 |

### sub-21 (Cross-Model Swing: 14.67%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 51.70% | 51.70% | 51.70% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 54.13% | 50.64% | 57.61% | 6.97% | 4.93% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 60.68% | 60.68% | 60.68% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 57.68% | 52.19% | 63.18% | 10.99% | 7.77% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 49.68% | 49.68% | 49.68% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 58.56% | 52.78% | 64.35% | 11.56% | 8.18% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 51.35% | 51.35% | 51.35% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 52.60% | 51.92% | 53.29% | 1.37% | 0.97% | 2 |

### sub-22 (Cross-Model Swing: 14.11%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 58.43% | 53.69% | 63.18% | 9.49% | 6.71% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 49.07% | 49.07% | 49.07% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 58.53% | 58.53% | 58.53% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 53.08% | 53.08% | 53.08% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 56.81% | 56.81% | 56.81% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 54.55% | 54.55% | 54.55% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 56.12% | 56.12% | 56.12% | 0.00% | 0.00% | 1 |

### sub-23 (Cross-Model Swing: 27.08%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 60.71% | 58.09% | 63.34% | 5.25% | 3.71% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 74.36% | 74.36% | 74.36% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 47.77% | 47.77% | 47.77% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 47.28% | 47.28% | 47.28% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 68.35% | 68.35% | 68.35% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 48.41% | 48.41% | 48.41% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 60.25% | 60.25% | 60.25% | 0.00% | 0.00% | 1 |

### sub-24 (Cross-Model Swing: 12.41%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 53.28% | 53.07% | 53.49% | 0.42% | 0.30% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 51.10% | 51.10% | 51.10% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 49.09% | 46.34% | 51.85% | 5.51% | 3.90% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 58.74% | 58.74% | 58.74% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 49.10% | 49.10% | 49.10% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 49.22% | 49.22% | 49.22% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 51.61% | 51.61% | 51.61% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 51.12% | 49.49% | 52.76% | 3.26% | 2.31% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 46.64% | 46.64% | 46.64% | 0.00% | 0.00% | 1 |

### sub-25 (Cross-Model Swing: 18.97%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 50.11% | 49.91% | 50.32% | 0.41% | 0.29% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 54.38% | 54.38% | 54.38% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 55.01% | 55.01% | 55.01% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 45.38% | 42.90% | 47.85% | 4.94% | 3.50% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 43.25% | 41.12% | 45.38% | 4.26% | 3.01% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 56.91% | 56.91% | 56.91% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 42.12% | 37.94% | 46.29% | 8.35% | 5.91% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 53.19% | 53.19% | 53.19% | 0.00% | 0.00% | 1 |

### sub-26 (Cross-Model Swing: 24.69%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 59.22% | 53.49% | 65.86% | 12.38% | 5.10% | 4 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 66.89% | 66.89% | 66.89% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 57.53% | 51.85% | 63.21% | 11.36% | 8.03% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 48.80% | 48.80% | 48.80% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 49.10% | 49.10% | 49.10% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 46.76% | 45.94% | 47.58% | 1.65% | 1.16% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 54.69% | 54.69% | 54.69% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 55.60% | 46.69% | 70.63% | 23.94% | 13.09% | 3 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 59.68% | 59.68% | 59.68% | 0.00% | 0.00% | 1 |

### sub-27 (Cross-Model Swing: 29.18%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 60.19% | 57.20% | 63.34% | 6.14% | 3.07% | 3 |
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 57.06% | 57.06% | 57.06% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 66.82% | 59.28% | 74.36% | 15.08% | 10.67% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 61.95% | 57.18% | 66.72% | 9.55% | 6.75% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 49.55% | 45.18% | 53.91% | 8.72% | 6.17% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 51.28% | 51.28% | 51.28% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 68.35% | 68.35% | 68.35% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 58.83% | 54.35% | 63.31% | 8.95% | 4.48% | 3 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 60.25% | 60.25% | 60.25% | 0.00% | 0.00% | 1 |

## PCA_L_2_Random - Detailed Breakdown

### sub-1 (Cross-Model Swing: 19.85%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 58.39% | 58.39% | 58.39% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 59.13% | 59.13% | 59.13% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 43.66% | 41.18% | 46.14% | 4.95% | 3.50% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 44.23% | 44.23% | 44.23% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 41.18% | 41.18% | 41.18% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 61.03% | 61.03% | 61.03% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 43.44% | 43.44% | 43.44% | 0.00% | 0.00% | 1 |

### sub-11 (Cross-Model Swing: 13.98%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 55.40% | 54.56% | 56.24% | 1.68% | 1.19% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 54.25% | 54.25% | 54.25% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 43.97% | 43.97% | 43.97% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 46.77% | 42.26% | 51.27% | 9.01% | 6.37% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 47.09% | 43.44% | 50.74% | 7.31% | 5.17% | 2 |

### sub-13 (Cross-Model Swing: 5.47%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 55.13% | 55.13% | 55.13% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 49.66% | 49.66% | 49.66% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 49.66% | 49.66% | 49.66% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 49.66% | 49.66% | 49.66% | 0.00% | 0.00% | 1 |

### sub-14 (Cross-Model Swing: 12.51%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 48.87% | 48.27% | 49.47% | 1.20% | 0.85% | 2 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 58.89% | 58.89% | 58.89% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 50.21% | 47.81% | 51.44% | 3.63% | 2.08% | 3 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 55.44% | 54.70% | 56.17% | 1.47% | 1.04% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 54.42% | 54.42% | 54.42% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 56.52% | 52.73% | 60.32% | 7.59% | 5.37% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 59.40% | 59.40% | 59.40% | 0.00% | 0.00% | 1 |

### sub-15 (Cross-Model Swing: 40.17%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 49.42% | 46.64% | 52.19% | 5.55% | 3.92% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 53.08% | 53.08% | 53.08% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 43.86% | 43.86% | 43.86% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 60.24% | 48.82% | 71.67% | 22.85% | 16.15% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 51.46% | 51.46% | 51.46% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 55.84% | 55.84% | 55.84% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 68.38% | 52.72% | 84.04% | 31.31% | 22.14% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 58.85% | 58.85% | 58.85% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 50.68% | 50.68% | 50.68% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 57.11% | 57.11% | 57.11% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 52.68% | 47.52% | 57.85% | 10.33% | 7.30% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 48.55% | 48.55% | 48.55% | 0.00% | 0.00% | 1 |

### sub-16 (Cross-Model Swing: 11.76%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 48.61% | 48.61% | 48.61% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 52.35% | 52.35% | 52.35% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 60.37% | 60.37% | 60.37% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 55.14% | 55.14% | 55.14% | 0.00% | 0.00% | 1 |

### sub-17 (Cross-Model Swing: 29.20%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 51.98% | 51.98% | 51.98% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 49.52% | 49.52% | 49.52% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 78.72% | 78.72% | 78.72% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 51.36% | 51.36% | 51.36% | 0.00% | 0.00% | 1 |

### sub-18 (Cross-Model Swing: 49.60%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 42.47% | 37.43% | 47.50% | 10.07% | 7.12% | 2 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 53.83% | 52.31% | 55.34% | 3.03% | 2.14% | 2 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 69.26% | 61.70% | 76.83% | 15.13% | 10.70% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 63.41% | 51.28% | 87.04% | 35.76% | 16.04% | 4 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 49.04% | 49.04% | 49.04% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 51.48% | 51.48% | 51.48% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 59.79% | 59.63% | 59.96% | 0.33% | 0.23% | 2 |
| SVM | C=0.1, gamma=auto, kernel=linear | 50.98% | 50.49% | 51.48% | 0.99% | 0.70% | 2 |
| SVM | C=0.1, gamma=auto, kernel=poly | 48.67% | 48.52% | 48.82% | 0.30% | 0.21% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 54.46% | 50.84% | 58.08% | 7.24% | 5.12% | 2 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 50.96% | 50.44% | 51.48% | 1.04% | 0.74% | 2 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 58.62% | 55.19% | 62.05% | 6.87% | 4.85% | 2 |

### sub-19 (Cross-Model Swing: 33.83%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 52.21% | 49.03% | 55.38% | 6.35% | 4.49% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 55.52% | 52.72% | 58.31% | 5.59% | 3.95% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 68.76% | 54.66% | 82.86% | 28.20% | 19.94% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 55.47% | 55.47% | 55.47% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 57.03% | 57.03% | 57.03% | 0.00% | 0.00% | 1 |

### sub-2 (Cross-Model Swing: 12.27%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 50.43% | 50.43% | 50.43% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 51.29% | 51.29% | 51.29% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 60.52% | 60.52% | 60.52% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 57.17% | 57.17% | 57.17% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 53.85% | 53.85% | 53.85% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 48.25% | 48.25% | 48.25% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 59.41% | 59.41% | 59.41% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 49.00% | 49.00% | 49.00% | 0.00% | 0.00% | 1 |

### sub-21 (Cross-Model Swing: 5.67%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 54.19% | 54.19% | 54.19% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 53.05% | 53.05% | 53.05% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 53.05% | 53.05% | 53.05% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 58.73% | 58.73% | 58.73% | 0.00% | 0.00% | 1 |

### sub-22 (Cross-Model Swing: 15.58%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 51.36% | 51.36% | 51.36% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 60.60% | 60.60% | 60.60% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 66.93% | 66.93% | 66.93% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 52.46% | 52.46% | 52.46% | 0.00% | 0.00% | 1 |

### sub-23 (Cross-Model Swing: 36.35%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 40.24% | 40.24% | 40.24% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 61.41% | 61.41% | 61.41% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 76.59% | 76.59% | 76.59% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 72.59% | 72.59% | 72.59% | 0.00% | 0.00% | 1 |

### sub-24 (Cross-Model Swing: 24.09%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 50.10% | 50.10% | 50.10% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 71.79% | 71.79% | 71.79% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 54.35% | 54.35% | 54.35% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 58.49% | 49.23% | 67.76% | 18.53% | 13.11% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 51.07% | 51.07% | 51.07% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 62.21% | 62.21% | 62.21% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 47.70% | 47.70% | 47.70% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 48.84% | 48.84% | 48.84% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 71.66% | 71.66% | 71.66% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 69.57% | 69.57% | 69.57% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 65.60% | 65.60% | 65.60% | 0.00% | 0.00% | 1 |

### sub-28 (Cross-Model Swing: 9.01%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 52.45% | 52.45% | 52.45% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 52.66% | 52.66% | 52.66% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 50.63% | 50.63% | 50.63% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 51.06% | 51.06% | 51.06% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 50.14% | 50.14% | 50.14% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 50.73% | 50.73% | 50.73% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 50.32% | 50.32% | 50.32% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 59.15% | 59.15% | 59.15% | 0.00% | 0.00% | 1 |

### sub-3 (Cross-Model Swing: 47.94%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 76.20% | 76.20% | 76.20% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 28.25% | 28.25% | 28.25% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 65.62% | 65.62% | 65.62% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 30.03% | 30.03% | 30.03% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 64.48% | 64.48% | 64.48% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 30.03% | 30.03% | 30.03% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 31.07% | 31.07% | 31.07% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 69.27% | 69.27% | 69.27% | 0.00% | 0.00% | 1 |

### sub-30 (Cross-Model Swing: 52.09%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 60.21% | 60.21% | 60.21% | 0.00% | 0.00% | 1 |
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 67.60% | 67.60% | 67.60% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 38.46% | 38.46% | 38.46% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[150, 50] | 90.44% | 90.44% | 90.44% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 62.10% | 62.10% | 62.10% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 38.34% | 38.34% | 38.34% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 47.46% | 47.46% | 47.46% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 49.88% | 49.88% | 49.88% | 0.00% | 0.00% | 1 |

### sub-33 (Cross-Model Swing: 8.90%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=7, weights=uniform | 55.62% | 55.62% | 55.62% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 64.52% | 64.52% | 64.52% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=poly | 58.10% | 58.10% | 58.10% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 62.55% | 62.55% | 62.55% | 0.00% | 0.00% | 1 |

### sub-35 (Cross-Model Swing: 34.78%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=1, weights=uniform | 50.61% | 48.67% | 52.55% | 3.88% | 2.75% | 2 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[200, 100, 50] | 49.41% | 46.98% | 51.84% | 4.87% | 3.44% | 2 |
| SVM | C=0.1, gamma=auto, kernel=rbf | 66.55% | 51.33% | 81.76% | 30.43% | 21.51% | 2 |
| XGBoost | learning, rate=0.2, max, depth=3, n, estimators=100, subsample=0.7 | 51.13% | 51.13% | 51.13% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=9, n, estimators=100, subsample=0.7 | 49.05% | 49.05% | 49.05% | 0.00% | 0.00% | 1 |

### sub-36 (Cross-Model Swing: 3.86%)

| Model | Hyperparameters | Mean | Min | Max | Swing | Std Dev | N Folds |
|-------|----------------|------|-----|-----|-------|---------|----------|
| KNN | metric=euclidean, n, neighbors=15, weights=uniform | 55.22% | 55.22% | 55.22% | 0.00% | 0.00% | 1 |
| MLP_(Neural_Network) | activation=tanh, alpha=0.1, hidden, layer, sizes=[100] | 59.09% | 59.09% | 59.09% | 0.00% | 0.00% | 1 |
| SVM | C=0.1, gamma=auto, kernel=linear | 55.66% | 55.66% | 55.66% | 0.00% | 0.00% | 1 |
| XGBoost | learning, rate=0.2, max, depth=6, n, estimators=100, subsample=0.7 | 55.66% | 55.66% | 55.66% | 0.00% | 0.00% | 1 |

