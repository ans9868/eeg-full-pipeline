# Classical ML Ax Tune Plan

## Goal

Use Ray Tune plus Ax for the simpler classical ML models, starting with AD/Cntrl. This should tune the existing sklearn-style models over PySpark-produced feature tables, not the raw-waveform deep-learning path.

The deep-learning models have tunable knobs like learning rate, dropout, batch size, architecture width, and early-stopping patience, but that is not the best first optimization target here. The current value is much clearer for classical models because their hyperparameters are cheap to evaluate and have direct model behavior effects.

## Why AD/Cntrl First

AD/Cntrl is the best first target because it is the cleanest binary classification case:

- binary labels and metrics are already natural
- subject-disjoint evaluation is easy to reason about
- the existing feature pipeline already supports the AD/Cntrl style configs
- KNN/SVM/RF/XGBoost-style tuning is fast enough for laptop smoke and scalable on HPC
- results are easier to debug before repeating the same approach for SCZ/Cntrl

## Existing Code To Reuse

Main Ray/Ax implementation:

- `eeg-ray-tuner/eeg_ray_tuner/tuning/ax_search_strategy.py`
- `eeg-ray-tuner/eeg_ray_tuner/tuning/base_search_strategy.py`
- `eeg-ray-tuner/eeg_ray_tuner/tuning/strategy_factory.py`
- `eeg-ray-tuner/eeg_ray_tuner/models/model_runner.py`

Useful existing pieces:

- `CustomAxSearcher`
- `_convert_yaml_config_to_tune_space`
- per-model `num_samples`
- `tune.Tuner(...)` orchestration
- `ModelRunner.train_and_evaluate_model`
- existing transformed fold/data loading
- existing result layout under `ml_results_ax`

## What We Are Not Doing

Do not tune raw-waveform deep-learning in this pass.

Do not add a new deep-learning-specific Ax config block.

Do not change PySpark raw-waveform export for this work.

Do not optimize on held-out test accuracy. Ax should optimize a validation/CV metric where possible; test metrics should remain final reporting/sanity outputs.

## Classical Models Worth Tuning

Good first set:

- `KNN`
- `Random Forest`
- `SVM`
- `Gradient Boosting`
- `XGBoost`, if available in the Ray container
- `MLP (Neural Network)` as a classical sklearn MLP, not the raw EEG deep model

Suggested order:

1. KNN only for laptop proof of life
2. KNN plus Random Forest for a slightly richer sanity run
3. Add SVM and Gradient Boosting on HPC
4. Add XGBoost if dependency/runtime behavior is clean

## Current Ax Config Shape

The existing config style already supports this:

```yaml
ray:
  search_strategies:
  - ax

  ax:
    models:
    - KNN
    max_concurrent: "1"
    cv_folds: "2"
    max_concurrent_trials: 1
    model_configs:
      KNN:
        use_default: false
        num_samples: 5
        hyperparameters:
          n_neighbors:
            type: quniform
            bounds: [1, 7]
            q: 1
          weights:
            type: choice
            values: [uniform, distance]
          metric:
            type: choice
            values: [euclidean, manhattan]

  metric: accuracy
  mode: max
```

That should stay under `ray.ax`, because this is the existing classical ML tuning surface.

## Recommended AD/Cntrl Laptop Config

Make a tiny config copied from the known working non-deep-learning test config. Keep PySpark output feature-based, not raw-waveform:

```yaml
project:
  name: ax_ad_cntrl_seed42_laptop
  output_dir: ./data
  experiment_type: ML Classification
  subjects_or_events: subjects
  deployment_method: Docker
  random_seed: 42
  expose_ports: "No"

data_input:
  groups:
    alz:
    - /Users/user/projects/eeg-full-pipeline/eeg-pyspark-pipeline/tests/test_eeg_data/sub-001_task-eyesclosed_eeg.set
    - /Users/user/projects/eeg-full-pipeline/eeg-pyspark-pipeline/tests/test_eeg_data/sub-002_task-eyesclosed_eeg.set
    cntrl:
    - /Users/user/projects/eeg-full-pipeline/eeg-pyspark-pipeline/tests/test_eeg_data/sub-003_task-eyesclosed_eeg.set
    - /Users/user/projects/eeg-full-pipeline/eeg-pyspark-pipeline/tests/test_eeg_data/sub-004_task-eyesclosed_eeg.set
  reuse_processed_subjects: "No"
  save_processed_subjects: "Yes"
  reuse_transformed: "No"
  save_transformed: "Yes"
  reuse_transformed_across_experiments: "No"

preprocessing:
  bands:
    Delta: [0.5, 4]
    Theta: [4, 8]
    Alpha: [8, 12]
    Beta: [12, 30]
  window_size: 3.0
  sliding_window: 0.5
  downsampling: 64
  reject_by_annotation: "Yes"
  normalize_psd: "Yes"
  use_epoch_rejection: "No"
  epoch_rejection:
    reject: 600.0
    flat: 0.3
  extreme_datapoint_removal: null

feature_extraction:
  method: welch
  features:
    per_channel_across_bands:
    - absolute_band_power
    - relative_band_power
    per_channel_per_band: []
  output_format: ml
  show_intermediate_results: "No"
  show_intermediate_counts: "No"

feature_transformation:
  transformations:
  - ANOVA F-test
  - MinMax scaler
  synthetic: None
  anova_label_column: Group
  anova_label_type: categorical
  anova_selection_mode: numTopFeatures
  anova_selection_threshold: 8
  minmax_range: [0, 1]

data_transformation_strategy:
  strategy: Transform all data together (intra subject split) (no split - fastest, and potential data leakage)

pyspark:
  docker_image: eeg-spark-pipeline:latest
  master: "2"
  driver_memory: "2"
  executor_memory: "2"
  executor_cores: "1"
  shuffle_partitions: "2"

ray:
  docker_image: eeg-ray-tuner:latest
  docker_shared_mem_mb: 2048
  search_strategies:
  - ax
  ax:
    models:
    - KNN
    model_configs:
      KNN:
        use_default: false
        num_samples: 5
        hyperparameters:
          n_neighbors:
            type: quniform
            bounds: [1, 7]
            q: 1
          weights:
            type: choice
            values: [uniform, distance]
          metric:
            type: choice
            values: [euclidean, manhattan]
    max_concurrent: "1"
    cv_folds: "2"
    max_concurrent_trials: 1
  metric: accuracy
  mode: max
  resources:
    num_cpus: "2"
    memory_gb: "2"
    object_store_memory_gb: "1"
    num_gpus: 0
    dashboard_port: "8265"
```

This is the first “does Ax actually work for the classical pipeline?” run.

## Code Path To Verify

Expected execution:

1. `start-pipelines.py` runs the PySpark container.
2. PySpark writes normal ML feature outputs and transformed data.
3. `start-pipelines.py` runs the Ray container with `python /app/main.py --config /app/config.yaml`.
4. `main.py` creates strategies through `StrategyFactory`.
5. `AxSearchStrategy` builds a Ray Tune search space for KNN.
6. `CustomAxSearcher` suggests trials.
7. `_run_model_adaptive_optimization` loads train/test fold data.
8. `ModelRunner` trains/evaluates each trial.
9. Ray Tune reports `accuracy`, `test_accuracy`, and `train_accuracy`.
10. Results land under `data/<project>/ml_results_ax`.

## Main Things To Check

The first laptop run should confirm:

- `ray.search_strategies: [ax]` chooses only Ax
- config validation accepts `num_samples: 5`
- `CustomAxSearcher` receives the correct KNN search space
- Ax categorical choices work for `weights` and `metric`
- `quniform` for `n_neighbors` becomes an integer trial value
- trial outputs are saved in `ml_results_ax`
- summary/best-trial files are produced
- no leakage-suspicious subject overlap appears if the selected split strategy is subject-disjoint

## Likely Bugs

Possible issue 1: `num_samples` validation requires at least 5.

Use exactly 5 for laptop smoke, not 2 or 3.

Possible issue 2: `quniform` currently converts to `tune.randint`, which ignores `q`.

That is fine for integer parameters like `n_neighbors`. For true quantized floats, we may need a better converter later.

Possible issue 3: old/new concurrency names both exist.

Set both `max_concurrent: "1"` and `max_concurrent_trials: 1` in laptop configs to avoid surprises.

Possible issue 4: the Ray Ax path optimizes reported `accuracy`.

For now, use `accuracy` to match the existing code. Later we can make model selection cleaner by reporting a validation metric distinct from test accuracy.

Possible issue 5: `MLP hidden_layer_sizes` values need JSON encoding.

The existing Ax strategy has special handling for that model. KNN avoids this complexity for the first proof.

## HPC AD/Cntrl Shape

Once the KNN laptop config passes:

- use explicit AD/Cntrl subject lists
- use `reuse_processed_subjects: "Yes"` if the processed cache already exists
- use `reuse_transformed: "Yes"` if the transformed feature cache already exists and config hash behavior agrees
- tune 3-5 classical models
- start with `num_samples: 20` per model
- keep `max_concurrent_trials` conservative
- write one config per major feature/transform setup, for example:
  - `config_ax_ad_cntrl_anova_minmax_seed42.yaml`
  - `config_ax_ad_cntrl_pca_minmax_seed42.yaml`

## First Implementation Checklist

- Create `config/config_ax_ad_cntrl_seed42_laptop.yaml` from the known non-deep-learning test config.
- Enable only `ray.search_strategies: [ax]`.
- Use KNN only with `num_samples: 5`.
- Run `python3 start-pipelines.py config_ax_ad_cntrl_seed42_laptop.yaml`.
- If it fails, inspect `eeg-ray-tuner/eeg_ray_tuner/tuning/base_search_strategy.py` around `_run_model_adaptive_optimization`.
- If it passes, add Random Forest as the second model.
- Then scale the same config shape to AD/Cntrl full subject lists.

## Bottom Line

The right immediate target is not deep-learning tuning. It is Ax tuning for the existing classical ML models over the existing PySpark feature pipeline. The first useful proof is a tiny AD/Cntrl KNN Ax run, then AD/Cntrl multi-model Ax on HPC.
