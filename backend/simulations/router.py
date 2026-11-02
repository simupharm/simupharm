"""Simulations Router — All instrument simulation and ML identification endpoints.

Extracted from main.py for clean separation of concerns.
All endpoints are prefixed with /api/v1/simulate and /api/v1/analyze.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Science engines
from ..science.uvvis import generate_spectrum as uvvis_spectrum, calibration_curve as uvvis_calibration
from ..science.ftir import generate_ftir_spectrum
from ..science.hplc import simulate_hplc, HPLCParams
from ..science.gc import simulate_gc, GCParams
from ..science.mass_spec import simulate_mass_spec, MassSpecParams, MassSpecCompound
from ..science.polarimeter import calculate_rotation, PolarimetryCompound, PolarimetryParams
from ..science.psa import simulate_psa, PSAParams

# Compound database
from ..compounds.database import get_compound

# ML Analyzer
from ..analytics.ml_analyzer import identify_compound, match_uvvis, match_ftir, match_mass_spec

router = APIRouter(tags=["Simulation"])


# ========================================================================
# SIMULATION ENDPOINTS — Real Scientific Computing
# ========================================================================

# ---- UV-Vis ----
class UVVisRequest(BaseModel):
    compound_id: str = ""
    peaks: list[dict] = []         # Override with custom peaks
    concentration: float = 0.001   # mol/L
    path_length: float = 1.0       # cm
    wl_start: float = 200.0
    wl_end: float = 800.0


@router.post("/simulate/uvvis")
def simulate_uvvis(req: UVVisRequest):
    """Generate a UV-Vis spectrum using Beer-Lambert Law + Gaussian peaks."""
    peaks = req.peaks
    compound_name = "Custom"
    solvent = "water"

    if req.compound_id:
        compound = get_compound(req.compound_id)
        if not compound:
            raise HTTPException(status_code=404, detail=f"Compound '{req.compound_id}' not found")
        uv_data = compound.get("uvvis", {})
        peaks = uv_data.get("peaks", [])
        compound_name = compound["name"]
        solvent = uv_data.get("solvent", "water")

    if not peaks:
        raise HTTPException(status_code=400, detail="No UV-Vis peaks defined")

    result = uvvis_spectrum(
        peaks=peaks,
        concentration=req.concentration,
        path_length=req.path_length,
        wl_start=req.wl_start,
        wl_end=req.wl_end
    )
    result.compound = compound_name
    result.solvent = solvent
    return result


class CalibrationRequest(BaseModel):
    compound_id: str
    wavelength: float = 0.0         # 0 = auto (λmax)
    concentrations: list[float] = [0.0001, 0.0005, 0.001, 0.005, 0.01]
    path_length: float = 1.0


@router.post("/simulate/uvvis/calibration")
def simulate_calibration(req: CalibrationRequest):
    """Generate a Beer-Lambert calibration curve with R² analysis."""
    compound = get_compound(req.compound_id)
    if not compound:
        raise HTTPException(status_code=404, detail=f"Compound '{req.compound_id}' not found")

    peaks = compound.get("uvvis", {}).get("peaks", [])
    if not peaks:
        raise HTTPException(status_code=400, detail="No UV-Vis data for this compound")

    # Auto-select wavelength (λmax = highest ε peak)
    wavelength = req.wavelength
    if wavelength == 0:
        wavelength = max(peaks, key=lambda p: p["epsilon"])["center"]

    return uvvis_calibration(
        peaks=peaks,
        wavelength=wavelength,
        concentrations=req.concentrations,
        path_length=req.path_length
    )


# ---- FTIR ----
class FTIRRequest(BaseModel):
    compound_id: str = ""
    peaks: list[dict] = []


@router.post("/simulate/ftir")
def simulate_ftir(req: FTIRRequest):
    """Generate an FTIR spectrum with functional group identification."""
    peaks = req.peaks
    compound_name = "Custom"

    if req.compound_id:
        compound = get_compound(req.compound_id)
        if not compound:
            raise HTTPException(status_code=404, detail=f"Compound '{req.compound_id}' not found")
        peaks = compound.get("ftir", {}).get("peaks", [])
        compound_name = compound["name"]

    if not peaks:
        raise HTTPException(status_code=400, detail="No FTIR peaks defined")

    result = generate_ftir_spectrum(peaks)
    return {"compound": compound_name, **result.model_dump()}


# ---- HPLC ----
@router.post("/simulate/hplc")
def simulate_hplc_endpoint(params: HPLCParams):
    """Simulate an HPLC chromatogram with Van Deemter plate theory."""
    return simulate_hplc(params)


# ---- GC ----
@router.post("/simulate/gc")
def simulate_gc_endpoint(params: GCParams):
    """Simulate a GC chromatogram with temperature programming."""
    return simulate_gc(params)


# ---- Mass Spectrometry ----
@router.post("/simulate/mass-spec")
def simulate_mass_spec_endpoint(params: MassSpecParams):
    """Generate a mass spectrum with fragmentation and isotope pattern."""
    return simulate_mass_spec(params)


class MassSpecFromDB(BaseModel):
    compound_id: str
    ionization_mode: str = "EI"


@router.post("/simulate/mass-spec/compound")
def simulate_mass_spec_from_db(req: MassSpecFromDB):
    """Generate a mass spectrum for a compound from the database."""
    compound = get_compound(req.compound_id)
    if not compound:
        raise HTTPException(status_code=404, detail=f"Compound '{req.compound_id}' not found")

    ms_data = compound.get("mass_spec", {})
    params = MassSpecParams(
        compound=MassSpecCompound(
            name=compound["name"],
            molecular_weight=compound["molecular_weight"],
            formula=compound.get("formula", ""),
            fragments=ms_data.get("fragments", [])
        ),
        ionization_mode=req.ionization_mode
    )
    return simulate_mass_spec(params)


# ---- Polarimeter ----
class PolarimeterRequest(BaseModel):
    compound_id: str = ""
    specific_rotation: float = 0.0
    concentration: float = 0.1      # g/mL
    path_length: float = 1.0        # dm
    temperature: float = 20.0       # °C
    wavelength: float = 589.3       # nm


@router.post("/simulate/polarimeter")
def simulate_polarimeter(req: PolarimeterRequest):
    """Calculate optical rotation with temperature/wavelength corrections."""
    specific_rotation = req.specific_rotation

    if req.compound_id:
        compound = get_compound(req.compound_id)
        if not compound:
            raise HTTPException(status_code=404, detail=f"Compound '{req.compound_id}' not found")
        pol_data = compound.get("polarimetry", {})
        specific_rotation = pol_data.get("specific_rotation", 0)

    return calculate_rotation(
        specific_rotation=specific_rotation,
        concentration=req.concentration,
        path_length=req.path_length,
        temperature=req.temperature,
        wavelength=req.wavelength
    )


# ---- PSA ----
@router.post("/simulate/psa")
def simulate_psa_endpoint(params: PSAParams):
    """Simulate a particle size distribution analysis."""
    return simulate_psa(params)


# ========================================================================
# ML IDENTIFICATION — Multi-instrument Compound Identification
# ========================================================================

class IdentifyRequest(BaseModel):
    uvvis_peaks: list[dict] | None = None       # [{wavelength, absorbance}]
    ftir_peaks: list[dict] | None = None        # [{wavenumber}]
    ms_fragments: list[dict] | None = None      # [{mz, intensity}]
    molecular_weight: float = 0


@router.post("/analyze/identify")
def identify_unknown(req: IdentifyRequest):
    """Identify an unknown compound from spectral data using multi-instrument matching.

    Provide peaks from one or more instruments for best results.
    Multi-instrument submissions receive a confidence bonus.
    """
    if not req.uvvis_peaks and not req.ftir_peaks and not req.ms_fragments:
        raise HTTPException(status_code=400, detail="Provide spectral data from at least one instrument")

    return identify_compound(
        uvvis_peaks=req.uvvis_peaks,
        ftir_peaks=req.ftir_peaks,
        ms_fragments=req.ms_fragments,
        molecular_weight=req.molecular_weight
    )
