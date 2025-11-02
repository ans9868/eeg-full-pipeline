#!/usr/bin/env python
"""Investigate why PySpark might skip fold 49 in L_2 config but not L_6."""

import yaml
import sys
sys.path.insert(0, '/Users/user/projects/eeg-full-pipeline/eeg-pyspark-pipeline')

from config_handler import UnifiedConfigHandler

configs = [
    ('config_20251101_213555.yaml', 'L_2 (2-person folds)'),
    ('config_20251101_213406.yaml', 'L_6 (6-person folds)')
]

print("="*70)
print("INVESTIGATING LPSO FOLD LOADING")
print("="*70)

for config_file, description in configs:
    print(f"\n{description}")
    print(f"File: {config_file}")
    print("-"*70)
    
    # Load raw YAML
    with open(config_file, 'r') as f:
        raw_yaml = yaml.safe_load(f)
    
    # Check raw YAML
    lpso_folds_raw = raw_yaml.get('data_transformation_strategy', {}).get('lpso_folds', [])
    print(f"Raw YAML - lpso_folds count: {len(lpso_folds_raw)}")
    print(f"Raw YAML - First fold size: {len(lpso_folds_raw[0]) if lpso_folds_raw else 'N/A'}")
    print(f"Raw YAML - Last fold size: {len(lpso_folds_raw[-1]) if lpso_folds_raw else 'N/A'}")
    print(f"Raw YAML - Last fold index: {len(lpso_folds_raw) - 1 if lpso_folds_raw else 'N/A'}")
    
    # Load via UnifiedConfigHandler
    handler = UnifiedConfigHandler(config_file)
    lpso_folds_handler = handler.lpso_folds or []
    
    print(f"\nConfigHandler - lpso_folds count: {len(lpso_folds_handler)}")
    print(f"ConfigHandler - First fold size: {len(lpso_folds_handler[0]) if lpso_folds_handler else 'N/A'}")
    print(f"ConfigHandler - Last fold size: {len(lpso_folds_handler[-1]) if lpso_folds_handler else 'N/A'}")
    print(f"ConfigHandler - Last fold index: {len(lpso_folds_handler) - 1 if lpso_folds_handler else 'N/A'}")
    
    # Check if they match
    if len(lpso_folds_raw) != len(lpso_folds_handler):
        print(f"\n⚠️  MISMATCH: Raw YAML has {len(lpso_folds_raw)}, ConfigHandler has {len(lpso_folds_handler)}")
    else:
        print(f"\n✅ Fold counts match")
    
    # Compare last folds
    if lpso_folds_raw and lpso_folds_handler:
        last_raw = lpso_folds_raw[-1]
        last_handler = lpso_folds_handler[-1]
        
        print(f"\nLast fold comparison:")
        print(f"  Raw YAML last fold ({len(last_raw)} subjects):")
        for i, subj in enumerate(last_raw):
            print(f"    {i+1}. {subj.split('/')[-1]}")
        
        if len(lpso_folds_handler) == len(lpso_folds_raw):
            print(f"  ConfigHandler last fold ({len(last_handler)} subjects):")
            for i, subj in enumerate(last_handler):
                print(f"    {i+1}. {subj.split('/')[-1]}")
        else:
            print(f"  ConfigHandler has fewer folds - showing last available:")
            if lpso_folds_handler:
                last_handler = lpso_folds_handler[-1]
                print(f"    Last handler fold ({len(last_handler)} subjects):")
                for i, subj in enumerate(last_handler):
                    print(f"      {i+1}. {subj.split('/')[-1]}")
    
    # Check for any special characters or issues in the last fold
    if lpso_folds_raw:
        last_fold_raw = lpso_folds_raw[-1]
        print(f"\nLast fold in YAML analysis:")
        print(f"  Number of subjects: {len(last_fold_raw)}")
        for i, path in enumerate(last_fold_raw):
            # Check for encoding issues, special chars, etc.
            has_issue = False
            if '\n' in path:
                print(f"    ⚠️  Subject {i+1} has newline in path!")
                has_issue = True
            if '\r' in path:
                print(f"    ⚠️  Subject {i+1} has carriage return in path!")
                has_issue = True
            if len(path.strip()) != len(path):
                print(f"    ⚠️  Subject {i+1} has leading/trailing whitespace!")
                has_issue = True
            if not has_issue:
                print(f"    ✅ Subject {i+1}: {path.split('/')[-1]}")
    
    # Check YAML structure around last fold
    print(f"\nYAML structure check:")
    with open(config_file, 'r') as f:
        yaml_lines = f.readlines()
    
    # Find the lpso_folds section
    in_lpso_folds = False
    fold_start_lines = []
    last_fold_line_start = None
    
    for i, line in enumerate(yaml_lines):
        if 'lpso_folds:' in line:
            in_lpso_folds = True
            print(f"  Found lpso_folds at line {i+1}")
        elif in_lpso_folds and line.strip().startswith('- -'):
            # Start of a new fold
            fold_start_lines.append(i+1)
            if len(fold_start_lines) == len(lpso_folds_raw):
                last_fold_line_start = i+1
    
    if last_fold_line_start:
        print(f"  Last fold starts at line {last_fold_line_start}")
        print(f"  Showing lines around last fold:")
        start = max(0, last_fold_line_start - 3)
        end = min(len(yaml_lines), last_fold_line_start + 5)
        for line_num in range(start, end):
            marker = ">>> " if line_num == last_fold_line_start - 1 else "    "
            print(f"{marker}{line_num+1:4}: {yaml_lines[line_num].rstrip()}")
    
    print()

print("="*70)
print("INVESTIGATION COMPLETE")
print("="*70)

