#!/usr/bin/env python3
"""
Checklist validator for FTD-vs-CNTRL random LPSO config files.

Validates:
- Required config files exist
- Group paths (ftd/cntrl) match participants.tsv
- Fold count/size/balance is correct
- No duplicate folds
- Metadata consistency
- ANOVA vs PCA pair-fold consistency for same fold size

No external dependencies required.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


EXPECTED_CONFIGS: Dict[str, int] = {
    "ANOVA_L_2_FTD_C_random50.yaml": 2,
    "ANOVA_L_6_FTD_C_random50.yaml": 6,
    "PCA_L_2_FTD_C_random50.yaml": 2,
    "PCA_L_6_FTD_C_random50.yaml": 6,
}


def load_participant_paths(participants_tsv: Path, dataset_root: Path) -> Tuple[set[str], set[str]]:
    ftd_paths: set[str] = set()
    cntrl_paths: set[str] = set()
    with participants_tsv.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            participant_id = row["participant_id"].strip()
            group = row["Group"].strip()
            path = f"{dataset_root}/{participant_id}/eeg/{participant_id}_task-eyesclosed_eeg.set"
            if group == "F":
                ftd_paths.add(path)
            elif group == "C":
                cntrl_paths.add(path)
    return ftd_paths, cntrl_paths


def extract_group_paths(lines: Sequence[str]) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}
    in_groups = False
    current_group: str | None = None

    for line in lines:
        if line.startswith("  groups:"):
            in_groups = True
            current_group = None
            continue

        if not in_groups:
            continue

        if line.startswith("  ") and not line.startswith("    "):
            break

        stripped = line.strip()
        if line.startswith("    ") and stripped.endswith(":") and not stripped.startswith("-"):
            current_group = stripped[:-1]
            groups.setdefault(current_group, [])
            continue

        if line.startswith("    - ") and current_group:
            groups[current_group].append(line[len("    - ") :].strip())

    return groups


def extract_lpso_folds(lines: Sequence[str]) -> List[List[str]]:
    in_strategy = False
    in_folds = False
    current_fold: List[str] | None = None
    folds: List[List[str]] = []

    for line in lines:
        if line.startswith("data_transformation_strategy:"):
            in_strategy = True
            continue

        if not in_strategy:
            continue

        if line.startswith("pyspark:"):
            break

        if line.startswith("  lpso_folds:"):
            in_folds = True
            continue

        if not in_folds:
            continue

        if line.startswith("  lpso_metadata:"):
            break

        if line.startswith("  - - "):
            current_fold = [line[len("  - - ") :].strip()]
            folds.append(current_fold)
            continue

        if line.startswith("    - ") and current_fold is not None:
            current_fold.append(line[len("    - ") :].strip())

    return folds


def extract_value(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def parse_fold_sizes(lines: Sequence[str]) -> List[int]:
    result: List[int] = []
    in_fold_sizes = False
    for line in lines:
        if line.startswith("    fold_sizes:"):
            in_fold_sizes = True
            continue
        if in_fold_sizes:
            if line.startswith("    - "):
                try:
                    result.append(int(line[len("    - ") :].strip()))
                except ValueError:
                    pass
                continue
            # end of fold_sizes block
            if line.startswith("    ") and line.strip().endswith(":"):
                in_fold_sizes = False
            elif line.startswith("  "):
                in_fold_sizes = False
    return result


def validate_one_config(
    cfg_path: Path,
    expected_fold_size: int,
    expected_ftd: set[str],
    expected_cntrl: set[str],
) -> Tuple[List[str], List[str], List[Tuple[str, ...]]]:
    errors: List[str] = []
    warnings: List[str] = []
    text = cfg_path.read_text()
    lines = text.splitlines()

    strategy = extract_value(text, r"^  strategy:\s*(.+)$")
    if not strategy or "LPSO (Leave-P-Subjects-Out)" not in strategy:
        errors.append("strategy is not LPSO")

    use_lpso = extract_value(text, r"^  use_lpso:\s*(.+)$")
    if not use_lpso or use_lpso.lower() != "true":
        errors.append("use_lpso is not true")

    groups = extract_group_paths(lines)
    keys = set(groups.keys())
    if keys != {"ftd", "cntrl"}:
        errors.append(f"group keys must be {{ftd, cntrl}}, found {sorted(keys)}")
        return errors, warnings, []

    ftd_paths = groups["ftd"]
    cntrl_paths = groups["cntrl"]

    if set(ftd_paths) != expected_ftd:
        missing = sorted(expected_ftd - set(ftd_paths))
        extra = sorted(set(ftd_paths) - expected_ftd)
        errors.append(f"ftd path mismatch (missing={len(missing)}, extra={len(extra)})")
    if set(cntrl_paths) != expected_cntrl:
        missing = sorted(expected_cntrl - set(cntrl_paths))
        extra = sorted(set(cntrl_paths) - expected_cntrl)
        errors.append(f"cntrl path mismatch (missing={len(missing)}, extra={len(extra)})")

    if len(ftd_paths) != len(set(ftd_paths)):
        errors.append("duplicate paths in ftd group")
    if len(cntrl_paths) != len(set(cntrl_paths)):
        errors.append("duplicate paths in cntrl group")

    all_paths = set(ftd_paths) | set(cntrl_paths)
    missing_files = [p for p in sorted(all_paths) if not Path(p).exists()]
    if missing_files:
        errors.append(f"{len(missing_files)} group paths do not exist on disk")

    folds = extract_lpso_folds(lines)
    if len(folds) != 50:
        errors.append(f"lpso_folds must have 50 folds, found {len(folds)}")

    normalized_folds: List[Tuple[str, ...]] = []
    fold_subject_counts: Counter[str] = Counter()
    expected_half = expected_fold_size // 2

    for idx, fold in enumerate(folds, start=1):
        if len(fold) != expected_fold_size:
            errors.append(f"fold {idx} has size {len(fold)} (expected {expected_fold_size})")
            continue

        if len(set(fold)) != len(fold):
            errors.append(f"fold {idx} has duplicate subject path(s)")

        n_ftd = sum(1 for path in fold if path in expected_ftd)
        n_cntrl = sum(1 for path in fold if path in expected_cntrl)
        unknown = len(fold) - n_ftd - n_cntrl
        if unknown:
            errors.append(f"fold {idx} contains {unknown} unknown path(s)")
        if n_ftd != expected_half or n_cntrl != expected_half:
            errors.append(
                f"fold {idx} is unbalanced (ftd={n_ftd}, cntrl={n_cntrl}, expected {expected_half}/{expected_half})"
            )

        normalized = tuple(sorted(fold))
        normalized_folds.append(normalized)
        for path in fold:
            fold_subject_counts[path] += 1

    unique_folds = set(normalized_folds)
    if len(unique_folds) != len(normalized_folds):
        errors.append(
            f"duplicate folds detected ({len(normalized_folds) - len(unique_folds)} duplicates)"
        )

    # Metadata checks
    total_folds = extract_value(text, r"^    total_folds:\s*(\d+)\s*$")
    if total_folds and int(total_folds) != 50:
        errors.append(f"lpso_metadata.total_folds is {total_folds}, expected 50")

    fold_sizes = parse_fold_sizes(lines)
    if fold_sizes and fold_sizes != [expected_fold_size]:
        errors.append(f"lpso_metadata.fold_sizes is {fold_sizes}, expected [{expected_fold_size}]")

    folds_per_size = extract_value(text, r"^    folds_per_size:\s*(\d+)\s*$")
    if folds_per_size and int(folds_per_size) != 50:
        errors.append(f"lpso_metadata.folds_per_size is {folds_per_size}, expected 50")

    random_seed = extract_value(text, r"^    random_seed:\s*(\d+)\s*$")
    if random_seed and int(random_seed) != 42:
        warnings.append(f"lpso_metadata.random_seed is {random_seed} (expected 42)")

    balance_by_group = extract_value(text, r"^    balance_by_group:\s*(\w+)\s*$")
    if balance_by_group and balance_by_group.lower() != "true":
        errors.append(f"lpso_metadata.balance_by_group is {balance_by_group}, expected true")

    generation_method = extract_value(text, r"^    fold_generation_method:\s*(\w+)\s*$")
    if generation_method and generation_method != "random_sampling":
        warnings.append(
            f"lpso_metadata.fold_generation_method is {generation_method} (expected random_sampling)"
        )

    if fold_subject_counts:
        counts = list(fold_subject_counts.values())
        warnings.append(
            f"subject appearance range across folds: min={min(counts)}, max={max(counts)}, mean={sum(counts)/len(counts):.2f}"
        )

    return errors, warnings, normalized_folds


def main() -> int:
    parser = argparse.ArgumentParser(description="Checklist validator for FTD-vs-CNTRL random LPSO configs.")
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path("configs_ftd_vs_cntrl/lpso_random_50"),
        help="Directory containing the 4 target YAML files.",
    )
    parser.add_argument(
        "--participants-tsv",
        type=Path,
        default=Path("/Volumes/CrucialX6/Home/projects/eeg-ds004504/ds004504/participants.tsv"),
        help="participants.tsv for ds004504.",
    )
    parser.add_argument(
        "--dataset-root",
        type=Path,
        default=Path("/Volumes/CrucialX6/Home/projects/eeg-ds004504/ds004504"),
        help="Dataset root used to construct expected EEG .set paths.",
    )
    args = parser.parse_args()

    if not args.config_dir.exists():
        print(f"ERROR: config directory not found: {args.config_dir}")
        return 1
    if not args.participants_tsv.exists():
        print(f"ERROR: participants.tsv not found: {args.participants_tsv}")
        return 1

    expected_ftd, expected_cntrl = load_participant_paths(args.participants_tsv, args.dataset_root)
    print(f"Expected groups from participants.tsv: ftd={len(expected_ftd)}, cntrl={len(expected_cntrl)}")

    overall_errors = 0
    folds_by_file: Dict[str, List[Tuple[str, ...]]] = {}

    present_files = sorted(path.name for path in args.config_dir.glob("*.yaml"))
    missing_files = sorted(set(EXPECTED_CONFIGS) - set(present_files))
    extra_files = sorted(set(present_files) - set(EXPECTED_CONFIGS))
    if missing_files:
        print(f"ERROR: missing required config files: {missing_files}")
        overall_errors += len(missing_files)
    if extra_files:
        print(f"WARN: extra yaml files present (ignored): {extra_files}")

    for file_name, fold_size in EXPECTED_CONFIGS.items():
        cfg_path = args.config_dir / file_name
        if not cfg_path.exists():
            continue

        errors, warnings, normalized_folds = validate_one_config(
            cfg_path, fold_size, expected_ftd, expected_cntrl
        )
        folds_by_file[file_name] = normalized_folds

        print(f"\n[{file_name}]")
        if errors:
            for item in errors:
                print(f"  ERROR: {item}")
            overall_errors += len(errors)
        else:
            print("  OK: core checklist checks passed")
        for item in warnings:
            print(f"  NOTE: {item}")

    # Cross-file consistency checks
    l2_a = folds_by_file.get("ANOVA_L_2_FTD_C_random50.yaml")
    l2_p = folds_by_file.get("PCA_L_2_FTD_C_random50.yaml")
    if l2_a is not None and l2_p is not None:
        if l2_a != l2_p:
            print("\nERROR: L2 fold list mismatch between ANOVA and PCA configs")
            overall_errors += 1
        else:
            print("\nOK: L2 fold list is identical between ANOVA and PCA")

    l6_a = folds_by_file.get("ANOVA_L_6_FTD_C_random50.yaml")
    l6_p = folds_by_file.get("PCA_L_6_FTD_C_random50.yaml")
    if l6_a is not None and l6_p is not None:
        if l6_a != l6_p:
            print("ERROR: L6 fold list mismatch between ANOVA and PCA configs")
            overall_errors += 1
        else:
            print("OK: L6 fold list is identical between ANOVA and PCA")

    print(f"\nChecklist result: {'PASS' if overall_errors == 0 else 'FAIL'}")
    return 0 if overall_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
