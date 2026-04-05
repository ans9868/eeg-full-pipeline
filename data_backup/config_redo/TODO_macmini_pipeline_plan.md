# Mac Mini Pipeline TODO

Scope: planning only. No code edits yet.

## Must Do (Certain)

- [ ] Add batch processing to subject ingestion in `eeg-pyspark-pipeline/eeg_spark_etl/processing/process_subjects.py`.
- [ ] Goal: avoid loading/processing all EEG files at once, which causes memory crashes on Mac mini.
- [ ] Implement one of these approaches (or both):
  - [ ] Config-driven batching (e.g., `batch_size_subjects`, optional order policy in YAML).
  - [ ] Dynamic batching (auto-compute batches using file sizes and available memory).
- [ ] Include a smart ingestion order policy (largest-first, smallest-first, or balanced packing) and document the choice.
- [ ] Persist intermediate batch outputs safely so failed runs can resume from the last completed batch.

## Maybe 1

- [ ] Replace "one config per split version" workflow with a single orchestrated run for all versions (similar to LPSO-style looping).
- [ ] Idea: one driver config + a list of split versions, then iterate in PySpark/Ray with shared orchestration.
- [ ] Expected benefit: fewer manual reruns, fewer config handling errors, and easier reproducibility.

## Maybe 2

- [ ] Decide whether batching policy should live in config by default or be fully automatic with runtime heuristics.
- [ ] Option A: explicit config knobs (predictable/reproducible).
- [ ] Option B: dynamic memory-aware planner (simpler for users, more adaptive).
- [ ] Potential compromise: dynamic default with optional config overrides.

## Validation Checklist (When We Start Implementation)

- [ ] Confirm no OOM with full 65-subject classification runs on Mac mini.
- [ ] Verify labels remain correct (`ML Classification` => binary group labels).
- [ ] Verify transformed and ML outputs are identical (or explainably close) vs non-batched baseline.
- [ ] Verify resume/recovery behavior after interrupting mid-run.

