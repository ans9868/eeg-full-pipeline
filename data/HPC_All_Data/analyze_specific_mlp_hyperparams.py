#!/usr/bin/env python
"""
Analyze performance of specific MLP hyperparameter combination across folds.

This script extracts performance for MLP with:
- hidden_layer_sizes: [100]
- activation: "tanh"
- alpha: 0.1

Across all folds to demonstrate variance.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
import statistics

# Set up paths
BASE_DIR = Path(__file__).parent

# Define experiments to analyze
EXPERIMENTS = {
    "ANOVA_L_2": BASE_DIR / "grid_50_random_folds/Anova_L_2_incomplete_ml_results/MLP_(Neural_Network)",
    "PCA_L_2": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results/MLP_(Neural_Network)",
}

# Target hyperparameters
TARGET_HYPERPARAMS = {
    "hidden_layer_sizes": [100],
    "activation": "tanh",
    "alpha": "0.1"
}

def normalize_hyperparams(hyperparams):
    """Normalize hyperparameters for comparison."""
    normalized = {}
    for key, value in hyperparams.items():
        if key == "hidden_layer_sizes":
            # Convert to list and sort if it's a list
            if isinstance(value, list):
                normalized[key] = sorted(value)
            else:
                normalized[key] = [value] if value else []
        elif key == "alpha":
            # Convert to string for comparison
            normalized[key] = str(value)
        else:
            normalized[key] = value
    return normalized

def matches_target(hyperparams):
    """Check if hyperparameters match target."""
    normalized = normalize_hyperparams(hyperparams)
    target_normalized = normalize_hyperparams(TARGET_HYPERPARAMS)
    
    # Check hidden_layer_sizes
    if normalized.get("hidden_layer_sizes") != target_normalized.get("hidden_layer_sizes"):
        return False
    
    # Check activation
    if normalized.get("activation") != target_normalized.get("activation"):
        return False
    
    # Check alpha
    if normalized.get("alpha") != target_normalized.get("alpha"):
        return False
    
    return True

def extract_fold_performances(mlp_results_dir):
    """Extract performances for target hyperparameters across all folds for a specific experiment."""
    fold_results = []
    
    if not mlp_results_dir.exists():
        print(f"⚠️  Directory not found: {mlp_results_dir}")
        return []
    
    # Find all results.json files
    results_files = list(mlp_results_dir.rglob("results.json"))
    
    for results_file in results_files:
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            # Check hyperparameters
            hyperparams = data.get('hyperparams', {})
            
            if not matches_target(hyperparams):
                continue
            
            # Extract fold information
            # The fold name is the parent directory (e.g., "sub-13_sub-59")
            # Sometimes results.json is in task_XXX subdirectory, so need parent.parent
            if results_file.parent.name.startswith('task_'):
                fold_name = results_file.parent.parent.name
            else:
                fold_name = results_file.parent.name
            
            # Get accuracy
            accuracy = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
            
            if accuracy is not None:
                fold_results.append({
                    'fold_name': fold_name,
                    'fold_id': data.get('fold_id', ''),
                    'accuracy': float(accuracy),
                    'test_f1': data.get('test_results', {}).get('f1'),
                    'test_precision': data.get('test_results', {}).get('precision'),
                    'test_recall': data.get('test_results', {}).get('recall'),
                    'train_accuracy': data.get('train_accuracy') or data.get('train_results', {}).get('accuracy'),
                    'task_id': data.get('task_id', ''),
                    'path': str(results_file)
                })
        except Exception as e:
            continue
    
    return fold_results

def analyze_variance(fold_results, exp_name):
    """Analyze variance in fold performances."""
    if not fold_results:
        print("❌ No results found for target hyperparameters")
        return
    
    accuracies = [r['accuracy'] for r in fold_results]
    
    # Calculate statistics
    mean_acc = statistics.mean(accuracies)
    median_acc = statistics.median(accuracies)
    std_acc = statistics.stdev(accuracies) if len(accuracies) > 1 else 0
    min_acc = min(accuracies)
    max_acc = max(accuracies)
    range_acc = max_acc - min_acc
    
    # Calculate quartiles
    sorted_acc = sorted(accuracies)
    n = len(sorted_acc)
    q1_idx = n // 4
    q3_idx = 3 * n // 4
    q1 = sorted_acc[q1_idx] if q1_idx < n else sorted_acc[0]
    q3 = sorted_acc[q3_idx] if q3_idx < n else sorted_acc[-1]
    iqr = q3 - q1
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"PERFORMANCE ANALYSIS: {exp_name} - MLP with [100] hidden layers, tanh activation, alpha=0.1")
    print("=" * 80)
    print(f"\n📊 Statistics across {len(fold_results)} folds:")
    print(f"   Mean:     {mean_acc:.1%}")
    print(f"   Median:   {median_acc:.1%}")
    print(f"   Std Dev:  {std_acc:.1%}")
    print(f"   Min:      {min_acc:.1%}")
    print(f"   Max:      {max_acc:.1%}")
    print(f"   Range:    {range_acc:.1%} (span: {range_acc:.1f} percentage points)")
    print(f"   Q1:       {q1:.1%}")
    print(f"   Q3:       {q3:.1%}")
    print(f"   IQR:      {iqr:.1%}")
    
    # Create table with selected folds
    sorted_results = sorted(fold_results, key=lambda x: x['accuracy'])
    
    # Select representative folds
    num_folds = len(sorted_results)
    selected_indices = []
    
    if num_folds >= 1:
        selected_indices.append(0)  # Minimum
    if num_folds >= 3:
        selected_indices.append(num_folds // 4)  # Lower quartile
    if num_folds >= 2:
        selected_indices.append(num_folds // 2)  # Median
    if num_folds >= 3:
        selected_indices.append(3 * num_folds // 4)  # Upper quartile
    if num_folds >= 1:
        selected_indices.append(num_folds - 1)  # Maximum
    
    selected_folds = [sorted_results[i] for i in selected_indices]
    
    # Generate markdown table
    print("\n" + "=" * 80)
    print("TABLE: Single Hyperparameter Combination Across Folds")
    print("=" * 80)
    print("\n```markdown")
    
    # Create header
    fold_labels = [f"Fold {chr(65+i)}" for i in range(len(selected_folds))]
    header = f"| Fold | {' | '.join(fold_labels)} |"
    separator = f"|------|{' | '.join(['--------' for _ in fold_labels])} |"
    acc_values = [f"{r['accuracy']:.1%}" for r in selected_folds]
    data_row = f"| Accuracy | {' | '.join(acc_values)} |"
    
    print(header)
    print(separator)
    print(data_row)
    print()
    
    # Print fold details
    print("### Fold Details\n")
    for i, fold in enumerate(selected_folds):
        label = chr(65 + i)  # A, B, C, D, E
        subjects = fold['fold_name'].replace('sub-', '').replace('_', ', ')
        print(f"**Fold {label} ({fold['accuracy']:.1%}):**")
        print(f"- **Fold Name:** `{fold['fold_name']}`")
        print(f"- **Test Subjects:** {subjects}")
        print(f"- **Accuracy:** {fold['accuracy']:.1%}")
        print()
    
    print("```")
    
    # Save detailed CSV
    sorted_results = sorted(fold_results, key=lambda x: x['accuracy'])
    output_file = BASE_DIR / f"mlp_hidden100_tanh_alpha01_{exp_name.lower()}_performance.csv"
    
    if sorted_results:
        fieldnames = sorted_results[0].keys()
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_results)
        print(f"\n✅ Saved detailed results to: {output_file}")
    
    # Create markdown file
    markdown_content = f"""# MLP Performance: [100] Hidden Layers, Tanh, Alpha=0.1 - {exp_name}

## Feature Extraction Method

**{exp_name}**

## Hyperparameter Configuration

```yaml
hidden_layer_sizes: [100]
activation: "tanh"
alpha: 0.1
```

---

## Performance Statistics

- **Number of Folds:** {len(fold_results)}
- **Mean:** {mean_acc:.1%} ± {std_acc:.1%}
- **Median:** {median_acc:.1%}
- **Range:** {min_acc:.1%} - {max_acc:.1%} (span: **{range_acc:.1f} percentage points**)
- **Interquartile Range (IQR):** {iqr:.1%}
- **Standard Deviation:** {std_acc:.1%}

---

## Table: Performance Across Folds

| Fold | {' | '.join(fold_labels)} |
|------|{' | '.join(['--------' for _ in fold_labels])} |
| Accuracy | {' | '.join([f"{r['accuracy']:.1%}" for r in selected_folds])} |

---

## Individual Fold Details

"""
    
    for i, fold in enumerate(selected_folds):
        label = chr(65 + i)
        subjects = fold['fold_name'].replace('sub-', '').replace('_', ', ')
        percentile = ""
        if i == 0:
            percentile = " (Minimum)"
        elif i == len(selected_folds) - 1:
            percentile = " (Maximum)"
        elif i == len(selected_folds) // 2:
            percentile = " (Median)"
        elif i == len(selected_folds) // 4:
            percentile = " (Lower Quartile)"
        elif i == 3 * len(selected_folds) // 4:
            percentile = " (Upper Quartile)"
        
        markdown_content += f"""### Fold {label} ({fold['accuracy']:.1%}{percentile})
- **Fold Name:** `{fold['fold_name']}`
- **Test Subjects:** {subjects}
- **Accuracy:** {fold['accuracy']:.1%}
- **F1 Score:** {fold.get('test_f1', 0):.1%} (if available)
- **Precision:** {fold.get('test_precision', 0):.1%} (if available)
- **Recall:** {fold.get('test_recall', 0):.1%} (if available)

"""
    
    markdown_content += f"""---

## Interpretation

This analysis demonstrates **fold-to-fold variance** for a single hyperparameter combination. Even with fixed hyperparameters (single hidden layer of 100 neurons, tanh activation, alpha=0.1), performance varies dramatically depending on which subjects are left out for testing.

**Key Observations:**
1. **Fixed Hyperparameters:** All folds use identical model architecture and training settings
2. **Subject-Dependent Performance:** Variance comes from which subjects are in test vs. train sets
3. **Range:** Performance spans {range_acc:.1f} percentage points ({min_acc:.1%} to {max_acc:.1%})
4. **Why Median + IQR?** This variance shows why reporting median and IQR over many folds is essential - a single fold result ({min_acc:.1%} vs {max_acc:.1%}) can be highly misleading.

---

## Full Data

All {len(fold_results)} fold results are available in: `mlp_hidden100_tanh_alpha01_{exp_name.lower()}_performance.csv`

*Generated by `analyze_specific_mlp_hyperparams.py`*
"""
    
    markdown_file = BASE_DIR / f"mlp_hidden100_tanh_alpha01_{exp_name.lower()}_performance.md"
    with open(markdown_file, 'w') as f:
        f.write(markdown_content)
    print(f"✅ Saved markdown report to: {markdown_file}")
    
    return fold_results

def main():
    """Main function."""
    print("=" * 80)
    print("ANALYZING SPECIFIC MLP HYPERPARAMETER COMBINATION")
    print("=" * 80)
    print(f"\n🔍 Target hyperparameters:")
    print(f"   hidden_layer_sizes: {TARGET_HYPERPARAMS['hidden_layer_sizes']}")
    print(f"   activation: {TARGET_HYPERPARAMS['activation']}")
    print(f"   alpha: {TARGET_HYPERPARAMS['alpha']}")
    
    # Analyze each experiment separately
    for exp_name, mlp_results_dir in EXPERIMENTS.items():
        print(f"\n{'='*80}")
        print(f"Analyzing {exp_name}")
        print(f"{'='*80}")
        
        # Extract fold performances
        fold_results = extract_fold_performances(mlp_results_dir)
        
        if fold_results:
            print(f"✅ Found {len(fold_results)} folds with matching hyperparameters")
            analyze_variance(fold_results, exp_name)
        else:
            print(f"\n❌ No matching results found for {exp_name}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()

