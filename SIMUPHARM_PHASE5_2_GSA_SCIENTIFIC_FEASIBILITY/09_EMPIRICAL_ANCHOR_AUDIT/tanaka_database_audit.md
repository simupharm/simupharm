# FORENSIC AUDIT: TANAKA COLUMN CHARACTERIZATION DATABASE
## EVALUATION AS AN EXTERNAL VALIDATION ANCHOR FOR GLOBAL SENSITIVITY ANALYSIS

### 1. SPECIFICATION OF THE TANAKA CHARACTERIZATION PROTOCOL
The Tanaka column test protocol (Tanaka et al., 1989; Kimata et al., 1989; Euerby & Petersson, 2003) is the most widely adopted framework for characterizing reversed-phase liquid chromatographic stationary phases.

The database compiles measurements across more than 100 commercial HPLC columns using six standardized chromatographic selectivity tests:
1. **Hydrophobic Retention ($k'_{PB}$):** Pentylbenzene retention factor in 80:20 methanol/water at 40 °C.
2. **Hydrophobic Selectivity ($\alpha_{CH2}$):** Selectivity between pentylbenzene and butylbenzene ($k'_{PB} / k'_{BB}$).
3. **Steric / Shape Selectivity ($\alpha_{T/O}$):** Selectivity between triphenylene and o-terphenyl ($k'_{Triphenyl} / k'_{o-Terphenyl}$).
4. **Hydrogen Bonding Capacity ($\alpha_{C/P}$):** Selectivity between caffeine and phenol ($k'_{Caff} / k'_{Phen}$).
5. **Total Ion-Exchange Capacity at pH 7.6 ($\alpha_{B/P}$):** Selectivity between benzylamine and phenol in methanol/phosphate buffer pH 7.6.
6. **Acidic Ion-Exchange Capacity at pH 2.7 ($\alpha_{B/P}$):** Selectivity between benzylamine and phenol at pH 2.7.

---

### 2. CAN TANAKA DATA VALIDATE SENSITIVITY SURFACES?
To evaluate whether Tanaka database entries can validate SimuPharm's Global Sensitivity Analysis, we examine the structural alignment between what Tanaka provides and what Direction B simulates:

1. **Parameter Dimensionality:**
   - Tanaka parameters describe **stationary phase chemistry** (ligand density, carbon load, silanol activity, pore structure).
   - SimuPharm's engine does not model stationary phase chemistry parameters (no terms for ligand density, silanol pKa, or hydrophobic surface area).
   - SimuPharm simulates **operational variables**: Flow Rate ($F$), % Organic modifier ($\%B$), Column Length ($L$), and Particle Size ($d_p$).
2. **Operational Grids:**
   - In the Tanaka database, all columns are evaluated under fixed standardized mobile phases and fixed flow rates (1.0 mL/min).
   - There are **no flow rate sweeps**, **no organic gradient sweeps**, and **no multi-dimensional robustness grids**.
3. **Applicability to SimuPharm:**
   - SimuPharm's engine assumes generic $k'_{\text{ref}}$ capacity factors for 21 APIs and scales retention purely by $(100 - \%B)/40$.
   - Tanaka data cannot validate the $(100 - \%B)/40$ slope because Tanaka tests are performed at fixed 80% methanol.

---

### 3. AUDIT VERDICT ON EMPIRICAL ANCHORING
- **Model Calibration:** Tanaka data can provide reference retention factors for caffeine and phenol on specific C18 brands, but this constitutes single-point parameter fitting, not sensitivity validation.
- **Model Validation:** Tanaka data cannot validate the prediction of retention under varying flow, temperature, or mobile phase composition.
- **Sensitivity Validation:** **IMPOSSIBLE.** The Tanaka protocol has zero variance across operational parameters ($F, \%B, L$).
- **Robustness Boundary Validation:** **IMPOSSIBLE.**
- **Consequence for Direction B:** Direction B cannot rely on either NIST SRM 870 or the Tanaka database to provide empirical validation of its Global Sensitivity Analysis. If Direction B is submitted to an analytical chemistry journal without independent multi-dimensional experimental data, reviewers will classify the paper as a purely synthetic numerical simulation study on an unvalidated toy model.
