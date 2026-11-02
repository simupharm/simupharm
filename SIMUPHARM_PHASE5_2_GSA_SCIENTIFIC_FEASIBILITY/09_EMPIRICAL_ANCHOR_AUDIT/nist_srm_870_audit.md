# FORENSIC AUDIT: NIST SRM 870 COLUMN CHARACTERIZATION STANDARD
## EVALUATION AS AN EXTERNAL VALIDATION ANCHOR FOR GLOBAL SENSITIVITY ANALYSIS

### 1. SPECIFICATION & EXPERIMENTAL CONDITIONS OF NIST SRM 870
NIST Standard Reference Material (SRM) 870 ("Column Selectivity Test Mixture for Liquid Chromatography") is an internationally recognized reference material developed by Sander and Wise (NIST, 2003) to characterize the chromatographic selectivity and activity of reversed-phase C18 columns.

The standard defines a strictly frozen, single-condition operational protocol:
- **Mobile Phase:** Methanol / Water mixture (80:20 v/v) containing 0.02 M potassium phosphate buffer, pH 7.00 ± 0.05.
- **Flow Rate:** Exactly 1.00 ± 0.05 mL/min.
- **Temperature:** Exactly 23.0 ± 0.5 °C.
- **Column Dimensions:** 4.6 mm internal diameter × 250 mm length (or 150 mm with proportional flow scaling).
- **Test Analytes (5 Compounds):**
  1. *Uracil:* Void volume ($t_0$) marker (unretained solute).
  2. *Toluene:* Hydrophobic retention and methylene selectivity reference.
  3. *Ethylbenzene:* Hydrophobic retention reference ($k'_{EB}$).
  4. *Quinizarin:* Chelation / metal activity marker (binds residual trace heavy metals on silica substrate).
  5. *Amitriptyline:* Silanophilic activity / base tailing marker at neutral pH (cation exchange with unreacted silanol groups $\equiv \text{Si-O}^-$).

---

### 2. FORENSIC AUDIT OF VARIANCE & PARAMETER PERTURBATIONS
To serve as an empirical anchor or validation dataset for **Global Sensitivity Analysis (GSA)** or **Variance Decomposition**, a candidate benchmark must satisfy two fundamental requirements:
1. It must provide experimental response measurements across a **multi-dimensional grid of varying factors** (e.g., varying flow rate $F$, varying modifier fraction $\%B$, varying temperature $T$, and varying column geometry $L, d_p$).
2. It must permit empirical estimation of first-order sensitivity slopes ($\partial y / \partial x_i$) and cross-parameter interaction curvatures ($\partial^2 y / \partial x_i \partial x_j$).

#### Critical Audit Finding:
**NIST SRM 870 provides NONE of these multi-dimensional perturbations.**
- In NIST SRM 870, flow rate is **fixed at 1.0 mL/min**. It is not varied.
- Mobile phase composition is **fixed at 80:20 methanol:buffer**. It is not varied.
- Temperature is **fixed at 23 °C**. It is not varied.
- Column length is **fixed at 250 mm**. It is not varied.
- Particle size is fixed for each tested column.

The NIST SRM 870 certificate records chromatographic descriptors (retention factor $k'_{EB}$, methylene selectivity $\alpha = k'_{EB}/k'_{Tol}$, chelation activity ratio $r = k'_{Quin}/k'_{Tol}$, and base asymmetry factor $As_{Amit}$) at **ONE SINGLE OPERATING POINT**.

---

### 3. FALSIFICATION CONCLUSION FOR DIRECTION B
- **Can NIST SRM 870 validate retention times at 80:20 methanol?** Yes, as a single-point calibration check for those specific five analytes.
- **Can NIST SRM 870 validate parameter sensitivity rankings ($S_i$)?** **NO.** A dataset with zero variance in operational parameters cannot measure, validate, or falsify sensitivity derivatives or variance decomposition.
- **Can NIST SRM 870 validate failure boundary contours ($R_s < 1.5$)?** **NO.** The standard protocol guarantees baseline separation of its five solutes on acceptable C18 columns; it does not explore failure boundaries.
- **Audit Verdict:** Classifying NIST SRM 870 as an "empirical validation dataset for GSA" is a **methodological error**. Reviewers at *J. Chromatogr. A* would immediately reject any claim that NIST SRM 870 validates multidimensional Sobol sensitivity rankings.
