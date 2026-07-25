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

## Pipeline Integration

Added pipeline-owned entrypoints after the initial standalone rebuttal smoke activity passed:

- PySpark pipeline: `eeg_spark_etl.utils.deep_learning_smoke_export`
- Ray pipeline: `eeg_ray_tuner.deep_learning_smoke.training`
- Root orchestrator: `start-pipelines.py` now recognizes a `deep_learning_smoke` YAML section.

Small YAML configs were added under `config/`:

- `config/config_deep_learning_smoke_local.yaml`
- `config/config_deep_learning_smoke_docker.yaml`

Final local orchestrator test passed:

```bash
py-neuro-env
python3 start-pipelines.py config/config_deep_learning_smoke_local.yaml
```

This produced the same engineering smoke result shape through the root launcher: 512 rows, 4 subjects, two classes, zero shared subjects for subject-disjoint splits, four shared subjects for subject-overlap splits, and finite metrics for EEGNet-style and transformer-style smoke models.

Container updates:

- Rebuilt PySpark image locally with `cd eeg-pyspark-pipeline && make build`; produced `eeg-spark-pipeline:latest`.
- Rebuilt Ray image locally with `cd eeg-ray-tuner && make build`; produced `eeg-ray-tuner:latest`.
- No Docker Hub push was run.

Final Docker orchestrator test passed:

```bash
python3 start-pipelines.py config/config_deep_learning_smoke_docker.yaml
```

The Docker smoke test wrote `rebuttal/deep_learning_local_smoke_test/outputs/pipeline_docker/summary_metrics.csv` with four runs. Integrity checks confirmed zero shared subjects for subject-disjoint runs and four shared subjects for subject-overlap runs.
