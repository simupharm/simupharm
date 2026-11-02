"""
SimuPharm Particle Size Analysis (PSA) Module — Distribution & Surface Area Modeling

Simulates dynamic light scattering and laser diffraction particle size distributions:
- Log-normal cumulative and density distributions
- Percentile metrics: D10, D50 (median diameter), D90
- Span calculation: (D90 - D10) / D50
- Volume-weighted mean diameter and specific surface area (SSA) modeling
"""
from typing import List
import numpy as np
from pydantic import BaseModel, Field


class PSAParams(BaseModel):
    d50_um: float = Field(default=50.0, description="Median diameter D50 in µm")
    geometric_std: float = Field(default=1.5, description="Geometric standard deviation sigma_g")
    n_bins: int = Field(default=100, description="Number of logarithmic size bins")
    size_min_um: float = Field(default=0.1, description="Minimum size boundary in µm")
    size_max_um: float = Field(default=1000.0, description="Maximum size boundary in µm")


class PSAResult(BaseModel):
    diameters: List[float]
    volume_distribution: List[float]
    cumulative_distribution: List[float]
    d10: float
    d50: float
    d90: float
    span: float
    mean_diameter: float
    surface_area_m2_g: float
    uniformity: float


def simulate_psa(params: PSAParams) -> PSAResult:
    """Simulate a particle size distribution analysis."""
    diameters = np.logspace(
        np.log10(params.size_min_um),
        np.log10(params.size_max_um),
        params.n_bins
    )

    ln_d = np.log(diameters)
    ln_d50 = np.log(params.d50_um)
    ln_sigma = np.log(params.geometric_std)

    volume_pdf = (1.0 / (diameters * ln_sigma * np.sqrt(2.0 * np.pi))) * \
                 np.exp(-0.5 * ((ln_d - ln_d50) / ln_sigma) ** 2)

    if volume_pdf.sum() > 0:
        volume_pdf = (volume_pdf / volume_pdf.sum()) * 100.0

    cumulative = np.cumsum(volume_pdf)
    if cumulative[-1] > 0:
        cumulative = (cumulative / cumulative[-1]) * 100.0

    d10 = float(np.interp(10.0, cumulative, diameters))
    d50 = float(np.interp(50.0, cumulative, diameters))
    d90 = float(np.interp(90.0, cumulative, diameters))
    d60 = float(np.interp(60.0, cumulative, diameters))

    span = (d90 - d10) / d50 if d50 > 0 else 0.0
    mean_d = float(np.sum(diameters * volume_pdf) / max(np.sum(volume_pdf), 1e-10))

    d32 = float(np.sum(volume_pdf * (diameters ** 3)) / max(np.sum(volume_pdf * (diameters ** 2)), 1e-10))
    ssa = 6.0 / (1.0 * d32 * 1e-4) if d32 > 0 else 0.0
    uniformity = d60 / d10 if d10 > 0 else 0.0

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
