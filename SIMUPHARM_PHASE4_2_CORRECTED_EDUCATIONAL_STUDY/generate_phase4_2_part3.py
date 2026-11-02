import os
import sys

dir_primary = r"c:\Users\dsant\OneDrive\simupro - Copy\SIMUPHARM_PHASE4_2_CORRECTED_EDUCATIONAL_STUDY"
dir_artifact = r"C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\SIMUPHARM_PHASE4_2_CORRECTED_EDUCATIONAL_STUDY"

def write_both(rel_path, content):
    p1 = os.path.join(dir_primary, rel_path)
    p2 = os.path.join(dir_artifact, rel_path)
    os.makedirs(os.path.dirname(p1), exist_ok=True)
    os.makedirs(os.path.dirname(p2), exist_ok=True)
    with open(p1, "w", encoding="utf-8") as f:
        f.write(content)
    with open(p2, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {rel_path} ({len(content)} bytes)")

# =========================================================================
# 04_CORRECTED_USABILITY
# =========================================================================

# 1. SUS_instrument.md (Canonical Brooke 1996 Wording Restored)
sus_content = """# Canonical System Usability Scale (SUS) Instrument
**Document ID:** P4.2-SUS-2026-REV2  
**Standard Citation:** Brooke, J. (1996). *SUS: A 'quick and dirty' usability scale.* Usability Evaluation in Industry, 189(194), 4–7.  
**Instrument Classification:** Standard Unmodified Brooke (1996) System Usability Scale  
**Scale:** 1 (Strongly Disagree) to 5 (Strongly Agree)  

---

**Participant ID Code:** ____________________  

### Instructions for Participants
Please rate each statement based on your immediate reaction to using the SimuPharm simulator today. Do not spend too much time on any single statement; your first impression is the most valuable. All statements must be answered.

| # | Statement | 1<br/>Strongly Disagree | 2<br/>Disagree | 3<br/>Neutral | 4<br/>Agree | 5<br/>Strongly Agree |
| :-: | :--- | :-: | :-: | :-: | :-: | :-: |
| **Q1** | I think that I would like to use this system frequently. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q2** | I found the system unnecessarily complex. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q3** | I thought the system was easy to use. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q4** | I think that I would need the support of a technical person to be able to use this system. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q5** | I found the various functions in this system were well integrated. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q6** | I thought there was too much inconsistency in this system. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q7** | I would imagine that most people would learn to use this system very quickly. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q8** | I found the system very cumbersome to use. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q9** | I felt very confident using the system. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **Q10**| I needed to learn a lot of things before I could get going with this system. | [ ] | [ ] | [ ] | [ ] | [ ] |

---

### Standard Scoring Algorithm (Brooke 1996)
1. For odd-numbered items (Q1, Q3, Q5, Q7, Q9), score contribution = $\text{User Response} - 1$ (range 0 to 4).
2. For even-numbered items (Q2, Q4, Q6, Q8, Q10), score contribution = $5 - \text{User Response}$ (range 0 to 4).
3. Sum the 10 score contributions and multiply by 2.5:
   $$\text{SUS Score} = 2.5 \times \left[ \sum_{i \in \{1,3,5,7,9\}} (R_i - 1) + \sum_{j \in \{2,4,6,8,10\}} (5 - R_j) \right]$$
4. Final score ranges from 0 to 100 points. Benchmark percentile curves follow Bangor et al. (2008) and Sauro & Lewis (2016).
"""
write_both("04_CORRECTED_USABILITY/SUS_instrument.md", sus_content)

# 2. usability_questionnaire.md (Isolated Targeted UX Items)
ux_content = """# Targeted Pedagogical Usability Questionnaire
**Document ID:** P4.2-UX-SURVEY-2026-REV2  
**Target:** Evaluation of Domain-Specific HPLC Educational Features (Kept Strictly Separate from SUS)  
**Scale:** 1 (Strongly Disagree) to 5 (Strongly Agree)  

---

**Participant ID Code:** ____________________  

| Variable | Statement | 1<br/>SD | 2<br/>D | 3<br/>N | 4<br/>A | 5<br/>SA |
| :---: | :--- | :-: | :-: | :-: | :-: | :-: |
| `ux_u1` | The real-time chromatographic canvas helped me understand how peaks separate. | [ ] | [ ] | [ ] | [ ] | [ ] |
| `ux_u2` | Adjusting the solvent composition slider (% B) clearly illustrated retention changes. | [ ] | [ ] | [ ] | [ ] | [ ] |
| `ux_u3` | The simulated pressure gauge made it easy to detect instrument fluidic leaks. | [ ] | [ ] | [ ] | [ ] | [ ] |
| `ux_u4` | The visual baseline spikes clearly demonstrated pump cavitation behavior. | [ ] | [ ] | [ ] | [ ] | [ ] |
| `ux_u5` | The split peaks shown during column voiding helped me connect bed collapse to peak shape. | [ ] | [ ] | [ ] | [ ] | [ ] |
| `ux_u6` | The simulator was intuitive to navigate without requiring external assistance. | [ ] | [ ] | [ ] | [ ] | [ ] |
| `ux_u7` | Practicing on the simulator increased my confidence in troubleshooting physical HPLC systems. | [ ] | [ ] | [ ] | [ ] | [ ] |
| `ux_u8` | I would recommend this simulation tool to other chemistry and pharmacy students. | [ ] | [ ] | [ ] | [ ] | [ ] |
"""
write_both("04_CORRECTED_USABILITY/usability_questionnaire.md", ux_content)

# 3. qualitative_feedback_form.md
qual_content = """# Qualitative Learning Experience Form
**Document ID:** P4.2-QUAL-2026-REV2  
**Target:** Open-Ended Participant Reflections & Inductive Thematic Coding  

---

**Participant ID Code:** ____________________  

### 1. Diagnostic Learning & Concept Clarification
*Which simulated instrument fault was the easiest to identify, and which was the most difficult? Explain why.*  
__________________________________________________________________________  
__________________________________________________________________________  
__________________________________________________________________________  

### 2. Interface Usability & Visual Feedback
*What specific visual or numeric feature of the SimuPharm simulator was most useful in helping you diagnose faults (e.g., pressure gauge, peak shape, retention time, baseline noise)?*  
__________________________________________________________________________  
__________________________________________________________________________  
__________________________________________________________________________  

### 3. Suggested Improvements & Challenges
*Did you experience any confusion, technical difficulties, or unrealistic behavior while using the simulator? What would you improve?*  
__________________________________________________________________________  
__________________________________________________________________________  
__________________________________________________________________________  
"""
write_both("04_CORRECTED_USABILITY/qualitative_feedback_form.md", qual_content)

# =========================================================================
# 05_CORRECTED_DATA_SCHEMA
# =========================================================================

# 4. participant_data_template.csv (Reconciled Schema with 24-pt Rubric & Raters)
header_columns = [
    "participant_id", "degree_program", "prior_hplc_lab",
    "pre_q1", "pre_q2", "pre_q3", "pre_q4", "pre_q5", "pre_q6", "pre_q7", "pre_q8", "pre_q9", "pre_q10", "pre_test_total",
    "post_q1", "post_q2", "post_q3", "post_q4", "post_q5", "post_q6", "post_q7", "post_q8", "post_q9", "post_q10", "post_test_total",
    "score_gain", "hake_gain",
    "task_alpha_id_score", "task_alpha_reason_score", "task_alpha_action_score", "task_alpha_rubric_total", "task_alpha_time_s", "task_alpha_conf",
    "task_beta_id_score", "task_beta_reason_score", "task_beta_action_score", "task_beta_rubric_total", "task_beta_time_s", "task_beta_conf",
    "task_gamma_id_score", "task_gamma_reason_score", "task_gamma_action_score", "task_gamma_rubric_total", "task_gamma_time_s", "task_gamma_conf",
    "task_delta_id_score", "task_delta_reason_score", "task_delta_action_score", "task_delta_rubric_total", "task_delta_time_s", "task_delta_conf",
    "rater1_grand_total", "rater2_grand_total", "task_rubric_grand_total",
    "sus_q1", "sus_q2", "sus_q3", "sus_q4", "sus_q5", "sus_q6", "sus_q7", "sus_q8", "sus_q9", "sus_q10", "sus_total_score",
    "ux_u1", "ux_u2", "ux_u3", "ux_u4", "ux_u5", "ux_u6", "ux_u7", "ux_u8"
]
csv_content = ",".join(header_columns) + "\n"
write_both("05_CORRECTED_DATA_SCHEMA/participant_data_template.csv", csv_content)

# 5. anonymized_data_dictionary.md (Comprehensive Variable Codebook)
data_dict = """# Reconciled Anonymized Participant Data Dictionary
**Document ID:** P4.2-DATA-DICT-2026-REV2  
**Target:** Variable Definitions, Valid Ranges, and Storage Formats  
**Associated Template:** `participant_data_template.csv`  

---

| Variable Name | Data Type | Permissible Range | Null Allowed? | Description & Coding Rules |
| :--- | :---: | :---: | :---: | :--- |
| `participant_id` | String | `P01`–`P99` | NO | Unique anonymous identifier assigned to participant envelope. |
| `degree_program` | Categorical | `B.Pharm`, `Chemistry`, `Other` | NO | Student academic enrollment program. |
| `prior_hplc_lab` | Binary | `0`, `1` | NO | Prior hands-on physical HPLC laboratory experience ($0 = \text{No}, 1 = \text{Yes}$). |
| `pre_q1` to `pre_q10` | Binary | `0`, `1` | YES (NaN) | Item-level score on pre-test ($0 = \text{Incorrect}, 1 = \text{Correct}$). |
| `pre_test_total` | Integer | `0` to `10` | YES (NaN) | Sum of pre-test item scores ($\ge 1$ blank item results in `NaN`). |
| `post_q1` to `post_q10` | Binary | `0`, `1` | YES (NaN) | Item-level score on post-test ($0 = \text{Incorrect}, 1 = \text{Correct}$). |
| `post_test_total` | Integer | `0` to `10` | YES (NaN) | Sum of post-test item scores ($\ge 1$ blank item results in `NaN`). |
| `score_gain` | Integer | `-10` to `+10` | YES (NaN) | Paired Troubleshooting Gain ($\Delta\text{Score} = \text{post\_test\_total} - \text{pre\_test\_total}$). |
| `hake_gain` | Float | `0.00` to `1.00`, `NaN` | YES (NaN) | Normalized gain: $\frac{\text{Post} - \text{Pre}}{10 - \text{Pre}}$. If $\text{Pre} = 10$, coded as `NaN`. |
| `task_alpha_id_score` | Integer | `0`, `1`, `2` | NO | Fault identification score for Scenario Alpha (Fitting Leak). |
| `task_alpha_reason_score`| Integer | `0`, `1`, `2` | NO | Physical reasoning score for Scenario Alpha. |
| `task_alpha_action_score`| Integer | `0`, `1`, `2` | NO | Corrective action score for Scenario Alpha. |
| `task_alpha_rubric_total`| Integer | `0` to `6` | NO | Total rubric score for Scenario Alpha ($= \text{ID} + \text{Reason} + \text{Action}$). |
| `task_alpha_time_s` | Integer | `10` to `300` | YES (NaN) | Diagnostic latency in seconds for Scenario Alpha. |
| `task_alpha_conf` | Integer | `1` to `5` | NO | Subjective confidence rating for Scenario Alpha ($1 = \text{Guess}, 5 = \text{Certain}$). |
| `task_beta_id_score` ... | Integer | `0` to `2` | NO | Corresponding columns for Scenario Beta (Column Void). |
| `task_gamma_id_score` ...| Integer | `0` to `2` | NO | Corresponding columns for Scenario Gamma (Air Bubble). |
| `task_delta_id_score` ...| Integer | `0` to `2` | NO | Corresponding columns for Scenario Delta (Contamination). |
| `rater1_grand_total` | Integer | `0` to `24` | NO | Independent grand total rubric score awarded by Faculty Rater 1. |
| `rater2_grand_total` | Integer | `0` to `24` | NO | Independent grand total rubric score awarded by Faculty Rater 2. |
| `task_rubric_grand_total`| Integer | `0` to `24` | NO | Final adjudicated practical diagnostic score across all 4 scenarios. |
| `sus_q1` to `sus_q10` | Integer | `1` to `5` | YES (Impute) | Canonical Brooke SUS item responses ($1 = \text{SD}, 5 = \text{SA}$). |
| `sus_total_score` | Float | `0.0` to `100.0` | YES (NaN) | Composite System Usability Scale score (Brooke 1996 formula). |
| `ux_u1` to `ux_u8` | Integer | `1` to `5` | YES (NaN) | Targeted pedagogical usability ratings ($1 = \text{SD}, 5 = \text{SA}$). |
"""
write_both("05_CORRECTED_DATA_SCHEMA/anonymized_data_dictionary.md", data_dict)

# 6. data_entry_instructions.md
entry_instr = """# Double-Blind Data Entry & Schema Auditing Protocol
**Document ID:** P4.2-ENTRY-INSTR-2026-REV2  
**Target:** Standard Operating Procedure for Converting Paper Responses to Digital Dataset  

---

## 1. Governance Rules
1. **Zero Data Fabrication:** Data entry personnel may ONLY transcribe physical student responses from verified paper assessment envelopes.
2. **Double-Blind Independent Entry:**
   - Clerk A enters all paper response packets into `data_entry_pass1.csv`.
   - Clerk B independently enters the same packets into `data_entry_pass2.csv`.
   - A reconciliation script compares Pass 1 and Pass 2 cell-by-cell. Any discrepancies are flagged and resolved by inspecting the physical sheet.
   - The verified dataset is exported to `participant_data_template.csv`.
3. **Missing Value Coding:**
   - Blank multiple-choice pre/post-test questions: enter `NaN`.
   - Blank SUS items: enter `NaN` (analysis code will apply Sauro 2016 single/double item imputation).
   - Skipped practical scenario: enter `0` for scores; enter `NaN` for latency.
"""
write_both("05_CORRECTED_DATA_SCHEMA/data_entry_instructions.md", entry_instr)

print("Part 3 generation complete.")
