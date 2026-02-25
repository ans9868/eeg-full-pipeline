# Performance Tables: Grid 12 Folds vs Grid 50 Random Folds

This document provides detailed performance tables clearly distinguishing between:
- **AVERAGE**: Performance across ALL hyperparameter configurations
- **BEST MODEL**: Performance of the BEST hyperparameter configuration

---

## Table of Contents
1. [Grid 12 Folds - AVERAGE Performance](#grid-12-folds---average-performance)
2. [Grid 12 Folds - BEST MODEL Performance](#grid-12-folds---best-model-performance)
3. [Grid 50 Random Folds - AVERAGE Performance](#grid-50-random-folds---average-performance)
4. [Grid 50 Random Folds - BEST MODEL Performance](#grid-50-random-folds---best-model-performance)
5. [Comparison Tables](#comparison-tables)

---

## Grid 12 Folds - AVERAGE Performance

### Overall Statistics (AVERAGE)
| Metric | Value |
|--------|-------|
| Total Results | 336 |
| Configurations | 6 |
| Models | 4 |
| Mean Accuracy | 0.6272 ± 0.1375 |
| Median Accuracy | 0.6127 |
| Min Accuracy | 0.0356 |
| Max Accuracy | 0.9817 |

### Per-Configuration Performance (AVERAGE)
*Average performance across all hyperparameter configurations for each config*

| Configuration | Mean Accuracy | Std Dev | Median | Min | Max | Total Results | Models | Folds |
|---------------|---------------|---------|--------|-----|-----|---------------|--------|-------|
| ANOVA_L_6_C_Resource_Boosted | **0.6701** | 0.0840 | 0.6756 | - | - | 144 | 4 | 12 |
| ANOVA_W_C | **0.8235** | 0.0810 | 0.8297 | - | - | 12 | 4 | 1 |
| ANOVA_W_F | **0.6578** | 0.3495 | 0.7173 | - | - | 12 | 4 | 1 |
| PCA_L_6_C-3 | **0.5360** | 0.0650 | 0.5342 | - | - | 144 | 4 | 12 |
| PCA_W_C-3 | **0.8038** | 0.1673 | 0.8974 | - | - | 12 | 4 | 1 |
| PCA_W_F-3 | **0.8041** | 0.1675 | 0.8995 | - | - | 12 | 4 | 1 |

### Per-Model Performance (AVERAGE)
*Average performance across all hyperparameter configurations and all configs*

| Model | Mean Accuracy | Std Dev | Median | Total Results | Configurations |
|-------|---------------|---------|--------|---------------|----------------|
| KNN | **0.6140** | 0.0940 | 0.6194 | 84 | 6 |
| MLP (Neural Network) | **0.6510** | 0.1520 | 0.6520 | 84 | 6 |
| SVM | **0.5965** | 0.1447 | 0.5693 | 84 | 6 |
| XGBoost | **0.6474** | 0.1459 | 0.6212 | 84 | 6 |

---

## Grid 12 Folds - BEST MODEL Performance

### Per-Configuration Best Models (BEST MODEL)
*Best hyperparameter configuration for each config*

| Configuration | Best Model | Mean Accuracy | Std Dev | Best Hyperparams | Folds |
|---------------|------------|---------------|---------|------------------|-------|
| ANOVA_L_6_C_Resource_Boosted | **SVM** | **0.7107** | 0.0903 | C=0.1, kernel=linear, gamma=auto | 12 |
| ANOVA_W_C | **XGBoost** | **0.9494** | 0.0000 | n_estimators=100, max_depth=9, learning_rate=0.2, subsample=0.7 | 1 |
| ANOVA_W_F | **XGBoost** | **0.9761** | 0.0000 | n_estimators=100, max_depth=3, learning_rate=0.2, subsample=0.7 | 1 |
| PCA_L_6_C-3 | **SVM** | **0.5826** | 0.0647 | C=0.1, kernel=rbf, gamma=auto | 12 |
| PCA_W_C-3 | **MLP** | **0.9817** | 0.0000 | hidden_layers=[200,100,50], activation=tanh, alpha=0.1 | 1 |
| PCA_W_F-3 | **MLP** | **0.9811** | 0.0000 | hidden_layers=[200,100,50], activation=tanh, alpha=0.1 | 1 |

---

## Grid 50 Random Folds - AVERAGE Performance

### Overall Statistics (AVERAGE)
| Metric | Value |
|--------|-------|
| Total Results | 2120 |
| Configurations | 4 |
| Models | 4 |
| Mean Accuracy | 0.6053 ± 0.1244 |
| Median Accuracy | 0.5947 |
| Min Accuracy | 0.1686 |
| Max Accuracy | 0.9834 |

### Per-Configuration Performance (AVERAGE)
*Average performance across all hyperparameter configurations for each config*

| Configuration | Mean Accuracy | Std Dev | Median | Total Results | Models | Folds |
|---------------|---------------|---------|--------|---------------|--------|-------|
| Anova_L_2_incomplete | **0.7022** | 0.1435 | 0.6921 | 464 | 4 | 50 |
| Anova_L_6_Incomplete | **0.6768** | 0.0851 | 0.6749 | 456 | 4 | 50 |
| PCA_L_2 | **0.5433** | 0.0971 | 0.5254 | 600 | 4 | 50 |
| PCA_L_6 | **0.5379** | 0.0657 | 0.5248 | 600 | 4 | 50 |

### Per-Model Performance (AVERAGE)
*Average performance across all hyperparameter configurations and all configs*

| Model | Mean Accuracy | Std Dev | Median | Total Results | Configurations |
|-------|---------------|---------|--------|---------------|----------------|
| KNN | **0.6132** | 0.1095 | 0.6178 | 559 | 4 |
| MLP (Neural Network) | **0.6079** | 0.1333 | 0.5992 | 482 | 4 |
| SVM | **0.5914** | 0.1276 | 0.5774 | 550 | 4 |
| XGBoost | **0.6089** | 0.1264 | 0.5925 | 529 | 4 |

---

## Grid 50 Random Folds - BEST MODEL Performance

### Per-Configuration Best Models (BEST MODEL)
*Best hyperparameter configuration for each config*

| Configuration | Best Model | Mean Accuracy | Std Dev | Best Hyperparams | Folds |
|---------------|------------|---------------|---------|------------------|-------|
| Anova_L_2_incomplete | **MLP** | **0.9834** | - | *Best hyperparams: See results.json* | 50 |
| Anova_L_6_Incomplete | **MLP** | **0.8974** | - | *Best hyperparams: See results.json* | 50 |
| PCA_L_2 | **SVM** | **0.6045** | 0.1229 | C=0.1, kernel=rbf, gamma=auto | 50 |
| PCA_L_6 | **SVM** | **0.5734** | 0.0775 | C=0.1, kernel=rbf, gamma=auto | 50 |

### Per-Model Best Performance (BEST MODEL)
*Best hyperparameter configuration across all configs for each model*

| Model | Best Config | Mean Accuracy | Std Dev | Best Hyperparams |
|-------|-------------|---------------|---------|------------------|
| KNN | Anova_L_2_incomplete | **0.9273** | - | *Best hyperparams: See results.json* |
| MLP (Neural Network) | Anova_L_2_incomplete | **0.9834** | - | *Best hyperparams: See results.json* |
| SVM | Anova_L_6_Incomplete | **0.8559** | - | *Best hyperparams: See results.json* |
| XGBoost | Anova_L_2_incomplete | **0.9681** | - | *Best hyperparams: See results.json* |

---

## Comparison Tables

### Overall Comparison: AVERAGE Performance
| Metric | Grid 12 Folds | Grid 50 Random Folds | Difference | % Change |
|--------|---------------|----------------------|------------|----------|
| Mean Accuracy | **0.6272** | **0.6053** | -0.0219 | -3.50% |
| Std Dev | 0.1375 | 0.1244 | -0.0131 | -9.53% |
| Median Accuracy | 0.6127 | 0.5947 | -0.0180 | -2.94% |
| Min Accuracy | 0.0356 | 0.1686 | +0.1330 | +373.60% |
| Max Accuracy | 0.9817 | 0.9834 | +0.0017 | +0.17% |
| Total Results | 336 | 2120 | +1784 | +531.0% |

### Per-Model Comparison: AVERAGE Performance
| Model | Grid 12 Folds | Grid 50 Random Folds | Difference | % Change |
|-------|---------------|----------------------|------------|----------|
| KNN | **0.6140** | **0.6132** | -0.0008 | -0.13% |
| MLP (Neural Network) | **0.6510** | **0.6079** | -0.0431 | -6.61% |
| SVM | **0.5965** | **0.5914** | -0.0051 | -0.86% |
| XGBoost | **0.6474** | **0.6089** | -0.0384 | -5.93% |

### Best Model Comparison: BEST MODEL Performance
*Best hyperparameter configuration in each group*

| Model | Grid 12 Folds Best | Grid 50 Random Folds Best | Difference | % Change |
|-------|-------------------|---------------------------|------------|----------|
| KNN | **0.6939** (ANOVA_L_6) | **0.9273** (Anova_L_2_incomplete) | +0.2334 | +33.64% |
| MLP (Neural Network) | **0.9817** (PCA_W_C-3) | **0.9834** (Anova_L_2_incomplete) | +0.0017 | +0.17% |
| SVM | **0.7107** (ANOVA_L_6) | **0.8559** (Anova_L_6_Incomplete) | +0.1452 | +20.43% |
| XGBoost | **0.9761** (ANOVA_W_F) | **0.9681** (Anova_L_2_incomplete) | -0.0080 | -0.82% |

*Note: Grid 12 Folds includes within-subject configs (W_C, W_F) which show very high performance due to different evaluation setup. Grid 50 Random Folds best models are from incomplete ANOVA configs which may have different characteristics.*

---

## Key Insights

### AVERAGE vs BEST MODEL

**Grid 12 Folds:**
- **AVERAGE Performance**: 0.6272 ± 0.1375
- **BEST MODEL Performance**: See individual config `model_comparison.csv` files
- *Note: Best model analysis requires loading per-config data*

**Grid 50 Random Folds:**
- **AVERAGE Performance**: 0.6053 ± 0.1244
- **BEST MODEL Performance**: 
  - Best overall: **MLP at 0.9834** (Anova_L_2_incomplete)
  - Best SVM: **0.8559** (Anova_L_6_Incomplete)
  - Best KNN: **0.9273** (Anova_L_2_incomplete)
  - Best XGBoost: **0.9681** (Anova_L_2_incomplete)

### Performance Gap Analysis: AVERAGE vs BEST MODEL

**Grid 12 Folds:**
- **AVERAGE vs BEST MODEL Gap**:
  - MLP: 0.6510 (AVERAGE) → 0.9817 (BEST) = **+50.8% improvement**
  - SVM: 0.5965 (AVERAGE) → 0.7107 (BEST) = **+19.1% improvement**
  - KNN: 0.6140 (AVERAGE) → 0.6939 (BEST) = **+13.0% improvement**
  - XGBoost: 0.6474 (AVERAGE) → 0.9761 (BEST) = **+50.7% improvement**

**Grid 50 Random Folds:**
- **AVERAGE vs BEST MODEL Gap**:
  - MLP: 0.6079 (AVERAGE) → 0.9834 (BEST) = **+61.8% improvement**
  - SVM: 0.5914 (AVERAGE) → 0.8559 (BEST) = **+44.7% improvement**
  - KNN: 0.6132 (AVERAGE) → 0.9273 (BEST) = **+51.2% improvement**
  - XGBoost: 0.6089 (AVERAGE) → 0.9681 (BEST) = **+59.0% improvement**

**Key Finding:** Hyperparameter tuning provides significant performance gains (13-62% improvement) across all models!

---

## Notes

- **AVERAGE** means performance averaged across ALL hyperparameter configurations tested
- **BEST MODEL** means performance of the SINGLE BEST hyperparameter configuration
- Performance gaps between AVERAGE and BEST show the value of hyperparameter tuning
- Grid 50 Random Folds has more comprehensive hyperparameter exploration (2120 results vs 336)
- Grid 12 Folds uses systematic fold generation (12 folds)
- Grid 50 Random Folds uses random fold generation (50 random folds)

---

*Generated by comprehensive_analysis.py*

