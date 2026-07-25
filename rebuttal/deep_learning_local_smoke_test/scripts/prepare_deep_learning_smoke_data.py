#!/usr/bin/env python3
"""Prepare a tiny cached NPZ dataset from processed EEG parquet features."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from dl_smoke_common import dense_feature, encode_labels


def read_processed_rows(input_dir: Path, max_rows: int) -> pd.DataFrame:
    parquet_files = sorted(input_dir.glob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError(f"No parquet files found under {input_dir}")

    chunks: list[pd.DataFrame] = []
    total = 0
    labels: set[str] = set()
    for path in parquet_files:
        df = pd.read_parquet(path, columns=["SubjectID", "EpochID", "Group", "features", "label"])
        chunks.append(df)
        total += len(df)
        labels.update(str(x) for x in df["label"].dropna().unique().tolist())
        current = pd.concat(chunks, ignore_index=True)
        label_subject_counts = (
            current.assign(_label=current["label"].astype(str), _subject=current["SubjectID"].astype(str))
            .groupby("_label")["_subject"]
            .nunique()
            .to_dict()
        )
        has_disjoint_subjects = len(labels) >= 2 and all(count >= 2 for count in label_subject_counts.values())
        if total >= max_rows and has_disjoint_subjects:
            break

    data = pd.concat(chunks, ignore_index=True)
    labels_in_data = sorted(set(str(x) for x in data["label"].tolist()))
    if len(labels_in_data) < 2:
        raise ValueError("Prepared subset is single-class after reading all available parquet files")
    if len(data) <= max_rows:
        return data.copy()

    per_class = max(1, max_rows // len(labels_in_data))
    data = data.reset_index(drop=True)
    parts: list[pd.DataFrame] = []
    for label in labels_in_data:
        label_df = data[data["label"].astype(str) == label]
        subject_parts: list[pd.DataFrame] = []
        subject_ids = sorted(label_df["SubjectID"].astype(str).unique().tolist())
        per_subject = max(1, math.ceil(per_class / len(subject_ids)))
        for offset, subject in enumerate(subject_ids):
            subject_df = label_df[label_df["SubjectID"].astype(str) == subject]
            subject_parts.append(
                subject_df.sample(n=min(per_subject, len(subject_df)), random_state=42 + offset)
            )
        class_subset = pd.concat(subject_parts)
        if len(class_subset) > per_class:
            class_subset = class_subset.sample(n=per_class, random_state=45)
        parts.append(class_subset)
    subset = pd.concat(parts)
    if len(subset) < max_rows:
        remaining = data.drop(index=subset.index)
        if len(remaining):
            needed = min(max_rows - len(subset), len(remaining))
            subset = pd.concat(
                [subset, remaining.sample(n=needed, random_state=43)]
            )
    return subset.sample(frac=1.0, random_state=44).head(max_rows).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-rows", type=int, default=512)
    args = parser.parse_args()

    df = read_processed_rows(args.input_dir, args.max_rows)
    features = [dense_feature(value) for value in df["features"].tolist()]
    lengths = {len(x) for x in features}
    if len(lengths) != 1:
        raise ValueError(f"Inconsistent feature lengths after conversion: {sorted(lengths)}")
    x = np.vstack(features).astype(np.float32)
    if not np.isfinite(x).all():
        raise ValueError("NaN/inf values appear after feature conversion")

    y, label_mapping = encode_labels(df["label"].tolist())
    subjects = df["SubjectID"].astype(str).to_numpy()
    epochs = df["EpochID"].astype(str).to_numpy()
    groups = df["Group"].astype(str).to_numpy()
    class_counts = Counter(str(x) for x in df["label"].tolist())

    meta = {
        "source": str(args.input_dir),
        "rows": int(len(df)),
        "unique_subjects": int(len(set(subjects.tolist()))),
        "class_counts": dict(sorted(class_counts.items())),
        "feature_dim": int(x.shape[1]),
        "label_mapping": label_mapping,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output,
        x=x,
        y=y,
        SubjectID=subjects,
        EpochID=epochs,
        Group=groups,
        original_label=df["label"].astype(str).to_numpy(),
        meta=json.dumps(meta, sort_keys=True),
    )
    print(json.dumps(meta, indent=2, sort_keys=True))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
