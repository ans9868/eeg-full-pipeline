# Per-Subject Success Rate Variance Analysis

## Experiment: PCA_L_2_Random

## Model×Hyperparameters: KNN (metric=euclidean, n_neighbors=1, weights=uniform)


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

| 1 | 0.5000 | 0.0000 | 50.00% |

| 2 | 0.3333 | 0.0000 | 49.44% |

| 3 | 0.3000 | 0.0000 | 49.67% |

| 4 | 0.2857 | 0.0000 | 50.71% |

| 5 | 0.2796 | 0.0047 | 50.56% |

| 6 | 0.2724 | 0.0028 | 49.22% |

| 7 | 0.2700 | 0.0026 | 50.34% |

| 8 | 0.2659 | 0.0053 | 51.14% |

| 9 | 0.2651 | 0.0030 | 50.11% |

| 10 | 0.2633 | 0.0020 | 49.45% |

| 11 | 0.2617 | 0.0038 | 49.89% |

| 12 | 0.2606 | 0.0030 | 50.23% |

| 13 | 0.2606 | 0.0026 | 49.53% |

| 14 | 0.2592 | 0.0048 | 49.05% |

| 15 | 0.2592 | 0.0028 | 48.94% |

| 16 | 0.2587 | 0.0019 | 49.27% |

| 17 | 0.2582 | 0.0028 | 50.12% |

| 18 | 0.2583 | 0.0019 | 49.96% |

| 19 | 0.2582 | 0.0010 | 50.60% |

| 20 | 0.2580 | 0.0013 | 50.98% |

| 21 | 0.2579 | 0.0010 | 49.35% |

| 22 | 0.2570 | 0.0013 | 50.49% |

| 23 | 0.2570 | 0.0018 | 49.05% |

| 24 | 0.2568 | 0.0013 | 50.07% |

| 25 | 0.2568 | 0.0013 | 50.00% |

| 26 | 0.2563 | 0.0016 | 50.67% |

| 27 | 0.2560 | 0.0022 | 48.59% |

| 28 | 0.2562 | 0.0010 | 50.08% |

| 29 | 0.2557 | 0.0023 | 48.33% |

| 30 | 0.2559 | 0.0011 | 49.63% |

| 31 | 0.2554 | 0.0017 | 49.08% |

| 32 | 0.2558 | 0.0007 | 49.31% |

| 33 | 0.2555 | 0.0011 | 48.73% |

| 34 | 0.2557 | 0.0006 | 49.07% |

| 35 | 0.2556 | 0.0007 | 48.65% |

| 36 | 0.2554 | 0.0010 | 48.96% |

| 37 | 0.2552 | 0.0007 | 49.21% |

| 38 | 0.2554 | 0.0005 | 49.48% |

| 39 | 0.2554 | 0.0005 | 48.97% |

| 40 | 0.2552 | 0.0007 | 50.02% |

| 41 | 0.2552 | 0.0006 | 48.44% |

| 42 | 0.2553 | 0.0005 | 49.34% |

| 43 | 0.2553 | 0.0004 | 49.23% |

| 44 | 0.2552 | 0.0004 | 48.99% |

| 45 | 0.2552 | 0.0002 | 49.19% |

| 46 | 0.2551 | 0.0004 | 48.77% |

| 47 | 0.2551 | 0.0002 | 48.75% |

| 48 | 0.2551 | 0.0002 | 49.03% |

| 49 | 0.2551 | 0.0001 | 48.94% |

| 50 | 0.2551 | 0.0000 | 48.98% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.2551 at 46 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.2551

- Mean Success Rate: 48.98%
