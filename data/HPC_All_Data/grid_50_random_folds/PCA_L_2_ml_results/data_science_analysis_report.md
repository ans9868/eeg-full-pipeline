# Data Science Analysis Report

## Executive Summary

This report provides comprehensive statistical analysis distinguishing between:
- **AVERAGE Performance**: Performance across ALL hyperparameter configurations
- **BEST MODEL Performance**: Performance of the BEST hyperparameter configuration

## 1. AVERAGE Performance (All Hyperparameters)

### Summary Statistics

| Model | Mean Accuracy | Std Dev | Median | Min | Max | Folds | Hyperparam Configs |
|-------|---------------|---------|--------|-----|-----|-------|-------------------|
| KNN | 0.5488 | 0.0894 | 0.5422 | 0.2604 | 0.7851 | 50 | 3 |
| MLP (Neural Network) | 0.5451 | 0.1061 | 0.5241 | 0.2557 | 0.9044 | 50 | 3 |
| SVM | 0.5317 | 0.1041 | 0.5140 | 0.2557 | 0.8404 | 50 | 3 |
| XGBoost | 0.5476 | 0.0872 | 0.5320 | 0.2707 | 0.8783 | 50 | 3 |

## 2. BEST MODEL Performance (Best Hyperparameters)

### Summary Statistics

| Model | Mean Accuracy | Std Dev | Median | Min | Max | Folds | Best Hyperparams |
|-------|---------------|---------|--------|-----|-----|-------|------------------|
| KNN | 0.5726 | 0.0985 | 0.5608 | 0.2604 | 0.7851 | 50 | {'metric': 'euclidean', 'n_neighbors': 15, 'weight... |
| MLP (Neural Network) | 0.5542 | 0.1272 | 0.5241 | 0.2557 | 0.9044 | 50 | {'activation': 'tanh', 'alpha': '0.1', 'hidden_lay... |
| SVM | 0.6045 | 0.1229 | 0.5968 | 0.2885 | 0.8404 | 50 | {'C': '0.1', 'gamma': 'auto', 'kernel': 'rbf'} |
| XGBoost | 0.5500 | 0.0832 | 0.5355 | 0.3107 | 0.7677 | 50 | {'learning_rate': '0.2', 'max_depth': '6', 'n_esti... |

## 3. Statistical Tests

### BEST MODEL Pairwise Comparisons (t-tests)

| Comparison | Mean 1 | Mean 2 | t-statistic | p-value | Significant? |
|------------|--------|--------|-------------|---------|--------------|
| KNN vs MLP (Neural Network) | 0.5726 | 0.5542 | 0.8094 | 0.4202 | No |
| KNN vs SVM | 0.5726 | 0.6045 | -1.4300 | 0.1559 | No |
| KNN vs XGBoost | 0.5726 | 0.5500 | 1.2433 | 0.2167 | No |
| MLP (Neural Network) vs SVM | 0.5542 | 0.6045 | -2.0096 | 0.0472 | Yes (p<0.05) |
| MLP (Neural Network) vs XGBoost | 0.5542 | 0.5500 | 0.1981 | 0.8434 | No |
| SVM vs XGBoost | 0.6045 | 0.5500 | 2.5975 | 0.0108 | Yes (p<0.05) |

### AVERAGE MODEL Pairwise Comparisons (t-tests)

| Comparison | Mean 1 | Mean 2 | t-statistic | p-value | Significant? |
|------------|--------|--------|-------------|---------|--------------|
| KNN vs MLP (Neural Network) | 0.5488 | 0.5451 | 0.3184 | 0.7504 | No |
| KNN vs SVM | 0.5488 | 0.5317 | 1.5208 | 0.1294 | No |
| KNN vs XGBoost | 0.5488 | 0.5476 | 0.1139 | 0.9094 | No |
| MLP (Neural Network) vs SVM | 0.5451 | 0.5317 | 1.1066 | 0.2694 | No |
| MLP (Neural Network) vs XGBoost | 0.5451 | 0.5476 | -0.2180 | 0.8276 | No |
| SVM vs XGBoost | 0.5317 | 0.5476 | -1.4315 | 0.1533 | No |

## 4. Key Insights

### Best AVERAGE Model: KNN
- Mean Accuracy: 0.5488 ± 0.0894
- This represents performance across ALL hyperparameter configurations

### Best MODEL Overall: SVM
- Mean Accuracy: 0.6045 ± 0.1229
- This represents performance of the BEST hyperparameter configuration
- Best Hyperparams: {'C': '0.1', 'gamma': 'auto', 'kernel': 'rbf'}

### Performance Gap: AVERAGE vs BEST
- Average Best Model: KNN (0.5488)
- Best Model Overall: SVM (0.6045)
- Gap: 0.0557 (10.16% improvement)

