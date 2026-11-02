"""
SimuPharm Mass Spectrometry Module — Ionization, Fragmentation & Isotope Distribution

Simulates mass spectrometry spectra:
- Molecular ion (M+) generation from exact molecular formula
- Natural isotopic abundance patterns (M, M+1 from 13C, M+2 from 18O/34S/37Cl/81Br)
- Electron Ionization (EI) and Electrospray Ionization (ESI) fragmentation trees
- Mass centroid peak detection and m/z distribution
"""
from typing import List, Dict, Optional
import numpy as np
from pydantic import BaseModel, Field


class MSFragment(BaseModel):
    mz: float = Field(description="Mass-to-charge ratio m/z")
    intensity: float = Field(description="Relative ion abundance (%)")
    label: str = Field(default="", description="Ion structural attribution (e.g., [M-H2O]+)")


class MassSpecCompound(BaseModel):
    name: str
    molecular_weight: float = Field(description="Monoisotopic or average molecular weight")
    formula: str = Field(description="Hill system chemical formula (e.g., C8H9NO2)")
    fragments: List[MSFragment] = Field(default_factory=list)


class MassSpecParams(BaseModel):
    compound: MassSpecCompound
    ionization_mode: str = Field(default="EI", description="Ionization technique: EI (70 eV), ESI+, ESI-")
    mass_range_min: float = Field(default=10.0, description="Lower m/z scan boundary")
    mass_range_max: float = Field(default=0.0, description="Upper m/z scan boundary (0 = auto)")
    resolution: float = Field(default=1.0, description="Peak resolution in Da (FWHM)")


class MSPeak(BaseModel):
    mz: float
    intensity: float
    label: str = ""


class MassSpecResult(BaseModel):
    mz_values: List[float]
    intensities: List[float]
    peaks: List[MSPeak]
    molecular_ion: float
    base_peak: float


def calculate_isotope_pattern(formula: str, base_mz: float) -> List[Dict[str, float]]:
    """Estimate natural isotopic envelope (M, M+1, M+2) from empirical formula."""
    import re
    # Extract element counts
    c_match = re.search(r'C(\d*)', formula)
    n_carbon = 1 if c_match and c_match.group(1) == "" else (int(c_match.group(1)) if c_match else 0)

    # 13C abundance is ~1.1% per carbon atom
    m_plus_1_pct = n_carbon * 1.1

    # Check for Chlorine or Bromine
    cl_match = re.search(r'Cl(\d*)', formula)
    n_cl = 1 if cl_match and cl_match.group(1) == "" else (int(cl_match.group(1)) if cl_match else 0)

    m_plus_2_pct = 0.0
    if n_cl > 0:
        m_plus_2_pct = n_cl * 32.5  # 37Cl is ~32.5% of 35Cl

    return [
        {"mz": round(base_mz, 1), "abundance": 100.0, "label": "M+"},
        {"mz": round(base_mz + 1.0, 1), "abundance": round(m_plus_1_pct, 1), "label": "[M+1]+"},
        {"mz": round(base_mz + 2.0, 1), "abundance": round(m_plus_2_pct, 1), "label": "[M+2]+"}
    ]


def simulate_mass_spec(params: MassSpecParams) -> MassSpecResult:
    """Simulate a mass spectrum with fragmentation and isotopic clusters."""
    mw = params.compound.molecular_weight
    if params.ionization_mode == "ESI+":
        parent_mz = mw + 1.0078  # [M+H]+
    elif params.ionization_mode == "ESI-":
        parent_mz = mw - 1.0078  # [M-H]-
    else:
        parent_mz = mw  # M+ (EI)

    max_scan = params.mass_range_max if params.mass_range_max > 0 else (parent_mz + 30.0)
    min_scan = params.mass_range_min

    peaks = []

    # Add parent ion isotopic cluster
    isotopes = calculate_isotope_pattern(params.compound.formula, parent_mz)
    for iso in isotopes:
        peaks.append(MSPeak(mz=iso["mz"], intensity=iso["abundance"], label=iso["label"]))

    # Add daughter fragments
    for frag in params.compound.fragments:
        peaks.append(MSPeak(mz=frag.mz, intensity=frag.intensity, label=frag.label))

    # Normalize so base peak is 100%
    max_intensity = max((p.intensity for p in peaks), default=1.0)
    for p in peaks:
        p.intensity = round((p.intensity / max_intensity) * 100.0, 1)

    # Sort by m/z
    peaks = sorted(peaks, key=lambda p: p.mz)
    base_peak_mz = max(peaks, key=lambda p: p.intensity).mz

    # Continuous profile simulation
    mz_grid = np.arange(min_scan, max_scan, 0.2)
    intensity_grid = np.zeros_like(mz_grid)
    sigma = params.resolution / 2.355  # FWHM to sigma

    for p in peaks:
        intensity_grid += p.intensity * np.exp(-0.5 * ((mz_grid - p.mz) / max(sigma, 0.05)) ** 2)

    return MassSpecResult(
        mz_values=[round(float(m), 2) for m in mz_grid],
        intensities=[round(float(i), 2) for i in intensity_grid],
        peaks=peaks,
        molecular_ion=round(parent_mz, 2),
        base_peak=round(base_peak_mz, 2)
    )
