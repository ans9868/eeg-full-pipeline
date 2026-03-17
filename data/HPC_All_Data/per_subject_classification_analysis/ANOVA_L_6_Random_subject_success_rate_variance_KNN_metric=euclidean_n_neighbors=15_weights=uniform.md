# Per-Subject Success Rate Variance Analysis

## Experiment: ANOVA_L_6_Random

## Model×Hyperparameters: KNN (metric=euclidean, n_neighbors=15, weights=uniform)


## Methods

This analysis examines how the variance of per-subject success rates (>50% accuracy) 
changes as we include more folds in the analysis.


**Methodology:**

1. For each subject, calculate the percentage of folds where that subject's accuracy > 50%

2. Calculate the variance of these percentages across all subjects

3. Repeat for different numbers of folds (1 to N folds)

4. For each number of folds, sample 30 random combinations to estimate variance


**Key Metrics:**

- **Variance**: How much subjects differ in their success rates

- **Mean Success Rate**: Average percentage of folds where subjects exceed 50% accuracy


## Results


| Number of Folds | Mean Variance | Std Dev of Variance | Mean Success Rate |

|----------------|---------------|---------------------|-------------------|

| 1 | 0.1300 | 0.1088 | 85.00% |

| 2 | 0.1358 | 0.0683 | 84.11% |

| 3 | 0.1380 | 0.0567 | 83.16% |

| 4 | 0.1421 | 0.0444 | 83.12% |

| 5 | 0.1447 | 0.0412 | 82.34% |

| 6 | 0.1425 | 0.0375 | 82.48% |

| 7 | 0.1330 | 0.0336 | 83.91% |

| 8 | 0.1270 | 0.0325 | 84.67% |

| 9 | 0.1310 | 0.0300 | 84.13% |

| 10 | 0.1311 | 0.0244 | 84.18% |

| 11 | 0.1319 | 0.0234 | 83.93% |

| 12 | 0.1294 | 0.0201 | 84.36% |

| 13 | 0.1357 | 0.0190 | 83.17% |

| 14 | 0.1328 | 0.0175 | 83.57% |

| 15 | 0.1305 | 0.0193 | 84.02% |

| 16 | 0.1274 | 0.0213 | 84.18% |

| 17 | 0.1316 | 0.0171 | 83.68% |

| 18 | 0.1305 | 0.0151 | 84.01% |

| 19 | 0.1292 | 0.0182 | 83.96% |

| 20 | 0.1295 | 0.0146 | 83.99% |

| 21 | 0.1311 | 0.0125 | 83.67% |

| 22 | 0.1272 | 0.0130 | 84.10% |

| 23 | 0.1274 | 0.0112 | 84.08% |

| 24 | 0.1256 | 0.0094 | 84.39% |

| 25 | 0.1289 | 0.0094 | 83.95% |

| 26 | 0.1305 | 0.0084 | 83.71% |

| 27 | 0.1261 | 0.0104 | 84.31% |

| 28 | 0.1294 | 0.0084 | 83.88% |

| 29 | 0.1272 | 0.0096 | 83.99% |

| 30 | 0.1282 | 0.0071 | 83.94% |

| 31 | 0.1278 | 0.0077 | 83.93% |

| 32 | 0.1280 | 0.0077 | 83.99% |

| 33 | 0.1287 | 0.0061 | 83.74% |

| 34 | 0.1281 | 0.0070 | 83.89% |

| 35 | 0.1293 | 0.0069 | 83.73% |

| 36 | 0.1305 | 0.0054 | 83.60% |

| 37 | 0.1303 | 0.0058 | 83.61% |

| 38 | 0.1283 | 0.0046 | 83.80% |

| 39 | 0.1283 | 0.0050 | 83.79% |

| 40 | 0.1287 | 0.0048 | 83.74% |

| 41 | 0.1295 | 0.0036 | 83.62% |

| 42 | 0.1297 | 0.0026 | 83.61% |

| 43 | 0.1294 | 0.0021 | 83.62% |

| 44 | 0.1297 | 0.0030 | 83.58% |

| 45 | 0.1296 | 0.0013 | 83.58% |

| 46 | 0.1291 | 0.0014 | 83.61% |

| 47 | 0.1289 | 0.0010 | 83.65% |

| 48 | 0.1292 | 0.0010 | 83.61% |

| 49 | 0.1293 | 0.0008 | 83.60% |

| 50 | 0.1292 | 0.0000 | 83.62% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1256 at 24 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1292

- Mean Success Rate: 83.62%
