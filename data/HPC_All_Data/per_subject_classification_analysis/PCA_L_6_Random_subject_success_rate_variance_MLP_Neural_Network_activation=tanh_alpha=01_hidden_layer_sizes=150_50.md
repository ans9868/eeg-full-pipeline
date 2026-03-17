# Per-Subject Success Rate Variance Analysis

## Experiment: PCA_L_6_Random

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

| 1 | 0.2922 | 0.0258 | 51.67% |

| 2 | 0.2660 | 0.0176 | 53.12% |

| 3 | 0.2601 | 0.0102 | 52.80% |

| 4 | 0.2490 | 0.0181 | 54.25% |

| 5 | 0.2456 | 0.0180 | 52.95% |

| 6 | 0.2494 | 0.0124 | 53.82% |

| 7 | 0.2430 | 0.0152 | 53.63% |

| 8 | 0.2448 | 0.0114 | 52.61% |

| 9 | 0.2427 | 0.0128 | 53.85% |

| 10 | 0.2276 | 0.0165 | 55.52% |

| 11 | 0.2339 | 0.0153 | 54.76% |

| 12 | 0.2317 | 0.0162 | 56.15% |

| 13 | 0.2308 | 0.0148 | 55.82% |

| 14 | 0.2282 | 0.0170 | 55.53% |

| 15 | 0.2226 | 0.0131 | 57.17% |

| 16 | 0.2261 | 0.0135 | 55.46% |

| 17 | 0.2247 | 0.0125 | 56.12% |

| 18 | 0.2252 | 0.0142 | 56.62% |

| 19 | 0.2255 | 0.0147 | 55.68% |

| 20 | 0.2249 | 0.0140 | 56.46% |

| 21 | 0.2183 | 0.0141 | 57.11% |

| 22 | 0.2190 | 0.0133 | 56.58% |

| 23 | 0.2188 | 0.0160 | 57.10% |

| 24 | 0.2158 | 0.0121 | 57.88% |

| 25 | 0.2137 | 0.0130 | 57.16% |

| 26 | 0.2139 | 0.0125 | 57.63% |

| 27 | 0.2105 | 0.0100 | 58.02% |

| 28 | 0.2082 | 0.0141 | 58.17% |

| 29 | 0.2092 | 0.0118 | 57.94% |

| 30 | 0.2042 | 0.0142 | 58.16% |

| 31 | 0.2083 | 0.0111 | 57.94% |

| 32 | 0.2041 | 0.0120 | 58.49% |

| 33 | 0.1990 | 0.0108 | 58.92% |

| 34 | 0.2014 | 0.0120 | 58.59% |

| 35 | 0.2056 | 0.0127 | 57.63% |

| 36 | 0.1988 | 0.0085 | 58.63% |

| 37 | 0.1989 | 0.0105 | 58.01% |

| 38 | 0.1989 | 0.0099 | 58.24% |

| 39 | 0.1995 | 0.0090 | 58.62% |

| 40 | 0.1961 | 0.0080 | 58.97% |

| 41 | 0.1995 | 0.0092 | 58.58% |

| 42 | 0.1975 | 0.0108 | 58.71% |

| 43 | 0.1977 | 0.0079 | 58.50% |

| 44 | 0.1943 | 0.0072 | 58.62% |

| 45 | 0.1913 | 0.0079 | 58.56% |

| 46 | 0.1922 | 0.0070 | 58.64% |

| 47 | 0.1919 | 0.0046 | 58.56% |

| 48 | 0.1906 | 0.0049 | 58.72% |

| 49 | 0.1899 | 0.0029 | 58.57% |

| 50 | 0.1888 | 0.0000 | 58.61% |


## Interpretation


**Variance Stabilization**: Variance appears to stabilize after ~46 folds 
(change < 0.01 in last 5 data points).


**Minimum Variance**: 0.1888 at 50 folds.


**Final Statistics** (with all 50 folds):

- Mean Variance: 0.1888

- Mean Success Rate: 58.61%
