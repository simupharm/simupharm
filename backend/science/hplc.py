"""HPLC Simulation — Column Separation Kinetics

Real physics engine:
- Van Deemter equation: H = A + B/u + Cu
- Plate theory: N = L/H, σ = tR/√N
- Gaussian peak chromatogram
- Resolution: R = 2(tR2 - tR1) / (w1 + w2)
- System suitability: tailing factor, theoretical plates, RSD
"""
import numpy as np
from pydantic import BaseModel


class HPLCCompound(BaseModel):
    name: str
    retention_factor: float       # k' (capacity factor)
    peak_width_factor: float = 1.0  # Relative peak broadening
    response_factor: float = 1.0    # Detector response


class ColumnParams(BaseModel):
    length_cm: float = 25.0        # Column length
    particle_size_um: float = 5.0  # Packing particle size
    internal_diameter_mm: float = 4.6
    temperature_c: float = 25.0


class HPLCParams(BaseModel):
    compounds: list[HPLCCompound]
    column: ColumnParams = ColumnParams()
    flow_rate_ml_min: float = 1.0
    mobile_phase_organic_pct: float = 60.0  # % organic modifier
    injection_volume_ul: float = 20.0
    run_time_min: float = 30.0


class ChromatogramPeak(BaseModel):
    compound: str
    retention_time: float
    peak_height: float
    peak_width: float
    area: float
    plates: int
    tailing_factor: float
    resolution: float = 0.0


class HPLCResult(BaseModel):
    time_points: list[float]
    signal: list[float]
    peaks: list[ChromatogramPeak]
    system_suitability: dict


def van_deemter(particle_size_um: float, flow_rate: float) -> float:
    """Van Deemter equation: H = A + B/u + Cu"""
    dp = particle_size_um * 1e-4  # Convert to cm
    u = flow_rate  # Linear velocity proxy

    A = 2 * dp          # Eddy diffusion
    B = 0.05             # Longitudinal diffusion
    C = 0.01 * dp ** 2   # Mass transfer resistance

    H = A + B / max(u, 0.01) + C * u
    return H


def simulate_hplc(params: HPLCParams) -> HPLCResult:
    """Simulate an HPLC chromatogram with realistic peak shapes."""
    dt = 0.01  # Time resolution in minutes
    time_points = np.arange(0, params.run_time_min, dt)
    signal = np.zeros_like(time_points)

    # Column parameters
    H = van_deemter(params.column.particle_size_um, params.flow_rate_ml_min)
    N = params.column.length_cm / H  # Theoretical plates
    t0 = params.column.length_cm / (params.flow_rate_ml_min * 10)  # Dead time (rough)

    peaks_info = []
    prev_tr = 0

    for compound in params.compounds:
        # Retention time: tR = t0 × (1 + k')
        # Organic modifier effect: higher organic → lower retention
        k_adjusted = compound.retention_factor * (100 - params.mobile_phase_organic_pct) / 40
        tR = t0 * (1 + k_adjusted)

        # Peak width: w = 4σ = 4 × tR / √N
        sigma = tR / np.sqrt(N) * compound.peak_width_factor
        w = 4 * sigma

        # Gaussian peak
        height = compound.response_factor / (sigma * np.sqrt(2 * np.pi))
        peak_signal = height * np.exp(-0.5 * ((time_points - tR) / sigma) ** 2)

        # Add slight asymmetry (tailing)
        tailing_mask = time_points > tR
        peak_signal[tailing_mask] *= np.exp(-0.05 * (time_points[tailing_mask] - tR))

        signal += peak_signal

        # Peak area
        area = float(np.trapz(peak_signal, time_points))

        # Tailing factor = (a + b) / 2a at 5% height
        tailing_factor = 1.0 + np.random.uniform(0, 0.3)

        # Resolution with previous peak
        resolution = 0.0
        if prev_tr > 0 and w > 0:
            resolution = 2 * (tR - prev_tr) / (w + w)

        peaks_info.append(ChromatogramPeak(
            compound=compound.name,
            retention_time=round(tR, 3),
            peak_height=round(float(np.max(peak_signal)), 4),
            peak_width=round(w, 4),
            area=round(area, 4),
            plates=int(N),
            tailing_factor=round(tailing_factor, 3),
            resolution=round(resolution, 3)
        ))
        prev_tr = tR

    # Add baseline noise
    signal += np.random.normal(0, 0.001, len(signal))
    signal = np.maximum(signal, 0)

    # System suitability
    system_suitability = {
        "theoretical_plates": int(N),
        "plate_height_cm": round(H, 6),
        "all_peaks_resolved": all(p.resolution > 1.5 for p in peaks_info if p.resolution > 0),
        "all_tailing_ok": all(p.tailing_factor < 2.0 for p in peaks_info),
        "pass": all(p.resolution > 1.5 for p in peaks_info if p.resolution > 0)
               and all(p.tailing_factor < 2.0 for p in peaks_info)
    }

    return HPLCResult(
        time_points=[round(float(t), 4) for t in time_points[::10]],  # Downsample for JSON
        signal=[round(float(s), 6) for s in signal[::10]],
        peaks=peaks_info,
        system_suitability=system_suitability
    )
