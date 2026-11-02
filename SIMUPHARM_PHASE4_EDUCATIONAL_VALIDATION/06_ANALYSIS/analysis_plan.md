# ANALYSIS EXECUTION PROTOCOL & SCRIPT SPECIFICATIONS
**Document ID:** P4-ANL-PLAN-2026-REV1  
**Platform:** Python 3.10+ (NumPy, SciPy, Pandas, Statsmodels)  

---

## SCRIPT INVENTORY & WORKFLOW

```mermaid
flowchart TD
    Raw["Raw Participant Data<br/>participant_data_template.csv"] --> S1["calculate_pre_post_stats.py<br/>• Shapiro-Wilk Normality<br/>• Paired t-test + Cohen's d_z<br/>• Wilcoxon + Rank-Biserial r"]
    Raw --> S2["calculate_sus_score.py<br/>• Brooke 1996 Algorithm<br/>• Mean, Median, SD, 95% CI<br/>• Bangor Adjective Rating"]
    Raw --> S3["calculate_hake_gain.py<br/>• Average Normalized Gain <g><br/>• Hake Class Distribution"]
    S1 --> Output["Formatted Publication Tables & CIs<br/>for JCE Manuscript Results Section"]
    S2 --> Output
    S3 --> Output
```

### Script Execution Orders:
1. `python calculate_pre_post_stats.py [csv_path]`
2. `python calculate_sus_score.py [csv_path]`
3. `python calculate_hake_gain.py [csv_path]`
