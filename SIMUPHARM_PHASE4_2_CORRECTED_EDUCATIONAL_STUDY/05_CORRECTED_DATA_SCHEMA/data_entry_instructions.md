# Double-Blind Data Entry & Schema Auditing Protocol
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
