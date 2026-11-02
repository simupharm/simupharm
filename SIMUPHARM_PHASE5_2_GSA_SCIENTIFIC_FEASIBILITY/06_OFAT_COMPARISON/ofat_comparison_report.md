# ONE-FACTOR-AT-A-TIME (OFAT) BASELINE COMPARISON
## BENCHMARKING GLOBAL SENSITIVITY ANALYSIS AGAINST LOCAL SWEEPS

### 1. EXPERIMENTAL BASELINE SETUP
To establish a rigorous baseline, conventional one-factor-at-a-time (OFAT) sensitivity sweeps were executed across identical parameter bounds.
- **Center Point (Nominal Conditions):** $L = 15.0$ cm, $F = 1.0$ mL/min, $d_p = 3.5$ $\mu$m, $\%B = 50.0\%$, $T = 25.0$ °C, $d_c = 4.6$ mm.
- **Baseline Resolution:** $R_{s,\text{base}} = 1.505$.
- **Sweep Density:** 21 equally spaced points per factor spanning 100% of its range while holding the remaining 5 factors at nominal baseline values (126 total model runs).

---

### 2. QUANTITATIVE OFAT METRICS VS. SOBOL INDICES

| Parameter | Baseline Value | Range [Low, High] | $\Delta R_s = \max - \min$ | OFAT Normalized Importance | OFAT Rank | Sobol $S_1$ Rank | Sobol $S_T$ Rank | Spearman Correlation ($\rho$) |
|---|---|---|---|---|---|---|---|---|
| **$L$ (Column Length)** | $15.0$ cm | $[5.0, 25.0]$ | $1.074$ | $41.84\%$ | **1** | **1** | **1** | **1.000** |
| **$F$ (Flow Rate)** | $1.0$ mL/min | $[0.5, 2.0]$ | $1.046$ | $40.75\%$ | **2** | **2** | **2** | **1.000** |
| **$\%B$ (Organic Modifier)** | $50.0\%$ | $[30.0, 80.0]$ | $0.438$ | $17.06\%$ | **3** | **3** | **3** | **1.000** |
| **$d_p$ (Particle Size)** | $3.5$ $\mu$m | $[1.8, 5.0]$ | $0.009$ | $0.35\%$ | **4** | **4** | **4** | **1.000** |
| **$T$ (Temperature)** | $25.0$ °C | $[20.0, 60.0]$ | $0.000$ | $0.00\%$ | **5** (tie) | **5** (tie) | **5** (tie) | **1.000** |
| **$d_c$ (Internal Diameter)** | $4.6$ mm | $[2.1, 4.6]$ | $0.000$ | $0.00\%$ | **5** (tie) | **5** (tie) | **5** (tie) | **1.000** |

---

### 3. AUDIT EVALUATION & INFORMATION GAIN TEST
1. **Identical Parameter Rankings:**
   - Spearman rank-order correlation between OFAT and Global Sobol sensitivity is **$\rho = 1.000$** (perfect concordance).
   - Both methods identify Column Length as the primary sensitivity driver, Flow Rate as second, Organic Modifier as third, Particle Size as negligible, and Temperature / Column ID as zero.
2. **Computational Cost Comparison:**
   - OFAT required **$126$ model evaluations** to elucidate the exact parameter ranking and diagnose parameter inactivity.
   - Sobol GSA required **$14,336$ model evaluations** ($114\times$ greater computational cost) to arrive at the identical qualitative ranking.
3. **Information Gain Deficit:**
   - In systems with strong non-linear interactions, GSA justifies its high computational cost by revealing rank inversions, masking effects, and cross-coupling that OFAT is mathematically blind to.
   - In SimuPharm, because total interaction variance is only $4.47\%$ in wide space and $0.16\%$ in narrow space, **OFAT misses almost nothing**.
   - **Kill Condition 5 (No Meaningful Added Value Over OFAT) is triggered.** GSA does not change any practical chromatographic conclusion relative to a simple 10-minute OFAT screen.
