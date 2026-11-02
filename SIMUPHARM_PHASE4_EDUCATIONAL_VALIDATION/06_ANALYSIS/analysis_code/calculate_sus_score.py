import sys
import os
import pandas as pd
import numpy as np
from scipy import stats

def analyze_sus(csv_file):
    print(f"=== SIMUPHARM SYSTEM USABILITY SCALE (SUS) ANALYSIS ===")
    print(f"Data source: {csv_file}")
    
    if not os.path.exists(csv_file):
        print(f"ERROR: File {csv_file} not found.")
        return
        
    df = pd.read_csv(csv_file)
    if len(df) == 0:
        print("NOTICE: Dataset contains 0 rows (template is blank as required prior to real study).")
        return
        
    sus_cols = [f'sus_q{i}' for i in range(1, 11)]
    for c in sus_cols:
        if c not in df.columns:
            print(f"ERROR: Column {c} missing from CSV.")
            return
            
    df_sus = df[sus_cols].dropna()
    n = len(df_sus)
    print(f"Usable SUS Submissions (N): {n}")
    
    scores = []
    for idx, row in df_sus.iterrows():
        # Brooke 1996 scoring
        # Odd items (1,3,5,7,9): x - 1
        # Even items (2,4,6,8,10): 5 - x
        q1 = row['sus_q1'] - 1
        q2 = 5 - row['sus_q2']
        q3 = row['sus_q3'] - 1
        q4 = 5 - row['sus_q4']
        q5 = row['sus_q5'] - 1
        q6 = 5 - row['sus_q6']
        q7 = row['sus_q7'] - 1
        q8 = 5 - row['sus_q8']
        q9 = row['sus_q9'] - 1
        q10 = 5 - row['sus_q10']
        total = 2.5 * (q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10)
        scores.append(total)
        
    scores = np.array(scores)
    mean_sus = np.mean(scores)
    sd_sus = np.std(scores, ddof=1) if n > 1 else 0.0
    se_sus = sd_sus / np.sqrt(n) if n > 0 else 0.0
    ci_low = mean_sus - stats.t.ppf(0.975, df=max(1, n-1)) * se_sus
    ci_high = mean_sus + stats.t.ppf(0.975, df=max(1, n-1)) * se_sus
    
    print(f"\nMean SUS Score: {mean_sus:.2f} (SD: {sd_sus:.2f})")
    print(f"Median SUS Score: {np.median(scores):.2f} (IQR: {stats.iqr(scores):.2f})")
    print(f"95% Confidence Interval: [{ci_low:.2f}, {ci_high:.2f}]")
    
    # Bangor et al. (2008) adjective rating
    adj = "Best Imaginable" if mean_sus >= 85 else (
        "Excellent" if mean_sus >= 80 else (
            "Good" if mean_sus >= 70 else (
                "OK / Marginal" if mean_sus >= 50 else "Poor / Not Acceptable"
            )
        )
    )
    print(f"Bangor Usability Rating: {adj}")
    print("==================================================")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'participant_data_template.csv'
    analyze_sus(path)
