#!/usr/bin/env python3
import pandas as pd
import os

print("Testing CSV reading...")

try:
    df = pd.read_csv('analysis_1/ANOVA_L_6_Random_per_subject_summary.csv')
    print(f"Successfully loaded {len(df)} rows")
    print("First few rows:")
    print(df.head())
except Exception as e:
    print(f"Error: {e}")

print("Test complete")





