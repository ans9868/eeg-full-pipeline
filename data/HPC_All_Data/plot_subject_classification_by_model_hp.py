#!/usr/bin/env python
"""
Plot number of correctly classified subjects (>50% accuracy) for each model×HP combination.

For each experiment, shows:
- X-axis: Model×Hyperparameter combination
- Y-axis: Number of subjects correctly classified (>50% accuracy)
- Bar chart showing classification success rate
"""

import pandas as pd
import json
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict
import re

BASE_DIR = Path(__file__).parent

# Focus on 4 main experiments
EXPERIMENTS = {
    "ANOVA_L_2_Random": BASE_DIR / "grid_50_random_folds/ANOVA_L_2_complete",
    "ANOVA_L_6_Random": BASE_DIR / "grid_50_random_folds/Anova_L_6_Incomplete_ml_results",
    "PCA_L_2_Random": BASE_DIR / "grid_50_random_folds/PCA_L_2_ml_results",
    "PCA_L_6_Random": BASE_DIR / "grid_50_random_folds/PCA_L_6_ml_results",
}

def extract_hyperparams(results_file):
    """Extract hyperparameters from results.json file."""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        return data.get('hyperparams', {})
    except:
        return {}

def format_model_hp_label(model_name, hyperparams):
    """Format model×hyperparameter label."""
    if hyperparams:
        sorted_keys = sorted(hyperparams.keys())
        param_str = ", ".join([f"{k}={hyperparams[k]}" for k in sorted_keys])
        return f"{model_name} ({param_str})"
    else:
        return f"{model_name} (default)"

def extract_subject_ids_from_fold(fold_name):
    """Extract subject IDs from fold name."""
    return re.findall(r'sub-(\d+)', fold_name)

def load_subject_classification_from_parquet(exp_name, results_dir):
    """
    Load per-subject accuracy from parquet files and count correctly classified subjects.
    
    Returns: {model_hp_key: set of correctly classified subjects}
    """
    if not results_dir.exists():
        return {}
    
    results_path = results_dir / "ml_results_grid_search"
    if not results_path.exists():
        results_path = results_dir
    
    # Structure: {model_hp_key: set of correctly classified subjects}
    model_hp_correct_subjects = defaultdict(set)
    
    for model_dir in results_path.iterdir():
        if not model_dir.is_dir() or model_dir.name in ['graphs', 'debug'] or model_dir.name.startswith('_'):
            continue
        
        model_name = model_dir.name
        
        for fold_dir in model_dir.iterdir():
            if not fold_dir.is_dir() or not fold_dir.name.startswith('sub-'):
                continue
            
            fold_name = fold_dir.name
            
            # Find task directories
            task_dirs = [d for d in fold_dir.iterdir() if d.is_dir() and d.name.startswith('task_')]
            
            for task_dir in task_dirs:
                test_parquet = task_dir / "test_predictions.parquet"
                results_file = task_dir / "results.json"
                
                if not test_parquet.exists() or not results_file.exists():
                    continue
                
                try:
                    # Get hyperparameters
                    hyperparams = extract_hyperparams(results_file)
                    model_hp_key = format_model_hp_label(model_name, hyperparams)
                    
                    # Read test predictions
                    test_df = pd.read_parquet(test_parquet)
                    
                    # Calculate per-subject accuracy
                    for subject_id_num in test_df['SubjectID'].unique():
                        subject_id = f"sub-{int(subject_id_num)}"
                        
                        # Filter data for this subject
                        subject_data = test_df[test_df['SubjectID'] == subject_id_num]
                        
                        # Calculate accuracy
                        correct = (subject_data['label'] == subject_data['prediction']).sum()
                        total = len(subject_data)
                        accuracy = correct / total if total > 0 else 0.0
                        
                        # If accuracy > 50%, subject is correctly classified
                        if accuracy > 0.5:
                            model_hp_correct_subjects[model_hp_key].add(subject_id)
                            
                except Exception as e:
                    continue
    
    # Convert to counts
    model_hp_counts = {k: len(v) for k, v in model_hp_correct_subjects.items()}
    return model_hp_counts

def plot_subject_classification_by_model_hp(exp_name, model_hp_counts, output_dir):
    """Create bar chart showing number of correctly classified subjects per model×HP."""
    if not model_hp_counts:
        return False
    
    # Sort by count (descending)
    sorted_items = sorted(model_hp_counts.items(), key=lambda x: x[1], reverse=True)
    model_hps = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Create bar chart
    bars = ax.bar(range(len(model_hps)), counts, color='steelblue', alpha=0.7, edgecolor='black')
    
    # Add value labels on bars
    for i, (bar, count) in enumerate(zip(bars, counts)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Truncate long model×HP names for x-axis
    truncated_labels = [label[:50] + "..." if len(label) > 50 else label for label in model_hps]
    
    ax.set_xlabel('Model×Hyperparameter Combination', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Subjects Correctly Classified (>50% Accuracy)', 
                  fontsize=13, fontweight='bold')
    ax.set_title(f'{exp_name}\nSubjects Correctly Classified (>50% Accuracy) by Model×Hyperparameter',
                 fontsize=15, fontweight='bold', pad=20)
    
    ax.set_xticks(range(len(model_hps)))
    ax.set_xticklabels(truncated_labels, rotation=45, ha='right', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Set y-axis to show total subjects (65)
    ax.set_ylim(0, 65)
    
    # Add note about what "correctly classified" means
    ax.text(0.02, 0.98, 
            'Note: A subject is correctly classified if accuracy > 50%\nin at least one fold×model combination',
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    output_file = output_dir / f'{exp_name}_subject_classification_by_model_hp.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"   ✅ Saved: {output_file.name}")
    return True

def main():
    """Main function."""
    output_dir = BASE_DIR / "per_subject_classification_analysis"
    output_dir.mkdir(exist_ok=True)
    
    for exp_name, results_dir in EXPERIMENTS.items():
        print(f"\n📊 Processing {exp_name}...")
        
        # Load subject classification from parquet files
        model_hp_counts = load_subject_classification_from_parquet(exp_name, results_dir)
        
        if not model_hp_counts:
            print(f"   ⚠️  No data found")
            continue
        
        print(f"   Found {len(model_hp_counts)} model×HP combinations")
        print(f"   Max subjects correctly classified: {max(model_hp_counts.values())}")
        
        # Create plot
        plot_subject_classification_by_model_hp(exp_name, model_hp_counts, output_dir)
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
