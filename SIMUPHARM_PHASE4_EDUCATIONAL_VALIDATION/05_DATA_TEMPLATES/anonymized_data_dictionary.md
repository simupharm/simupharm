# ANONYMIZED DATA DICTIONARY & VARIABLE SCHEMA
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
