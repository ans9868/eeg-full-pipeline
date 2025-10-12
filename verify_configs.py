#!/usr/bin/env python3
"""Verify all configs load correctly with new format."""

import sys
sys.path.insert(0, '/Users/user/projects/eeg-full-pipeline/eeg-ray-tuner')

from config_handler import UnifiedConfigHandler
from pathlib import Path

config_dir = Path('/Users/user/projects/eeg-full-pipeline/config')
yaml_files = sorted([f for f in config_dir.glob('*.yaml') if not f.name.endswith('.bak')])

print(f"🔍 Testing {len(yaml_files)} config files...\n")
print("=" * 70)

passed = []
failed = []

for config_file in yaml_files:
    try:
        handler = UnifiedConfigHandler(str(config_file))
        
        # Verify new properties exist
        strategies = handler.search_strategies
        uses_grid = handler.uses_grid_search
        
        status = "✅ PASS"
        details = f"strategies={strategies}, grid={uses_grid}"
        passed.append(config_file.name)
        
    except Exception as e:
        status = "❌ FAIL"
        details = str(e)[:60]
        failed.append((config_file.name, str(e)))
    
    print(f"{status} {config_file.name:<45} {details}")

print("=" * 70)
print(f"\n📊 Results: {len(passed)} passed, {len(failed)} failed")

if failed:
    print("\n❌ Failed configs:")
    for name, error in failed:
        print(f"   {name}: {error}")
else:
    print("\n✅ ALL CONFIGS VALID!")

