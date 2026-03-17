#!/usr/bin/env python
"""
Generate graphs and CSV analysis from HPC compiled ML results.

This script:
1. Loads ML results from a directory
2. Aggregates results across models and folds
3. Generates graphs and CSV files
4. Creates comprehensive analysis
"""

import sys
import os
from pathlib import Path

# Add eeg-ray-tuner to path
project_root = Path(__file__).parent.parent.parent
eeg_ray_tuner_path = project_root / 'eeg-ray-tuner'
sys.path.insert(0, str(eeg_ray_tuner_path))

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Import Ray Tuner modules
try:
    from eeg_ray_tuner.results.result_aggregator import ResultAggregator
    from eeg_ray_tuner.results.result_saver import ResultSaver
    from eeg_ray_tuner.visualization.graph_generator import GraphGenerator
    from config_handler import UnifiedConfigHandler
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure you're running from the correct directory")
    sys.exit(1)


def load_tasks_from_csv(task_table_path: Path) -> List[Dict]:
    """Load tasks from task_table.csv."""
    if not task_table_path.exists():
        print(f"⚠️ Task table not found: {task_table_path}")
        return []
    
    df = pd.read_csv(task_table_path)
    
    tasks = []
    for _, row in df.iterrows():
        if row['status'] == 'completed':
            # Parse hyperparams
            try:
                hyperparams = json.loads(row['hyperparams']) if pd.notna(row['hyperparams']) else {}
            except:
                hyperparams = {}
            
            task = {
                'task_id': row['task_id'],
                'model_name': row['model_name'],
                'fold_id': str(row['fold_id']),
                'hyperparams': hyperparams,
                'results_path': row['results_path'],
            }
            tasks.append(task)
    
    print(f"✅ Loaded {len(tasks)} completed tasks from CSV")
    return tasks


def load_result_file(results_path: str) -> Optional[Dict]:
    """Load a single results.json file."""
    results_file = Path(results_path) / 'results.json'
    
    if not results_file.exists():
        return None
    
    try:
        with open(results_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading {results_file}: {e}")
        return None


def aggregate_results(ml_results_dir: Path, tasks: List[Dict]) -> Dict[str, Any]:
    """Aggregate results from tasks."""
    print(f"\n📊 Aggregating results from {len(tasks)} tasks...")
    
    # Group by model
    model_results = defaultdict(list)
    
    for task in tasks:
        model_name = task['model_name']
        result_data = load_result_file(task['results_path'])
        
        if result_data:
            result_data['hyperparams'] = task['hyperparams']
            result_data['fold_id'] = task['fold_id']
            model_results[model_name].append(result_data)
    
    # Create mock config handler for aggregation
    class MockConfigHandler:
        optimization_metric = 'accuracy'
    
    config_handler = MockConfigHandler()
    aggregator = ResultAggregator(config_handler)
    
    # Convert to MLTask-like objects (simplified)
    class SimpleTask:
        def __init__(self, task_dict):
            self.model_name = task_dict['model_name']
            self.results_path = task_dict['results_path']
            self.status = 'completed'
        
        def __getattr__(self, name):
            return None
    
    # Aggregate
    aggregated = {}
    for model_name, results in model_results.items():
        print(f"   📊 Processing {model_name}: {len(results)} results")
        
        # Aggregate manually (simpler approach)
        aggregated[model_name] = aggregate_model_results(model_name, results)
    
    return aggregated


def aggregate_model_results(model_name: str, results: List[Dict]) -> Dict[str, Any]:
    """Aggregate results for a single model."""
    # Group by hyperparameters
    hyperparam_groups = defaultdict(list)
    
    for result in results:
        hyperparams = result.get('hyperparams', {})
        hyperparam_key = json.dumps(hyperparams, sort_keys=True)
        hyperparam_groups[hyperparam_key].append(result)
    
    # Aggregate each hyperparameter combination
    hyperparam_aggregates = []
    
    for hyperparam_key, group_results in hyperparam_groups.items():
        test_accuracies = []
        test_f1s = []
        test_precisions = []
        test_recalls = []
        train_accuracies = []
        
        for r in group_results:
            test_results = r.get('test_results', {})
            train_results = r.get('train_results', {})
            
            if 'accuracy' in test_results:
                test_accuracies.append(test_results['accuracy'])
            if 'f1' in test_results:
                test_f1s.append(test_results['f1'])
            if 'precision' in test_results:
                test_precisions.append(test_results['precision'])
            if 'recall' in test_results:
                test_recalls.append(test_results['recall'])
            if 'accuracy' in train_results:
                train_accuracies.append(train_results['accuracy'])
        
        if test_accuracies:
            hyperparam_aggregates.append({
                'hyperparams': json.loads(hyperparam_key),
                'mean_test_accuracy': np.mean(test_accuracies),
                'std_test_accuracy': np.std(test_accuracies),
                'mean_test_f1': np.mean(test_f1s) if test_f1s else 0,
                'mean_test_precision': np.mean(test_precisions) if test_precisions else 0,
                'mean_test_recall': np.mean(test_recalls) if test_recalls else 0,
                'mean_train_accuracy': np.mean(train_accuracies) if train_accuracies else 0,
                'num_folds': len(group_results),
                'fold_results': group_results,
            })
    
    # Find best hyperparameters
    if hyperparam_aggregates:
        hyperparam_aggregates.sort(key=lambda x: x['mean_test_accuracy'], reverse=True)
        best = hyperparam_aggregates[0]
        
        return {
            'model_name': model_name,
            'best_hyperparams': best['hyperparams'],
            'best_metrics': {
                'test_accuracy': best['mean_test_accuracy'],
                'std_test_accuracy': best['std_test_accuracy'],
                'test_f1': best['mean_test_f1'],
                'test_precision': best['mean_test_precision'],
                'test_recall': best['mean_test_recall'],
                'train_accuracy': best['mean_train_accuracy'],
                'std_train_accuracy': 0,  # Would need to calculate
            },
            'all_hyperparameter_results': hyperparam_aggregates,
            'total_tasks': len(results),
            'num_folds': best['num_folds'],
        }
    else:
        return {
            'model_name': model_name,
            'error': 'No valid results found'
        }


def save_model_comparison_csv(aggregated_results: Dict[str, Any], output_dir: Path):
    """Save model comparison CSV."""
    rows = []
    
    for model_name, results in aggregated_results.items():
        if 'error' not in results:
            best_metrics = results.get('best_metrics', {})
            row = {
                'model_name': model_name,
                'best_test_accuracy': best_metrics.get('test_accuracy', 0),
                'std_test_accuracy': best_metrics.get('std_test_accuracy', 0),
                'best_train_accuracy': best_metrics.get('train_accuracy', 0),
                'std_train_accuracy': best_metrics.get('std_train_accuracy', 0),
                'test_f1': best_metrics.get('test_f1', 0),
                'test_precision': best_metrics.get('test_precision', 0),
                'test_recall': best_metrics.get('test_recall', 0),
                'num_folds': results.get('num_folds', 0),
                'total_tasks': results.get('total_tasks', 0),
                'best_hyperparams': str(results.get('best_hyperparams', {}))
            }
            rows.append(row)
    
    if rows:
        df = pd.DataFrame(rows)
        df = df.sort_values('best_test_accuracy', ascending=False)
        
        csv_file = output_dir / 'model_comparison.csv'
        df.to_csv(csv_file, index=False)
        print(f"✅ Saved model comparison CSV: {csv_file}")
        return csv_file
    else:
        print("⚠️ No results to save")
        return None


def main():
    """Main analysis function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate graphs and CSV from ML results')
    parser.add_argument('ml_results_dir', type=str, help='Path to ml_results directory')
    parser.add_argument('--config', type=str, help='Path to config file (optional)')
    parser.add_argument('--graphs-only', action='store_true', help='Only generate graphs')
    parser.add_argument('--csv-only', action='store_true', help='Only generate CSV')
    
    args = parser.parse_args()
    
    ml_results_dir = Path(args.ml_results_dir).resolve()
    
    if not ml_results_dir.exists():
        print(f"❌ ML results directory not found: {ml_results_dir}")
        sys.exit(1)
    
    print("="*70)
    print("ML RESULTS ANALYSIS GENERATOR")
    print("="*70)
    print(f"📁 ML Results Directory: {ml_results_dir}")
    
    # Load task table
    task_table_path = ml_results_dir / 'task_table.csv'
    tasks = load_tasks_from_csv(task_table_path)
    
    if not tasks:
        print("⚠️ No completed tasks found. Checking for results files directly...")
        # Try to find results files directly
        results_files = list(ml_results_dir.rglob("results.json"))
        print(f"   Found {len(results_files)} results.json files")
        
        if not results_files:
            print("❌ No results found")
            sys.exit(1)
    
    # Generate CSV if not graphs-only
    if not args.graphs_only:
        print("\n" + "="*70)
        print("GENERATING CSV FILES")
        print("="*70)
        
        aggregated_results = aggregate_results(ml_results_dir, tasks)
        
        if aggregated_results:
            csv_file = save_model_comparison_csv(aggregated_results, ml_results_dir)
            
            # Print summary
            print("\n📊 Model Comparison Summary:")
            print("-"*70)
            for model_name, results in sorted(aggregated_results.items()):
                if 'error' not in results:
                    best = results['best_metrics']
                    print(f"{model_name:25} | Accuracy: {best['test_accuracy']:.4f} ± {best.get('std_test_accuracy', 0):.4f} | "
                          f"F1: {best.get('test_f1', 0):.4f} | Folds: {results.get('num_folds', 0)}")
        else:
            print("⚠️ No results aggregated")
    
    # Generate graphs if not csv-only
    if not args.csv_only:
        print("\n" + "="*70)
        print("GENERATING GRAPHS")
        print("="*70)
        
        try:
            # Try to load config if provided
            if args.config and Path(args.config).exists():
                config_handler = UnifiedConfigHandler(args.config)
            else:
                # Create minimal config for graph generation
                print("⚠️ No config provided, using default graph settings")
                class MinimalConfigHandler:
                    best_models_graph = True
                    per_model_across_hyperparameters_graph = True
                    per_model_per_hyperparameter_across_folds_graph = True
                    per_subject_analysis_graph = True
                
                config_handler = MinimalConfigHandler()
            
            # Create graph generator
            graph_generator = GraphGenerator(
                config_handler=config_handler,
                ml_results_path=str(ml_results_dir)
            )
            
            # Generate graphs
            graph_generator.generate_graphs()
            print("✅ Graphs generated successfully")
            
        except Exception as e:
            print(f"⚠️ Error generating graphs: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()


