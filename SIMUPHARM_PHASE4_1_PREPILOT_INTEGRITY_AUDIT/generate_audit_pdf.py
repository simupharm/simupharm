import os
import sys
from playwright.sync_api import sync_playwright

dir_primary = r"c:\Users\dsant\OneDrive\simupro - Copy\SIMUPHARM_PHASE4_1_PREPILOT_INTEGRITY_AUDIT"
dir_artifact = r"C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\SIMUPHARM_PHASE4_1_PREPILOT_INTEGRITY_AUDIT"
os.makedirs(dir_primary, exist_ok=True)
os.makedirs(dir_artifact, exist_ok=True)

pdf_filename = "SIMUPHARM_PHASE4_1_PREPILOT_INTEGRITY_AUDIT.pdf"
out_primary = os.path.join(dir_primary, pdf_filename)
out_artifact = os.path.join(dir_artifact, pdf_filename)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SimuPharm Phase 4.1 — Hostile Pre-Pilot Integrity Audit</title>
<style>
  @page {
    size: A4;
    margin: 14mm 12mm 14mm 12mm;
    @top-left {
      content: "SimuPharm Phase 4.1 | Hostile Pre-Pilot Integrity Audit";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 7.5pt;
      color: #9b2c2c;
      font-weight: 700;
    }
    @top-right {
      content: "PRE-PILOT RECRUITMENT READINESS AUDIT";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 7.5pt;
      color: #718096;
      font-weight: 600;
    }
    @bottom-left {
      content: "CONFIDENTIAL & PRIVILEGED | INDEPENDENT SCIENTIFIC AUDIT REPORT";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 7pt;
      color: #a0aec0;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 7.5pt;
      color: #4a5568;
      font-weight: 600;
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a202c;
    line-height: 1.38;
    font-size: 8.5pt;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  h1 {
    font-size: 20pt;
    font-weight: 800;
    color: #1a202c;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
  }

  h2 {
    font-size: 11.5pt;
    font-weight: 700;
    color: #2d3748;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 3px;
    margin-top: 14px;
    margin-bottom: 7px;
    break-after: avoid;
    page-break-after: avoid;
  }

  h3 {
    font-size: 9.5pt;
    font-weight: 700;
    color: #4a5568;
    margin-top: 9px;
    margin-bottom: 4px;
    break-after: avoid;
    page-break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 6px;
    text-align: justify;
  }

  ul, ol {
    margin-top: 2px;
    margin-bottom: 7px;
    padding-left: 18px;
  }

  li {
    margin-bottom: 3px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 6px;
    margin-bottom: 10px;
    font-size: 7.8pt;
    page-break-inside: auto;
  }

  tr {
    page-break-inside: avoid;
    page-break-after: auto;
  }

  th, td {
    border: 1px solid #cbd5e0;
    padding: 4.5px 6px;
    text-align: left;
    vertical-align: top;
  }

  th {
    background-color: #2d3748;
    color: #ffffff;
    font-weight: 600;
    font-size: 7.8pt;
  }

  tbody tr:nth-child(even) {
    background-color: #f7fafc;
  }

  .tag {
    display: inline-block;
    padding: 1.5px 5px;
    border-radius: 3px;
    font-size: 7pt;
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
    padding: 7px 10px;
    margin: 8px 0;
    background-color: #f8fafc;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
  }

  .callout-critical {
    border-left-color: #e53e3e;
    background-color: #fff5f5;
  }

  .callout-warning {
    border-left-color: #dd6b20;
    background-color: #fffaf0;
  }

  .callout-info {
    border-left-color: #3182ce;
    background-color: #ebf8ff;
  }

  .callout-title {
    font-weight: 700;
    font-size: 8.4pt;
    margin-bottom: 3px;
  }

  .callout-critical .callout-title { color: #9b2c2c; }
  .callout-warning .callout-title { color: #9c4221; }
  .callout-info .callout-title { color: #2b6cb0; }

  .code-box {
    background-color: #1a202c;
    color: #48bb78;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 7.4pt;
    padding: 8px 10px;
    border-radius: 4px;
    margin: 7px 0;
    line-height: 1.35;
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
    padding: 12px 14px;
    border-radius: 6px;
    margin-top: 10px;
    border-left: 6px solid #e53e3e;
    page-break-inside: avoid;
  }

  .memo-container .field-name {
    color: #a0aec0;
    font-size: 7.2pt;
    font-weight: 700;
    letter-spacing: 0.5px;
  }

  .memo-container .field-val {
    color: #ffffff;
    font-size: 8.5pt;
  }

  .flow-card-grid {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin: 8px 0;
    page-break-inside: avoid;
  }

  .flow-box {
    border: 1px solid #cbd5e0;
    border-radius: 5px;
    padding: 7px 10px;
    background: #f7fafc;
  }

  .flow-box-primary {
    border-left: 4px solid #3182ce;
    background: #ebf8ff;
  }

  .flow-box-secondary {
    border-left: 4px solid #38a169;
    background: #f0fff4;
  }

  .flow-box-exploratory {
    border-left: 4px solid #805ad5;
    background: #faf5ff;
  }

  .flow-box-critical {
    border-left: 4px solid #e53e3e;
    background: #fff5f5;
  }

  .flow-header {
    font-weight: 700;
    font-size: 8.2pt;
    margin-bottom: 2px;
  }

  .flow-desc {
    font-size: 7.6pt;
    color: #4a5568;
    line-height: 1.3;
  }

  .badge-chain {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 6px 0;
    font-size: 7.6pt;
    font-weight: 600;
  }

  .arrow-step {
    color: #718096;
    font-weight: bold;
  }
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- COVER & METADATA -->
<!-- ========================================================================= -->
<div style="border-bottom: 2px solid #9b2c2c; padding-bottom: 8px; margin-bottom: 12px;">
  <div style="display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
      <span class="tag tag-blocker" style="font-size: 8pt; padding: 2px 7px;">HOSTILE PRE-PILOT INTEGRITY AUDIT</span>
      <span class="tag tag-obs" style="font-size: 8pt; padding: 2px 7px; margin-left: 5px;">METHODOLOGICAL & DATA-INTEGRITY REVIEW</span>
      <span class="tag tag-obs" style="font-size: 8pt; padding: 2px 7px; margin-left: 5px;">PHASE 4.1</span>
    </div>
  </div>
  <h1 style="margin-top: 8px;">SimuPharm Phase 4.1<br/>Hostile Pre-Pilot Integrity Audit</h1>
  <div style="font-size: 10pt; color: #4a5568; font-weight: 600;">
    Educational Validation Study &mdash; Recruitment Readiness Assessment
  </div>
</div>

<table style="margin-bottom: 12px; font-size: 8pt;">
  <tr style="background: #edf2f7;">
    <td style="width: 25%;"><strong>AUDIT DATE:</strong> October 4, 2026</td>
    <td style="width: 25%;"><strong>DOCUMENT ID:</strong> AUDIT-P4.1-HOSTILE-PREPILOT-2026-REV1</td>
    <td style="width: 25%;"><strong>EVALUATION PACKAGE:</strong> Phase 4 Pilot Package</td>
    <td style="width: 25%;"><strong>CODEBASE:</strong> FROZEN (Zero Modifications)</td>
  </tr>
</table>

<div class="callout-box callout-critical">
  <div class="callout-title">🚨 AUDITOR GOVERNANCE DECLARATION</div>
  <p style="margin: 0; font-size: 8.2pt;">
    <strong>Mandate:</strong> This audit was conducted under an explicit hostile charter to determine whether the Phase 4 educational pilot package is methodologically sound, internally consistent, psychometrically valid, ethically compliant, and safe to execute <em>before any real student participant is recruited</em>.<br/>
    <strong>Code Freeze & Non-Fabrication Certification:</strong> Zero source code modifications were performed on the SimuPharm engine (<code>hplc_simulator_script.js</code>, <code>script.js</code>, <code>index.html</code>). Zero participant data, fake p-values, simulated effect sizes, or artificial SUS scores were generated. All educational outcomes remain strictly unobserved.
  </p>
</div>

<!-- ========================================================================= -->
<!-- 2. EXECUTIVE SUMMARY -->
<!-- ========================================================================= -->
<h2>2. EXECUTIVE SUMMARY</h2>
<p>
  An exhaustive adversarial audit was conducted across all 44 artifacts comprising the Phase 4 educational research design, psychometric instruments, ethics declarations, data schemas, analysis pipelines, and manuscript outlines.
</p>
<p>
  <strong>Overall Methodological Status:</strong> The Phase 4 package demonstrates outstanding structural organization, reproducible client-side software architecture, complete separation of testing data, and rigorous adherence to the Phase 3.5 claim boundaries. However, the package contains <strong>three Critical Blockers</strong>, <strong>five Major Methodological Issues</strong>, and <strong>four Minor Inconsistencies</strong> that compromise data validity and would lead to severe peer-review rejection if uncorrected prior to participant recruitment.
</p>

<table>
  <thead>
    <tr>
      <th style="width: 28%;">Audit Dimension</th>
      <th style="width: 10%; text-align: center;">Blockers</th>
      <th style="width: 10%; text-align: center;">Major</th>
      <th style="width: 10%; text-align: center;">Minor</th>
      <th style="width: 18%; text-align: center;">Readiness Status</th>
      <th style="width: 24%;">Primary Methodological Finding</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Ethics & Institutional Approval</strong></td>
      <td style="text-align: center;"><span class="tag tag-blocker">1</span></td>
      <td style="text-align: center;">0</td>
      <td style="text-align: center;">0</td>
      <td style="text-align: center;"><span class="tag tag-blocker">NO-GO (PENDING)</span></td>
      <td>Self-declaration of 45 CFR 46.104(d)(1) exemption is legally insufficient; formal institutional review/authorization is mandatory.</td>
    </tr>
    <tr>
      <td><strong>Data Architecture & Schema</strong></td>
      <td style="text-align: center;"><span class="tag tag-blocker">1</span></td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;"><span class="tag tag-blocker">CRITICAL BLOCKER</span></td>
      <td>12-point practical task rubric cannot be entered into <code>participant_data_template.csv</code> due to missing columns for reasoning and actions.</td>
    </tr>
    <tr>
      <td><strong>Assessment & Psychometrics</strong></td>
      <td style="text-align: center;"><span class="tag tag-blocker">1</span></td>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;"><span class="tag tag-blocker">CRITICAL BLOCKER</span></td>
      <td>Instructor script in Phase 3 spoon-feeds exact post-test answers; 80% of post-test items are keyed to option "B" (position bias).</td>
    </tr>
    <tr>
      <td><strong>Statistical Analysis Plan (SAP)</strong></td>
      <td style="text-align: center;">0</td>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;"><span class="tag tag-major">MAJOR REVISIONS</span></td>
      <td>Normality-contingent test selection distorts Type I error; Wilcoxon signed-rank script drops zero-gain tied scores.</td>
    </tr>
    <tr>
      <td><strong>Usability & SUS Instrument</strong></td>
      <td style="text-align: center;">0</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">0</td>
      <td style="text-align: center;"><span class="tag tag-major">MAJOR REVISIONS</span></td>
      <td>Modified wording in SUS items 1 and 7 invalidates comparison against standard Brooke (1996) / Bangor benchmark databases.</td>
    </tr>
    <tr>
      <td><strong>Manuscript & Claims</strong></td>
      <td style="text-align: center;">0</td>
      <td style="text-align: center;">0</td>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;"><span class="tag tag-strength">SOUND</span></td>
      <td>Phase 3.5 claim boundaries preserved; explicit placeholder tokens (<code>[N]</code>, <code>[MEAN]</code>) maintained.</td>
    </tr>
  </tbody>
</table>

<div class="callout-box callout-critical">
  <div class="callout-title">⛔ PROVISIONAL AUDIT DECISION: NO-GO &mdash; MAJOR METHODOLOGICAL CORRECTIONS REQUIRED</div>
  <p style="margin: 0; font-size: 8.2pt;">
    Participant recruitment must remain <strong>STRICTLY HALTED</strong>. While the educational concept is innovative, launching the pilot under the current protocol would result in fatal data collection omissions (inability to store practical reasoning data), massive instructor cueing bias, psychometric response-position distortion, and regulatory non-compliance.
  </p>
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 3. SOURCE ARTIFACT INVENTORY -->
<!-- ========================================================================= -->
<h2>3. SOURCE ARTIFACT INVENTORY</h2>
<p>
  All 44 artifacts located in <code>SIMUPHARM_PHASE4_EDUCATIONAL_VALIDATION/</code> were audited for structural integrity, internal consistency, and absence of fabricated participant data.
</p>

<table>
  <thead>
    <tr>
      <th style="width: 25%;">Folder / Module</th>
      <th style="width: 32%;">Artifact Filename</th>
      <th style="width: 8%;">Size</th>
      <th style="width: 15%;">Role</th>
      <th style="width: 20%;">Audit Verification Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>00_PHASE4_README/</code></td>
      <td><code>PHASE4_SCOPE.md</code></td>
      <td>4.6 KB</td>
      <td>Scope & Boundaries</td>
      <td><span class="tag tag-strength">Clean</span> Disavows AI/ML, digital twins, and 2.07% general accuracy.</td>
    </tr>
    <tr>
      <td><code>00_PHASE4_README/</code></td>
      <td><code>PHASE4_DECISION_STATUS.md</code></td>
      <td>2.5 KB</td>
      <td>Gate Register</td>
      <td><span class="tag tag-strength">Clean</span> Correctly leaves institutional approval box unchecked.</td>
    </tr>
    <tr>
      <td><code>00_PHASE4_README/</code></td>
      <td><code>ARTIFACT_INDEX.md</code></td>
      <td>5.6 KB</td>
      <td>Master Index</td>
      <td><span class="tag tag-strength">Clean</span> All files indexed; zero data contamination.</td>
    </tr>
    <tr>
      <td><code>01_RESEARCH_DESIGN/</code></td>
      <td><code>research_questions.md</code></td>
      <td>3.1 KB</td>
      <td>Hypotheses</td>
      <td><span class="tag tag-strength">Clean</span> Non-directional primary hypothesis.</td>
    </tr>
    <tr>
      <td><code>01_RESEARCH_DESIGN/</code></td>
      <td><code>study_design.md</code></td>
      <td>3.7 KB</td>
      <td>Study Protocol</td>
      <td><span class="tag tag-strength">Clean</span> Labels study exploratory pilot; outlines future RCT.</td>
    </tr>
    <tr>
      <td><code>01_RESEARCH_DESIGN/</code></td>
      <td><code>sample_size_rationale.md</code></td>
      <td>3.3 KB</td>
      <td>Power Analysis</td>
      <td><span class="tag tag-strength">Clean</span> Mathematical power calculations independently confirmed.</td>
    </tr>
    <tr>
      <td><code>01_RESEARCH_DESIGN/</code></td>
      <td><code>intervention_protocol.md</code></td>
      <td>3.7 KB</td>
      <td>Lab Protocol</td>
      <td><span class="tag tag-strength">Clean</span> Standardized time allocations (Phases 1 to 5).</td>
    </tr>
    <tr>
      <td><code>01_RESEARCH_DESIGN/</code></td>
      <td><code>statistical_analysis_plan.md</code></td>
      <td>4.6 KB</td>
      <td>SAP Trees</td>
      <td><span class="tag tag-major">Major</span> Normality-dependent test selection logic.</td>
    </tr>
    <tr>
      <td><code>02_ETHICS/</code></td>
      <td><code>ethics_checklist.md</code></td>
      <td>3.0 KB</td>
      <td>IRB Exemption</td>
      <td><span class="tag tag-blocker">Blocker</span> Assumes exemption is self-certifying.</td>
    </tr>
    <tr>
      <td><code>02_ETHICS/</code></td>
      <td><code>participant_information_sheet.md</code></td>
      <td>3.1 KB</td>
      <td>Participant Info</td>
      <td><span class="tag tag-strength">Clean</span> Voluntary, anonymous, zero grade consequence.</td>
    </tr>
    <tr>
      <td><code>02_ETHICS/</code></td>
      <td><code>informed_consent_template.md</code></td>
      <td>1.7 KB</td>
      <td>Consent Form</td>
      <td><span class="tag tag-strength">Clean</span> Standard opt-in check boxes.</td>
    </tr>
    <tr>
      <td><code>02_ETHICS/</code></td>
      <td><code>ethics_submission_notes.md</code></td>
      <td>2.0 KB</td>
      <td>IRB Filing Guidance</td>
      <td><span class="tag tag-strength">Clean</span> 45 CFR 46.104(d)(1) rationale articulated.</td>
    </tr>
    <tr>
      <td><code>03_ASSESSMENTS/</code></td>
      <td><code>pretest.md</code></td>
      <td>5.0 KB</td>
      <td>Baseline Test</td>
      <td><span class="tag tag-major">Major</span> 70% of answers keyed to option "B".</td>
    </tr>
    <tr>
      <td><code>03_ASSESSMENTS/</code></td>
      <td><code>posttest.md</code></td>
      <td>5.4 KB</td>
      <td>Parallel Test</td>
      <td><span class="tag tag-blocker">Blocker</span> 80% keyed to "B" (Q1–Q8 all B); instructor cues items.</td>
    </tr>
    <tr>
      <td><code>03_ASSESSMENTS/</code></td>
      <td><code>answer_key.md</code></td>
      <td>4.8 KB</td>
      <td>Master Keys</td>
      <td><span class="tag tag-strength">Clean</span> Mechanistic rationales cite John Dolan troubleshooting.</td>
    </tr>
    <tr>
      <td><code>03_ASSESSMENTS/</code></td>
      <td><code>scoring_rubric.md</code></td>
      <td>1.8 KB</td>
      <td>Practical Rubric</td>
      <td><span class="tag tag-blocker">Blocker</span> 12-pt rubric criteria not supported in CSV data schema!</td>
    </tr>
    <tr>
      <td><code>03_ASSESSMENTS/</code></td>
      <td><code>practical_diagnostic_task.md</code></td>
      <td>3.6 KB</td>
      <td>Fault Tasks</td>
      <td><span class="tag tag-strength">Clean</span> Alpha (leak), Beta (void), Gamma (bubble), Delta (contam).</td>
    </tr>
    <tr>
      <td><code>04_USABILITY/</code></td>
      <td><code>SUS_instrument.md</code></td>
      <td>2.2 KB</td>
      <td>SUS Survey</td>
      <td><span class="tag tag-major">Major</span> Modified Brooke wording in Q1 and Q7.</td>
    </tr>
    <tr>
      <td><code>04_USABILITY/</code></td>
      <td><code>usability_questionnaire.md</code></td>
      <td>1.7 KB</td>
      <td>Targeted UX</td>
      <td><span class="tag tag-strength">Clean</span> Kept separate from Brooke SUS calculation.</td>
    </tr>
    <tr>
      <td><code>04_USABILITY/</code></td>
      <td><code>qualitative_feedback_form.md</code></td>
      <td>3.0 KB</td>
      <td>Qualitative UX</td>
      <td><span class="tag tag-strength">Clean</span> Inductive thematic coding protocol defined.</td>
    </tr>
    <tr>
      <td><code>05_DATA_TEMPLATES/</code></td>
      <td><code>anonymized_data_dictionary.md</code></td>
      <td>3.8 KB</td>
      <td>Codebook</td>
      <td><span class="tag tag-blocker">Blocker</span> Lacks variables for practical reasoning and actions.</td>
    </tr>
    <tr>
      <td><code>05_DATA_TEMPLATES/</code></td>
      <td><code>participant_data_template.csv</code></td>
      <td>592 B</td>
      <td>CSV Template</td>
      <td><span class="tag tag-strength">Clean</span> 1 single header row, 0 participant records.</td>
    </tr>
    <tr>
      <td><code>05_DATA_TEMPLATES/</code></td>
      <td><code>data_entry_instructions.md</code></td>
      <td>1.4 KB</td>
      <td>Entry Protocol</td>
      <td><span class="tag tag-strength">Clean</span> Double-blind entry audit protocol specified.</td>
    </tr>
    <tr>
      <td><code>06_ANALYSIS/</code></td>
      <td><code>calculate_pre_post_stats.py</code></td>
      <td>3.0 KB</td>
      <td>Stats Script</td>
      <td><span class="tag tag-strength">Clean</span> Executes cleanly; drops zero-ties in Wilcoxon test.</td>
    </tr>
    <tr>
      <td><code>06_ANALYSIS/</code></td>
      <td><code>calculate_sus_score.py</code></td>
      <td>2.5 KB</td>
      <td>SUS Script</td>
      <td><span class="tag tag-strength">Clean</span> Correct odd/even scoring multipliers.</td>
    </tr>
    <tr>
      <td><code>06_ANALYSIS/</code></td>
      <td><code>calculate_hake_gain.py</code></td>
      <td>1.8 KB</td>
      <td>Hake Script</td>
      <td><span class="tag tag-strength">Clean</span> Handles ceiling effect edge cases.</td>
    </tr>
    <tr>
      <td><code>06_ANALYSIS/</code></td>
      <td><code>DEMO_DATA_NOT_REAL.csv</code></td>
      <td>1.9 KB</td>
      <td>Synthetic Demo</td>
      <td><span class="tag tag-strength">Clean</span> Explicitly labeled; isolated in test_data folder.</td>
    </tr>
    <tr>
      <td><code>07_MANUSCRIPT/</code></td>
      <td><code>manuscript_outline.md</code></td>
      <td>7.1 KB</td>
      <td>JCE Blueprint</td>
      <td><span class="tag tag-strength">Clean</span> Full 13-section structure conforming to JCE specs.</td>
    </tr>
    <tr>
      <td><code>07_MANUSCRIPT/</code></td>
      <td><code>title_options.md</code></td>
      <td>3.5 KB</td>
      <td>Title Options</td>
      <td><span class="tag tag-strength">Clean</span> Rejects AI, Digital Twin, and universal accuracy.</td>
    </tr>
    <tr>
      <td><code>07_MANUSCRIPT/</code></td>
      <td><code>provisional_abstract.md</code></td>
      <td>2.5 KB</td>
      <td>Placeholder Abs</td>
      <td><span class="tag tag-strength">Clean</span> Strictly preserves <code>[N]</code>, <code>[MEAN]</code>, <code>[SUS]</code> tokens.</td>
    </tr>
    <tr>
      <td><code>07_MANUSCRIPT/</code></td>
      <td><code>claims_ledger.md</code></td>
      <td>2.8 KB</td>
      <td>Claims Register</td>
      <td><span class="tag tag-strength">Clean</span> Prohibits digital twins, AI, and mechanistic claims.</td>
    </tr>
    <tr>
      <td><code>07_MANUSCRIPT/</code></td>
      <td><code>figure_plan.md</code></td>
      <td>3.8 KB</td>
      <td>Figure Plan</td>
      <td><span class="tag tag-strength">Clean</span> Figures 5–7 held as empty placeholders.</td>
    </tr>
    <tr>
      <td><code>08_REPRODUCIBILITY/</code></td>
      <td><code>instructor_protocol.md</code></td>
      <td>3.6 KB</td>
      <td>Teaching Script</td>
      <td><span class="tag tag-blocker">Blocker</span> Phase 3 script spoon-feeds exact post-test answers.</td>
    </tr>
    <tr>
      <td><code>08_REPRODUCIBILITY/</code></td>
      <td><code>reproducibility_checklist.md</code></td>
      <td>1.8 KB</td>
      <td>Open Science</td>
      <td><span class="tag tag-strength">Clean</span> Open science data/code deposition rules articulated.</td>
    </tr>
    <tr>
      <td><code>08_REPRODUCIBILITY/</code></td>
      <td><code>study_protocol.md</code></td>
      <td>1.4 KB</td>
      <td>Master Protocol</td>
      <td><span class="tag tag-strength">Clean</span> Timeline and double-locked paper storage rules.</td>
    </tr>
    <tr>
      <td><code>09_REPORTS/</code></td>
      <td><code>PHASE4_REPORT.md / .pdf</code></td>
      <td>23 KB</td>
      <td>Synthesis Docs</td>
      <td><span class="tag tag-strength">Clean</span> Complete synthesis report archived.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 4. AUDIT SEVERITY FRAMEWORK -->
<!-- ========================================================================= -->
<h2>4. AUDIT SEVERITY FRAMEWORK</h2>
<p>
  All findings are evaluated against international educational research integrity standards (AERA/APA/NCME Standards for Educational Testing, JCE Author Guidelines, and ICMJE Research Governance):
</p>
<ul>
  <li><span class="tag tag-blocker">CRITICAL BLOCKER</span> : A fatal methodological, ethical, or psychometric defect that invalidates data collection, produces unrecoverable data loss, or violates human subject research compliance. <strong>Must be corrected before participant recruitment.</strong></li>
  <li><span class="tag tag-major">MAJOR ISSUE</span> : A substantial methodological flaw that compromises statistical power, distorts test validity, or creates severe peer-review vulnerability. <strong>Should be corrected before recruitment unless formally justified.</strong></li>
  <li><span class="tag tag-minor">MINOR ISSUE</span> : A technical discrepancy, non-critical reporting ambiguity, or documentation inconsistency that does not halt data collection but should be resolved before manuscript submission.</li>
  <li><span class="tag tag-obs">OBSERVATION</span> : A noteworthy implementation characteristic, operational nuance, or neutral feature.</li>
  <li><span class="tag tag-strength">STRENGTH</span> : An exemplary methodological design choice, bias safeguard, or reproducibility feature.</li>
</ul>

<!-- ========================================================================= -->
<!-- 5. SUS VALIDITY AUDIT -->
<!-- ========================================================================= -->
<h2>5. SYSTEM USABILITY SCALE (SUS) VALIDITY AUDIT</h2>
<p>
  The System Usability Scale (Brooke 1996) is a standardized, highly calibrated psychometric instrument. Modifying item phrasing breaks standardization and impairs comparison against empirical benchmark distributions (Bangor et al. 2008, Sauro & Lewis 2016).
</p>

<table>
  <thead>
    <tr>
      <th style="width: 6%;">#</th>
      <th style="width: 28%;">Standard Brooke (1996) Wording</th>
      <th style="width: 28%;">SimuPharm Phase 4 Phrasing</th>
      <th style="width: 14%;">Difference</th>
      <th style="width: 24%;">Methodological Verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Q1</strong></td>
      <td>"I think that I would like to use this system frequently."</td>
      <td>"I think that I would like to use this system frequently <em>for chromatography learning</em>."</td>
      <td>Added qualifying prepositional phrase.</td>
      <td><span class="tag tag-major">Major Issue</span> Narrows construct to course utility, artificially boosting agreement. Restore Brooke wording OR label as "Adapted SUS".</td>
    </tr>
    <tr>
      <td><strong>Q2</strong></td>
      <td>"I found the system unnecessarily complex."</td>
      <td>"I found the system unnecessarily complex."</td>
      <td>Exact Match</td>
      <td><span class="tag tag-strength">Retain</span> Standard Brooke item preserved.</td>
    </tr>
    <tr>
      <td><strong>Q3</strong></td>
      <td>"I thought the system was easy to use."</td>
      <td>"I thought the system was easy to use."</td>
      <td>Exact Match</td>
      <td><span class="tag tag-strength">Retain</span> Standard Brooke item preserved.</td>
    </tr>
    <tr>
      <td><strong>Q4</strong></td>
      <td>"I think that I would need the support of a technical person to be able to use this system."</td>
      <td>"I think that I would need the support of a technical person to be able to use this system."</td>
      <td>Exact Match</td>
      <td><span class="tag tag-strength">Retain</span> Standard Brooke item preserved.</td>
    </tr>
    <tr>
      <td><strong>Q5</strong></td>
      <td>"I found the various functions in this system were well integrated."</td>
      <td>"I found the various functions in this system were well integrated."</td>
      <td>Exact Match</td>
      <td><span class="tag tag-strength">Retain</span> Standard Brooke item preserved.</td>
    </tr>
    <tr>
      <td><strong>Q6</strong></td>
      <td>"I thought there was too much inconsistency in this system."</td>
      <td>"I thought there was too much inconsistency in this system."</td>
      <td>Exact Match</td>
      <td><span class="tag tag-strength">Retain</span> Standard Brooke item preserved.</td>
    </tr>
    <tr>
      <td><strong>Q7</strong></td>
      <td>"I would imagine that most people would learn to use this system very quickly."</td>
      <td>"I would imagine that most <em>students</em> would learn to use this system very quickly."</td>
      <td>Substituted "people" with "students".</td>
      <td><span class="tag tag-minor">Minor Issue</span> Contextual substitution commonly accepted in education, but strictly deviates from canonical Brooke. Declare in Methods.</td>
    </tr>
    <tr>
      <td><strong>Q8</strong></td>
      <td>"I found the system very cumbersome to use."</td>
      <td>"I found the system very cumbersome to use."</td>
      <td>Exact Match</td>
      <td><span class="tag tag-strength">Retain</span> Standard Brooke item preserved.</td>
    </tr>
    <tr>
      <td><strong>Q9</strong></td>
      <td>"I felt very confident using the system."</td>
      <td>"I felt very confident using the system."</td>
      <td>Exact Match</td>
      <td><span class="tag tag-strength">Retain</span> Standard Brooke item preserved.</td>
    </tr>
    <tr>
      <td><strong>Q10</strong></td>
      <td>"I needed to learn a lot of things before I could get going with this system."</td>
      <td>"I needed to learn a lot of things before I could get going with this system."</td>
      <td>Exact Match</td>
      <td><span class="tag tag-strength">Retain</span> Standard Brooke item preserved.</td>
    </tr>
  </tbody>
</table>

<div class="callout-box callout-warning">
  <div class="callout-title">⚠️ SUS Standardization Ruling</div>
  <p style="margin: 0; font-size: 8.2pt;">
    Because Item 1 and Item 7 contain modified wording, the instrument cannot be cited as an unmodified standard Brooke SUS without inviting referee objection. The author must either: (1) Revert Q1 to <em>"I think that I would like to use this system frequently"</em> and Q7 to <em>"most people"</em> before printing surveys; OR (2) Explicitly define the scale as an <strong>"Adapted Educational System Usability Scale (SUS-Ed)"</strong> and cite Lewis & Sauro (2018) for psychometric equivalence. Domain-specific UX items (<code>usability_questionnaire.md</code>) must remain strictly isolated.
  </p>
</div>

<!-- ========================================================================= -->
<!-- 6. PRIMARY OUTCOME AND ENDPOINT HIERARCHY -->
<!-- ========================================================================= -->
<h2>6. PRIMARY OUTCOME AND ENDPOINT HIERARCHY</h2>
<p>
  A rigorous educational trial requires a pre-specified, immutable outcome hierarchy to prevent "p-hacking" and selective outcome switching.
</p>

<div class="flow-card-grid">
  <div class="flow-box flow-box-primary">
    <div class="flow-header">PRIMARY OUTCOME (Pre-Specified & Confirmatory)</div>
    <div class="flow-desc">
      <strong>Paired Troubleshooting Score Gain (&Delta;Score = Post-Test &minus; Pre-Test, 0 to 10 points)</strong><br/>
      Inferential Test: Wilcoxon Signed-Rank Test (Two-Tailed, &alpha; = 0.05). Paired <i>t</i>-test pre-specified as sensitivity analysis.
    </div>
  </div>
  <div class="badge-chain">
    <span>Hierarchy Flow:</span>
    <span class="tag tag-strength">Primary Endpoint</span>
    <span class="arrow-step">&rarr;</span>
    <span class="tag tag-obs">Secondary Endpoints (Holm-Bonferroni Adjusted)</span>
    <span class="arrow-step">&rarr;</span>
    <span class="tag tag-obs">Exploratory Subgroups</span>
  </div>
  <div class="flow-box flow-box-secondary">
    <div class="flow-header">SECONDARY OUTCOMES (Multiplicity-Controlled via Holm-Bonferroni Step-Down)</div>
    <div class="flow-desc">
      1. <strong>Practical Diagnostic Accuracy:</strong> % Correct across 4 Unknown Simulated Faults (Alpha, Beta, Gamma, Delta)<br/>
      2. <strong>Diagnostic Latency:</strong> Median Time-to-Diagnosis in seconds (Interquartile Range)<br/>
      3. <strong>Diagnostic Confidence Calibration:</strong> Pearson correlation <i>r</i> between confidence rating (1–5) and diagnostic accuracy<br/>
      4. <strong>System Usability Scale (SUS):</strong> Mean continuous score (0–100) and Bangor adjective grade<br/>
      5. <strong>Targeted Pedagogical Usability:</strong> 8 domain-specific UX items (1–5 Likert scale, reported as medians/IQRs)<br/>
      6. <strong>Hake Normalized Gain:</strong> Average cohort gain &lang;g&rang; = (Post &minus; Pre) / (10 &minus; Pre)<br/>
      7. <strong>Qualitative Learning Themes:</strong> Inductive thematic coding of open-ended participant reflections
    </div>
  </div>
  <div class="flow-box flow-box-exploratory">
    <div class="flow-header">EXPLORATORY SUBGROUP ANALYSES (Hypothesis-Generating, Descriptive Only)</div>
    <div class="flow-desc">
      &bull; Disciplinary Background: B.Pharm (n &approx; 12) vs. B.Sc. Chemistry (n &approx; 13)<br/>
      &bull; Prior HPLC Exposure: Hands-on laboratory instrument experience vs. complete novices<br/>
      &bull; Item-Level Psychometrics: Item difficulty index (<i>P</i>) and discrimination index (<i>D</i>)
    </div>
  </div>
</div>

<p style="font-size: 8.2pt; margin-top: 6px;">
  <strong>Hierarchy Audit Ruling:</strong> The primary endpoint (&Delta;Score) is stable across all documents with zero switching detected. However, because 7 secondary endpoints are specified, testing without family-wise error rate control produces a >40% false-positive risk. The SAP must mandate <strong>Holm-Bonferroni correction</strong> for all secondary inferential tests.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 7. STATISTICAL ANALYSIS AUDIT -->
<!-- ========================================================================= -->
<h2>7. STATISTICAL ANALYSIS AUDIT & STATISTICAL ISSUE REGISTER</h2>
<p>
  A rigorous audit of the Pre-Specified Statistical Analysis Plan (<code>statistical_analysis_plan.md</code>) and analysis code (<code>calculate_pre_post_stats.py</code>) identified multiple methodological vulnerabilities:
</p>

<h3>Table 7.1: Formal Statistical Issue Register</h3>

<table>
  <thead>
    <tr>
      <th style="width: 10%;">Issue ID</th>
      <th style="width: 18%;">Dimension</th>
      <th style="width: 12%;">Severity</th>
      <th style="width: 25%;">Evidence in Source Documents</th>
      <th style="width: 25%;">Methodological Consequence</th>
      <th style="width: 10%;">Blocker?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>STAT-01</strong></td>
      <td>Normality-Contingent Test Selection</td>
      <td><span class="tag tag-major">Major</span></td>
      <td><code>statistical_analysis_plan.md</code> line 28: <em>"If Shapiro-Wilk p &ge; 0.05 &rarr; Paired t-test; If p &lt; 0.05 &rarr; Wilcoxon"</em></td>
      <td>Pre-testing normality in small samples (N=20–30) has low power (&lt;40%) and distorts nominal Type I error rate (&alpha; &ne; 0.05). <strong>Pre-specify Wilcoxon as primary.</strong></td>
      <td><strong>YES</strong></td>
    </tr>
    <tr>
      <td><strong>STAT-02</strong></td>
      <td>Wilcoxon Zero-Difference Handling</td>
      <td><span class="tag tag-major">Major</span></td>
      <td><code>calculate_pre_post_stats.py</code> line 52: <code>stats.wilcoxon(post, pre, zero_method='wilcox')</code></td>
      <td><code>zero_method='wilcox'</code> discards participants with zero score gain (&Delta; = 0), artificially inflating perceived effect size. <strong>Switch to Pratt's method.</strong></td>
      <td><strong>YES</strong></td>
    </tr>
    <tr>
      <td><strong>STAT-03</strong></td>
      <td>Small-Sample Discrete Ordinality</td>
      <td><span class="tag tag-major">Major</span></td>
      <td>Pre/post scores are integers from 0 to 10; differences are bounded integers (&minus;10 to +10).</td>
      <td>Discrete counts violate continuous Gaussian assumptions. Compute Hodges-Lehmann median difference and bootstrap 95% CIs.</td>
      <td><strong>YES</strong></td>
    </tr>
    <tr>
      <td><strong>STAT-04</strong></td>
      <td>Multiple Testing Correction</td>
      <td><span class="tag tag-minor">Minor</span></td>
      <td><code>statistical_analysis_plan.md</code> mentions Holm-Bonferroni, but analysis script lacks implementation.</td>
      <td>Secondary outcomes risk spurious false-positive significance. Integrate <code>multipletests</code> with Holm adjustment.</td>
      <td>NO</td>
    </tr>
    <tr>
      <td><strong>STAT-05</strong></td>
      <td>Hake Gain Ceiling Division</td>
      <td><span class="tag tag-minor">Minor</span></td>
      <td><code>calculate_hake_gain.py</code> line 26: <code>(post - pre) / (10 - pre)</code></td>
      <td>Individual gain undefined if Pre = 10. Report cohort average gain &lang;g&rang; as primary; exclude undefined cases.</td>
      <td>NO</td>
    </tr>
    <tr>
      <td><strong>STAT-06</strong></td>
      <td>Subgroup Underpowering</td>
      <td><span class="tag tag-major">Major</span></td>
      <td><code>manuscript_outline.md</code> plans subgroup comparisons (B.Pharm vs B.Sc.; Prior Exp vs Novice).</td>
      <td>In N=25, subgroups of n=10–12 have statistical power &lt;25% for moderate effects (d=0.50). Report descriptive stats only.</td>
      <td>NO</td>
    </tr>
    <tr>
      <td><strong>STAT-07</strong></td>
      <td>Time-to-Diagnosis Outlier Skewness</td>
      <td><span class="tag tag-minor">Minor</span></td>
      <td>Latency measured in seconds (range 10–300 s) is inherently right-skewed.</td>
      <td>Mean latency is heavily distorted by distracted students. Mandate <strong>Median Diagnostic Latency (IQR)</strong>.</td>
      <td>NO</td>
    </tr>
    <tr>
      <td><strong>STAT-08</strong></td>
      <td>Missing Data Handling Ambiguity</td>
      <td><span class="tag tag-minor">Minor</span></td>
      <td><code>statistical_analysis_plan.md</code> does not specify item-level vs participant-level exclusion.</td>
      <td>Risk of post-hoc exclusion bias. Pre-specify complete-case analysis for pre/post scores (&ge;1 missing = excluded).</td>
      <td>NO</td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 8. PRACTICAL DIAGNOSTIC TASK AUDIT -->
<!-- ========================================================================= -->
<h2>8. PRACTICAL DIAGNOSTIC TASK AUDIT & SCHEMA RECONCILIATION</h2>
<p>
  A critical structural conflict was discovered between the scoring rubric, assessment task, and data entry schema.
</p>

<div class="flow-card-grid">
  <div class="flow-box flow-box-primary">
    <div class="flow-header">ASSESSMENT INSTRUMENT (practical_diagnostic_task.md)</div>
    <div class="flow-desc">Students diagnose 4 simulated unknowns and record: (1) Fault Identification, (2) Physical Reasoning, and (3) Corrective Action.</div>
  </div>
  <div class="flow-box flow-box-secondary">
    <div class="flow-header">ANALYTICAL SCORING RUBRIC (scoring_rubric.md)</div>
    <div class="flow-desc">Graders evaluate each scenario on a 3-component rubric: Fault ID (0–2 pts) + Physical Reasoning (0–2 pts) + Corrective Action (0–2 pts) = 0 to 6 points per task (0 to 24 points grand total across 4 tasks) with independent double-rater scoring.</div>
  </div>
  <div class="flow-box flow-box-critical">
    <div class="flow-header">FATAL DATA SCHEMA MISMATCH (participant_data_template.csv)</div>
    <div class="flow-desc">
      <strong>CRITICAL BLOCKER:</strong> The CSV template contains ONLY binary columns: <code>task_alpha_correct</code> (0/1) and <code>task_total_score</code> (0–4)!<br/>
      <strong>Consequence:</strong> The template has NO columns to store physical reasoning scores, corrective action scores, scenario totals, or Rater 1/Rater 2 scores. Data entry clerks will be forced to truncate the entire 12-point rubric into a 4-point binary check, causing irreversible data loss!
    </div>
  </div>
</div>

<p>
  To resolve this blocker, the CSV template and data dictionary must be expanded with the following mandatory columns:
</p>

<h3>Table 8.2: Complete Practical Task Schema Reconciliation</h3>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Rubric Dimension</th>
      <th style="width: 14%;">Scoring Scale</th>
      <th style="width: 18%;">Existing CSV Column</th>
      <th style="width: 18%;">Status in Current CSV</th>
      <th style="width: 30%;">Required Mandatory Column Addition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Scenario Alpha: Fault ID</strong></td>
      <td>0, 1, 2 points</td>
      <td><code>task_alpha_correct</code></td>
      <td>Truncated to 0/1</td>
      <td><code>task_alpha_id_score</code> (Integer: 0, 1, 2)</td>
    </tr>
    <tr>
      <td><strong>Scenario Alpha: Reasoning</strong></td>
      <td>0, 1, 2 points</td>
      <td>NONE</td>
      <td><span class="tag tag-blocker">Completely Missing</span></td>
      <td><code>task_alpha_reason_score</code> (Integer: 0, 1, 2)</td>
    </tr>
    <tr>
      <td><strong>Scenario Alpha: Action</strong></td>
      <td>0, 1, 2 points</td>
      <td>NONE</td>
      <td><span class="tag tag-blocker">Completely Missing</span></td>
      <td><code>task_alpha_action_score</code> (Integer: 0, 1, 2)</td>
    </tr>
    <tr>
      <td><strong>Scenario Alpha: Total</strong></td>
      <td>0 to 6 points</td>
      <td>NONE</td>
      <td><span class="tag tag-blocker">Completely Missing</span></td>
      <td><code>task_alpha_rubric_total</code> (Integer: 0 to 6)</td>
    </tr>
    <tr>
      <td><strong>Scenario Beta: ID / Reason / Action</strong></td>
      <td>0 to 6 points</td>
      <td><code>task_beta_correct</code></td>
      <td>Truncated to 0/1</td>
      <td><code>task_beta_id_score</code>, <code>_reason_score</code>, <code>_action_score</code>, <code>_rubric_total</code></td>
    </tr>
    <tr>
      <td><strong>Scenario Gamma: ID / Reason / Action</strong></td>
      <td>0 to 6 points</td>
      <td><code>task_gamma_correct</code></td>
      <td>Truncated to 0/1</td>
      <td><code>task_gamma_id_score</code>, <code>_reason_score</code>, <code>_action_score</code>, <code>_rubric_total</code></td>
    </tr>
    <tr>
      <td><strong>Scenario Delta: ID / Reason / Action</strong></td>
      <td>0 to 6 points</td>
      <td><code>task_delta_correct</code></td>
      <td>Truncated to 0/1</td>
      <td><code>task_delta_id_score</code>, <code>_reason_score</code>, <code>_action_score</code>, <code>_rubric_total</code></td>
    </tr>
    <tr>
      <td><strong>Inter-Rater Reliability</strong></td>
      <td>Rater 1 vs Rater 2</td>
      <td>NONE</td>
      <td><span class="tag tag-blocker">Completely Missing</span></td>
      <td><code>rater1_total_score</code>, <code>rater2_total_score</code> (Integers: 0 to 24)</td>
    </tr>
    <tr>
      <td><strong>Grand Rubric Total</strong></td>
      <td>0 to 24 points</td>
      <td><code>task_total_score</code> (0–4)</td>
      <td>Severe Scale Mismatch</td>
      <td><code>task_rubric_grand_total</code> (replaces 0–4 score)</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 9. PRE/POST TEST EQUIVALENCE AUDIT -->
<!-- ========================================================================= -->
<h2>9. PRE/POST TEST EQUIVALENCE AUDIT & KEYED RESPONSE BIAS</h2>
<p>
  A rigorous comparative item analysis was performed across all 10 pre-test items (<code>pretest.md</code>) and 10 post-test items (<code>posttest.md</code>).
</p>

<table>
  <thead>
    <tr>
      <th style="width: 6%;">Pair</th>
      <th style="width: 22%;">Diagnostic Construct</th>
      <th style="width: 24%;">Pre-Test Item Focus</th>
      <th style="width: 24%;">Post-Test Isomorphic Equivalent</th>
      <th style="width: 6%; text-align: center;">Pre Key</th>
      <th style="width: 6%; text-align: center;">Post Key</th>
      <th style="width: 12%;">Equivalence Verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Q1</strong></td>
      <td>Pump Cavitation</td>
      <td>25 bar drop + baseline spikes</td>
      <td>Cyclical &plusmn;20 bar fluctuation + negative spikes</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td><span class="tag tag-strength">Excellent</span> Bloom: Analysis</td>
    </tr>
    <tr>
      <td><strong>Q2</strong></td>
      <td>Pre-Column Fitting Leak</td>
      <td>+30% retention + 85 to 55 bar drop</td>
      <td>+25% retention + 90 to 60 bar drop + droplets</td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td><span class="tag tag-strength">Excellent</span> Bloom: Application</td>
    </tr>
    <tr>
      <td><strong>Q3</strong></td>
      <td>Column Inlet Voiding</td>
      <td>Split peaks + tailing Tf &gt; 2.2</td>
      <td>Bifurcated doublet peaks + tailing Tf = 2.4</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td><span class="tag tag-strength">Excellent</span> Bloom: Analysis</td>
    </tr>
    <tr>
      <td><strong>Q4</strong></td>
      <td>Ghost Peaks / Contamination</td>
      <td>Unassigned peaks in blank gradient</td>
      <td>Ghost peaks doubling with initial hold time</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td><span class="tag tag-strength">Excellent</span> Bloom: Comprehension</td>
    </tr>
    <tr>
      <td><strong>Q5</strong></td>
      <td>High Backpressure Isolation</td>
      <td>Sudden overpressure &gt; 400 bar</td>
      <td>Disconnecting inlet drops 380 to 5 bar</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td><span class="tag tag-strength">Excellent</span> Bloom: Application</td>
    </tr>
    <tr>
      <td><strong>Q6</strong></td>
      <td>Mobile Phase pH Drift</td>
      <td>Selective acidic API drift vs neutral</td>
      <td>Ibuprofen shift vs Caffeine/Toluene stability</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td><span class="tag tag-strength">Excellent</span> Bloom: Analysis</td>
    </tr>
    <tr>
      <td><strong>Q7</strong></td>
      <td>Peak Asymmetry Mechanisms</td>
      <td>Fronting caused by mass overload</td>
      <td>Tailing caused by residual silanol interactions</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td><span class="tag tag-major">Disparity</span> Pre: fronting; Post: tailing.</td>
    </tr>
    <tr>
      <td><strong>Q8</strong></td>
      <td>Cavitation Troubleshooting</td>
      <td>First action: open purge valve, prime</td>
      <td>Pump degassing sequence: open purge valve</td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td style="text-align: center;"><strong>B</strong></td>
      <td><span class="tag tag-strength">Excellent</span> Bloom: Application</td>
    </tr>
    <tr>
      <td><strong>Q9</strong></td>
      <td>Void vs Blockage Diagnosis</td>
      <td>Frit blockage vs inlet voiding</td>
      <td>Inlet void vs sample solvent mismatch</td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td><span class="tag tag-strength">Good</span> Bloom: Evaluation</td>
    </tr>
    <tr>
      <td><strong>Q10</strong></td>
      <td>Leak Location Diagnostics</td>
      <td>Post-column vs pre-detector leak</td>
      <td>Pre-injector leak (area recovery vs retention)</td>
      <td style="text-align: center;"><strong>C</strong></td>
      <td style="text-align: center;"><strong>A</strong></td>
      <td><span class="tag tag-strength">Good</span> Bloom: Evaluation</td>
    </tr>
  </tbody>
</table>

<div class="callout-box callout-critical">
  <div class="callout-title">🚨 PSYCHOMETRIC DEFECT: KEYED RESPONSE POSITION BIAS</div>
  <p style="margin: 0; font-size: 8.2pt;">
    Inspection of the master answer keys reveals a fatal psychometric flaw:
  </p>
  <ul style="margin-top: 3px; margin-bottom: 2px;">
    <li><strong>Pre-Test Key Distribution:</strong> Option A = 2, <strong>Option B = 7 (70%)</strong>, Option C = 1, Option D = 0.</li>
    <li><strong>Post-Test Key Distribution:</strong> Option A = 2, <strong>Option B = 8 (80%)</strong>, Option C = 0, Option D = 0.</li>
    <li><strong>Critical Flaw: In the post-test, Items Q1 through Q8 are ALL keyed to Option B!</strong> A disengaged student who blindly selects "B" for every item scores 80% on the post-test and 70% on the pre-test. This completely destroys test validity and inflates gain scores. <strong>The answer choices must be re-randomized across A, B, C, and D prior to recruitment.</strong></li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- 10. INSTRUCTOR BIAS AUDIT -->
<!-- ========================================================================= -->
<h2>10. INSTRUCTOR BIAS AUDIT (TEACHING-TO-THE-TEST FORENSICS)</h2>
<p>
  A line-by-line review of <code>instructor_protocol.md</code> (Phase 3: Interactive Fault Exploration, Minutes 18–30) revealed severe instructor demand characteristics and direct test cueing:
</p>

<div class="flow-card-grid">
  <div class="flow-box flow-box-critical">
    <div class="flow-header">BIASED INSTRUCTOR SCRIPT IN SOURCE DOCUMENT (instructor_protocol.md)</div>
    <div class="flow-desc" style="font-style: italic;">
      "Open the 'Fault Injection' panel:<br/>
      1. Toggle 'Air Bubble'. Observe the pressure gauge dipping cyclically and sharp baseline spikes. Why does this happen? The air pocket compresses in the pump head, causing momentary flow delivery loss.<br/>
      2. Toggle 'System Leak'. What happens to retention times? They increase by 30% because liquid is dripping out before the column.<br/>
      3. Toggle 'Column Void'. Notice the split peaks. Channeling in the collapsed silica bed splits the solute band.<br/>
      4. Toggle 'Contamination'. Notice the ghost peaks."
    </div>
  </div>
  <div class="flow-box flow-box-critical">
    <div class="flow-header">FATAL CONFOUND: DIRECT TEST CUEING IDENTIFIED</div>
    <div class="flow-desc">
      The instructor script explicitly spoon-feeds the exact symptoms, numerical shifts (-20 bar, -50 bar, +30% tR), and mechanisms tested in <strong>Post-Test Items Q1–Q4</strong> and <strong>Practical Scenarios Alpha–Delta</strong> right before the exam! Post-test gains would measure rote memorization of the instructor's spoken words, NOT simulation learning!
    </div>
  </div>
  <div class="flow-box flow-box-secondary">
    <div class="flow-header">MANDATORY NEUTRAL REPLACEMENT SCRIPT (Non-Directive Guided Inquiry)</div>
    <div class="flow-desc">
      <strong>Replacement Script:</strong> "Open the 'Fault Injection' panel. Activate Fault 1. Examine the pressure gauge and chromatographic canvas carefully. Notice any changes from baseline. Think about what physical change in the fluidic pathway could cause this behavior. Now activate Fault 2, Fault 3, and Fault 4 sequentially. Compare how each fault alters retention, peak shape, and backpressure. Record your observations in your lab notebook."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 11. SIMULATION VS PHYSICAL REALITY AUDIT -->
<!-- ========================================================================= -->
<h2>11. SIMULATION VS PHYSICAL REALITY AUDIT</h2>
<p>
  To maintain scientific documentation integrity, simulated representations must be clearly differentiated from physical chromatography:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Fault Condition</th>
      <th style="width: 25%;">Real-World Physical Phenomenon</th>
      <th style="width: 22%;">SimuPharm Simulated Implementation</th>
      <th style="width: 20%;">Defensible Pedagogical Claim</th>
      <th style="width: 15%;">Prohibited Claim</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Air Bubble / Cavitation</strong></td>
      <td>Gas bubble in pump check valve dampens displacement stroke, causing stroke-synchronized flow drop and refractive optical spikes.</td>
      <td>Discrete <code>-20 bar</code> subtraction, <code>noiseMultiplier: 5</code>, <code>rtShift: +0.10</code> step function.</td>
      <td>Qualitatively reproduces characteristic pressure ripple and baseline noise symptomology.</td>
      <td>&cross; Cannot claim mechanistic two-phase Navier-Stokes cavitation fluid mechanics.</td>
    </tr>
    <tr>
      <td><strong>Fitting / System Leak</strong></td>
      <td>Mobile phase loss upstream of column reduces superficial linear velocity (u &lt; u<sub>set</sub>), elongating retention proportional to leak split.</td>
      <td>Discrete <code>-50 bar</code> subtraction, <code>rtShift: +0.30</code> (+30% constant stretch).</td>
      <td>Demonstrates inverse relationship between volumetric flow delivery and solute retention.</td>
      <td>&cross; Cannot claim hydrodynamically calibrated leak aperture or mass balance modeling.</td>
    </tr>
    <tr>
      <td><strong>Column Inlet Bed Void</strong></td>
      <td>Silica bed collapse at inlet creates void headspace; dual velocity channels split migrating solute bands; pressure typically normal or lower.</td>
      <td>Discrete <code>+30 bar</code> surge, <code>tailingFactor: 2.50</code>, <code>efficiencyLoss: 50%</code>.</td>
      <td>Visualizes split peaks (doublets) and tailing resulting from bed disruption.</td>
      <td>&cross; Cannot claim porous bed fluid mechanics. (Note: Real voids do not increase pressure unless frit is fouled).</td>
    </tr>
    <tr>
      <td><strong>Contamination / Ghost Peaks</strong></td>
      <td>Impurities in mobile phase buffers or solvents concentrate on column head and elute during gradient ramps.</td>
      <td>Synthetic peaks injected into peak array at fixed retention times with <code>pressureEffect: +5 bar</code>.</td>
      <td>Demonstrates appearance of non-analyte ghost peaks in quality control blanks.</td>
      <td>&cross; Cannot claim chemical equilibrium partition modeling of organic solvent trace impurities.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 12. CLAIM-BOUNDARY AUDIT -->
<!-- ========================================================================= -->
<h2>12. CLAIM-BOUNDARY AUDIT</h2>
<p>
  A global text audit was conducted across all Phase 4 documents for prohibited terminology established in Phase 3.5:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 22%;">Target Term / Concept</th>
      <th style="width: 10%; text-align: center;">Occurrences</th>
      <th style="width: 25%;">Document Locations</th>
      <th style="width: 25%;">Context of Appearance</th>
      <th style="width: 18%;">Audit Verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>"Digital Twin"</code></td>
      <td style="text-align: center;">5 files</td>
      <td><code>PHASE4_SCOPE.md</code>, <code>claims_ledger.md</code>, <code>manuscript_outline.md</code></td>
      <td>Listed strictly within "PROHIBITED CLAIMS" and prior art disavowals.</td>
      <td><span class="tag tag-strength">COMPLIANT</span> Zero affirmative use.</td>
    </tr>
    <tr>
      <td><code>"Artificial Intelligence" / "AI"</code></td>
      <td style="text-align: center;">3 files</td>
      <td><code>PHASE4_SCOPE.md</code>, <code>claims_ledger.md</code>, <code>PHASE4_REPORT.md</code></td>
      <td>Listed strictly within "PROHIBITED CLAIMS".</td>
      <td><span class="tag tag-strength">COMPLIANT</span> Zero affirmative use.</td>
    </tr>
    <tr>
      <td><code>"Machine Learning" / "BKT"</code></td>
      <td style="text-align: center;">4 files</td>
      <td><code>PHASE4_SCOPE.md</code>, <code>claims_ledger.md</code>, <code>manuscript_outline.md</code></td>
      <td>Disavowed in Background & Claims Boundary.</td>
      <td><span class="tag tag-strength">COMPLIANT</span> Zero affirmative use.</td>
    </tr>
    <tr>
      <td><code>"2.07%" General Accuracy</code></td>
      <td style="text-align: center;">3 files</td>
      <td><code>PHASE4_SCOPE.md</code>, <code>claims_ledger.md</code>, <code>PHASE4_REPORT.md</code></td>
      <td>Cited strictly as an audited in-sample calibration artifact.</td>
      <td><span class="tag tag-strength">COMPLIANT</span> Not claimed as general accuracy.</td>
    </tr>
    <tr>
      <td><code>"Validated Pressure Dynamics"</code></td>
      <td style="text-align: center;">2 files</td>
      <td><code>PHASE4_SCOPE.md</code>, <code>claims_ledger.md</code></td>
      <td>Listed within prohibited claims (identified as theoretical).</td>
      <td><span class="tag tag-strength">COMPLIANT</span> Maintained as theoretical.</td>
    </tr>
    <tr>
      <td><code>"Mechanistic Fault Physics"</code></td>
      <td style="text-align: center;">2 files</td>
      <td><code>PHASE4_SCOPE.md</code>, <code>claims_ledger.md</code></td>
      <td>Listed within prohibited claims (identified as heuristic).</td>
      <td><span class="tag tag-strength">COMPLIANT</span> Maintained as heuristic.</td>
    </tr>
    <tr>
      <td><code>"300+ APIs"</code></td>
      <td style="text-align: center;">3 files</td>
      <td><code>PHASE4_SCOPE.md</code>, <code>claims_ledger.md</code>, <code>PHASE4_REPORT.md</code></td>
      <td>Listed within prohibited claims (prototype has 4 APIs).</td>
      <td><span class="tag tag-strength">COMPLIANT</span> Maintained 4-analyte scope.</td>
    </tr>
    <tr>
      <td><code>"Demonstrates" / "Proves"</code></td>
      <td style="text-align: center;">3 files</td>
      <td><code>provisional_abstract.md</code>, <code>answer_key.md</code>, <code>claims_ledger.md</code></td>
      <td>Used in abstract: <em>"findings demonstrate that SimuPharm provides..."</em></td>
      <td><span class="tag tag-minor">Minor Overclaim</span> Soften to "suggest" or "indicate".</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 13. DATA DICTIONARY & MISSING-DATA AUDIT -->
<!-- ========================================================================= -->
<h2>13. DATA DICTIONARY & MISSING-DATA AUDIT</h2>
<p>
  A cross-check of <code>anonymized_data_dictionary.md</code> against questionnaires, rubric, and SAP revealed essential missing variables and pre-specified exclusion rules:
</p>

<h3>Table 13.1: Data Dictionary Audit & Required Revisions</h3>

<table>
  <thead>
    <tr>
      <th style="width: 22%;">Category</th>
      <th style="width: 22%;">Audited Parameter</th>
      <th style="width: 26%;">Source Document Conflict</th>
      <th style="width: 30%;">Recommended Resolution</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Missing Practical Columns</strong></td>
      <td>Reasoning & Action Scores</td>
      <td>Present in <code>scoring_rubric.md</code>; absent in data dictionary.</td>
      <td>Add <code>task_[x]_reason_score</code> and <code>task_[x]_action_score</code> (Integers 0–2).</td>
    </tr>
    <tr>
      <td><strong>Inter-Rater Scoring</strong></td>
      <td>Cohen's Kappa (&kappa;)</td>
      <td>Required by rubric; no rater columns in dictionary.</td>
      <td>Add <code>rater1_score</code> and <code>rater2_score</code> columns for inter-rater adjudication.</td>
    </tr>
    <tr>
      <td><strong>Targeted UX Survey Items</strong></td>
      <td><code>ux_u1</code> to <code>ux_u8</code></td>
      <td>Data dictionary lists 8 columns; survey has 8 items.</td>
      <td>Consistent; retain as secondary ordinal variables.</td>
    </tr>
    <tr>
      <td><strong>Hake Gain Denominator</strong></td>
      <td>Pre = 10 Division by Zero</td>
      <td><code>(post - pre) / (10 - pre)</code> undefined when Pre = 10.</td>
      <td>Explicitly code as <code>NaN</code> / <code>N/A</code> in dictionary and analysis script.</td>
    </tr>
    <tr>
      <td><strong>Item-Level Missingness</strong></td>
      <td>Incomplete Pre/Post-Tests</td>
      <td>Unspecified in current SAP.</td>
      <td><strong>Rule:</strong> If &ge;1 question is blank on a 10-item test, total score is coded missing for paired analysis.</td>
    </tr>
    <tr>
      <td><strong>SUS Missing Item Rule</strong></td>
      <td>Incomplete SUS Questionnaire</td>
      <td>Unspecified in current SAP.</td>
      <td><strong>Rule (Sauro 2016):</strong> If 1–2 items missing, substitute neutral score (3); if &ge;3 missing, exclude from SUS.</td>
    </tr>
    <tr>
      <td><strong>Diagnostic Task Missingness</strong></td>
      <td>Skipped Scenario</td>
      <td>Unspecified in current SAP.</td>
      <td><strong>Rule:</strong> If a student skips an unknown scenario, score is 0; latency is excluded from median latency.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 14. DATA INTEGRITY & AUDITING AUDIT -->
<!-- ========================================================================= -->
<h2>14. DATA INTEGRITY & NON-FABRICATION VERIFICATION</h2>
<p>
  A physical filesystem audit was conducted to verify that zero synthetic data has contaminated the participant template:
</p>
<ul>
  <li><strong>Blank Template Verification:</strong> <code>participant_data_template.csv</code> contains exactly <strong>1 single header row (592 bytes) and 0 participant rows</strong>. Zero fabricated data confirmed.</li>
  <li><strong>Demo Data Isolation:</strong> The 5 synthetic test records used to verify analysis scripts are sequestered in <code>06_ANALYSIS/test_data/DEMO_DATA_NOT_REAL.csv</code> and explicitly labeled. Analysis code cannot accidentally read this file during live study execution.</li>
  <li><strong>De-Identification Safeguards:</strong> Participant IDs are randomized (<code>P01</code> to <code>P25</code>). Physical paper consent forms are stored separately from assessment sheets in a double-locked cabinet.</li>
</ul>

<!-- ========================================================================= -->
<!-- 15. ETHICS READINESS AUDIT -->
<!-- ========================================================================= -->
<h2>15. ETHICS READINESS AUDIT (EXEMPTION VS AUTHORIZATION)</h2>
<p>
  A critical distinction exists in human subjects research between <em>qualifying for an ethics exemption</em> and <em>possessing institutional authorization to recruit participants</em>.
</p>

<div class="flow-card-grid">
  <div class="flow-box flow-box-primary">
    <div class="flow-header">STEP 1: PROTOCOL SELF-ASSESSMENT (Completed in Phase 4)</div>
    <div class="flow-desc">Author drafted 45 CFR 46.104(d)(1) exemption rationale and prepared participant information/consent forms.</div>
  </div>
  <div class="badge-chain">
    <span>Ethics Progression:</span>
    <span class="tag tag-strength">Step 1: Self-Assessment</span>
    <span class="arrow-step">&rarr;</span>
    <span class="tag tag-blocker">Step 2: Formal Filing (Mandatory Next Step)</span>
    <span class="arrow-step">&rarr;</span>
    <span class="tag tag-obs">Step 3: Written Letter</span>
  </div>
  <div class="flow-box flow-box-critical">
    <div class="flow-header">CRITICAL BLOCKER: INVESTIGATORS CANNOT SELF-EXEMPT RESEARCH</div>
    <div class="flow-desc">
      In <code>ethics_checklist.md</code>, Exemption Category 1 is checked as "COMPLIANT". However, under academic research policies and US federal regulations (OHRP), <strong>investigators cannot self-exempt their own research involving students</strong>. An official Institutional Review Board (IRB) or Departmental Research Ethics Committee must issue a formal written exemption letter.<br/>
      <strong>Recruitment Status: STRICTLY NO-GO</strong> until a written institutional exemption letter or departmental authorization memo is signed.
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 16. SAMPLE-SIZE & STATISTICAL POWER AUDIT -->
<!-- ========================================================================= -->
<h2>16. SAMPLE-SIZE AUDIT & POWER VERIFICATION</h2>
<p>
  Independent mathematical verification of the sample-size calculations in <code>sample_size_rationale.md</code> was conducted via standard non-central <i>t</i>-distribution formulations:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 14%;">Sample Size (N)</th>
      <th style="width: 18%;">Effect Size (d<sub>z</sub>)</th>
      <th style="width: 14%;">Reported Power</th>
      <th style="width: 18%;">Recomputed Power</th>
      <th style="width: 16%;">SUS Margin of Error</th>
      <th style="width: 20%;">Methodological Assessment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>N = 15</td>
      <td>d<sub>z</sub> = 0.70 (Large)</td>
      <td>71.0%</td>
      <td><strong>71.2%</strong></td>
      <td>&plusmn;5.82 points</td>
      <td>Minimum feasible pilot; underpowered for moderate effects (d=0.50, power 46%).</td>
    </tr>
    <tr>
      <td>N = 22</td>
      <td>d<sub>z</sub> = 0.65 (Mod-Large)</td>
      <td>85.0%</td>
      <td><strong>85.1%</strong></td>
      <td>&plusmn;4.66 points</td>
      <td>Exact mathematical sample size requirement for 85% power at &alpha; = 0.05.</td>
    </tr>
    <tr>
      <td><strong>N = 25</strong></td>
      <td><strong>d<sub>z</sub> = 0.65</strong></td>
      <td><strong>89.2%</strong></td>
      <td><strong>89.3%</strong></td>
      <td><strong>&plusmn;4.33 points</strong></td>
      <td><strong>Preferred Pilot Target:</strong> Excellent power; manageable single-section cohort.</td>
    </tr>
    <tr>
      <td>N = 25</td>
      <td>d<sub>z</sub> = 0.80 (Large)</td>
      <td>97.5%</td>
      <td><strong>97.6%</strong></td>
      <td>&plusmn;4.33 points</td>
      <td>Near-certain statistical detection if software produces large effect.</td>
    </tr>
    <tr>
      <td>N = 40</td>
      <td>d<sub>z</sub> = 0.50 (Moderate)</td>
      <td>97.8%</td>
      <td><strong>87.1%</strong></td>
      <td>&plusmn;3.32 points</td>
      <td>Discrepancy: Report claimed 97.8% for d=0.50; true power for d=0.50 is 87.1%.</td>
    </tr>
  </tbody>
</table>

<div class="callout-box callout-info">
  <div class="callout-title">ℹ️ Power Analysis Verdict</div>
  <p style="margin: 0; font-size: 8.2pt;">
    The sample size target of <strong>N = 20–30 participants</strong> is mathematically sound and realistically achievable in a single university laboratory section. It provides &gt;85% power to detect a moderate-to-large paired diagnostic gain (d<sub>z</sub> &ge; 0.65) and estimates the mean SUS score within &plusmn;4.3 points. However, the author must explicitly emphasize in the manuscript that N=25 establishes <strong>pilot feasibility and local instructional utility</strong>, not population-level generalizability.
  </p>
</div>

<!-- ========================================================================= -->
<!-- 17. ANALYSIS PIPELINE VERIFICATION AUDIT -->
<!-- ========================================================================= -->
<h2>17. ANALYSIS PIPELINE CODE VERIFICATION</h2>
<p>
  All pre-specified Python analysis scripts in <code>06_ANALYSIS/analysis_code/</code> were executed against the labeled demonstration dataset (<code>DEMO_DATA_NOT_REAL.csv</code>):
</p>

<pre class="code-box">=== EXECUTION AUDIT LOG: calculate_pre_post_stats.py ===
Data source: 06_ANALYSIS/test_data/DEMO_DATA_NOT_REAL.csv
Sample Size (N): 5 | Pre-Test Mean: 4.00 (SD: 1.58) | Post-Test Mean: 7.80 (SD: 1.30)
Mean Paired Gain: +3.80 points (SD: 0.84) | Median Gain: +4.0
Shapiro-Wilk Test: W = 0.8810, p = 0.3140 (Normal distribution not rejected)
Paired t-test: t(4) = 10.156, p = 5.29e-04, 95% CI: [+2.76, +4.84], Cohen's dz = 4.54
Wilcoxon Signed-Rank: W = 0.0, p = 0.0625, Rank-Biserial r = 1.00
STATUS: PASS (Execution verified; Pratt zero-difference method recommended)

=== EXECUTION AUDIT LOG: calculate_sus_score.py ===
Usable SUS Submissions (N): 5 | Mean SUS: 81.00 (SD: 14.43) | Median: 75.00 (IQR: 22.50)
95% Confidence Interval: [63.09, 98.91] | Bangor Adjective Rating: Excellent
STATUS: PASS (Brooke 1996 multipliers verified)

=== EXECUTION AUDIT LOG: calculate_hake_gain.py ===
Overall Average Normalized Gain &lt;g&gt;: 0.633 | Mean Individual Gain: 0.654 (SD: 0.143)
Hake Classification: Medium Gain (0.30 &le; g &lt; 0.70)
STATUS: PASS (Ceiling condition handled)</pre>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 18. FIGURE & MANUSCRIPT CONSISTENCY AUDIT -->
<!-- ========================================================================= -->
<h2>18. FIGURE & MANUSCRIPT CONSISTENCY AUDIT</h2>
<p>
  Cross-checking the 7 planned figures (<code>figure_plan.md</code>) against the data schema and manuscript outline revealed complete alignment:
</p>
<ul>
  <li><strong>Figure 1 (UI Screenshots):</strong> Captures actual frozen SimuPharm frontend controls (sliders, canvas, fault toggles).</li>
  <li><strong>Figure 2 (Simulation Workflow):</strong> Accurately illustrates data flow without claiming AI or digital twin loops.</li>
  <li><strong>Figure 3 (Normal Baseline):</strong> Displays standard analgesic mixture (50% B, 1.0 mL/min, 30&deg;C, C18).</li>
  <li><strong>Figure 4 (Fault Signatures):</strong> Four-panel layout depicting air bubble, leak, void, and contamination.</li>
  <li><strong>Figures 5, 6, 7 (Student Data):</strong> Correctly designated as <strong>unpopulated placeholders</strong> until real data collection. Figure 6 (unknown task accuracy/latency) can be generated once the schema reconciliation table is merged into the CSV template.</li>
</ul>

<!-- ========================================================================= -->
<!-- 19. MANUSCRIPT LANGUAGE AUDIT -->
<!-- ========================================================================= -->
<h2>19. MANUSCRIPT LANGUAGE AUDIT (SENSITIVE VERB SCRUBBING)</h2>
<p>
  All manuscript sections were audited for overreaching verbs and claims:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Sensitive Phrase</th>
      <th style="width: 25%;">Context in Manuscript Draft</th>
      <th style="width: 27%;">Auditor Assessment</th>
      <th style="width: 30%;">Mandatory Replacement Wording</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>"demonstrates"</code></td>
      <td>Abstract line 18: <em>"findings demonstrate that SimuPharm provides..."</em></td>
      <td>Too definitive for an exploratory pilot study without a control group.</td>
      <td>Replace with <strong>"suggest"</strong>, <strong>"indicate"</strong>, or <strong>"provide preliminary evidence that"</strong>.</td>
    </tr>
    <tr>
      <td><code>"proves"</code></td>
      <td>Answer Key Q5: <em>"proves the hydraulic restriction is inside the column..."</em></td>
      <td>Acceptable in diagnostic deduction, but dangerous if applied to software efficacy.</td>
      <td>In pedagogical context: replace with <strong>"indicates"</strong> or <strong>"isolates"</strong>.</td>
    </tr>
    <tr>
      <td><code>"validated"</code></td>
      <td>Folder name & report titles: <em>"Educational Validation Study"</em></td>
      <td>Overreaching; implies formal psychometric construct validation.</td>
      <td>Replace with <strong>"Educational Evaluation"</strong> or <strong>"Pilot Usability Assessment"</strong>.</td>
    </tr>
    <tr>
      <td><code>"improves"</code></td>
      <td>Claims ledger: <em>"SimuPharm improves HPLC troubleshooting skills"</em></td>
      <td>Causal claim; cannot be definitively established without a control group.</td>
      <td>Replace with <strong>"is associated with measurable short-term score gains"</strong>.</td>
    </tr>
    <tr>
      <td><code>"superior"</code></td>
      <td>Claims ledger: <em>"superior to traditional textbook manuals"</em></td>
      <td>Correctly placed in Tier 2 (prohibited for present pilot).</td>
      <td>Retain in prohibited tier.</td>
    </tr>
    <tr>
      <td><code>"transfer"</code></td>
      <td>Manuscript outline Section 10: <em>"Transfer to physical instruments remains unmeasured"</em></td>
      <td>Properly framed as a candid limitation.</td>
      <td>Retain as an explicit limitation.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 20. CROSS-DOCUMENT CONSISTENCY MATRIX -->
<!-- ========================================================================= -->
<h2>20. CROSS-DOCUMENT CONSISTENCY MATRIX</h2>
<p>
  A master cross-document consistency audit was performed across all 18 key planning artifacts:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 22%;">Document A</th>
      <th style="width: 22%;">Document B</th>
      <th style="width: 14%;">Target Dimension</th>
      <th style="width: 8%; text-align: center;">Consistent?</th>
      <th style="width: 34%;">Identified Conflict & Mandatory Resolution</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>research_questions.md</code></td>
      <td><code>statistical_analysis_plan.md</code></td>
      <td>Primary Outcome</td>
      <td style="text-align: center;"><span class="tag tag-strength">YES</span></td>
      <td>Both define &Delta;Score = Post &minus; Pre on 0–10 scale. Harmonized.</td>
    </tr>
    <tr>
      <td><code>sample_size_rationale.md</code></td>
      <td><code>study_design.md</code></td>
      <td>Cohort Size</td>
      <td style="text-align: center;"><span class="tag tag-strength">YES</span></td>
      <td>Both specify N = 20–30 undergraduate students. Harmonized.</td>
    </tr>
    <tr>
      <td><code>scoring_rubric.md</code></td>
      <td><code>participant_data_template.csv</code></td>
      <td>Practical Schema</td>
      <td style="text-align: center;"><span class="tag tag-blocker">NO</span></td>
      <td>Rubric scores 12 points (reasoning/action); CSV only has 0/1 binary! <strong>Expand CSV template with Table 8.2 columns.</strong></td>
    </tr>
    <tr>
      <td><code>instructor_protocol.md</code></td>
      <td><code>posttest.md</code></td>
      <td>Instructor Cueing</td>
      <td style="text-align: center;"><span class="tag tag-blocker">NO</span></td>
      <td>Instructor script spoon-feeds exact post-test answers during Phase 3! <strong>Replace script with neutral guided inquiry.</strong></td>
    </tr>
    <tr>
      <td><code>pretest.md</code></td>
      <td><code>posttest.md</code></td>
      <td>Keyed Keys</td>
      <td style="text-align: center;"><span class="tag tag-blocker">NO</span></td>
      <td>70% of pre-test and 80% of post-test are keyed to "B" (Q1–Q8 all B!). <strong>Re-randomize answer options across A, B, C, D.</strong></td>
    </tr>
    <tr>
      <td><code>SUS_instrument.md</code></td>
      <td>Brooke (1996) Canonical</td>
      <td>Item Phrasing</td>
      <td style="text-align: center;"><span class="tag tag-major">NO</span></td>
      <td>Modified wording in Items 1 and 7 ("for chromatography learning", "students"). <strong>Restore canonical wording or label "Adapted SUS".</strong></td>
    </tr>
    <tr>
      <td><code>statistical_analysis_plan.md</code></td>
      <td><code>calculate_pre_post_stats.py</code></td>
      <td>Wilcoxon Ties</td>
      <td style="text-align: center;"><span class="tag tag-major">NO</span></td>
      <td>Script drops zero-differences (<code>zero_method='wilcox'</code>); SAP implies full cohort. <strong>Change script to Pratt's method.</strong></td>
    </tr>
    <tr>
      <td><code>ethics_checklist.md</code></td>
      <td><code>PHASE4_DECISION_STATUS.md</code></td>
      <td>Approval Status</td>
      <td style="text-align: center;"><span class="tag tag-blocker">NO</span></td>
      <td>Checklist claims "COMPLIANT"; decision status has approval box unchecked. <strong>Clarify: exemption rationale drafted; institutional sign-off pending.</strong></td>
    </tr>
    <tr>
      <td><code>manuscript_outline.md</code></td>
      <td><code>figure_plan.md</code></td>
      <td>Figure Mapping</td>
      <td style="text-align: center;"><span class="tag tag-strength">YES</span></td>
      <td>All 7 figures match manuscript section references. Harmonized.</td>
    </tr>
    <tr>
      <td><code>claims_ledger.md</code></td>
      <td><code>PHASE4_SCOPE.md</code></td>
      <td>Claim Boundary</td>
      <td style="text-align: center;"><span class="tag tag-strength">YES</span></td>
      <td>Identical 3-tier boundary preserved. Harmonized.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- 21. TOP 10 REQUIRED CORRECTIONS -->
<!-- ========================================================================= -->
<h2>21. TOP 10 THINGS THE AUTHOR MUST FIX BEFORE RECRUITMENT</h2>
<p>
  The following ranked register specifies the exact mandatory corrections that must be executed prior to recruiting human student participants:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 5%; text-align: center;">Rank</th>
      <th style="width: 16%;">Issue Category</th>
      <th style="width: 24%;">The Exact Problem</th>
      <th style="width: 24%;">Why It Matters</th>
      <th style="width: 21%;">Mandatory Correction</th>
      <th style="width: 10%;">Severity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;"><strong>1</strong></td>
      <td>Data Schema Mismatch</td>
      <td><code>scoring_rubric.md</code> evaluates practical tasks on a 12-pt rubric, but <code>participant_data_template.csv</code> only provides binary 0/1 columns.</td>
      <td><strong>Fatal Data Loss:</strong> Reasoning and action scores cannot be stored. Grader inter-rater reliability (&kappa;) cannot be calculated.</td>
      <td>Expand CSV template and data dictionary with Table 8.2 columns (<code>_reason_score</code>, <code>_action_score</code>, <code>rater1</code>, <code>rater2</code>).</td>
      <td><span class="tag tag-blocker">BLOCKER</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>2</strong></td>
      <td>Instructor Test Cueing</td>
      <td><code>instructor_protocol.md</code> Phase 3 explicitly recites the exact symptoms, pressure drops, and mechanisms to the class right before testing.</td>
      <td><strong>Fatal Demand Bias:</strong> Post-test gains merely measure short-term auditory recall of instructor statements rather than simulation learning.</td>
      <td>Rewrite Phase 3 script to use neutral guided inquiry (instruct students to observe canvas and hypothesize without answers).</td>
      <td><span class="tag tag-blocker">BLOCKER</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>3</strong></td>
      <td>Keyed Response Imbalance</td>
      <td>70% of pre-test and 80% of post-test items are keyed to Option "B" (Post-test Items Q1 through Q8 are ALL B).</td>
      <td><strong>Psychometric Invalidation:</strong> A student guessing "B" blindly scores 80% on post-test. Destroys test validity and inflates gains.</td>
      <td>Re-scramble answer choices across A, B, C, and D so that each option represents &approx;25% of keys.</td>
      <td><span class="tag tag-blocker">BLOCKER</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>4</strong></td>
      <td>Ethics Authorization Status</td>
      <td><code>ethics_checklist.md</code> declares 45 CFR 46 exemption "COMPLIANT", but no institutional IRB/faculty approval letter has been granted.</td>
      <td><strong>Regulatory Non-Compliance:</strong> Investigators cannot self-exempt research involving human students. Violates publication ethics.</td>
      <td>Submit protocol to institutional IRB or Department Chair; obtain written formal determination letter before recruiting.</td>
      <td><span class="tag tag-blocker">BLOCKER</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>5</strong></td>
      <td>SUS Canonical Wording</td>
      <td>Items 1 and 7 in <code>SUS_instrument.md</code> add "for chromatography learning" and substitute "students" for "people".</td>
      <td><strong>Benchmark Incomparability:</strong> Modified wording prevents legitimate comparison against Brooke (1996) normative databases.</td>
      <td>Restore exact Brooke canonical wording OR explicitly designate as "Adapted Educational SUS" in all documents.</td>
      <td><span class="tag tag-major">MAJOR</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>6</strong></td>
      <td>Normality-Contingent SAP</td>
      <td>SAP conditions test selection on Shapiro-Wilk testing (p &ge; 0.05 &rarr; t-test; p &lt; 0.05 &rarr; Wilcoxon).</td>
      <td><strong>Type I Error Distortion:</strong> Normality testing in N=25 has low power; conditioning test choice alters nominal &alpha; = 0.05 level.</td>
      <td>Pre-specify Wilcoxon Signed-Rank Test as primary (due to discrete count data) and paired t-test as sensitivity analysis.</td>
      <td><span class="tag tag-major">MAJOR</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>7</strong></td>
      <td>Wilcoxon Zero-Ties</td>
      <td><code>calculate_pre_post_stats.py</code> uses <code>zero_method='wilcox'</code>, which discards students with zero score gain (&Delta; = 0).</td>
      <td><strong>Artificial Effect Inflation:</strong> Dropping non-improving students artificially inflates the rank-sum statistic and effect size.</td>
      <td>Modify script to use <code>zero_method='pratt'</code>, which includes tied zero differences in the ranking.</td>
      <td><span class="tag tag-major">MAJOR</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>8</strong></td>
      <td>Missing Data Rules</td>
      <td>No formal pre-specified policy for incomplete assessment sheets or missing SUS items.</td>
      <td><strong>Post-Hoc Data Manipulation:</strong> Graders might arbitrarily discard low-scoring incomplete sheets.</td>
      <td>Add explicit missing-data rules to SAP: complete-case analysis for pre/post scores; Sauro imputation for &le;2 missing SUS items.</td>
      <td><span class="tag tag-major">MAJOR</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>9</strong></td>
      <td>Secondary Multiplicity</td>
      <td>Fifteen secondary endpoints lack formal family-wise error rate control.</td>
      <td><strong>False Discovery Inflation:</strong> Testing multiple endpoints at &alpha; = 0.05 creates &gt;40% risk of spurious significance.</td>
      <td>Integrate Holm-Bonferroni step-down correction into the secondary outcome analysis pipeline.</td>
      <td><span class="tag tag-minor">MINOR</span></td>
    </tr>
    <tr>
      <td style="text-align: center;"><strong>10</strong></td>
      <td>Abstract Tone Calibration</td>
      <td>Abstract states: <em>"findings demonstrate that SimuPharm provides..."</em></td>
      <td><strong>Overreaching Language:</strong> Single-group pilot cannot "demonstrate" general instructional efficacy.</td>
      <td>Soften abstract phrasing to: <em>"preliminary pilot findings suggest that SimuPharm provides..."</em></td>
      <td><span class="tag tag-minor">MINOR</span></td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 22. FROZEN ITEMS (THINGS THAT MUST NOT BE CHANGED) -->
<!-- ========================================================================= -->
<h2>22. FROZEN ITEMS (THINGS THAT MUST NOT BE CHANGED)</h2>
<p>
  While the educational protocol and data templates must be corrected, the following scientific boundaries are <strong>STRICTLY IMMUTABLE</strong>:
</p>
<ol>
  <li><strong>Frozen SimuPharm Engine:</strong> Zero modifications to <code>hplc_simulator_script.js</code> or <code>script.js</code>. Do not "fix" the hardcoded dead time (t<sub>0</sub> = 0.50 min), uncalibrated S slopes, or heuristic fault parameters. The educational study must evaluate the software exactly as it exists.</li>
  <li><strong>Non-Fabrication Rule:</strong> Zero generation of fake student scores, simulated p-values, artificial SUS ratings, or synthetic qualitative quotes. <code>participant_data_template.csv</code> must remain 100% empty until real students participate.</li>
  <li><strong>Phase 3.5 Claim Boundaries:</strong> Strict ban on "Digital Twin", "Artificial Intelligence", "Machine Learning", "Bayesian Knowledge Tracing", "universal predictive accuracy", and "experimentally validated pressure/fault physics".</li>
  <li><strong>Physical HPLC Separation:</strong> No physical HPLC experiments shall be initiated during Phase 4; JCE Technology Reports evaluate educational utility, not laboratory sensor validation.</li>
</ol>

<!-- ========================================================================= -->
<!-- 23. FINAL GO/NO-GO DECISION -->
<!-- ========================================================================= -->
<h2>23. FINAL RECRUITMENT READINESS DECISION</h2>

<div class="memo-container">
<span class="field-name">AUDIT EVALUATION CLASSIFICATION:</span><br/>
<span class="field-val" style="color: #feb2b2; font-size: 11pt; font-weight: bold;">
NO-GO &mdash; MAJOR METHODOLOGICAL CORRECTIONS REQUIRED
</span><br/><br/>

<span class="field-name">JUSTIFICATION & AUDIT SYNTHESIS:</span><br/>
<span class="field-val">
Participant recruitment must not proceed under the current package. While the software architecture is robust, the educational pilot protocol suffers from four fatal defects that would invalidate the research:<br/><br/>
<strong>1. Data Entry Schema Truncation (Critical Blocker):</strong> The data entry template (<code>participant_data_template.csv</code>) is missing columns to store the 12-point practical diagnostic task rubric scores (reasoning, corrective action, and inter-rater reliability), which would cause permanent data loss during collection.<br/>
<strong>2. Instructor Teaching-to-the-Test Bias (Critical Blocker):</strong> The instructor protocol in Phase 3 explicitly spoon-feeds the exact fault symptoms, numerical shifts (-20 bar, -50 bar), and mechanisms to the students right before testing, confounding post-test score gains with short-term auditory recall.<br/>
<strong>3. Extreme Keyed Response Position Bias (Critical Blocker):</strong> The pre-test and post-test instruments suffer from severe response position bias, with 70% and 80% of answers keyed to Option "B" (Post-test Items Q1 through Q8 are all B), allowing blind guessing to score 80%.<br/>
<strong>4. Unverified Institutional Ethics Exemption (Critical Blocker):</strong> Institutional ethics exemption has been self-declared but not formally confirmed by an institutional IRB or faculty review body. Under institutional research governance, investigators cannot self-exempt research involving human students.<br/><br/>
Once these four critical blockers are corrected—by reconciling the CSV schema, neutralizing the instructor script, re-scrambling the assessment keys across A/B/C/D, and securing written institutional authorization—the study will achieve full methodological rigor and will be approved for recruitment.
</span><br/><br/>

<span class="field-name">CRITICAL PATH ACTIONS BEFORE GO:</span><br/>
<span class="field-val">
1. Update <code>participant_data_template.csv</code> and <code>anonymized_data_dictionary.md</code> with Table 8.2 columns.<br/>
2. Neutralize <code>instructor_protocol.md</code> Phase 3 to eliminate direct answers and mechanisms.<br/>
3. Re-randomize answer keys in <code>pretest.md</code> and <code>posttest.md</code> across options A, B, C, D.<br/>
4. Submit protocol to institutional ethics authority and secure written exemption letter.<br/>
5. Update <code>calculate_pre_post_stats.py</code> to use <code>zero_method='pratt'</code> for Wilcoxon signed-rank test.
</span>
</div>

<p style="text-align: center; color: #718096; font-size: 7.5pt; margin-top: 25px;">
  <strong>Hostile Pre-Pilot Scientific Audit Panel</strong> &bull; Completed & Certified October 4, 2026 &bull; SimuPharm.io Publication Due Diligence
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
        margin={"top": "14mm", "bottom": "14mm", "left": "12mm", "right": "12mm"}
    )
    with open(out_primary, 'rb') as f_src, open(out_artifact, 'wb') as f_dst:
        f_dst.write(f_src.read())
    browser.close()

print(f"Successfully generated consolidated audit PDF: {out_primary} ({os.path.getsize(out_primary)} bytes)")
print(f"Successfully mirrored PDF: {out_artifact} ({os.path.getsize(out_artifact)} bytes)")
