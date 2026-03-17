#!/usr/bin/env python3
"""Per-experiment accuracy statistics with all models pooled.

Within each experiment all models and HP configs are pooled together.
Reads ../all_experiments_combined.csv and writes
per_experiment_all_models_pooled_stats.csv.
"""

import csv
import statistics
from collections import defaultdict
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / 'all_experiments_combined.csv'
DST = Path(__file__).resolve().parent / 'per_experiment_all_models_pooled_stats.csv'

COLUMNS = [
    'experiment', 'experiment_type', 'feature_set', 'holdout_size_P',
    'n_runs', 'n_folds',
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


def main():
    groups = defaultdict(lambda: {'accs': [], 'folds': defaultdict(list), 'meta': {}})

    with open(SRC) as f:
        for row in csv.DictReader(f):
            key = row['experiment']
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
                }

    with open(DST, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for key in sorted(groups):
            g = groups[key]
            accs = g['accs']
            q1, q3 = quartiles(accs)
            fold_bests = [max(v) for v in g['folds'].values()]
            med_bpf = statistics.median(fold_bests) if fold_bests else statistics.median(accs)
            row = {
                **g['meta'],
                'n_runs': len(accs),
                'n_folds': len(g['folds']),
                'median_all_runs': round(statistics.median(accs), 6),
                'median_best_per_fold': round(med_bpf, 6),
                'iqr_all_runs': round(q3 - q1, 6),
                'mean_all_runs': round(statistics.mean(accs), 6),
                'sd_all_runs': round(statistics.stdev(accs), 6) if len(accs) > 1 else 0.0,
                'min_all_runs': round(min(accs), 6),
                'max_all_runs': round(max(accs), 6),
            }
            w.writerow(row)

    print(f'Wrote {DST}  ({len(groups)} rows)')


if __name__ == '__main__':
    main()
