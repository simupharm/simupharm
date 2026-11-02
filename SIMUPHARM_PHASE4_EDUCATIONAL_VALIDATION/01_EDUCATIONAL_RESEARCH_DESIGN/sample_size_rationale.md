# SAMPLE SIZE RATIONALE & POWER ANALYSIS
**Document ID:** P4-SAMPLE-2026-REV1  
**Focus:** Statistical Power, Feasibility, and Realistic Pilot Scope  

---

## 1. THREE-TIER SAMPLE SIZE TARGETS

| Sample Size Tier | Participant Target ($N$) | Methodological Scope & Justification | What This Sample Size CAN Establish | What This Sample Size CANNOT Establish |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Minimum Feasible Pilot** | $N = 15$ | Smallest cohort capable of detecting large paired gains ($d \ge 0.80$) and providing stable SUS estimates. | Software usability; interface barriers; feasibility of diagnostic tasks; large educational effects. | Population-level generalizability; subgroup differences; detection of subtle pedagogical gains. |
| **Tier 2: Preferred Target (Present Study)** | $\mathbf{N = 2 0 - 30}$ | Standard cohort size for a single university laboratory section. Adequate power for moderate-to-large effects. | Statistically defensible paired pre/post gains; stable SUS score within $\pm 3.5$ points; fault difficulty hierarchy. | Definitive causal superiority over competing instructional methods; longitudinal retention. |
| **Tier 3: Ideal Powered Trial (Future)** | $N = 64 - 84$ | Two-group controlled trial with $1:1$ allocation (Intervention vs Control) powered at $1 - eta = 0.80$, $lpha = 0.05$. | Definite causal efficacy; superiority over static textbook troubleshooting guides; interaction effects. | Long-term industry workplace transfer (requires professional longitudinal tracking). |

---

## 2. STATISTICAL POWER CALCULATIONS (G*POWER / SCIPY FORMULATION)

### Scenario A: Paired Pre/Post Difference (Within-Subjects, Single Group)
For a two-tailed paired $t$-test with significance criterion $lpha = 0.05$:
- **Assumed Effect Size:** Cohen's $d_z = 0.65$ (moderate-to-large educational effect, typical of interactive software interventions in chemical education).
- **Target Power:** $1 - eta = 0.85$ (85% probability of rejecting the null hypothesis if an effect exists).
- **Required Sample Size:**
  $$N = \left(rac{z_{1 - lpha/2} + z_{1 - eta}}{d_z}ight)^2 + rac{z_{1 - lpha/2}^2}{2} = \left(rac{1.96 + 1.036}{0.65}ight)^2 + rac{1.96^2}{2} = 21.24 \implies \mathbf{N = 22}$$

**Conclusion:** A planned sample of **$N = 25$ participants** provides **$89.2\%$ statistical power** to detect a moderate-to-large learning gain ($d_z = 0.65$) at $lpha = 0.05$. If the effect size is large ($d_z = 0.80$), $N = 25$ achieves **$97.5\%$ power**.

### Scenario B: System Usability Scale (SUS) Margin of Error
Based on Sauro & Lewis (2016) usability benchmarking:
- Standard deviation of SUS scores in educational software: $\sigma pprox 10.5$ points.
- For $N = 25$, the standard error of the mean is:
  $$	ext{SE} = rac{\sigma}{\sqrt{N}} = rac{10.5}{\sqrt{25}} = 2.10	ext{ points}$$
- The 95% confidence interval half-width is:
  $$	ext{Margin of Error} = t_{0.025, 24} 	imes 	ext{SE} = 2.064 	imes 2.10 = \mathbf{\pm 4.33	ext{ points}}$$

**Conclusion:** An $N = 25$ sample estimates the mean SUS score with a margin of error of $\pm 4.3$ points, which is more than sufficient to position SimuPharm definitively against Bangor's usability grade benchmarks (e.g., distinguishing "Acceptable" $> 70$ from "Marginal" $< 60$).
