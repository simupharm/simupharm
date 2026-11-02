# Reconciled Anonymized Participant Data Dictionary
**Document ID:** P4.2-DATA-DICT-2026-REV2  
**Target:** Variable Definitions, Valid Ranges, and Storage Formats  
**Associated Template:** `participant_data_template.csv`  

---

| Variable Name | Data Type | Permissible Range | Null Allowed? | Description & Coding Rules |
| :--- | :---: | :---: | :---: | :--- |
| `participant_id` | String | `P01`–`P99` | NO | Unique anonymous identifier assigned to participant envelope. |
| `degree_program` | Categorical | `B.Pharm`, `Chemistry`, `Other` | NO | Student academic enrollment program. |
| `prior_hplc_lab` | Binary | `0`, `1` | NO | Prior hands-on physical HPLC laboratory experience ($0 = 	ext{No}, 1 = 	ext{Yes}$). |
| `pre_q1` to `pre_q10` | Binary | `0`, `1` | YES (NaN) | Item-level score on pre-test ($0 = 	ext{Incorrect}, 1 = 	ext{Correct}$). |
| `pre_test_total` | Integer | `0` to `10` | YES (NaN) | Sum of pre-test item scores ($\ge 1$ blank item results in `NaN`). |
| `post_q1` to `post_q10` | Binary | `0`, `1` | YES (NaN) | Item-level score on post-test ($0 = 	ext{Incorrect}, 1 = 	ext{Correct}$). |
| `post_test_total` | Integer | `0` to `10` | YES (NaN) | Sum of post-test item scores ($\ge 1$ blank item results in `NaN`). |
| `score_gain` | Integer | `-10` to `+10` | YES (NaN) | Paired Troubleshooting Gain ($\Delta	ext{Score} = 	ext{post\_test\_total} - 	ext{pre\_test\_total}$). |
| `hake_gain` | Float | `0.00` to `1.00`, `NaN` | YES (NaN) | Normalized gain: $rac{	ext{Post} - 	ext{Pre}}{10 - 	ext{Pre}}$. If $	ext{Pre} = 10$, coded as `NaN`. |
| `task_alpha_id_score` | Integer | `0`, `1`, `2` | NO | Fault identification score for Scenario Alpha (Fitting Leak). |
| `task_alpha_reason_score`| Integer | `0`, `1`, `2` | NO | Physical reasoning score for Scenario Alpha. |
| `task_alpha_action_score`| Integer | `0`, `1`, `2` | NO | Corrective action score for Scenario Alpha. |
| `task_alpha_rubric_total`| Integer | `0` to `6` | NO | Total rubric score for Scenario Alpha ($= 	ext{ID} + 	ext{Reason} + 	ext{Action}$). |
| `task_alpha_time_s` | Integer | `10` to `300` | YES (NaN) | Diagnostic latency in seconds for Scenario Alpha. |
| `task_alpha_conf` | Integer | `1` to `5` | NO | Subjective confidence rating for Scenario Alpha ($1 = 	ext{Guess}, 5 = 	ext{Certain}$). |
| `task_beta_id_score` ... | Integer | `0` to `2` | NO | Corresponding columns for Scenario Beta (Column Void). |
| `task_gamma_id_score` ...| Integer | `0` to `2` | NO | Corresponding columns for Scenario Gamma (Air Bubble). |
| `task_delta_id_score` ...| Integer | `0` to `2` | NO | Corresponding columns for Scenario Delta (Contamination). |
| `rater1_grand_total` | Integer | `0` to `24` | NO | Independent grand total rubric score awarded by Faculty Rater 1. |
| `rater2_grand_total` | Integer | `0` to `24` | NO | Independent grand total rubric score awarded by Faculty Rater 2. |
| `task_rubric_grand_total`| Integer | `0` to `24` | NO | Final adjudicated practical diagnostic score across all 4 scenarios. |
| `sus_q1` to `sus_q10` | Integer | `1` to `5` | YES (Impute) | Canonical Brooke SUS item responses ($1 = 	ext{SD}, 5 = 	ext{SA}$). |
| `sus_total_score` | Float | `0.0` to `100.0` | YES (NaN) | Composite System Usability Scale score (Brooke 1996 formula). |
| `ux_u1` to `ux_u8` | Integer | `1` to `5` | YES (NaN) | Targeted pedagogical usability ratings ($1 = 	ext{SD}, 5 = 	ext{SA}$). |
