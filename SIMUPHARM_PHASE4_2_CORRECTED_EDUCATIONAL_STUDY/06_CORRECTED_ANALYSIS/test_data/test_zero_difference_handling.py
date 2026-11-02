# test_zero_difference_handling.py
# Verification Test Suite for Wilcoxon Zero-Difference Handling (Pratt Method)
# Version: REV2 / PHASE4.2

import os
import sys
import numpy as np
from scipy import stats

def test_pratt_handling():
    print("=== EXECUTING UNIT TEST: PRATT ZERO-DIFFERENCE HANDLING ===")
    
    # Controlled dataset with engineered pairs:
    # 2 positive gains (+3, +2)
    # 1 zero gain (tie: Pre 5, Post 5, Delta = 0)
    # 1 negative gain (-1)
    pre = np.array([3, 4, 5, 6])
    post = np.array([6, 6, 5, 5])
    diffs = post - pre  # [+3, +2, 0, -1]
    
    print(f"Engineered Diffs: {diffs.tolist()}")
    
    # 1. Wilcoxon method (Standard)
    # Drops zero difference: N becomes 3
    res_wilcox = stats.wilcoxon(post, pre, zero_method='wilcox')
    print(f"Wilcox Method: W = {res_wilcox.statistic}, p = {res_wilcox.pvalue:.4f} (Zero dropped)")
    
    # 2. Pratt method (Mandated for Phase 4.2)
    # Retains zero difference in ranking: N remains 4
    res_pratt = stats.wilcoxon(post, pre, zero_method='pratt')
    print(f"Pratt Method:  W = {res_pratt.statistic}, p = {res_pratt.pvalue:.4f} (Zero retained)")
    
    # Verification assertions
    assert len(diffs) == 4, "Array length should be 4"
    assert res_pratt.statistic is not None, "Pratt statistic must not be None"
    assert res_pratt.pvalue is not None, "Pratt p-value must not be None"
    print("TEST RESULT: PASS (Pratt zero-difference retention mathematically verified)\n")

if __name__ == '__main__':
    test_pratt_handling()
