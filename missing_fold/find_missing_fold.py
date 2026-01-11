#!/usr/bin/env python3
"""Find the missing fold by comparing task tables."""

import csv
from collections import defaultdict

# Analyze size_2
fold_counts_2 = defaultdict(int)
model_counts_2 = defaultdict(set)
with open('task_table-size_2.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fold_id = int(row['fold_id'])
        model_name = row['model_name']
        fold_counts_2[fold_id] += 1
        model_counts_2[fold_id].add(model_name)

# Analyze size_6  
fold_counts_6 = defaultdict(int)
model_counts_6 = defaultdict(set)
with open('task_table-size_6.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fold_id = int(row['fold_id'])
        model_name = row['model_name']
        fold_counts_6[fold_id] += 1
        model_counts_6[fold_id].add(model_name)

print('=' * 80)
print('MISSING FOLD ANALYSIS')
print('=' * 80)
print(f'\nSize 2: {sum(fold_counts_2.values())} total tasks, {len(fold_counts_2)} folds')
print(f'Size 6: {sum(fold_counts_6.values())} total tasks, {len(fold_counts_6)} folds')
print(f'\nDifference: {sum(fold_counts_6.values()) - sum(fold_counts_2.values())} tasks')

missing_folds = set(fold_counts_6.keys()) - set(fold_counts_2.keys())
if missing_folds:
    print(f'\n❌ Missing Fold IDs: {sorted(missing_folds)}')
    for fold_id in sorted(missing_folds):
        print(f'   Fold {fold_id}: Missing {fold_counts_6[fold_id]} tasks')
        print(f'      Models that should be in this fold: {sorted(model_counts_6[fold_id])}')

print(f'\nFold ID Ranges:')
print(f'  Size 2: {min(fold_counts_2.keys())} to {max(fold_counts_2.keys())}')
print(f'  Size 6: {min(fold_counts_6.keys())} to {max(fold_counts_6.keys())}')

# Check for partial folds (same fold_id but different model counts)
print(f'\nChecking for folds with missing models:')
for fold_id in sorted(fold_counts_6.keys()):
    count_2 = fold_counts_2[fold_id]
    count_6 = fold_counts_6[fold_id]
    if count_2 < count_6:
        missing_models = model_counts_6[fold_id] - model_counts_2[fold_id]
        print(f'  Fold {fold_id}: Size 2 has {count_2} tasks, Size 6 has {count_6} tasks')
        print(f'    Missing models: {sorted(missing_models)}')

print(f'\nExpected analysis:')
expected_2 = len(fold_counts_2) * len(model_counts_6[0]) if model_counts_6 else 0
expected_6 = len(fold_counts_6) * len(model_counts_6[0]) if model_counts_6 else 0
print(f'  Size 2: Expected {expected_2} tasks ({len(fold_counts_2)} folds × {len(model_counts_6[0]) if model_counts_6 else 0} models), Got {sum(fold_counts_2.values())}')
print(f'  Size 6: Expected {expected_6} tasks ({len(fold_counts_6)} folds × {len(model_counts_6[0]) if model_counts_6 else 0} models), Got {sum(fold_counts_6.values())}')

print('\n✅ Analysis complete!')

