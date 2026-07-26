#!/usr/bin/env python3
"""Fold-aggregated Ax tuning for AD/CN classical ML models.

This script implements the rebuttal tuning design:

    one Ax searcher
    -> one candidate hyperparameter setting per Ax trial
    -> evaluate that same setting across every fold
    -> return mean fold metric to Ax

It intentionally does not use the pipeline's built-in per-fold Ax tuning path.
Run inside the Ray SIF so dependencies match the HPC environment.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ax.service.ax_client import AxClient
from ax.service.utils.instantiation import ObjectiveProperties
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier


@dataclass(frozen=True)
class Fold:
    name: str
    train_path: Path
    test_path: Path
    data_root: Path
    data_root_name: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", choices=["w_c", "lpso"], required=True)
    parser.add_argument("--data-root", help="Project data root containing transformed/")
    parser.add_argument(
        "--data-roots",
        help=(
            "Comma-separated project data roots. For w_c, this evaluates one Ax "
            "candidate across all listed seed roots and returns the mean metric."
        ),
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--experiment-name", required=True)
    parser.add_argument("--model", choices=["xgboost", "knn", "svm", "mlp"], default="xgboost")
    parser.add_argument(
        "--search-space",
        choices=["xgboost_max_depth", "xgboost_expanded", "knn_expanded", "svm_expanded", "mlp_expanded"],
        default="xgboost_max_depth",
    )
    parser.add_argument("--num-trials", type=int, default=5)
    parser.add_argument("--metric", choices=["accuracy", "balanced_accuracy"], default="balanced_accuracy")
    parser.add_argument("--random-seed", type=int, default=42)
    parser.add_argument("--max-depth-min", type=int, default=3)
    parser.add_argument("--max-depth-max", type=int, default=12)
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--learning-rate", type=float, default=0.2)
    parser.add_argument("--subsample", type=float, default=0.7)
    parser.add_argument("--n-jobs", type=int, default=1)
    parser.add_argument("--limit-folds", type=int, default=0, help="Optional first-N fold limit for debugging")
    return parser.parse_args()


def setup_logging(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "run.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_path)],
    )


def parse_data_roots(args: argparse.Namespace) -> list[Path]:
    data_roots: list[Path] = []
    if args.data_roots:
        data_roots.extend(Path(item.strip()) for item in args.data_roots.split(",") if item.strip())
    if args.data_root:
        data_roots.append(Path(args.data_root))

    if not data_roots:
        raise ValueError("Specify --data-root or --data-roots")
    if len(data_roots) > 1 and args.protocol != "w_c":
        raise ValueError("--data-roots is currently supported for protocol w_c only")

    return data_roots


def discover_folds(
    data_root: Path,
    protocol: str,
    limit_folds: int = 0,
    *,
    include_data_root_in_name: bool = False,
) -> list[Fold]:
    transformed = data_root / "transformed"
    if not transformed.exists():
        raise FileNotFoundError(f"Missing transformed directory: {transformed}")

    if protocol == "w_c":
        fold_name = "within_subject_split"
        if include_data_root_in_name:
            fold_name = f"{data_root.name}::within_subject_split"
        folds = [
            Fold(
                name=fold_name,
                train_path=transformed / "within_subject_split" / "train_data",
                test_path=transformed / "within_subject_split" / "test_data",
                data_root=data_root,
                data_root_name=data_root.name,
            )
        ]
    else:
        folds = []
        for fold_dir in sorted(transformed.iterdir()):
            if not fold_dir.is_dir():
                continue
            train_path = fold_dir / "train_data"
            test_path = fold_dir / "test_data"
            if train_path.exists() and test_path.exists():
                folds.append(
                    Fold(
                        name=fold_dir.name,
                        train_path=train_path,
                        test_path=test_path,
                        data_root=data_root,
                        data_root_name=data_root.name,
                    )
                )

    if limit_folds:
        folds = folds[:limit_folds]

    if not folds:
        raise RuntimeError(f"No folds discovered under {transformed}")

    for fold in folds:
        if not fold.train_path.exists():
            raise FileNotFoundError(f"Missing train path for {fold.name}: {fold.train_path}")
        if not fold.test_path.exists():
            raise FileNotFoundError(f"Missing test path for {fold.name}: {fold.test_path}")

    return folds


def discover_all_folds(data_roots: list[Path], protocol: str, limit_folds: int) -> list[Fold]:
    include_data_root_in_name = len(data_roots) > 1
    folds: list[Fold] = []
    for data_root in data_roots:
        folds.extend(
            discover_folds(
                data_root,
                protocol,
                limit_folds,
                include_data_root_in_name=include_data_root_in_name,
            )
        )
    return folds


def load_split(path: Path) -> tuple[np.ndarray, np.ndarray]:
    parquet_files = sorted(path.glob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError(f"No parquet files in {path}")
    df = pd.concat((pd.read_parquet(p) for p in parquet_files), ignore_index=True)
    if "features_array" not in df.columns or "label" not in df.columns:
        raise ValueError(f"Expected features_array and label columns in {path}; got {list(df.columns)}")
    x = np.vstack(df["features_array"].to_numpy()).astype(np.float32)
    y = df["label"].to_numpy().astype(int)
    return x, y


def parse_hidden_layer_sizes(value: Any) -> tuple[int, ...]:
    if isinstance(value, (tuple, list)):
        return tuple(int(item) for item in value)
    return tuple(int(item) for item in str(value).split("_") if item)


def evaluate_one_fold(
    fold: Fold,
    parameters: dict[str, Any],
    *,
    model_name: str,
    random_seed: int,
    n_estimators: int,
    learning_rate: float,
    subsample: float,
    n_jobs: int,
) -> dict[str, Any]:
    start = time.time()
    x_train, y_train = load_split(fold.train_path)
    x_test, y_test = load_split(fold.test_path)

    if model_name == "xgboost":
        model = XGBClassifier(
            n_estimators=int(parameters.get("n_estimators", n_estimators)),
            max_depth=int(parameters["max_depth"]),
            learning_rate=float(parameters.get("learning_rate", learning_rate)),
            subsample=float(parameters.get("subsample", subsample)),
            colsample_bytree=float(parameters.get("colsample_bytree", 1.0)),
            min_child_weight=float(parameters.get("min_child_weight", 1.0)),
            random_state=random_seed,
            n_jobs=n_jobs,
            eval_metric="logloss",
        )
    elif model_name == "knn":
        model = KNeighborsClassifier(
            n_neighbors=int(parameters["n_neighbors"]),
            weights=str(parameters["weights"]),
            metric=str(parameters["metric"]),
            n_jobs=n_jobs,
        )
    elif model_name == "svm":
        class_weight = parameters.get("class_weight")
        if class_weight == "none":
            class_weight = None
        model = make_pipeline(
            StandardScaler(),
            LinearSVC(
                C=float(parameters["C"]),
                class_weight=class_weight,
                max_iter=int(parameters.get("max_iter", 5000)),
                random_state=random_seed,
                dual=False,
            ),
        )
    elif model_name == "mlp":
        model = make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=parse_hidden_layer_sizes(parameters["hidden_layer_sizes"]),
                alpha=float(parameters["alpha"]),
                learning_rate_init=float(parameters["learning_rate_init"]),
                batch_size=int(parameters["batch_size"]),
                activation=str(parameters.get("activation", "relu")),
                solver="adam",
                early_stopping=True,
                validation_fraction=0.15,
                n_iter_no_change=10,
                max_iter=int(parameters.get("max_iter", 150)),
                random_state=random_seed,
            ),
        )
    else:
        raise ValueError(f"Unsupported model: {model_name}")
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    return {
        "fold_name": fold.name,
        "data_root": str(fold.data_root),
        "data_root_name": fold.data_root_name,
        **flatten_parameters(parameters),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_test, y_pred)),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "seconds": float(time.time() - start),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def flatten_parameters(parameters: dict[str, Any]) -> dict[str, Any]:
    return {f"param_{k}": v for k, v in sorted(parameters.items())}


def ax_parameters(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.search_space == "xgboost_max_depth":
        return [
            {
                "name": "max_depth",
                "type": "range",
                "bounds": [args.max_depth_min, args.max_depth_max],
                "value_type": "int",
            }
        ]
    if args.search_space == "xgboost_expanded":
        return [
            {"name": "max_depth", "type": "range", "bounds": [2, 12], "value_type": "int"},
            {"name": "learning_rate", "type": "range", "bounds": [0.01, 0.3], "value_type": "float", "log_scale": True},
            {"name": "n_estimators", "type": "range", "bounds": [50, 400], "value_type": "int"},
            {"name": "subsample", "type": "range", "bounds": [0.5, 1.0], "value_type": "float"},
            {"name": "colsample_bytree", "type": "range", "bounds": [0.5, 1.0], "value_type": "float"},
            {"name": "min_child_weight", "type": "range", "bounds": [1.0, 10.0], "value_type": "float"},
        ]
    if args.search_space == "knn_expanded":
        return [
            {"name": "n_neighbors", "type": "range", "bounds": [1, 31], "value_type": "int"},
            {"name": "weights", "type": "choice", "values": ["uniform", "distance"]},
            {"name": "metric", "type": "choice", "values": ["euclidean", "manhattan"]},
        ]
    if args.search_space == "svm_expanded":
        return [
            {"name": "C", "type": "range", "bounds": [0.001, 100.0], "value_type": "float", "log_scale": True},
            {"name": "class_weight", "type": "choice", "values": ["none", "balanced"]},
            {"name": "max_iter", "type": "choice", "values": [3000, 5000, 8000], "value_type": "int"},
        ]
    if args.search_space == "mlp_expanded":
        return [
            {"name": "hidden_layer_sizes", "type": "choice", "values": ["64", "128", "64_32", "128_64"]},
            {"name": "alpha", "type": "range", "bounds": [0.00001, 0.01], "value_type": "float", "log_scale": True},
            {"name": "learning_rate_init", "type": "range", "bounds": [0.0001, 0.01], "value_type": "float", "log_scale": True},
            {"name": "batch_size", "type": "choice", "values": [64, 128, 256], "value_type": "int"},
            {"name": "activation", "type": "choice", "values": ["relu", "tanh"]},
            {"name": "max_iter", "type": "choice", "values": [100, 150], "value_type": "int"},
        ]
    raise ValueError(f"Unsupported search space: {args.search_space}")


def make_ax_client(args: argparse.Namespace) -> AxClient:
    ax_client = AxClient(verbose_logging=False)
    ax_client.create_experiment(
        name=args.experiment_name,
        parameters=ax_parameters(args),
        objectives={args.metric: ObjectiveProperties(minimize=False)},
    )
    return ax_client


def main() -> None:
    args = parse_args()
    data_roots = parse_data_roots(args)
    output_dir = Path(args.output_dir)
    setup_logging(output_dir)

    if args.model == "xgboost" and not args.search_space.startswith("xgboost"):
        raise ValueError(f"Model {args.model} is incompatible with search space {args.search_space}")
    if args.model == "knn" and args.search_space != "knn_expanded":
        raise ValueError(f"Model {args.model} is incompatible with search space {args.search_space}")
    if args.model == "svm" and args.search_space != "svm_expanded":
        raise ValueError(f"Model {args.model} is incompatible with search space {args.search_space}")
    if args.model == "mlp" and args.search_space != "mlp_expanded":
        raise ValueError(f"Model {args.model} is incompatible with search space {args.search_space}")

    logging.info("Starting fold-aggregated Ax run")
    logging.info("Arguments: %s", vars(args))

    folds = discover_all_folds(data_roots, args.protocol, args.limit_folds)
    logging.info("Discovered %d fold(s) across %d data root(s)", len(folds), len(data_roots))
    for fold in folds:
        logging.info("Fold %s root=%s train=%s test=%s", fold.name, fold.data_root, fold.train_path, fold.test_path)

    ax_client = make_ax_client(args)
    trial_rows: list[dict[str, Any]] = []
    trial_fold_rows: list[dict[str, Any]] = []

    run_start = time.time()
    for trial_number in range(args.num_trials):
        parameters, ax_trial_index = ax_client.get_next_trial()
        logging.info("Trial %d Ax index %s parameters=%s", trial_number, ax_trial_index, parameters)

        fold_results = []
        for fold in folds:
            row = evaluate_one_fold(
                fold,
                parameters,
                model_name=args.model,
                random_seed=args.random_seed,
                n_estimators=args.n_estimators,
                learning_rate=args.learning_rate,
                subsample=args.subsample,
                n_jobs=args.n_jobs,
            )
            row.update(
                {
                    "trial_number": trial_number,
                    "ax_trial_index": ax_trial_index,
                    "protocol": args.protocol,
                    "experiment_name": args.experiment_name,
                }
            )
            fold_results.append(row)
            logging.info(
                "Trial %d fold %s accuracy=%.6f balanced_accuracy=%.6f seconds=%.2f",
                trial_number,
                row["fold_name"],
                row["accuracy"],
                row["balanced_accuracy"],
                row["seconds"],
            )

        aggregate_score = float(np.mean([row[args.metric] for row in fold_results]))
        mean_accuracy = float(np.mean([row["accuracy"] for row in fold_results]))
        mean_balanced_accuracy = float(np.mean([row["balanced_accuracy"] for row in fold_results]))

        ax_client.complete_trial(
            trial_index=ax_trial_index,
            raw_data={args.metric: aggregate_score},
        )

        trial_fold_rows.extend(fold_results)
        trial_row = {
            "trial_number": trial_number,
            "ax_trial_index": ax_trial_index,
            **flatten_parameters(parameters),
            "objective_metric": args.metric,
            "objective_value": aggregate_score,
            "mean_accuracy": mean_accuracy,
            "mean_balanced_accuracy": mean_balanced_accuracy,
            "n_folds": len(fold_results),
            "n_data_roots": len({row["data_root_name"] for row in fold_results}),
            "protocol": args.protocol,
            "experiment_name": args.experiment_name,
        }
        trial_rows.append(trial_row)
        logging.info("Trial %d aggregate %s=%.6f", trial_number, args.metric, aggregate_score)

        write_csv(output_dir / "trials.csv", trial_rows)
        write_csv(output_dir / "trial_fold_results.csv", trial_fold_rows)

    best_parameters, best_values = ax_client.get_best_parameters()
    best_trial = max(trial_rows, key=lambda row: row["objective_value"])
    best_fold_rows = [
        row for row in trial_fold_rows if row["trial_number"] == best_trial["trial_number"]
    ]

    summary = {
        "experiment_name": args.experiment_name,
        "protocol": args.protocol,
        "data_root": str(data_roots[0]) if len(data_roots) == 1 else None,
        "data_roots": [str(path) for path in data_roots],
        "n_data_roots": len(data_roots),
        "output_dir": str(output_dir),
        "num_trials": args.num_trials,
        "n_folds": len(folds),
        "model": args.model,
        "search_space": args.search_space,
        "objective_metric": args.metric,
        "best_parameters_from_ax": best_parameters,
        "best_values_from_ax": str(best_values),
        "best_trial_by_recorded_objective": best_trial,
        "total_seconds": float(time.time() - run_start),
        "fixed_model_config": {
            "n_estimators": args.n_estimators,
            "learning_rate": args.learning_rate,
            "subsample": args.subsample,
            "random_seed": args.random_seed,
        },
    }

    write_csv(output_dir / "best_trial_fold_results.csv", best_fold_rows)
    write_json(output_dir / "best_hyperparameters.json", best_parameters)
    write_json(output_dir / "summary.json", summary)
    (output_dir / "summary.txt").write_text(
        "\n".join(
            [
                f"experiment_name: {args.experiment_name}",
                f"protocol: {args.protocol}",
                f"model: {args.model}",
                f"search_space: {args.search_space}",
                f"data_root: {data_roots[0] if len(data_roots) == 1 else 'multiple'}",
                f"data_roots: {[str(path) for path in data_roots]}",
                f"num_trials: {args.num_trials}",
                f"n_folds: {len(folds)}",
                f"objective_metric: {args.metric}",
                f"best_parameters: {best_parameters}",
                f"best_objective_value: {best_trial['objective_value']}",
                f"best_mean_accuracy: {best_trial['mean_accuracy']}",
                f"best_mean_balanced_accuracy: {best_trial['mean_balanced_accuracy']}",
                f"total_seconds: {summary['total_seconds']}",
            ]
        )
        + "\n"
    )
    logging.info("Finished. Best trial: %s", best_trial)
    logging.info("Wrote outputs to %s", output_dir)


if __name__ == "__main__":
    main()
