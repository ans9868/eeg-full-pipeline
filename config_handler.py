"""
Unified Configuration Handler for EEG Full Pipeline

This module provides a unified interface for configuration management across
both PySpark and Ray components of the EEG processing pipeline.

Author: Adel Sahuc
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import yaml


class UnifiedConfigHandler:
    """
    Unified configuration management for the entire EEG pipeline.
    Handles both PySpark and Ray configurations with consistent validation.

    Every validation method directly corresponds to a Part function in config-maker.py:
        - metadataPart0_validate() ← metadataPart0()
        - dataInputPart1_validate() ← dataInputPart1()
        - preprocessingPart2_validate() ← preprocessingPart2()
        - featureCreationPart3_validate() ← featureCreationPart3()
        - featureTransformationsPart4_validate() ← featureTransformationsPart4()
        - dataLeakagePreventionPart5_validate() ← dataLeakagePreventionPart5()
        - deploymentMethodPart6_validate() ← deploymentMethodPart6() (PySpark section)
        - rayConfigurationPart7_validate() ← rayConfigurationPart7()
        - slurmOptionsPart6_validate() ← deploymentMethodPart6() (SLURM section)

    This ensures perfect synchronization between configuration creation and validation.

    Why:
    This class is useful because it allows consistent validation across the pipepline (the ray and pyspark sections).
    Before this class each function had its own validation logic which led to wild goose chases for dubugging validation errors and insuring consistent functionality accross runs.
    """

    def __init__(self, config_path: str):
        """Initialize the unified configuration handler.

        Parameters
        ----------
        config_path : str
            Path to the configuration YAML file
        """
        self.config_path = config_path
        self.raw_config = None
        self._load_and_validate()

    # ========================================
    # CORE LOADING AND VALIDATION
    # ========================================

    def _load_and_validate(self) -> None:
        """Load and validate the configuration in one step."""
        self.raw_config = self._load_config()
        self._validate_config()
        print("✅ Configuration loaded and validated successfully!")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        print(f"🔧 Loading configuration from: {self.config_path}")

        # Check if config file exists
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, "r") as f:
                config = cast(Dict[str, Any], yaml.safe_load(f))

            if config is None:
                raise ValueError("Configuration file is empty")

            print("📋 Configuration loaded successfully!")
            return config

        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML configuration: {e}")
            raise
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            raise

    def _validate_config(self) -> None:
        """Validate the entire configuration."""
        print("🔍 Validating configuration...")

        # Skip validation if this is a test configuration
        if self.raw_config.get("test", False):
            print("🧪 Test configuration detected - skipping validation")
            return

        # TODO edit this to only validate sections needed for the target container and/or setup
        # This could be enhanced to validate only sections needed based on:
        # - Container type (PySpark-only, Ray-only, or full)
        # - Experiment type (ML vs Analysis)
        # - Deployment method (Docker vs Singularity)
        required_sections = ["project"]

        # Check required sections exist
        for section in required_sections:
            if section not in self.raw_config:
                raise ValueError(f"Missing required configuration section: {section}")
            if not self.raw_config[section]:
                raise ValueError(f"Config section '{section}' is empty")

        # Validate individual sections
        self.metadataPart0_validate()

        # Conditional validation based on what's present
        if "data_input" in self.raw_config:
            self.dataInputPart1_validate()
        if "preprocessing" in self.raw_config:
            self.preprocessingPart2_validate()
        if "feature_extraction" in self.raw_config:
            self.featureCreationPart3_validate()
        if "feature_transformation" in self.raw_config:
            self.featureTransformationsPart4_validate()
        if "data_leakage_prevention" in self.raw_config:
            self.dataLeakagePreventionPart5_validate()
        if "pyspark" in self.raw_config:
            self.deploymentMethodPart6_validate()
        if "ray" in self.raw_config:
            self.rayConfigurationPart7_validate()

        # Validate SLURM options if present (created by config-maker.py)
        # SLURM options are stored inside the project section
        project_config = self.raw_config.get("project", {})
        if "slurm_options" in project_config:
            self.slurmOptionsPart6_validate()

        print("✅ Configuration validation completed!")

    # ========================================
    # SECTION-SPECIFIC VALIDATION
    # ========================================
    # Each validation method directly corresponds to a Part function in config-maker.py:
    # all the functions and names are at the top of the file

    def metadataPart0_validate(self) -> None:
        """Validate project configuration (metadataPart0)."""
        project_config = self.raw_config.get("project", {})

        # Required project fields
        required_project_fields = ["name", "experiment_type", "deployment_method", "random_seed"]
        for field in required_project_fields:
            if field not in project_config:
                raise ValueError(f"Missing required project field: {field}")
            if not project_config[field]:
                raise ValueError(f"Project field '{field}' is empty")
        
        # Validate random_seed
        random_seed = project_config["random_seed"]
        if not isinstance(random_seed, int):
            raise ValueError("random_seed must be an integer")
        if random_seed < 0:
            raise ValueError("random_seed must be non-negative")

        # Validate experiment type
        valid_experiment_types = [
            "ML Classification",
            "ML Clustering", 
            "ML Fingerprinting",
            "Analysis (No Ray ML)",
        ]

        experiment_type = project_config["experiment_type"]
        if experiment_type not in valid_experiment_types:
            raise ValueError(
                f"Invalid experiment type: {experiment_type}. "
                f"Must be one of: {valid_experiment_types}"
            )

        # Validate deployment method
        valid_deployment_methods = [
            "Docker",
            "Singularity with Slurm",
            "Singularity without Slurm",
        ]

        deployment_method = project_config["deployment_method"]
        if deployment_method not in valid_deployment_methods:
            raise ValueError(
                f"Invalid deployment method: {deployment_method}. "
                f"Must be one of: {valid_deployment_methods}"
            )

        # Validate subjects_or_events if present
        if "subjects_or_events" in project_config:
            subjects_or_events = project_config["subjects_or_events"]
            if subjects_or_events not in ["subjects", "events"]:
                raise ValueError("subjects_or_events must be 'subjects' or 'events'")

        # Validate events_of_interest if analyzing events
        if "subjects_or_events" in project_config and project_config["subjects_or_events"] == "events":
            raise ValueError(
                "Unfortunately support for events has not been created yet."
            )

        # Validate output_dir if present
        if "output_dir" in project_config:
            output_dir = project_config["output_dir"]
            if not isinstance(output_dir, str) or not output_dir.strip():
                raise ValueError("output_dir must be a non-empty string")

        # Validate config_name if present
        if "config_name" in project_config:
            config_name = project_config["config_name"]
            if not isinstance(config_name, str) or not config_name.strip():
                raise ValueError("config_name must be a non-empty string")

    def dataInputPart1_validate(self) -> None:
        """Validate data input configuration (dataInputPart1)."""
        data_input_config = self.raw_config.get("data_input", {})

        # Check groups
        if "groups" not in data_input_config:
            raise ValueError("Missing 'groups' in data_input section")

        groups = data_input_config["groups"]
        if not groups:
            raise ValueError("Data input 'groups' section is empty")

        # Check each group has files
        for group_name, file_paths in groups.items():
            if not file_paths:
                raise ValueError(f"Group '{group_name}' has no file paths")
            if not isinstance(file_paths, list):
                raise ValueError(f"Group '{group_name}' file_paths must be a list")
            if len(file_paths) == 0:
                raise ValueError(f"Group '{group_name}' has empty file paths list")

    def preprocessingPart2_validate(self) -> None:
        """Validate preprocessing configuration (preprocessingPart2)."""
        preprocessing_config = self.raw_config.get("preprocessing", {})

        # Check required preprocessing fields
        required_preprocessing_fields = [
            "window_size",
            "sliding_window",
            "reject_by_annotation",
        ]
        for field in required_preprocessing_fields:
            if field not in preprocessing_config:
                raise ValueError(f"Missing required preprocessing field: {field}")
            if preprocessing_config[field] is None:
                raise ValueError(f"Preprocessing field '{field}' is None")

        # Check bands if present
        if "bands" in preprocessing_config:
            bands = preprocessing_config["bands"]
            if not bands:
                raise ValueError("Preprocessing 'bands' section is empty")

        # Validate downsampling if present
        if "downsampling" in preprocessing_config:
            downsampling = preprocessing_config["downsampling"]
            if downsampling is not None and not isinstance(downsampling, (int, float)):
                raise ValueError("Downsampling must be a number or None")
            if downsampling is not None and downsampling <= 0:
                raise ValueError("Downsampling rate must be positive")

        # Validate normalize_psd if present
        if "normalize_psd" in preprocessing_config:
            normalize_psd = preprocessing_config["normalize_psd"]
            if normalize_psd not in ["Yes", "No"]:
                raise ValueError("normalize_psd must be 'Yes' or 'No'")

        # Validate epoch rejection if present
        if "epoch_rejection" in preprocessing_config:
            epoch_rejection = preprocessing_config["epoch_rejection"]
            if epoch_rejection is not None:
                if not isinstance(epoch_rejection, dict):
                    raise ValueError("epoch_rejection must be a dictionary or None")
                if "reject" in epoch_rejection:
                    reject = epoch_rejection["reject"]
                    if not isinstance(reject, (int, float)) or reject <= 0:
                        raise ValueError(
                            "epoch_rejection.reject must be a positive number"
                        )
                if "flat" in epoch_rejection:
                    flat = epoch_rejection["flat"]
                    if not isinstance(flat, (int, float)) or flat < 0:
                        raise ValueError(
                            "epoch_rejection.flat must be a non-negative number"
                        )

        # Validate use_epoch_rejection if present
        if "use_epoch_rejection" in preprocessing_config:
            use_epoch_rejection = preprocessing_config["use_epoch_rejection"]
            if use_epoch_rejection not in ["Yes", "No"]:
                raise ValueError("use_epoch_rejection must be 'Yes' or 'No'")

    def featureCreationPart3_validate(self) -> None:
        """Validate feature extraction configuration (featureCreationPart3)."""
        feature_extraction_config = self.raw_config.get("feature_extraction", {})

        # Check required feature extraction fields
        required_feature_extraction_fields = ["method", "features", "output_format"]
        for field in required_feature_extraction_fields:
            if field not in feature_extraction_config:
                raise ValueError(f"Missing required feature_extraction field: {field}")
            if feature_extraction_config[field] is None:
                raise ValueError(f"Feature extraction field '{field}' is None")

        # Validate method
        method = feature_extraction_config["method"]
        valid_methods = ["welch", "multitaper"]
        if method not in valid_methods:
            raise ValueError(
                f"Feature extraction method must be one of: {valid_methods}"
            )

        # Validate output_format
        output_format = feature_extraction_config["output_format"]
        valid_formats = ["ml", "analysis"]
        if output_format not in valid_formats:
            raise ValueError(f"Output format must be one of: {valid_formats}")

        # Validate features structure
        features = feature_extraction_config["features"]
        if not isinstance(features, dict):
            raise ValueError("Features must be a dictionary")

        # Check for required feature types
        required_feature_types = ["per_channel_across_bands", "per_channel_per_band"]
        for feature_type in required_feature_types:
            if feature_type not in features:
                raise ValueError(f"Missing required feature type: {feature_type}")
            if not isinstance(features[feature_type], list):
                raise ValueError(f"Feature type {feature_type} must be a list")

        # Validate relative band power requirements
        self._validate_relative_band_power_requirements(features)

    def featureTransformationsPart4_validate(self) -> None:
        """Validate feature transformation configuration (featureTransformationsPart4)."""
        feature_transformation_config = self.raw_config.get(
            "feature_transformation", {}
        )

        # Check required feature transformation fields
        required_feature_transformation_fields = ["transformations", "synthetic"]
        for field in required_feature_transformation_fields:
            if field not in feature_transformation_config:
                raise ValueError(
                    f"Missing required feature_transformation field: {field}"
                )
            # Allow None for transformations field (means no transformation)
            if field == "transformations" and feature_transformation_config[field] is None:
                continue
            if field != "transformations" and feature_transformation_config[field] is None:
                raise ValueError(f"Feature transformation field '{field}' is None")

        # Validate transformations
        transformations = feature_transformation_config["transformations"]
        if not self._validate_transformation(transformations):
            raise ValueError(f"Unsupported transformation: {transformations}")

        # Validate synthetic
        synthetic = feature_transformation_config["synthetic"]
        valid_synthetic_options = ["None"]  # Add more as they become available
        if synthetic not in valid_synthetic_options:
            raise ValueError(
                f"Synthetic option must be one of: {valid_synthetic_options}"
            )

        # Validate transformer-specific configurations if transformations are selected
        if transformations is not None and transformations != ["None"]:
            # PCA configuration

            if "PCA (manual count)" in transformations:
                if "pca_components" not in feature_transformation_config:
                    raise ValueError(
                        "Missing pca_components for PCA (manual count) transformation"
                    )
                pca_components = feature_transformation_config["pca_components"]
                if not isinstance(pca_components, int) or pca_components <= 0:
                    raise ValueError("pca_components must be a positive integer")

            # SVD configuration
            if "SVD (k components)" in transformations:
                if "svd_components" not in feature_transformation_config:
                    raise ValueError(
                        "Missing svd_components for SVD (k components) transformation"
                    )
                svd_components = feature_transformation_config["svd_components"]
                if not isinstance(svd_components, int) or svd_components <= 0:
                    raise ValueError("svd_components must be a positive integer")

            # MinMax scaler configuration
            if "MinMax scaler" in transformations:
                if "minmax_range" not in feature_transformation_config:
                    raise ValueError(
                        "Missing minmax_range for MinMax scaler transformation"
                    )
                minmax_range = feature_transformation_config["minmax_range"]
                if not isinstance(minmax_range, list) or len(minmax_range) != 2:
                    raise ValueError(
                        "minmax_range must be a list with exactly 2 elements"
                    )
                if not all(isinstance(x, (int, float)) for x in minmax_range):
                    raise ValueError("minmax_range elements must be numbers")

            # Robust scaler configuration
            if "Robust scaler" in transformations:
                if "robust_scaler_with_centering" not in feature_transformation_config:
                    raise ValueError(
                        "Missing robust_scaler_with_centering for Robust scaler transformation"
                    )
                if "robust_scaler_with_scaling" not in feature_transformation_config:
                    raise ValueError(
                        "Missing robust_scaler_with_scaling for Robust scaler transformation"
                    )
                if not isinstance(
                    feature_transformation_config["robust_scaler_with_centering"], bool
                ):
                    raise ValueError("robust_scaler_with_centering must be a boolean")
                if not isinstance(
                    feature_transformation_config["robust_scaler_with_scaling"], bool
                ):
                    raise ValueError("robust_scaler_with_scaling must be a boolean")

            # Normalizer configuration
            if "Normalizer" in transformations:
                if "normalizer_p" not in feature_transformation_config:
                    raise ValueError(
                        "Missing normalizer_p for Normalizer transformation"
                    )
                normalizer_p = feature_transformation_config["normalizer_p"]
                if not isinstance(normalizer_p, (int, float)) and normalizer_p != float(
                    "inf"
                ):
                    raise ValueError("normalizer_p must be a number or float('inf')")

            # ANOVA F-test configuration
            if "ANOVA F-test" in transformations:
                # Check required ANOVA fields
                required_anova_fields = [
                    "anova_label_column", 
                    "anova_label_type", 
                    "anova_selection_mode", 
                    "anova_selection_threshold"
                ]
                for field in required_anova_fields:
                    if field not in feature_transformation_config:
                        raise ValueError(f"Missing required ANOVA field: {field}")

                # Validate anova_label_column
                anova_label_column = feature_transformation_config["anova_label_column"]
                valid_label_columns = ["Group", "SubjectID"]
                if anova_label_column not in valid_label_columns:
                    raise ValueError(f"anova_label_column must be one of: {valid_label_columns}")

                # Validate anova_label_type
                anova_label_type = feature_transformation_config["anova_label_type"]
                valid_label_types = ["categorical"]
                if anova_label_type not in valid_label_types:
                    raise ValueError(f"anova_label_type must be one of: {valid_label_types}")

                # Validate anova_selection_mode
                anova_selection_mode = feature_transformation_config["anova_selection_mode"]
                valid_selection_modes = ["numTopFeatures", "percentile"]
                if anova_selection_mode not in valid_selection_modes:
                    raise ValueError(f"anova_selection_mode must be one of: {valid_selection_modes}")

                # Validate anova_selection_threshold based on selection mode
                anova_selection_threshold = feature_transformation_config["anova_selection_threshold"]
                if anova_selection_mode == "numTopFeatures":
                    if not isinstance(anova_selection_threshold, int) or anova_selection_threshold <= 0:
                        raise ValueError("anova_selection_threshold must be a positive integer for numTopFeatures mode")
                elif anova_selection_mode == "percentile":
                    if not isinstance(anova_selection_threshold, (int, float)) or anova_selection_threshold <= 0 or anova_selection_threshold > 1:
                        raise ValueError("anova_selection_threshold must be a float between 0 and 1 for percentile mode")

            # Cohen test configuration
            if "Cohen test (manual count)" in transformations:
                if "cohen_components" not in feature_transformation_config:
                    raise ValueError(
                        "Missing cohen_components for Cohen test (manual count) transformation"
                    )
                cohen_components = feature_transformation_config["cohen_components"]
                if not isinstance(cohen_components, int) or cohen_components <= 0:
                    raise ValueError("cohen_components must be a positive integer")

            if "Cohen test (limit to % for example 0.05)" in transformations:
                if "cohen_limit" not in feature_transformation_config:
                    raise ValueError(
                        "Missing cohen_limit for Cohen test (limit to %) transformation"
                    )
                cohen_limit = feature_transformation_config["cohen_limit"]
                if (
                    not isinstance(cohen_limit, (int, float))
                    or cohen_limit <= 0
                    or cohen_limit >= 1
                ):
                    raise ValueError("cohen_limit must be a number between 0 and 1")

    def dataLeakagePreventionPart5_validate(self) -> None:
        """Validate data leakage prevention configuration (dataLeakagePreventionPart5)."""
        data_leakage_config = self.raw_config.get("data_leakage_prevention", {})

        if not data_leakage_config:
            return  # Optional section

        # Check required field
        if "strategy" not in data_leakage_config:
            raise ValueError("Missing required data_leakage_prevention field: strategy")

        strategy = data_leakage_config["strategy"]
        valid_strategies = [
            "1 test/1 train split (inter subject split) with transforms applied to training set only (faster, single split)",
            "Within-subject (intra subject split) train/test split (80/20 per subject) - each subject contributes to both train and test",
            "LPSO (Leave-P-Subjects-Out) (inter subject split) - systematic cross-validation (recommended for small datasets)",
            "Transform all data together (intra subject split) (no split - fastest, and potential data leakage)",
        ]

        if strategy not in valid_strategies:
            raise ValueError(
                f"Data leakage prevention strategy must be one of: {valid_strategies}"
            )

        # ML Fingerprinting can only use intra-subject splits (same subjects in train/test)
        experiment_type = self.raw_config.get("project", {}).get("experiment_type", "")
        if experiment_type == "ML Fingerprinting":
            inter_subject_strategies = [
                "1 test/1 train split (inter subject split) with transforms applied to training set only (faster, single split)",
                "LPSO (Leave-P-Subjects-Out) (inter subject split) - systematic cross-validation (recommended for small datasets)",
            ]
            if strategy in inter_subject_strategies:
                raise ValueError(
                    f"ML Fingerprinting cannot use inter-subject splits. "
                    f"Strategy '{strategy}' is not allowed for ML Fingerprinting. "
                    f"Please use 'Transform all data together (intra subject split)' or "
                    f"'Within-subject (intra subject split) train/test split' instead."
                )

        # Validate additional fields based on strategy
        if "LPSO (Leave-P-Subjects-Out)" in strategy:
            required_lpso_fields = [
                "use_lpso",
                "lpso_subjects_per_group",
                "lpso_folds",
                "lpso_metadata",
            ]
            for field in required_lpso_fields:
                if field not in data_leakage_config:
                    raise ValueError(f"Missing {field} for LPSO strategy")

            # Validate LPSO-specific fields
            if not isinstance(data_leakage_config["use_lpso"], bool):
                raise ValueError("use_lpso must be a boolean")

            if not isinstance(data_leakage_config["lpso_subjects_per_group"], int):
                raise ValueError("lpso_subjects_per_group must be an integer")

            if not isinstance(data_leakage_config["lpso_folds"], list):
                raise ValueError("lpso_folds must be a list")

            if not isinstance(data_leakage_config["lpso_metadata"], dict):
                raise ValueError("lpso_metadata must be a dictionary")
            
            # Get data input groups to calculate total subjects
            groups = self.groups

            if not groups:
                return  # No groups configured, validation will happen later

            # Calculate total subjects
            total_subjects = sum(len(paths) for paths in groups.values())

            # Check each fold to ensure it doesn't leave out all subjects
            for fold_idx, fold_subjects in enumerate(self.lpso_folds):
                if len(fold_subjects) >= total_subjects:
                    raise ValueError(
                        f"❌ Invalid LPSO configuration detected! "
                        f"Fold {fold_idx + 1} leaves out {len(fold_subjects)} subjects >= {total_subjects} total subjects. "
                        f"This would leave no training subjects, preventing transformers from fitting. "
                        f"Please ensure at least one subject remains for training."
                    )

            print(
                f"✅ LPSO configuration validation passed: {len(self.lpso_folds)} folds, {total_subjects} total subjects"
            )
            
            # Validate leaky LPSO configuration if present
            if "leaky_lpso" in data_leakage_config:
                if not isinstance(data_leakage_config["leaky_lpso"], bool):
                    raise ValueError("leaky_lpso must be a boolean")
                
                if data_leakage_config["leaky_lpso"]:
                    print("⚠️  LEAKY LPSO ENABLED: This will cause data leakage!")
                    print("   📊 Transformers will be fitted on ALL subjects (including test)")
                    print("   🎯 Use only for research experiments studying data leakage effects")
                    print("   ⚠️  This may lead to overly optimistic performance estimates")
                else:
                    print("✅ Standard LPSO: No data leakage (recommended)")
            else:
                # Default to False if not specified
                data_leakage_config["leaky_lpso"] = False
                print("✅ Standard LPSO: No data leakage (default)")

        elif "Within-subject" in strategy and "train/test split" in strategy:
            # Check for new unified intra_test_train_split configuration
            if "intra_test_train_split" in data_leakage_config:
                self._validate_intra_test_train_split(data_leakage_config["intra_test_train_split"])
            # Check for deprecated within_subject_split configuration
            elif "within_subject_split" in data_leakage_config:
                print("⚠️  DEPRECATION WARNING: 'within_subject_split' is deprecated. Please use 'intra_test_train_split' instead.")
                self._validate_within_subject_split_deprecated(data_leakage_config["within_subject_split"])
            else:
                raise ValueError(
                    "Missing intra_test_train_split configuration for within-subject split strategy. "
                    "Please add 'intra_test_train_split' section to your configuration."
                )

        elif "Transform all data together" in strategy:
            # Check for optional intra_test_train_split configuration
            if "intra_test_train_split" in data_leakage_config:
                self._validate_intra_test_train_split(data_leakage_config["intra_test_train_split"])
                print("✅ Intra-test-train split configuration found for 'Transform all data together' strategy")

        elif "1 test/1 train split" in strategy:
            if "single_split_method" not in data_leakage_config:
                raise ValueError(
                    "Missing single_split_method for 1 test/1 train split strategy"
                )

    def _validate_intra_test_train_split(self, intra_test_train_split_config: Dict[str, Any]) -> None:
        """Validate the new unified intra_test_train_split configuration."""
        required_fields = [
            "train_ratio",
            "random_seed",
            "split_method"
        ]
        
        for field in required_fields:
            if field not in intra_test_train_split_config:
                raise ValueError(f"Missing {field} in intra_test_train_split configuration")
        
        # Validate train_ratio
        train_ratio = intra_test_train_split_config["train_ratio"]
        if not isinstance(train_ratio, (int, float)) or not (0.1 <= train_ratio <= 1.0):
            raise ValueError("train_ratio must be a number between 0.1 and 1.0")
        
        # Validate random_seed
        if not isinstance(intra_test_train_split_config["random_seed"], int):
            raise ValueError("random_seed must be an integer")
        
        # Validate split_method
        valid_split_methods = ["start", "middle", "end", "random"]
        if intra_test_train_split_config["split_method"] not in valid_split_methods:
            raise ValueError(f"split_method must be one of: {valid_split_methods}")
        
        print(f"✅ Intra-test-train split validation passed: {train_ratio} train ratio, {intra_test_train_split_config['split_method']} method")

    def _validate_within_subject_split_deprecated(self, within_subject_config: Dict[str, Any]) -> None:
        """Validate the deprecated within_subject_split configuration."""
        required_fields = [
            "train_ratio",
            "test_ratio", 
            "random_seed",
            "split_method"
        ]
        
        for field in required_fields:
            if field not in within_subject_config:
                raise ValueError(f"Missing {field} in within_subject_split configuration")
        
        # Validate train_ratio and test_ratio
        train_ratio = within_subject_config["train_ratio"]
        test_ratio = within_subject_config["test_ratio"]
        
        if not isinstance(train_ratio, (int, float)) or not (0.1 <= train_ratio <= 0.9):
            raise ValueError("train_ratio must be a number between 0.1 and 0.9")
        
        if not isinstance(test_ratio, (int, float)) or not (0.1 <= test_ratio <= 0.9):
            raise ValueError("test_ratio must be a number between 0.1 and 0.9")
        
        if abs((train_ratio + test_ratio) - 1.0) > 0.001:
            raise ValueError("train_ratio + test_ratio must equal 1.0")
        
        # Validate random_seed
        if not isinstance(within_subject_config["random_seed"], int):
            raise ValueError("random_seed must be an integer")
        
        # Validate split_method
        valid_split_methods = ["random", "stratified"]
        if within_subject_config["split_method"] not in valid_split_methods:
            raise ValueError(f"split_method must be one of: {valid_split_methods}")

    def deploymentMethodPart6_validate(self) -> None:
        """Validate PySpark configuration (deploymentMethodPart6)."""
        pyspark_config = self.raw_config.get("pyspark", {})

        # Check required PySpark fields
        required_pyspark_fields = [
            "master",
            "driver_memory",
            "executor_memory",
            "executor_cores",
            "shuffle_partitions",
        ]
        for field in required_pyspark_fields:
            if field not in pyspark_config:
                raise ValueError(f"Missing required PySpark field: {field}")
            if pyspark_config[field] is None:
                raise ValueError(f"PySpark field '{field}' is None")

    def rayConfigurationPart7_validate(self) -> None:
        """Validate Ray configuration (rayConfigurationPart7)."""
        ray_config = self.raw_config.get("ray", {})

        # Basic validation - Ray config is more flexible
        if "models" in ray_config:
            models = ray_config["models"]
            if not isinstance(models, list):
                raise ValueError("Ray models must be a list")

        # Validate numeric fields if present
        numeric_fields = ["num_trials", "max_concurrent", "cv_folds", "random_state"]
        for field in numeric_fields:
            if field in ray_config:
                try:
                    int(ray_config[field])
                except (ValueError, TypeError):
                    raise ValueError(f"Ray field '{field}' must be a valid integer")

        # Validate Ray resources if present
        if "resources" in ray_config:
            resources = ray_config["resources"]
            if resources is None:
                raise ValueError("Ray resources must be a dictionary and not None")
            if not isinstance(resources, dict):
                raise ValueError("Ray resources must be a dictionary and not None")

            # Validate required resource fields
            required_resource_fields = [
                "num_cpus",
                "memory_gb",
                "object_store_memory_gb",
            ]
            for field in required_resource_fields:
                if field in resources:
                    try:
                        int(resources[field])
                    except (ValueError, TypeError):
                        raise ValueError(
                            f"Ray resource field '{field}' must be a valid integer"
                        )

            # Validate GPU configuration
            if "num_gpus" in resources:
                try:
                    gpu_count = int(resources["num_gpus"])
                    if gpu_count < 0:
                        raise ValueError(
                            "Ray resource num_gpus must be non-negative"
                        )
                except (ValueError, TypeError):
                    raise ValueError(
                        "Ray resource num_gpus must be a valid integer"
                    )

            # Validate dashboard port
            if "dashboard_port" in resources:
                try:
                    port = int(resources["dashboard_port"])
                    if port < 1 or port > 65535:
                        raise ValueError(
                            "Ray resource dashboard_port must be between 1 and 65535"
                        )
                except (ValueError, TypeError):
                    raise ValueError(
                        "Ray resource dashboard_port must be a valid integer"
                    )

        # Validate model_configs if present
        if "model_configs" in ray_config:
            model_configs = ray_config["model_configs"]
            if not isinstance(model_configs, dict):
                raise ValueError("Ray model_configs must be a dictionary")

            # Validate each model configuration
            for model_name, model_config in model_configs.items():
                if not isinstance(model_config, dict):
                    raise ValueError(
                        f"Ray model_config for {model_name} must be a dictionary"
                    )

                if "use_default" in model_config:
                    if not isinstance(model_config["use_default"], bool):
                        raise ValueError(
                            f"Ray model_config.use_default for {model_name} must be a boolean"
                        )

                if "hyperparameters" in model_config:
                    hyperparams = model_config["hyperparameters"]
                    if not isinstance(hyperparams, dict):
                        raise ValueError(
                            f"Ray model_config.hyperparameters for {model_name} must be a dictionary"
                        )

        # Validate graph data visualization configuration
        """Validate graph data visualization configuration."""
        graph_config = ray_config.get("graph_data_visualization", {})
        
        # Check if any graph options are enabled
        graph_options = [
            "best_models_graph",
            "per_model_accross_hyperparameters_graph", 
            "per_model_per_hyperparameter_across_folds_graph",
            "per_subject_analysis_graph",
            "per_subject_hyperparameter_analysis"
        ]
        
        any_graph_enabled = any(
            graph_config.get(option, "No") == "Yes" 
            for option in graph_options
        )
        
        # If any graph is enabled, save_prediction_outputs must also be enabled
        if any_graph_enabled:
            save_outputs = graph_config.get("save_prediction_outputs", "No")
            if save_outputs != "Yes":
                raise ValueError(
                    "Graph visualization options require 'save_prediction_outputs' to be set to 'Yes'. "
                    f"Current value: '{save_outputs}'. "
                    "Please enable 'save_prediction_outputs' in your configuration."
                )


    def slurmOptionsPart6_validate(self) -> None:
        """Validate SLURM options configuration (slurmOptionsPart6)."""
        # SLURM options are stored inside the project section
        project_config = self.raw_config.get("project", {})
        slurm_config = project_config.get("slurm_options", {})

        if not isinstance(slurm_config, dict):
            raise ValueError("SLURM options must be a dictionary")

        # Validate build options if present
        if "build" in slurm_config:
            build_options = slurm_config["build"]
            if not isinstance(build_options, str):
                raise ValueError("SLURM build options must be a string")

        # Validate PySpark options if present
        if "pyspark" in slurm_config:
            pyspark_options = slurm_config["pyspark"]
            if not isinstance(pyspark_options, str):
                raise ValueError("SLURM PySpark options must be a string")

        # Validate Ray options if present
        if "ray" in slurm_config:
            ray_options = slurm_config["ray"]
            if not isinstance(ray_options, str):
                raise ValueError("SLURM Ray options must be a string")

    def validate_all_sections(self) -> None:
        """
        Validate all configuration sections upfront.
        This method provides comprehensive validation of the entire configuration
        and should be called once in main.py before passing config to pipeline functions.
        """
        print("🔍 Validating all configuration sections...")

        # Validate individual sections
        self.metadataPart0_validate()

      # Conditional validation based on experiment type and what's present
        experiment_type = self.raw_config.get("project", {}).get("experiment_type", "")
        
        # Base sections that should always be present
        sections_to_validate = [
            "data_input",
            "preprocessing", 
            "feature_extraction",
            "feature_transformation",
            "pyspark",
        ]
        
        # Add ML-specific sections only for ML experiments (not Analysis)
        if experiment_type.startswith("ML "):
            sections_to_validate.append("data_leakage_prevention")
            sections_to_validate.append("ray")
        
        # Add SLURM section if using Singularity with Slurm
        include_slurm = (
            self.raw_config["project"]["deployment_method"] == "Singularity with Slurm"
        )
        if include_slurm:
            # SLURM options are stored inside the project section, not at root level
            project_config = self.raw_config.get("project", {})
            if "slurm_options" not in project_config:
                raise ValueError("Section slurm_options is missing from the project configuration")
            
        # Every section should be in self.raw_config (except slurm_options which is in project)
        for section in sections_to_validate:
            if section not in self.raw_config:
                raise ValueError(f"Section {section} is missing from the configuration")

        self.dataInputPart1_validate()
        self.preprocessingPart2_validate()
        self.featureCreationPart3_validate()
        self.featureTransformationsPart4_validate()
        self.dataLeakagePreventionPart5_validate()
        self.deploymentMethodPart6_validate()
        self.rayConfigurationPart7_validate()

        if include_slurm:
            self.slurmOptionsPart6_validate()

        print("✅ All configuration sections validated successfully!")



    def _validate_transformation(self, transformations) -> bool:
        """
        Validate that the transformation(s) are supported.

        Args:
            transformations: String, list of strings, or None describing the transformation(s)

        Returns:
            True if all transformations are supported
        """
        supported_transformations = [
            "None",
            "Dummy (+1)",
            "MinMax scaler",
            "Z-score standardization",
            "Standard scaler",
            "Robust scaler",
            "Normalizer",
            "Log transform (log1p)",
            "PCA (retain 95% variance)",
            "PCA (manual count)",
            "SVD (k components)",
            "ANOVA F-test",
            # 'Cohen test (manual count)', # not implemented (can be done with logistic regression)
            # 'Cohen test (limit to % for example 0.05)'
        ]

        # Handle None case (no transformation)
        if transformations is None:
            return True

        # Handle both string and list formats for backward compatibility
        if isinstance(transformations, str):
            # Convert string to list (backward compatibility)
            if transformations == "None":
                transformations = ["None"]
            else:
                # Split by comma and clean up
                transformations = [
                    t.strip() for t in transformations.split(",") if t.strip()
                ]

        # Validate each transformation
        for transformation in transformations:
            if transformation not in supported_transformations:
                return False

        return True

    def _validate_relative_band_power_requirements(self, features: Dict[str, List[str]]) -> None:
        """
        Validate relative band power requirements.
        
        Args:
            features: Features configuration dictionary
        """
        # Check if relative_band_power is selected
        per_channel_per_band_features = features.get('per_channel_per_band', [])
        has_relative_band_power = 'relative_band_power' in per_channel_per_band_features
        
        if not has_relative_band_power:
            return  # No validation needed if relative_band_power is not selected
        
        # Get frequency bands from preprocessing config
        preprocessing_config = self.raw_config.get("preprocessing", {})
        bands = preprocessing_config.get('bands', {})
        bands_count = len(bands)
        
        # Validate that we have at least 2 bands for relative power calculation
        if bands_count < 2:
            raise ValueError(
                f"relative_band_power requires 2+ frequency bands, but only {bands_count} band(s) selected. "
                f"Please select more bands in the preprocessing configuration."
            )
        
        # Validate that bands are properly configured
        if not bands:
            raise ValueError(
                "relative_band_power requires frequency bands to be configured in preprocessing. "
                "Please add 'bands' section to 'preprocessing' config."
            )
        
        # Validate band structure
        for band_name, band_range in bands.items():
            if not isinstance(band_range, list) or len(band_range) != 2:
                raise ValueError(
                    f"Invalid frequency band format for '{band_name}'. "
                    f"Expected [low, high] but got {band_range}"
                )
            if band_range[0] >= band_range[1]:
                raise ValueError(
                    f"Invalid frequency range for '{band_name}': "
                    f"low ({band_range[0]}) must be less than high ({band_range[1]})"
                )

    # ========================================
    # PROPERTY ACCESSORS - UNIFIED INTERFACE
    # ========================================

    # Project Properties
    @property
    def project_name(self) -> str:
        """Get project name."""
        return self.raw_config.get("project", {}).get("name", "eeg_pipeline")

    @property
    def global_random_seed(self) -> int:
        """Get global random seed."""
        return self.raw_config.get("project", {}).get("random_seed", 42)

    @property
    def experiment_type(self) -> str:
        """Get experiment type."""
        return self.raw_config.get("project", {}).get(
            "experiment_type", "Analysis (No Ray ML)"
        )

    @property
    def deployment_method(self) -> str:
        """Get deployment method."""
        return self.raw_config.get("project", {}).get("deployment_method")

    @property
    def base_output_dir(self) -> str:
        """Get base output directory."""
        return self.raw_config.get("project", {}).get("output_dir", "./data")

    @property
    def output_dir(self) -> Path:
        """Get full output directory path."""
        return Path(self.base_output_dir) / self.project_name

    # Data Input Properties
    @property
    def data_input(self) -> Dict[str, Any]:
        """Get complete data input configuration."""
        return self.raw_config.get("data_input", {})
    
    @property
    def groups(self) -> Dict[str, list]:
        """Get data groups."""
        return self.raw_config.get("data_input", {}).get("groups", {})

    @property
    def reuse_processed_subjects(self) -> bool:
        """Get reuse_processed_subjects setting."""
        return (
            self.raw_config.get("data_input", {}).get("reuse_processed_subjects", "No")
            == "Yes"
        )

    @property
    def save_processed_subjects(self) -> bool:
        """Get save_processed_subjects setting."""
        return (
            self.raw_config.get("data_input", {}).get("save_processed_subjects", "No")
            == "Yes"
        )

    @property
    def reuse_transformed(self) -> bool:
        """Get reuse_transformed setting."""
        return (
            self.raw_config.get("data_input", {}).get("reuse_transformed", "No")
            == "Yes"
        )

    @property
    def save_transformed(self) -> bool:
        """Get save_transformed setting."""
        return (
            self.raw_config.get("data_input", {}).get("save_transformed", "No") == "Yes"
        )

    # Preprocessing Properties
    @property
    def window_size(self) -> float:
        """Get window size setting."""
        return self.raw_config.get("preprocessing", {}).get("window_size")

    @property
    def sliding_window(self) -> float:
        """Get sliding window setting."""
        return self.raw_config.get("preprocessing", {}).get("sliding_window")

    @property
    def reject_by_annotation(self) -> bool:
        """Get reject_by_annotation setting."""
        return (
            self.raw_config.get("preprocessing", {}).get("reject_by_annotation", "Yes")
            == "Yes"
        )

    @property
    def downsampling(self) -> Optional[float]:
        """Get downsampling rate setting."""
        return self.raw_config.get("preprocessing", {}).get("downsampling", None)

    @property
    def normalize_psd(self) -> bool:
        """Get normalize_psd setting."""
        return (
            self.raw_config.get("preprocessing", {}).get("normalize_psd", "Yes")
            == "Yes"
        )

    # Feature Extraction Properties
    @property
    def method(self) -> str:
        """Get feature extraction method."""
        return self.raw_config.get("feature_extraction", {}).get("method", "welch")

    @property
    def output_format(self) -> str:
        """Get output format setting."""
        return self.raw_config.get("feature_extraction", {}).get("output_format", "ml")

    @property
    def features(self) -> Dict[str, List[str]]:
        """Get features configuration."""
        return self.raw_config.get("feature_extraction", {}).get("features", {})

    @property
    def show_intermediate_results(self) -> bool:
        """Get show_intermediate_results setting."""
        return (
            self.raw_config.get("feature_extraction", {}).get(
                "show_intermediate_results", "No"
            )
            == "Yes"
        )

    @property
    def show_intermediate_counts(self) -> bool:
        """Get show_intermediate_counts setting."""
        return (
            self.raw_config.get("feature_extraction", {}).get(
                "show_intermediate_counts", "No"
            )
            == "Yes"
        )

    # Feature Transformation Properties
    @property
    def transform_features_flag(self) -> str:
        """Get transform_features_flag setting."""
        return self.raw_config.get("feature_transformation", {}).get(
            "transformations", "None"
        )

    @property
    def synthetic(self) -> str:
        """Get synthetic data generation method."""
        return self.raw_config.get("feature_transformation", {}).get(
            "synthetic", "None"
        )

 
    @property
    def anova_selection_mode(self) -> str:
        """Get ANOVA F-test selection mode."""
        return self.raw_config.get("feature_transformation", {}).get("anova_selection_mode", None)

    @property
    def anova_label_column(self) -> str:
        """Get ANOVA F-test label column."""
        return self.raw_config.get("feature_transformation", {}).get("anova_label_column", None)

    @property
    def anova_selection_threshold(self) -> Union[int, float]:
        """Get ANOVA F-test selection threshold."""
        return self.raw_config.get("feature_transformation", {}).get("anova_selection_threshold", None)

    @property
    def anova_label_type(self) -> str:
        """Get ANOVA F-test label type."""
        return self.raw_config.get("feature_transformation", {}).get("anova_label_type", None)


    # Data Leakage Prevention Properties
    @property
    def data_leakage_strategy(self) -> str:
        """Get data leakage prevention strategy."""
        return self.raw_config.get("data_leakage_prevention", {}).get(
            "strategy",
            "Transform all data together (intra subject split) (no split - fastest, and potential data leakage)",
        )

    @property
    def uses_lpso(self) -> bool:
        """Check if LPSO cross-validation is being used."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        strategy = dlp_config.get("strategy", "")
        return "LPSO" in strategy or dlp_config.get("use_lpso", False)

    @property
    def lpso_folds(self) -> Optional[List[List[str]]]:
        """Get LPSO folds if available."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        return dlp_config.get("lpso_folds")

    @property
    def test_subjects(self) -> Optional[List[str]]:
        """Get test subjects if available."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        return dlp_config.get("test_subjects_paths")

    @property
    def individual_lpso(self) -> bool:
        """Get individual_lpso setting."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        return dlp_config.get("individual_lpso", False)

    @property
    def leaky_lpso(self) -> bool:
        """Get leaky_lpso setting (data leakage experiment)."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        return dlp_config.get("leaky_lpso", False)

    @property
    def intra_test_train_split_train_ratio(self) -> float:
        """Get intra-test-train split train ratio."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        intra_split_config = dlp_config.get("intra_test_train_split", {})
        return intra_split_config.get("train_ratio")

    @property
    def intra_test_train_split_test_ratio(self) -> float:
        """Get intra-test-train split test ratio."""
        return (10.0*1.0 - self.intra_test_train_split_train_ratio*10.0)/10.0
        
    @property
    def intra_test_train_split_seed(self) -> int:
        """Get intra-test-train split random seed."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        intra_split_config = dlp_config.get("intra_test_train_split", {})
        return intra_split_config.get("random_seed", self.global_random_seed)

    @property
    def intra_test_train_split_method(self) -> str:
        """Get intra-test-train split method."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        intra_split_config = dlp_config.get("intra_test_train_split", {})
        return intra_split_config.get("split_method", "random")

    # Deprecated properties for backward compatibility
    @property
    def within_subject_train_ratio(self) -> float:
        """Get within-subject train ratio (deprecated - use intra_test_train_split_train_ratio)."""
        dlp_config = self.raw_config.get("data_leakage_prevention", {})
        # Try new unified config first
        intra_split_config = dlp_config.get("intra_test_train_split", {})
        if intra_split_config:
            return intra_split_config.get("train_ratio")
        # Fallback to deprecated config
        within_subject_config = dlp_config.get("within_subject_split", {})
        return within_subject_config.get("train_ratio")

    @property
    def within_subject_test_ratio(self) -> float:
        """Get within-subject test ratio (deprecated - calculated from train_ratio)."""
        train_ratio = self.intra_test_train_split_train_ratio
        return (10*1.0 - 10*train_ratio)/10.0

    @property
    def within_subject_split_seed(self) -> int:
        """Get within-subject split random seed (deprecated - use intra_test_train_split_seed)."""
        return self.intra_test_train_split_seed

    @property
    def within_subject_split_method(self) -> str:
        """Get within-subject split method (deprecated - use intra_test_train_split_method)."""
        return self.intra_test_train_split_method

    @property
    def uses_within_subject_split(self) -> bool:
        """Check if within-subject split is configured."""
        return "Within-subject" in self.data_leakage_strategy and "train/test split" in self.data_leakage_strategy

    # Ray Properties
    @property
    def selected_models(self) -> List[str]:
        """Get selected ML models from Ray configuration."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("models", [])

    @property
    def optimization_metric(self) -> str:
        """Get the optimization metric from Ray configuration."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("metric", "accuracy")

    @property
    def optimization_mode(self) -> str:
        """Get the optimization mode from Ray configuration."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("mode", "max")

    @property
    def num_trials(self) -> int:
        """Get number of trials from Ray configuration."""
        ray_config = self.raw_config.get("ray", {})
        return int(ray_config.get("num_trials", 10))

    @property
    def max_concurrent_trials(self) -> int:
        """Get maximum concurrent trials from Ray configuration."""
        ray_config = self.raw_config.get("ray", {})
        return int(ray_config.get("max_concurrent", 2))

    @property
    def cv_folds(self) -> int:
        """Get number of CV folds from Ray configuration."""
        ray_config = self.raw_config.get("ray", {})
        return int(ray_config.get("cv_folds", 5))

    @property
    def random_state(self) -> int:
        """Get random state from Ray configuration."""
        ray_config = self.raw_config.get("ray", {})
        return int(ray_config.get("random_state", self.global_random_seed))

    @property
    def ray_resources(self) -> Optional[Dict[str, Any]]:
        """Get Ray resource configuration."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("ray")

    @property
    def has_ray_resources(self) -> bool:
        """Check if Ray-specific resources are configured."""
        return self.ray_resources is not None

    @property
    def model_configs(self) -> Dict[str, Any]:
        """Get model configurations from Ray configuration."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("model_configs", {})

    @property
    def ray_resources_config(self) -> Optional[Dict[str, Any]]:
        """Get Ray resources configuration (nested under 'resources' key)."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("resources")

    @property
    def ray_num_cpus(self) -> int:
        """Get number of CPUs for Ray cluster."""
        resources = self.ray_resources_config
        if resources:
            return int(resources.get("num_cpus", 4))
        return 4

    @property
    def ray_memory_gb(self) -> int:
        """Get memory in GB for Ray cluster."""
        resources = self.ray_resources_config
        if resources:
            return int(resources.get("memory_gb", 8))
        return 8

    @property
    def ray_object_store_memory_gb(self) -> int:
        """Get object store memory in GB for Ray cluster."""
        resources = self.ray_resources_config
        if resources:
            return int(resources.get("object_store_memory_gb", 4))
        return 4

    @property
    def ray_num_gpus(self) -> int:
        """Get number of GPUs for Ray cluster."""
        resources = self.ray_resources_config
        if resources:
            return int(resources.get("num_gpus", 0))
        return 0

    @property
    def ray_dashboard_port(self) -> int:
        """Get dashboard port for Ray cluster."""
        resources = self.ray_resources_config
        if resources:
            return int(resources.get("dashboard_port", 8265))
        return 8265
    
    # @property 
    # def data_directory(self) -> str:
    #     """Get the data directory path for the project."""
    #     return str(self.output_dir)
    
    @property
    def experiment_config(self) -> Dict[str, Any]:
        """Get complete experiment configuration for Ray workers."""
        return {
            'experiment_type': self.experiment_type,
            'random_seed': self.global_random_seed,
            'data_leakage_strategy': self.data_leakage_strategy,
            'selected_models': self.selected_models,
            'optimization_metric': self.optimization_metric,
            'optimization_mode': self.optimization_mode
        }

    # Hash Keys for Stage Validation
    @property
    def processed_subjects_keys(self) -> List[str]:
        """Get processed subjects config keys for hash validation."""
        return ["feature_extraction", "preprocessing"]

    @property
    def transformed_keys(self) -> List[str]:
        """Get transformed config keys for hash validation."""
        return ["feature_transformation", "feature_extraction", "data_leakage_prevention"]

    # ========================================
    # SECTION ACCESSORS
    # ========================================

    def get_raw_config(self) -> Dict[str, Any]:
        """Get raw config dict for backward compatibility."""
        return self.raw_config

    def get_project_config(self) -> Dict[str, Any]:
        """Get project configuration."""
        return self.raw_config.get("project", {})

    def get_data_input_config(self) -> Dict[str, Any]:
        """Get data input configuration."""
        return self.raw_config.get("data_input", {})

    def get_preprocessing_config(self) -> Dict[str, Any]:
        """Get preprocessing configuration."""
        return self.raw_config.get("preprocessing", {})

    def get_feature_extraction_config(self) -> Dict[str, Any]:
        """Get feature extraction configuration."""
        return self.raw_config.get("feature_extraction", {})

    def get_feature_transformation_config(self) -> Dict[str, Any]:
        """Get feature transformation configuration."""
        return self.raw_config.get("feature_transformation", {})

    def get_data_leakage_prevention_config(self) -> Dict[str, Any]:
        """Get data leakage prevention configuration."""
        return self.raw_config.get("data_leakage_prevention", {})

    def get_pyspark_config(self) -> Dict[str, Any]:
        """Get PySpark configuration."""
        return self.raw_config.get("pyspark", {})

    def get_ray_config(self) -> Dict[str, Any]:
        """Get Ray configuration."""
        return self.raw_config.get("ray", {})
    
    def get_graph_visualization_config(self) -> Dict[str, Any]:
        """Get graph visualization configuration."""
        ray_config = self.get_ray_config()
        return ray_config.get("graph_data_visualization", {})
    
    @property
    def save_prediction_outputs(self) -> bool:
        """Get save prediction outputs configuration."""
        graph_config = self.get_graph_visualization_config()
        return graph_config.get("save_prediction_outputs", "No") == "Yes"

    @property
    def graphs_wanted(self) -> bool:
        """Check if graph visualization is enabled by inferring from the graph options."""
        graph_config = self.get_graph_visualization_config()
        
        # Check if any of the graph options are enabled
        best_models_enabled = graph_config.get("best_models_graph", "No") == "Yes"
        hyperparam_enabled = graph_config.get("per_model_accross_hyperparameters_graph", "No") == "Yes"
        folds_enabled = graph_config.get("per_model_per_hyperparameter_across_folds_graph", "No") == "Yes"
        per_subject_enabled = graph_config.get("per_subject_analysis_graph", "No") == "Yes"
        per_subject_hyperparam_enabled = graph_config.get("per_subject_hyperparameter_analysis", "No") == "Yes"
        
        # If any graph option is enabled, then graphs are wanted
        return best_models_enabled or hyperparam_enabled or folds_enabled or per_subject_enabled or per_subject_hyperparam_enabled
    
    @property
    def which_models_for_graphs(self) -> str:
        """Get which models to generate graphs for."""
        graph_config = self.get_graph_visualization_config()
        return graph_config.get("which_models", "All")
    
    @property
    def visualization_enabled(self) -> bool:
        """Check if visualization is enabled."""
        return self.graphs_wanted
    
    @property
    def individual_config_visualizations_enabled(self) -> bool:
        """Check if individual configuration visualizations are enabled."""
        return self.graphs_wanted and self.which_models_for_graphs == "All"
    
    @property
    def best_models_graph(self) -> bool:
        """Check if best models graph is enabled."""
        graph_config = self.get_graph_visualization_config()
        return graph_config.get("best_models_graph", "No") == "Yes"
    
    @property
    def per_model_across_hyperparameters_graph(self) -> bool:
        """Check if per model across hyperparameters graph is enabled."""
        graph_config = self.get_graph_visualization_config()
        return graph_config.get("per_model_accross_hyperparameters_graph", "No") == "Yes"
    
    @property
    def per_model_per_hyperparameter_across_folds_graph(self) -> bool:
        """Check if per model per hyperparameter across folds graph is enabled."""
        graph_config = self.get_graph_visualization_config()
        return graph_config.get("per_model_per_hyperparameter_across_folds_graph", "No") == "Yes"
    
    @property
    def per_subject_analysis_graph(self) -> bool:
        """Check if per subject analysis graph is enabled."""
        graph_config = self.get_graph_visualization_config()
        return graph_config.get("per_subject_analysis_graph", "No") == "Yes"
    
    @property
    def per_subject_hyperparameter_analysis(self) -> bool:
        """Check if hyperparameter-specific per-subject analysis is enabled."""
        graph_config = self.get_graph_visualization_config()
        return graph_config.get("per_subject_hyperparameter_analysis", "No") == "Yes"
    
    @property
    def per_subject_top_n_models(self) -> int:
        """Get the number of top models to include in per-subject analysis."""
        graph_config = self.get_graph_visualization_config()
        return int(graph_config.get("per_subject_top_n_models", "3"))

    # ========================================
    # UTILITY METHODS
    # ========================================

    def is_ml_experiment(self) -> bool:
        """Check if this is an ML experiment."""
        return "ML" in self.experiment_type

    def is_classification_experiment(self) -> bool:
        """Check if this is a classification experiment."""
        return self.experiment_type == "ML Classification"

    def is_clustering_experiment(self) -> bool:
        """Check if this is a clustering experiment."""
        return self.experiment_type == "ML Clustering"
    
    def is_fingerprinting_experiment(self) -> bool:
        """Check if this is a fingerprinting experiment."""
        return self.experiment_type == "ML Fingerprinting"

    def print_summary(self) -> None:
        """Print a summary of the configuration."""
        print(f"\n📋 Configuration Summary for: {self.project_name}")
        print(f"🔬 Experiment Type: {self.experiment_type}")
        print(f"🚀 Deployment Method: {self.deployment_method}")
        print(f"📁 Output Directory: {self.output_dir}")
        print(f"🎲 Random Seed: {self.global_random_seed}")
        
        if self.is_ml_experiment():
            print(f"🤖 Selected Models: {', '.join(self.selected_models)}")
            print(f"📊 Data Leakage Strategy: {self.data_leakage_strategy}")
            print(f"🔧 Transformations: {self.transform_features_flag}")
        
        print(f"✅ Configuration is valid and ready to use!")


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        try:
            handler = UnifiedConfigHandler(config_path)
            handler.print_summary()
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("Usage: python config-handler.py <config_file.yaml>")
        print("Example: python config-handler.py config/config_example.yaml")
