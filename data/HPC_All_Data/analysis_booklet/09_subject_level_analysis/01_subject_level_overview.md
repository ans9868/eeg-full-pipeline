# Subject-Level Evaluation — Overview

## Purpose

Epoch-level accuracy (the primary metric throughout this project) measures how well each
individual EEG epoch is classified. Subject-level accuracy asks a clinically harder and
more meaningful question: given *all* epochs recorded from one subject, can we correctly
identify whether that subject has Alzheimer's Disease?

This section reports a full subject-level evaluation performed across all six LPSO
experiments (3 ANOVA + 3 PCA), using both the 12-fold systematic (Uniform) and 50-fold
random (Random) cross-validation strategies.

---

## Experimental Setup

### Data

| Parameter | Value |
|-----------|-------|
| Total epoch-level prediction rows loaded | 4,856 parquet files |
| Experiments evaluated | 6 (ANOVA_L_2_Random, ANOVA_L_6_Random, ANOVA_L_6_Uniform, PCA_L_2_Random, PCA_L_6_Random, PCA_L_6_Uniform) |
| Models | KNN, MLP, SVM, XGBoost |
| Cross-validation strategies | Uniform-12 (12 systematic folds), Random-50 (50 random folds) |

### Label Mapping

| Value | Meaning |
|-------|---------|
| Group = 'alz' | Alzheimer's Disease (AD) patient |
| Group = 'cntrl' | Healthy Control |
| label = 0 | AD (ground truth) |
| label = 1 | Control (ground truth) |
| prediction = 0 | Predicted AD |
| prediction = 1 | Predicted Control |

### AD-Ratio Decision Rule

For each subject within a fold, the fraction of epochs predicted as AD is computed:

$$\text{AD\_ratio} = \frac{\sum_{i} \mathbf{1}[\hat{y}_i = 0]}{N_{\text{epochs}}}$$

The subject is classified as AD if $\text{AD\_ratio} \geq \tau = 0.5$ (majority vote),
otherwise as Control.

**Subject accuracy per fold** = fraction of subjects in that fold whose label matches
their majority-vote prediction.

---

## HP Selection Modes

Two hyperparameter selection modes are evaluated:

- **Mode 1 (paper-consistent):** Select the HP set that maximises *median epoch accuracy*
  across folds. This mirrors the primary reported results.
- **Mode 2 (deployment-aligned):** Select the HP set that maximises *median subject
  accuracy* across folds. This explores whether subject-optimised HPs differ.

All acceptance-criteria comparisons use **Mode 1** to remain fully consistent with the
primary analysis.

---

## Quantisation Warning

With $P = 6$ subjects per fold, subject accuracy is restricted to a discrete set:

$$\text{subject\_acc} \in \left\{0,\ \tfrac{1}{6},\ \tfrac{2}{6},\ \tfrac{3}{6},\ \tfrac{4}{6},\ \tfrac{5}{6},\ 1\right\}$$

i.e. {0%, 16.67%, 33.33%, 50%, 66.67%, 83.33%, 100%}. With $P = 2$ the set collapses
further to {0%, 50%, 100%}.

This heavy discretisation creates tied ranks in Wilcoxon/Mann-Whitney tests; p-values
remain valid but statistical power is substantially lower than for continuous epoch
accuracy. Bootstrap confidence intervals on subject-accuracy medians may collapse to a
single point estimate.
