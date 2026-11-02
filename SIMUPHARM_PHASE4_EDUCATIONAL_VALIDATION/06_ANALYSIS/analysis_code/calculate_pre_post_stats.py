import sys
import os
import pandas as pd
import numpy as np
from scipy import stats

def analyze_pre_post(csv_file):
    print(f"=== SIMUPHARM PRE/POST STATISTICAL ANALYSIS ===")
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
    
    if len(pre) != len(post):
        print("ERROR: Unequal length of pre and post scores.")
        return
        
    n = len(pre)
    diff = post - pre
    
    print(f"\nSample Size (N): {n}")
    print(f"Pre-Test Mean (SD): {np.mean(pre):.2f} ({np.std(pre, ddof=1):.2f}) | Median (IQR): {np.median(pre):.1f} ({stats.iqr(pre):.1f})")
    print(f"Post-Test Mean (SD): {np.mean(post):.2f} ({np.std(post, ddof=1):.2f}) | Median (IQR): {np.median(post):.1f} ({stats.iqr(post):.1f})")
    print(f"Mean Gain (SD): {np.mean(diff):+.2f} ({np.std(diff, ddof=1):.2f}) | Median Gain: {np.median(diff):+.1f}")
    
    # 1. Normality Assessment (Shapiro-Wilk)
    stat_sw, p_sw = stats.shapiro(diff)
    print(f"\nShapiro-Wilk Test of Differences: W = {stat_sw:.4f}, p = {p_sw:.4f}")
    if p_sw >= 0.05:
        print("Interpretation: Differences do NOT significantly deviate from normality (p >= 0.05). Paired t-test is appropriate.")
    else:
        print("Interpretation: Differences deviate from normality (p < 0.05). Wilcoxon signed-rank test is primary.")
        
    # 2. Paired Student's t-test
    t_stat, p_val_t = stats.ttest_rel(post, pre)
    se_diff = np.std(diff, ddof=1) / np.sqrt(n)
    ci_low = np.mean(diff) - stats.t.ppf(0.975, df=n-1) * se_diff
    ci_high = np.mean(diff) + stats.t.ppf(0.975, df=n-1) * se_diff
    cohen_dz = np.mean(diff) / np.std(diff, ddof=1) if np.std(diff, ddof=1) > 0 else 0.0
    
    print(f"\n--- Parametric Analysis (Paired t-test) ---")
    print(f"t({n-1}) = {t_stat:.3f}, p-value = {p_val_t:.4e}")
    print(f"95% CI of Mean Difference: [{ci_low:+.2f}, {ci_high:+.2f}] points")
    print(f"Effect Size (Cohen's d_z): {cohen_dz:.2f}")
    
    # 3. Wilcoxon Signed-Rank Test
    w_stat, p_val_w = stats.wilcoxon(post, pre, zero_method='wilcox', correction=True)
    # Rank biserial r
    r_biserial = 1.0 - (2.0 * w_stat) / (n * (n + 1) / 2.0)
    print(f"\n--- Non-Parametric Analysis (Wilcoxon Signed-Rank) ---")
    print(f"W = {w_stat:.1f}, p-value = {p_val_w:.4e}")
    print(f"Effect Size (Rank-Biserial r): {r_biserial:.2f}")
    print("==================================================")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'participant_data_template.csv'
    analyze_pre_post(path)
