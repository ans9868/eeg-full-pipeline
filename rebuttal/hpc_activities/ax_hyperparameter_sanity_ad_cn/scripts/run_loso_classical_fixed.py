#!/usr/bin/env python3
"""Run fixed-hyperparameter classical ML on true LOSO transformed folds."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


DEFAULT_PARAMS: dict[str, dict[str, Any]] = {
    "knn": {"n_neighbors": 31, "weights": "uniform", "metric": "manhattan"},
    "svm": {"C": 1.0, "class_weight": "balanced", "max_iter": 5000},
    "mlp": {
        "hidden_layer_sizes": "128_64",
        "alpha": 0.001,
        "learning_rate_init": 0.001,
        "batch_size": 128,
        "activation": "relu",
        "max_iter": 150,
    },
    "xgboost": {
        "max_depth": 12,
        "learning_rate": 0.01,
        "n_estimators": 321,
        "subsample": 0.5,
        "colsample_bytree": 0.5,
        "min_child_weight": 1.0,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, help="Root containing transformed/<fold>/train_data and test_data")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--experiment-name", required=True)
    parser.add_argument("--models", default="knn,svm,mlp,xgboost")
    parser.add_argument("--params-json", help="Optional JSON file overriding DEFAULT_PARAMS")
    parser.add_argument("--limit-folds", type=int, default=0)
    parser.add_argument("--random-seed", type=int, default=42)
    parser.add_argument("--n-jobs", type=int, default=1)
    return parser.parse_args()


def load_params(path: str | None) -> dict[str, dict[str, Any]]:
    params = {model: values.copy() for model, values in DEFAULT_PARAMS.items()}
    if path:
        overrides = json.loads(Path(path).read_text())
        for model, values in overrides.items():
            params.setdefault(model, {}).update(values)
    return params


def discover_folds(data_root: Path, limit_folds: int = 0) -> list[Path]:
    transformed = data_root / "transformed"
    if not transformed.exists():
        raise FileNotFoundError(f"Missing transformed directory: {transformed}")
    folds = [
        path for path in sorted(transformed.iterdir())
        if path.is_dir() and (path / "train_data").exists() and (path / "test_data").exists()
    ]
    if limit_folds:
        folds = folds[:limit_folds]
    if not folds:
        raise RuntimeError(f"No transformed folds found under {transformed}")
    return folds


def load_split(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    parquet_files = sorted(path.glob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError(f"No parquet files found in {path}")
    df = pd.concat((pd.read_parquet(p) for p in parquet_files), ignore_index=True)
    missing = {"features_array", "label", "SubjectID"} - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns {sorted(missing)} in {path}")
    x = np.vstack(df["features_array"].to_numpy()).astype(np.float32)
    y = df["label"].to_numpy().astype(int)
    subjects = df["SubjectID"].astype(str).to_numpy()
    return x, y, subjects


def parse_hidden_layer_sizes(value: Any) -> tuple[int, ...]:
    if isinstance(value, (tuple, list)):
        return tuple(int(item) for item in value)
    return tuple(int(item) for item in str(value).split("_") if item)


def make_model(model_name: str, params: dict[str, Any], random_seed: int, n_jobs: int):
    if model_name == "knn":
        return KNeighborsClassifier(
            n_neighbors=int(params["n_neighbors"]),
            weights=str(params["weights"]),
            metric=str(params["metric"]),
            n_jobs=n_jobs,
        )
    if model_name == "svm":
        class_weight = params.get("class_weight")
        if class_weight == "none":
            class_weight = None
        return make_pipeline(
            StandardScaler(),
            LinearSVC(
                C=float(params["C"]),
                class_weight=class_weight,
                max_iter=int(params.get("max_iter", 5000)),
                random_state=random_seed,
                dual=False,
            ),
        )
    if model_name == "mlp":
        return make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=parse_hidden_layer_sizes(params["hidden_layer_sizes"]),
                alpha=float(params["alpha"]),
                learning_rate_init=float(params["learning_rate_init"]),
                batch_size=int(params["batch_size"]),
                activation=str(params.get("activation", "relu")),
                solver="adam",
                early_stopping=True,
                validation_fraction=0.15,
                n_iter_no_change=10,
                max_iter=int(params.get("max_iter", 150)),
                random_state=random_seed,
            ),
        )
    if model_name == "xgboost":
        try:
            from xgboost import XGBClassifier
        except ImportError as exc:
            raise RuntimeError("xgboost is not installed in this environment") from exc
        return XGBClassifier(
            n_estimators=int(params["n_estimators"]),
            max_depth=int(params["max_depth"]),
            learning_rate=float(params["learning_rate"]),
            subsample=float(params["subsample"]),
            colsample_bytree=float(params["colsample_bytree"]),
            min_child_weight=float(params["min_child_weight"]),
            random_state=random_seed,
            n_jobs=n_jobs,
            eval_metric="logloss",
        )
    raise ValueError(f"Unsupported model: {model_name}")


def majority_vote(values: np.ndarray) -> int:
    counts = Counter(int(value) for value in values)
    return int(sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0])


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def evaluate_model(
    model_name: str,
    params: dict[str, Any],
    folds: list[Path],
    args: argparse.Namespace,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    fold_rows: list[dict[str, Any]] = []
    subject_rows: list[dict[str, Any]] = []
    all_true: list[np.ndarray] = []
    all_pred: list[np.ndarray] = []
    start = time.time()

    for fold_idx, fold in enumerate(folds, start=1):
        fold_start = time.time()
        x_train, y_train, _ = load_split(fold / "train_data")
        x_test, y_test, subjects = load_split(fold / "test_data")
        model = make_model(model_name, params, args.random_seed, args.n_jobs)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test).astype(int)

        all_true.append(y_test)
        all_pred.append(y_pred)
        fold_subjects = sorted(set(subjects))
        if len(fold_subjects) != 1:
            raise ValueError(f"Expected one held-out subject in {fold}, found {fold_subjects}")
        subject_id = fold_subjects[0]
        true_subject_label = majority_vote(y_test)
        pred_subject_label = majority_vote(y_pred)

        fold_rows.append(
            {
                "experiment_name": args.experiment_name,
                "model": model_name,
                "fold_index": fold_idx,
                "fold_name": fold.name,
                "SubjectID": subject_id,
                "true_subject_label": true_subject_label,
                "pred_subject_label": pred_subject_label,
                "subject_majority_correct": int(true_subject_label == pred_subject_label),
                "epoch_accuracy": float(accuracy_score(y_test, y_pred)),
                "n_train": int(len(y_train)),
                "n_test": int(len(y_test)),
                "seconds": float(time.time() - fold_start),
            }
        )
        subject_rows.append(fold_rows[-1].copy())

    y_true = np.concatenate(all_true)
    y_pred = np.concatenate(all_pred)
    subject_true = [row["true_subject_label"] for row in subject_rows]
    subject_pred = [row["pred_subject_label"] for row in subject_rows]
    summary = {
        "experiment_name": args.experiment_name,
        "model": model_name,
        "params": json.dumps(params, sort_keys=True),
        "n_folds": len(folds),
        "n_subjects": len(subject_rows),
        "pooled_epoch_accuracy": float(accuracy_score(y_true, y_pred)),
        "pooled_epoch_balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "mean_subject_epoch_accuracy": float(np.mean([row["epoch_accuracy"] for row in subject_rows])),
        "subject_majority_accuracy": float(accuracy_score(subject_true, subject_pred)),
        "subject_balanced_accuracy": float(balanced_accuracy_score(subject_true, subject_pred)),
        "total_seconds": float(time.time() - start),
    }
    return summary, fold_rows, subject_rows


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    params_by_model = load_params(args.params_json)
    folds = discover_folds(Path(args.data_root), args.limit_folds)
    models = [item.strip() for item in args.models.split(",") if item.strip()]

    summary_rows: list[dict[str, Any]] = []
    all_fold_rows: list[dict[str, Any]] = []
    all_subject_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []

    for model_name in models:
        try:
            summary, fold_rows, subject_rows = evaluate_model(
                model_name, params_by_model[model_name], folds, args
            )
        except Exception as exc:
            skipped_rows.append({"model": model_name, "error": str(exc)})
            continue
        summary_rows.append(summary)
        all_fold_rows.extend(fold_rows)
        all_subject_rows.extend(subject_rows)

    write_csv(output_dir / "model_summary.csv", summary_rows)
    write_csv(output_dir / "fold_results.csv", all_fold_rows)
    write_csv(output_dir / "subject_predictions.csv", all_subject_rows)
    write_csv(output_dir / "skipped_models.csv", skipped_rows)
    (output_dir / "run_config.json").write_text(
        json.dumps(
            {
                "data_root": args.data_root,
                "experiment_name": args.experiment_name,
                "models": models,
                "limit_folds": args.limit_folds,
                "params_by_model": params_by_model,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"Wrote {len(summary_rows)} model summaries to {output_dir / 'model_summary.csv'}")
    if skipped_rows:
        print(f"Skipped {len(skipped_rows)} model(s); see {output_dir / 'skipped_models.csv'}")


if __name__ == "__main__":
    main()
