# SOBOL CONVERGENCE & SAMPLE SIZE EFFICIENCY ANALYSIS
## TRAJECTORY OF SENSITIVITY INDICES ACROSS N = 256, 512, 1024, 2048

### 1. CONVERGENCE TRAJECTORY & CONFIDENCE INTERVAL EVOLUTION
Sobol first-order ($S_1$) and total-order ($S_T$) indices were computed across a progressive sequence of base sample sizes $N \in [256, 512, 1024, 2048]$, corresponding to total model evaluation counts of $3,584$, $7,168$, $14,336$, and $28,672$ runs.

| Base $N$ | Total Evals | Exec Time (s) | $S_T(L) \pm \text{CI}_{95}$ | $S_T(F) \pm \text{CI}_{95}$ | $S_T(\%B) \pm \text{CI}_{95}$ | $S_T(d_p) \pm \text{CI}_{95}$ | $S_T(T)$ |
|---|---|---|---|---|---|---|---|
| **$256$** | $3,584$ | $4.68$ | $0.5222 \pm 0.0838$ | $0.4039 \pm 0.0684$ | $0.0881 \pm 0.0179$ | $0.00010 \pm 0.00003$ | $0.0000$ |
| **$512$** | $7,168$ | $7.38$ | $0.5242 \pm 0.0637$ | $0.4058 \pm 0.0482$ | $0.0880 \pm 0.0136$ | $0.00009 \pm 0.00002$ | $0.0000$ |
| **$1024$** | $14,336$ | $13.42$ | $0.5264 \pm 0.0436$ | $0.4062 \pm 0.0371$ | $0.0884 \pm 0.0092$ | $0.00009 \pm 0.00001$ | $0.0000$ |
| **$2048$** | $28,672$ | $28.82$ | $0.5267 \pm 0.0312$ | $0.4068 \pm 0.0254$ | $0.0886 \pm 0.0073$ | $0.00009 \pm 0.00001$ | $0.0000$ |

---

### 2. CONVERGENCE CRITERION & CONFIDENCE INTERVAL WIDTHS
- **Point Estimate Convergence:** Between $N = 1024$ and $N = 2048$, point estimates changed by less than $0.0003$ for $S_T(L)$ ($0.5264 \to 0.5267$, a relative shift of $0.06\%$) and by less than $0.0006$ for $S_T(F)$ ($0.4062 \to 0.4068$, a relative shift of $0.15\%$).
- **Confidence Interval Narrowing:** The 95% bootstrap confidence interval width for $S_T(L)$ decreased monotonically from $\pm 0.0838$ at $N = 256$ to $\pm 0.0312$ at $N = 2048$ ($O(1/\sqrt{N})$ scaling).
- **Minimum Sample Requirement:** Base sample size $N = 1024$ ($14,336$ evaluations) is fully sufficient to achieve stable, reviewer-resistant Sobol indices with confidence intervals under $\pm 0.045$.
- **Convergence Verdict:** The Sobol variance decomposition converges rapidly and economically. Falsification is NOT due to numerical non-convergence.
