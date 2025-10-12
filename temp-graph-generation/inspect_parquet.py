#!/usr/bin/env python3
"""
Simple Spark script to inspect parquet files and check column values.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, min as spark_min, max as spark_max, mean, stddev
import sys
import os

def inspect_parquet_files(parquet_path):
    """Inspect parquet files and display column information."""
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("ParquetInspector") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    try:
        print(f"🔍 Inspecting parquet files in: {parquet_path}")
        print("=" * 60)
        
        # Read the parquet files
        df = spark.read.parquet(parquet_path)
        
        # Basic information
        print(f"📊 Total number of rows: {df.count()}")
        print(f"📋 Number of columns: {len(df.columns)}")
        print(f"📝 Column names: {df.columns}")
        print()
        
        # Show schema
        print("🏗️  Schema:")
        df.printSchema()
        print()
        
        # Show first few rows
        print("👀 First 5 rows:")
        df.show(5, truncate=False)
        print()
        
        # Show sample of data
        print("🎲 Sample of 10 rows:")
        df.sample(0.1).show(10, truncate=False)
        print()
        
        # Basic statistics for numeric columns
        print("📈 Basic Statistics for Numeric Columns:")
        numeric_cols = [field.name for field in df.schema.fields 
                       if field.dataType.typeName() in ['integer', 'long', 'float', 'double']]
        
        if numeric_cols:
            df.select(*[col(c) for c in numeric_cols]).describe().show()
        else:
            print("No numeric columns found.")
        print()
        
        # Check for null values
        print("❓ Null value counts:")
        null_counts = []
        for col_name in df.columns:
            null_count = df.filter(col(col_name).isNull()).count()
            null_counts.append((col_name, null_count))
        
        for col_name, null_count in null_counts:
            if null_count > 0:
                print(f"  {col_name}: {null_count} nulls")
            else:
                print(f"  {col_name}: No nulls")
        print()
        
        # Check unique values for string columns
        print("🔤 Unique values for String/Categorical columns:")
        string_cols = [field.name for field in df.schema.fields 
                      if field.dataType.typeName() in ['string']]
        
        for col_name in string_cols[:5]:  # Limit to first 5 string columns
            unique_count = df.select(col_name).distinct().count()
            print(f"  {col_name}: {unique_count} unique values")
            
            if unique_count <= 20:  # Show values if not too many
                unique_values = df.select(col_name).distinct().rdd.map(lambda row: row[0]).collect()
                print(f"    Values: {sorted(unique_values)}")
        print()
        
        # Check data types
        print("🏷️  Data Types:")
        for field in df.schema.fields:
            print(f"  {field.name}: {field.dataType}")
        print()
        
    except Exception as e:
        print(f"❌ Error reading parquet files: {e}")
        return False
    
    finally:
        spark.stop()
    
    return True

def main():
    """Main function to run the inspection."""
    
    # Default path from the terminal selection
    # default_path = "/Users/user/projects/eeg-full-pipeline/data/fingerPrintAllTogether/processed_subjects"
    # default_path = "/Users/user/projects/eeg-full-pipeline/data/fingerPrintAllTogether/transformed/all_data_together/test_data/part-00000-a593ac4d-7a09-40ee-b6a5-5de9befd4e03-c000.snappy.parquet"
    default_path = "/Users/user/projects/eeg-full-pipeline/data/fingerPrintAllTogether/ml_results/KNN/KNN_0_0686/test_predictions.parquet"
    # Use command line argument if provided, otherwise use default
    if len(sys.argv) > 1:
        parquet_path = sys.argv[1]
    else:
        parquet_path = default_path
    
    # Check if path exists
    if not os.path.exists(parquet_path):
        print(f"❌ Path does not exist: {parquet_path}")
        return
    
    # Run inspection
    success = inspect_parquet_files(parquet_path)
    
    if success:
        print("✅ Inspection completed successfully!")
    else:
        print("❌ Inspection failed!")

if __name__ == "__main__":
    main()
