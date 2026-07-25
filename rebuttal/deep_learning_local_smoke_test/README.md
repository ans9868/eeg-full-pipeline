# Deep Learning Local Smoke Test

This activity is a local engineering smoke test for neural EEG baselines. It is not the final rebuttal/HPC experiment unless rerun at full scale with the intended data, split manifests, and GPU/HPC settings.

The scripts validate the data loader, split logic, leakage checks, model forward passes, training loop, metric calculation, and output schema for:

- `eegnet_feature_smoke`: a compact EEGNet-inspired convolutional model over existing feature vectors.
- `transformer_feature_smoke`: a small transformer encoder classifier over fixed-size feature chunks.

The feature-vector EEGNet path is deliberately labeled as a smoke test, not canonical raw-signal EEGNet. Rebuttal claims about neural architectures should use only full HPC/GPU runs after those runs complete and pass integrity checks.

## Local Commands

Run commands from the repository root after activating the local environment:

```bash
py-neuro-env

python3 rebuttal/deep_learning_local_smoke_test/scripts/prepare_deep_learning_smoke_data.py \
  --input-dir ANOVA_L_2_ad_cntrl_random50/processed_subjects \
  --output rebuttal/deep_learning_local_smoke_test/outputs/anova_l2_tiny_smoke_data.npz \
  --max-rows 512

python3 rebuttal/deep_learning_local_smoke_test/scripts/train_eegnet_smoke.py \
  --data rebuttal/deep_learning_local_smoke_test/outputs/anova_l2_tiny_smoke_data.npz \
  --split subject_disjoint_smoke \
  --epochs 1 \
  --batch-size 32

python3 rebuttal/deep_learning_local_smoke_test/scripts/train_transformer_smoke.py \
  --data rebuttal/deep_learning_local_smoke_test/outputs/anova_l2_tiny_smoke_data.npz \
  --split subject_overlap_smoke \
  --epochs 1 \
  --batch-size 32
```

Then run all four model/split smoke checks:

```bash
bash rebuttal/deep_learning_local_smoke_test/scripts/run_all_deep_learning_smoke_tests.sh
```

Expected outputs are written under `outputs/`:

- `<run_id>_metrics.csv`
- `<run_id>_predictions.csv`
- `<run_id>_split_subjects.json`
- `<run_id>_training_log.json`
- `summary_metrics.csv`

`report.md` is refreshed after completed model runs.
