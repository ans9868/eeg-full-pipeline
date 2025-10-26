"""
Graph Generator for EEG Ray Tuner

This module provides the main interface for generating graphs from ML results.
It automatically detects the split type and creates appropriate graphs.
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from .single_split_graphs import BestModelsGraph, HyperparameterGraph
from .multi_fold_graphs import (
    BestModelsGraphMultiFold, 
    HyperparameterGraphMultiFold, 
    PerModelPerHyperparamAcrossFoldsGraph,
    PerSubjectAnalysisGraph
)


class GraphGenerator:
    """
    Main graph generator that handles different split types and creates appropriate graphs.
    """
    
    def __init__(self, config_handler, ml_results_path: str):
        """
        Initialize the graph generator.
        
        Args:
            config_handler: UnifiedConfigHandler instance
            ml_results_path: Path to ml_results directory
        """
        self.config_handler = config_handler
        self.ml_results_path = Path(ml_results_path)
        self.logger = logging.getLogger('ray_driver')
        
        # Verify ml_results directory exists
        if not self.ml_results_path.exists():
            raise FileNotFoundError(f"ML results directory not found: {self.ml_results_path}")
        
        # Create graphs output directory
        self.graphs_output_dir = self.ml_results_path / "graphs"
        self.graphs_output_dir.mkdir(exist_ok=True)
        
        self.logger.info(f"📊 Graph generator initialized")
        self.logger.info(f"📁 ML results path: {self.ml_results_path}")
        self.logger.info(f"📊 Graphs output: {self.graphs_output_dir}")
    
    def generate_graphs(self) -> None:
        """
        Generate all enabled graphs based on configuration.
        """
        try:
            self.logger.info("🎨 Starting graph generation...")
            self.logger.info(f"📁 ML results path: {self.ml_results_path}")
            self.logger.info(f"📊 Graphs output dir: {self.graphs_output_dir}")
            
            # Verify paths exist
            if not self.ml_results_path.exists():
                raise FileNotFoundError(f"ML results path does not exist: {self.ml_results_path}")
            
            # Check if any graphs are enabled
            if not self._any_graphs_enabled():
                self.logger.info("📊 No graphs enabled in configuration - skipping graph generation")
                return
            
            # Clear existing graphs directory to avoid confusion with old files
            self._clear_graphs_directory()
            
            # Detect split type
            split_type = self._detect_split_type()
            self.logger.info(f"🔍 Detected split type: {split_type}")
            
            if split_type == "single_split":
                self._generate_single_split_graphs()
            elif split_type == "multi_fold":
                self._generate_multi_fold_graphs()
            else:
                raise ValueError(f"Unknown split type: {split_type}")
                
            self.logger.info("✅ Graph generation completed successfully!")
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR in graph generation: {e}")
            self.logger.error(f"💥 Error type: {type(e).__name__}")
            import traceback
            self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
            raise  # Re-raise to ensure the error is not silently ignored
    
    def _any_graphs_enabled(self) -> bool:
        """Check if any graphs are enabled in configuration."""
        return (
            self.config_handler.best_models_graph or
            self.config_handler.per_model_across_hyperparameters_graph or
            self.config_handler.per_model_per_hyperparameter_across_folds_graph or
            self.config_handler.per_subject_analysis_graph
        )
    
    def _detect_split_type(self) -> str:
        """
        Detect whether this is a single split or multi-fold (LPSO) scenario.
        
        Returns:
            "single_split" or "multi_fold"
        """
        # First, check the configuration to see if LPSO is enabled
        try:
            # Check if the config indicates LPSO
            if hasattr(self.config_handler, 'data_leakage_strategy'):
                strategy = self.config_handler.data_leakage_strategy
                if 'LPSO' in strategy or 'Leave-P-Subjects-Out' in strategy:
                    self.logger.info(f"🔍 Detected multi-fold structure via config: {strategy}")
                    return "multi_fold"
            
            # Check if use_lpso is true in ray config
            ray_config = self.config_handler.get_ray_config()
            if ray_config.get('use_lpso', False):
                self.logger.info("🔍 Detected multi-fold structure via config: use_lpso=true")
                return "multi_fold"
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error checking config for LPSO: {e}")
        
        # Fallback: check for actual fold directories with sub- pattern
        print(f"🔍 DEBUG: Checking for multi-fold structure via fold directories with sub- pattern")
        self.logger.debug(f"🔍 DEBUG: Checking for multi-fold structure via fold directories with sub- pattern")
        # todo: do we need fallback method ? or just remove it ? 
        model_dirs = [d for d in self.ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        
        if model_dirs:
            # Check if any model directory contains sub-XXX_sub-YYY pattern
            for model_dir in model_dirs:
                fold_dirs = [d for d in model_dir.iterdir() 
                           if d.is_dir() and "sub-" in d.name and "_sub-" in d.name]
                if fold_dirs:
                    self.logger.info(f"🔍 Detected multi-fold structure via: {fold_dirs[0].name}")
                    return "multi_fold"
        
        # If no fold directories found, check model_comparison.csv
        model_comparison_file = self.ml_results_path / "model_comparison.csv"
        
        if model_comparison_file.exists():
            try:
                df = pd.read_csv(model_comparison_file)
                # Check if we have hyperparameter directories (single-split) vs fold directories (multi-fold)
                # Single-split typically has hyperparameter directories like "KNN_0_0097", "KNN_1_0910"
                # Multi-fold typically has fold directories like "sub-001_sub-002", "sub-003_sub-004"
                
                # Look for hyperparameter-style directories in model directories
                has_hyperparam_dirs = False
                for model_dir in model_dirs:
                    subdirs = [d for d in model_dir.iterdir() if d.is_dir()]
                    # Check if any subdirectory looks like a hyperparameter directory (contains underscores and numbers)
                    for subdir in subdirs:
                        if '_' in subdir.name and any(char.isdigit() for char in subdir.name):
                            has_hyperparam_dirs = True
                            break
                    if has_hyperparam_dirs:
                        break
                
                if has_hyperparam_dirs:
                    self.logger.info("🔍 Detected single-split structure via hyperparameter directories")
                    return "single_split"
                else:
                    # If no hyperparameter directories and num_folds > 1, might be multi-fold
                    if 'num_folds' in df.columns and any(df['num_folds'] > 1):
                        self.logger.info("🔍 Detected multi-fold structure via model_comparison.csv (num_folds>1)")
                        return "multi_fold"
                    else:
                        self.logger.info("🔍 Detected single-split structure via model_comparison.csv")
                        return "single_split"
            except Exception as e:
                self.logger.warning(f"⚠️ Error reading model_comparison.csv: {e}")
        
        # Fallback: check for hyperparameter comparison files
        if model_dirs:
            first_model_dir = model_dirs[0]
            hyperparam_file = first_model_dir / "hyperparameter_comparison.csv"
            
            if hyperparam_file.exists():
                try:
                    df = pd.read_csv(hyperparam_file)
                    if 'num_folds' in df.columns and all(df['num_folds'] == 1):
                        self.logger.info("🔍 Detected single-split structure via hyperparameter_comparison.csv (num_folds=1)")
                        return "single_split"
                    elif 'num_folds' in df.columns and any(df['num_folds'] > 1):
                        self.logger.info("🔍 Detected multi-fold structure via hyperparameter_comparison.csv (num_folds>1)")
                        return "multi_fold"
                except Exception as e:
                    self.logger.warning(f"⚠️ Error reading hyperparameter file: {e}")
        
        # Default to single_split if no clear indicators found
        self.logger.info("🔍 No clear indicators found, defaulting to single-split structure")
        return "single_split"
    
    def _generate_single_split_graphs(self) -> None:
        """Generate graphs for single split scenarios."""
        self.logger.info("📊 Generating single split graphs...")
        
        # Generate best models graph
        if self.config_handler.best_models_graph:
            self.logger.info("📈 Creating best models graph...")
            try:
                best_models_graph = BestModelsGraph(
                    config_handler=self.config_handler,
                    output_dir=self.graphs_output_dir
                )
                best_models_graph.generate_and_save(self.ml_results_path)
                self.logger.info("✅ Best models graph created successfully")
            except Exception as e:
                self.logger.error(f"💥 CRITICAL ERROR creating best models graph: {e}")
                import traceback
                self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
                raise  # Hard fail
        
        # Generate hyperparameter graphs for each model
        if self.config_handler.per_model_across_hyperparameters_graph:
            self.logger.info("📈 Creating hyperparameter comparison graphs...")
            try:
                models = self._get_available_models()
                if not models:
                    raise ValueError("No models found in ml_results directory")
                
                for model_name in models:
                    self.logger.info(f"📊 Creating hyperparameter graph for {model_name}...")
                    hyperparam_graph = HyperparameterGraph(
                        config_handler=self.config_handler,
                        model_name=model_name,
                        output_dir=self.graphs_output_dir
                    )
                    hyperparam_graph.generate_and_save(self.ml_results_path)
                    self.logger.info(f"✅ Hyperparameter graph for {model_name} created successfully")
            except Exception as e:
                self.logger.error(f"💥 CRITICAL ERROR creating hyperparameter graphs: {e}")
                import traceback
                self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
                raise  # Hard fail
        
        # Generate per-subject analysis graph
        if self.config_handler.per_subject_analysis_graph:
            self.logger.info("📈 Creating per-subject analysis graph...")
            print(f"🔍 DEBUG: per_subject_analysis_graph enabled: {self.config_handler.per_subject_analysis_graph}")
            print(f"🔍 DEBUG: graphs_output_dir: {self.graphs_output_dir}")
            try:
                per_subject_graph = PerSubjectAnalysisGraph(
                    config_handler=self.config_handler,
                    output_dir=self.graphs_output_dir
                )
                per_subject_graph.generate_and_save(self.ml_results_path)
                self.logger.info("✅ Per-subject analysis graph created successfully")
                print("✅ Per-subject analysis graph created successfully")
            except Exception as e:
                self.logger.error(f"💥 CRITICAL ERROR creating per-subject analysis graph: {e}")
                print(f"💥 CRITICAL ERROR creating per-subject analysis graph: {e}")
                import traceback
                self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
                print(f"💥 Traceback: {traceback.format_exc()}")
                raise  # Hard fail
        else:
            self.logger.info("📊 Per-subject analysis graph not enabled")
            print(f"🔍 DEBUG: per_subject_analysis_graph not enabled: {self.config_handler.per_subject_analysis_graph}")
        
        # Multi-fold graphs are not implemented yet
        if self.config_handler.per_model_per_hyperparameter_across_folds_graph:
            self.logger.info("📊 Per-model per-hyperparameter across folds graphs not implemented yet")
    
    def _generate_multi_fold_graphs(self) -> None:
        """Generate graphs for multi-fold scenarios."""
        self.logger.info("📊 Generating multi-fold graphs...")
        
        # Generate best models multi-fold graph
        if self.config_handler.best_models_graph:
            self.logger.info("📈 Creating best models multi-fold graph...")
            try:
                best_models_graph = BestModelsGraphMultiFold(
                    config_handler=self.config_handler,
                    output_dir=self.graphs_output_dir
                )
                best_models_graph.generate_and_save(self.ml_results_path)
                self.logger.info("✅ Best models multi-fold graph created successfully")
            except Exception as e:
                self.logger.error(f"💥 CRITICAL ERROR creating best models multi-fold graph: {e}")
                import traceback
                self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
                raise  # Hard fail
        
        # Generate hyperparameter multi-fold graphs for each model
        if self.config_handler.per_model_across_hyperparameters_graph:
            self.logger.info("📈 Creating hyperparameter multi-fold comparison graphs...")
            try:
                models = self._get_available_models()
                if not models:
                    raise ValueError("No models found in ml_results directory")
                
                for model_name in models:
                    self.logger.info(f"📊 Creating hyperparameter multi-fold graph for {model_name}...")
                    hyperparam_graph = HyperparameterGraphMultiFold(
                        config_handler=self.config_handler,
                        model_name=model_name,
                        output_dir=self.graphs_output_dir
                    )
                    hyperparam_graph.generate_and_save(self.ml_results_path)
                    self.logger.info(f"✅ Hyperparameter multi-fold graph for {model_name} created successfully")
            except Exception as e:
                self.logger.error(f"💥 CRITICAL ERROR creating hyperparameter multi-fold graphs: {e}")
                import traceback
                self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
                raise  # Hard fail
        
        # Generate per-model per-hyperparameter across folds graphs
        if self.config_handler.per_model_per_hyperparameter_across_folds_graph:
            self.logger.info("📈 Creating per-model per-hyperparameter across folds graphs...")
            try:
                models = self._get_available_models()
                if not models:
                    raise ValueError("No models found in ml_results directory")
                
                for model_name in models:
                    # Get hyperparameter combinations for this model
                    hyperparam_combinations = self._get_hyperparameter_combinations(model_name)
                    
                    for hyperparam_combo in hyperparam_combinations:
                        self.logger.info(f"📊 Creating fold graph for {model_name} - {hyperparam_combo}...")
                        fold_graph = PerModelPerHyperparamAcrossFoldsGraph(
                            config_handler=self.config_handler,
                            model_name=model_name,
                            hyperparam_combination=hyperparam_combo,
                            output_dir=self.graphs_output_dir
                        )
                        fold_graph.generate_and_save(self.ml_results_path)
                        self.logger.info(f"✅ Fold graph for {model_name} - {hyperparam_combo} created successfully")
            except Exception as e:
                self.logger.error(f"💥 CRITICAL ERROR creating per-model per-hyperparameter across folds graphs: {e}")
                import traceback
                self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
                raise  # Hard fail
        
        # Generate per-subject analysis graph
        if self.config_handler.per_subject_analysis_graph:
            self.logger.info("📈 Creating per-subject analysis graph...")
            try:
                per_subject_graph = PerSubjectAnalysisGraph(
                    config_handler=self.config_handler,
                    output_dir=self.graphs_output_dir
                )
                per_subject_graph.generate_and_save(self.ml_results_path)
                self.logger.info("✅ Per-subject analysis graph created successfully")
            except Exception as e:
                self.logger.error(f"💥 CRITICAL ERROR creating per-subject analysis graph: {e}")
                import traceback
                self.logger.error(f"💥 Traceback: {traceback.format_exc()}")
                raise  # Hard fail
    
    def _get_available_models(self) -> List[str]:
        """Get list of available models from ml_results directory."""
        model_dirs = [d for d in self.ml_results_path.iterdir() 
                     if d.is_dir() and d.name != "graphs"]
        return [d.name for d in model_dirs]
    
    def _get_hyperparameter_combinations(self, model_name: str) -> List[str]:
        """Get list of hyperparameter combinations for a specific model."""
        model_dir = self.ml_results_path / model_name
        
        if not model_dir.exists():
            return []
        
        # Get all fold directories for this model
        fold_dirs = [d for d in model_dir.iterdir() 
                    if d.is_dir() and "sub-" in d.name and "_sub-" in d.name]
        
        hyperparam_combinations = set()
        
        for fold_dir in fold_dirs:
            results_file = fold_dir / "results.json"
            
            if results_file.exists():
                try:
                    import json
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    
                    # Extract hyperparameters
                    hyperparams = results.get('hyperparameters', {})
                    
                    # Create hyperparameter combination name
                    if model_name == "KNN":
                        n_neighbors = hyperparams.get('n_neighbors', '?')
                        weights = hyperparams.get('weights', '?')
                        metric = hyperparams.get('metric', '?')
                        combo_name = f"KNN_{metric}_n={n_neighbors}_w={weights}"
                    elif model_name == "MLP":
                        hidden_layers = hyperparams.get('hidden_layer_sizes', '?')
                        activation = hyperparams.get('activation', '?')
                        combo_name = f"MLP_{activation}_layers={hidden_layers}"
                    elif model_name == "SVM":
                        kernel = hyperparams.get('kernel', '?')
                        C = hyperparams.get('C', '?')
                        combo_name = f"SVM_{kernel}_C={C}"
                    else:
                        # Generic fallback
                        # todo: fill in the rest of the models here so no fallback is needed
                        param_strs = [f"{k}={v}" for k, v in hyperparams.items()]
                        combo_name = f"{model_name}_{'_'.join(param_strs)}"
                    
                    hyperparam_combinations.add(combo_name)
                    
                except Exception as e:
                    self.logger.warning(f"Error reading results from {results_file}: {e}")
        
        return list(hyperparam_combinations)
    
    def _clear_graphs_directory(self) -> None:
        """
        Clear the graphs directory to remove old graph files.
        This ensures we don't have confusion with previous runs.
        """
        try:
            if self.graphs_output_dir.exists():
                # Count existing files
                existing_files = list(self.graphs_output_dir.glob("*"))
                if existing_files:
                    self.logger.info(f"🧹 Clearing {len(existing_files)} existing graph files from {self.graphs_output_dir}")
                    
                    # Remove all files in the graphs directory
                    for file_path in existing_files:
                        if file_path.is_file():
                            file_path.unlink()
                            self.logger.debug(f"🗑️ Removed: {file_path.name}")
                        elif file_path.is_dir():
                            # Remove subdirectories recursively
                            import shutil
                            shutil.rmtree(file_path)
                            self.logger.debug(f"🗑️ Removed directory: {file_path.name}")
                    
                    self.logger.info("✅ Graphs directory cleared successfully")
                else:
                    self.logger.info("📁 Graphs directory is already empty")
            else:
                # Create the directory if it doesn't exist
                self.graphs_output_dir.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"📁 Created graphs directory: {self.graphs_output_dir}")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Warning: Could not clear graphs directory: {e}")
            # Don't fail the entire process if we can't clear the directory
