#!/usr/bin/env python3
"""Prepare a tiny cached NPZ dataset from processed EEG parquet features."""

from __future__ import annotations

import argparse
import json
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
        if total >= max_rows and len(labels) >= 2:
            break

    data = pd.concat(chunks, ignore_index=True)
    if len(set(str(x) for x in data["label"].tolist())) < 2:
        raise ValueError("Prepared subset is single-class after reading all available parquet files")
    return data.head(max_rows).copy()


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
