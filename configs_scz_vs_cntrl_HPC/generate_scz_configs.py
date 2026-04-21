#!/usr/bin/env python3
"""
Generate YAML configs for schizophrenia vs control (N=28, eyes-closed).

Dataset: EEG-in-schizophrenia
  cntrl: sub-001 .. sub-014  (h01-h14)
  scz:   sub-015 .. sub-028  (s01-s14)
  Task:  eyesclosed
  Format: .edf

Output layout:
  configs_scz_vs_cntrl_HPC/
    lpso_random_50/
      ANOVA_L_6_scz_cntrl_random50.yaml
      ANOVA_L_2_scz_cntrl_random50.yaml
      PCA_L_6_scz_cntrl_random50.yaml
      PCA_L_2_scz_cntrl_random50.yaml
    anova_w_c/
      ANOVA_W_C_scz_cntrl_seed42.yaml  ...  seed51.yaml
    pca_w_c/
      PCA_W_C_scz_cntrl_seed42.yaml    ...  seed51.yaml

LPSO fold banks (P=6 and P=2) are generated once with seed=42
and shared between ANOVA and PCA configs of the same P.
"""

import random
from pathlib import Path
from typing import Dict, List

import yaml

# ── Paths ──────────────────────────────────────────────────────────────────────
BIDS_ROOT  = "/scratch/ans9868/EEG-in-schizophrenia/BIDS"
TASK       = "rest"
OUT_DIR    = Path(__file__).parent

SLURM = {
    "build":   "--time=00:15:00 --mem=12G  --cpus-per-task=2  --account=torch_pr_60_general",
    "pyspark": "--time=00:30:00 --mem=56G  --cpus-per-task=12 --account=torch_pr_60_general",
    "ray":     "--time=00:30:00 --mem=56G  --cpus-per-task=12 --account=torch_pr_60_general",
}

# ── Subject lists ──────────────────────────────────────────────────────────────
def edf_path(sub_id: str) -> str:
    return f"{BIDS_ROOT}/{sub_id}/eeg/{sub_id}_task-{TASK}_eeg.edf"

GROUPS: Dict[str, List[str]] = {
    "cntrl": [edf_path(f"sub-{i:03d}") for i in range(1,  15)],   # sub-001..sub-014
    "scz":   [edf_path(f"sub-{i:03d}") for i in range(15, 29)],   # sub-015..sub-028
}

# ── Fold generation ────────────────────────────────────────────────────────────
def make_folds(fold_size: int, n_folds: int = 50, seed: int = 42) -> List[List[str]]:
    """Generate n_folds unique balanced LPSO folds. fold_size subjects drawn equally per group.
    Keeps sampling until n_folds distinct folds are collected (no duplicate fold compositions).
    """
    per_group = fold_size // len(GROUPS)
    rng = random.Random(seed)
    seen: set = set()
    folds: List[List[str]] = []
    max_attempts = n_folds * 1000
    attempts = 0
    while len(folds) < n_folds:
        if attempts >= max_attempts:
            raise RuntimeError(
                f"Could not generate {n_folds} unique folds for fold_size={fold_size} "
                f"after {max_attempts} attempts (pool too small?)"
            )
        fold = []
        for paths in GROUPS.values():
            fold.extend(rng.sample(paths, per_group))
        key = tuple(sorted(fold))
        if key not in seen:
            seen.add(key)
            folds.append(fold)
        attempts += 1
    return folds

def lpso_metadata(fold_size: int, n_folds: int = 50, seed: int = 42) -> dict:
    return {
        "total_folds":                n_folds,
        "subjects_per_group":         fold_size,
        "subjects_per_group_per_fold": fold_size // len(GROUPS),
        "total_subjects":             sum(len(v) for v in GROUPS.values()),
        "groups":                     list(GROUPS.keys()),
        "num_groups":                 len(GROUPS),
        "fold_generation_method":     "random_sampling",
        "fold_sizes":                 [fold_size],
        "folds_per_size":             n_folds,
        "balance_by_group":           True,
        "random_seed":                seed,
    }

# ── Shared config blocks ───────────────────────────────────────────────────────
PREPROCESSING = {
    "bands": {
        "Delta": [0.5, 4], "Theta": [4, 8],
        "Alpha": [8, 12],  "Beta":  [12, 30],
    },
    "window_size": 3.0,
    "sliding_window": 0.5,
    "reject_by_annotation": "Yes",
    "normalize_psd": "Yes",
    "use_epoch_rejection": "Yes",
    "epoch_rejection": {"reject": 800.0, "flat": 0.3},
    "extreme_datapoint_removal": None,
}

FEATURE_EXTRACTION = {
    "method": "welch",
    "features": {
        "per_channel_across_bands": ["band_power", "none"],
        "per_channel_per_band":     ["relative_band_power"],
    },
    "show_intermediate_results": "No",
    "show_intermediate_counts":  "No",
    "output_format": "ml",
}

FEATURE_TRANSFORMATION_ANOVA = {
    "transformations":         ["ANOVA F-test", "MinMax scaler"],
    "synthetic":               "None",
    "minmax_range":            [-1.0, 1.0],
    "anova_label_column":      "Group",
    "anova_label_type":        "categorical",
    "anova_selection_mode":    "fwe",
    "anova_selection_threshold": 0.05,
}

FEATURE_TRANSFORMATION_PCA = {
    "transformations": ["Z-score standardization", "PCA (retain 95% variance)"],
    "synthetic":       "None",
}

PYSPARK_LPSO = {"master": 12, "driver_memory": 36, "executor_memory": 36,
                "executor_cores": 12, "shuffle_partitions": 24}
PYSPARK_WC   = {"master": 12, "driver_memory": 36, "executor_memory": 36,
                "executor_cores": 12, "shuffle_partitions": 24}

RAY_GRID = {
    "search_strategies": ["grid_search"],
    "grid_search": {
        "models": ["XGBoost", "MLP (Neural Network)", "KNN", "SVM"],
        "model_configs": {
            "XGBoost": {
                "use_default": False,
                "hyperparameters": {
                    "n_estimators": ["100"],
                    "max_depth": ["3", "6", "9"],
                    "learning_rate": ["0.2"],
                    "subsample": ["0.7"],
                },
            },
            "MLP (Neural Network)": {
                "use_default": False,
                "hyperparameters": {
                    "hidden_layer_sizes": [[100], [150, 50], [200, 100, 50]],
                    "activation": ["tanh"],
                    "alpha": ["0.1"],
                },
            },
            "KNN": {
                "use_default": False,
                "hyperparameters": {
                    "n_neighbors": [1, 7, 15],
                    "weights": ["uniform"],
                    "metric": ["euclidean"],
                },
            },
            "SVM": {
                "use_default": False,
                "hyperparameters": {
                    "C": ["0.1"],
                    "kernel": ["linear", "rbf", "poly"],
                    "gamma": ["auto"],
                },
            },
        },
        "max_concurrent_trials": 4,
        "cv_folds": 5,
    },
    "metric": "accuracy",
    "mode": "max",
    "graph_data_visualization": {
        "save_prediction_outputs": "Yes",
        "best_models_graph": "Yes",
        "per_model_accross_hyperparameters_graph": "Yes",
        "per_model_per_hyperparameter_across_folds_graph": "Yes",
        "per_subject_analysis_graph": "Yes",
        "per_subject_top_n_models": 5,
        "per_subject_hyperparameter_analysis": "Yes",
    },
    "resources": {
        "num_cpus": 8, "memory_gb": 16,
        "object_store_memory_gb": 6, "num_gpus": 0,
    },
}

DATA_INPUT = {
    "groups": GROUPS,
    "reuse_processed_subjects": "Yes",
    "save_processed_subjects": "Yes",
    "reuse_transformed": "No",
    "save_transformed": "Yes",
    "reuse_transformed_across_experiments": "No",
    "reuse_processed_subjects_across_experiments": "Yes",
}

# ── Writers ────────────────────────────────────────────────────────────────────
def write_yaml(path: Path, cfg: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(cfg, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"  wrote {path.relative_to(OUT_DIR.parent)}")


def make_lpso_config(name: str, feature_transform: dict,
                     folds: List[List[str]], metadata: dict) -> dict:
    config_filename = f"config_{name}.yaml"
    return {
        "project": {
            "name": name,
            "output_dir": "./data",
            "experiment_type": "ML Classification",
            "subjects_or_events": "subjects",
            "deployment_method": "Singularity with Slurm",
            "random_seed": 42,
            "expose_ports": "No",
            "config_name": config_filename,
            "slurm_options": SLURM,
        },
        "data_input": DATA_INPUT,
        "preprocessing": PREPROCESSING,
        "feature_extraction": FEATURE_EXTRACTION,
        "feature_transformation": feature_transform,
        "data_transformation_strategy": {
            "strategy": "LPSO (Leave-P-Subjects-Out) (inter subject split) - systematic cross-validation (recommended for small datasets)",
            "lpso_subjects_per_group": metadata["subjects_per_group"],
            "uneven_handling": "cutoff",
            "lpso_folds": folds,
            "lpso_metadata": metadata,
            "use_lpso": True,
            "leaky_lpso": False,
            "shuffle_transformed_data": "Yes",
        },
        "pyspark": PYSPARK_LPSO,
        "ray": RAY_GRID,
    }


def make_wc_config(name: str, feature_transform: dict, seed: int) -> dict:
    config_filename = f"config_{name}.yaml"
    return {
        "project": {
            "name": name,
            "output_dir": "./data",
            "experiment_type": "ML Classification",
            "subjects_or_events": "subjects",
            "deployment_method": "Singularity with Slurm",
            "random_seed": seed,
            "expose_ports": "No",
            "config_name": config_filename,
            "slurm_options": SLURM,
        },
        "data_input": DATA_INPUT,
        "preprocessing": PREPROCESSING,
        "feature_extraction": FEATURE_EXTRACTION,
        "feature_transformation": feature_transform,
        "data_transformation_strategy": {
            "strategy": "Within-subject (intra subject split) train/test split (80/20 per subject) - each subject contributes to both train and test",
            "intra_test_train_split": {
                "train_ratio": 0.8,
                "random_seed": seed,
                "split_method": "random",
            },
            "shuffle_transformed_data": "Yes",
        },
        "pyspark": PYSPARK_WC,
        "ray": RAY_GRID,
    }


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    print("Generating fold banks ...")
    fold_bank = {
        6: make_folds(fold_size=6),   # 3 per group, 50 folds
        2: make_folds(fold_size=2),   # 1 per group, 50 folds
    }
    for p, folds in fold_bank.items():
        print(f"  P={p}: {len(folds)} folds, {len(folds[0])} subjects/fold")

    # ── LPSO configs (4 total) ────────────────────────────────────────────────
    print("\nLPSO configs ...")
    lpso_dir = OUT_DIR / "lpso_random_50"
    for p in (6, 2):
        folds = fold_bank[p]
        meta  = lpso_metadata(fold_size=p)
        for prefix, ft in (("ANOVA", FEATURE_TRANSFORMATION_ANOVA),
                           ("PCA",   FEATURE_TRANSFORMATION_PCA)):
            name = f"{prefix}_L_{p}_scz_cntrl_random50"
            cfg  = make_lpso_config(name, ft, folds, meta)
            write_yaml(lpso_dir / f"{name}.yaml", cfg)

    # ── W_C seed configs (20 total: 10 ANOVA + 10 PCA) ───────────────────────
    print("\nW_C seed configs ...")
    for prefix, subdir, ft in (
        ("ANOVA", "anova_w_c", FEATURE_TRANSFORMATION_ANOVA),
        ("PCA",   "pca_w_c",   FEATURE_TRANSFORMATION_PCA),
    ):
        wc_dir = OUT_DIR / subdir
        for seed in range(42, 52):
            name = f"{prefix}_W_C_scz_cntrl_seed{seed}"
            cfg  = make_wc_config(name, ft, seed)
            write_yaml(wc_dir / f"{name}.yaml", cfg)

    print(f"\nDone — 24 configs written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
