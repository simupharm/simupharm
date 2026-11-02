import sys
import os
import pandas as pd
import numpy as np

def analyze_hake(csv_file):
    print(f"=== SIMUPHARM HAKE NORMALIZED GAIN ANALYSIS ===")
    print(f"Data source: {csv_file}")
    
    if not os.path.exists(csv_file):
        print(f"ERROR: File {csv_file} not found.")
        return
        
    df = pd.read_csv(csv_file)
    if len(df) == 0:
        print("NOTICE: Dataset contains 0 rows (template is blank as required prior to real study).")
        return
        
    pre = df['pre_score'].dropna().values
    post = df['post_score'].dropna().values
    
    # Average normalized gain: <g> = (mean(post) - mean(pre)) / (10 - mean(pre))
    mean_pre = np.mean(pre)
    mean_post = np.mean(post)
    
    if mean_pre >= 10.0:
        print("Ceiling effect: Pre-test mean is 10.0.")
        return
        
    overall_g = (mean_post - mean_pre) / (10.0 - mean_pre)
    
    # Individual normalized gains
    indiv_g = []
    for p_pre, p_post in zip(pre, post):
        if p_pre == 10:
            indiv_g.append(1.0 if p_post == 10 else 0.0)
        else:
            indiv_g.append((p_post - p_pre) / (10.0 - p_pre))
            
    print(f"\nOverall Average Normalized Gain <g>: {overall_g:.3f}")
    print(f"Mean Individual Normalized Gain: {np.mean(indiv_g):.3f} (SD: {np.std(indiv_g, ddof=1):.3f})")
    
    # Classification
    cat = "High Gain (g >= 0.70)" if overall_g >= 0.70 else (
        "Medium Gain (0.30 <= g < 0.70)" if overall_g >= 0.30 else "Low Gain (g < 0.30)"
    )
    print(f"Hake Classification: {cat}")
    print("==================================================")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'participant_data_template.csv'
    analyze_hake(path)
