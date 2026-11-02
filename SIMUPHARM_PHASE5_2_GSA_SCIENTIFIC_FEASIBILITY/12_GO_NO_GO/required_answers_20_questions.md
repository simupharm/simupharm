# REQUIRED FINAL ANSWERS: 20 CORE SCIENTIFIC QUESTIONS
## EXPLICIT, UNAMBIGUOUS VERDICTS FROM THE PHASE 5.2 SPRINT

### 1. DOES SIMUPHARM SHOW NON-TRIVIAL GLOBAL PARAMETER INTERACTIONS?
**NO.** Total interaction variance across all parameters is only **$4.47\%$** in the wide design space ($\sum(S_T - S_1) = 0.0447 < 0.05$) and collapses to **$0.16\%$** in the narrow operational space. The model is **$97.75\%$ additive** in wide screening and **$99.84\%$ additive** under routine method robustness testing. All interactions fall strictly below the pre-registered significance threshold.

---

### 2. WHICH PARAMETERS MATTER MOST?
1. **Column Length ($L$):** $S_1 = 0.5063$, $S_T = 0.5264$ (Rank 1, accounts for $50.6\%$ of variance).
2. **Flow Rate ($F$):** $S_1 = 0.3878$, $S_T = 0.4062$ (Rank 2, accounts for $38.8\%$ of variance).
3. **Organic Modifier Fraction ($\%B$):** $S_1 = 0.0819$, $S_T = 0.0884$ (Rank 3, accounts for $8.2\%$ of variance).
4. **Particle Size ($d_p$):** $S_1 \approx 0.00001$, $S_T = 0.00009$ (Rank 4, negligible).
5. **Temperature ($T$) & Internal Diameter ($d_c$):** $S_1 = 0.00000$, $S_T = 0.00000$ (Rank 5-6, completely inactive in code).

---

### 3. WHICH INTERACTIONS MATTER MOST?
The only detectable pairwise interaction is **$L \times F$** ($S_2 = 0.0167 \pm 0.0865$), but its 95% confidence interval spans zero, making it statistically indistinguishable from Monte Carlo sampling noise. All other pairs account for $< 0.35\%$ of variance. The hypothesized $T \times \%B$ interaction is **identically 0.0000**.

---

### 4. ARE THEY STABLE?
**YES.** Numerical stability across random seeds ($42, 123, 456, 789$) is exceptional ($CV < 1.1\%$ for primary factors). Numerical estimates converge within $0.15\%$ between $N=1024$ and $N=2048$.

---

### 5. DO THEY SURVIVE DIFFERENT PARAMETER RANGES?
**QUALITATIVELY YES, QUANTITATIVELY NO.** The ranking order ($L > F > \%B$) survives, but in the narrow operational space ($\pm 10\%$), Column Length sensitivity surges to $77.9\%$ while total interaction variance completely vanishes ($0.16\%$).

---

### 6. DO THEY SURVIVE DIFFERENT SAMPLING CONDITIONS?
**YES.** Results are identical across independent Sobol sequences and sample sizes from $N=512$ to $N=2048$.

---

### 7. ARE THEY PHYSICALLY PLAUSIBLE?
**NO.** The high sensitivity of Flow Rate ($S_1 = 0.388$) is driven by an inverted Van Deemter curve where $R_s$ increases monotonically with flow rate up to $2.0$ mL/min. Furthermore, $33.98\%$ of the wide parameter space generates physical backpressures exceeding the $400$ bar limit of standard HPLC instruments (up to $4,668$ bar).

---

### 8. ARE THEY DOMINATED BY MODEL ARTIFACTS?
**YES.** The entire sensitivity ranking is driven by two implementation artifacts:
1. An uncalibrated Van Deemter equation ($B = 0.05$, $C = 2.5 \times 10^{-9}$, $u_{\text{opt}} = 4,472$ mL/min) that forces the simulator onto the steep $B/u$ branch.
2. A linear retention modifier heuristic $(100 - \%B)/40$ that artificially dampens organic solvent sensitivity relative to real exponential/logarithmic retention thermodynamics.

---

### 9. DOES GSA ADD INFORMATION BEYOND OFAT?
**NO.** A simple 126-run OFAT sweep produced the **exact same parameter ranking** ($\rho = 1.000$) and identified the exact same active parameters as the 14,336-run Sobol analysis.

---

### 10. DOES GSA ADD INFORMATION BEYOND CONVENTIONAL DOE/RSM?
**NO.** A standard second-order polynomial response surface (RSM) fitted on just 200 points achieved an independent test set $R^2$ of **0.9966** (99.66% variance explained, $\text{RMSE} = 0.0265$). Conventional DoE captures virtually all response behavior.

---

### 11. CAN NIST SRM 870 ACTUALLY VALIDATE ANY PART OF THE CLAIM?
**NO.** NIST SRM 870 is evaluated under a single fixed condition (1.0 mL/min, 80:20 MeOH, 23 °C, 250 mm). A dataset with zero variance in operational factors cannot validate multidimensional sensitivity surfaces.

---

### 12. CAN TANAKA DATA ACTUALLY VALIDATE ANY PART OF THE CLAIM?
**NO.** The Tanaka database characterizes stationary phase chemistry (ligand density, silanol activity) under fixed mobile phase conditions. It provides no operational parameter sweeps.

---

### 13. IS THERE A CREDIBLE INDEPENDENT VALIDATION STRATEGY?
**NO (WITHOUT PHYSICAL WET-LAB WORK).** Without running a dedicated multi-factorial wet-lab HPLC experiment or acquiring an external experimental chromatographic DoE dataset, SimuPharm's synthetic sensitivity analysis cannot be validated.

---

### 14. WHAT IS THE ACTUAL NOVELTY?
**NEGLIGIBLE.** The study reduces to applying an existing open-source Python package (`SALib`) to an existing educational simulator (`backend/science/hplc.py`).

---

### 15. WHAT WOULD A HOSTILE REVIEWER ATTACK?
Reviewers at *JCA* or *ACA* would attack: (1) the inverted Van Deemter curve, (2) the absence of temperature dependence, (3) the lack of empirical validation, (4) the sampling of unphysical 4,000-bar conditions, and (5) the fact that a 2nd-order DoE already explains $99.7\%$ of the variance.

---

### 16. IS THE PAPER SCIENTIFICALLY PUBLISHABLE?
**NO.** In its current formulation as an analytical chemistry contribution, it has a $> 95\%$ rejection probability in peer review.

---

### 17. WHAT IS THE MINIMUM ADDITIONAL WORK?
To make Direction B publishable in a chemistry journal, one would have to completely rewrite the engine physics (non-linear LSS retention, realistic Van Deemter $C$-term, hydraulic pressure coupling) and execute an empirical multi-factorial wet-lab study on a physical instrument.

---

### 18. DO WE NEED STUDENTS?
**NO.** This is a pure computational / physical chemistry problem. Student recruitment is irrelevant.

---

### 19. DO WE NEED A PHYSICAL LAB?
**YES (FOR DIRECTION B TO SUCCEED AS A CHEMISTRY PAPER).** Without physical chromatographic data, Direction B cannot be defended.

---

### 20. SHOULD WE CONTINUE?
**ABSOLUTELY NOT.** Direction B must be **KILLED IMMEDIATELY**. We must pivot to **Direction G (SoftwareX Scientific Software Paper)** as primary, with **Direction C (Multimodal QC Identification)** as secondary.
