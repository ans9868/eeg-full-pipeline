#!/usr/bin/env python3
"""
Comprehensive graph generator that can create all types of graphs.
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

# Add parent directory to path for imports
sys.path.append('..')

class ComprehensiveGraphGenerator:
    """Creates all types of graphs for EEG ML results."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.logger = logging.getLogger('comprehensive_graph')
        
        # Set up matplotlib style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Graph configuration
        self.figure_size = (12, 8)
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
        
        print(f"Initialized ComprehensiveGraphGenerator")
    
    def generate_all_graphs(self, ml_results_path: Path) -> None:
        """Generate all types of graphs."""
        try:
            print(f"📊 Loading data from: {ml_results_path}")
            
            # Generate per-subject analysis graphs
            print("🎨 Generating per-subject analysis graphs...")
            self._generate_per_subject_graphs(ml_results_path)
            
            # Generate hyperparameter box plots
            print("🎨 Generating hyperparameter box plots...")
            self._generate_hyperparameter_boxplots(ml_results_path)
            
            # Generate best models comparison
            print("🎨 Generating best models comparison...")
            self._generate_best_models_comparison(ml_results_path)
            
            print("✅ All graph generation completed successfully!")
            
        except Exception as e:
            print(f"💥 CRITICAL ERROR in graph generation: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _generate_per_subject_graphs(self, ml_results_path: Path) -> None:
        """Generate per-subject analysis graphs."""
        # Load per-subject data
        all_data = self._load_per_subject_data(ml_results_path)
        if all_data is None or all_data.empty:
            print("⚠️ No per-subject data found, skipping per-subject graphs")
            return
        
        print(f"📊 Loaded {len(all_data)} subjects for per-subject analysis")
        
        # Create overall per-subject graph
        overall_data = self._create_overall_per_subject_data(all_data)
        if overall_data is not None and not overall_data.empty:
            figure = self._create_per_subject_graph(overall_data, "Per-Subject Test Accuracy (Overall)")
            if figure is not None:
                self.save_graph(figure, "per_subject_analysis")
                print("✅ Overall per-subject analysis graph generated")
        
        # Create individual per-subject graphs
        self._create_individual_per_subject_graphs(all_data)
    
    def _generate_hyperparameter_boxplots(self, ml_results_path: Path) -> None:
        """Generate hyperparameter box plots."""
        # Load hyperparameter data
        all_data = self._load_hyperparameter_data(ml_results_path)
        if all_data is None or all_data.empty:
            print("⚠️ No hyperparameter data found, skipping hyperparameter box plots")
            return
        
        print(f"📊 Loaded {len(all_data)} hyperparameter combinations")
        
        # Create box plots for each model
        models = all_data['model_name'].unique()
        for model_name in models:
            model_data = all_data[all_data['model_name'] == model_name]
            if len(model_data) > 0:
                figure = self._create_single_model_boxplot(model_data, model_name)
                if figure is not None:
                    clean_model = model_name.replace(' ', '_').replace('(', '').replace(')', '').lower()
                    filename = f"hyperparameter_boxplot_{clean_model}"
                    self.save_graph(figure, filename)
                    print(f"✅ Hyperparameter box plot for {model_name} generated")
        
        # Create overall comparison box plot
        figure = self._create_overall_hyperparameter_boxplot(all_data)
        if figure is not None:
            self.save_graph(figure, "overall_hyperparameter_boxplot")
            print("✅ Overall hyperparameter box plot generated")
    
    def _generate_best_models_comparison(self, ml_results_path: Path) -> None:
        """Generate best models comparison graph."""
        # Load hyperparameter data
        all_data = self._load_hyperparameter_data(ml_results_path)
        if all_data is None or all_data.empty:
            print("⚠️ No hyperparameter data found, skipping best models comparison")
            return
        
        # Find best performance for each model
        best_models_data = []
        for model_name in all_data['model_name'].unique():
            model_data = all_data[all_data['model_name'] == model_name]
            best_idx = model_data['test_accuracy'].idxmax()
            best_row = model_data.loc[best_idx]
            best_models_data.append(best_row)
        
        if best_models_data:
            best_df = pd.DataFrame(best_models_data)
            figure = self._create_best_models_graph(best_df)
            if figure is not None:
                self.save_graph(figure, "best_models_comparison")
                print("✅ Best models comparison graph generated")
    
    def _load_per_subject_data(self, ml_results_path: Path) -> pd.DataFrame:
        """Load per-subject data by reading prediction parquet files."""
        model_dirs = [d for d in ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        
        if not model_dirs:
            return pd.DataFrame()
        
        all_subject_data = []
        
        for model_dir in model_dirs:
            model_name = model_dir.name
            hyperparam_dirs = [d for d in model_dir.iterdir() 
                             if d.is_dir() and "_" in d.name]
            
            for hyperparam_dir in hyperparam_dirs:
                test_parquet_file = hyperparam_dir / "test_predictions.parquet"
                results_json_file = hyperparam_dir / "results.json"
                
                if test_parquet_file.exists():
                    try:
                        df = pd.read_parquet(test_parquet_file)
                        
                        if 'SubjectID' in df.columns and 'label' in df.columns and 'prediction' in df.columns:
                            if 'Group' in df.columns:
                                per_subject = df.groupby('SubjectID').apply(
                                    lambda x: pd.Series({
                                        'accuracy': (x['label'] == x['prediction']).mean(),
                                        'group': x['Group'].iloc[0]
                                    }), include_groups=False
                                ).reset_index()
                                
                                per_subject['model_name'] = model_name
                                per_subject['hyperparam_dir'] = hyperparam_dir.name
                                all_subject_data.append(per_subject)
                    except Exception as e:
                        print(f"Error reading parquet file {test_parquet_file}: {e}")
        
        if not all_subject_data:
            return pd.DataFrame()
        
        return pd.concat(all_subject_data, ignore_index=True)
    
    def _load_hyperparameter_data(self, ml_results_path: Path) -> pd.DataFrame:
        """Load hyperparameter data by reading results.json files."""
        model_dirs = [d for d in ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        
        if not model_dirs:
            return pd.DataFrame()
        
        all_hyperparam_data = []
        
        for model_dir in model_dirs:
            model_name = model_dir.name
            hyperparam_dirs = [d for d in model_dir.iterdir() 
                             if d.is_dir() and "_" in d.name]
            
            for hyperparam_dir in hyperparam_dirs:
                results_json_file = hyperparam_dir / "results.json"
                
                if results_json_file.exists():
                    try:
                        with open(results_json_file, 'r') as f:
                            results = json.load(f)
                        
                        test_accuracy = results.get('test_accuracy', 0.0)
                        if test_accuracy == 0.0:
                            test_results = results.get('test_results', {})
                            test_accuracy = test_results.get('accuracy', 0.0)
                        
                        hyperparams = results.get('hyperparameters', {})
                        if not hyperparams:
                            hyperparams = results.get('detailed_results', {}).get('hyperparams', {})
                        if not hyperparams:
                            hyperparams = results.get('hyperparams', {})
                        
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
            return pd.DataFrame()
        
        return pd.DataFrame(all_hyperparam_data)
    
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
            param_strs = [f"{k}={v}" for k, v in hyperparams.items()]
            return f"{model_name}_{'_'.join(param_strs)}"
    
    def _create_overall_per_subject_data(self, all_data: pd.DataFrame) -> pd.DataFrame:
        """Create overall per-subject data by averaging across all models/hyperparameters."""
        if 'group' in all_data.columns:
            per_subject_avg = all_data.groupby('SubjectID').agg({
                'accuracy': 'mean',
                'group': 'first'
            }).reset_index()
        else:
            return pd.DataFrame()
        
        return per_subject_avg.sort_values('SubjectID', ascending=True)
    
    def _create_per_subject_graph(self, data: pd.DataFrame, title: str = "Per-Subject Test Accuracy") -> plt.Figure:
        """Create the per-subject analysis graph with bar chart."""
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        x_pos = np.arange(len(data))
        
        if 'group' in data.columns:
            unique_groups = data['group'].unique()
        else:
            return None
        
        if len(unique_groups) <= 10:
            color_palette = ['#2E8B57', '#DC143C', '#FF8C00', '#4169E1', '#8B0000', 
                           '#9370DB', '#20B2AA', '#FF6347', '#32CD32', '#FF1493']
        else:
            color_palette = cm.Set3(np.linspace(0, 1, len(unique_groups)))
        
        group_colors = {group: color_palette[i % len(color_palette)] 
                       for i, group in enumerate(unique_groups)}
        
        colors = [group_colors[group] for group in data['group']]
        bars = ax.bar(x_pos, data['accuracy'], color=colors, alpha=0.8)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(data['SubjectID'], rotation=45, ha='right', fontsize=12)
        ax.set_ylabel('Test Accuracy')
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        if len(unique_groups) > 1:
            legend_elements = []
            for group in unique_groups:
                color = group_colors[group]
                legend_elements.append(plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.8, label=group.title()))
            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))
        
        plt.tight_layout()
        return fig
    
    def _create_individual_per_subject_graphs(self, all_data: pd.DataFrame) -> None:
        """Create individual per-subject graphs for each model×hyperparameter combination."""
        per_subject_dir = self.output_dir / "per_subject_individual"
        per_subject_dir.mkdir(parents=True, exist_ok=True)
        
        grouped = all_data.groupby(['model_name', 'hyperparam_dir'])
        
        for (model_name, hyperparam_dir), group_data in grouped:
            clean_model = model_name.replace(' ', '_').lower()
            clean_hyperparam = hyperparam_dir.replace(' ', '_').replace('=', '_').lower()
            filename = f"per_subject_{clean_model}_{clean_hyperparam}"
            
            sorted_data = group_data.sort_values('SubjectID')
            readable_title = f"Per-Subject Test Accuracy: {model_name} - {hyperparam_dir}"
            
            figure = self._create_per_subject_graph(sorted_data, readable_title)
            if figure is not None:
                output_path = per_subject_dir / f"{filename}.{self.format}"
                figure.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                              facecolor='white', edgecolor='none')
                plt.close(figure)
    
    def _create_single_model_boxplot(self, model_data: pd.DataFrame, model_name: str) -> plt.Figure:
        """Create a box plot for a single model's hyperparameters."""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        hyperparams = model_data['hyperparam_name'].unique()
        box_data = []
        positions = []
        
        for i, hyperparam in enumerate(hyperparams):
            hyperparam_data = model_data[model_data['hyperparam_name'] == hyperparam]['test_accuracy']
            box_data.append(hyperparam_data)
            positions.append(i)
        
        color = self.model_colors.get(model_name, '#666666')
        bp = ax.boxplot(box_data, positions=positions, patch_artist=True, 
                       tick_labels=hyperparams, showfliers=True)
        
        for patch in bp['boxes']:
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add 50% accuracy reference line
        ax.axhline(y=0.5, color='lightcoral', linestyle='--', linewidth=2, alpha=0.8)
        
        # Add best and worst performance indicators
        for i, hyperparam in enumerate(hyperparams):
            hyperparam_data = model_data[model_data['hyperparam_name'] == hyperparam]
            if len(hyperparam_data) > 0:
                best_accuracy = hyperparam_data['test_accuracy'].max()
                worst_accuracy = hyperparam_data['test_accuracy'].min()
                
                ax.scatter(i, best_accuracy, color='lightgreen', s=80, marker='o', 
                          edgecolors='darkgreen', linewidth=2, zorder=5)
                ax.scatter(i, worst_accuracy, color='lightcoral', s=80, marker='o', 
                          edgecolors='darkred', linewidth=2, zorder=5)
        
        ax.set_xticklabels(hyperparams, rotation=45, ha='right', fontsize=10)
        ax.set_ylabel('Test Accuracy')
        ax.set_title(f'{model_name} - Hyperparameter Performance Distribution', 
                    fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def _create_overall_hyperparameter_boxplot(self, all_data: pd.DataFrame) -> plt.Figure:
        """Create an overall box plot comparing all models and their hyperparameters."""
        fig, ax = plt.subplots(figsize=(16, 10))
        
        models = all_data['model_name'].unique()
        box_data = []
        positions = []
        
        for i, model in enumerate(models):
            model_data = all_data[all_data['model_name'] == model]['test_accuracy']
            box_data.append(model_data)
            positions.append(i)
        
        bp = ax.boxplot(box_data, positions=positions, patch_artist=True, 
                       tick_labels=models, showfliers=True)
        
        for patch, model in zip(bp['boxes'], models):
            color = self.model_colors.get(model, '#666666')
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add 50% accuracy reference line
        ax.axhline(y=0.5, color='lightcoral', linestyle='--', linewidth=2, alpha=0.8)
        
        # Add best and worst performance indicators
        for i, model in enumerate(models):
            model_data = all_data[all_data['model_name'] == model]
            if len(model_data) > 0:
                best_accuracy = model_data['test_accuracy'].max()
                worst_accuracy = model_data['test_accuracy'].min()
                
                ax.scatter(i, best_accuracy, color='lightgreen', s=80, marker='o', 
                          edgecolors='darkgreen', linewidth=2, zorder=5)
                ax.scatter(i, worst_accuracy, color='lightcoral', s=80, marker='o', 
                          edgecolors='darkred', linewidth=2, zorder=5)
        
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
        
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig
    
    def _create_best_models_graph(self, best_models_data: pd.DataFrame) -> plt.Figure:
        """Create a bar chart comparing the best performance of each model."""
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        x_pos = np.arange(len(best_models_data))
        colors = [self.model_colors.get(model, '#666666') for model in best_models_data['model_name']]
        
        bars = ax.bar(x_pos, best_models_data['test_accuracy'], color=colors, alpha=0.8)
        
        # Add 50% accuracy reference line
        ax.axhline(y=0.5, color='lightcoral', linestyle='--', linewidth=2, alpha=0.8, label='50% Accuracy')
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(best_models_data['model_name'], rotation=45, ha='right', fontsize=12)
        ax.set_ylabel('Test Accuracy')
        ax.set_title('Best Model Performance Comparison', fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, best_models_data['test_accuracy'])):
            ax.text(bar.get_x() + bar.get_width()/2, value + 0.01, 
                   f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def save_graph(self, figure: plt.Figure, filename: str) -> None:
        """Save the graph to the output directory."""
        output_path = self.output_dir / f"{filename}.{self.format}"
        figure.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                      facecolor='white', edgecolor='none')
        print(f"💾 Graph saved: {output_path}")
        plt.close(figure)

def main():
    print("🚀 Starting generate_all_graphs.py")
    print(f"📋 Arguments: {sys.argv}")
    
    if len(sys.argv) < 2:
        print("Usage: python generate_all_graphs.py <ml_results_path>")
        print("Example: python generate_all_graphs.py /path/to/ml_results")
        sys.exit(1)
    
    print("✅ Arguments check passed")
    
    ml_results_path = sys.argv[1]
    
    try:
        # Create output directory
        output_dir = Path(ml_results_path) / "graphs"
        output_dir.mkdir(exist_ok=True)
        
        print(f"📊 Output directory: {output_dir}")
        
        # Generate all graphs
        print("🎨 Generating all types of graphs...")
        graph_generator = ComprehensiveGraphGenerator(output_dir=output_dir)
        graph_generator.generate_all_graphs(Path(ml_results_path))
        print("✅ All graph generation completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
