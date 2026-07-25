# Deep Learning Ax Tune Plan

## Goal

Add a real Ray Tune plus Ax path for raw-waveform deep-learning experiments, starting with AD/Cntrl. The first implementation should stay close to the already-working deep-learning smoke path and reuse the existing Ray/Ax code where it is helpful.

The important idea is: PySpark still owns raw EEG loading, preprocessing, epoching, downsampling, epoch rejection, and writing `processed_subjects`. Ray then owns model tuning over those processed raw-waveform epochs.

## Why AD/Cntrl First

AD/Cntrl is the best first target because it is the cleanest binary classification case and already matches the smoke trainer assumptions:

- two groups
- binary metrics already implemented
- subject-disjoint leakage sentinel is meaningful
- bundled laptop test data can mimic the shape locally
- HPC can scale the same YAML shape to the full explicit subject list

Once AD/Cntrl is stable, SCZ/Cntrl should mostly be config-level repetition, not new architecture.

## Existing Code To Reuse

Existing Ax machinery:

- `eeg-ray-tuner/eeg_ray_tuner/tuning/ax_search_strategy.py`
- `eeg-ray-tuner/eeg_ray_tuner/tuning/base_search_strategy.py`
- `eeg-ray-tuner/eeg_ray_tuner/tuning/strategy_factory.py`

Useful parts:

- `CustomAxSearcher`
- `_convert_yaml_config_to_tune_space`
- per-model `num_samples`
- `tune.Tuner(...)` orchestration
- object-store pattern from `_run_model_adaptive_optimization`
- result folder style and summary aggregation ideas

Existing deep-learning machinery:

- `eeg-ray-tuner/eeg_ray_tuner/deep_learning_smoke/training.py`
- `eeg-ray-tuner/eeg_ray_tuner/deep_learning_smoke/common.py`
- `eeg-ray-tuner/eeg_ray_tuner/deep_learning_smoke/models.py`

Useful parts:

- `load_processed_subject_waveforms`
- `split_indices`
- `standardize_train_test`
- `_validation_split_indices`
- early stopping
- `run_eegnet_smoke`
- `run_transformer_smoke`

## Proposed Config Shape

Keep the current `deep_learning_smoke` block for laptop smoke. Add a sibling block for real tuning:

```yaml
deep_learning_tune:
  enabled: "Yes"
  source: raw-waveform
  processed_subjects: /app/data/AD_CNTRL_DEEP/processed_subjects
  output_dir: /app/data/AD_CNTRL_DEEP/deep_learning_tune_outputs
  metric: validation_accuracy
  mode: max
  split: subject_disjoint_smoke
  max_rows: null
  seed: 42

  training:
    epochs: 100
    validation_split: 0.2
    early_stopping:
      enabled: "Yes"
      monitor: validation_loss
      mode: min
      patience: 10
      min_delta: 0.0001
      restore_best_weights: "Yes"

  ax:
    max_concurrent_trials: 1
    num_samples: 20

  models:
    eegnet_raw:
      enabled: "Yes"
      hyperparameters:
        batch_size:
          type: choice
          values: [16, 32, 64]
        learning_rate:
          type: loguniform
          bounds: [0.0001, 0.01]
        eegnet_dropout:
          type: uniform
          bounds: [0.1, 0.6]

    transformer_raw:
      enabled: "Yes"
      hyperparameters:
        batch_size:
          type: choice
          values: [16, 32]
        learning_rate:
          type: loguniform
          bounds: [0.00005, 0.005]
        transformer_dropout:
          type: uniform
          bounds: [0.05, 0.5]
        chunk_size:
          type: choice
          values: [16, 32, 64]
        embed_dim:
          type: choice
          values: [32, 64, 128]
        heads:
          type: choice
          values: [2, 4, 8]
```

For laptop, use the same block but with `epochs: 3`, `num_samples: 5`, `max_rows: 128`, and `max_concurrent_trials: 1`.

## Code Shape

### 1. Factor The Trainer Into A Trial Callable

The current `_train_and_evaluate(...)` is almost the right core. The tuning path needs one function that accepts a single trial config and returns a metrics dict without assuming smoke output names.

Sketch:

```python
def train_deep_learning_trial(
    *,
    model_name: str,
    data_path: Path,
    output_dir: Path,
    split: str,
    seed: int,
    trial_config: dict[str, Any],
    base_training_config: dict[str, Any],
) -> dict[str, Any]:
    params = {**base_training_config, **trial_config}

    if model_name == "eegnet_raw":
        return _train_and_evaluate(
            model_kind="eegnet_feature_smoke",
            data_path=data_path,
            output_dir=output_dir,
            split=split,
            epochs=int(params["epochs"]),
            batch_size=int(params["batch_size"]),
            learning_rate=float(params["learning_rate"]),
            seed=seed,
            eegnet_dropout=float(params["eegnet_dropout"]),
            validation_split=float(params["validation_split"]),
            early_stopping_enabled=bool(params["early_stopping_enabled"]),
            early_stopping_monitor=params["early_stopping_monitor"],
            early_stopping_mode=params["early_stopping_mode"],
            early_stopping_patience=int(params["early_stopping_patience"]),
            early_stopping_min_delta=float(params["early_stopping_min_delta"]),
            restore_best_weights=bool(params["restore_best_weights"]),
        )

    if model_name == "transformer_raw":
        return _train_and_evaluate(
            model_kind="transformer_feature_smoke",
            data_path=data_path,
            output_dir=output_dir,
            split=split,
            epochs=int(params["epochs"]),
            batch_size=int(params["batch_size"]),
            learning_rate=float(params["learning_rate"]),
            seed=seed,
            chunk_size=int(params["chunk_size"]),
            embed_dim=int(params["embed_dim"]),
            heads=int(params["heads"]),
            transformer_dropout=float(params["transformer_dropout"]),
            validation_split=float(params["validation_split"]),
            early_stopping_enabled=bool(params["early_stopping_enabled"]),
            early_stopping_monitor=params["early_stopping_monitor"],
            early_stopping_mode=params["early_stopping_mode"],
            early_stopping_patience=int(params["early_stopping_patience"]),
            early_stopping_min_delta=float(params["early_stopping_min_delta"]),
            restore_best_weights=bool(params["restore_best_weights"]),
        )

    raise ValueError(f"Unknown deep-learning tune model: {model_name}")
```

This can be cleaned up later, but the first version should be explicit and boring.

### 2. Add A Deep Learning Ax Entrypoint

Add a new module, probably:

`eeg-ray-tuner/eeg_ray_tuner/deep_learning_tune/ax_tuning.py`

Responsibilities:

- load config
- convert `processed_subjects` to one `_raw_waveform_tune_data.npz` once
- build search spaces from `deep_learning_tune.models.*.hyperparameters`
- create one `CustomAxSearcher` per model
- run `tune.Tuner(trainable, tune_config=...)`
- save one trial directory per trial
- write `summary_metrics.csv`
- write `best_trials.json`

Sketch:

```python
def run_deep_learning_ax_tune(config: dict[str, Any]) -> None:
    from ray import tune, train
    import ray

    tune_config = config["deep_learning_tune"]
    data = load_processed_subject_waveforms(
        Path(tune_config["processed_subjects"]),
        tune_config.get("max_rows"),
    )
    data_path = Path(tune_config["output_dir"]) / "_raw_waveform_tune_data.npz"
    np.savez_compressed(data_path, **data)

    data_ref = ray.put(str(data_path))

    all_rows = []
    for model_name, model_cfg in enabled_models(tune_config):
        search_space = convert_yaml_to_tune_space(model_cfg["hyperparameters"])
        search_alg = CustomAxSearcher(
            search_space,
            metric=tune_config.get("metric", "validation_accuracy"),
            mode=tune_config.get("mode", "max"),
            experiment_name=f"dl_ax_{model_name}",
        )

        def trainable(trial_params):
            trial_data_path = Path(ray.get(data_ref))
            trial_id = train.get_context().get_trial_id()
            trial_output_dir = Path(tune_config["output_dir"]) / model_name / trial_id

            metrics = train_deep_learning_trial(
                model_name=model_name,
                data_path=trial_data_path,
                output_dir=trial_output_dir,
                split=tune_config.get("split", "subject_disjoint_smoke"),
                seed=int(tune_config.get("seed", 42)),
                trial_config=trial_params,
                base_training_config=flatten_training_config(tune_config),
            )

            train.report({
                "accuracy": metrics["accuracy"],
                "validation_accuracy": metrics["validation_accuracy"],
                "validation_loss": metrics["validation_loss"],
                "epochs_ran": metrics["epochs_ran"],
            })

        tuner = tune.Tuner(
            trainable,
            tune_config=tune.TuneConfig(
                search_alg=search_alg,
                metric=tune_config.get("metric", "validation_accuracy"),
                mode=tune_config.get("mode", "max"),
                num_samples=int(tune_config["ax"]["num_samples"]),
            ),
            run_config=tune.RunConfig(
                name=f"deep_learning_ax_{model_name}",
                storage_path=str(Path(tune_config["output_dir"]) / "ray_debug"),
                verbose=0,
                log_to_file=False,
            ),
        )
        result_grid = tuner.fit()
        all_rows.extend(extract_trial_rows(result_grid, model_name))

    write_csv(Path(tune_config["output_dir"]) / "summary_metrics.csv", all_rows)
```

### 3. Wire `start-pipelines.py`

The root launcher already has special handling for `deep_learning_smoke.source: raw-waveform`. Add a second branch:

```python
deep_learning_tune = config.get("deep_learning_tune", {})
if deep_learning_tune.get("enabled") == "Yes":
    return " ".join([
        "python",
        "-m",
        "eeg_ray_tuner.deep_learning_tune.ax_tuning",
        "--config",
        "/app/config.yaml",
    ])
```

This should only affect the Ray container command. PySpark can remain unchanged because it already writes raw-waveform `processed_subjects`.

### 4. Validation

The config handler should accept `deep_learning_tune` without disturbing the old `ray.ax` sklearn path.

Minimum validation:

- `enabled` is `Yes` or `No`
- `source` is `raw-waveform`
- `processed_subjects` and `output_dir` are strings
- `metric` is one of `validation_accuracy`, `validation_loss`, `accuracy`, `balanced_accuracy`
- `mode` is `max` or `min`
- `ax.num_samples >= 5`
- each enabled model has a hyperparameter dict
- `choice`, `uniform`, `loguniform`, `quniform` use the same schema as the current Ax helper

Do not overload `ray.ax` yet. Keep deep-learning tuning separate from sklearn tuning to avoid bending the existing ML config around raw waveform models.

## Result Layout

Recommended output:

```text
data/AD_CNTRL_DEEP/deep_learning_tune_outputs/
  _raw_waveform_tune_data.npz
  summary_metrics.csv
  best_trials.json
  eegnet_raw/
    <trial_id>/
      eegnet_feature_smoke_subject_disjoint_smoke_metrics.csv
      eegnet_feature_smoke_subject_disjoint_smoke_predictions.csv
      eegnet_feature_smoke_subject_disjoint_smoke_training_log.json
      trial_config.json
  transformer_raw/
    <trial_id>/
      transformer_feature_smoke_subject_disjoint_smoke_metrics.csv
      transformer_feature_smoke_subject_disjoint_smoke_predictions.csv
      transformer_feature_smoke_subject_disjoint_smoke_training_log.json
      trial_config.json
  ray_debug/
```

`summary_metrics.csv` should include trial hyperparameters as columns in addition to model metrics. This makes quick HPC auditing easier.

## Metrics To Optimize

For the first AD/Cntrl run, optimize `validation_accuracy` or `validation_loss`, not test accuracy.

Recommended first default:

```yaml
metric: validation_accuracy
mode: max
```

Keep test accuracy in the result row as a final held-out sanity metric. This preserves the distinction between model selection and final evaluation. The current smoke trainer already splits validation only from the training partition, which is the behavior we want.

## First Implementation Phases

### Phase 1: No New Model Logic

- add `deep_learning_tune/ax_tuning.py`
- reuse `CustomAxSearcher`
- reuse `_train_and_evaluate`
- support only `eegnet_raw`
- laptop config: 5 Ax samples, 3 epochs, max_rows 128
- run through Docker with `python3 start-pipelines.py deep_learning_ax_test_laptop.yaml`

### Phase 2: Transformer

- add `transformer_raw`
- include `chunk_size`, `embed_dim`, `heads`, and `transformer_dropout`
- make sure invalid `embed_dim % heads != 0` combinations are rejected before the trial starts or constrained in config

### Phase 3: HPC AD/Cntrl

- use explicit AD/Cntrl subject list
- `reuse_processed_subjects: "Yes"` once the PySpark stage has produced the raw waveform epochs
- increase `num_samples` to 20-50 per model
- increase epochs with early stopping, for example `epochs: 100`, `patience: 10`
- keep `max_concurrent_trials` conservative until GPU/CPU memory behavior is known

### Phase 4: Better Reporting

- `best_trials.json`
- per-model best summary
- fold/subject leakage sentinels
- optional training curves from `*_training_log.json`

## Main Risk Points

- Ax categorical handling: keep values primitive. For complex values, JSON-encode them before giving them to Ax.
- Transformer constraints: `embed_dim` must divide cleanly by `heads`.
- Trial output collisions: every trial needs its own directory.
- Validation leakage: never optimize on test accuracy, even though test metrics should still be saved.
- Memory: raw waveforms can be large. Load the NPZ once and use Ray object store or path passing carefully.
- Config confusion: keep `deep_learning_smoke` and `deep_learning_tune` separate so a smoke test remains tiny and deterministic.

## Minimal Laptop Test Config

```yaml
deep_learning_tune:
  enabled: "Yes"
  source: raw-waveform
  processed_subjects: /app/data/deep_learning_ax_test_laptop/processed_subjects
  output_dir: /app/data/deep_learning_ax_test_laptop/deep_learning_tune_outputs
  metric: validation_accuracy
  mode: max
  split: subject_disjoint_smoke
  max_rows: 128
  seed: 42
  training:
    epochs: 3
    validation_split: 0.2
    early_stopping:
      enabled: "Yes"
      monitor: validation_loss
      mode: min
      patience: 1
      min_delta: 0.0001
      restore_best_weights: "Yes"
  ax:
    max_concurrent_trials: 1
    num_samples: 5
  models:
    eegnet_raw:
      enabled: "Yes"
      hyperparameters:
        batch_size:
          type: choice
          values: [16, 32]
        learning_rate:
          type: loguniform
          bounds: [0.0001, 0.01]
        eegnet_dropout:
          type: uniform
          bounds: [0.1, 0.5]
```

This is the first "does this actually work?" test. The HPC version should be the same shape with larger subject lists, `max_rows: null`, more epochs, and more Ax samples.
