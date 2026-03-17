# Per-Subject Success Rate Variance Analysis

## Experiment: PCA_L_2_Random

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

| 1 | 0.5000 | 0.0000 | 50.00% |

| 2 | 0.3250 | 0.0254 | 51.39% |

| 3 | 0.2989 | 0.0061 | 50.89% |

| 4 | 0.2838 | 0.0083 | 51.07% |

| 5 | 0.2776 | 0.0058 | 50.45% |

| 6 | 0.2679 | 0.0114 | 52.38% |

| 7 | 0.2644 | 0.0110 | 50.85% |

| 8 | 0.2610 | 0.0108 | 51.02% |

| 9 | 0.2633 | 0.0057 | 49.09% |

| 10 | 0.2590 | 0.0095 | 51.55% |

| 11 | 0.2550 | 0.0123 | 52.44% |

| 12 | 0.2551 | 0.0105 | 51.97% |

| 13 | 0.2546 | 0.0089 | 51.33% |

| 14 | 0.2543 | 0.0078 | 51.71% |

| 15 | 0.2541 | 0.0069 | 51.22% |

| 16 | 0.2512 | 0.0072 | 51.80% |

| 17 | 0.2480 | 0.0092 | 50.34% |

| 18 | 0.2515 | 0.0068 | 53.00% |

| 19 | 0.2496 | 0.0079 | 51.69% |

| 20 | 0.2476 | 0.0092 | 52.86% |

| 21 | 0.2467 | 0.0074 | 52.37% |

| 22 | 0.2480 | 0.0089 | 53.17% |

| 23 | 0.2436 | 0.0096 | 52.21% |

| 24 | 0.2460 | 0.0087 | 52.87% |

| 25 | 0.2436 | 0.0086 | 52.75% |

| 26 | 0.2446 | 0.0066 | 52.78% |

| 27 | 0.2456 | 0.0073 | 52.03% |

| 28 | 0.2458 | 0.0083 | 51.53% |

| 29 | 0.2429 | 0.0061 | 52.93% |

| 30 | 0.2403 | 0.0064 | 53.33% |

| 31 | 0.2402 | 0.0062 | 53.55% |

| 32 | 0.2407 | 0.0070 | 53.79% |

| 33 | 0.2416 | 0.0087 | 53.69% |

| 34 | 0.2396 | 0.0056 | 53.34% |

| 35 | 0.2406 | 0.0059 | 53.55% |

| 36 | 0.2386 | 0.0056 | 53.22% |

| 37 | 0.2419 | 0.0046 | 53.82% |

| 38 | 0.2390 | 0.0061 | 54.20% |

| 39 | 0.2374 | 0.0050 | 54.02% |

| 40 | 0.2380 | 0.0056 | 54.14% |

| 41 | 0.2366 | 0.0039 | 53.97% |

| 42 | 0.2378 | 0.0051 | 53.90% |

| 43 | 0.2364 | 0.0039 | 54.24% |

| 44 | 0.2360 | 0.0042 | 54.27% |

| 45 | 0.2367 | 0.0036 | 54.49% |

| 46 | 0.2353 | 0.0029 | 54.53% |

| 47 | 0.2355 | 0.0022 | 54.41% |

| 48 | 0.2351 | 0.0018 | 54.38% |

| 49 | 0.2346 | 0.0011 | 54.70% |

| 50 | 0.2347 | 0.0000 | 54.59% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.2346 at 49 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.2347

- Mean Success Rate: 54.59%
