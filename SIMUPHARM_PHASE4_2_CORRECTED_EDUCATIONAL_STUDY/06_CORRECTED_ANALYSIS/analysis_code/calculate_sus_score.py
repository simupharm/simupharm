# calculate_sus_score.py
# Canonical Brooke (1996) System Usability Scale Analysis Pipeline
# Version: REV2 / PHASE4.2

import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

def compute_sus_single(row):
    """Compute SUS for a single participant following Brooke (1996) and Sauro (2016) imputation."""
    sus_cols = [f'sus_q{i}' for i in range(1, 11)]
    vals = [row[c] for c in sus_cols]
    
    # Count missing values
    missing_count = sum(pd.isna(vals))
    if missing_count >= 3:
        return np.nan  # Exclude submission
        
    # Impute missing items (1-2 missing) with neutral score (3)
    clean_vals = [3 if pd.isna(v) else float(v) for v in vals]
    
    # Brooke 1996 algorithm
    # Odd items (0, 2, 4, 6, 8): val - 1
    # Even items (1, 3, 5, 7, 9): 5 - val
    contributions = []
    for idx, v in enumerate(clean_vals):
        if idx % 2 == 0:  # Odd item (1, 3, 5, 7, 9)
            contributions.append(v - 1.0)
        else:             # Even item (2, 4, 6, 8, 10)
            contributions.append(5.0 - v)
            
    return sum(contributions) * 2.5

def run_sus_analysis(csv_path):
    print(f"=== RUNNING CANONICAL BROOKE (1996) SUS ANALYSIS PIPELINE ===")
    print(f"Data source: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"ERROR: Dataset {csv_path} not found.")
        sys.exit(1)
        
    df = pd.read_csv(csv_path)
    sus_cols = [f'sus_q{i}' for i in range(1, 11)]
    
    scores = []
    for _, row in df.iterrows():
        s = compute_sus_single(row)
        scores.append(s)
        
    df['sus_calculated'] = scores
    valid_scores = df['sus_calculated'].dropna().values
    n_valid = len(valid_scores)
    
    print(f"Total Submissions Evaluated: {len(df)}")
    print(f"Usable Valid SUS Submissions: {n_valid}")
    
    if n_valid < 3:
        print("ERROR: Insufficient valid SUS records.")
        return
        
    mean_sus = float(np.mean(valid_scores))
    sd_sus = float(np.std(valid_scores, ddof=1))
    median_sus = float(np.median(valid_scores))
    q25, q75 = np.percentile(valid_scores, [25, 75])
    iqr_sus = float(q75 - q25)
    
    ci_low, ci_high = stats.t.interval(0.95, df=n_valid-1, loc=mean_sus, scale=sd_sus / np.sqrt(n_valid))
    
    # Bangor Adjective Rating
    if mean_sus >= 85.0:
        adj = "Excellent (Grade A+)"
    elif mean_sus >= 72.0:
        adj = "Good (Grade B / B+)"
    elif mean_sus >= 68.0:
        adj = "OK / Above Average (Grade C+)"
    elif mean_sus >= 51.0:
        adj = "Poor (Grade D)"
    else:
        adj = "Unacceptable (Grade F)"
        
    print(f"\n--- SUS EMPIRICAL BENCHMARK METRICS ---")
    print(f"Mean SUS Score: {mean_sus:.2f} (SD: {sd_sus:.2f})")
    print(f"Median SUS Score: {median_sus:.2f} (IQR: {iqr_sus:.2f})")
    print(f"95% Confidence Interval: [{ci_low:.2f}, {ci_high:.2f}]")
    print(f"Bangor Adjective Rating: {adj}")
    print(f"Industry Benchmark (68.0): {'SURPASSES BENCHMARK' if mean_sus >= 68.0 else 'BELOW BENCHMARK'}")
    print(f"Pipeline Execution Status: PASS\n")

if __name__ == '__main__':
    default_csv = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'DEMO_TEST_ONLY.csv')
    run_sus_analysis(default_csv)
