"""Compounds Router — Search, retrieve, and get spectral data for compounds."""
from fastapi import APIRouter, Query
from .database import search_compounds, get_compound

router = APIRouter(prefix="/compounds", tags=["Compounds"])


@router.get("")
def list_compounds(q: str = Query("", description="Search query"), category: str = Query("", description="Filter by category")):
    """Search compounds by name, formula, CAS, or category."""
    results = search_compounds(query=q, category=category)
    # Return summary (without heavy spectral data)
    summary = []
    for c in results:
        summary.append({
            "id": c["id"],
            "name": c["name"],
            "category": c.get("category", ""),
            "molecular_weight": c.get("molecular_weight", 0),
            "formula": c.get("formula", ""),
            "cas": c.get("cas", ""),
            "pharmacopeia": c.get("pharmacopeia", ""),
            "therapeutic_class": c.get("therapeutic_class", "")
        })
    return {"count": len(summary), "compounds": summary}


@router.get("/{compound_id}")
def get_compound_detail(compound_id: str):
    """Get full compound data including all spectral information."""
    compound = get_compound(compound_id)
    if not compound:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Compound '{compound_id}' not found")
    return compound


@router.get("/{compound_id}/spectrum/{instrument}")
def get_spectrum_data(compound_id: str, instrument: str):
    """Get spectral data for a specific instrument (uvvis, ftir, hplc, mass_spec, polarimetry)."""
    compound = get_compound(compound_id)
    if not compound:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Compound '{compound_id}' not found")

    instrument_key = instrument.lower().replace("-", "_")
    spectral_data = compound.get(instrument_key)
    if not spectral_data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"No {instrument} data for '{compound_id}'")

    return {
        "compound_id": compound_id,
        "compound_name": compound["name"],
        "instrument": instrument,
        "data": spectral_data
    }
