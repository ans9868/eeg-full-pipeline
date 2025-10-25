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

        # Validate expose_ports if present
        if "expose_ports" in project_config:
            expose_ports = project_config["expose_ports"]
            if expose_ports not in ["Yes", "No"]:
                raise ValueError("expose_ports must be 'Yes' or 'No'")

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
        """Validate Ray configuration with multiple search strategies (rayConfigurationPart7)."""
        ray_config = self.raw_config.get("ray", {})

        # 1. Validate search_strategies list (NEW)
        if "search_strategies" not in ray_config:
            raise ValueError("Ray configuration must include 'search_strategies' list")
        
        search_strategies = ray_config.get("search_strategies", [])
        if not isinstance(search_strategies, list):
            raise ValueError("Ray 'search_strategies' must be a list")
        
        if len(search_strategies) == 0:
            raise ValueError("At least one search strategy must be selected")
        
        valid_strategies = ["grid_search", "ax"]
        for strategy in search_strategies:
            if strategy not in valid_strategies:
                raise ValueError(
                    f"Invalid search strategy '{strategy}'. "
                    f"Valid strategies: {valid_strategies}"
                )

        # 2. Validate Grid Search config if present
        if "grid_search" in search_strategies:
            if "grid_search" not in ray_config:
                raise ValueError("'grid_search' strategy selected but configuration missing")
            self._validate_grid_search_config(ray_config["grid_search"])

        # 3. Validate Ax config if present
        if "ax" in search_strategies:
            if "ax" not in ray_config:
                raise ValueError("'ax' strategy selected but configuration missing")
            self._validate_ax_config(ray_config["ax"])

        # 4. Validate common Ray configuration
        self._validate_ray_common_config(ray_config)

    def _validate_grid_search_config(self, grid_config: Dict[str, Any]) -> None:
        """Validate Grid Search specific configuration."""
        # Validate models
        if "models" not in grid_config:
            raise ValueError("Grid Search configuration must include 'models' list")
        
        models = grid_config["models"]
        if not isinstance(models, list):
            raise ValueError("Grid Search 'models' must be a list")
        
        if len(models) == 0:
            raise ValueError("At least one model must be selected for Grid Search")

        # Validate max_concurrent
        if "max_concurrent" in grid_config:
            try:
                max_concurrent = int(grid_config["max_concurrent"])
                if max_concurrent < 1:
                    raise ValueError("Grid Search 'max_concurrent' must be positive")
            except (ValueError, TypeError):
                raise ValueError("Grid Search 'max_concurrent' must be a valid integer")

        # Validate cv_folds
        if "cv_folds" in grid_config:
            try:
                cv_folds = int(grid_config["cv_folds"])
                if cv_folds < 2:
                    raise ValueError("Grid Search 'cv_folds' must be at least 2")
            except (ValueError, TypeError):
                raise ValueError("Grid Search 'cv_folds' must be a valid integer")

        # Validate model_configs if present
        if "model_configs" in grid_config:
            model_configs = grid_config["model_configs"]
            if not isinstance(model_configs, dict):
                raise ValueError("Grid Search 'model_configs' must be a dictionary")

            # Validate each model configuration
            for model_name, model_config in model_configs.items():
                if not isinstance(model_config, dict):
                        raise ValueError(
                        f"Grid Search model_config for {model_name} must be a dictionary"
                    )

                if "use_default" in model_config:
                    if not isinstance(model_config["use_default"], bool):
                        raise ValueError(
                            f"Grid Search model_config.use_default for {model_name} must be a boolean"
                        )

                if "hyperparameters" in model_config:
                    hyperparams = model_config["hyperparameters"]
                    if not isinstance(hyperparams, dict):
                        raise ValueError(
                            f"Grid Search model_config.hyperparameters for {model_name} must be a dictionary"
                        )
                    
                    # 🔧 FIX: Convert MLP hidden_layer_sizes from string tuples to lists
                    if model_name == "MLP (Neural Network)" and "hidden_layer_sizes" in hyperparams:
                        hyperparams["hidden_layer_sizes"] = self._convert_mlp_architectures(
                            hyperparams["hidden_layer_sizes"], 
                            f"Grid Search {model_name}"
                        )

        # Validate CPU resource configuration
        if "cpus_per_model_task" in grid_config:
            cpus_per_model = grid_config["cpus_per_model_task"]
            try:
                cpus_per_model = int(cpus_per_model)
            except (ValueError, TypeError):
                raise ValueError(
                    f"grid_search.cpus_per_model_task must be a valid integer, got: {cpus_per_model}"
                )
            if cpus_per_model < 2:
                raise ValueError(
                    f"grid_search.cpus_per_model_task must be >= 2, got: {cpus_per_model}"
                )

        if "max_concurrent_trials" in grid_config:
            max_concurrent = grid_config["max_concurrent_trials"]
            try:
                max_concurrent = int(max_concurrent)
            except (ValueError, TypeError):
                raise ValueError(
                    f"grid_search.max_concurrent_trials must be a valid integer, got: {max_concurrent}"
                )
            if max_concurrent < 1:
                raise ValueError(
                    f"grid_search.max_concurrent_trials must be >= 1, got: {max_concurrent}"
                )
            
            # Validate relationship: max_concurrent_trials < cpus_per_model_task
            if "cpus_per_model_task" in grid_config:
                cpus_per_model = grid_config["cpus_per_model_task"]
                try:
                    cpus_per_model = int(cpus_per_model)
                except (ValueError, TypeError):
                    cpus_per_model = 0
                if max_concurrent >= cpus_per_model and cpus_per_model > 0:
                    raise ValueError(
                        f"grid_search.max_concurrent_trials ({max_concurrent}) must be < "
                        f"grid_search.cpus_per_model_task ({cpus_per_model}). "
                        f"At least 1 CPU must be reserved for Tuner coordination."
                    )

        # Support old naming (max_concurrent) for backward compatibility
        if "max_concurrent" in grid_config and "max_concurrent_trials" not in grid_config:
            print("⚠️  WARNING: Using deprecated 'max_concurrent' field. Please use 'max_concurrent_trials' instead.")

    def _validate_ax_config(self, ax_config: Dict[str, Any]) -> None:
        """Validate Ax specific configuration."""
        # Validate models
        if "models" not in ax_config:
            raise ValueError("Ax configuration must include 'models' list")
        
        models = ax_config["models"]
        if not isinstance(models, list):
            raise ValueError("Ax 'models' must be a list")
        
        if len(models) == 0:
            raise ValueError("At least one model must be selected for Ax")

        # Validate max_concurrent
        if "max_concurrent" in ax_config:
            try:
                max_concurrent = int(ax_config["max_concurrent"])
                if max_concurrent < 1:
                    raise ValueError("Ax 'max_concurrent' must be positive")
            except (ValueError, TypeError):
                raise ValueError("Ax 'max_concurrent' must be a valid integer")

        # Validate cv_folds
        if "cv_folds" in ax_config:
            try:
                cv_folds = int(ax_config["cv_folds"])
                if cv_folds < 2:
                    raise ValueError("Ax 'cv_folds' must be at least 2")
            except (ValueError, TypeError):
                raise ValueError("Ax 'cv_folds' must be a valid integer")

        # Validate model_configs if present
        if "model_configs" in ax_config:
            model_configs = ax_config["model_configs"]
            if not isinstance(model_configs, dict):
                raise ValueError("Ax 'model_configs' must be a dictionary")

            # Validate each model configuration
            for model_name, model_config in model_configs.items():
                if not isinstance(model_config, dict):
                    raise ValueError(
                        f"Ax model_config for {model_name} must be a dictionary"
                    )

                if "use_default" in model_config:
                    if not isinstance(model_config["use_default"], bool):
                        raise ValueError(
                            f"Ax model_config.use_default for {model_name} must be a boolean"
                        )

                # Validate num_samples (per-model trials)
                if "num_samples" in model_config:
                    try:
                        num_samples = int(model_config["num_samples"])
                        if num_samples < 5:
                            raise ValueError(
                                f"Ax num_samples for {model_name} must be at least 5"
                            )
                    except (ValueError, TypeError):
                        raise ValueError(
                            f"Ax num_samples for {model_name} must be a valid integer"
                        )

                if "hyperparameters" in model_config:
                    hyperparams = model_config["hyperparameters"]
                    if not isinstance(hyperparams, dict):
                        raise ValueError(
                            f"Ax model_config.hyperparameters for {model_name} must be a dictionary"
                        )
                    # Validate Ax-specific search spaces
                    self._validate_ax_search_spaces(hyperparams, model_name)

        # Validate CPU resource configuration
        if "cpus_per_model_task" in ax_config:
            cpus_per_model = ax_config["cpus_per_model_task"]
            try:
                cpus_per_model = int(cpus_per_model)
            except (ValueError, TypeError):
                raise ValueError(
                    f"ax.cpus_per_model_task must be a valid integer, got: {cpus_per_model}"
                )
            if cpus_per_model < 2:
                raise ValueError(
                    f"ax.cpus_per_model_task must be >= 2, got: {cpus_per_model}"
                )

        if "max_concurrent_trials" in ax_config:
            max_concurrent = ax_config["max_concurrent_trials"]
            try:
                max_concurrent = int(max_concurrent)
            except (ValueError, TypeError):
                raise ValueError(
                    f"ax.max_concurrent_trials must be a valid integer, got: {max_concurrent}"
                )
            if max_concurrent < 1:
                raise ValueError(
                    f"ax.max_concurrent_trials must be >= 1, got: {max_concurrent}"
                )
            
            # Validate relationship: max_concurrent_trials < cpus_per_model_task
            if "cpus_per_model_task" in ax_config:
                cpus_per_model = ax_config["cpus_per_model_task"]
                try:
                    cpus_per_model = int(cpus_per_model)
                except (ValueError, TypeError):
                    cpus_per_model = 0
                if max_concurrent >= cpus_per_model and cpus_per_model > 0:
                    raise ValueError(
                        f"ax.max_concurrent_trials ({max_concurrent}) must be < "
                        f"ax.cpus_per_model_task ({cpus_per_model}). "
                        f"At least 1 CPU must be reserved for Tuner coordination."
                    )
            
            # Ax-specific warning for high concurrency
            if max_concurrent > 3:
                print(f"⚠️  WARNING: ax.max_concurrent_trials={max_concurrent} is higher than recommended")
                print("   💡 Ax uses Bayesian optimization which works best with 2-3 concurrent trials")

        # Support old naming (max_concurrent) for backward compatibility
        if "max_concurrent" in ax_config and "max_concurrent_trials" not in ax_config:
            print("⚠️  WARNING: Using deprecated 'max_concurrent' field. Please use 'max_concurrent_trials' instead.")

        # COMMENTED OUT: Advanced constraint validation (not yet implemented in config-maker)
        # # Validate parameter_constraints if present
        # if "parameter_constraints" in ax_config:
        #     constraints = ax_config["parameter_constraints"]
        #     if not isinstance(constraints, list):
        #         raise ValueError("Ax 'parameter_constraints' must be a list")
        #     for constraint in constraints:
        #         if not isinstance(constraint, str):
        #             raise ValueError("Each Ax parameter constraint must be a string")
        #
        # # Validate outcome_constraints if present
        # if "outcome_constraints" in ax_config:
        #     constraints = ax_config["outcome_constraints"]
        #     if not isinstance(constraints, list):
        #         raise ValueError("Ax 'outcome_constraints' must be a list")
        #     for constraint in constraints:
        #         if not isinstance(constraint, str):
        #             raise ValueError("Each Ax outcome constraint must be a string")

        # Note: Ax resources are handled by Ray automatically
        # No per-strategy resource validation needed

    def _convert_mlp_architectures(self, architectures: List[Any], context: str) -> List[List[int]]:
        """
        Convert MLP hidden_layer_sizes from various formats to standard list format.
        
        Handles:
        - String tuples: "(5, 5)" -> [5, 5]
        - Already lists: [5, 5] -> [5, 5]
        - Tuples: (5, 5) -> [5, 5]
        
        Parameters
        ----------
        architectures : list
            List of architectures in various formats
        context : str
            Context string for error messages (e.g., "Grid Search MLP")
        
        Returns
        -------
        list
            List of architectures as lists of integers
        
        Raises
        ------
        ValueError
            If architecture format is invalid
        """
        import ast
        
        converted = []
        for i, arch in enumerate(architectures):
            try:
                if isinstance(arch, str):
                    # String tuple like "(5, 5)" or "(100,)" 
                    if arch.startswith('(') and arch.endswith(')'):
                        # Parse string tuple to actual tuple
                        parsed = ast.literal_eval(arch)
                        if isinstance(parsed, tuple):
                            arch = list(parsed)
                        elif isinstance(parsed, int):
                            arch = [parsed]
                        else:
                            raise ValueError(f"Unexpected parsed type: {type(parsed)}")
                    else:
                        # Try to parse as a number
                        arch = [int(arch)]
                
                elif isinstance(arch, tuple):
                    # Convert tuple to list
                    arch = list(arch)
                
                elif isinstance(arch, int):
                    # Single neuron layer
                    arch = [arch]
                
                elif isinstance(arch, list):
                    # Already a list - validate it contains only integers
                    if not all(isinstance(x, int) for x in arch):
                        raise ValueError(f"Architecture must contain only integers, got: {arch}")
                
                else:
                    raise ValueError(f"Unexpected architecture type: {type(arch)}")
                
                # Final validation: ensure it's a list of positive integers
                if not isinstance(arch, list) or not arch:
                    raise ValueError(f"Architecture must be a non-empty list")
                
                if not all(isinstance(x, int) and x > 0 for x in arch):
                    raise ValueError(f"Architecture must contain only positive integers")
                
                converted.append(arch)
                
            except Exception as e:
                raise ValueError(
                    f"{context}: Invalid hidden_layer_sizes architecture at index {i}: {arch}. "
                    f"Error: {e}. Expected format: [5, 5] or (5, 5) or '(5, 5)'"
                )
        
        if converted:
            print(f"   ✅ {context}: Converted {len(converted)} MLP architecture(s)")
            for i, arch in enumerate(converted):
                print(f"      • Architecture {i+1}: {arch} (tuple will be: {tuple(arch)})")
        
        return converted
    
    @staticmethod
    def convert_mlp_layers_for_sklearn(hidden_layer_sizes: Union[List[int], Tuple[int], Any]) -> Tuple[int]:
        """
        Convert MLP hidden_layer_sizes to sklearn-compatible tuple format.
        
        This is a centralized conversion method used by both strategies and model_runner
        to ensure consistent MLP layer format conversion.
        
        Parameters
        ----------
        hidden_layer_sizes : list, tuple, str (including JSON), or int
            Layer architecture in various formats:
            - List: [5, 5] or [100]
            - Tuple: (5, 5) - already correct
            - String tuple: "(5, 5)" - will be parsed
            - JSON string: "[5, 5]" - used by Ax encoding (decoded here)
            - Integer: 100 - single layer
        
        Returns
        -------
        tuple
            Sklearn-compatible tuple format, e.g., (5, 5) or (100,)
        
        Examples
        --------
        >>> convert_mlp_layers_for_sklearn([5, 5])
        (5, 5)
        >>> convert_mlp_layers_for_sklearn([100])
        (100,)
        >>> convert_mlp_layers_for_sklearn((5, 5))
        (5, 5)
        >>> convert_mlp_layers_for_sklearn("[5, 5]")  # Ax JSON encoding
        (5, 5)
        """
        import ast
        import json
        
        if isinstance(hidden_layer_sizes, tuple):
            # Already a tuple - return as is
            return hidden_layer_sizes
        
        elif isinstance(hidden_layer_sizes, list):
            # List - convert to tuple
            return tuple(hidden_layer_sizes)
        
        elif isinstance(hidden_layer_sizes, str):
            # 🔧 NEW: JSON string from Ax encoding (e.g., "[5, 5]")
            if hidden_layer_sizes.startswith('[') and hidden_layer_sizes.endswith(']'):
                try:
                    parsed = json.loads(hidden_layer_sizes)
                    if isinstance(parsed, list):
                        return tuple(parsed)
                except json.JSONDecodeError:
                    pass
            
            # String tuple representation like "(5, 5)" - parse it
            if hidden_layer_sizes.startswith('(') and hidden_layer_sizes.endswith(')'):
                parsed = ast.literal_eval(hidden_layer_sizes)
                if isinstance(parsed, tuple):
                    return parsed
                elif isinstance(parsed, int):
                    return (parsed,)
            
            # Try as comma-separated string
            try:
                values = [int(x.strip()) for x in hidden_layer_sizes.split(',')]
                return tuple(values)
            except:
                pass
        
        elif isinstance(hidden_layer_sizes, int):
            # Single integer - create single-layer tuple
            return (hidden_layer_sizes,)
        
        # If we get here, format is unexpected - raise error
        raise ValueError(
            f"Cannot convert hidden_layer_sizes to sklearn format: {hidden_layer_sizes} "
            f"(type: {type(hidden_layer_sizes)}). Expected list, tuple, or parseable string."
        )

    @staticmethod
    def convert_hyperparameter_types(model_name: str, hyperparams: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert hyperparameters from strings to proper types for sklearn models.
        
        This method handles the conversion of string hyperparameters (from YAML config)
        to the proper types expected by sklearn models.
        
        Parameters
        ----------
        model_name : str
            Name of the ML model
        hyperparams : Dict[str, Any]
            Dictionary of hyperparameters (may contain strings)
        
        Returns
        -------
        Dict[str, Any]
            Dictionary with properly typed hyperparameters
        
        Examples
        --------
        >>> convert_hyperparameter_types('KNN', {'n_neighbors': '5', 'weights': 'uniform'})
        {'n_neighbors': 5, 'weights': 'uniform'}
        >>> convert_hyperparameter_types('XGBoost', {'n_estimators': '100', 'max_depth': '6'})
        {'n_estimators': 100, 'max_depth': 6}
        """
        converted_params = {}
        
        for param_name, param_value in hyperparams.items():
            try:
                # Model-specific type conversions
                if model_name == 'KNN':
                    if param_name == 'n_neighbors':
                        converted_params[param_name] = int(param_value)
                    elif param_name in ['weights', 'metric']:
                        # Keep as string for categorical parameters
                        converted_params[param_name] = param_value
                    else:
                        converted_params[param_name] = param_value
                
                elif model_name == 'XGBoost':
                    if param_name in ['n_estimators', 'max_depth', 'min_child_weight', 'reg_alpha', 'reg_lambda']:
                        converted_params[param_name] = int(param_value)
                    elif param_name in ['learning_rate', 'subsample', 'colsample_bytree', 'gamma']:
                        converted_params[param_name] = float(param_value)
                    else:
                        converted_params[param_name] = param_value
                
                elif model_name == 'Random Forest':
                    if param_name in ['n_estimators', 'max_depth', 'min_samples_split', 'min_samples_leaf']:
                        if param_value is None or str(param_value).lower() == 'none':
                            converted_params[param_name] = None
                        else:
                            converted_params[param_name] = int(param_value)
                    elif param_name in ['max_features']:
                        # Handle max_features which can be string, float, or None
                        if param_value is None or str(param_value).lower() == 'none':
                            converted_params[param_name] = None
                        elif str(param_value) in ['sqrt', 'log2']:
                            converted_params[param_name] = param_value  # Keep as string
                        else:
                            converted_params[param_name] = float(param_value)
                    else:
                        converted_params[param_name] = param_value
                
                elif model_name == 'SVM':
                    if param_name == 'C':
                        converted_params[param_name] = float(param_value)
                    elif param_name == 'gamma':
                        if str(param_value).lower() in ['scale', 'auto']:
                            converted_params[param_name] = param_value  # Keep as string
                        else:
                            converted_params[param_name] = float(param_value)
                    elif param_name in ['kernel', 'degree']:
                        if param_name == 'degree':
                            converted_params[param_name] = int(param_value)
                        else:
                            converted_params[param_name] = param_value  # Keep as string
                    else:
                        converted_params[param_name] = param_value
                
                elif model_name == 'MLP (Neural Network)':
                    if param_name == 'hidden_layer_sizes':
                        # Use existing MLP conversion method
                        converted_params[param_name] = UnifiedConfigHandler.convert_mlp_layers_for_sklearn(param_value)
                    elif param_name in ['max_iter', 'early_stopping']:
                        if param_name == 'max_iter':
                            converted_params[param_name] = int(param_value)
                        else:
                            converted_params[param_name] = bool(param_value)
                    elif param_name in ['learning_rate_init', 'alpha', 'beta_1', 'beta_2', 'epsilon']:
                        converted_params[param_name] = float(param_value)
                    else:
                        converted_params[param_name] = param_value
                
                elif model_name == 'Logistic Regression':
                    if param_name == 'C':
                        converted_params[param_name] = float(param_value)
                    elif param_name == 'max_iter':
                        converted_params[param_name] = int(param_value)
                    elif param_name in ['penalty', 'solver']:
                        converted_params[param_name] = param_value  # Keep as string
                    else:
                        converted_params[param_name] = param_value
                
                else:
                    # For other models, try to convert common numeric parameters
                    if param_name in ['n_estimators', 'max_depth', 'min_samples_split', 'min_samples_leaf', 
                                    'max_iter', 'n_neighbors', 'C', 'gamma']:
                        try:
                            if str(param_value).lower() == 'none':
                                converted_params[param_name] = None
                            elif '.' in str(param_value):
                                converted_params[param_name] = float(param_value)
                            else:
                                converted_params[param_name] = int(param_value)
                        except (ValueError, TypeError):
                            converted_params[param_name] = param_value
                    else:
                        converted_params[param_name] = param_value
            
            except (ValueError, TypeError) as e:
                # If conversion fails, keep original value and log warning
                print(f"⚠️  WARNING: Could not convert {param_name}={param_value} for {model_name}: {e}")
                converted_params[param_name] = param_value
        
        return converted_params

    def _validate_ax_search_spaces(self, hyperparams: Dict[str, Any], model_name: str) -> None:
        """Validate Ax search space definitions using Ray Tune syntax."""
        for param_name, param_config in hyperparams.items():
            if not isinstance(param_config, dict):
                raise ValueError(
                    f"Ax hyperparameter '{param_name}' for {model_name} must be a dictionary"
                )
            
            if "type" not in param_config:
                raise ValueError(
                    f"Ax hyperparameter '{param_name}' for {model_name} must include 'type'"
                )
            
            param_type = param_config["type"]
            valid_types = ["uniform", "quniform", "loguniform", "choice"]
            
            if param_type not in valid_types:
                raise ValueError(
                    f"Ax hyperparameter '{param_name}' has invalid type '{param_type}'. "
                    f"Valid types: {valid_types}"
                )
            
            # Validate type-specific requirements
            if param_type in ["uniform", "loguniform"]:
                if "bounds" not in param_config:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' with type '{param_type}' must include 'bounds'"
                    )
                bounds = param_config["bounds"]
                if not isinstance(bounds, list) or len(bounds) != 2:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' bounds must be a list of [low, high]"
                    )
                if bounds[0] >= bounds[1]:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' bounds[0] must be < bounds[1]"
                    )
            
            elif param_type == "quniform":
                if "bounds" not in param_config or "q" not in param_config:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' with type 'quniform' must include 'bounds' and 'q'"
                    )
                bounds = param_config["bounds"]
                if not isinstance(bounds, list) or len(bounds) != 2:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' bounds must be a list of [low, high]"
                    )
                if bounds[0] >= bounds[1]:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' bounds[0] must be < bounds[1]"
                    )
                q = param_config["q"]
                if not isinstance(q, (int, float)) or q <= 0:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' 'q' must be a positive number"
                    )
            
            elif param_type == "choice":
                if "values" not in param_config:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' with type 'choice' must include 'values'"
                    )
                values = param_config["values"]
                if not isinstance(values, list) or len(values) == 0:
                    raise ValueError(
                        f"Ax hyperparameter '{param_name}' 'values' must be a non-empty list"
                    )
                
                # 🔧 FIX: Convert MLP hidden_layer_sizes in choice values
                if model_name == "MLP (Neural Network)" and param_name == "hidden_layer_sizes":
                    # Convert to lists (validation only - no tuple conversion)
                    # Ax search strategy will handle JSON encoding for tune.choice()
                    architectures_as_lists = self._convert_mlp_architectures(
                        values, 
                        f"Ax {model_name}"
                    )
                    # Keep as lists in config (will be JSON-encoded later in ax_search_strategy.py)
                    param_config["values"] = architectures_as_lists
                    print(f"   ✅ Ax {model_name}: Validated MLP architectures (will be JSON-encoded for Ax)")

    def _validate_ray_resource_utilization(self, ray_config: Dict[str, Any]) -> None:
        """
        Validate Ray resource utilization across all strategies.
        Ensures total strategy resources don't exceed global resources.
        """
        resources = ray_config.get("resources", {})
        global_cpus = resources.get("num_cpus", 0)
        
        # Convert to int if it's a string
        try:
            global_cpus = int(global_cpus)
        except (ValueError, TypeError):
            return  # Skip validation if can't convert to int
        
        if global_cpus <= 0:
            return  # Skip validation if no global resources configured
        
        total_strategy_cpus = 0
        strategy_details = []
        
        # Calculate Grid Search resource usage
        if "grid_search" in ray_config:
            grid_config = ray_config["grid_search"]
            grid_cpus = grid_config.get("cpus_per_model_task", 0)
            try:
                grid_cpus = int(grid_cpus)
            except (ValueError, TypeError):
                grid_cpus = 0
            
            grid_models = len(grid_config.get("models", []))
            grid_total = grid_cpus * grid_models
            total_strategy_cpus += grid_total
            if grid_total > 0:
                strategy_details.append(f"Grid Search: {grid_models} models × {grid_cpus} CPUs = {grid_total} CPUs")
        
        # Calculate Ax resource usage
        if "ax" in ray_config:
            ax_config = ray_config["ax"]
            ax_cpus = ax_config.get("cpus_per_model_task", 0)
            try:
                ax_cpus = int(ax_cpus)
            except (ValueError, TypeError):
                ax_cpus = 0
            
            ax_models = len(ax_config.get("models", []))
            ax_total = ax_cpus * ax_models
            total_strategy_cpus += ax_total
            if ax_total > 0:
                strategy_details.append(f"Ax Search: {ax_models} models × {ax_cpus} CPUs = {ax_total} CPUs")
        
        # Validate total resource usage
        if total_strategy_cpus > global_cpus:
            raise ValueError(
                f"❌ Resource validation failed: Total strategy CPUs ({total_strategy_cpus}) "
                f"exceeds global resources ({global_cpus}). "
                f"Strategy details: {'; '.join(strategy_details)}. "
                f"Please reduce cpus_per_model_task or increase global num_cpus."
            )
        
        # Calculate and report utilization
        utilization_percent = (total_strategy_cpus / global_cpus) * 100 if global_cpus > 0 else 0
        
        if utilization_percent > 95:
            print(f"⚠️  WARNING: Very high resource utilization ({utilization_percent:.1f}%)")
            print("   💡 Consider reducing cpus_per_model_task or adding more global CPUs")
        elif utilization_percent < 50:
            print(f"💡 INFO: Low resource utilization ({utilization_percent:.1f}%)")
            print("   💡 You could increase cpus_per_model_task for better performance")
        else:
            print(f"✅ Good resource utilization ({utilization_percent:.1f}%)")
        
        print(f"   📊 Resource Summary: {total_strategy_cpus}/{global_cpus} CPUs used")
        if strategy_details:
            for detail in strategy_details:
                print(f"      • {detail}")

    def _validate_ray_common_config(self, ray_config: Dict[str, Any]) -> None:
        """Validate common Ray configuration shared across strategies."""
        # Validate metric and mode
        if "metric" in ray_config:
            metric = ray_config["metric"]
            valid_metrics = ["accuracy", "f1", "precision", "recall", "auc", "mse", "mae", "r2"]
            if metric not in valid_metrics:
                raise ValueError(
                    f"Ray 'metric' must be one of {valid_metrics}, got '{metric}'"
                )

        if "mode" in ray_config:
            mode = ray_config["mode"]
            if mode not in ["max", "min"]:
                raise ValueError("Ray 'mode' must be either 'max' or 'min'")

        # Validate random_state
        if "random_state" in ray_config:
            try:
                int(ray_config["random_state"])
            except (ValueError, TypeError):
                raise ValueError("Ray 'random_state' must be a valid integer")

        # Validate global Ray resources if present
        if "resources" in ray_config:
            resources = ray_config["resources"]
            if not isinstance(resources, dict):
                raise ValueError("Ray 'resources' must be a dictionary")

            # Validate required resource fields
            if "num_cpus" in resources:
                try:
                    cpus = int(resources["num_cpus"])
                    if cpus < 1:
                        raise ValueError("Ray resources 'num_cpus' must be positive")
                except (ValueError, TypeError):
                    raise ValueError("Ray resources 'num_cpus' must be a valid integer")

            if "memory_gb" in resources:
                try:
                    mem = int(resources["memory_gb"])
                    if mem < 1:
                        raise ValueError("Ray resources 'memory_gb' must be positive")
                except (ValueError, TypeError):
                    raise ValueError("Ray resources 'memory_gb' must be a valid integer")

            if "object_store_memory_gb" in resources:
                try:
                    obj_mem = int(resources["object_store_memory_gb"])
                    if obj_mem < 1:
                        raise ValueError("Ray resources 'object_store_memory_gb' must be positive")
                except (ValueError, TypeError):
                    raise ValueError("Ray resources 'object_store_memory_gb' must be a valid integer")

            if "num_gpus" in resources:
                try:
                    gpus = int(resources["num_gpus"])
                    if gpus < 0:
                        raise ValueError("Ray resources 'num_gpus' must be non-negative")
                except (ValueError, TypeError):
                    raise ValueError("Ray resources 'num_gpus' must be a valid integer")
            
            # NEW: Validate resource utilization across strategies
            self._validate_ray_resource_utilization(ray_config)

        # Validate graph data visualization configuration
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
    def expose_ports(self) -> bool:
        """Get port exposure setting."""
        return self.raw_config.get("project", {}).get("expose_ports", "No") == "Yes"

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

    # Ray Properties - NEW NESTED STRUCTURE
    
    # Common Ray Properties
    @property
    def search_strategies(self) -> List[str]:
        """Get list of enabled search strategies."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("search_strategies", [])
    
    @property
    def uses_grid_search(self) -> bool:
        """Check if Grid Search strategy is enabled."""
        return "grid_search" in self.search_strategies
    
    @property
    def uses_ax(self) -> bool:
        """Check if Ax strategy is enabled."""
        return "ax" in self.search_strategies

    @property
    def optimization_metric(self) -> str:
        """Get the optimization metric from Ray configuration (common)."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("metric", "accuracy")

    @property
    def optimization_mode(self) -> str:
        """Get the optimization mode from Ray configuration (common)."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("mode", "max")

    @property
    def random_state(self) -> int:
        """Get random state from Ray configuration (common)."""
        ray_config = self.raw_config.get("ray", {})
        return int(ray_config.get("random_state", self.global_random_seed))

    # Grid Search Properties
    @property
    def grid_search_config(self) -> Dict[str, Any]:
        """Get Grid Search configuration."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("grid_search", {})

    @property
    def grid_search_models(self) -> List[str]:
        """Get selected models for Grid Search."""
        return self.grid_search_config.get("models", [])

    @property
    def grid_search_model_configs(self) -> Dict[str, Any]:
        """Get model configurations for Grid Search."""
        return self.grid_search_config.get("model_configs", {})
    
    @property
    def grid_search_max_concurrent(self) -> int:
        """Get maximum concurrent trials for Grid Search."""
        return int(self.grid_search_config.get("max_concurrent", 2))
    
    @property
    def grid_search_cv_folds(self) -> int:
        """Get number of CV folds for Grid Search."""
        return int(self.grid_search_config.get("cv_folds", 5))
    
    # Note: Grid Search resources removed - Ray handles resource allocation automatically

    # Ax Properties
    @property
    def ax_config(self) -> Dict[str, Any]:
        """Get Ax configuration."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("ax", {})
    
    @property
    def ax_models(self) -> List[str]:
        """Get selected models for Ax."""
        return self.ax_config.get("models", [])
    
    @property
    def ax_model_configs(self) -> Dict[str, Any]:
        """Get model configurations for Ax."""
        return self.ax_config.get("model_configs", {})
    
    @property
    def ax_max_concurrent(self) -> int:
        """Get maximum concurrent trials for Ax."""
        return int(self.ax_config.get("max_concurrent", 4))
    
    @property
    def ax_cv_folds(self) -> int:
        """Get number of CV folds for Ax."""
        return int(self.ax_config.get("cv_folds", 5))
    
    # Note: Ax resources removed - Ray handles resource allocation automatically
    # Note: ax_total_trials is now per-model, access via ax_model_configs[model_name]["num_samples"]
    # Note: Ax constraints commented out for now (can be added later)

    # Per-Strategy CPU Resource Properties
    @property
    def grid_search_cpus_per_model_task(self) -> int:
        """Get CPU budget per model task for Grid Search."""
        return int(self.grid_search_config.get("cpus_per_model_task", 4))

    @property
    def grid_search_max_concurrent_trials(self) -> int:
        """Get maximum concurrent trials for Grid Search (renamed from max_concurrent)."""
        # Support both old and new naming for backward compatibility
        return int(
            self.grid_search_config.get(
                "max_concurrent_trials",
                self.grid_search_config.get("max_concurrent", 2)
            )
        )

    @property
    def ax_cpus_per_model_task(self) -> int:
        """Get CPU budget per model task for Ax."""
        return int(self.ax_config.get("cpus_per_model_task", 4))

    @property
    def ax_max_concurrent_trials(self) -> int:
        """Get maximum concurrent trials for Ax (renamed from max_concurrent)."""
        # Support both old and new naming for backward compatibility
        return int(
            self.ax_config.get(
                "max_concurrent_trials",
                self.ax_config.get("max_concurrent", 3)
            )
        )

    # Backward Compatibility: selected_models now returns models from all strategies
    @property
    def selected_models(self) -> List[str]:
        """Get selected ML models from all enabled strategies (combined)."""
        all_models = []
        if self.uses_grid_search:
            all_models.extend(self.grid_search_models)
        if self.uses_ax:
            all_models.extend(self.ax_models)
        # Remove duplicates while preserving order
        seen = set()
        unique_models = []
        for model in all_models:
            if model not in seen:
                seen.add(model)
                unique_models.append(model)
        return unique_models

    # Deprecated/Legacy properties (kept for backward compatibility)
    @property
    def num_trials(self) -> int:
        """DEPRECATED: Get number of trials (returns Grid Search max_concurrent if Grid Search enabled)."""
        if self.uses_grid_search:
            return self.grid_search_max_concurrent
        return 10
    
    @property
    def max_concurrent_trials(self) -> int:
        """DEPRECATED: Get maximum concurrent trials (returns first available strategy's value)."""
        if self.uses_grid_search:
            return self.grid_search_max_concurrent
        elif self.uses_ax:
            return self.ax_max_concurrent
        return 2
    
    @property
    def cv_folds(self) -> int:
        """DEPRECATED: Get number of CV folds (returns first available strategy's value)."""
        if self.uses_grid_search:
            return self.grid_search_cv_folds
        elif self.uses_ax:
            return self.ax_cv_folds
        return 5

    @property
    def ray_resources(self) -> Optional[Dict[str, Any]]:
        """Get Ray resource configuration (global)."""
        ray_config = self.raw_config.get("ray", {})
        return ray_config.get("resources")

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
    
    # NEW: Resource Management Properties
    @property
    def ray_global_cpus(self) -> int:
        """Get total global CPUs for Ray cluster (building capacity)."""
        resources = self.ray_resources_config
        if resources:
            return int(resources.get("num_cpus", 4))
        return 4
    
    @property
    def ray_total_strategy_cpus(self) -> int:
        """Get total CPUs used by all strategies combined."""
        total_cpus = 0
        
        # Grid Search CPUs
        if self.uses_grid_search:
            grid_models = len(self.grid_search_models)
            grid_cpus_per_model = self.grid_search_cpus_per_model_task
            total_cpus += grid_models * grid_cpus_per_model
        
        # Ax Search CPUs
        if self.uses_ax:
            ax_models = len(self.ax_models)
            ax_cpus_per_model = self.ax_cpus_per_model_task
            total_cpus += ax_models * ax_cpus_per_model
        
        return total_cpus
    
    @property
    def ray_resource_utilization_percent(self) -> float:
        """Get resource utilization percentage."""
        global_cpus = self.ray_global_cpus
        if global_cpus <= 0:
            return 0.0
        return (self.ray_total_strategy_cpus / global_cpus) * 100
    
    @property
    def ray_remaining_cpus(self) -> int:
        """Get remaining CPUs after strategy allocation."""
        return self.ray_global_cpus - self.ray_total_strategy_cpus
    
    @property
    def ray_resource_efficiency_rating(self) -> str:
        """Get resource efficiency rating."""
        utilization = self.ray_resource_utilization_percent
        if utilization > 95:
            return "Very High"
        elif utilization >= 70:
            return "High"
        elif utilization >= 50:
            return "Good"
        else:
            return "Low"
    
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
            
            # Show Ray resource management if configured
            if self.has_ray_resources:
                print(f"\n🏢 Ray Resource Management:")
                print(f"   📊 Global Building Capacity: {self.ray_global_cpus} CPUs")
                print(f"   📈 Strategy Resource Usage: {self.ray_total_strategy_cpus} CPUs")
                print(f"   📊 Utilization: {self.ray_resource_utilization_percent:.1f}%")
                print(f"   🔄 Remaining CPUs: {self.ray_remaining_cpus}")
                print(f"   ⭐ Efficiency Rating: {self.ray_resource_efficiency_rating}")
                
                # Show per-strategy details
                if self.uses_grid_search:
                    grid_models = len(self.grid_search_models)
                    grid_cpus = self.grid_search_cpus_per_model_task
                    print(f"   🔍 Grid Search: {grid_models} models × {grid_cpus} CPUs = {grid_models * grid_cpus} CPUs")
                
                if self.uses_ax:
                    ax_models = len(self.ax_models)
                    ax_cpus = self.ax_cpus_per_model_task
                    print(f"   🎯 Ax Search: {ax_models} models × {ax_cpus} CPUs = {ax_models * ax_cpus} CPUs")
        
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
