#!/usr/bin/env python3
"""
Count LPSO folds from YAML file and compare with task tables
"""

import yaml
import csv
from collections import defaultdict
from pathlib import Path

def count_lpso_folds_from_yaml(yaml_file):
    """Count LPSO folds from YAML file."""
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Get lpso_folds
    if isinstance(data, dict):
        dt_strategy = data.get('data_transformation_strategy', {})
        lpso_folds = dt_strategy.get('lpso_folds', [])
        if not lpso_folds:
            lpso_folds = data.get('lpso_folds', [])
    elif isinstance(data, list):
        lpso_folds = data
    else:
        lpso_folds = []
    
    return len(lpso_folds), lpso_folds

def analyze_task_table(csv_path):
    """Analyze a task table and return fold/model statistics."""
    fold_model_counts = defaultdict(lambda: defaultdict(int))
    fold_ids = set()
    model_names = set()
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fold_id = int(row['fold_id'])
            model_name = row['model_name']
            fold_ids.add(fold_id)
            model_names.add(model_name)
            fold_model_counts[fold_id][model_name] += 1
    
    return {
        'fold_ids': sorted(fold_ids),
        'model_names': sorted(model_names),
        'fold_model_counts': fold_model_counts,
        'total_folds': len(fold_ids),
        'total_models': len(model_names),
        'total_tasks': sum(sum(counts.values()) for counts in fold_model_counts.values())
    }

def main():
    base_dir = Path("/Users/user/projects/eeg-full-pipeline/missing_fold")
    
    yaml_file = base_dir / "data_transform_strategy.yaml"
    size_2_file = base_dir / "task_table-size_2.csv"
    size_6_file = base_dir / "task_table-size_6.csv"
    
    print("=" * 80)
    print("LPSO FOLD COUNT ANALYSIS")
    print("=" * 80)
    
    # Count folds in YAML
    print(f"\n📄 Reading YAML file: {yaml_file}")
    yaml_fold_count, yaml_folds = count_lpso_folds_from_yaml(yaml_file)
    print(f"   ✅ Found {yaml_fold_count} LPSO folds in YAML")
    
    if yaml_folds:
        print(f"\n📋 First 5 folds:")
        for i, fold in enumerate(yaml_folds[:5]):
            subject_ids = []
            for path in fold:
                # Extract subject ID from path
                parts = path.split('/')
                for part in parts:
                    if part.startswith('sub-'):
                        subject_ids.append(part)
                        break
            print(f"   Fold {i}: {len(fold)} subjects - {subject_ids}")
        if len(yaml_folds) > 5:
            print(f"   ... and {len(yaml_folds) - 5} more folds")
    
    # Analyze task tables
    print(f"\n📊 Analyzing Task Tables:")
    size_2_stats = analyze_task_table(size_2_file)
    size_6_stats = analyze_task_table(size_6_file)
    
    print(f"\n   Size 2 (LPSO=2):")
    print(f"      Total tasks: {size_2_stats['total_tasks']}")
    print(f"      Total folds: {size_2_stats['total_folds']}")
    print(f"      Total models: {size_2_stats['total_models']}")
    print(f"      Expected: {size_2_stats['total_models']} models × {size_2_stats['total_folds']} folds = {size_2_stats['total_models'] * size_2_stats['total_folds']}")
    
    print(f"\n   Size 6 (LPSO=6):")
    print(f"      Total tasks: {size_6_stats['total_tasks']}")
    print(f"      Total folds: {size_6_stats['total_folds']}")
    print(f"      Total models: {size_6_stats['total_models']}")
    print(f"      Expected: {size_6_stats['total_models']} models × {size_6_stats['total_folds']} folds = {size_6_stats['total_models'] * size_6_stats['total_folds']}")
    
    # Compare
    print(f"\n🔍 Comparison:")
    print(f"   YAML fold count: {yaml_fold_count}")
    print(f"   Size 2 fold count: {size_2_stats['total_folds']}")
    print(f"   Size 6 fold count: {size_6_stats['total_folds']}")
    
    print(f"\n   Task differences:")
    print(f"      Size 2 missing: {size_2_stats['total_models'] * size_2_stats['total_folds'] - size_2_stats['total_tasks']} tasks")
    print(f"      Size 6 missing: {size_6_stats['total_models'] * size_6_stats['total_folds'] - size_6_stats['total_tasks']} tasks")
    
    # Check if YAML matches
    if yaml_fold_count == size_2_stats['total_folds']:
        print(f"\n✅ YAML fold count ({yaml_fold_count}) matches Size 2 task table folds ({size_2_stats['total_folds']})")
    elif yaml_fold_count == size_6_stats['total_folds']:
        print(f"\n✅ YAML fold count ({yaml_fold_count}) matches Size 6 task table folds ({size_6_stats['total_folds']})")
    else:
        print(f"\n⚠️  YAML fold count ({yaml_fold_count}) doesn't match either task table!")
        print(f"   Size 2: {size_2_stats['total_folds']} folds")
        print(f"   Size 6: {size_6_stats['total_folds']} folds")
    
    # Find missing fold IDs
    missing_fold_ids = set(size_6_stats['fold_ids']) - set(size_2_stats['fold_ids'])
    if missing_fold_ids:
        print(f"\n❌ Missing Fold IDs in Size 2: {sorted(missing_fold_ids)}")
        print(f"   This means {len(missing_fold_ids)} complete fold(s) are missing from Size 2")
        print(f"   Each missing fold should have {size_2_stats['total_models']} models")
        print(f"   Total missing tasks: {len(missing_fold_ids) * size_2_stats['total_models']}")
        
        # Show which fold IDs are missing
        for fold_id in sorted(missing_fold_ids):
            print(f"\n   Missing Fold {fold_id}:")
            fold_6_models = list(size_6_stats['fold_model_counts'][fold_id].keys())
            print(f"      Models in Size 6: {', '.join(fold_6_models)}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ YAML contains: {yaml_fold_count} folds")
    print(f"✅ Size 2 task table: {size_2_stats['total_folds']} folds, {size_2_stats['total_tasks']} tasks")
    print(f"✅ Size 6 task table: {size_6_stats['total_folds']} folds, {size_6_stats['total_tasks']} tasks")
    print(f"✅ Expected tasks (Size 2): {size_2_stats['total_models'] * size_2_stats['total_folds']}")
    print(f"✅ Expected tasks (Size 6): {size_6_stats['total_models'] * size_6_stats['total_folds']}")
    
    if missing_fold_ids:
        print(f"\n❌ Missing {len(missing_fold_ids)} fold(s) in Size 2: {sorted(missing_fold_ids)}")
        print(f"   Missing {len(missing_fold_ids) * size_2_stats['total_models']} total tasks")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()

