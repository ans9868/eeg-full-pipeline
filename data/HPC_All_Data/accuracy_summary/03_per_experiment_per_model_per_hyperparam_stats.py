#!/usr/bin/env python3
"""Per-experiment, per-model, per-hyperparameter accuracy statistics.

At this granularity there is one run per fold, so a single set of
fold-level stats is reported. Reads ../all_experiments_combined.csv
and writes per_experiment_per_model_per_hyperparam_stats.csv.
"""

import csv
import statistics
from collections import defaultdict
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / 'all_experiments_combined.csv'
DST = Path(__file__).resolve().parent / 'per_experiment_per_model_per_hyperparam_stats.csv'

COLUMNS = [
    'experiment', 'experiment_type', 'feature_set', 'holdout_size_P',
    'model', 'hyperparams', 'n_folds',
    'median', 'iqr', 'mean', 'sd', 'min', 'max',
]


def quartiles(vals):
    s = sorted(vals)
    n = len(s)
    if n < 2:
        return s[0], s[0]
    q1 = statistics.median(s[:n // 2])
    q3 = statistics.median(s[n // 2 + n % 2:])
    return q1, q3


def main():
    groups = defaultdict(lambda: {'accs': [], 'meta': {}})

    with open(SRC) as f:
        for row in csv.DictReader(f):
            key = (row['experiment'], row['model'], row['hyperparams'])
            g = groups[key]
            g['accs'].append(float(row['test_accuracy']))
            if not g['meta']:
                g['meta'] = {
                    'experiment': row['experiment'],
                    'experiment_type': row['experiment_type'],
                    'feature_set': row['feature_set'],
                    'holdout_size_P': row['holdout_size_P'],
                    'model': row['model'],
                    'hyperparams': row['hyperparams'],
                }

    with open(DST, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for key in sorted(groups):
            g = groups[key]
            accs = g['accs']
            q1, q3 = quartiles(accs)
            row = {
                **g['meta'],
                'n_folds': len(accs),
                'median': round(statistics.median(accs), 6),
                'iqr': round(q3 - q1, 6),
                'mean': round(statistics.mean(accs), 6),
                'sd': round(statistics.stdev(accs), 6) if len(accs) > 1 else 0.0,
                'min': round(min(accs), 6),
                'max': round(max(accs), 6),
            }
            w.writerow(row)

    print(f'Wrote {DST}  ({len(groups)} rows)')


if __name__ == '__main__':
    main()
