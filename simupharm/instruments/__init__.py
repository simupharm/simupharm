"""
SimuPharm Instruments Package.
"""
from simupharm.instruments.hplc import simulate_hplc, HPLCParams, ColumnParams, HPLCCompound, HPLCResult
from simupharm.instruments.uvvis import simulate_uvvis, UVVisParams, UVVisCompound, UVVisPeak, UVVisResult, generate_calibration_curve
from simupharm.instruments.ftir import simulate_ftir, FTIRParams, IRPeak, FTIRResult, identify_functional_groups
from simupharm.instruments.gc import simulate_gc, GCParams, GCCompound, TempRamp, GCResult
from simupharm.instruments.mass_spec import simulate_mass_spec, MassSpecParams, MassSpecCompound, MSFragment, MassSpecResult
from simupharm.instruments.polarimeter import simulate_polarimeter, PolarimetryParams, PolarimetryCompound, PolarimetryResult
from simupharm.instruments.psa import simulate_psa, PSAParams, PSAResult
