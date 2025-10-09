#!/usr/bin/env python3
"""
Hyperparameter box plot generator for EEG ML results.
Creates box plots showing performance distribution across hyperparameter combinations.
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np

class HyperparameterBoxPlotGenerator:
    """Creates box plots for hyperparameter performance across different configurations."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.logger = logging.getLogger('hyperparameter_boxplot')
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Graph configuration
        self.figure_size = (14, 8)
        self.dpi = 300
        self.format = "png"
        
        # Model colors
        self.model_colors = {
            "KNN": "#1f77b4",
            "MLP_(Neural_Network)": "#ff7f0e", 
            "SVM": "#2ca02c",
            "Random_Forest": "#d62728",
            "Logistic_Regression": "#9467bd"
        }
        
        print(f"Initialized HyperparameterBoxPlotGenerator")
    
    def generate_and_save(self, ml_results_path: Path) -> None:
        """Generate and save hyperparameter box plot graphs."""
        try:
            print(f"📊 Loading hyperparameter data from: {ml_results_path}")
            
            # Load and process hyperparameter data
            all_data = self._load_hyperparameter_data(ml_results_path)
            if all_data is None or all_data.empty:
                raise ValueError("No hyperparameter data found or data is empty")
            
            print(f"📊 Loaded {len(all_data)} hyperparameter combinations")
            
            # Create box plots for each model
            self._create_model_hyperparameter_boxplots(all_data)
            
            # Create overall comparison box plot
            self._create_overall_hyperparameter_boxplot(all_data)
            
            print("✅ All hyperparameter box plot graphs generated and saved successfully")
            
        except Exception as e:
            print(f"💥 CRITICAL ERROR generating hyperparameter box plots: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _load_hyperparameter_data(self, ml_results_path: Path) -> pd.DataFrame:
        """Load hyperparameter data by reading results.json files."""
        model_dirs = [d for d in ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        
        if not model_dirs:
            raise ValueError("No model directories found")
        
        all_hyperparam_data = []
        
        for model_dir in model_dirs:
            model_name = model_dir.name
            print(f"📊 Processing model: {model_name}")
            
            # Get all hyperparameter directories for this model
            hyperparam_dirs = [d for d in model_dir.iterdir() 
                             if d.is_dir() and "_" in d.name]
            
            if not hyperparam_dirs:
                print(f"No hyperparameter directories found for model {model_name}")
                continue
            
            # Collect data from all hyperparameter directories
            for hyperparam_dir in hyperparam_dirs:
                results_json_file = hyperparam_dir / "results.json"
                
                if results_json_file.exists():
                    try:
                        # Read the results file
                        with open(results_json_file, 'r') as f:
                            results = json.load(f)
                        
                        # Extract test accuracy and hyperparameters
                        test_accuracy = results.get('test_accuracy', 0.0)
                        if test_accuracy == 0.0:
                            # Try alternative structure
                            test_results = results.get('test_results', {})
                            test_accuracy = test_results.get('accuracy', 0.0)
                        
                        # Extract hyperparameters
                        hyperparams = results.get('hyperparameters', {})
                        if not hyperparams:
                            hyperparams = results.get('detailed_results', {}).get('hyperparams', {})
                        if not hyperparams:
                            hyperparams = results.get('hyperparams', {})
                        
                        # Create hyperparameter combination name
                        hyperparam_name = self._create_hyperparameter_name(model_name, hyperparams)
                        
                        all_hyperparam_data.append({
                            'model_name': model_name,
                            'hyperparam_dir': hyperparam_dir.name,
                            'hyperparam_name': hyperparam_name,
                            'test_accuracy': test_accuracy,
                            **{f'hyperparam_{k}': v for k, v in hyperparams.items()}
                        })
                        
                    except Exception as e:
                        print(f"Error reading results from {results_json_file}: {e}")
        
        if not all_hyperparam_data:
            raise ValueError("No hyperparameter data found in any results files")
        
        # Combine all data
        combined_data = pd.DataFrame(all_hyperparam_data)
        return combined_data
    
    def _create_hyperparameter_name(self, model_name: str, hyperparams: Dict[str, Any]) -> str:
        """Create a readable name for hyperparameter combination."""
        if model_name == "KNN":
            n_neighbors = hyperparams.get('n_neighbors', '?')
            weights = hyperparams.get('weights', '?')
            metric = hyperparams.get('metric', '?')
            return f"KNN_{metric}_n={n_neighbors}_w={weights}"
        elif model_name == "MLP_(Neural_Network)":
            hidden_layers = hyperparams.get('hidden_layer_sizes', '?')
            activation = hyperparams.get('activation', '?')
            return f"MLP_{activation}_layers={hidden_layers}"
        elif model_name == "SVM":
            kernel = hyperparams.get('kernel', '?')
            C = hyperparams.get('C', '?')
            return f"SVM_{kernel}_C={C}"
        elif model_name == "Random_Forest":
            n_estimators = hyperparams.get('n_estimators', '?')
            max_depth = hyperparams.get('max_depth', '?')
            return f"RF_est={n_estimators}_depth={max_depth}"
        else:
            # Generic fallback
            param_strs = [f"{k}={v}" for k, v in hyperparams.items()]
            return f"{model_name}_{'_'.join(param_strs)}"
    
    def _create_model_hyperparameter_boxplots(self, all_data: pd.DataFrame) -> None:
        """Create individual box plots for each model's hyperparameters."""
        models = all_data['model_name'].unique()
        
        for model_name in models:
            model_data = all_data[all_data['model_name'] == model_name]
            
            if len(model_data) == 0:
                continue
            
            # Create box plot for this model
            figure = self._create_single_model_boxplot(model_data, model_name)
            
            if figure is not None:
                # Save the graph
                clean_model = model_name.replace(' ', '_').replace('(', '').replace(')', '').lower()
                filename = f"hyperparameter_boxplot_{clean_model}"
                self.save_graph(figure, filename)
                print(f"✅ Hyperparameter box plot for {model_name} created successfully")
    
    def _create_single_model_boxplot(self, model_data: pd.DataFrame, model_name: str) -> plt.Figure:
        """Create a box plot for a single model's hyperparameters."""
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Get unique hyperparameter combinations
        hyperparams = model_data['hyperparam_name'].unique()
        
        # Create box plot data
        box_data = []
        positions = []
        hyperparam_names = []
        
        for i, hyperparam in enumerate(hyperparams):
            hyperparam_data = model_data[model_data['hyperparam_name'] == hyperparam]['test_accuracy']
            box_data.append(hyperparam_data)
            positions.append(i)
            hyperparam_names.append(hyperparam)
        
        # Create box plot
        color = self.model_colors.get(model_name, '#666666')
        bp = ax.boxplot(box_data, positions=positions, patch_artist=True, 
                       tick_labels=hyperparam_names, showfliers=True)
        
        # Color the boxes
        for patch in bp['boxes']:
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add 50% accuracy reference line
        ax.axhline(y=0.5, color='lightcoral', linestyle='--', linewidth=2, alpha=0.8, label='50% Accuracy')
        
        # Add best and worst performance indicators
        for i, hyperparam in enumerate(hyperparams):
            hyperparam_data = model_data[model_data['hyperparam_name'] == hyperparam]
            if len(hyperparam_data) > 0:
                # Best performance (light green)
                best_accuracy = hyperparam_data['test_accuracy'].max()
                ax.scatter(i, best_accuracy, 
                          color='lightgreen', s=80, marker='o', 
                          edgecolors='darkgreen', linewidth=2, zorder=5, label='Best' if i == 0 else "")
                
                # Worst performance (light red)
                worst_accuracy = hyperparam_data['test_accuracy'].min()
                ax.scatter(i, worst_accuracy, 
                          color='lightcoral', s=80, marker='o', 
                          edgecolors='darkred', linewidth=2, zorder=5, label='Worst' if i == 0 else "")
        
        # Customize the plot
        ax.set_xticklabels(hyperparam_names, rotation=45, ha='right', fontsize=10)
        ax.set_ylabel('Test Accuracy')
        ax.set_title(f'{model_name} - Hyperparameter Performance Distribution', 
                    fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            plt.Line2D([0], [0], color='lightcoral', linestyle='--', linewidth=2, label='50% Accuracy'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', 
                      markeredgecolor='darkgreen', markersize=8, linewidth=2, label='Best Performance'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightcoral', 
                      markeredgecolor='darkred', markersize=8, linewidth=2, label='Worst Performance')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig
    
    def _create_overall_hyperparameter_boxplot(self, all_data: pd.DataFrame) -> None:
        """Create an overall box plot comparing all models and their hyperparameters."""
        # Create figure
        fig, ax = plt.subplots(figsize=(16, 10))
        
        # Get unique models
        models = all_data['model_name'].unique()
        
        # Create box plot data for each model
        box_data = []
        positions = []
        model_names = []
        
        for i, model in enumerate(models):
            model_data = all_data[all_data['model_name'] == model]['test_accuracy']
            box_data.append(model_data)
            positions.append(i)
            model_names.append(model)
        
        # Create box plot
        bp = ax.boxplot(box_data, positions=positions, patch_artist=True, 
                       tick_labels=model_names, showfliers=True)
        
        # Color the boxes
        for patch, model in zip(bp['boxes'], models):
            color = self.model_colors.get(model, '#666666')
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add 50% accuracy reference line
        ax.axhline(y=0.5, color='lightcoral', linestyle='--', linewidth=2, alpha=0.8, label='50% Accuracy')
        
        # Add best and worst performance indicators for each model
        for i, model in enumerate(models):
            model_data = all_data[all_data['model_name'] == model]
            if len(model_data) > 0:
                # Best performance (light green)
                best_accuracy = model_data['test_accuracy'].max()
                ax.scatter(i, best_accuracy, 
                          color='lightgreen', s=80, marker='o', 
                          edgecolors='darkgreen', linewidth=2, zorder=5, label='Best' if i == 0 else "")
                
                # Worst performance (light red)
                worst_accuracy = model_data['test_accuracy'].min()
                ax.scatter(i, worst_accuracy, 
                          color='lightcoral', s=80, marker='o', 
                          edgecolors='darkred', linewidth=2, zorder=5, label='Worst' if i == 0 else "")
        
        # Customize the plot
        ax.set_ylabel('Test Accuracy')
        ax.set_title('Model Performance Distribution Across All Hyperparameters', 
                    fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = []
        for model in models:
            color = self.model_colors.get(model, '#666666')
            legend_elements.append(Patch(facecolor=color, alpha=0.7, label=model))
        
        # Add performance indicators to legend
        legend_elements.extend([
            plt.Line2D([0], [0], color='lightcoral', linestyle='--', linewidth=2, label='50% Accuracy'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', 
                      markeredgecolor='darkgreen', markersize=8, linewidth=2, label='Best Performance'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightcoral', 
                      markeredgecolor='darkred', markersize=8, linewidth=2, label='Worst Performance')
        ])
        
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        
        # Save the graph
        self.save_graph(fig, "overall_hyperparameter_boxplot")
        print("✅ Overall hyperparameter box plot created successfully")
    
    def save_graph(self, figure: plt.Figure, filename: str) -> None:
        """Save the graph to the output directory."""
        output_path = self.output_dir / f"{filename}.{self.format}"
        figure.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                      facecolor='white', edgecolor='none')
        print(f"💾 Graph saved: {output_path}")
        plt.close(figure)

def main():
    print("🚀 Starting hyperparameter_boxplot_generator.py")
    print(f"📋 Arguments: {sys.argv}")
    
    if len(sys.argv) < 2:
        print("Usage: python hyperparameter_boxplot_generator.py <ml_results_path>")
        print("Example: python hyperparameter_boxplot_generator.py /path/to/ml_results")
        sys.exit(1)
    
    print("✅ Arguments check passed")
    
    ml_results_path = sys.argv[1]
    
    try:
        # Create output directory
        output_dir = Path(ml_results_path) / "graphs"
        output_dir.mkdir(exist_ok=True)
        
        print(f"📊 Output directory: {output_dir}")
        
        # Generate hyperparameter box plots
        print("🎨 Generating hyperparameter box plots...")
        boxplot_generator = HyperparameterBoxPlotGenerator(output_dir=output_dir)
        boxplot_generator.generate_and_save(Path(ml_results_path))
        print("✅ Hyperparameter box plot generation completed!")
        
        print("✅ Graph generation completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
