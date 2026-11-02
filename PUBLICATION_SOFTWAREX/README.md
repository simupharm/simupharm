# SimuPharm: Multi-Instrument Analytical & Spectroscopic Simulation Engine

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/simupharm/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Build & Tests](https://img.shields.io/badge/tests-15%20passed%20(100%25)-brightgreen.svg)](tests/)

**SimuPharm** is a high-performance, open-source Python library designed to simulate seven major analytical chemistry instruments used in pharmaceutical quality control, academic instruction, and automated method development.

---

## Key Instruments Supported

1. **HPLC (High-Performance Liquid Chromatography)**: Van Deemter plate height kinetics, dead-time adjustments, capacity factors, peak tailing asymmetry, and USP <621> suitability calculations.
2. **UV-Vis Spectrophotometry**: Beer-Lambert electronic transitions, Gaussian absorption deconvolution, multicomponent mixtures, and ICH Q2(R1) calibration fitting (LOD/LOQ).
3. **FTIR Spectroscopy**: Michelson interferogram FFT synthesis, Beer absorbance to transmittance conversion, baseline tilt, and automated functional group correlation tagging.
4. **Gas Chromatography (GC)**: Golay capillary plate kinetics, multi-ramp temperature programming, carrier gas velocity, and retention index mapping.
5. **Mass Spectrometry (MS)**: Electron Ionization (EI) and Electrospray Ionization (ESI), natural isotopic abundance patterns (M, M+1, M+2), and fragmentation trees.
6. **Polarimetry**: Biot's optical rotation, Drude dispersion modeling, concentration dependence, and enantiomeric excess ($ee$) analysis.
7. **Particle Size Analysis (PSA)**: Dynamic light scattering, log-normal size distribution, D10/D50/D90 percentile calculations, span, and specific surface area (SSA).

---

## Installation

```bash
pip install simupharm
```

Or install from source:

```bash
git clone https://github.com/simupharm/simupharm.git
cd simupharm
pip install -e .
```

---

## Quickstart

```python
from simupharm.instruments.hplc import simulate_hplc, HPLCParams, HPLCCompound, ColumnParams

# Define separation target
compounds = [
    HPLCCompound(name="Paracetamol", retention_factor=1.8),
    HPLCCompound(name="Caffeine", retention_factor=4.5)
]

params = HPLCParams(
    compounds=compounds,
    column=ColumnParams(length_cm=25.0, particle_size_um=5.0),
    flow_rate_ml_min=1.0,
    mobile_phase_organic_pct=45.0
)

result = simulate_hplc(params)
for peak in result.peaks:
    print(f"{peak.compound}: tR = {peak.retention_time:.2f} min, Resolution Rs = {peak.resolution:.2f}, Plates N = {peak.plates}")
```

---

## Verification Test Suite

SimuPharm includes an extensive automated test suite covering all 7 analytical engines and multimodal chemometrics:

```bash
pytest tests/simupharm/ -v
```

---

## Citation

```bibtex
@article{simupharm2026,
  title = {SimuPharm: An Open-Source Multi-Instrument Analytical and Spectroscopic Simulation Suite for Pharmaceutical Research and Education},
  journal = {SoftwareX},
  volume = {X},
  pages = {100XXX},
  year = {2026},
  publisher = {Elsevier}
}
```

---

## License

SimuPharm is distributed under the permissive [MIT License](LICENSE).
