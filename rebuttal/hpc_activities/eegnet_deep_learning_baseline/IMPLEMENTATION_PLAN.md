# Neural Baseline Implementation Plan

## Checkpoint Rule

- [ ] Stop and ping the user after local implementation and local laptop sanity test pass.
- [ ] Do not rebuild/run on HPC before the user checkpoint.

## Phase 0: Planning And Context

- [x] Lock model choices.
  - `canonical_eegnet`
  - `eeg_conformer_small`
- [x] Record why BIOT is not the first transformer-family choice.
- [x] Create living context file.
- [x] Create checkbox implementation plan.
- [ ] Update this plan whenever tasks are added, removed, completed, or marked not needed.

## Phase 1: Inspect Available Model Options

- [ ] Check whether Braindecode is already installed locally in `py-neuro-env`.
- [ ] Check whether Braindecode is already present in the Ray Docker/Singularity dependency stack.
- [ ] Inspect Braindecode model names and constructor signatures for:
  - [ ] EEGNet
  - [ ] EEGConformer or equivalent Conformer model
- [ ] Decide whether to use Braindecode directly or implement small in-repo PyTorch versions.
- [ ] Record decision in `CONTEXT.md`.

## Phase 2: Model Code

- [ ] Add `canonical_eegnet` model builder.
- [ ] Add `eeg_conformer_small` model builder.
- [ ] Keep existing smoke model builders available as debug paths.
- [ ] Ensure models accept raw waveform tensors shaped like:
  - local: `4 x 193`
  - HPC: `19 x 193`
- [ ] Ensure binary classification output shape is `[batch, 2]`.
- [ ] Add clear model metadata to training logs.

## Phase 3: Config Selection

- [ ] Add config support for selecting model list, for example:

```yaml
deep_learning_smoke:
  models:
  - canonical_eegnet
  - eeg_conformer_small
```

- [ ] Support EEGNet-only local/HPC runs.
- [ ] Support Conformer-only local/HPC runs.
- [ ] Support running both.
- [ ] Preserve backward compatibility if `models` is omitted.
- [ ] Keep output model names explicit in metrics and filenames.

## Phase 4: Training Loop Integration

- [ ] Wire `canonical_eegnet` into the existing raw-waveform training path.
- [ ] Wire `eeg_conformer_small` into the existing raw-waveform training path.
- [ ] Preserve early stopping behavior.
- [ ] Preserve validation split behavior.
- [ ] Preserve subject-disjoint and subject-overlap diagnostics.
- [ ] Confirm test metrics are not used for early stopping.

## Phase 5: Local Laptop Sanity

- [ ] Update or create laptop config for tiny model sanity.
- [ ] Use bundled `.set` files.
- [ ] Use tiny settings:
  - `max_rows: 256`
  - `epochs: 2`
  - small batch size
- [ ] Run local compile checks.
- [ ] Rebuild Ray Docker image if dependencies/code require it.
- [ ] Run:

```bash
python3 start-pipelines.py deep_learning_test_laptop.yaml
```

- [ ] Verify both selected models instantiate.
- [ ] Verify both selected models train for at least one epoch.
- [ ] Verify `summary_metrics.csv` exists.
- [ ] Verify predictions/log files exist.
- [ ] Verify split sentinels:
  - subject-disjoint shared subjects = `0`
  - subject-overlap shared subjects > `0`
- [ ] Update `CONTEXT.md` with local result summary.

## Phase 6: User Checkpoint Before HPC

- [ ] Ping user before any HPC rebuild/run.
- [ ] Include changed files.
- [ ] Include local test result.
- [ ] Include commit hashes.
- [ ] Include proposed HPC commands.
- [ ] Include risks/odd behavior.
- [ ] Wait for user confirmation before proceeding to HPC.

## Phase 7: Commit And Push

- [ ] Commit Ray model/training changes.
- [ ] Commit root config/context/plan changes.
- [ ] Push submodule repos first.
- [ ] Push root repo after submodule pointers are updated.
- [ ] Confirm GitHub `main` matches local for:
  - PySpark
  - Ray
  - root

## Phase 8: HPC Container Refresh

- [ ] Rebuild/update PySpark SIF if needed.
- [ ] Rebuild/update Ray SIF with new model/dependency code.
- [ ] Verify PySpark SIF contains raw-waveform branch:

```bash
singularity exec containers/eeg-pyspark-pipeline.sif \
  grep -n "raw-waveform" /app/eeg_spark_etl/processing/process_epoch.py
```

- [ ] Verify Ray SIF contains new model names:

```bash
singularity exec containers/eeg-ray-tuner.sif \
  grep -R "canonical_eegnet\|eeg_conformer_small" -n /app/eeg_ray_tuner
```

## Phase 9: HPC Smoke Sanity

- [ ] Create or update HPC smoke config.
- [ ] Use limited settings:
  - small `max_rows`
  - `epochs: 2-3`
- [ ] Run canonical EEGNet smoke.
- [ ] Run EEG Conformer small smoke.
- [ ] Verify output files.
- [ ] Verify row counts and subject counts.
- [ ] Verify split sentinels.
- [ ] Update `CONTEXT.md`.

## Phase 10: Full HPC Rebuttal Runs

- [ ] Run canonical EEGNet full AD/Cntrl WC seed 42.
- [ ] Run EEG Conformer small full AD/Cntrl WC seed 42.
- [ ] Preserve both diagnostic outputs:
  - subject-disjoint
  - subject-overlap/WC
- [ ] Check:
  - row counts
  - subject counts
  - group counts
  - training logs
  - early stopping behavior
  - split integrity
- [ ] Decide whether to repeat across more seeds/conditions.

## Phase 11: Result Interpretation

- [ ] Compare disjoint vs overlap/WC performance.
- [ ] Mark results as rebuttal-grade only after integrity checks pass.
- [ ] Draft cautious language:
  - canonical neural baselines tested
  - overlap/WC vs subject-disjoint contrast
  - implications for fingerprint/leakage concern

## Not Needed For First Pass

- [ ] BIOT full implementation.
- [ ] Large pretrained foundation model loading.
- [ ] Hyperparameter tuning.
- [ ] Multi-GPU training.
