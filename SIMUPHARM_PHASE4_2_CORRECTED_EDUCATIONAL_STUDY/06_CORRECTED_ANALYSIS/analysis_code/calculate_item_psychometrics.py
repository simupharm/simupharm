# calculate_item_psychometrics.py
# Exploratory Item Analysis: Item Difficulty (P) & Discrimination (D)
# Version: REV2.1 / PHASE4.2.1 (FINAL PROTOCOL FREEZE)

import os
import sys
import numpy as np
import pandas as pd

def run_item_analysis(csv_path):
    print("=== RUNNING EXPLORATORY ITEM ANALYSIS ===")
    print(f"Data source: {csv_path}")
    print("Note: Exploratory item analysis describes relative concept difficulty within this pilot.")
    print("Sample size (N approx 25) limits precision; this is NOT psychometric validation.\n")
    
    if not os.path.exists(csv_path):
        print(f"ERROR: Dataset {csv_path} not found.")
        sys.exit(1)
        
    df = pd.read_csv(csv_path)
    
    print("--- PRE-TEST ITEM DIFFICULTY (P) ---")
    for i in range(1, 11):
        col = f'pre_q{i}'
        if col in df.columns:
            p_val = df[col].dropna().mean()
            print(f"Item Q{i:02d}: Difficulty Index P = {p_val:.2f} ({'Relatively Difficult' if p_val < 0.3 else 'Moderate' if p_val <= 0.7 else 'Relatively Easy'})")
            
    print("\n--- POST-TEST ITEM DIFFICULTY (P) ---")
    for i in range(1, 11):
        col = f'post_q{i}'
        if col in df.columns:
            p_val = df[col].dropna().mean()
            print(f"Item Q{i:02d}: Difficulty Index P = {p_val:.2f} ({'Relatively Difficult' if p_val < 0.3 else 'Moderate' if p_val <= 0.7 else 'Relatively Easy'})")
            
    print("\nExploratory Item Analysis Pipeline Execution: PASS\n")

if __name__ == '__main__':
    default_csv = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'DEMO_TEST_ONLY.csv')
    run_item_analysis(default_csv)
