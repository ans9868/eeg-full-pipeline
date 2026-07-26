#!/usr/bin/env python3
"""Generate true LOSO AD/CN configs for classical-ML rebuttal runs."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parents[2]
OUT_DIR = ROOT / "yaml_plan" / "loso_classical"
OUTPUTS = ROOT / "outputs"

BASE_CONFIGS = {
    "anova": PROJECT_ROOT / "configs_ad_vs_cntrl_HPC" / "lpso_random_50" / "ANOVA_L_6_ad_cntrl_random50.yaml",
    "pca": PROJECT_ROOT / "configs_ad_vs_cntrl_HPC" / "lpso_random_50" / "PCA_L_6_ad_cntrl_random50.yaml",
}


def subject_sort_key(path: str) -> int:
    match = re.search(r"sub-(\d+)", path)
    if not match:
        raise ValueError(f"Could not extract subject id from path: {path}")
    return int(match.group(1))


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return yaml.safe_load(f)


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def all_subject_paths(config: dict[str, Any]) -> list[str]:
    groups = config["data_input"]["groups"]
    paths: list[str] = []
    for group_name in sorted(groups):
        paths.extend(groups[group_name])
    return sorted(paths, key=subject_sort_key)


def make_loso_config(feature_name: str, base_path: Path) -> Path:
    config = load_yaml(base_path)
    subjects = all_subject_paths(config)
    folds = [[path] for path in subjects]
    project_name = f"LOSO_{feature_name.upper()}_ad_cntrl_65fold_v1"

    project = config.setdefault("project", {})
    project["name"] = project_name
    project["config_name"] = f"{project_name}.yaml"
    project["random_seed"] = 42
    project["slurm_options"] = {
        "build": "--time=00:20:00 --mem=16G --cpus-per-task=2 --account=torch_pr_60_general",
        "pyspark": "--time=08:00:00 --mem=56G --cpus-per-task=12 --account=torch_pr_60_general",
        "ray": "--time=00:20:00 --mem=16G --cpus-per-task=2 --account=torch_pr_60_general",
    }

    data_input = config.setdefault("data_input", {})
    data_input["reuse_processed_subjects"] = "Yes"
    data_input["save_processed_subjects"] = "Yes"
    data_input["reuse_transformed"] = "No"
    data_input["save_transformed"] = "Yes"
    data_input["reuse_transformed_across_experiments"] = "No"
    data_input["reuse_processed_subjects_across_experiments"] = "Yes"

    strategy = config.setdefault("data_transformation_strategy", {})
    strategy["strategy"] = (
        "LPSO (Leave-P-Subjects-Out) (inter subject split) - systematic cross-validation "
        "(recommended for small datasets)"
    )
    strategy["lpso_subjects_per_group"] = 1
    strategy["uneven_handling"] = "none"
    strategy["lpso_folds"] = folds
    strategy["use_lpso"] = True
    strategy["leaky_lpso"] = False
    strategy["lpso_metadata"] = {
        "total_folds": len(folds),
        "subjects_per_group": 1,
        "total_subjects": len(subjects),
        "groups": sorted(config["data_input"]["groups"]),
        "num_groups": len(config["data_input"]["groups"]),
        "fold_generation_method": "deterministic_leave_one_subject_out",
        "random_seed": 42,
        "note": "Each fold holds out exactly one subject; use pooled or subject-majority metrics across all folds.",
    }

    out = OUT_DIR / project["config_name"]
    write_yaml(out, config)
    return out


def write_manifest(paths: list[Path]) -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    manifest = OUTPUTS / "loso_classical_config_manifest.csv"
    with manifest.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "config_path",
                "project_name",
                "feature_family",
                "protocol",
                "folds",
                "held_out_subjects_per_fold",
            ],
        )
        writer.writeheader()
        for path in paths:
            config = load_yaml(path)
            writer.writerow(
                {
                    "config_path": str(path.relative_to(ROOT)),
                    "project_name": config["project"]["name"],
                    "feature_family": config["project"]["name"].split("_")[1].lower(),
                    "protocol": "loso",
                    "folds": len(config["data_transformation_strategy"]["lpso_folds"]),
                    "held_out_subjects_per_fold": 1,
                }
            )


def main() -> None:
    paths = [make_loso_config(name, path) for name, path in BASE_CONFIGS.items()]
    write_manifest(paths)
    print("Generated LOSO configs:")
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
