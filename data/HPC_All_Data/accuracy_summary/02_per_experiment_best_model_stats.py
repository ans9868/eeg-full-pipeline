#!/usr/bin/env python3
"""Per-experiment best-model accuracy statistics.

For each experiment, selects the model with the highest median_all_runs
and reports its stats. Reads ../all_experiments_combined.csv and writes
per_experiment_best_model_stats.csv into this directory.
"""

import csv
import statistics
from collections import defaultdict
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / 'all_experiments_combined.csv'
DST = Path(__file__).resolve().parent / 'per_experiment_best_model_stats.csv'

COLUMNS = [
    'experiment', 'experiment_type', 'feature_set', 'holdout_size_P',
    'best_model', 'n_runs', 'n_folds',
    'median_all_runs', 'median_best_per_fold',
    'iqr_all_runs', 'mean_all_runs', 'sd_all_runs',
    'min_all_runs', 'max_all_runs',
]


def quartiles(vals):
    s = sorted(vals)
    n = len(s)
    q1 = statistics.median(s[:n // 2])
    q3 = statistics.median(s[n // 2 + n % 2:])
    return q1, q3


def compute_stats(accs, fold_accs):
    med = statistics.median(accs)
    q1, q3 = quartiles(accs)
    fold_bests = [max(v) for v in fold_accs.values()]
    med_bpf = statistics.median(fold_bests) if fold_bests else med
    return {
        'n_runs': len(accs),
        'n_folds': len(fold_accs),
        'median_all_runs': round(med, 6),
        'median_best_per_fold': round(med_bpf, 6),
        'iqr_all_runs': round(q3 - q1, 6),
        'mean_all_runs': round(statistics.mean(accs), 6),
        'sd_all_runs': round(statistics.stdev(accs), 6) if len(accs) > 1 else 0.0,
        'min_all_runs': round(min(accs), 6),
        'max_all_runs': round(max(accs), 6),
    }


def main():
    groups = defaultdict(lambda: {'accs': [], 'folds': defaultdict(list), 'meta': {}})

    with open(SRC) as f:
        for row in csv.DictReader(f):
            key = (row['experiment'], row['model'])
            g = groups[key]
            acc = float(row['test_accuracy'])
            g['accs'].append(acc)
            g['folds'][row['fold_id']].append(acc)
            if not g['meta']:
                g['meta'] = {
                    'experiment': row['experiment'],
                    'experiment_type': row['experiment_type'],
                    'feature_set': row['feature_set'],
                    'holdout_size_P': row['holdout_size_P'],
                    'model': row['model'],
                }

    experiments = defaultdict(list)
    for (exp, model), g in groups.items():
        med = statistics.median(g['accs'])
        experiments[exp].append((med, model, g))

    with open(DST, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for exp in sorted(experiments):
            candidates = experiments[exp]
            candidates.sort(key=lambda x: (-x[0], x[1]))
            _, best_model, g = candidates[0]
            stats = compute_stats(g['accs'], g['folds'])
            row = {
                'experiment': exp,
                'experiment_type': g['meta']['experiment_type'],
                'feature_set': g['meta']['feature_set'],
                'holdout_size_P': g['meta']['holdout_size_P'],
                'best_model': best_model,
                **stats,
            }
            w.writerow(row)

    print(f'Wrote {DST}  ({len(experiments)} rows)')


if __name__ == '__main__':
    main()
