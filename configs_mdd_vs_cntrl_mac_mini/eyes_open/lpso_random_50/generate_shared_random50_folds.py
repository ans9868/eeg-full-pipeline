#!/usr/bin/env python3
"""
Preview or export the shared random-50 LPSO fold banks for the cleaned
eyes-closed MDD-vs-control dataset.

This helper is intentionally standard-library only so it can run even when
`config-maker.py` itself cannot be imported due to interactive dependencies.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from typing import Dict, Iterable, List


DEFAULT_DATASET_ROOT = Path("/Volumes/CrucialX6/Home/bigData/4244171_normalized/BIDS")
DEFAULT_PARTICIPANTS = DEFAULT_DATASET_ROOT / "participants.tsv"
DEFAULT_CONFIG_MAKER = Path(__file__).resolve().parents[3] / "config-maker.py"


def extract_function_source(script_path: Path, function_name: str) -> str:
    lines = script_path.read_text().splitlines()
    start = None
    indent = None

    for idx, line in enumerate(lines):
        if line.startswith(f"def {function_name}("):
            start = idx
            indent = len(line) - len(line.lstrip(" "))
            break

    if start is None:
        raise ValueError(f"Function not found: {function_name}")

    end = len(lines)
    for idx in range(start + 1, len(lines)):
        line = lines[idx]
        stripped = line.strip()
        if not stripped:
            continue
        current_indent = len(line) - len(line.lstrip(" "))
        if current_indent <= indent and line.startswith("def "):
            end = idx
            break

    return "\n".join(lines[start:end])


def build_group_paths(
    participants_tsv: Path, dataset_root: Path, condition: str
) -> Dict[str, List[str]]:
    if condition not in {"eyesclosed", "eyesopen"}:
        raise ValueError(f"Unsupported condition: {condition}")

    availability_col = f"has_{condition}"
    groups: Dict[str, List[str]] = {"mdd": [], "cntrl": []}

    with participants_tsv.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            participant_id = row["participant_id"].strip()
            group = row["group"].strip().lower()
            available = row[availability_col].strip().lower() == "yes"
            if not available:
                continue

            if group == "control":
                target_group = "cntrl"
            elif group == "mdd":
                target_group = "mdd"
            else:
                continue

            eeg_path = (
                dataset_root
                / participant_id
                / "eeg"
                / f"{participant_id}_task-{condition}_eeg.edf"
            )
            groups[target_group].append(str(eeg_path))

    return groups


def generate_random_balanced_folds(
    groups: Dict[str, List[str]],
    fold_size: int,
    folds_per_size: int,
    random_seed: int,
) -> List[List[str]]:
    if fold_size % len(groups) != 0:
        raise ValueError(
            f"fold_size={fold_size} must be evenly divisible by num_groups={len(groups)}"
        )

    per_group = fold_size // len(groups)
    rng = random.Random(random_seed)

    for group_name, paths in groups.items():
        if len(paths) < per_group:
            raise ValueError(
                f"group {group_name} has {len(paths)} paths, needs at least {per_group}"
            )

    folds: List[List[str]] = []
    ordered_group_names = list(groups.keys())

    for _ in range(folds_per_size):
        fold: List[str] = []
        for group_name in ordered_group_names:
            selected = rng.sample(groups[group_name], per_group)
            fold.extend(selected)
        folds.append(fold)

    return folds


def validate_folds(
    folds: Iterable[List[str]], groups: Dict[str, List[str]], fold_size: int
) -> Dict[str, object]:
    group_sets = {name: set(paths) for name, paths in groups.items()}
    per_group_expected = fold_size // len(groups)
    normalized = []
    duplicate_within_fold = 0
    unbalanced_folds = 0

    for fold in folds:
        if len(set(fold)) != len(fold):
            duplicate_within_fold += 1

        counts = {}
        for name, path_set in group_sets.items():
            counts[name] = sum(1 for path in fold if path in path_set)

        if any(count != per_group_expected for count in counts.values()):
            unbalanced_folds += 1

        normalized.append(tuple(sorted(fold)))

    return {
        "total_folds": len(normalized),
        "unique_folds": len(set(normalized)),
        "duplicate_within_fold_count": duplicate_within_fold,
        "unbalanced_fold_count": unbalanced_folds,
    }


def build_lpso_metadata(
    groups: Dict[str, List[str]],
    fold_size: int,
    folds_per_size: int,
    random_seed: int,
) -> Dict[str, object]:
    return {
        "total_folds": folds_per_size,
        "subjects_per_group": fold_size,
        "subjects_per_group_per_fold": fold_size // len(groups),
        "total_subjects": sum(len(paths) for paths in groups.values()),
        "groups": list(groups.keys()),
        "num_groups": len(groups),
        "fold_generation_method": "random_sampling",
        "fold_sizes": [fold_size],
        "folds_per_size": folds_per_size,
        "balance_by_group": True,
        "random_seed": random_seed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate shared random-50 LPSO fold banks.")
    parser.add_argument("--participants-tsv", type=Path, default=DEFAULT_PARTICIPANTS)
    parser.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET_ROOT)
    parser.add_argument("--condition", default="eyesopen", choices=["eyesclosed", "eyesopen"])
    parser.add_argument("--random-seed", type=int, default=42)
    parser.add_argument("--fold-sizes", type=int, nargs="+", default=[2, 6])
    parser.add_argument("--folds-per-size", type=int, default=50)
    parser.add_argument("--show-config-maker-source", action="store_true")
    parser.add_argument("--config-maker-path", type=Path, default=DEFAULT_CONFIG_MAKER)
    parser.add_argument("--write-json", type=Path, default=None)
    args = parser.parse_args()

    if args.show_config_maker_source:
        print(f"=== {args.config_maker_path} ===")
        for function_name in ("generate_lpso_folds", "select_test_subjects_automatically"):
            print()
            print(f"--- {function_name} ---")
            print(extract_function_source(args.config_maker_path, function_name))

    groups = build_group_paths(args.participants_tsv, args.dataset_root, args.condition)

    print("Subject pool:")
    for group_name, paths in groups.items():
        print(f"  {group_name}: {len(paths)}")

    payload: Dict[str, object] = {
        "condition": args.condition,
        "random_seed": args.random_seed,
        "groups": groups,
        "shared_folds": {},
    }

    for fold_size in args.fold_sizes:
        folds = generate_random_balanced_folds(
            groups=groups,
            fold_size=fold_size,
            folds_per_size=args.folds_per_size,
            random_seed=args.random_seed,
        )
        validation = validate_folds(folds, groups, fold_size)
        metadata = build_lpso_metadata(
            groups=groups,
            fold_size=fold_size,
            folds_per_size=args.folds_per_size,
            random_seed=args.random_seed,
        )

        key = f"L{fold_size}"
        payload["shared_folds"][key] = {
            "lpso_folds": folds,
            "lpso_metadata": metadata,
            "validation": validation,
        }

        print()
        print(f"{key}:")
        print(f"  folds: {len(folds)}")
        print(f"  first fold size: {len(folds[0]) if folds else 0}")
        print(f"  validation: {validation}")
        if folds:
            print("  first fold preview:")
            for path in folds[0]:
                print(f"    - {path}")

    if args.write_json:
        args.write_json.write_text(json.dumps(payload, indent=2))
        print()
        print(f"Wrote shared fold payload to {args.write_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
