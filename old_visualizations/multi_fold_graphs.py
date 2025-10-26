"""
Multi-Fold Graph Implementations for EEG Ray Tuner

This module contains classes for generating specific graph types
for multi-fold data leakage prevention strategies (e.g., LPSO cross-validation).
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np
import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from config_handler import UnifiedConfigHandler
from .single_split_graphs import BaseGraph

logger = logging.getLogger(__name__)


class BestModelsGraphMultiFold(BaseGraph):
    """
    Creates best model comparison graph for multi-fold scenarios.
    Uses box plots with best/worst fold indicators.
    """
    
    def __init__(self, config_handler: UnifiedConfigHandler, output_dir: Path):
        super().__init__(config_handler, output_dir)
        self.primary_metric = "test_accuracy"  # Will be adjusted based on data
        self.graph_name = "best_models_comparison_multifold"
        logger.info(f"Initialized BestModelsGraphMultiFold for metric: {self.primary_metric}")

    def generate_and_save(self, ml_results_path: Path) -> None:
        """
        Generate and save the best models multi-fold graph.
        """
        try:
            self.logger.info(f"📊 Loading multi-fold model comparison data from: {ml_results_path}")
            
            # Load and process multi-fold data
            data = self._load_multifold_model_data(ml_results_path)
            if data is None or data.empty:
                raise ValueError("No multi-fold model comparison data found or data is empty")
            
            self.logger.info(f"📊 Loaded {len(data)} models for multi-fold best models graph")
            
            # Create graph
            figure = self._create_best_models_multifold_graph(data)
            if figure is None:
                raise ValueError("Failed to create best models multi-fold graph figure")
            
            # Save graph
            self.save_graph(figure, self.graph_name)
            
            self.logger.info("✅ Best models multi-fold graph generated and saved successfully")
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR generating best models multi-fold graph: {e}")
            import traceback
            self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
            raise  # Hard fail

    def _load_multifold_model_data(self, ml_results_path: Path) -> pd.DataFrame:
        """
        Load multi-fold model comparison data by aggregating across folds.
        For LPSO scenarios, data might be stored in hyperparameter directories.
        """
        model_dirs = [d for d in ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        
        if not model_dirs:
            raise ValueError("No model directories found")
        
        all_data = []
        
        for model_dir in model_dirs:
            model_name = model_dir.name
            self.logger.info(f"📊 Processing model: {model_name}")
            
            # First, try to find fold directories (traditional LPSO structure)
            fold_dirs = [d for d in model_dir.iterdir() 
                        if d.is_dir() and "sub-" in d.name and "_sub-" in d.name]
            
            if fold_dirs:
                # Traditional LPSO structure with fold directories
                self.logger.info(f"Found {len(fold_dirs)} fold directories for {model_name}")
                fold_data = self._load_from_fold_directories(fold_dirs, model_name)
            else:
                # LPSO data stored in hyperparameter directories
                self.logger.info(f"No fold directories found, checking hyperparameter directories for {model_name}")
                hyperparam_dirs = [d for d in model_dir.iterdir() 
                                 if d.is_dir() and "_" in d.name]
                if hyperparam_dirs:
                    fold_data = self._load_from_hyperparam_directories(hyperparam_dirs, model_name)
                else:
                    self.logger.warning(f"No suitable directories found for model {model_name}")
                    continue
            
            if fold_data:
                all_data.extend(fold_data)
        
        if not all_data:
            raise ValueError("No fold data found for any model")
        
        return pd.DataFrame(all_data)
    
    def _load_from_fold_directories(self, fold_dirs: List[Path], model_name: str) -> List[Dict]:
        """Load data from traditional fold directories."""
        fold_data = []
        for fold_dir in fold_dirs:
            fold_name = fold_dir.name
            results_file = fold_dir / "results.json"
            
            if results_file.exists():
                try:
                    import json
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    
                    # Extract test accuracy
                    test_accuracy = results.get('test_accuracy', 0.0)
                    fold_data.append({
                        'model_name': model_name,
                        'fold_name': fold_name,
                        'test_accuracy': test_accuracy
                    })
                except Exception as e:
                    self.logger.warning(f"Error reading results from {results_file}: {e}")
        return fold_data
    
    def _load_from_hyperparam_directories(self, hyperparam_dirs: List[Path], model_name: str) -> List[Dict]:
        """Load data from hyperparameter directories (LPSO data stored differently)."""
        fold_data = []
        for hyperparam_dir in hyperparam_dirs:
            results_file = hyperparam_dir / "results.json"
            
            if results_file.exists():
                try:
                    import json
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    
                    # Extract test accuracy and fold information
                    # Check for different possible structures
                    test_accuracy = results.get('test_accuracy', 0.0)
                    if test_accuracy == 0.0:
                        # Try alternative structure
                        test_results = results.get('test_results', {})
                        test_accuracy = test_results.get('accuracy', 0.0)
                    
                    # Try to extract fold information from results
                    fold_name = results.get('fold_name', None)
                    if not fold_name:
                        # Try to get fold info from fold_id
                        fold_id = results.get('fold_id', None)
                        if fold_id is not None:
                            fold_name = f"fold_{fold_id}"
                        else:
                            # Use a generic fold name based on the hyperparameter directory
                            fold_name = f"hyperparam_{hyperparam_dir.name}"
                    
                    fold_data.append({
                        'model_name': model_name,
                        'fold_name': fold_name,
                        'test_accuracy': test_accuracy
                    })
                except Exception as e:
                    self.logger.warning(f"Error reading results from {results_file}: {e}")
        return fold_data

    def _create_best_models_multifold_graph(self, data: pd.DataFrame) -> plt.Figure:
        """Create the best models multi-fold graph with box plots."""
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Get unique models
        models = data['model_name'].unique()
        
        # Create box plot data
        box_data = []
        positions = []
        model_names = []
        
        for i, model in enumerate(models):
            model_data = data[data['model_name'] == model]['test_accuracy']
            box_data.append(model_data)
            positions.append(i)
            model_names.append(model)
        
        # Create box plot
        bp = ax.boxplot(box_data, positions=positions, patch_artist=True, 
                       labels=model_names, showfliers=False)
        
        # Color the boxes
        for patch, model in zip(bp['boxes'], models):
            color = self.model_colors.get(model, '#666666')
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add best and worst fold indicators
        for i, model in enumerate(models):
            model_data = data[data['model_name'] == model]
            if len(model_data) > 0:
                # Best fold (light green)
                best_fold = model_data.loc[model_data['test_accuracy'].idxmax()]
                ax.scatter(i, best_fold['test_accuracy'], 
                          color='lightgreen', s=50, marker='o', 
                          edgecolors='darkgreen', linewidth=1, zorder=5)
                
                # Worst fold (light red)
                worst_fold = model_data.loc[model_data['test_accuracy'].idxmin()]
                ax.scatter(i, worst_fold['test_accuracy'], 
                          color='lightcoral', s=50, marker='o', 
                          edgecolors='darkred', linewidth=1, zorder=5)
        
        # Customize the plot
        ax.set_ylabel('Test Accuracy')
        ax.set_title('Best Model Performance Comparison (Multi-Fold)', fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='lightgreen', edgecolor='darkgreen', label='Best Fold'),
            Patch(facecolor='lightcoral', edgecolor='darkred', label='Worst Fold')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig


class HyperparameterGraphMultiFold(BaseGraph):
    """
    Creates hyperparameter comparison graph for multi-fold scenarios.
    Uses box plots with best/worst fold indicators.
    """
    
    def __init__(self, config_handler: UnifiedConfigHandler, model_name: str, output_dir: Path):
        super().__init__(config_handler, output_dir)
        self.model_name = model_name
        self.primary_metric = "test_accuracy"
        self.graph_name = f"{model_name.lower()}_hyperparameter_comparison_multifold"
        logger.info(f"Initialized HyperparameterGraphMultiFold for model: {self.model_name}")

    def generate_and_save(self, ml_results_path: Path) -> None:
        """
        Generate and save the hyperparameter multi-fold graph for this model.
        """
        try:
            self.logger.info(f"📊 Loading multi-fold hyperparameter data for {self.model_name} from: {ml_results_path}")
            
            # Load and process multi-fold data
            data = self._load_multifold_hyperparameter_data(ml_results_path)
            if data is None or data.empty:
                raise ValueError(f"No multi-fold hyperparameter data found for {self.model_name}")
            
            self.logger.info(f"📊 Loaded {len(data)} hyperparameter combinations for {self.model_name}")
            
            # Create graph
            figure = self._create_hyperparameter_multifold_graph(data)
            if figure is None:
                raise ValueError(f"Failed to create hyperparameter multi-fold graph figure for {self.model_name}")
            
            # Save graph
            self.save_graph(figure, self.graph_name)
            
            self.logger.info(f"✅ Hyperparameter multi-fold graph for {self.model_name} generated and saved successfully")
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR generating hyperparameter multi-fold graph for {self.model_name}: {e}")
            import traceback
            self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
            raise  # Hard fail

    def _load_multifold_hyperparameter_data(self, ml_results_path: Path) -> pd.DataFrame:
        """
        Load multi-fold hyperparameter data for this model.
        For LPSO scenarios, data might be stored in hyperparameter directories.
        """
        model_dir = ml_results_path / self.model_name
        
        if not model_dir.exists():
            raise ValueError(f"Model directory not found: {model_dir}")
        
        # First, try to find fold directories (traditional LPSO structure)
        fold_dirs = [d for d in model_dir.iterdir() 
                    if d.is_dir() and "sub-" in d.name and "_sub-" in d.name]
        
        if fold_dirs:
            # Traditional LPSO structure with fold directories
            self.logger.info(f"Found {len(fold_dirs)} fold directories for {self.model_name}")
            all_data = self._load_from_fold_directories_hyperparam(fold_dirs)
        else:
            # LPSO data stored in hyperparameter directories
            self.logger.info(f"No fold directories found, checking hyperparameter directories for {self.model_name}")
            hyperparam_dirs = [d for d in model_dir.iterdir() 
                             if d.is_dir() and "_" in d.name]
            if hyperparam_dirs:
                all_data = self._load_from_hyperparam_directories_hyperparam(hyperparam_dirs)
            else:
                raise ValueError(f"No suitable directories found for model {self.model_name}")
        
        if not all_data:
            raise ValueError(f"No fold data found for model {self.model_name}")
        
        return pd.DataFrame(all_data)
    
    def _load_from_fold_directories_hyperparam(self, fold_dirs: List[Path]) -> List[Dict]:
        """Load data from traditional fold directories for hyperparameter graphs."""
        all_data = []
        for fold_dir in fold_dirs:
            fold_name = fold_dir.name
            results_file = fold_dir / "results.json"
            
            if results_file.exists():
                try:
                    import json
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    
                    # Extract hyperparameters and test accuracy
                    hyperparams = results.get('hyperparameters', {})
                    test_accuracy = results.get('test_accuracy', 0.0)
                    
                    # Create hyperparameter combination name
                    hyperparam_name = self._create_hyperparameter_name(hyperparams)
                    
                    all_data.append({
                        'hyperparameter_name': hyperparam_name,
                        'fold_name': fold_name,
                        'test_accuracy': test_accuracy,
                        **{f'hyperparam_{k}': v for k, v in hyperparams.items()}
                    })
                    
                except Exception as e:
                    self.logger.warning(f"Error reading results from {results_file}: {e}")
        return all_data
    
    def _load_from_hyperparam_directories_hyperparam(self, hyperparam_dirs: List[Path]) -> List[Dict]:
        """Load data from hyperparameter directories for hyperparameter graphs."""
        all_data = []
        for hyperparam_dir in hyperparam_dirs:
            results_file = hyperparam_dir / "results.json"
            
            if results_file.exists():
                try:
                    import json
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    
                    # Extract hyperparameters and test accuracy
                    hyperparams = results.get('hyperparams', {})  # Note: 'hyperparams' not 'hyperparameters'
                    test_accuracy = results.get('test_accuracy', 0.0)
                    if test_accuracy == 0.0:
                        # Try alternative structure
                        test_results = results.get('test_results', {})
                        test_accuracy = test_results.get('accuracy', 0.0)
                    
                    # Create hyperparameter combination name
                    hyperparam_name = self._create_hyperparameter_name(hyperparams)
                    
                    # Try to extract fold information from results
                    fold_name = results.get('fold_name', None)
                    if not fold_name:
                        # Try to get fold info from fold_id
                        fold_id = results.get('fold_id', None)
                        if fold_id is not None:
                            fold_name = f"fold_{fold_id}"
                        else:
                            # Use a generic fold name based on the hyperparameter directory
                            fold_name = f"hyperparam_{hyperparam_dir.name}"
                    
                    all_data.append({
                        'hyperparameter_name': hyperparam_name,
                        'fold_name': fold_name,
                        'test_accuracy': test_accuracy,
                        **{f'hyperparam_{k}': v for k, v in hyperparams.items()}
                    })
                    
                except Exception as e:
                    self.logger.warning(f"Error reading results from {results_file}: {e}")
        return all_data

    def _create_hyperparameter_multifold_graph(self, data: pd.DataFrame) -> plt.Figure:
        """Create the hyperparameter multi-fold graph with box plots."""
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Get unique hyperparameter combinations
        hyperparams = data['hyperparameter_name'].unique()
        
        # Create box plot data
        box_data = []
        positions = []
        hyperparam_names = []
        
        for i, hyperparam in enumerate(hyperparams):
            hyperparam_data = data[data['hyperparameter_name'] == hyperparam]['test_accuracy']
            box_data.append(hyperparam_data)
            positions.append(i)
            hyperparam_names.append(hyperparam)
        
        # Create box plot
        color = self.model_colors.get(self.model_name, '#666666')
        bp = ax.boxplot(box_data, positions=positions, patch_artist=True, 
                       labels=hyperparam_names, showfliers=False)
        
        # Color the boxes
        for patch in bp['boxes']:
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add best and worst fold indicators
        for i, hyperparam in enumerate(hyperparams):
            hyperparam_data = data[data['hyperparameter_name'] == hyperparam]
            if len(hyperparam_data) > 0:
                # Best fold (light green)
                best_fold = hyperparam_data.loc[hyperparam_data['test_accuracy'].idxmax()]
                ax.scatter(i, best_fold['test_accuracy'], 
                          color='lightgreen', s=50, marker='o', 
                          edgecolors='darkgreen', linewidth=1, zorder=5)
                
                # Worst fold (light red)
                worst_fold = hyperparam_data.loc[hyperparam_data['test_accuracy'].idxmin()]
                ax.scatter(i, worst_fold['test_accuracy'], 
                          color='lightcoral', s=50, marker='o', 
                          edgecolors='darkred', linewidth=1, zorder=5)
        
        # Customize the plot
        ax.set_xticklabels(hyperparam_names, rotation=45, ha='right', fontsize=10)
        ax.set_ylabel('Test Accuracy')
        ax.set_title(f'{self.model_name} - Hyperparameter Performance Comparison (Multi-Fold)', 
                    fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='lightgreen', edgecolor='darkgreen', label='Best Fold'),
            Patch(facecolor='lightcoral', edgecolor='darkred', label='Worst Fold')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig

    def _create_hyperparameter_name(self, hyperparams: Dict[str, Any]) -> str:
        """Create a readable name for hyperparameter combination."""
        if self.model_name == "KNN":
            n_neighbors = hyperparams.get('n_neighbors', '?')
            weights = hyperparams.get('weights', '?')
            metric = hyperparams.get('metric', '?')
            return f"KNN_{metric}_n={n_neighbors}_w={weights}"
        elif self.model_name == "MLP":
            hidden_layers = hyperparams.get('hidden_layer_sizes', '?')
            activation = hyperparams.get('activation', '?')
            return f"MLP_{activation}_layers={hidden_layers}"
        elif self.model_name == "SVM":
            kernel = hyperparams.get('kernel', '?')
            C = hyperparams.get('C', '?')
            return f"SVM_{kernel}_C={C}"
        else:
            # Generic fallback
            param_strs = [f"{k}={v}" for k, v in hyperparams.items()]
            return f"{self.model_name}_{'_'.join(param_strs)}"


class PerModelPerHyperparamAcrossFoldsGraph(BaseGraph):
    """
    Creates a bar graph for a specific hyperparameter combination across all folds.
    Shows each fold on the x-axis with the target metric on the y-axis.
    """
    
    def __init__(self, config_handler: UnifiedConfigHandler, model_name: str, 
                 hyperparam_combination: str, output_dir: Path):
        super().__init__(config_handler, output_dir)
        self.model_name = model_name
        self.hyperparam_combination = hyperparam_combination
        self.primary_metric = "test_accuracy"
        self.graph_name = f"{model_name.lower()}_{hyperparam_combination.lower().replace(' ', '_')}_across_folds"
        logger.info(f"Initialized PerModelPerHyperparamAcrossFoldsGraph for {self.model_name} - {self.hyperparam_combination}")

    def generate_and_save(self, ml_results_path: Path) -> None:
        """
        Generate and save the per-hyperparameter across folds graph.
        """
        try:
            self.logger.info(f"📊 Loading fold data for {self.model_name} - {self.hyperparam_combination} from: {ml_results_path}")
            
            # Load and process fold data
            data = self._load_fold_data(ml_results_path)
            if data is None or data.empty:
                raise ValueError(f"No fold data found for {self.model_name} - {self.hyperparam_combination}")
            
            self.logger.info(f"📊 Loaded {len(data)} folds for {self.model_name} - {self.hyperparam_combination}")
            
            # Create graph
            figure = self._create_fold_graph(data)
            if figure is None:
                raise ValueError(f"Failed to create fold graph figure for {self.model_name} - {self.hyperparam_combination}")
            
            # Save graph
            self.save_graph(figure, self.graph_name)
            
            self.logger.info(f"✅ Fold graph for {self.model_name} - {self.hyperparam_combination} generated and saved successfully")
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR generating fold graph for {self.model_name} - {self.hyperparam_combination}: {e}")
            import traceback
            self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
            raise  # Hard fail

    def _load_fold_data(self, ml_results_path: Path) -> pd.DataFrame:
        """
        Load fold data for the specific hyperparameter combination.
        """
        model_dir = ml_results_path / self.model_name
        
        if not model_dir.exists():
            raise ValueError(f"Model directory not found: {model_dir}")
        
        # Get all fold directories for this model
        fold_dirs = [d for d in model_dir.iterdir() 
                    if d.is_dir() and "sub-" in d.name and "_sub-" in d.name]
        
        if not fold_dirs:
            raise ValueError(f"No fold directories found for model {self.model_name}")
        
        fold_data = []
        
        for fold_dir in fold_dirs:
            fold_name = fold_dir.name
            results_file = fold_dir / "results.json"
            
            if results_file.exists():
                try:
                    import json
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    
                    # Check if this fold matches our hyperparameter combination
                    hyperparams = results.get('hyperparameters', {})
                    current_hyperparam_name = self._create_hyperparameter_name(hyperparams)
                    
                    if current_hyperparam_name == self.hyperparam_combination:
                        test_accuracy = results.get('test_accuracy', 0.0)
                        fold_data.append({
                            'fold_name': fold_name,
                            'test_accuracy': test_accuracy
                        })
                    
                except Exception as e:
                    self.logger.warning(f"Error reading results from {results_file}: {e}")
        
        if not fold_data:
            raise ValueError(f"No fold data found for hyperparameter combination: {self.hyperparam_combination}")
        
        return pd.DataFrame(fold_data)

    def _create_fold_graph(self, data: pd.DataFrame) -> plt.Figure:
        """Create the fold comparison graph with bar chart."""
        # Sort by fold name for consistent ordering
        data_sorted = data.sort_values('fold_name')
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Create bar chart
        x_pos = np.arange(len(data_sorted))
        color = self.model_colors.get(self.model_name, '#666666')
        bars = ax.bar(x_pos, data_sorted['test_accuracy'], color=color, alpha=0.8)
        
        # Customize the plot
        ax.set_xticks(x_pos)
        ax.set_xticklabels(data_sorted['fold_name'], rotation=45, ha='right', fontsize=10)
        ax.set_ylabel('Test Accuracy')
        ax.set_title(f'{self.model_name} - {self.hyperparam_combination} Across Folds', 
                    fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars (removed for cleaner visualization)
        # for i, (bar, value) in enumerate(zip(bars, data_sorted['test_accuracy'])):
        #     ax.text(bar.get_x() + bar.get_width()/2, value + 0.01, 
        #            f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        return fig

    def _create_hyperparameter_name(self, hyperparams: Dict[str, Any]) -> str:
        """Create a readable name for hyperparameter combination."""
        if self.model_name == "KNN":
            n_neighbors = hyperparams.get('n_neighbors', '?')
            weights = hyperparams.get('weights', '?')
            metric = hyperparams.get('metric', '?')
            return f"KNN_{metric}_n={n_neighbors}_w={weights}"
        elif self.model_name == "MLP":
            hidden_layers = hyperparams.get('hidden_layer_sizes', '?')
            activation = hyperparams.get('activation', '?')
            return f"MLP_{activation}_layers={hidden_layers}"
        elif self.model_name == "SVM":
            kernel = hyperparams.get('kernel', '?')
            C = hyperparams.get('C', '?')
            return f"SVM_{kernel}_C={C}"
        else:
            # Generic fallback
            param_strs = [f"{k}={v}" for k, v in hyperparams.items()]
            return f"{self.model_name}_{'_'.join(param_strs)}"


class PerSubjectAnalysisGraph(BaseGraph):
    """
    Creates per-subject analysis graphs showing accuracy for each subject.
    Reads from prediction parquet files to calculate per-subject performance.
    Creates both overall per-subject graph and individual graphs for each model×hyperparameter.
    """
    
    def __init__(self, config_handler: UnifiedConfigHandler, output_dir: Path):
        super().__init__(config_handler, output_dir)
        self.graph_name = "per_subject_analysis"
        # Create subdirectory for individual per-subject graphs
        self.per_subject_dir = output_dir / "per_subject_individual"
        logger.info(f"Initialized PerSubjectAnalysisGraph")

    def generate_and_save(self, ml_results_path: Path) -> None:
        """
        Generate and save per-subject analysis graphs.
        Creates both overall per-subject graph and individual graphs for each model×hyperparameter.
        """
        try:
            self.logger.info(f"📊 Loading per-subject data from: {ml_results_path}")
            
            # Load and process per-subject data
            all_data = self._load_per_subject_data(ml_results_path)
            if all_data is None or all_data.empty:
                raise ValueError("No per-subject data found or data is empty")
            
            self.logger.info(f"📊 Loaded {len(all_data)} subjects for per-subject analysis")
            
            # 1. Create overall per-subject graph (average across all models/hyperparams)
            overall_data = self._create_overall_per_subject_data(all_data)
            if overall_data is not None and not overall_data.empty:
                figure = self._create_per_subject_graph(overall_data, "Per-Subject Test Accuracy (Overall)")
                if figure is not None:
                    self.save_graph(figure, self.graph_name)
                    self.logger.info("✅ Overall per-subject analysis graph generated and saved successfully")
            
            # 2. Create individual graphs for each model×hyperparameter combination
            self._create_individual_per_subject_graphs(all_data)
            
            self.logger.info("✅ All per-subject analysis graphs generated and saved successfully")
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR generating per-subject analysis graph: {e}")
            import traceback
            self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
            raise  # Hard fail

    def _load_per_subject_data(self, ml_results_path: Path) -> pd.DataFrame:
        """
        Load per-subject data by reading prediction parquet files.
        Also loads hyperparameter information from results.json files.
        """
        model_dirs = [d for d in ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        
        if not model_dirs:
            raise ValueError("No model directories found")
        
        all_subject_data = []
        
        for model_dir in model_dirs:
            model_name = model_dir.name
            self.logger.info(f"📊 Processing model: {model_name}")
            
            # Get all hyperparameter directories for this model
            hyperparam_dirs = [d for d in model_dir.iterdir() 
                             if d.is_dir() and "_" in d.name]
            
            if not hyperparam_dirs:
                self.logger.warning(f"No hyperparameter directories found for model {model_name}")
                continue
            
            # Collect data from all hyperparameter directories
            for hyperparam_dir in hyperparam_dirs:
                test_parquet_file = hyperparam_dir / "test_predictions.parquet"
                results_json_file = hyperparam_dir / "results.json"
                
                if test_parquet_file.exists():
                    try:
                        # Read the parquet file
                        df = pd.read_parquet(test_parquet_file)
                        
                        # DEBUG: Print what columns we actually have (commented out for production)
                        # self.logger.info(f"🔍 DEBUG: Parquet file {test_parquet_file.name} columns: {df.columns.tolist()}")
                        # self.logger.info(f"🔍 DEBUG: Parquet file shape: {df.shape}")
                        # if not df.empty:
                        #     self.logger.info(f"🔍 DEBUG: First few rows:\n{df.head(2)}")
                        
                        # Calculate per-subject accuracy
                        if 'SubjectID' in df.columns and 'label' in df.columns and 'prediction' in df.columns:
                            # Check if Group column exists
                            if 'Group' in df.columns:
                                # Group by SubjectID and calculate accuracy and get group info
                                per_subject = df.groupby('SubjectID').apply(
                                    lambda x: pd.Series({
                                        'accuracy': (x['label'] == x['prediction']).mean(),
                                        'group': x['Group'].iloc[0]  # Get the group for each subject
                                    })
                                ).reset_index()
                            else:
                                # Group column doesn't exist - fail with informative error
                                self.logger.error(f"❌ CRITICAL ERROR: Group column not found in {test_parquet_file.name}")
                                self.logger.error(f"   📋 Available columns: {df.columns.tolist()}")
                                self.logger.error(f"   📊 DataFrame shape: {df.shape}")
                                self.logger.error(f"   🔍 Expected columns: ['SubjectID', 'EpochID', 'Group', 'label', 'prediction']")
                                self.logger.error(f"   💡 This suggests the data transformation pipeline didn't preserve the Group column")
                                raise ValueError(f"Group column missing from {test_parquet_file.name}. Available columns: {df.columns.tolist()}")
                            
                            # Add model and hyperparameter info
                            per_subject['model_name'] = model_name
                            per_subject['hyperparam_dir'] = hyperparam_dir.name
                            
                            # Try to load hyperparameter information from results.json
                            hyperparam_info = self._load_hyperparameter_info(results_json_file)
                            per_subject['hyperparam_info'] = hyperparam_info
                            
                            all_subject_data.append(per_subject)
                            
                    except Exception as e:
                        self.logger.warning(f"Error reading parquet file {test_parquet_file}: {e}")
        
        if not all_subject_data:
            raise ValueError("No per-subject data found in any parquet files")
        
        # Combine all data
        combined_data = pd.concat(all_subject_data, ignore_index=True)
        return combined_data

    def _create_overall_per_subject_data(self, all_data: pd.DataFrame) -> pd.DataFrame:
        """
        Create overall per-subject data by averaging across all models/hyperparameters.
        """
        # Calculate average accuracy per subject across all models/hyperparameters
        if 'group' in all_data.columns:
            # Include group information if available
            per_subject_avg = all_data.groupby('SubjectID').agg({
                'accuracy': 'mean',
                'group': 'first'  # Get the group for each subject (should be consistent)
            }).reset_index()
        else:
            # No group information available - fail with informative error
            self.logger.error(f"❌ CRITICAL ERROR: Group column not found in overall data")
            self.logger.error(f"   📋 Available columns: {all_data.columns.tolist()}")
            self.logger.error(f"   📊 DataFrame shape: {all_data.shape}")
            self.logger.error(f"   🔍 Expected columns: ['SubjectID', 'accuracy', 'group', 'model_name', 'hyperparam_dir']")
            self.logger.error(f"   💡 This suggests the per-subject data loading failed to include group information")
            raise ValueError(f"Group column missing from overall data. Available columns: {all_data.columns.tolist()}")
        
        per_subject_avg = per_subject_avg.sort_values('SubjectID', ascending=True)
        return per_subject_avg

    def _create_individual_per_subject_graphs(self, all_data: pd.DataFrame) -> None:
        """
        Create individual per-subject graphs for each model×hyperparameter combination.
        Saves them in a subdirectory within the graphs folder.
        """
        # Create the subdirectory if it doesn't exist
        self.per_subject_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"📁 Created individual per-subject graphs directory: {self.per_subject_dir}")
        
        # Group by model and hyperparameter
        grouped = all_data.groupby(['model_name', 'hyperparam_dir'])
        
        for (model_name, hyperparam_dir), group_data in grouped:
            # Create a clean filename (keep the directory name for uniqueness)
            clean_model = model_name.replace(' ', '_').lower()
            clean_hyperparam = hyperparam_dir.replace(' ', '_').replace('=', '_').lower()
            filename = f"per_subject_{clean_model}_{clean_hyperparam}"
            
            # Sort by subject ID (smallest first, e.g., sub-001, sub-002, etc.)
            sorted_data = group_data.sort_values('SubjectID')
            
            # Create a readable title with actual hyperparameters
            readable_title = self._create_readable_title(model_name, hyperparam_dir, all_data)
            
            # Create graph
            figure = self._create_per_subject_graph(sorted_data, readable_title)
            
            if figure is not None:
                # Save in the subdirectory
                self.save_graph_in_subdir(figure, filename)
                # self.logger.info(f"✅ Per-subject graph created for {model_name} - {hyperparam_dir}")

    def _create_per_subject_graph(self, data: pd.DataFrame, title: str = "Per-Subject Test Accuracy") -> plt.Figure:
        """Create the per-subject analysis graph with bar chart."""
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Create bar chart with color coding by group
        x_pos = np.arange(len(data))
        
        # Generate colors dynamically based on unique groups
        # Handle both 'Group' and 'group' column names
        if 'group' in data.columns:
            unique_groups = data['group'].unique()
        elif 'Group' in data.columns:
            unique_groups = data['Group'].unique()
        else:
            # No group column found - fail with informative error
            self.logger.error(f"❌ CRITICAL ERROR: No group column found in data for graph creation")
            self.logger.error(f"   📋 Available columns: {data.columns.tolist()}")
            self.logger.error(f"   📊 DataFrame shape: {data.shape}")
            self.logger.error(f"   🔍 Expected columns: ['SubjectID', 'accuracy', 'group']")
            self.logger.error(f"   💡 This suggests the data aggregation failed to include group information")
            raise ValueError(f"No group column found in data. Available columns: {data.columns.tolist()}")
        
        # Use a color palette that works well for categorical data
        import matplotlib.cm as cm
        import matplotlib.colors as mcolors
        
        # Generate distinct colors for each group
        if len(unique_groups) <= 10:
            # Use a predefined color palette for small number of groups
            color_palette = ['#2E8B57', '#DC143C', '#FF8C00', '#4169E1', '#8B0000', 
                           '#9370DB', '#20B2AA', '#FF6347', '#32CD32', '#FF1493']
        else:
            # Use a colormap for larger number of groups
            color_palette = cm.Set3(np.linspace(0, 1, len(unique_groups)))
        
        # Create mapping from group names to colors
        group_colors = {group: color_palette[i % len(color_palette)] 
                       for i, group in enumerate(unique_groups)}
        
        # Get colors for each bar based on group
        colors = [group_colors[group] for group in data['group']]
        
        bars = ax.bar(x_pos, data['accuracy'], color=colors, alpha=0.8)
        
        # Customize the plot
        ax.set_xticks(x_pos)
        ax.set_xticklabels(data['SubjectID'], rotation=45, ha='right', fontsize=12)
        ax.set_ylabel('Test Accuracy')
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        # Add legend for groups
        legend_elements = []
        for group in unique_groups:
            color = group_colors[group]
            legend_elements.append(plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.8, label=group.title()))
        
        if len(unique_groups) > 1:  # Only add legend if there are multiple groups
            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))
        
        # Add value labels on bars (removed for cleaner visualization)
        # for i, (bar, value) in enumerate(zip(bars, data['accuracy'])):
        #     ax.text(bar.get_x() + bar.get_width()/2, value + 0.01, 
        #            f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        return fig

    def save_graph_in_subdir(self, figure: plt.Figure, filename: str) -> None:
        """Save graph to the per_subject_individual subdirectory."""
        output_path = self.per_subject_dir / f"{filename}.{self.format}"
        figure.savefig(output_path, dpi=self.dpi, bbox_inches='tight', 
                      facecolor='white', edgecolor='none')
        self.logger.info(f"💾 Individual per-subject graph saved: {output_path}")
        plt.close(figure)

    def _load_hyperparameter_info(self, results_json_file: Path) -> str:
        """
        Load hyperparameter information from results.json file.
        Returns a readable string of hyperparameters.
        """
        try:
            if not results_json_file.exists():
                return "Unknown hyperparameters"
            
            import json
            with open(results_json_file, 'r') as f:
                results = json.load(f)
            
            # Extract hyperparameters from the results
            # Try different possible locations for hyperparameters
            hyperparams = results.get('hyperparameters', {})
            if not hyperparams:
                hyperparams = results.get('detailed_results', {}).get('hyperparams', {})
            if not hyperparams:
                hyperparams = results.get('hyperparams', {})
            
            if not hyperparams:
                return "Unknown hyperparameters"
            
            # Create a readable string of hyperparameters
            param_strings = []
            for key, value in hyperparams.items():
                if key.lower() in ['n_neighbors', 'n_neigh', 'k']:
                    param_strings.append(f"n_neighbors={value}")
                elif key.lower() in ['metric', 'distance_metric']:
                    param_strings.append(f"metric={value}")
                elif key.lower() in ['weights', 'weight']:
                    param_strings.append(f"weights={value}")
                elif key.lower() in ['algorithm', 'algo']:
                    param_strings.append(f"algorithm={value}")
                elif key.lower() in ['leaf_size']:
                    param_strings.append(f"leaf_size={value}")
                elif key.lower() in ['p']:
                    param_strings.append(f"p={value}")
                else:
                    param_strings.append(f"{key}={value}")
            
            return ", ".join(param_strings)
            
        except Exception as e:
            self.logger.warning(f"Could not load hyperparameters from {results_json_file}: {e}")
            return "Unknown hyperparameters"

    def _create_readable_title(self, model_name: str, hyperparam_dir: str, all_data: pd.DataFrame) -> str:
        """
        Create a readable title by extracting hyperparameters from the loaded data.
        Falls back to directory name if hyperparameters can't be extracted.
        """
        try:
            # Find the first row with this model and hyperparam_dir to get the hyperparam info
            sample_row = all_data[(all_data['model_name'] == model_name) & 
                                (all_data['hyperparam_dir'] == hyperparam_dir)].iloc[0]
            
            hyperparam_info = sample_row.get('hyperparam_info', 'Unknown hyperparameters')
            
            if hyperparam_info and hyperparam_info != "Unknown hyperparameters":
                return f"Per-Subject Test Accuracy: {model_name} - {hyperparam_info}"
            else:
                return f"Per-Subject Test Accuracy: {model_name} - {hyperparam_dir}"
                
        except Exception as e:
            self.logger.warning(f"Could not create readable title for {model_name} - {hyperparam_dir}: {e}")
            return f"Per-Subject Test Accuracy: {model_name} - {hyperparam_dir}"
