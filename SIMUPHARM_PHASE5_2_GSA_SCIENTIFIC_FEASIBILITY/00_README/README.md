# SIMUPHARM.IO — PHASE 5.2
## GSA SCIENTIFIC FEASIBILITY, FALSIFICATION & KILL SPRINT
### PROJECT REPOSITORY & ARCHIVAL REGISTER

**Status:** ACTIVE AUDIT & COMPUTATIONAL SPRINT  
**Target Research Direction:** Direction B (Global Sensitivity Analysis / Sobol Variance Decomposition of Chromatographic Robustness & Failure Regions)  
**Governance Framework:** Pre-registered Falsification Architecture (Adversarial Red-Team Protocol)  
**Code Freeze Authority:** Phase 4 / Phase 5 Non-Negotiable Engine Freeze (`backend/science/hplc.py` strictly locked)

---

### DIRECTORY STRUCTURE & REPOSITORY MAP

```
SIMUPHARM_PHASE5_2_GSA_SCIENTIFIC_FEASIBILITY/
├── 00_README/
│   └── README.md                                    # This directory index and scope definition
├── 01_GOVERNANCE/
│   ├── governance_charter.md                       # Non-negotiable rules, code freeze, ethics boundary
│   └── falsification_protocol.md                   # Formal pre-registered hypotheses and kill criteria
├── 02_ENGINE_AUDIT/
│   ├── engine_forensic_audit.md                    # In-depth mathematical and structural engine dissection
│   ├── engine_audit_summary.json                   # Numerical verification of parameter sensitivities
│   ├── physical_plausibility_summary.json          # Hydraulic pressure limits and invalid domain proportions
│   ├── van_deemter_audit.png                       # Forensic plot of inverted Van Deemter curve
│   └── hydraulic_pressure_audit.png                # Backpressure distribution across sampled particle sizes
├── 03_PARAMETER_SPACE/
│   ├── parameter_ranges.csv                        # Operational limits, baselines, and justification
│   ├── wide_vs_narrow_sobol_comparison.csv         # Sensitivity index comparison across range choices
│   └── range_sensitivity_comparison.png           # Bar chart comparing wide vs narrow design spaces
├── 04_PILOT_SOBOL/
│   ├── sobol_indices_N1024_seed42.csv              # Reference First-order (S1) and Total-order (ST) indices
│   ├── sobol_seed_stability.csv                    # Evaluation across random seeds (42, 123, 456, 789)
│   └── sobol_seed_stability_stats.csv              # Mean, standard deviation, and CV across seeds
├── 05_CONVERGENCE/
│   ├── sobol_convergence_by_N.csv                  # Sobol indices across N = 256, 512, 1024, 2048
│   └── convergence_plot_ST.png                     # Multi-curve convergence trajectory plot
├── 06_OFAT_COMPARISON/
│   ├── ofat_baseline_results.csv                   # One-factor-at-a-time sensitivity and ranking
│   ├── ofat_response_curves.csv                    # 21-point OFAT sweeps for all 6 parameters
│   └── ofat_response_curves.png                    # Normalized OFAT response curves
├── 07_INTERACTION_ANALYSIS/
│   ├── pairwise_interactions_S2.csv                # Complete second-order Sobol interaction matrix
│   ├── rsm_comparison_summary.json                 # 2nd-order polynomial DoE / RSM fit and R² evaluation
│   ├── sobol_S1_ST_barchart.png                    # First-order vs Total-order bar chart (ST - S1)
│   └── rsm_actual_vs_predicted.png                 # Scatter plot of RSM predicted vs SimuPharm actual Rs
├── 08_FAILURE_BOUNDARY/
│   ├── failure_boundary_summary.json               # Empirical failure probability P(Rs < 1.5) and tree rules
│   └── failure_boundary_contour.png                # 2D contour map with overlay of critical failure boundary
├── 09_EMPIRICAL_ANCHOR_AUDIT/
│   ├── nist_srm_870_audit.md                       # Forensic audit of NIST SRM 870 single-point data
│   └── tanaka_database_audit.md                    # Forensic audit of Tanaka column characterization data
├── 10_LITERATURE_RECHECK/
│   └── literature_synthesis_2020_2026.md           # Systematic review of GSA in HPLC and AQbD
├── 11_REVIEWER_RED_TEAM/
│   └── hostile_reviewer_cross_examination.md      # 18-question adversarial red-team examination
├── 12_GO_NO_GO/
│   ├── decision_matrix_16_dimensions.md            # Comprehensive 16-criteria evaluation matrix
│   ├── required_answers_20_questions.md            # Explicit answers to all 20 required questions
│   └── final_scientific_decision.md                # Exact format verdict and governance determination
├── 13_REPRODUCIBILITY/
│   ├── reproduction_guide.md                       # Complete software environment, seeds, execution instructions
│   └── run_gsa_feasibility_analysis.py             # Self-contained computational pipeline script
└── 14_FINAL_REPORT/
    └── SIMUPHARM_PHASE5_2_GSA_SCIENTIFIC_FEASIBILITY_AND_KILL_SPRINT.pdf # Consolidated master deliverable
```

---

### CORE FALSIFICATION PHILOSOPHY
Phase 5.2 operates under an absolute adversarial falsification standard. We do not attempt to justify Direction B; we actively interrogate its physical validity, mathematical stability, incremental information gain over conventional DoE/OFAT, and defense against expert chromatographic peer review.
