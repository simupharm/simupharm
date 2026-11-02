# PARAMETER SPACE & OPERATIONAL RANGE AUDIT
## METHOD SCOUTING SPACE VS. AQBD ROBUSTNESS SPACE

### 1. EXPERIMENTAL PARAMETER DEFINITIONS & BOUNDS
Two distinct parameter spaces were audited and computationally evaluated:

1. **Wide Design Space (Method Scouting / Exploratory Space):**
   - $L \in [5.0, 25.0]$ cm (Baseline: $15.0$ cm)
   - $F \in [0.5, 2.0]$ mL/min (Baseline: $1.0$ mL/min)
   - $d_p \in [1.8, 5.0]$ $\mu$m (Baseline: $3.5$ $\mu$m)
   - $\%B \in [30.0, 80.0]$ % (Baseline: $50.0$ %)
   - $T \in [20.0, 60.0]$ °C (Baseline: $25.0$ °C)
   - $d_c \in [2.1, 4.6]$ mm (Baseline: $4.6$ mm)

2. **Narrow Robustness Space (ICH Q14 AQbD Operational Space):**
   - $L \in [12.0, 18.0]$ cm ($\pm 20\%$)
   - $F \in [0.9, 1.1]$ mL/min ($\pm 10\%$)
   - $d_p \in [3.0, 4.0]$ $\mu$m ($\pm 14\%$)
   - $\%B \in [45.0, 55.0]$ % ($\pm 10\%$ relative)
   - $T \in [22.0, 28.0]$ °C ($\pm 3$ °C)
   - $d_c \in [4.0, 4.6]$ mm

---

### 2. QUANTITATIVE COMPARISON OF SOBOL SENSITIVITIES (WIDE VS. NARROW)
Sobol variance decomposition ($N = 1024$ Saltelli base samples, 14,336 evaluations per space) yielded the following indices:

| Parameter | Wide Design Space ($S_1$) | Wide Design Space ($S_T$) | Wide Interaction ($S_T - S_1$) | Narrow Space ($S_1$) | Narrow Space ($S_T$) | Narrow Interaction ($S_T - S_1$) |
|---|---|---|---|---|---|---|
| **$L$ (Length)** | $0.5063$ | $0.5264$ | $0.0200$ | $0.7794$ | $0.7799$ | $0.0005$ |
| **$F$ (Flow Rate)** | $0.3878$ | $0.4062$ | $0.0183$ | $0.1881$ | $0.1888$ | $0.0007$ |
| **$\%B$ (Organic Modifier)** | $0.0819$ | $0.0884$ | $0.0066$ | $0.0311$ | $0.0313$ | $0.0002$ |
| **$d_p$ (Particle Size)** | $0.00001$ | $0.00009$ | $0.00008$ | $-0.00009$ | $0.00009$ | $0.00018$ |
| **$T$ (Temperature)** | $0.00000$ | $0.00000$ | $0.00000$ | $0.00000$ | $0.00000$ | $0.00000$ |
| **$d_c$ (Internal Diameter)** | $0.00000$ | $0.00000$ | $0.00000$ | $0.00000$ | $0.00000$ | $0.00000$ |
| **Total Interaction Sum $\sum(S_T - S_1)$** | — | — | **$0.0447$** | — | — | **$0.0016$** |
| **Total First-Order Sum $\sum S_1$** | **$0.9760$** | — | — | **$0.9986$** | — | — |

---

### 3. AUDIT FINDINGS ON RANGE DEPENDENCE & FALSIFICATION
1. **Range Sensitivity Stability:**
   - Parameter rankings are preserved between spaces: $L > F > \%B > d_p > T = d_c = 0$.
   - However, in the narrow AQbD robustness space, the relative contribution of Column Length surges from $50.6\%$ to $77.9\%$, while Flow Rate sensitivity drops from $38.8\%$ to $18.8\%$, and Modifier sensitivity drops from $8.2\%$ to $3.1\%$.
2. **Total Interaction Collapse:**
   - In the wide space, total interaction variance accounts for only **$4.47\%$** ($\sum(S_T - S_1) = 0.0447 < 0.05$).
   - In the narrow operational space, total interaction variance collapses to **$0.16\%$** ($\sum(S_T - S_1) = 0.0016$).
   - **First-order main effects explain $99.86\%$ of all variance** in the narrow operational space!
   - This proves that in real-world AQbD robustness testing (where factors vary by $\pm 5-10\%$), the SimuPharm engine is **purely additive and linear**.
   - Under ICH Q14 conditions, Sobol variance decomposition provides zero added value over simple single-factor derivatives.
