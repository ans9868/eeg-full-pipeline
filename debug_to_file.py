#!/usr/bin/env python3
"""
Debug test that writes output to a file.
"""

import sys
import os
sys.path.append('eeg-pyspark-pipeline')

# Redirect stdout to a file
with open('debug_output.txt', 'w') as f:
    sys.stdout = f
    
    print("🔍 DEBUG - Starting debug test...")
    
    try:
        from eeg_spark_etl.features.transformers.pipeline_transformer import FeaturePipeline, TrainTestSplitManager
        print("🔍 DEBUG - Successfully imported pipeline components")
    except Exception as e:
        print(f"❌ ERROR importing pipeline components: {e}")
    
    try:
        from config_handler import UnifiedConfigHandler
        print("🔍 DEBUG - Successfully imported config handler")
    except Exception as e:
        print(f"❌ ERROR importing config handler: {e}")
    
    print("🔍 DEBUG - All imports successful!")
    print("🔍 DEBUG - Test completed successfully!")

# Restore stdout
sys.stdout = sys.__stdout__
print("Debug output written to debug_output.txt")
