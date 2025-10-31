#!/usr/bin/env python3
"""Validate the LPSO config file."""

import sys
sys.path.insert(0, '.')
from config_handler import UnifiedConfigHandler

def main():
    config_path = 'config/config_PCA_L_6_C_39-10-2025-1826.yaml'
    print(f'🔍 Validating config: {config_path}')
    print('=' * 60)
    
    try:
        handler = UnifiedConfigHandler(config_path)
        print('✅ Config loaded successfully')
        print()
        
        print('📋 Running validation checks...')
        handler.validate_all_sections()
        
        print()
        print('=' * 60)
        print('✅ CONFIG VALIDATION: PASSED')
        print('=' * 60)
        print()
        print('📊 CONFIG SUMMARY:')
        print(f'   Project Name: {handler.project_name}')
        print(f'   Experiment Type: {handler.experiment_type}')
        print(f'   Transformations: {handler.get_feature_transformation_config().get("transformations")}')
        print(f'   Split Strategy: {handler.data_leakage_strategy}')
        print(f'   Search Strategies: {handler.search_strategies}')
        print(f'   Uses LPSO: {handler.uses_lpso}')
        if handler.uses_lpso:
            print(f'   LPSO Folds: {len(handler.lpso_folds) if handler.lpso_folds else 0}')
            print(f'   Leaky LPSO: {handler.leaky_lpso}')
        print(f'   Ray CPUs: {handler.ray_num_cpus}')
        print(f'   Grid Search Max Concurrent: {handler.grid_search_max_concurrent_trials}')
        print()
        print('✅ All validations passed!')
        return 0
        
    except Exception as e:
        print()
        print('=' * 60)
        print('❌ CONFIG VALIDATION: FAILED')
        print('=' * 60)
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

