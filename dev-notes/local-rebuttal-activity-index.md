# Local Rebuttal Activity Index

Created 2026-07-25.

This note indexes the local-only reproducibility package in `rebuttal/`.
No generated scripts or outputs for this package should live outside `dev-notes/`
and `rebuttal/`.

## Activity folders

| Folder | Purpose |
|---|---|
| `rebuttal/balanced_accuracy_confusion_matrices/` | Subject-level clinical metrics and confusion matrices. |
| `rebuttal/fingerprinting_best_accuracy/` | Best 65-way fingerprinting accuracy and chance-level check. |
| `rebuttal/subject_recognition_fingerprinting/` | Mechanism-control framing for subject identity decodability. |
| `rebuttal/literature_audit_counts/` | Counts and percentages from the literature audit trap coding. |
| `rebuttal/deep_learning_local_smoke_test/` | Local laptop smoke test for EEGNet-style and transformer-style feature-vector neural code paths; engineering validation only, not final rebuttal results. |
| `rebuttal/trap2_fold_variance_iqr/` | Held-out cohort size sensitivity and fold variance summaries. |
| `rebuttal/trap3_rank_mismatch/` | Epoch-vs-subject model ranking mismatch. |
| `rebuttal/trap3_spearman_rho/` | Spearman correlation between epoch and subject ranking metrics. |

## Canonical context

Read `dev-notes/context-for-analysis.md` first. It records source paths,
known caveats, and the split between local activities and HPC-only reruns.
