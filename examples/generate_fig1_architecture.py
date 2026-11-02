"""
Generate Fig 1: SimuPharm Modular System Architecture & Data Flow
Fixed typography and padding to eliminate any text/border collisions.
Generates publication-grade (300 DPI) diagram.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_architecture_figure():
    fig = plt.figure(figsize=(15, 9.2), dpi=300)
    ax = fig.add_subplot(111)
    ax.axis("off")

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Professional color palette
    color_input = "#EBF3FB"      # Soft Ice Blue
    color_border_in = "#1565C0"  # Deep Blue
    color_engine = "#EAF5EA"     # Soft Mint Green
    color_border_eng = "#2E7D32" # Forest Green
    color_analytics = "#FFF4E5"  # Soft Warm Amber
    color_border_ana = "#E65100" # Rich Orange
    color_app = "#F4EBF7"        # Soft Lilac
    color_border_app = "#6A1B9A" # Deep Purple

    def draw_box(x, y, w, h, bg, border, title, items, subtitle=""):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.5",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        # Title
        ax.text(x + w/2, y + h - 3.2, title, ha="center", va="center", fontsize=11, fontweight="bold", color=border)
        
        # Subtitle & start position
        if subtitle:
            ax.text(x + w/2, y + h - 6.2, subtitle, ha="center", va="center", fontsize=8.0, fontstyle="italic", color="#555555")
            start_y = y + h - 9.5
        else:
            start_y = y + h - 7.0

        # Dynamic spacing to ensure bottom text is ALWAYS generously above bottom line
        n_items = len(items)
        available_height = start_y - (y + 3.0)
        step = min(2.7, available_height / max(n_items - 1, 1))

        for i, item in enumerate(items):
            item_y = start_y - i * step
            ax.text(x + 2.2, item_y, f"• {item}", ha="left", va="center", fontsize=7.8, color="#1a1a1a")

    # Layer 1: Inputs & Compound Database (Top: y=67, h=27 -> top=94)
    draw_box(4, 67, 26, 27, color_input, color_border_in, "Method Parameters", [
        "Column specs (L, dp, dc)",
        "Flow rate (0.1–5 mL/min)",
        "Mobile phase composition",
        "Temperature ramps (GC)",
        "Optical path & wavelengths",
        "Additive Gaussian noise"
    ], "Pydantic-validated Inputs")

    draw_box(34, 67, 30, 27, color_input, color_border_in, "Reference Compound DB", [
        "21 Active Pharmacopeial APIs",
        "Molar absorptivities (ε)",
        "Characteristic FTIR bands",
        "EI/ESI mass fragment trees",
        "Specific optical rotations [α]",
        "Hydrophobic indices & logP"
    ], "Curated Analytical Knowledgebase")

    draw_box(68, 67, 28, 27, color_input, color_border_in, "Computational Core", [
        "Pure Python 3.10+ & NumPy",
        "Vectorized execution (<5 ms)",
        "Zero wet-lab overhead",
        "Deterministic reproducibility",
        "Stateless functional architecture",
        "Standards-compliant build"
    ], "High-Throughput Foundation")

    # Layer 2: 7 Analytical Instrument Engines (Middle: y=33, h=30 -> top=63)
    rect_eng_group = patches.FancyBboxPatch((3, 33), 94, 30, boxstyle="round,pad=0.8,rounding_size=2.0",
                                            facecolor=color_engine, edgecolor=color_border_eng, linewidth=2.0)
    ax.add_patch(rect_eng_group)
    ax.text(50, 60.5, "SimuPharm Modular Instrument Simulation Suite (simupharm.instruments)",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=color_border_eng)

    engines = [
        ("HPLC", ["Van Deemter kinetics", "Plate height H(u)", "Asymmetry & tailing"], 4.8),
        ("UV-Vis", ["Beer-Lambert law", "Gaussian deconv.", "Multi-band overlap"], 18.2),
        ("FTIR", ["Interferogram FFT", "Beer absorption", "Functional modes"], 31.6),
        ("GC", ["Golay capillary eq.", "Carrier velocity", "Thermal ramps"], 45.0),
        ("Mass Spec", ["EI / ESI ionization", "Isotope envelopes", "Fragment trees"], 58.4),
        ("Polarimeter", ["Biot's optical law", "Drude dispersion", "Enantiomeric excess"], 71.8),
        ("PSA", ["Dynamic light scatter", "Log-normal size dist.", "D10, D50, D90 spans"], 85.2)
    ]

    for name, feats, x_pos in engines:
        card = patches.FancyBboxPatch((x_pos, 35.5), 11.2, 21.5, boxstyle="round,pad=0.4,rounding_size=1.0",
                                       facecolor="white", edgecolor=color_border_eng, linewidth=1.2)
        ax.add_patch(card)
        ax.text(x_pos + 5.6, 54.5, name, ha="center", va="center", fontsize=10.0, fontweight="bold", color="#1B5E20")
        for j, feat in enumerate(feats):
            ax.text(x_pos + 0.9, 49.8 - j * 4.2, f"• {feat}", ha="left", va="top", fontsize=7.0, color="#333333")

    # Layer 3: Chemometrics & Analytics (Bottom Left: y=4, h=25)
    draw_box(4, 4, 44, 25, color_analytics, color_border_ana, "Analytics & Chemometrics Layer", [
        "USP <621> System Suitability (Plates N, Tailing T, Resolution Rs)",
        "ICH Q2(R1) Method Validation (OLS Calibration, LOD, LOQ)",
        "Multimodal Orthogonal Consensus Matching (UV + FTIR + MS)",
        "Cosine Spectral Similarity & Peak Centroid Matching Algorithms"
    ], "simupharm.analytics")

    # Layer 4: Applications & Integration (Bottom Right: y=4, h=25)
    draw_box(52, 4, 44, 25, color_app, color_border_app, "Deployment & Integration Ecosystem", [
        "Standalone Open-Source Python Package (pip install simupharm)",
        "Interactive Educational GUI (React 18 + Tailwind + Lucide)",
        "FastAPI High-Performance RESTful Microservice Endpoints",
        "Automated Test Infrastructure (100% pytest suite verification)"
    ], "Open-Science Delivery")

    # Connecting Arrows
    arrow_style = dict(arrowstyle="->,head_width=0.45,head_length=0.6", color="#424242", lw=1.8)
    # Inputs -> Engines
    ax.annotate("", xy=(50, 63.8), xytext=(50, 66.8), arrowprops=arrow_style)
    # Engines -> Analytics & Apps
    ax.annotate("", xy=(26, 29.8), xytext=(26, 32.8), arrowprops=arrow_style)
    ax.annotate("", xy=(74, 29.8), xytext=(74, 32.8), arrowprops=arrow_style)

    # Title header
    fig.text(0.5, 0.97, "Figure 1: Modular Architecture and Functional Pipeline of the SimuPharm Platform",
             ha="center", va="center", fontsize=13.5, fontweight="bold", color="#1a1a1a")

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "PUBLICATION_SOFTWAREX", "figures", "fig1_system_architecture.png"))
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[Figure 1 Generated] Saved cleanly padded architecture diagram to:\n  -> {output_path}")

    # Copy to latex/figures as well
    latex_fig_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "PUBLICATION_SOFTWAREX", "latex", "figures", "fig1_system_architecture.png"))
    if os.path.exists(os.path.dirname(latex_fig_path)):
        import shutil
        shutil.copyfile(output_path, latex_fig_path)
        print(f"[Copied] Latex figure: {latex_fig_path}")

if __name__ == "__main__":
    generate_architecture_figure()
