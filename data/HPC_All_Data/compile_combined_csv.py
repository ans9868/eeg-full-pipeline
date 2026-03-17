#!/usr/bin/env python3
"""
Compile all experiment results into one combined CSV with integrity checks.

Reads every results.json from the 10 canonical experiments defined in the
design doc (COMBINED_ACCURACY_CSV_DESIGN.md) and produces:
  - all_experiments_combined.csv (2,736 rows expected)
  - all_experiments_integrity_report.md
"""

import csv
import json
import sys
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent

MODEL_DIRS = ['KNN', 'SVM', 'XGBoost', 'MLP_(Neural_Network)']

MODEL_NORMALIZE = {
    'KNN': 'KNN',
    'SVM': 'SVM',
    'XGBoost': 'XGBoost',
    'MLP_(Neural_Network)': 'MLP',
}

EXPERIMENTS = [
    {
        'name': 'ANOVA_L_6_Random',
        'dir': 'grid_50_random_folds/ANOVA_L_6_complete',
        'type': 'LPSO_Random_50',
        'feature': 'ANOVA',
        'P': '6',
        'has_ml_subdir': False,
        'expected_folds': 50,
        'expected_results_per_model': 150,
    },
    {
        'name': 'ANOVA_L_2_Random',
        'dir': 'grid_50_random_folds/ANOVA_L_2_complete',
        'type': 'LPSO_Random_50',
        'feature': 'ANOVA',
        'P': '2',
        'has_ml_subdir': False,
        'expected_folds': 50,
        'expected_results_per_model': 150,
    },
    {
        'name': 'PCA_L_6_Random',
        'dir': 'grid_50_random_folds/PCA_L_6_ml_results',
        'type': 'LPSO_Random_50',
        'feature': 'PCA',
        'P': '6',
        'has_ml_subdir': False,
        'expected_results_per_model': 150,
        'expected_folds': 50,
    },
    {
        'name': 'PCA_L_2_Random',
        'dir': 'grid_50_random_folds/PCA_L_2_ml_results',
        'type': 'LPSO_Random_50',
        'feature': 'PCA',
        'P': '2',
        'has_ml_subdir': False,
        'expected_folds': 50,
        'expected_results_per_model': 150,
    },
    {
        'name': 'ANOVA_L_6_Uniform',
        'dir': 'grid_12_folds/ANOVA_L_6_C_Resource_Boosted',
        'type': 'LPSO_Systematic_12',
        'feature': 'ANOVA',
        'P': '6',
        'has_ml_subdir': True,
        'expected_folds': 12,
        'expected_results_per_model': 36,
    },
    {
        'name': 'PCA_L_6_Uniform',
        'dir': 'grid_12_folds/PCA_L_6_C-3',
        'type': 'LPSO_Systematic_12',
        'feature': 'PCA',
        'P': '6',
        'has_ml_subdir': True,
        'expected_folds': 12,
        'expected_results_per_model': 36,
    },
    {
        'name': 'ANOVA_W_C',
        'dir': 'grid_12_folds/ANOVA_W_C',
        'type': 'Within_Subject',
        'feature': 'ANOVA',
        'P': 'N/A',
        'has_ml_subdir': True,
        'expected_folds': 1,
        'expected_results_per_model': 3,
    },
    {
        'name': 'ANOVA_W_F',
        'dir': 'grid_12_folds/ANOVA_W_F',
        'type': 'Within_Subject',
        'feature': 'ANOVA',
        'P': 'N/A',
        'has_ml_subdir': True,
        'expected_folds': 1,
        'expected_results_per_model': 3,
    },
    {
        'name': 'PCA_W_C',
        'dir': 'grid_12_folds/PCA_W_C-3',
        'type': 'Within_Subject',
        'feature': 'PCA',
        'P': 'N/A',
        'has_ml_subdir': True,
        'expected_folds': 1,
        'expected_results_per_model': 3,
    },
    {
        'name': 'PCA_W_F',
        'dir': 'grid_12_folds/PCA_W_F-3',
        'type': 'Within_Subject',
        'feature': 'PCA',
        'P': 'N/A',
        'has_ml_subdir': True,
        'expected_folds': 1,
        'expected_results_per_model': 3,
    },
]

EXPECTED_GRAND_TOTAL = 2736

CSV_COLUMNS = [
    'experiment', 'experiment_dir', 'experiment_type', 'feature_set',
    'holdout_size_P', 'model', 'fold_id', 'task_id', 'hyperparams',
    'test_accuracy', 'train_accuracy', 'test_f1', 'test_precision',
    'test_recall', 'source_file',
]


def resolve_models_path(exp):
    exp_path = BASE_DIR / exp['dir']
    if exp['has_ml_subdir']:
        return exp_path / 'ml_results_grid_search'
    return exp_path


def collect_rows(exp):
    """Walk one experiment and yield CSV row dicts."""
    models_path = resolve_models_path(exp)
    if not models_path.exists():
        print(f"  ERROR: path does not exist: {models_path}")
        return

    for model_dir_name in MODEL_DIRS:
        model_path = models_path / model_dir_name
        if not model_path.exists():
            print(f"  WARNING: model dir missing: {model_path}")
            continue

        model_norm = MODEL_NORMALIZE[model_dir_name]

        fold_dirs = sorted([
            d for d in model_path.iterdir()
            if d.is_dir() and (d.name.startswith('sub-') or d.name == 'within_subject_split')
        ])

        for fold_dir in fold_dirs:
            task_dirs = sorted([
                t for t in fold_dir.iterdir()
                if t.is_dir() and t.name.startswith('task_')
            ])

            for task_dir in task_dirs:
                results_file = task_dir / 'results.json'
                if not results_file.exists():
                    continue

                try:
                    with open(results_file) as f:
                        data = json.load(f)
                except (json.JSONDecodeError, OSError) as e:
                    print(f"  WARNING: bad results.json: {results_file} ({e})")
                    continue

                test = data.get('test_results', {})
                train = data.get('train_results', {})
                rel_path = results_file.relative_to(BASE_DIR)

                yield {
                    'experiment': exp['name'],
                    'experiment_dir': exp['dir'],
                    'experiment_type': exp['type'],
                    'feature_set': exp['feature'],
                    'holdout_size_P': exp['P'],
                    'model': model_norm,
                    'fold_id': fold_dir.name,
                    'task_id': task_dir.name,
                    'hyperparams': json.dumps(data.get('hyperparams', {}), sort_keys=True),
                    'test_accuracy': test.get('accuracy', ''),
                    'train_accuracy': train.get('accuracy', ''),
                    'test_f1': test.get('f1', ''),
                    'test_precision': test.get('precision', ''),
                    'test_recall': test.get('recall', ''),
                    'source_file': str(rel_path),
                }


def run_integrity_checks(all_rows):
    """Run all validation checks. Returns (passed, report_lines)."""
    report = []
    warnings = []
    passed = True

    counts = defaultdict(lambda: defaultdict(int))   # (exp, model) -> count
    folds = defaultdict(lambda: defaultdict(set))     # (exp, model) -> set of fold_ids
    sources = set()
    dup_count = 0

    for row in all_rows:
        key_exp = row['experiment']
        key_model = row['model']
        counts[key_exp][key_model] += 1
        folds[key_exp][key_model].add(row['fold_id'])
        src = row['source_file']
        if src in sources:
            dup_count += 1
        sources.add(src)

    report.append("# Combined CSV Integrity Report\n")
    report.append(f"**Total rows:** {len(all_rows)}")
    report.append(f"**Expected:** {EXPECTED_GRAND_TOTAL}")
    report.append(f"**Match:** {'YES' if len(all_rows) == EXPECTED_GRAND_TOTAL else 'NO'}\n")

    if len(all_rows) != EXPECTED_GRAND_TOTAL:
        passed = False
        warnings.append(f"Grand total mismatch: got {len(all_rows)}, expected {EXPECTED_GRAND_TOTAL}")

    report.append("## 1. Per-Experiment x Per-Model Counts\n")
    report.append("| Experiment | Model | Expected | Actual | Status |")
    report.append("|-----------|-------|----------|--------|--------|")

    for exp in EXPERIMENTS:
        expected = exp['expected_results_per_model']
        for model_dir_name in MODEL_DIRS:
            model_norm = MODEL_NORMALIZE[model_dir_name]
            actual = counts[exp['name']][model_norm]
            ok = actual == expected
            status = "PASS" if ok else "FAIL"
            if not ok:
                passed = False
                warnings.append(f"{exp['name']}/{model_norm}: expected {expected}, got {actual}")
            report.append(f"| {exp['name']} | {model_norm} | {expected} | {actual} | {status} |")

    report.append("\n## 2. Fold-Dir Counts\n")
    report.append("| Experiment | Model | Expected Folds | Actual Folds | Status |")
    report.append("|-----------|-------|---------------|--------------|--------|")

    for exp in EXPERIMENTS:
        expected_f = exp['expected_folds']
        for model_dir_name in MODEL_DIRS:
            model_norm = MODEL_NORMALIZE[model_dir_name]
            actual_f = len(folds[exp['name']][model_norm])
            ok = actual_f == expected_f
            status = "PASS" if ok else "FAIL"
            if not ok:
                passed = False
                warnings.append(f"{exp['name']}/{model_norm} folds: expected {expected_f}, got {actual_f}")
            report.append(f"| {exp['name']} | {model_norm} | {expected_f} | {actual_f} | {status} |")

    report.append("\n## 3. HP-Per-Fold Check (3 expected)\n")
    hp_issues = []
    for exp in EXPERIMENTS:
        for model_dir_name in MODEL_DIRS:
            model_norm = MODEL_NORMALIZE[model_dir_name]
            fold_set = folds[exp['name']][model_norm]
            expected_per_fold = exp['expected_results_per_model'] // max(exp['expected_folds'], 1)
            for fold_id in fold_set:
                fold_count = sum(
                    1 for r in all_rows
                    if r['experiment'] == exp['name']
                    and r['model'] == model_norm
                    and r['fold_id'] == fold_id
                )
                if fold_count != expected_per_fold:
                    hp_issues.append(f"{exp['name']}/{model_norm}/{fold_id}: {fold_count} (expected {expected_per_fold})")

    if hp_issues:
        passed = False
        report.append(f"Found **{len(hp_issues)}** fold(s) with wrong HP count:")
        for issue in hp_issues[:20]:
            report.append(f"- {issue}")
        if len(hp_issues) > 20:
            report.append(f"- ... and {len(hp_issues) - 20} more")
    else:
        report.append("All folds have exactly 3 HP configs per model. **PASS**")

    report.append("\n## 4. Duplicate Check\n")
    if dup_count > 0:
        passed = False
        report.append(f"**FAIL:** {dup_count} duplicate source_file paths found.")
        warnings.append(f"{dup_count} duplicate source paths")
    else:
        report.append("No duplicate source_file paths. **PASS**")

    report.append("\n---\n")
    if passed:
        report.append("## RESULT: ALL CHECKS PASSED")
    else:
        report.append("## RESULT: SOME CHECKS FAILED\n")
        report.append("### Warnings:\n")
        for w in warnings:
            report.append(f"- {w}")

    return passed, '\n'.join(report)


def main():
    print("=" * 70)
    print("COMPILING COMBINED CSV FROM 10 CANONICAL EXPERIMENTS")
    print("=" * 70)

    all_rows = []

    for exp in EXPERIMENTS:
        print(f"\n[{exp['name']}] {exp['dir']}")
        exp_path = resolve_models_path(exp)
        if not exp_path.exists():
            print(f"  ERROR: path not found: {exp_path}")
            continue

        before = len(all_rows)
        for row in collect_rows(exp):
            all_rows.append(row)
        after = len(all_rows)
        print(f"  Collected {after - before} rows")

    print(f"\n{'=' * 70}")
    print(f"TOTAL ROWS: {len(all_rows)}")
    print(f"EXPECTED:   {EXPECTED_GRAND_TOTAL}")
    print(f"{'=' * 70}")

    csv_path = BASE_DIR / 'all_experiments_combined.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\nCSV saved: {csv_path}")
    print(f"  Rows: {len(all_rows)}, Columns: {len(CSV_COLUMNS)}")

    print(f"\nRunning integrity checks...")
    passed, report = run_integrity_checks(all_rows)

    report_path = BASE_DIR / 'all_experiments_integrity_report.md'
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"Report saved: {report_path}")

    if passed:
        print("\nALL INTEGRITY CHECKS PASSED")
    else:
        print("\nSOME INTEGRITY CHECKS FAILED — see report for details")

    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
