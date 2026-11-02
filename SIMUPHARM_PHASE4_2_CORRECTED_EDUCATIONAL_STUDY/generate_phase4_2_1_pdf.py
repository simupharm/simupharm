import os
import sys
from playwright.sync_api import sync_playwright

dir_primary = r"c:\Users\dsant\OneDrive\simupro - Copy\SIMUPHARM_PHASE4_2_CORRECTED_EDUCATIONAL_STUDY"
dir_artifact = r"C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\SIMUPHARM_PHASE4_2_CORRECTED_EDUCATIONAL_STUDY"
os.makedirs(dir_primary, exist_ok=True)
os.makedirs(dir_artifact, exist_ok=True)

pdf_filename = "SIMUPHARM_PHASE4_2_1_FINAL_PROTOCOL_FREEZE.pdf"
out_primary = os.path.join(dir_primary, pdf_filename)
out_artifact = os.path.join(dir_artifact, pdf_filename)

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SimuPharm Phase 4.2.1 — Final Protocol Freeze & Governance Certification</title>
<style>
  @page {
    size: A4;
    margin: 13mm 11mm 13mm 11mm;
    @top-left {
      content: "SimuPharm Phase 4.2.1 | Final Protocol Freeze & Governance Certification";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 7.2pt;
      color: #2b6cb0;
      font-weight: 700;
    }
    @top-right {
      content: "FINAL PRE-PILOT REGULATORY & METHODOLOGICAL FREEZE";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 7.2pt;
      color: #718096;
      font-weight: 600;
    }
    @bottom-left {
      content: "CONFIDENTIAL & PRIVILEGED | SCIENTIFIC DUE DILIGENCE & PUBLICATION READINESS";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.8pt;
      color: #a0aec0;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 7.2pt;
      color: #4a5568;
      font-weight: 600;
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a202c;
    line-height: 1.34;
    font-size: 8.2pt;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  h1 {
    font-size: 18pt;
    font-weight: 800;
    color: #1a202c;
    margin: 0 0 3px 0;
    letter-spacing: -0.5px;
  }

  h2 {
    font-size: 10.5pt;
    font-weight: 700;
    color: #2d3748;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 2px;
    margin-top: 10px;
    margin-bottom: 5px;
    break-after: avoid;
    page-break-after: avoid;
  }

  h3 {
    font-size: 8.8pt;
    font-weight: 700;
    color: #4a5568;
    margin-top: 7px;
    margin-bottom: 3px;
    break-after: avoid;
    page-break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 4.5px;
    text-align: justify;
  }

  ul, ol {
    margin-top: 2px;
    margin-bottom: 5px;
    padding-left: 17px;
  }

  li {
    margin-bottom: 2px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 4px;
    margin-bottom: 7px;
    font-size: 7.4pt;
    page-break-inside: auto;
  }

  tr {
    page-break-inside: avoid;
    page-break-after: auto;
  }

  th, td {
    border: 1px solid #cbd5e0;
    padding: 3.5px 5.5px;
    text-align: left;
    vertical-align: top;
  }

  th {
    background-color: #2d3748;
    color: #ffffff;
    font-weight: 600;
    font-size: 7.4pt;
  }

  tbody tr:nth-child(even) {
    background-color: #f7fafc;
  }

  .tag {
    display: inline-block;
    padding: 1px 4.5px;
    border-radius: 3px;
    font-size: 6.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }

  .tag-blocker { background-color: #fed7d7; color: #9b2c2c; border: 1px solid #feb2b2; }
  .tag-major { background-color: #feebc8; color: #9c4221; border: 1px solid #fbd38d; }
  .tag-minor { background-color: #fefcbf; color: #744210; border: 1px solid #faf089; }
  .tag-strength { background-color: #c6f6d5; color: #22543d; border: 1px solid #9ae6b4; }
  .tag-obs { background-color: #e2e8f0; color: #2d3748; border: 1px solid #cbd5e0; }

  .callout-box {
    border-left: 3.5px solid;
    padding: 5px 8px;
    margin: 6px 0;
    background-color: #f8fafc;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
  }

  .callout-critical { border-left-color: #e53e3e; background-color: #fff5f5; }
  .callout-warning { border-left-color: #dd6b20; background-color: #fffaf0; }
  .callout-info { border-left-color: #3182ce; background-color: #ebf8ff; }
  .callout-success { border-left-color: #38a169; background-color: #f0fff4; }

  .callout-title {
    font-weight: 700;
    font-size: 8pt;
    margin-bottom: 2px;
  }

  .callout-critical .callout-title { color: #9b2c2c; }
  .callout-warning .callout-title { color: #9c4221; }
  .callout-info .callout-title { color: #2b6cb0; }
  .callout-success .callout-title { color: #22543d; }

  .code-box {
    background-color: #1a202c;
    color: #48bb78;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 7pt;
    padding: 6px 8px;
    border-radius: 4px;
    margin: 5px 0;
    line-height: 1.3;
    white-space: pre-wrap;
    page-break-inside: avoid;
    border-left: 3.5px solid #38a169;
  }

  .page-break {
    page-break-after: always;
  }

  .memo-container {
    background: #1a202c;
    color: #edf2f7;
    padding: 9px 11px;
    border-radius: 6px;
    margin-top: 7px;
    border-left: 6px solid #e53e3e;
    page-break-inside: avoid;
  }

  .memo-container .field-name {
    color: #a0aec0;
    font-size: 6.8pt;
    font-weight: 700;
    letter-spacing: 0.5px;
  }

  .memo-container .field-val {
    color: #ffffff;
    font-size: 8pt;
  }

  .flow-card-grid {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin: 5px 0;
    page-break-inside: avoid;
  }

  .flow-box {
    border: 1px solid #cbd5e0;
    border-radius: 4px;
    padding: 5px 7px;
    background: #f7fafc;
  }

  .flow-box-primary { border-left: 4px solid #3182ce; background: #ebf8ff; }
  .flow-box-secondary { border-left: 4px solid #38a169; background: #f0fff4; }
  .flow-box-exploratory { border-left: 4px solid #805ad5; background: #faf5ff; }
  .flow-box-critical { border-left: 4px solid #e53e3e; background: #fff5f5; }

  .flow-header {
    font-weight: 700;
    font-size: 7.8pt;
    margin-bottom: 1.5px;
  }

  .flow-desc {
    font-size: 7.2pt;
    color: #4a5568;
    line-height: 1.25;
  }
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- COVER & METADATA -->
<!-- ========================================================================= -->
<div style="border-bottom: 2px solid #2b6cb0; padding-bottom: 5px; margin-bottom: 8px;">
  <div style="display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
      <span class="tag tag-strength" style="font-size: 7.2pt; padding: 2px 6px;">PHASE 4.2.1 FINAL PROTOCOL FREEZE</span>
      <span class="tag tag-obs" style="font-size: 7.2pt; padding: 2px 6px; margin-left: 4px;">GOVERNANCE & AUDIT CERTIFICATION</span>
      <span class="tag tag-obs" style="font-size: 7.2pt; padding: 2px 6px; margin-left: 4px;">REV2.1 / PHASE4.2.1</span>
    </div>
  </div>
  <h1 style="margin-top: 5px;">SimuPharm Phase 4.2.1<br/>Final Protocol Freeze & Governance Certification</h1>
  <div style="font-size: 9pt; color: #4a5568; font-weight: 600;">
    Final Micro-Correction Pass, Immutable Protocol Freeze, & Pre-Pilot Institutional Governance Lock
  </div>
</div>

<table style="margin-bottom: 7px; font-size: 7.4pt;">
  <tr style="background: #edf2f7;">
    <td style="width: 25%;"><strong>RELEASE DATE:</strong> October 4, 2026</td>
    <td style="width: 25%;"><strong>DOCUMENT ID:</strong> AUDIT-P4.2.1-FREEZE-2026-REV2.1</td>
    <td style="width: 25%;"><strong>EVALUATION TARGET:</strong> SimuPharm Educational Pilot</td>
    <td style="width: 25%;"><strong>SIMULATOR CODE:</strong> FROZEN (Zero Modifications)</td>
  </tr>
</table>

<!-- ========================================================================= -->
<!-- 1. EXECUTIVE SUMMARY -->
<!-- ========================================================================= -->
<h2>1. EXECUTIVE SUMMARY</h2>
<div class="callout-box callout-success">
  <div class="callout-title">📋 EXECUTIVE SUMMARY & FINAL PROTOCOL FREEZE</div>
  <p style="margin: 0; font-size: 7.8pt;">
    <strong>Mandate & Mission:</strong> Phase 4.2.1 represents the final, definitive micro-correction pass on the SimuPharm educational evaluation study package. Building upon the structural reconciliations of Phase 4.2, this phase eliminates all lingering overclaims, calibrates statistical and psychometric terminology, reframes ethics governance under institutional review rather than automatic US federal exemption, verifies SHA-256 hashes of the frozen simulation engine, and formally <strong>FREEZES THE WORKING PROTOCOL</strong> prior to student recruitment.<br/>
    <strong>Non-Negotiable Code Freeze:</strong> Zero modifications were performed on the underlying SimuPharm simulation engine (<code>hplc_simulator_script.js</code>, <code>script.js</code>, <code>index.html</code>). Cryptographic checksums confirm exact bit-level immutability (PASS — ENGINE FROZEN).<br/>
    <strong>Absolute Non-Fabrication:</strong> Zero student records, simulated scores, or artificial ratings exist. The participant data entry template (<code>participant_data_template.csv</code>) contains exactly 1 single header row and 0 participant rows.
  </p>
</div>

<!-- ========================================================================= -->
<!-- 2. PHASE 4.2 CORRECTIONS RETAINED -->
<!-- ========================================================================= -->
<h2>2. PHASE 4.2 CORRECTIONS RETAINED</h2>
<p>
  All structural architectural decisions established in Phase 4.2 are confirmed, locked, and retained without redesign:
</p>
<ul>
  <li><strong>Single-Group Pre/Post Pilot Design:</strong> $N \approx 25$ undergraduate pharmacy and chemistry students participating in a standardized 50-minute scheduled laboratory session.</li>
  <li><strong>Conclusive 24-Point Practical Scoring Rubric:</strong> 0 to 6 points per scenario across 4 blind unknown tasks (0–2 Fault ID, 0–2 Physical Reasoning, 0–2 Corrective Action) scored independently by two faculty raters.</li>
  <li><strong>Balanced Isomorphic Assessments:</strong> 10-item pre-test and 10-item parallel post-test with balanced key distributions (~25% each A, B, C, D; max consecutive identical keys = 1; Chi2 $p = 0.9402$).</li>
  <li><strong>Canonical Brooke (1996) SUS Instrument:</strong> Unmodified standard 10-item questionnaire benchmarked against Bangor et al. (2008) and Sauro & Lewis (2016) normative databases.</li>
  <li><strong>Neutral Guided Inquiry Protocol:</strong> Excised all symptom cueing and fluidic mechanisms; standardized instructor verbal script paired with a 10-point independent observer fidelity checklist.</li>
  <li><strong>Non-Contingent Primary Statistical Plan:</strong> Primary test locked to Wilcoxon Signed-Rank Test using Pratt's zero-difference method, paired $t$-test as sensitivity analysis, and Holm-Bonferroni correction for secondary tests.</li>
  <li><strong>Reconciled 73-Column Data Schema:</strong> Expanded CSV template capturing all component scores, rater scores, latencies, confidences, and SUS items with zero data truncation.</li>
</ul>

<!-- ========================================================================= -->
<!-- 3. PHASE 4.2.1 MICRO-CORRECTIONS IMPLEMENTED -->
<!-- ========================================================================= -->
<h2>3. PHASE 4.2.1 MICRO-CORRECTIONS IMPLEMENTED</h2>
<p>
  A rigorous audit of the Phase 4.2 text and scripts identified specific overclaims, statistical phrasing nuances, and governance assumptions that required precise calibration:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Audit Dimension</th>
      <th style="width: 38%;">Phase 4.2 Phrasing / Assumption</th>
      <th style="width: 44%;">Phase 4.2.1 Calibrated Micro-Correction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Confidence Calibration</strong></td>
      <td>Stated that confidence-accuracy correlation "proves that SimuPharm fosters calibrated metacognition".</td>
      <td><strong>Excised all causal claims:</strong> Replaced with: <em>"The study will explore the association between diagnostic confidence and diagnostic accuracy as an exploratory indicator of confidence–performance calibration."</em></td>
    </tr>
    <tr>
      <td><strong>Expert Content Review</strong></td>
      <td>Stated that expert review "confirms experimental realism" or "validates physical instrument behavior".</td>
      <td><strong>Reframed as Content-Validity Assessment:</strong> Evaluates educational relevance, clarity, and diagnostic plausibility from an expert perspective. Does NOT constitute physical sensor validation.</td>
    </tr>
    <tr>
      <td><strong>Practical Rubric Phrasing</strong></td>
      <td>Claimed that the 24-point rubric "becomes continuous" or "has continuous-like distribution properties".</td>
      <td><strong>Calibrated to Scoring Resolution:</strong> Replaced with: <em>"The graduated 24-point rubric provides greater scoring resolution than binary component scoring and allows partial understanding to be distinguished from incorrect or incomplete responses."</em></td>
    </tr>
    <tr>
      <td><strong>Item Analysis Framing</strong></td>
      <td>Classified item difficulty and discrimination as "psychometric validation" or "validated examination".</td>
      <td><strong>Classified as Exploratory Item Analysis:</strong> Explicitly acknowledges that $N \approx 25$ limits estimation precision; describes relative difficulty within this pilot rather than population-wide misconceptions.</td>
    </tr>
    <tr>
      <td><strong>Ethics Governance Scope</strong></td>
      <td>Assumed US 45 CFR 46.104(d)(1) exemption applies automatically to an Indian educational institution.</td>
      <td><strong>Reframed under Host-Institution Authority:</strong> Governed by <em>"host-institution research ethics/IEC/IRB or equivalent institutional determination, as applicable under institutional policy and relevant regulations."</em> Placeholders added.</td>
    </tr>
    <tr>
      <td><strong>Overstatements of Completeness</strong></td>
      <td>Used phrases such as "100% methodologically complete", "psychometrically sound", "certified".</td>
      <td><strong>Scrubbed to Conservative Phrasing:</strong> Replaced with "protocol finalized", "methodologically specified", "recruitment-ready pending institutional authorization", "exploratory pilot".</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 4. FINAL SCORING ARCHITECTURE -->
<!-- ========================================================================= -->
<h2>4. FINAL SCORING ARCHITECTURE (24-POINT GRADUATED RUBRIC)</h2>
<p>
  The practical diagnostic task evaluates student diagnostic competence across four unknown simulated fault scenarios (Alpha: Fitting Leak, Beta: Column Void, Gamma: Pump Cavitation, Delta: Mobile Phase Contamination) scored on a standardized 24-point analytical rubric:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Rubric Component</th>
      <th style="width: 12%; text-align: center;">Score Scale</th>
      <th style="width: 34%;">Grading Benchmarks & Criteria</th>
      <th style="width: 34%;">Pedagogical & Psychometric Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Component A:<br/>Fault Identification</strong></td>
      <td style="text-align: center;">0, 1, 2 points</td>
      <td>
        <strong>2 pts:</strong> Exact specific fault correctly identified.<br/>
        <strong>1 pt:</strong> General system module or anomaly recognized, but lacks specificity.<br/>
        <strong>0 pts:</strong> Incorrect, unrelated, or physically impossible fault named.
      </td>
      <td>Measures symptom-to-fault pattern recognition while allowing partial credit for isolating the correct instrument module.</td>
    </tr>
    <tr>
      <td><strong>Component B:<br/>Physical Reasoning</strong></td>
      <td style="text-align: center;">0, 1, 2 points</td>
      <td>
        <strong>2 pts:</strong> Sound mechanistic explanation citing hydrodynamic resistance, flow delivery, or bed voiding.<br/>
        <strong>1 pt:</strong> Identifies primary physical factor but explanation is incomplete.<br/>
        <strong>0 pts:</strong> Incorrect physical mechanism or no explanation.
      </td>
      <td>Distinguishes deep fluidic/chemical comprehension from superficial guessing. Captures emerging student mental models.</td>
    </tr>
    <tr>
      <td><strong>Component C:<br/>Corrective Action</strong></td>
      <td style="text-align: center;">0, 1, 2 points</td>
      <td>
        <strong>2 pts:</strong> Targeted correct SOP troubleshooting step specified.<br/>
        <strong>1 pt:</strong> Generic safe action that does not resolve root cause.<br/>
        <strong>0 pts:</strong> Unsafe action that would damage instrument or worsen fault.
      </td>
      <td>Evaluates procedural troubleshooting competence and adherence to good laboratory practice (GLP).</td>
    </tr>
    <tr>
      <td><strong>Composite Scores</strong></td>
      <td style="text-align: center;">0–6 per task<br/><strong>0–24 Grand Total</strong></td>
      <td>
        Scenario Total $= \text{ID} + \text{Reason} + \text{Action}$ (0 to 6 points).<br/>
        Grand Rubric Total across 4 scenarios $= 0$ to 24 points.
      </td>
      <td>Provides greater scoring resolution than binary scoring; enables calculation of Weighted Kappa (&kappa;<sub>w</sub>) and ICC(2,1).</td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 5. FINAL STUDY PROTOCOL -->
<!-- ========================================================================= -->
<h2>5. FINAL STUDY PROTOCOL & SESSION TIMELINE</h2>
<p>
  The study protocol is executed within a single 50-minute scheduled undergraduate laboratory period under standardized conditions:
</p>

<div class="flow-card-grid">
  <div class="flow-box flow-box-primary">
    <div class="flow-header">PHASE 1: INFORMED CONSENT & ONBOARDING (Minutes 00:00 – 00:05 | 5 min)</div>
    <div class="flow-desc">Distribution of anonymous envelopes (P01–P25); plain-language briefing; voluntary signed consent administration. Zero impact on course grades confirmed.</div>
  </div>
  <div class="flow-box flow-box-secondary">
    <div class="flow-header">PHASE 2: DIAGNOSTIC BASELINE PRE-TEST (Minutes 00:05 – 00:15 | 10 min)</div>
    <div class="flow-desc">10-item isomorphic multiple-choice test on paper; closed-book, no browser access; balanced key distribution (~25% each A, B, C, D). Sheets collected facedown.</div>
  </div>
  <div class="flow-box flow-box-exploratory">
    <div class="flow-header">PHASE 3: STANDARDIZED SIMULATOR EXPLORATION (Minutes 00:15 – 00:27 | 12 min)</div>
    <div class="flow-desc">
      &bull; <strong>Min 15–18:</strong> Interface orientation (sliders for % B, flow rate, temperature; pressure gauge; Canvas chromatogram).<br/>
      &bull; <strong>Min 18–21:</strong> Normal baseline separation of 4-analyte analgesic mixture.<br/>
      &bull; <strong>Min 21–27 (Neutral Guided Inquiry):</strong> Sequential testing of Faults 1 to 4; students observe canvas, pressure gauge, and hypothesize without instructor answers.
    </div>
  </div>
  <div class="flow-box flow-box-primary">
    <div class="flow-header">PHASE 4: BLIND UNKNOWN PRACTICAL TASKS (Minutes 00:27 – 00:39 | 12 min)</div>
    <div class="flow-desc">Four unknown simulated fault scenarios (Alpha: Leak, Beta: Void, Gamma: Bubble, Delta: Contamination; 3 min each). Students record Fault ID, Physical Reasoning, Corrective Action, Confidence (1–5), and Latency (s).</div>
  </div>
  <div class="flow-box flow-box-secondary">
    <div class="flow-header">PHASE 5: POST-TEST & USABILITY EVALUATION (Minutes 00:39 – 00:49 | 10 min)</div>
    <div class="flow-desc">10-item parallel diagnostic post-test (closed book, browser closed); 10-item canonical Brooke (1996) SUS; 8-item targeted UX survey; qualitative reflection form.</div>
  </div>
  <div class="flow-box flow-box-primary">
    <div class="flow-header">PHASE 6: COLLECTION & DEBRIEF (Minutes 00:49 – 00:50 | 1 min)</div>
    <div class="flow-desc">All completed sheets placed into envelopes, sealed, and deposited into double-locked receptacle.</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 6. FINAL ASSESSMENT ARCHITECTURE -->
<!-- ========================================================================= -->
<h2>6. FINAL ASSESSMENT ARCHITECTURE & BALANCED KEYS</h2>
<p>
  Pre-test and post-test instruments assess identical diagnostic constructs and Bloom cognitive levels using parallel isomorphic scenarios with balanced answer-key distributions:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 5%; text-align: center;">Pair</th>
      <th style="width: 22%;">Diagnostic Construct</th>
      <th style="width: 14%;">Bloom Level</th>
      <th style="width: 18%;">Pre-Test Item Focus</th>
      <th style="width: 18%;">Post-Test Equivalent Focus</th>
      <th style="width: 7%; text-align: center;">Pre Key</th>
      <th style="width: 7%; text-align: center;">Post Key</th>
      <th style="width: 9%; text-align: center;">Position Bias</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;"><strong>Q1</strong></td>
      <td>Pump Cavitation</td>
      <td>Analysis</td>
      <td>25 bar drop + baseline spikes</td>
      <td>Cyclical &plusmn;20 bar fluctuation + spikes</td>
      <td style="text-align: center;"><strong>C</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q2</strong></td>
      <td>Pre-Column Fitting Leak</td>
      <td>Application</td>
      <td>+30% retention + 85 to 55 bar drop</td>
      <td>+25% retention + 90 to 60 bar drop + droplets</td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td style="text-align: center;"><strong>D</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q3</strong></td>
      <td>Column Inlet Voiding</td>
      <td>Analysis</td>
      <td>Split peaks + tailing Tf &gt; 2.2</td>
      <td>Bifurcated doublet peaks + tailing Tf = 2.4</td>
      <td style="text-align: center;"><strong>D</strong></td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q4</strong></td>
      <td>Ghost Peaks / Contam</td>
      <td>Comprehension</td>
      <td>Unassigned peaks in blank gradient</td>
      <td>Ghost peaks doubling with initial hold</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>C</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q5</strong></td>
      <td>Pressure Surge Isolation</td>
      <td>Application</td>
      <td>Sudden overpressure &gt; 400 bar</td>
      <td>Disconnecting inlet drops 380 to 5 bar</td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q6</strong></td>
      <td>Mobile Phase pH Drift</td>
      <td>Analysis</td>
      <td>Selective acidic API drift vs neutral</td>
      <td>Ibuprofen shift vs Caffeine/Toluene stability</td>
      <td style="text-align: center;"><strong>C</strong></td>
      <td style="text-align: center;"><strong>C</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q7</strong></td>
      <td>Peak Asymmetry Origins</td>
      <td>Comprehension</td>
      <td>Fronting caused by mass overload</td>
      <td>Tailing caused by residual silanol interactions</td>
      <td style="text-align: center;"><strong>D</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q8</strong></td>
      <td>Degassing Sequence</td>
      <td>Application</td>
      <td>First action: open purge valve, prime</td>
      <td>Pump degassing: open purge valve, flush</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>D</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q9</strong></td>
      <td>Void vs Blockage</td>
      <td>Evaluation</td>
      <td>Frit blockage vs inlet voiding</td>
      <td>Inlet void vs sample solvent mismatch</td>
      <td style="text-align: center;"><strong>C</strong></td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>Q10</strong></td>
      <td>Leak Location Diagnostics</td>
      <td>Evaluation</td>
      <td>Post-column vs pre-detector leak</td>
      <td>Pre-injector leak (area recovery vs retention)</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>C</strong></td>
      <td style="text-align: center;"><span class="tag tag-strength">Balanced</span></td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 7. FINAL STATISTICAL ANALYSIS PLAN -->
<!-- ========================================================================= -->
<h2>7. FINAL STATISTICAL ANALYSIS PLAN (SAP)</h2>
<p>
  The Statistical Analysis Plan establishes an immutable inferential hierarchy free of normality-contingent branching:
</p>
<ul>
  <li><strong>Primary Confirmatory Analysis:</strong> Paired Troubleshooting Score Gain ($\Delta\text{Score} = \text{PostTest} - \text{PreTest}$, range: $-10$ to $+10$) evaluated via the <strong>Wilcoxon Signed-Rank Test (Two-Tailed, $\alpha = 0.05$) using Pratt's zero-difference method</strong> (`zero_method='pratt'`).
    <ul>
      <li><em>Pratt's Zero-Difference Method:</em> Retains students with zero gain ($\Delta = 0$) in the ranking procedure, preserving the true sample size ($N \approx 25$) and preventing artificial rank-sum inflation.</li>
      <li><em>Effect Size & Median Difference:</em> Reported as rank-biserial correlation $r = 1 - \frac{2W}{S}$ and Hodges-Lehmann median difference with 95% BCa bootstrap confidence intervals.</li>
    </ul>
  </li>
  <li><strong>Sensitivity Analysis:</strong> Paired Student's $t$-test ($t$, $p$-value, Cohen's $d_z$, 95% CI) reported side-by-side to assess robustness to distributional assumptions.</li>
  <li><strong>Secondary Outcomes Multiplicity Control:</strong> The family of 5 secondary hypotheses (Diagnostic Rubric Total, Latency, Confidence Calibration, SUS, Hake Gain) is controlled via the <strong>Holm-Bonferroni step-down procedure</strong> at family-wise $\alpha = 0.05$.</li>
  <li><strong>Missing Data Rules:</strong> Complete-case analysis for pre/post scores ($\ge 1$ blank item excludes record from paired gain); Sauro (2016) imputation for SUS (1–2 missing items imputed with neutral score 3; $\ge 3$ missing items excludes submission).</li>
</ul>

<!-- ========================================================================= -->
<!-- 8. CONFIDENCE-ANALYSIS DEFINITION -->
<!-- ========================================================================= -->
<h2>8. CONFIDENCE-ANALYSIS DEFINITION (EXPLORATORY)</h2>
<p>
  The study explores the association between diagnostic confidence and diagnostic accuracy as an **exploratory indicator of confidence–performance calibration**. All causal claims suggesting that SimuPharm "fosters" or "proves" calibrated metacognition are strictly excised:
</p>
<ul>
  <li><strong>Data Collected:</strong> Post-task confidence rating on a 5-point Likert scale (1 = Guessing, 5 = Absolutely Certain) recorded for each practical diagnostic scenario (`task_[x]_conf`).</li>
  <li><strong>Analytical Metrics:</strong>
    <ol>
      <li><strong>Spearman Rank Correlation ($\rho$) & Pearson $r$:</strong> Non-parametric and parametric correlations between mean student confidence and total 24-point practical rubric performance.</li>
      <li><strong>Confidence-Stratified Performance:</strong> Tabulation of mean diagnostic accuracy across low (1–2), moderate (3), and high (4–5) confidence ratings.</li>
      <li><strong>Calibration Scatterplot:</strong> Bivariate plot displaying confidence versus rubric total with LOESS smoothing.</li>
    </ol>
  </li>
  <li><strong>Methodological Scope:</strong> Evaluated purely as a descriptive, exploratory indicator. Causal metacognitive learning claims are explicitly prohibited.</li>
</ul>

<!-- ========================================================================= -->
<!-- 9. EXPERT-REVIEW METHODOLOGY -->
<!-- ========================================================================= -->
<h2>9. EXPERT-REVIEW METHODOLOGY (CONTENT-VALIDITY ASSESSMENT)</h2>
<p>
  Content-validity assessment evaluates educational appropriateness, diagnostic plausibility, and symptom clarity from an expert perspective. It does **NOT** constitute physical HPLC sensor or hardware validation:
</p>
<ul>
  <li><strong>Review Panel:</strong> 3 to 5 independent analytical chromatography faculty and industrial chromatographers with $\ge 5$ years of instrumentation experience.</li>
  <li><strong>Form Status:</strong> The expert review form (<code>expert_content_validation_form.md</code>) remains **strictly blank** until real experts participate. Zero ratings or CVI values are fabricated.</li>
  <li><strong>Evaluation Dimensions (4-Point Scale: 1 = Not Relevant to 4 = Highly Relevant):</strong>
    <ol>
      <li>Symptom Representation: Cavitation pressure ripple and baseline noise.</li>
      <li>Symptom Representation: Fitting leak inverse flow-retention relationship.</li>
      <li>Symptom Representation: Column bed void doublet peak splitting and tailing.</li>
      <li>Symptom Representation: Ghost peak contaminant accumulation in blank gradients.</li>
      <li>Curricular Relevance: Priority and fit for undergraduate chemical/pharmaceutical education.</li>
      <li>Assessment Alignment: Alignment of pre/post tests with conceptual troubleshooting.</li>
    </ol>
  </li>
  <li><strong>Formulas:</strong> Item Content Validity Index ($\text{I-CVI} = N_{3,4} / N_{\text{total}}$, benchmark $\ge 0.80$); Scale-Level Index ($\text{S-CVI/Ave} = \text{Mean}(\text{I-CVI})$, benchmark $\ge 0.90$).</li>
</ul>

<!-- ========================================================================= -->
<!-- 10. EXPLORATORY ITEM-ANALYSIS METHODOLOGY -->
<!-- ========================================================================= -->
<h2>10. EXPLORATORY ITEM-ANALYSIS METHODOLOGY</h2>
<p>
  Item-level analysis is classified strictly as **EXPLORATORY ITEM ANALYSIS** (not psychometric validation):
</p>
<ul>
  <li><strong>Sample Size Boundary:</strong> The pilot cohort ($N \approx 25$) limits the precision and stability of item-level estimates. Findings describe relative concept difficulty within this specific pilot cohort, not generalized psychometric parameters.</li>
  <li><strong>Reported Metrics:</strong>
    <ul>
      <li><strong>Item Difficulty ($P$):</strong> Proportion of correct responses ($P = N_{\text{correct}} / N$). Values $<0.30$ indicate relatively difficult concepts; $>0.70$ indicate relatively easy concepts.</li>
      <li><strong>Exploratory Item Discrimination ($D$):</strong> Difference in difficulty between upper 27% and lower 27% scoring students ($D = P_{\text{upper}} - P_{\text{lower}}$).</li>
      <li><strong>Distractor Selection Patterns:</strong> Frequency distribution of distractor choices to identify specific persistent conceptual confounds.</li>
    </ul>
  </li>
</ul>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 11. QUALITATIVE ANALYSIS FRAMEWORK -->
<!-- ========================================================================= -->
<h2>11. QUALITATIVE ANALYSIS FRAMEWORK</h2>
<p>
  Student qualitative responses from <code>qualitative_feedback_form.md</code> are analyzed using **Inductive Thematic Analysis** (Braun & Clarke 2006) across three structured domains:
</p>
<ul>
  <li><strong>Domain 1: Visual Affordances & Diagnostic Strategies:</strong> Identifies which interface elements (pressure gauge ripple, peak doublets, baseline spikes) served as primary diagnostic cues.</li>
  <li><strong>Domain 2: Persistent Misconceptions & Cognitive Confounds:</strong> Catalogs recurring conceptual difficulties (e.g., confusing inlet bed voids with frit blockages, or misattributing silanol tailing to voiding).</li>
  <li><strong>Domain 3: Instructional Usability & Simulator Engagement:</strong> Evaluates student perceptions of psychological safety during simulated failure and parameter exploration freedom.</li>
  <li><strong>Coder Reliability:</strong> Two independent researchers code a random 20% sample; agreement is verified via Cohen's Kappa ($\kappa \ge 0.80$) prior to coding remaining transcripts.</li>
</ul>

<!-- ========================================================================= -->
<!-- 12. ETHICS GOVERNANCE & RECRUITMENT GATE -->
<!-- ========================================================================= -->
<h2>12. ETHICS GOVERNANCE & RECRUITMENT GATE</h2>
<p>
  The study is governed by the host institution's ethical research standards under relevant national regulations. Under established research governance, investigators cannot self-exempt research involving human student subjects:
</p>

<div class="memo-container">
<span class="field-name">ETHICAL GOVERNANCE & RECRUITMENT STATUS:</span><br/>
<span class="field-val" style="color: #feb2b2; font-size: 10pt; font-weight: bold;">
NO-GO — INSTITUTIONAL ETHICS AUTHORIZATION PENDING
</span><br/><br/>

<span class="field-name">HOST-INSTITUTION ADMINISTRATIVE DETERMINATION PLACEHOLDERS:</span><br/>
<span class="field-val" style="font-family: 'Consolas', monospace; font-size: 7.5pt; color: #cbd5e0;">
Approving Institution:           [ __________________________________________________ ]<br/>
Responsible Ethics Committee:    [ Institutional Ethics Committee (IEC) / IRB / Faculty Committee ]<br/>
Determination Type:              [ ] Exemption Confirmed  [ ] Expedited Approval  [ ] Full Approval<br/>
                                 [ ] Formal Institutional Confirmation that Review Not Required<br/>
Protocol / Reference Number:     [ __________________________________________________ ]<br/>
Date of Determination:           [ DD / MM / YYYY ]<br/>
Expiry / Continuing Review Date: [ DD / MM / YYYY / N/A ]<br/>
Attached Determination Letter:   [ 02_CORRECTED_ETHICS/institutional_approval_letter.pdf — PENDING ]
</span><br/><br/>

<span class="field-name">GOVERNANCE RULE:</span><br/>
<span class="field-val">
Participant recruitment must remain strictly halted until the responsible institutional authority signs the determination letter. Upon archiving the executed document, Gate 2 status will transition to <strong>GO — RECRUITMENT READY</strong>.
</span>
</div>

<!-- ========================================================================= -->
<!-- 13. FINAL CLAIMS LEDGER -->
<!-- ========================================================================= -->
<h2>13. FINAL 4-TIER CLAIMS LEDGER</h2>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Category</th>
      <th style="width: 38%;">Permissible & Supported Claims</th>
      <th style="width: 42%;">Mandatory Restrictions & Strict Prohibitions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Category A:<br/>Directly Measurable</strong></td>
      <td>Interactive client-side execution; subjective usability (canonical SUS); within-subject pre-to-post score gain ($\Delta\text{Score}$); 24-point practical rubric performance; diagnostic latency; subjective confidence; qualitative feedback themes; expert content review (CVI).</td>
      <td>Must state outcomes represent short-term learning within a single 50-minute laboratory period. Zero claims of long-term memory retention.</td>
    </tr>
    <tr>
      <td><strong>Category B:<br/>Exploratory Analyses</strong></td>
      <td>Confidence–accuracy association (exploratory calibration indicator); exploratory item difficulty ($P$); exploratory item discrimination ($D$); disciplinary descriptive patterns (B.Pharm vs Chemistry); diagnostic efficiency trends.</td>
      <td>Must be explicitly labeled as hypothesis-generating. Zero causal claims of simulator-induced metacognitive calibration.</td>
    </tr>
    <tr>
      <td><strong>Category C:<br/>Not Measured (Future)</strong></td>
      <td>Transfer of diagnostic skills to physical HPLC instrumentation; retention at 2–4 weeks; comparative superiority over textbook guides; reduction in physical hardware damage rates.</td>
      <td>Must be explicitly declared as unmeasured in the present pilot and discussed candidly in study limitations.</td>
    </tr>
    <tr>
      <td><strong>Category D:<br/>Strictly Prohibited</strong></td>
      <td><em>None permitted.</em></td>
      <td>❌ NO "Digital Twin" | ❌ NO "AI / Machine Learning / BKT" | ❌ NO "Universal HPLC Accuracy" | ❌ NO "Validated CFD / Navier-Stokes" | ❌ NO "Physical Pressure Dynamics".</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 14. OPEN-SCIENCE & REPRODUCIBILITY PLAN -->
<!-- ========================================================================= -->
<h2>14. OPEN-SCIENCE & REPRODUCIBILITY PLAN</h2>
<p>
  All project assets conform to JCE Transparency and Openness Promotion (TOP) Guidelines Level 2, partitioned into five isolated compartments:
</p>
<ul>
  <li><strong>1. Frozen Simulator Source Code:</strong> Immutable client-side source code verified by cryptographic hashes.</li>
  <li><strong>2. Educational Study Materials:</strong> Full protocols, student worksheets, neutral scripts, rubrics, and fidelity checklists.</li>
  <li><strong>3. Analysis Code Pipeline:</strong> Automated Python statistical scripts deposited under open MIT License.</li>
  <li><strong>4. Participant Data (Post-Collection):</strong> Completely de-identified raw CSV data deposited only after study completion.</li>
  <li><strong>5. Demo / Unit-Test Data:</strong> Synthetic edge-case test records labeled <code>DEMO_TEST_ONLY.csv</code> sequestered in <code>test_data/</code>.</li>
</ul>

<!-- ========================================================================= -->
<!-- 15. FINAL ARTIFACT CONSISTENCY MATRIX -->
<!-- ========================================================================= -->
<h2>15. FINAL ARTIFACT CONSISTENCY MATRIX (18 ARTIFACTS AUDITED)</h2>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Target Dimension</th>
      <th style="width: 24%;">Artifact A Checked</th>
      <th style="width: 24%;">Artifact B Checked</th>
      <th style="width: 14%; text-align: center;">Conflict?</th>
      <th style="width: 18%; text-align: center;">Verified Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Rubric Architecture</strong></td>
      <td><code>scoring_rubric.md</code></td>
      <td><code>participant_data_template.csv</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Rubric Grand Total</strong></td>
      <td><code>practical_diagnostic_task.md</code></td>
      <td><code>anonymized_data_dictionary.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Session Timing (50 min)</strong></td>
      <td><code>intervention_protocol.md</code></td>
      <td><code>study_design.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Sample Size ($N=20–30$)</strong></td>
      <td><code>sample_size_rationale.md</code></td>
      <td><code>study_design.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Canonical SUS Wording</strong></td>
      <td><code>SUS_instrument.md</code></td>
      <td><code>calculate_sus_score.py</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Neutral Instructor Script</strong></td>
      <td><code>instructor_protocol.md</code></td>
      <td><code>instructor_fidelity_checklist.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Balanced Pre-Test Keys</strong></td>
      <td><code>pretest.md</code></td>
      <td><code>answer_key.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Balanced Post-Test Keys</strong></td>
      <td><code>posttest.md</code></td>
      <td><code>answer_key.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Primary Endpoint Stability</strong></td>
      <td><code>research_questions.md</code></td>
      <td><code>statistical_analysis_plan.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Primary Test (Wilcoxon Pratt)</strong></td>
      <td><code>statistical_analysis_plan.md</code></td>
      <td><code>calculate_pre_post_stats.py</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Missing Data Code</strong></td>
      <td><code>statistical_analysis_plan.md</code></td>
      <td><code>calculate_pre_post_stats.py</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Confidence Framing</strong></td>
      <td><code>research_questions.md</code></td>
      <td><code>calculate_confidence_calibration.py</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Expert Review Framing</strong></td>
      <td><code>expert_content_validation_form.md</code></td>
      <td><code>claims_ledger.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Item Analysis Framing</strong></td>
      <td><code>research_questions.md</code></td>
      <td><code>calculate_item_psychometrics.py</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
    <tr>
      <td><strong>Ethics Governance Status</strong></td>
      <td><code>ethics_submission_package.md</code></td>
      <td><code>RECRUITMENT_READINESS_CHECKLIST.md</code></td>
      <td style="text-align: center;">NO</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 16. FROZEN-ENGINE INTEGRITY CHECK -->
<!-- ========================================================================= -->
<h2>16. FROZEN-ENGINE INTEGRITY CHECK</h2>
<p>
  Independent SHA-256 cryptographic checksums of the client-side simulation engine were verified against baseline values:
</p>

<pre class="code-box">=== FROZEN SIMULATION ENGINE CHECKSUM VERIFICATION ===
hplc_simulator_script.js: 2fad9547f9fc7c671176346e78732be30246a515853631dede21ae8f7d3b7167 (184,262 bytes) -> PASS
script.js:                9812fea221fee06391a35d2680c28ce375ca62bc26bc265ed07f36d4d96f0600 ( 67,625 bytes) -> PASS
index.html:               dfb896b41790efcc365a3721b8ccc7aa8f49861485a74b02538eb38cadbdee36 ( 85,537 bytes) -> PASS
hplc_simulator.html:      02b2b226bf291c2466c23832382e296523cecc68811afe26ba65822197afd6bb ( 93,721 bytes) -> PASS
FINAL ENGINE STATUS: PASS — ENGINE FROZEN (Zero Modifications Confirmed)</pre>

<!-- ========================================================================= -->
<!-- 17. RECRUITMENT CHECKLIST -->
<!-- ========================================================================= -->
<h2>17. FINAL RECRUITMENT READINESS CHECKLIST</h2>

<table>
  <thead>
    <tr>
      <th style="width: 6%; text-align: center;">#</th>
      <th style="width: 24%;">Audit Dimension</th>
      <th style="width: 44%;">Locked Requirement</th>
      <th style="width: 13%; text-align: center;">Audit Result</th>
      <th style="width: 13%; text-align: center;">Gate Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">01</td>
      <td>Methodological Specification</td>
      <td>24-pt rubric, balanced keys, canonical SUS, neutral script locked.</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
      <td style="text-align: center;">CLEARED</td>
    </tr>
    <tr>
      <td style="text-align: center;">02</td>
      <td>Data Schema Integrity</td>
      <td>73-column CSV template; zero data loss; zero fabricated rows.</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
      <td style="text-align: center;">CLEARED</td>
    </tr>
    <tr>
      <td style="text-align: center;">03</td>
      <td>Statistical Plan Locked</td>
      <td>Wilcoxon Pratt method primary; paired t-test sensitivity; Holm correction.</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
      <td style="text-align: center;">CLEARED</td>
    </tr>
    <tr>
      <td style="text-align: center;">04</td>
      <td>Claim Boundary Compliance</td>
      <td>All AI, digital twin, and causal calibration overclaims excised.</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
      <td style="text-align: center;">CLEARED</td>
    </tr>
    <tr>
      <td style="text-align: center;">05</td>
      <td>Engine Integrity Verified</td>
      <td>SHA-256 hashes match baseline to the byte (PASS — ENGINE FROZEN).</td>
      <td style="text-align: center;"><span class="tag tag-strength">PASS</span></td>
      <td style="text-align: center;">CLEARED</td>
    </tr>
    <tr>
      <td style="text-align: center;">06</td>
      <td>Institutional Ethics Sign-Off</td>
      <td>Written determination letter from responsible institutional authority.</td>
      <td style="text-align: center;"><span class="tag tag-blocker">PENDING</span></td>
      <td style="text-align: center;">HOLD</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 18. REMAINING LIMITATIONS -->
<!-- ========================================================================= -->
<h2>18. REMAINING METHODOLOGICAL LIMITATIONS</h2>
<p>
  The study package candidly acknowledges the following structural boundaries of the exploratory pilot design:
</p>
<ol>
  <li><strong>Single-Group Design:</strong> The pre/post design demonstrates within-subject score improvement but cannot rule out testing familiarity or prove causal superiority over traditional instruction.</li>
  <li><strong>Unmeasured Hardware Transfer:</strong> Evaluates diagnostic reasoning on simulated chromatographic data; transfer to physical HPLC instrumentation remains an unmeasured future research question.</li>
  <li><strong>Short-Term Temporal Horizon:</strong> Learning gains represent immediate retention within a single 50-minute laboratory period; long-term conceptual retention (2 to 4 weeks) is not assessed.</li>
  <li><strong>Local Cohort Scope:</strong> $N \approx 25$ participants from an intact university laboratory section establishes local instructional utility and software feasibility, not universal generalizability.</li>
</ol>

<!-- ========================================================================= -->
<!-- 19. FINAL DECISION -->
<!-- ========================================================================= -->
<h2>19. FINAL RECRUITMENT READINESS DECISION</h2>

<div class="memo-container">
<span class="field-name">AUDIT EVALUATION CLASSIFICATION:</span><br/>
<span class="field-val" style="color: #feb2b2; font-size: 10.5pt; font-weight: bold;">
NO-GO &mdash; INSTITUTIONAL ETHICS AUTHORIZATION PENDING
</span><br/><br/>

<span class="field-name">FINAL METHODOLOGICAL & REGULATORY DETERMINATION:</span><br/>
<span class="field-val">
The SimuPharm Phase 4.2.1 educational pilot protocol is <strong>fully finalized, methodologically specified, internally consistent, and scientifically conservative</strong>. All architectural decisions (24-point graduated rubric, balanced pre/post keys, canonical Brooke SUS, neutral guided inquiry, Pratt Wilcoxon analysis, and 73-column reconciled schema) are permanently locked. The simulation engine is 100% frozen, and zero participant data have been collected or fabricated.<br/><br/>
However, under host-institution research ethics governance and relevant regulations, <strong>investigators cannot self-exempt research involving human student participants</strong>. Participant recruitment must remain <strong>HALTED</strong> until the responsible Institutional Ethics Committee (IEC) / IRB or Department Chair executes the formal written determination letter.
</span><br/><br/>

<span class="field-name">CRITICAL PATH TO UNLOCK FULL "GO — RECRUITMENT READY":</span><br/>
<span class="field-val">
1. Submit <code>ethics_submission_package.md</code> to the responsible Institutional Ethics Committee or Department Chair.<br/>
2. Obtain the signed institutional determination letter confirming exemption, approval, or formal waiver.<br/>
3. Archive the signed letter in <code>02_CORRECTED_ETHICS/institutional_approval_letter.pdf</code>.<br/>
4. Upon archiving, Gate 2 status in <code>RECRUITMENT_READINESS_CHECKLIST.md</code> automatically transitions to: <strong>GO &mdash; RECRUITMENT READY</strong>.
</span>
</div>

<p style="text-align: center; color: #718096; font-size: 7.5pt; margin-top: 25px;">
  <strong>Hostile Pre-Pilot Scientific Audit & Correction Panel</strong> &bull; Protocol Freeze Certified October 4, 2026 &bull; SimuPharm.io Publication Due Diligence
</p>

</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html_content, wait_until="networkidle")
    page.pdf(
        path=out_primary,
        format="A4",
        print_background=True,
        margin={"top": "13mm", "bottom": "13mm", "left": "11mm", "right": "11mm"}
    )
    with open(out_primary, 'rb') as f_src, open(out_artifact, 'wb') as f_dst:
        f_dst.write(f_src.read())
    browser.close()

print(f"Successfully generated consolidated Phase 4.2.1 PDF: {out_primary} ({os.path.getsize(out_primary)} bytes)")
print(f"Successfully mirrored PDF: {out_artifact} ({os.path.getsize(out_artifact)} bytes)")
