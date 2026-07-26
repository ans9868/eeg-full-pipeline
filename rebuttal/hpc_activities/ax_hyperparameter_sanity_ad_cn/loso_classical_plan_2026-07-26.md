# LOSO Classical ML Plan - 2026-07-26

## Goal

Run true leave-one-subject-out AD/CN evaluation for the classical feature
models. This is stronger than P=6 random LPSO because every subject is held out
exactly once. LOSO is a fixed evaluation, not an Ax tuning run.

## Design

- Feature roots: ANOVA/T-test and PCA.
- Folds: 65 LOSO folds, one held-out subject per fold.
- Models: KNN, XGBoost, SVM, MLP.
- Hyperparameters: fixed values from the existing rebuttal model-family runs or
  conservative defaults; no LOSO hyperparameter search.
- Primary metric: `subject_balanced_accuracy`, computed from majority-vote
  prediction for each held-out subject across all 65 folds.
- Secondary metrics: pooled epoch accuracy, pooled epoch balanced accuracy,
  mean fold accuracy, and subject-majority accuracy.

## Why The Metric Matters

Each LOSO fold has only one held-out subject, so the fold test set contains only
one class. Per-fold balanced accuracy is therefore not the right primary
quantity. The standalone LOSO evaluator aggregates all held-out subjects and
computes subject-majority balanced accuracy across the complete 65-subject LOSO
panel.

## Checklist

- [x] Confirm existing PySpark LPSO machinery accepts arbitrary fold lists.
- [x] Add LOSO YAML generator for ANOVA and PCA transformed roots.
- [x] Add standalone fixed-hyperparameter LOSO evaluator.
- [x] Validate standalone evaluator locally on tiny synthetic LOSO folds using `/Users/user/py-neuro-env`.
- [x] Generate LOSO YAMLs and inspect fold count.
- [ ] Copy/sync scripts and YAMLs to Torch.
- [ ] Run PySpark-only LOSO transforms for ANOVA and PCA.
- [ ] Run fixed LOSO model evaluations.
- [ ] Summarize and add to rebuttal response.

## Local Prototype Result

Local environment: `/Users/user/py-neuro-env`.

The standalone evaluator was validated on synthetic LOSO parquet folds with 8
held-out subjects. It ran KNN, SVM, MLP, and XGBoost, wrote
`model_summary.csv`, `fold_results.csv`, and `subject_predictions.csv`, and
computed subject-majority accuracy plus subject balanced accuracy. This confirms
the local mechanics before moving to Torch.

## Expected Resources

PySpark transforms:

- Two jobs: ANOVA LOSO and PCA LOSO.
- Resources: 12 CPU, 56 GB RAM each.
- Time estimate: 2-8 hours each; 65 folds is slightly more than the 50-fold P=6
  transforms, but each test split is smaller.

Fixed LOSO model evaluations:

- Eight evaluations: two feature roots times four model families.
- Resources: 12 CPU, 56 GB RAM each.
- Time estimate: KNN/SVM likely under 1 hour once transformed data exists;
  XGBoost/MLP likely 1-4 hours depending on fold size and convergence. Run in
  parallel if cluster load allows.

## Torch Paths

Planned transformed roots:

- `/scratch/ans9868/rebuttal-deep-eeg-full-pipeline/eeg-full-pipeline/data/LOSO_ANOVA_ad_cntrl_65fold_v1`
- `/scratch/ans9868/rebuttal-deep-eeg-full-pipeline/eeg-full-pipeline/data/LOSO_PCA_ad_cntrl_65fold_v1`

Planned LOSO output root:

- `/scratch/ans9868/rebuttal-deep-eeg-full-pipeline/eeg-full-pipeline/rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn/outputs/fixed_loso_classical_2026-07-26`
