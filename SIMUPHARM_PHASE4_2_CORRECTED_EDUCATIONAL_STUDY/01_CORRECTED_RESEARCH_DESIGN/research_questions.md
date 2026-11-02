# Corrected Educational Research Questions & Hypotheses
**Version:** REV2.3 / PHASE4.2.3 (ABSOLUTE PROTOCOL FREEZE)  
**Date:** October 4, 2026  

---

## 1. Primary Research Question (Prespecified Inferential)
**RQ1:** Does student engagement with the interactive SimuPharm troubleshooting module produce a measurable within-subject improvement in HPLC diagnostic performance from pre-test to post-test in an undergraduate laboratory setting?

- **Null Hypothesis ($H_0$):** There is no difference in student diagnostic scores between the pre-test and post-test ($\text{Median}(\Delta\text{Score}) = 0$).
- **Alternative Hypothesis ($H_1$):** There is a statistically significant change in student diagnostic scores between the pre-test and post-test ($\text{Median}(\Delta\text{Score}) \ne 0$).
- **Prespecified Primary Inferential Test:** Wilcoxon Signed-Rank Test (Two-Tailed, $\alpha = 0.05$, Pratt's zero-difference method). Paired $t$-test pre-specified as sensitivity analysis.
- **Reporting Metrics:** Hodges-Lehmann median difference with 95% Walsh order-statistic confidence interval (using prespecified critical-index approximation) and signed rank-biserial correlation ($r_{rb}$). Standalone inferential analysis ($\alpha = 0.05$).

---

## 2. Secondary Educational & Usability Outcomes (Descriptive Benchmarking)
Secondary outcomes are evaluated as descriptive benchmarks and educational profiles without ungrounded one-sample inferential hypothesis testing:

- **RQ2 (System Usability Contextual Benchmarking):** What is the subjective usability profile of SimuPharm among undergraduate students?
  - *Metric:* Canonical Brooke (1996) System Usability Scale (SUS) composite score (0–100). Reported as mean, SD, median, and IQR, compared contextually against the commonly cited 68.0 benchmark (Bangor et al., 2008). Not presented as proof of educational effectiveness, a control group, or educational superiority.
- **RQ3 (Practical Troubleshooting Competence):** How do students perform on simulated unknown instrument fault diagnosis across the 24-point analytical rubric?
  - *Metric:* Grand diagnostic rubric total (0–24) and component-level scores (Symptom Identification, Physical Reasoning, Corrective Action: 0–2 each). Reported as medians, IQRs, and percentage distributions. No arbitrary "6/24 random guessing threshold" is assumed. Inter-rater reliability evaluated via Weighted Kappa ($\kappa_w$) for ordinal components and $\text{ICC}(2,1)$ for grand total.

---

## 3. Exploratory & Descriptive Research Questions (Hypothesis-Generating)
All exploratory outcomes are reported descriptively without hypothesis testing or multiplicity penalties:

- **RQ4 (Diagnostic Efficiency):** What is the median time required for undergraduate students to complete simulated fault troubleshooting?
  - *Metric:* Median Diagnostic Latency in seconds (IQR) across the 4 practical scenarios.
- **RQ5 (Exploratory Confidence–Performance Association):** What is the association between diagnostic confidence and objective diagnostic accuracy?
  - *Metric:* Spearman rank correlation ($\rho$) and Pearson ($r$) between post-task confidence ratings (1–5) and rubric diagnostic scores as an exploratory indicator of confidence–performance calibration. Zero causal claims of simulator-induced metacognitive calibration are made.
- **RQ6 (Normalized Learning Gain — Descriptive):** What is the cohort-level normalized learning gain achieved by participants?
  - *Metric:* Cohort average normalized gain $\langle g \rangle = (\bar{x}_{\text{post}} - \bar{x}_{\text{pre}}) / (10 - \bar{x}_{\text{pre}})$. Explicitly reported descriptively and not used as evidence of causal educational effectiveness. No individual student categorization is performed.
- **RQ7 (Targeted Pedagogical Usability):** How do students evaluate individual interactive interface features?
  - *Metric:* 8-item targeted UX survey on a 5-point Likert scale (medians, IQRs, Likert frequency profiles).
- **RQ8 (Disciplinary Descriptions):** How do diagnostic score gains and usability ratings present across B.Pharm and B.Sc. Chemistry cohorts? (Descriptive medians/IQRs only; no inferential claims).
- **RQ9 (Prior Instrument Exposure):** How do students with prior hands-on HPLC experience compare descriptively with complete novices? (Descriptive medians/IQRs only).
- **RQ10 (Exploratory Item Analysis & Psychometrics):** Which specific fault concepts present difficulty for learners within this pilot cohort?
  - *Metric:* Item difficulty index ($P$) and item discrimination ($D$). Internal-consistency estimates (e.g., Cronbach's alpha) are exploratory and unstable at the pilot sample size ($N \approx 25$); they are not used to establish psychometric validity, and tests are not claimed as validated based on alpha.
