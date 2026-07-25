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

Added `config/deep_learning_test_laptop.yaml` as the human-facing laptop Docker smoke config.

The first version intentionally used an existing processed-feature parquet fixture. After review, that was replaced with a config-faithful raw EEG path: the YAML now lists subjects explicitly under `data_input.groups`, controls `window_size`, `sliding_window`, `downsampling`, annotation rejection, and epoch rejection through the normal preprocessing section, and sets `feature_extraction.output_format: raw-waveform`.

Minimal Spark changes:

- Added `raw-waveform` as a valid output format.
- Added a raw-waveform processed-subject schema.
- Added a narrow `process_epoch` branch that returns `epoch.get_data()[0]` as flattened channel-major waveform samples with `n_channels`, `n_times`, `sfreq`, and `channel_names`.
- Added use of the existing `preprocessing.downsampling` setting before epoch construction.
- Skipped feature transformations only after raw-waveform processed subjects are saved.

Ray changes:

- Added a deep-learning reader for raw-waveform `processed_subjects` parquet.
- Reconstructs waveform rows to `(samples, channels, time)` tensors.
- Uses raw-waveform EEGNet-style and transformer-style smoke models when the input is 3D.

Verified with:

```bash
python3 start-pipelines.py deep_learning_test_laptop.yaml
```

The final raw-waveform Docker run completed both stages successfully. PySpark loaded the four bundled `.set` files, downsampled 256 Hz to 64 Hz, made 35 epochs per subject with `window_size: 3.0` and `sliding_window: 0.5`, saved `data/deep_learning_test_laptop/processed_subjects`, and skipped transformations. A schema check confirmed waveform rows with columns `SubjectID`, `EpochID`, `Group`, `waveform`, `n_channels`, `n_times`, `sfreq`, `channel_names`, and `label`; a sampled row had shape `4 x 193`, flattened length `772`, `sfreq=64.0`, and finite values.

Ray read directly from `data/deep_learning_test_laptop/processed_subjects`, wrote `_raw_waveform_smoke_data.npz`, and ran EEGNet-style and transformer-style smoke training. Results were written to `data/deep_learning_test_laptop/deep_learning_smoke_outputs/summary_metrics.csv`. The expected leakage sentinels were preserved: zero shared subjects for subject-disjoint runs and four shared subjects for subject-overlap runs.

Added early stopping support in the Ray deep-learning smoke trainer. The YAML now supports `validation_split` plus an `early_stopping` block with `enabled`, `monitor`, `mode`, `patience`, `min_delta`, and `restore_best_weights`. Validation rows are split only from the training partition after the smoke train/test subject split, so held-out test rows are not used for stopping decisions. The summary metrics now include requested max epochs, epochs actually run, whether early stopping fired, best epoch, best validation metric, validation loss, validation accuracy, and validation row count.

Verified the updated `deep_learning_test_laptop.yaml` through `python3 start-pipelines.py deep_learning_test_laptop.yaml` after rebuilding the local Ray container. The Docker run completed end to end and wrote early-stopping metrics for all four smoke runs; none stopped early on this seed-42 laptop data because the monitored validation loss kept improving before the 10-epoch cap.

Also ran a direct trainer check with an intentionally large `early_stopping.min_delta` to force the stop branch. All four smoke runs stopped at 2 of 5 requested epochs with `early_stopped: true`, confirming the autostop path fires and reports `epochs_ran` correctly.

## Non-Deep-Learning Full-Pipeline Sanity

Added `config/config_testanova1_seed42_testdata_smoke.yaml` by copying the shape of `config/config_testanova1_09-10-2025_1727.yaml` and pointing it at the bundled PySpark test EEG files. This keeps the run full end-to-end through Docker while avoiding unavailable raw-data paths. The config uses seed 42, the ANOVA F-test plus MinMax transformation path, a within-subject split, and a single small KNN grid point for laptop-safe Ray execution.

First full Docker attempt reached PySpark subject processing and mounted all four test files successfully, but the copied config's epoch rejection settings dropped every epoch in the tiny test fixture. For this smoke config only, epoch rejection was disabled so the fixture produces rows for the ANOVA transform and downstream Ray stage.

Successful full Docker run:

```bash
python3 start-pipelines.py config/config_testanova1_seed42_testdata_smoke.yaml
```

PySpark processed all four bundled test `.set` files, created 18 epochs per subject, saved processed subjects, fit ANOVA on 56 training rows, selected 2 of 12 features, applied MinMax scaling, and saved the within-subject train/test transformed data. Ray then discovered the transformed fold and completed the single KNN grid-search task successfully. Results were written under `data/testAnova1Seed42TestDataSmoke/ml_results_grid_search`; `model_comparison.csv` reported KNN test accuracy `0.8125` and train accuracy `0.9285714285714286`.
