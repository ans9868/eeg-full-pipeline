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

## Local Dependency Inspection

Initial local inspection in `py-neuro-env` found:

- `torch`: installed, version `2.8.0`
- `braindecode`: not installed
- `torcheeg`: not installed

The Ray Docker requirements did not initially include Braindecode. The first fast local implementation used small in-repo PyTorch builders, but the final reviewer-facing decision is to use direct Braindecode implementations instead.

Braindecode local install/check:

- `braindecode==1.2.0`
- local `torch==2.8.0`
- local `torchaudio` initially mismatched at `2.11.0`
- aligned local `torchaudio==2.8.0`

Direct Braindecode fake tensor checks passed:

- `EEGNet`, input `2 x 4 x 193`, output `2 x 2`
- `EEGNet`, input `2 x 19 x 193`, output `2 x 2`
- `EEGConformer`, input `2 x 4 x 193`, output `2 x 2`
- `EEGConformer`, input `2 x 19 x 193`, output `2 x 2`

Ray now keeps the same config names but backs them with Braindecode:

- `canonical_eegnet` -> `braindecode.models.EEGNet`
- `eeg_conformer_small` -> `braindecode.models.EEGConformer`

Ray Docker dependency notes:

- Added `braindecode==1.2.0`
- Added `torchaudio==2.8.0` to match `torch==2.8.0`
- Regenerated `requirements/docker.txt` with `uv pip compile --python-version 3.10`
- The explicit Python 3.10 compile matters because `mne-bids==0.19.0` requires Python 3.11; the Python 3.10-compatible lock uses `mne-bids==0.17.0`

## Known Risks

- Braindecode dependency may bring extra packages or version conflicts.
- Model constructors may expect different input shape conventions.
- Local laptop test data has 4 channels, while HPC data has 19 channels.
- Conformer may require input time length/channel count constraints.
- HPC SIFs must be rebuilt after code/dependency changes.
- Current launcher always passes `--max-rows`; avoid YAML null unless launcher is fixed.

## Local Canonical Model Sanity Result

Initial in-repo PyTorch builders were implemented for:

- `canonical_eegnet`
- `eeg_conformer_small`

Local direct trainer check passed with existing laptop raw-waveform `processed_subjects`:

```bash
PYTHONPATH=eeg-ray-tuner:$PYTHONPATH python3 -m eeg_ray_tuner.deep_learning_smoke.training \
  --processed-subjects data/deep_learning_test_laptop/processed_subjects \
  --output-dir /tmp/canonical_neural_local_check \
  --max-rows 256 \
  --epochs 2 \
  --models canonical_eegnet,eeg_conformer_small
```

Full Docker laptop run also passed:

```bash
python3 start-pipelines.py deep_learning_test_laptop.yaml
```

Summary from `data/deep_learning_test_laptop/deep_learning_smoke_outputs/summary_metrics.csv`:

- `canonical_eegnet_subject_disjoint_smoke`: balanced accuracy `0.500`
- `canonical_eegnet_subject_overlap_smoke`: balanced accuracy `0.786`
- `eeg_conformer_small_subject_disjoint_smoke`: balanced accuracy `0.014`
- `eeg_conformer_small_subject_overlap_smoke`: balanced accuracy `0.857`

The purpose of this run was only model/launcher sanity. Both models instantiated, trained for two epochs, wrote metrics/predictions/training logs, and preserved split sentinels.

## Local Braindecode Container Sanity Result

Replaced the final baseline builders with direct Braindecode models and rebuilt the local Ray Docker image:

```bash
make build
```

The first build attempt failed because the generated lock selected `mne-bids==0.19.0`, which is Python 3.11-only. Regenerating for Python 3.10 selected `mne-bids==0.17.0`, and the image then built successfully.

Container import and fake tensor checks passed:

- `braindecode 1.2.0`
- `torch 2.8.0+cpu`
- `torchaudio 2.8.0`
- both models accepted `4 x 193` and `19 x 193` raw waveform inputs

Full local Docker launcher passed:

```bash
python3 start-pipelines.py config/deep_learning_test_laptop.yaml
```

The run processed 4 bundled `.set` test files, wrote raw-waveform `processed_subjects`, then trained both Braindecode-backed models for 2 epochs. Training logs confirm:

- `canonical_eegnet`: `braindecode.models.EEGNet`
- `eeg_conformer_small`: `braindecode.models.EEGConformer`

Summary metrics were written to:

```text
data/deep_learning_test_laptop/deep_learning_smoke_outputs/summary_metrics.csv
```

Split sentinels remained valid:

- subject-disjoint shared subjects: `0`
- subject-overlap shared subjects: `4`
