# Context - 2026-07-25 AX Grouped WC Fix

## Issue

The first expanded WC Ax runs used one independent Ax search per seed, for example separate jobs such as `knn_wc_seed49_ax20` and `knn_wc_seed51_ax20`.

That is not the intended rebuttal design. It lets Ax choose different hyperparameters per seed, so the result cannot support a statement like "this hyperparameter setting was selected based on mean performance across seeds."

## Correct Design

For WC:

```text
for each Ax trial:
  propose one hyperparameter set
  evaluate the same setting on seed42..seed51
  objective = mean balanced_accuracy across seeds
```

For LPSO:

```text
for each Ax trial:
  propose one hyperparameter set
  evaluate the same setting across all LPSO folds
  objective = mean balanced_accuracy across folds
```

The existing LPSO runner already follows this fold-aggregated pattern.

## Actions Taken

- Added `--data-roots` support to `run_fold_aggregated_ax_xgboost.py`.
- Kept `--data-root` support for existing single-root LPSO and proof workflows.
- Updated per-fold result rows with `data_root` and `data_root_name`.
- Updated trial summaries with `n_data_roots` and `data_roots`.
- Updated `run_fold_aggregated_ax_xgboost_slurm.sh` so a comma-separated roots argument uses `--data-roots`.
- Archived incorrect independent WC seed outputs on HPC:
  `rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/outputs/fold_aggregated_ax_expanded_2026-07-25/archived_incorrect_independent_wc_seed_ax/`
- Added rerun plan:
  `rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/grouped_wc_ax_rerun_plan_2026-07-25.md`

## Validation

- Local syntax check passed:
  `python3 -m py_compile rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/scripts/run_fold_aggregated_ax_xgboost.py`
- HPC syntax check passed via `conda run -n dev-env python -m py_compile ...`.

## Current Stop Point

No grouped WC rerun has been submitted yet. Next step is to review the proof command together, then run the tiny grouped WC proof job before launching full grouped WC KNN/XGBoost jobs.
