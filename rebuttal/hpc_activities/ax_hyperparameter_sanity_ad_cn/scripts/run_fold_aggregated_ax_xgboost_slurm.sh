#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 7 ]; then
  echo "Usage: $0 <protocol> <data_root_or_comma_separated_roots> <output_dir> <experiment_name> <model> <search_space> <num_trials> [metric] [limit_folds] [walltime]" >&2
  exit 2
fi

protocol="$1"
data_root="$2"
output_dir="$3"
experiment_name="$4"
model="$5"
search_space="$6"
num_trials="$7"
metric="${8:-balanced_accuracy}"
limit_folds="${9:-0}"
walltime="${10:-04:00:00}"

project_root="/scratch/ans9868/rebuttal-deep-eeg-full-pipeline/eeg-full-pipeline"
activity_rel="rebuttal/hpc_activities/ax_hyperparameter_sanity_ad_cn"
script="/app/$activity_rel/scripts/run_fold_aggregated_ax_xgboost.py"

cd "$project_root"
mkdir -p containers "$output_dir"

data_root_cli="--data-root '$data_root'"
if [[ "$data_root" == *,* ]]; then
  data_root_cli="--data-roots '$data_root'"
fi

sbatch \
  --time="$walltime" \
  --mem=56G \
  --cpus-per-task=12 \
  --account=torch_pr_60_general \
  --job-name=fold-ax-"$model" \
  --output=./containers/fold_ax_"$model"_%j.out \
  --error=./containers/fold_ax_"$model"_%j.err \
  --wrap="singularity exec --bind ./data:/app/data --bind ./rebuttal:/app/rebuttal --bind /scratch/ans9868/eeg-full-pipeline/data:/old_data ./containers/eeg-ray-tuner.sif python $script --protocol '$protocol' $data_root_cli --output-dir '$output_dir' --experiment-name '$experiment_name' --model '$model' --search-space '$search_space' --num-trials '$num_trials' --metric '$metric' --limit-folds '$limit_folds' --n-jobs 1"
