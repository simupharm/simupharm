import os
import sys
from playwright.sync_api import sync_playwright

dir_primary = r"c:\Users\dsant\OneDrive\simupro - Copy\SIMUPHARM_PHASE4_2_CORRECTED_EDUCATIONAL_STUDY"
dir_artifact = r"C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\SIMUPHARM_PHASE4_2_CORRECTED_EDUCATIONAL_STUDY"
os.makedirs(dir_primary, exist_ok=True)
os.makedirs(dir_artifact, exist_ok=True)

pdf_filename = "SIMUPHARM_PHASE4_2_3_ABSOLUTE_PROTOCOL_FREEZE.pdf"
out_primary = os.path.join(dir_primary, pdf_filename)
out_artifact = os.path.join(dir_artifact, pdf_filename)

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SimuPharm Phase 4.2.3 — Final Statistical Methodology Correction & Absolute Freeze</title>
<style>
  @page {
    size: A4;
    margin: 10mm 9mm 10mm 9mm;
    @top-left {
      content: "SimuPharm Phase 4.2.3 | Final Statistical Methodology Correction & Absolute Freeze";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.8pt;
      color: #0f172a;
      font-weight: 700;
    }
    @top-right {
      content: "FINAL STATISTICAL METHODOLOGY CERTIFICATION";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.8pt;
      color: #64748b;
      font-weight: 600;
    }
    @bottom-left {
      content: "CONFIDENTIAL & PRIVILEGED | RECRUITMENT-READY PROTOCOL FREEZE";
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.5pt;
      color: #94a3b8;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 6.8pt;
      color: #334155;
      font-weight: 600;
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    line-height: 1.28;
    font-size: 7.7pt;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  h1 {
    font-size: 16pt;
    font-weight: 800;
    color: #020617;
    margin: 0 0 2px 0;
    letter-spacing: -0.4px;
  }

  h2 {
    font-size: 9.2pt;
    font-weight: 700;
    color: #0f172a;
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
    color: #1e293b;
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
    margin-bottom: 4px;
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
    background-color: #f8fafc;
    font-weight: 700;
    color: #0f172a;
  }

  .badge {
    display: inline-block;
    padding: 1px 4px;
    border-radius: 3px;
    font-weight: 700;
    font-size: 6.4pt;
    text-transform: uppercase;
  }
  .badge-pass { background-color: #dcfce7; color: #166534; border: 1px solid #86efac; }
  .badge-warn { background-color: #fef9c3; color: #854d0e; border: 1px solid #fde047; }
  .badge-stop { background-color: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
  .badge-info { background-color: #e0f2fe; color: #075985; border: 1px solid #7dd3fc; }

  .callout {
    border-left: 3px solid #0284c7;
    background-color: #f0f9ff;
    padding: 4px 7px;
    margin-top: 3px;
    margin-bottom: 5px;
    border-radius: 0 3px 3px 0;
    font-size: 7.4pt;
  }

  .callout-alert {
    border-left: 3px solid #dc2626;
    background-color: #fef2f2;
    padding: 4px 7px;
    margin-top: 3px;
    margin-bottom: 5px;
    border-radius: 0 3px 3px 0;
    font-size: 7.4pt;
  }

  .callout-success {
    border-left: 3px solid #16a34a;
    background-color: #f0fdf4;
    padding: 4px 7px;
    margin-top: 3px;
    margin-bottom: 5px;
    border-radius: 0 3px 3px 0;
    font-size: 7.4pt;
  }

  .code-inline {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 6.7pt;
    background-color: #f1f5f9;
    padding: 1px 3px;
    border-radius: 2px;
    border: 1px solid #e2e8f0;
  }
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- TITLE & HEADER -->
<!-- ========================================================================= -->
<div style="border-bottom: 2px solid #0f172a; padding-bottom: 4px; margin-bottom: 6px;">
  <div style="display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
      <span class="badge badge-info" style="margin-bottom: 2px;">PHASE 4.2.3 ABSOLUTE PROTOCOL FREEZE</span>
      <h1 style="margin: 1px 0 1px 0;">SimuPharm Educational Pilot Evaluation</h1>
      <div style="font-size: 8.3pt; font-weight: 600; color: #475569;">
        Final Technical Sanity Audit, Statistical Methodology Correction & Governance Certification
      </div>
    </div>
    <div style="text-align: right; font-size: 7.0pt; color: #64748b;">
      <div><strong>Date:</strong> October 4, 2026</div>
      <div><strong>Governance Status:</strong> <span class="badge badge-stop">NO-GO — ETHICS PENDING</span></div>
      <div><strong>Engine Status:</strong> <span class="badge badge-pass">MATCH — FROZEN</span></div>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 1. EXECUTIVE SUMMARY -->
<!-- ========================================================================= -->
<h2>1. EXECUTIVE SUMMARY & STUDY ARCHITECTURE LOCK</h2>
<p>
  This audit constitutes the definitive, immutable pre-recruitment certification for the <strong>SimuPharm Educational Evaluation Study</strong>. The study architecture is completely <strong>LOCKED</strong>: single-group within-subjects pre/post exploratory pilot ($N \approx 25$ undergraduate pharmacy and chemistry students), standardized 50-minute scheduled laboratory session, 10-item isomorphic diagnostic knowledge tests, 4-scenario troubleshooting task evaluated via a 24-point analytical rubric, and the canonical Brooke (1996) System Usability Scale (SUS). <strong>Zero software modifications have been made to the simulation engine, no study arms or participant-facing features have been added, no participant data has been collected or fabricated, and all analysis templates remain 100% blank.</strong>
</p>

<!-- ========================================================================= -->
<!-- 2. CORRECTIONS FROM PHASE 4.2.2 -->
<!-- ========================================================================= -->
<h2>2. CORRECTIONS IMPLEMENTED FROM PHASE 4.2.2 AUDIT</h2>
<table>
  <thead>
    <tr>
      <th style="width: 4%;">#</th>
      <th style="width: 22%;">Methodological Domain</th>
      <th style="width: 32%;">Phase 4.2.2 Baseline Finding</th>
      <th style="width: 32%;">Phase 4.2.3 Precise Calibration</th>
      <th style="width: 10%;">Audit Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1</strong></td>
      <td><strong>Readiness Language</strong></td>
      <td>Stated: "Gate 1 (Scientific & Statistical Readiness): CLEARED (100%)", inadvertently implying absolute pre-empirical readiness.</td>
      <td>Replaced with: <strong>"Technical and statistical protocol verification: COMPLETED"</strong>. All pre-data "100% readiness" claims removed.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>2</strong></td>
      <td><strong>Hodges–Lehmann CI Terminology</strong></td>
      <td>Previously characterized as an "Exact Inversion CI", while the critical index $k_{\text{crit}}$ was calculated using a normal $z$ approximation.</td>
      <td>Designated precisely as: <strong>"Wilcoxon/Walsh order-statistic confidence interval using the prespecified critical-index approximation"</strong>. Word "exact" removed.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>3</strong></td>
      <td><strong>Rubric Guessing Hypothesis</strong></td>
      <td>Included a one-sample inferential hypothesis test: $H_0: \text{Median Rubric} \le 6.0/24$, arbitrarily assuming 6 points as "random guessing".</td>
      <td><strong>Excised inferential test.</strong> The multi-component rubric (ID, reasoning, action) lacks a mathematical guessing model; retained purely as a descriptive outcome.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>4</strong></td>
      <td><strong>SUS Usability Framework</strong></td>
      <td>Posed a one-sample Wilcoxon test against the 68.0 benchmark ($H_0: \text{Median SUS} \le 68.0$), blurring benchmarking with inferential claims.</td>
      <td><strong>Excised inferential test.</strong> Reclassified as <strong>contextual descriptive benchmarking</strong> (mean, median, SD, IQR); benchmark is not a control group or proof of efficacy.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>5</strong></td>
      <td><strong>Qualitative Paradigm Consistency</strong></td>
      <td>Incompatibly combined reflexive thematic analysis (Braun & Clarke 2006) with dual coding and a mandatory inter-coder threshold ($\kappa \ge 0.80$).</td>
      <td>Adopted a unified framework: <strong>Structured thematic analysis with an inductively developed codebook, 25% dual coding, descriptive agreement $\kappa$, and consensus resolution</strong>.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>6</strong></td>
      <td><strong>Internal-Consistency Reliability</strong></td>
      <td>Mentioned Cronbach's $\alpha$ for the 10-item pre/post test without qualification, risking over-interpretation at pilot sample size ($N \approx 25$).</td>
      <td>Explicitly designated as <strong>exploratory and unstable at $N \approx 25$</strong>; not used to establish psychometric validity; tests not claimed as "validated" based on $\alpha$.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>7</strong></td>
      <td><strong>Hake Normalized Gain Framing</strong></td>
      <td>Risked being perceived as an inferential hypothesis test or basis for categorizing individual students into learning brackets.</td>
      <td>Explicitly stated: <strong>"The normalized gain is reported descriptively and is not used as evidence of causal educational effectiveness."</strong> Individual tagging removed.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>8</strong></td>
      <td><strong>Multiplicity & Family Definition</strong></td>
      <td>Holm-Bonferroni correction was previously applied across a mixed bag of hypothesis tests and descriptive metrics ($k=2$ to $k=5$).</td>
      <td>With secondary tests reclassified as descriptive benchmarking, <strong>Tier 1 is a standalone primary inferential test ($\alpha = 0.05$)</strong>, eliminating artificial multiplicity penalties.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>9</strong></td>
      <td><strong>Inter-Rater Reliability Metrics</strong></td>
      <td>Grouped Weighted Kappa ($\kappa_w$) and $\text{ICC}(2,1)$ without clearly distinguishing their application to rubric measurement levels.</td>
      <td>Explicitly distinguished: <strong>$\kappa_w$ for component-level ordinal agreement (0–2)</strong> vs <strong>$\text{ICC}(2,1)$ for grand-total score reliability (0–24)</strong>.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
    <tr>
      <td><strong>10</strong></td>
      <td><strong>Study Allocation Terminology</strong></td>
      <td>Referred to "randomized Participant IDs", risking confusion with a randomized controlled trial design.</td>
      <td>Replaced with: <strong>"assigned anonymous Participant IDs (`P01` to `P25`)"</strong> across all intervention and ethics documents.</td>
      <td><span class="badge badge-pass">CORRECTED</span></td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 3. HODGES-LEHMANN CI & EFFECT-SIZE VERIFICATION -->
<!-- ========================================================================= -->
<h2>3. HODGES–LEHMANN CONFIDENCE INTERVAL & EFFECT-SIZE VERIFICATION</h2>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px; background-color: #f8fafc;">
    <h3 style="margin-top: 0; color: #0f172a;">Walsh Order-Statistic CI (Normal-Approximation)</h3>
    <p>
      For $N$ complete-case pairs, $M = \frac{N(N+1)}{2}$ pairwise Walsh averages $A_{(k)} = \frac{d_i + d_j}{2}$ ($1 \le i \le j \le N$) are calculated and sorted in ascending order.
    </p>
    <ul>
      <li><strong>Point Estimator:</strong> $\text{HL} = \text{Median}(\{A_{(k)}\})$.</li>
      <li><strong>Critical Index Approximation (Bauer 1972):</strong> The bounds are order statistics $A_{(k_{\text{crit}})}$ and $A_{(M - k_{\text{crit}} + 1)}$, where:
        $$k_{\text{crit}} = \left\lfloor \frac{N(N+1)}{4} - z_{1-\alpha/2}\sqrt{\frac{N(N+1)(2N+1)}{24}} \right\rfloor$$
      </li>
      <li><strong>Epistemological Clarification:</strong> Because $k_{\text{crit}}$ relies on the continuous normal approximation of the discrete Wilcoxon distribution, this interval is <strong>NOT called an "exact" interval</strong>; it is a <em>Walsh order-statistic confidence interval using the prespecified critical-index approximation</em>. For $N=25$, $M=325$, $k_{\text{crit}}=89$, yielding $[A_{(89)}, A_{(237)}]$.</li>
    </ul>
  </div>

  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px; background-color: #f8fafc;">
    <h3 style="margin-top: 0; color: #0f172a;">Signed Rank-Biserial Correlation ($r_{rb}$)</h3>
    <p>
      Non-parametric effect size is computed directly from Pratt rank sums of positive ($W^+$) and negative ($W^-$) differences:
    </p>
    <ul>
      <li><strong>Formula:</strong> $r_{rb} = \frac{W^+ - W^-}{W^+ + W^-} \quad (\text{if } W^+ + W^- = 0, \ r_{rb} = 0.0)$.</li>
      <li><strong>Directional Verification across 7 Stress Cases:</strong>
        <ul>
          <li>Case A (All Positive): $r_{rb} = +1.000, \ p = 0.0078$ <span class="badge badge-pass">PASS</span></li>
          <li>Case B (All Negative): $r_{rb} = -1.000, \ p = 0.0078$ <span class="badge badge-pass">PASS</span></li>
          <li>Case C (Mixed Ranks): $r_{rb} = +0.722, \ p = 0.0781$ <span class="badge badge-pass">PASS</span></li>
          <li>Case D (Pratt Zeros): $r_{rb} = +1.000, \ p = 0.0474$ <span class="badge badge-pass">PASS</span></li>
          <li>Case E (All Zeros): $r_{rb} = 0.000, \ p = 1.0000$ <span class="badge badge-pass">PASS</span></li>
          <li>Case F (Balanced Ties): $r_{rb} = 0.000, \ p = 1.0000$ <span class="badge badge-pass">PASS</span></li>
          <li>Case G (Missing Pairs): Complete-case filtering ($N_{\text{valid}}=4$) <span class="badge badge-pass">PASS</span></li>
        </ul>
      </li>
    </ul>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 4. FINAL INFERENTIAL HIERARCHY -->
<!-- ========================================================================= -->
<h2>4. FINAL INFERENTIAL HIERARCHY & PRE-REGISTRATION ARCHITECTURE</h2>
<p>
  Following the removal of ungrounded secondary one-sample tests, the outcome structure is finalized into an uncompromised, pre-registered three-tier hierarchy:
</p>

<div style="border: 1px solid #cbd5e1; padding: 5px 8px; border-radius: 4px; background-color: #f8fafc; font-size: 7.3pt;">
  <div style="margin-bottom: 4px;">
    <strong style="color: #020617; font-size: 8.0pt;">TIER 1: PRIMARY PRESPECIFIED INFERENTIAL ANALYSIS (STANDALONE $\alpha = 0.05$, TWO-TAILED)</strong><br/>
    &bull; <strong>Paired Troubleshooting Score Gain ($\Delta\text{Score} = \text{PostTest} - \text{PreTest}$):</strong> Two-tailed Wilcoxon Signed-Rank Test using Pratt's method (<code class="code-inline">zero_method='pratt'</code>). Reported with Hodges–Lehmann median difference with 95% Walsh order-statistic CI (critical-index approximation) and signed rank-biserial correlation ($r_{rb}$). Paired Student's $t$-test pre-specified as sensitivity analysis.
  </div>

  <div style="margin-bottom: 4px;">
    <strong style="color: #1e293b; font-size: 8.0pt;">TIER 2: SECONDARY INFERENTIAL HYPOTHESIS TESTS</strong><br/>
    &bull; <strong>Status: NONE PRE-SPECIFIED.</strong> Because the 24-point practical rubric lacks a mathematical guessing model and SUS is a subjective usability questionnaire, these metrics are properly evaluated via descriptive benchmarking rather than artificial one-sample null hypotheses. <em>No family-wise error adjustments or multiplicity penalties are required.</em>
  </div>

  <div>
    <strong style="color: #475569; font-size: 8.0pt;">TIER 3: EXPLORATORY & DESCRIPTIVE OUTCOMES (NO MULTIPLICITY PENALTY, HYPOTHESIS-GENERATING)</strong><br/>
    &bull; <strong>Practical Rubric Mastery:</strong> Grand score (0–24) and components (ID, Reasoning, Action: 0–2 each); medians, IQRs, percentage of maximum.<br/>
    &bull; <strong>System Usability Scale (SUS):</strong> Mean, SD, median, and IQR compared contextually against the widely cited 68.0 benchmark.<br/>
    &bull; <strong>Diagnostic Latency:</strong> Median Time-to-Diagnosis in seconds with IQR across practical scenarios.<br/>
    &bull; <strong>Exploratory Confidence–Performance Association:</strong> Spearman $\rho$ and Pearson $r$ between confidence ratings (1–5) and rubric performance (zero causal claims).<br/>
    &bull; <strong>Hake Normalized Gain ($\langle g \rangle$):</strong> Cohort average normalized gain reported descriptively without individual student categorization.<br/>
    &bull; <strong>Exploratory Item Analysis:</strong> Item difficulty ($P$) and discrimination ($D$) with explicit small-sample ($N \approx 25$) stability caveats.<br/>
    &bull; <strong>Subgroup Summaries:</strong> B.Pharm vs Chemistry; prior HPLC experience vs novices (descriptive medians/IQRs only; zero inferential claims).
  </div>
</div>

<!-- ========================================================================= -->
<!-- 5. PRACTICAL RUBRIC & SUS METHODOLOGY -->
<!-- ========================================================================= -->
<div style="page-break-before: always;"></div>
<h2>5. PRACTICAL RUBRIC & SUS METHODOLOGICAL JUSTIFICATIONS</h2>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #0f172a;">24-Point Analytical Rubric Justification</h3>
    <p>
      The 4-scenario practical troubleshooting task evaluates three distinct cognitive/procedural dimensions: Symptom ID (0–2), Physical Reasoning (0–2), and Corrective Action Plan (0–2), yielding 0–6 per scenario and 0–24 grand total.
    </p>
    <ul>
      <li><strong>Rejection of Arbitrary Guessing Null:</strong> Multiple-choice guessing ($p=0.25$) does not apply to open-response rubric scoring. Setting $H_0 \le 6.0/24$ arbitrarily assumes that a student guessing randomly scores exactly 1.5 points per task, which is unsupported by psychometric theory.</li>
      <li><strong>Reporting Standard:</strong> Evaluated descriptively via median, IQR, component distributions, and scenario-level difficulty rankings.</li>
    </ul>
  </div>

  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #0f172a;">SUS Contextual Benchmarking Framework</h3>
    <p>
      The 10-item System Usability Scale (Brooke 1996) is scored continuously (0–100) using Sauro & Lewis (2016) item imputation for records with $\le 2$ missing items.
    </p>
    <ul>
      <li><strong>Benchmarking vs Hypothesis Testing:</strong> The 68.0 benchmark (Bangor et al., 2008) is an empirical industry average derived across hundreds of diverse software systems. It is NOT an experimental control group.</li>
      <li><strong>Boundary of Interpretation:</strong> A cohort mean or median $\ge 68.0$ indicates acceptable usability contextually; it does <strong>NOT prove educational effectiveness or simulator superiority</strong>.</li>
    </ul>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 6. QUALITATIVE & RELIABILITY METHODOLOGY -->
<!-- ========================================================================= -->
<h2>6. QUALITATIVE & RELIABILITY METHODOLOGICAL CONSISTENCY</h2>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #0f172a;">Structured Qualitative Framework</h3>
    <p>
      To resolve paradigm conflicts, the qualitative methodology is formalized as <em>structured thematic analysis with an inductively developed codebook</em>:
    </p>
    <ul>
      <li><strong>Dual-Coding Protocol:</strong> Two independent researchers code a random 25% sample ($n \approx 6\text{--}7$ transcripts) across three themes (Visual Cues, Misconceptions, Usability).</li>
      <li><strong>Inter-Coder Agreement ($\kappa$):</strong> Cohen's Kappa is reported descriptively as an agreement statistic on coded segments. It is <strong>NOT claimed to mathematically validate the qualitative findings</strong>.</li>
      <li><strong>Consensus Adjudication:</strong> Discordant codes are reconciled by discussion before coding the remaining 75% of transcripts.</li>
    </ul>
  </div>

  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #0f172a;">Inter-Rater Rubric Reliability Metrics</h3>
    <p>
      Two faculty raters independently score all participant response sheets blind to participant identity. Inter-rater reliability is partitioned by measurement level:
    </p>
    <ul>
      <li><strong>Component-Level Ordinal Agreement:</strong> Weighted Cohen's Kappa ($\kappa_w$, linear weighting) evaluated on individual 0–2 item ratings (Fault ID, Reasoning, Action Plan).</li>
      <li><strong>Grand-Total Reliability:</strong> Intraclass Correlation Coefficient $\text{ICC}(2,1)$ (two-way random effects, single rater, absolute agreement) evaluated on the 0–24 aggregate score.</li>
      <li><strong>Adjudication:</strong> Discrepancies $>1$ point are resolved via consensus to yield <code class="code-inline">task_rubric_grand_total</code>.</li>
    </ul>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 7. PSYCHOMETRIC & HAKE GAIN METHODOLOGICAL LIMITATIONS -->
<!-- ========================================================================= -->
<h2>7. PSYCHOMETRIC & HAKE-GAIN METHODOLOGICAL LIMITATIONS</h2>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #0f172a;">Item-Level Psychometric Caveats</h3>
    <ul>
      <li><strong>Sample Size Instability:</strong> For $N \approx 25$, Item Difficulty ($P$) and Item Discrimination ($D$) indices describe relative item behavior in this pilot cohort only; they do not represent population parameters.</li>
      <li><strong>Internal Consistency (Cronbach's $\alpha$):</strong> Classical test reliability estimates with 10 items and $N \approx 25$ have wide confidence intervals and are unstable. Internal consistency is reported as exploratory; <strong>the pre/post tests are NOT claimed as "psychometrically validated" based on $\alpha$</strong>.</li>
    </ul>
  </div>

  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #0f172a;">Hake Normalized Gain Boundaries</h3>
    <ul>
      <li><strong>Descriptive Function:</strong> Normalized gain $\langle g \rangle = \frac{\bar{x}_{\text{post}} - \bar{x}_{\text{pre}}}{10 - \bar{x}_{\text{pre}}}$ describes the proportion of possible gain achieved relative to cohort baseline.</li>
      <li><strong>Non-Causal Restriction:</strong> Explicitly reported descriptively and <strong>NOT used as evidence of causal educational effectiveness</strong>.</li>
      <li><strong>No Individual Categorization:</strong> Students are not classified into arbitrary "low/medium/high learning" bins; only cohort distribution and aggregate values are reported.</li>
    </ul>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 8. FINAL CLAIM-LANGUAGE AUDIT REGISTER -->
<!-- ========================================================================= -->
<h2>8. FINAL CLAIM-LANGUAGE AUDIT REGISTER (12 PRESCRIBED PHRASES)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 20%;">Prescribed Term</th>
      <th style="width: 14%;">Audit Status</th>
      <th style="width: 44%;">Context in Study Documents & Codebases</th>
      <th style="width: 22%;">Governance Action Taken</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>"100%"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Used only for technical facts: simulator runs "100% offline", engine is "100% frozen", template has "0 data rows".</td>
      <td>Excised from Gate 1 readiness language ("CLEARED [100%]" removed).</td>
    </tr>
    <tr>
      <td><strong>"confirmatory"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Appears only in historic audit changelogs as a past finding that was resolved.</td>
      <td>Replaced with "Primary Prespecified Inferential Analysis" across all active SAP and RQ files.</td>
    </tr>
    <tr>
      <td><strong>"validated"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Appears in Prohibited Claims ledger ("Validated across 300+ APIs") and as a limitation warning.</td>
      <td>Preserved in Prohibited Claims ledger. Pre/post tests explicitly not claimed as validated based on $\alpha$.</td>
    </tr>
    <tr>
      <td><strong>"psychometrically validated"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Zero positive occurrences in active methodology or claims documents.</td>
      <td>Confirmed absent.</td>
    </tr>
    <tr>
      <td><strong>"random guessing threshold"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Mentioned only to disclaim it ("No arbitrary 6/24 random guessing threshold is assumed").</td>
      <td>Preserved as an explicit methodological disclaimer.</td>
    </tr>
    <tr>
      <td><strong>"proves"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Appears only in Prohibited Claims register ("Proves SimuPharm replaces physical wet laboratory").</td>
      <td>Calibrated to "indicates" in answer key. Preserved in Prohibited Claims.</td>
    </tr>
    <tr>
      <td><strong>"effective"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Zero claims asserting proven instructional effectiveness.</td>
      <td>Confirmed absent.</td>
    </tr>
    <tr>
      <td><strong>"superior"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Zero claims asserting superiority over traditional wet laboratory training.</td>
      <td>Confirmed absent.</td>
    </tr>
    <tr>
      <td><strong>"causes"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Used exclusively in multiple-choice distractor options explaining physical HPLC mechanisms.</td>
      <td>Preserved in assessment instruments. No causal study design claims made.</td>
    </tr>
    <tr>
      <td><strong>"exact CI"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Zero occurrences in active methodology files.</td>
      <td>Replaced with "Walsh order-statistic CI using prespecified critical-index approximation".</td>
    </tr>
    <tr>
      <td><strong>"randomized"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Removed from participant tracking descriptions.</td>
      <td>Replaced with "assigned anonymous Participant IDs" (`P01` to `P25`).</td>
    </tr>
    <tr>
      <td><strong>"generalizable"</strong></td>
      <td><span class="badge badge-pass">SAFE</span></td>
      <td>Zero claims of generalizability exist; single-institution pilot boundaries declared.</td>
      <td>Confirmed absent.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 9. DATA-INTEGRITY & FROZEN-ENGINE VERIFICATION -->
<!-- ========================================================================= -->
<div style="page-break-before: always;"></div>
<h2>9. DATA INTEGRITY & CRYPTOGRAPHIC ENGINE VERIFICATION</h2>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #0f172a;">Data Schema Purity Verification</h3>
    <ul>
      <li><strong>Schema Location:</strong> <code class="code-inline">05_CORRECTED_DATA_SCHEMA/participant_data_template.csv</code></li>
      <li><strong>Audited Row Count:</strong> Exactly <strong>1 header row</strong> (73 variables), <strong>0 participant data rows</strong>.</li>
      <li><strong>Fabrication Audit:</strong> Zero participant records, zero fabricated scores, zero synthetic participant IDs presented as empirical data.</li>
      <li><strong>Isolation:</strong> Stress-test datasets are strictly segregated in <code class="code-inline">06_CORRECTED_ANALYSIS/test_data/DEMO_TEST_ONLY.csv</code>.</li>
    </ul>
  </div>

  <div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #0f172a;">Simulation Engine Hash Verification</h3>
    <table style="margin-top: 2px; margin-bottom: 2px;">
      <thead>
        <tr>
          <th>Source File</th>
          <th>Calculated SHA-256 Checksum</th>
          <th>Verdict</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code class="code-inline">hplc_simulator_script.js</code></td>
          <td><code class="code-inline">2fad9547f9fc7c671176346e78732be30246a515853631dede21ae8f7d3b7167</code></td>
          <td><span class="badge badge-pass">MATCH — FROZEN</span></td>
        </tr>
        <tr>
          <td><code class="code-inline">script.js</code></td>
          <td><code class="code-inline">9812fea221fee06391a35d2680c28ce375ca62bc26bc265ed07f36d4d96f0600</code></td>
          <td><span class="badge badge-pass">MATCH — FROZEN</span></td>
        </tr>
        <tr>
          <td><code class="code-inline">index.html</code></td>
          <td><code class="code-inline">dfb896b41790efcc365a3721b8ccc7aa8f49861485a74b02538eb38cadbdee36</code></td>
          <td><span class="badge badge-pass">MATCH — FROZEN</span></td>
        </tr>
        <tr>
          <td><code class="code-inline">hplc_simulator.html</code></td>
          <td><code class="code-inline">02b2b226bf291c2466c23832382e296523cecc68811afe26ba65822197afd6bb</code></td>
          <td><span class="badge badge-pass">MATCH — FROZEN</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 10. METHODOLOGICAL LIMITATIONS & RECRUITMENT GATE -->
<!-- ========================================================================= -->
<h2>10. STUDY LIMITATIONS & RECRUITMENT GATE DETERMINATION</h2>
<div style="border: 1px solid #cbd5e1; padding: 4px 6px; border-radius: 4px; background-color: #f8fafc; font-size: 7.2pt; margin-bottom: 5px;">
  <strong>Mandatory Manuscript Disclaimers:</strong> (1) <em>Single-Group Design:</em> The within-subjects pre/post design cannot establish causal superiority over traditional laboratory instruction. (2) <em>Short-Term Evaluation:</em> Evaluates diagnostic gains immediately following a single 50-minute laboratory session; delayed retention is unmeasured. (3) <em>Transfer to Physical Hardware:</em> Transfer of diagnostic skills to real physical HPLC instruments remains unmeasured. (4) <em>Small Sample Size ($N \approx 25$):</em> Subgroup comparisons (B.Pharm vs Chemistry) are exploratory and underpowered.
</div>

<div style="page-break-inside: avoid; break-inside: avoid;">
  <div class="callout-alert" style="margin-top: 3px; margin-bottom: 5px;">
    <div style="font-weight: 800; font-size: 8.3pt; color: #991b1b; margin-bottom: 2px;">
      FINAL RECRUITMENT READINESS VERDICT: NO-GO — INSTITUTIONAL ETHICS AUTHORIZATION PENDING
    </div>
    <div>
      <strong>Technical & Statistical Protocol Verification:</strong> <span class="badge badge-pass">COMPLETED</span> — Code, assessments, rubrics, analysis pipelines, and templates are technically verified.<br/>
      <strong>Institutional Ethics Authorization:</strong> <span class="badge badge-stop">PENDING</span> — Written determination from the host institution's Institutional Ethics Committee (IEC / IRB) has not yet been issued.<br/>
      <strong>Governance Mandate:</strong> In accordance with international research ethics standards (Declaration of Helsinki) and host-institution regulations, no student participant may be recruited, consented, or assessed until formal written institutional authorization is secured. Zero self-exemption is permitted.
    </div>
  </div>

  <div style="margin-top: 6px; border-top: 2px solid #0f172a; padding-top: 5px; text-align: center;">
    <div style="font-size: 8.5pt; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">
      PROTOCOL STATUS:
    </div>
    <div style="font-size: 10.5pt; font-weight: 800; color: #b91c1c; margin: 1px 0 3px 0;">
      FROZEN PENDING INSTITUTIONAL ETHICS AUTHORIZATION
    </div>
    <div style="font-size: 8.0pt; font-weight: 800; color: #0f172a; letter-spacing: 0.5px;">
      NEXT SCIENTIFIC ACTION:
    </div>
    <div style="font-size: 9.8pt; font-weight: 800; color: #166534; margin-top: 1px;">
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
        
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "9mm", "right": "9mm"}
        )
        browser.close()
        
        with open(out_primary, "wb") as f:
            f.write(pdf_bytes)
        print(f"Successfully generated Phase 4.2.3 PDF: {out_primary} ({len(pdf_bytes)} bytes)")
        
        with open(out_artifact, "wb") as f:
            f.write(pdf_bytes)
        print(f"Successfully mirrored PDF: {out_artifact} ({len(pdf_bytes)} bytes)")

if __name__ == '__main__':
    generate_pdf()
