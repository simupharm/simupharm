import os
from playwright.sync_api import sync_playwright

def build_pdf():
    dir1 = r'c:\Users\dsant\OneDrive\simupro - Copy\audit_output'
    dir2 = r'C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\audit_output'
    os.makedirs(dir1, exist_ok=True)
    os.makedirs(dir2, exist_ok=True)
    
    out1 = os.path.join(dir1, "SIMUPHARM_PHASE3_5_HOSTILE_REVALIDATION_REPORT.pdf")
    out2 = os.path.join(dir2, "SIMUPHARM_PHASE3_5_HOSTILE_REVALIDATION_REPORT.pdf")
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SimuPharm.io — Phase 3.5 Hostile Independent Scientific Re-Validation Audit</title>
<style>
  @page {
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
    @top-left {
      content: "SimuPharm.io | Phase 3.5 Hostile Scientific Audit & Re-Validation";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #9b2c2c;
      font-weight: 700;
    }
    @top-right {
      content: "REVIEWER #2 FORENSIC AUDIT";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #718096;
      font-weight: 600;
    }
    @bottom-left {
      content: "CONFIDENTIAL & PRIVILEGED | SCIENTIFIC DUE DILIGENCE";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 7.5pt;
      color: #a0aec0;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #4a5568;
      font-weight: 600;
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a202c;
    line-height: 1.45;
    font-size: 9.2pt;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  .cover-header {
    border-bottom: 3px solid #9b2c2c;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }

  .badge-danger {
    display: inline-block;
    background-color: #9b2c2c;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 800;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .badge-warning {
    display: inline-block;
    background-color: #c05621;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 800;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
    margin-left: 6px;
  }

  h1 {
    font-size: 19pt;
    font-weight: 800;
    color: #1a202c;
    line-height: 1.15;
    margin: 4px 0 8px 0;
  }

  .subtitle {
    font-size: 11.5pt;
    color: #4a5568;
    font-weight: 600;
    margin-bottom: 12px;
  }

  .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    background-color: #fff5f5;
    border: 1px solid #feb2b2;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 18px;
  }

  .meta-item {
    font-size: 8pt;
  }
  .meta-label {
    color: #742a2a;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 6.8pt;
  }
  .meta-val {
    color: #1a202c;
    font-weight: 600;
    margin-top: 1px;
  }

  h2 {
    font-size: 12.5pt;
    font-weight: 800;
    color: #2d3748;
    border-left: 4px solid #9b2c2c;
    padding-left: 8px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }

  h3 {
    font-size: 10pt;
    font-weight: 700;
    color: #4a5568;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }

  p {
    margin: 0 0 8px 0;
    text-align: justify;
  }

  .callout-box {
    border-radius: 6px;
    padding: 10px 14px;
    margin: 12px 0;
    font-size: 8.8pt;
    page-break-inside: avoid;
  }

  .callout-critical {
    background-color: #fff5f5;
    border-left: 4px solid #e53e3e;
    color: #742a2a;
  }

  .callout-warning {
    background-color: #fffaf0;
    border-left: 4px solid #dd6b20;
    color: #7b341e;
  }

  .callout-info {
    background-color: #ebf8ff;
    border-left: 4px solid #3182ce;
    color: #2a4365;
  }

  .callout-title {
    font-weight: 800;
    text-transform: uppercase;
    font-size: 7.8pt;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 7.8pt;
    page-break-inside: avoid;
  }

  th {
    background-color: #2d3748;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 5px 6px;
    border: 1px solid #cbd5e0;
  }

  td {
    padding: 4px 6px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }

  tr:nth-child(even) {
    background-color: #f7fafc;
  }

  .tag {
    display: inline-block;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 6.8pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .tag-fatal { background-color: #fed7d7; color: #9b2c2c; }
  .tag-major { background-color: #feebc8; color: #7b341e; }
  .tag-match { background-color: #c6f6d5; color: #22543d; }
  .tag-fail { background-color: #fed7d7; color: #9b2c2c; }
  .tag-info { background-color: #e2e8f0; color: #4a5568; }

  .proof-box {
    background-color: #f7fafc;
    border: 1px solid #cbd5e0;
    border-radius: 5px;
    padding: 8px 12px;
    font-family: "Courier New", Courier, monospace;
    font-size: 8pt;
    line-height: 1.4;
    margin: 8px 0 12px 0;
    page-break-inside: avoid;
  }

  .memo-container {
    background-color: #1a202c;
    color: #f7fafc;
    border-radius: 6px;
    padding: 14px 18px;
    margin: 18px 0;
    font-family: "Courier New", Courier, monospace;
    font-size: 8.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
  }
  .memo-container .field-name { color: #f6ad55; font-weight: bold; }
  .memo-container .field-val { color: #ffffff; }

  .page-break {
    page-break-after: always;
  }
</style>
</head>
<body>

<div class="cover-header">
  <span class="badge-danger">Hostile Scientific Audit</span>
  <span class="badge-warning">Reviewer #2 Due Diligence</span>
  <h1>SIMUPHARM.IO — PHASE 3.5 HOSTILE SCIENTIFIC AUDIT REPORT</h1>
  <div class="subtitle">Independent Statistical, Benchmark Provenance & Forensic Re-Validation</div>
</div>

<div class="meta-grid">
  <div class="meta-item">
    <div class="meta-label">Auditor Role</div>
    <div class="meta-val">Independent Adversarial Referee</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Target Audit Document</div>
    <div class="meta-val">Phase 3 Validation Report (MD/PDF)</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Target Codebase</div>
    <div class="meta-val">SimuPharm Engine (Frozen Baseline)</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Audit Decision</div>
    <div class="meta-val" style="color: #c53030;">CLAIMS PARTIALLY BROKEN</div>
  </div>
</div>

<div class="callout-box callout-critical">
  <div class="callout-title">🚨 Hostile Auditor Executive Notice</div>
  This forensic audit was commissioned to determine whether the Phase 3 validation claims survive adversarial scientific re-analysis. 
  <strong>Auditor Conclusion:</strong> Phase 3 contains fatal methodological defects. The headline <strong>2.07% isocratic MAPE is an arithmetic tautology</strong> resulting from reference-state calibration circularity; the flow and temperature sweep benchmarks were <strong>synthesized in Python</strong> to clone the baseline error; and true out-of-sample predictive tests (gradient elution) collapsed with <strong>MAPE = 25.50%</strong> (+61% error on Paracetamol). The simulator cannot be published as an industrial digital twin, but is conditionally viable for the <em>Journal of Chemical Education</em> as an educational troubleshooting simulator if claims are honestly re-framed.
</div>

<h2>1. PRIMARY AUDIT QUESTION & SUMMARY VERDICT</h2>
<p>
  <strong>Primary Question:</strong> Can the Phase 3 Validation Report establish quantitatively defensible, independent experimental validation suitable for peer-reviewed publication in high-impact analytical chemistry literature?
</p>
<p>
  <strong>Auditor Verdict: NO.</strong> The evidence compiled proves that:
</p>
<ul>
  <li><strong>The 2.07% MAPE is not predictive validation:</strong> At 50% B ($\phi = \phi_{\text{ref}} = 0.50$), $\exp(-S(\phi - \phi_{\text{ref}})) = 1.0$, reducing the engine to $t_R = \text{standardRt}$. Comparing this output against monograph values simply verifies the author's dictionary constants.</li>
  <li><strong>Flow and temperature sweep data are synthetic:</strong> Benchmarks across 20 flow runs and 16 temperature runs were created in Python using $1/F$ and $\exp(0.025(30-T))$, manufacturing artificial $p < 10^{-7}$ certainty through pseudoreplication.</li>
  <li><strong>Gradient mode fails:</strong> With MAPE = 25.50% and Paracetamol deviating by +61.05%, the model fails out-of-sample due to hardcoded dead time ($t_0 = 0.50\text{ min}$ vs physical $1.42\text{ min}$) and uncalibrated $S$ parameters.</li>
  <li><strong>Benchmark provenance is composite:</strong> Franeta et al. (2002) assayed Phenobarbital, not Ibuprofen. Ibuprofen was spliced from a Waters marketing note without disclosure.</li>
</ul>

<h2>2. PART 1 — INDEPENDENT RECOMPUTATION & SCHOLARLY DISCREPANCIES</h2>
<p>
  Independent recomputation of all 108 raw simulation points confirms exact arithmetic calculations inside the deposited CSV, but reveals an embarrassing transcription discrepancy in the Phase 3 Report Table 8.1.
</p>

<table>
  <thead>
    <tr>
      <th>Validation Domain</th>
      <th>n</th>
      <th>Metric</th>
      <th>Phase 3 Report (Table 8.1)</th>
      <th>Phase 3 CSV Value</th>
      <th>Audited Value</th>
      <th>Status</th>
      <th>Auditor Root-Cause Analysis</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Isocratic 50% B Standard</strong></td>
      <td>4</td>
      <td>MAE / MAPE</td>
      <td>0.138 min / 2.07%</td>
      <td>0.138 min / 2.07%</td>
      <td><strong>0.138 min / 2.07%</strong></td>
      <td><span class="tag tag-match">Exact Match</span></td>
      <td>Exact arithmetic calculation of 4 point errors.</td>
    </tr>
    <tr>
      <td><strong>Isocratic 50% B Standard</strong></td>
      <td>4</td>
      <td>RMSE / 95% LoA</td>
      <td>0.203 / [-0.45, 0.27]</td>
      <td>0.205 / [-0.51, 0.33]</td>
      <td><strong>0.205 / [-0.51, 0.33]</strong></td>
      <td><span class="tag tag-fail">Discrepancy</span></td>
      <td>Report rounded down RMSE and altered LoA bounds.</td>
    </tr>
    <tr>
      <td><strong>Isocratic Flow Sweep</strong></td>
      <td>20</td>
      <td>MAE / MAPE</td>
      <td>0.215 min / 3.48%</td>
      <td>0.144 min / 2.07%</td>
      <td><strong>0.144 min / 2.07%</strong></td>
      <td><span class="tag tag-fatal">Draft Error</span></td>
      <td>Table 8.1 typed 3.48% to conceal that CSV cloned 2.07%!</td>
    </tr>
    <tr>
      <td><strong>Isocratic Temp Sweep</strong></td>
      <td>16</td>
      <td>MAE / MAPE</td>
      <td>0.285 min / 5.22%</td>
      <td>0.117 min / 2.07%</td>
      <td><strong>0.117 min / 2.07%</strong></td>
      <td><span class="tag tag-fatal">Draft Error</span></td>
      <td>Table 8.1 typed 5.22% to conceal that CSV cloned 2.07%!</td>
    </tr>
    <tr>
      <td><strong>Gradient Elution</strong></td>
      <td>12</td>
      <td>MAE / MAPE</td>
      <td>1.243 min / 25.50%</td>
      <td>1.243 min / 25.50%</td>
      <td><strong>1.243 min / 25.50%</strong></td>
      <td><span class="tag tag-match">Exact Match</span></td>
      <td>Confirms severe out-of-sample gradient divergence.</td>
    </tr>
    <tr>
      <td><strong>All Nominal Baseline</strong></td>
      <td>68 / 52</td>
      <td>MAPE</td>
      <td>10.12% (n=52)</td>
      <td>22.65% (n=68)</td>
      <td><strong>22.65% (n=68)</strong></td>
      <td><span class="tag tag-fatal">Omission</span></td>
      <td>Report dropped 16 divergent low %B runs to claim 10.12%.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>3. PART 2 — MATHEMATICAL PROOF OF CALIBRATION TAUTOLOGY</h2>
<p>
  Phase 3 builds its primary narrative around the 2.07% MAPE achieved on four analgesic APIs at 50% B ($1.0\text{ mL/min}$, $30^\circ\text{C}$).
</p>

<table>
  <thead>
    <tr>
      <th>Analyte</th>
      <th>SimuPharm Hardcoded standardRt</th>
      <th>Benchmark Literature tR</th>
      <th>Simulated Output tR</th>
      <th>Absolute Difference</th>
      <th>Percentage Error</th>
      <th>Parameter Source / Calibration Nature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Paracetamol</strong></td>
      <td>2.800 min</td>
      <td>2.850 min</td>
      <td>2.800 min</td>
      <td>-0.050 min</td>
      <td>-1.75%</td>
      <td>Hardcoded dictionary constant in COMPOUND_LIBRARY.</td>
    </tr>
    <tr>
      <td><strong>Caffeine</strong></td>
      <td>3.500 min</td>
      <td>3.450 min</td>
      <td>3.500 min</td>
      <td>+0.050 min</td>
      <td>+1.45%</td>
      <td>Hardcoded dictionary constant in COMPOUND_LIBRARY.</td>
    </tr>
    <tr>
      <td><strong>Aspirin</strong></td>
      <td>6.200 min</td>
      <td>6.150 min</td>
      <td>6.200 min</td>
      <td>+0.050 min</td>
      <td>+0.81%</td>
      <td>Hardcoded dictionary constant in COMPOUND_LIBRARY.</td>
    </tr>
    <tr>
      <td><strong>Ibuprofen</strong></td>
      <td>9.000 min</td>
      <td>9.400 min</td>
      <td>9.000 min</td>
      <td>-0.400 min</td>
      <td>-4.26%</td>
      <td>Hardcoded constant (responsible for 73% of total MSE).</td>
    </tr>
    <tr>
      <td><strong>Arithmetic Mean</strong></td>
      <td>—</td>
      <td><strong>5.463 min</strong></td>
      <td><strong>5.375 min</strong></td>
      <td><strong>0.138 min</strong></td>
      <td><strong>2.07%</strong></td>
      <td><strong>TAUTOLOGY: Evaluates identity tR = standardRt</strong></td>
    </tr>
  </tbody>
</table>

<div class="proof-box">
<strong>MATHEMATICAL PROOF OF TAUTOLOGICAL EVALUATION:</strong><br/>
1. In hplc_simulator_script.js (lines 820-845):<br/>
   tR = t0 + (compound.standardRt - t0) * Math.exp(-S * (phi - phiRef)) * tempFactor<br/>
2. At baseline validation conditions: phi = 0.50, phiRef = 0.50, tempFactor = 1.000, t0 = 0.50 min.<br/>
3. Therefore: phi - phiRef = 0.00  ==>  Math.exp(-S * 0.0) = 1.000000.<br/>
4. Therefore: tR = 0.50 + (compound.standardRt - 0.50) * 1.0 = compound.standardRt.<br/>
5. CONCLUSION: Under standard isocratic conditions, the simulator is mathematically forced to<br/>
   output standardRt. Testing this against published monograph values is an evaluation of the<br/>
   author's reference constants, NOT an independent test of predictive chromatographic physics!
</div>

<h2>4. PART 3 & 4 — BENCHMARK PROVENANCE & FORENSIC CHAIN</h2>
<p>
  Forensic tracing of benchmark dataset DS-02 reveals critical literature mismatches and unannounced composite splicing:
</p>
<ul>
  <li><strong>The Franeta Citation Fallacy:</strong> Phase 3 cited Franeta et al. (2002) for Paracetamol, Caffeine, Aspirin, and Ibuprofen. <em>Franeta et al. (2002) assayed Phenobarbital, NOT Ibuprofen.</em> Table 2 of Franeta (2002) lists Phenobarbital at 7.82 min. Ibuprofen was secretly imported from Waters App Note 720003922EN.</li>
  <li><strong>Gradient vs Isocratic Conflation:</strong> Franeta (2002) ran a 10%–70% gradient. Phase 3 extracted 2.85 min (Paracetamol) and 6.15 min (Aspirin) and <em>assigned them to BOTH the isocratic and gradient runs</em>, which violates physical retention laws.</li>
  <li><strong>Synthetic Sweeps:</strong> The 20 flow runs and 16 temperature runs were created inside Python script line 211 via $t_{R,\text{exp}} = t_{R,\text{ref}} \times (1/F) \times \exp(0.025(30-T))$. Zero physical runs exist.</li>
</ul>

<h2>5. PART 5, 6 & 7 — TOST EQUIVALENCE, PSEUDOREPLICATION & STATISTICS</h2>

<table>
  <thead>
    <tr>
      <th>Comparison Domain</th>
      <th>Reported N</th>
      <th>True Independent Solutes</th>
      <th>Claimed TOST p-value</th>
      <th>Reproducible p-value</th>
      <th>IID Normality Met?</th>
      <th>Auditor Statistical Verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Isocratic 50% Standard</strong></td>
      <td>4</td>
      <td>4</td>
      <td>0.0116</td>
      <td>0.0116</td>
      <td>NO (n=4 df=3)</td>
      <td><span class="tag tag-fail">Underpowered / Invalid</span></td>
    </tr>
    <tr>
      <td><strong>Flow Rate Sweep</strong></td>
      <td>20</td>
      <td>4</td>
      <td>0.0000</td>
      <td>6.93e-9</td>
      <td>NO (Synthetic pseudodata)</td>
      <td><span class="tag tag-fatal">Fatally Invalid Pseudoreplication</span></td>
    </tr>
    <tr>
      <td><strong>Temperature Sweep</strong></td>
      <td>16</td>
      <td>4</td>
      <td>0.0000</td>
      <td>6.30e-8</td>
      <td>NO (Synthetic pseudodata)</td>
      <td><span class="tag tag-fatal">Fatally Invalid Pseudoreplication</span></td>
    </tr>
    <tr>
      <td><strong>Gradient Elution</strong></td>
      <td>12</td>
      <td>4</td>
      <td>0.1219</td>
      <td>0.1219</td>
      <td>NO (Correlated clusters)</td>
      <td><span class="tag tag-fatal">Equivalence Rejected (p > 0.05)</span></td>
    </tr>
    <tr>
      <td><strong>Full Simulation Suite</strong></td>
      <td>108</td>
      <td>4</td>
      <td>0.2645</td>
      <td>0.2645</td>
      <td>NO (Deterministic runs)</td>
      <td><span class="tag tag-fail">Gross Pseudoreplication</span></td>
    </tr>
  </tbody>
</table>

<div class="callout-box callout-warning">
  <div class="callout-title">⚠️ Forensic Code Discovery — Hardcoded Equivalence Logic</div>
  In <code>generate_phase3_artifacts.py</code> line 681, the statistical conclusion is assigned as: 
  <code>concl = "EQUIVALENT (MAPE < 3.0%)" if mape <= 3.0 else ...</code>. 
  <strong>The script completely ignores whether the TOST p-value was significant.</strong> The conclusion was hardcoded strictly on MAPE. Reporting TOST in the manuscript was decorative theater.
</div>

<div class="page-break"></div>

<h2>6. PART 10, 11, 14 & 15 — GRADIENT, PRESSURE & FAULT FORENSICS</h2>

<h3>Gradient Elution Failure (The Honest Test)</h3>
<p>
  When the simulator is tested away from the $\phi_{\text{ref}} = 0.50$ calibration anchor in gradient mode (10% to 70% B over 10 min):
</p>
<ul>
  <li><strong>Paracetamol:</strong> Simulated 4.59 min vs Experimental 2.85 min $\implies \mathbf{+61.05\% \text{ error}}$ (+1.74 min shift).</li>
  <li><strong>Caffeine:</strong> Simulated 4.88 min vs Experimental 4.60 min $\implies \mathbf{+6.09\% \text{ error}}$.</li>
  <li><strong>Aspirin:</strong> Simulated 6.59 min vs Experimental 6.15 min $\implies \mathbf{+7.15\% \text{ error}}$.</li>
  <li><strong>Ibuprofen:</strong> Simulated 6.91 min vs Experimental 9.40 min $\implies \mathbf{-26.49\% \text{ error}}$ (-2.49 min shift).</li>
  <li><strong>Overall Gradient MAPE:</strong> $\mathbf{25.50\%}$.</li>
</ul>
<p>
  <strong>Root Causes:</strong>
  1) <em>Dead-Time Defect:</em> SimuPharm hardcodes $t_0 = 0.50\text{ min}$ at $1.0\text{ mL/min}$. For a $150 \times 4.6\text{ mm}$ column ($V_0 \approx 1.62\text{ mL}$), physical dead time is $1.42\text{ min}$ (a 300% error). Early eluters are distorted by over 1.7 minutes.  
  2) <em>Dwell Volume Omission:</em> SimuPharm has zero gradient mixer delay ($V_D = 0$).  
  3) <em>Uncalibrated Slopes:</em> $S$ parameters (4.0, 3.5, 5.0, 6.5) were guessed rather than measured.
</p>

<h3>Fluidic Pressure & Fault Injection Reality Check</h3>
<ul>
  <li><strong>Pressure Validation (MAPE = 8.3%):</strong> SimuPharm's Kozeny-Carman calculation was compared against textbook Darcy flow equations. Zero physical pressure sensor data was recorded. <em>This is theoretical consistency, not experimental validation.</em></li>
  <li><strong>Fault Injection Engine:</strong> Hardcoded offsets (-20 bar for air bubble, -50 bar for leak, +30 bar and tailing = 2.5 for column void) are rule-based engineering heuristics. They capture John Dolan's qualitative diagnostic patterns, but are <em>not mechanistic digital twins</em>.</li>
</ul>

<h2>7. PART 18 — 20 LETHAL REVIEWER #2 ATTACKS & DEFENSE</h2>

<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>Topic</th>
      <th>Lethal Reviewer #2 Objection</th>
      <th>Severity</th>
      <th>Fatal to Paper?</th>
      <th>Mandatory Remedy / Strategy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>REV-01</strong></td>
      <td>Circularity</td>
      <td>2.07% MAPE is an artifact of reference-state calibration circularity ($\phi = \phi_{\text{ref}}$).</td>
      <td><span class="tag tag-fatal">Fatal to Predictive Claim</span></td>
      <td>Kills JCA paper; survives as teaching tool.</td>
      <td>Re-frame 50% B as calibration anchor; report out-of-sample errors candidly.</td>
    </tr>
    <tr>
      <td><strong>REV-02</strong></td>
      <td>Synthetic Flow Sweep</td>
      <td>Reporting TOST $p = 0.0000$ on synthetic flow pseudodata borders on scientific fraud.</td>
      <td><span class="tag tag-fatal">Fatal if Uncorrected</span></td>
      <td>Triggers immediate rejection / retraction.</td>
      <td>Purge synthetic flow TOST from manuscript; present as code verification.</td>
    </tr>
    <tr>
      <td><strong>REV-03</strong></td>
      <td>Synthetic Temp Sweep</td>
      <td>Temperature benchmarks were synthesized using the code's own Van 't Hoff formula.</td>
      <td><span class="tag tag-fatal">Fatal if Uncorrected</span></td>
      <td>Kills empirical claims.</td>
      <td>Retract empirical temperature claims; describe as educational feature.</td>
    </tr>
    <tr>
      <td><strong>REV-04</strong></td>
      <td>Composite Provenance</td>
      <td>Franeta (2002) assayed Phenobarbital, not Ibuprofen. Spliced from Waters App Note.</td>
      <td><span class="tag tag-major">Major Defect</span></td>
      <td>Destroys scholarly credibility.</td>
      <td>Transparently disclose composite literature benchmark origins in Methods.</td>
    </tr>
    <tr>
      <td><strong>REV-05</strong></td>
      <td>Gradient Divergence</td>
      <td>Simulator fails in gradient mode with 25.50% MAPE and +61% error on Paracetamol.</td>
      <td><span class="tag tag-fatal">Fatal to Accuracy Claim</span></td>
      <td>Kills analytical chemistry submissions.</td>
      <td>Embrace gradient limitation openly; analyze root causes in Discussion.</td>
    </tr>
    <tr>
      <td><strong>REV-06</strong></td>
      <td>Unphysical Dead Time</td>
      <td>Hardcoded $t_0 = 0.50\text{ min}$ for a $150 \times 4.6\text{ mm}$ column is off by 300% from reality ($1.42\text{ min}$).</td>
      <td><span class="tag tag-major">Major Defect</span></td>
      <td>Prevents physical model claims.</td>
      <td>Acknowledge as simplified educational lumped constant.</td>
    </tr>
    <tr>
      <td><strong>REV-07</strong></td>
      <td>Pressure Validation</td>
      <td>Comparing Darcy equation against Kozeny equation is not experimental validation.</td>
      <td><span class="tag tag-major">Misleading</span></td>
      <td>Blocks empirical pressure claim.</td>
      <td>Re-label as "Fluidic Hydrodynamic Theoretical Verification".</td>
    </tr>
    <tr>
      <td><strong>REV-08</strong></td>
      <td>Heuristic Faults</td>
      <td>Step functions (-20 bar, tailing 2.5) are arbitrary heuristics, not mechanistic digital twins.</td>
      <td><span class="tag tag-fatal">Fatal to Digital Twin</span></td>
      <td>Destroys CFD / mechanistic claims.</td>
      <td>Define as phenomenological troubleshooting training scenarios.</td>
    </tr>
    <tr>
      <td><strong>REV-09</strong></td>
      <td>Zero Lab Data</td>
      <td>Not a single physical injection was made; all data is from literature or synthesized.</td>
      <td><span class="tag tag-major">Scope Limit</span></td>
      <td>Blocks physical measurement journals.</td>
      <td>Target educational / software technology note track.</td>
    </tr>
    <tr>
      <td><strong>REV-10</strong></td>
      <td>Zero Student Data</td>
      <td>No student pre/post quiz scores, learning gains, or classroom evaluations are provided.</td>
      <td><span class="tag tag-fatal">Fatal to Research Paper</span></td>
      <td>Blocks full JCE Research Article.</td>
      <td>Submit as JCE "Technology Report" or run a quick student study.</td>
    </tr>
    <tr>
      <td><strong>REV-11</strong></td>
      <td>TOST Violations</td>
      <td>Running TOST on $N=4$ heterogeneous solutes violates basic distributional assumptions.</td>
      <td><span class="tag tag-major">Statistical Defect</span></td>
      <td>Invalidates statistical inferences.</td>
      <td>Remove formal TOST tests; report Bland-Altman LoA and point errors.</td>
    </tr>
    <tr>
      <td><strong>REV-12</strong></td>
      <td>Pseudoreplication</td>
      <td>Claiming $N=108$ sample size on 4 solutes in a deterministic engine is pseudoreplication.</td>
      <td><span class="tag tag-fatal">Fatal to Statistics</span></td>
      <td>Invalidates degrees of freedom.</td>
      <td>Report true degrees of freedom ($N=4$ analytes across 27 scenarios).</td>
    </tr>
    <tr>
      <td><strong>REV-13</strong></td>
      <td>Novelty vs Boswell</td>
      <td>Boswell (2013) published an open-source web HPLC simulator in JCE with gradient integration.</td>
      <td><span class="tag tag-major">Novelty Threat</span></td>
      <td>Challenges novelty claims.</td>
      <td>Highlight SimuPharm's unique fault injection and full QC workflow.</td>
    </tr>
    <tr>
      <td><strong>REV-14</strong></td>
      <td>Table 8.1 vs CSV</td>
      <td>Table 8.1 reported Flow MAPE = 3.48% while CSV reported 2.07%. Contradicts data.</td>
      <td><span class="tag tag-fatal">Scholar Discrepancy</span></td>
      <td>Triggers fraud suspicion.</td>
      <td>Synchronize all manuscript tables directly with audited CSV data.</td>
    </tr>
    <tr>
      <td><strong>REV-15</strong></td>
      <td>pH Blindness</td>
      <td>No Henderson-Hasselbalch ionization equilibria; blind to mobile phase pH.</td>
      <td><span class="tag tag-major">Boundary Limit</span></td>
      <td>Prevents method development claims.</td>
      <td>Explicitly restrict scope to acidic mobile phases (pH < 2.5).</td>
    </tr>
    <tr>
      <td><strong>REV-16</strong></td>
      <td>Dwell Volume Omission</td>
      <td>Zero dwell volume ($V_D = 0$) guarantees gradient prediction errors.</td>
      <td><span class="tag tag-major">Physical Omission</span></td>
      <td>Explains gradient divergence.</td>
      <td>Feature as scientific explanation in Discussion.</td>
    </tr>
    <tr>
      <td><strong>REV-17</strong></td>
      <td>Missing Solutes</td>
      <td>Cannot simulate Tanaka stationary phase test mix due to missing library solutes.</td>
      <td><span class="tag tag-info">Scope Limit</span></td>
      <td>Limits benchmark scope.</td>
      <td>Clarify study focuses on standard pharmaceutical analgesics.</td>
    </tr>
    <tr>
      <td><strong>REV-18</strong></td>
      <td>Lumped Viscosity</td>
      <td>Ignores axial viscosity gradients across column length during gradient runs.</td>
      <td><span class="tag tag-info">Minor</span></td>
      <td>Minor theoretical critique.</td>
      <td>Acknowledge as simplified lumped hydraulic approximation.</td>
    </tr>
    <tr>
      <td><strong>REV-19</strong></td>
      <td>"Digital Twin" Hype</td>
      <td>Calling a JavaScript page an "Industrial Digital Twin" is marketing hyperbole.</td>
      <td><span class="tag tag-major">Reputational</span></td>
      <td>Causes negative referee bias.</td>
      <td>Purge "Digital Twin"; use "Interactive Educational HPLC Simulator".</td>
    </tr>
    <tr>
      <td><strong>REV-20</strong></td>
      <td>Re-labeling Values</td>
      <td>Assigning 6.15 min and 9.40 min to BOTH isocratic and gradient runs is physically impossible.</td>
      <td><span class="tag tag-fatal">Integrity Risk</span></td>
      <td>Severe referee attack.</td>
      <td>Disclose benchmark assembly openly; separate runs cleanly.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>8. STRATEGIC PIVOT & PUBLICATION ROADMAP</h2>
<ul>
  <li><strong>Physical HPLC Decision: NO. NOT YET JUSTIFIED.</strong> Do not spend lab funds attempting to validate a codebase with unphysical dead time and uncalibrated slopes. It would merely verify physical divergence.</li>
  <li><strong>Target Venue:</strong> Pivot from <em>Journal of Chromatography A</em> to <strong>Journal of Chemical Education (Technology Report Track)</strong>. JCE welcomes accessible web tools with qualitative fault injection and does not require physical experimental runs if literature benchmarking and educational utility are sound.</li>
  <li><strong>Minimum Path to Publication:</strong>
    1) Purge all overclaims ("publication-grade", "digital twin", "experimentally validated pressure", synthetic flow TOST).  
    2) Honestly report 50% B as calibration fidelity and gradient (25.5% MAPE) as a teachable model limitation.  
    3) Conduct a brief 20-student usability / troubleshooting study.  
    4) Submit without modifying a single line of frozen code!
</li>
</ul>

<h2>9. MANDATORY FINAL DECISION MEMO</h2>

<div class="memo-container">
<span class="field-name">PHASE 3 RESULT VALIDATED?:</span><br/>
<span class="field-val">PARTIALLY</span><br/><br/>
<span class="field-name">2.07% MAPE MATHEMATICALLY CORRECT?:</span><br/>
<span class="field-val">YES</span><br/><br/>
<span class="field-name">2.07% MAPE SCIENTIFICALLY REPRESENTATIVE OF GENERAL HPLC ACCURACY?:</span><br/>
<span class="field-val">NO</span><br/><br/>
<span class="field-name">BENCHMARK PROVENANCE:</span><br/>
<span class="field-val">PROBLEMATIC</span><br/><br/>
<span class="field-name">CALIBRATION LEAKAGE:</span><br/>
<span class="field-val">CONFIRMED</span><br/><br/>
<span class="field-name">TOST VALID?:</span><br/>
<span class="field-val">NO</span><br/><br/>
<span class="field-name">PSEUDOREPLICATION:</span><br/>
<span class="field-val">PRESENT</span><br/><br/>
<span class="field-name">PRESSURE VALIDATION:</span><br/>
<span class="field-val">THEORETICAL</span><br/><br/>
<span class="field-name">FAULT VALIDATION:</span><br/>
<span class="field-val">HEURISTIC</span><br/><br/>
<span class="field-name">GRADIENT VALIDATION:</span><br/>
<span class="field-val">FAILED</span><br/><br/>
<span class="field-name">STRONGEST SCIENTIFIC RESULT:</span><br/>
<span class="field-val">The platform successfully implements an interactive, real-time web simulator executing Blake-Kozeny fluidic pressure and phenomenological chromatographic fault symptomology.</span><br/><br/>
<span class="field-name">MOST SERIOUS PROBLEM:</span><br/>
<span class="field-val">The claimed 2.07% isocratic accuracy is an artifact of reference-state calibration circularity, while the flow and temperature sweeps were fabricated via synthetic equation scaling.</span><br/><br/>
<span class="field-name">CURRENT PUBLICATION STATUS:</span><br/>
<span class="field-val">Conditionally viable for Journal of Chemical Education as an educational Technology Report if manuscript claims are honestly re-framed and synthetic statistics are retracted.</span><br/><br/>
<span class="field-name">PHYSICAL HPLC EXPERIMENT:</span><br/>
<span class="field-val">NOT YET JUSTIFIED</span><br/><br/>
<span class="field-name">EDUCATIONAL STUDY:</span><br/>
<span class="field-val">RECOMMENDED</span><br/><br/>
<span class="field-name">NEXT PHASE:</span><br/>
<span class="field-val">Draft a rigorous, intellectually honest educational manuscript for the Journal of Chemical Education targeting the Technology Report track, completely replacing Phase 3 overclaims with Phase 3.5 audited reality.</span>
</div>

<p style="text-align: center; color: #718096; font-size: 8pt; margin-top: 24px;">
  <strong>Independent Hostile Scientific Auditor ("Reviewer #2")</strong> &bull; Certified October 4, 2026 &bull; SimuPharm.io Publication Panel
</p>

</body>
</html>
"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        page.pdf(
            path=out1,
            format="A4",
            print_background=True,
            margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"}
        )
        # Copy to out2
        with open(out1, 'rb') as f_src, open(out2, 'wb') as f_dst:
            f_dst.write(f_src.read())
        browser.close()

    print(f"Successfully generated PDF: {out1} ({os.path.getsize(out1)} bytes)")
    print(f"Successfully mirrored PDF: {out2} ({os.path.getsize(out2)} bytes)")

if __name__ == '__main__':
    build_pdf()
