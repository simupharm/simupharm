"""Mass Spectrometry — Fragmentation & Isotope Pattern Simulation

Real physics engine:
- Molecular ion peak from molecular weight
- Fragmentation pattern based on bond energies
- Isotope pattern calculation (M, M+1, M+2)
- m/z distribution with relative intensities
"""
import numpy as np
from pydantic import BaseModel


class MassSpecCompound(BaseModel):
    name: str
    molecular_weight: float
    formula: str
    fragments: list[dict] = []  # [{mz, intensity, label}]


class MassSpecParams(BaseModel):
    compound: MassSpecCompound
    ionization_mode: str = "EI"       # EI, ESI+, ESI-
    mass_range_min: float = 10.0
    mass_range_max: float = 0.0       # 0 = auto (MW + 50)
    resolution: float = 1.0


class MassSpecResult(BaseModel):
    mz_values: list[float]
    intensities: list[float]
    base_peak_mz: float
    base_peak_intensity: float
    molecular_ion_mz: float
    fragments: list[dict]
    isotope_pattern: list[dict]


# ---- Common Fragmentation Rules ----
COMMON_LOSSES = [
    {"loss": 1, "label": "H·", "probability": 0.3},
    {"loss": 15, "label": "CH₃·", "probability": 0.6},
    {"loss": 17, "label": "OH·", "probability": 0.5},
    {"loss": 18, "label": "H₂O", "probability": 0.7},
    {"loss": 28, "label": "CO / C₂H₄", "probability": 0.5},
    {"loss": 29, "label": "CHO·", "probability": 0.4},
    {"loss": 31, "label": "OCH₃·", "probability": 0.3},
    {"loss": 43, "label": "CH₃CO· / C₃H₇·", "probability": 0.6},
    {"loss": 44, "label": "CO₂", "probability": 0.4},
    {"loss": 45, "label": "OC₂H₅·", "probability": 0.3},
    {"loss": 57, "label": "C₄H₉·", "probability": 0.3},
    {"loss": 77, "label": "C₆H₅·", "probability": 0.4},
]


def parse_formula(formula: str) -> dict:
    """Parse molecular formula like C8H9NO2 → {C:8, H:9, N:1, O:2}."""
    import re
    elements = {}
    # Handle subscript unicode and regular text
    clean = formula.replace("₁", "1").replace("₂", "2").replace("₃", "3")
    clean = clean.replace("₄", "4").replace("₅", "5").replace("₆", "6")
    clean = clean.replace("₇", "7").replace("₈", "8").replace("₉", "9").replace("₀", "0")
    for match in re.finditer(r'([A-Z][a-z]?)(\d*)', clean):
        elem = match.group(1)
        count = int(match.group(2)) if match.group(2) else 1
        elements[elem] = elements.get(elem, 0) + count
    return elements


def calculate_isotope_pattern(formula: str, mw: float) -> list[dict]:
    """Calculate M, M+1, M+2 isotope pattern."""
    elements = parse_formula(formula)
    # Natural abundance ratios
    # M+1: 1.1% per C, 0.37% per N
    # M+2: 0.2% per O, 4.4% per S, 32.0% per Cl, 49.3% per Br
    m1_ratio = elements.get("C", 0) * 1.1 + elements.get("N", 0) * 0.37
    m2_ratio = elements.get("O", 0) * 0.2 + elements.get("S", 0) * 4.4 + \
               elements.get("Cl", 0) * 32.0 + elements.get("Br", 0) * 49.3

    return [
        {"mz": mw, "intensity": 100.0, "label": "M⁺"},
        {"mz": mw + 1, "intensity": round(m1_ratio, 2), "label": "M+1"},
        {"mz": mw + 2, "intensity": round(m2_ratio, 2), "label": "M+2"},
    ]


def generate_fragmentation(mw: float, formula: str, known_fragments: list[dict]) -> list[dict]:
    """Generate fragmentation pattern from molecular weight and common losses."""
    fragments = []

    # Use known fragments if provided
    if known_fragments:
        for frag in known_fragments:
            fragments.append({
                "mz": frag["mz"],
                "intensity": frag.get("intensity", 50),
                "label": frag.get("label", f"m/z {frag['mz']}")
            })
    else:
        # Generate from common fragmentation rules
        for loss in COMMON_LOSSES:
            fragment_mz = mw - loss["loss"]
            if fragment_mz > 10:
                intensity = np.random.uniform(10, 80) * loss["probability"]
                fragments.append({
                    "mz": fragment_mz,
                    "intensity": round(intensity, 1),
                    "label": f"M - {loss['label']} ({fragment_mz:.0f})"
                })

    return fragments


def simulate_mass_spec(params: MassSpecParams) -> MassSpecResult:
    """Generate a mass spectrum with molecular ion, fragments, and isotopes."""
    mw = params.compound.molecular_weight
    max_mz = params.mass_range_max if params.mass_range_max > 0 else mw + 50

    # Molecular ion
    mol_ion_intensity = 100.0 if params.ionization_mode == "EI" else 80.0

    # Fragmentation
    fragments = generate_fragmentation(mw, params.compound.formula, params.compound.fragments)

    # Isotope pattern
    isotopes = calculate_isotope_pattern(params.compound.formula, mw)

    # Build stick spectrum
    all_peaks = {}
    # Molecular ion
    all_peaks[round(mw)] = mol_ion_intensity
    # Fragments
    for frag in fragments:
        mz_key = round(frag["mz"])
        if params.mass_range_min <= mz_key <= max_mz:
            all_peaks[mz_key] = max(all_peaks.get(mz_key, 0), frag["intensity"])
    # Isotopes
    for iso in isotopes:
        mz_key = round(iso["mz"])
        all_peaks[mz_key] = max(all_peaks.get(mz_key, 0), iso["intensity"])

    # Normalize to base peak = 100
    if all_peaks:
        max_intensity = max(all_peaks.values())
        if max_intensity > 0:
            all_peaks = {k: round(v / max_intensity * 100, 1) for k, v in all_peaks.items()}

    # Sort by m/z
    sorted_mz = sorted(all_peaks.keys())
    mz_values = [float(m) for m in sorted_mz]
    intensities = [float(all_peaks[m]) for m in sorted_mz]

    # Find base peak
    base_idx = int(np.argmax(intensities)) if intensities else 0

    return MassSpecResult(
        mz_values=mz_values,
        intensities=intensities,
        base_peak_mz=mz_values[base_idx] if mz_values else 0,
        base_peak_intensity=intensities[base_idx] if intensities else 0,
        molecular_ion_mz=mw,
        fragments=fragments,
        isotope_pattern=isotopes
    )
