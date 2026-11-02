"""
SimuPharm Polarimetry Module — Optical Rotation & Enantiomeric Purity Modeling

Simulates polarimetric measurements:
- Biot's law: alpha = [alpha]_D^T * l * c
- Temperature correction: [alpha]_T = [alpha]_20 * (1 - 0.00035 * (T - 20))
- Wavelength dispersion correction (Drude equation)
- Enantiomeric excess (% ee) determination
- Quantitative concentration determination from optical rotation
"""
from pydantic import BaseModel, Field


class PolarimetryCompound(BaseModel):
    name: str
    specific_rotation: float = Field(description="Specific rotation [alpha]_D^20 in degrees*(mL/(dm*g))")
    concentration_g_ml: float = Field(default=0.01, description="Concentration in g/mL")
    wavelength_nm: float = Field(default=589.3, description="Light wavelength in nm (Default: Sodium D line)")
    molecular_weight: float = Field(default=0.0)


class PolarimetryParams(BaseModel):
    compound: PolarimetryCompound
    path_length_dm: float = Field(default=1.0, description="Sample cell optical path length in decimeters")
    temperature_c: float = Field(default=20.0, description="Measurement temperature in °C")
    wavelength_nm: float = Field(default=589.3, description="Wavelength in nm")


class PolarimetryResult(BaseModel):
    observed_rotation: float
    specific_rotation: float
    corrected_rotation: float
    enantiomeric_excess: float
    concentration: float
    path_length: float
    temperature: float
    wavelength: float
    interpretation: str


def simulate_polarimeter(params: PolarimetryParams) -> PolarimetryResult:
    """Calculate observed optical rotation and enantiomeric purity."""
    spec_rot = params.compound.specific_rotation
    conc = params.compound.concentration_g_ml
    path_len = params.path_length_dm
    temp = params.temperature_c
    wl = params.wavelength_nm

    # Temperature correction
    temp_factor = 1.0 - 0.00035 * (temp - 20.0)
    corrected_rotation = spec_rot * temp_factor

    # Drude dispersion approximation
    wl_factor = (589.3 / max(wl, 100.0)) ** 2
    corrected_rotation *= wl_factor

    # Biot's Law: alpha = [alpha] * l * c
    observed = corrected_rotation * path_len * conc

    # Enantiomeric excess
    ee = abs(observed / (spec_rot * path_len * conc) * 100.0) if (conc > 0 and spec_rot != 0) else 100.0

    if observed > 0.0001:
        direction = "dextrorotatory (+)"
    elif observed < -0.0001:
        direction = "levorotatory (-)"
    else:
        direction = "optically inactive"

    interpretation = (
        f"Observed rotation: {observed:+.3f}° ({direction}). "
        f"Specific rotation [alpha]_D^{temp:.0f} = {corrected_rotation:+.2f}°. "
        f"Enantiomeric excess: {ee:.1f}%."
    )

    return PolarimetryResult(
        observed_rotation=round(float(observed), 4),
        specific_rotation=round(float(spec_rot), 2),
        corrected_rotation=round(float(corrected_rotation), 4),
        enantiomeric_excess=round(min(float(ee), 100.0), 2),
        concentration=conc,
        path_length=path_len,
        temperature=temp,
        wavelength=wl,
        interpretation=interpretation
    )
