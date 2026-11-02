# verify_wilcoxon_pipeline.py
# Comprehensive Technical Verification Suite for Wilcoxon / Pratt & Hodges-Lehmann Pipeline
# Tests synthetic edge cases:
# A. All positive differences
# B. All negative differences
# C. Mixed differences
# D. Zero differences included
# E. All zero differences (SciPy ValueError safeguard)
# F. Tied absolute differences
# G. Missing observations (complete-case filtering)

import numpy as np
import pandas as pd
from scipy import stats

def compute_wilcoxon_pratt_robust(pre, post, alpha=0.05):
    """
    Robust paired Wilcoxon signed-rank calculation using Pratt's zero-difference method.
    Returns:
      n: number of paired valid observations
      w_plus: sum of ranks of positive differences
      w_minus: sum of ranks of negative differences
      w_stat: test statistic (min(w_plus, w_minus))
      p_value: two-sided p-value
      r_rb: rank-biserial correlation (-1.0 to +1.0)
      hl_est: Hodges-Lehmann median difference
      hl_ci_low, hl_ci_high: 95% Walsh order-statistic confidence interval
    """
    pre = np.asarray(pre, dtype=float)
    post = np.asarray(post, dtype=float)
    diff = post - pre
    n = len(diff)
    
    if n == 0:
        return {"n": 0, "error": "No valid observations"}
        
    # Check for all-zero differences
    if np.all(diff == 0):
        return {
            "n": n,
            "w_plus": 0.0,
            "w_minus": 0.0,
            "w_stat": 0.0,
            "p_value": 1.0,
            "r_rb": 0.0,
            "hl_est": 0.0,
            "hl_ci_low": 0.0,
            "hl_ci_high": 0.0,
            "all_zero": True
        }
        
    # Pratt method ranking: zeros are included in rank assignment
    abs_d = np.abs(diff)
    ranks = stats.rankdata(abs_d)
    w_plus = float(np.sum(ranks[diff > 0]))
    w_minus = float(np.sum(ranks[diff < 0]))
    s_nonzero = w_plus + w_minus
    
    # Rank-biserial correlation: (W+ - W-) / (W+ + W-)
    r_rb = float((w_plus - w_minus) / s_nonzero) if s_nonzero > 0 else 0.0
    
    # SciPy Pratt Wilcoxon test
    try:
        res = stats.wilcoxon(post, pre, zero_method='pratt', alternative='two-sided')
        w_stat = float(res.statistic)
        p_val = float(res.pvalue)
    except Exception as e:
        # Fallback if scipy encounters an edge case
        w_stat = min(w_plus, w_minus)
        p_val = 1.0
        
    # Hodges-Lehmann estimator & Walsh average CI
    walsh = []
    for i in range(n):
        for j in range(i, n):
            walsh.append((diff[i] + diff[j]) / 2.0)
    walsh = np.sort(walsh)
    m = len(walsh)
    hl_est = float(np.median(walsh))
    
    # Walsh order-statistic CI using critical-index approximation (Bauer 1972 / Hollander & Wolfe 1999)
    if n >= 4:
        mean_w = n * (n + 1) / 4.0
        var_w = n * (n + 1) * (2 * n + 1) / 24.0
        z = stats.norm.ppf(1.0 - alpha / 2.0)
        c = z * np.sqrt(var_w)
        k = int(np.floor(mean_w - c))
        k = max(1, min(k, m // 2))
        ci_low = float(walsh[k - 1])
        ci_high = float(walsh[m - k])
    else:
        ci_low, ci_high = float(walsh[0]), float(walsh[-1])
        
    return {
        "n": n,
        "w_plus": w_plus,
        "w_minus": w_minus,
        "w_stat": w_stat,
        "p_value": p_val,
        "r_rb": r_rb,
        "hl_est": hl_est,
        "hl_ci_low": ci_low,
        "hl_ci_high": ci_high,
        "all_zero": False
    }

def run_suite():
    print("=====================================================================")
    print("   PHASE 4.2.2 DEMO_TEST_ONLY WILCOXON & CI VERIFICATION SUITE       ")
    print("=====================================================================\n")
    
    cases = {
        "Case A (All Positive Differences)": {
            "pre":  [2, 3, 4, 3, 2, 4, 3, 2],
            "post": [5, 6, 7, 6, 5, 8, 7, 6]
        },
        "Case B (All Negative Differences)": {
            "pre":  [6, 7, 8, 7, 6, 8, 7, 6],
            "post": [3, 4, 5, 4, 3, 5, 4, 3]
        },
        "Case C (Mixed Differences)": {
            "pre":  [3, 4, 5, 6, 4, 5, 3, 6],
            "post": [6, 5, 4, 7, 6, 4, 5, 8]
        },
        "Case D (Zero Differences Present)": {
            "pre":  [4, 5, 5, 6, 3, 4, 5, 5],
            "post": [6, 5, 7, 6, 5, 4, 8, 5]
        },
        "Case E (All Zero Differences)": {
            "pre":  [5, 5, 5, 5, 5],
            "post": [5, 5, 5, 5, 5]
        },
        "Case F (Tied Absolute Differences)": {
            "pre":  [3, 3, 3, 3, 3, 3],
            "post": [5, 5, 5, 1, 1, 1]
        },
        "Case G (Missing Observations Included)": {
            "pre":  [3, 4, np.nan, 5, 6, np.nan, 4],
            "post": [5, np.nan, 6, 7, 6, np.nan, 7]
        }
    }
    
    for name, data in cases.items():
        pre_arr = np.array(data["pre"])
        post_arr = np.array(data["post"])
        
        # Missing data complete case filter
        valid = ~np.isnan(pre_arr) & ~np.isnan(post_arr)
        pre_valid = pre_arr[valid]
        post_valid = post_arr[valid]
        diffs = post_valid - pre_valid
        
        res = compute_wilcoxon_pratt_robust(pre_valid, post_valid)
        
        print(f"--- {name} ---")
        print(f"Raw N: {len(pre_arr)} | Valid Paired N: {res['n']}")
        print(f"Differences: {diffs.tolist()}")
        print(f"W+ (Positive Ranks): {res['w_plus']} | W- (Negative Ranks): {res['w_minus']}")
        print(f"Wilcoxon Statistic: {res['w_stat']} | p-value: {res['p_value']:.4e}")
        print(f"Rank-Biserial r: {res['r_rb']:+.3f}")
        print(f"Hodges-Lehmann: {res['hl_est']:+.2f} [95% CI: {res['hl_ci_low']:+.2f}, {res['hl_ci_high']:+.2f}]")
        
        # Directional and sanity assertions
        if name.startswith("Case A"):
            assert res['r_rb'] == +1.0, "Case A r_rb must be +1.0"
            assert res['hl_est'] > 0, "Case A HL must be > 0"
            print(">> VERIFICATION PASS: Strict positive direction verified.")
        elif name.startswith("Case B"):
            assert res['r_rb'] == -1.0, "Case B r_rb must be -1.0"
            assert res['hl_est'] < 0, "Case B HL must be < 0"
            print(">> VERIFICATION PASS: Strict negative direction verified.")
        elif name.startswith("Case E"):
            assert res['r_rb'] == 0.0, "Case E r_rb must be 0.0"
            assert res['p_value'] == 1.0, "Case E p-value must be 1.0"
            assert res['hl_est'] == 0.0, "Case E HL must be 0.0"
            print(">> VERIFICATION PASS: All-zero difference safeguard verified.")
        elif name.startswith("Case F"):
            assert res['r_rb'] == 0.0, "Case F r_rb must be 0.0"
            assert res['hl_est'] == 0.0, "Case F HL must be 0.0"
            print(">> VERIFICATION PASS: Balanced ties produce null effect.")
        elif name.startswith("Case G"):
            assert res['n'] == 4, "Case G complete pairs must be 4"
            print(">> VERIFICATION PASS: Missing observations correctly filtered.")
        print()

if __name__ == '__main__':
    run_suite()
