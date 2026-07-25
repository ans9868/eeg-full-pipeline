# Deep Learning Local Smoke Test Dev Note

Created 2026-07-25.

## Scope

Implemented `rebuttal/deep_learning_local_smoke_test/` as a laptop-safe engineering smoke test for EEGNet-style and transformer-style neural model code paths over existing processed EEG feature parquet artifacts.

This is not a final rebuttal/HPC neural baseline result. It only validates data loading, split construction, forward passes, training loops, metrics, leakage checks, and local output schemas.

## Local Savepoints

- Pre-edit savepoint commit: `0b867d4` (`Savepoint before local deep learning smoke test`).
- Initial implementation commit: `3016944` (`Add local deep learning smoke test activity`).

## Environment

- `py-neuro-env` is available as an interactive zsh alias: `source ~/py-neuro-env/bin/activate`.
- Local checks were run through `zsh -lic 'py-neuro-env && ...'`.
- Needed local packages were already present: NumPy, pandas, pyarrow, PyTorch, and sklearn.
- No container files or dependency manifests were changed. No `make build` container rebuild was needed.

## Bugs Found And Fixed

- Initial tiny subset used the first `--max-rows` rows after reading parquet files, which could be single-class because the sorted parquet order is subject/class clustered. Fixed by sampling a deterministic class-balanced subset after reading enough data.
- The first balanced subset had both labels but only three subjects, which made the subject-disjoint holdout leave a single-class training set. Fixed by reading until each class has at least two subjects and sampling across subjects within each class.

## Successful Local Run

`bash rebuttal/deep_learning_local_smoke_test/scripts/run_all_deep_learning_smoke_tests.sh` completed inside `py-neuro-env`.

Smoke data:

- Source: `ANOVA_L_2_ad_cntrl_random50/processed_subjects`
- Rows: 512
- Unique subjects: 4
- Class counts: 256 / 256
- Feature dimension: 95

Integrity checks:

- Subject-disjoint runs reported zero shared train/test subjects.
- Subject-overlap runs reported four shared train/test subjects.
- All metrics were finite.
- `report.md` and `outputs/summary_metrics.csv` were refreshed locally.
