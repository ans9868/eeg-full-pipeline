# Neural Subject Fingerprinting Plan - 2026-07-26

## Goal

Run a raw-waveform neural subject-recognition experiment that mirrors the existing 65-subject fingerprinting design:

- Task: 65-way `SubjectID` prediction.
- Split: within-subject W/C 80/20 random train/test split, seed 42 first.
- Inputs: same AD/CN raw EEG epochs used for the rebuttal neural disease runs, 3 s windows, 0.5 s stride, 64 Hz downsampling.
- Models: `canonical_eegnet` first, `eeg_conformer_small` also included if the same run remains stable.
- Primary metric: top-1 accuracy against 65-way chance, 1/65 = 1.54%.
- Prediction rows must include true/predicted subject IDs so top-k or error audits can be derived later without rerunning.

## Why Code Is Needed

The current raw-waveform deep-learning runner is binary-only:

- `common.py` encodes only the `label` column and rejects non-binary labels.
- `models.py` hardcodes two output logits.
- `training.py` computes binary metrics and writes only `prob_class_1`.
- `start-pipelines.py` does not expose a YAML key for `label_column` or one-split-only execution.

Therefore this is not a YAML-only change. The minimal correct patch is to make the runner multiclass-capable while keeping binary disease classification unchanged by default.
This also covers the existing fingerprinting convention where PySpark may hot-encode `SubjectID` into the generic `label` column for `ML Fingerprinting`: Ray now accepts multiclass labels whether they come from explicit `SubjectID` or from pre-encoded `label`.

## Checklist

- [x] Confirm YAML-only is not sufficient because the neural runner is binary-only.
- [x] Add multiclass label encoding with binary default preserved.
- [x] Add `label_column` support for raw processed-subject waveform loading.
- [x] Confirm raw-waveform rows include `SubjectID`, `Group`, `waveform`, and `label`.
- [x] Confirm Ray accepts multiclass subject labels already stored in the `label` column.
- [x] Add configurable neural output size for EEGNet/Conformer/smoke model heads.
- [x] Add multiclass top-1 metrics and mapped `true_class`/`pred_class` prediction output.
- [x] Add `--label-column` CLI support.
- [x] Add `--splits` CLI support so subject-ID can run W/C only.
- [x] Add YAML bridge for `deep_learning_smoke.label_column` and `deep_learning_smoke.splits`.
- [x] Run local syntax checks.
- [x] Run local binary-regression loader check on synthetic raw-waveform parquet.
- [x] Run local multiclass synthetic parquet loader/split check for `label_column=SubjectID`.
- [x] Add seed-42 neural fingerprinting YAML.
- [x] Validate generated container command includes `--label-column SubjectID` and `--splits subject_overlap_smoke`.
- [x] Run local one-epoch multiclass neural training check in local `rayenv`.
- [ ] Run Torch-side one-epoch multiclass neural training check before submitting the full job.
- [ ] Push to origin for rebuilding the HPC image/SIF.
- [ ] Build updated image/SIF on Torch.
- [ ] Submit seed-42 full-design neural subject-recognition run.
- [ ] Summarize neural top-1 accuracy versus 1.54% chance.
- [ ] Add final results and evidence paths to rebuttal drafts.

## Minimal Run

Minimum reviewer-response run:

- One seed: 42.
- Split: W/C 80/20 only.
- Model: `canonical_eegnet`.
- Epochs: 25 with validation-loss early stopping, matching the prior neural rebuttal runs.
- Resources: CPU `cs` or `cpu_short`, 12 CPUs, 56 GB RAM, no GPU.
- Expected wall time: roughly 1 to 2.5 hours if preprocessing is reused or fast; longer if PySpark has to regenerate raw-waveform epochs.

This is enough to say whether raw-waveform EEGNet can perform subject recognition under the same within-subject fingerprinting design.

## Preferred Run

Preferred single-seed run:

- Seed: 42.
- Split: W/C 80/20 only.
- Models: `canonical_eegnet,eeg_conformer_small`.
- Epochs: 25 with early stopping.
- Resources: CPU `cs`, 12 CPUs, 56 GB RAM, no GPU.
- Expected Ray training wall time: roughly 2 to 3 hours for both models, based on the completed disease W/C seed sweep taking 2:16:49 for 10 seeds x 2 models once data existed.
- Expected end-to-end wall time: same-day if raw-waveform processed subjects are reused; add preprocessing time if not.

## Interpretation Plan

Compare neural top-1 subject-ID accuracy to:

- Chance: 1.54%.
- Existing handcrafted-feature fingerprinting:
  - PCA + MLP: 98.11%.
  - ANOVA + XGBoost: 97.61%.

Possible outcomes:

- High neural subject-ID accuracy supports the reviewer-response point that EEG contains strong subject fingerprints, consistent with the feature-based fingerprinting results.
- Lower neural subject-ID accuracy would not refute fingerprinting, but would say these compact raw-waveform neural baselines are not as tuned for subject recognition as the handcrafted-feature models.

## Evidence Locations

Existing local evidence:

- `rebuttal/subject_recognition_fingerprinting/report.md`
- `rebuttal/subject_recognition_fingerprinting/subject_recognition_summary.csv`

Planned neural output location:

- Local YAML: `rebuttal/hpc_activities/eegnet_deep_learning_baseline/yaml_plan/DL_W_F_subjectid_seed42_hpc.yaml`
- HPC output: `/scratch/ans9868/rebuttal-deep-eeg-full-pipeline/eeg-full-pipeline/data/DL_W_F_subjectid_seed42_hpc/deep_learning_smoke_outputs/`
- Key files: `summary_metrics.csv`, `*_metrics.csv`, `*_predictions.csv`, `*_training_log.json`
