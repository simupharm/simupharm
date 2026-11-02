"""
PHASE 5 — PART 3: SECTIONS 17 TO 24
SimuPharm Open-Ended Publication & Innovation Discovery Sprint
"""

def get_part3_html():
    return """
    <!-- SECTION 17: COMPETITOR & PRIOR-ART LANDSCAPE -->
    <div class="page">
        <h2 class="section-title">17. COMPETITOR & PRIOR-ART LANDSCAPE</h2>
        
        <p class="body-text">
            To establish clear novelty, SimuPharm must be rigorously contrasted against the entire landscape of existing analytical modeling tools, 
            chromatography simulators, and virtual laboratory environments. 
            Competing tools fall into three distinct functional categories: 
            (1) <em>Commercial Method Development Software</em>, 
            (2) <em>Academic Separation Simulators</em>, and 
            (3) <em>Gamified Virtual Science Labs</em>.
        </p>

        <h3 class="subsection-title">17.1 Major Competing Platforms</h3>
        <ul class="bullet-list">
            <li><strong>DryLab® 4 (Molnár-Institute, Berlin):</strong> The global gold-standard commercial modeling software in regulated pharmaceutical AQbD. 
            Uses Snyder's Linear Solvent Strength (LSS) theory to model multi-dimensional resolution cubes ($t_G \\times T \\times \\text{pH} \\times \\%B$) from 4 to 12 scouting runs. 
            <em>Strengths:</em> Industrial regulatory acceptance (FDA, EMA), high accuracy, ICH Q14 documentation. 
            <em>Weaknesses:</em> Closed-source, extremely expensive ($10,000+ per license), desktop-only Windows installation, zero fault simulation, limited to liquid chromatography.</li>
            <li><strong>ChromSword® Auto (Dr. Galushko Software):</strong> Leading commercial automated method development suite. 
            Integrates directly with physical HPLC hardware (Waters, Agilent) to autonomously execute screening runs and optimize gradient profiles via heuristic search. 
            <em>Strengths:</em> Hardware automation, automated column screening. 
            <em>Weaknesses:</em> Closed proprietary algorithms, high cost, no spectroscopic cross-instrument capabilities, no public API.</li>
            <li><strong>HPLC-Simulator.org (Boswell, Stoll, Carr, 2013–2024):</strong> Open-source, web-based educational simulator (J. Chem. Educ. 2013, 90, 2, 198–202). 
            Runs in browser via JavaScript; simulates isocratic and simple gradient separations, column parameters, and solvent composition. 
            <em>Strengths:</em> Free, web-accessible, well-known in chemical education. 
            <em>Weaknesses:</em> Purely educational, strictly 1D HPLC (no UV, FTIR, MS, GC, or polarimetry), zero physical fault modes, no sensitivity quantification, no backend API.</li>
            <li><strong>CADET / CADET-Process (Leweke & von Lieres, FZ Jülich, 2018):</strong> Open-source, high-performance C++/Python/Julia framework 
            for chromatography and downstream bioprocess modeling (Comput. Chem. Eng. 2018, 113, 274–294). 
            <em>Strengths:</em> Rigorous mathematical solver for General Rate Model (GRM) coupled PDAEs, sensitivity analysis, simulated moving bed (SMB) chromatography. 
            <em>Weaknesses:</em> Heavy computational setup, steep learning curve, oriented toward bioprocess engineering rather than small-molecule pharmaceutical QC, no web UI.</li>
            <li><strong>PyChrom (Shukla, 2019):</strong> Python package for chromatographic modeling and isotherm parameter estimation. 
            <em>Strengths:</em> Clean Python interface. <em>Weaknesses:</em> Limited maintenance, no web interface, lacks spectroscopic or multi-instrument integration.</li>
            <li><strong>Labster / PraxiLabs:</strong> Commercial 3D virtual science laboratories for university education. 
            <em>Strengths:</em> High-end 3D graphics, gamified student narrative, broad institutional adoption. 
            <em>Weaknesses:</em> Scientifically superficial; procedural animations rather than real physical/kinetic differential solvers; cannot be used for research or method development.</li>
        </ul>

        <h3 class="subsection-title">17.2 The Strategic White Space for SimuPharm</h3>
        <div class="callout callout-discovery">
            <strong>CRITICAL GAP DISCOVERY:</strong> Across the entire competitive spectrum, there is <strong>not a single platform</strong> that combines:
            (1) <em>Zero-installation, client-side web accessibility</em>, 
            (2) <em>Multi-instrument orthogonal analytical integration</em> (HPLC + GC + UV-Vis + FTIR + MS), 
            (3) <em>Physically coupled fault-injection and diagnostic troubleshooting</em>, and 
            (4) <em>Open-source programmatic APIs for automated chemometric experimentation</em>. 
            This white space represents SimuPharm's defensible scientific territory.
        </div>
    </div>

    <!-- SECTION 18: PRIOR-ART DETAILED OVERLAP ANALYSIS -->
    <div class="page">
        <h2 class="section-title">18. PRIOR-ART DETAILED OVERLAP ANALYSIS</h2>
        
        <p class="body-text">
            To prevent claims of novelty over existing work, this section provides an exhaustive feature-by-feature comparison 
            between SimuPharm and the primary prior-art platforms across sixteen technical dimensions.
        </p>

        <h3 class="subsection-title">18.1 Master Feature Comparison Matrix</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Capability Dimension</th>
                    <th>SimuPharm (Audited)</th>
                    <th>HPLC-Simulator.org</th>
                    <th>DryLab® 4</th>
                    <th>CADET</th>
                    <th>Labster</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Access Architecture</strong></td>
                    <td>Browser (JS) + Python FastAPI</td>
                    <td>Browser (JS)</td>
                    <td>Desktop (Windows Native)</td>
                    <td>C++ Engine + Python CLI</td>
                    <td>Web / Desktop App</td>
                </tr>
                <tr>
                    <td><strong>Open Source Status</strong></td>
                    <td>Open Source (Target MIT/GPL)</td>
                    <td>Open Source</td>
                    <td>Proprietary Closed Source</td>
                    <td>Open Source (GPL-3.0)</td>
                    <td>Proprietary Commercial</td>
                </tr>
                <tr>
                    <td><strong>Multi-Instrument Suite</strong></td>
                    <td><strong>7 Instruments</strong> (LC, GC, UV, IR, MS, Pol, PSA)</td>
                    <td>1 Instrument (HPLC Only)</td>
                    <td>1 Instrument (HPLC/UHPLC)</td>
                    <td>1 Instrument (Column Prep LC)</td>
                    <td>Multiple (Cartoon Animation)</td>
                </tr>
                <tr>
                    <td><strong>Separation Physics</strong></td>
                    <td>Van Deemter + Plate Theory + Darcy</td>
                    <td>Empirical Fitting + Poppe plots</td>
                    <td>Snyder LSS + Neue-Kuss Models</td>
                    <td>General Rate Model (GRM PDAEs)</td>
                    <td>Pre-scripted Animation Frames</td>
                </tr>
                <tr>
                    <td><strong>Spectroscopic Modeling</strong></td>
                    <td>Beer-Lambert + FFT FTIR + MS Isotopes</td>
                    <td>Single-wavelength absorbance</td>
                    <td>None (Chromatograms only)</td>
                    <td>None (Solute concentrations)</td>
                    <td>Static texture overlays</td>
                </tr>
                <tr>
                    <td><strong>Instrument Fault Injection</strong></td>
                    <td><strong>6 Dynamic Physical Fault Modes</strong></td>
                    <td>None</td>
                    <td>None (Ideal physics only)</td>
                    <td>None (Ideal transport only)</td>
                    <td>Scripted quiz errors</td>
                </tr>
                <tr>
                    <td><strong>Diagnostic Inversion</strong></td>
                    <td>Implemented (Heuristic) / Extensible</td>
                    <td>None</td>
                    <td>None</td>
                    <td>Parameter optimization only</td>
                    <td>Multiple choice feedback</td>
                </tr>
                <tr>
                    <td><strong>AQbD Design Space Cube</strong></td>
                    <td>Extensible (Pareto optimization)</td>
                    <td>None</td>
                    <td><strong>Gold Standard 3D MODR</strong></td>
                    <td>Process optimization flowsheets</td>
                    <td>None</td>
                </tr>
                <tr>
                    <td><strong>Global Sensitivity Analysis</strong></td>
                    <td>Extensible (Sobol / SALib ready)</td>
                    <td>None</td>
                    <td>Local OFAT robustness table</td>
                    <td>Forward sensitivity derivatives</td>
                    <td>None</td>
                </tr>
                <tr>
                    <td><strong>API / Programmatic Execution</strong></td>
                    <td>Full REST API (FastAPI JSON endpoints)</td>
                    <td>None (GUI only)</td>
                    <td>Restricted Automation API</td>
                    <td>Full Python / Julia API</td>
                    <td>None (Closed LMS)</td>
                </tr>
                <tr>
                    <td><strong>Autonomous AI Agent</strong></td>
                    <td>Implemented (Tool-calling LabAgent)</td>
                    <td>None</td>
                    <td>None</td>
                    <td>None</td>
                    <td>Scripted virtual assistant</td>
                </tr>
                <tr>
                    <td><strong>Concept Knowledge Graph</strong></td>
                    <td>Implemented (NetworkX 25+ nodes)</td>
                    <td>None</td>
                    <td>None</td>
                    <td>None</td>
                    <td>Linear story progression</td>
                </tr>
                <tr>
                    <td><strong>Cost Barrier</strong></td>
                    <td><strong>Free / Open Science</strong></td>
                    <td>Free / Open Science</td>
                    <td>$10,000 – $25,000 / seat</td>
                    <td>Free / Open Science</td>
                    <td>High Institutional Subscription</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 19: NOVELTY GAP ANALYSIS -->
    <div class="page">
        <h2 class="section-title">19. NOVELTY GAP ANALYSIS</h2>
        
        <p class="body-text">
            To withstand hostile peer review in top analytical chemistry and computational chemistry journals, every proposed publication 
            direction must be dissected across five rigorous criteria: 
            <strong>A. Prior Art</strong>, 
            <strong>B. Direct Overlap</strong>, 
            <strong>C. Definitive Difference</strong>, 
            <strong>D. Novelty Status</strong>, and 
            <strong>E. Required Empirical Evidence</strong>.
        </p>

        <h3 class="subsection-title">19.1 Novelty Dissection of Top Candidate Concepts</h3>

        <div class="card" style="margin-bottom: 12px;">
            <div class="card-title">Concept 1: Global Sensitivity Analysis (Sobol GSA) of Chromatographic Separation Spaces</div>
            <p class="card-text">
                <strong>A. Prior Art:</strong> Commercial tools (DryLab) compute local robustness by stepping variables $\pm 1$ unit one-at-a-time (OFAT). 
                Von Lieres et al. (CADET) implemented sensitivity equations for preparative bioprocess chromatography.<br>
                <strong>B. Overlap:</strong> Both examine how method parameters (flow, temperature, %B) affect chromatographic separation quality.<br>
                <strong>C. Definitive Difference:</strong> SimuPharm introduces <em>variance-based global sensitivity analysis (Sobol indices $S_i, S_{Ti}$)</em> 
                to analytical small-molecule chromatography, mapping non-linear interactions across the full ICH Q14 design space without local linearity assumptions.<br>
                <strong>D. Novelty Status:</strong> <span class="badge badge-green">GENUINE METHODOLOGICAL NOVELTY</span> in analytical HPLC QC.<br>
                <strong>E. Evidence Required:</strong> Mathematical proof of convergence, Sobol bootstrap confidence intervals, and benchmark against an experimental 4-compound separation.
            </p>
        </div>

        <div class="card" style="margin-bottom: 12px;">
            <div class="card-title">Concept 2: Multi-Modal Analytical Fault Inversion & Self-Diagnosing PAT</div>
            <p class="card-text">
                <strong>A. Prior Art:</strong> Decades of qualitative troubleshooting guides (Dolan, Meyer, Snyder); univariate rule-based expert systems (1990s).<br>
                <strong>B. Overlap:</strong> Both identify common chromatographic faults such as leaks, bubbles, and column fouling.<br>
                <strong>C. Definitive Difference:</strong> SimuPharm models faults as continuous, physically coupled parameter perturbations across hydrodynamic, kinetic, 
                and optical domains simultaneously, applying Bayesian inversion to resolve symptom degeneracy (e.g. distinguishing frit clogging from head voiding).<br>
                <strong>D. Novelty Status:</strong> <span class="badge badge-green">HIGH NOVELTY FRONTIER</span>.<br>
                <strong>E. Evidence Required:</strong> Cross-validation against experimental fault records (e.g., intentional bubble injection, physical frit fouling).
            </p>
        </div>

        <div class="card" style="margin-bottom: 12px;">
            <div class="card-title">Concept 3: Orthogonal Multi-Instrument False Discovery Rate Quantification</div>
            <p class="card-text">
                <strong>A. Prior Art:</strong> Single-instrument database search algorithms (NIST MS search, FTIR correlation tables).<br>
                <strong>B. Overlap:</strong> Both score spectral and chromatographic matches against reference databases.<br>
                <strong>C. Definitive Difference:</strong> SimuPharm mathematically quantifies the joint orthogonal probability of misidentification across five coupled 
                analytical dimensions (UV-Vis + FTIR + HPLC + GC + MS) under varying noise regimes.<br>
                <strong>D. Novelty Status:</strong> <span class="badge badge-green">MODERATE-TO-HIGH CHEMOMETRIC NOVELTY</span>.<br>
                <strong>E. Evidence Required:</strong> Monte Carlo simulation across SimuPharm's 21-compound database with synthetic chemical decoys.
            </p>
        </div>
    </div>

    <!-- SECTION 20: EDUCATIONAL PUBLICATION ROUTE ASSESSMENT -->
    <div class="page">
        <h2 class="section-title">20. EDUCATIONAL PUBLICATION ROUTE ASSESSMENT</h2>
        
        <p class="body-text">
            While SimuPharm is capable of pure computational chemistry research, its browser interface and fault-injection architecture 
            were originally conceived with educational utility in mind. 
            This section assesses the <strong>Chemical & Pharmaceutical Education publication route</strong> with complete objectivity.
        </p>

        <h3 class="subsection-title">20.1 Primary Educational Target Venues</h3>
        <div class="grid-2">
            <div class="card">
                <div class="card-title">Journal of Chemical Education (ACS)</div>
                <p class="card-text">
                    <strong>Impact Factor:</strong> ~3.2 | <strong>Article Type:</strong> Chemical Education Research (CER) or Technology Report.<br>
                    <strong>Acceptance Criteria:</strong> High pedagogical rigor. Rejects simple "we built a software tool" papers. Requires measurable evidence of student learning gains 
                    (normalized gain $g$, paired $t$-test / Wilcoxon), validated assessment instruments, and clear integration into undergraduate chemistry curricula.
                </p>
            </div>
            <div class="card">
                <div class="card-title">Currents in Pharmacy Teaching & Learning (Elsevier)</div>
                <p class="card-text">
                    <strong>Impact Factor:</strong> ~1.8 | <strong>Article Type:</strong> Research Article or Instructional Design Note.<br>
                    <strong>Acceptance Criteria:</strong> Directly values pharmacy curriculum relevance (e.g., pharmacopeial quality control, USP compliance). 
                    More receptive to usability evaluations (SUS) and small-cohort exploratory pilots ($N=20–30$).
                </p>
            </div>
        </div>

        <h3 class="subsection-title">20.2 The Human-Participant Bottleneck</h3>
        <div class="callout callout-warning">
            <strong>CRITICAL GOVERNANCE CONSTRAINT:</strong> In Phase 4.2.3, the educational pilot was audited and frozen:
            <span class="badge badge-red">NO-GO — INSTITUTIONAL ETHICS AUTHORIZATION PENDING</span>. 
            No human data can be collected until formal institutional IRB/IEC approval is granted. 
            Publishing in JCE or CPTL <em>without real human participants</em> is impossible. 
            Therefore, <strong>the educational route must NOT be the sole or primary publication strategy</strong>. 
            SimuPharm must pursue computational, chemometric, and methods routes that operate independently of human recruitment.
        </div>
    </div>

    <!-- SECTION 21: EXPERIMENTAL VALIDATION OPTIONS (LEVELS 0 TO 4) -->
    <div class="page">
        <h2 class="section-title">21. EXPERIMENTAL VALIDATION OPTIONS (LEVELS 0 TO 4)</h2>
        
        <p class="body-text">
            A major strategic question in computational research is determining the <strong>Minimum Information Principle</strong>: 
            <em>What is the smallest physical laboratory investment that maximizes peer-reviewed scientific credibility?</em> 
            We define five discrete experimental tiers:
        </p>

        <table class="data-table">
            <thead>
                <tr>
                    <th>Experimental Level</th>
                    <th>Required Laboratory Infrastructure & Materials</th>
                    <th>Financial Cost</th>
                    <th>Time to Execute</th>
                    <th>Scientific Information Gained</th>
                    <th>Target Journal Ceiling</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>LEVEL 0: Pure Computational / Theoretical</strong></td>
                    <td>Zero physical laboratory work. Uses mathematical derivations, Sobol GSA, MCMC sampling, and synthetic noise benchmarks.</td>
                    <td><strong>$0</strong></td>
                    <td>1–3 weeks</td>
                    <td>Defines theoretical bounds, algorithmic convergence, and sensitivity architecture.</td>
                    <td><em>Comput. Chem. Eng.</em><br><em>SoftwareX</em><br>(IF: 2.8 – 4.3)</td>
                </tr>
                <tr>
                    <td><strong>LEVEL 1: Public Experimental Datasets</strong></td>
                    <td>Zero physical lab work. Uses open repositories: METLIN SMRT (80,000 runs), NIST SRM 870, Tanaka 250-column database.</td>
                    <td><strong>$0</strong></td>
                    <td>2–4 weeks</td>
                    <td>Proves real-world predictive validity against independent, gold-standard physical measurements with zero data leakage.</td>
                    <td><em>Anal. Chim. Acta</em><br><em>J. Chem. Inf. Model.</em><br>(IF: 5.6 – 6.0)</td>
                </tr>
                <tr>
                    <td><strong>LEVEL 2: Small Targeted Bench Experiment</strong></td>
                    <td>Standard HPLC-UV unit. 1 column (C18), 3 standard pharmaceutical compounds (Paracetamol, Aspirin, Caffeine). Exactly <strong>12 injections</strong> (4 isocratic, 2 gradients, 3 flow rates, 3 fault injections).</td>
                    <td><strong>~$300 – $800</strong><br>(Solvents, standards, column time)</td>
                    <td>2–3 days</td>
                    <td>Provides direct, undisputed laboratory verification of SimuPharm's specific retention and fault equations; silences skeptical reviewers.</td>
                    <td><em>J. Chromatogr. A</em><br><em>Talanta</em><br>(IF: 4.6 – 6.1)</td>
                </tr>
                <tr>
                    <td><strong>LEVEL 3: Moderate Multi-Instrument Validation</strong></td>
                    <td>HPLC + UV-Vis + FTIR. Testing 10 pharmaceutical APIs across varying mobile phases, temperatures, and spectral concentrations.</td>
                    <td>~$2,500 – $5,000</td>
                    <td>2–4 weeks</td>
                    <td>Full multi-modal orthogonal validation of the compound database and matching engine.</td>
                    <td><em>Analytical Chemistry</em><br>(IF: 7.4)</td>
                </tr>
                <tr>
                    <td><strong>LEVEL 4: Full Empirical Research Campaign</strong></td>
                    <td>HPLC, GC-MS, LC-MS/MS, FTIR, Polarimeter. Extensive design-of-experiments (DoE) with forced degradation and formal validation.</td>
                    <td>$15,000+</td>
                    <td>3–6 months</td>
                    <td>Exhaustive industrial qualification; unnecessary for academic proof-of-concept.</td>
                    <td><em>Analytical Chemistry</em><br>(Diminishing ROI)</td>
                </tr>
            </tbody>
        </table>

        <div class="callout callout-discovery">
            <strong>THE SWEET SPOT:</strong> <strong>Level 1 (Public Datasets)</strong> delivers the absolute highest <em>information-to-effort ratio</em>, 
            unlocking Q1 journals (*Analytica Chimica Acta*) at zero financial cost. 
            If laboratory access becomes available, <strong>Level 2 (a 12-injection micro-campaign)</strong> provides definitive physical verification 
            in under 72 hours.
        </div>
    </div>

    <!-- SECTION 22: ACADEMIC JOURNAL LANDSCAPE & TARGET MAPPING -->
    <div class="page">
        <h2 class="section-title">22. ACADEMIC JOURNAL LANDSCAPE & TARGET MAPPING</h2>
        
        <p class="body-text">
            SimuPharm must not be submitted blindly. Each academic journal possesses specific editorial priorities, reviewer expectations, 
            and evidence thresholds. Ten premier journals across four sectors were comprehensively mapped.
        </p>

        <h3 class="subsection-title">22.1 Comprehensive Journal Target Matrix</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Journal Name & Publisher</th>
                    <th>Impact Factor</th>
                    <th>Primary Scope & Editorial Stance</th>
                    <th>Typical Review Cycle</th>
                    <th>Minimum Evidence Expectation</th>
                    <th>SimuPharm Fit & Best Direction</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Analytica Chimica Acta</strong><br>(Elsevier)</td>
                    <td><strong>6.0</strong></td>
                    <td>Fundamental and applied analytical chemistry, chemometrics, novel computational methods.</td>
                    <td>4–6 weeks</td>
                    <td>Rigorous methodological validation against real experimental data; clear analytical significance.</td>
                    <td><span class="badge badge-green">EXCELLENT FIT</span><br>Direction: Sobol GSA / Robustness Optimization</td>
                </tr>
                <tr>
                    <td><strong>Journal of Chromatography A</strong><br>(Elsevier)</td>
                    <td><strong>4.6</strong></td>
                    <td>The premier journal dedicated exclusively to chromatography and separation science.</td>
                    <td>5–8 weeks</td>
                    <td>Extremely strict chromatographic reviewers; requires verified retention physics (LSS / Neue-Kuss).</td>
                    <td><span class="badge badge-green">EXCELLENT FIT</span><br>Direction: Inverse Parameter Estimation / SMRT Blind Prediction</td>
                </tr>
                <tr>
                    <td><strong>Analytical Chemistry</strong><br>(ACS)</td>
                    <td><strong>7.4</strong></td>
                    <td>Flagship journal of analytical chemistry; highly selective (~25% acceptance).</td>
                    <td>3–5 weeks</td>
                    <td>Requires transformative analytical novelty or paradigm-shifting methodology. Rejects incremental simulations.</td>
                    <td><span class="badge badge-yellow">CHALLENGING</span><br>Direction: Inverse Fault Deconvolution (State C only)</td>
                </tr>
                <tr>
                    <td><strong>Computers & Chemical Engineering</strong><br>(Elsevier)</td>
                    <td><strong>4.3</strong></td>
                    <td>Process systems engineering, mathematical modeling, numerical methods, sensitivity analysis.</td>
                    <td>6–10 weeks</td>
                    <td>Demands mathematical rigor, convergence proofs, sensitivity equations; chemistry is secondary.</td>
                    <td><span class="badge badge-green">EXCELLENT FIT</span><br>Direction: Sobol GSA / Multi-Objective Pareto Method Optimization</td>
                </tr>
                <tr>
                    <td><strong>Chemometrics & Intelligent Laboratory Systems</strong><br>(Elsevier)</td>
                    <td><strong>3.9</strong></td>
                    <td>Application of mathematical, statistical, and ML methods to analytical chemistry.</td>
                    <td>5–7 weeks</td>
                    <td>Requires formal chemometric modeling, cross-validation, and ROC/AUC false discovery analysis.</td>
                    <td><span class="badge badge-green">HIGH FIT</span><br>Direction: Multi-Instrument Orthogonal Identification Benchmark</td>
                </tr>
                <tr>
                    <td><strong>Journal of Chemical Information & Modeling (JCIM)</strong><br>(ACS)</td>
                    <td><strong>5.6</strong></td>
                    <td>Computational chemistry, cheminformatics, molecular modeling, AI in chemical sciences.</td>
                    <td>4–6 weeks</td>
                    <td>Requires reproducible software code, open data, and rigorous computational benchmarking.</td>
                    <td><span class="badge badge-green">HIGH FIT</span><br>Direction: Autonomous Analytical Lab Agent / Knowledge Graph</td>
                </tr>
                <tr>
                    <td><strong>Journal of Pharmaceutical and Biomedical Analysis (JPBA)</strong><br>(Elsevier)</td>
                    <td><strong>3.4</strong></td>
                    <td>Pharmaceutical QC, method validation, stability testing, pharmacopeial assays.</td>
                    <td>4–6 weeks</td>
                    <td>Values practical pharmaceutical utility, ICH compliance, and impurity quantification.</td>
                    <td><span class="badge badge-green">HIGH FIT</span><br>Direction: Virtual AQbD Method Transfer Between Laboratories</td>
                </tr>
                <tr>
                    <td><strong>SoftwareX</strong><br>(Elsevier)</td>
                    <td><strong>2.8</strong></td>
                    <td>Peer-reviewed scientific software impact, open-source architectures, code reproducibility.</td>
                    <td>3–5 weeks</td>
                    <td>Requires working code repository, open license, verified installation, and clean architecture description.</td>
                    <td><span class="badge badge-green">IMMEDIATE FIT</span><br>Direction: SimuPharm Full-Stack Architecture Paper</td>
                </tr>
                <tr>
                    <td><strong>Journal of Chemical Education (JCE)</strong><br>(ACS)</td>
                    <td><strong>3.2</strong></td>
                    <td>Chemical education research, instructional laboratory tools, technology reports.</td>
                    <td>6–12 weeks</td>
                    <td>Requires formal human participant data ($N \\ge 25$), IRB approval, learning gain statistics.</td>
                    <td><span class="badge badge-yellow">ETHICS BLOCKED</span><br>Direction: Phase 4 Educational Pilot (On Hold)</td>
                </tr>
                <tr>
                    <td><strong>Talanta</strong><br>(Elsevier)</td>
                    <td><strong>6.1</strong></td>
                    <td>Pure and applied analytical chemistry, sensor technologies, automated analytical systems.</td>
                    <td>4–6 weeks</td>
                    <td>Values novel analytical devices, automation algorithms, and rapid testing workflows.</td>
                    <td><span class="badge badge-green">HIGH FIT</span><br>Direction: Diagnostic Fault Inversion for Automated PAT</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 23: PUBLICATION SCORECARD -->
    <div class="page">
        <h2 class="section-title">23. PUBLICATION SCORECARD (15+ CANDIDATE DIRECTIONS)</h2>
        
        <p class="body-text">
            To make an objective, quantitative decision, <strong>sixteen distinct research directions</strong> were evaluated across nine criteria, 
            scored on a scale from 1 (poor / severe barrier) to 10 (exceptional / highly favorable).
        </p>

        <h3 class="subsection-title">23.1 Scoring Rubric & Master Scorecard Table</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 20%;">Candidate Research Direction</th>
                    <th>Nov. (10)</th>
                    <th>Sci. Imp. (10)</th>
                    <th>Evid. Avail. (10)</th>
                    <th>Valid. Feas. (10)</th>
                    <th>Impl. Ease (10)</th>
                    <th>Pub. Ceil. (10)</th>
                    <th>Low Cost (10)</th>
                    <th>Fast Time (10)</th>
                    <th>Total Score (90)</th>
                    <th>Action Class</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>D1: Sobol Global Sensitivity & AQbD Robustness</strong></td>
                    <td>8</td>
                    <td>9</td>
                    <td>9</td>
                    <td>9</td>
                    <td>8</td>
                    <td>8</td>
                    <td>10</td>
                    <td>9</td>
                    <td><strong>78</strong></td>
                    <td><span class="badge badge-green">GREEN (TOP 1)</span></td>
                </tr>
                <tr>
                    <td><strong>D2: Multi-Instrument Orthogonal QC Benchmark</strong></td>
                    <td>8</td>
                    <td>8</td>
                    <td>9</td>
                    <td>9</td>
                    <td>8</td>
                    <td>8</td>
                    <td>10</td>
                    <td>8</td>
                    <td><strong>76</strong></td>
                    <td><span class="badge badge-green">GREEN (TOP 2)</span></td>
                </tr>
                <tr>
                    <td><strong>D3: SMRT Blind Prediction & LSS Retention Engine</strong></td>
                    <td>7</td>
                    <td>8</td>
                    <td>10</td>
                    <td>9</td>
                    <td>7</td>
                    <td>8</td>
                    <td>10</td>
                    <td>8</td>
                    <td><strong>74</strong></td>
                    <td><span class="badge badge-green">GREEN (TOP 3)</span></td>
                </tr>
                <tr>
                    <td><strong>D4: Inverse Bayesian Parameter Estimation (MCMC)</strong></td>
                    <td>8</td>
                    <td>8</td>
                    <td>8</td>
                    <td>8</td>
                    <td>7</td>
                    <td>8</td>
                    <td>10</td>
                    <td>7</td>
                    <td><strong>72</strong></td>
                    <td><span class="badge badge-green">GREEN (TOP 4)</span></td>
                </tr>
                <tr>
                    <td><strong>D5: Diagnostic Fault-Signature Inversion Engine</strong></td>
                    <td>9</td>
                    <td>9</td>
                    <td>7</td>
                    <td>7</td>
                    <td>6</td>
                    <td>9</td>
                    <td>9</td>
                    <td>6</td>
                    <td><strong>72</strong></td>
                    <td><span class="badge badge-green">GREEN (TOP 5)</span></td>
                </tr>
                <tr>
                    <td><strong>D6: Open-Source SoftwareX Platform Paper</strong></td>
                    <td>4</td>
                    <td>6</td>
                    <td>10</td>
                    <td>10</td>
                    <td>10</td>
                    <td>5</td>
                    <td>10</td>
                    <td>10</td>
                    <td><strong>71</strong></td>
                    <td><span class="badge badge-green">GREEN (IMMEDIATE)</span></td>
                </tr>
                <tr>
                    <td><strong>D7: Autonomous Lab Agent & Knowledge Graph (LLM)</strong></td>
                    <td>9</td>
                    <td>8</td>
                    <td>6</td>
                    <td>6</td>
                    <td>5</td>
                    <td>9</td>
                    <td>9</td>
                    <td>5</td>
                    <td><strong>63</strong></td>
                    <td><span class="badge badge-yellow">YELLOW</span></td>
                </tr>
                <tr>
                    <td><strong>D8: Synthetic Chromatographic Benchmark Generator</strong></td>
                    <td>7</td>
                    <td>7</td>
                    <td>8</td>
                    <td>8</td>
                    <td>7</td>
                    <td>7</td>
                    <td>10</td>
                    <td>7</td>
                    <td><strong>69</strong></td>
                    <td><span class="badge badge-green">GREEN</span></td>
                </tr>
                <tr>
                    <td><strong>D9: Pareto Multi-Objective Method Optimization</strong></td>
                    <td>7</td>
                    <td>8</td>
                    <td>8</td>
                    <td>8</td>
                    <td>7</td>
                    <td>7</td>
                    <td>10</td>
                    <td>7</td>
                    <td><strong>70</strong></td>
                    <td><span class="badge badge-green">GREEN</span></td>
                </tr>
                <tr>
                    <td><strong>D10: Educational Evaluation Pilot (JCE)</strong></td>
                    <td>5</td>
                    <td>6</td>
                    <td>3</td>
                    <td>4</td>
                    <td>6</td>
                    <td>6</td>
                    <td>8</td>
                    <td>4</td>
                    <td><strong>48</strong></td>
                    <td><span class="badge badge-yellow">YELLOW (IRB BLOCKED)</span></td>
                </tr>
                <tr>
                    <td><strong>D11: Comparative Multi-Simulator Benchmark Study</strong></td>
                    <td>6</td>
                    <td>6</td>
                    <td>8</td>
                    <td>8</td>
                    <td>8</td>
                    <td>5</td>
                    <td>10</td>
                    <td>8</td>
                    <td><strong>65</strong></td>
                    <td><span class="badge badge-yellow">YELLOW</span></td>
                </tr>
                <tr>
                    <td><strong>D12: Level 2 Experimental Bench Validation (12 Injections)</strong></td>
                    <td>7</td>
                    <td>9</td>
                    <td>9</td>
                    <td>8</td>
                    <td>5</td>
                    <td>8</td>
                    <td>7</td>
                    <td>6</td>
                    <td><strong>66</strong></td>
                    <td><span class="badge badge-yellow">YELLOW (LAB PENDING)</span></td>
                </tr>
                <tr>
                    <td><strong>D13: Level 4 Full Physical Campaign (100+ Runs)</strong></td>
                    <td>6</td>
                    <td>8</td>
                    <td>8</td>
                    <td>5</td>
                    <td>2</td>
                    <td>9</td>
                    <td>2</td>
                    <td>2</td>
                    <td><strong>48</strong></td>
                    <td><span class="badge badge-red">RED (POOR ROI)</span></td>
                </tr>
                <tr>
                    <td><strong>D14: Pure 3D VR Visual Laboratory (WebGL/Metaverse)</strong></td>
                    <td>5</td>
                    <td>3</td>
                    <td>4</td>
                    <td>4</td>
                    <td>4</td>
                    <td>3</td>
                    <td>8</td>
                    <td>4</td>
                    <td><strong>38</strong></td>
                    <td><span class="badge badge-red">RED (UNPUBLISHABLE)</span></td>
                </tr>
                <tr>
                    <td><strong>D15: Direct Unmodified Science Paper (State A as Novel)</strong></td>
                    <td>1</td>
                    <td>2</td>
                    <td>8</td>
                    <td>8</td>
                    <td>10</td>
                    <td>2</td>
                    <td>10</td>
                    <td>10</td>
                    <td><strong>52</strong></td>
                    <td><span class="badge badge-red">RED (DESK REJECT)</span></td>
                </tr>
                <tr>
                    <td><strong>D16: Single-Instrument GC Boiling Point Paper</strong></td>
                    <td>2</td>
                    <td>3</td>
                    <td>6</td>
                    <td>6</td>
                    <td>9</td>
                    <td>2</td>
                    <td>10</td>
                    <td>9</td>
                    <td><strong>49</strong></td>
                    <td><span class="badge badge-red">RED (HEURISTIC)</span></td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 24: TOP 5 SMART MODIFICATIONS: DEEP ARCHITECTURE BLUEPRINTS -->
    <div class="page">
        <h2 class="section-title">24. TOP 5 SMART MODIFICATIONS: DEEP ARCHITECTURE BLUEPRINTS</h2>
        
        <p class="body-text">
            Based on the quantitative scorecard, the <strong>Top 5 Smart Modifications</strong> were selected. 
            Each modification represents a high-efficiency computational advancement that transforms SimuPharm into a publication-grade scientific tool. 
            Below are their detailed architectural blueprints.
        </p>

        <h3 class="subsection-title">24.1 Blueprint 1: Global Sensitivity Analysis & Robustness Quantification (Sobol Engine)</h3>
        <div class="card" style="margin-bottom: 12px;">
            <p class="card-text">
                <strong>CURRENT STATE:</strong> SimuPharm evaluates retention deterministically for single parameter sets. 
                Robustness is tested manually by sliding GUI bars.<br>
                <strong>PROBLEM:</strong> Regulated pharma (ICH Q14) requires proving method robustness across multi-dimensional spaces. 
                Manual testing cannot capture parameter interactions or quantify variance contributions.<br>
                <strong>MODIFICATION:</strong> Integrate a Python module (<span class="code-span">salib_sobol.py</span>) that samples $N=10,000$ Saltelli quasirandom parameter sets 
                across 6 operational variables ($\phi, T, F, d_p, L, V_{\text{inj}}$) and computes first-order ($S_i$) and total-effect ($S_{Ti}$) Sobol indices.<br>
                <strong>SCIENTIFIC HYPOTHESIS:</strong> Parameter interactions between organic modifier proportioning ($\phi$) and column temperature ($T$) 
                account for over 30% of total critical pair resolution variance near the edge of the design space.<br>
                <strong>NOVELTY HYPOTHESIS:</strong> First open-source application of variance-based global sensitivity analysis to pharmaceutical separation design spaces.<br>
                <strong>IMPLEMENTATION EFFORT:</strong> <span class="badge badge-green">LOW (1–2 WEEKS)</span>. Pure Python utilizing <span class="code-span">SALib</span> and existing <span class="code-span">backend/science/hplc.py</span>.<br>
                <strong>VALIDATION PLAN:</strong> Compare Sobol indices against an experimental 4-compound mixture (Paracetamol, Aspirin, Caffeine, Ibuprofen).<br>
                <strong>TARGET PUBLICATION:</strong> <em>Computers & Chemical Engineering</em> or <em>Analytica Chimica Acta</em>.<br>
                <strong>KILL CRITERION:</strong> If higher-order interaction variance is negligible ($S_{Ti} - S_i &lt; 0.02$ across all parameters), 
                proving that standard linear OFAT robustness testing is completely sufficient.
            </p>
        </div>

        <h3 class="subsection-title">24.2 Blueprint 2: Multi-Instrument Orthogonal Compound Identification Benchmark</h3>
        <div class="card" style="margin-bottom: 12px;">
            <p class="card-text">
                <strong>CURRENT STATE:</strong> <span class="code-span">backend/analytics/ml_analyzer.py</span> calculates separate cosine scores for UV and peak position scores for FTIR.<br>
                <strong>PROBLEM:</strong> Matching algorithms lack a statistical framework to calculate compound identification confidence and false-positive bounds across orthogonal dimensions.<br>
                <strong>MODIFICATION:</strong> Build an integrated probabilistic classifier that combines UV-Vis spectral distance, FTIR functional group matches, 
                HPLC retention factor $k'$, GC boiling point, and MS isotopic distribution into a unified Bayesian posterior probability score.<br>
                <strong>SCIENTIFIC HYPOTHESIS:</strong> Adding orthogonal chromatographic retention ($t_R$) to a 2-peak UV spectrum reduces the false-positive 
                identification rate by $&gt;90\\%$ in a 1,000-compound decoy database.<br>
                <strong>NOVELTY HYPOTHESIS:</strong> Provides a rigorous open benchmark quantifying the exact mathematical value of analytical orthogonality.<br>
                <strong>IMPLEMENTATION EFFORT:</strong> <span class="badge badge-green">LOW (2 WEEKS)</span>. Builds directly upon the existing 21-compound multi-modal database.<br>
                <strong>VALIDATION PLAN:</strong> Cross-validation using MassBank and open UV databases with 500 in silico decoy compounds.<br>
                <strong>TARGET PUBLICATION:</strong> <em>Chemometrics and Intelligent Laboratory Systems</em> or <em>Talanta</em>.<br>
                <strong>KILL CRITERION:</strong> If spectral overlap alone in UV/IR already yields $&gt;99.9\\%$ unique identification, rendering orthogonal coupling redundant.
            </p>
        </div>

        <h3 class="subsection-title">24.3 Blueprint 3: Physics-Informed Retention Engine Benchmarked on METLIN SMRT</h3>
        <div class="card" style="margin-bottom: 12px;">
            <p class="card-text">
                <strong>CURRENT STATE:</strong> Backend HPLC retention uses a linear modifier approximation ($k' = k'_0 (100 - \\%B)/40$).<br>
                <strong>PROBLEM:</strong> Linear retention fails catastrophically across broad gradients and cannot accurately reproduce real reversed-phase chromatography.<br>
                <strong>MODIFICATION:</strong> Replace heuristic retention with Snyder's Linear Solvent Strength (LSS) model: $\\ln k = \\ln k_w - S\\phi$, 
                integrated via numerical ODE solver ($dt_R / dz = u(z) / (1 + k(z))$) for arbitrary non-linear gradient profiles.<br>
                <strong>SCIENTIFIC HYPOTHESIS:</strong> A 2-parameter LSS numerical engine achieves $RMSE &lt; 0.12$ min across a blind test set of 1,000 small molecules from the METLIN SMRT dataset.<br>
                <strong>NOVELTY HYPOTHESIS:</strong> High-speed client-side WebAssembly / Python implementation achieving sub-millisecond gradient simulation with zero data leakage.<br>
                <strong>IMPLEMENTATION EFFORT:</strong> <span class="badge badge-yellow">MEDIUM (2–3 WEEKS)</span>. Requires numerical Runge-Kutta gradient integration.<br>
                <strong>VALIDATION PLAN:</strong> Blind prediction against the public 80,000-molecule METLIN SMRT dataset.<br>
                <strong>TARGET PUBLICATION:</strong> <em>Journal of Chromatography A</em>.<br>
                <strong>KILL CRITERION:</strong> If prediction error on unseen gradients exceeds $RMSE &gt; 0.5$ min due to non-linear modifier deviations.
            </p>
        </div>

        <h3 class="subsection-title">24.4 Blueprint 4: Bayesian Inverse Parameter Estimation Engine (MCMC)</h3>
        <div class="card" style="margin-bottom: 12px;">
            <p class="card-text">
                <strong>CURRENT STATE:</strong> Parameters must be manually specified by the user.<br>
                <strong>PROBLEM:</strong> Analysts possess only experimental retention times from two scouting runs and must deduce underlying solute parameters.<br>
                <strong>MODIFICATION:</strong> Implement an inverse Bayesian MCMC solver (<span class="code-span">emcee</span>) that takes $M=2$ experimental chromatograms 
                and outputs full posterior probability distributions for $\\ln k_w$, $S$, and column dead volume $V_0$.<br>
                <strong>SCIENTIFIC HYPOTHESIS:</strong> Two scouting runs are sufficient to constrain the 95% Bayesian credible interval of predicted future gradient retention to within $\\pm 6$ seconds.<br>
                <strong>NOVELTY HYPOTHESIS:</strong> Open-source, probabilistic alternative to DryLab's deterministic least-squares parameter fitting.<br>
                <strong>IMPLEMENTATION EFFORT:</strong> <span class="badge badge-yellow">MEDIUM (2–3 WEEKS)</span>.<br>
                <strong>VALIDATION PLAN:</strong> Benchmarked against published experimental gradient retention times (Snyder & Dolan literature datasets).<br>
                <strong>TARGET PUBLICATION:</strong> <em>Journal of Chromatography A</em> or <em>Analytica Chimica Acta</em>.<br>
                <strong>KILL CRITERION:</strong> If parameter correlation between $\\ln k_w$ and $S$ creates severe unidentifiability that widens prediction intervals beyond analytical utility.
            </p>
        </div>

        <h3 class="subsection-title">24.5 Blueprint 5: Probabilistic Diagnostic Fault Inversion for Self-Diagnosing PAT</h3>
        <div class="card" style="margin-bottom: 12px;">
            <p class="card-text">
                <strong>CURRENT STATE:</strong> SimuPharm injects faults forward into the simulation as user-triggered modes.<br>
                <strong>PROBLEM:</strong> In physical operations, faults are unknown; the analyst observes only corrupted data and must infer the mechanical root cause.<br>
                <strong>MODIFICATION:</strong> Invert the fault model using a multi-class random forest and Bayesian diagnostic matrix that maps observed chromatographic 
                perturbations ($\\Delta P, \\sigma_{\\Delta P}, \\Delta T_{\\text{tailing}}, \\Delta N, \\Delta t_R$) back to physical fault probabilities.<br>
                <strong>SCIENTIFIC HYPOTHESIS:</strong> Coupled pressure-retention-peak shape feature vectors can uniquely distinguish column inlet frit blockage 
                from column head voids with $&gt;95\\%$ diagnostic accuracy.<br>
                <strong>NOVELTY HYPOTHESIS:</strong> The first quantitative, physics-grounded diagnostic classifier for automated liquid chromatography troubleshooting.<br>
                <strong>IMPLEMENTATION EFFORT:</strong> <span class="badge badge-yellow">MEDIUM (3–4 WEEKS)</span>.<br>
                <strong>VALIDATION PLAN:</strong> Tested against historical Zenodo chromatography troubleshooting datasets and synthetic noisy runs.<br>
                <strong>TARGET PUBLICATION:</strong> <em>Analytical Chemistry</em> (ACS) or <em>Talanta</em>.<br>
                <strong>KILL CRITERION:</strong> If severe symptom degeneracy causes classification accuracy to drop below 70% in the presence of realistic instrument noise.
            </p>
        </div>
    </div>
    """

if __name__ == "__main__":
    print("Part 3 module loaded successfully. HTML length:", len(get_part3_html()))
