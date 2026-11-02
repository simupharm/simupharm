import os

base_paths = [
    r'c:\Users\dsant\OneDrive\simupro - Copy\SIMUPHARM_PHASE4_EDUCATIONAL_VALIDATION',
    r'C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\SIMUPHARM_PHASE4_EDUCATIONAL_VALIDATION'
]

def write_both(rel_path, content):
    for base in base_paths:
        full_path = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# ==============================================================================
# 04_USABILITY
# ==============================================================================

sus_instrument = """# SYSTEM USABILITY SCALE (SUS) QUESTIONNAIRE
**Document ID:** P4-SUS-2026-REV1  
**Source Standard:** Brooke, J. (1996) *SUS: A quick and dirty usability scale*  
**Administration:** Post-Intervention (Session Minute 45)  

---

**Participant ID Code:** ____________________  

### Instructions:
Please indicate your level of agreement with each statement by checking one box per item.  
Scale: 1 = Strongly Disagree (SD), 2 = Disagree (D), 3 = Neutral (N), 4 = Agree (A), 5 = Strongly Agree (SA).

| # | Statement | 1 (SD) | 2 (D) | 3 (N) | 4 (A) | 5 (SA) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Q1** | I think that I would like to use this system frequently for chromatography learning. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q2** | I found the system unnecessarily complex. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q3** | I thought the system was easy to use. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q4** | I think that I would need the support of a technical person to be able to use this system. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q5** | I found the various functions in this system were well integrated. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q6** | I thought there was too much inconsistency in this system. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q7** | I would imagine that most students would learn to use this system very quickly. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q8** | I found the system very cumbersome to use. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q9** | I felt very confident using the system. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q10** | I needed to learn a lot of things before I could get going with this system. | [ ] | [ ] | [ ] | [ ] | [ ] |

---

### Standard Scoring Algorithm (Brooke 1996):
- For odd items ($1, 3, 5, 7, 9$): Score contribution $= \text{Scale Position} - 1$
- For even items ($2, 4, 6, 8, 10$): Score contribution $= 5 - \text{Scale Position}$
- Individual SUS Score $= 2.5 \times \sum_{i=1}^{10} \text{Contribution}_i \in [0, 100]$
- Continuous interpretation against Bangor et al. (2008) empirical thresholds:
  - $< 50$: Not Acceptable
  - $50 - 69$: Marginal
  - $70 - 79$: Acceptable / Good
  - $\ge 80$: Excellent
  - $\ge 85$: Best Imaginable
"""

usability_survey = """# TARGETED USABILITY & INTERACTION SURVEY
**Document ID:** P4-UXSURV-2026-REV1  
**Construct:** Domain-Specific Interaction Quality in HPLC Simulation  

---

**Participant ID Code:** ____________________  

Please rate each aspect of SimuPharm from 1 (Poor / Strongly Disagree) to 5 (Excellent / Strongly Agree):

| # | Usability Dimension | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **U1** | **Visual Clarity:** Chromatograms, peak labels, and axes were clear and legible. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **U2** | **Instrument Feedback:** The digital pressure gauge and status indicators clearly reflected system state changes. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **U3** | **Parameter Controls:** Sliders and inputs for flow rate, %B, and column type were intuitive and responsive. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **U4** | **Diagnostic Distinguishability:** The visual differences between fault conditions (air bubble vs leak vs void) were clear. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **U5** | **Execution Speed:** Simulation runs executed rapidly without frustrating browser lag or freezing. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **U6** | **Learning Autonomy:** I was able to test "what-if" operating scenarios independently without instructor assistance. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **U7** | **Laboratory Relevance:** Practicing with these fault simulations helped me understand physical HPLC instrument risks. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **U8** | **Pre-Lab Utility:** I would find this simulator valuable as a mandatory pre-lab exercise before physical HPLC operation. | [ ] | [ ] | [ ] | [ ] | [ ] |
"""

qualitative_feedback = """# QUALITATIVE USER EXPERIENCE FEEDBACK FORM
**Document ID:** P4-QUAL-2026-REV1  
**Methodology:** Open-Ended Experiential Inquiry & Thematic Coding Protocol  

---

**Participant ID Code:** ____________________  

### Open-Ended Questions:

1. **What feature or aspect of the SimuPharm simulator did you find easiest or most helpful for your learning?**  
   ________________________________________________________________________________________________  
   ________________________________________________________________________________________________  

2. **What aspect of the interface, controls, or outputs was most confusing, difficult, or frustrating?**  
   ________________________________________________________________________________________________  
   ________________________________________________________________________________________________  

3. **Which fault scenario (air bubble, leak, column void, contamination) was the hardest to diagnose, and why?**  
   ________________________________________________________________________________________________  
   ________________________________________________________________________________________________  

4. **What chromatographic, physical, or numerical information did you feel was missing that would have helped your diagnosis?**  
   ________________________________________________________________________________________________  
   ________________________________________________________________________________________________  

5. **Would you recommend SimuPharm as a required preparatory assignment before students enter the physical HPLC laboratory? Why or why not?**  
   ________________________________________________________________________________________________  
   ________________________________________________________________________________________________  

6. **What is one specific improvement or new feature you would like to see in the next version of this software?**  
   ________________________________________________________________________________________________  
   ________________________________________________________________________________________________  

---

## THEMATIC ANALYSIS PROTOCOL (FOR RESEARCH TEAM)
1. **Transcription:** Responses transcribed verbatim into data ledger.
2. **Inductive Coding:** Two independent researchers generate initial codebook from responses.
3. **Sentiment Classification:** Feedback categorized as Positive (+1), Constructive / Neutral (0), or Negative / Critical (-1).
4. **Frequency Matrix:** Report percentage of participants mentioning recurring themes (e.g., "Pressure gauge visibility", "Need for split-peak explanation", "Browser zoom issues").
5. **No Cherry-Picking Rule:** In accordance with JCE peer-review standards, all critical and negative feedback must be documented in the manuscript Discussion and Limitations sections.
"""

write_both("04_USABILITY/SUS_instrument.md", sus_instrument)
write_both("04_USABILITY/usability_questionnaire.md", usability_survey)
write_both("04_USABILITY/qualitative_feedback_form.md", qualitative_feedback)

# ==============================================================================
# 05_DATA_TEMPLATES
# ==============================================================================

data_dictionary = """# ANONYMIZED DATA DICTIONARY & VARIABLE SCHEMA
**Document ID:** P4-DICT-2026-REV1  
**Target File:** `participant_data_template.csv`  

---

## VARIABLE SPECIFICATIONS

| Variable Name | Data Type | Units / Format | Permissible Range | Definition & Coding Rules |
| :--- | :--- | :--- | :--- | :--- |
| `participant_id` | String | Identifier | `P01` to `P99` | Unique anonymized participant identifier. |
| `group` | String | Categorical | `PILOT_SINGLE` | Study group designation. |
| `degree_major` | String | Categorical | `B_PHARM`, `BSC_CHEM`, `OTHER` | Academic degree program. |
| `year_of_study` | Integer | Years | `1` to `5` | Current academic year. |
| `prior_hplc_exp` | String | Categorical | `NONE`, `1_2_LABS`, `GT_3_LABS` | Self-reported prior physical HPLC laboratory experience. |
| `pre_score` | Integer | Points | `0` to `10` | Total pre-test score (sum of Q1–Q10). |
| `post_score` | Integer | Points | `0` to `10` | Total post-test score (sum of Q1–Q10). |
| `score_gain` | Integer | Points | `-10` to `+10` | Paired difference: `post_score - pre_score`. |
| `hake_gain` | Float | Ratio | `N/A`, `[-inf, 1.0]` | Normalized gain: `(post - pre) / (10 - pre)`. Set to `N/A` if `pre_score == 10`. |
| `pre_time_sec` | Integer | Seconds | `60` to `900` | Latency to complete pre-test. |
| `post_time_sec` | Integer | Seconds | `60` to `900` | Latency to complete post-test. |
| `task_alpha_correct` | Integer | Binary | `0, 1` | Practical task 1 (Fitting leak) correct diagnosis (0=No, 1=Yes). |
| `task_alpha_time_s` | Integer | Seconds | `10` to `300` | Time to submit diagnosis for Scenario Alpha. |
| `task_alpha_conf` | Integer | Likert | `1` to `5` | Diagnostic confidence for Scenario Alpha. |
| `task_beta_correct` | Integer | Binary | `0, 1` | Practical task 2 (Column void) correct diagnosis (0=No, 1=Yes). |
| `task_beta_time_s` | Integer | Seconds | `10` to `300` | Time to submit diagnosis for Scenario Beta. |
| `task_beta_conf` | Integer | Likert | `1` to `5` | Diagnostic confidence for Scenario Beta. |
| `task_gamma_correct`| Integer | Binary | `0, 1` | Practical task 3 (Air bubble) correct diagnosis (0=No, 1=Yes). |
| `task_gamma_time_s` | Integer | Seconds | `10` to `300` | Time to submit diagnosis for Scenario Gamma. |
| `task_gamma_conf` | Integer | Likert | `1` to `5` | Diagnostic confidence for Scenario Gamma. |
| `task_delta_correct`| Integer | Binary | `0, 1` | Practical task 4 (Contamination) correct diagnosis (0=No, 1=Yes). |
| `task_delta_time_s` | Integer | Seconds | `10` to `300` | Time to submit diagnosis for Scenario Delta. |
| `task_delta_conf` | Integer | Likert | `1` to `5` | Diagnostic confidence for Scenario Delta. |
| `task_total_score` | Integer | Points | `0` to `4` | Total practical diagnostic tasks answered correctly. |
| `mean_diag_time_s` | Float | Seconds | `10.0` to `300.0` | Average diagnostic latency across completed tasks. |
| `sus_q1` to `sus_q10` | Integer | Likert | `1` to `5` | Raw responses to Brooke SUS questions 1 through 10. |
| `sus_total` | Float | Index | `0.0` to `100.0` | Standard calculated Brooke SUS score. |
| `ux_u1` to `ux_u8` | Integer | Likert | `1` to `5` | Raw responses to targeted usability survey items. |
| `qual_easiest` | String | Free Text | Text | Verbatim response to qualitative prompt 1. |
| `qual_confusing` | String | Free Text | Text | Verbatim response to qualitative prompt 2. |
| `qual_hardest` | String | Free Text | Text | Verbatim response to qualitative prompt 3. |
| `qual_missing` | String | Free Text | Text | Verbatim response to qualitative prompt 4. |
| `qual_prelab_rec` | String | Free Text | Text | Verbatim response to qualitative prompt 5. |
| `qual_suggestions` | String | Free Text | Text | Verbatim response to qualitative prompt 6. |
"""

blank_csv_header = """participant_id,group,degree_major,year_of_study,prior_hplc_exp,pre_score,post_score,score_gain,hake_gain,pre_time_sec,post_time_sec,task_alpha_correct,task_alpha_time_s,task_alpha_conf,task_beta_correct,task_beta_time_s,task_beta_conf,task_gamma_correct,task_gamma_time_s,task_gamma_conf,task_delta_correct,task_delta_time_s,task_delta_conf,task_total_score,mean_diag_time_s,sus_q1,sus_q2,sus_q3,sus_q4,sus_q5,sus_q6,sus_q7,sus_q8,sus_q9,sus_q10,sus_total,ux_u1,ux_u2,ux_u3,ux_u4,ux_u5,ux_u6,ux_u7,ux_u8,qual_easiest,qual_confusing,qual_hardest,qual_missing,qual_prelab_rec,qual_suggestions"""

data_entry_instructions = """# DATA ENTRY & AUDITING PROTOCOL
**Document ID:** P4-ENTRY-2026-REV1  
**Integrity Rule:** Zero Simulated Data Allowed in Participant Template  

---

## 1. DATA ENTRY WORKFLOW
1. **Source Documents:** Collect paper assessment packets containing:
   - Signed Informed Consent Sheet (stored in separate ethical binder).
   - Pre-Test Sheet with Participant ID code.
   - Diagnostic Performance Task Sheet.
   - Post-Test, SUS, and Qualitative Survey Sheet.
2. **Double-Blind Entry Protocol:**
   - Entry Operator A enters all numeric scores and Likert responses into `entry_batch_A.csv`.
   - Entry Operator B independently enters identical sheets into `entry_batch_B.csv`.
   - Automated discrepancy script flags any mismatch between Batch A and Batch B.
   - Discrepancies adjudicated by direct inspection of physical paper sheet.
3. **Consolidation:** The reconciled, audited records are saved into `participant_data_template.csv`.

---

## 2. STRICT NON-FABRICATION RULE
- **The primary template `participant_data_template.csv` must remain strictly empty (headers only) until real university students execute the pilot.**
- Under no circumstances may simulated, estimated, or synthetic participant records be placed in this file.
- Demonstration data used for verifying analysis pipelines are strictly sequestered in `06_ANALYSIS/test_data/DEMO_DATA_NOT_REAL.csv`.
"""

write_both("05_DATA_TEMPLATES/anonymized_data_dictionary.md", data_dictionary)
write_both("05_DATA_TEMPLATES/participant_data_template.csv", blank_csv_header)
write_both("05_DATA_TEMPLATES/data_entry_instructions.md", data_entry_instructions)

# ==============================================================================
# 06_ANALYSIS
# ==============================================================================

analysis_plan = """# ANALYSIS EXECUTION PROTOCOL & SCRIPT SPECIFICATIONS
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
"""

calc_stats_code = """import sys
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
    
    print(f"\\nSample Size (N): {n}")
    print(f"Pre-Test Mean (SD): {np.mean(pre):.2f} ({np.std(pre, ddof=1):.2f}) | Median (IQR): {np.median(pre):.1f} ({stats.iqr(pre):.1f})")
    print(f"Post-Test Mean (SD): {np.mean(post):.2f} ({np.std(post, ddof=1):.2f}) | Median (IQR): {np.median(post):.1f} ({stats.iqr(post):.1f})")
    print(f"Mean Gain (SD): {np.mean(diff):+.2f} ({np.std(diff, ddof=1):.2f}) | Median Gain: {np.median(diff):+.1f}")
    
    # 1. Normality Assessment (Shapiro-Wilk)
    stat_sw, p_sw = stats.shapiro(diff)
    print(f"\\nShapiro-Wilk Test of Differences: W = {stat_sw:.4f}, p = {p_sw:.4f}")
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
    
    print(f"\\n--- Parametric Analysis (Paired t-test) ---")
    print(f"t({n-1}) = {t_stat:.3f}, p-value = {p_val_t:.4e}")
    print(f"95% CI of Mean Difference: [{ci_low:+.2f}, {ci_high:+.2f}] points")
    print(f"Effect Size (Cohen's d_z): {cohen_dz:.2f}")
    
    # 3. Wilcoxon Signed-Rank Test
    w_stat, p_val_w = stats.wilcoxon(post, pre, zero_method='wilcox', correction=True)
    # Rank biserial r
    r_biserial = 1.0 - (2.0 * w_stat) / (n * (n + 1) / 2.0)
    print(f"\\n--- Non-Parametric Analysis (Wilcoxon Signed-Rank) ---")
    print(f"W = {w_stat:.1f}, p-value = {p_val_w:.4e}")
    print(f"Effect Size (Rank-Biserial r): {r_biserial:.2f}")
    print("==================================================")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'participant_data_template.csv'
    analyze_pre_post(path)
"""

calc_sus_code = """import sys
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
    
    print(f"\\nMean SUS Score: {mean_sus:.2f} (SD: {sd_sus:.2f})")
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
"""

calc_hake_code = """import sys
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
            
    print(f"\\nOverall Average Normalized Gain <g>: {overall_g:.3f}")
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
"""

demo_csv_content = """participant_id,group,degree_major,year_of_study,prior_hplc_exp,pre_score,post_score,score_gain,hake_gain,pre_time_sec,post_time_sec,task_alpha_correct,task_alpha_time_s,task_alpha_conf,task_beta_correct,task_beta_time_s,task_beta_conf,task_gamma_correct,task_gamma_time_s,task_gamma_conf,task_delta_correct,task_delta_time_s,task_delta_conf,task_total_score,mean_diag_time_s,sus_q1,sus_q2,sus_q3,sus_q4,sus_q5,sus_q6,sus_q7,sus_q8,sus_q9,sus_q10,sus_total,ux_u1,ux_u2,ux_u3,ux_u4,ux_u5,ux_u6,ux_u7,ux_u8,qual_easiest,qual_confusing,qual_hardest,qual_missing,qual_prelab_rec,qual_suggestions
DEMO_01,PILOT_SINGLE,B_PHARM,3,NONE,4,8,4,0.67,420,380,1,45,4,1,60,5,1,35,4,0,80,3,3,55.0,4,2,4,2,4,2,4,2,4,2,75.0,4,4,5,4,5,4,5,5,Seeing real-time peaks,Gradient parameters,Contamination ghost peaks,UV absorbance spectrum,Yes very helpful,Add autosampler animation
DEMO_02,PILOT_SINGLE,B_PHARM,3,1_2_LABS,5,9,4,0.80,390,340,1,40,5,1,50,4,1,30,5,1,65,4,4,46.25,5,1,5,1,5,1,5,1,5,1,100.0,5,5,5,5,5,5,5,5,Instant fault injection,Flow rate unit conversion,None,Baseline zoom button,Definitely,More drug compounds
DEMO_03,PILOT_SINGLE,BSC_CHEM,3,NONE,3,7,4,0.57,480,410,1,55,3,0,90,2,1,45,4,1,70,3,3,65.0,4,3,4,2,4,2,4,3,3,2,65.0,4,3,4,3,4,4,4,4,Pressure gauge feedback,Peak split mechanism,Column void,Dwell volume indicator,Yes,More explanation on split peaks"""

readme_analysis = """# ANALYSIS CODE & VERIFICATION SUITE
**Directory:** `SIMUPHARM_PHASE4_EDUCATIONAL_VALIDATION/06_ANALYSIS/`  

---

## CONTENTS
- `analysis_plan.md`: Formal mathematical plan for computing inferential statistics.
- `analysis_code/calculate_pre_post_stats.py`: Automated paired difference testing script.
- `analysis_code/calculate_sus_score.py`: Automated Brooke SUS calculation script.
- `analysis_code/calculate_hake_gain.py`: Automated Hake normalized gain script.
- `test_data/DEMO_DATA_NOT_REAL.csv`: Explicitly labeled synthetic test data used strictly to verify that Python analysis scripts run smoothly prior to real data collection.

## HOW TO RUN
To verify scripts using the demo dataset:
```bash
python analysis_code/calculate_pre_post_stats.py test_data/DEMO_DATA_NOT_REAL.csv
python analysis_code/calculate_sus_score.py test_data/DEMO_DATA_NOT_REAL.csv
python analysis_code/calculate_hake_gain.py test_data/DEMO_DATA_NOT_REAL.csv
```

When real participant data is collected, execute:
```bash
python analysis_code/calculate_pre_post_stats.py ../05_DATA_TEMPLATES/participant_data_template.csv
```
"""

write_both("06_ANALYSIS/analysis_plan.md", analysis_plan)
write_both("06_ANALYSIS/README.md", readme_analysis)
write_both("06_ANALYSIS/analysis_code/calculate_pre_post_stats.py", calc_stats_code)
write_both("06_ANALYSIS/analysis_code/calculate_sus_score.py", calc_sus_code)
write_both("06_ANALYSIS/analysis_code/calculate_hake_gain.py", calc_hake_code)
write_both("06_ANALYSIS/test_data/DEMO_DATA_NOT_REAL.csv", demo_csv_content)

print("--- PART 3 COMPLETED (Folders 04, 05, and 06) ---")
