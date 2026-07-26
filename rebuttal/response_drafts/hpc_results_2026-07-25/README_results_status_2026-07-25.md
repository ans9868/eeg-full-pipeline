# HPC Results Snapshot - 2026-07-25

Local response-results directory:

```text
/Users/user/projects/eeg-full-pipeline/rebuttal/response_drafts/hpc_results_2026-07-25
```

HPC project root:

```text
/scratch/ans9868/rebuttal-deep-eeg-full-pipeline/eeg-full-pipeline
```

## Summary CSVs

| File | Purpose |
|---|---|
| `ax_results_summary_2026-07-25.csv` | One row per AX result directory, including finished/partial status, best observed score, best observed params, and full local/HPC paths. |
| `ax_trial_level_results_2026-07-25.csv` | One row per AX trial from every copied `trials.csv`. |
| `ax_best_trial_fold_spread_2026-07-25.csv` | Fold/seed-unit distribution for each best observed AX trial. |
| `deep_learning_results_summary_2026-07-25.csv` | One row per deep-learning model/split from copied `summary_metrics.csv` files. |
| `neural_lpso_p6_results_status_2026-07-25.csv` | Neural P=6 subject-disjoint GPU pilot/full-run status and aggregate metrics. |
| `neural_lpso_p6_per_fold_2026-07-25.csv` | Per-fold metrics from the completed 10-fold neural P=6 GPU pilot. |
| `results_file_manifest_2026-07-25.csv` | Full local and HPC path manifest for copied raw result files. |
| `current_squeue_2026-07-25.txt` | Latest saved scheduler snapshot when this local bundle was generated. |

## Current Scheduler Snapshot

```text
JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
          14769929       all fold-ax-  ans9868  R    1:46:01      1 ga013
          14771787 cpu_short fold-ax-  ans9868  R       5:47      1 cs628
          14771324 cpu_short neural_l  ans9868  R      35:50      1 cs640
```

## Key AX Results In This Snapshot

| result_name | status | model | protocol | trials_completed | trials_expected | n_folds_or_units | n_data_roots | best_balanced_accuracy | best_mean_accuracy | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| archived_incorrect_independent_wc_seed_ax | archived_not_final |  | w_c |  |  |  |  |  |  | 20 independent per-seed WC Ax dirs archived; diagnostic only |
| knn_lpso_full50_ax20 | finished | knn | lpso | 20.0 | 20.0 | 50.0 |  | 0.7297113428875338 | 0.7280561807602903 | final candidate |
| knn_wc_seeds42-51_ax20_grouped | finished | knn | w_c | 20.0 | 20.0 | 10.0 | 10.0 | 0.8373332660568467 | 0.8386157448053849 | final candidate |
| proof_knn_lpso5_ax2 | finished | knn | lpso | 2.0 | 2.0 | 5.0 |  | 0.7850192725714148 | 0.7848569640424878 | proof/smoke only |
| proof_knn_wc_seeds42-43_ax2_grouped | finished | knn | w_c | 2.0 | 2.0 | 2.0 | 2.0 | 0.8303584511939042 | 0.8315774070822359 | proof/smoke only |
| proof_xgb_lpso5_ax2 | finished | xgboost | lpso | 2.0 | 2.0 | 5.0 |  | 0.7590195129297383 | 0.7588794497511411 | proof/smoke only |
| xgboost_lpso_full50_ax20 | partial_or_running | xgboost | lpso | 14.0 | 20.0 | 50.0 |  | 0.7184984154214823 | 0.7163045393567681 | partial snapshot; job may still be running |
| xgboost_wc_seeds42-51_ax20_grouped | partial_or_running | xgboost | w_c | 4.0 | 20.0 | 10.0 | 10.0 | 0.9564504902658758 | 0.9580772607550484 | partial snapshot; job may still be running |

## Key Deep Learning Results In This Snapshot

| result_name | model | split | accuracy | balanced_accuracy | shared_subject_count | epochs_ran | early_stopped |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DL_W_C_ad_cntrl_seed42_hpc | eegnet_feature_smoke | subject_disjoint_smoke | 0.4474929044465468 | 0.4450250626566416 | 0 | 21 | True |
| DL_W_C_ad_cntrl_seed42_hpc | eegnet_feature_smoke | subject_overlap_smoke | 0.9562436400639628 | 0.9537334347702232 | 65 | 25 | False |
| DL_W_C_ad_cntrl_seed42_hpc | transformer_feature_smoke | subject_disjoint_smoke | 0.4626300851466414 | 0.4621052631578947 | 0 | 24 | True |
| DL_W_C_ad_cntrl_seed42_hpc | transformer_feature_smoke | subject_overlap_smoke | 0.9815380142462568 | 0.9820502760800556 | 65 | 14 | True |
| DL_W_C_ad_cntrl_seed42_hpc_braindecode_full | canonical_eegnet | subject_disjoint_smoke | 0.3500473036896878 | 0.3478947368421053 | 0 | 17 | True |
| DL_W_C_ad_cntrl_seed42_hpc_braindecode_full | canonical_eegnet | subject_overlap_smoke | 0.9060910015990696 | 0.9046940858995332 | 65 | 25 | False |
| DL_W_C_ad_cntrl_seed42_hpc_braindecode_full | eeg_conformer_small | subject_disjoint_smoke | 0.3945127719962157 | 0.3929323308270676 | 0 | 20 | True |
| DL_W_C_ad_cntrl_seed42_hpc_braindecode_full | eeg_conformer_small | subject_overlap_smoke | 0.9803750545137374 | 0.98021264219786 | 65 | 20 | True |
| DL_W_C_ad_cntrl_seed42_hpc_braindecode_smoke | canonical_eegnet | subject_disjoint_smoke | 0.7142857142857143 | 0.657516339869281 | 0 | 2 | False |
| DL_W_C_ad_cntrl_seed42_hpc_braindecode_smoke | canonical_eegnet | subject_overlap_smoke | 0.6470588235294118 | 0.5384615384615384 | 8 | 2 | False |
| DL_W_C_ad_cntrl_seed42_hpc_braindecode_smoke | eeg_conformer_small | subject_disjoint_smoke | 0.7142857142857143 | 0.5519607843137255 | 0 | 2 | False |
| DL_W_C_ad_cntrl_seed42_hpc_braindecode_smoke | eeg_conformer_small | subject_overlap_smoke | 0.9117647058823528 | 0.9236874236874236 | 8 | 2 | False |

## Neural P=6 Subject-Disjoint GPU Status

| result_name | status | job_id | folds | protocol | resources | elapsed | canonical_eegnet mean BA | eeg_conformer_small mean BA | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DL_LPSO_P6_ad_cntrl_random50_braindecode_gpu_pilot10 | completed | 14772889 | 10 | P=6 random stratified, 3 AD + 3 CN held out, shared subjects 0 | 1 H200 GPU, 4 CPU, 56G RAM | 00:11:29 | 0.5258 | 0.5349 | Completed pilot; local raw outputs copied into `raw_deep_learning`. |
| DL_LPSO_P6_ad_cntrl_random50_braindecode_gpu_full50 | pending | 14773564 | 50 | P=6 random stratified, 3 AD + 3 CN held out | 1 H200 GPU, 4 CPU, 56G RAM | not started | pending | pending | Submitted 2026-07-26; pending on `QOSGrpGRES` at last check. |

## Full Paths

All copied files have both local and HPC paths in:

```text
/Users/user/projects/eeg-full-pipeline/rebuttal/response_drafts/hpc_results_2026-07-25/results_file_manifest_2026-07-25.csv
```

The raw AX result mirror is here:

```text
/Users/user/projects/eeg-full-pipeline/rebuttal/response_drafts/hpc_results_2026-07-25/raw_ax
```

The raw deep-learning result mirror is here:

```text
/Users/user/projects/eeg-full-pipeline/rebuttal/response_drafts/hpc_results_2026-07-25/raw_deep_learning
```

## Notes

- `knn_lpso_full50_ax20` is finished and usable as the LPSO KNN AX result.
- `knn_wc_seeds42-51_ax20_grouped` is finished in this snapshot and is the corrected grouped-WC KNN result.
- `xgboost_wc_seeds42-51_ax20_grouped` finished after this snapshot with best grouped-WC balanced accuracy `0.9602919718876446`.
- `xgboost_lpso_full50_ax20` ended at 19 fully completed trials out of the planned 20 because the SLURM walltime limit stopped the final in-progress trial. The best fully completed trial was trial 17 with balanced accuracy `0.7252525512911437` and mean accuracy `0.7230845354398571` across 50 LPSO folds.
- The XGBoost LPSO search had effectively plateaued before the walltime stop: the top completed balanced accuracies were `0.7253`, `0.7250`, `0.7235`, `0.7220`, and `0.7185`. This supports treating the 19/20 run as a near-complete tuning sensitivity check while still reporting the precise completed-trial count in methods/notes.
- `archived_incorrect_independent_wc_seed_ax` is retained only as a diagnostic archive; it is not final rebuttal evidence.
- The neural P=6 GPU pilot is completed and supports the reviewer-facing claim that true subject-disjoint neural evaluation is much harder than W/C subject-overlap evaluation. The 50-fold neural GPU run is submitted as the cleaner canonical result.

## XGBoost LPSO 19/20 Trial Details

The intended budget was 20 Ax trials. Trial 19 was launched and partially
evaluated, but the job timed out before all 50 LPSO folds completed. The
`trials.csv` file therefore contains 19 complete aggregate evaluations
(`trial_number` 0 through 18). For analysis, use only those complete rows.

Top completed XGBoost LPSO trials:

| Trial | Balanced accuracy | Mean accuracy | Notes |
|---:|---:|---:|---|
| 17 | `0.7252525513` | `0.7230845354` | best completed trial |
| 14 | `0.7249581787` | `0.7227282319` | essentially tied with best |
| 15 | `0.7234674647` | `0.7213257993` | plateau region |
| 16 | `0.7219920127` | `0.7197445643` | plateau region |
| 12 | `0.7184984154` | `0.7163045394` | start of plateau |

Best completed XGBoost LPSO hyperparameters:

```text
max_depth: 12
learning_rate: 0.01
n_estimators: 321
subsample: 0.5
colsample_bytree: 0.5
min_child_weight: 1.0
```
