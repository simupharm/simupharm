# calculate_hake_gain.py
# Normalized Learning Gain (Hake 1998) Analysis Pipeline
# Version: REV2 / PHASE4.2

import os
import sys
import numpy as np
import pandas as pd

def run_hake_analysis(csv_path):
    print(f"=== RUNNING HAKE NORMALIZED GAIN ANALYSIS PIPELINE ===")
    print(f"Data source: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"ERROR: Dataset {csv_path} not found.")
        sys.exit(1)
        
    df = pd.read_csv(csv_path)
    valid_mask = df['pre_test_total'].notna() & df['post_test_total'].notna()
    df_valid = df[valid_mask].copy()
    
    pre = df_valid['pre_test_total'].astype(float).values
    post = df_valid['post_test_total'].astype(float).values
    
    # 1. Cohort Average Normalized Gain: <g> = (post_mean - pre_mean) / (10 - pre_mean)
    pre_mean = float(np.mean(pre))
    post_mean = float(np.mean(post))
    
    if pre_mean < 10.0:
        cohort_gain = (post_mean - pre_mean) / (10.0 - pre_mean)
    else:
        cohort_gain = np.nan
        
    # 2. Individual Normalized Gains: g_i = (post - pre) / (10 - pre)
    indiv_gains = []
    for pr, po in zip(pre, post):
        if pr == 10.0:
            indiv_gains.append(np.nan)  # Ceiling effect handling
        else:
            indiv_gains.append((po - pr) / (10.0 - pr))
            
    df_valid['indiv_gain'] = indiv_gains
    valid_indiv = df_valid['indiv_gain'].dropna().values
    
    # Classification based on Hake (1998)
    if cohort_gain >= 0.70:
        hake_class = "High Normalized Gain (g >= 0.70)"
    elif cohort_gain >= 0.30:
        hake_class = "Medium Normalized Gain (0.30 <= g < 0.70)"
    else:
        hake_class = "Low Normalized Gain (g < 0.30)"
        
    print(f"Cohort Average Pre-Test: {pre_mean:.2f} / 10.0")
    print(f"Cohort Average Post-Test: {post_mean:.2f} / 10.0")
    print(f"Overall Cohort Normalized Gain <g>: {cohort_gain:.3f}")
    print(f"Hake Gain Classification: {hake_class}")
    if len(valid_indiv) > 0:
        print(f"Mean Individual Normalized Gain: {np.mean(valid_indiv):.3f} (SD: {np.std(valid_indiv, ddof=1):.3f})")
    print(f"Pipeline Execution Status: PASS\n")

if __name__ == '__main__':
    default_csv = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'DEMO_TEST_ONLY.csv')
    run_hake_analysis(default_csv)
