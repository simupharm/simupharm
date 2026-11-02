"""
SimuPharm Case Study 1: HPLC Method Optimization & Robustness Profiling

Demonstrates:
1. In silico isocratic separation of a binary pharmaceutical mixture (Paracetamol & Caffeine).
2. Van Deemter plate height kinetics and optimal mobile phase linear velocity determination.
3. Organic modifier (%B) optimization for USP <621> baseline chromatographic resolution.
4. Export of high-resolution 300 DPI publication figure (Fig 2).
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure simupharm is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simupharm.instruments.hplc import (
    simulate_hplc,
    HPLCParams,
    HPLCCompound,
    ColumnParams,
    van_deemter
)

def run_hplc_case_study():
    print("=" * 70)
    print("SIMUPHARM CASE STUDY 1: HPLC METHOD OPTIMIZATION")
    print("=" * 70)

    # 1. Define compounds
    paracetamol = HPLCCompound(name="Paracetamol", retention_factor=1.8, peak_width_factor=1.0, response_factor=1.2)
    caffeine = HPLCCompound(name="Caffeine", retention_factor=4.5, peak_width_factor=1.05, response_factor=1.0)
    compounds = [paracetamol, caffeine]
    column = ColumnParams(length_cm=25.0, particle_size_um=5.0, internal_diameter_mm=4.6)

    # 2. Simulate across organic modifier ratios (% methanol)
    organic_pcts = [35.0, 50.0, 65.0]
    chromatograms = {}

    for org in organic_pcts:
        params = HPLCParams(
            compounds=compounds,
            column=column,
            flow_rate_ml_min=1.0,
            mobile_phase_organic_pct=org,
            run_time_min=20.0
        )
        res = simulate_hplc(params)
        chromatograms[org] = res
        p1 = res.peaks[0]
        p2 = res.peaks[1]
        print(f"[%B = {org:4.1f}%] Paracetamol tR={p1.retention_time:.2f} min, Caffeine tR={p2.retention_time:.2f} min | Rs={p2.resolution:.2f} (Plates N={p1.plates})")

    # 3. Parametric sweep for Resolution vs %B
    sweep_org = np.linspace(25.0, 75.0, 50)
    resolutions = []
    run_times = []

    for org in sweep_org:
        p = HPLCParams(
            compounds=compounds,
            column=column,
            flow_rate_ml_min=1.0,
            mobile_phase_organic_pct=float(org),
            run_time_min=30.0
        )
        r = simulate_hplc(p)
        resolutions.append(r.peaks[1].resolution)
        run_times.append(r.peaks[1].retention_time + 2.0 * r.peaks[1].peak_width)

    # 4. Van Deemter Curve calculation
    flow_rates = np.linspace(0.2, 3.0, 100)
    dp_cm = 5.0 * 1e-4
    A_term = np.full_like(flow_rates, 2.0 * dp_cm * 1e4) # um
    B_term = (0.05 / flow_rates) * 1e4 # um
    C_term = (0.01 * (dp_cm ** 2) * flow_rates) * 1e4 # um
    H_total = np.array([van_deemter(5.0, float(u)) * 1e4 for u in flow_rates]) # um

    u_opt_idx = np.argmin(H_total)
    u_opt = flow_rates[u_opt_idx]
    h_min = H_total[u_opt_idx]

    print(f"\n[Van Deemter] Optimal Flow Rate: {u_opt:.2f} mL/min (Minimum Plate Height H: {h_min:.2f} µm)")

    # 5. Generate Multi-panel Publication Figure (300 DPI)
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.size"] = 10
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8), dpi=300)

    # Panel A: Overlaid Chromatograms
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for i, (org, res) in enumerate(chromatograms.items()):
        axes[0].plot(res.time_points, res.signal, label=f"%B = {int(org)}% MeOH", color=colors[i], lw=1.8)
    axes[0].axhline(0, color="gray", lw=0.6, ls="--")
    axes[0].set_xlim(0, 15)
    axes[0].set_ylim(bottom=-0.05)
    axes[0].set_xlabel("Retention Time (min)", fontweight="bold")
    axes[0].set_ylabel("Absorbance / Detector Response (AU)", fontweight="bold")
    axes[0].set_title("(a) Chromatographic Separation Profiles", fontweight="bold", pad=10)
    axes[0].legend(frameon=True, facecolor="white", edgecolor="none", loc="upper right")
    axes[0].grid(True, alpha=0.25, ls=":")

    # Panel B: Van Deemter Kinetics
    axes[1].plot(flow_rates, H_total, "k-", lw=2.2, label=r"Total $H = A + B/u + Cu$")
    axes[1].plot(flow_rates, A_term, "b--", lw=1.2, alpha=0.7, label=r"Eddy diffusion ($A$)")
    axes[1].plot(flow_rates, B_term, "g--", lw=1.2, alpha=0.7, label=r"Longitudinal diff. ($B/u$)")
    axes[1].plot(flow_rates, C_term, "r--", lw=1.2, alpha=0.7, label=r"Mass transfer ($Cu$)")
    axes[1].scatter([u_opt], [h_min], color="crimson", zorder=5, s=60, label=f"Optimum: {u_opt:.2f} mL/min")
    axes[1].set_xlim(0.2, 3.0)
    axes[1].set_ylim(0, 35)
    axes[1].set_xlabel("Mobile Phase Flow Rate (mL/min)", fontweight="bold")
    axes[1].set_ylabel("Theoretical Plate Height $H$ (µm)", fontweight="bold")
    axes[1].set_title("(b) Van Deemter Kinetic Optimization", fontweight="bold", pad=10)
    axes[1].legend(frameon=True, facecolor="white", edgecolor="none", fontsize=8.5, loc="upper right")
    axes[1].grid(True, alpha=0.25, ls=":")

    # Panel C: Method Design Space (Rs vs %B)
    ax3_twin = axes[2].twinx()
    l1 = axes[2].plot(sweep_org, resolutions, color="#d62728", lw=2.0, label="USP Resolution ($R_s$)")
    l2 = ax3_twin.plot(sweep_org, run_times, color="#7f7f7f", lw=1.8, ls="-.", label="Retention Time (min)")
    axes[2].axhline(1.5, color="black", ls=":", lw=1.2, label=r"USP Baseline Threshold ($R_s=1.5$)")
    
    # Shade design space (Rs >= 1.5)
    valid_mask = np.array(resolutions) >= 1.5
    axes[2].fill_between(sweep_org, 0, resolutions, where=valid_mask, color="#2ca02c", alpha=0.12, label="Acceptable Design Region")
    
    axes[2].set_xlim(25, 75)
    axes[2].set_ylim(0, 6)
    ax3_twin.set_ylim(0, 25)
    axes[2].set_xlabel("Organic Modifier %B (% v/v MeOH)", fontweight="bold")
    axes[2].set_ylabel("USP Resolution $R_s$ (dimensionless)", fontweight="bold", color="#d62728")
    ax3_twin.set_ylabel("Total Run Duration (min)", fontweight="bold", color="#7f7f7f")
    axes[2].tick_params(axis='y', labelcolor="#d62728")
    ax3_twin.tick_params(axis='y', labelcolor="#7f7f7f")
    axes[2].set_title("(c) Resolution vs. Analysis Speed Design Space", fontweight="bold", pad=10)
    
    lines = l1 + l2 + [axes[2].lines[1]]
    labels = [l.get_label() for l in lines]
    axes[2].legend(lines, labels, loc="upper right", frameon=True, fontsize=8.5)
    axes[2].grid(True, alpha=0.25, ls=":")

    plt.tight_layout()
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "PUBLICATION_SOFTWAREX", "figures", "fig2_hplc_optimization.png"))
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\n[Figure Generated] Saved 300 DPI figure to:\n  -> {output_path}")
    print("=" * 70)

if __name__ == "__main__":
    run_hplc_case_study()
