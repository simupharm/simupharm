"""
SimuPharm: A Unified Open-Source Multi-Instrument Analytical and Spectroscopic Simulation Engine in Python.

Simulates:
- HPLC: Column separation kinetics, Van Deemter plate theory, peak resolution
- GC: Capillary gas chromatography with linear temperature programs
- FTIR: Fast Fourier Transform interferometry and functional group tagging
- UV-Vis: Electronic absorption, Beer-Lambert calibration curves, regression
- Mass Spectrometry: Electron & electrospray ionization, fragmentation, isotopic clusters
- Polarimetry: Optical rotation, Biot's law, enantiomeric excess
- Particle Size Analysis: Dynamic light scattering, log-normal distributions, D-values
- Chemometrics: Multi-instrument orthogonal compound identification
"""

__version__ = "1.0.0"
__author__ = "SimuPharm Research Team"
__license__ = "MIT"

# Instrument Engines
from simupharm.instruments.hplc import (
    simulate_hplc,
    HPLCParams,
    ColumnParams,
    HPLCCompound,
    HPLCResult,
    van_deemter
)
from simupharm.instruments.uvvis import (
    simulate_uvvis,
    UVVisParams,
    UVVisCompound,
    UVVisPeak,
    UVVisResult,
    generate_calibration_curve,
    CalibrationResult
)
from simupharm.instruments.ftir import (
    simulate_ftir,
    FTIRParams,
    IRPeak,
    FTIRResult,
    identify_functional_groups
)
from simupharm.instruments.gc import (
    simulate_gc,
    GCParams,
    GCCompound,
    TempRamp,
    GCResult
)
from simupharm.instruments.mass_spec import (
    simulate_mass_spec,
    MassSpecParams,
    MassSpecCompound,
    MSFragment,
    MassSpecResult
)
from simupharm.instruments.polarimeter import (
    simulate_polarimeter,
    PolarimetryParams,
    PolarimetryCompound,
    PolarimetryResult
)
from simupharm.instruments.psa import (
    simulate_psa,
    PSAParams,
    PSAResult
)

# Reference Compound Database
from simupharm.database.compounds import (
    COMPOUNDS,
    get_compound,
    list_compounds
)

# Multimodal Chemometrics & Compound Identification
from simupharm.analytics.matcher import (
    identify_compound,
    MatchResult,
    IdentificationResult,
    cosine_similarity,
    peak_position_score
)

__all__ = [
    "simulate_hplc", "HPLCParams", "ColumnParams", "HPLCCompound", "HPLCResult", "van_deemter",
    "simulate_uvvis", "UVVisParams", "UVVisCompound", "UVVisPeak", "UVVisResult", "generate_calibration_curve", "CalibrationResult",
    "simulate_ftir", "FTIRParams", "IRPeak", "FTIRResult", "identify_functional_groups",
    "simulate_gc", "GCParams", "GCCompound", "TempRamp", "GCResult",
    "simulate_mass_spec", "MassSpecParams", "MassSpecCompound", "MSFragment", "MassSpecResult",
    "simulate_polarimeter", "PolarimetryParams", "PolarimetryCompound", "PolarimetryResult",
    "simulate_psa", "PSAParams", "PSAResult",
    "COMPOUNDS", "get_compound", "list_compounds",
    "identify_compound", "MatchResult", "IdentificationResult", "cosine_similarity", "peak_position_score"
]
