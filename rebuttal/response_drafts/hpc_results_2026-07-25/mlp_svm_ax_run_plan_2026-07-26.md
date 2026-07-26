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
- [x] Monitor full SVM LPSO job `14775146`, completed `00:09:37`.
- [x] Monitor full MLP LPSO job `14775147`, completed `01:47:35`.
- [x] Monitor full SVM grouped WC job `14775148`, completed `00:02:41`.
- [x] Monitor full MLP grouped WC job `14775149`, completed `00:16:46`.

## Proof Results

| Proof | Job | Status | Shape | Best balanced accuracy |
|---|---:|---|---|---:|
| SVM LPSO 5-fold AX2 | `14775130` | completed | 2 trials x 5 folds | `0.675447` |
| MLP LPSO 5-fold AX2 | `14775131` | completed | 2 trials x 5 folds | `0.664775` |
| SVM grouped WC seed42+43 AX2 | `14775132` | completed | 2 trials x 2 seed roots | `0.807855` |
| MLP grouped WC seed42+43 AX2 | `14775133` | completed | 2 trials x 2 seed roots | `0.951022` |

## Timeout Interpretation

If an MLP/SVM full run hits walltime, use only fully completed trials in `trials.csv`. Report the exact number completed and treat it as an AX-budget sensitivity check, consistent with the XGBoost LPSO 19/20 run.

## Final Full Results

All four full MLP/SVM AX jobs completed without walltime truncation.

| Run | Job | Trials | Units | Best balanced accuracy | Best mean accuracy | Best parameters |
|---|---:|---:|---:|---:|---:|---|
| SVM LPSO full50 | `14775146` | 20 | 50 folds | `0.7367509422` | `0.7350160027` | `C=0.001`, `class_weight=balanced`, `max_iter=5000` |
| MLP LPSO full50 | `14775147` | 20 | 50 folds | `0.7440630210` | `0.7427222009` | `alpha=0.01`, `learning_rate_init=0.0001`, `batch_size=256`, `activation=relu`, `max_iter=100`, `hidden_layer_sizes=128` |
| SVM grouped W/C seeds42-51 | `14775148` | 20 | 10 seed roots | `0.8104940605` | `0.8146619842` | `C=0.2275256886`, `class_weight=balanced`, `max_iter=8000` |
| MLP grouped W/C seeds42-51 | `14775149` | 20 | 10 seed roots | `0.9689624566` | `0.9695785777` | `alpha=0.01`, `learning_rate_init=0.0021319416`, `batch_size=256`, `activation=tanh`, `max_iter=150`, `hidden_layer_sizes=128_64` |
