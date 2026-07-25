# Grouped WC Ax Rerun Plan - 2026-07-25

## Status

- [x] Identified issue: prior WC Ax jobs ran one independent Ax search per seed.
- [x] Archived those WC outputs under `outputs/fold_aggregated_ax_expanded_2026-07-25/archived_incorrect_independent_wc_seed_ax/`.
- [x] Added an archive README explaining why those runs should not be used as grouped WC hyperparameter tuning evidence.
- [x] Updated the Ax runner so WC can evaluate one candidate hyperparameter set across multiple seed roots.
- [x] Updated the SLURM wrapper so a comma-separated root list uses grouped WC mode.
- [ ] Review the rerun commands together before submitting.
- [ ] Run a tiny grouped WC proof job.
- [ ] If proof output is correct, submit grouped WC KNN and XGBoost jobs.

## Correct Objective

For WC seed aggregation:

```text
for each Ax trial:
  propose one hyperparameter set
  evaluate that same hyperparameter set on seed42..seed51
  objective = mean balanced_accuracy across seeds
```

For LPSO fold aggregation, the current design is already correct:

```text
for each Ax trial:
  propose one hyperparameter set
  evaluate that same hyperparameter set over all LPSO folds
  objective = mean balanced_accuracy across folds
```

## Seed Roots

```bash
WC_ROOTS_42_51="/old_data/ANOVA_W_C_ad_cntrl_seed42,/old_data/ANOVA_W_C_ad_cntrl_seed43,/old_data/ANOVA_W_C_ad_cntrl_seed44,/old_data/ANOVA_W_C_ad_cntrl_seed45,/old_data/ANOVA_W_C_ad_cntrl_seed46,/old_data/ANOVA_W_C_ad_cntrl_seed47,/old_data/ANOVA_W_C_ad_cntrl_seed48,/old_data/ANOVA_W_C_ad_cntrl_seed49,/old_data/ANOVA_W_C_ad_cntrl_seed50,/old_data/ANOVA_W_C_ad_cntrl_seed51"
WC_ROOTS_PROOF="/old_data/ANOVA_W_C_ad_cntrl_seed42,/old_data/ANOVA_W_C_ad_cntrl_seed43"
```

## Proof Command

This should produce one Ax search with two seed evaluations per trial.

```bash
cd /scratch/ans9868/rebuttal-deep-eeg-full-pipeline/eeg-full-pipeline

WC_ROOTS_PROOF="/old_data/ANOVA_W_C_ad_cntrl_seed42,/old_data/ANOVA_W_C_ad_cntrl_seed43"

bash rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/scripts/run_fold_aggregated_ax_xgboost_slurm.sh \
  w_c \
  "$WC_ROOTS_PROOF" \
  rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/outputs/fold_aggregated_ax_expanded_2026-07-25/proof_knn_wc_seeds42-43_ax2_grouped \
  proof_knn_wc_seeds42_43_ax2_grouped \
  knn \
  knn_expanded \
  2 \
  balanced_accuracy \
  0 \
  00:20:00
```

Expected proof checks:

```bash
python - <<'PY'
import pandas as pd
out = "rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/outputs/fold_aggregated_ax_expanded_2026-07-25/proof_knn_wc_seeds42-43_ax2_grouped"
trials = pd.read_csv(f"{out}/trials.csv")
folds = pd.read_csv(f"{out}/trial_fold_results.csv")
print(trials[["trial_number", "objective_value", "n_folds", "n_data_roots"]])
print(folds[["trial_number", "fold_name", "data_root_name", "balanced_accuracy"]])
PY
```

We want `trials.n_folds == 2`, `trials.n_data_roots == 2`, and two `trial_fold_results` rows per trial.

## Full Rerun Commands

Only run these after the proof output looks right.

```bash
cd /scratch/ans9868/rebuttal-deep-eeg-full-pipeline/eeg-full-pipeline

WC_ROOTS_42_51="/old_data/ANOVA_W_C_ad_cntrl_seed42,/old_data/ANOVA_W_C_ad_cntrl_seed43,/old_data/ANOVA_W_C_ad_cntrl_seed44,/old_data/ANOVA_W_C_ad_cntrl_seed45,/old_data/ANOVA_W_C_ad_cntrl_seed46,/old_data/ANOVA_W_C_ad_cntrl_seed47,/old_data/ANOVA_W_C_ad_cntrl_seed48,/old_data/ANOVA_W_C_ad_cntrl_seed49,/old_data/ANOVA_W_C_ad_cntrl_seed50,/old_data/ANOVA_W_C_ad_cntrl_seed51"

bash rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/scripts/run_fold_aggregated_ax_xgboost_slurm.sh \
  w_c \
  "$WC_ROOTS_42_51" \
  rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/outputs/fold_aggregated_ax_expanded_2026-07-25/knn_wc_seeds42-51_ax20_grouped \
  knn_wc_seeds42_51_ax20_grouped \
  knn \
  knn_expanded \
  20 \
  balanced_accuracy \
  0 \
  01:00:00

bash rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/scripts/run_fold_aggregated_ax_xgboost_slurm.sh \
  w_c \
  "$WC_ROOTS_42_51" \
  rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/outputs/fold_aggregated_ax_expanded_2026-07-25/xgboost_wc_seeds42-51_ax20_grouped \
  xgboost_wc_seeds42_51_ax20_grouped \
  xgboost \
  xgboost_expanded \
  20 \
  balanced_accuracy \
  0 \
  03:00:00
```

## Notes

- The ongoing LPSO full50 Ax jobs are not part of this mistake because each Ax trial already averages across LPSO folds.
- The corrected WC outputs should use new names with `seeds42-51` and `grouped` so they cannot be confused with the archived independent per-seed runs.
