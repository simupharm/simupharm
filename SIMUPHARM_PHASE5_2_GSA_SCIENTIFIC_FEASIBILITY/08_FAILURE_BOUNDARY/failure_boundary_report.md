# FAILURE-BOUNDARY & CHROMATOGRAPHIC DESIGN SPACE ANALYSIS
## PROBABILITY OF SYSTEM SUITABILITY FAILURE & DECISION RULES

### 1. SPECIFICATION OF SYSTEM SUITABILITY FAILURE CRITERIA
In pharmaceutical liquid chromatography under USP <621> and FDA guidance, chromatographic separation failure is defined by minimum peak resolution:
- **Marginal Separation Failure:** $R_{s,\min} < 1.5$ (Baseline separation between critical pair is lost, violating standard quantitative assay suitability).
- **Severe Separation Failure:** $R_{s,\min} < 1.0$ (Significant peak co-elution / overlap, preventing integration).
- **Secondary Failure Modes:**
  - Column overpressure: $\Delta P > 400$ bar (instrument shutdown).
  - Unacceptable throughput: $t_R > 30.0$ min (unfeasible QC cycle time).
  - Void volume breakthrough: $k'_1 < 0.5$ (solute elutes in solvent front).

---

### 2. EMPIRICAL FAILURE PROBABILITY OVER DESIGN SPACE
Monte Carlo sampling ($N = 5,000$ points) across the wide exploratory design space yielded:
- **Probability of Separation Failure ($R_{s,\min} < 1.5$):** $P(\text{Fail}) = \mathbf{0.4846}$ ($48.46\%$).
- **Probability of Severe Failure ($R_{s,\min} < 1.0$):** $P(\text{Severe}) = \mathbf{0.1126}$ ($11.26\%$).
- **In the Narrow Robustness Space:** $P(\text{Fail}) = \mathbf{0.0000}$ ($0.0\%$, all points maintain $R_s \ge 1.5$ because nominal baseline $R_s = 1.505$ is buffered).

---

### 3. DECISION TREE EXTRACTION OF FAILURE BOUNDARIES
A shallow decision tree (depth 3) trained on the 5,000 Monte Carlo evaluations isolated the exact boundary conditions governing chromatographic failure:

```
[Primary Boundary Decision Logic]
|--- Column Length (L) <= 12.04 cm
|   |--- Flow Rate (F) <= 1.64 mL/min
|   |   |--- L <= 9.87 cm  --> CLASS: FAIL (Rs < 1.5, 100% probability)
|   |   |--- L >  9.87 cm  --> CLASS: FAIL (Rs < 1.5, 96% probability)
|   |--- Flow Rate (F) >  1.64 mL/min
|   |   |--- L <= 8.27 cm  --> CLASS: FAIL (Rs < 1.5)
|   |   |--- L >  8.27 cm  --> CLASS: PASS (Rs >= 1.5)
|--- Column Length (L) >  12.04 cm
|   |--- Flow Rate (F) <= 0.91 mL/min
|   |   |--- L <= 19.80 cm --> CLASS: FAIL (Rs < 1.5)
|   |   |--- L >  19.80 cm --> CLASS: FAIL (Rs < 1.5)
|   |--- Flow Rate (F) >  0.91 mL/min
|   |   |--- F <= 1.13 mL/min --> CLASS: PASS (Rs >= 1.5)
|   |   |--- F >  1.13 mL/min --> CLASS: PASS (Rs >= 1.5)
```

---

### 4. AUDIT EVALUATION: PHYSICAL TRUTH VS. ARTIFACTUAL BOUNDARY
- The decision tree reveals that the failure boundary is almost entirely determined by **Column Length ($L$)** and **Flow Rate ($F$)**.
- Notice the direction of the boundary: In SimuPharm, operating at low flow rates ($F \le 0.91$ mL/min) triggers separation failure even on 15 cm columns!
- Conversely, increasing flow rate above $1.13$ mL/min rescues separation and guarantees $R_s \ge 1.5$.
- In the real physical laboratory, running at $1.5 - 2.0$ mL/min on a 5 µm column degrades efficiency and reduces resolution due to the $C$-term resistance to mass transfer.
- The failure boundary mapped by GSA in SimuPharm is **inverted relative to real chromatographic physics**. An analytical chemist following this simulated "robust design space" in a real lab would operate at high flow rates, leading to excessive column backpressure and degraded chromatographic resolution.
