# Neural Baseline Context

## Current Goal

Add two rebuttal-grade, raw-waveform neural baselines to the EEG full pipeline:

- `canonical_eegnet`
- `eeg_conformer_small`

These replace the current lightweight smoke approximations for final rebuttal use. The existing smoke models remain useful only for debugging and pipeline sanity checks.

## User Checkpoint Requirement

Stop and ping the user after local implementation and local laptop sanity testing are complete, before any HPC rebuild or HPC run.

The checkpoint should include:

- changed files
- local test command and result
- commits involved
- exact proposed HPC commands
- any risks or odd behavior

Do not proceed directly to HPC execution before that checkpoint.

## Current Pipeline State

Raw-waveform PySpark support exists in the repo:

- PySpark commit: `c31cf4c Add raw waveform deep learning output`
- Expected code path: `eeg_spark_etl/processing/process_epoch.py`
- Expected branch: `if output_format == "raw-waveform":`

Ray raw-waveform deep-learning support exists in the repo:

- Ray commit: `f87d72a Add early stopping to deep learning smoke trainer`
- Entry point: `python -m eeg_ray_tuner.deep_learning_smoke.training`

Root config/orchestration support exists:

- Root config: `rebuttal/hpc_activities/eegnet_deep_learning_baseline/yaml_plan/DL_W_C_ad_cntrl_seed42_hpc.yaml`
- Root launcher chooses the deep-learning Ray command when `deep_learning_smoke.source: raw-waveform`.

## Important HPC Finding

The HPC `containers/eeg-pyspark-pipeline.sif` inspected on Torch was stale. Inside the SIF, `process_epoch.py` did not contain the raw-waveform early-return branch and only checked `output_format == "ml"` after PSD/frequency-band logic.

This explains the earlier HPC warning:

```text
No frequency bands found in config. Please add 'bands' section to 'preprocessing' config.
```

That warning is not harmless if the stale container is used; it means epochs fail before raw-waveform rows are emitted.

## First HPC Smoke Result

The later completed HPC run produced raw-waveform output:

- rows: `34,397`
- subjects: `65`
- groups: `alz=18,822`, `cntrl=15,575`
- sample shape: `19 x 193`
- sampling rate: `64.0`

The current smoke approximation showed the expected diagnostic pattern:

- EEGNet-style subject-disjoint balanced accuracy: about `0.445`
- EEGNet-style subject-overlap/WC balanced accuracy: about `0.954`
- Transformer-style subject-disjoint balanced accuracy: about `0.462`
- Transformer-style subject-overlap/WC balanced accuracy: about `0.982`

Interpretation: this supports the overlap/fingerprint diagnostic pattern, but it is not final rebuttal-grade neural evidence because the models are smoke approximations.

## Locked Model Choices

Use two simple, fast, justifiable models:

1. `canonical_eegnet`
   - canonical EEGNet architecture for raw EEG
   - preferred first neural baseline
   - should be lightweight and fast

2. `eeg_conformer_small`
   - small EEG Conformer-style transformer-family baseline
   - chosen over BIOT for simplicity/speed
   - should be directly EEG-classification oriented

BIOT is a possible future candidate but is not the first pick because it is likely heavier and more dependency/shape-sensitive.

## Implementation Preferences

- Prefer reliable library-backed models if dependency footprint is acceptable.
- Braindecode is the leading candidate because it provides EEG-specific models.
- Keep model names explicit in config and outputs.
- Keep old smoke models available but clearly label them as smoke/debug.
- Keep local tests tiny.
- Preserve split diagnostics:
  - `subject_disjoint_smoke`
  - `subject_overlap_smoke`

## Known Risks

- Braindecode dependency may bring extra packages or version conflicts.
- Model constructors may expect different input shape conventions.
- Local laptop test data has 4 channels, while HPC data has 19 channels.
- Conformer may require input time length/channel count constraints.
- HPC SIFs must be rebuilt after code/dependency changes.
- Current launcher always passes `--max-rows`; avoid YAML null unless launcher is fixed.
