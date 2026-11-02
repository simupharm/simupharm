# Publication-Value Addition Audit & Multi-Criteria Assessment
**Document ID:** P4.2-ADDITION-AUDIT-2026-REV2.2  
**Target:** Evaluation of Potential Enhancements against Scientific, Educational, and Feasibility Criteria  

---

## 1. Decision Criteria (Scale 1 to 5)
- **Scientific Value (SV):** Rigor, defensibility, and depth of the empirical insight.
- **Educational Value (EV):** Practical relevance to chemical/pharmaceutical pedagogical instruction.
- **Publication Value (PV):** Impact on referee acceptance at *Journal of Chemical Education* (JCE).
- **Participant Burden (PB):** Added time, cognitive strain, or complexity imposed on students ($1 = \text{Minimal}, 5 = \text{Excessive}$).
- **Implementation Complexity (IC):** Software, logistical, or scoring overhead ($1 = \text{Simple}, 5 = \text{Prohibitive}$).
- **Risk of Bias (RB):** Likelihood of introducing observer, demand, or attrition bias ($1 = \text{Negligible}, 5 = \text{Severe}$).

---

## 2. Multi-Criteria Evaluation Matrix

| Candidate Addition | SV | EV | PV | PB | IC | RB | Decision | Methodological Justification |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **C1. Interaction / Event Logging** | 3 | 3 | 3 | 1 | 4 | 2 | **DEFER** | Requires telemetry server or client-side storage modifications to frozen engine. Unnecessary complexity for $N \approx 25$. |
| **C2. Diagnostic Efficiency Metric** | 3 | 3 | 3 | 1 | 2 | 2 | **OPTIONAL** | Ratio of score/time is easily calculated post-hoc from existing columns; reported as exploratory secondary metric. |
| **C3. Confidence Calibration Analysis** | 4 | 5 | 4 | 1 | 1 | 1 | **IMPLEMENT** | Explores association between subjective confidence and diagnostic accuracy; zero added burden. High JCE relevance. |
| **C4. Expert Content Validation (SME)** | 5 | 5 | 5 | 1 | 2 | 1 | **IMPLEMENT** | 3–5 independent faculty reviews assess curricular relevance and symptom plausibility without student burden. |
| **C5. Item-Level Psychometrics** | 4 | 4 | 4 | 1 | 1 | 1 | **IMPLEMENT** | Computes exploratory Item Difficulty ($P$) and Item Discrimination ($D$) using existing test items ($N \approx 25$ caveat). |
| **C6. Delayed Retention Test (2 Weeks)** | 5 | 4 | 5 | 4 | 4 | 4 | **OPTIONAL HIGH-VALUE** | High scientific value, but high attrition risk (>30%) and scheduling hurdles. Recommended for post-pilot RCT. |
| **C7. Concurrent Control Group (RCT)** | 5 | 4 | 5 | 3 | 5 | 3 | **DEFER (FUTURE)** | Converting to 2-arm trial requires doubling sample size ($N \ge 50$) and IRB amendment. Deferred to Phase 5 definitive RCT. |
| **C8. Qualitative Thematic Framework** | 4 | 5 | 4 | 1 | 2 | 1 | **IMPLEMENT** | Structures student comments into a formal 3-theme qualitative codebook (Misconceptions, Visual Cues, Cognitive Load). |
| **C9. Open Science Reproducibility Pkg** | 5 | 4 | 5 | 1 | 1 | 1 | **IMPLEMENT** | SHA-256 code hashes, preregistration template, and Zenodo/OSF repository metadata supporting transparency and reproducibility. |

---

## 3. Publication Contribution Test for Implemented Additions
- **C3 (Confidence Calibration Indicator):** *New Scientifically Interpretable Result:* Explores the empirical association between subjective diagnostic confidence and objective diagnostic performance, serving as an exploratory indicator of confidence–performance calibration without causal claims.
- **C4 (Expert Content Validity Assessment):** *New Scientifically Interpretable Result:* Measures expert consensus on curricular relevance and symptom plausibility across independent faculty reviewers (evaluated descriptively via I-CVI and S-CVI/Ave benchmarks, noting that small panel size imposes descriptive rather than universal mandatory thresholds; does not validate physical sensor dynamics).
- **C5 (Exploratory Item Analysis):** *New Scientifically Interpretable Result:* Identifies specific chromatographic concepts where students exhibit persistent post-instruction misconceptions within this pilot cohort (subject to $N \approx 25$ precision caveats).
- **C8 (Qualitative Thematic Framework):** *New Scientifically Interpretable Result:* Uncovers specific visual affordances (such as pressure ripple visualization) that facilitate conceptual schema shifts during active troubleshooting.
- **C9 (Open Science Package):** *New Scientifically Interpretable Result:* Open-science practices are structured to support transparency, reproducibility, and responsible data/code sharing through reproducible pipelines and cryptographically verified simulation hashes.
