#!/usr/bin/env python3
"""
Build subject_accuracy_per_model.csv from *_per_subject_detailed.csv files.

Reads each experiment's detailed CSV (Subject, Fold, Model, Accuracy),
aggregates by (experiment, subject, model) to get median/mean accuracy and n_folds,
and writes one combined CSV for the booklet.
"""

import csv
import statistics
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "per_subject_classification_analysis"
OUTPUT_CSV = INPUT_DIR / "subject_accuracy_per_model.csv"

EXPERIMENT_PREFIXES = [
    "ANOVA_L_2_Random",
    "ANOVA_L_6_Random",
    "ANOVA_L_6_Uniform",
    "PCA_L_2_Random",
    "PCA_L_6_Random",
    "PCA_L_6_Uniform",
]


def main():
    rows = []
    for exp in EXPERIMENT_PREFIXES:
        path = INPUT_DIR / f"{exp}_per_subject_detailed.csv"
        if not path.exists():
            print(f"Skip (missing): {path.name}")
            continue
        # (subject, model) -> list of accuracies (one per fold)
        by_subject_model = defaultdict(list)
        with open(path, newline="") as f:
            r = csv.DictReader(f)
            for row in r:
                sub = row["Subject"]
                model = row["Model"]
                acc = float(row["Accuracy"])
                by_subject_model[(sub, model)].append(acc)
        for (sub, model), accs in sorted(by_subject_model.items(), key=lambda x: (int(x[0][0].split("-")[1]), x[0][1])):
            rows.append({
                "experiment": exp,
                "subject_id": sub,
                "model": model,
                "median_accuracy": round(statistics.median(accs), 4),
                "mean_accuracy": round(statistics.mean(accs), 4),
                "n_folds": len(accs),
            })
    # Sort: experiment, subject number, model
    rows.sort(key=lambda r: (r["experiment"], int(r["subject_id"].split("-")[1]), r["model"]))
    with open(OUTPUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["experiment", "subject_id", "model", "median_accuracy", "mean_accuracy", "n_folds"],
        )
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {OUTPUT_CSV} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
