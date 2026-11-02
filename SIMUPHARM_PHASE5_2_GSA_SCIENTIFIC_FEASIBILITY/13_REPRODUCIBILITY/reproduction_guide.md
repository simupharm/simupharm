# REPRODUCIBILITY GUIDE & PIPELINE EXECUTION REGISTER
## COMPUTATIONAL ENVIRONMENT, SEEDS & EXECUTION PROTOCOL

### 1. COMPUTATIONAL ENVIRONMENT SPECIFICATIONS
- **Operating System:** Microsoft Windows 11 Pro (x86_64)
- **Python Version:** Python 3.12.3
- **Primary Numerical Libraries:**
  - `numpy`: Version 2.2.6
  - `scipy`: Version 1.14.1
  - `pandas`: Version 3.0.2
  - `scikit-learn`: Version 1.5.2
  - `matplotlib`: Version 3.10.8
  - `SALib`: Version 1.6.0
  - `playwright`: Version 1.63.0
  - `pypdf`: Version 6.19.0

---

### 2. EXECUTION INSTRUCTIONS
The entire computational pipeline for Phase 5.2 is self-contained within:
`SIMUPHARM_PHASE5_2_GSA_SCIENTIFIC_FEASIBILITY/run_gsa_feasibility_analysis.py`

To reproduce all numerical indices, tables, and figures from scratch:
```powershell
python SIMUPHARM_PHASE5_2_GSA_SCIENTIFIC_FEASIBILITY/run_gsa_feasibility_analysis.py
```
- **Total Execution Time:** ~152 seconds (~2.5 minutes).
- **Total Model Runs:** ~102,000 evaluations of `simulate_hplc`.
- **Output Artifacts:** Automatically populated across subdirectories `02_ENGINE_AUDIT` through `08_FAILURE_BOUNDARY`.

---

### 3. PSEUDO-RANDOM NUMBER GENERATOR SEEDS
All stochastic routines are strictly locked to explicit seeds to ensure bit-level reproducibility:
- **Sobol Convergence Sequences ($N = 256, 512, 1024, 2048$):** Seed = `42`
- **Seed Stability Evaluation:** Seeds = `[42, 123, 456, 789]`
- **DoE / Response Surface Training Sample:** Seed = `42`
- **Response Surface Independent Test Set ($N=1000$):** Seed = `42`
- **Failure Boundary Monte Carlo Sample ($N=5000$):** Seed = `999`
- **Physical Plausibility Hydraulic Pressure Sample ($N=5000$):** Seed = `1234`
- **Decision Tree Classifier:** `random_state = 42`

---

### 4. DATA CATALOG & OUTPUT ARTIFACT REGISTER
- `02_ENGINE_AUDIT/engine_audit_summary.json`: Forensic parameter sensitivities & Van Deemter coefficients.
- `02_ENGINE_AUDIT/physical_plausibility_summary.json`: Hydraulic pressure statistics & valid domain fraction.
- `03_PARAMETER_SPACE/parameter_ranges.csv`: Operational parameter bounds & baseline values.
- `03_PARAMETER_SPACE/wide_vs_narrow_sobol_comparison.csv`: Range sensitivity comparison table.
- `04_PILOT_SOBOL/sobol_indices_N1024_seed42.csv`: Reference Sobol $S_1$ and $S_T$ indices with 95% CIs.
- `04_PILOT_SOBOL/sobol_seed_stability_stats.csv`: Mean and standard deviation across independent seeds.
- `05_CONVERGENCE/sobol_convergence_by_N.csv`: Convergence trajectories across sample sizes.
- `06_OFAT_COMPARISON/ofat_baseline_results.csv`: OFAT sensitivities and rankings.
- `07_INTERACTION_ANALYSIS/pairwise_interactions_S2.csv`: Full pairwise second-order interaction matrix.
- `07_INTERACTION_ANALYSIS/rsm_comparison_summary.json`: 2nd-order polynomial $R^2$ and RMSE metrics.
- `08_FAILURE_BOUNDARY/failure_boundary_summary.json`: Failure probability $P(R_s < 1.5)$ and decision tree rules.
