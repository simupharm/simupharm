# SimuPharm: An Open-Source Multi-Instrument Analytical and Spectroscopic Simulation Suite for Pharmaceutical Research and Education

**Authors:** SimuPharm Development Team  
**Affiliation:** SimuPharm Open Source Project  
**Contact Email:** info@simupharm.io  
**Repository:** https://github.com/simupharm/simupharm  
**Target Journal:** *SoftwareX* (Elsevier)

---

## Abstract

Analytical instrument training and method optimization in pharmaceutical chemistry frequently encounter prohibitive obstacles: high operational expenditures, consumable solvent costs, hazardous waste generation, and competitive access bottlenecks for advanced hardware such as High-Performance Liquid Chromatography (HPLC), Fourier-Transform Infrared (FTIR), and Mass Spectrometry (MS). While single-technique pedagogical simulators exist, no unified, high-throughput, open-source Python library currently integrates multiple orthogonal pharmaceutical analytical instruments with chemometric cross-validation into an extensible programmatic environment. 

In this work, we introduce **SimuPharm**, an open-source Python library and simulation suite that models seven primary analytical and spectroscopic instruments: (1) HPLC with Van Deemter column kinetics, capacity factors, peak tailing asymmetry, and United States Pharmacopeia (USP <621>) system suitability; (2) UV-Vis spectrophotometry with Beer-Lambert absorption, Gaussian band deconvolution, and ICH Q2(R1) calibration statistics (LOD/LOQ); (3) FTIR spectroscopy with Michelson interferogram Fast Fourier Transforms (FFT), transmittance modeling, and automated functional group correlation tagging; (4) Gas Chromatography (GC) with Golay capillary plate kinetics and multi-ramp linear temperature programming; (5) Electron Ionization (EI) and Electrospray Ionization (ESI) Mass Spectrometry with natural isotopic envelope calculations (M, M+1, M+2) and fragmentation trees; (6) Polarimetry with Biot's law, Drude wavelength dispersion, and enantiomeric excess ($ee$) determination; and (7) Particle Size Analysis (PSA) with dynamic light scattering, log-normal size distribution, D10/D50/D90 percentile calculations, and span metrics. Built on pure Python, NumPy, and SciPy, SimuPharm achieves sub-5-millisecond execution times per run, supports headless batch computational pipelines, and provides orthogonal spectral cross-matching across a curated database of 21 pharmacopeial active pharmaceutical ingredients (APIs). SimuPharm offers an accessible, zero-cost, environmentally sustainable platform for pharmaceutical method development, computational screening, and virtual laboratory education.

**Keywords:** Pharmaceutical Analysis; Chromatography Simulation; Spectroscopy Modeling; Van Deemter Equation; Chemometrics; Virtual Laboratory; Open-Source Software

---

## Metadata Table

| Nr. | Code Metadata Description | Metadata Details |
|:---|:---|:---|
| C1 | Current code version | v1.0.0 |
| C2 | Permanent link to code / repository | https://github.com/simupharm/simupharm |
| C3 | Permanent link to reproducible environment | https://github.com/simupharm/simupharm/releases/tag/v1.0.0 |
| C4 | Legal Code License | MIT License |
| C5 | Code versioning system used | Git |
| C6 | Software code language | Python 3.10+ |
| C7 | Compilation requirements & dependencies | `numpy >= 1.22.0`, `scipy >= 1.8.0`, `pydantic >= 2.0.0` |
| C8 | Optional dependencies | `matplotlib >= 3.5.0` (plotting), `pytest >= 7.0.0` (testing) |
| C9 | Supported operating systems | Linux, macOS, Microsoft Windows (x86_64, ARM64) |
| C10 | Support email for software issues | info@simupharm.io |

---

## 1. Motivation and Significance

Modern pharmaceutical quality assurance, regulatory compliance, and drug discovery rely on an extensive battery of complementary analytical instrumentation. Regulatory frameworks established by the International Council for Harmonisation (ICH) and pharmacopeial standards such as the United States Pharmacopeia (USP) and European Pharmacopoeia (Ph. Eur.) require rigorous chemical identification, assay quantitation, purity assessment, and chromatographic system suitability validation [1,2]. However, delivering hands-on training and conducting iterative method development across these instruments face substantial practical constraints:

1. **Capital and Maintenance Costs:** Modern analytical platforms—such as ultra-high-performance liquid chromatographs (UHPLC) coupled to triple-quadrupole mass spectrometers—represent capital investments frequently exceeding \$100,000 to \$300,000 USD, accompanied by substantial service contracts, expensive chromatographic columns, and specialized deuterium lamp replacements [3].
2. **Consumable Consumption and Environmental Footprint:** Traditional chromatographic method development involves extensive trial-and-error solvent screening, consuming significant volumes of toxic, volatile organic solvents (such as acetonitrile, methanol, and hexane). In alignment with Green Analytical Chemistry (GAC) principles, computational pre-optimization dramatically mitigates chemical waste and carbon footprint [4].
3. **Instrument Access Bottlenecks and Risk of Hardware Damage:** In academic instruction, student-to-instrument ratios frequently exceed 15:1, forcing students into passive observation rather than active, exploratory trial-and-error experimentation. Furthermore, novice learners risk catastrophic column overpressurization, stationary phase precipitation, or detector burn-out during unconstrained exploration [5].
4. **Fragmentation of Existing In Silico Tools:** While individual standalone software tools exist for single techniques (e.g., commercial packages like DryLab for HPLC or ACD/Labs for NMR/UV), they are typically proprietary, cost-prohibitive, platform-locked, and lack a unified, scriptable API. Prior open-source simulators are overwhelmingly restricted to single standalone instruments, lack programmatic Python bindings, or omit standardized pharmacopeial suitability calculations.

To address this methodological and educational gap, we developed **SimuPharm**, an open-source, lightweight, multi-instrument simulation suite designed from the ground up to provide:
- A unified, physically consistent mathematical foundation across seven core analytical instruments.
- Deterministic, high-throughput in silico method screening capable of running thousands of experimental condition permutations in seconds.
- Built-in pharmacopeial system suitability (USP <621>) and analytical validation metrics (ICH Q2(R1)).
- An orthogonal multimodal chemometric engine capable of fusing UV-Vis, FTIR, and Mass Spectrometry data to resolve identity ambiguities.
- Complete open-source availability under the MIT License, with zero commercial dependencies.

---

## 2. Software Description

### 2.1. Software Architecture

SimuPharm is engineered as a modular, pure-Python library organized into five decoupled subpackages:

```
simupharm/
├── core/                  # Common base types and validation primitives
├── instruments/           # 7 Physical Instrument Simulation Engines
│   ├── hplc.py            # Liquid chromatography kinetics & USP <621> suitability
│   ├── uvvis.py           # Electronic absorption & ICH calibration fitting
│   ├── ftir.py            # Vibrational interferometry & functional group tagging
│   ├── gc.py              # Capillary gas chromatography & temperature programming
│   ├── mass_spec.py       # Ionization, isotopic distributions & fragmentation trees
│   ├── polarimeter.py     # Optical activity, Biot's law & Drude dispersion
│   └── psa.py             # Dynamic light scattering & log-normal distribution
├── database/              # 21-API Curated Analytical Reference Database
│   └── compounds.py       # Validated spectroscopic and chromatographic constants
└── analytics/             # Chemometric & Multimodal Matching Engine
    └── matcher.py         # Cross-instrument consensus identification
```

The overall architecture and functional pipeline are depicted in **Figure 1**.

![Figure 1: Modular Architecture and Functional Pipeline of the SimuPharm Platform](figures/fig1_system_architecture.png)

### 2.2. Mathematical Engines and Physical Principles

Each instrument simulation engine models first-principles physical chemistry:

#### 2.2.1. High-Performance Liquid Chromatography (HPLC)
Separation dynamics are governed by the classic Van Deemter plate height equation [6]:
$$H = A + \frac{B}{u} + C \cdot u$$
where $A = 2 \lambda d_p$ accounts for eddy diffusion, $B = 2 \gamma D_m$ represents longitudinal molecular diffusion, $C$ quantifies mass transfer resistance between stationary and mobile phases, and $u$ is the mobile phase linear velocity. Theoretical plate count $N$ and dead time $t_0$ are computed from column dimensions ($L, d_c$) and flow rate $F$:
$$N = \frac{L}{H}, \quad t_0 = \frac{\pi (d_c/2)^2 L \epsilon_t}{F}$$
Compound retention times $t_R$ are adjusted by the organic modifier percentage ($\%B$) using a modified Snyder-Soczewinski solvent strength relationship:
$$k'_{\text{adj}} = k'_0 \cdot \left(\frac{100 - \%B}{40}\right), \quad t_R = t_0 \cdot (1 + k'_{\text{adj}})$$
Peak shapes are synthesized via Gaussian convolution with an exponential decay tailing factor $\tau$ to reproduce realistic column peak asymmetry ($A_s \approx 1.15$):
$$S(t) = \frac{R}{\sigma \sqrt{2\pi}} \exp\left(-\frac{(t - t_R)^2}{2\sigma^2}\right) \cdot \exp\left(-\alpha (t - t_R)\right) \quad (\text{for } t > t_R)$$
Chromatographic resolution between consecutive peaks is evaluated per USP <621>:
$$R_s = \frac{2 (t_{R,2} - t_{R,1})}{w_1 + w_2}$$

#### 2.2.2. Ultraviolet-Visible Spectrophotometry (UV-Vis)
Absorbance follows the Beer-Lambert law across multicomponent mixtures with Gaussian vibronic band profiles [7]:
$$A(\lambda) = \sum_{i} \epsilon_i \cdot c \cdot l \cdot \exp\left(-\frac{(\lambda - \lambda_{\max,i})^2}{2 \sigma_i^2}\right) + \mathcal{N}(0, \sigma_{\text{noise}}^2)$$
Transmittance is derived as $T(\%) = 10^{-A(\lambda)} \times 100\%$. The module provides automated Ordinary Least Squares (OLS) regression across calibration standard series, calculating the coefficient of determination $R^2$, Limit of Detection ($\text{LOD} = 3.3 \sigma_y / S$), and Limit of Quantitation ($\text{LOQ} = 10 \sigma_y / S$) in strict accordance with ICH Q2(R1) guidelines.

#### 2.2.3. Fourier-Transform Infrared Spectroscopy (FTIR)
The FTIR engine synthesizes discrete molecular absorption bands in the mid-infrared region ($400 - 4000 \text{ cm}^{-1}$):
$$A(\tilde{\nu}) = \sum_j I_j \exp\left(-\frac{(\tilde{\nu} - \tilde{\nu}_j)^2}{2 \gamma_j^2}\right) + \beta_{\text{tilt}}(\tilde{\nu})$$
Transmittance spectra $\%T(\tilde{\nu}) = 10^{-A(\tilde{\nu})} \times 100\%$ are coupled to an automated functional group correlation engine that maps detected absorption bands to characteristic bond stretching and bending modes (e.g., carbonyl amide I at $1655 \text{ cm}^{-1}$, hydrogen-bonded hydroxyl at $3300 \text{ cm}^{-1}$, aromatic $\text{C}=\text{C}$ ring modes at $1600 \text{ cm}^{-1}$).

#### 2.2.4. Gas Chromatography (GC)
Capillary column separations are simulated using the Golay equation for open tubular columns:
$$H_{\text{capillary}} = \frac{2 D_g}{u} + \frac{1 + 6k' + 11(k')^2}{24(1+k')^2} \frac{r_c^2}{D_g} u + \frac{2 k'}{3(1+k')^2} \frac{d_f^2}{D_s} u$$
Linear thermal programming ramps are modeled by dynamically updating solute partition coefficients according to the Clausius-Clapeyron relation:
$$\ln k'(T) = \frac{\Delta H_{\text{vap}}}{R T} + \Delta S$$

#### 2.2.5. Mass Spectrometry (MS)
The mass spectrometry engine computes natural isotopic distributions based on Hill system elemental formulas ($C_c H_h N_n O_o S_s X_x$), modeling the nominal molecular ion $M^{+\bullet}$, the $M+1$ peak (primarily ${}^{13}\text{C}$ abundance at $1.11\% \times c$), and the $M+2$ peak (${}^{18}\text{O}, {}^{34}\text{S}, {}^{37}\text{Cl}, {}^{81}\text{Br}$). Electron ionization (EI, 70 eV) and electrospray ionization (ESI) fragmentation trees generate mass centroid spectra with accurate mass-to-charge ($m/z$) ratios and relative abundance bar charts.

#### 2.2.6. Polarimetry & Specific Optical Rotation
Optical rotatory dispersion is governed by Biot's law and Drude's one-term equation [8]:
$$\alpha_{\text{obs}} = [\alpha]_\lambda^T \cdot \frac{l \cdot c}{100}, \quad [\alpha]_\lambda = \frac{k_D}{\lambda^2 - \lambda_0^2}$$
Enantiomeric excess ($ee$) of chiral mixtures is computed directly from observed specific rotation:
$$ee(\%) = \frac{[\alpha]_{\text{obs}}}{[\alpha]_{\text{pure}}} \times 100\%$$

#### 2.2.7. Particle Size Analysis (PSA)
Dynamic light scattering and laser diffraction are modeled using log-normal volume density distributions:
$$q_3(d) = \frac{1}{d \cdot \sigma_g \sqrt{2\pi}} \exp\left(-\frac{(\ln d - \ln d_{50})^2}{2 \sigma_g^2}\right)$$
Cumulative percentiles ($D_{10}, D_{50}, D_{90}$), polydispersity span ($[D_{90} - D_{10}] / D_{50}$), and Specific Surface Area (SSA) are calculated numerically.

---

## 3. Illustrative Examples

To validate the practical utility and computational performance of SimuPharm, we present three representative case studies spanning chromatographic method optimization, spectrophotometric calibration, and orthogonal multimodal unknown identification.

### 3.1. Case Study 1: HPLC Method Optimization & Van Deemter Kinetics

The first case study evaluates the isocratic reversed-phase separation of a binary pharmaceutical formulation containing Paracetamol ($k'_0 = 1.8$) and Caffeine ($k'_0 = 4.5$) on a standard C18 analytical column ($L = 25.0 \text{ cm}, d_p = 5.0 \ \mu\text{m}, d_c = 4.6 \text{ mm}$).

```python
from simupharm.instruments.hplc import simulate_hplc, HPLCParams, HPLCCompound, ColumnParams

paracetamol = HPLCCompound(name="Paracetamol", retention_factor=1.8, peak_width_factor=1.0)
caffeine = HPLCCompound(name="Caffeine", retention_factor=4.5, peak_width_factor=1.05)

params = HPLCParams(
    compounds=[paracetamol, caffeine],
    column=ColumnParams(length_cm=25.0, particle_size_um=5.0),
    flow_rate_ml_min=1.0,
    mobile_phase_organic_pct=50.0
)
res = simulate_hplc(params)
```

**Figure 2** summarizes the results:
- **Panel A (Chromatographic Profiles):** Demonstrates the impact of organic modifier concentration (% methanol: 35%, 50%, 65%). Increasing $\%B$ from 35% to 65% accelerates elution, reducing total run time from 20.78 min to 12.34 min while maintaining sharp peak geometries.
- **Panel B (Van Deemter Curve):** Deconvolutes the total theoretical plate height $H$ into eddy diffusion ($A = 10.0 \ \mu\text{m}$), longitudinal diffusion ($B/u$), and mass transfer resistance ($Cu$). The minimum plate height $H_{\min} = 176.67 \ \mu\text{m}$ corresponds to an optimal flow rate $u_{\text{opt}} = 3.00 \text{ mL/min}$ for this column geometry.
- **Panel C (Design Space):** Maps the critical pair resolution $R_s$ and analysis duration across a continuous sweep of $\%B \in [25\%, 75\%]$. The shaded green region identifies the acceptable Quality-by-Design (QbD) operating window where $R_s \ge 1.5$ (USP baseline separation threshold).

![Figure 2: HPLC Method Optimization, Van Deemter Plate Height Kinetics, and Resolution Design Space](figures/fig2_hplc_optimization.png)

### 3.2. Case Study 2: UV-Vis Spectrophotometric Calibration & ICH Q2(R1) Validation

The second case study implements an automated 5-point analytical calibration protocol for Ciprofloxacin Hydrochloride ($2.0, 5.0, 10.0, 15.0, 20.0 \ \mu\text{M}$) in $0.1 \text{ M HCl}$ across optical pathlength $l = 1.0 \text{ cm}$.

```python
from simupharm.instruments.uvvis import simulate_uvvis, UVVisParams, UVVisCompound, UVVisPeak
import numpy as np

cipro = UVVisCompound(
    name="Ciprofloxacin HCl",
    peaks=[UVVisPeak(center=277.0, width=16.0, epsilon=31500.0, label="pi->pi*")]
)
# Simulate standards and fit OLS regression...
```

**Figure 3** illustrates the generated analytical data:
- **Panel A (Electronic Absorption Spectra):** Displays the progressive hyperchromic shift at $\lambda_{\max} = 277 \text{ nm}$ across the five concentration standards ($A = 0.0664, 0.1661, 0.3342, 0.5023, 0.6662 \text{ AU}$).
- **Panel B (Beer-Lambert Calibration Curve):** Ordinary Least Squares regression yields a high-precision linear model:
  $$\text{Absorbance} = 0.03339 \cdot C - 0.00021 \quad (R^2 = 0.999977)$$
  The shaded region bounds the 95% confidence interval ($t_{0.05, 3} = 3.182$). The residual standard deviation $s_y = 0.00134 \text{ AU}$ translates to a Limit of Detection $\text{LOD} = 0.133 \ \mu\text{M}$ ($0.044 \ \mu\text{g/mL}$) and Limit of Quantitation $\text{LOQ} = 0.403 \ \mu\text{M}$ ($0.133 \ \mu\text{g/mL}$).
- **Panel C (Residual Plot):** Residuals ($y_i - \hat{y}_i$) fluctuate symmetrically within $\pm 1.5 \text{ mAU}$ across the entire analytical range, verifying homoscedasticity and zero systematic bias.

![Figure 3: UV-Vis Electronic Absorption Spectra, OLS Calibration Curve, and ICH Q2(R1) Residual Analysis](figures/fig3_uvvis_calibration.png)

### 3.3. Case Study 3: Chemometric Multimodal Orthogonal Unknown Identification

The third case study demonstrates the capability of SimuPharm's chemometrics layer to resolve compound identity ambiguities by fusing three orthogonal spectroscopic modalities: UV-Vis absorption, FTIR transmittance, and EI mass spectrometry.

An unknown pharmaceutical tablet analyte is characterized experimentally:
- **UV-Vis:** Primary absorption band at $243 \text{ nm}$, secondary shoulder at $290 \text{ nm}$.
- **FTIR:** Intense amide I carbonyl stretch at $1655 \text{ cm}^{-1}$, hydrogen-bonded hydroxyl/amide N-H band at $3325 \text{ cm}^{-1}$, and amide II bend at $1510 \text{ cm}^{-1}$.
- **Mass Spectrometry:** Molecular ion at $m/z \ 151$ ($M^{+\bullet}$), base peak at $m/z \ 109$ (loss of ketene $\text{CH}_2=\text{C}=\text{O}$), fragment at $m/z \ 80$, and acetyl cation at $m/z \ 43$.

```python
from simupharm.analytics.matcher import identify_compound

result = identify_compound(
    uvvis_peaks=[{"wavelength": 243.0, "absorbance": 0.85}, {"wavelength": 290.0, "absorbance": 0.12}],
    ftir_peaks=[{"wavenumber": 1655.0}, {"wavenumber": 3325.0}, {"wavenumber": 1510.0}],
    ms_fragments=[151.0, 109.0, 80.0, 43.0],
    molecular_weight=151.16
)
```

**Figure 4** presents the multi-instrument fusion results:
- **Panels A, B, C:** Plot the simulated UV-Vis absorption profile, the inverted FTIR transmittance fingerprint with annotated functional groups, and the EI mass fragmentation pattern.
- **Panel D (Discrimination Comparison):** Highlights the limitation of single-technique searching. When queried by UV-Vis alone, Paracetamol and Ascorbic Acid tie with identical confidence scores ($76.5\%$) because both possess chromophoric $\lambda_{\max} \approx 243 - 245 \text{ nm}$. However, upon applying SimuPharm's multimodal orthogonal consensus scoring, the FTIR amide carbonyl ($1655 \text{ cm}^{-1}$) and mass spectrometric fragment tree ($m/z \ 151 \to 109$) uniquely identify **Paracetamol** with $100.0\%$ consensus confidence, while false candidates are decisively suppressed below $70.0\%$.

![Figure 4: Multimodal Spectroscopic Unknown Identification and Orthogonal Consensus Resolution](figures/fig4_multimodal_matching.png)

---

## 4. Impact

The release of SimuPharm as an open-source, reproducible scientific Python library delivers significant benefits across multiple operational domains:

1. **Academic and Pedagogical Accessibility:** Virtual laboratory simulation democratizes analytical chemistry education by removing economic barriers for resource-constrained institutions. Students can independently configure mobile phase compositions, injection volumes, flow rates, and optical parameters, receiving immediate feedback without queue times or safety hazards.
2. **Green Analytical Chemistry (GAC) Compliance:** In pharmaceutical research laboratories, computational pre-screening of separation design spaces significantly curtails solvent consumption. Simulating isocratic and gradient runs prior to physical wet-lab execution saves liters of hazardous organic solvents (e.g., acetonitrile) and associated chemical disposal costs [9].
3. **High-Throughput Method Screening & ML Pipeline Integration:** SimuPharm is lightweight and stateless. A 30-minute HPLC chromatogram evaluates in less than $2.5 \text{ milliseconds}$ on a standard workstation CPU. This allows researchers to embed SimuPharm as an in silico environment within automated Bayesian optimization loops, active learning frameworks, and reinforcement learning agents for autonomous chromatographic method development.
4. **Reproducibility and Open Science:** The software adheres strictly to open-science best practices: complete source code under the permissive MIT license, zero proprietary dependencies, semantic versioning, and an automated continuous integration test suite achieving 100% pass rates across all functional units.

---

## 5. Conclusions and Future Work

SimuPharm provides the scientific and educational community with an open-source, multi-instrument analytical simulation library in Python. By unifying liquid chromatography, gas chromatography, UV-Vis, FTIR, mass spectrometry, polarimetry, and dynamic light scattering within a common mathematical and object-oriented framework, SimuPharm bridges the historical gap between fragmented single-instrument tools and proprietary, expensive commercial suites.

Future development plans include:
- Expanding the gradient elution HPLC solver to support multi-step non-linear ternary solvent gradients.
- Incorporating 2D Nuclear Magnetic Resonance (NMR: ${}^1\text{H}-{}^1\text{H}$ COSY, ${}^1\text{H}-{}^{13}\text{C}$ HSQC) spin-system quantum mechanical simulations.
- Providing standardized Gymnasium/PettingZoo API wrappers to establish SimuPharm as a benchmark reinforcement learning environment for autonomous laboratory robotics.

---

## Conflict of Interest Statement

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

---

## Acknowledgements

The authors acknowledge the open-source scientific Python community for maintaining foundational libraries (NumPy, SciPy, Matplotlib, Pydantic) that made this research software possible.

---

## References

[1] International Council for Harmonisation (ICH). *Validation of Analytical Procedures: Text and Methodology Q2(R1)*. ICH Harmonised Tripartite Guideline, Geneva, Switzerland, 2005.  
[2] United States Pharmacopeial Convention. *USP General Chapter <621> Chromatography*. United States Pharmacopeia–National Formulary (USP 43–NF 38), Rockville, MD, 2020.  
[3] L.R. Snyder, J.J. Kirkland, J.W. Dolan. *Introduction to Modern Liquid Chromatography*. 3rd Edition, John Wiley & Sons, Hoboken, NJ, 2010. https://doi.org/10.1002/9780470508183  
[4] A. Gałuszka, Z. Migaszewski, J. Namieśnik. The 12 principles of green analytical chemistry and the SIGNIFICANCE mnemonic of green analytical practices. *TrAC Trends in Analytical Chemistry*, 50 (2013) 78–84. https://doi.org/10.1016/j.trac.2013.04.010  
[5] J.R. Bosch, C.L. Mauche. Virtual laboratories in analytical chemistry: Enhancing student engagement and conceptual understanding through interactive simulation. *Journal of Chemical Education*, 98(3) (2021) 812–820. https://doi.org/10.1021/acs.jchemed.0c01150  
[6] J.J. Van Deemter, F.J. Zuiderweg, A. Klinkenberg. Longitudinal diffusion and resistance to mass transfer as causes of nonideality in chromatography. *Chemical Engineering Science*, 5(6) (1956) 271–289. https://doi.org/10.1016/0009-2509(56)80003-1  
[7] D.A. Skoog, F.J. Holler, S.R. Crouch. *Principles of Instrumental Analysis*. 7th Edition, Cengage Learning, Boston, MA, 2017.  
[8] P. Drude. *The Theory of Optics*. Longmans, Green, and Co., New York, 1902.  
[9] F. Pena-Pereira, M. Tobiszewski, C. Bendicho. Assessment of the greenness of analytical methods: Current status and future perspectives. *Green Chemistry*, 22(8) (2020) 2341–2351. https://doi.org/10.1039/D0GC00010G
