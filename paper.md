---
title: 'SimuPharm: An Open-Source Multi-Instrument Analytical and Spectroscopic Simulation Suite'
tags:
  - Python
  - analytical chemistry
  - chromatography
  - spectroscopy
  - chemometrics
  - pharmaceutical analysis
authors:
  - name: Pranav Santosh Dhanwate
    affiliation: 1
affiliations:
  - name: Department of Pharmaceutical Chemistry, Pravara Rural College of Pharmacy, Loni, Maharashtra 413736, India
    index: 1
date: 22 November 2026
bibliography: paper.bib
---

# Summary

Analytical instrumentation represents the backbone of modern pharmaceutical quality assurance, chemical manufacturing, and regulatory compliance. However, hands-on training, method screening, and iterative validation on physical hardware are severely bottlenecked by capital acquisition costs ($100,000–$300,000 per instrument), expensive column replacement, hazardous organic solvent consumption, and equipment availability. While isolated simulation tools exist for individual analytical modalities, no open-source Python library unifies multiple orthogonal instruments with chemometric cross-validation into an extensible, headless computational pipeline.

`SimuPharm` is an open-source, modular Python package that models first-principles physical kinetics and chemometric suitability across seven analytical and spectroscopic instruments:
1. **High-Performance Liquid Chromatography (HPLC):** Implements Van Deemter plate height kinetics, capacity factors, solvent strength gradient modeling, peak tailing asymmetry, and automated USP <621> suitability (theoretical plates $N$, tailing factor $T$, resolution $R_s$).
2. **UV-Visible Spectrophotometry:** Implements Beer-Lambert electronic absorption, Gaussian vibronic deconvolution, additive photometric noise, and ICH Q2(R1) ordinary least squares calibration statistics ($R^2$, LOD, LOQ).
3. **Fourier Transform Infrared (FTIR) Spectroscopy:** Synthesizes Michelson interferograms with fast Fourier transform (FFT) conversion and functional group vibrational assignment.
4. **Gas Chromatography (GC):** Implements Golay capillary column kinetics with linear thermal programming.
5. **Mass Spectrometry (EI & ESI-MS):** Computes natural isotopic abundance envelopes (M, M+1, M+2) and fragmentation trees.
6. **Polarimetry:** Implements Biot's optical rotation law with Drude wavelength dispersion and enantiomeric excess ($ee$) calculation.
7. **Particle Size Analysis (PSA):** Simulates dynamic light scattering and log-normal volume distributions ($D_{10}, D_{50}, D_{90}$, Span).

Evaluating full chromatograms in sub-3-millisecond runtimes, `SimuPharm` enables large-scale virtual screening, automated Quality-by-Design (QbD) optimization, synthetic dataset generation for analytical machine learning, and multimodal compound deconvolution across a curated database of 21 pharmacopeial active pharmaceutical ingredients (APIs).

# Statement of Need

Modern pharmaceutical regulatory submissions governed by the International Council for Harmonisation (ICH) and United States Pharmacopeia (USP) require orthogonal analytical verification across multiple complementary instruments. In educational institutions and resource-constrained research laboratories, access to operational UHPLC, FTIR, or Mass Spectrometers is frequently unavailable or strictly rationed.

Commercial chromatography modeling platforms (such as DryLab and ACD/Labs) provide accurate separation modeling but are proprietary, closed-source, cost-prohibitive, and lack headless Python integration for batch automation. Open-source separation packages (e.g., PyChroma, ChromAuto) generally model only HPLC or GC in isolation and omit orthogonal spectroscopic techniques and pharmacopeial compliance metrics.

`SimuPharm` bridges this gap by providing an open-access, pure-Python 3.10+ package with standardized Pydantic data schemas, zero wet-lab overhead, and 100% automated test coverage. Researchers can embed `SimuPharm` into automated chromatographic optimization workflows, synthetic analytical benchmark generation, and remote interactive teaching environments.

# Software Architecture and Verification

`SimuPharm` is structured into four decoupled layers:
- **Parameter Validation Layer:** Pydantic-validated models for instrument operating parameters and compound physicochemical properties.
- **Physical Simulation Engines:** Vectorized NumPy/SciPy engines calculating physical separation kinetics, interferogram FFTs, and light dispersion.
- **Analytics & Chemometrics Layer:** Automated USP <621> system suitability verification, ICH Q2(R1) calibration, and multimodal orthogonal consensus matching.
- **Deployment Interfaces:** Pure Python API, FastAPI REST endpoints, and interactive React web interface.

The package includes a comprehensive automated test suite executed via `pytest`, achieving 100% test passing rates across all seven physical engines and chemometric validation pipelines. Source code, documentation, and automated tests are hosted openly on GitHub under the MIT License: https://github.com/simupharm/simupharm.

# Acknowledgements

The author acknowledges the Department of Pharmaceutical Chemistry at Pravara Rural College of Pharmacy, Loni, Maharashtra, India, for academic support and computational infrastructure.

# References
