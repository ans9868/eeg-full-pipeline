#!/usr/bin/env python3
"""
Check config file and generate task table for grid search.

Usage:
    python check_config_tasks.py <config_file_path>
    
Example:
    python check_config_tasks.py config/HPC_configs_v2/config_ANOVA_L_6_C_39-10-2025-1826.yaml
"""

import sys
import yaml
from itertools import product
from pathlib import Path


def generate_combinations(model_config):
    """Generate all hyperparameter combinations for a model."""
    use_default = model_config.get("use_default", False)
    
    if use_default:
        return None, "default grid"
    
    hyperparams = model_config.get("hyperparameters", {})
    if not hyperparams:
        return None, "no hyperparameters"
    
    # Convert single values to lists
    hyperparam_lists = {}
    for param_name, param_values in hyperparams.items():
        if not isinstance(param_values, list):
            hyperparam_lists[param_name] = [param_values]
        else:
            hyperparam_lists[param_name] = param_values
    
    # Generate Cartesian product
    param_names = list(hyperparam_lists.keys())
    param_values = [hyperparam_lists[name] for name in param_names]
    
    combinations = []
    for value_combo in product(*param_values):
        combo_dict = dict(zip(param_names, value_combo))
        combinations.append(combo_dict)
    
    return combinations, param_names


def check_config(config_path):
    """Check config file and display task table."""
    print(f'Loading config: {config_path}\n')
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Extract grid search config
    if 'ray' not in config or 'grid_search' not in config['ray']:
        print("❌ Error: No grid_search configuration found in config file")
        return False
    
    grid_search = config['ray']['grid_search']
    model_configs = grid_search.get('model_configs', {})
    models = grid_search.get('models', [])
    
    if not models:
        print("❌ Error: No models specified in grid_search")
        return False
    
    print(f"Models: {models}\n")
    print("=" * 80)
    
    # Generate combinations for each model
    total_combinations = 0
    all_combinations = {}
    
    for model_name in models:
        model_config = model_configs.get(model_name, {})
        combinations, param_names = generate_combinations(model_config)
        
        if combinations is None:
            print(f"\n{model_name}: {param_names}")
            continue
        
        all_combinations[model_name] = combinations
        total_combinations += len(combinations)
        
        print(f"\n{model_name}:")
        print(f"  Total combinations: {len(combinations)}")
        print(f"  Hyperparameters: {param_names}")
        print(f"  Combinations:")
        for i, combo in enumerate(combinations, 1):
            # Format hyperparameters nicely
            combo_str = ", ".join([f"{k}={v}" for k, v in combo.items()])
            print(f"    {i}. {combo_str}")
    
    # Determine number of folds based on strategy
    num_folds = 1
    if 'data_transformation_strategy' in config:
        strategy = config['data_transformation_strategy'].get('strategy', '')
        if 'LPSO' in strategy:
            # Try to get fold count from lpso_metadata
            lpso_metadata = config['data_transformation_strategy'].get('lpso_metadata', {})
            num_folds = lpso_metadata.get('total_folds', 1)
            print(f"\n  → Detected LPSO with {num_folds} folds")
        elif 'Within-subject' in strategy:
            print(f"\n  → Detected Within-subject split (single fold per model)")
    
    total_tasks = total_combinations * num_folds
    
    print("\n" + "=" * 80)
    print(f"\nSummary:")
    print(f"  Models: {len(models)}")
    print(f"  Total combinations per fold: {total_combinations}")
    print(f"  Folds: {num_folds}")
    print(f"  Total tasks: {total_combinations} combinations × {num_folds} folds = {total_tasks} tasks")
    
    # Verify we have exactly 3 per model (as intended)
    expected_combinations = len(models) * 3
    if total_combinations == expected_combinations:
        print(f"\n✅ Perfect! Exactly 3 combinations per model ({expected_combinations} total)")
    else:
        print(f"\n⚠️  Note: Expected {expected_combinations} combinations (3 per model), got {total_combinations}")
    
    print("\n✅ Config is valid!")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_config_tasks.py <config_file_path>")
        print("\nExample:")
        print("  python check_config_tasks.py config/HPC_configs_v2/config_ANOVA_L_6_C_39-10-2025-1826.yaml")
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    
    if not config_path.exists():
        print(f"❌ Error: Config file not found: {config_path}")
        sys.exit(1)
    
    success = check_config(config_path)
    sys.exit(0 if success else 1)

