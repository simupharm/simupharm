# Corrected Manuscript Blueprint & Outline
**Document ID:** P4.2-MS-OUTLINE-2026-REV2.2  
**Target Journal:** *Journal of Chemical Education* (JCE)  
**Article Category:** Chemical Education Research / Technology Report  
**Word Count Target:** 4,000 – 4,500 words (excluding figures and references)  

---

## Section-by-Section Manuscript Structure

### 1. Title & Abstract
- **Title:** *Interactive Browser-Based HPLC Troubleshooting: Educational Evaluation and Usability Assessment in an Undergraduate Laboratory*
- **Structured Abstract:** Context, Pedagogical Innovation, Research Design ($N \approx 25$ exploratory pilot), Pre/Post Gains ($\Delta\text{Score}$), Practical Diagnostic Mastery (24-point rubric), Usability (Canonical Brooke SUS), and Limitations.

### 2. Introduction & Pedagogical Context
- High cost, instrument maintenance downtime, and safety constraints limiting hands-on HPLC troubleshooting in pharmacy and chemistry education.
- Need for accessible, zero-install, browser-based simulation supplements.
- Grounding in Cognitive Load Theory and Guided Discovery Learning.

### 3. Simulator Architecture & Capabilities
- Client-side browser architecture (HTML5 Canvas, JavaScript, Web Audio).
- Deterministic retention modeling (Snyder-Giddings-Dolan C18 framework).
- Heuristic fault injection: Air bubble (pressure ripple), Fitting leak (flow loss), Column void (split doublets), Contamination (ghost peaks).
- **Explicit Declaration of Simulation Limitations:** Qualitative phenomenological representation, not mechanistic CFD or industrial digital twin.

### 4. Educational Research Design & Methodology
- Pre-test / post-test within-subject exploratory pilot evaluation ($N \approx 25$).
- 50-minute standardized laboratory protocol.
- Neutral guided inquiry protocol (zero teaching-to-the-test cueing) and fidelity monitoring.
- Double-blind scoring of practical tasks on a 24-point analytical rubric by two independent raters.

### 5. Assessment Instruments & Psychometric Properties
- 10-item isomorphic pre-test and post-test (balanced A/B/C/D keys, zero position bias).
- Standard unmodified Brooke (1996) System Usability Scale (SUS).
- 4 unknown simulated fault diagnosis scenarios (Fault ID, Physical Reasoning, Corrective Action).

### 6. Statistical Analysis & Outcome Hierarchy
- Prespecified Primary Inferential Analysis: Wilcoxon Signed-Rank Test using Pratt's method for zero differences; Hodges-Lehmann median difference with exact 95% Walsh order-statistic CI and signed rank-biserial correlation ($r_{rb}$).
- Paired $t$-test reported side-by-side as sensitivity analysis.
- Multiplicity control: Holm-Bonferroni step-down across secondary inferential outcomes (SUS benchmark, Rubric threshold).
- Pre-specified complete-case and Sauro missing data rules.

### 7. Results (Preserved Unpopulated Placeholders Until Recruitment)
- Sample Demographics: $N = [N]$ participants ($[N_{\text{Pharm}}]$ B.Pharm, $[N_{\text{Chem}}]$ Chemistry).
- Diagnostic Gain: Pre-test Mean $= [M_{\text{pre}}]$ vs Post-test Mean $= [M_{\text{post}}]$; Mean Gain $= [M_{\text{diff}}]$, Median Gain $= [MD_{\text{diff}}]$, Wilcoxon $W = [W]$, $p = [p]$, Rank-Biserial $r_{rb} = [r_{rb}]$, Hodges-Lehmann Median Difference $= [HL]$ (95% Walsh CI: $[CI]$).
- Practical Diagnostic Mastery: Mean Rubric Total $= [M_{\text{rubric}}] / 24.0$; Inter-Rater Reliability $\kappa_w = [\kappa]$, $\text{ICC}(2,1) = [\text{ICC}]$.
- Diagnostic Latency: Median Time-to-Diagnosis $= [M_{\text{lat}}]\text{ s}$ (IQR: $[IQR]$).
- Confidence Association: Spearman $\rho = [\rho]$, $p = [p]$; Pearson $r = [r]$.
- Usability: Mean SUS $= [M_{\text{SUS}}] \pm [SD]$ (Bangor Grade $[Grade]$).
- Expert Content Validity: Scale $\text{S-CVI/Ave} = [\text{CVI}]$ across $[3\text{--}5]$ reviewers.

### 8. Discussion & Educational Implications
- Interpretation of diagnostic gains and symptom-to-cause mental model development.
- Usability insights: Accessibility across heterogeneous student hardware.
- Exploratory confidence–performance association: Alignment between subjective confidence and objective diagnostic accuracy.

### 9. Study Limitations & Methodological Candidacy
- **Single-Group Design:** Absence of a concurrent control group limits definitive causal claims of superiority over traditional instruction.
- **Short-Term Horizon:** Evaluates immediate learning within a single 50-minute lab period; long-term retention remains unmeasured.
- **Transfer to Physical Hardware:** Diagnostic transfer to physical HPLC instruments is unmeasured and requires future empirical study.
- **Sample Size:** Pilot cohort ($N \approx 25$) precludes definitive subgroup inferential claims.
