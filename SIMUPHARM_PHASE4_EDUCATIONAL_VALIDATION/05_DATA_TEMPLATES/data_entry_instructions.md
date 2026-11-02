# DATA ENTRY & AUDITING PROTOCOL
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
