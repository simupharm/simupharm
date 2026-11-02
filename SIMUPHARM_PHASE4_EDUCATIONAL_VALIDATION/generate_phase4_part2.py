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
# 02_ETHICS
# ==============================================================================

ethics_checklist = """# INSTITUTIONAL ETHICS & COMPLIANCE CHECKLIST
**Document ID:** P4-ETHICS-2026-REV1  
**Regulatory Framework:** US 45 CFR 46 (Common Rule) Exemption Category 1 / Institutional Research Ethics Guidelines  

---

## 1. ETHICAL REVIEW STATUS & COMPLIANCE CRITERIA

| Evaluation Domain | Regulatory Requirement | SimuPharm Protocol Implementation | Compliance Status |
| :--- | :--- | :--- | :--- |
| **Exemption Category** | Research conducted in established or commonly accepted educational settings involving normal educational practices. | Study evaluates normal instructional activity using an educational software tool during a scheduled laboratory period. | **EXEMPTION CRITERIA MET** (45 CFR 46.104(d)(1)) |
| **Informed Consent** | Participants must be fully informed of study aims, procedures, voluntary nature, and lack of penalty. | Written Participant Information Sheet and Informed Consent Form administered prior to pre-test. | **COMPLIANT** |
| **Voluntary Participation** | Students must have free choice to participate without academic coercion or perceived grade impact. | Protocol explicitly states participation is optional; non-participating students complete the standard curriculum without penalty. | **COMPLIANT** |
| **Right to Withdraw** | Participants may withdraw at any time during or after the session without consequence. | Anonymized withdrawal protocol: participants may withhold their de-identified submission without penalty. | **COMPLIANT** |
| **Anonymization & Privacy** | No personally identifiable information (PII) may be stored in research datasets. | Strict numeric coding (`PARTICIPANT_01` to `PARTICIPANT_25`). Names, student ID numbers, and emails are never recorded. | **COMPLIANT** |
| **Data Security & Storage** | Research records must be stored securely with access restricted to certified researchers. | Encrypted storage on password-protected institutional drive; physical survey sheets locked in departmental safe for 3 years. | **COMPLIANT** |
| **Educational Parity** | Intervention must not disadvantage any student cohort academically. | All students (participants and non-participants) receive full access to SimuPharm and answer keys after the session. | **COMPLIANT** |
| **No Grading Consequences** | Pre-test and post-test scores must not influence course grades or academic evaluations. | Assessments are strictly formative and for educational research purposes only; zero contribution to degree GPA. | **COMPLIANT** |
| **Instructor Conflict Mitigation** | Conflict of interest between researcher and course instructor must be managed. | Study administered by independent teaching assistant or co-investigator; primary course grader is blinded to participation. | **COMPLIANT** |
| **Open Science & Reporting** | Transparency in reporting positive, neutral, and negative outcomes. | Pre-registered Statistical Analysis Plan (SAP); commitment to publish negative usability and diagnostic findings. | **COMPLIANT** |
"""

participant_info_sheet = """# PARTICIPANT INFORMATION SHEET
**Study Title:** Usability and Diagnostic Efficacy of a Browser-Based HPLC Troubleshooting Simulator in Undergraduate Pharmacy Education  
**Principal Investigator:** Educational Research Evaluation Team  
**Institution:** Academic Pharmacy & Chemistry Department  

---

### 1. What is the purpose of this study?
You are invited to take part in an educational evaluation study investigating the usability and learning utility of **SimuPharm**, an interactive, web-based High-Performance Liquid Chromatography (HPLC) simulation tool. This study aims to evaluate whether an interactive simulator can help students understand chromatographic principles and recognize diagnostic equipment faults (such as air bubbles, leaks, and column degradation).

### 2. Do I have to take part?
**No. Participation is entirely voluntary.** It is up to you to decide whether or not to take part. If you decide not to participate, your decision will have **absolutely no impact** on your course grades, academic standing, or relationship with your instructors.

### 3. What will happen if I take part?
If you agree to take part, you will participate in a single 50-minute laboratory session:
1. **Pre-Test (10 minutes):** You will complete a brief 10-question multiple-choice questionnaire about HPLC troubleshooting.
2. **Interactive Simulation (20 minutes):** You will use the SimuPharm web application on a computer to run virtual HPLC experiments and observe different instrument faults.
3. **Diagnostic Performance Task (10 minutes):** You will inspect four unknown simulated chromatograms and record your diagnosis and reasoning.
4. **Post-Test & Usability Survey (10 minutes):** You will complete a parallel 10-question post-test and a standard 10-item System Usability Scale (SUS) questionnaire, along with brief open-ended feedback.

### 4. Are there any risks or discomforts?
There are no physical risks associated with this study. The software runs in a standard web browser. The quiz questions are for research purposes only and will **not** count toward your course grade.

### 5. What are the possible benefits?
You will gain hands-on practice with HPLC troubleshooting scenarios that are typically too costly or dangerous to deliberately recreate on physical laboratory instruments.

### 6. Will my information be kept confidential?
**Yes. All data collected will be completely anonymous.** You will be assigned a random participant identification code (e.g., `PARTICIPANT_05`). Your name, student ID number, and contact details will **never** be linked to your responses or stored in any research database. Only summarized, de-identified group data will be presented in scientific publications.

### 7. What if I change my mind?
You are free to withdraw from the study at any time during the session without giving a reason and without any penalty.

### 8. Contact Information
If you have questions regarding this study or your rights as an educational research participant, please contact the Principal Investigator or the Institutional Ethics Board.
"""

consent_template = """# INFORMED CONSENT FORM
**Project:** Educational Evaluation of SimuPharm HPLC Troubleshooting Simulator  
**Participant Identification Code:** ____________________  

---

### PARTICIPANT DECLARATION & AGREEMENT

Please read each statement carefully and initial the corresponding box:

1. [ ] I confirm that I have read and understand the Participant Information Sheet for this study. I have had the opportunity to consider the information, ask questions, and have had these answered satisfactorily.
2. [ ] I understand that my participation is entirely voluntary and that I am free to withdraw at any time without giving any reason and without my academic standing or legal rights being affected.
3. [ ] I understand that my test responses, diagnostic task timing, and usability feedback will be collected anonymously under a random identification number, and that my name or student ID will never be published or linked to my data.
4. [ ] I understand that the pre-test and post-test results are collected solely for educational research and will have no bearing on my course grades or academic assessments.
5. [ ] I understand that all students in the course will receive equal access to the SimuPharm software and learning materials regardless of participation.
6. [ ] I agree to take part in the above educational research study.

---

**Participant Signature (or Digital Consent Checkbox):**  
Signature: _____________________________________________ Date: ___________________  

**Researcher Statement:**  
I confirm that I have explained the nature and purpose of this study to the participant named above.  
Researcher Name: ______________________________________ Date: ___________________  
"""

ethics_notes = """# ETHICS SUBMISSION & INSTITUTIONAL AUTHORIZATION NOTES
**Document ID:** P4-ETHICS-NOTES-2026-REV1  
**Category:** Protocol Justification for Institutional Review Board / Departmental Head  

---

## 1. REGULATORY EXEMPTION JUSTIFICATION (45 CFR 46.104(d)(1))
Under United States Department of Health and Human Services (HHS) regulations (45 CFR 46.104(d)(1)), research conducted in established or commonly accepted educational settings that involves normal educational practices is exempt from full institutional committee review when:
1. The research evaluates regular or special education instructional strategies; or
2. The research evaluates the effectiveness of, or the comparison among, instructional techniques, curricula, or classroom management methods.

### Application to SimuPharm Pilot:
- **Instructional Context:** The study takes place within a standard undergraduate instrumental pharmaceutical analysis laboratory session.
- **Normal Practice:** Troubleshooting instruction, formative quizzes, and hands-on computer simulation are established components of pharmaceutical chemistry curricula.
- **Zero Risk:** The intervention introduces zero physical, psychological, social, or legal risks.
- **Data Protection:** All data collection instruments are strictly anonymous at the point of capture.

---

## 2. PROCEDURAL SAFEGUARDS FOR PARTICIPANT PROTECTION
1. **Voluntary Opt-In:** Participation is recruited using neutral announcements without faculty coercion.
2. **Grade Independence:** Consent forms explicitly declare zero impact on course grades.
3. **Curricular Equality:** Non-participating students perform the same virtual lab activity using SimuPharm, but their assessment sheets are not entered into the research database.
4. **Data Destruction Protocol:** Physical paper questionnaires are retained in a double-locked departmental cabinet for 3 years post-publication, after which they are shredded. Electronic data templates contain zero PII.
"""

write_both("02_ETHICS/ethics_checklist.md", ethics_checklist)
write_both("02_ETHICS/participant_information_sheet.md", participant_info_sheet)
write_both("02_ETHICS/informed_consent_template.md", consent_template)
write_both("02_ETHICS/ethics_submission_notes.md", ethics_notes)

# ==============================================================================
# 03_ASSESSMENT_INSTRUMENTS
# ==============================================================================

pretest = """# 10-ITEM DIAGNOSTIC TROUBLESHOOTING PRE-TEST
**Document ID:** P4-PRETEST-2026-REV1  
**Target:** Baseline Knowledge of HPLC System Symptoms & Troubleshooting Actions  
**Scoring:** 1 point per correct answer (Total: 0 to 10 points)  
**Time Limit:** 10 Minutes  

---

**Participant ID Code:** ____________________  
**Major / Degree:** [ ] B.Pharm  [ ] B.Sc. Chemistry  [ ] Other: _________  
**Prior Hands-On HPLC Experience:** [ ] None  [ ] 1–2 Lab Sessions  [ ] > 3 Lab Sessions  

---

### Questions

#### Q1. Backpressure & Flow
During an isocratic run on a reverse-phase C18 column, the system backpressure suddenly drops by 25 bar and the baseline exhibits cyclical, sharp spikes synchronized with pump piston strokes. What is the most probable cause?
- A) Severe column inlet fouling
- B) An air bubble trapped inside the pump check valve or piston chamber
- C) Sample mass overload on the stationary phase
- D) Mobile phase organic modifier evaporation

#### Q2. Retention Time Drift
An analyst notices that between run 1 and run 5, the retention times of all analgesic analytes systematically lengthen by 30%, while the column backpressure drops from 85 bar to 55 bar. The pump flow setpoint is unchanged at 1.0 mL/min. What fault explains this pattern?
- A) A fitting leak upstream of the column inlet (post-pump)
- B) Bacterial growth blocking the inlet frit
- C) Column stationary phase collapse
- D) Temperature increase from 30°C to 45°C

#### Q3. Peak Shape Distortion
In a standard quality control assay, all peaks in the chromatogram suddenly exhibit severe peak splitting (double peaks) and pronounced tailing ($T_f > 2.2$), while retention times and backpressure remain relatively stable. What is the primary diagnostic conclusion?
- A) Air bubble trapped in the UV detector flow cell
- B) A physical void or bed collapse at the head of the packed column
- C) Excessive mobile phase buffer salt concentration
- D) Faulty proportioning valve delivering incorrect solvent mixture

#### Q4. Spurious Peaks
During a blank gradient injection (0% sample, solvent only), several sharp, unassigned peaks elute consistently between 35% and 60% B. What is the most likely source of these "ghost peaks"?
- A) Column bed channeling
- B) Organic solvent impurities or contaminated aqueous buffer in the mobile phase
- C) UV detector lamp failing
- D) Pump check valve cavitation

#### Q5. Pressure Surge
While starting an analytical run at 1.0 mL/min, the instrument system pressure exceeds the maximum cutoff limit (400 bar) almost immediately after the injection valve rotates. What is the most immediate diagnostic check?
- A) Check for trapped air in the autosampler needle
- B) Disconnect the column inlet line to determine if the blockage is in the column inlet frit or autosampler tubing
- C) Increase the column oven temperature to reduce viscosity
- D) Change the UV detection wavelength

#### Q6. Selective vs Universal Retention Shifts
If an analyst observes that only weakly retained, acidic analytes shift in retention while neutral analytes maintain perfect retention stability, what parameter has drifted?
- A) Pump volumetric flow rate
- B) Mobile phase pH (affecting analyte ionization equilibria)
- C) Column packing bed permeability
- D) System dwell volume

#### Q7. Peak Asymmetry Causes
Which of the following physical defects is the dominant cause of peak fronting (asymmetry factor $A_s < 0.85$)?
- A) Column void at the inlet
- B) Column overload (exceeding linear capacity of stationary phase)
- C) Flow cell window dirt
- D) Pump seal leak

#### Q8. Troubleshooting Sequence
When an HPLC pump produces erratic, pulsing backpressure accompanied by high baseline noise, what is the first corrective action an operator should execute?
- A) Replace the analytical column immediately
- B) Purge and prime the pump at high flow (e.g., 5 mL/min with purge valve open) using thoroughly degassed solvent
- C) Calibrate the UV detector optical bench
- D) Re-inject the sample at double volume

#### Q9. Column Void Identification
How can an operator differentiate between a blocked column inlet frit and a physical column void?
- A) A blocked frit causes severe pressure surge without splitting; a void causes peak splitting without massive pressure surge
- B) A void always causes pressure to drop to zero; a blocked frit causes retention time extension
- C) A blocked frit changes detection wavelength; a void alters flow rate
- D) They produce identical chromatographic symptoms and cannot be distinguished

#### Q10. System Leak Diagnosis
If a micro-leak occurs *after* the column outlet but *before* the UV detector flow cell, what chromatographic symptom will be observed?
- A) Loss of backpressure on the pump gauge
- B) Systematic elongation of retention times
- C) Loss of peak area/height with baseline noise, but normal pump backpressure and normal retention times
- D) Peak fronting and retention shortening
"""

posttest = """# 10-ITEM DIAGNOSTIC TROUBLESHOOTING POST-TEST (PARALLEL FORM)
**Document ID:** P4-POSTTEST-2026-REV1  
**Target:** Post-Intervention Diagnostic Reasoning & Symptom-to-Fault Mapping  
**Scoring:** 1 point per correct answer (Total: 0 to 10 points)  
**Time Limit:** 10 Minutes  

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
- B) A fluidic fitting leak causing reduced superficial linear velocity through the column
- C) Stationary phase hydrolysis
- D) Ambient temperature decrease

#### Q3. Peak Shape Distortion (Isomorphic to Pre-Test Q3)
An analytical chemist runs a pharmaceutical standard and observes that every analyte in the mixture displays a bifurcated (split) peak top and significant tailing ($T_f = 2.4$), even though backpressure is normal. What fault has occurred?
- A) UV detector lamp deterioration
- B) Collapse or voiding of the packed bed at the column inlet
- C) Flow cell gas bubble
- D) Injection volume set too small

#### Q4. Spurious Peaks (Isomorphic to Pre-Test Q4)
In gradient HPLC, a series of reproducible unassigned peaks elute during the high-organic segment of a blank run. When the initial hold time at 5% B is doubled, the peak areas of these ghost peaks double proportionally. Where are the contaminants originating?
- A) Trapped inside the autosampler injection rotor
- B) Accumulating from the weak aqueous mobile phase component during the initial re-equilibration hold
- C) Bleeding from the C18 stationary phase
- D) Generated by detector electronic noise

#### Q5. Pressure Surge (Isomorphic to Pre-Test Q5)
The pressure limit on an HPLC instrument trips at 380 bar upon starting a run. When the analyst loosens the fitting at the column inlet, the pump pressure drops immediately to 5 bar. Where is the hydraulic blockage located?
- A) In the autosampler needle seat capillary
- B) Inside the column inlet frit or packed bed
- C) Inside the purge valve
- D) In the UV detector flow cell waste line

#### Q6. Selective vs Universal Retention Shifts (Isomorphic to Pre-Test Q6)
Following the preparation of a fresh batch of mobile phase, the retention times of neutral compounds (Caffeine, Toluene) are unchanged, but Ibuprofen ($pK_a = 4.4$) elutes 3 minutes earlier than normal. What is the root cause?
- A) Column temperature increased by 10°C
- B) Buffer pH was prepared higher than target, increasing Ibuprofen ionization and reducing hydrophobic retention
- C) Pump seal leak reduced flow velocity
- D) Organic solvent modifier percentage was decreased

#### Q7. Peak Asymmetry Causes (Isomorphic to Pre-Test Q7)
A standard injection exhibits severe peak tailing ($T_f = 2.6$) for basic pharmaceutical amines on an older C18 column, but neutral solutes elute with ideal Gaussian symmetry ($T_f = 1.05$). What mechanism is causing the tailing?
- A) Physical column void at inlet
- B) Secondary silanol interactions between ionized amine solutes and unreacted residual silanols on the silica surface
- C) Autosampler needle leak
- D) Excessively high mobile phase flow rate

#### Q8. Troubleshooting Sequence (Isomorphic to Pre-Test Q8)
When troubleshooting an HPLC system with suspected pump cavitation (air bubble), what is the correct operational sequence?
- A) Immediately invert the column and flush with 100% methanol
- B) Stop flow, open the purge valve, flush the pump heads with thoroughly degassed solvent at high flow, and close purge valve
- C) Increase column oven temperature to 60°C to dissolve the air bubble
- D) Replace the injector rotor seal

#### Q9. Column Void Identification (Isomorphic to Pre-Test Q9)
What characteristic chromatographic change indicates that peak distortion is caused by an inlet column void rather than sample solvent mismatch?
- A) An inlet void distorts all peaks in the chromatogram regardless of injection volume; solvent mismatch primarily distorts early eluters
- B) An inlet void only affects the last-eluting compound
- C) Solvent mismatch causes backpressure to drop to zero
- D) An inlet void changes the retention order of the analytes

#### Q10. System Leak Diagnosis (Isomorphic to Pre-Test Q10)
A loose fitting is detected *before* the injector (between pump and autosampler). What pattern of symptoms will this produce?
- A) Lower system backpressure and longer retention times, but 100% peak area recovery
- B) Higher system backpressure and shorter retention times
- C) Peak splitting and loss of plate count with unchanged pressure
- D) Baseline drift only with zero pressure change
"""

answer_key = """# MASTER ANSWER KEY & DIAGNOSTIC RATIONALE
**Document ID:** P4-KEY-2026-REV1  
**Coverage:** Pre-Test and Post-Test Instruments  

---

## PRE-TEST ANSWER KEY

| Item | Correct Option | Diagnostic Principle / Physical Mechanism | Reference in Literature |
| :--- | :--- | :--- | :--- |
| **Q1** | **B** | Trapped gas in the pump check valve compresses during the delivery stroke, causing transient delivery failure (pressure drop) and optical baseline noise spikes. | Dolan (2005) *LCGC* 23(6), 574–582 |
| **Q2** | **A** | A leak before the column head reduces effective superficial linear velocity ($u_{\text{eff}} < u_{\text{set}}$), directly elongating retention times and reducing hydraulic backpressure proportionally. | Dolan (2008) *LCGC* 26(9), 890–896 |
| **Q3** | **B** | Collapse of the packed silica bed at the column inlet creates a headspace channel; solute molecules enter the bed at different times, creating dual flow paths that split every peak. | Dolan (2008) *LCGC* 26(3), 258–264 |
| **Q4** | **B** | Organic impurities in polar aqueous buffers concentrate on the column head during low %B initial conditions and elute as sharp "ghost peaks" as solvent strength increases. | Dolan (2007) *LCGC* 25(8), 704–712 |
| **Q5** | **B** | Disconnecting the column inlet isolates whether backpressure originates upstream (tubing/injector) or downstream (column inlet frit). If pressure drops to zero, the column inlet is plugged. | Snyder, Kirkland, Glajch (1997) *Practical HPLC Method Development* |
| **Q6** | **B** | Neutral solutes depend only on bulk %B and temperature; ionizable solutes ($pK_a$) are exquisitely sensitive to mobile phase pH, which governs the ionized/neutral fraction. | Neue (1997) *HPLC Columns* |
| **Q7** | **B** | Peak fronting ($A_s < 1.0$) is almost exclusively a symptom of column mass overload, where the solute concentration exceeds the linear isotherm region of the stationary phase. | Dolan (2004) *LCGC* 22(10), 972–980 |
| **Q8** | **B** | Opening the purge valve bypasses the analytical column, allowing high-velocity solvent flushing to dislodge entrapped air bubbles without overpressuring the column. | Meyer (2010) *Practical HPLC* |
| **Q9** | **A** | An inlet void disrupts band morphology for all peaks across the run; solvent mismatch (sample in stronger solvent than mobile phase) primarily distorts early eluters. | Dolan (2008) *LCGC* 26(3), 258–264 |
| **Q10** | **C** | A post-column, pre-detector leak allows fluid to escape without affecting column backpressure or retention times, resulting in reduced peak area and optical noise. | Dolan (2008) *LCGC* 26(9), 890–896 |

---

## POST-TEST ANSWER KEY

| Item | Correct Option | Diagnostic Principle / Physical Mechanism | Reference in Literature |
| :--- | :--- | :--- | :--- |
| **Q1** | **B** | Entrapped air bubble causes stroke-dependent delivery failure, generating cyclical pressure fluctuations and negative baseline spikes. | Dolan (2005) *LCGC* 23(6), 574–582 |
| **Q2** | **B** | Physical leak at column inlet fitting vents mobile phase, reducing linear flow velocity through the column, which extends retention times and lowers backpressure. | Dolan (2008) *LCGC* 26(9), 890–896 |
| **Q3** | **B** | Bed voiding at column inlet creates split peaks (doublets) across all analytes in the mixture. | Dolan (2008) *LCGC* 26(3), 258–264 |
| **Q4** | **B** | Contaminants in the weak solvent component accumulate at the column inlet during re-equilibration; doubling the hold time doubles accumulated peak area. | Dolan (2007) *LCGC* 25(8), 704–712 |
| **Q5** | **B** | Pressure dropping from 380 bar to 5 bar upon disconnecting column inlet proves the hydraulic restriction is inside the column inlet frit or bed. | Snyder et al. (1997) |
| **Q6** | **B** | Ibuprofen ($pK_a 4.4$) elutes earlier when mobile phase pH increases because ionization increases, decreasing hydrophobic retention on reverse phase. | Neue (1997) *HPLC Columns* |
| **Q7** | **B** | Basic amine solutes undergo secondary ion exchange with residual acidic silanols ($\equiv\text{Si}-\text{O}^-$), causing severe tailing on non-deactivated silicas. | Dolan (2004) *LCGC* 22(10), 972–980 |
| **Q8** | **B** | Standard pump degassing sequence requires opening purge valve and flushing at high flow (5 mL/min) with thoroughly degassed mobile phase. | Meyer (2010) |
| **Q9** | **A** | Physical bed void distorts all peaks universally; injection solvent mismatch causes band broadening that diminishes with retention factor. | Dolan (2008) *LCGC* 26(3), 258–264 |
| **Q10** | **A** | Pre-injector leak loses solvent before sample is introduced; retention times lengthen and pressure drops, but 100% of injected sample reaches detector. | Dolan (2008) *LCGC* 26(9), 890–896 |
"""

scoring_rubric = """# SCORING RUBRIC & EVALUATION PROTOCOL
**Document ID:** P4-RUBRIC-2026-REV1  

---

## 1. PRE-TEST & POST-TEST SCORING
- **Scoring Scale:** Binary 0 or 1 point per question (Total score: 0 to 10 points).
- **Rule:** Exact match with master answer key required.
- **Ambiguity Rule:** If a participant selects multiple options on paper, the item is scored 0.

---

## 2. PRACTICAL DIAGNOSTIC TASK SCORING (4 UNKNOWN SCENARIOS)
Each scenario is scored on a **3-point analytical rubric** (Total: 0 to 12 points across 4 tasks):

| Diagnostic Component | 0 Points (Inadequate) | 1 Point (Partial) | 2 Points (Complete / Competent) |
| :--- | :--- | :--- | :--- |
| **Fault Identification** | Incorrect diagnosis (e.g., calls column void a leak). | Identifies symptom correctly but misclassifies fault category. | Correctly identifies precise fault mode (e.g., "Air bubble in pump head"). |
| **Physical Reasoning** | Flawed or absent reasoning; guesses without citing evidence. | Cites observable symptom (e.g., "pressure dropped") without linking to mechanism. | Correctly explains underlying mechanism (e.g., "air compression during pump stroke reduces effective flow"). |
| **Corrective Action** | Dangerous or counterproductive action (e.g., "inject more sample"). | Vague action (e.g., "fix pump"). | Actionable, industry-standard corrective procedure (e.g., "open purge valve, prime with degassed ACN at 5 mL/min"). |

---

## 3. BLIND SCORING & INTER-RATER RELIABILITY
- To eliminate grader bias, qualitative reasoning on the practical task is independently scored by two trained graders blinded to participant ID and intervention timing.
- Inter-rater agreement evaluated via Cohen's Kappa ($\kappa$); disagreements resolved by consensus adjudication with a third senior faculty reviewer.
"""

practical_task = """# PRACTICAL DIAGNOSTIC PERFORMANCE TASK (4 UNKNOWN SCENARIOS)
**Document ID:** P4-TASK-2026-REV1  
**Format:** Interactive In-Software Evaluation Sheet  
**Session Timing:** Minutes 30 to 40  

---

**Participant ID Code:** ____________________  

### Instructions for Students:
You will be presented with four unknown simulated runs on your computer screen. For each scenario:
1. Examine the real-time pressure gauge and the resulting chromatogram.
2. Select the primary fault mode from the diagnostic drop-down list.
3. Record your confidence level from 1 (Pure guess) to 5 (Completely confident).
4. Explain in 1–2 sentences the physical reason for your diagnosis.
5. State the immediate corrective action an analyst should take.

---

### Scenario Alpha (Unknown Run 1)
- **Observed Instrument Readout:** Backpressure reads 62 bar (normal baseline is 82 bar). Baseline is stable without spikes. All four peaks elute $\sim 30\%$ later than normal ($t_R$ increased from 2.8, 3.5, 6.2, 9.0 min to 3.6, 4.5, 8.0, 11.7 min). Peak widths and symmetry remain normal.
- **Your Diagnosis:** [ ] Air Bubble  [ ] System Fitting Leak  [ ] Column Void  [ ] Contamination  [ ] Normal Run
- **Confidence:** [ ] 1 (Guess)  [ ] 2  [ ] 3  [ ] 4  [ ] 5 (Certain)
- **Reasoning:** __________________________________________________________________________________
- **Corrective Action:** ___________________________________________________________________________

---

### Scenario Beta (Unknown Run 2)
- **Observed Instrument Readout:** Backpressure reads 82 bar (normal). Every peak in the chromatogram exhibits a pronounced notch / split top, appearing as a doublet. Peak tailing factor is 2.5. Total plate count is reduced by $> 50\%$. Retention times are slightly shorter than normal.
- **Your Diagnosis:** [ ] Air Bubble  [ ] System Fitting Leak  [ ] Column Void  [ ] Contamination  [ ] Normal Run
- **Confidence:** [ ] 1 (Guess)  [ ] 2  [ ] 3  [ ] 4  [ ] 5 (Certain)
- **Reasoning:** __________________________________________________________________________________
- **Corrective Action:** ___________________________________________________________________________

---

### Scenario Gamma (Unknown Run 3)
- **Observed Instrument Readout:** Backpressure fluctuates between 60 bar and 82 bar cyclically. The baseline displays sharp negative and positive spikes. Retention times show small, irregular variations ($\pm 0.1\text{ min}$). Peak shapes are otherwise unaffected.
- **Your Diagnosis:** [ ] Air Bubble  [ ] System Fitting Leak  [ ] Column Void  [ ] Contamination  [ ] Normal Run
- **Confidence:** [ ] 1 (Guess)  [ ] 2  [ ] 3  [ ] 4  [ ] 5 (Certain)
- **Reasoning:** __________________________________________________________________________________
- **Corrective Action:** ___________________________________________________________________________

---

### Scenario Delta (Unknown Run 4)
- **Observed Instrument Readout:** Backpressure reads 87 bar. Three small, unassigned peaks elute at 1.8 min, 4.2 min, and 7.1 min that do not correspond to any component of the analgesic standard. Baseline noise is elevated (3x baseline).
- **Your Diagnosis:** [ ] Air Bubble  [ ] System Fitting Leak  [ ] Column Void  [ ] Contamination  [ ] Normal Run
- **Confidence:** [ ] 1 (Guess)  [ ] 2  [ ] 3  [ ] 4  [ ] 5 (Certain)
- **Reasoning:** __________________________________________________________________________________
- **Corrective Action:** ___________________________________________________________________________
"""

write_both("03_ASSESSMENT_INSTRUMENTS/pretest.md", pretest)
write_both("03_ASSESSMENT_INSTRUMENTS/posttest.md", posttest)
write_both("03_ASSESSMENT_INSTRUMENTS/answer_key.md", answer_key)
write_both("03_ASSESSMENT_INSTRUMENTS/scoring_rubric.md", scoring_rubric)
write_both("03_ASSESSMENT_INSTRUMENTS/practical_diagnostic_task.md", practical_task)

print("--- PART 2 COMPLETED (Folders 02 and 03) ---")
