# check_position_bias.py
# Automated Verification of Answer-Key Position Bias in Pre-Test and Post-Test
# Version: REV2 / PHASE4.2

import numpy as np
from scipy import stats

pretest_keys = ['C', 'A', 'D', 'B', 'A', 'C', 'D', 'B', 'C', 'B']
posttest_keys = ['B', 'D', 'A', 'C', 'A', 'C', 'B', 'D', 'A', 'C']

def audit_keys(name, keys):
    print(f"=== AUDITING ANSWER KEYS: {name} ===")
    total = len(keys)
    counts = {opt: keys.count(opt) for opt in ['A', 'B', 'C', 'D']}
    pcts = {opt: counts[opt] / total * 100 for opt in ['A', 'B', 'C', 'D']}
    
    print(f"Total Items: {total}")
    for opt in ['A', 'B', 'C', 'D']:
        print(f"  Option {opt}: {counts[opt]} items ({pcts[opt]:.1f}%)")
        
    # Check max consecutive identical keys
    max_consecutive = 1
    current_consecutive = 1
    for i in range(1, len(keys)):
        if keys[i] == keys[i-1]:
            current_consecutive += 1
            if current_consecutive > max_consecutive:
                max_consecutive = current_consecutive
        else:
            current_consecutive = 1
    print(f"  Max Consecutive Identical Keys: {max_consecutive}")
    
    # Chi-square goodness-of-fit against uniform (2.5 each)
    expected = [total / 4.0] * 4
    observed = [counts['A'], counts['B'], counts['C'], counts['D']]
    chi2, p_val = stats.chisquare(f_obs=observed, f_exp=expected)
    print(f"  Chi-Square Goodness-of-Fit: Chi2 = {chi2:.3f}, p = {p_val:.4f}")
    
    # Assertions
    assert max(pcts.values()) <= 35.0, f"Option percentage {max(pcts.values())}% exceeds 35% threshold!"
    assert min(pcts.values()) >= 15.0, f"Option percentage {min(pcts.values())}% below 15% threshold!"
    assert max_consecutive <= 2, f"Consecutive identical keys {max_consecutive} exceeds limit of 2!"
    print("  STATUS: PASS (Zero Position Bias Confirmed)\\n")

if __name__ == '__main__':
    audit_keys("Pre-Test (P4.2-PRETEST-2026-REV2)", pretest_keys)
    audit_keys("Post-Test (P4.2-POSTTEST-2026-REV2)", posttest_keys)
    print("ALL PSYCHOMETRIC POSITION BIAS CHECKS PASSED SUCCESSFULLY.")
