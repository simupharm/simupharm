# FORENSIC AUDIT: SIMUPHARM HPLC ENGINE ARCHITECTURE
## MATHEMATICAL EQUATIONS, CODE CONSTRAINTS & STRUCTURAL ARTIFACT AUDIT

### 1. CODEBASE INSPECTION & VERIFICATION OF CODE FREEZE
The scientific simulation engine was inspected in its frozen state within `backend/science/hplc.py` (144 lines) and `backend/simulations/router.py` (lines 128–132). In compliance with the Phase 4/5 code freeze, no code modifications were made. The simulator was evaluated strictly as-is through Python 3.12 API calls.

---

### 2. MATHEMATICAL SPECIFICATION OF ENGINE EQUATIONS

#### A. Plate Height Equation (Van Deemter Formulation)
The engine implements the classical Van Deemter equation in `van_deemter(particle_size_um, flow_rate)`:
$$H = A + \frac{B}{u} + C \cdot u$$
Where:
- $d_p = d_{p,\mu m} \times 10^{-4}$ (particle diameter in cm)
- $u = \text{flow\_rate}$ (flow rate in mL/min, used directly as linear velocity proxy)
- $A = 2 \cdot d_p$ (eddy diffusion term)
- $B = 0.05$ cm·mL/min (longitudinal diffusion coefficient)
- $C = 0.01 \cdot d_p^2 = 0.01 \cdot (d_p \times 10^{-4})^2 = 1.0 \times 10^{-10} \cdot d_{p,\mu m}^2$ (resistance to mass transfer)

#### Mathematical Audit of the Inverted Flow Rate Phenomenon:
The theoretical optimum linear velocity $u_{\text{opt}}$ where plate height is minimized is given by:
$$u_{\text{opt}} = \sqrt{\frac{B}{C}} = \sqrt{\frac{0.05}{0.01 \cdot (5 \times 10^{-4})^2}} = \sqrt{\frac{0.05}{2.5 \times 10^{-9}}} = \sqrt{2 \times 10^7} \approx 4,472.1 \text{ mL/min}$$
The corresponding minimum plate height is:
$$H_{\min} = A + 2\sqrt{B \cdot C} = 0.001 + 2\sqrt{0.05 \times 2.5 \times 10^{-9}} = 0.001022 \text{ cm}$$

**Critical Structural Flaw:**
- In genuine reversed-phase HPLC, $u_{\text{opt}}$ occurs at flow rates between $0.5$ and $1.0$ mL/min for a standard 4.6 mm ID column.
- In SimuPharm, $u_{\text{opt}}$ is **4,472 mL/min** (4.47 Liters per minute!).
- Across the entire operational flow range ($0.2$ to $2.5$ mL/min), the resistance to mass transfer term $C \cdot u$ is completely negligible ($\sim 10^{-9}$ cm), while the longitudinal diffusion term $B/u$ completely dominates ($0.025$ to $0.25$ cm).
- Consequently, **higher flow rate monotonically decreases $H$, increases plate count $N$, and increases chromatographic resolution $R_s$**.
- This is the exact inverse of physical chromatography in the normal operational range, where operating above $1.0$ mL/min degrades resolution due to mass transfer limitations.

#### B. Column Dead Time ($t_0$)
The engine calculates dead time using an empirical shortcut:
$$t_0 = \frac{L}{10 \cdot F}$$
Where $L$ is column length in cm and $F$ is flow rate in mL/min.
- **Physical Reality:** In physical HPLC, $t_0 = \frac{V_0}{F} = \frac{\epsilon_u \cdot \pi \cdot (d_c/2)^2 \cdot L}{F}$.
- **Omission:** The engine formula completely ignores column internal diameter $d_c$ and interstitial column porosity $\epsilon_u$. A 2.1 mm narrow-bore column and a 4.6 mm standard column have identical dead times in SimuPharm.

#### C. Retention Factor & Mobile Phase Modifier Response
The engine implements a linear capacity factor scaling heuristic:
$$k'_{\text{adjusted}} = k'_{\text{ref}} \cdot \frac{100 - \%B}{40}$$
$$t_R = t_0 \cdot (1 + k'_{\text{adjusted}}) = \frac{L}{10 \cdot F} \left[1 + k'_{\text{ref}} \cdot \frac{100 - \%B}{40}\right]$$
- **Theoretical Assessment:** In physical chromatography, retention factor varies exponentially/logarithmically with organic modifier fraction according to the Snyder-Soczewinski or Linear Solvent Strength (LSS) model: $\ln k' = \ln k'_w - S \cdot \phi$.
- SimuPharm uses a linear slope normalized around $\%B = 60\%$ (where $(100 - 60)/40 = 1.0$).
- Outside the range $30\% \le \%B \le 70\%$, this linear heuristic diverges severely from real retention isotherms, resulting in the 25.50% MAPE documented in the Phase 3 forensic audit.
- If $\%B > 100\%$, $k'_{\text{adjusted}}$ becomes negative, predicting solute elution before dead time ($t_R < t_0$), which violates causality.

#### D. Chromatographic Resolution ($R_s$)
In the simulation loop for successive peaks:
$$R_s = \frac{2(t_{R2} - t_{R1})}{w_2 + w_2} = \frac{t_{R2} - t_{R1}}{w_2}$$
Where $w_2 = 4\sigma_2 = 4 \frac{t_{R2}}{\sqrt{N}} = 4 \frac{t_{R2} \sqrt{H}}{\sqrt{L}}$.
Substituting the expressions for retention times:
$$t_{R2} - t_{R1} = t_0 \cdot \frac{100 - \%B}{40} (k'_{2} - k'_{1})$$
$$R_s = \frac{t_0 \cdot \frac{100 - \%B}{40} (k'_2 - k'_1)}{4 \cdot \frac{t_0 [1 + k'_2 (100 - \%B)/40] \sqrt{H}}{\sqrt{L}}} = \frac{\sqrt{L}}{4\sqrt{H}} \cdot \frac{(k'_2 - k'_1) \frac{100 - \%B}{40}}{1 + k'_2 \frac{100 - \%B}{40}}$$

**Crucial Analytical Finding:**
- Dead time $t_0 = \frac{L}{10 F}$ cancels out completely from the resolution equation!
- Resolution depends on $L$ solely via $\sqrt{L}$.
- Resolution depends on $F$ and $d_p$ solely via $1/\sqrt{H(d_p, F)}$.
- Resolution depends on $\%B$ solely via the hyperbolic ratio $\frac{\Delta k' (100 - \%B)}{40 + k'_2 (100 - \%B)}$.

---

### 3. AUDIT OF INACTIVE & STOCHASTIC ENGINE PARAMETERS
A systematic sensitivity audit was conducted to verify which declared parameters exert an active physical influence:

| Parameter | Pydantic Schema Status | Mathematical Role in Engine | Verified Sensitivity ($S_i$) | Audit Classification |
|---|---|---|---|---|
| Column Length ($L$) | Declared in `ColumnParams` | Determines $N = L/H$ and $t_0$ | $0.5063$ | **Active** |
| Flow Rate ($F$) | Declared in `HPLCParams` | Determines $H$ via $B/u$ and $t_0$ | $0.3878$ | **Active (Artifactual)** |
| Organic Fraction ($\%B$) | Declared in `HPLCParams` | Modifies $k'$ via $(100 - \%B)/40$ | $0.0819$ | **Active (Heuristic)** |
| Particle Size ($d_p$) | Declared in `ColumnParams` | Enters $A$ and $C$ in Van Deemter | $0.00001$ | **Trace Active** |
| Temperature ($T$) | Declared in `ColumnParams` | **COMPLETELY UNUSED** | **$0.00000$** | **DEAD INACTIVE** |
| Internal Diameter ($d_c$) | Declared in `ColumnParams` | **COMPLETELY UNUSED** | **$0.00000$** | **DEAD INACTIVE** |
| Injection Volume | Declared in `HPLCParams` | **COMPLETELY UNUSED** | **$0.00000$** | **DEAD INACTIVE** |
| Tailing Factor | Returned in `ChromatogramPeak` | `1.0 + np.random.uniform(0, 0.3)` | **Stochastic Noise** | **DEAD ARTIFACT** |
| Baseline Signal | Returned in `HPLCResult` | `+ np.random.normal(0, 0.001)` | **Stochastic Noise** | **DEAD ARTIFACT** |

### 4. FORENSIC AUDIT CONCLUSION
1. Temperature is declared in the user schema but is absent from all retention and plate count calculations. The Phase 5.1 hypothesis of a strong $T \times \%B$ interaction is falsified by inspection of the code.
2. The model's primary sensitivity driver ($L$, $S_1 = 0.506$) and second driver ($F$, $S_1 = 0.388$) reflect a non-physical inverted Van Deemter curve where $R_s$ improves monotonically with flow rate.
3. The peak asymmetry/tailing factor is generated purely by pseudo-random number draws ($U(0, 0.3)$) and has zero relationship to column chemistry, mobile phase pH, or silanol interactions.
4. Applying advanced Sobol sensitivity analysis to this engine means analyzing numerical artifacts rather than chromatographic physics.
