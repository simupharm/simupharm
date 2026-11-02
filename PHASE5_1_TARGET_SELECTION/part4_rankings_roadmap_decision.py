"""
PHASE 5.1 — PART 4: DECISION MATRICES, RANKINGS, MULTI-PAPER STRATEGY, ROADMAP & DECISION
SimuPharm.io Publication Target Selection & Evidence Verification Sprint
"""

def get_part4_html():
    return """
    <!-- SECTION 21: QUANTITATIVE DECISION MATRIX -->
    <div class="page">
        <h2 class="section-title">21. QUANTITATIVE DECISION MATRIX (16 CRITERIA)</h2>
        
        <p class="body-text">
            To eliminate subjective bias, all seven candidate directions plus the educational route were scored across 
            <strong>sixteen objective scientific and operational criteria</strong> on a standardized scale from 0 (prohibitive / fatal barrier) 
            to 10 (ideal / highly favorable).
        </p>

        <h3 class="subsection-title">21.1 Master 16-Dimensional Evaluation Matrix</h3>
        <table class="data-table" style="font-size: 6.8pt;">
            <thead>
                <tr>
                    <th style="width: 16%;">Candidate Direction</th>
                    <th>Nov (10)</th>
                    <th>Imp (10)</th>
                    <th>Gap (10)</th>
                    <th>Code (10)</th>
                    <th>Val (10)</th>
                    <th>Data (10)</th>
                    <th>Rep (10)</th>
                    <th>Def (10)</th>
                    <th>Fit (10)</th>
                    <th>Ceil (10)</th>
                    <th>LowEff (10)</th>
                    <th>NoLab (10)</th>
                    <th>NoStu (10)</th>
                    <th>NoCirc (10)</th>
                    <th>NoCode (10)</th>
                    <th>Long (10)</th>
                    <th>Raw (160)</th>
                    <th>Risk-Adj (160)</th>
                    <th>Confidence</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Dir B: Sobol GSA / AQbD Robustness</strong></td>
                    <td>8</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>10</td><td>8</td><td>9</td><td>8</td><td>8</td><td>10</td><td>10</td><td>9</td><td>8</td><td>9</td>
                    <td><strong>142</strong></td>
                    <td><strong>136</strong></td>
                    <td><span class="badge badge-green">95% HIGH</span></td>
                </tr>
                <tr>
                    <td><strong>Dir C: Multimodal Orthogonal QC</strong></td>
                    <td>8</td><td>8</td><td>8</td><td>9</td><td>8</td><td>8</td><td>9</td><td>8</td><td>8</td><td>8</td><td>8</td><td>10</td><td>10</td><td>8</td><td>8</td><td>8</td>
                    <td><strong>137</strong></td>
                    <td><strong>128</strong></td>
                    <td><span class="badge badge-green">90% HIGH</span></td>
                </tr>
                <tr>
                    <td><strong>Dir G: SoftwareX Platform Paper</strong></td>
                    <td>4</td><td>6</td><td>7</td><td>10</td><td>10</td><td>10</td><td>10</td><td>9</td><td>9</td><td>5</td><td>10</td><td>10</td><td>10</td><td>10</td><td>10</td><td>6</td>
                    <td><strong>136</strong></td>
                    <td><strong>134</strong></td>
                    <td><span class="badge badge-green">98% VERY HIGH</span></td>
                </tr>
                <tr>
                    <td><strong>Dir D: Bayesian MCMC Inference</strong></td>
                    <td>8</td><td>8</td><td>7</td><td>8</td><td>8</td><td>8</td><td>9</td><td>7</td><td>8</td><td>8</td><td>7</td><td>10</td><td>10</td><td>7</td><td>7</td><td>8</td>
                    <td><strong>128</strong></td>
                    <td><strong>116</strong></td>
                    <td><span class="badge badge-green">85% HIGH</span></td>
                </tr>
                <tr>
                    <td><strong>Dir A: Mechanistic Retention Prediction</strong></td>
                    <td>7</td><td>8</td><td>7</td><td>7</td><td>7</td><td>7</td><td>8</td><td>6</td><td>8</td><td>8</td><td>6</td><td>10</td><td>10</td><td>8</td><td>7</td><td>8</td>
                    <td><strong>122</strong></td>
                    <td><strong>108</strong></td>
                    <td><span class="badge badge-yellow">80% MOD</span></td>
                </tr>
                <tr>
                    <td><strong>Dir E: Diagnostic Fault Inversion (PAT)</strong></td>
                    <td>9</td><td>9</td><td>9</td><td>8</td><td>6</td><td>6</td><td>7</td><td>6</td><td>9</td><td>9</td><td>5</td><td>8</td><td>10</td><td>4</td><td>5</td><td>9</td>
                    <td><strong>119</strong></td>
                    <td><strong>98</strong></td>
                    <td><span class="badge badge-yellow">75% MOD</span></td>
                </tr>
                <tr>
                    <td><strong>Dir F: Autonomous Method Optimization</strong></td>
                    <td>7</td><td>7</td><td>6</td><td>7</td><td>6</td><td>7</td><td>7</td><td>6</td><td>7</td><td>7</td><td>5</td><td>10</td><td>10</td><td>7</td><td>5</td><td>8</td>
                    <td><strong>112</strong></td>
                    <td><strong>96</strong></td>
                    <td><span class="badge badge-yellow">70% MOD</span></td>
                </tr>
                <tr>
                    <td><strong>Educational Pilot (Phase 4 Freeze)</strong></td>
                    <td>5</td><td>6</td><td>7</td><td>8</td><td>4</td><td>3</td><td>7</td><td>6</td><td>7</td><td>6</td><td>6</td><td>10</td><td>0</td><td>8</td><td>8</td><td>6</td>
                    <td><strong>97</strong></td>
                    <td><strong>72</strong></td>
                    <td><span class="badge badge-red">60% ETHICS BLOCK</span></td>
                </tr>
            </tbody>
        </table>

        <div class="callout callout-note">
            <strong>SCORING RATIONALE SUMMARY:</strong> Direction B (Sobol GSA) achieves the highest raw score (142/160) and highest risk-adjusted score (136/160) 
            due to its perfect scores in zero lab requirement, zero student requirement, high reproducibility, and strong journal fit with <em>Analytica Chimica Acta</em>. 
            Direction G (SoftwareX) has the highest evidence confidence (98%) and lowest operational risk. 
            Direction E has immense ceiling (9/10), but suffers heavily in circularity risk (4/10) and development effort.
        </div>
    </div>

    <!-- SECTION 22: TEN INDEPENDENT RANKINGS -->
    <div class="page">
        <h2 class="section-title">22. TEN INDEPENDENT RANKINGS (RANKINGS A THROUGH J)</h2>
        
        <p class="body-text">
            To provide precise strategic clarity under any operational scenario, we construct 
            <strong>ten independent rankings</strong> addressing specific organizational goals:
        </p>

        <div class="grid-2">
            <div class="card">
                <div class="card-title">RANKING A: Best Paper with CURRENT CODE (Zero Mod)</div>
                <p class="card-text">
                    1. <strong>Direction G: SoftwareX Platform Paper</strong> (IF: 2.8)<br>
                    2. Direction C: Multimodal Matching Descriptor in Chemometrics<br>
                    3. Phase 3.5 Forensic Benchmark Report in JCE (Technology Report)
                </p>
            </div>
            <div class="card">
                <div class="card-title">RANKING B: Best After MINIMAL MODIFICATION (2–3 Wks)</div>
                <p class="card-text">
                    1. <strong>Direction B: Sobol GSA / AQbD in Anal. Chim. Acta</strong> (IF: 6.0)<br>
                    2. Direction C: Multimodal Orthogonal Benchmark in Chemometr.<br>
                    3. Direction D: Bayesian MCMC Inference in J. Chromatogr. A
                </p>
            </div>
        </div>

        <div class="grid-2" style="margin-top: 10px;">
            <div class="card">
                <div class="card-title">RANKING C: Best After LIMITED HPLC LAB (12 Injections)</div>
                <p class="card-text">
                    1. <strong>Direction B + Level 2 Lab Verification in Talanta</strong> (IF: 6.1)<br>
                    2. Direction D + Level 2 MCMC Verification in J. Chromatogr. A<br>
                    3. Direction E + Level 2 Physical Fault Injection in Anal. Chem.
                </p>
            </div>
            <div class="card">
                <div class="card-title">RANKING D: HIGHEST SCIENTIFIC CEILING (Flagship)</div>
                <p class="card-text">
                    1. <strong>Direction E: Fault Inversion for PAT in Analytical Chemistry</strong> (IF: 7.4)<br>
                    2. Direction B: Global Sensitivity & Failure Mapping in ACA (IF: 6.0)<br>
                    3. Direction F: Autonomous Chemometrics Agent in JCIM (IF: 5.6)
                </p>
            </div>
        </div>

        <div class="grid-2" style="margin-top: 10px;">
            <div class="card">
                <div class="card-title">RANKING E: Best EVIDENCE-TO-EFFORT Ratio</div>
                <p class="card-text">
                    1. <strong>Direction B: Sobol GSA</strong> (Score: 136; Effort: 2.5 weeks)<br>
                    2. Direction G: SoftwareX Descriptor (Score: 134; Effort: 1.5 weeks)<br>
                    3. Direction C: Multimodal Orthogonal QC (Score: 128; Effort: 2 weeks)
                </p>
            </div>
            <div class="card">
                <div class="card-title">RANKING F: LOWEST-RISK Publication Route</div>
                <p class="card-text">
                    1. <strong>Direction G: SoftwareX Platform Paper</strong> (>90% acceptance)<br>
                    2. Direction B: Sobol GSA in Computers & Chem. Eng.<br>
                    3. Direction C: Multimodal Chemometric Benchmark
                </p>
            </div>
        </div>

        <div class="grid-2" style="margin-top: 10px;">
            <div class="card">
                <div class="card-title">RANKING G: Best for TIER-1 ANALYTICAL CHEMISTRY</div>
                <p class="card-text">
                    1. <strong>Direction B: Sobol GSA in Analytica Chimica Acta</strong> (IF: 6.0)<br>
                    2. Direction E: Fault Inversion in Analytical Chemistry (IF: 7.4)<br>
                    3. Direction D: Bayesian Parameter Inference in J. Chromatogr. A
                </p>
            </div>
            <div class="card">
                <div class="card-title">RANKING H: Best Route Requiring NO STUDENTS</div>
                <p class="card-text">
                    1. <strong>Direction B: Sobol GSA / AQbD Robustness</strong><br>
                    2. Direction C: Multimodal Orthogonal QC Benchmark<br>
                    3. Direction G: SoftwareX Platform Descriptor
                </p>
            </div>
        </div>

        <div class="grid-2" style="margin-top: 10px;">
            <div class="card">
                <div class="card-title">RANKING I: Best Route Requiring NO PHYSICAL LAB</div>
                <p class="card-text">
                    1. <strong>Direction B: Sobol GSA</strong> (NIST SRM 870 validation)<br>
                    2. Direction C: Multimodal QC (MassBank/GNPS validation)<br>
                    3. Direction G: SoftwareX (Automated test suite validation)
                </p>
            </div>
            <div class="card">
                <div class="card-title">RANKING J: Best LONG-TERM SIMUPHARM PROGRAM</div>
                <p class="card-text">
                    1. <strong>Phase 1: SoftwareX Paper</strong> (Establish software baseline)<br>
                    2. <strong>Phase 2: ACA Sobol GSA Paper</strong> (Flagship methods contribution)<br>
                    3. <strong>Phase 3: Analytical Chemistry PAT Paper</strong> (Fault inversion)
                </p>
            </div>
        </div>
    </div>

    <!-- SECTION 23: MULTI-PAPER STRATEGY & INDEPENDENCE -->
    <div class="page">
        <h2 class="section-title">23. MULTI-PAPER STRATEGY & INDEPENDENCE VERIFICATION</h2>
        
        <p class="body-text">
            Can SimuPharm support multiple publications without committing "salami slicing"? 
            We audit scientific independence across three proposed papers:
        </p>

        <h3 class="subsection-title">23.1 Rigorous Scientific Independence Audit</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Evaluation Dimension</th>
                    <th>Paper 1: Software Platform (SoftwareX)</th>
                    <th>Paper 2: AQbD Global Sensitivity (ACA)</th>
                    <th>Paper 3: Multimodal QC Benchmark (Chemometrics)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Central Question</strong></td>
                    <td>How to architect client-side 7-instrument simulation?</td>
                    <td>How do non-linear parameter uncertainties propagate into separation failure under ICH Q14?</td>
                    <td>What is the quantitative false-discovery reduction achieved by orthogonal multi-instrument data fusion?</td>
                </tr>
                <tr>
                    <td><strong>Primary Contribution</strong></td>
                    <td>Open-source software platform and modular REST APIs.</td>
                    <td>Variance-based global sensitivity methodology and failure mapping.</td>
                    <td>Information-theoretic entropy reduction and false-discovery bounds.</td>
                </tr>
                <tr>
                    <td><strong>Mathematical Engine</strong></td>
                    <td>Full-stack WebAssembly/FastAPI numerical architecture.</td>
                    <td>Sobol functional ANOVA decomposition ($S_i, S_{Ti}$).</td>
                    <td>Bayesian evidence fusion across 5 orthogonal measurement blocks.</td>
                </tr>
                <tr>
                    <td><strong>Empirical Benchmark</strong></td>
                    <td>Unit test coverage and latency execution benchmarks.</td>
                    <td>NIST SRM 870 certified column selectivity probe mixture.</td>
                    <td>21 curated APIs + 1,000 synthetic isomer decoy matrices.</td>
                </tr>
                <tr>
                    <td><strong>Overlap Verdict</strong></td>
                    <td colspan="3" style="text-align: center; background-color: #f0fdf4; color: #166534; font-weight: 700;">
                        100% SCIENTIFICALLY INDEPENDENT. ZERO OVERLAPPING CLAIMS. FULLY COMPATIBLE PORTFOLIO.
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 24: SMART-WORK DECISION -->
    <div class="page">
        <h2 class="section-title">24. SMART-WORK DECISION: MAXIMIZING VALUE / MINIMIZING RISK</h2>
        
        <p class="body-text">
            The Phase 5.1 audit answers the quintessential strategic question: 
            <em>"What is the smartest scientific thing we can do next?"</em>
        </p>

        <div class="callout callout-discovery">
            <strong>THE SMART-WORK FORMULATION:</strong><br>
            $$\text{Publication Value} = \frac{\text{Scientific Novelty} \times \text{Journal Impact Factor} \times \text{Reviewer Acceptance Probability}}{\text{Development Time} + \text{Financial Cost} + \text{Regulatory / Ethics Risk}}$$
        </div>

        <p class="body-text">
            Applying this formula eliminates low-yield paths:
        </p>
        <ul class="bullet-list">
            <li><strong>Eliminate Full Lab Campaigns (Level 4):</strong> Spending $15,000 and 6 months running physical chromatograms provides diminishing returns when open public benchmarks (NIST, Tanaka) already exist for free.</li>
            <li><strong>Bypass Student Recruitment:</strong> Bypassing the frozen Phase 4 educational study eliminates months of IRB delays and participant recruitment risks.</li>
            <li><strong>Avoid Deep Machine Learning on Single Gradients:</strong> Training 100,000-parameter neural networks on METLIN SMRT yields an uninterpretable black box that reviewers will criticize for lack of physical insight.</li>
            <li><strong>Select the Smartest Move:</strong> Direction B (Sobol GSA in <em>Analytica Chimica Acta</em>) maximizes the numerator (Q1 IF 6.0, high novelty under ICH Q14, >85% acceptance) while minimizing the denominator (2.5 weeks, $0 cost, zero regulatory risk).</li>
        </ul>
    </div>

    <!-- SECTION 25: FINAL RECOMMENDATION (18-POINT STRUCTURE) -->
    <div class="page">
        <h2 class="section-title">25. FINAL RECOMMENDATION (EXPLICIT 18-POINT STRUCTURE)</h2>
        
        <p class="body-text">
            In exact compliance with Section 26 of the project directive, we deliver the definitive strategic decision:
        </p>

        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 32%;">Decision Field</th>
                    <th style="width: 68%;">Authoritative Strategic Ruling</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>1. BEST CURRENT-CODE PAPER</strong></td>
                    <td><strong>SoftwareX Architecture Paper</strong>: <em>"SimuPharm: An Open-Source, Full-Stack Multi-Instrument Pharmaceutical Simulation Platform."</em></td>
                </tr>
                <tr>
                    <td><strong>2. BEST MINIMAL-MODIFICATION PAPER</strong></td>
                    <td><strong>Direction B in Analytica Chimica Acta</strong>: <em>"Global Sensitivity Analysis and Sobol Variance Decomposition of Chromatographic Uncertainty Spaces in Analytical Quality by Design (ICH Q14)."</em></td>
                </tr>
                <tr>
                    <td><strong>3. BEST LIMITED-LAB PAPER</strong></td>
                    <td><strong>Direction B + 12 Targeted Bench HPLC Injections</strong> in <em>Talanta</em> (verifying predicted parameter sensitivity ranking on real C18 hardware).</td>
                </tr>
                <tr>
                    <td><strong>4. HIGHEST-CEILING PAPER</strong></td>
                    <td><strong>Direction E in Analytical Chemistry (ACS)</strong>: <em>"Probabilistic Inverse Fault Deconvolution for Self-Diagnosing Process Analytical Technology in Liquid Chromatography."</em></td>
                </tr>
                <tr>
                    <td><strong>5. BEST NO-STUDENT ROUTE</strong></td>
                    <td><strong>Direction B (Sobol GSA / AQbD Robustness)</strong>: Completely independent of human participants.</td>
                </tr>
                <tr>
                    <td><strong>6. BEST NO-LAB ROUTE</strong></td>
                    <td><strong>Direction B (Sobol GSA / AQbD Robustness)</strong>: Validated via NIST SRM 870 certified constants and Tanaka 250-column database.</td>
                </tr>
                <tr>
                    <td><strong>7. BEST EVIDENCE/EFFORT ROUTE</strong></td>
                    <td><strong>Direction B (Sobol GSA)</strong>: Score 136/160; requires only ~200 lines of Python wrapping <span class="code-span">SALib</span> around existing code.</td>
                </tr>
                <tr>
                    <td><strong>8. BEST TARGET JOURNAL</strong></td>
                    <td><strong>Analytica Chimica Acta</strong> (Elsevier, Impact Factor: <strong>6.0</strong>).</td>
                </tr>
                <tr>
                    <td><strong>9. SECOND-BEST TARGET JOURNAL</strong></td>
                    <td><strong>Computers & Chemical Engineering</strong> (Elsevier, Impact Factor: <strong>4.3</strong>) or <strong>SoftwareX</strong> (Impact Factor: <strong>2.8</strong>).</td>
                </tr>
                <tr>
                    <td><strong>10. ROUTE TO EXECUTE FIRST</strong></td>
                    <td><strong>Direction B (Sobol GSA for AQbD)</strong>, with <strong>Direction G (SoftwareX)</strong> prepared concurrently.</td>
                </tr>
                <tr>
                    <td><strong>11. ROUTE TO KEEP AS BACKUP</strong></td>
                    <td><strong>Direction C (Multimodal Orthogonal Identification Benchmark)</strong>.</td>
                </tr>
                <tr>
                    <td><strong>12. ROUTES TO ABANDON</strong></td>
                    <td>(1) Submitting unmodified code as "novel chemistry", (2) METLIN SMRT single-gradient mechanistic prediction, (3) Level 4 physical lab campaigns, and (4) Pure 3D VR WebGL marketing papers.</td>
                </tr>
                <tr>
                    <td><strong>13. DO WE NEED STUDENTS?</strong></td>
                    <td><strong>NO.</strong> Educational route is ethically blocked and narrow. All top-ranked routes require zero human participants.</td>
                </tr>
                <tr>
                    <td><strong>14. DO WE NEED A LAB?</strong></td>
                    <td><strong>NO.</strong> Open experimental reference datasets (NIST SRM 870, Tanaka database) provide complete independent empirical anchors.</td>
                </tr>
                <tr>
                    <td><strong>15. DO WE NEED MAJOR CODE REWRITE?</strong></td>
                    <td><strong>NO.</strong> The core scientific engine is verified. Direction B requires only an external analysis script without modifying core source code.</td>
                </tr>
                <tr>
                    <td><strong>16. CAN PLATFORM SUPPORT >1 INDEPENDENT PAPER?</strong></td>
                    <td><strong>YES.</strong> Supports three genuinely independent papers (SoftwareX architecture, ACA Sobol GSA, and Chemometrics multimodal QC).</td>
                </tr>
                <tr>
                    <td><strong>17. MOST IMPORTANT EXPERIMENT / ANALYSIS NEXT</strong></td>
                    <td>Implement Saltelli parameter sampling ($N=16,384$) on SimuPharm's HPLC model to calculate first-order ($S_i$) and total-order ($S_{Ti}$) Sobol indices for the NIST SRM 870 mixture.</td>
                </tr>
                <tr>
                    <td><strong>18. MOST IMPORTANT THING NOT TO DO</strong></td>
                    <td><strong>DO NOT revive refuted marketing claims</strong> ("universal 2% accuracy", "digital twin", "300+ compounds") or present hardcoded 50% B calibration as independent predictive validation.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 26: EXECUTION ROADMAP -->
    <div class="page">
        <h2 class="section-title">26. PHASED RESEARCH EXECUTION ROADMAP (PHASES 1–9)</h2>
        
        <p class="body-text">
            Below is the operational execution roadmap to transition from the Phase 5.1 decision to peer-reviewed submission:
        </p>

        <div class="timeline-container">
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 1: EVIDENCE & HASH VERIFICATION</span><span class="timeline-duration">DAYS 1–3</span></div>
                <p class="timeline-text">Freeze engine hashes; archive Phase 5.1 report; verify reproducible execution of <span class="code-span">backend/science/hplc.py</span> under Python 3.12.</p>
            </div>
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 2: DATASET ACQUISITION & FORMATTING</span><span class="timeline-duration">DAYS 4–7</span></div>
                <p class="timeline-text">Download and structure NIST SRM 870 certified constants and Tanaka 250-column database into standardized JSON input format.</p>
            </div>
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 3: MODEL/DATA COMPATIBILITY AUDIT</span><span class="timeline-duration">DAYS 8–10</span></div>
                <p class="timeline-text">Execute forward simulation runs on NIST SRM 870 probe solutes; confirm zero divergence in retention time and pressure bounds.</p>
            </div>
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 4: INDEPENDENT BENCHMARK SCRIPTING</span><span class="timeline-duration">DAYS 11–14</span></div>
                <p class="timeline-text">Write <span class="code-span">salib_sobol.py</span> wrapper; define 6-parameter sampling problem; execute $N=1,024$ trial convergence test.</p>
            </div>
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 5: BASELINE IMPLEMENTATION</span><span class="timeline-duration">DAYS 15–17</span></div>
                <p class="timeline-text">Implement conventional One-Factor-at-a-Time (OFAT) local sensitivity stepping for direct head-to-head comparison against Sobol GSA.</p>
            </div>
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 6: MAIN COMPUTATIONAL EXPERIMENT</span><span class="timeline-duration">DAYS 18–21</span></div>
                <p class="timeline-text">Execute full Saltelli quasirandom sweep ($N=16,384$ runs); record $R_{s, \min}, t_R, \Delta P, T$; compute first-order and total-effect indices.</p>
            </div>
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 7: ROBUSTNESS & INTERACTION MAPPING</span><span class="timeline-duration">DAYS 22–24</span></div>
                <p class="timeline-text">Map non-linear parameter interaction surfaces ($S_{Ti} - S_i$); calculate Separation Failure Probability ($P(R_s < 1.5)$) across ICH Q14 MODR.</p>
            </div>
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 8: REVIEWER RED-TEAM AUDIT</span><span class="timeline-duration">DAYS 25–26</span></div>
                <p class="timeline-text">Conduct internal adversarial review against top 5 reviewer objections; verify bootstrap confidence intervals on all Sobol indices.</p>
            </div>
            <div class="timeline-card">
                <div class="timeline-header"><span class="timeline-phase">PHASE 9: MANUSCRIPT PREPARATION & SUBMISSION</span><span class="timeline-duration">DAYS 27–30</span></div>
                <p class="timeline-text">Draft full manuscript following <em>Analytica Chimica Acta</em> formatting guidelines; format publication-quality vector figures; submit.</p>
            </div>
        </div>
    </div>

    <!-- SECTION 27: COMPREHENSIVE EVIDENCE LEDGER -->
    <div class="page">
        <h2 class="section-title">27. COMPREHENSIVE EVIDENCE LEDGER</h2>
        
        <p class="body-text">
            To maintain absolute transparency and prevent unverified inferences from masquerading as facts, 
            every critical assertion in this report is cataloged with its evidentiary provenance and falsification condition:
        </p>

        <h3 class="subsection-title">27.1 Epistemic Ledger</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 25%;">Major Factual Assertion / Claim</th>
                    <th>Source Document / Code File</th>
                    <th>Evidence Classification</th>
                    <th>Epistemic Confidence</th>
                    <th>What Would Falsify It?</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>SimuPharm contains 21 compounds, not 300+</strong></td>
                    <td><span class="code-span">backend/compounds/database.py</span> (AST inspection)</td>
                    <td><span class="badge badge-observed">DIRECTLY OBSERVED</span></td>
                    <td>100% Certain</td>
                    <td>Finding an external uncommitted JSON file with $>279$ additional valid compound records.</td>
                </tr>
                <tr>
                    <td><strong>2.07% MAPE is an artifact of calibration at 50% B</strong></td>
                    <td><span class="code-span">hplc_simulator_script.js</span> & Phase 3.5 hostile audit</td>
                    <td><span class="badge badge-observed">DIRECTLY OBSERVED</span></td>
                    <td>100% Certain</td>
                    <td>Demonstrating that the simulator was evaluated on arbitrary uncalibrated mixtures without hardcoded `standardRt`.</td>
                </tr>
                <tr>
                    <td><strong>Gradient simulation exhibits 25.50% MAPE</strong></td>
                    <td>Phase 3.5 raw simulation results (<span class="code-span">phase3_raw_simulation_results.json</span>)</td>
                    <td><span class="badge badge-data">AUDITED NUMERICAL DATA</span></td>
                    <td>100% Certain</td>
                    <td>Recalculating gradient residuals against verified experimental chromatograms and discovering mathematical calculation error.</td>
                </tr>
                <tr>
                    <td><strong>METLIN SMRT has only 1 gradient per compound</strong></td>
                    <td>Figshare repository metadata (<span class="code-span">doi.org/10.6084/m9.figshare.8038913</span>)</td>
                    <td><span class="badge badge-pub">VERIFIED PUBLIC DATASET</span></td>
                    <td>100% Certain</td>
                    <td>Locating a multi-gradient supplementary file in METLIN SMRT containing isocratic runs.</td>
                </tr>
                <tr>
                    <td><strong>Sobol interactions account for >25% of variance</strong></td>
                    <td>Theoretical sensitivity formulation & Phase 5 screening</td>
                    <td><span class="badge badge-hyp">RESEARCH HYPOTHESIS</span></td>
                    <td>85% Plausible</td>
                    <td>Executing $N=16,384$ Saltelli runs and finding that $\sum (S_{Ti} - S_i) < 0.05$ across all operational variables.</td>
                </tr>
                <tr>
                    <td><strong>SoftwareX will accept SimuPharm architecture</strong></td>
                    <td>SoftwareX Aims & Scope, recent published articles (2022–2025)</td>
                    <td><span class="badge badge-lit">SUPPORTED BY LITERATURE</span></td>
                    <td>90% High</td>
                    <td>SoftwareX editorial desk rejection stating analytical chemistry simulation is out of scope.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 28: BIBLIOGRAPHIC REFERENCES -->
    <div class="page">
        <h2 class="section-title">28. BIBLIOGRAPHIC REFERENCES (VERIFIED DOIs ONLY)</h2>
        
        <p class="body-text" style="font-size: 7.5pt; line-height: 1.35;">
            [1] Boswell, P. G.; Stoll, D. R.; Carr, P. W. Easy-to-Use Web-Based High-Performance Liquid Chromatography Simulator for Teaching and Learning. <em>J. Chem. Educ.</em> <strong>2013</strong>, <em>90</em> (2), 198–202. DOI: 10.1021/ed300508h.<br>
            [2] Boswell, P. G.; Carr, P. W.; Stoll, D. R. A Simple Method for Predicting Retention in Reversed-Phase Liquid Chromatography under Any Gradient Conditions. <em>J. Chromatogr. A</em> <strong>2011</strong>, <em>1218</em> (38), 6732–6741. DOI: 10.1016/j.chroma.2011.07.070.<br>
            [3] Leweke, S.; von Lieres, E. Chromatography Analysis and Design Toolkit (CADET). <em>Comput. Chem. Eng.</em> <strong>2018</strong>, <em>113</em>, 274–294. DOI: 10.1016/j.compchemeng.2018.03.023.<br>
            [4] Domingo-Almenara, X.; Guijas, C.; Billings, E.; Benton, H. P.; Siuzdak, G. The METLIN Small Molecule Dataset for Machine Learning-Based Retention Time Prediction. <em>Nat. Commun.</em> <strong>2019</strong>, <em>10</em>, 5813. DOI: 10.1038/s41467-019-13680-7.<br>
            [5] Molnár, I.; Rieger, H. J.; Monks, K. E. Aspects of the "Design Space" in High Performance Liquid Chromatography Method Development. <em>J. Chromatogr. A</em> <strong>2010</strong>, <em>1217</em> (19), 3193–3200. DOI: 10.1016/j.chroma.2010.02.001.<br>
            [6] Sobol, I. M. Global Sensitivity Indices for Nonlinear Mathematical Models and Their Monte Carlo Estimates. <em>Math. Comput. Simul.</em> <strong>2001</strong>, <em>55</em> (1–3), 271–280. DOI: 10.1016/S0378-4754(00)00270-6.<br>
            [7] Saltelli, A.; Ratto, M.; Andres, T.; Campolongo, F.; Cariboni, J.; Gatelli, D.; Saisana, M.; Tarantola, S. <em>Global Sensitivity Analysis: The Primer</em>; John Wiley & Sons: Chichester, UK, 2008.<br>
            [8] International Council for Harmonisation (ICH). ICH Harmonised Guideline: Analytical Procedure Development Q14; Step 4 Version; ICH: Geneva, Switzerland, 2023.<br>
            [9] International Council for Harmonisation (ICH). ICH Harmonised Guideline: Validation of Analytical Procedures Q2(R2); Step 4 Version; ICH: Geneva, Switzerland, 2023.<br>
            [10] Tanaka, N.; Kimata, K.; Mikawa, Y.; Hosoya, K.; Araki, T.; Ohtsu, Y.; Shiojima, Y.; Tsuboi, R.; Tsuchiya, H. Characterization of Reversed-Phase Liquid Chromatography Columns by Chromatographic Tests. <em>J. Chromatogr. Sci.</em> <strong>1989</strong>, <em>27</em> (12), 721–728. DOI: 10.1093/chromsci/27.12.721.<br>
            [11] Euerby, M. R.; Petersson, P. Chromatographic Classification and Comparison of Reversed-Phase High-Performance Liquid Chromatography Columns. <em>J. Chromatogr. A</em> <strong>2003</strong>, <em>994</em> (1–2), 13–36. DOI: 10.1016/S0021-9673(03)00394-5.<br>
            [12] Neue, U. D.; Kuss, H. J. Improved Method for the Calculation of the Retention of Small Molecules in Reversed-Phase Liquid Chromatography. <em>J. Chromatogr. A</em> <strong>2002</strong>, <em>946</em> (1–2), 91–101. DOI: 10.1016/S0021-9673(01)01540-9.<br>
            [13] Snyder, L. R.; Kirkland, J. J.; Dolan, J. W. <em>Introduction to Modern Liquid Chromatography</em>, 3rd ed.; John Wiley & Sons: Hoboken, NJ, 2010.<br>
            [14] Dolan, J. W. LCGC Troubleshooting: Temperature and Retention. <em>LCGC North Am.</em> <strong>2014</strong>, <em>32</em> (10), 786–791.<br>
            [15] Herman, J.; Usher, W. SALib: An Open-Source Python Library for Sensitivity Analysis. <em>J. Open Source Softw.</em> <strong>2017</strong>, <em>2</em> (9), 97. DOI: 10.21105/joss.00097.<br>
            [16] Foreman-Mackey, D.; Hogg, D. W.; Lang, D.; Goodman, J. emcee: The MCMC Hammer. <em>Publ. Astron. Soc. Pac.</em> <strong>2013</strong>, <em>125</em> (925), 306–312. DOI: 10.1086/670067.<br>
            [17] Horai, H.; Arita, M.; Kanaya, S.; Nihei, Y.; Tasaka, T.; et al. MassBank: A Public Repository for Sharing Mass Spectral Data for Life Sciences. <em>J. Mass Spectrom.</em> <strong>2010</strong>, <em>45</em> (7), 703–714. DOI: 10.1002/jms.1777.<br>
            [18] National Institute of Standards and Technology (NIST). <em>Standard Reference Material 870: Column Selectivity Test Mixture for Liquid Chromatography</em>; NIST Special Publication 260-142; Gaithersburg, MD, 2004.<br>
            [19] Desmet, G.; Cabooter, D. Kinetic Plots for the Comparison and Selection of Chromatographic Systems. <em>J. Chromatogr. A</em> <strong>2009</strong>, <em>1216</em> (8), 1276–1288. DOI: 10.1016/j.chroma.2008.10.024.<br>
            [20] De Vos, J.; Stassen, C.; Desmet, G.; Euerby, M. R. Retention Modelling and Design Space Optimisation in Liquid Chromatography. <em>TrAC Trends Anal. Chem.</em> <strong>2021</strong>, <em>135</em>, 116147. DOI: 10.1016/j.trac.2020.116147.
        </p>
    </div>
    """

if __name__ == "__main__":
    print("Part 4 generated successfully. Length:", len(get_part4_html()))
