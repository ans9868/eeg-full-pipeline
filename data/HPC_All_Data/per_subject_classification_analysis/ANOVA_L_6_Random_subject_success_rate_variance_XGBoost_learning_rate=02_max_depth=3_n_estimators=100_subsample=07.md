# Per-Subject Success Rate Variance Analysis

## Experiment: ANOVA_L_6_Random

## Model×Hyperparameters: XGBoost (learning_rate=0.2, max_depth=3, n_estimators=100, subsample=0.7)


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

| 1 | 0.1711 | 0.1078 | 78.89% |

| 2 | 0.1986 | 0.0506 | 74.40% |

| 3 | 0.1646 | 0.0602 | 78.50% |

| 4 | 0.1823 | 0.0365 | 75.73% |

| 5 | 0.1779 | 0.0394 | 75.77% |

| 6 | 0.1708 | 0.0374 | 77.12% |

| 7 | 0.1704 | 0.0255 | 76.91% |

| 8 | 0.1710 | 0.0260 | 76.08% |

| 9 | 0.1534 | 0.0296 | 78.69% |

| 10 | 0.1616 | 0.0287 | 77.65% |

| 11 | 0.1616 | 0.0202 | 76.84% |

| 12 | 0.1574 | 0.0277 | 77.77% |

| 13 | 0.1609 | 0.0199 | 77.22% |

| 14 | 0.1531 | 0.0195 | 78.07% |

| 15 | 0.1544 | 0.0181 | 77.55% |

| 16 | 0.1544 | 0.0173 | 77.63% |

| 17 | 0.1530 | 0.0126 | 77.67% |

| 18 | 0.1547 | 0.0185 | 77.35% |

| 19 | 0.1498 | 0.0167 | 78.13% |

| 20 | 0.1512 | 0.0130 | 77.25% |

| 21 | 0.1544 | 0.0098 | 76.97% |

| 22 | 0.1495 | 0.0153 | 77.76% |

| 23 | 0.1495 | 0.0111 | 77.42% |

| 24 | 0.1501 | 0.0117 | 77.23% |

| 25 | 0.1501 | 0.0118 | 77.09% |

| 26 | 0.1494 | 0.0116 | 77.37% |

| 27 | 0.1470 | 0.0105 | 77.50% |

| 28 | 0.1464 | 0.0118 | 77.74% |

| 29 | 0.1485 | 0.0096 | 77.42% |

| 30 | 0.1482 | 0.0085 | 77.24% |

| 31 | 0.1453 | 0.0067 | 77.41% |

| 32 | 0.1466 | 0.0086 | 77.47% |

| 33 | 0.1478 | 0.0070 | 77.05% |

| 34 | 0.1456 | 0.0076 | 77.35% |

| 35 | 0.1465 | 0.0069 | 77.00% |

| 36 | 0.1460 | 0.0062 | 77.19% |

| 37 | 0.1454 | 0.0075 | 77.19% |

| 38 | 0.1441 | 0.0059 | 77.26% |

| 39 | 0.1438 | 0.0050 | 77.26% |

| 40 | 0.1445 | 0.0046 | 77.08% |

| 41 | 0.1438 | 0.0042 | 77.32% |

| 42 | 0.1433 | 0.0039 | 77.20% |

| 43 | 0.1433 | 0.0030 | 77.28% |

| 44 | 0.1433 | 0.0022 | 77.20% |

| 45 | 0.1435 | 0.0028 | 77.12% |

| 46 | 0.1439 | 0.0033 | 76.99% |

| 47 | 0.1438 | 0.0018 | 77.06% |

| 48 | 0.1433 | 0.0012 | 77.02% |

| 49 | 0.1434 | 0.0013 | 76.98% |

| 50 | 0.1430 | 0.0000 | 77.03% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1430 at 50 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1430

- Mean Success Rate: 77.03%
