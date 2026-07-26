# MLP/SVM AX Run Plan - 2026-07-26

## Goal

Extend the AD/CN hyperparameter sanity check from KNN/XGBoost to two additional classical model families:

- `svm`: scaled linear SVM on transformed features.
- `mlp`: scaled sklearn MLP on transformed features.

This tests whether the subject-overlap versus subject-disjoint gap persists beyond distance-based and boosted-tree baselines.

## Search Design

The same fold-aggregated AX objective is used:

```text
for each Ax trial:
  propose one hyperparameter set
  evaluate that same setting over all folds/seeds
  objective = mean balanced_accuracy
```

For LPSO:

```text
same params across 50 LPSO folds
```

For grouped WC:

```text
same params across seed42..seed51 within-subject splits
```

## Models

### SVM

Implementation:

```text
StandardScaler -> LinearSVC
```

Search space:

- `C`: log range `0.001` to `100.0`
- `class_weight`: `none` or `balanced`
- `max_iter`: `3000`, `5000`, or `8000`

Rationale: linear SVM is much safer than RBF SVM for the current fold sizes.

### MLP

Implementation:

```text
StandardScaler -> sklearn.neural_network.MLPClassifier
```

Search space:

- `hidden_layer_sizes`: `64`, `128`, `64_32`, `128_64`
- `alpha`: log range `1e-5` to `1e-2`
- `learning_rate_init`: log range `1e-4` to `1e-2`
- `batch_size`: `64`, `128`, `256`
- `activation`: `relu`, `tanh`
- `max_iter`: `100`, `150`

MLP uses sklearn early stopping.

## Run Order

- [x] Submit proof: SVM LPSO 5 folds, 2 AX trials. Job `14775130`, completed.
- [x] Submit proof: MLP LPSO 5 folds, 2 AX trials. Job `14775131`, completed.
- [x] Submit proof: SVM grouped WC seed42+seed43, 2 AX trials. Job `14775132`, completed.
- [x] Submit proof: MLP grouped WC seed42+seed43, 2 AX trials. Job `14775133`, completed.
- [x] Confirm proof output row counts and summary files.
- [x] Submit full SVM LPSO 50 folds, 20 AX trials, 6-hour walltime. Job `14775146`.
- [x] Submit full MLP LPSO 50 folds, 20 AX trials, 6-hour walltime. Job `14775147`.
- [x] Submit full SVM grouped WC seed42..51, 20 AX trials, 6-hour walltime. Job `14775148`.
- [x] Submit full MLP grouped WC seed42..51, 20 AX trials, 6-hour walltime. Job `14775149`.
- [ ] Monitor full SVM LPSO job `14775146`.
- [ ] Monitor full MLP LPSO job `14775147`.
- [ ] Monitor full SVM grouped WC job `14775148`.
- [ ] Monitor full MLP grouped WC job `14775149`.

## Proof Results

| Proof | Job | Status | Shape | Best balanced accuracy |
|---|---:|---|---|---:|
| SVM LPSO 5-fold AX2 | `14775130` | completed | 2 trials x 5 folds | `0.675447` |
| MLP LPSO 5-fold AX2 | `14775131` | completed | 2 trials x 5 folds | `0.664775` |
| SVM grouped WC seed42+43 AX2 | `14775132` | completed | 2 trials x 2 seed roots | `0.807855` |
| MLP grouped WC seed42+43 AX2 | `14775133` | completed | 2 trials x 2 seed roots | `0.951022` |

## Timeout Interpretation

If an MLP/SVM full run hits walltime, use only fully completed trials in `trials.csv`. Report the exact number completed and treat it as an AX-budget sensitivity check, consistent with the XGBoost LPSO 19/20 run.
