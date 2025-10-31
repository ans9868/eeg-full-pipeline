#!/usr/bin/env python3
"""Validate config file without checking if paths exist."""

from config_handler import UnifiedConfigHandler
import sys

def main():
    config_path = 'config/config_PCA_W_C_26-10-2025_0206.yaml'
    
    try:
        print(f"🔍 Validating config: {config_path}")
        print("=" * 60)
        print("ℹ️  Note: Path existence validation is skipped")
        print("=" * 60)
        print()
        
        # Load config
        handler = UnifiedConfigHandler(config_path)
        
        # Validate all sections
        print("📋 Running validation checks...")
        print()
        
        handler.validate_all_sections()
        
        print()
        print("=" * 60)
        print("✅ CONFIG VALIDATION: PASSED")
        print("=" * 60)
        print()
        print("📊 CONFIG SUMMARY:")
        print(f"   Project Name: {handler.project_name}")
        print(f"   Experiment Type: {handler.experiment_type}")
        print(f"   Transformations: {handler.get_feature_transformation_config().get('transformations')}")
        print(f"   Split Strategy: {handler.data_leakage_strategy}")
        print(f"   Search Strategies: {handler.search_strategies}")
        print(f"   Train Ratio: {handler.intra_test_train_split_train_ratio}")
        print(f"   Split Method: {handler.intra_test_train_split_method}")
        print()
        print("✅ All validations passed (path existence not checked)")
        return 0
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ CONFIG VALIDATION: FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

