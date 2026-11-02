# calculate_pre_post_stats.py
# Primary Inferential Statistical Analysis Pipeline for SimuPharm Pilot
# Version: REV2 / PHASE4.2

import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

def compute_hodges_lehmann(diffs):
    """Compute Hodges-Lehmann estimator (median of all pairwise Walsh averages)."""
    diffs = np.array(diffs)
    walsh_averages = []
    n = len(diffs)
    for i in range(n):
        for j in range(i, n):
            walsh_averages.append((diffs[i] + diffs[j]) / 2.0)
    return float(np.median(walsh_averages))

def run_pre_post_analysis(csv_path):
    print(f"=== RUNNING PRE/POST STATISTICAL ANALYSIS PIPELINE ===")
    print(f"Data source: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"ERROR: Dataset {csv_path} not found.")
        sys.exit(1)
        
    df = pd.read_csv(csv_path)
    
    # Missing data handling: complete case analysis for paired pre/post scores
    valid_mask = df['pre_test_total'].notna() & df['post_test_total'].notna()
    df_valid = df[valid_mask].copy()
    
    pre = df_valid['pre_test_total'].astype(float).values
    post = df_valid['post_test_total'].astype(float).values
    diff = post - pre
    n = len(diff)
    
    print(f"Total Cohort Enrolled: {len(df)}")
    print(f"Usable Complete-Case Paired Records (N): {n}")
    
    if n < 3:
        print("ERROR: Insufficient sample size for inferential testing.")
        return
        
    # Descriptive Statistics
    pre_mean, pre_sd = float(np.mean(pre)), float(np.std(pre, ddof=1))
    post_mean, post_sd = float(np.mean(post)), float(np.std(post, ddof=1))
    gain_mean, gain_sd = float(np.mean(diff)), float(np.std(diff, ddof=1))
    gain_median = float(np.median(diff))
    
    print(f"Pre-Test Score:  Mean = {pre_mean:.2f} (SD = {pre_sd:.2f}) | Median = {np.median(pre):.1f}")
    print(f"Post-Test Score: Mean = {post_mean:.2f} (SD = {post_sd:.2f}) | Median = {np.median(post):.1f}")
    print(f"Paired Difference: Mean Gain = {gain_mean:+.2f} (SD = {gain_sd:.2f}) | Median Gain = {gain_median:+.1f}")
    
    # Descriptive Distributional Check
    sw_stat, sw_p = stats.shapiro(diff)
    print(f"Shapiro-Wilk Normality Test on Diffs: W = {sw_stat:.4f}, p = {sw_p:.4f}")
    
    # 1. PRIMARY INFERENTIAL TEST: Wilcoxon Signed-Rank Test (Pratt Method)
    # Pratt method explicitly incorporates zero-difference ties in the ranking
    abs_d = np.abs(diff)
    ranks = stats.rankdata(abs_d)
    w_plus = float(np.sum(ranks[diff > 0]))
    w_minus = float(np.sum(ranks[diff < 0]))
    s_nonzero = w_plus + w_minus
    
    # Exact signed rank-biserial correlation: (W+ - W-) / (W+ + W-)
    # Positive = improvement, Negative = deterioration, Zero = no effect
    rank_biserial_r = float((w_plus - w_minus) / s_nonzero) if s_nonzero > 0 else 0.0
    
    if np.all(diff == 0):
        w_stat = 0.0
        w_p = 1.0
        hl_est = 0.0
        hl_ci_low, hl_ci_high = 0.0, 0.0
    else:
        try:
            w_res = stats.wilcoxon(post, pre, zero_method='pratt', alternative='two-sided')
            w_stat, w_p = float(w_res.statistic), float(w_res.pvalue)
        except Exception:
            w_stat = min(w_plus, w_minus)
            w_p = 1.0
            
        hl_est = compute_hodges_lehmann(diff)
        
        # Walsh-average order-statistic 95% CI using critical-index approximation (Bauer 1972; Hollander & Wolfe 1999)
        walsh = []
        for i in range(n):
            for j in range(i, n):
                walsh.append((diff[i] + diff[j]) / 2.0)
        walsh = np.sort(walsh)
        m_walsh = len(walsh)
        if n >= 4:
            mean_w = n * (n + 1) / 4.0
            var_w = n * (n + 1) * (2 * n + 1) / 24.0
            z_crit = stats.norm.ppf(0.975)
            c_crit = z_crit * np.sqrt(var_w)
            k_crit = int(np.floor(mean_w - c_crit))
            k_crit = max(1, min(k_crit, m_walsh // 2))
            hl_ci_low = float(walsh[k_crit - 1])
            hl_ci_high = float(walsh[m_walsh - k_crit])
        else:
            hl_ci_low, hl_ci_high = float(walsh[0]), float(walsh[-1])
    
    print(f"\n--- PRIMARY PRESPECIFIED INFERENTIAL ANALYSIS (WILCOXON SIGNED-RANK / PRATT) ---")
    print(f"Wilcoxon W Statistic: {w_stat:.1f} (W+ = {w_plus:.1f}, W- = {w_minus:.1f})")
    print(f"Asymptotic / Exact p-value: {w_p:.5e} (Significant at alpha=0.05: {w_p < 0.05})")
    print(f"Hodges-Lehmann Median Difference: {hl_est:+.2f} points (95% Walsh order-statistic CI: [{hl_ci_low:+.2f}, {hl_ci_high:+.2f}])")
    print(f"Rank-Biserial Correlation (r_rb): {rank_biserial_r:+.3f}")
    
    # 2. SENSITIVITY ANALYSIS: Paired Student's t-test
    t_res = stats.ttest_rel(post, pre)
    t_stat, t_p = float(t_res.statistic), float(t_res.pvalue)
    cohens_dz = float(gain_mean / gain_sd) if gain_sd > 0 else 0.0
    ci_low, ci_high = stats.t.interval(0.95, df=n-1, loc=gain_mean, scale=gain_sd / np.sqrt(n))
    
    print(f"\n--- SENSITIVITY ANALYSIS (PAIRED t-TEST) ---")
    print(f"Paired t-statistic: t({n-1}) = {t_stat:.3f}, p = {t_p:.5e}")
    print(f"Cohen's dz: {cohens_dz:.3f}")
    print(f"95% Confidence Interval for Mean Difference: [{ci_low:+.2f}, {ci_high:+.2f}]")
    print(f"Pipeline Execution Status: PASS\n")

if __name__ == '__main__':
    default_csv = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'DEMO_TEST_ONLY.csv')
    run_pre_post_analysis(default_csv)
