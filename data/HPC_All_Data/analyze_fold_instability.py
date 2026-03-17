#!/usr/bin/env python
"""
Analyze fold-by-fold instability to demonstrate single-fold performance variance.

This script extracts per-fold performance for specific model+feature combinations
to create a table showing how dramatically performance can vary across folds.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import statistics

# Set up paths
BASE_DIR = Path(__file__).parent
GRID_50_DIR = BASE_DIR / "grid_50_random_folds"
GRID_12_DIR = BASE_DIR / "grid_12_folds"

def load_fold_results_from_results_json(results_dir: Path, model_name: str) -> list:
    """Load all fold results from results.json files for a specific model."""
    fold_results = []
    
    model_dir = results_dir / model_name
    if not model_dir.exists():
        return fold_results
    
    # Find all results.json files for this model
    results_files = list(model_dir.rglob("results.json"))
    
    for results_file in results_files:
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            # Extract fold information
            fold_id = data.get('fold_id', '')
            fold_name = results_file.parent.name  # Usually "sub-X_sub-Y"
            
            # Get accuracy
            accuracy = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
            
            if accuracy is not None:
                fold_results.append({
                    'fold_name': fold_name,
                    'fold_id': str(fold_id),
                    'accuracy': float(accuracy),
                    'model': model_name,
                    'path': str(results_file)
                })
        except Exception as e:
            continue
    
    return fold_results

def extract_fold_performances(experiment_path: Path, model_name: str = None) -> dict:
    """Extract per-fold performances for all models or a specific model."""
    fold_performances = {}
    
    # Try ml_results_grid_search subdirectory first
    ml_results_path = experiment_path / "ml_results_grid_search"
    if not ml_results_path.exists():
        ml_results_path = experiment_path
    
    if not ml_results_path.exists():
        return fold_performances
    
    # Get model directories
    if model_name:
        model_dirs = [ml_results_path / model_name] if (ml_results_path / model_name).exists() else []
    else:
        model_dirs = [d for d in ml_results_path.iterdir() 
                      if d.is_dir() and d.name not in ['graphs', 'debug'] and not d.name.startswith('_')]
    
    for model_dir in model_dirs:
        if not model_dir.exists():
            continue
            
        m_name = model_dir.name
        accuracies = []
        fold_names = []
        
        # Get all fold directories or results.json files
        results_files = list(model_dir.rglob("results.json"))
        
        for results_file in results_files:
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                
                acc = data.get('test_accuracy') or data.get('test_results', {}).get('accuracy')
                if acc is not None:
                    accuracies.append(float(acc))
                    # Get fold name from path
                    fold_name = results_file.parent.name
                    if not fold_name or not fold_name.startswith('sub-'):
                        # Try parent's parent
                        fold_name = results_file.parent.parent.name
                    fold_names.append(fold_name if fold_name.startswith('sub-') else str(data.get('fold_id', '')))
            except:
                pass
        
        if accuracies:
            fold_performances[m_name] = {
                'accuracies': accuracies,
                'fold_names': fold_names
            }
    
    return fold_performances

def find_most_variable_combinations(base_dir: Path, experiment_dirs: dict):
    """Find the most variable model+feature combinations across folds."""
    all_combinations = []
    
    for exp_name, exp_path in experiment_dirs.items():
        # Extract feature type from name
        if 'anova' in exp_name.lower():
            feature_type = 'ANOVA'
        elif 'pca' in exp_name.lower():
            feature_type = 'PCA'
        else:
            feature_type = 'Unknown'
        
        # Extract fold sizes if possible
        if 'L_2' in exp_name or 'l_2' in exp_name:
            fold_size = 'L_2'
        elif 'L_6' in exp_name or 'l_6' in exp_name:
            fold_size = 'L_6'
        else:
            fold_size = 'Unknown'
        
        print(f"\n📊 Analyzing {exp_name} ({feature_type}, {fold_size})...")
        
        # Extract fold performances
        fold_perfs = extract_fold_performances(exp_path)
        
        for model_name, model_data in fold_perfs.items():
            accuracies = model_data['accuracies']
            fold_names = model_data['fold_names']
            
            if len(accuracies) < 3:  # Need at least 3 folds for meaningful variance
                continue
            
            # Calculate statistics
            mean_acc = statistics.mean(accuracies)
            std_acc = statistics.stdev(accuracies) if len(accuracies) > 1 else 0
            min_acc = min(accuracies)
            max_acc = max(accuracies)
            range_acc = max_acc - min_acc
            
            # Sort to find extremes
            sorted_data = sorted(zip(accuracies, fold_names), key=lambda x: x[0])
            
            all_combinations.append({
                'experiment': exp_name,
                'feature': feature_type,
                'fold_size': fold_size,
                'model': model_name,
                'mean': mean_acc,
                'std': std_acc,
                'min': min_acc,
                'max': max_acc,
                'range': range_acc,
                'cv': std_acc / mean_acc if mean_acc > 0 else 0,
                'num_folds': len(accuracies),
                'accuracies': accuracies,
                'fold_names': fold_names,
                'sorted_data': sorted_data
            })
            
            print(f"   {model_name}: {len(accuracies)} folds, mean={mean_acc:.3f}, std={std_acc:.3f}, range=[{min_acc:.3f}, {max_acc:.3f}]")
    
    return all_combinations

def create_instability_table(combinations: list, top_n: int = 10):
    """Create a table showing the most variable fold performances."""
    
    # Sort by range (most variable first)
    sorted_combos = sorted(combinations, key=lambda x: x['range'], reverse=True)
    
    print("\n" + "=" * 80)
    print("SINGLE-FOLD INSTABILITY ANALYSIS")
    print("=" * 80)
    
    # Find most dramatic examples
    print("\n📊 Top 10 Most Variable Model+Feature Combinations:")
    print("-" * 80)
    
    for i, combo in enumerate(sorted_combos[:top_n], 1):
        print(f"\n{i}. {combo['model']} + {combo['feature']} ({combo['experiment']}):")
        print(f"   Range: {combo['min']:.1%} - {combo['max']:.1%} (span: {combo['range']:.1%})")
        print(f"   Mean: {combo['mean']:.1%}, Std: {combo['std']:.1%}, CV: {combo['cv']:.1%}")
        print(f"   Folds: {combo['num_folds']}")
    
    # Create table examples
    print("\n" + "=" * 80)
    print("TABLE 1: Single-Fold Instability Examples")
    print("=" * 80)
    
    # Get best examples showing high variance
    examples = []
    
    # Look for combinations with:
    # 1. High range (max - min)
    # 2. Multiple folds available
    # 3. Clear feature type
    for combo in sorted_combos:
        if combo['num_folds'] >= 3 and combo['feature'] != 'Unknown':
            # Select a few representative folds
            sorted_data = combo['sorted_data']
            num_folds = len(sorted_data)
            
            # Select: min, median, max, and a couple in between
            selected_folds = []
            if num_folds >= 1:
                selected_folds.append(sorted_data[0])  # Min
            if num_folds >= 3:
                selected_folds.append(sorted_data[num_folds // 3])  # Lower quartile
            if num_folds >= 2:
                selected_folds.append(sorted_data[num_folds // 2])  # Median
            if num_folds >= 3:
                selected_folds.append(sorted_data[2 * num_folds // 3])  # Upper quartile
            if num_folds >= 1:
                selected_folds.append(sorted_data[-1])  # Max
            
            examples.append({
                'model': combo['model'],
                'feature': combo['feature'],
                'fold_size': combo['fold_size'],
                'selected_folds': selected_folds[:5],  # Limit to 5 folds for table
                'range': combo['range'],
                'min': combo['min'],
                'max': combo['max'],
                'mean': combo['mean'],
                'std': combo['std']
            })
            
            if len(examples) >= 5:  # Get top 5 examples
                break
    
    # Generate markdown table
    print("\n### Markdown Table Format:\n")
    print("```markdown")
    
    for example in examples:
        model_feature = f"{example['model']} + {example['feature']}"
        
        # Create header
        fold_headers = [f"Fold {chr(65+i)}" for i in range(len(example['selected_folds']))]  # A, B, C, D, E
        header = f"| Model + Features | {' | '.join(fold_headers)} |"
        separator = f"|------------------|{' | '.join(['--------' for _ in fold_headers])} |"
        
        # Create data row
        fold_values = [f"{acc:.1%}" for acc, _ in example['selected_folds']]
        data_row = f"| {model_feature} | {' | '.join(fold_values)} |"
        
        print(header)
        print(separator)
        print(data_row)
        print()
        
        # Print summary statistics
        print(f"Range: {example['min']:.1%} - {example['max']:.1%} (span: {example['range']:.1%})")
        print(f"Mean: {example['mean']:.1%} ± {example['std']:.1%}")
        print()
    
    print("```")
    
    # Also create a detailed CSV
    print("\n" + "=" * 80)
    print("DETAILED PER-FOLD DATA")
    print("=" * 80)
    
    detailed_data = []
    for example in examples:
        for fold_acc, fold_name in example['selected_folds']:
            detailed_data.append({
                'model': example['model'],
                'feature': example['feature'],
                'fold_size': example['fold_size'],
                'fold_name': fold_name,
                'accuracy': fold_acc,
                'accuracy_pct': f"{fold_acc:.1%}"
            })
    
    df = pd.DataFrame(detailed_data)
    output_file = BASE_DIR / "fold_instability_examples.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Saved detailed per-fold data to: {output_file}")
    
    return examples

def main():
    """Main function."""
    print("=" * 80)
    print("FOLD INSTABILITY ANALYSIS")
    print("=" * 80)
    
    # Define experiments
    experiments_50 = {
        'Anova_L_2_incomplete': GRID_50_DIR / 'Anova_L_2_incomplete_ml_results',
        'Anova_L_6_Incomplete': GRID_50_DIR / 'Anova_L_6_Incomplete_ml_results',
        'PCA_L_2': GRID_50_DIR / 'PCA_L_2_ml_results',
        'PCA_L_6': GRID_50_DIR / 'PCA_L_6_ml_results',
    }
    
    experiments_12 = {
        'ANOVA_L_6_C_Resource_Boosted': GRID_12_DIR / 'ANOVA_L_6_C_Resource_Boosted' / 'ml_results_grid_search',
        'PCA_L_6_C-3': GRID_12_DIR / 'PCA_L_6_C-3' / 'ml_results_grid_search',
    }
    
    # Analyze grid_50_random_folds (more folds = better for instability analysis)
    print("\n📊 Analyzing Grid 50 Random Folds...")
    combinations_50 = find_most_variable_combinations(GRID_50_DIR, experiments_50)
    
    # Also check grid_12_folds
    print("\n📊 Analyzing Grid 12 Folds...")
    combinations_12 = find_most_variable_combinations(GRID_12_DIR, experiments_12)
    
    # Combine and analyze
    all_combinations = combinations_50 + combinations_12
    
    # Create instability table
    examples = create_instability_table(all_combinations, top_n=10)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\n💡 Key Insight:")
    print("   Single LPSO folds can vary dramatically (e.g., 47%-98%).")
    print("   Median + IQR over many folds is required for robust evaluation.")
    print("=" * 80)

if __name__ == '__main__':
    main()


