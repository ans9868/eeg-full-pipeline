#!/usr/bin/env python
"""
Analyze per-subject accuracy across LPSO folds.

For each subject, find all folds where they appear as test, then calculate:
- Mean accuracy across all folds where subject was tested
- Min/Max accuracy (swing)
- Visualize per-subject performance
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics
import re

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("⚠️  matplotlib not available - skipping visualizations")

BASE_DIR = Path(__file__).parent

EXPERIMENTS = {
    "ANOVA_L_6_Random": {
        "path": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
        "description": "ANOVA P=6 (50 random folds)"
    },
    "ANOVA_L_2_Random": {
        "path": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
        "description": "ANOVA P=2 (50 random folds)"
    },
    "PCA_L_6_Random": {
        "path": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
        "description": "PCA P=6 (50 random folds)"
    },
    "PCA_L_2_Random": {
        "path": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
        "description": "PCA P=2 (50 random folds)"
    },
    "ANOVA_L_6_Uniform": {
        "path": BASE_DIR / "grid_12_folds/ANOVA_L_6_C_Resource_Boosted",
        "description": "ANOVA P=6 (12 uniform folds)"
    },
    "PCA_L_6_Uniform": {
        "path": BASE_DIR / "grid_12_folds/PCA_L_6_C-3",
        "description": "PCA P=6 (12 uniform folds)"
    },
}

def extract_subject_ids_from_fold(fold_dir_name):
    """Extract subject IDs from fold directory name (e.g., 'sub-2_sub-6_sub-14' -> ['sub-2', 'sub-6', 'sub-14'])."""
    # Match pattern: sub- followed by digits
    pattern = r'sub-(\d+)'
    matches = re.findall(pattern, fold_dir_name)
    return [f"sub-{m}" for m in matches]

def extract_per_subject_accuracies(results_dir, best_model_only=True):
    """Extract per-subject accuracies from LPSO results."""
    if not results_dir.exists():
        return {}
    
    # Try ml_results_grid_search first
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Find best model by median if best_model_only
    if best_model_only:
        model_stats = {}
        model_dirs = [d for d in results_path.iterdir() 
                      if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
        
        for model_dir in model_dirs:
            results_files = list(model_dir.rglob("results.json"))
            accuracies = []
            for results_file in results_files:
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                    accuracy = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                    if accuracy is not None:
                        accuracies.append(float(accuracy))
                except:
                    continue
            if accuracies:
                model_stats[model_dir.name] = statistics.median(accuracies)
        
        if not model_stats:
            return {}
        
        best_model = max(model_stats.items(), key=lambda x: x[1])[0]
        model_dir = results_path / best_model
        print(f"      Using best model: {best_model} (median: {model_stats[best_model]:.2%})")
    else:
        # Use all models
        model_dirs = [d for d in results_path.iterdir() 
                      if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
        if not model_dirs:
            return {}
        model_dir = model_dirs[0]  # Just use first for now
    
    # Find fold directories
    fold_dirs = [d for d in model_dir.iterdir() 
                 if d.is_dir() and d.name.startswith('sub-')]
    
    # Map: subject_id -> list of accuracies from folds where subject was test
    subject_accuracies = defaultdict(list)
    fold_to_accuracy = {}
    
    for fold_dir in fold_dirs:
        fold_name = fold_dir.name
        subject_ids = extract_subject_ids_from_fold(fold_name)
        
        # Find results.json in this fold
        results_files = list(fold_dir.rglob("results.json"))
        if not results_files:
            # Try task directories
            task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
            for task_dir in task_dirs:
                results_file = task_dir / "results.json"
                if results_file.exists():
                    results_files.append(results_file)
                    break
        
        if results_files:
            try:
                with open(results_files[0], 'r') as f:
                    data = json.load(f)
                accuracy = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                if accuracy is not None:
                    acc = float(accuracy)
                    fold_to_accuracy[fold_name] = acc
                    # Add this accuracy to all subjects in this fold
                    for subject_id in subject_ids:
                        subject_accuracies[subject_id].append(acc)
            except Exception as e:
                continue
    
    return dict(subject_accuracies)

def analyze_subject_swings(subject_accuracies):
    """Calculate statistics for each subject."""
    subject_stats = {}
    
    for subject_id, accuracies in subject_accuracies.items():
        if accuracies:
            subject_stats[subject_id] = {
                'mean': statistics.mean(accuracies),
                'median': statistics.median(accuracies),
                'min': min(accuracies),
                'max': max(accuracies),
                'swing': max(accuracies) - min(accuracies),
                'std': statistics.stdev(accuracies) if len(accuracies) > 1 else 0,
                'n_folds': len(accuracies)
            }
    
    return subject_stats

def create_visualizations(subject_stats_by_exp, output_dir):
    """Create visualizations for per-subject accuracy analysis."""
    if not HAS_MATPLOTLIB:
        print("   ⚠️  Skipping visualizations (matplotlib not available)")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # 1. Per-subject mean accuracy comparison across experiments
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Per-Subject Accuracy Analysis Across LPSO Experiments', fontsize=16, fontweight='bold')
    
    for idx, (exp_name, exp_data) in enumerate(subject_stats_by_exp.items()):
        if not exp_data:
            continue
        
        ax = axes[idx // 2, idx % 2]
        
        # Sort subjects by mean accuracy
        subjects = sorted(exp_data.keys(), key=lambda x: exp_data[x]['mean'])
        means = [exp_data[s]['mean'] * 100 for s in subjects]
        mins = [exp_data[s]['min'] * 100 for s in subjects]
        maxs = [exp_data[s]['max'] * 100 for s in subjects]
        
        # Create error bars
        y_pos = range(len(subjects))
        ax.errorbar(means, y_pos, xerr=[[means[i] - mins[i] for i in range(len(means))],
                                         [maxs[i] - means[i] for i in range(len(means))]],
                   fmt='o', capsize=5, capthick=2, alpha=0.7, color='steelblue')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(subjects, fontsize=8)
        ax.set_xlabel('Accuracy (%)', fontsize=10)
        ax.set_title(f"{exp_name}\n(Mean ± Range)", fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        ax.set_xlim(0, 100)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'per_subject_accuracy_comparison.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: per_subject_accuracy_comparison.png")
    
    # 2. Swing analysis (max - min accuracy per subject)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Per-Subject Accuracy Swing (Max - Min) Analysis', fontsize=16, fontweight='bold')
    
    for idx, (exp_name, exp_data) in enumerate(subject_stats_by_exp.items()):
        if not exp_data:
            continue
        
        ax = axes[idx // 2, idx % 2]
        
        subjects = sorted(exp_data.keys(), key=lambda x: exp_data[x]['swing'], reverse=True)
        swings = [exp_data[s]['swing'] * 100 for s in subjects]
        
        colors = ['red' if s > 30 else 'orange' if s > 20 else 'steelblue' for s in swings]
        bars = ax.barh(range(len(subjects)), swings, color=colors, alpha=0.7)
        
        ax.set_yticks(range(len(subjects)))
        ax.set_yticklabels(subjects, fontsize=8)
        ax.set_xlabel('Swing (Max - Min Accuracy, %)', fontsize=10)
        ax.set_title(f"{exp_name}\n(Largest Swings Highlighted)", fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, swing) in enumerate(zip(bars, swings)):
            ax.text(swing + 1, i, f'{swing:.1f}%', va='center', fontsize=7)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'per_subject_swing_analysis.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: per_subject_swing_analysis.png")
    
    # 3. Find biggest swings
    print("\n" + "=" * 80)
    print("TOP 20 SUBJECTS WITH LARGEST SWINGS (Biggest Variance)")
    print("=" * 80)
    
    all_swings = []
    for exp_name, exp_data in subject_stats_by_exp.items():
        if exp_data:
            for subject_id, stats in exp_data.items():
                all_swings.append({
                    'experiment': exp_name,
                    'subject': subject_id,
                    'swing': stats['swing'] * 100,
                    'mean': stats['mean'] * 100,
                    'min': stats['min'] * 100,
                    'max': stats['max'] * 100,
                    'n_folds': stats['n_folds']
                })
    
    all_swings.sort(key=lambda x: x['swing'], reverse=True)
    
    print(f"\n{'Rank':<6} {'Subject':<10} {'Experiment':<30} {'Swing':<8} {'Range':<20} {'Mean':<8} {'Folds':<6}")
    print("-" * 100)
    for i, swing_data in enumerate(all_swings[:20], 1):
        print(f"{i:2d}.   {swing_data['subject']:8s} | {swing_data['experiment']:28s} | "
              f"{swing_data['swing']:6.1f}% | "
              f"{swing_data['min']:5.1f}%-{swing_data['max']:5.1f}% | "
              f"{swing_data['mean']:5.1f}% | "
              f"{swing_data['n_folds']:3d}")
    
    # Save top swings to file
    swings_file = output_dir / 'biggest_swings_summary.md'
    with open(swings_file, 'w') as f:
        f.write("# Top 20 Subjects with Largest Accuracy Swings\n\n")
        f.write("| Rank | Subject | Experiment | Swing | Range (Min-Max) | Mean | N Folds |\n")
        f.write("|------|---------|------------|-------|-----------------|------|----------|\n")
        for i, swing_data in enumerate(all_swings[:20], 1):
            f.write(f"| {i} | {swing_data['subject']} | {swing_data['experiment']} | "
                   f"{swing_data['swing']:.1f}% | "
                   f"{swing_data['min']:.1f}% - {swing_data['max']:.1f}% | "
                   f"{swing_data['mean']:.1f}% | {swing_data['n_folds']} |\n")
    
    print(f"\n   ✅ Saved: {swings_file}")

def main():
    """Main function."""
    print("=" * 80)
    print("PER-SUBJECT ACCURACY ANALYSIS ACROSS LPSO EXPERIMENTS")
    print("=" * 80)
    
    subject_stats_by_exp = {}
    
    for exp_name, exp_info in EXPERIMENTS.items():
        print(f"\n📊 Analyzing {exp_name} ({exp_info['description']})...")
        print(f"   Path: {exp_info['path']}")
        
        subject_accuracies = extract_per_subject_accuracies(exp_info['path'], best_model_only=True)
        
        if subject_accuracies:
            print(f"   ✅ Found {len(subject_accuracies)} subjects")
            subject_stats = analyze_subject_swings(subject_accuracies)
            subject_stats_by_exp[exp_name] = subject_stats
            
            # Show summary
            swings = [s['swing'] * 100 for s in subject_stats.values()]
            means = [s['mean'] * 100 for s in subject_stats.values()]
            
            print(f"      Mean accuracy across subjects: {statistics.mean(means):.2f}%")
            print(f"      Mean swing: {statistics.mean(swings):.2f}%")
            print(f"      Largest swing: {max(swings):.2f}%")
        else:
            print(f"   ⚠️  No results found")
            subject_stats_by_exp[exp_name] = {}
    
    # Create visualizations
    print("\n" + "=" * 80)
    print("CREATING VISUALIZATIONS")
    print("=" * 80)
    
    output_dir = BASE_DIR / "per_subject_analysis"
    create_visualizations(subject_stats_by_exp, output_dir)
    
    # Save detailed results
    print("\n" + "=" * 80)
    print("SAVING DETAILED RESULTS")
    print("=" * 80)
    
    results_file = BASE_DIR / "per_subject_accuracy_analysis.md"
    with open(results_file, 'w') as f:
        f.write("# Per-Subject Accuracy Analysis Across LPSO Experiments\n\n")
        
        for exp_name, exp_data in subject_stats_by_exp.items():
            if not exp_data:
                continue
            
            f.write(f"## {exp_name}\n\n")
            f.write("| Subject | Mean | Min | Max | Swing | Std Dev | N Folds |\n")
            f.write("|---------|------|-----|-----|-------|---------|----------|\n")
            
            # Sort by swing (descending)
            sorted_subjects = sorted(exp_data.items(), key=lambda x: x[1]['swing'], reverse=True)
            
            for subject_id, stats in sorted_subjects:
                f.write(f"| {subject_id} | {stats['mean']:.2%} | {stats['min']:.2%} | "
                       f"{stats['max']:.2%} | {stats['swing']:.2%} | "
                       f"{stats['std']:.2%} | {stats['n_folds']} |\n")
            
            f.write("\n")
    
    print(f"   ✅ Saved: {results_file}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

