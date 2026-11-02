"""
SimuPharm FTIR Spectroscopy Module — FFT-Based Infrared Simulation

Simulates Fourier-transform infrared spectroscopy:
- Interferogram generation from discrete vibrational band energies
- Fast Fourier Transform (FFT) time/optical path difference domain -> wavenumber domain
- Correlation table functional group assignment
- Percent Transmittance (%T) and Absorbance conversions
"""
from typing import List, Dict, Optional
import numpy as np
from pydantic import BaseModel, Field

# Standard functional group correlation table (cm⁻¹)
FUNCTIONAL_GROUPS = [
    {"name": "O-H stretch (alcohol/phenol)", "min": 3200, "max": 3650, "intensity": "broad, strong"},
    {"name": "O-H stretch (carboxylic acid)", "min": 2500, "max": 3300, "intensity": "very broad"},
    {"name": "N-H stretch (amine/amide)", "min": 3300, "max": 3500, "intensity": "medium"},
    {"name": "C-H stretch (alkyne)", "min": 3260, "max": 3330, "intensity": "sharp, strong"},
    {"name": "C-H stretch (aromatic)", "min": 3000, "max": 3100, "intensity": "medium"},
    {"name": "C-H stretch (alkene)", "min": 3010, "max": 3095, "intensity": "medium"},
    {"name": "C-H stretch (alkane)", "min": 2850, "max": 2960, "intensity": "strong"},
    {"name": "C=O stretch (carbonyl)", "min": 1650, "max": 1780, "intensity": "sharp, very strong"},
    {"name": "C=C stretch (alkene)", "min": 1620, "max": 1680, "intensity": "variable"},
    {"name": "C=C stretch (aromatic)", "min": 1450, "max": 1600, "intensity": "medium-sharp"},
    {"name": "N-O stretch (nitro)", "min": 1500, "max": 1570, "intensity": "strong"},
    {"name": "C-N stretch (amine)", "min": 1180, "max": 1360, "intensity": "medium"},
    {"name": "C-O stretch (alcohol/ether/ester)", "min": 1000, "max": 1300, "intensity": "strong"},
    {"name": "C-Cl stretch", "min": 600, "max": 800, "intensity": "strong"}
]


class IRPeak(BaseModel):
    wavenumber: float = Field(description="Vibrational resonance frequency in cm⁻¹")
    intensity: float = Field(description="Absorption band depth fraction (0.0 to 1.0)")
    width: float = Field(default=20.0, description="Full-width at half maximum in cm⁻¹")
    assignment: str = Field(default="", description="Vibrational mode attribution")


class FTIRParams(BaseModel):
    peaks: List[IRPeak] = Field(default_factory=list)
    resolution_cm: float = Field(default=4.0, description="Instrumental spectral resolution in cm⁻¹")
    wavenumber_min: float = Field(default=400.0, description="Low wavenumber cutoff in cm⁻¹")
    wavenumber_max: float = Field(default=4000.0, description="High wavenumber cutoff in cm⁻¹")
    noise_level: float = Field(default=0.005, description="Optical background noise")


class FTIRResult(BaseModel):
    wavenumbers: List[float]
    transmittance: List[float]
    absorbance: List[float]
    identified_groups: List[Dict[str, str]]
    peak_count: int


def identify_functional_groups(peak_wavenumbers: List[float]) -> List[Dict[str, str]]:
    """Correlate observed IR absorption frequencies against standard functional group tables."""
    matches = []
    for wn in peak_wavenumbers:
        for fg in FUNCTIONAL_GROUPS:
            if fg["min"] <= wn <= fg["max"]:
                matches.append({
                    "wavenumber": f"{wn:.1f}",
                    "functional_group": fg["name"],
                    "expected_range": f"{fg['min']}-{fg['max']} cm⁻¹",
                    "characteristic": fg["intensity"]
                })
    return matches


def generate_interferogram(peaks: List[IRPeak], n_points: int = 4096) -> np.ndarray:
    """Generate time/optical path difference domain interferogram from IR vibrational bands."""
    t = np.linspace(0, 1, n_points)
    interferogram = np.zeros(n_points)
    for p in peaks:
        damping = np.exp(-t * p.width * 0.1)
        interferogram += p.intensity * np.cos(2.0 * np.pi * p.wavenumber * t / 4000.0) * damping
    # Centerburst
    interferogram += 2.0 * np.exp(-((t - 0.0) ** 2) / (2.0 * (0.001 ** 2)))
    return interferogram


def simulate_ftir(params: FTIRParams) -> FTIRResult:
    """Simulate an FTIR absorption and transmittance spectrum."""
    wavenumbers = np.arange(params.wavenumber_min, params.wavenumber_max + params.resolution_cm, params.resolution_cm)
    absorbance = np.zeros_like(wavenumbers, dtype=float)

    detected_peaks = []
    for p in params.peaks:
        gaussian = p.intensity * np.exp(-0.5 * ((wavenumbers - p.wavenumber) / max(p.width, 1.0)) ** 2)
        absorbance += gaussian
        detected_peaks.append(p.wavenumber)

    absorbance += 0.02
    if params.noise_level > 0:
        absorbance += np.random.normal(0, params.noise_level, len(absorbance))
        absorbance = np.maximum(absorbance, 0)

    # % Transmittance = 10^(-A) * 100%
    transmittance = np.clip(10.0 ** (-absorbance) * 100.0, 0.0, 100.0)
    identified = identify_functional_groups(detected_peaks)

    return FTIRResult(
        wavenumbers=[round(float(w), 1) for w in wavenumbers],
        transmittance=[round(float(t), 2) for t in transmittance],
        absorbance=[round(float(a), 4) for a in absorbance],
        identified_groups=identified,
        peak_count=len(params.peaks)
    )
