"""
SimuPharm Case Study 2: UV-Vis Spectrophotometric Calibration & ICH Q2(R1) Validation

Demonstrates:
1. In silico simulation of electronic absorption spectra for Ciprofloxacin at 5 concentrations.
2. Beer-Lambert molar extinction and Gaussian band deconvolution.
3. Ordinary least squares (OLS) regression calibration curve generation.
4. Limit of Detection (LOD) and Limit of Quantitation (LOQ) computation per ICH Q2(R1).
5. Export of high-resolution 300 DPI publication figure (Fig 3).
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure simupharm is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simupharm.instruments.uvvis import (
    simulate_uvvis,
    UVVisParams,
    UVVisCompound,
    UVVisPeak,
    generate_calibration_curve
)

def run_uvvis_case_study():
    print("=" * 70)
    print("SIMUPHARM CASE STUDY 2: UV-VIS SPECTROPHOTOMETRY & CALIBRATION")
    print("=" * 70)

    # 1. Define Ciprofloxacin (dual absorption bands: 277 nm primary pi->pi*, 315 nm secondary n->pi*)
    cipro_peaks = [
        UVVisPeak(center=277.0, width=16.0, epsilon=31500.0, label="pi->pi* (quinolone core)"),
        UVVisPeak(center=315.0, width=22.0, epsilon=8500.0, label="n->pi*")
    ]
    compound = UVVisCompound(name="Ciprofloxacin HCl", peaks=cipro_peaks, solvent="0.1M HCl")

    # 2. Calibration Series (2 to 20 micromolar: 2e-6 to 20e-6 M)
    concs_um = np.array([2.0, 5.0, 10.0, 15.0, 20.0]) # uM
    concs_m = concs_um * 1e-6 # mol/L

    spectra = []
    abs_at_lambda_max = []
    np.random.seed(42) # Reproducible photometric noise

    for c in concs_m:
        params = UVVisParams(
            compound=compound,
            concentration_molar=float(c),
            path_length_cm=1.0,
            wavelength_min=220.0,
            wavelength_max=400.0,
            noise_level=0.0015
        )
        res = simulate_uvvis(params)
        spectra.append(res)
        # Extract absorbance at 277 nm
        idx_277 = int(277.0 - 220.0)
        abs_val = res.absorbance[idx_277]
        abs_at_lambda_max.append(abs_val)
        print(f"[C = {c*1e6:4.1f} µM] Absorbance at 277 nm: {abs_val:.4f} AU (Transmittance: {res.transmittance[idx_277]:.1f}%)")

    # 3. OLS Regression & ICH Validation
    abs_arr = np.array(abs_at_lambda_max)
    slope, intercept = np.polyfit(concs_um, abs_arr, 1)
    y_pred = slope * concs_um + intercept
    residuals = abs_arr - y_pred

    ss_tot = np.sum((abs_arr - np.mean(abs_arr)) ** 2)
    ss_res = np.sum(residuals ** 2)
    r2 = 1.0 - (ss_res / ss_tot)

    s_y = np.sqrt(np.sum(residuals ** 2) / (len(concs_um) - 2))
    lod_um = 3.3 * s_y / slope
    loq_um = 10.0 * s_y / slope

    print("\n--- Calibration Regression Summary ---")
    print(f"Slope (Sensitivity): {slope:.5f} AU/(µmol/L)")
    print(f"Intercept:           {intercept:+.5f} AU")
    print(f"R² Coefficient:      {r2:.6f}")
    print(f"Residual Std Dev Sy: {s_y:.5f} AU")
    print(f"ICH LOD:             {lod_um:.3f} µM ({lod_um * 0.3313:.3f} µg/mL)")
    print(f"ICH LOQ:             {loq_um:.3f} µM ({loq_um * 0.3313:.3f} µg/mL)")

    # 4. Multi-panel Publication Figure (300 DPI)
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.size"] = 10
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8), dpi=300)

    # Panel A: Overlaid Spectra
    cmap = plt.get_cmap("viridis")
    norm_colors = np.linspace(0.2, 0.85, len(concs_um))
    for i, res in enumerate(spectra):
        axes[0].plot(res.wavelengths, res.absorbance, label=f"{concs_um[i]:.1f} µM", color=cmap(norm_colors[i]), lw=1.8)

    axes[0].axvline(277.0, color="gray", ls="--", lw=1.0, alpha=0.7)
    axes[0].text(279.0, 0.55, r"$\lambda_{\max} = 277$ nm", color="dimgray", fontsize=9, fontweight="bold")
    axes[0].set_xlim(220, 380)
    axes[0].set_ylim(0, 0.75)
    axes[0].set_xlabel("Wavelength (nm)", fontweight="bold")
    axes[0].set_ylabel("Absorbance (AU)", fontweight="bold")
    axes[0].set_title("(a) Electronic Absorption Spectra", fontweight="bold", pad=10)
    axes[0].legend(title="Concentration", frameon=True, facecolor="white", edgecolor="none", fontsize=8.5)
    axes[0].grid(True, alpha=0.25, ls=":")

    # Panel B: Calibration Line & 95% Confidence Band
    c_dense = np.linspace(0, 22, 100)
    y_dense = slope * c_dense + intercept
    # 95% prediction interval approximation
    t_val = 3.182 # t for df=3, 95%
    se_line = s_y * np.sqrt(1/len(concs_um) + (c_dense - np.mean(concs_um))**2 / np.sum((concs_um - np.mean(concs_um))**2))
    
    axes[1].fill_between(c_dense, y_dense - t_val * se_line, y_dense + t_val * se_line, color="#1f77b4", alpha=0.15, label="95% Confidence Band")
    axes[1].plot(c_dense, y_dense, "r-", lw=2.0, label=f"OLS: $y = {slope:.4f}x {intercept:+.4f}$")
    axes[1].scatter(concs_um, abs_arr, color="#1f77b4", edgecolor="black", s=50, zorder=5, label="Standards ($N=5$)")
    
    # Annotate stats box
    stats_text = (
        f"$R^2 = {r2:.5f}$\n"
        f"LOD = {lod_um:.2f} µM\n"
        f"LOQ = {loq_um:.2f} µM\n"
        f"$S_y = {s_y:.4f}$ AU"
    )
    axes[1].text(0.06, 0.65, stats_text, transform=axes[1].transAxes, fontsize=9,
                 verticalalignment="top", bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8f9fa", edgecolor="#ced4da", alpha=0.9))
    
    axes[1].set_xlim(0, 22)
    axes[1].set_ylim(0, 0.75)
    axes[1].set_xlabel("Ciprofloxacin Concentration (µM)", fontweight="bold")
    axes[1].set_ylabel("Absorbance at 277 nm (AU)", fontweight="bold")
    axes[1].set_title("(b) Beer-Lambert Calibration Curve", fontweight="bold", pad=10)
    axes[1].legend(loc="lower right", frameon=True, facecolor="white", edgecolor="none", fontsize=8.5)
    axes[1].grid(True, alpha=0.25, ls=":")

    # Panel C: Residual Plot
    axes[2].axhline(0, color="black", lw=1.2, ls="--")
    axes[2].scatter(concs_um, residuals * 1e3, color="#d62728", s=60, edgecolor="black", zorder=5)
    for cx, rx in zip(concs_um, residuals):
        axes[2].plot([cx, cx], [0, rx * 1e3], color="#d62728", ls=":", lw=1.2)
    
    axes[2].set_xlim(0, 22)
    max_res = max(abs(residuals)) * 1e3 * 1.5
    axes[2].set_ylim(-max(max_res, 3.0), max(max_res, 3.0))
    axes[2].set_xlabel("Ciprofloxacin Concentration (µM)", fontweight="bold")
    axes[2].set_ylabel(r"Residual ($y_i - \hat{y}_i$) [mAU]", fontweight="bold")
    axes[2].set_title("(c) Ordinary Least Squares Residuals", fontweight="bold", pad=10)
    axes[2].grid(True, alpha=0.25, ls=":")

    plt.tight_layout()
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "PUBLICATION_SOFTWAREX", "figures", "fig3_uvvis_calibration.png"))
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\n[Figure Generated] Saved 300 DPI figure to:\n  -> {output_path}")
    print("=" * 70)

if __name__ == "__main__":
    run_uvvis_case_study()
