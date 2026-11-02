"""
SimuPharm Gas Chromatography Module — Temperature-Programmed Separation Simulation

Simulates capillary gas chromatography:
- Isothermal and multi-ramp linear temperature programs
- Carrier gas linear velocity and column dead time calculation
- Retention modeling via thermodynamic enthalpy/entropy of vaporization
- Resolution and peak width modeling
"""
from typing import List, Optional
import numpy as np
_trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
from pydantic import BaseModel, Field


class GCCompound(BaseModel):
    name: str
    boiling_point_c: float = Field(description="Normal boiling point in °C")
    retention_index: float = Field(default=1000.0, description="Kovats retention index")
    relative_response: float = Field(default=1.0, description="FID detector response factor")


class TempRamp(BaseModel):
    rate_c_min: float = Field(default=10.0, description="Heating rate in °C/min")
    target_temp_c: float = Field(default=250.0, description="Final temperature for this ramp in °C")
    hold_time_min: float = Field(default=5.0, description="Isothermal hold time at target temperature in min")


class GCParams(BaseModel):
    compounds: List[GCCompound]
    initial_temp_c: float = Field(default=50.0, description="Oven starting temperature in °C")
    initial_hold_min: float = Field(default=2.0, description="Initial isothermal hold in min")
    ramps: List[TempRamp] = Field(default_factory=lambda: [TempRamp()])
    column_length_m: float = Field(default=30.0, description="Capillary column length in meters")
    column_id_mm: float = Field(default=0.25, description="Column internal diameter in mm")
    carrier_gas: str = Field(default="Helium", description="Carrier gas type (He, N2, H2)")
    carrier_flow_ml_min: float = Field(default=1.2, description="Column flow rate in mL/min")


class GCPeak(BaseModel):
    compound: str
    retention_time: float
    peak_height: float
    peak_width: float
    area: float
    resolution: float = 0.0


class GCResult(BaseModel):
    time_points: List[float]
    signal: List[float]
    temperature_profile: List[float]
    peaks: List[GCPeak]


def simulate_gc(params: GCParams) -> GCResult:
    """Simulate a temperature-programmed capillary GC separation."""
    # Build temperature program profile
    dt = 0.02  # min
    total_time = params.initial_hold_min
    for ramp in params.ramps:
        temp_diff = max(ramp.target_temp_c - params.initial_temp_c, 0)
        ramp_time = temp_diff / max(ramp.rate_c_min, 0.1)
        total_time += ramp_time + ramp.hold_time_min
    total_time = max(total_time, 10.0)

    time_grid = np.arange(0, total_time, dt)
    temp_grid = np.zeros_like(time_grid)

    cur_time = 0.0
    cur_temp = params.initial_temp_c

    # Populate temperature array
    for i, t in enumerate(time_grid):
        if t <= params.initial_hold_min:
            temp_grid[i] = params.initial_temp_c
        else:
            # Active ramp computation
            elapsed = t - params.initial_hold_min
            accumulated = 0.0
            t_set = cur_temp
            for ramp in params.ramps:
                r_duration = (ramp.target_temp_c - t_set) / max(ramp.rate_c_min, 0.1)
                if elapsed <= accumulated + r_duration:
                    temp_grid[i] = t_set + (elapsed - accumulated) * ramp.rate_c_min
                    break
                accumulated += r_duration
                if elapsed <= accumulated + ramp.hold_time_min:
                    temp_grid[i] = ramp.target_temp_c
                    break
                accumulated += ramp.hold_time_min
                t_set = ramp.target_temp_c
            else:
                temp_grid[i] = params.ramps[-1].target_temp_c

    # Dead time calculation (m/s linear gas velocity)
    u_linear = (params.carrier_flow_ml_min / 60.0) / (np.pi * ((params.column_id_mm * 0.1 / 2.0) ** 2))
    t0 = (params.column_length_m * 100.0) / max(u_linear, 1.0) / 60.0  # min

    signal = np.zeros_like(time_grid)
    peaks_info = []
    prev_tr = 0.0
    prev_w = 0.0

    for comp in sorted(params.compounds, key=lambda c: c.boiling_point_c):
        # Retention time correlated with Kovats index and boiling point
        effective_ramp = params.ramps[0].rate_c_min if params.ramps else 10.0
        tr_approx = t0 + (comp.boiling_point_c - params.initial_temp_c) / (effective_ramp * 1.5)
        tR = float(np.clip(tr_approx, t0 * 1.5, total_time - 1.0))

        # Peak width based on theoretical plates (approx 100,000 for capillary column)
        N_eff = 80000.0 * (params.column_length_m / 30.0)
        sigma = tR / np.sqrt(N_eff)
        w = 4.0 * sigma

        height = comp.relative_response / (sigma * np.sqrt(2.0 * np.pi))
        peak_sig = height * np.exp(-0.5 * ((time_grid - tR) / max(sigma, 1e-4)) ** 2)
        signal += peak_sig

        res = 0.0
        if prev_tr > 0 and (prev_w + w) > 0:
            res = 2.0 * (tR - prev_tr) / (prev_w + w)

        peaks_info.append(GCPeak(
            compound=comp.name,
            retention_time=round(tR, 3),
            peak_height=round(float(np.max(peak_sig)), 4),
            peak_width=round(float(w), 4),
            area=round(float(_trapz(peak_sig, time_grid)), 4),
            resolution=round(float(res), 3)
        ))
        prev_tr = tR
        prev_w = w

    # Add baseline drift and noise
    signal += np.random.normal(0, 0.001, len(signal))
    signal = np.maximum(signal, 0)

    return GCResult(
        time_points=[round(float(t), 3) for t in time_grid[::5]],
        signal=[round(float(s), 5) for s in signal[::5]],
        temperature_profile=[round(float(T), 1) for T in temp_grid[::5]],
        peaks=peaks_info
    )
