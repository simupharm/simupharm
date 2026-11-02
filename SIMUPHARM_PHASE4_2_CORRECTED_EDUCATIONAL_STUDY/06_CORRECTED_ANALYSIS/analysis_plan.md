# Analysis Pipeline Architecture & Execution Protocols
**Document ID:** P4.2-ANALYSIS-PLAN-2026-REV2.2  
**Target:** Automated Pre-Registered Statistical Pipeline for SimuPharm Pilot Study  

---

## 1. Analysis Code Inventory
The analysis pipeline consists of standalone, reproducible Python scripts designed to execute directly on the reconciled participant data schema:

1. `calculate_pre_post_stats.py`: Primary prespecified inferential test (Wilcoxon Signed-Rank with Pratt's zero-difference method), Hodges-Lehmann median difference with exact 95% Walsh order-statistic CI, signed rank-biserial effect size ($r_{rb}$), and paired t-test sensitivity analysis.
2. `calculate_sus_score.py`: Canonical Brooke (1996) System Usability Scale calculation with Sauro (2016) item imputation for incomplete records.
3. `calculate_hake_gain.py`: Cohort average normalized gain and individual normalized learning gains with Pre=10 ceiling case handling.
4. `calculate_item_psychometrics.py`: Exploratory item difficulty index ($P$) and item discrimination index ($D$) with $N \approx 25$ sample size caveats.
5. `calculate_confidence_calibration.py`: Pearson correlation ($r$) and Spearman rank correlation ($\rho$) between subjective confidence and diagnostic performance as an exploratory calibration indicator (zero causal claims).

---

## 2. Testing Isolation Safeguards
- **NO REAL PARTICIPANT DATA IS STORED HERE.**
- Analysis code testing is strictly restricted to `test_data/DEMO_TEST_ONLY.csv`, a synthetic dataset containing engineered edge cases (zero gains, negative gains, missing values, Pre=10 ceiling).
- The pipeline will ONLY execute on real data after formal institutional authorization is signed and participant collection is concluded.
