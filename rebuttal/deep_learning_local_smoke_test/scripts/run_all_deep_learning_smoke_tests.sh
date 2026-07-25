#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "${ROOT_DIR}"

DATA="rebuttal/deep_learning_local_smoke_test/outputs/anova_l2_tiny_smoke_data.npz"

python3 rebuttal/deep_learning_local_smoke_test/scripts/prepare_deep_learning_smoke_data.py \
  --input-dir ANOVA_L_2_ad_cntrl_random50/processed_subjects \
  --output "${DATA}" \
  --max-rows 512

python3 rebuttal/deep_learning_local_smoke_test/scripts/train_eegnet_smoke.py \
  --data "${DATA}" \
  --split subject_disjoint_smoke \
  --epochs 1 \
  --batch-size 32

python3 rebuttal/deep_learning_local_smoke_test/scripts/train_eegnet_smoke.py \
  --data "${DATA}" \
  --split subject_overlap_smoke \
  --epochs 1 \
  --batch-size 32

python3 rebuttal/deep_learning_local_smoke_test/scripts/train_transformer_smoke.py \
  --data "${DATA}" \
  --split subject_disjoint_smoke \
  --epochs 1 \
  --batch-size 32

python3 rebuttal/deep_learning_local_smoke_test/scripts/train_transformer_smoke.py \
  --data "${DATA}" \
  --split subject_overlap_smoke \
  --epochs 1 \
  --batch-size 32
