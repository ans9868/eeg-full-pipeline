# Per-Subject Success Rate Variance Analysis

## Experiment: ANOVA_L_2_Random

## Model×Hyperparameters: XGBoost (learning_rate=0.2, max_depth=6, n_estimators=100, subsample=0.7)


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

| 1 | 0.1500 | 0.2330 | 85.00% |

| 2 | 0.1444 | 0.1400 | 83.33% |

| 3 | 0.1667 | 0.0935 | 81.56% |

| 4 | 0.1478 | 0.0895 | 82.68% |

| 5 | 0.1733 | 0.0749 | 78.49% |

| 6 | 0.1609 | 0.0602 | 80.88% |

| 7 | 0.1457 | 0.0552 | 82.55% |

| 8 | 0.1328 | 0.0565 | 83.74% |

| 9 | 0.1446 | 0.0556 | 82.27% |

| 10 | 0.1300 | 0.0417 | 84.95% |

| 11 | 0.1329 | 0.0550 | 84.12% |

| 12 | 0.1558 | 0.0370 | 80.83% |

| 13 | 0.1487 | 0.0418 | 81.63% |

| 14 | 0.1557 | 0.0356 | 80.78% |

| 15 | 0.1483 | 0.0347 | 81.54% |

| 16 | 0.1531 | 0.0417 | 80.67% |

| 17 | 0.1459 | 0.0357 | 81.60% |

| 18 | 0.1435 | 0.0326 | 82.39% |

| 19 | 0.1416 | 0.0305 | 82.58% |

| 20 | 0.1443 | 0.0260 | 82.43% |

| 21 | 0.1422 | 0.0274 | 82.29% |

| 22 | 0.1465 | 0.0246 | 81.68% |

| 23 | 0.1456 | 0.0243 | 81.29% |

| 24 | 0.1433 | 0.0272 | 81.82% |

| 25 | 0.1413 | 0.0219 | 82.10% |

| 26 | 0.1459 | 0.0218 | 81.53% |

| 27 | 0.1404 | 0.0243 | 82.12% |

| 28 | 0.1526 | 0.0168 | 80.31% |

| 29 | 0.1374 | 0.0212 | 82.68% |

| 30 | 0.1393 | 0.0195 | 82.34% |

| 31 | 0.1347 | 0.0199 | 82.68% |

| 32 | 0.1337 | 0.0229 | 82.78% |

| 33 | 0.1331 | 0.0187 | 82.86% |

| 34 | 0.1334 | 0.0175 | 82.80% |

| 35 | 0.1374 | 0.0164 | 82.29% |

| 36 | 0.1324 | 0.0183 | 82.93% |

| 37 | 0.1317 | 0.0158 | 83.07% |

| 38 | 0.1267 | 0.0173 | 83.38% |

| 39 | 0.1294 | 0.0132 | 83.06% |

| 40 | 0.1326 | 0.0124 | 82.62% |

| 41 | 0.1299 | 0.0114 | 82.91% |

| 42 | 0.1273 | 0.0173 | 83.10% |

| 43 | 0.1279 | 0.0122 | 82.86% |

| 44 | 0.1268 | 0.0118 | 83.06% |

| 45 | 0.1252 | 0.0099 | 83.32% |

| 46 | 0.1260 | 0.0080 | 83.22% |

| 47 | 0.1278 | 0.0063 | 82.82% |

| 48 | 0.1244 | 0.0016 | 83.06% |

| 49 | 0.1232 | 0.0026 | 83.27% |

| 50 | 0.1234 | 0.0000 | 83.16% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1232 at 49 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1234

- Mean Success Rate: 83.16%
