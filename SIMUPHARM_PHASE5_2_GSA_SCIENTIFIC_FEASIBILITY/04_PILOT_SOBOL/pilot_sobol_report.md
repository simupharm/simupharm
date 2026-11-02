# PILOT SOBOL EXPERIMENTAL REPORT & SEED STABILITY
## EMPIRICAL EVALUATION ACROSS RANDOM SEEDS & PARAMETERS

### 1. EXPERIMENTAL DESIGN & SETUP
The pilot global sensitivity analysis was executed using Saltelli's extension of the Sobol variance decomposition algorithm via the `SALib` library (Saltelli et al., 2002, 2010).
- **Model Target:** SimuPharm `simulate_hplc` frozen physics engine.
- **Model System:** Separation of Paracetamol ($k'_{\text{ref}} = 1.8$) and Caffeine ($k'_{\text{ref}} = 3.2$).
- **Primary Response:** Critical pair resolution $R_{s,\min}$.
- **Base Sample Size:** $N = 1024$ ($N(2k + 2) = 14,336$ model evaluations per seed).
- **Tested Sampling Seeds:** 4 independent random seeds ($42, 123, 456, 789$).

---

### 2. SEED STABILITY & UNCERTAINTY QUANTIFICATION
To evaluate numerical stability and rule out random sampling artifacts, all Sobol indices were calculated independently across the four random seeds:

| Parameter | $S_1$ Mean $\pm$ Std | $S_1$ CV (%) | $S_T$ Mean $\pm$ Std | $S_T$ CV (%) | $(S_T - S_1)$ Mean $\pm$ Std | Ranking Stability |
|---|---|---|---|---|---|---|
| **$L$ (Column Length)** | $0.5065 \pm 0.0034$ | $0.67\%$ | $0.5268 \pm 0.0028$ | $0.53\%$ | $0.0203 \pm 0.0012$ | 100% Stable (Rank 1) |
| **$F$ (Flow Rate)** | $0.3879 \pm 0.0041$ | $1.06\%$ | $0.4063 \pm 0.0031$ | $0.76\%$ | $0.0184 \pm 0.0014$ | 100% Stable (Rank 2) |
| **$\%B$ (Organic Modifier)** | $0.0821 \pm 0.0029$ | $3.53\%$ | $0.0884 \pm 0.0015$ | $1.70\%$ | $0.0063 \pm 0.0016$ | 100% Stable (Rank 3) |
| **$d_p$ (Particle Size)** | $0.00003 \pm 0.00008$ | N/A (Near 0) | $0.00009 \pm 0.00001$ | $11.1\%$ | $0.00006 \pm 0.00008$ | 100% Stable (Rank 4) |
| **$T$ (Temperature)** | $0.00000 \pm 0.00000$ | $0.00\%$ | $0.00000 \pm 0.00000$ | $0.00\%$ | $0.00000 \pm 0.00000$ | 100% Inactive (Rank 5-6) |
| **$d_c$ (Internal Diameter)** | $0.00000 \pm 0.00000$ | $0.00\%$ | $0.00000 \pm 0.00000$ | $0.00\%$ | $0.00000 \pm 0.00000$ | 100% Inactive (Rank 5-6) |

---

### 3. AUDIT FINDINGS
1. **Numerical Stability:**
   - Sobol indices exhibit exceptional numerical stability across seeds at $N=1024$. Coefficient of variation (CV) is $< 1.1\%$ for the dominant parameters ($L$ and $F$) and $< 3.6\%$ for organic fraction $\%B$.
   - Parameter rankings are 100% invariant across seeds ($L > F > \%B > d_p > T = d_c = 0$).
   - Kill Condition 2 (Numerical Instability) is **NOT triggered**. The algorithm converges cleanly and reliably.
2. **Dominance of First-Order Main Effects:**
   - Sum of first-order indices $\sum S_1 = 0.9765 \pm 0.005$. Main effects alone account for **$97.65\%$** of total resolution variance.
   - Total model interaction sum $\sum(S_T - S_1) = 0.0450 \pm 0.002$ ($4.5\%$).
   - Interaction variance is strictly below the pre-registered $5.0\%$ threshold.
