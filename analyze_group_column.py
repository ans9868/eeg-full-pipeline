#!/usr/bin/env python3
"""
Focused analysis of the Group column in the parquet files.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct, when, sum as spark_sum
from pyspark.sql.types import StringType
import sys
import os

def analyze_group_column(parquet_path):
    """Detailed analysis of the Group column."""
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("GroupColumnAnalyzer") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    try:
        print(f"🔍 Analyzing Group column in: {parquet_path}")
        print("=" * 60)
        
        # Read the parquet files
        df = spark.read.parquet(parquet_path)
        
        # Basic Group column information
        print("📊 GROUP COLUMN ANALYSIS")
        print("-" * 30)
        
        # Total count
        total_rows = df.count()
        print(f"Total rows: {total_rows}")
        
        # Group column statistics
        print(f"\n📋 Group column info:")
        print(f"  - Data type: {df.schema['Group'].dataType}")
        print(f"  - Null values: {df.filter(col('Group').isNull()).count()}")
        
        # Unique values and counts
        print(f"\n🎯 Unique Group values:")
        group_counts = df.groupBy("Group").count().orderBy("count", ascending=False)
        group_counts.show(truncate=False)
        
        # Convert to Pandas for easier analysis
        group_counts_pd = group_counts.toPandas()
        
        # Calculate percentages
        print(f"\n📈 Group distribution (percentages):")
        for _, row in group_counts_pd.iterrows():
            percentage = (row['count'] / total_rows) * 100
            print(f"  {row['Group']}: {row['count']} rows ({percentage:.2f}%)")
        
        # Group by Subject and Group to see subject-level distribution
        print(f"\n👥 Subject-Group distribution:")
        subject_group_counts = df.groupBy("SubjectID", "Group").count().orderBy("SubjectID", "Group")
        subject_group_counts.show(truncate=False)
        
        # Convert to Pandas for analysis
        subject_group_pd = subject_group_counts.toPandas()
        
        # Analyze each subject's group distribution
        print(f"\n🔍 Per-subject Group analysis:")
        for subject in sorted(df.select("SubjectID").distinct().rdd.map(lambda row: row[0]).collect()):
            subject_data = subject_group_pd[subject_group_pd['SubjectID'] == subject]
            print(f"\n  Subject {subject}:")
            for _, row in subject_data.iterrows():
                percentage = (row['count'] / subject_data['count'].sum()) * 100
                print(f"    {row['Group']}: {row['count']} epochs ({percentage:.1f}%)")
        
        # Check for any subjects with mixed groups
        print(f"\n🔀 Mixed Group Analysis:")
        subjects_with_multiple_groups = df.groupBy("SubjectID").agg(countDistinct("Group").alias("group_count")).filter(col("group_count") > 1)
        mixed_subjects = subjects_with_multiple_groups.collect()
        
        if mixed_subjects:
            print(f"  Found {len(mixed_subjects)} subjects with multiple groups:")
            for row in mixed_subjects:
                print(f"    {row['SubjectID']}: {row['group_count']} different groups")
        else:
            print("  ✅ All subjects belong to only one group")
        
        # Group by EpochID and Group to see epoch-level distribution
        print(f"\n⏱️  Epoch-Group distribution (first 20 epochs):")
        epoch_group_counts = df.groupBy("EpochID", "Group").count().orderBy("EpochID").limit(20)
        epoch_group_counts.show(truncate=False)
        
        # Summary statistics
        print(f"\n📊 Summary:")
        print(f"  - Total unique groups: {df.select('Group').distinct().count()}")
        print(f"  - Total subjects: {df.select('SubjectID').distinct().count()}")
        print(f"  - Total epochs: {df.select('EpochID').distinct().count()}")
        
        # Check if groups are balanced
        group_balance = group_counts_pd['count'].values
        if len(group_balance) == 2:
            balance_ratio = min(group_balance) / max(group_balance)
            print(f"  - Group balance ratio: {balance_ratio:.3f} (1.0 = perfectly balanced)")
            if balance_ratio > 0.8:
                print("    ✅ Groups are well balanced")
            elif balance_ratio > 0.6:
                print("    ⚠️  Groups are moderately balanced")
            else:
                print("    ❌ Groups are imbalanced")
        
        # Show some sample data grouped by Group
        print(f"\n📝 Sample data by Group:")
        for group in df.select("Group").distinct().rdd.map(lambda row: row[0]).collect():
            print(f"\n  Group '{group}' samples:")
            sample_data = df.filter(col("Group") == group).select("SubjectID", "EpochID", "Group", "label").limit(3)
            sample_data.show(truncate=False)
        
    except Exception as e:
        print(f"❌ Error analyzing Group column: {e}")
        return False
    
    finally:
        spark.stop()
    
    return True

def main():
    """Main function to run the Group column analysis."""
    
    # Default path from the terminal selection
    default_path = "/Users/user/projects/eeg-full-pipeline/data/fingerPrintAllTogether/processed_subjects"
    
    # Use command line argument if provided, otherwise use default
    if len(sys.argv) > 1:
        parquet_path = sys.argv[1]
    else:
        parquet_path = default_path
    
    # Check if path exists
    if not os.path.exists(parquet_path):
        print(f"❌ Path does not exist: {parquet_path}")
        return
    
    # Run analysis
    success = analyze_group_column(parquet_path)
    
    if success:
        print("\n✅ Group column analysis completed successfully!")
    else:
        print("\n❌ Group column analysis failed!")

if __name__ == "__main__":
    main()
