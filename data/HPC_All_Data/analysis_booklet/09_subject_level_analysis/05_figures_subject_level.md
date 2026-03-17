# Subject-Level Analysis — Figures

## Figure 1: Subject Accuracy Distribution (P=6 folds)

Subject accuracy per fold, split by pipeline (ANOVA / PCA) and cross-validation strategy
(Uniform-12 / Random-50), for experiments with 6 subjects per fold. Each panel shows the
distribution across all folds for all four models (KNN, MLP, SVM, XGBoost).

![Subject accuracy distributions for P=6 folds. ANOVA experiments achieve medians at 83.33%, while all PCA experiments cluster at the 50% chance level.](09_subject_level_analysis/fig_subject_accuracy_small_multiples_P6.png)

---

## Figure 2: Subject Accuracy Distribution (P=2 folds)

Same layout as Figure 1 but for experiments with 2 subjects per fold. The further
discretisation to {0%, 50%, 100%} is clearly visible. ANOVA achieves 100% median subject
accuracy; PCA remains at 50%.

![Subject accuracy distributions for P=2 folds. ANOVA achieves a median of 100% with P=2; PCA remains at 50%.](09_subject_level_analysis/fig_subject_accuracy_small_multiples_P2.png)

---

## Figure 3: Epoch Accuracy vs Subject Accuracy Scatter (P=6)

Scatter plot showing fold-level epoch accuracy (x-axis) against fold-level subject
accuracy (y-axis) for all experiments with 6 subjects per fold. One point per fold per
model per experiment. Pearson correlation lines are overlaid.

![Epoch vs subject accuracy scatter for P=6 folds. Strong positive correlation in ANOVA experiments (r > 0.80); moderate correlation in PCA experiments.](09_subject_level_analysis/fig_epoch_vs_subject_scatter_P6.png)

---

## Figure 4: Epoch Accuracy vs Subject Accuracy Scatter (P=2)

Same as Figure 3 for P=2 folds. The trimodal subject accuracy distribution (0%, 50%,
100%) is clearly visible.

![Epoch vs subject accuracy scatter for P=2 folds. The discrete nature of subject accuracy with only 2 subjects is visible.](09_subject_level_analysis/fig_epoch_vs_subject_scatter_P2.png)

---

## Figure 5: Subject Minus Epoch Accuracy Delta Distribution

Violin + boxplot of the per-fold difference $\Delta = \text{subject\_acc} - \text{epoch\_acc}$,
grouped by pipeline (ANOVA / PCA) and subject count ($P = 2$ / $P = 6$). Values above
zero indicate folds where majority voting improved accuracy over direct epoch
classification.

![Distribution of per-fold subject_acc minus epoch_acc. ANOVA shows a positive delta (majority voting helps); PCA shows a negative delta (majority voting at chance level, epoch accuracy was modestly above chance).](09_subject_level_analysis/fig_subject_minus_epoch_delta_distribution.png)


---

## Figure 6: Aggregate Subject Accuracy vs Mean Epoch Accuracy (P=6)

Each point represents one model x hyperparameter configuration aggregated across **all
P=6 folds** (Random-50: 300 subjects total; Uniform-12: 72 subjects total).

- **X-axis** -- mean epoch accuracy across all folds for that configuration (%).
- **Y-axis** -- percentage of subjects correctly classified across all folds (%).
- **Colour** -- model (MLP=blue, XGBoost=orange, SVM=green, KNN=red).
- **Marker** -- strategy (circle = Random-50,  square = Uniform-12).
- Dashed diagonal: y = x  (subject accuracy = epoch accuracy).

This view reveals whether high epoch accuracy reliably translates to high subject
accuracy across diverse hyperparameter settings.

![Aggregate scatter P=6](09_subject_level_analysis/fig_aggregate_epoch_vs_subject_P6.png)
