"""UV-Vis Spectrophotometer — Beer-Lambert Law & Gaussian Peak Modeling

Real physics engine:
- Beer-Lambert: A = εlc
- Gaussian peak shape: A(λ) = ε × exp(-0.5 × ((λ - λmax) / σ)²)
- Multi-peak compounds with realistic absorbance profiles
- Peak detection with prominence filtering
- Calibration curve with linear regression & R² analysis
"""
import numpy as np
from pydantic import BaseModel


class UVVisPeak(BaseModel):
    center: float       # λmax in nm
    width: float        # Gaussian σ in nm
    epsilon: float      # Molar absorptivity (L/(mol·cm))
    label: str = ""     # e.g. "π→π*", "n→π*"


class UVVisCompound(BaseModel):
    name: str
    peaks: list[UVVisPeak]
    solvent: str = "water"


class SpectrumPoint(BaseModel):
    wavelength: float
    absorbance: float


class DetectedPeak(BaseModel):
    wavelength: float
    absorbance: float
    label: str = ""


class SpectrumResult(BaseModel):
    spectrum: list[SpectrumPoint]
    peaks: list[DetectedPeak]
    max_absorbance: float
    lambda_max: float
    compound: str
    concentration: float
    path_length: float
    solvent: str


class CalibrationResult(BaseModel):
    points: list[dict]      # [{concentration, absorbance}]
    slope: float
    intercept: float
    r_squared: float
    equation: str
    wavelength: float


# ---- Core Physics ----

def calculate_absorbance(
    peaks: list[dict],
    wavelength: float,
    concentration: float,
    path_length: float = 1.0
) -> float:
    """
    Beer-Lambert Law with Gaussian peak modeling.
    A = Σ (ε_i × l × c × exp(-0.5 × ((λ - λmax_i) / σ_i)²))
    """
    total_abs = 0.0
    for peak in peaks:
        gaussian = np.exp(-0.5 * ((wavelength - peak["center"]) / peak["width"]) ** 2)
        total_abs += peak["epsilon"] * path_length * concentration * gaussian
    return float(total_abs)


def generate_spectrum(
    peaks: list[dict],
    concentration: float,
    path_length: float = 1.0,
    wl_start: float = 200.0,
    wl_end: float = 800.0,
    step: float = 1.0,
    noise_level: float = 0.002
) -> SpectrumResult:
    """Generate a full UV-Vis spectrum with optional noise."""
    wavelengths = np.arange(wl_start, wl_end + step, step)
    absorbances = np.array([
        calculate_absorbance(peaks, wl, concentration, path_length)
        for wl in wavelengths
    ])

    # Add realistic noise
    if noise_level > 0:
        absorbances += np.random.normal(0, noise_level, len(absorbances))
        absorbances = np.maximum(absorbances, 0)

    # Build spectrum
    spectrum = [
        SpectrumPoint(wavelength=float(wl), absorbance=float(ab))
        for wl, ab in zip(wavelengths, absorbances)
    ]

    # Detect peaks
    detected = detect_peaks(wavelengths, absorbances, peaks)

    # Find λmax
    max_idx = int(np.argmax(absorbances))

    return SpectrumResult(
        spectrum=spectrum,
        peaks=detected,
        max_absorbance=float(absorbances[max_idx]),
        lambda_max=float(wavelengths[max_idx]),
        compound="",
        concentration=concentration,
        path_length=path_length,
        solvent=""
    )


def detect_peaks(
    wavelengths: np.ndarray,
    absorbances: np.ndarray,
    known_peaks: list[dict],
    threshold: float = 0.01
) -> list[DetectedPeak]:
    """Detect peaks using local maxima with prominence filtering."""
    from scipy.signal import find_peaks as sp_find_peaks
    indices, properties = sp_find_peaks(absorbances, prominence=threshold, distance=5)
    detected = []
    for idx in indices:
        wl = float(wavelengths[idx])
        ab = float(absorbances[idx])
        # Match to known peak label
        label = ""
        for kp in known_peaks:
            if abs(wl - kp["center"]) < kp["width"] * 1.5:
                label = kp.get("label", "")
                break
        detected.append(DetectedPeak(wavelength=wl, absorbance=ab, label=label))
    return detected


def calibration_curve(
    peaks: list[dict],
    wavelength: float,
    concentrations: list[float],
    path_length: float = 1.0
) -> CalibrationResult:
    """Generate a calibration curve (A vs c) at a specific wavelength."""
    points = []
    for c in concentrations:
        ab = calculate_absorbance(peaks, wavelength, c, path_length)
        points.append({"concentration": c, "absorbance": float(ab)})

    # Linear regression: A = slope × c + intercept
    x = np.array(concentrations)
    y = np.array([p["absorbance"] for p in points])

    if len(x) < 2:
        return CalibrationResult(
            points=points, slope=0, intercept=0, r_squared=0,
            equation="Insufficient data", wavelength=wavelength
        )

    coeffs = np.polyfit(x, y, 1)
    slope, intercept = float(coeffs[0]), float(coeffs[1])

    # R² calculation
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = float(1 - ss_res / ss_tot) if ss_tot > 0 else 1.0

    equation = f"A = {slope:.4f} × c + {intercept:.4f} (R² = {r_squared:.6f})"

    return CalibrationResult(
        points=points, slope=slope, intercept=intercept,
        r_squared=r_squared, equation=equation, wavelength=wavelength
    )
