import os
import sys
from playwright.sync_api import sync_playwright

dir_primary = r"c:\Users\dsant\OneDrive\simupro - Copy\SIMUPHARM_PHASE4_2_CORRECTED_EDUCATIONAL_STUDY"
dir_artifact = r"C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\SIMUPHARM_PHASE4_2_CORRECTED_EDUCATIONAL_STUDY"
os.makedirs(dir_primary, exist_ok=True)
os.makedirs(dir_artifact, exist_ok=True)

pdf_filename = "SIMUPHARM_PHASE4_2_2_FINAL_STATISTICAL_GOVERNANCE_CHECK.pdf"
out_primary = os.path.join(dir_primary, pdf_filename)
out_artifact = os.path.join(dir_artifact, pdf_filename)

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SimuPharm Phase 4.2.2 — Final Statistical & Governance Sanity Check</title>
<style>
  @page {
    size: A4;
    margin: 10mm 9mm 10mm 9mm;
    @top-left {
      content: "SimuPharm Phase 4.2.2 | Final Statistical & Governance Sanity Check";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.8pt;
      color: #1a365d;
      font-weight: 700;
    }
    @top-right {
      content: "TECHNICAL SANITY AUDIT & REGULATORY CERTIFICATION";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.8pt;
      color: #718096;
      font-weight: 600;
    }
    @bottom-left {
      content: "CONFIDENTIAL & PRIVILEGED | FINAL AUDIT BEFORE EMPIRICAL ENROLLMENT";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.5pt;
      color: #a0aec0;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.8pt;
      color: #4a5568;
      font-weight: 600;
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a202c;
    line-height: 1.27;
    font-size: 7.7pt;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  h1 {
    font-size: 16pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 2px 0;
    letter-spacing: -0.4px;
  }

  h2 {
    font-size: 9.3pt;
    font-weight: 700;
    color: #1e293b;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 2px;
    margin-top: 7px;
    margin-bottom: 3px;
    break-after: avoid;
    page-break-after: avoid;
  }

  h3 {
    font-size: 8.0pt;
    font-weight: 700;
    color: #334155;
    margin-top: 5px;
    margin-bottom: 2px;
    break-after: avoid;
    page-break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 3px;
    text-align: justify;
  }

  ul, ol {
    margin-top: 2px;
    margin-bottom: 3px;
    padding-left: 16px;
  }

  li {
    margin-bottom: 1.5px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 2px;
    margin-bottom: 5px;
    font-size: 6.8pt;
    page-break-inside: auto;
  }

  tr {
    page-break-inside: avoid;
    page-break-after: auto;
  }

  th, td {
    border: 1px solid #cbd5e1;
    padding: 2.2px 3.5px;
    text-align: left;
    vertical-align: top;
  }

  th {
    background-color: #f1f5f9;
    font-weight: 700;
    color: #0f172a;
  }

  .badge {
    display: inline-block;
    padding: 1px 4px;
    border-radius: 3px;
    font-weight: 700;
    font-size: 6.5pt;
    text-transform: uppercase;
  }
  .badge-pass { background-color: #dcfce7; color: #15803d; border: 1px solid #86efac; }
  .badge-warn { background-color: #fef9c3; color: #854d0e; border: 1px solid #fde047; }
  .badge-stop { background-color: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
  .badge-info { background-color: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }

  .callout {
    border-left: 3px solid #0284c7;
    background-color: #f0f9ff;
    padding: 5px 8px;
    margin-top: 4px;
    margin-bottom: 6px;
    border-radius: 0 4px 4px 0;
    font-size: 7.5pt;
  }

  .callout-alert {
    border-left: 3px solid #dc2626;
    background-color: #fef2f2;
    padding: 5px 8px;
    margin-top: 4px;
    margin-bottom: 6px;
    border-radius: 0 4px 4px 0;
    font-size: 7.5pt;
  }

  .callout-success {
    border-left: 3px solid #16a34a;
    background-color: #f0fdf4;
    padding: 5px 8px;
    margin-top: 4px;
    margin-bottom: 6px;
    border-radius: 0 4px 4px 0;
    font-size: 7.5pt;
  }

  .code-inline {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 6.8pt;
    background-color: #f1f5f9;
    padding: 1px 3px;
    border-radius: 2px;
    border: 1px solid #e2e8f0;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- HEADER & TITLE -->
<!-- ========================================================================= -->
<div style="border-bottom: 2px solid #0f172a; padding-bottom: 5px; margin-bottom: 8px;">
  <div style="display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
      <span class="badge badge-info" style="margin-bottom: 3px;">PHASE 4.2.2 TECHNICAL & GOVERNANCE SANITY AUDIT</span>
      <h1 style="margin: 2px 0 2px 0;">SimuPharm Educational Pilot Evaluation</h1>
      <div style="font-size: 8.5pt; font-weight: 600; color: #475569;">
        Final Pre-Recruitment Statistical Verification, Schema Validation & Governance Lock
      </div>
    </div>
    <div style="text-align: right; font-size: 7.0pt; color: #64748b;">
      <div><strong>Date:</strong> October 4, 2026</div>
      <div><strong>Status:</strong> <span class="badge badge-stop">NO-GO — ETHICS PENDING</span></div>
      <div><strong>Engine State:</strong> <span class="badge badge-pass">PASS — ENGINE FROZEN</span></div>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 1. EXECUTIVE SUMMARY & CHECKS PERFORMED -->
<!-- ========================================================================= -->
<h2>1. EXECUTIVE SUMMARY & AUDIT SCOPE</h2>
<p>
  This technical audit constitutes the definitive sanity check of the pre-recruitment protocol package for the <strong>SimuPharm Educational Evaluation Study</strong>. In strict compliance with the Phase 4 charter, <strong>no study redesign has been performed, no simulation source code has been altered, no participant-facing features or arms have been added, and no student data has been simulated</strong>. The audit examined all statistical code implementations, non-parametric effect sizes, confidence interval mathematics, data dictionary schemas, multiple-comparison hierarchies, 50-minute session logistics, and publication claims across the repository.
</p>

<div class="callout-success">
  <strong>Key Audit Outcome:</strong> All computational implementations (paired Pratt Wilcoxon, signed rank-biserial correlation, Walsh-average order-statistic confidence intervals, and complete-case filtering) have been verified across 7 stress-test edge cases. All overreaching claim language and unsupported journal compliance declarations have been systematically purged. The protocol package is methodologically and statistically sealed.
</div>

<!-- ========================================================================= -->
<!-- 2. ISSUES IDENTIFIED & CORRECTIONS MADE -->
<!-- ========================================================================= -->
<h2>2. ISSUES IDENTIFIED & CORRECTIONS IMPLEMENTED</h2>
<table>
  <thead>
    <tr>
      <th style="width: 4%;">#</th>
      <th style="width: 20%;">Audit Domain</th>
      <th style="width: 33%;">Issue Identified in Frozen Package</th>
      <th style="width: 33%;">Corrective Action Implemented</th>
      <th style="width: 10%;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1</strong></td>
      <td><strong>Analysis Terminology</strong></td>
      <td>Primary outcome labeled as "Primary Confirmatory Analysis", inappropriately implying definitive evidence of educational effectiveness for an exploratory pilot ($N \approx 25$).</td>
      <td>Replaced with <strong>"Primary Prespecified Inferential Analysis"</strong> across all research questions, SAP, and analysis plans. Confirmatory framing removed.</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>2</strong></td>
      <td><strong>Wilcoxon SciPy Edge Case</strong></td>
      <td>SciPy's <code class="code-inline">stats.wilcoxon(..., zero_method='pratt')</code> raises an unhandled <code class="code-inline">ValueError</code> when all paired differences are zero ($\Delta\text{Score} = 0 \ \forall i$).</td>
      <td>Implemented an explicit all-zero difference safeguard: catches zero-difference arrays and returns $W = 0$, $p = 1.0$, $r_{rb} = 0.0$, and Hodges-Lehmann difference $= 0.0$.</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>3</strong></td>
      <td><strong>Effect-Size Direction Flaw</strong></td>
      <td>Formula $r = 1 - \frac{2W}{S}$ using SciPy's test statistic $W = \min(W^+, W^-)$ flips signs and yields $+1.0$ for both all-positive and all-negative differences.</td>
      <td>Replaced with the exact signed rank-biserial formula: $r_{rb} = \frac{W^+ - W^-}{W^+ + W^-}$. Positive indicates improvement, negative indicates deterioration, zero indicates null effect.</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>4</strong></td>
      <td><strong>Hodges–Lehmann CI Audit</strong></td>
      <td>The protocol stated a "95% BCa bootstrap confidence interval" for Hodges–Lehmann, but it was unbuilt in code and mathematically prone to jackknife instability for discrete scores.</td>
      <td>Implemented the exact <strong>Walsh-average order-statistic confidence interval (Bauer 1972; Hollander & Wolfe 1999)</strong>, which directly inverts the Wilcoxon signed-rank test.</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>5</strong></td>
      <td><strong>Confidence-Calibration Scope</strong></td>
      <td>Certain sections previously referenced confidence analysis as demonstrating "calibrated metacognition" or "simulator-induced calibration".</td>
      <td>Re-anchored strictly as an <strong>exploratory confidence–performance association indicator</strong> (Spearman $\rho$, Pearson $r$). All causal claims excised.</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>6</strong></td>
      <td><strong>Expert Review Thresholds</strong></td>
      <td>Lynn (1986) cutoffs ($\text{I-CVI} \ge 0.80$, $\text{S-CVI/Ave} \ge 0.90$) were presented as universal mandatory hurdles rather than descriptive panel-size benchmarks.</td>
      <td>Specified exact panel size (3–5 experts), formulas, and noted that small $N$ requires unanimous consensus ($3/3$) or $4/5$; characterized as descriptive benchmarks.</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>7</strong></td>
      <td><strong>Open-Science Compliance Claim</strong></td>
      <td>Claimed all assets conform to "JCE Transparency and Openness Promotion (TOP) Guidelines Level 2" without external journal verification.</td>
      <td>Excised TOP Level 2 claim; replaced with: <em>"Open-science practices are structured to support transparency, reproducibility, and responsible data/code sharing."</em></td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>8</strong></td>
      <td><strong>Multiple-Testing Family</strong></td>
      <td>All 5 secondary metrics (Rubric, Latency, Calibration, SUS, Hake) were lumped into a single Holm family, combining hypothesis tests with descriptive indices.</td>
      <td>Restructured into a 3-tier hierarchy: (1) Primary Prespecified Inferential; (2) Secondary Inferential (SUS, Rubric; Holm $k=2$); (3) Exploratory & Descriptive.</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>9</strong></td>
      <td><strong>50-Minute Lab Feasibility</strong></td>
      <td>Answering 3 extensive qualitative reflection prompts alongside 10 post-test items, 10 SUS items, and 8 UX items in 10 min risked severe cognitive strain.</td>
      <td>Shortened qualitative instructions: explicitly designated as optional bullet-point/short-phrase feedback (1–2 sentences, $\le 30$ words), preserving the 50-min ceiling.</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
    <tr>
      <td><strong>10</strong></td>
      <td><strong>Answer Key Claim Wording</strong></td>
      <td>Answer key rationale for Post-Test Q4 asserted that peak area scaling "proves contamination".</td>
      <td>Calibrated to "indicates contaminants accumulate from weak mobile phase component during equilibration."</td>
      <td><span class="badge badge-pass">RESOLVED</span></td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 3. STATISTICAL IMPLEMENTATION VERIFICATION -->
<!-- ========================================================================= -->
<h2>3. STATISTICAL IMPLEMENTATION VERIFICATION (DEMO_TEST_ONLY SUITE)</h2>
<p>
  A dedicated technical verification script (<code class="code-inline">verify_wilcoxon_pipeline.py</code>) was executed across seven synthetic stress-test datasets representing mathematical boundary conditions. No participant data was generated or analyzed:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 14%;">Dataset Case</th>
      <th style="width: 22%;">Synthetic Paired Scores</th>
      <th style="width: 18%;">Wilcoxon Pratt Output</th>
      <th style="width: 14%;">Signed $r_{rb}$</th>
      <th style="width: 18%;">Hodges–Lehmann & 95% CI</th>
      <th style="width: 14%;">Technical Verification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Case A: All Positive</strong></td>
      <td>Pre: [2, 3, 4, 3, 2, 4, 3, 2]<br/>Post: [5, 6, 7, 6, 5, 8, 7, 6]<br/>$\Delta$: [+3, +3, +3, +3, +3, +4, +4, +4]</td>
      <td>$W^+ = 36.0, \ W^- = 0.0$<br/>$W = 0.0, \ p = 0.00781$</td>
      <td style="text-align: center;"><strong style="color: #15803d;">+1.000</strong></td>
      <td>HL = +3.50<br/>95% Walsh: [+3.00, +4.00]</td>
      <td><span class="badge badge-pass">PASS: Strict Positive</span></td>
    </tr>
    <tr>
      <td><strong>Case B: All Negative</strong></td>
      <td>Pre: [6, 7, 8, 7, 6, 8, 7, 6]<br/>Post: [3, 4, 5, 4, 3, 5, 4, 3]<br/>$\Delta$: [-3, -3, -3, -3, -3, -3, -3, -3]</td>
      <td>$W^+ = 0.0, \ W^- = 36.0$<br/>$W = 0.0, \ p = 0.00781$</td>
      <td style="text-align: center;"><strong style="color: #b91c1c;">-1.000</strong></td>
      <td>HL = -3.00<br/>95% Walsh: [-3.00, -3.00]</td>
      <td><span class="badge badge-pass">PASS: Strict Negative</span></td>
    </tr>
    <tr>
      <td><strong>Case C: Mixed Differences</strong></td>
      <td>Pre: [3, 4, 5, 6, 4, 5, 3, 6]<br/>Post: [6, 5, 4, 7, 6, 4, 5, 8]<br/>$\Delta$: [+3, +1, -1, +1, +2, -1, +2, +2]</td>
      <td>$W^+ = 31.0, \ W^- = 5.0$<br/>$W = 5.0, \ p = 0.07813$</td>
      <td style="text-align: center;"><strong>+0.722</strong></td>
      <td>HL = +1.25<br/>95% Walsh: [0.00, +2.50]</td>
      <td><span class="badge badge-pass">PASS: Proportional Rank</span></td>
    </tr>
    <tr>
      <td><strong>Case D: Zeros Present</strong></td>
      <td>Pre: [4, 5, 5, 6, 3, 4, 5, 5]<br/>Post: [6, 5, 7, 6, 5, 4, 8, 5]<br/>$\Delta$: [+2, 0, +2, 0, +2, 0, +3, 0]</td>
      <td>$W^+ = 26.0, \ W^- = 0.0$<br/>$W = 0.0, \ p = 0.04743$</td>
      <td style="text-align: center;"><strong>+1.000</strong></td>
      <td>HL = +1.00<br/>95% Walsh: [0.00, +2.50]</td>
      <td><span class="badge badge-pass">PASS: Pratt Zeros Preserved</span></td>
    </tr>
    <tr>
      <td><strong>Case E: All Zeros</strong></td>
      <td>Pre: [5, 5, 5, 5, 5]<br/>Post: [5, 5, 5, 5, 5]<br/>$\Delta$: [0, 0, 0, 0, 0]</td>
      <td>$W^+ = 0.0, \ W^- = 0.0$<br/>$W = 0.0, \ p = 1.00000$</td>
      <td style="text-align: center;"><strong>0.000</strong></td>
      <td>HL = 0.00<br/>95% Walsh: [0.00, 0.00]</td>
      <td><span class="badge badge-pass">PASS: Crash Safeguard</span></td>
    </tr>
    <tr>
      <td><strong>Case F: Balanced Ties</strong></td>
      <td>Pre: [3, 3, 3, 3, 3, 3]<br/>Post: [5, 5, 5, 1, 1, 1]<br/>$\Delta$: [+2, +2, +2, -2, -2, -2]</td>
      <td>$W^+ = 10.5, \ W^- = 10.5$<br/>$W = 10.5, \ p = 1.00000$</td>
      <td style="text-align: center;"><strong>0.000</strong></td>
      <td>HL = 0.00<br/>95% Walsh: [-2.00, +2.00]</td>
      <td><span class="badge badge-pass">PASS: Average Ties Null</span></td>
    </tr>
    <tr>
      <td><strong>Case G: Missing Values</strong></td>
      <td>Pre: [3, 4, NaN, 5, 6, NaN, 4]<br/>Post: [5, NaN, 6, 7, 6, NaN, 7]<br/>Pairs: 4 valid, 3 excluded</td>
      <td>$W^+ = 9.0, \ W^- = 0.0$<br/>$W = 0.0, \ p = 0.09182$</td>
      <td style="text-align: center;"><strong>+1.000</strong></td>
      <td>HL = +2.00<br/>95% Walsh: [0.00, +3.00]</td>
      <td><span class="badge badge-pass">PASS: Complete-Case N=4</span></td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 4. HODGES-LEHMANN CI & EFFECT-SIZE AUDIT -->
<!-- ========================================================================= -->
<h2>4. HODGES–LEHMANN & EFFECT-SIZE METHODOLOGICAL VERIFICATION</h2>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
  <div style="border: 1px solid #cbd5e1; padding: 5px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #1e3a8a;">Hodges–Lehmann Walsh CI Specification</h3>
    <p>
      For $N$ paired observations, $M = \frac{N(N+1)}{2}$ pairwise Walsh averages $A_{(k)} = \frac{d_i + d_j}{2}$ ($1 \le i \le j \le N$) are calculated and sorted in ascending order.
    </p>
    <ul>
      <li><strong>Point Estimate:</strong> $\text{HL} = \text{Median}(\{A_{(k)}\})$.</li>
      <li><strong>Exact Inversion CI (Bauer 1972):</strong> The $100(1-\alpha)\%$ confidence bounds are defined by order statistics $A_{(k_{\text{crit}})}$ and $A_{(M - k_{\text{crit}} + 1)}$, where $k_{\text{crit}} = \left\lfloor \frac{N(N+1)}{4} - z_{1-\alpha/2}\sqrt{\frac{N(N+1)(2N+1)}{24}} \right\rfloor$.</li>
      <li><strong>Defensibility:</strong> For $N=25$, $M = 325$, $k_{\text{crit}} = 89$. Exact CI is $[A_{(89)}, A_{(237)}]$. Eliminates bootstrap instability on discrete integers.</li>
    </ul>
  </div>

  <div style="border: 1px solid #cbd5e1; padding: 5px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #1e3a8a;">Signed Rank-Biserial Effect Size ($r_{rb}$)</h3>
    <p>
      The Kerby (2014) rank-biserial correlation is computed directly from positive and negative rank sums under Pratt's ranking:
    </p>
    <ul>
      <li><strong>Formula:</strong> $r_{rb} = \frac{W^+ - W^-}{W^+ + W^-} \quad (\text{if } W^+ + W^- = 0, \ r_{rb} = 0.0)$.</li>
      <li><strong>Directional Integrity:</strong>
        <ul>
          <li>$r_{rb} > 0$: cohort improvement (post-test > pre-test).</li>
          <li>$r_{rb} < 0$: cohort deterioration (post-test < pre-test).</li>
          <li>$r_{rb} = 0$: no directional shift (balanced ranks).</li>
        </ul>
      </li>
      <li><strong>Manuscript Guidance:</strong> Prevents sign errors that arise when using $\min(W^+, W^-)$ in unadjusted formulas.</li>
    </ul>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 5. 73-COLUMN DATA-SCHEMA AUDIT -->
<!-- ========================================================================= -->
<h2>5. 73-COLUMN DATA-SCHEMA EXHAUSTIVE AUDIT</h2>
<p>
  Every column of the 73-variable schema (<code class="code-inline">participant_data_template.csv</code>) was audited against the SAP, instruments, and analysis scripts:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Column Variable(s)</th>
      <th style="width: 22%;">Measurement Purpose</th>
      <th style="width: 14%;">Instrument Source</th>
      <th style="width: 22%;">Analysis Pipeline Utilization</th>
      <th style="width: 10%;">Required?</th>
      <th style="width: 12%;">Audit Decision</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code class="code-inline">participant_id</code></td>
      <td>Unique anonymous tracking code</td>
      <td>Envelope Code</td>
      <td>Record integrity, deduplication</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">degree_program</code></td>
      <td>Student major (B.Pharm, Chem)</td>
      <td>Demographic Form</td>
      <td>Exploratory subgroup descriptive summary</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">prior_hplc_lab</code></td>
      <td>Prior wet-lab experience (0/1)</td>
      <td>Demographic Form</td>
      <td>Exploratory subgroup descriptive summary</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">pre_q1</code> to <code class="code-inline">pre_q10</code> (10 cols)</td>
      <td>Item-level pre-test accuracy (0/1)</td>
      <td>Pre-Test Form</td>
      <td>Exploratory item analysis ($P$, $D$), Cronbach's $\alpha$</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">pre_test_total</code></td>
      <td>Pre-test total score (0–10)</td>
      <td>Calculated</td>
      <td>Wilcoxon signed-rank, paired $t$-test, Hake gain</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">post_q1</code> to <code class="code-inline">post_q10</code> (10 cols)</td>
      <td>Item-level post-test accuracy (0/1)</td>
      <td>Post-Test Form</td>
      <td>Exploratory item analysis ($P$, $D$), Cronbach's $\alpha$</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">post_test_total</code></td>
      <td>Post-test total score (0–10)</td>
      <td>Calculated</td>
      <td>Wilcoxon signed-rank, paired $t$-test, Hake gain</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">score_gain</code></td>
      <td>Paired gain ($\text{Post} - \text{Pre}$)</td>
      <td>Derived</td>
      <td>Primary outcome distribution & Shapiro-Wilk</td>
      <td>Derived</td>
      <td><span class="badge badge-pass">RETAINED (CONV)</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">hake_gain</code></td>
      <td>Normalized gain $\langle g \rangle$</td>
      <td>Derived</td>
      <td>Descriptive gain categorization (low/med/high)</td>
      <td>Derived</td>
      <td><span class="badge badge-pass">RETAINED (CONV)</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">task_alpha_id_score</code>, <br/><code class="code-inline">task_alpha_reason_score</code>, <br/><code class="code-inline">task_alpha_action_score</code></td>
      <td>Scenario Alpha component rubric scores (0, 1, 2 each)</td>
      <td>Rubric Sheet</td>
      <td>Component-level descriptive reporting (Fitting Leak)</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">task_alpha_rubric_total</code></td>
      <td>Alpha scenario total (0–6)</td>
      <td>Derived</td>
      <td>Task difficulty comparison</td>
      <td>Derived</td>
      <td><span class="badge badge-pass">RETAINED (CONV)</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">task_alpha_time_s</code></td>
      <td>Alpha diagnostic latency (s)</td>
      <td>Worksheet Stamp</td>
      <td>Exploratory diagnostic efficiency (median/IQR)</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">task_alpha_conf</code></td>
      <td>Alpha subjective confidence (1–5)</td>
      <td>Worksheet Scale</td>
      <td>Exploratory confidence–accuracy correlation</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td>Tasks Beta, Gamma, Delta<br/>(18 columns total)</td>
      <td>Corresponding 6 metrics for Voids, Air Bubbles, and Contamination</td>
      <td>Rubric Sheet & Worksheet</td>
      <td>Multi-scenario rubric aggregation, latency distribution, confidence association</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">rater1_grand_total</code>, <br/><code class="code-inline">rater2_grand_total</code></td>
      <td>Independent grand totals (0–24)</td>
      <td>Faculty Raters</td>
      <td>Inter-rater reliability: Weighted Kappa ($\kappa_w$), $\text{ICC}(2,1)$</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">task_rubric_grand_total</code></td>
      <td>Adjudicated grand score (0–24)</td>
      <td>Rater Consensus</td>
      <td>Secondary inferential test against guessing (6.0)</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">sus_q1</code> to <code class="code-inline">sus_q10</code> (10 cols)</td>
      <td>Canonical Brooke SUS items (1–5)</td>
      <td>SUS Instrument</td>
      <td>Item profiling, Sauro missing imputation</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">sus_total_score</code></td>
      <td>Composite SUS score (0–100)</td>
      <td>Derived</td>
      <td>Secondary inferential test against 68.0 benchmark</td>
      <td>Derived</td>
      <td><span class="badge badge-pass">RETAINED (CONV)</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">ux_u1</code> to <code class="code-inline">ux_u8</code> (8 cols)</td>
      <td>Pedagogical UX items (1–5)</td>
      <td>UX Instrument</td>
      <td>Formative UI feature diagnostics (medians/IQRs)</td>
      <td>YES</td>
      <td><span class="badge badge-pass">RETAINED</span></td>
    </tr>
  </tbody>
</table>

<div class="callout">
  <strong>Schema Audit Summary:</strong> Exactly 73 columns. Zero unneeded or phantom variables. 64 primary collected metrics + 9 standard convenience/derived columns (<code class="code-inline">_total</code>, <code class="code-inline">_gain</code>). Template purity verified: exactly 1 header row, <strong>zero data rows</strong>.
</div>

<!-- ========================================================================= -->
<!-- 6. MULTIPLE-COMPARISON HIERARCHY -->
<!-- ========================================================================= -->
<h2>6. MULTIPLE-COMPARISON INFERENTIAL HIERARCHY</h2>
<p>
  To prevent post-hoc $p$-value fishing and preserve family-wise error rate ($\alpha = 0.05$), the study outcomes are partitioned into three immutable, pre-specified tiers:
</p>

<div style="border: 1px solid #cbd5e1; padding: 6px; border-radius: 4px; background-color: #f8fafc;">
  <div style="margin-bottom: 5px;">
    <strong style="color: #0f172a; font-size: 8.2pt;">TIER 1: PRIMARY PRESPECIFIED INFERENTIAL ANALYSIS (STANDALONE $\alpha = 0.05$)</strong><br/>
    <span style="font-size: 7.5pt;">
      &bull; <strong>Paired Troubleshooting Score Gain ($\Delta\text{Score} = \text{PostTest} - \text{PreTest}$):</strong> Two-tailed Wilcoxon Signed-Rank Test using Pratt's method (<code class="code-inline">zero_method='pratt'</code>). Reported with Hodges–Lehmann median difference (95% Walsh order-statistic CI) and signed rank-biserial correlation ($r_{rb}$). Paired Student's $t$-test reported as pre-specified sensitivity analysis.
    </span>
  </div>

  <div style="margin-bottom: 5px;">
    <strong style="color: #1e3a8a; font-size: 8.2pt;">TIER 2: SECONDARY INFERENTIAL HYPOTHESIS FAMILY (HOLM-BONFERRONI CONTROLLED, $k = 2$)</strong><br/>
    <span style="font-size: 7.5pt;">
      &bull; <strong>System Usability Acceptability ($H_{0,1}$):</strong> One-sample Wilcoxon signed-rank test comparing SUS composite scores against the industry average benchmark of 68.0 ($H_0: \text{Median SUS} \le 68.0$).<br/>
      &bull; <strong>Practical Diagnostic Competence ($H_{0,2}$):</strong> One-sample Wilcoxon signed-rank test comparing grand diagnostic rubric scores against the random-guessing threshold ($H_0: \text{Median Rubric} \le 6.0/24$).<br/>
      <em>Multiplicity Adjustment:</em> Holm-Bonferroni step-down correction: sort $p_{(1)} \le p_{(2)}$. Reject $H_{0,(1)}$ if $p_{(1)} \le 0.025$; reject $H_{0,(2)}$ if $p_{(2)} \le 0.050$.
    </span>
  </div>

  <div>
    <strong style="color: #475569; font-size: 8.2pt;">TIER 3: EXPLORATORY & DESCRIPTIVE OUTCOMES (NO MULTIPLICITY PENALTY, HYPOTHESIS-GENERATING)</strong><br/>
    <span style="font-size: 7.5pt;">
      &bull; <strong>Hake Normalized Gain ($\langle g \rangle$):</strong> Reported descriptively via Hake's brackets (low &lt; 0.3, med 0.3–0.7, high &gt; 0.7). Identical null to Tier 1.<br/>
      &bull; <strong>Exploratory Confidence–Performance Association:</strong> Spearman $\rho$ and Pearson $r$ between confidence and rubric performance (zero causal claims).<br/>
      &bull; <strong>Diagnostic Latency:</strong> Median completion time in seconds with IQR across practical scenarios.<br/>
      &bull; <strong>Exploratory Item Analysis:</strong> Item difficulty ($P$) and discrimination ($D$) with small-sample ($N \approx 25$) caveats.<br/>
      &bull; <strong>Subgroup Summaries:</strong> B.Pharm vs Chemistry; prior HPLC experience vs novices (medians/IQRs only; zero inferential claims).
    </span>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 7. 50-MINUTE FEASIBILITY & PROTOCOL TIMELINE -->
<!-- ========================================================================= -->
<h2>7. 50-MINUTE SESSION FEASIBILITY & COGNITIVE LOAD AUDIT</h2>
<p>
  Session timing was audited to ensure strict adherence to standard undergraduate laboratory periods:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 14%;">Block / Time</th>
      <th style="width: 22%;">Activity Description</th>
      <th style="width: 38%;">Participant Task & Cognitive Burden</th>
      <th style="width: 14%;">Duration Audit</th>
      <th style="width: 12%;">Feasibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Block 1<br/>$t = 00\text{--}05$ min</strong></td>
      <td>Briefing & Consent</td>
      <td>Institutional consent form review, voluntary signature, anonymous ID code assignment. Neutral script.</td>
      <td>5 minutes</td>
      <td><span class="badge badge-pass">VERIFIED</span></td>
    </tr>
    <tr>
      <td><strong>Block 2<br/>$t = 05\text{--}15$ min</strong></td>
      <td>Pre-Test Diagnostic Assessment</td>
      <td>10 multiple-choice / matching diagnostic items. Focus on baseline chromatographic problem-solving.</td>
      <td>10 minutes<br/>(60 s / item)</td>
      <td><span class="badge badge-pass">VERIFIED</span></td>
    </tr>
    <tr>
      <td><strong>Block 3<br/>$t = 15\text{--}27$ min</strong></td>
      <td>SimuPharm Active Exploration</td>
      <td>Unguided simulation familiarization: flow rate, mobile phase, temperature, and fault injection exploration.</td>
      <td>12 minutes</td>
      <td><span class="badge badge-pass">VERIFIED</span></td>
    </tr>
    <tr>
      <td><strong>Block 4<br/>$t = 27\text{--}39$ min</strong></td>
      <td>Practical Troubleshooting Tasks</td>
      <td>4 blinded simulated scenarios (Alpha: Leak, Beta: Void, Gamma: Bubble, Delta: Contamination). Worksheet recording.</td>
      <td>12 minutes<br/>(3 min / task)</td>
      <td><span class="badge badge-pass">VERIFIED</span></td>
    </tr>
    <tr>
      <td><strong>Block 5<br/>$t = 39\text{--}49$ min</strong></td>
      <td>Post-Test, SUS & Feedback</td>
      <td>10 isomorphic post-test items (~5 min), canonical Brooke SUS (~2 min), 8 UX items (~1.5 min), brief qualitative prompts (~1.5 min).</td>
      <td>10 minutes</td>
      <td><span class="badge badge-pass">VERIFIED</span></td>
    </tr>
    <tr>
      <td><strong>Block 6<br/>$t = 49\text{--}50$ min</strong></td>
      <td>Instrument Debrief & Collection</td>
      <td>Submission of envelope packets, verification of completion, participant dismissal.</td>
      <td>1 minute</td>
      <td><span class="badge badge-pass">VERIFIED</span></td>
    </tr>
  </tbody>
</table>

<div class="callout">
  <strong>Cognitive Load Mitigation in Block 5:</strong> To ensure students comfortably complete all instruments within 10 minutes, qualitative instructions are explicitly calibrated: short phrases or bullet points (1–2 sentences, $\le 30$ words per prompt) are requested. Zero lengthy essay prompts. Total elapsed session time is locked at exactly <strong>50 minutes</strong>.
</div>

<!-- ========================================================================= -->
<!-- 8. EXPERT CONTENT-VALIDITY METHODOLOGY VERIFICATION -->
<!-- ========================================================================= -->
<h2>8. EXPERT CONTENT-VALIDITY METHODOLOGY AUDIT</h2>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
  <div style="border: 1px solid #cbd5e1; padding: 5px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #1e3a8a;">Reviewer Panel & Formulas</h3>
    <ul>
      <li><strong>Panel Composition:</strong> 3 to 5 independent analytical chromatography faculty and pharmaceutical educators.</li>
      <li><strong>Item Content Validity Index:</strong> $\text{I-CVI} = \frac{N_{3,4}}{N_{\text{experts}}}$, where $N_{3,4}$ is the number of experts rating relevance/clarity as 3 (Quite relevant) or 4 (Highly relevant).</li>
      <li><strong>Scale Content Validity Index:</strong> $\text{S-CVI/Ave} = \frac{1}{K} \sum_{k=1}^K \text{I-CVI}_k$.</li>
      <li><strong>Status:</strong> Form remains strictly unpopulated. Zero fabricated ratings.</li>
    </ul>
  </div>

  <div style="border: 1px solid #cbd5e1; padding: 5px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #1e3a8a;">Descriptive Framework & Small-$N$ Caveat</h3>
    <ul>
      <li><strong>Descriptive Benchmarks:</strong> Lynn (1986) cutoffs ($\text{I-CVI} \ge 0.80$, $\text{S-CVI/Ave} \ge 0.90$) are descriptive guidelines, not universal mandatory hurdles.</li>
      <li><strong>Small-Panel Sensitivity:</strong> When $N_{\text{experts}} = 3$, $100\%$ agreement ($3/3 = 1.00$) is required; a single dissenter drops I-CVI to $0.67$. For $N_{\text{experts}} = 5$, $4/5 = 0.80$.</li>
      <li><strong>Scope Boundary:</strong> Evaluates curricular appropriateness and symptom plausibility; does <strong>NOT</strong> substitute for physical instrument validation.</li>
    </ul>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 9. CLAIM-LANGUAGE AUDIT REGISTER -->
<!-- ========================================================================= -->
<h2>9. CLAIM-LANGUAGE AUDIT REGISTER (12 PRESCRIBED PHRASES)</h2>
<p>
  All Phase 4.2.1 text files and codebases were scanned for 12 sensitive claim terms. Each occurrence was audited against empirical evidence:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Audited Term</th>
      <th style="width: 12%;">Occurrences</th>
      <th style="width: 14%;">Audit Classification</th>
      <th style="width: 38%;">Context in Phase 4 Artifacts</th>
      <th style="width: 18%;">Action Taken</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>"proves"</strong></td>
      <td>5 matches</td>
      <td><span class="badge badge-warn">NEEDS QUALIFICATION</span></td>
      <td>1 in Answer Key Q4 ("proves contamination"); others in Prohibited Claims ledger.</td>
      <td>Replaced with "indicates contamination" in answer key. Preserved in Prohibited register.</td>
    </tr>
    <tr>
      <td><strong>"validated"</strong></td>
      <td>3 matches</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Appears in Prohibited Claims register ("Validated across 300+ APIs") and as a limitation warning.</td>
      <td>Preserved inside Prohibited Claims register. No unsupported positive claims exist.</td>
    </tr>
    <tr>
      <td><strong>"confirmatory"</strong></td>
      <td>11 matches</td>
      <td><span class="badge badge-warn">NEEDS QUALIFICATION</span></td>
      <td>Used in RQ1, SAP, and outline ("Primary Confirmatory Analysis").</td>
      <td>Replaced with "Primary Prespecified Inferential Analysis" across all files.</td>
    </tr>
    <tr>
      <td><strong>"psychometrically sound"</strong></td>
      <td>1 match</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Recorded in Readiness Checklist as an overstatement that was excised.</td>
      <td>Preserved as audit record of removal.</td>
    </tr>
    <tr>
      <td><strong>"experimentally validated"</strong></td>
      <td>1 match</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Appears in Prohibited Claims ledger ("Experimentally Validated Physical Pressure Dynamics").</td>
      <td>Preserved as a prohibited claim.</td>
    </tr>
    <tr>
      <td><strong>"physical validation"</strong></td>
      <td>1 match</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Recorded in Checklist confirming that expert review is NOT claimed as physical validation.</td>
      <td>Preserved as governance qualification.</td>
    </tr>
    <tr>
      <td><strong>"causal"</strong></td>
      <td>8 matches</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Used exclusively to disclaim causality ("Zero causal claims are made") or in Prohibited Claims.</td>
      <td>Preserved as essential methodological disclaimers.</td>
    </tr>
    <tr>
      <td><strong>"effective"</strong></td>
      <td>0 matches</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Zero unverified claims of "effectiveness" found in active text.</td>
      <td>None required.</td>
    </tr>
    <tr>
      <td><strong>"superior"</strong></td>
      <td>0 matches</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Zero claims of superiority over traditional instruction.</td>
      <td>None required.</td>
    </tr>
    <tr>
      <td><strong>"TOP Level 2"</strong></td>
      <td>4 matches</td>
      <td><span class="badge badge-stop">REMOVE</span></td>
      <td>Asserted conformance to "JCE TOP Guidelines Level 2" without external journal verification.</td>
      <td>Replaced with generic responsible open-science and reproducibility language.</td>
    </tr>
    <tr>
      <td><strong>"generalizable"</strong></td>
      <td>0 matches</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Single-institution $N \approx 25$ pilot explicitly acknowledges non-generalizability.</td>
      <td>None required.</td>
    </tr>
    <tr>
      <td><strong>"metacognitive improvement"</strong></td>
      <td>0 matches</td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Causal metacognitive learning claims previously excised; only association indicator used.</td>
      <td>None required.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 10. FROZEN ENGINE INTEGRITY & RECRUITMENT GATE -->
<!-- ========================================================================= -->
<h2>10. FROZEN-ENGINE INTEGRITY CHECK & RECRUITMENT GATE</h2>
<p>
  Cryptographic verification confirms that the SimuPharm scientific simulation engine remains 100% frozen:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 25%;">Engine File</th>
      <th style="width: 45%;">Calculated SHA-256 Checksum</th>
      <th style="width: 15%;">Phase 4 Baseline</th>
      <th style="width: 15%;">Audit Verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code class="code-inline">hplc_simulator_script.js</code></td>
      <td><code class="code-inline">2fad9547f9fc7c671176346e78732be30246a515853631dede21ae8f7d3b7167</code></td>
      <td>Identical</td>
      <td><span class="badge badge-pass">MATCH (FROZEN)</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">script.js</code></td>
      <td><code class="code-inline">9812fea221fee06391a35d2680c28ce375ca62bc26bc265ed07f36d4d96f0600</code></td>
      <td>Identical</td>
      <td><span class="badge badge-pass">MATCH (FROZEN)</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">index.html</code></td>
      <td><code class="code-inline">dfb896b41790efcc365a3721b8ccc7aa8f49861485a74b02538eb38cadbdee36</code></td>
      <td>Identical</td>
      <td><span class="badge badge-pass">MATCH (FROZEN)</span></td>
    </tr>
    <tr>
      <td><code class="code-inline">hplc_simulator.html</code></td>
      <td><code class="code-inline">02b2b226bf291c2466c23832382e296523cecc68811afe26ba65822197afd6bb</code></td>
      <td>Identical</td>
      <td><span class="badge badge-pass">MATCH (FROZEN)</span></td>
    </tr>
  </tbody>
</table>

<div style="page-break-inside: avoid; break-inside: avoid; margin-top: 6px;">
  <div class="callout-alert" style="margin-top: 4px; margin-bottom: 6px;">
    <div style="font-weight: 800; font-size: 8.5pt; color: #991b1b; margin-bottom: 2px;">
      FINAL RECRUITMENT READINESS VERDICT: NO-GO — INSTITUTIONAL ETHICS AUTHORIZATION PENDING
    </div>
    <div>
      <strong>Gate 1 (Scientific & Statistical Readiness):</strong> <span class="badge badge-pass">CLEARED (100%)</span> — All code, assessments, rubrics, analysis pipelines, and templates are technically verified.<br/>
      <strong>Gate 2 (Institutional Ethics Authorization):</strong> <span class="badge badge-stop">PENDING</span> — Written determination from the host institution's Institutional Ethics Committee (IEC / IRB) has not yet been issued.<br/>
      <strong>Rule of Law:</strong> In accordance with international research ethics standards (Declaration of Helsinki) and institutional governance, no student participant may be recruited, consented, or assessed until formal written authorization is secured. Zero self-exemption is permitted.
    </div>
  </div>

  <div style="margin-top: 8px; border-top: 2px solid #0f172a; padding-top: 6px; text-align: center;">
    <div style="font-size: 8.5pt; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">
      PROTOCOL STATUS:
    </div>
    <div style="font-size: 10.5pt; font-weight: 800; color: #b91c1c; margin: 2px 0 4px 0;">
      FROZEN PENDING INSTITUTIONAL ETHICS AUTHORIZATION
    </div>
    <div style="font-size: 8.0pt; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">
      NEXT SCIENTIFIC ACTION:
    </div>
    <div style="font-size: 10.0pt; font-weight: 800; color: #15803d; margin-top: 2px;">
      REAL PARTICIPANT DATA COLLECTION AFTER AUTHORIZATION
    </div>
  </div>
</div>

</body>
</html>
"""

def generate_pdf():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        
        # Render PDF
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "9mm", "right": "9mm"}
        )
        browser.close()
        
        with open(out_primary, "wb") as f:
            f.write(pdf_bytes)
        print(f"Successfully generated Phase 4.2.2 PDF: {out_primary} ({len(pdf_bytes)} bytes)")
        
        with open(out_artifact, "wb") as f:
            f.write(pdf_bytes)
        print(f"Successfully mirrored PDF: {out_artifact} ({len(pdf_bytes)} bytes)")

if __name__ == '__main__':
    generate_pdf()
