# Per-Subject Success Rate Variance Analysis

## Experiment: PCA_L_2_Random

## Model×Hyperparameters: MLP_(Neural_Network) (activation=tanh, alpha=0.1, hidden_layer_sizes=[200, 100, 50])


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

| 1 | 0.4833 | 0.0913 | 51.67% |

| 2 | 0.3333 | 0.0000 | 48.89% |

| 3 | 0.3000 | 0.0000 | 50.33% |

| 4 | 0.2850 | 0.0105 | 51.13% |

| 5 | 0.2785 | 0.0058 | 50.77% |

| 6 | 0.2735 | 0.0024 | 49.67% |

| 7 | 0.2691 | 0.0038 | 49.50% |

| 8 | 0.2655 | 0.0040 | 52.12% |

| 9 | 0.2644 | 0.0040 | 51.80% |

| 10 | 0.2626 | 0.0052 | 52.29% |

| 11 | 0.2624 | 0.0022 | 51.15% |

| 12 | 0.2613 | 0.0022 | 50.55% |

| 13 | 0.2604 | 0.0025 | 51.95% |

| 14 | 0.2602 | 0.0028 | 51.02% |

| 15 | 0.2588 | 0.0026 | 52.23% |

| 16 | 0.2587 | 0.0022 | 52.22% |

| 17 | 0.2583 | 0.0021 | 52.06% |

| 18 | 0.2577 | 0.0022 | 51.89% |

| 19 | 0.2566 | 0.0026 | 51.53% |

| 20 | 0.2571 | 0.0022 | 50.71% |

| 21 | 0.2567 | 0.0024 | 51.60% |

| 22 | 0.2567 | 0.0016 | 51.75% |

| 23 | 0.2566 | 0.0022 | 51.79% |

| 24 | 0.2560 | 0.0028 | 52.62% |

| 25 | 0.2562 | 0.0017 | 52.29% |

| 26 | 0.2558 | 0.0016 | 52.57% |

| 27 | 0.2555 | 0.0023 | 51.63% |

| 28 | 0.2555 | 0.0023 | 52.47% |

| 29 | 0.2556 | 0.0014 | 51.94% |

| 30 | 0.2554 | 0.0015 | 52.01% |

| 31 | 0.2559 | 0.0010 | 51.50% |

| 32 | 0.2552 | 0.0014 | 52.73% |

| 33 | 0.2551 | 0.0015 | 52.72% |

| 34 | 0.2547 | 0.0020 | 52.63% |

| 35 | 0.2549 | 0.0013 | 52.70% |

| 36 | 0.2553 | 0.0011 | 52.05% |

| 37 | 0.2548 | 0.0014 | 52.60% |

| 38 | 0.2546 | 0.0012 | 52.80% |

| 39 | 0.2547 | 0.0011 | 52.75% |

| 40 | 0.2547 | 0.0011 | 52.50% |

| 41 | 0.2546 | 0.0011 | 52.79% |

| 42 | 0.2544 | 0.0012 | 52.89% |

| 43 | 0.2542 | 0.0010 | 53.22% |

| 44 | 0.2547 | 0.0006 | 52.46% |

| 45 | 0.2543 | 0.0010 | 53.04% |

| 46 | 0.2542 | 0.0007 | 53.35% |

| 47 | 0.2543 | 0.0006 | 53.03% |

| 48 | 0.2544 | 0.0005 | 52.80% |

| 49 | 0.2542 | 0.0004 | 53.15% |

| 50 | 0.2543 | 0.0000 | 53.06% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.2542 at 46 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.2543

- Mean Success Rate: 53.06%
