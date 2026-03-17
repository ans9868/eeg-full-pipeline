# Per-Subject Success Rate Variance Analysis

## Experiment: PCA_L_6_Random

## Model×Hyperparameters: SVM (C=0.1, gamma=auto, kernel=poly)


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

| 1 | 0.3000 | 0.0000 | 50.00% |

| 2 | 0.2723 | 0.0044 | 50.40% |

| 3 | 0.2651 | 0.0012 | 50.91% |

| 4 | 0.2599 | 0.0039 | 51.89% |

| 5 | 0.2591 | 0.0024 | 52.06% |

| 6 | 0.2574 | 0.0025 | 51.70% |

| 7 | 0.2568 | 0.0014 | 52.79% |

| 8 | 0.2556 | 0.0022 | 52.77% |

| 9 | 0.2553 | 0.0020 | 51.21% |

| 10 | 0.2544 | 0.0025 | 53.23% |

| 11 | 0.2548 | 0.0013 | 52.52% |

| 12 | 0.2543 | 0.0018 | 52.95% |

| 13 | 0.2536 | 0.0020 | 53.00% |

| 14 | 0.2544 | 0.0010 | 51.85% |

| 15 | 0.2537 | 0.0013 | 52.76% |

| 16 | 0.2536 | 0.0014 | 53.02% |

| 17 | 0.2527 | 0.0025 | 53.74% |

| 18 | 0.2526 | 0.0020 | 53.91% |

| 19 | 0.2519 | 0.0021 | 54.63% |

| 20 | 0.2522 | 0.0024 | 54.14% |

| 21 | 0.2526 | 0.0018 | 53.59% |

| 22 | 0.2525 | 0.0016 | 53.95% |

| 23 | 0.2527 | 0.0013 | 53.51% |

| 24 | 0.2519 | 0.0018 | 54.58% |

| 25 | 0.2523 | 0.0015 | 54.04% |

| 26 | 0.2523 | 0.0013 | 53.99% |

| 27 | 0.2516 | 0.0015 | 54.83% |

| 28 | 0.2517 | 0.0012 | 54.65% |

| 29 | 0.2519 | 0.0012 | 54.46% |

| 30 | 0.2518 | 0.0011 | 54.65% |

| 31 | 0.2515 | 0.0011 | 54.90% |

| 32 | 0.2510 | 0.0012 | 55.33% |

| 33 | 0.2515 | 0.0008 | 54.92% |

| 34 | 0.2512 | 0.0009 | 55.13% |

| 35 | 0.2514 | 0.0009 | 54.99% |

| 36 | 0.2513 | 0.0009 | 55.04% |

| 37 | 0.2512 | 0.0008 | 55.16% |

| 38 | 0.2512 | 0.0005 | 55.16% |

| 39 | 0.2510 | 0.0006 | 55.34% |

| 40 | 0.2511 | 0.0007 | 55.27% |

| 41 | 0.2509 | 0.0006 | 55.44% |

| 42 | 0.2510 | 0.0004 | 55.38% |

| 43 | 0.2509 | 0.0003 | 55.40% |

| 44 | 0.2510 | 0.0003 | 55.34% |

| 45 | 0.2509 | 0.0003 | 55.47% |

| 46 | 0.2509 | 0.0003 | 55.42% |

| 47 | 0.2510 | 0.0000 | 55.38% |

| 48 | 0.2510 | 0.0001 | 55.36% |

| 49 | 0.2510 | 0.0000 | 55.38% |

| 50 | 0.2510 | 0.0000 | 55.38% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.2509 at 45 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.2510

- Mean Success Rate: 55.38%
