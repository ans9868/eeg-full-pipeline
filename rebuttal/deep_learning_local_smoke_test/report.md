# Deep Learning Local Smoke Test Report

These local runs validate that the EEGNet-style and transformer-style neural model code paths execute end-to-end on the existing processed EEG feature artifacts. They are smoke tests, not final rebuttal-grade neural baseline results. Rebuttal claims about neural architectures should use only full-scale HPC/GPU runs with the intended data and split definitions.

Last refreshed: 2026-07-25T03:28:24

## Data

- source: `ANOVA_L_2_ad_cntrl_random50/processed_subjects`
- rows: `512`
- unique_subjects: `4`
- class_counts: `{'0.0': 256, '1.0': 256}`
- feature_dim: `95`
- label_mapping: `{'0.0': 0, '1.0': 1}`

## Runs

- eegnet_feature_smoke_subject_disjoint_smoke: split `subject_disjoint_smoke`, rows train/test `256/256`, subjects train/test `2/2`, shared subjects `0`, accuracy `0.5`, balanced accuracy `0.5`, sensitivity `1.0`, specificity `0.0`
- eegnet_feature_smoke_subject_overlap_smoke: split `subject_overlap_smoke`, rows train/test `410/102`, subjects train/test `4/4`, shared subjects `4`, accuracy `0.49019607843137253`, balanced accuracy `0.49019607843137253`, sensitivity `0.9803921568627451`, specificity `0.0`
- transformer_feature_smoke_subject_disjoint_smoke: split `subject_disjoint_smoke`, rows train/test `256/256`, subjects train/test `2/2`, shared subjects `0`, accuracy `0.62109375`, balanced accuracy `0.62109375`, sensitivity `0.4375`, specificity `0.8046875`
- transformer_feature_smoke_subject_overlap_smoke: split `subject_overlap_smoke`, rows train/test `410/102`, subjects train/test `4/4`, shared subjects `4`, accuracy `0.696078431372549`, balanced accuracy `0.696078431372549`, sensitivity `0.5294117647058824`, specificity `0.8627450980392157`

## Integrity Checks

- `subject_disjoint_smoke` is required to report zero shared train/test subjects.
- `subject_overlap_smoke` is required to report at least one shared train/test subject and is the deliberately leaked control.
- Metrics are engineering checks only; poor accuracy is acceptable for this local 1-2 epoch run when values are finite and outputs are written.

## Container Notes

Pipeline-owned smoke entrypoints were later added to `eeg-pyspark-pipeline/`, `eeg-ray-tuner/`, and `start-pipelines.py`. The local root-orchestrator smoke config completed successfully with:

```bash
python3 start-pipelines.py config/config_deep_learning_smoke_local.yaml
```

Because containerized execution code changed, the PySpark and Ray Docker images should be rebuilt locally with each subproject Makefile before Docker/Singularity smoke execution. No Docker Hub push is needed for this local validation.
