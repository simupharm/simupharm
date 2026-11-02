# GLOBAL INTERACTION ANALYSIS & RSM BENCHMARKING
## SOBOL TOTAL-ORDER EFFECTS, PAIRWISE INTERACTIONS & 2ND-ORDER DOE

### 1. SOBOL INTERACTION DECOMPOSITION ($S_T - S_1$)
In variance-based global sensitivity analysis, the difference between the total-order index and first-order index ($S_{Ti} - S_i$) quantifies all interactions involving parameter $X_i$ with all other input factors.

| Parameter ($X_i$) | First-Order ($S_1$) | Total-Order ($S_T$) | Interaction ($S_T - S_1$) | Pre-Registered Classification |
|---|---|---|---|---|
| **$L$ (Column Length)** | $0.5063 \pm 0.0544$ | $0.5264 \pm 0.0436$ | **$0.0200$** | **Weak Interaction** |
| **$F$ (Flow Rate)** | $0.3878 \pm 0.0507$ | $0.4062 \pm 0.0371$ | **$0.0183$** | **Trivial Interaction** |
| **$\%B$ (Organic Modifier)** | $0.0819 \pm 0.0247$ | $0.0884 \pm 0.0092$ | **$0.0066$** | **Trivial Interaction** |
| **$d_p$ (Particle Size)** | $0.00001 \pm 0.00083$ | $0.00009 \pm 0.00001$ | **$0.00008$** | **Trivial Interaction** |
| **$T$ (Temperature)** | $0.00000 \pm 0.00000$ | $0.00000 \pm 0.00000$ | **$0.00000$** | **Zero Interaction** |
| **$d_c$ (Internal Diameter)** | $0.00000 \pm 0.00000$ | $0.00000 \pm 0.00000$ | **$0.00000$** | **Zero Interaction** |
| **Total Model Interactions** | $\sum S_1 = \mathbf{0.9760}$ | — | $\sum(S_T - S_1) = \mathbf{0.0447}$ | **Overall Trivial / Near-Additive** |

---

### 2. PAIRWISE SECOND-ORDER SOBOL INDICES ($S_{ij}$)
Second-order Sobol indices $S_{ij}$ were calculated from the $N=1024$ Saltelli evaluation matrix:

| Factor Pair | Second-Order Index ($S_2$) | 95% Confidence Interval | Reviewer Interpretation |
|---|---|---|---|
| **$L \times F$** | $0.0167$ | $\pm 0.0865$ | Detectable point estimate ($1.67\%$), but CI spans zero; statistically indistinguishable from MC noise |
| **$L \times \%B$** | $0.0037$ | $\pm 0.0748$ | Negligible ($0.37\%$), CI spans zero |
| **$F \times \%B$** | $0.0033$ | $\pm 0.0721$ | Negligible ($0.33\%$), CI spans zero |
| **$T \times \%B$** | **$0.0000$** | $\pm 0.0341$ | **ZERO (Hypothesis of $0.28$ interaction conclusively disproved)** |
| **All Other Pairs** | $< 0.0010$ | $\pm 0.07$ | Pure numerical Monte Carlo background noise |

---

### 3. RESPONSE SURFACE METHODOLOGY (RSM / DOE) COMPARISON
To determine whether an analytical chemist would need 14,000 Sobol runs or could obtain identical guidance from a standard 2nd-order polynomial DoE (Central Composite / Box-Behnken design), a standard quadratic response surface was fitted:
$$\hat{R}_s = \beta_0 + \sum_{i=1}^k \beta_i x_i + \sum_{i=1}^k \beta_{ii} x_i^2 + \sum_{i < j} \beta_{ij} x_i x_j$$

#### Performance Metrics on $N=200$ DoE Training and $N=1000$ Independent Test Set:
- **Linear Model (Main Effects Only):** $R^2 = 0.9718$, $\text{RMSE} = 0.0767$.
- **Quadratic RSM Model (Main + Quadratic + 2-Way Interactions):**
  - Training Set $R^2 = \mathbf{0.9972}$, $\text{RMSE} = 0.0243$.
  - Independent Unseen Test Set $R^2 = \mathbf{0.9966}$ ($99.66\%$ variance explained), $\text{Test RMSE} = \mathbf{0.0265}$.
- **Statistical Assessment:**
  - A standard 2nd-order response surface explains **$99.66\%$ of the total variance** with an average error of only $0.026$ resolution units.
  - Conventional DoE captures both the linear curvature and the small $L \times F$ coupling perfectly.
  - Global Sobol variance decomposition provides zero incremental information beyond standard DoE tools already ubiquitous in chromatographic method development.
  - **Kill Condition 5 (DoE Redundancy) is conclusively satisfied.**
