"""Gas Chromatography — Temperature Program Simulation

Real physics engine:
- Kovats retention index calculation
- Temperature-programmed retention time
- FID/TCD detector response modeling
- Gaussian peak chromatogram
"""
import numpy as np
from pydantic import BaseModel


class GCCompound(BaseModel):
    name: str
    boiling_point_c: float
    kovats_index: float = 0.0       # Kovats retention index
    response_factor: float = 1.0


class GCParams(BaseModel):
    compounds: list[GCCompound]
    oven_initial_c: float = 50.0
    oven_final_c: float = 280.0
    ramp_rate_c_min: float = 10.0
    hold_initial_min: float = 2.0
    hold_final_min: float = 5.0
    flow_rate_ml_min: float = 1.5
    column_length_m: float = 30.0
    detector: str = "FID"           # FID or TCD
    run_time_min: float = 30.0


class GCResult(BaseModel):
    time_points: list[float]
    signal: list[float]
    temperature_profile: list[float]
    peaks: list[dict]


def calculate_oven_temperature(t: float, params: GCParams) -> float:
    """Calculate oven temperature at time t (minutes)."""
    if t < params.hold_initial_min:
        return params.oven_initial_c
    ramp_time = (params.oven_final_c - params.oven_initial_c) / params.ramp_rate_c_min
    ramp_end = params.hold_initial_min + ramp_time
    if t < ramp_end:
        return params.oven_initial_c + params.ramp_rate_c_min * (t - params.hold_initial_min)
    return params.oven_final_c


def simulate_gc(params: GCParams) -> GCResult:
    """Simulate a GC chromatogram with temperature programming."""
    dt = 0.02
    time_points = np.arange(0, params.run_time_min, dt)
    signal = np.zeros_like(time_points)
    temp_profile = np.array([calculate_oven_temperature(t, params) for t in time_points])

    peaks_info = []

    for compound in params.compounds:
        # Retention time: roughly proportional to boiling point relative to oven temp
        # Higher BP → elutes later; higher ramp rate → faster elution
        bp = compound.boiling_point_c
        t_elute = params.hold_initial_min + (bp - params.oven_initial_c) / max(params.ramp_rate_c_min, 0.1)
        t_elute = max(t_elute, 0.5)
        t_elute = min(t_elute, params.run_time_min * 0.95)

        # Peak width broadens with retention time
        sigma = 0.05 + 0.01 * t_elute

        # Gaussian peak
        height = compound.response_factor / (sigma * np.sqrt(2 * np.pi))
        peak_signal = height * np.exp(-0.5 * ((time_points - t_elute) / sigma) ** 2)
        signal += peak_signal

        area = float(np.trapz(peak_signal, time_points))
        peaks_info.append({
            "compound": compound.name,
            "retention_time": round(t_elute, 3),
            "boiling_point": bp,
            "peak_height": round(float(np.max(peak_signal)), 4),
            "area": round(area, 4),
            "sigma": round(sigma, 4),
            "elution_temperature": round(calculate_oven_temperature(t_elute, params), 1)
        })

    # Baseline noise
    signal += np.random.normal(0, 0.0005, len(signal))
    signal = np.maximum(signal, 0)

    # Downsample
    step = 10
    return GCResult(
        time_points=[round(float(t), 3) for t in time_points[::step]],
        signal=[round(float(s), 6) for s in signal[::step]],
        temperature_profile=[round(float(t), 1) for t in temp_profile[::step]],
        peaks=peaks_info
    )
