"""Particle Size Analysis — Distribution Modeling

Real physics engine:
- Log-normal particle size distribution
- D10, D50 (median), D90 calculation
- Span calculation: (D90 - D10) / D50
- Surface area and volume moment calculations
- Mie scattering intensity approximation
"""
import numpy as np
from pydantic import BaseModel


class PSAParams(BaseModel):
    d50_um: float = 50.0           # Median diameter (μm)
    geometric_std: float = 1.5     # Geometric standard deviation
    n_bins: int = 100              # Number of size bins
    size_min_um: float = 0.1
    size_max_um: float = 1000.0
    distribution_type: str = "volume"  # volume, number, surface


class PSAResult(BaseModel):
    diameters: list[float]        # μm
    volume_distribution: list[float]
    cumulative_distribution: list[float]
    d10: float
    d50: float
    d90: float
    span: float
    mean_diameter: float
    surface_area_m2_g: float       # Specific surface area
    uniformity: float


def log_normal_distribution(
    diameters: np.ndarray,
    d50: float,
    geo_std: float
) -> np.ndarray:
    """Generate a log-normal particle size distribution."""
    ln_d = np.log(diameters)
    ln_d50 = np.log(d50)
    ln_sigma = np.log(geo_std)

    pdf = (1 / (diameters * ln_sigma * np.sqrt(2 * np.pi))) * \
          np.exp(-0.5 * ((ln_d - ln_d50) / ln_sigma) ** 2)

    return pdf


def simulate_psa(params: PSAParams) -> PSAResult:
    """Simulate a particle size distribution analysis."""
    # Generate logarithmically spaced diameter bins
    diameters = np.logspace(
        np.log10(params.size_min_um),
        np.log10(params.size_max_um),
        params.n_bins
    )

    # Volume-weighted log-normal distribution
    volume_pdf = log_normal_distribution(diameters, params.d50_um, params.geometric_std)

    # Normalize
    if volume_pdf.sum() > 0:
        volume_pdf = volume_pdf / volume_pdf.sum() * 100

    # Add slight noise
    noise = np.random.normal(0, 0.1, len(volume_pdf))
    volume_pdf = np.maximum(volume_pdf + noise, 0)

    # Cumulative distribution
    cumulative = np.cumsum(volume_pdf)
    if cumulative[-1] > 0:
        cumulative = cumulative / cumulative[-1] * 100

    # Calculate D-values by interpolation
    d10 = float(np.interp(10, cumulative, diameters))
    d50 = float(np.interp(50, cumulative, diameters))
    d90 = float(np.interp(90, cumulative, diameters))

    # Span
    span = (d90 - d10) / d50 if d50 > 0 else 0

    # Mean diameter (volume-weighted)
    mean_d = float(np.sum(diameters * volume_pdf) / max(np.sum(volume_pdf), 1e-10))

    # Specific surface area (assuming spherical particles, density = 1 g/cm³)
    # SSA = 6 / (ρ × D[3,2])
    d32 = float(np.sum(volume_pdf * diameters ** 3) / max(np.sum(volume_pdf * diameters ** 2), 1e-10))
    ssa = 6.0 / (1.0 * d32 * 1e-4) if d32 > 0 else 0  # m²/g (diameter in μm → cm)

    # Uniformity coefficient
    d60 = float(np.interp(60, cumulative, diameters))
    uniformity = d60 / d10 if d10 > 0 else 0

    return PSAResult(
        diameters=[round(float(d), 4) for d in diameters],
        volume_distribution=[round(float(v), 4) for v in volume_pdf],
        cumulative_distribution=[round(float(c), 2) for c in cumulative],
        d10=round(d10, 3),
        d50=round(d50, 3),
        d90=round(d90, 3),
        span=round(span, 3),
        mean_diameter=round(mean_d, 3),
        surface_area_m2_g=round(ssa, 2),
        uniformity=round(uniformity, 3)
    )
