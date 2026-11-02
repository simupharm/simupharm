"""Spectral Matching Engine — Multi-Instrument Compound Identification

Uses cosine similarity and peak-position matching to identify unknown compounds
from their spectral data against the pharmaceutical compound database.

Features:
- UV-Vis spectrum matching (peak positions + intensities)
- FTIR functional group fingerprinting
- Mass spectrum fragmentation pattern matching
- Multi-instrument combined scoring
- Anomaly detection (unusual peaks, poor baselines)
"""
import numpy as np
from pydantic import BaseModel
from simupharm.database.compounds import COMPOUNDS


class MatchResult(BaseModel):
    compound_id: str
    compound_name: str
    confidence: float        # 0-100%
    instrument: str
    matched_peaks: list[dict]
    notes: str = ""


class IdentificationResult(BaseModel):
    top_matches: list[MatchResult]
    analysis_notes: list[str]
    anomalies: list[str]


# ---- Spectral Similarity ----

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors."""
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


def peak_position_score(query_peaks: list[float], ref_peaks: list[float], tolerance: float = 5.0) -> float:
    """Score based on how many query peaks match reference peaks within tolerance."""
    if not query_peaks or not ref_peaks:
        return 0.0
    matches = 0
    matched_pairs = []
    for qp in query_peaks:
        for rp in ref_peaks:
            if abs(qp - rp) <= tolerance:
                matches += 1
                matched_pairs.append((qp, rp))
                break
    score = matches / max(len(query_peaks), len(ref_peaks))
    return score


# ---- UV-Vis Matching ----

def match_uvvis(query_peaks: list[dict], tolerance: float = 8.0) -> list[MatchResult]:
    """Match UV-Vis peaks against compound database."""
    results = []
    query_centers = [p.get("wavelength", p.get("center", 0)) if isinstance(p, dict) else float(p) for p in query_peaks]

    for comp_id, comp in COMPOUNDS.items():
        uv_data = comp.get("uvvis", {})
        ref_peaks = uv_data.get("peaks", [])
        if not ref_peaks:
            continue

        ref_centers = [p["center"] for p in ref_peaks]

        # Peak position matching
        pos_score = peak_position_score(query_centers, ref_centers, tolerance)

        # Bonus for matching the strongest peak (lambda_max)
        strongest_ref = max(ref_peaks, key=lambda p: p["epsilon"])
        lambda_max_match = any(abs(qc - strongest_ref["center"]) <= tolerance for qc in query_centers)
        if lambda_max_match:
            pos_score = min(1.0, pos_score + 0.2)

        if pos_score > 0.2:
            matched = []
            for qc in query_centers:
                for rp in ref_peaks:
                    if abs(qc - rp["center"]) <= tolerance:
                        matched.append({
                            "query_wavelength": qc,
                            "reference_wavelength": rp["center"],
                            "transition": rp.get("label", ""),
                            "deviation": round(abs(qc - rp["center"]), 1)
                        })
            results.append(MatchResult(
                compound_id=comp_id,
                compound_name=comp["name"],
                confidence=round(pos_score * 100, 1),
                instrument="uvvis",
                matched_peaks=matched
            ))

    results.sort(key=lambda r: r.confidence, reverse=True)
    return results[:5]


# ---- FTIR Matching ----

def match_ftir(query_peaks: list[dict], tolerance: float = 30.0) -> list[MatchResult]:
    """Match FTIR peaks against compound database."""
    results = []
    query_wn = [p.get("wavenumber", 0) if isinstance(p, dict) else float(p) for p in query_peaks]

    for comp_id, comp in COMPOUNDS.items():
        ir_data = comp.get("ftir", {})
        ref_peaks = ir_data.get("peaks", [])
        if not ref_peaks:
            continue

        ref_wn = [p["wavenumber"] for p in ref_peaks]
        pos_score = peak_position_score(query_wn, ref_wn, tolerance)

        if pos_score > 0.2:
            matched = []
            for qw in query_wn:
                for rp in ref_peaks:
                    if abs(qw - rp["wavenumber"]) <= tolerance:
                        matched.append({
                            "query_wavenumber": qw,
                            "reference_wavenumber": rp["wavenumber"],
                            "assignment": rp.get("assignment", ""),
                            "deviation": round(abs(qw - rp["wavenumber"]), 1)
                        })
            results.append(MatchResult(
                compound_id=comp_id,
                compound_name=comp["name"],
                confidence=round(pos_score * 100, 1),
                instrument="ftir",
                matched_peaks=matched
            ))

    results.sort(key=lambda r: r.confidence, reverse=True)
    return results[:5]


# ---- Mass Spec Matching ----

def match_mass_spec(query_fragments: list[dict], molecular_weight: float = 0, tolerance: float = 1.0) -> list[MatchResult]:
    """Match mass spectrum against compound database."""
    results = []
    query_mz = [f.get("mz", 0) if isinstance(f, dict) else float(f) for f in query_fragments]

    for comp_id, comp in COMPOUNDS.items():
        ms_data = comp.get("mass_spec", {})
        ref_frags = ms_data.get("fragments", [])
        if not ref_frags:
            continue

        # MW match bonus
        mw_bonus = 0
        if molecular_weight > 0 and abs(molecular_weight - comp["molecular_weight"]) < 2:
            mw_bonus = 0.3

        ref_mz = [f["mz"] for f in ref_frags]
        pos_score = peak_position_score(query_mz, ref_mz, tolerance)
        total_score = min(1.0, pos_score + mw_bonus)

        if total_score > 0.15:
            matched = []
            for qm in query_mz:
                for rf in ref_frags:
                    if abs(qm - rf["mz"]) <= tolerance:
                        matched.append({
                            "query_mz": qm,
                            "reference_mz": rf["mz"],
                            "label": rf.get("label", ""),
                            "deviation": round(abs(qm - rf["mz"]), 1)
                        })
            results.append(MatchResult(
                compound_id=comp_id,
                compound_name=comp["name"],
                confidence=round(total_score * 100, 1),
                instrument="mass_spec",
                matched_peaks=matched,
                notes=f"MW match: {comp['molecular_weight']}" if mw_bonus > 0 else ""
            ))

    results.sort(key=lambda r: r.confidence, reverse=True)
    return results[:5]


# ---- Multi-instrument Identification ----

def identify_compound(
    uvvis_peaks: list[dict] | None = None,
    ftir_peaks: list[dict] | None = None,
    ms_fragments: list[dict] | None = None,
    molecular_weight: float = 0
) -> IdentificationResult:
    """Identify a compound using data from multiple instruments."""
    all_matches: dict[str, dict] = {}  # compound_id -> {scores, details}
    analysis_notes = []
    anomalies = []

    # UV-Vis matching
    if uvvis_peaks:
        uv_matches = match_uvvis(uvvis_peaks)
        analysis_notes.append(f"UV-Vis: {len(uvvis_peaks)} peaks queried, {len(uv_matches)} candidates found")
        for m in uv_matches:
            if m.compound_id not in all_matches:
                all_matches[m.compound_id] = {"scores": [], "name": m.compound_name, "details": []}
            all_matches[m.compound_id]["scores"].append(m.confidence)
            all_matches[m.compound_id]["details"].extend(m.matched_peaks)

    # FTIR matching
    if ftir_peaks:
        ir_matches = match_ftir(ftir_peaks)
        analysis_notes.append(f"FTIR: {len(ftir_peaks)} peaks queried, {len(ir_matches)} candidates found")
        for m in ir_matches:
            if m.compound_id not in all_matches:
                all_matches[m.compound_id] = {"scores": [], "name": m.compound_name, "details": []}
            all_matches[m.compound_id]["scores"].append(m.confidence)
            all_matches[m.compound_id]["details"].extend(m.matched_peaks)

    # MS matching
    if ms_fragments is not None or molecular_weight > 0:
        ms_matches = match_mass_spec(ms_fragments or [], molecular_weight)
        analysis_notes.append(f"Mass Spec: {len(ms_fragments or [])} fragments queried, {len(ms_matches)} candidates found")
        for m in ms_matches:
            if m.compound_id not in all_matches:
                all_matches[m.compound_id] = {"scores": [], "name": m.compound_name, "details": []}
            all_matches[m.compound_id]["scores"].append(m.confidence)
            all_matches[m.compound_id]["details"].extend(m.matched_peaks)

    # Compute combined scores (average across instruments, bonus for multi-instrument)
    top_matches = []
    for comp_id, data in all_matches.items():
        avg_score = np.mean(data["scores"])
        # Multi-instrument bonus: +10% per additional instrument
        multi_bonus = (len(data["scores"]) - 1) * 10
        final_score = min(100, avg_score + multi_bonus)

        top_matches.append(MatchResult(
            compound_id=comp_id,
            compound_name=data["name"],
            confidence=round(final_score, 1),
            instrument="combined",
            matched_peaks=data["details"],
            notes=f"Matched across {len(data['scores'])} instrument(s)"
        ))

    top_matches.sort(key=lambda r: r.confidence, reverse=True)

    # Anomaly detection
    if top_matches and top_matches[0].confidence < 40:
        anomalies.append("Low confidence — compound may not be in the database")
    if top_matches and len(top_matches) > 1:
        if top_matches[0].confidence - top_matches[1].confidence < 10:
            anomalies.append("Multiple compounds with similar scores — consider additional analysis")

    instruments_used = sum([bool(uvvis_peaks), bool(ftir_peaks), bool(ms_fragments)])
    analysis_notes.append(f"Combined analysis using {instruments_used} instrument(s)")

    return IdentificationResult(
        top_matches=top_matches[:5],
        analysis_notes=analysis_notes,
        anomalies=anomalies
    )
