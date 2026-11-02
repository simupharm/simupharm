"""Polarimetry — Optical Rotation Calculation

Real physics engine:
- Specific rotation: [α]_D^T = α / (l × c)
- Temperature correction: [α]_T = [α]_20 × (1 - 0.00035 × (T - 20))
- Wavelength correction (Drude equation)
- Enantiomeric excess: ee = [α]_obs / [α]_pure × 100
- Concentration determination from rotation
"""
import numpy as np
from pydantic import BaseModel


class PolarimetryCompound(BaseModel):
    name: str
    specific_rotation: float     # [α]_D^20 in degrees
    concentration_g_ml: float    # g/mL
    wavelength_nm: float = 589.3  # Sodium D line
    molecular_weight: float = 0.0


class PolarimetryParams(BaseModel):
    compound: PolarimetryCompound
    path_length_dm: float = 1.0  # decimeters (standard)
    temperature_c: float = 20.0
    wavelength_nm: float = 589.3


class PolarimetryResult(BaseModel):
    observed_rotation: float      # α (degrees)
    specific_rotation: float      # [α]_D^T
    corrected_rotation: float     # Temperature-corrected
    enantiomeric_excess: float    # ee %
    concentration: float
    path_length: float
    temperature: float
    wavelength: float
    interpretation: str


def calculate_rotation(
    specific_rotation: float,
    concentration: float,
    path_length: float = 1.0,
    temperature: float = 20.0,
    wavelength: float = 589.3
) -> PolarimetryResult:
    """Calculate observed optical rotation and related parameters."""

    # Temperature correction: [α]_T = [α]_20 × (1 - 0.00035 × (T - 20))
    temp_factor = 1 - 0.00035 * (temperature - 20)
    corrected_rotation = specific_rotation * temp_factor

    # Wavelength correction (Drude approximation)
    # [α]_λ = [α]_D × (589.3 / λ)²
    wl_factor = (589.3 / wavelength) ** 2
    corrected_rotation *= wl_factor

    # Observed rotation: α = [α] × l × c
    observed = corrected_rotation * path_length * concentration

    # Enantiomeric excess
    ee = abs(observed / (specific_rotation * path_length * concentration) * 100) if concentration > 0 else 0

    # Interpretation
    if observed > 0:
        direction = "dextrorotatory (+)"
    elif observed < 0:
        direction = "levorotatory (-)"
    else:
        direction = "optically inactive"

    interpretation = (
        f"Observed rotation: {observed:+.3f}° ({direction}). "
        f"Specific rotation [α]_D^{temperature:.0f} = {corrected_rotation:+.2f}°. "
        f"Enantiomeric excess: {ee:.1f}%."
    )

    return PolarimetryResult(
        observed_rotation=round(observed, 4),
        specific_rotation=round(specific_rotation, 2),
        corrected_rotation=round(corrected_rotation, 4),
        enantiomeric_excess=round(min(ee, 100), 2),
        concentration=concentration,
        path_length=path_length,
        temperature=temperature,
        wavelength=wavelength,
        interpretation=interpretation
    )


def determine_concentration(
    observed_rotation: float,
    specific_rotation: float,
    path_length: float = 1.0
) -> float:
    """Calculate concentration from observed rotation: c = α / ([α] × l)."""
    if specific_rotation == 0 or path_length == 0:
        return 0.0
    return round(observed_rotation / (specific_rotation * path_length), 6)
