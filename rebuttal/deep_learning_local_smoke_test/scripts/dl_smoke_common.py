#!/usr/bin/env python3
"""Shared helpers for local deep-learning smoke tests."""

from __future__ import annotations

import csv
import json
import math
import random
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ACTIVITY_DIR / "outputs"
REPORT_PATH = ACTIVITY_DIR / "report.md"
SUMMARY_PATH = OUTPUT_DIR / "summary_metrics.csv"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        torch.use_deterministic_algorithms(False)
    except ImportError:
        pass


def require_torch():
    try:
        import torch
    except ImportError as exc:
        raise SystemExit(
            "PyTorch is required for this smoke test. Activate py-neuro-env "
            "and install torch there before rerunning."
        ) from exc
    return torch


def dense_feature(value: Any) -> np.ndarray:
    if isinstance(value, dict):
        if "values" in value and value["values"] is not None:
            arr = np.asarray(value["values"], dtype=np.float32)
        elif {"size", "indices"}.issubset(value):
            size = int(value["size"])
            arr = np.zeros(size, dtype=np.float32)
            arr[np.asarray(value["indices"], dtype=np.int64)] = np.asarray(
                value.get("values", []), dtype=np.float32
            )
        else:
            raise ValueError(f"Unsupported feature dict keys: {sorted(value)}")
    elif hasattr(value, "toArray"):
        arr = np.asarray(value.toArray(), dtype=np.float32)
    else:
        arr = np.asarray(value, dtype=np.float32)
    return np.ravel(arr).astype(np.float32)


def load_npz(path: str | Path) -> dict[str, np.ndarray]:
    data = np.load(path, allow_pickle=True)
    return {key: data[key] for key in data.files}


def encode_labels(raw_labels: list[Any]) -> tuple[np.ndarray, dict[str, int]]:
    normalized = [str(x) for x in raw_labels]
    classes = sorted(set(normalized))
    if len(classes) != 2:
        raise ValueError(f"Smoke tests require exactly two classes, found {classes}")
    mapping = {label: idx for idx, label in enumerate(classes)}
    return np.asarray([mapping[x] for x in normalized], dtype=np.int64), mapping


def split_indices(
    y: np.ndarray,
    subjects: np.ndarray,
    split: str,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    rng = np.random.default_rng(seed)
    unique_subjects = np.asarray(sorted(set(subjects.tolist())))
    if len(unique_subjects) < 3:
        raise ValueError("Need at least three unique subjects for smoke-test splits")

    if split == "subject_disjoint_smoke":
        subject_majority: dict[Any, int] = {}
        for subject in unique_subjects:
            labels = y[subjects == subject]
            subject_majority[subject] = int(Counter(labels.tolist()).most_common(1)[0][0])

        test_subjects: list[Any] = []
        for label in sorted(set(y.tolist())):
            candidates = [s for s in unique_subjects if subject_majority[s] == label]
            if candidates:
                test_subjects.append(rng.choice(candidates).item())
        if len(set(test_subjects)) < 2:
            remaining = [s for s in unique_subjects if s not in test_subjects]
            test_subjects.extend(
                rng.choice(remaining, size=2 - len(set(test_subjects)), replace=False).tolist()
            )
        test_subjects = sorted(set(test_subjects))

        test_mask = np.isin(subjects, test_subjects)
        train_idx = np.flatnonzero(~test_mask)
        test_idx = np.flatnonzero(test_mask)
    elif split == "subject_overlap_smoke":
        train_parts: list[np.ndarray] = []
        test_parts: list[np.ndarray] = []
        for label in sorted(set(y.tolist())):
            label_idx = np.flatnonzero(y == label)
            rng.shuffle(label_idx)
            n_test = max(1, int(round(len(label_idx) * 0.2)))
            test_parts.append(label_idx[:n_test])
            train_parts.append(label_idx[n_test:])
        train_idx = np.concatenate(train_parts)
        test_idx = np.concatenate(test_parts)
        rng.shuffle(train_idx)
        rng.shuffle(test_idx)
    else:
        raise ValueError(f"Unknown split: {split}")

    if len(train_idx) == 0 or len(test_idx) == 0:
        raise ValueError(f"Split {split} produced an empty train/test partition")
    if len(set(y[train_idx].tolist())) < 2:
        raise ValueError(f"Split {split} produced single-class train labels")
    if len(set(y[test_idx].tolist())) < 2:
        raise ValueError(f"Split {split} produced single-class test labels")

    train_subjects = set(subjects[train_idx].tolist())
    test_subjects = set(subjects[test_idx].tolist())
    overlap = sorted(train_subjects & test_subjects)
    if split == "subject_disjoint_smoke" and overlap:
        raise ValueError(f"Subject-disjoint split leaked subjects: {overlap}")
    if split == "subject_overlap_smoke" and not overlap:
        raise ValueError("Subject-overlap split unexpectedly has zero shared subjects")

    info = {
        "split": split,
        "seed": seed,
        "train_rows": int(len(train_idx)),
        "test_rows": int(len(test_idx)),
        "train_subject_count": int(len(train_subjects)),
        "test_subject_count": int(len(test_subjects)),
        "shared_subject_count": int(len(overlap)),
        "shared_subjects": [str(x) for x in overlap],
        "held_out_subjects": [str(x) for x in sorted(test_subjects)]
        if split == "subject_disjoint_smoke"
        else [],
    }
    return train_idx, test_idx, info


def standardize_train_test(
    x: np.ndarray, train_idx: np.ndarray, test_idx: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    train = x[train_idx].astype(np.float32)
    test = x[test_idx].astype(np.float32)
    mean = train.mean(axis=0, keepdims=True)
    std = train.std(axis=0, keepdims=True)
    std[std < 1e-6] = 1.0
    return (train - mean) / std, (test - mean) / std


def binary_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float | int]:
    y_true = y_true.astype(int)
    y_pred = y_pred.astype(int)
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    sensitivity = tp / (tp + fn) if tp + fn else 0.0
    specificity = tn / (tn + fp) if tn + fp else 0.0
    accuracy = (tp + tn) / max(1, len(y_true))
    balanced = (sensitivity + specificity) / 2.0
    return {
        "accuracy": float(accuracy),
        "balanced_accuracy": float(balanced),
        "sensitivity": float(sensitivity),
        "specificity": float(specificity),
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
    }


def subject_majority_accuracy(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    subjects: np.ndarray,
) -> float:
    correct = 0
    total = 0
    for subject in sorted(set(subjects.tolist())):
        mask = subjects == subject
        true_vote = Counter(y_true[mask].astype(int).tolist()).most_common(1)[0][0]
        pred_vote = Counter(y_pred[mask].astype(int).tolist()).most_common(1)[0][0]
        correct += int(true_vote == pred_vote)
        total += 1
    return float(correct / total) if total else 0.0


def save_run_outputs(
    run_id: str,
    metrics: dict[str, Any],
    predictions: list[dict[str, Any]],
    split_info: dict[str, Any],
    training_log: dict[str, Any],
    data_meta: dict[str, Any],
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics_path = OUTPUT_DIR / f"{run_id}_metrics.csv"
    predictions_path = OUTPUT_DIR / f"{run_id}_predictions.csv"
    split_path = OUTPUT_DIR / f"{run_id}_split_subjects.json"
    log_path = OUTPUT_DIR / f"{run_id}_training_log.json"

    with metrics_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(metrics.keys()))
        writer.writeheader()
        writer.writerow(metrics)

    with predictions_path.open("w", newline="") as fh:
        fieldnames = ["row_index", "SubjectID", "EpochID", "true_label", "pred_label", "prob_class_1"]
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(predictions)

    split_path.write_text(json.dumps(split_info, indent=2, sort_keys=True) + "\n")
    log_path.write_text(json.dumps(training_log, indent=2, sort_keys=True) + "\n")
    refresh_summary_and_report(data_meta)


def refresh_summary_and_report(data_meta: dict[str, Any]) -> None:
    metric_files = sorted(OUTPUT_DIR.glob("*_metrics.csv"))
    rows: list[dict[str, str]] = []
    for path in metric_files:
        if path.name == "summary_metrics.csv":
            continue
        with path.open(newline="") as fh:
            reader = csv.DictReader(fh)
            rows.extend(reader)

    if rows:
        fieldnames = list(rows[0].keys())
        with SUMMARY_PATH.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    lines = [
        "# Deep Learning Local Smoke Test Report",
        "",
        "These local runs validate that the EEGNet-style and transformer-style neural model code paths execute end-to-end on the existing processed EEG feature artifacts. They are smoke tests, not final rebuttal-grade neural baseline results. Rebuttal claims about neural architectures should use only full-scale HPC/GPU runs with the intended data and split definitions.",
        "",
        f"Last refreshed: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Data",
        "",
    ]
    for key in ["source", "rows", "unique_subjects", "class_counts", "feature_dim", "label_mapping"]:
        if key in data_meta:
            lines.append(f"- {key}: `{data_meta[key]}`")
    lines.extend(["", "## Runs", ""])
    if rows:
        for row in rows:
            lines.append(
                "- {run_id}: split `{split}`, rows train/test `{train_rows}/{test_rows}`, "
                "subjects train/test `{train_subject_count}/{test_subject_count}`, shared subjects `{shared_subject_count}`, "
                "accuracy `{accuracy}`, balanced accuracy `{balanced_accuracy}`, sensitivity `{sensitivity}`, specificity `{specificity}`".format(
                    **row
                )
            )
    else:
        lines.append("- No completed model runs yet.")
    lines.extend(
        [
            "",
            "## Integrity Checks",
            "",
            "- `subject_disjoint_smoke` is required to report zero shared train/test subjects.",
            "- `subject_overlap_smoke` is required to report at least one shared train/test subject and is the deliberately leaked control.",
            "- Metrics are engineering checks only; poor accuracy is acceptable for this local 1-2 epoch run when values are finite and outputs are written.",
            "",
            "## Container Notes",
            "",
            "No containerized execution code or dependency files were changed for this local smoke test, so no `make build` container rebuild was required.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n")


def finite_metrics(metrics: dict[str, Any]) -> None:
    for key, value in metrics.items():
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"Metric {key} is not finite: {value}")
