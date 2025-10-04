#!/usr/bin/env python3
"""
Debug script to test the pipeline transformations with extensive logging.
"""

import sys
import os
sys.path.append('eeg-pyspark-pipeline')

from eeg_spark_etl.features.transformers.pipeline_transformer import FeaturePipeline, TrainTestSplitManager
from config_handler import UnifiedConfigHandler
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, rand
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.ml.linalg import Vectors, VectorUDT
import yaml

def create_test_data(spark):
    """Create test data with multiple subjects and epochs."""
    print("🔍 DEBUG - Creating test data...")
    
    # Create test data with 3 subjects, 10 epochs each
    data = []
    for subject_id in range(1, 4):  # Subjects 1, 2, 3
        for epoch_id in range(1, 11):  # Epochs 1-10
            # Create a simple feature vector with 5 features
            features = Vectors.dense([1.0, 2.0, 3.0, 4.0, 5.0])
            data.append((f"subject_{subject_id}", epoch_id, features))
    
    schema = StructType([
        StructField("SubjectID", StringType(), True),
        StructField("EpochID", IntegerType(), True),
        StructField("features", VectorUDT(), True)
    ])
    
    df = spark.createDataFrame(data, schema)
    print(f"🔍 DEBUG - Created test data with {df.count()} rows")
    print(f"🔍 DEBUG - Subjects: {df.select('SubjectID').distinct().count()}")
    print(f"🔍 DEBUG - Epochs per subject: {df.groupBy('SubjectID').count().collect()}")
    
    return df

def test_within_subject_strategy(spark, test_data):
    """Test the within-subject strategy."""
    print("\n" + "="*80)
    print("🎯 TESTING WITHIN-SUBJECT STRATEGY")
    print("="*80)
    
    # Load config for within-subject strategy
    config = UnifiedConfigHandler("debug_config_within.yaml")
    split_manager = TrainTestSplitManager(config)
    
    # Create pipeline with dummy transformer
    pipeline = FeaturePipeline(config, split_manager)
    
    # Test fit_transform
    print("\n🔍 DEBUG - Testing fit_transform...")
    train_df, test_df = pipeline.fit_transform(test_data)
    
    print(f"\n🔍 DEBUG - Final results:")
    print(f"   Train rows: {train_df.count()}")
    print(f"   Test rows: {test_df.count()}")
    
    return train_df, test_df

def test_all_together_strategy(spark, test_data):
    """Test the transform-all-together strategy."""
    print("\n" + "="*80)
    print("🎯 TESTING TRANSFORM-ALL-TOGETHER STRATEGY")
    print("="*80)
    
    # Create config for transform-all-together strategy
    config_dict = {
        'data_leakage_prevention': {
            'strategy': 'transform_all_together'
        },
        'intra_test_train_split': {
            'train_ratio': 0.8,
            'split_method': 'start',  # Use start method for deterministic results
            'split_seed': 42
        },
        'feature_transformation': {
            'transformations': ['Dummy (+1)']
        },
        'output_format': 'ml'
    }
    
    config = UnifiedConfigHandler(config_dict)
    split_manager = TrainTestSplitManager(config)
    
    # Create pipeline with dummy transformer
    pipeline = FeaturePipeline(config, split_manager)
    
    # Test fit_transform
    print("\n🔍 DEBUG - Testing fit_transform...")
    train_df, test_df = pipeline.fit_transform(test_data)
    
    print(f"\n🔍 DEBUG - Final results:")
    print(f"   Train rows: {train_df.count()}")
    print(f"   Test rows: {test_df.count()}")
    
    return train_df, test_df

def main():
    """Main function to run the debug tests."""
    print("🔍 DEBUG - Starting pipeline debug test...")
    
    # Create Spark session
    print("🔍 DEBUG - Creating Spark session...")
    spark = SparkSession.builder \
        .appName("PipelineDebugTest") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "false") \
        .getOrCreate()
    print("🔍 DEBUG - Spark session created successfully")
    
    try:
        # Create test data
        test_data = create_test_data(spark)
        
        # Test both strategies
        within_train, within_test = test_within_subject_strategy(spark, test_data)
        all_together_train, all_together_test = test_all_together_strategy(spark, test_data)
        
        print("\n" + "="*80)
        print("🔍 DEBUG - COMPARISON SUMMARY")
        print("="*80)
        print(f"Within-subject strategy:")
        print(f"   Train: {within_train.count()} rows")
        print(f"   Test: {within_test.count()} rows")
        print(f"Transform-all-together strategy:")
        print(f"   Train: {all_together_train.count()} rows")
        print(f"   Test: {all_together_test.count()} rows")
        
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
