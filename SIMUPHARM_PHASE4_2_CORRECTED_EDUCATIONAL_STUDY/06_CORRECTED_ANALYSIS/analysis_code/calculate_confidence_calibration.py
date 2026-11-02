# calculate_confidence_calibration.py
# Exploratory Analysis: Association Between Diagnostic Confidence and Accuracy
# Version: REV2.1 / PHASE4.2.1 (FINAL PROTOCOL FREEZE)

import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

def run_calibration_analysis(csv_path):
    print("=== RUNNING EXPLORATORY CONFIDENCE-ACCURACY ASSOCIATION ANALYSIS ===")
    print(f"Data source: {csv_path}")
    print("Note: This analysis explores the association between diagnostic confidence and accuracy")
    print("as an exploratory indicator of confidence-performance calibration. Zero causal claims are made.\n")
    
    if not os.path.exists(csv_path):
        print(f"ERROR: Dataset {csv_path} not found.")
        sys.exit(1)
        
    df = pd.read_csv(csv_path)
    
    # Calculate mean confidence across 4 scenarios
    conf_cols = ['task_alpha_conf', 'task_beta_conf', 'task_gamma_conf', 'task_delta_conf']
    df['mean_conf'] = df[conf_cols].mean(axis=1)
    
    # Rubric total (0 to 24 points)
    valid_mask = df['mean_conf'].notna() & df['task_rubric_grand_total'].notna()
    df_valid = df[valid_mask].copy()
    
    conf = df_valid['mean_conf'].values
    score = df_valid['task_rubric_grand_total'].values
    n = len(conf)
    
    if n < 4:
        print("ERROR: Insufficient data points for correlation.")
        return
        
    r_pearson, p_pearson = stats.pearsonr(conf, score)
    rho_spearman, p_spearman = stats.spearmanr(conf, score)
    
    print(f"Valid Paired Observations (N): {n}")
    print(f"Mean Subjective Confidence (1-5): {np.mean(conf):.2f} (SD: {np.std(conf, ddof=1):.2f})")
    print(f"Mean Practical Rubric Total (0-24): {np.mean(score):.2f} (SD: {np.std(score, ddof=1):.2f})")
    print(f"Spearman Rank Correlation (rho): {rho_spearman:.3f}, p = {p_spearman:.4f}")
    print(f"Pearson Correlation (r): {r_pearson:.3f}, p = {p_pearson:.4f}")
    print("Exploratory Indicator Status: Association evaluated descriptively (Exploratory)\n")

if __name__ == '__main__':
    default_csv = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'DEMO_TEST_ONLY.csv')
    run_calibration_analysis(default_csv)
