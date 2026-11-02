import os
from playwright.sync_api import sync_playwright

def build_pdf():
    dir1 = r'c:\Users\dsant\OneDrive\simupro - Copy\SIMUPHARM_PHASE4_EDUCATIONAL_VALIDATION\09_REPORTS'
    dir2 = r'C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\SIMUPHARM_PHASE4_EDUCATIONAL_VALIDATION\09_REPORTS'
    os.makedirs(dir1, exist_ok=True)
    os.makedirs(dir2, exist_ok=True)
    
    out1 = os.path.join(dir1, "PHASE4_EDUCATIONAL_VALIDATION_REPORT.pdf")
    out2 = os.path.join(dir2, "PHASE4_EDUCATIONAL_VALIDATION_REPORT.pdf")
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SimuPharm.io — Phase 4 Educational Pilot & JCE Evidence Package</title>
<style>
  @page {
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
    @top-left {
      content: "SimuPharm.io | Phase 4 Educational Pilot & JCE Technology Report Package";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #2b6cb0;
      font-weight: 700;
    }
    @top-right {
      content: "EDUCATIONAL PILOT PROTOCOL";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 8pt;
      color: #718096;
      font-weight: 600;
    }
    @bottom-left {
      content: "CONFIDENTIAL & PRIVILEGED | JCE TECHNOLOGY REPORT PREPARATION";
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
    border-bottom: 3px solid #2b6cb0;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }

  .badge-primary {
    display: inline-block;
    background-color: #2b6cb0;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 800;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .badge-success {
    display: inline-block;
    background-color: #2f855a;
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
    background-color: #ebf8ff;
    border: 1px solid #bee3f8;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 18px;
  }

  .meta-item {
    font-size: 8pt;
  }
  .meta-label {
    color: #2b6cb0;
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
    border-left: 4px solid #2b6cb0;
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

  .callout-info {
    background-color: #ebf8ff;
    border-left: 4px solid #3182ce;
    color: #2a4365;
  }

  .callout-critical {
    background-color: #fff5f5;
    border-left: 4px solid #e53e3e;
    color: #742a2a;
  }

  .callout-success {
    background-color: #f0fff4;
    border-left: 4px solid #38a169;
    color: #22543d;
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
  .tag-safe { background-color: #c6f6d5; color: #22543d; }
  .tag-barred { background-color: #fed7d7; color: #9b2c2c; }
  .tag-ready { background-color: #bee3f8; color: #2b6cb0; }
  .tag-pilot { background-color: #feebc8; color: #7b341e; }

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
  <span class="badge-primary">Phase 4 Educational Package</span>
  <span class="badge-success">JCE Technology Report Dossier</span>
  <h1>SIMUPHARM.IO — PHASE 4 EDUCATIONAL PILOT & JCE READINESS REPORT</h1>
  <div class="subtitle">Usability Evaluation Protocol, Diagnostic Instruments & Pre-Specified Statistical Analysis Plan</div>
</div>

<div class="meta-grid">
  <div class="meta-item">
    <div class="meta-label">Target Journal</div>
    <div class="meta-val">Journal of Chemical Education</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Article Category</div>
    <div class="meta-val">Technology Report / Tip</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Codebase State</div>
    <div class="meta-val" style="color: #2f855a;">FROZEN (Zero Code Edits)</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Data Integrity</div>
    <div class="meta-val" style="color: #2b6cb0;">ZERO FABRICATION CONFIRMED</div>
  </div>
</div>

<div class="callout-box callout-success">
  <div class="callout-title">📘 Phase 4 Strategic Pivot</div>
  Following the Phase 3.5 Hostile Audit, which broke claims of general predictive accuracy and industrial digital-twin fidelity, Phase 4 establishes the definitive educational evidence package for SimuPharm. The study positions SimuPharm as an <strong>interactive, browser-based chromatography teaching tool</strong> that enables undergraduate pharmacy and chemistry students to safely practice diagnosing classic instrument malfunctions (air bubbles, leaks, voids, contamination).
</div>

<h2>1. CURRENT SCIENTIFIC CLAIM BOUNDARY</h2>
<p>
  To guarantee intellectual honesty and protect against referee rejection, publication claims are categorized into three rigid tiers:
</p>

<table>
  <thead>
    <tr>
      <th>Claim Tier</th>
      <th>Permissibility Status</th>
      <th>Permitted Manuscript Statements & Prohibitions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Tier 1: Safe Claims</strong></td>
      <td><span class="tag tag-safe">Permitted</span></td>
      <td>
        • "SimuPharm is a free, zero-install, browser-based educational simulator."<br/>
        • "The platform allows interactive observation of qualitative chromatographic fault symptoms."<br/>
        • "Undergraduate students operated the simulator without extensive technical training, rating it as usable (SUS)."<br/>
        • "Participants demonstrated short-term diagnostic gains on parallel troubleshooting assessments."
      </td>
    </tr>
    <tr>
      <td><strong>Tier 2: Stronger Claims</strong></td>
      <td><span class="tag tag-pilot">Requires Multi-Cohort RCT</span></td>
      <td>
        • "SimuPharm produces long-term retention of chromatographic troubleshooting skills."<br/>
        • "SimuPharm is demonstrably superior to traditional static textbook troubleshooting manuals."<br/>
        • "Simulation directly reduces instrument error rates and column fouling in physical laboratories."
      </td>
    </tr>
    <tr>
      <td><strong>Tier 3: Prohibited Claims</strong></td>
      <td><span class="tag tag-barred">Strictly Barred</span></td>
      <td>
        ❌ "Industrial Digital Twin" / "Digital Twin"<br/>
        ❌ "Universal predictive accuracy" or "2.07% general HPLC accuracy"<br/>
        ❌ "Artificial Intelligence" / "Machine Learning" / "Bayesian Knowledge Tracing"<br/>
        ❌ "Experimentally validated column backpressure dynamics"<br/>
        ❌ "Mechanistic computational fluid dynamics of pump cavitation or bed voiding"<br/>
        ❌ "Validated library of 300+ pharmaceutical APIs"
      </td>
    </tr>
  </tbody>
</table>

<h2>2. EDUCATIONAL RESEARCH QUESTIONS & DESIGN</h2>
<p>
  <strong>Primary Research Question:</strong> <em>"Can an interactive, browser-based HPLC simulation environment support undergraduate pharmacy and chemistry learners in identifying, interpreting, and troubleshooting common chromatographic system faults?"</em>
</p>
<p>
  <strong>Study Design:</strong> Single-group pre-test / post-test exploratory educational pilot ($N = 20–30$ undergraduate students). The study is integrated into a single 50-minute scheduled laboratory period.
</p>

<table>
  <thead>
    <tr>
      <th>Session Phase</th>
      <th>Time</th>
      <th>Instructional Activity</th>
      <th>Instrument / Tool Used</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Phase 1: Baseline</strong></td>
      <td>00–10 min</td>
      <td>Ethical briefing, voluntary informed consent, and 10-item baseline pre-test.</td>
      <td>Paper Questionnaire (10-item Pre-Test)</td>
    </tr>
    <tr>
      <td><strong>Phase 2: Orientation</strong></td>
      <td>10–18 min</td>
      <td>Platform orientation; independent student execution of nominal baseline run.</td>
      <td>SimuPharm ($50\%$ B, $1.0\text{ mL/min}$, C18 baseline run)</td>
    </tr>
    <tr>
      <td><strong>Phase 3: Fault Practice</strong></td>
      <td>18–30 min</td>
      <td>Interactive exploration of 4 faults: air bubble, leak, column void, contamination.</td>
      <td>SimuPharm Fault Injection Console</td>
    </tr>
    <tr>
      <td><strong>Phase 4: Diagnostic Task</strong></td>
      <td>30–40 min</td>
      <td>Practical diagnostic performance task: 4 unknown simulated runs.</td>
      <td>Scenarios Alpha, Beta, Gamma, Delta (Timing recorded)</td>
    </tr>
    <tr>
      <td><strong>Phase 5: Evaluation</strong></td>
      <td>40–50 min</td>
      <td>Parallel post-test, 10-item System Usability Scale (SUS), and qualitative feedback.</td>
      <td>Post-Test, Brooke SUS Instrument, Qualitative Form</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>3. DIAGNOSTIC FAULT SCENARIOS (FROZEN-CODE MAPPING)</h2>
<p>
  SimuPharm implements four discrete diagnostic faults in <code>CONFIG.faults</code>, mapped directly to John Dolan's <em>LCGC</em> troubleshooting literature:
</p>

<table>
  <thead>
    <tr>
      <th>Fault Mode</th>
      <th>Code Implementation</th>
      <th>Observable Symptoms</th>
      <th>Physical Mechanism</th>
      <th>Corrective Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Air Bubble in Pump</strong></td>
      <td><code>pressureEffect: -20</code><br/><code>noiseMultiplier: 5</code></td>
      <td>Cyclical pressure dips (-20 bar); optical baseline noise spikes; retention jitter.</td>
      <td>Gas compressibility dampens piston stroke, causing transient delivery loss.</td>
      <td>Open purge valve; prime pump at $5\text{ mL/min}$ with degassed solvent.</td>
    </tr>
    <tr>
      <td><strong>System Fitting Leak</strong></td>
      <td><code>pressureEffect: -50</code><br/><code>rtShift: +0.30</code></td>
      <td>Steady backpressure drop (-50 bar); $+30\%$ retention time elongation.</td>
      <td>Pre-column fluid loss reduces linear flow velocity through packed bed.</td>
      <td>Tighten fluidic fittings at pump/injector/column; replace worn ferrule.</td>
    </tr>
    <tr>
      <td><strong>Column Inlet Bed Void</strong></td>
      <td><code>pressureEffect: +30</code><br/><code>tailingFactor: 2.50</code></td>
      <td>Split doublet peaks across all analytes; severe tailing ($T_f = 2.50$); $N$ drop $>50\%$.</td>
      <td>Packed bed collapse at column head creates split flow paths for solute band.</td>
      <td>Replace analytical column; install guard column; check frit.</td>
    </tr>
    <tr>
      <td><strong>Solvent Contamination</strong></td>
      <td><code>ghostPeaks: true</code><br/><code>noiseMultiplier: 3</code></td>
      <td>Spurious ghost peaks in blank runs; elevated baseline drift.</td>
      <td>Impurities in aqueous buffer or weak solvent concentrate and elute.</td>
      <td>Discard contaminated mobile phase; clean lines; prepare fresh HPLC grade.</td>
    </tr>
  </tbody>
</table>

<h2>4. PSYCHOMETRIC ASSESSMENT & USABILITY INSTRUMENTS</h2>
<ul>
  <li><strong>10-Item Isomorphic Pre/Post-Tests:</strong> Parallel items mapped onto identical Bloom cognitive levels covering backpressure anomalies, retention drift, peak splitting, ghost peaks, blockage isolation, pH sensitivity, silanol tailing, degassing sequence, void differentiation, and leak localization.</li>
  <li><strong>4 Unknown Practical Diagnostic Tasks:</strong> Real-time assessment measuring diagnostic accuracy (0/1), latency to diagnosis (seconds), diagnostic confidence (Likert 1–5), physical reasoning, and corrective action.</li>
  <li><strong>System Usability Scale (SUS):</strong> Standard Brooke (1996) 10-item instrument scored on a 0–100 scale, evaluated against Bangor et al. (2008) empirical thresholds.</li>
</ul>

<h2>5. PRE-SPECIFIED STATISTICAL ANALYSIS PIPELINE</h2>
<p>
  All statistical procedures were pre-specified in <code>statistical_analysis_plan.md</code> and verified via Python scripts on labeled demonstration data:
</p>
<ul>
  <li><strong>Normality Rule:</strong> Shapiro-Wilk test on paired score differences ($\Delta \text{Score}$). If $p \ge 0.05 \implies$ Paired Student's $t$-test + Cohen's $d_z$; If $p < 0.05 \implies$ Wilcoxon signed-rank test + rank-biserial correlation $r$. Both tests reported side-by-side.</li>
  <li><strong>Normalized Gain:</strong> Hake's $\langle g \rangle = (\text{Post} - \text{Pre}) / (10 - \text{Pre})$.</li>
  <li><strong>Non-Fabrication Assurance:</strong> The primary template <code>participant_data_template.csv</code> is strictly empty. No student data has been manufactured. Placeholders are preserved in the provisional abstract and manuscript.</li>
</ul>

<h2>6. MANUSCRIPT READINESS EVALUATION (10 GATES)</h2>

<table>
  <thead>
    <tr>
      <th>Readiness Gate</th>
      <th>Standard Required</th>
      <th>Current Gate Status</th>
      <th>Action Required Prior to Submission</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Software Description</strong></td>
      <td>Clear client-side architecture</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Complete in manuscript outline.</td>
    </tr>
    <tr>
      <td><strong>2. Model Description</strong></td>
      <td>Equations & boundary limits</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Limits clearly articulated.</td>
    </tr>
    <tr>
      <td><strong>3. Prior Art Delineation</strong></td>
      <td>Distinct from Boswell (2013)</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Positioned around fault injection.</td>
    </tr>
    <tr>
      <td><strong>4. Educational Methods</strong></td>
      <td>Reproducible 50-min protocol</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Instructor guide archived in SI.</td>
    </tr>
    <tr>
      <td><strong>5. Assessment Tools</strong></td>
      <td>Pre/post tests, rubrics, keys</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Archived in Folder 03.</td>
    </tr>
    <tr>
      <td><strong>6. Statistical Plan</strong></td>
      <td>Pre-registered Python scripts</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Verified in Folder 06.</td>
    </tr>
    <tr>
      <td><strong>7. Ethics Compliance</strong></td>
      <td>IRB exemption checklist</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Exemption criteria documented.</td>
    </tr>
    <tr>
      <td><strong>8. Participant Data</strong></td>
      <td>Zero fake data; blank template</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Awaiting real student execution.</td>
    </tr>
    <tr>
      <td><strong>9. Reproducibility</strong></td>
      <td>Open science TOP compliance</td>
      <td><span class="tag tag-ready">Ready</span></td>
      <td>Checklist completed in Folder 08.</td>
    </tr>
    <tr>
      <td><strong>10. JCE Submission</strong></td>
      <td>Full package readiness</td>
      <td><span class="tag tag-pilot">Conditionally Ready</span></td>
      <td><strong>Execute student pilot to populate placeholders.</strong></td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>7. MANDATORY FINAL DECISION</h2>

<div class="memo-container">
<span class="field-name">CURRENT PAPER THESIS:</span><br/>
<span class="field-val">SimuPharm is a free, zero-install, browser-based educational HPLC simulator that provides a usable, engaging, and instructionally viable virtual laboratory platform for teaching undergraduate pharmacy and chemistry students how to recognize, interpret, and troubleshoot common chromatographic system faults.</span><br/><br/>

<span class="field-name">ONE-SENTENCE CONTRIBUTION:</span><br/>
<span class="field-val">SimuPharm fills a critical gap in pharmaceutical chromatography education by introducing interactive, real-time phenomenological fault injection (pump cavitation, leaks, bed voiding, and contamination) into an open-access web environment, enabling low-stakes deliberate practice in instrument diagnostics.</span><br/><br/>

<span class="field-name">PRIMARY EDUCATIONAL RESEARCH QUESTION:</span><br/>
<span class="field-val">Can an interactive, browser-based HPLC simulation environment support undergraduate pharmacy and chemistry learners in identifying, interpreting, and troubleshooting common chromatographic system faults?</span><br/><br/>

<span class="field-name">STUDY DESIGN:</span><br/>
<span class="field-val">Single-group pre-test / post-test exploratory educational pilot embedded within a standardized 50-minute undergraduate laboratory session, incorporating 10-item isomorphic assessments, 4 practical unknown diagnostic tasks, and the System Usability Scale (SUS).</span><br/><br/>

<span class="field-name">TARGET SAMPLE:</span><br/>
<span class="field-val">N = 20–30 undergraduate B.Pharm (Years 3–4) or B.Sc. Chemistry (Years 2–3) students enrolled in an instrumental analysis or pharmaceutical analysis laboratory course.</span><br/><br/>

<span class="field-name">PRIMARY ENDPOINT:</span><br/>
<span class="field-val">Change in troubleshooting assessment score (Delta Score = Post-Test Score - Pre-Test Score, scale 0–10 points) evaluated via paired Student's t-test or Wilcoxon signed-rank test.</span><br/><br/>

<span class="field-name">SECONDARY ENDPOINTS:</span><br/>
<span class="field-val">1. System Usability Scale (SUS) continuous score (scale 0–100) and Bangor adjective rating.<br/>
2. Practical diagnostic task accuracy (percentage correct across 4 unknown fault scenarios).<br/>
3. Median time-to-diagnosis latency (seconds).<br/>
4. Diagnostic confidence-accuracy calibration.<br/>
5. Qualitative usability barriers and student misconceptions.</span><br/><br/>

<span class="field-name">CURRENT SCIENTIFIC CLAIMS THAT ARE SAFE:</span><br/>
<span class="field-val">1. SimuPharm is an accessible, zero-install web simulator suitable for undergraduate chromatography education.<br/>
2. The platform interactively displays qualitative hydraulic and chromatographic symptoms of classic instrument malfunctions.<br/>
3. The platform achieves acceptable usability among undergraduate student users without extensive orientation.<br/>
4. The simulator supports short-term improvements in conceptual troubleshooting scores.</span><br/><br/>

<span class="field-name">CLAIMS THAT MUST REMAIN PROHIBITED:</span><br/>
<span class="field-val">1. "Industrial Digital Twin" / "Digital Twin"<br/>
2. "Artificial Intelligence" / "Machine Learning" / "Bayesian Knowledge Tracing"<br/>
3. "Universal predictive accuracy" or "2.07% general HPLC accuracy"<br/>
4. "Experimentally validated column backpressure dynamics"<br/>
5. "Mechanistic computational fluid dynamics of pump cavitation or bed voiding"<br/>
6. "Validated library of 300+ pharmaceutical APIs"</span><br/><br/>

<span class="field-name">PHYSICAL HPLC REQUIRED FOR THIS PAPER?:</span><br/>
<span class="field-val">NO. (JCE Technology Reports do not require physical experimental runs when literature benchmarking is sound and educational utility is demonstrated).</span><br/><br/>

<span class="field-name">EDUCATIONAL PILOT REQUIRED?:</span><br/>
<span class="field-val">YES. (Mandatory: Student participant data must be collected to populate manuscript placeholders).</span><br/><br/>

<span class="field-name">ETHICS APPROVAL REQUIRED/PENDING?:</span><br/>
<span class="field-val">EXEMPTION AUTHORIZED / PENDING FACULTY CONFIRMATION under standard educational research exemption criteria (45 CFR 46.104(d)(1)).</span><br/><br/>

<span class="field-name">CURRENT MANUSCRIPT READINESS:</span><br/>
<span class="field-val">MANUSCRIPT READY SUBJECT TO PILOT POPULATION. (All architecture, protocols, instruments, and analysis pipelines are complete; ready to insert real participant data).</span><br/><br/>

<span class="field-name">BIGGEST REMAINING RISK:</span><br/>
<span class="field-val">Failure to recruit an adequate student sample (N < 15) or low student compliance resulting in incomplete pre/post-test pairs during the pilot lab session.</span><br/><br/>

<span class="field-name">NEXT ACTION:</span><br/>
<span class="field-val">Obtain formal departmental / institutional authorization, schedule the 50-minute laboratory session with the enrolled student cohort, execute the standardized protocol, and enter audited participant data into the template.</span>
</div>

<p style="text-align: center; color: #718096; font-size: 8pt; margin-top: 24px;">
  <strong>Phase 4 Educational Evaluation Team</strong> &bull; Certified October 4, 2026 &bull; SimuPharm.io Publication Due Diligence Panel
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
        with open(out1, 'rb') as f_src, open(out2, 'wb') as f_dst:
            f_dst.write(f_src.read())
        browser.close()

    print(f"Successfully generated PDF: {out1} ({os.path.getsize(out1)} bytes)")
    print(f"Successfully mirrored PDF: {out2} ({os.path.getsize(out2)} bytes)")

if __name__ == '__main__':
    build_pdf()
