# Per-Subject Success Rate Variance Analysis

## Experiment: PCA_L_6_Random

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

| 1 | 0.2967 | 0.0102 | 51.67% |

| 2 | 0.2655 | 0.0140 | 55.87% |

| 3 | 0.2529 | 0.0251 | 54.58% |

| 4 | 0.2469 | 0.0190 | 57.43% |

| 5 | 0.2467 | 0.0187 | 55.88% |

| 6 | 0.2479 | 0.0124 | 55.37% |

| 7 | 0.2394 | 0.0168 | 57.93% |

| 8 | 0.2381 | 0.0180 | 57.26% |

| 9 | 0.2393 | 0.0172 | 57.01% |

| 10 | 0.2395 | 0.0135 | 56.89% |

| 11 | 0.2382 | 0.0119 | 56.56% |

| 12 | 0.2379 | 0.0140 | 57.07% |

| 13 | 0.2292 | 0.0133 | 58.69% |

| 14 | 0.2314 | 0.0119 | 56.97% |

| 15 | 0.2282 | 0.0142 | 57.70% |

| 16 | 0.2300 | 0.0164 | 57.97% |

| 17 | 0.2269 | 0.0138 | 58.86% |

| 18 | 0.2260 | 0.0119 | 57.92% |

| 19 | 0.2238 | 0.0118 | 58.48% |

| 20 | 0.2218 | 0.0165 | 59.22% |

| 21 | 0.2209 | 0.0144 | 59.02% |

| 22 | 0.2204 | 0.0112 | 58.70% |

| 23 | 0.2216 | 0.0123 | 58.65% |

| 24 | 0.2217 | 0.0147 | 58.47% |

| 25 | 0.2168 | 0.0134 | 59.35% |

| 26 | 0.2181 | 0.0120 | 59.14% |

| 27 | 0.2141 | 0.0111 | 59.23% |

| 28 | 0.2118 | 0.0125 | 59.91% |

| 29 | 0.2116 | 0.0113 | 59.86% |

| 30 | 0.2112 | 0.0103 | 59.95% |

| 31 | 0.2109 | 0.0101 | 59.41% |

| 32 | 0.2116 | 0.0105 | 59.53% |

| 33 | 0.2108 | 0.0113 | 59.33% |

| 34 | 0.2069 | 0.0111 | 59.68% |

| 35 | 0.2078 | 0.0080 | 59.78% |

| 36 | 0.2052 | 0.0097 | 59.93% |

| 37 | 0.2031 | 0.0090 | 60.43% |

| 38 | 0.2079 | 0.0102 | 59.35% |

| 39 | 0.2058 | 0.0067 | 59.75% |

| 40 | 0.2061 | 0.0077 | 59.61% |

| 41 | 0.2009 | 0.0076 | 60.10% |

| 42 | 0.2018 | 0.0077 | 59.82% |

| 43 | 0.2012 | 0.0058 | 59.95% |

| 44 | 0.2016 | 0.0071 | 59.81% |

| 45 | 0.1992 | 0.0049 | 59.87% |

| 46 | 0.2003 | 0.0049 | 59.89% |

| 47 | 0.1985 | 0.0044 | 59.93% |

| 48 | 0.1970 | 0.0021 | 60.06% |

| 49 | 0.1970 | 0.0019 | 59.98% |

| 50 | 0.1969 | 0.0000 | 60.00% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1969 at 50 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1969

- Mean Success Rate: 60.00%
