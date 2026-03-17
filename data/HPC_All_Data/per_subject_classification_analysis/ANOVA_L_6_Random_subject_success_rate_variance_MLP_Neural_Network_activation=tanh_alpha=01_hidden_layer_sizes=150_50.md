# Per-Subject Success Rate Variance Analysis

## Experiment: ANOVA_L_6_Random

## Model×Hyperparameters: MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_layer_sizes=[150, 50])


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

| 1 | 0.1689 | 0.1075 | 78.89% |

| 2 | 0.1635 | 0.0513 | 80.45% |

| 3 | 0.1414 | 0.0620 | 82.48% |

| 4 | 0.1602 | 0.0537 | 79.34% |

| 5 | 0.1325 | 0.0483 | 83.24% |

| 6 | 0.1558 | 0.0391 | 79.78% |

| 7 | 0.1460 | 0.0386 | 81.16% |

| 8 | 0.1382 | 0.0352 | 81.60% |

| 9 | 0.1358 | 0.0373 | 81.40% |

| 10 | 0.1378 | 0.0278 | 81.78% |

| 11 | 0.1382 | 0.0289 | 81.46% |

| 12 | 0.1462 | 0.0186 | 80.24% |

| 13 | 0.1422 | 0.0212 | 80.51% |

| 14 | 0.1387 | 0.0193 | 80.96% |

| 15 | 0.1353 | 0.0147 | 81.03% |

| 16 | 0.1336 | 0.0177 | 81.04% |

| 17 | 0.1311 | 0.0179 | 81.41% |

| 18 | 0.1373 | 0.0158 | 80.39% |

| 19 | 0.1380 | 0.0146 | 80.59% |

| 20 | 0.1302 | 0.0195 | 81.04% |

| 21 | 0.1280 | 0.0171 | 81.24% |

| 22 | 0.1303 | 0.0119 | 80.98% |

| 23 | 0.1331 | 0.0100 | 80.22% |

| 24 | 0.1305 | 0.0150 | 80.61% |

| 25 | 0.1321 | 0.0111 | 80.38% |

| 26 | 0.1322 | 0.0109 | 80.19% |

| 27 | 0.1266 | 0.0127 | 80.65% |

| 28 | 0.1256 | 0.0124 | 80.85% |

| 29 | 0.1262 | 0.0089 | 80.99% |

| 30 | 0.1268 | 0.0109 | 80.42% |

| 31 | 0.1261 | 0.0101 | 80.64% |

| 32 | 0.1252 | 0.0083 | 80.57% |

| 33 | 0.1259 | 0.0098 | 80.50% |

| 34 | 0.1247 | 0.0090 | 80.64% |

| 35 | 0.1218 | 0.0078 | 80.53% |

| 36 | 0.1215 | 0.0070 | 80.60% |

| 37 | 0.1204 | 0.0063 | 80.63% |

| 38 | 0.1211 | 0.0077 | 80.68% |

| 39 | 0.1198 | 0.0069 | 80.63% |

| 40 | 0.1194 | 0.0090 | 80.80% |

| 41 | 0.1209 | 0.0077 | 80.30% |

| 42 | 0.1198 | 0.0072 | 80.41% |

| 43 | 0.1193 | 0.0062 | 80.40% |

| 44 | 0.1203 | 0.0077 | 79.94% |

| 45 | 0.1166 | 0.0035 | 80.38% |

| 46 | 0.1163 | 0.0040 | 80.33% |

| 47 | 0.1159 | 0.0034 | 80.38% |

| 48 | 0.1152 | 0.0028 | 80.38% |

| 49 | 0.1148 | 0.0020 | 80.39% |

| 50 | 0.1142 | 0.0000 | 80.35% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1142 at 50 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1142

- Mean Success Rate: 80.35%
