# Per-Subject Success Rate Variance Analysis

## Experiment: PCA_L_2_Random

## Model×Hyperparameters: SVM (C=0.1, gamma=auto, kernel=rbf)


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

| 4 | 0.2857 | 0.0000 | 48.81% |

| 5 | 0.2783 | 0.0020 | 49.44% |

| 6 | 0.2723 | 0.0054 | 49.37% |

| 7 | 0.2693 | 0.0035 | 50.31% |

| 8 | 0.2669 | 0.0018 | 51.19% |

| 9 | 0.2658 | 0.0020 | 49.33% |

| 10 | 0.2639 | 0.0020 | 49.35% |

| 11 | 0.2625 | 0.0019 | 49.97% |

| 12 | 0.2613 | 0.0020 | 49.95% |

| 13 | 0.2609 | 0.0018 | 50.16% |

| 14 | 0.2603 | 0.0012 | 50.20% |

| 15 | 0.2593 | 0.0018 | 50.58% |

| 16 | 0.2589 | 0.0029 | 50.46% |

| 17 | 0.2578 | 0.0025 | 51.57% |

| 18 | 0.2586 | 0.0011 | 50.53% |

| 19 | 0.2576 | 0.0017 | 50.39% |

| 20 | 0.2574 | 0.0023 | 50.90% |

| 21 | 0.2575 | 0.0015 | 50.03% |

| 22 | 0.2567 | 0.0024 | 50.09% |

| 23 | 0.2566 | 0.0018 | 51.09% |

| 24 | 0.2565 | 0.0016 | 50.68% |

| 25 | 0.2566 | 0.0016 | 50.53% |

| 26 | 0.2563 | 0.0019 | 49.97% |

| 27 | 0.2564 | 0.0015 | 50.76% |

| 28 | 0.2560 | 0.0012 | 50.83% |

| 29 | 0.2556 | 0.0014 | 51.09% |

| 30 | 0.2558 | 0.0010 | 51.39% |

| 31 | 0.2561 | 0.0008 | 50.36% |

| 32 | 0.2559 | 0.0009 | 51.39% |

| 33 | 0.2555 | 0.0012 | 51.56% |

| 34 | 0.2555 | 0.0009 | 50.98% |

| 35 | 0.2558 | 0.0005 | 50.36% |

| 36 | 0.2553 | 0.0014 | 51.32% |

| 37 | 0.2555 | 0.0006 | 50.88% |

| 38 | 0.2554 | 0.0006 | 51.17% |

| 39 | 0.2553 | 0.0005 | 50.94% |

| 40 | 0.2552 | 0.0008 | 50.27% |

| 41 | 0.2552 | 0.0007 | 51.21% |

| 42 | 0.2553 | 0.0004 | 50.59% |

| 43 | 0.2553 | 0.0003 | 50.46% |

| 44 | 0.2553 | 0.0003 | 50.79% |

| 45 | 0.2552 | 0.0003 | 50.88% |

| 46 | 0.2551 | 0.0004 | 51.13% |

| 47 | 0.2551 | 0.0002 | 51.04% |

| 48 | 0.2552 | 0.0002 | 50.82% |

| 49 | 0.2551 | 0.0001 | 50.92% |

| 50 | 0.2551 | 0.0000 | 51.02% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.2551 at 50 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.2551

- Mean Success Rate: 51.02%
