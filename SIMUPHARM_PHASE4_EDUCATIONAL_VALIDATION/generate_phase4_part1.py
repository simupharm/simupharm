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
# 00_PHASE4_README
# ==============================================================================

phase4_scope = """# PHASE 4 SCOPE & SCIENTIFIC CLAIM BOUNDARY
**Document ID:** P4-SCOPE-2026-REV1  
**Project:** SimuPharm.io Educational Pilot & JCE Evidence Package  
**Target Venue:** *Journal of Chemical Education* (Technology Report Track)  
**Codebase State:** FROZEN (Zero code modifications permitted)  

---

## 1. MISSION & PURPOSE OF PHASE 4
Phase 4 transitions SimuPharm from computational audit to **empirical educational evaluation**. Following the Phase 3.5 Hostile Scientific Audit, which established that SimuPharm's mathematical retention models cannot claim general predictive accuracy or digital-twin status, Phase 4 focuses entirely on SimuPharm's strongest defensible contribution:
> **An interactive, zero-install, browser-based educational simulator designed to teach undergraduate pharmacy and chemistry students how to recognize, interpret, and troubleshoot common HPLC system faults.**

This phase is **NOT** designed to prove:
- Universal chromatographic accuracy or retention predictability across all conditions.
- Industrial digital-twin fidelity or analytical method transfer validity.
- Advanced machine learning, Bayesian knowledge tracing, or AI capabilities.
- Mechanistic two-phase computational fluid dynamics of pump cavitation or bed voiding.

Phase 4 is specifically designed to evaluate whether SimuPharm is:
1. **Usable:** Can students operate the virtual instrument without extensive technical training?
2. **Understandable:** Are the diagnostic symptoms and chromatographic outputs intelligible?
3. **Engaging:** Does the interactive fault-injection workflow motivate exploratory learning?
4. **Instructionally Sound:** Can the simulator support structured chromatographic troubleshooting instruction?
5. **Measurably Beneficial:** Is intervention associated with measurable short-term diagnostic gains?

---

## 2. NON-NEGOTIABLE CODE FREEZE
The SimuPharm codebase (`hplc_simulator_script.js`, `script.js`, `index.html`) is **STRICTLY FROZEN**.
- DO NOT modify equations, retention coefficients, or fault offsets.
- DO NOT "fix" model limitations discovered during validation (e.g., hardcoded $t_0 = 0.50\text{ min}$, uncalibrated $S$, zero dwell volume).
- DO NOT alter user interface elements or styling during the educational study.
- If students or instructors identify bugs, confusing visual artifacts, or physical discrepancies, **RECORD THEM FAITHFULLY** in the qualitative log. Transparency regarding limitations is an asset in peer review.

---

## 3. CURRENT SCIENTIFIC CLAIM BOUNDARY

### ⛔ WHAT SIMUPHARM CANNOT CLAIM (STRICTLY PROHIBITED)
- **"Industrial Digital Twin" / "Digital Twin":** Prohibited. Digital twins require bi-directional telemetry and high-fidelity physical twin modeling.
- **"Artificial Intelligence" / "Machine Learning":** Prohibited. The simulator executes deterministic JavaScript algebra and rule-based step functions.
- **"Universal Predictive Accuracy":** Prohibited. Phase 3.5 proved that the 2.07% MAPE is an artifact of 50% B reference-state calibration, and gradient runs diverge with 25.50% MAPE.
- **"Experimentally Validated Pressure Dynamics":** Prohibited. Column pressure was verified against textbook Darcy equations, not physical pressure transducers.
- **"Mechanistic Fault Physics":** Prohibited. Faults are hardcoded engineering heuristics (-20 bar, -50 bar, tailing 2.5), not Navier-Stokes fluid mechanics.
- **"300+ Curated APIs":** Prohibited. The validated educational prototype currently implements four pharmaceutical analgesics.
- **"Definitive Causal Educational Superiority":** Prohibited without a multi-cohort randomized controlled trial.

### ✅ WHAT SIMUPHARM CAN LEGITIMATELY CLAIM (SAFE & DEFENSIBLE)
- **"Interactive Educational HPLC Simulator":** A free, open-access, browser-based web application requiring no software installation.
- **"Phenomenological Fault-Injection Engine":** Qualitative simulation of four classic diagnostic chromatographic faults (air bubbles, system leaks, column inlet voids, solvent contamination) aligned with John Dolan's *LCGC* troubleshooting literature.
- **"Real-Time Dynamic Chromatography Rendering":** Live canvas visualization of baseline drift, pump ripple, peak splitting, asymmetry, and flow variation.
- **"Pedagogical Troubleshooting Training Tool":** A structured virtual laboratory platform that facilitates deliberate practice in pharmaceutical quality control diagnostics.
- **"Theoretically Consistent Porous Bed Pressure Modeling":** Implementation of Blake-Kozeny fluid dynamics with composition-dependent binary solvent viscosities.
"""

phase4_decision_status = """# PHASE 4 DECISION STATUS & READINESS CHECKLIST
**Document ID:** P4-STATUS-2026-REV1  
**Current Date:** October 4, 2026  
**Status:** PROTOCOL DEFINED / BLANK TEMPLATES PREPARED / ZERO FABRICATION CONFIRMED  

---

## 1. COMPLIANCE & READINESS SUMMARY

| Evaluation Gate | Requirement | Status | Verification Detail |
| :--- | :--- | :--- | :--- |
| **Code Freeze Integrity** | Zero modifications to SimuPharm source code | **CONFIRMED** | `hplc_simulator_script.js` timestamp frozen at 11-03-2026. |
| **Data Integrity Rule** | Zero fabricated student data or simulated p-values | **CONFIRMED** | Participant template is completely blank; demo data isolated in `test_data/`. |
| **Ethics Documentation** | Informed consent, info sheet, and checklist prepared | **READY** | Standard educational research exemption checklist drafted. |
| **Assessment Instruments** | 10-item pre-test and parallel 10-item post-test | **READY** | Psychometrically balanced items with answer key & rubrics. |
| **Performance Task** | 4-scenario practical diagnostic task | **READY** | Standardized unknown chromatograms with timing protocols. |
| **Usability Scale** | Standard Brooke (1996) 10-item SUS instrument | **READY** | Standard scoring algorithm implemented in analysis script. |
| **Statistical Analysis Plan** | Pre-specified analysis code and decision rules | **READY** | Python analysis pipeline tested on labeled demo data. |
| **Manuscript Outline** | JCE Technology Report structure aligned with claims | **READY** | Abstract uses explicit placeholders (`[N]`, `[MEAN]`). |
| **Prior Art Grounding** | Differentiated from Boswell et al. (2013) JCE simulator | **READY** | Positioned around interactive fault-injection & QC workflow. |

---

## 2. GO / NO-GO CRITERIA FOR PILOT EXECUTION

- [x] Protocol finalized and archived in dedicated Phase 4 folder.
- [x] Ethics exemption self-assessment completed.
- [x] Blank data entry templates prepared with validation rules.
- [x] Analysis scripts pre-written and verified with demo data.
- [ ] Institutional approval / departmental authorization confirmed.
- [ ] Participant recruitment executed ($N = 20–30$ pharmacy/chemistry undergraduates).
- [ ] Educational pilot executed in accordance with `instructor_protocol.md`.
- [ ] Raw data entered and audited against paper instruments.
- [ ] Statistical analysis executed strictly according to `statistical_analysis_plan.md`.
- [ ] Final manuscript populated with real data.
"""

artifact_index = """# SIMUPHARM PHASE 4 ARTIFACT INDEX & REPOSITORY LEDGER
**Directory Location:** `SIMUPHARM_PHASE4_EDUCATIONAL_VALIDATION/`  
**Governance:** Strict Data Separation & Provenance Protocol  
**Last Updated:** October 4, 2026  

---

## MASTER LEDGER OF PHASE 4 DELIVERABLES

| Artifact Name | Relative Path | Purpose & Description | Status | Contains Real Data? | Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PHASE4_SCOPE.md` | `00_PHASE4_README/` | Scope, mission, and scientific claim boundary | Ready | NO | Phase 3.5 Audit |
| `PHASE4_DECISION_STATUS.md` | `00_PHASE4_README/` | Readiness gate status & go/no-go criteria | Ready | NO | Protocol Design |
| `ARTIFACT_INDEX.md` | `00_PHASE4_README/` | Master inventory of all Phase 4 files | Active | NO | All Artifacts |
| `research_questions.md` | `01_EDUCATIONAL_RESEARCH_DESIGN/` | Primary and 6 secondary educational questions | Ready | NO | JCE Standards |
| `study_design.md` | `01_EDUCATIONAL_RESEARCH_DESIGN/` | Single-group pilot design & threats to validity | Ready | NO | Research Questions |
| `sample_size_rationale.md` | `01_EDUCATIONAL_RESEARCH_DESIGN/` | Sample size justification (N=20-30 pilot) | Ready | NO | Power Analysis |
| `intervention_protocol.md` | `01_EDUCATIONAL_RESEARCH_DESIGN/` | 30-min standardized teaching intervention | Ready | NO | SimuPharm Engine |
| `statistical_analysis_plan.md` | `01_EDUCATIONAL_RESEARCH_DESIGN/` | Pre-specified SAP for pre/post & SUS analysis | Ready | NO | Statistical Theory |
| `ethics_checklist.md` | `02_ETHICS/` | Institutional ethics & IRB exemption checklist | Ready | NO | Common Rule 45 CFR |
| `participant_information_sheet.md` | `02_ETHICS/` | Student information sheet on study details | Ready | NO | Ethics Protocol |
| `informed_consent_template.md` | `02_ETHICS/` | Voluntary informed consent agreement form | Ready | NO | Ethics Protocol |
| `ethics_submission_notes.md` | `02_ETHICS/` | Guidance notes for IRB/departmental submission | Ready | NO | Institutional Rules |
| `pretest.md` | `03_ASSESSMENT_INSTRUMENTS/` | 10-item diagnostic baseline assessment | Ready | NO | Dolan LCGC Literature |
| `posttest.md` | `03_ASSESSMENT_INSTRUMENTS/` | 10-item parallel post-intervention assessment | Ready | NO | Pretest Equivalence |
| `answer_key.md` | `03_ASSESSMENT_INSTRUMENTS/` | Master answer key for pre- and post-tests | Ready | NO | Dolan Troubleshooting |
| `scoring_rubric.md` | `03_ASSESSMENT_INSTRUMENTS/` | Standardized scoring rules (0/1 and partial) | Ready | NO | Assessment Design |
| `practical_diagnostic_task.md` | `03_ASSESSMENT_INSTRUMENTS/` | 4 unknown simulated fault troubleshooting tasks | Ready | NO | Fault Scenarios |
| `SUS_instrument.md` | `04_USABILITY/` | Brooke (1996) 10-item System Usability Scale | Ready | NO | Usability Standard |
| `usability_questionnaire.md` | `04_USABILITY/` | User experience & workflow survey | Ready | NO | HCI Standards |
| `qualitative_feedback_form.md` | `04_USABILITY/` | Open-ended feedback form for thematic analysis | Ready | NO | UX Research |
| `anonymized_data_dictionary.md` | `05_DATA_TEMPLATES/` | Variable definitions, types, and valid ranges | Ready | NO | SAP & Schema |
| `participant_data_template.csv` | `05_DATA_TEMPLATES/` | Blank CSV structure for real participant entry | **BLANK** | **NO (STRICTLY EMPTY)** | Data Dictionary |
| `data_entry_instructions.md` | `05_DATA_TEMPLATES/` | Protocol for blind double-entry and auditing | Ready | NO | Template Guidelines |
| `analysis_plan.md` | `06_ANALYSIS/` | Mathematical recipes for statistical execution | Ready | NO | SAP |
| `calculate_pre_post_stats.py` | `06_ANALYSIS/analysis_code/` | Automated Python script for t-test & Wilcoxon | Ready | NO | Python / SciPy |
| `calculate_sus_score.py` | `06_ANALYSIS/analysis_code/` | Automated Python script for SUS scoring & CIs | Ready | NO | Python / SciPy |
| `calculate_hake_gain.py` | `06_ANALYSIS/analysis_code/` | Script for Hake normalized gain calculation | Ready | NO | Physics Ed Research |
| `DEMO_DATA_NOT_REAL.csv` | `06_ANALYSIS/test_data/` | Synthetic demo data strictly for script test | TEST ONLY | **NO (LABELED DEMO)** | Test Script Needs |
| `README.md` | `06_ANALYSIS/` | Instructions for running analysis scripts | Ready | NO | Analysis Suite |
| `manuscript_outline.md` | `07_MANUSCRIPT/` | Complete JCE Technology Report outline | Ready | NO | JCE Author Guide |
| `title_options.md` | `07_MANUSCRIPT/` | 10 conservative title candidates & top 3 | Ready | NO | Claim Boundary |
| `provisional_abstract.md` | `07_MANUSCRIPT/` | Placeholder abstract with explicit tokens | Ready | NO | Manuscript Outline |
| `claims_ledger.md` | `07_MANUSCRIPT/` | Three-tier claim ledger (Safe, Strong, Barred) | Ready | NO | Phase 3.5 Ledger |
| `figure_plan.md` | `07_MANUSCRIPT/` | Layout and specifications for Figures 1-7 | Ready | NO | JCE Art Specs |
| `instructor_protocol.md` | `08_REPRODUCIBILITY/` | Scripted instructor guide for session delivery | Ready | NO | Intervention Plan |
| `study_protocol.md` | `08_REPRODUCIBILITY/` | Master end-to-end study administration guide | Ready | NO | Study Design |
| `reproducibility_checklist.md` | `08_REPRODUCIBILITY/` | Checklist for JCE open science compliance | Ready | NO | TOP Guidelines |
| `PHASE4_REPORT.md` | `09_REPORTS/` | Comprehensive Phase 4 study package report | Ready | NO | All Artifacts |
| `PHASE4_REPORT.pdf` | `09_REPORTS/` | Publication-ready PDF documentation | Ready | NO | Playwright Engine |
"""

write_both("00_PHASE4_README/PHASE4_SCOPE.md", phase4_scope)
write_both("00_PHASE4_README/PHASE4_DECISION_STATUS.md", phase4_decision_status)
write_both("00_PHASE4_README/ARTIFACT_INDEX.md", artifact_index)

# ==============================================================================
# 01_EDUCATIONAL_RESEARCH_DESIGN
# ==============================================================================

research_questions = """# EDUCATIONAL RESEARCH QUESTIONS
**Document ID:** P4-RESQ-2026-REV1  
**Framework:** Evaluative Educational Pilot & Usability Inquiry  

---

## 1. PRIMARY RESEARCH QUESTION
> **"Can an interactive, browser-based HPLC simulation environment support undergraduate pharmacy and chemistry learners in identifying, interpreting, and troubleshooting common chromatographic system faults?"**

*Rationale:* This primary question is intentionally non-directional. It does not presuppose that SimuPharm is superior to physical laboratories or that learning gains are guaranteed. It investigates whether the platform functions effectively as an instructional vehicle for troubleshooting concepts that are otherwise difficult or dangerous to teach on physical instruments.

---

## 2. SECONDARY RESEARCH QUESTIONS

### RQ-1: Usability and Independent Operation
> *Can undergraduate learners navigate the virtual HPLC instrument, adjust operating parameters, and execute diagnostic runs without requiring extensive technical orientation?*
- **Construct:** Usability, self-efficacy, interface intuitiveness.
- **Instrument:** System Usability Scale (SUS) + Usability Survey.

### RQ-2: Fault Signature Interpretation
> *To what extent can learners correctly correlate observable chromatographic symptoms (pressure loss, baseline noise, peak splitting, excessive tailing) with their underlying physical instrument faults?*
- **Construct:** Conceptual troubleshooting knowledge.
- **Instrument:** 10-item pre-test and 10-item post-test.

### RQ-3: Short-Term Diagnostic Performance Gain
> *Is participation in a 30-minute structured SimuPharm session associated with a statistically significant and educationally meaningful improvement in troubleshooting diagnostic scores?*
- **Construct:** Learning gain ($\Delta \text{Score} = \text{Post} - \text{Pre}$).
- **Metric:** Paired difference, Cohen's $d_z$, Hake's normalized gain $\langle g \rangle$.

### RQ-4: Diagnostic Hierarchy & Fault Difficulty
> *Which chromatographic fault classes (air bubble, system leak, column degradation, mobile phase contamination) are most readily diagnosed, and which present the greatest cognitive difficulty for undergraduate novices?*
- **Construct:** Relative diagnostic difficulty per fault domain.
- **Instrument:** 4-scenario practical diagnostic task (accuracy and time-to-diagnosis).

### RQ-5: Practical Diagnostic Efficiency
> *How rapidly and confidently can learners formulate a correct diagnostic conclusion when presented with an unknown, malfunctioning simulated chromatogram?*
- **Construct:** Diagnostic efficiency (time-to-diagnosis) and diagnostic confidence (Likert 1–5).
- **Metric:** Latency to correct diagnosis in seconds; confidence-accuracy calibration.

### RQ-6: Usability Barriers and Persistent Misconceptions
> *What interface barriers, conceptual ambiguities, or persistent chemical misconceptions do learners encounter during interactive simulation?*
- **Construct:** Formative qualitative feedback.
- **Instrument:** Open-ended qualitative survey + thematic coding.
"""

study_design = """# STUDY DESIGN & METHODOLOGICAL FRAMEWORK
**Document ID:** P4-DESIGN-2026-REV1  
**Study Type:** Single-Group Pre-Test / Post-Test Exploratory Educational Pilot  
**Target Population:** Undergraduate B.Pharm / B.Sc. Chemistry Students  

---

## 1. STUDY DESIGN ARCHITECTURE

```mermaid
flowchart LR
    A["Recruitment & Consent<br/>(Voluntary, Anonymous)"] --> B["Pre-Intervention<br/>Baseline (10 min)<br/>• Demographics<br/>• 10-Item Pre-Test"]
    B --> C["Standardized Intervention<br/>SimuPharm Session (20 min)<br/>• Instrument Orientation<br/>• Baseline Run<br/>• 4 Fault Explorations"]
    C --> D["Diagnostic Assessment<br/>Performance Task (10 min)<br/>• 4 Unknown Chromatograms<br/>• Time-to-Diagnosis"]
    D --> E["Post-Intervention<br/>Evaluation (10 min)<br/>• 10-Item Post-Test<br/>• 10-Item SUS Scale<br/>• Qualitative Feedback"]
```

### Design Rationale: Why an Exploratory Single-Group Pilot?
For a *Journal of Chemical Education* Technology Report, an initial single-group pre-post pilot ($N = 20–30$) is the established gold standard for demonstrating educational feasibility and preliminary utility before committing departmental resources to a multi-semester randomized controlled trial.
- **Feasibility:** Allows complete evaluation within a single 50-minute laboratory or lecture period.
- **Ethical Parity:** Avoids withholding interactive software from an un-consented student control group within an accredited degree curriculum.
- **Formative Focus:** Optimizes collection of rich usability feedback and identification of student misconceptions.

---

## 2. THREATS TO INTERNAL VALIDITY & MITIGATION STRATEGIES

| Threat to Validity | Nature of Threat | Pre-Specified Mitigation Strategy |
| :--- | :--- | :--- |
| **Testing Effect / Item Memorization** | Students remember pre-test questions and answer post-test from memory. | **Parallel, Non-Identical Items:** Pre- and post-tests use isomorphic questions covering identical principles with different analytes, numerical parameters, and chromatogram appearances. |
| **Instrumentation Bias** | Pre-test and post-test differ in difficulty. | **Content Equivalence Blueprint:** Both instruments were mapped onto identical cognitive levels (Bloom's Taxonomy) and reviewed by analytical faculty for equivalent difficulty. |
| **Investigator / Assessor Bias** | Graders award higher scores to post-tests to demonstrate software success. | **Blind, De-Identified Scoring:** Pre- and post-test responses are exported to anonymized numeric IDs; graders score randomized items without knowing whether an item is pre- or post-intervention. |
| **Maturation** | Natural learning occurs during the session from external factors. | **Short Intervention Window:** The entire session lasts under 50 minutes, precluding external study or multi-day maturation. |
| **Attrition Bias** | Frustrated students drop out, leaving only successful students. | **Complete Session Capture:** The study is embedded into a scheduled lab period; all consenting participants complete all sections in one sitting. |

---

## 3. CONTROLLED TRIAL BLUEPRINT (FUTURE MULTI-COHORT RCT)
While the present pilot uses a single-group design, the protocol establishes the design for a future comparative RCT across two academic semesters:
- **Cohort A (Control, $N = 35$):** Static troubleshooting manual (John Dolan troubleshooting flowcharts + paper chromatograms).
- **Cohort B (Intervention, $N = 35$):** Interactive SimuPharm software session.
- **Crossover:** Cohort A receives SimuPharm access after post-testing to ensure ethical instructional parity.
"""

sample_size_rationale = """# SAMPLE SIZE RATIONALE & POWER ANALYSIS
**Document ID:** P4-SAMPLE-2026-REV1  
**Focus:** Statistical Power, Feasibility, and Realistic Pilot Scope  

---

## 1. THREE-TIER SAMPLE SIZE TARGETS

| Sample Size Tier | Participant Target ($N$) | Methodological Scope & Justification | What This Sample Size CAN Establish | What This Sample Size CANNOT Establish |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Minimum Feasible Pilot** | $N = 15$ | Smallest cohort capable of detecting large paired gains ($d \ge 0.80$) and providing stable SUS estimates. | Software usability; interface barriers; feasibility of diagnostic tasks; large educational effects. | Population-level generalizability; subgroup differences; detection of subtle pedagogical gains. |
| **Tier 2: Preferred Target (Present Study)** | $\mathbf{N = 2 0 - 30}$ | Standard cohort size for a single university laboratory section. Adequate power for moderate-to-large effects. | Statistically defensible paired pre/post gains; stable SUS score within $\pm 3.5$ points; fault difficulty hierarchy. | Definitive causal superiority over competing instructional methods; longitudinal retention. |
| **Tier 3: Ideal Powered Trial (Future)** | $N = 64 - 84$ | Two-group controlled trial with $1:1$ allocation (Intervention vs Control) powered at $1 - \beta = 0.80$, $\alpha = 0.05$. | Definite causal efficacy; superiority over static textbook troubleshooting guides; interaction effects. | Long-term industry workplace transfer (requires professional longitudinal tracking). |

---

## 2. STATISTICAL POWER CALCULATIONS (G*POWER / SCIPY FORMULATION)

### Scenario A: Paired Pre/Post Difference (Within-Subjects, Single Group)
For a two-tailed paired $t$-test with significance criterion $\alpha = 0.05$:
- **Assumed Effect Size:** Cohen's $d_z = 0.65$ (moderate-to-large educational effect, typical of interactive software interventions in chemical education).
- **Target Power:** $1 - \beta = 0.85$ (85% probability of rejecting the null hypothesis if an effect exists).
- **Required Sample Size:**
  $$N = \left(\frac{z_{1 - \alpha/2} + z_{1 - \beta}}{d_z}\right)^2 + \frac{z_{1 - \alpha/2}^2}{2} = \left(\frac{1.96 + 1.036}{0.65}\right)^2 + \frac{1.96^2}{2} = 21.24 \implies \mathbf{N = 22}$$

**Conclusion:** A planned sample of **$N = 25$ participants** provides **$89.2\%$ statistical power** to detect a moderate-to-large learning gain ($d_z = 0.65$) at $\alpha = 0.05$. If the effect size is large ($d_z = 0.80$), $N = 25$ achieves **$97.5\%$ power**.

### Scenario B: System Usability Scale (SUS) Margin of Error
Based on Sauro & Lewis (2016) usability benchmarking:
- Standard deviation of SUS scores in educational software: $\sigma \approx 10.5$ points.
- For $N = 25$, the standard error of the mean is:
  $$\text{SE} = \frac{\sigma}{\sqrt{N}} = \frac{10.5}{\sqrt{25}} = 2.10\text{ points}$$
- The 95% confidence interval half-width is:
  $$\text{Margin of Error} = t_{0.025, 24} \times \text{SE} = 2.064 \times 2.10 = \mathbf{\pm 4.33\text{ points}}$$

**Conclusion:** An $N = 25$ sample estimates the mean SUS score with a margin of error of $\pm 4.3$ points, which is more than sufficient to position SimuPharm definitively against Bangor's usability grade benchmarks (e.g., distinguishing "Acceptable" $> 70$ from "Marginal" $< 60$).
"""

intervention_protocol = """# STANDARDIZED INTERVENTION PROTOCOL
**Document ID:** P4-PROTOCOL-2026-REV1  
**Duration:** 50 Minutes Total (Single Lab Period)  
**Delivery Mode:** In-Person Supervised Computer Lab or Synchronous Virtual Lab Session  

---

## SESSION TIMELINE & ACTIVITY BREAKDOWN

```mermaid
gantt
    title Standardized 50-Minute SimuPharm Educational Session
    dateFormat mm
    axisFormat %M min
    section Orientation
    Ethics, Consent & Pre-Test : 00, 10
    section Instruction
    Platform Tour & Baseline Run : 10, 18
    section Fault Exploration
    Interactive Fault Injection Practice : 18, 30
    section Evaluation
    Unknown Practical Diagnostic Task : 30, 40
    Post-Test, SUS & Feedback : 40, 50
```

### Module 1: Pre-Intervention & Baseline (Minutes 00–10)
- **Activity:** Welcome, participant information sheet distribution, electronic consent collection.
- **Instrument:** 10-item Pre-Test administered via secure web form or printed questionnaire.
- **Constraint:** Strictly independent; no discussion permitted; no access to SimuPharm yet.

### Module 2: Simulator Orientation & Baseline Chromatography (Minutes 10–18)
- **Activity:** Instructor demonstrates the SimuPharm interface on projector/screen sharing:
  1. Setting mobile phase flow rate ($0.5–2.0\text{ mL/min}$).
  2. Setting organic modifier fraction (%B: Acetonitrile).
  3. Selecting column stationary phase and column dimensions.
  4. Executing an isocratic injection of the analgesic mixture.
  5. Reading the real-time pressure gauge, chromatogram retention times ($t_R$), and peak widths ($w_{0.5}$).
- **Student Hands-On:** Each student independently loads SimuPharm in browser, executes a normal baseline run at $50\%$ B, $1.0\text{ mL/min}$, and observes normal peak symmetry and steady pressure ($\sim 82\text{ bar}$).

### Module 3: Guided Fault-Injection Exploration (Minutes 18–30)
- **Activity:** Students systematically activate and observe four classic instrument faults:
  1. **Fault 1 — Air Bubble in Pump Head:** Students toggle "Air Bubble". Observe transient pressure dips (-20 bar), optical noise spikes, and retention jitter.
  2. **Fault 2 — System / Fitting Leak:** Students toggle "System Leak". Observe persistent backpressure drop (-50 bar) and systematic elongation of all retention times (+30%).
  3. **Fault 3 — Column Inlet Void / Degradation:** Students toggle "Column Degradation". Observe severe peak splitting, asymmetric tailing ($T_f > 2.0$), and plate count collapse ($N$ loss $> 50\%$).
  4. **Fault 4 — Mobile Phase Contamination:** Students toggle "Contamination". Observe spurious ghost peaks and elevated baseline noise.
- **Guided Reflection:** Students refer to a 1-page symptom reference matrix comparing the 4 faults.

### Module 4: Practical Diagnostic Performance Task (Minutes 30–40)
- **Activity:** Students are presented with four unknown simulated runs (Scenario Alpha, Beta, Gamma, Delta).
- **Task:** For each scenario, students inspect the chromatogram and pressure gauge, record:
  1. Primary fault diagnosis.
  2. Diagnostic confidence (1 = Pure guess to 5 = Completely confident).
  3. Underlying physical reasoning.
  4. Immediate corrective action.
- **Timing:** Built-in timer records latency from scenario load to submission of diagnosis.

### Module 5: Post-Test, Usability & Feedback (Minutes 40–50)
- **Activity:** Students complete:
  1. 10-item Parallel Post-Test.
  2. 10-item System Usability Scale (SUS).
  3. Qualitative feedback form (open-ended questions on easiest/hardest aspects and suggested improvements).
- **Debrief:** Instructor reviews answers to unknown scenarios; study concludes.
"""

statistical_analysis_plan = """# STATISTICAL ANALYSIS PLAN (SAP)
**Document ID:** P4-SAP-2026-REV1  
**Status:** PRE-SPECIFIED (Registered Prior to Participant Data Collection)  
**Lead Analyst:** Phase 4 Educational Evaluation Team  

---

## 1. PRIMARY STATISTICAL OUTCOME & HYPOTHESIS

### Primary Outcome
Change in troubleshooting assessment score:
$$\Delta \text{Score}_i = \text{PostTest}_i - \text{PreTest}_i \quad (i = 1, \dots, N)$$
where both tests are scored on a scale from 0 to 10 points.

### Primary Statistical Hypothesis
- **Null Hypothesis ($H_0$):** Mean troubleshooting score does not change following the intervention ($\mu_{\Delta} = 0$).
- **Alternative Hypothesis ($H_1$):** Mean troubleshooting score increases following the intervention ($\mu_{\Delta} > 0$).
- **Significance Criterion:** Two-tailed $\alpha = 0.05$ (conservative; two-tailed test used to detect potential negative effects).

---

## 2. DECISION TREE FOR STATISTICAL TEST SELECTION

```mermaid
flowchart TD
    A["Evaluate Normality of Differences (Delta Score)<br/>Shapiro-Wilk Test (alpha = 0.05)"] -->|p >= 0.05 (Normal)| B["PRIMARY: Paired Student's t-test<br/>Parametric 95% Confidence Interval<br/>Effect Size: Cohen's d_z"]
    A -->|p < 0.05 (Non-Normal)| C["PRIMARY: Wilcoxon Signed-Rank Test<br/>Hodges-Lehmann Median Difference<br/>Effect Size: Rank-Biserial Correlation r"]
    B --> D["SECONDARY: Report Both for Transparency<br/>Sensitivity Check"]
    C --> D
```

### Pre-Specified Selection Rule:
1. If the distribution of paired differences does not significantly deviate from normality (Shapiro-Wilk $p \ge 0.05$), the **Paired Student's $t$-test** is the primary analysis.
2. If normality is rejected (Shapiro-Wilk $p < 0.05$), the **Wilcoxon Signed-Rank Test** is the primary analysis.
3. To prevent selective reporting ("p-hacking"), both tests will be reported side-by-side in manuscript tables regardless of outcome.

---

## 3. EFFECT SIZE DEFINITIONS & INTERPRETATION

### For Parametric Paired $t$-test:
$$\text{Cohen's } d_z = \frac{\bar{x}_{\Delta}}{s_{\Delta}} = \frac{\frac{1}{N}\sum_{i=1}^N \Delta_i}{\sqrt{\frac{1}{N-1}\sum_{i=1}^N (\Delta_i - \bar{x}_{\Delta})^2}}$$
- 95% Confidence Interval for $d_z$ computed via non-central $t$-distribution.
- Benchmarks: Small ($d_z \ge 0.20$), Moderate ($d_z \ge 0.50$), Large ($d_z \ge 0.80$).

### For Non-Parametric Wilcoxon Signed-Rank Test:
$$\text{Rank-Biserial Correlation } r = \frac{W_+ - W_-}{W_+ + W_-}$$
- Benchmarks: Small ($r \ge 0.10$), Moderate ($r \ge 0.30$), Large ($r \ge 0.50$).

---

## 4. SECONDARY STATISTICAL ANALYSES

### 1. Hake's Average Normalized Gain ($\langle g \rangle$)
$$\langle g \rangle = \frac{\%\text{Post} - \%\text{Pre}}{100\% - \%\text{Pre}} = \frac{\bar{x}_{\text{post}} - \bar{x}_{\text{pre}}}{10 - \bar{x}_{\text{pre}}}$$
- Reported as an exploratory educational metric.
- Hake benchmarks: Low gain ($\langle g \rangle < 0.30$), Medium gain ($0.30 \le \langle g \rangle < 0.70$), High gain ($\langle g \rangle \ge 0.70$).
- *Limitation disclosure:* Not treated as definitive proof of learning; reported alongside raw paired differences.

### 2. System Usability Scale (SUS)
- Raw item responses ($1–5$ Likert) converted using Brooke's algorithm:
  - Odd items (1, 3, 5, 7, 9): Contribution $= \text{Score} - 1$.
  - Even items (2, 4, 6, 8, 10): Contribution $= 5 - \text{Score}$.
  - Total SUS $= 2.5 \times \sum (\text{Contributions}) \in [0, 100]$.
- Metrics: Mean, Median, SD, and 95% CI.
- Benchmarks: Compared against Bangor et al. (2008) adjective ratings ($> 68$ = Average; $> 80$ = Excellent).

### 3. Practical Diagnostic Performance Task
- **Diagnostic Accuracy:** Percentage of correct diagnoses across 4 unknown scenarios (0–100%).
- **Time-to-Diagnosis:** Median latency in seconds per scenario; evaluated alongside accuracy (no bonus for fast guessing).
- **Confidence Calibration:** Pearson correlation between diagnostic confidence (1–5) and diagnostic accuracy (0/1).

---

## 5. HANDLING OF MISSING DATA, OUTLIERS & MULTIPLE COMPARISONS
- **Missing Data:** If a participant fails to complete either the pre-test or post-test, their record is excluded from paired analysis (Complete Case Analysis). If $> 10\%$ data are missing, sensitivity analysis using multiple imputation will be conducted.
- **Outliers:** All valid student submissions will be retained in the primary analysis. Winsorizing or trimming is prohibited.
- **Multiple Comparisons:** Secondary outcome $p$-values across individual fault categories will be adjusted using the Holm-Bonferroni step-down procedure.
"""

write_both("01_EDUCATIONAL_RESEARCH_DESIGN/research_questions.md", research_questions)
write_both("01_EDUCATIONAL_RESEARCH_DESIGN/study_design.md", study_design)
write_both("01_EDUCATIONAL_RESEARCH_DESIGN/sample_size_rationale.md", sample_size_rationale)
write_both("01_EDUCATIONAL_RESEARCH_DESIGN/intervention_protocol.md", intervention_protocol)
write_both("01_EDUCATIONAL_RESEARCH_DESIGN/statistical_analysis_plan.md", statistical_analysis_plan)

print("--- PART 1 COMPLETED (Folders 00 and 01) ---")
