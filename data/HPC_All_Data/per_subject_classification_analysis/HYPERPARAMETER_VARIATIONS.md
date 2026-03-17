# Hyperparameter Variations Across Experiments

## Summary

No model×HP combinations with identical hyperparameters were found across all 4 experiments.

Below are the hyperparameters found for each model type in each experiment:


## KNN


| Experiment | Hyperparameters |

|------------|----------------|

| ANOVA_L_2_Random | metric=euclidean, n_neighbors=7, weights=uniform |

| ANOVA_L_6_Random | metric=euclidean, n_neighbors=15, weights=uniform |

| PCA_L_2_Random | metric=euclidean, n_neighbors=1, weights=uniform |

| PCA_L_6_Random | metric=euclidean, n_neighbors=7, weights=uniform |



## MLP


| Experiment | Hyperparameters |

|------------|----------------|

| ANOVA_L_2_Random | activation=tanh, alpha=0.1, hidden_layer_sizes=(100,) |

| ANOVA_L_6_Random | activation=tanh, alpha=0.1, hidden_layer_sizes=(50, 150) |

| PCA_L_2_Random | activation=tanh, alpha=0.1, hidden_layer_sizes=(50, 100, 200) |

| PCA_L_6_Random | activation=tanh, alpha=0.1, hidden_layer_sizes=(50, 150) |



## SVM


| Experiment | Hyperparameters |

|------------|----------------|

| ANOVA_L_2_Random | C=0.1, gamma=auto, kernel=rbf |

| ANOVA_L_6_Random | C=0.1, gamma=auto, kernel=linear |

| PCA_L_2_Random | C=0.1, gamma=auto, kernel=rbf |

| PCA_L_6_Random | C=0.1, gamma=auto, kernel=poly |



## XGBoost


| Experiment | Hyperparameters |

|------------|----------------|

| ANOVA_L_2_Random | learning_rate=0.2, max_depth=6, n_estimators=100, subsample=0.7 |

| ANOVA_L_6_Random | learning_rate=0.2, max_depth=3, n_estimators=100, subsample=0.7 |

| PCA_L_2_Random | learning_rate=0.2, max_depth=3, n_estimators=100, subsample=0.7 |

| PCA_L_6_Random | learning_rate=0.2, max_depth=6, n_estimators=100, subsample=0.7 |


