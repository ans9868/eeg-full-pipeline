# Deep Learning WC AD/Cntrl Seed 42 Config

Created `DL_W_C_ad_cntrl_seed42_hpc.yaml` as a raw-waveform deep-learning version of the existing HPC `ANOVA_W_C_ad_cntrl_seed42.yaml` disease-prediction config.

Key points:

- Uses the same HPC AD/Cntrl subject paths from `/scratch/ans9868/ds004504-download`.
- Keeps seed `42` and the WC within-subject 80/20 strategy metadata.
- Switches PySpark output to `feature_extraction.output_format: raw-waveform`.
- Disables feature transformations because the deep-learning handoff reads raw waveform epochs from `processed_subjects`.
- Adds `deep_learning_smoke.source: raw-waveform`.
- Uses `downsampling: 64`, `window_size: 3.0`, and `sliding_window: 0.5`.
- Sets `max_rows: 1000000` to avoid the current launcher converting a YAML null into `--max-rows None`.

Validation:

```bash
python3 config_handler.py rebuttal/hpc_activities/eegnet_deep_learning_baseline/yaml_plan/DL_W_C_ad_cntrl_seed42_hpc.yaml
```

Result: passed.

Launcher command sanity:

- PySpark selects the normal Spark pipeline command.
- Ray selects `python -m eeg_ray_tuner.deep_learning_smoke.training` with `--processed-subjects /app/data/DL_W_C_ad_cntrl_seed42_hpc/processed_subjects`.

Note: the current deep-learning runner emits both `subject_disjoint_smoke` and `subject_overlap_smoke` outputs. For this WC-style config, the overlap output is the closest current deep-learning diagnostic to the within-subject disease-prediction setup.

TODO for rebuttal-grade neural baselines:

- Replace the current lightweight EEGNet-style smoke model with a canonical EEGNet implementation.
- Keep a separate slot for a Transformer / BIOT-style EEG baseline rather than treating the current tiny transformer smoke model as final.
- Split future configs/results clearly by model family so EEGNet and Transformer/BIOT can each have their own validated HPC run and output folder.
