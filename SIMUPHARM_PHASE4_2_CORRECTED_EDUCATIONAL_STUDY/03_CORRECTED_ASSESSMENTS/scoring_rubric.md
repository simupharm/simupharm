# Standardized 24-Point Practical Diagnostic Scoring Rubric
**Document ID:** P4.2.1-RUBRIC-2026-REV2.1 (FINAL PROTOCOL FREEZE)  
**Target:** Standardized Double-Rater Evaluation of Practical Diagnostic Tasks  
**Scale:** 0 to 6 Points per Scenario $\times$ 4 Scenarios = **0 to 24 Points Grand Total**  
**Scoring Method:** Two independent faculty raters; discrepancies $>1$ point adjudicated via consensus.  

---

## 1. Resolution of Scoring Architecture & Statistical Description
In Phase 4, documents conflicted between a 3-point/12-point rubric and a 6-point/24-point rubric. In Phase 4.2.1, the 24-point analytical architecture (0–6 points per scenario across 4 tasks) is permanently locked:
- **Statistical Description:** The graduated 24-point rubric provides greater scoring resolution than binary component scoring and allows partial understanding to be distinguished from incorrect or incomplete responses. It is an ordinal composite score (not continuous data).
- **Psychometric Reliability:** A 0–2 scale per component provides sufficient gradation to compute Weighted Cohen's Kappa ($\kappa_w$) and Intraclass Correlation Coefficients (ICC[2,1]) between independent raters.

---

## 2. Analytical Scoring Dimensions (0 to 6 Points per Scenario)

### Component A: Fault Identification (0 to 2 Points)
- **2 Points (Exact Identification):** Correctly identifies the specific fault (e.g., "Fitting Leak upstream of column", "Column Inlet Void / Bed Collapse", "Pump Check Valve Air Bubble / Cavitation", "Mobile Phase Contamination / Ghost Peaks").
- **1 Point (Partial Identification):** Identifies the general module or fluidic anomaly but lacks specificity (e.g., "Fluidic loss / flow problem", "Column packing defect", "Pump delivery irregularity", "Chemical impurity").
- **0 Points (Incorrect):** Names an unrelated or physically impossible fault (e.g., identifies cavitation as "detector lamp failure", identifies void as "solvent evaporation").

### Component B: Physical & Fluidic Reasoning (0 to 2 Points)
- **2 Points (Sound Mechanistic Explanation):** Accurately explains the underlying fluidic/chemical mechanism linking symptom to cause (e.g., "Loss of flow before column decreases superficial linear velocity $u$, increasing retention time $t_R = L/u$ and reducing Darcy pressure $\Delta P$").
- **1 Point (Partial Mechanistic Explanation):** Identifies the primary physical factor (e.g., mentions "lower flow rate") but fails to explain why retention increases or pressure drops.
- **0 Points (Incorrect / Absent):** Provides no explanation, cites an incorrect physical mechanism, or merely repeats the visual symptom.

### Component C: Corrective Troubleshooting Action (0 to 2 Points)
- **2 Points (Targeted SOP Action):** Specifies the standard chromatographic corrective action (e.g., "Inspect and tighten fitting at column inlet", "Invert column and flush or replace inlet frit/guard column", "Open purge valve and flush with degassed solvent at high flow", "Prepare fresh mobile phase with HPLC-grade water").
- **1 Point (Generic Safe Action):** Suggests a safe general troubleshooting step that does not directly solve the root cause (e.g., "Stop pump and check connections", "Rerun sample", "Call lab technician").
- **0 Points (Incorrect / Unsafe Action):** Suggests an action that would damage instrumentation or worsen the fault (e.g., "Increase flow rate to 5 mL/min through column", "Sonicate packed analytical column").

---

## 3. Inter-Rater Reliability Protocol
1. Rater 1 and Rater 2 independently score all participant response sheets blind to participant identity and each other's marks.
2. Total scenario scores (0–6) and grand total scores (0–24) are recorded separately in `rater1_grand_total` and `rater2_grand_total`.
3. If $| \text{Rater 1} - \text{Rater 2} | > 1$ point on any scenario, raters hold an adjudication conference to reach consensus. The agreed score is recorded in `task_rubric_grand_total`.
4. Pre-adjudication scores are used to evaluate inter-rater reliability using two mathematically distinct metrics:
   - **Component-Level Ordinal Agreement:** Weighted Cohen's Kappa ($\kappa_w$, linear weighting) evaluated across the 0–2 ordinal ratings for each individual component (Fault ID, Physical Reasoning, Action Plan).
   - **Grand-Total Score Reliability:** Intraclass Correlation Coefficient $\text{ICC}(2,1)$ (two-way random effects, single rater, absolute agreement) evaluated on the composite 0–24 grand total.
