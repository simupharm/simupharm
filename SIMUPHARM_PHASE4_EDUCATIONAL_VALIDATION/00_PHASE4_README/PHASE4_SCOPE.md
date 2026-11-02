# PHASE 4 SCOPE & SCIENTIFIC CLAIM BOUNDARY
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
- DO NOT "fix" model limitations discovered during validation (e.g., hardcoded $t_0 = 0.50	ext{ min}$, uncalibrated $S$, zero dwell volume).
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
