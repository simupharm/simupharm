"""
SimuPharm UV-Vis Spectroscopy Module — Beer-Lambert Law & Gaussian Peak Modeling

Simulates electronic absorption spectroscopy:
- Beer-Lambert absorption: A = epsilon * l * c
- Gaussian band profiles: A(lambda) = epsilon * exp(-0.5 * ((lambda - lambda_max) / sigma)^2)
- Multi-component additive absorbance
- Analytical calibration curves with ordinary least squares (OLS) regression
- Limit of Detection (LOD) and Limit of Quantitation (LOQ) calculation
"""
from typing import List, Optional
import numpy as np
from pydantic import BaseModel, Field


class UVVisPeak(BaseModel):
    center: float = Field(description="Absorption maximum wavelength lambda_max in nm")
    width: float = Field(default=20.0, description="Gaussian spectral bandwidth sigma in nm")
    epsilon: float = Field(description="Molar absorptivity epsilon in L/(mol*cm)")
    label: str = Field(default="", description="Electronic transition assignment (e.g., pi->pi*)")


class UVVisCompound(BaseModel):
    name: str
    peaks: List[UVVisPeak]
    solvent: str = "water"


class UVVisParams(BaseModel):
    compound: Optional[UVVisCompound] = None
    concentration_molar: float = Field(default=1e-4, description="Molar concentration in mol/L")
    path_length_cm: float = Field(default=1.0, description="Cuvette optical path length in cm")
    wavelength_min: float = Field(default=200.0, description="Start wavelength in nm")
    wavelength_max: float = Field(default=800.0, description="End wavelength in nm")
    noise_level: float = Field(default=0.002, description="Photometric baseline noise standard deviation")


class CalibrationPoint(BaseModel):
    concentration: float
    absorbance: float


class CalibrationResult(BaseModel):
    slope: float
    intercept: float
    r_squared: float
    lod: float
    loq: float
    equation: str


class UVVisResult(BaseModel):
    wavelengths: List[float]
    absorbance: List[float]
    transmittance: List[float]
    lambda_max: float
    max_absorbance: float


def simulate_uvvis(params: UVVisParams) -> UVVisResult:
    """Simulate a UV-Vis electronic absorption spectrum."""
    wavelengths = np.arange(params.wavelength_min, params.wavelength_max + 1.0, 1.0)
    absorbance = np.zeros_like(wavelengths)

    if params.compound and params.compound.peaks:
        for peak in params.compound.peaks:
            # Beer-Lambert: A = epsilon * c * l
            a_peak = peak.epsilon * params.concentration_molar * params.path_length_cm
            # Gaussian spectral line shape
            gaussian = np.exp(-0.5 * ((wavelengths - peak.center) / max(peak.width, 1.0)) ** 2)
            absorbance += a_peak * gaussian

    # Add photometric noise
    if params.noise_level > 0:
        absorbance += np.random.normal(0, params.noise_level, len(absorbance))
        absorbance = np.maximum(absorbance, 0)

    # Convert to Transmittance: T = 10^(-A) * 100%
    transmittance = np.clip(10 ** (-absorbance) * 100.0, 0, 100.0)

    max_idx = int(np.argmax(absorbance))
    lambda_max = float(wavelengths[max_idx])
    max_abs = float(absorbance[max_idx])

    return UVVisResult(
        wavelengths=[float(w) for w in wavelengths],
        absorbance=[round(float(a), 5) for a in absorbance],
        transmittance=[round(float(t), 3) for t in transmittance],
        lambda_max=lambda_max,
        max_absorbance=round(max_abs, 5)
    )


def generate_calibration_curve(concentrations: List[float], peak_epsilon: float, path_length: float = 1.0, noise: float = 0.002) -> CalibrationResult:
    """Generate and fit a linear calibration curve using Ordinary Least Squares."""
    c_arr = np.array(concentrations)
    # Theoretical absorbance with noise
    a_arr = peak_epsilon * c_arr * path_length + np.random.normal(0, noise, len(c_arr))
    a_arr = np.maximum(a_arr, 0)

    # OLS Regression
    slope, intercept = np.polyfit(c_arr, a_arr, 1)
    y_pred = slope * c_arr + intercept
    ss_tot = np.sum((a_arr - np.mean(a_arr)) ** 2)
    ss_res = np.sum((a_arr - y_pred) ** 2)
    r2 = 1.0 - (ss_res / max(ss_tot, 1e-12))

    # Standard deviation of residuals for LOD / LOQ
    s_y = np.sqrt(np.sum(ss_res) / max(len(c_arr) - 2, 1))
    lod = float(3.3 * s_y / max(slope, 1e-12))
    loq = float(10.0 * s_y / max(slope, 1e-12))

    sign = "+" if intercept >= 0 else "-"
    eq = f"A = {slope:.2e} * C {sign} {abs(intercept):.4f}"

    return CalibrationResult(
        slope=float(slope),
        intercept=float(intercept),
        r_squared=float(r2),
        lod=lod,
        loq=loq,
        equation=eq
    )
