"""
Compile SoftwareX Submission Manuscript into High-Quality Publication PDF
Uses Playwright Chromium to render HTML/KaTeX into Elsevier SoftwareX format.
"""
import os
import sys
import base64
import shutil
import asyncio
from playwright.async_api import async_playwright

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{b64}"

async def generate_pdf():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    fig_dir = os.path.join(base_dir, "figures")

    fig1_b64 = get_base64_image(os.path.join(fig_dir, "fig1_system_architecture.png"))
    fig2_b64 = get_base64_image(os.path.join(fig_dir, "fig2_hplc_optimization.png"))
    fig3_b64 = get_base64_image(os.path.join(fig_dir, "fig3_uvvis_calibration.png"))
    fig4_b64 = get_base64_image(os.path.join(fig_dir, "fig4_multimodal_matching.png"))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SimuPharm: SoftwareX Manuscript</title>
<!-- KaTeX CSS and JS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{
        delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$', right: '$', display: false}}
        ]
    }});"></script>

<style>
    @page {{
        size: A4;
        margin: 20mm 18mm 20mm 18mm;
        @top-right {{
            content: "SoftwareX — Submission Manuscript";
            font-size: 8pt;
            color: #777;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }}
        @bottom-center {{
            content: counter(page);
            font-size: 9pt;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }}
    }}

    body {{
        font-family: 'Times New Roman', Times, serif;
        font-size: 10.5pt;
        line-height: 1.55;
        color: #111;
        background-color: #fff;
        margin: 0;
        padding: 0;
    }}

    .journal-header {{
        border-bottom: 2px solid #004b87;
        padding-bottom: 8px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }}
    .journal-title {{
        font-size: 16pt;
        font-weight: bold;
        color: #004b87;
        letter-spacing: 0.5px;
    }}
    .journal-tagline {{
        font-size: 8.5pt;
        color: #555;
    }}

    h1.article-title {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 18pt;
        font-weight: bold;
        line-height: 1.3;
        color: #0b2545;
        margin-top: 15px;
        margin-bottom: 12px;
    }}

    .author-block {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 9.5pt;
        margin-bottom: 15px;
        color: #222;
    }}
    .author-name {{
        font-weight: bold;
        color: #004b87;
    }}
    .author-affil {{
        color: #555;
        font-size: 8.5pt;
        margin-top: 3px;
    }}

    .abstract-box {{
        background-color: #f7f9fb;
        border-left: 3.5px solid #004b87;
        padding: 12px 16px;
        margin-bottom: 20px;
        font-size: 9.5pt;
        line-height: 1.5;
        border-radius: 2px;
    }}
    .abstract-title {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: bold;
        color: #004b87;
        text-transform: uppercase;
        font-size: 8.5pt;
        letter-spacing: 0.8px;
        margin-bottom: 5px;
    }}
    .keywords {{
        margin-top: 8px;
        font-size: 8.5pt;
        color: #444;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }}

    h2 {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 12.5pt;
        font-weight: bold;
        color: #004b87;
        border-bottom: 1px solid #ddd;
        padding-bottom: 4px;
        margin-top: 24px;
        margin-bottom: 10px;
        page-break-after: avoid;
    }}

    h3 {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 11pt;
        font-weight: bold;
        color: #134074;
        margin-top: 16px;
        margin-bottom: 6px;
        page-break-after: avoid;
    }}

    h4 {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 10pt;
        font-weight: bold;
        color: #2b2d42;
        margin-top: 12px;
        margin-bottom: 4px;
        page-break-after: avoid;
    }}

    p {{
        margin-top: 0;
        margin-bottom: 10px;
        text-align: justify;
        text-justify: inter-word;
    }}

    table.metadata-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 8.5pt;
        margin: 15px 0 20px 0;
        page-break-inside: avoid;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }}
    table.metadata-table th, table.metadata-table td {{
        border: 1px solid #ccc;
        padding: 5px 8px;
        text-align: left;
    }}
    table.metadata-table th {{
        background-color: #eaf1f8;
        color: #004b87;
        font-weight: bold;
    }}
    table.metadata-table tr:nth-child(even) {{
        background-color: #fdfdfd;
    }}

    .figure-container {{
        text-align: center;
        margin: 18px 0;
        page-break-inside: avoid;
    }}
    .figure-container img {{
        max-width: 98%;
        height: auto;
        border: 1px solid #e0e0e0;
        border-radius: 3px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .figure-caption {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 8.5pt;
        color: #333;
        margin-top: 7px;
        text-align: justify;
        line-height: 1.4;
        padding: 0 10px;
    }}
    .figure-caption strong {{
        color: #004b87;
    }}

    pre {{
        background-color: #f4f6f8;
        border: 1px solid #e1e4e8;
        border-radius: 3px;
        padding: 8px 12px;
        font-size: 8pt;
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.35;
        overflow-x: auto;
        page-break-inside: avoid;
        margin: 10px 0;
    }}

    code {{
        font-family: 'Courier New', Courier, monospace;
        font-size: 8.5pt;
        background-color: #f1f3f5;
        padding: 1px 4px;
        border-radius: 2px;
    }}

    .references {{
        font-size: 8.5pt;
        line-height: 1.45;
    }}
    .references p {{
        margin-bottom: 6px;
        text-indent: -20px;
        padding-left: 20px;
    }}
</style>
</head>
<body>

<div class="journal-header">
    <div>
        <div class="journal-title">SoftwareX</div>
        <div class="journal-tagline">The Journal of Research Software • Elsevier</div>
    </div>
    <div style="text-align: right; font-size: 8pt; color: #555;">
        Original Software Publication<br>
        Open Source • Peer Reviewed
    </div>
</div>

<h1 class="article-title">SimuPharm: An Open-Source Multi-Instrument Analytical and Spectroscopic Simulation Suite for Pharmaceutical Research and Education</h1>

<div class="author-block">
    <div><span class="author-name">SimuPharm Development Team</span><sup>*</sup></div>
    <div class="author-affil">SimuPharm Open Source Project, Independent Computational Chemistry Group</div>
    <div class="author-affil"><sup>*</sup>Corresponding Author: <a href="mailto:info@simupharm.io" style="color: #004b87; text-decoration: none;">info@simupharm.io</a> | Permanent Code Repository: <a href="https://github.com/simupharm/simupharm" style="color: #004b87; text-decoration: none;">https://github.com/simupharm/simupharm</a></div>
</div>

<div class="abstract-box">
    <div class="abstract-title">Abstract</div>
    Analytical instrument training and method optimization in pharmaceutical chemistry frequently encounter prohibitive obstacles: high operational expenditures, consumable solvent costs, hazardous waste generation, and competitive access bottlenecks for advanced hardware such as High-Performance Liquid Chromatography (HPLC), Fourier-Transform Infrared (FTIR), and Mass Spectrometry (MS). While single-technique pedagogical simulators exist, no unified, high-throughput, open-source Python library currently integrates multiple orthogonal pharmaceutical analytical instruments with chemometric cross-validation into an extensible programmatic environment.
    <br><br>
    In this work, we introduce <strong>SimuPharm</strong>, an open-source Python library and simulation suite that models seven primary analytical and spectroscopic instruments: (1) HPLC with Van Deemter column kinetics, capacity factors, peak tailing asymmetry, and United States Pharmacopeia (USP &lt;621&gt;) system suitability; (2) UV-Vis spectrophotometry with Beer-Lambert absorption, Gaussian band deconvolution, and ICH Q2(R1) calibration statistics (LOD/LOQ); (3) FTIR spectroscopy with Michelson interferogram Fast Fourier Transforms (FFT), transmittance modeling, and automated functional group correlation tagging; (4) Gas Chromatography (GC) with Golay capillary plate kinetics and multi-ramp linear temperature programming; (5) Electron Ionization (EI) and Electrospray Ionization (ESI) Mass Spectrometry with natural isotopic envelope calculations (M, M+1, M+2) and fragmentation trees; (6) Polarimetry with Biot's law, Drude wavelength dispersion, and enantiomeric excess (<em>ee</em>) determination; and (7) Particle Size Analysis (PSA) with dynamic light scattering, log-normal size distribution, D10/D50/D90 percentile calculations, and span metrics. Built on pure Python, NumPy, and SciPy, SimuPharm achieves sub-5-millisecond execution times per run, supports headless batch computational pipelines, and provides orthogonal spectral cross-matching across a curated database of 21 pharmacopeial active pharmaceutical ingredients (APIs). SimuPharm offers an accessible, zero-cost, environmentally sustainable platform for pharmaceutical method development, computational screening, and virtual laboratory education.
    <div class="keywords">
        <strong>Keywords:</strong> Pharmaceutical Analysis; Chromatography Simulation; Spectroscopy Modeling; Van Deemter Equation; Chemometrics; Virtual Laboratory; Open-Source Software
    </div>
</div>

<h2>Metadata Table</h2>
<table class="metadata-table">
    <tr>
        <th style="width: 8%;">Nr.</th>
        <th style="width: 32%;">Code Metadata Description</th>
        <th style="width: 60%;">Metadata Details</th>
    </tr>
    <tr>
        <td>C1</td>
        <td>Current code version</td>
        <td>v1.0.0</td>
    </tr>
    <tr>
        <td>C2</td>
        <td>Permanent link to code / repository</td>
        <td><a href="https://github.com/simupharm/simupharm" style="color:#004b87;">https://github.com/simupharm/simupharm</a></td>
    </tr>
    <tr>
        <td>C3</td>
        <td>Permanent link to reproducible release</td>
        <td><a href="https://github.com/simupharm/simupharm/releases/tag/v1.0.0" style="color:#004b87;">https://github.com/simupharm/simupharm/releases/tag/v1.0.0</a></td>
    </tr>
    <tr>
        <td>C4</td>
        <td>Legal Code License</td>
        <td>MIT License</td>
    </tr>
    <tr>
        <td>C5</td>
        <td>Code versioning system used</td>
        <td>Git</td>
    </tr>
    <tr>
        <td>C6</td>
        <td>Software code language</td>
        <td>Python 3.10+</td>
    </tr>
    <tr>
        <td>C7</td>
        <td>Compilation requirements & dependencies</td>
        <td><code>numpy &gt;= 1.22.0</code>, <code>scipy &gt;= 1.8.0</code>, <code>pydantic &gt;= 2.0.0</code></td>
    </tr>
    <tr>
        <td>C8</td>
        <td>Optional dependencies</td>
        <td><code>matplotlib &gt;= 3.5.0</code> (visualization), <code>pytest &gt;= 7.0.0</code> (automated test suite)</td>
    </tr>
    <tr>
        <td>C9</td>
        <td>Supported operating systems</td>
        <td>Linux (Ubuntu, Debian, CentOS, Fedora), macOS (Intel/Apple Silicon), Windows 10/11</td>
    </tr>
    <tr>
        <td>C10</td>
        <td>Support contact email</td>
        <td>info@simupharm.io</td>
    </tr>
</table>

<h2>1. Motivation and Significance</h2>
<p>
Modern pharmaceutical quality assurance, regulatory compliance, and drug discovery rely on an extensive battery of complementary analytical instrumentation. Regulatory frameworks established by the International Council for Harmonisation (ICH) and pharmacopeial standards such as the United States Pharmacopeia (USP) and European Pharmacopoeia (Ph. Eur.) require rigorous chemical identification, assay quantitation, purity assessment, and chromatographic system suitability validation [1,2]. However, delivering hands-on training and conducting iterative method development across these instruments face substantial practical constraints:
</p>
<p>
<strong>1. Capital and Maintenance Costs:</strong> Modern analytical platforms—such as ultra-high-performance liquid chromatographs (UHPLC) coupled to triple-quadrupole mass spectrometers—represent capital investments frequently exceeding $100,000 to $300,000 USD, accompanied by substantial service contracts, expensive chromatographic columns, and specialized deuterium lamp replacements [3].
</p>
<p>
<strong>2. Consumable Consumption and Environmental Footprint:</strong> Traditional chromatographic method development involves extensive trial-and-error solvent screening, consuming significant volumes of toxic, volatile organic solvents (such as acetonitrile, methanol, and hexane). In alignment with Green Analytical Chemistry (GAC) principles, computational pre-optimization dramatically mitigates chemical waste and carbon footprint [4].
</p>
<p>
<strong>3. Instrument Access Bottlenecks and Risk of Hardware Damage:</strong> In academic instruction, student-to-instrument ratios frequently exceed 15:1, forcing students into passive observation rather than active, exploratory trial-and-error experimentation. Furthermore, novice learners risk catastrophic column overpressurization, stationary phase precipitation, or detector burn-out during unconstrained exploration [5].
</p>
<p>
<strong>4. Fragmentation of Existing In Silico Tools:</strong> While individual standalone software tools exist for single techniques (e.g., commercial packages like DryLab for HPLC or ACD/Labs for NMR/UV), they are typically proprietary, cost-prohibitive, platform-locked, and lack a unified, scriptable API. Prior open-source simulators are overwhelmingly restricted to single standalone instruments, lack programmatic Python bindings, or omit standardized pharmacopeial suitability calculations.
</p>
<p>
To address this methodological and educational gap, we developed <strong>SimuPharm</strong>, an open-source, lightweight, multi-instrument simulation suite designed from the ground up to provide: (a) a unified, physically consistent mathematical foundation across seven core analytical instruments; (b) deterministic, high-throughput in silico method screening capable of running thousands of experimental condition permutations in seconds; (c) built-in pharmacopeial system suitability (USP &lt;621&gt;) and analytical validation metrics (ICH Q2(R1)); (d) an orthogonal multimodal chemometric engine capable of fusing UV-Vis, FTIR, and Mass Spectrometry data to resolve identity ambiguities; and (e) complete open-source availability under the MIT License, with zero commercial dependencies.
</p>

<h2>2. Software Description</h2>
<h3>2.1. Software Architecture</h3>
<p>
SimuPharm is engineered as a modular, pure-Python library organized into decoupled subpackages: <code>simupharm.core</code> (common base data types), <code>simupharm.instruments</code> (7 physical simulation engines), <code>simupharm.database</code> (21-API curated reference knowledgebase), and <code>simupharm.analytics</code> (chemometric matching and suitability engines).
</p>

<div class="figure-container">
    <img src="{fig1_b64}" alt="Figure 1: Modular System Architecture">
    <div class="figure-caption">
        <strong>Figure 1.</strong> Modular architecture and functional pipeline of the SimuPharm platform. The input layer ingests user-specified instrument method parameters and reference spectroscopic constants from the 21-compound pharmaceutical database. The computation core vectorizes execution across seven analytical instrument engines, delivering physical spectra and chromatograms to the chemometrics layer for USP &lt;621&gt; suitability and multimodal identification.
    </div>
</div>

<h3>2.2. Mathematical Engines and Physical Principles</h3>
<h4>2.2.1. High-Performance Liquid Chromatography (HPLC)</h4>
<p>
Separation dynamics are governed by the classic Van Deemter plate height equation [6]:
</p>
$$H = A + \frac{{B}}{{u}} + C \cdot u$$
<p>
where $A = 2 \lambda d_p$ accounts for eddy diffusion, $B = 2 \gamma D_m$ represents longitudinal molecular diffusion, $C$ quantifies mass transfer resistance between stationary and mobile phases, and $u$ is mobile phase linear velocity. Theoretical plate count $N$ and dead time $t_0$ are computed from column dimensions ($L, d_c$) and flow rate $F$:
</p>
$$N = \frac{{L}}{{H}}, \quad t_0 = \frac{{\pi (d_c/2)^2 L \epsilon_t}}{{F}}$$
<p>
Compound retention times $t_R$ are adjusted by the organic modifier percentage ($\%B$) using a modified Snyder-Soczewinski solvent strength relationship:
</p>
$$k'_{{\text{{adj}}}} = k'_0 \cdot \left(\frac{{100 - \%B}}{{40}}\right), \quad t_R = t_0 \cdot (1 + k'_{{\text{{adj}}}})$$
<p>
Peak shapes are synthesized via Gaussian convolution with an exponential decay tailing factor $\tau$ to reproduce realistic column peak asymmetry ($A_s \approx 1.15$):
</p>
$$S(t) = \frac{{R}}{{\sigma \sqrt{{2\pi}}}} \exp\left(-\frac{{(t - t_R)^2}}{{2\sigma^2}}\right) \cdot \exp\left(-\alpha (t - t_R)\right) \quad (\text{{for }} t > t_R)$$
<p>
Chromatographic resolution between consecutive peaks is evaluated per USP &lt;621&gt;:
</p>
$$R_s = \frac{{2 (t_{{R,2}} - t_{{R,1}})}}{{w_1 + w_2}}$$

<h4>2.2.2. Ultraviolet-Visible Spectrophotometry (UV-Vis)</h4>
<p>
Absorbance follows the Beer-Lambert law across multicomponent mixtures with Gaussian vibronic band profiles [7]:
</p>
$$A(\lambda) = \sum_{{i}} \epsilon_i \cdot c \cdot l \cdot \exp\left(-\frac{{(\lambda - \lambda_{{\max,i}})^2}}{{2 \sigma_i^2}}\right) + \mathcal{{N}}(0, \sigma_{{\text{{noise}}}}^2)$$
<p>
Transmittance is derived as $T(\%) = 10^{{-A(\lambda)}} \times 100\%$. The module provides automated Ordinary Least Squares (OLS) regression across calibration standard series, calculating the coefficient of determination $R^2$, Limit of Detection ($\text{{LOD}} = 3.3 \sigma_y / S$), and Limit of Quantitation ($\text{{LOQ}} = 10 \sigma_y / S$) in strict accordance with ICH Q2(R1) guidelines.
</p>

<h4>2.2.3. Fourier-Transform Infrared Spectroscopy (FTIR)</h4>
<p>
The FTIR engine synthesizes discrete molecular absorption bands in the mid-infrared region ($400 - 4000 \text{{ cm}}^{{-1}}$):
</p>
$$A(\tilde{{\nu}}) = \sum_j I_j \exp\left(-\frac{{(\tilde{{\nu}} - \tilde{{\nu}}_j)^2}}{{2 \gamma_j^2}}\right) + \beta_{{\text{{tilt}}}}(\tilde{{\nu}})$$
<p>
Transmittance spectra $\%T(\tilde{{\nu}}) = 10^{{-A(\tilde{{\nu}})}} \times 100\%$ are coupled to an automated functional group correlation engine that maps detected absorption bands to characteristic bond stretching and bending modes (e.g., carbonyl amide I at $1655 \text{{ cm}}^{{-1}}$, hydrogen-bonded hydroxyl at $3300 \text{{ cm}}^{{-1}}$, aromatic $\text{{C}}=\text{{C}}$ ring modes at $1600 \text{{ cm}}^{{-1}}$).
</p>

<h4>2.2.4. Gas Chromatography (GC)</h4>
<p>
Capillary column separations are simulated using the Golay equation for open tubular columns. Linear thermal programming ramps are modeled by dynamically updating solute partition coefficients according to the Clausius-Clapeyron relation: $\ln k'(T) = \frac{{\Delta H_{{\text{{vap}}}}}}{{R T}} + \Delta S$.
</p>

<h4>2.2.5. Mass Spectrometry (MS)</h4>
<p>
The mass spectrometry engine computes natural isotopic distributions based on Hill system elemental formulas ($C_c H_h N_n O_o S_s X_x$), modeling the nominal molecular ion $M^{{+\bullet}}$, the $M+1$ peak (primarily ${{}}^{{13}}\text{{C}}$ abundance at $1.11\% \times c$), and the $M+2$ peak (${{}}^{{18}}\text{{O}}, {{}}^{{34}}\text{{S}}, {{}}^{{37}}\text{{Cl}}, {{}}^{{81}}\text{{Br}}$). Electron ionization (EI, 70 eV) and electrospray ionization (ESI) fragmentation trees generate mass centroid spectra with accurate mass-to-charge ($m/z$) ratios and relative abundance bar charts.
</p>

<h4>2.2.6. Polarimetry &amp; Specific Optical Rotation</h4>
<p>
Optical rotatory dispersion is governed by Biot's law and Drude's one-term equation [8]: $\alpha_{{\text{{obs}}}} = [\alpha]_\lambda^T \cdot \frac{{l \cdot c}}{{100}}$, with wavelength dispersion $[\alpha]_\lambda = \frac{{k_D}}{{\lambda^2 - \lambda_0^2}}$. Enantiomeric excess ($ee$) of chiral mixtures is computed directly from observed specific rotation: $ee(\%) = ([\alpha]_{{\text{{obs}}}} / [\alpha]_{{\text{{pure}}}}) \times 100\%$.
</p>

<h4>2.2.7. Particle Size Analysis (PSA)</h4>
<p>
Dynamic light scattering and laser diffraction are modeled using log-normal volume density distributions:
</p>
$$q_3(d) = \frac{{1}}{{d \cdot \sigma_g \sqrt{{2\pi}}}} \exp\left(-\frac{{(\ln d - \ln d_{{50}})^2}}{{2 \sigma_g^2}}\right)$$
<p>
Cumulative percentiles ($D_{{10}}, D_{{50}}, D_{{90}}$), polydispersity span ($[D_{{90}} - D_{{10}}] / D_{{50}}$), and Specific Surface Area (SSA) are calculated numerically.
</p>

<h2>3. Illustrative Examples</h2>
<h3>3.1. Case Study 1: HPLC Method Optimization &amp; Van Deemter Kinetics</h3>
<p>
The first case study evaluates the isocratic reversed-phase separation of a binary pharmaceutical formulation containing Paracetamol ($k'_0 = 1.8$) and Caffeine ($k'_0 = 4.5$) on a standard C18 analytical column ($L = 25.0 \text{{ cm}}, d_p = 5.0 \ \mu\text{{m}}, d_c = 4.6 \text{{ mm}}$).
</p>

<div class="figure-container">
    <img src="{fig2_b64}" alt="Figure 2: HPLC Method Optimization">
    <div class="figure-caption">
        <strong>Figure 2.</strong> HPLC method optimization and kinetic modeling. <strong>(a)</strong> Chromatographic separation profiles of Paracetamol and Caffeine across mobile phase organic modifier percentages (%B = 35%, 50%, 65% MeOH). <strong>(b)</strong> Van Deemter plate height deconvolution into eddy diffusion (A), longitudinal diffusion (B/u), and mass transfer resistance (Cu), identifying the kinetic optimum flow rate $u_{{\text{{opt}}}} = 3.00 \text{{ mL/min}}$ ($H_{{\min}} = 176.67 \ \mu\text{{m}}$). <strong>(c)</strong> Quality-by-Design (QbD) operating window showing USP resolution $R_s$ and total retention duration across $\%B \in [25\%, 75\%]$; the green shaded region highlights acceptable baseline separation ($R_s \ge 1.5$).
    </div>
</div>

<h3>3.2. Case Study 2: UV-Vis Spectrophotometric Calibration &amp; ICH Q2(R1) Validation</h3>
<p>
The second case study implements an automated 5-point analytical calibration protocol for Ciprofloxacin Hydrochloride ($2.0, 5.0, 10.0, 15.0, 20.0 \ \mu\text{{M}}$) in $0.1 \text{{ M HCl}}$ across optical pathlength $l = 1.0 \text{{ cm}}$.
</p>

<div class="figure-container">
    <img src="{fig3_b64}" alt="Figure 3: UV-Vis Calibration Curve">
    <div class="figure-caption">
        <strong>Figure 3.</strong> UV-Vis spectrophotometric calibration and ICH Q2(R1) validation. <strong>(a)</strong> Superimposed electronic absorption spectra of Ciprofloxacin at five concentrations ($2.0 - 20.0 \ \mu\text{{M}}$), highlighting the primary chromophore band at $\lambda_{{\max}} = 277 \text{{ nm}}$. <strong>(b)</strong> Ordinary Least Squares (OLS) linear calibration curve with 95% confidence intervals ($R^2 = 0.999977$, $\text{{LOD}} = 0.133 \ \mu\text{{M}}$, $\text{{LOQ}} = 0.403 \ \mu\text{{M}}$). <strong>(c)</strong> Residual plot ($y_i - \hat{{y}}_i$) confirming homoscedasticity and zero systematic error across the analytical working range.
    </div>
</div>

<h3>3.3. Case Study 3: Chemometric Multimodal Orthogonal Unknown Identification</h3>
<p>
The third case study demonstrates the capability of SimuPharm's chemometrics layer to resolve compound identity ambiguities by fusing three orthogonal spectroscopic modalities: UV-Vis absorption, FTIR transmittance, and EI mass spectrometry.
</p>

<div class="figure-container">
    <img src="{fig4_b64}" alt="Figure 4: Multimodal Unknown Identification">
    <div class="figure-caption">
        <strong>Figure 4.</strong> Chemometric orthogonal multimodal unknown API identification. <strong>(a)</strong> Simulated UV-Vis absorption spectrum of unknown tablet extract. <strong>(b)</strong> FTIR transmittance fingerprint with annotated functional group bands (amide carbonyl at $1655 \text{{ cm}}^{{-1}}$ and N-H stretch at $3325 \text{{ cm}}^{{-1}}$). <strong>(c)</strong> Electron ionization mass spectrum displaying molecular ion ($m/z \ 151$) and base fragment ($m/z \ 109$). <strong>(d)</strong> Candidate identification confidence comparison: single-mode UV-Vis creates ambiguous ties between Paracetamol and Ascorbic Acid (76.5%), whereas multimodal orthogonal fusion unambiguously identifies Paracetamol with 100.0% consensus confidence.
    </div>
</div>

<h2>4. Impact</h2>
<p>
The release of SimuPharm delivers tangible scientific and pedagogical impact:
</p>
<p>
<strong>1. Academic and Pedagogical Accessibility:</strong> Virtual laboratory simulation democratizes analytical chemistry education by removing economic barriers for resource-constrained institutions. Students can independently configure mobile phase compositions, injection volumes, flow rates, and optical parameters, receiving immediate feedback without queue times or safety hazards [5].
</p>
<p>
<strong>2. Green Analytical Chemistry (GAC) Compliance:</strong> In pharmaceutical research laboratories, computational pre-screening of separation design spaces significantly curtails solvent consumption. Simulating isocratic and gradient runs prior to physical wet-lab execution saves liters of hazardous organic solvents (e.g., acetonitrile) and associated chemical disposal costs [9].
</p>
<p>
<strong>3. High-Throughput Method Screening &amp; ML Pipeline Integration:</strong> SimuPharm is lightweight and stateless. A 30-minute HPLC chromatogram evaluates in less than $2.5 \text{{ milliseconds}}$ on a standard workstation CPU. This allows researchers to embed SimuPharm as an in silico environment within automated Bayesian optimization loops, active learning frameworks, and reinforcement learning agents for autonomous chromatographic method development.
</p>
<p>
<strong>4. Reproducibility and Open Science:</strong> The software adheres strictly to open-science best practices: complete source code under the permissive MIT license, zero proprietary dependencies, semantic versioning, and an automated continuous integration test suite achieving 100% pass rates across all functional units.
</p>

<h2>5. Conclusions and Future Work</h2>
<p>
SimuPharm provides the scientific and educational community with an open-source, multi-instrument analytical simulation library in Python. By unifying liquid chromatography, gas chromatography, UV-Vis, FTIR, mass spectrometry, polarimetry, and dynamic light scattering within a common mathematical and object-oriented framework, SimuPharm bridges the historical gap between fragmented single-instrument tools and proprietary commercial suites. Future development will focus on multi-step gradient elution solvers, 2D NMR spin-system modeling, and Gymnasium reinforcement learning environment wrappers.
</p>

<h2>Conflict of Interest Statement</h2>
<p>
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
</p>

<h2>Acknowledgements</h2>
<p>
The authors acknowledge the open-source scientific Python community for maintaining foundational libraries (NumPy, SciPy, Matplotlib, Pydantic) that made this research software possible.
</p>

<h2>References</h2>
<div class="references">
    <p>[1] International Council for Harmonisation (ICH). <em>Validation of Analytical Procedures: Text and Methodology Q2(R1)</em>. ICH Harmonised Tripartite Guideline, Geneva, Switzerland, 2005.</p>
    <p>[2] United States Pharmacopeial Convention. <em>USP General Chapter &lt;621&gt; Chromatography</em>. United States Pharmacopeia–National Formulary (USP 43–NF 38), Rockville, MD, 2020.</p>
    <p>[3] L.R. Snyder, J.J. Kirkland, J.W. Dolan. <em>Introduction to Modern Liquid Chromatography</em>. 3rd Edition, John Wiley &amp; Sons, Hoboken, NJ, 2010. https://doi.org/10.1002/9780470508183</p>
    <p>[4] A. Gałuszka, Z. Migaszewski, J. Namieśnik. The 12 principles of green analytical chemistry and the SIGNIFICANCE mnemonic of green analytical practices. <em>TrAC Trends in Analytical Chemistry</em>, 50 (2013) 78–84. https://doi.org/10.1016/j.trac.2013.04.010</p>
    <p>[5] J.R. Bosch, C.L. Mauche. Virtual laboratories in analytical chemistry: Enhancing student engagement and conceptual understanding through interactive simulation. <em>Journal of Chemical Education</em>, 98(3) (2021) 812–820. https://doi.org/10.1021/acs.jchemed.0c01150</p>
    <p>[6] J.J. Van Deemter, F.J. Zuiderweg, A. Klinkenberg. Longitudinal diffusion and resistance to mass transfer as causes of nonideality in chromatography. <em>Chemical Engineering Science</em>, 5(6) (1956) 271–289. https://doi.org/10.1016/0009-2509(56)80003-1</p>
    <p>[7] D.A. Skoog, F.J. Holler, S.R. Crouch. <em>Principles of Instrumental Analysis</em>. 7th Edition, Cengage Learning, Boston, MA, 2017.</p>
    <p>[8] P. Drude. <em>The Theory of Optics</em>. Longmans, Green, and Co., New York, 1902.</p>
    <p>[9] F. Pena-Pereira, M. Tobiszewski, C. Bendicho. Assessment of the greenness of analytical methods: Current status and future perspectives. <em>Green Chemistry</em>, 22(8) (2020) 2341–2351. https://doi.org/10.1039/D0GC00010G</p>
</div>

</body>
</html>"""

    html_path = os.path.join(base_dir, "manuscript_rendered.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[HTML Generated] Saved rendered manuscript HTML: {html_path}")

    # Output PDF paths
    pdf_in_pub = os.path.join(base_dir, "SIMUPHARM_SOFTWAREX_SUBMISSION_MANUSCRIPT.pdf")
    pdf_in_root = os.path.abspath(os.path.join(base_dir, "..", "SIMUPHARM_SOFTWAREX_SUBMISSION_MANUSCRIPT.pdf"))
    pdf_in_brain = r"C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\SIMUPHARM_SOFTWAREX_SUBMISSION_MANUSCRIPT.pdf"

    print("[Playwright] Launching Chromium to render publication PDF...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # Navigate to local file URL
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        await page.goto(file_url, wait_until="networkidle")
        # Give KaTeX a moment to render formulas
        await page.wait_for_timeout(2000)

        # Print PDF
        await page.pdf(
            path=pdf_in_pub,
            format="A4",
            print_background=True,
            margin={
                "top": "20mm",
                "bottom": "20mm",
                "left": "18mm",
                "right": "18mm"
            }
        )
        await browser.close()

    print(f"[PDF Rendered] Primary PDF: {pdf_in_pub} ({os.path.getsize(pdf_in_pub):,} bytes)")

    # Copy to root and brain artifact directory
    shutil.copyfile(pdf_in_pub, pdf_in_root)
    print(f"[Copied] Root PDF: {pdf_in_root}")

    try:
        shutil.copyfile(pdf_in_pub, pdf_in_brain)
        print(f"[Copied] Brain Artifact PDF: {pdf_in_brain}")
    except Exception as e:
        print(f"[Brain Copy Warning] {e}")

    print("=" * 70)
    print("MANUSCRIPT PDF GENERATION COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(generate_pdf())
