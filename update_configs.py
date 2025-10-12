#!/usr/bin/env python3
"""
Script to update old config files to new nested Ray structure.
Converts flat ray config to nested grid_search + ax structure.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any

def needs_update(config: Dict[str, Any]) -> bool:
    """Check if config needs updating."""
    if 'ray' not in config:
        return False
    
    ray_config = config['ray']
    
    # If it already has search_strategies, it's already updated
    if 'search_strategies' in ray_config:
        return False
    
    # If it has the old flat structure, needs update
    if 'models' in ray_config or 'model_configs' in ray_config:
        return True
    
    return False

def convert_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Convert old flat config to new nested structure."""
    if not needs_update(config):
        return config
    
    ray_config = config['ray']
    
    # Extract old fields
    models = ray_config.get('models', [])
    model_configs = ray_config.get('model_configs', {})
    max_concurrent = ray_config.get('max_concurrent_trials', 4)
    cv_folds = ray_config.get('cv_folds', 5)
    
    # Create new structure
    new_ray_config = {
        'search_strategies': ['grid_search'],
        
        'grid_search': {
            'models': models,
            'model_configs': model_configs,
            'max_concurrent': str(max_concurrent),  # Keep as string like in new configs
            'cv_folds': str(cv_folds)
        },
        
        'ax': {
            'models': [],
            'max_concurrent': '4',
            'cv_folds': '5'
        }
    }
    
    # Preserve other ray fields (metric, mode, etc.)
    for key in ['metric', 'mode', 'random_state', 'graph_data_visualization', 'resources']:
        if key in ray_config:
            new_ray_config[key] = ray_config[key]
    
    # Update config
    config['ray'] = new_ray_config
    
    return config

def update_config_file(filepath: Path, dry_run: bool = False):
    """Update a single config file."""
    try:
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
        
        if not needs_update(config):
            return 'skip', 'Already in new format'
        
        # Convert
        updated_config = convert_config(config)
        
        if dry_run:
            return 'would_update', 'Would be converted'
        
        # Backup original
        backup_path = filepath.with_suffix('.yaml.bak')
        with open(backup_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        # Write updated
        with open(filepath, 'w') as f:
            yaml.dump(updated_config, f, default_flow_style=False, sort_keys=False)
        
        return 'updated', f'Converted (backup: {backup_path.name})'
    
    except Exception as e:
        return 'error', str(e)

def main():
    config_dir = Path('/Users/user/projects/eeg-full-pipeline/config')
    
    # Find all yaml files
    yaml_files = list(config_dir.glob('*.yaml'))
    yaml_files = [f for f in yaml_files if not f.name.endswith('.bak')]
    
    print(f"🔍 Found {len(yaml_files)} config files in {config_dir}\n")
    
    # Dry run first
    print("=" * 70)
    print("DRY RUN - Checking which configs need updating")
    print("=" * 70)
    
    needs_updating = []
    already_updated = []
    
    for filepath in sorted(yaml_files):
        status, message = update_config_file(filepath, dry_run=True)
        
        if status == 'would_update':
            needs_updating.append(filepath.name)
            print(f"🔄 {filepath.name:<50} NEEDS UPDATE")
        elif status == 'skip':
            already_updated.append(filepath.name)
            print(f"✅ {filepath.name:<50} OK (already new format)")
        elif status == 'error':
            print(f"❌ {filepath.name:<50} ERROR: {message}")
    
    print("\n" + "=" * 70)
    print(f"Summary: {len(needs_updating)} need update, {len(already_updated)} already updated")
    print("=" * 70)
    
    if needs_updating:
        print("\n📝 Files that will be updated:")
        for name in needs_updating:
            print(f"   - {name}")
        
        print("\n" + "=" * 70)
        response = input("\nProceed with updating these files? (yes/no): ").strip().lower()
        
        if response == 'yes':
            print("\n" + "=" * 70)
            print("UPDATING CONFIGS...")
            print("=" * 70 + "\n")
            
            for filepath in sorted(yaml_files):
                if filepath.name in needs_updating:
                    status, message = update_config_file(filepath, dry_run=False)
                    
                    if status == 'updated':
                        print(f"✅ {filepath.name:<50} {message}")
                    elif status == 'error':
                        print(f"❌ {filepath.name:<50} ERROR: {message}")
            
            print("\n" + "=" * 70)
            print("✅ UPDATE COMPLETE!")
            print("=" * 70)
            print("\n💡 Backup files saved with .yaml.bak extension")
            print("💡 You can restore with: mv file.yaml.bak file.yaml")
        else:
            print("\n❌ Update cancelled")
    else:
        print("\n✅ All configs are already in the new format!")

if __name__ == '__main__':
    main()
