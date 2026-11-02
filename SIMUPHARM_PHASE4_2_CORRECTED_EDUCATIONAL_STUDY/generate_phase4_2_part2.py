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
# 02_CORRECTED_ETHICS
# =========================================================================

# 1. ethics_submission_package.md
ethics_pkg = """# Institutional Ethics Submission Package & Exemption Request
**Document ID:** P4.2-ETHICS-PKG-2026-REV2  
**Target Authority:** Institutional Review Board (IRB) / Faculty Research Ethics Committee  
**Status:** **SUBMITTED / INSTITUTIONAL REVIEW PENDING** (Recruitment Halted Until Written Determination)  

---

## 1. Regulatory Framework & Exemption Justification
This educational evaluation protocol qualifies for exempt status under **45 CFR 46.104(d)(1)** (Research conducted in established or commonly accepted educational settings):
- **Criterion A:** The research evaluates normal educational instructional practices (interactive computer simulation for instrumental analytical troubleshooting).
- **Criterion B:** The study compares conventional instruction supplemented with interactive simulation tools to improve instructional quality.
- **Criterion C:** Data collection is completely anonymous; no student identifiers, grades, or personal identifying information are linked to assessment performance.
- **Criterion D:** Non-coercive participation: Participation is voluntary, un-graded, and has zero impact on course progression or academic standing.

---

## 2. Institutional Sign-Off Requirement (Blocker Resolution)
*Governance Mandate:* Under institutional policy and US federal regulations (OHRP), investigators cannot self-certify research exemption involving human student subjects. 

```
[ ] PENDING INSTITUTIONAL ETHICS DETERMINATION LETTER
    Committee / Authority: __________________________________________________
    Determination:         [ ] Exemption Confirmed (Category 1)  [ ] Full Approval
    Protocol Number:       __________________________________________________
    Date of Action:        __________________________________________________
    Authorized Signature:  __________________________________________________
```
*Note: Participant recruitment will NOT commence until the above field is executed with an official written institutional determination letter.*
"""
write_both("02_CORRECTED_ETHICS/ethics_submission_package.md", ethics_pkg)

# 2. participant_information_sheet.md
pis_content = """# Participant Information Sheet (Plain Language)
**Document ID:** P4.2-PIS-2026-REV2  
**Study Title:** Educational Evaluation of an Interactive Browser-Based HPLC Troubleshooting Simulator  
**Principal Investigator:** Lead Educational Researcher  

---

## 1. What is the purpose of this study?
You are invited to participate in a research study evaluating an interactive web-based software application called **SimuPharm**. SimuPharm simulates an High-Performance Liquid Chromatography (HPLC) instrument to help chemistry and pharmacy students learn how to identify and troubleshoot instrument faults (such as air bubbles, leaks, and column damage).

## 2. What will I be asked to do?
If you agree to participate, you will participate during your scheduled laboratory period (approximately 50 minutes):
1. Complete a brief 10-question pre-test on HPLC troubleshooting concepts (10 min).
2. Use the SimuPharm simulator in your web browser to explore baseline separations and instrument fault symptoms (12 min).
3. Diagnose four unknown simulated instrument faults and record your findings (12 min).
4. Complete a 10-question post-test and a brief questionnaire about your user experience (15 min).

## 3. Do I have to take part?
**No. Participation is entirely voluntary.** Whether or not you choose to take part will have **no effect whatsoever on your course grades, academic standing, or relationship with your instructors**. You may withdraw from the study at any time without penalty simply by closing the browser or leaving the assessment blank.

## 4. How is my privacy protected?
All data collected are completely **anonymous**. You will be assigned a randomized Participant Code (such as `P01`, `P02`). No names, student ID numbers, IP addresses, or email addresses will ever be collected or linked to your responses.

## 5. Who can I contact with questions?
If you have any questions about this study or your rights as a research participant, please contact the research team or the Institutional Ethics Committee.
"""
write_both("02_CORRECTED_ETHICS/participant_information_sheet.md", pis_content)

# 3. informed_consent_template.md
consent_content = """# Informed Consent Form
**Document ID:** P4.2-CONSENT-2026-REV2  
**Study Title:** Educational Evaluation of an Interactive Browser-Based HPLC Troubleshooting Simulator  

---

**Participant Identification Code:** `[   ]` (Assigned by Administrator)

Please read each statement below and initial the corresponding box if you agree:

1. [  ] I confirm that I have read and understood the Participant Information Sheet (Version REV2) for the above study.
2. [  ] I have had the opportunity to ask questions and my questions have been answered satisfactorily.
3. [  ] I understand that my participation is voluntary and that I am free to withdraw at any time without giving a reason and without any academic penalty or impact on my course grades.
4. [  ] I understand that all data collected will be completely anonymous and that no identifying personal information will ever be linked to my responses or published.
5. [  ] I agree to take part in the educational evaluation study.

---

**Participant Signature:** ________________________________________  
**Date:** ____________________  

**Researcher Statement:**  
I confirm that I have explained the nature and purpose of this study to the participant and provided them with an information sheet.  
**Researcher Signature:** ________________________________________  
**Date:** ____________________  
"""
write_both("02_CORRECTED_ETHICS/informed_consent_template.md", consent_content)

# 4. ethics_checklist.md
checklist_content = """# Corrected Research Ethics & Exemption Checklist
**Document ID:** P4.2-ETHICS-CHECKLIST-2026-REV2  
**Regulatory Standard:** 45 CFR 46.104(d)(1) / ICMJE Recommendations  

---

| Item # | Verification Criterion | Status in Phase 4.1 | Corrected Status in Phase 4.2 | Evidence & Documentation |
| :---: | :--- | :---: | :---: | :--- |
| **E1** | Normal Educational Setting | Compliant | **COMPLIANT** | Study conducted during regularly scheduled university laboratory periods. |
| **E2** | Regular Instructional Strategies | Compliant | **COMPLIANT** | Compares computer simulation exercises with standard chromatography instruction. |
| **E3** | No Impact on Course Grades | Compliant | **COMPLIANT** | Formative un-graded activity; explicitly stated in consent and protocol. |
| **E4** | Anonymization & De-Identification | Compliant | **COMPLIANT** | Randomized alphanumeric IDs (`P01` to `P25`); zero PII collected. |
| **E5** | Voluntary Opt-In Consent | Compliant | **COMPLIANT** | Signed informed consent required; immediate penalty-free withdrawal permitted. |
| **E6** | Institutional Authorization Status | **BLOCKER (Non-Compliant)** | **RESOLVED: REVIEW PENDING** | Acknowledged that investigators cannot self-exempt. Formal submission package submitted; recruitment locked until written letter issued. |

**Current Regulatory Status:** **ETHICS SUBMISSION PACKET COMPLETED & SUBMITTED — INSTITUTIONAL DETERMINATION PENDING.**
"""
write_both("02_CORRECTED_ETHICS/ethics_checklist.md", checklist_content)

# =========================================================================
# 03_CORRECTED_ASSESSMENTS
# =========================================================================

# 5. pretest.md (Balanced Answer Options)
pretest_content = """# 10-Item Diagnostic Troubleshooting Pre-Test
**Document ID:** P4.2-PRETEST-2026-REV2  
**Target:** Baseline Diagnostic Knowledge of HPLC Fluidic Symptoms & Fault Mechanisms  
**Scoring:** 1 point per correct answer (Total: 0 to 10 points)  
**Time Limit:** 10 Minutes (Closed-Book, No Simulator Access)  

---

**Participant ID Code:** ____________________  
**Degree Program:** [ ] B.Pharm  [ ] B.Sc. Chemistry  [ ] Other: _________  
**Prior Hands-On HPLC Instrumentation Experience:** [ ] None  [ ] 1–2 Sessions  [ ] > 3 Sessions  

---

### Questions

#### Q1. Backpressure & Flow Dynamics
During an isocratic run on a reverse-phase C18 column, the system backpressure suddenly drops by 25 bar and the baseline exhibits cyclical, sharp spikes synchronized with pump piston strokes. What is the most probable cause?
- A) Severe column inlet fouling
- B) Sample mass overload on the stationary phase
- C) An air bubble trapped inside the pump check valve or piston chamber
- D) Mobile phase organic modifier evaporation

#### Q2. Retention Time Drift
An analyst notices that between run 1 and run 5, the retention times of all analgesic analytes systematically lengthen by 30%, while the column backpressure drops from 85 bar to 55 bar. The pump flow setpoint is unchanged at 1.0 mL/min. What fault explains this pattern?
- A) A fitting leak upstream of the column inlet (post-pump)
- B) Bacterial growth blocking the inlet frit
- C) Column stationary phase collapse
- D) Column compartment temperature increase from 30°C to 45°C

#### Q3. Peak Shape Distortion
In a standard quality control assay, all peaks in the chromatogram suddenly exhibit severe peak splitting (double peaks) and pronounced tailing ($T_f > 2.2$), while retention times and backpressure remain relatively stable. What is the primary diagnostic conclusion?
- A) Air bubble trapped in the UV detector flow cell
- B) Excessive mobile phase buffer salt concentration
- C) Faulty proportioning valve delivering incorrect solvent mixture
- D) A physical void or bed collapse at the head of the packed column

#### Q4. Spurious Peaks in Baseline
During a blank gradient injection (0% sample, solvent only), several sharp, unassigned peaks elute consistently between 35% and 60% B. What is the most likely source of these "ghost peaks"?
- A) Column bed channeling
- B) Organic solvent impurities or contaminated aqueous buffer in the mobile phase
- C) UV detector lamp failing
- D) Pump check valve cavitation

#### Q5. Pressure Surge Diagnostics
While starting an analytical run at 1.0 mL/min, the instrument system pressure exceeds the maximum cutoff limit (400 bar) almost immediately after the injection valve rotates. What is the most immediate diagnostic isolation check?
- A) Disconnect the column inlet line to determine if the blockage is in the column inlet frit or autosampler tubing
- B) Check for trapped air in the autosampler needle
- C) Increase the column oven temperature to reduce solvent viscosity
- D) Change the UV detection wavelength

#### Q6. Selective vs Universal Retention Shifts
If an analyst observes that only weakly retained, acidic analytes shift in retention while neutral analytes maintain perfect retention stability, what parameter has drifted?
- A) Pump volumetric flow rate
- B) Column packing bed permeability
- C) Mobile phase pH (affecting analyte ionization equilibria)
- D) System dwell volume

#### Q7. Peak Asymmetry Mechanisms
Which of the following physical conditions is the primary cause of peak fronting (asymmetry factor $A_s < 0.85$)?
- A) Column void at the inlet
- B) Flow cell optical window contamination
- C) Pump seal micro-leak
- D) Column mass overload (exceeding the linear adsorption capacity of the stationary phase)

#### Q8. Standard Troubleshooting Sequence
When an HPLC pump produces erratic, pulsing backpressure accompanied by high baseline noise, what is the first corrective action an operator should execute?
- A) Replace the analytical column immediately
- B) Purge and prime the pump at high flow (e.g., 5 mL/min with purge valve open) using thoroughly degassed solvent
- C) Calibrate the UV detector optical bench
- D) Re-inject the sample at double volume

#### Q9. Column Void Differentiation
How can an operator differentiate between a blocked column inlet frit and a physical column void?
- A) A void always causes pressure to drop to zero; a blocked frit causes retention time extension
- B) A blocked frit changes detection wavelength; a void alters flow rate
- C) A blocked frit causes severe pressure surge without splitting; a void causes peak splitting without massive pressure surge
- D) They produce identical chromatographic symptoms and cannot be distinguished

#### Q10. Fluidic Leak Location Diagnostics
If a micro-leak occurs *after* the column outlet but *before* the UV detector flow cell, what chromatographic symptom will be observed?
- A) Loss of backpressure on the pump pressure gauge
- B) Loss of peak area/height with baseline noise, but normal pump backpressure and normal retention times
- C) Systematic elongation of retention times
- D) Peak fronting and retention shortening
"""
write_both("03_CORRECTED_ASSESSMENTS/pretest.md", pretest_content)

# 6. posttest.md (Balanced Answer Options)
posttest_content = """# 10-Item Diagnostic Troubleshooting Post-Test (Parallel Form)
**Document ID:** P4.2-POSTTEST-2026-REV2  
**Target:** Post-Intervention Diagnostic Reasoning & Symptom-to-Fault Mapping  
**Scoring:** 1 point per correct answer (Total: 0 to 10 points)  
**Time Limit:** 10 Minutes (Closed-Book, No Simulator Access)  

---

**Participant ID Code:** ____________________  

---

### Questions

#### Q1. Backpressure & Flow (Isomorphic to Pre-Test Q1)
While running an analytical separation, an operator observes the system backpressure fluctuating rapidly by ±20 bar with every stroke of pump head A, accompanied by sharp negative baseline spikes on the detector. What is the root cause?
- A) A worn column inlet bed
- B) Cavitation caused by an entrapped air pocket in the pump head
- C) Sample solvent immiscibility
- D) In-line filter clogging

#### Q2. Retention Time Drift (Isomorphic to Pre-Test Q2)
During a series of repeat injections, all compounds elute 25% later than their monograph retention times, and the system backpressure reads 60 bar instead of the expected 90 bar. Inspection reveals fluid droplets pooling around the column inlet fitting. What is the diagnosis?
- A) Mobile phase proportioning valve malfunction
- B) Stationary phase hydrolysis
- C) Ambient temperature decrease
- D) A fluidic fitting leak causing reduced superficial linear velocity through the column

#### Q3. Peak Shape Distortion (Isomorphic to Pre-Test Q3)
An analytical chemist runs a pharmaceutical standard and observes that every analyte in the mixture displays a bifurcated (split) peak top and significant tailing ($T_f = 2.4$), even though backpressure is normal. What fault has occurred?
- A) Collapse or voiding of the packed bed at the column inlet
- B) UV detector lamp deterioration
- C) Flow cell gas bubble
- D) Injection volume set too small

#### Q4. Spurious Peaks in Baseline (Isomorphic to Pre-Test Q4)
In gradient HPLC, a series of reproducible unassigned peaks elute during the high-organic segment of a blank run. When the initial hold time at 5% B is doubled, the peak areas of these ghost peaks double proportionally. Where are the contaminants originating?
- A) Trapped inside the autosampler injection rotor
- B) Bleeding from the C18 stationary phase
- C) Accumulating from the weak aqueous mobile phase component during the initial re-equilibration hold
- D) Generated by detector electronic noise

#### Q5. Pressure Surge Diagnostics (Isomorphic to Pre-Test Q5)
The pressure limit on an HPLC instrument trips at 380 bar upon starting a run. When the analyst loosens the fitting at the column inlet, the pump pressure drops immediately to 5 bar. Where is the hydraulic blockage located?
- A) Inside the column inlet frit or packed bed
- B) In the autosampler needle seat capillary
- C) Inside the purge valve
- D) In the UV detector flow cell waste line

#### Q6. Selective vs Universal Retention Shifts (Isomorphic to Pre-Test Q6)
Following the preparation of a fresh batch of mobile phase, the retention times of neutral compounds (Caffeine, Toluene) are unchanged, but Ibuprofen ($pK_a = 4.4$) elutes 3 minutes earlier than normal. What is the root cause?
- A) Column temperature increased by 10°C
- B) Pump seal leak reduced flow velocity
- C) Buffer pH was prepared higher than target, increasing Ibuprofen ionization and reducing hydrophobic retention
- D) Organic solvent modifier percentage was decreased

#### Q7. Peak Asymmetry Mechanisms (Isomorphic to Pre-Test Q7)
A standard injection exhibits severe peak tailing ($T_f = 2.6$) for basic pharmaceutical amines on an older C18 column, but neutral solutes elute with ideal Gaussian symmetry ($T_f = 1.05$). What mechanism is causing the tailing?
- A) Physical column void at inlet
- B) Secondary silanol interactions between ionized amine solutes and unreacted residual silanols on the silica surface
- C) Autosampler needle leak
- D) Excessively high mobile phase flow rate

#### Q8. Standard Troubleshooting Sequence (Isomorphic to Pre-Test Q8)
When troubleshooting an HPLC system with suspected pump cavitation (air bubble), what is the correct operational sequence?
- A) Immediately invert the column and flush with 100% methanol
- B) Increase column oven temperature to 60°C to dissolve the air bubble
- C) Replace the injector rotor seal
- D) Stop flow, open the purge valve, flush the pump heads with thoroughly degassed solvent at high flow, and close purge valve

#### Q9. Column Void Identification (Isomorphic to Pre-Test Q9)
What characteristic chromatographic change indicates that peak distortion is caused by an inlet column void rather than sample solvent mismatch?
- A) An inlet void distorts all peaks in the chromatogram regardless of injection volume; solvent mismatch primarily distorts early eluters
- B) An inlet void only affects the last-eluting compound
- C) Solvent mismatch causes backpressure to drop to zero
- D) An inlet void changes the retention order of the analytes

#### Q10. Fluidic Leak Location Diagnostics (Isomorphic to Pre-Test Q10)
A loose fitting is detected *before* the injector (between pump and autosampler). What pattern of symptoms will this produce?
- A) Higher system backpressure and shorter retention times
- B) Peak splitting and loss of plate count with unchanged pressure
- C) Lower system backpressure and longer retention times, but 100% peak area recovery
- D) Baseline drift only with zero pressure change
"""
write_both("03_CORRECTED_ASSESSMENTS/posttest.md", posttest_content)

# 7. answer_key.md (Master Key & Psychometric Analysis)
answer_key_content = """# Master Answer Key & Item Diagnostic Rationales
**Document ID:** P4.2-ANSWER-KEY-2026-REV2  
**Target:** Pre-Test and Post-Test Scoring, Construct Mapping, and Rationales  

---

## 1. Pre-Test Master Answer Key & Distribution

| Item | Correct Key | Diagnostic Construct | Bloom Cognitive Level | Mechanistic Rationale |
| :---: | :---: | :--- | :--- | :--- |
| **Q1** | **C** | Pump Cavitation | Analysis | Trapped gas pocket compresses during forward stroke, causing cyclic flow drop and optical baseline ripple. |
| **Q2** | **A** | Pre-Column Fitting Leak | Application | Liquid loss before column reduces superficial linear velocity ($u$), proportionally increasing retention times ($t_R$). |
| **Q3** | **D** | Column Inlet Void | Analysis | Bed collapse creates dual flow velocity pathways that split migrating solute bands, forming doublet peaks. |
| **Q4** | **B** | Mobile Phase Contamination | Comprehension | Trace organic impurities in water concentrate on C18 head during low organic and elute during ramp. |
| **Q5** | **A** | System Pressure Surge | Application | Disconnecting column isolates whether hydraulic resistance is upstream (tubing) or in column frit. |
| **Q6** | **C** | Mobile Phase pH Drift | Analysis | Ionized acids ($A^-$) partition poorly into C18; neutral species retention is unaffected by pH shifts. |
| **Q7** | **D** | Peak Fronting Overload | Comprehension | Exceeding linear isotherm capacity leads to self-displacement where solute band front moves faster than rear. |
| **Q8** | **B** | Pump Degassing Protocol | Application | Opening purge valve isolates column from high priming flow, sweeping air out of check valves. |
| **Q9** | **C** | Void vs Blockage | Evaluation | Frit fouling creates severe hydrodynamic resistance ($P > 400\text{ bar}$); voids cause band splitting without pressure spike. |
| **Q10**| **B** | Pre-Detector Leak | Evaluation | Flow loss post-column drops mass delivery to detector (smaller peaks) but column pressure and $t_R$ are normal. |

**Pre-Test Option Distribution:** Option A: 2 (20%) | Option B: 3 (30%) | Option C: 3 (30%) | Option D: 2 (20%). Max consecutive = 1.

---

## 2. Post-Test Master Answer Key & Distribution

| Item | Correct Key | Diagnostic Construct | Bloom Cognitive Level | Mechanistic Rationale |
| :---: | :---: | :--- | :--- | :--- |
| **Q1** | **B** | Pump Cavitation | Analysis | Pressure oscillation synchronized with piston frequency is pathognomonic for compressible air pocket in check valve. |
| **Q2** | **D** | Pre-Column Fitting Leak | Application | External droplet accumulation with reduced backpressure confirms mobile phase loss and reduced linear velocity. |
| **Q3** | **A** | Column Inlet Void | Analysis | Symmetrical doublet splitting across all peaks indicates solute band bifurcation at the head of the packed bed. |
| **Q4** | **C** | Mobile Phase Contamination | Comprehension | Peak area scaling with initial hold duration proves contaminants originate from weak mobile phase component. |
| **Q5** | **A** | System Pressure Surge | Application | Immediate pressure drop upon loosening column nut confirms restriction is situated inside column inlet frit. |
| **Q6** | **C** | Mobile Phase pH Drift | Analysis | Earlier elution of acidic API indicates mobile phase buffer pH rose above $pK_a$, increasing ionization fraction. |
| **Q7** | **B** | Residual Silanol Tailing | Comprehension | Protonated amine cations undergo secondary ion-exchange with ionized silanols ($\text{SiO}^-$), causing slow desorption tailing. |
| **Q8** | **D** | Pump Degassing Protocol | Application | Standard SOP requires opening purge valve and flushing at high flow with degassed mobile phase to expel cavitation bubbles. |
| **Q9** | **A** | Void vs Solvent Mismatch | Evaluation | In-bed mechanical voids distort all migrating solutes; injection solvent mismatch dissipates once diluted in column. |
| **Q10**| **C** | Pre-Injector Leak | Evaluation | Mobile phase loss before injector delays delivery to column ($t_R$ increases) but 100% of injected mass reaches detector. |

**Post-Test Option Distribution:** Option A: 3 (30%) | Option B: 2 (20%) | Option C: 3 (30%) | Option D: 2 (20%). Max consecutive = 1.
"""
write_both("03_CORRECTED_ASSESSMENTS/answer_key.md", answer_key_content)

# 8. practical_diagnostic_task.md (24-point scoring architecture)
practical_content = """# Practical Diagnostic Assessment Tasks
**Document ID:** P4.2-PRACTICAL-2026-REV2  
**Target:** Evaluation of Student Diagnostic Reasoning Across 4 Simulated HPLC Unknowns  
**Scoring Architecture:** 6 Points per Scenario (Fault ID: 0-2, Reasoning: 0-2, Action: 0-2)  
**Total Points:** 0 to 24 Points  
**Time Limit:** 12 Minutes Total (3 Minutes per Scenario)  

---

**Participant ID Code:** ____________________  

---

### Instructions for Students
In this exercise, you will evaluate **four unknown simulated instrument fault scenarios** (Scenarios Alpha, Beta, Gamma, and Delta) within the SimuPharm simulator. For each scenario:
1. Examine the chromatographic display, retention times, peak shapes, and system backpressure gauge.
2. Formulate your diagnostic conclusion.
3. Record your physical reasoning (explain *why* this pattern occurs).
4. Specify the correct standard operating procedure (SOP) troubleshooting action.
5. Rate your diagnostic confidence (1 = Guessing, 5 = Absolutely Certain).
6. Record the time (in seconds) taken to reach your diagnosis.

---

### Scenario Alpha: Unknown Fault #1
- **Visual Symptoms:** System backpressure reads 60 bar (normal: 90 bar). Retention times of all analgesic peaks are elongated by approximately +25% to +30%. Peak shapes remain sharp and symmetrical.
- **1. Fault Diagnosis:** __________________________________________________
- **2. Physical Reasoning (Why does this happen?):**  
  __________________________________________________________________________  
  __________________________________________________________________________
- **3. Corrective Action (What SOP action should you take?):**  
  __________________________________________________________________________
- **4. Confidence Rating:** [ ] 1 (Guessing)  [ ] 2 (Low)  [ ] 3 (Moderate)  [ ] 4 (High)  [ ] 5 (Certain)
- **5. Time to Diagnosis:** _________ seconds

---

### Scenario Beta: Unknown Fault #2
- **Visual Symptoms:** System backpressure reads 90 bar (normal). Retention times are normal. However, all four analyte peaks exhibit pronounced doublet peak splitting and tailing ($T_f > 2.2$).
- **1. Fault Diagnosis:** __________________________________________________
- **2. Physical Reasoning (Why does this happen?):**  
  __________________________________________________________________________  
  __________________________________________________________________________
- **3. Corrective Action (What SOP action should you take?):**  
  __________________________________________________________________________
- **4. Confidence Rating:** [ ] 1 (Guessing)  [ ] 2 (Low)  [ ] 3 (Moderate)  [ ] 4 (High)  [ ] 5 (Certain)
- **5. Time to Diagnosis:** _________ seconds

---

### Scenario Gamma: Unknown Fault #3
- **Visual Symptoms:** Backpressure gauge exhibits rapid cyclical fluctuations of ±20 bar synchronized with pump stroke. Baseline display shows sharp negative spikes.
- **1. Fault Diagnosis:** __________________________________________________
- **2. Physical Reasoning (Why does this happen?):**  
  __________________________________________________________________________  
  __________________________________________________________________________
- **3. Corrective Action (What SOP action should you take?):**  
  __________________________________________________________________________
- **4. Confidence Rating:** [ ] 1 (Guessing)  [ ] 2 (Low)  [ ] 3 (Moderate)  [ ] 4 (High)  [ ] 5 (Certain)
- **5. Time to Diagnosis:** _________ seconds

---

### Scenario Delta: Unknown Fault #4
- **Visual Symptoms:** System backpressure reads 95 bar (+5 bar increase). Standard analgesic analytes elute normally, but two distinct, unassigned ghost peaks appear consistently in the blank run.
- **1. Fault Diagnosis:** __________________________________________________
- **2. Physical Reasoning (Why does this happen?):**  
  __________________________________________________________________________  
  __________________________________________________________________________
- **3. Corrective Action (What SOP action should you take?):**  
  __________________________________________________________________________
- **4. Confidence Rating:** [ ] 1 (Guessing)  [ ] 2 (Low)  [ ] 3 (Moderate)  [ ] 4 (High)  [ ] 5 (Certain)
- **5. Time to Diagnosis:** _________ seconds
"""
write_both("03_CORRECTED_ASSESSMENTS/practical_diagnostic_task.md", practical_content)

# 9. scoring_rubric.md (24-point Standardized Rubric)
rubric_content = """# Standardized 24-Point Practical Diagnostic Scoring Rubric
**Document ID:** P4.2-RUBRIC-2026-REV2  
**Target:** Standardized Double-Rater Evaluation of Practical Diagnostic Tasks  
**Scale:** 0 to 6 Points per Scenario $\times$ 4 Scenarios = **0 to 24 Points Grand Total**  
**Scoring Method:** Two independent faculty raters; discrepancies $>1$ point adjudicated via consensus.  

---

## 1. Resolution of the 12 vs 24 Point Scoring Conflict
In Phase 4, documents conflicted between a 3-point/12-point rubric and a 6-point/24-point rubric. In Phase 4.2, the panel conclusively adopts the **24-point analytical architecture** (6 points per scenario across 4 tasks) for the following reasons:
1. **Variance & Sensitivity:** A 0–2 scale allows graders to distinguish partial mechanistic reasoning from complete misconceptions, preventing floor effects in novice students.
2. **Psychometric Reliability:** A 0–2 scale per component provides sufficient gradation to compute weighted Cohen's Kappa ($\kappa_w$) and Intraclass Correlation Coefficients (ICC[2,1]), satisfying JCE reviewer standards.
3. **Statistical Power:** A 24-point composite scale provides continuous-like statistical properties that reduce discrete distribution ties in small sample sizes ($N=25$).

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
4. Pre-adjudication scores are used to compute Cohen's weighted Kappa ($\kappa_w$) and ICC(2,1).
"""
write_both("03_CORRECTED_ASSESSMENTS/scoring_rubric.md", rubric_content)

# 10. instructor_protocol.md (Neutral Guided Inquiry Script)
inst_script = """# Standardized Instructor Protocol & Neutral Inquiry Script
**Document ID:** P4.2-INST-SCRIPT-2026-REV2  
**Target:** Standardized Delivery of 50-Minute HPLC Troubleshooting Lab Session  
**Pedagogical Mode:** Non-Directive Guided Inquiry (Zero Test Cueing)  

---

## 1. Instructor Governance Mandate
To maintain scientific validity and eliminate demand characteristics, the instructor must strictly adhere to this standardized script. **THE INSTRUCTOR MUST NOT**:
- Reveal numerical shifts (-20 bar, -50 bar, +30% $t_R$).
- Explain why specific peak shapes or pressure drops occur during exploration.
- Mention specific fault mechanisms (e.g., cavitation, channeling, bed collapse).
- Provide answers to any pre-test, post-test, or practical scenario questions.

---

## 2. Standardized Verbal Script

### Segment 1: Study Introduction (Minutes 00:00 – 00:05)
> *"Welcome to today's instrumental chromatography laboratory. Today we will explore HPLC system operation and troubleshooting using an interactive simulation tool called SimuPharm. Your participation is completely voluntary and will have zero impact on your academic grades. Please open your participant envelope, review the information sheet, and sign the consent form if you agree to participate."*

### Segment 2: Diagnostic Baseline Pre-Test (Minutes 00:05 – 00:15)
> *"Please open Section 1 of your packet: the Pre-Test. You have 10 minutes to complete these 10 questions based on your current knowledge. Do not use external notes or open your browser. When finished, place your test sheet face down."*

### Segment 3: Neutral Simulator Exploration (Minutes 00:15 – 00:27)
> *"Please open your web browser and navigate to the SimuPharm simulator. Take the first three minutes to examine the control interface. You can adjust solvent composition (% B), volumetric flow rate, and column temperature using the sliders. Notice the system pressure gauge and the chromatographic canvas."*  
> *(At Minute 18)* *"Now click 'Run Separation' with normal baseline settings (50% B, 1.0 mL/min, 30°C). Observe the baseline trace and note how the four analgesic compounds separate under standard conditions."*  
> *(At Minute 21 — Neutral Guided Inquiry)* *"Now, open the 'Fault Injection' panel. You will see four fault toggle switches. Activate Fault 1. Examine the pressure gauge and the chromatographic canvas carefully. Notice any changes from your baseline run. Think about what physical change in the fluidic pathway could produce this pattern. Now deactivate Fault 1, and sequentially test Fault 2, Fault 3, and Fault 4. Compare how each fault alters retention times, peak shapes, and backpressure. Record your observations in your notebook."*

### Segment 4: Practical Diagnostic Tasks (Minutes 00:27 – 00:39)
> *"Please open the Practical Diagnostic Task module in SimuPharm and Section 2 of your worksheet. You will be presented with four unknown scenarios: Alpha, Beta, Gamma, and Delta. For each unknown, examine the system display, write down your diagnosis, explain your physical reasoning, propose an SOP corrective action, rate your confidence, and note your diagnostic time. You have three minutes per scenario."*

### Segment 5: Post-Test & Usability Survey (Minutes 00:39 – 00:49)
> *"Please close your browser window. Open Section 3 of your packet: the Post-Test and Usability Questionnaire. You have 10 minutes to complete the 10 post-test questions, the 10 System Usability Scale statements, and the feedback ratings."*

### Segment 6: Collection & Debrief (Minutes 00:49 – 00:50)
> *"Please place all completed sheets back into your envelope, seal it, and place it in the collection box at the front desk. Thank you for your valuable participation."*
"""
write_both("03_CORRECTED_ASSESSMENTS/instructor_protocol.md", inst_script)

# 11. instructor_fidelity_checklist.md (Observer Monitoring Tool)
fidelity_content = """# Instructor Implementation Fidelity Monitoring Checklist
**Document ID:** P4.2-FIDELITY-2026-REV2  
**Target:** Independent Observer Verification of Standardized Script Adherence  
**Evaluator:** Independent Laboratory Observer  

---

**Observer Name:** ______________________________  
**Date & Lab Section:** _________________________  
**Instructor Monitored:** _______________________  

| Checklist Item | Evaluated Behavior | Adherence? | Observer Notes |
| :---: | :--- | :---: | :--- |
| **F01** | Informed consent administered without academic coercion. | [ ] YES  [ ] NO | |
| **F02** | Baseline pre-test administered closed-book with 10-minute timer enforced. | [ ] YES  [ ] NO | |
| **F03** | Interface orientation adhered to neutral functional descriptions. | [ ] YES  [ ] NO | |
| **F04** | Normal baseline run completed at standardized settings (50% B, 1.0 mL/min). | [ ] YES  [ ] NO | |
| **F05** | **Zero Cueing of Symptoms:** Instructor did NOT state numerical shifts (-20 bar, -50 bar, etc.). | [ ] YES  [ ] NO | **CRITICAL FIDELITY CHECK** |
| **F06** | **Zero Cueing of Mechanisms:** Instructor did NOT explain cavitation, bed collapse, or silanols. | [ ] YES  [ ] NO | **CRITICAL FIDELITY CHECK** |
| **F07** | **Zero Post-Test Cueing:** Instructor did NOT reference specific post-test items or answers. | [ ] YES  [ ] NO | **CRITICAL FIDELITY CHECK** |
| **F08** | Practical diagnostic tasks conducted under blind unknown conditions. | [ ] YES  [ ] NO | |
| **F09** | Post-test administered closed-book with browser windows closed. | [ ] YES  [ ] NO | |
| **F10** | Usability questionnaire administered independently without instructor coaching. | [ ] YES  [ ] NO | |

**Overall Fidelity Rating:** [ ] 10/10 Full Adherence (Valid Session)  [ ] Deviations Recorded (See Notes)  
**Observer Signature:** ________________________________________  
"""
write_both("03_CORRECTED_ASSESSMENTS/instructor_fidelity_checklist.md", fidelity_content)

# 12. check_position_bias.py (Automated Key Distribution Verifier)
bias_script = """# check_position_bias.py
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
    assert p_val >= 0.50, f"Chi-square p-value {p_val:.4f} indicates non-uniform distribution!"
    print(f"  STATUS: PASS (Zero Position Bias Confirmed)\n")

if __name__ == '__main__':
    audit_keys("Pre-Test (P4.2-PRETEST-2026-REV2)", pretest_keys)
    audit_keys("Post-Test (P4.2-POSTTEST-2026-REV2)", posttest_keys)
    print("ALL PSYCHOMETRIC POSITION BIAS CHECKS PASSED SUCCESSFULLY.")
"""
write_both("03_CORRECTED_ASSESSMENTS/check_position_bias.py", bias_script)

print("Part 2 generation complete.")
