# Corrected Statistical Analysis Plan (SAP)
**Version:** REV2.3 / PHASE4.2.3 (ABSOLUTE PROTOCOL FREEZE)  
**Date:** October 4, 2026  

---

## 1. Outcome Hierarchy & Prespecified Primary Inferential Analysis
To eliminate outcome switching and multiplicity inflation, this SAP establishes a definitive inferential hierarchy:

### Primary Outcome (Prespecified Inferential)
- **Endpoint:** Paired Troubleshooting Score Gain ($\Delta\text{Score} = \text{PostTest} - \text{PreTest}$, discrete integer range: $-10$ to $+10$).
- **Primary Inferential Test:** **Wilcoxon Signed-Rank Test** (Two-Tailed, $\alpha = 0.05$).
  - *Zero-Difference Handling:* Mandated **Pratt's method** (`zero_method='pratt'`), which includes participants with zero gain ($\Delta = 0$) in the ranking procedure, preserving the true sample size ($N$).
  - *All-Zero Safeguard:* If all differences are zero, the test yields $W = 0$, $p = 1.0$, $r_{rb} = 0.0$, and Hodges-Lehmann difference $= 0.0$.
  - *Non-Parametric Effect Size:* Signed rank-biserial correlation $r_{rb} = \frac{W^+ - W^-}{W^+ + W^-}$, where $W^+$ is the rank sum of positive gains and $W^-$ is the rank sum of negative gains (positive indicates improvement; negative indicates deterioration; zero indicates no effect).
  - *Median Difference & CI:* Hodges-Lehmann median difference with 95% Walsh order-statistic confidence interval using the prespecified critical-index normal approximation (Bauer 1972; Hollander & Wolfe 1999). Not characterized as an "exact" interval.
- **Sensitivity Analysis:** Paired $t$-test ($t$, $p$-value, Cohen's $d_z$, 95% CI). Both primary and sensitivity results will be reported side-by-side in the manuscript.
- **Rule on Normality Testing:** Shapiro-Wilk testing will be reported descriptively for distributional reporting, but **will NOT be used to condition test selection**.

---

## 2. Secondary Educational & Usability Outcomes (Descriptive Benchmarking)
No artificial one-sample inferential hypothesis tests are imposed on secondary metrics:
1. **System Usability Scale (SUS):** Mean, SD, median, and IQR computed via canonical Brooke (1996) formula. Evaluated contextually against the widely cited 68.0 benchmark (Bangor et al., 2008). Not presented as proof of educational effectiveness, a control group, or educational superiority.
2. **Practical Troubleshooting Mastery:** Grand total score across 4 unknown scenarios on the 24-point analytical rubric (median, IQR, percentage of maximum). No arbitrary "6/24 random guessing threshold" is assumed. Inter-rater reliability is reported via Weighted Cohen's Kappa ($\kappa_w$) for ordinal 0–2 component items and Intraclass Correlation Coefficient $\text{ICC}(2,1)$ for the continuous 0–24 grand total.

---

## 3. Exploratory & Descriptive Secondary Outcomes (No Multiplicity Adjustment)
3. **Diagnostic Latency:** Median Time-to-Diagnosis in seconds with Interquartile Range (IQR).
4. **Exploratory Confidence–Performance Association:** Spearman rank correlation ($\rho$) and Pearson ($r$) between post-task confidence ratings (1–5) and rubric diagnostic scores as an exploratory indicator of calibration (zero causal claims).
5. **Hake Normalized Gain:** Cohort average normalized gain $\langle g \rangle = (\bar{x}_{\text{post}} - \bar{x}_{\text{pre}}) / (10 - \bar{x}_{\text{pre}})$. Explicitly reported descriptively and not used as evidence of causal educational effectiveness. No individual student categorization is performed.
6. **Exploratory Psychometrics:** Item difficulty index ($P$) and item discrimination ($D$). Internal-consistency estimates (e.g., Cronbach's alpha) are exploratory and unstable at the pilot sample size ($N \approx 25$); they are not used to establish psychometric validity, and tests are not claimed as validated based on alpha.

---

## 4. Pre-Specified Missing Data Rules
1. **Pre-Test / Post-Test Missingness:** Complete-case analysis is mandated. If a participant leaves $\ge 1$ question blank on a 10-item test, their total score is coded as missing (`NaN`) and excluded from paired $\Delta\text{Score}$ analysis.
2. **SUS Questionnaire Missingness:** Follows standard Sauro & Lewis (2016) psychometric guidelines:
   - If 1 or 2 items are missing, substitute the neutral response value (3).
   - If $\ge 3$ items are missing, the entire SUS submission is invalid and excluded from SUS analysis.
3. **Practical Task Missingness:** If a participant skips an unknown scenario, their score for that scenario is coded as 0; their latency for that scenario is excluded from median latency calculations.
4. **Study Withdrawal:** Any participant withdrawing prior to post-test completion is excluded from paired inferential analyses and reported in the participant flow diagram.
