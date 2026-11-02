# JCE TECHNOLOGY REPORT MANUSCRIPT ARCHITECTURE
**Document ID:** P4-MS-OUTLINE-2026-REV1  
**Target Journal:** *Journal of Chemical Education*  
**Article Type:** Technology Report (or Chemical Education Tip)  
**Estimated Length:** 3,800 Words (Excluding References & Supporting Information)  

---

## SECTION-BY-SECTION BLUEPRINT

### 1. TITLE
- Selected from `title_options.md` (e.g., *SimuPharm: An Interactive Browser-Based HPLC Simulator for Teaching Chromatographic Troubleshooting to Undergraduate Pharmacy Students*).

### 2. ABSTRACT (< 250 Words)
- Context: High equipment cost and safety constraints limit hands-on troubleshooting education on physical HPLC instruments.
- Tool: SimuPharm, a free, browser-based, zero-install educational HPLC simulator with phenomenological fault-injection capabilities.
- Educational Evaluation: Pilot study ($N = [N]$ students) evaluating usability (SUS) and diagnostic learning gains.
- Results Placeholder: Pre-test mean $[X]$, post-test mean $[Y]$, gain $[Z]$ ($p = [p]$, $d_z = [d]$); mean SUS $[S]$.
- Candid Limitations: Software uses simplified retention models and heuristic fault parameters; designed for foundational conceptual troubleshooting rather than method development.

### 3. INTRODUCTION
- The pedagogical challenge of chromatography education in pharmacy and chemistry curricula.
- Why equipment troubleshooting is rarely taught hands-on: fear of column fouling, detector cell damage, solvent wastage, and instrument downtime.
- Cognitive load and deliberate practice: benefits of interactive virtual simulation environments.
- Purpose of this paper: Introduce SimuPharm and evaluate its educational usability and preliminary diagnostic utility.

### 4. BACKGROUND & PRIOR ART POSITIONING
- Review of existing educational chromatography tools (e.g., Boswell et al. 2013 HPLC-Simulator).
- Clear differentiation:
  - Boswell focuses on method development, linear solvent strength calibration, and retention optimization.
  - SimuPharm introduces **real-time diagnostic fault injection** (pump cavitation, fluid leaks, column inlet collapse, solvent impurities) designed specifically for pharmaceutical quality control troubleshooting.
- Explicit disavowal of AI, machine learning, and digital twin claims.

### 5. SIMUPHARM PLATFORM & CHROMATOGRAPHIC ENGINE
- Frontend architecture: HTML5, CSS3, JavaScript (ES6+), HTML Canvas rendering (100% client-side, zero backend dependencies).
- Retention modeling: Isocratic and linear gradient retention using simplified linear solvent strength relationships.
- Fluidic backpressure: Real-time dynamic implementation of the Blake-Kozeny equation accounting for non-linear water-acetonitrile viscosity mixtures.
- Diagnostic Fault Injection Engine:
  - Air bubble in pump head (-20 bar, baseline optical noise spikes).
  - Pre-column system leak (-50 bar, systematic +30% retention time elongation).
  - Column bed void / collapse (+30 bar, severe peak splitting, tailing $T_f = 2.50$, plate count drop).
  - Mobile phase contamination (ghost peaks, elevated baseline drift).
- Pedagogical alignment with John Dolan's classic *LCGC* troubleshooting literature.

### 6. EDUCATIONAL USE CASE & LABORATORY INTEGRATION
- Description of the standardized 50-minute virtual lab session.
- Integration models: Pre-laboratory preparatory module, lecture demonstration tool, or asynchronous homework assignment.
- Alignment with ACPE (pharmacy) and ACS (chemistry) instrumental analysis competencies.

### 7. METHODS (EDUCATIONAL EVALUATION)
- Study design: Single-group exploratory educational pilot ($N = [N]$ undergraduate students).
- Participant profile: B.Pharm / B.Sc. Chemistry students with varying prior lab experience.
- Instructional protocol: 30-minute structured intervention (orientation, baseline run, fault exploration, unknown diagnostic tasks).
- Assessment instruments: 10-item pre-test and parallel 10-item post-test.
- Usability measurement: Standard 10-item System Usability Scale (Brooke 1996) + targeted UX survey.
- Qualitative inquiry: Open-ended feedback analyzed via inductive thematic coding.
- Statistical analysis: Pre-specified analysis plan (Shapiro-Wilk normality, paired $t$-test / Wilcoxon, Cohen's $d_z$, 95% CIs).

### 8. RESULTS (PRE-POPULATED PLACEHOLDERS)
- **Participant Demographics:** Sample size $N = [N]$, breakdown by degree and prior lab experience.
- **Diagnostic Learning Gains:** Pre-test score $[M \pm SD]$, post-test score $[M \pm SD]$, mean paired gain $[\Delta \pm SD]$, $t([df]) = [t]$, $p = [p]$, Cohen's $d_z = [d]$.
- **Normality & Non-Parametric Validation:** Wilcoxon signed-rank $W = [W]$, $p = [p]$, rank-biserial $r = [r]$.
- **Normalized Gain:** Hake's $\langle g angle = [g]$ (classification: [Category]).
- **Practical Unknown Diagnostic Performance:** Accuracy across 4 scenarios: Air bubble $[A\%]$, Leak $[B\%]$, Column Void $[C\%]$, Contamination $[D\%]$; median diagnosis latency $[T	ext{ sec}]$.
- **System Usability Scale (SUS):** Mean score $[S \pm SD]$ (Bangor rating: [Adjective]).
- **Targeted UX Ratings:** Visual clarity, feedback responsiveness, and pre-lab recommendation percentages.

### 9. QUALITATIVE FEEDBACK & STUDENT PERCEPTIONS
- Thematic analysis of positive perceptions (e.g., visual intuition, safe experimentation, pressure gauge clarity).
- Thematic analysis of negative / critical feedback (e.g., desire for broader drug library, confusion regarding split-peak mechanics, slider sensitivity).

### 10. CANDID DISCUSSION & MODEL LIMITATIONS
- **Scientific Engine Limitations:**
  - Hardcoded dead time ($t_0 = 0.50	ext{ min}$) distorts early eluters and gradient integration.
  - Heuristic $S$ slopes lead to out-of-sample gradient divergence (25.5% MAPE).
  - Lack of gradient dwell volume ($V_D$) modeling.
  - Inability to model mobile phase pH or analyte ionization equilibria.
  - Heuristic nature of discrete fault offsets.
- **Educational Evaluation Limitations:**
  - Single-group pilot design without concurrent randomized control group.
  - Short-term evaluation; long-term skill retention unmeasured.
  - Transfer to physical instrument troubleshooting remains to be formally verified.

### 11. FUTURE WORK
- Integration of a physical void volume calculator ($V_0 = \pi r^2 L \epsilon_t$).
- Implementation of pH-dependent Henderson-Hasselbalch ionization equilibria.
- Multi-institutional randomized controlled trial comparing SimuPharm to static paper manuals.

### 12. CONCLUSION
- Summary of contribution: An accessible, highly engaging, zero-install educational tool that fills a critical gap in pharmaceutical chromatography education by demystifying instrument troubleshooting.

### 13. ASSOCIATED CONTENT (SUPPORTING INFORMATION)
- S1: Complete Pre-Test and Post-Test Instruments with Answer Keys and Rubrics.
- S2: Standardized Instructor Facilitation Protocol.
- S3: Full System Usability Scale (SUS) and Qualitative Survey Instruments.
- S4: Anonymized Participant Dataset CSV.
- S5: Python Statistical Analysis Pipeline Scripts.
