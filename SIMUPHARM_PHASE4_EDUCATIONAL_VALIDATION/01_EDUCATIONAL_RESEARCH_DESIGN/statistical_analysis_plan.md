# STATISTICAL ANALYSIS PLAN (SAP)
**Document ID:** P4-SAP-2026-REV1  
**Status:** PRE-SPECIFIED (Registered Prior to Participant Data Collection)  
**Lead Analyst:** Phase 4 Educational Evaluation Team  

---

## 1. PRIMARY STATISTICAL OUTCOME & HYPOTHESIS

### Primary Outcome
Change in troubleshooting assessment score:
$$\Delta 	ext{Score}_i = 	ext{PostTest}_i - 	ext{PreTest}_i \quad (i = 1, \dots, N)$$
where both tests are scored on a scale from 0 to 10 points.

### Primary Statistical Hypothesis
- **Null Hypothesis ($H_0$):** Mean troubleshooting score does not change following the intervention ($\mu_{\Delta} = 0$).
- **Alternative Hypothesis ($H_1$):** Mean troubleshooting score increases following the intervention ($\mu_{\Delta} > 0$).
- **Significance Criterion:** Two-tailed $lpha = 0.05$ (conservative; two-tailed test used to detect potential negative effects).

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
$$	ext{Cohen's } d_z = rac{ar{x}_{\Delta}}{s_{\Delta}} = rac{rac{1}{N}\sum_{i=1}^N \Delta_i}{\sqrt{rac{1}{N-1}\sum_{i=1}^N (\Delta_i - ar{x}_{\Delta})^2}}$$
- 95% Confidence Interval for $d_z$ computed via non-central $t$-distribution.
- Benchmarks: Small ($d_z \ge 0.20$), Moderate ($d_z \ge 0.50$), Large ($d_z \ge 0.80$).

### For Non-Parametric Wilcoxon Signed-Rank Test:
$$	ext{Rank-Biserial Correlation } r = rac{W_+ - W_-}{W_+ + W_-}$$
- Benchmarks: Small ($r \ge 0.10$), Moderate ($r \ge 0.30$), Large ($r \ge 0.50$).

---

## 4. SECONDARY STATISTICAL ANALYSES

### 1. Hake's Average Normalized Gain ($\langle g angle$)
$$\langle g angle = rac{\%	ext{Post} - \%	ext{Pre}}{100\% - \%	ext{Pre}} = rac{ar{x}_{	ext{post}} - ar{x}_{	ext{pre}}}{10 - ar{x}_{	ext{pre}}}$$
- Reported as an exploratory educational metric.
- Hake benchmarks: Low gain ($\langle g angle < 0.30$), Medium gain ($0.30 \le \langle g angle < 0.70$), High gain ($\langle g angle \ge 0.70$).
- *Limitation disclosure:* Not treated as definitive proof of learning; reported alongside raw paired differences.

### 2. System Usability Scale (SUS)
- Raw item responses ($1–5$ Likert) converted using Brooke's algorithm:
  - Odd items (1, 3, 5, 7, 9): Contribution $= 	ext{Score} - 1$.
  - Even items (2, 4, 6, 8, 10): Contribution $= 5 - 	ext{Score}$.
  - Total SUS $= 2.5 	imes \sum (	ext{Contributions}) \in [0, 100]$.
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
