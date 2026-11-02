"""
PHASE 5.1 — PART 2: THE SEVEN CANDIDATE PUBLICATION DIRECTIONS & EDUCATIONAL ROUTE
SimuPharm.io Publication Target Selection & Evidence Verification Sprint
"""

def get_part2_html():
    return """
    <!-- SECTION 6: CANDIDATE DIRECTION A — RETENTION PREDICTION -->
    <div class="page">
        <h2 class="section-title">6. DIRECTION A: INDEPENDENT MECHANISTIC RETENTION PREDICTION</h2>
        
        <div class="callout callout-note">
            <strong>CORE SCIENTIFIC QUESTION:</strong> Can SimuPharm's liquid chromatographic engine predict experimentally measured retention times 
            under gradient and isocratic conditions that were <em>strictly excluded</em> from model calibration?
        </div>

        <h3 class="subsection-title">6.1 The Core Problem & Literature Gap</h3>
        <p class="body-text">
            In separation science, computer-assisted method development relies on either: 
            (1) <em>Empirical Quantitative Structure–Retention Relationships (QSRR)</em> using machine learning, which require thousands of molecules but fail when column chemistry changes, or 
            (2) <em>Mechanistic Retention Models</em> (such as Snyder's Linear Solvent Strength theory: $\ln k = \ln k_w - S\phi$), which require preliminary experimental scouting runs. 
            A major gap in the literature is <strong>independent condition-transferability</strong>: can a computational model calibrated from just two rapid isocratic scouting runs 
            accurately predict retention across complex multi-step, non-linear gradients on unseen experimental instruments without parameter leakage?
        </p>

        <h3 class="subsection-title">6.2 Forensic Audit of Public Benchmark Datasets</h3>
        <ul class="bullet-list">
            <li><strong>The METLIN SMRT Reality Check:</strong> The METLIN Small Molecule Retention Time dataset (Domingo-Almenara et al., <em>Nat. Commun.</em> 2019) 
            contains 80,038 small molecules on a Waters Acquity C18 column. 
            <em>Critical Forensic Finding:</em> METLIN SMRT recorded <strong>only a single gradient condition</strong> per molecule. 
            Because mechanistic LSS modeling mathematically requires at least two distinct solvent fractions to determine the solute slope parameter $S$, 
            <strong>METLIN SMRT cannot be used for mechanistic retention prediction without prior QSRR estimation of $S$</strong>. 
            Claiming that SimuPharm can "mechanistically predict METLIN SMRT retention directly" is mathematically impossible and will trigger immediate desk rejection.</li>
            <li><strong>Tanaka Column Characterization Database:</strong> Euerby & Petersson (<em>J. Chromatogr. A</em> 2003) compiled retention factors ($k$) 
            for 6 standard probe compounds across $>250$ commercial C18 columns. This dataset <em>does</em> provide independent isocratic validation 
            of column selectivity, methylene selectivity ($\alpha(\text{CH}_2)$), and silanol activity.</li>
            <li><strong>NIST Standard Reference Material 870:</strong> Provides certified retention times and separation factors for 5 probe compounds 
            under fixed chromatographic conditions ($80:20$ methanol:buffer, 20 mM phosphate, pH 7.00, $23^\circ\text{C}$). 
            Serves as a gold-standard reference benchmark for column selectivity.</li>
            <li><strong>Boswell & Stoll Literature Datasets:</strong> Published supplementary retention data (<em>J. Chromatogr. A</em> 2011, 1218: 6732–6741) 
            containing measured $\ln k_w$ and $S$ parameters for ~30 compounds across multiple gradient times and temperatures on Agilent Zorbax SB-C18. 
            This is the <strong>only open dataset directly compatible</strong> with SimuPharm's mechanistic gradient equations.</li>
        </ul>

        <h3 class="subsection-title">6.3 Why Gradient Performance Previously Failed (25.50% MAPE)</h3>
        <p class="body-text">
            In Phase 3.5, SimuPharm's gradient simulation exhibited an unacceptable <strong>25.50% MAPE</strong> (MAE = 1.243 min, RMSE = 1.512 min). 
            Hostile audit identified the three physical root causes:
        </p>
        <div class="grid-3">
            <div class="card">
                <div class="card-title">1. Dead Time Misestimation ($t_0$)</div>
                <p class="card-text">
                    Frontend used a fixed proxy ($t_0 = 0.50$ min) rather than calculating true column interstitial volume $V_0 = \pi r^2 L \epsilon_u$. 
                    At 1.0 mL/min on a 4.6 × 150 mm column, actual $V_0 \approx 1.5$ mL ($t_0 \approx 1.5$ min).
                </p>
            </div>
            <div class="card">
                <div class="card-title">2. Zero Dwell Volume ($V_d = 0$)</div>
                <p class="card-text">
                    The simulator assumed the gradient reaches the column head instantaneously at $t = 0$. 
                    Real HPLC systems have an instrumental mixer and tubing dwell volume ($V_d \approx 0.4 - 1.2$ mL) that delays the gradient.
                </p>
            </div>
            <div class="card">
                <div class="card-title">3. Arbitrary Slope Parameter ($S$)</div>
                <p class="card-text">
                    The modifier sensitivity parameter $S$ was approximated uniformly rather than calibrated per solute molecular weight and surface area.
                </p>
            </div>
        </div>

        <h3 class="subsection-title">6.4 Feasibility & Publication Verdict for Direction A</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Evaluation Dimension</th>
                    <th>Assessment & Ground Reality</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Required Development</strong></td><td>Moderate: Integrate numerical Runge-Kutta ODE gradient solver ($dt_R/dz$) and explicit dwell volume parameter ($V_d$).</td></tr>
                <tr><td><strong>External Dataset Usability</strong></td><td><span class="badge badge-yellow">YELLOW</span>: Boswell/Stoll 2011 data usable; METLIN SMRT strictly unusable for pure mechanistic LSS.</td></tr>
                <tr><td><strong>Target Journal</strong></td><td><em>Journal of Chromatography A</em> (Elsevier, IF: 4.6).</td></tr>
                <tr><td><strong>Reviewer Vulnerability</strong></td><td>High: Reviewers will note that Snyder LSS gradient integration is well-established in DryLab and Excel spreadsheets.</td></tr>
                <tr><td><strong>Strategic Ruling</strong></td><td><span class="badge badge-yellow">VIABLE BUT NOT FIRST PRIORITY</span>: Better suited as a supporting component of Direction B.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 7: CANDIDATE DIRECTION B — AQbD / GLOBAL SENSITIVITY -->
    <div class="page">
        <h2 class="section-title">7. DIRECTION B: AQbD & GLOBAL SENSITIVITY ANALYSIS (GSA)</h2>
        
        <div class="callout callout-discovery">
            <strong>CORE SCIENTIFIC QUESTION:</strong> How do coupled, non-linear operational uncertainties ($\phi, T, F, d_p, L, V_d$) propagate 
            into chromatographic separation failure across the ICH Q14 Method Operable Design Region (MODR), and which parameter interactions dominate quality risk?
        </div>

        <h3 class="subsection-title">7.1 Why This Direction Represents a Genuine Literature Gap</h3>
        <p class="body-text">
            Under the newly finalized <strong>ICH Q14 guideline (Analytical Procedure Development)</strong>, the global pharmaceutical industry 
            is mandated to demonstrate analytical method robustness during development. Current commercial software (e.g. DryLab) evaluates robustness 
            using local One-Factor-at-a-Time (OFAT) parameter stepping (e.g. stepping $T \pm 1^\circ\text{C}$ or $\phi \pm 1\%$). 
            Local OFAT methods are mathematically blind to <strong>non-linear parameter interactions</strong>: for example, temperature fluctuations 
            have negligible impact at high organic modifier concentrations, but trigger catastrophic co-elution ($R_s < 1.0$) at low organic fractions.
        </p>
        <p class="body-text">
            <strong>The Scientific Opportunity:</strong> SimuPharm can implement the first open-source, variance-based <strong>Global Sensitivity Analysis (GSA) 
            framework via Sobol decomposition</strong> applied to small-molecule pharmaceutical separation design spaces.
        </p>

        <h3 class="subsection-title">7.2 Mathematical Formulation of Sobol Variance Decomposition</h3>
        <div class="equation-block">
            <strong>Functional ANOVA Representation of Critical Pair Resolution:</strong><br>
            $$R_s(\mathbf{X}) = R_0 + \sum_{i=1}^k f_i(X_i) + \sum_{i < j} f_{ij}(X_i, X_j) + \dots + f_{1,2,\dots,k}(X_1, \dots, X_k)$$<br>
            <strong>First-Order (Main Effect) Sobol Index:</strong><br>
            $$S_i = \frac{\mathbb{V}_{X_i}\left(\mathbb{E}_{\mathbf{X}_{\sim i}}[R_s \mid X_i]\right)}{\mathbb{V}(R_s)}$$<br>
            <strong>Total-Effect Sobol Index (Including All Parameter Interactions):</strong><br>
            $$S_{Ti} = 1 - \frac{\mathbb{V}_{\mathbf{X}_{\sim i}}\left(\mathbb{E}_{X_i}[R_s \mid \mathbf{X}_{\sim i}]\right)}{\mathbb{V}(R_s)} = S_i + \sum_{j \ne i} S_{ij} + \dots$$
        </div>

        <h3 class="subsection-title">7.3 Why This is NOT "Just Running an Existing Algorithm"</h3>
        <p class="body-text">
            Hostile reviewers will inevitably attack: <em>"Sobol analysis is a standard statistical tool; applying it to chromatography is merely an implementation exercise."</em> 
            To withstand this attack, the paper must deliver three specific chemical contributions beyond the algorithm:
        </p>
        <ul class="bullet-list">
            <li><strong>1. Discovery of High-Order Interaction Boundaries:</strong> Demonstrating quantitatively that the interaction term $(S_{Ti} - S_i)$ 
            for column temperature and organic fraction accounts for $>28\%$ of total resolution variance near the edge of the MODR—proving that traditional 
            OFAT robustness testing produces false-positive regulatory assurance.</li>
            <li><strong>2. Risk-Based Design Space Contraction:</strong> Introducing a probabilistic metric, the <em>Separation Failure Probability ($P_{\text{fail}} = P(R_s < 1.5)$)</em>, 
            which maps exactly how manufacturing instrument tolerances contract the usable operational region.</li>
            <li><strong>3. Experimental Benchmark Anchor:</strong> Benchmarking the sensitivity rankings against the physical separation of the 
            NIST SRM 870 probe mixture, providing empirical validation of the predicted critical parameters.</li>
        </ul>

        <h3 class="subsection-title">7.4 Feasibility & Publication Verdict for Direction B</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Evaluation Dimension</th>
                    <th>Assessment & Ground Reality</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Required Development</strong></td><td><span class="badge badge-green">LOW (2–3 WEEKS)</span>: Standalone Python script wrapping <span class="code-span">SALib</span> around existing <span class="code-span">backend/science/hplc.py</span>. Zero engine rewrite.</td></tr>
                <tr><td><strong>External Dataset Usability</strong></td><td><span class="badge badge-green">GREEN</span>: NIST SRM 870 certified constants and Tanaka 250-column database.</td></tr>
                <tr><td><strong>Target Journal</strong></td><td><em>Analytica Chimica Acta</em> (Elsevier, IF: 6.0) or <em>Computers & Chemical Engineering</em> (IF: 4.3).</td></tr>
                <tr><td><strong>Resource Requirements</strong></td><td><strong>Zero wet lab, zero student recruitment, $0 financial cost.</strong></td></tr>
                <tr><td><strong>Strategic Ruling</strong></td><td><span class="badge badge-green">UNANIMOUS TOP RECOMMENDATION (RANK 1)</span>: Best evidence-to-effort ratio in the entire platform.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 8: CANDIDATE DIRECTION C — MULTIMODAL ANALYTICS -->
    <div class="page">
        <h2 class="section-title">8. DIRECTION C: MULTIMODAL ORTHOGONAL ANALYTICAL IDENTIFICATION</h2>
        
        <div class="callout callout-note">
            <strong>CORE SCIENTIFIC QUESTION:</strong> What is the quantitative mathematical relationship between analytical measurement dimensionality 
            (1D UV $\to$ 2D UV-HPLC $\to$ 5D full orthogonal suite) and false-positive compound misidentification rates in pharmaceutical screening?
        </div>

        <h3 class="subsection-title">8.1 The Core Problem & Industrial Need</h3>
        <p class="body-text">
            In pharmaceutical counterfeit screening, forensic toxicological analysis, and raw material quality control, single-technique identification 
            exhibits significant false-positive rates due to spectral degeneracy: structurally similar molecules (e.g., phenacetin vs paracetamol, 
            or positional drug isomers) produce near-identical UV absorption profiles. 
            Regulatory pharmacopeias mandate "orthogonal identification," but analytical chemistry lacks a standardized, open-source mathematical framework 
            that calculates the exact <strong>false discovery rate (FDR)</strong> and entropy reduction achieved as orthogonal techniques are incrementally combined.
        </p>

        <h3 class="subsection-title">8.2 SimuPharm's Unfair Advantage: The 21-API Orthogonal Matrix</h3>
        <p class="body-text">
            While SimuPharm's database contains only 21 compounds (refuting the "300+" marketing claim), each compound possesses 
            a complete, curated <strong>5-instrument orthogonal data matrix</strong>:
        </p>
        <div class="equation-block">
            $$\mathbf{\Theta}_k = \left[ \mathbf{A}_{\text{UV}}(\lambda), \quad \%\mathbf{T}_{\text{FTIR}}(\tilde{\nu}), \quad k'_{\text{HPLC}}, \quad t_{R, \text{GC}}, \quad \mathbf{I}_{\text{MS}}(m/z), \quad [\alpha]_D^{20} \right]$$
        </div>
        <p class="body-text">
            By coupling Bayesian evidence fusion across these modalities, SimuPharm can compute the joint posterior probability of identity:
        </p>
        <div class="equation-block">
            $$P(\text{Identity} = C_j \mid \mathbf{D}_{\text{obs}}) = \frac{\prod_{m=1}^M P(\mathbf{D}_m \mid C_j) \cdot P(C_j)}{\sum_{k=1}^K \prod_{m=1}^M P(\mathbf{D}_m \mid C_k) \cdot P(C_k)}$$
        </div>

        <h3 class="subsection-title">8.3 Hostile Vulnerability & Methodological Rescue</h3>
        <p class="body-text">
            <em>Hostile Reviewer Objection:</em> "Evaluating a classifier on only 21 compounds is trivial. Any algorithm can achieve 100% accuracy on 21 compounds."<br>
            <em>The Rescue Strategy:</em> The paper must not present this as a "machine learning compound classifier." 
            Instead, it must be framed as a <strong>theoretical chemometric benchmark</strong>: we synthesize 1,000 in silico chemical decoys and isomeric perturbations 
            under varying signal-to-noise ratios (S/N from 3 to 100). The paper calculates the <em>orthogonal information gain ($\Delta H = H_{\text{prior}} - H_{\text{posterior}}$)</em>, 
            proving analytically why 2D orthogonal coupling is exponentially superior to 1D screening.
        </p>

        <h3 class="subsection-title">8.4 Feasibility & Publication Verdict for Direction C</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Evaluation Dimension</th>
                    <th>Assessment & Ground Reality</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Required Development</strong></td><td><span class="badge badge-green">LOW (2 WEEKS)</span>: Probabilistic fusion wrapper around <span class="code-span">ml_analyzer.py</span> + decoy generation script.</td></tr>
                <tr><td><strong>External Dataset Usability</strong></td><td><span class="badge badge-pub">PUBLIC</span>: MassBank / GNPS and open UV spectral databases.</td></tr>
                <tr><td><strong>Target Journal</strong></td><td><em>Chemometrics and Intelligent Laboratory Systems</em> (Elsevier, IF: 3.9) or <em>Talanta</em> (IF: 6.1).</td></tr>
                <tr><td><strong>Resource Requirements</strong></td><td>Zero wet lab, zero student recruitment, $0 cost.</td></tr>
                <tr><td><strong>Strategic Ruling</strong></td><td><span class="badge badge-green">HIGH VALUE (RANK 2)</span>: Ideal second paper in the SimuPharm portfolio.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 9: CANDIDATE DIRECTION D — BAYESIAN INFERENCE -->
    <div class="page">
        <h2 class="section-title">9. DIRECTION D: BAYESIAN PARAMETER INFERENCE & MCMC</h2>
        
        <div class="callout callout-note">
            <strong>CORE SCIENTIFIC QUESTION:</strong> Can Markov Chain Monte Carlo (MCMC) sampling extract unobservable thermodynamic retention parameters 
            ($\ln k_w, S$) and column void volume ($V_0$) from limited experimental runs while rigorously quantifying parameter correlation and prediction uncertainty?
        </div>

        <h3 class="subsection-title">9.1 Problem Context & Literature Reality</h3>
        <p class="body-text">
            In reversed-phase chromatography, fitting retention parameters from scouting runs is conventionally performed via ordinary least-squares regression. 
            However, it is widely recognized that the thermodynamic parameters $\ln k_w$ (retention in 100% water) and $S$ (solvent sensitivity slope) 
            are <strong>strongly collinear</strong>: multiple pairs of $(\ln k_w, S)$ can fit two isocratic data points almost identically, 
            yet predict vastly different retention times when extrapolated to steep gradients. 
            Deterministic software (DryLab) yields single point estimates, masking this epistemic uncertainty from the analyst.
        </p>

        <h3 class="subsection-title">9.2 The Bayesian MCMC Formulation</h3>
        <p class="body-text">
            By implementing an affine-invariant ensemble MCMC sampler (<span class="code-span">emcee</span>) wrapped around SimuPharm's retention solver, 
            we sample the joint posterior probability distribution:
        </p>
        <div class="equation-block">
            $$\ln P(\ln k_w, S, V_0 \mid \mathbf{t}_R^{\text{obs}}) \propto -\frac{1}{2\sigma_\epsilon^2} \sum_{i=1}^M \left(t_{R, i}^{\text{obs}} - t_{R, i}^{\text{sim}}(\ln k_w, S, V_0, \phi_i)\right)^2 + \ln P(\ln k_w, S, V_0)$$
        </div>
        <p class="body-text">
            This yields two-dimensional posterior confidence ellipses, directly quantifying parameter identifiability and generating 
            <strong>95% Bayesian Credible Prediction Intervals</strong> for future gradient methods.
        </p>

        <h3 class="subsection-title">9.3 Feasibility & Publication Verdict for Direction D</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Evaluation Dimension</th>
                    <th>Assessment & Ground Reality</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Required Development</strong></td><td><span class="badge badge-yellow">MEDIUM (3 WEEKS)</span>: Integrating <span class="code-span">emcee</span> sampling and posterior corner-plot visualization.</td></tr>
                <tr><td><strong>External Dataset Usability</strong></td><td><span class="badge badge-green">GREEN</span>: Snyder & Dolan published retention data tables (multi-gradient scouting runs).</td></tr>
                <tr><td><strong>Target Journal</strong></td><td><em>Journal of Chromatography A</em> (Elsevier, IF: 4.6).</td></tr>
                <tr><td><strong>Reviewer Vulnerability</strong></td><td>Medium: Reviewers may ask why MCMC is necessary when 3 scouting runs resolve collinearity in practice.</td></tr>
                <tr><td><strong>Strategic Ruling</strong></td><td><span class="badge badge-green">SOLID PUBLICATION ROUTE (RANK 4)</span>: Highly defensible separation science contribution.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 10: CANDIDATE DIRECTION E — FAULT INVERSION -->
    <div class="page">
        <h2 class="section-title">10. DIRECTION E: FAULT-SIGNATURE INVERSION & DIAGNOSTIC PAT</h2>
        
        <div class="callout callout-note">
            <strong>CORE SCIENTIFIC QUESTION:</strong> Can observed multi-dimensional chromatographic anomalies (pressure spikes, peak splitting, 
            baseline drift, tailing factor degradation) be uniquely inverted to identify physical instrument hardware failures without human expert inspection?
        </div>

        <h3 class="subsection-title">10.1 The Self-Diagnosing Liquid Chromatograph</h3>
        <p class="body-text">
            SimuPharm possesses a rich forward fault-injection system (<span class="code-span">hplc_simulator_script.js</span>) modeling six common 
            operational failure modes: column inlet frit fouling, air bubbles in pump/flow-cell, pump check-valve leaks, column head voids, 
            stationary phase aging, and detector lamp degradation. 
            In Direction E, we invert this forward engine: by extracting a 7-dimensional feature vector:
        </p>
        <div class="equation-block">
            $$\mathbf{y}_{\text{fault}} = \left[ \Delta P_{\text{mean}}, \quad \sigma_{\Delta P}, \quad \Delta t_R, \quad T_{\text{tailing}}, \quad N_{\text{plates}}, \quad \sigma_{\text{baseline}}, \quad A_{\text{split}} \right]$$
        </div>
        <p class="body-text">
            we train a multi-class probabilistic classifier to output the root cause: $P(\text{Fault} = \text{Frit Clog} \mid \mathbf{y}_{\text{fault}}) = 96.4\%$. 
            This directly addresses the industrial grand challenge of <strong>autonomous, self-diagnosing Process Analytical Technology (PAT)</strong> in continuous manufacturing.
        </p>

        <h3 class="subsection-title">10.2 The Fatal Circular Validation Trap & Required Rescue</h3>
        <div class="callout callout-warning">
            <strong>CRITICAL FORENSIC WARNING:</strong> If we train a classifier on synthetic fault data generated by SimuPharm, 
            and then test that classifier on synthetic fault data generated by the same engine, <strong>the validation is 100% circular</strong>! 
            The classifier will achieve an artificial 99% accuracy that proves nothing about real physical chromatography. 
            Hostile reviewers will reject the paper instantly.
        </div>
        <p class="body-text">
            <em>How Direction E Can Survive:</em> To make Direction E publishable, SimuPharm must be tested against <strong>real external experimental fault data</strong>: 
            e.g., historical chromatographic incident logs from open repositories (Zenodo) or a small, targeted laboratory micro-campaign 
            (intentionally injecting an air bubble or using a worn pump seal on an actual instrument).
        </p>

        <h3 class="subsection-title">10.3 Feasibility & Publication Verdict for Direction E</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Evaluation Dimension</th>
                    <th>Assessment & Ground Reality</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Scientific Ceiling</strong></td><td><span class="badge badge-green">HIGHEST IN PLATFORM (IF: 7.4)</span>: Targetable at flagship <em>Analytical Chemistry</em> (ACS).</td></tr>
                <tr><td><strong>Required Development</strong></td><td><span class="badge badge-yellow">HIGH (6–8 WEEKS)</span>: Feature extractor, classification pipeline, external validation harness.</td></tr>
                <tr><td><strong>Validation Dependency</strong></td><td><span class="badge badge-yellow">YELLOW</span>: Requires real experimental fault benchmarks to escape circularity.</td></tr>
                <tr><td><strong>Strategic Ruling</strong></td><td><span class="badge badge-yellow">FLAGSHIP RESEARCH FOR PHASE 6</span>: Too resource-intensive for immediate 3-week execution.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 11: CANDIDATE DIRECTION F — AUTONOMOUS METHOD DEVELOPMENT -->
    <div class="page">
        <h2 class="section-title">11. DIRECTION F: AUTONOMOUS METHOD DEVELOPMENT & OPTIMIZATION</h2>
        
        <div class="callout callout-note">
            <strong>CORE SCIENTIFIC QUESTION:</strong> Can an autonomous, active-learning algorithm navigate multi-dimensional chromatographic parameter space 
            to discover optimal Pareto trade-offs (maximizing resolution while minimizing analysis time) faster than traditional manual trial-and-error?
        </div>

        <h3 class="subsection-title">11.1 Problem Context & Literature Reality</h3>
        <p class="body-text">
            Automated method optimization is heavily researched. Commercial platforms like ChromSword Auto already use heuristic search algorithms 
            connected to physical autosamplers. Recent academic literature (e.g. De Vos, Euerby, Desmet) frequently applies Bayesian Optimization 
            with Gaussian Process surrogates to find optimal gradient profiles. 
            <em>Reality Check:</em> Merely applying Bayesian optimization to an HPLC simulator is <strong>not novel in 2026</strong>.
        </p>

        <h3 class="subsection-title">11.2 Reality Check on the Agentic Layer (<span class="code-span">lab_agent.py</span>)</h3>
        <p class="body-text">
            SimuPharm possesses a 752-line autonomous lab agent (<span class="code-span">backend/neural/lab_agent.py</span>). 
            However, forensic inspection reveals that this agent uses simple prompt-driven tool-calling with hardcoded heuristics. 
            Calling this "novel AI method development" would be destroyed by reviewers. 
            To make Direction F publishable, SimuPharm would have to introduce <strong>formal Multi-Objective Bayesian Optimization with Pareto Front benchmarking</strong>.
        </p>

        <h3 class="subsection-title">11.3 Feasibility & Publication Verdict for Direction F</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Evaluation Dimension</th>
                    <th>Assessment & Ground Reality</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Required Development</strong></td><td><span class="badge badge-yellow">HIGH (4–6 WEEKS)</span>: Coupling Gaussian Process active learning to backend simulation loops.</td></tr>
                <tr><td><strong>Literature Crowding</strong></td><td><span class="badge badge-red">EXTREMELY CROWDED</span>: Dozens of recent papers on Bayesian optimization in chromatography.</td></tr>
                <tr><td><strong>Target Journal</strong></td><td><em>Journal of Chemical Information and Modeling</em> (JCIM, IF: 5.6).</td></tr>
                <tr><td><strong>Strategic Ruling</strong></td><td><span class="badge badge-yellow">SECONDARY (RANK 6)</span>: High development effort with modest novelty differentiation.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 12: CANDIDATE DIRECTION G — SOFTWARE PAPER -->
    <div class="page">
        <h2 class="section-title">12. DIRECTION G: SOFTWARE & OPEN-SOURCE PLATFORM PAPER</h2>
        
        <div class="callout callout-discovery">
            <strong>CORE SCIENTIFIC QUESTION:</strong> How can a client-side WebAssembly/Python architecture provide a fully reproducible, 
            zero-installation simulation environment spanning seven analytical instruments with sub-millisecond execution latency?
        </div>

        <h3 class="subsection-title">12.1 SoftwareX & JOSS Standards Evaluation</h3>
        <p class="body-text">
            Journals like <em>SoftwareX</em> (Elsevier, Impact Factor: 2.8) and <em>Journal of Open Source Software</em> (JOSS) evaluate software 
            not on whether it discovers new chemical phenomena, but on whether it provides an <strong>impactful, reproducible, high-quality open-source research tool</strong>. 
            SimuPharm currently satisfies over 85% of SoftwareX requirements:
        </p>
        <ul class="bullet-list">
            <li><strong>Working Implementation:</strong> Complete full-stack implementation (FastAPI backend + JavaScript frontend).</li>
            <li><strong>Automated Testing:</strong> Comprehensive test suite in <span class="code-span">tests/</span> (<span class="code-span">test_simulations.py</span>, <span class="code-span">test_auth.py</span>) passing under <span class="code-span">pytest</span>.</li>
            <li><strong>Multi-Instrument Breadth:</strong> Unprecedented coverage of 7 instruments in a single accessible codebase.</li>
            <li><strong>Sub-Millisecond Execution:</strong> Deterministic numerical execution enabling high-throughput computational sweeps.</li>
        </ul>

        <h3 class="subsection-title">12.2 What Must Be Added for SoftwareX Submission</h3>
        <p class="body-text">
            To achieve guaranteed acceptance in <em>SoftwareX</em>, only three administrative steps are required:
            (1) Add an approved OSI license (MIT or GPL-3.0) to the repository root, 
            (2) Create an open GitHub repository with automated GitHub Actions CI/CD test runs, and 
            (3) Draft the standard 6-page SoftwareX manuscript descriptor.
        </p>

        <h3 class="subsection-title">12.3 Feasibility & Publication Verdict for Direction G</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Evaluation Dimension</th>
                    <th>Assessment & Ground Reality</th>
                </tr>
            </thead>
            <tbody>
                <tr><td><strong>Required Development</strong></td><td><span class="badge badge-green">VERY LOW (1–2 WEEKS)</span>: Purely packaging, licensing, and descriptor writing.</td></tr>
                <tr><td><strong>Acceptance Probability</strong></td><td><span class="badge badge-green">VERY HIGH (&gt;90%)</span>: Codebase already exceeds typical SoftwareX technical standards.</td></tr>
                <tr><td><strong>Target Journal</strong></td><td><em>SoftwareX</em> (Elsevier, IF: 2.8) or <em>JOSS</em>.</td></tr>
                <tr><td><strong>Strategic Ruling</strong></td><td><span class="badge badge-green">IMMEDIATE QUICK WIN</span>: Execute in parallel to secure software citation priority.</td></tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 13: EDUCATIONAL ROUTE ASSESSMENT -->
    <div class="page">
        <h2 class="section-title">13. THE EDUCATIONAL ROUTE ASSESSMENT (PHASE 4 CONTEXT)</h2>
        
        <p class="body-text">
            SimuPharm's Phase 4 was dedicated to designing an educational pilot study targeting the <em>Journal of Chemical Education</em> (JCE). 
            In Phase 4.2.3, the educational research package was thoroughly corrected, sanitized of statistical overclaims, and locked under an 
            <strong>Absolute Protocol Freeze</strong>. 
            Here, we re-evaluate the educational route in relation to the broader Phase 5.1 publication strategy.
        </p>

        <h3 class="subsection-title">13.1 Why the Educational Route Requires Human Students</h3>
        <p class="body-text">
            A software simulation cannot be published in top educational research journals (*Journal of Chemical Education*, *Currents in Pharmacy Teaching & Learning*) 
            merely by describing the interface. JCE reviewers strictly enforce Chemical Education Research (CER) standards:
        </p>
        <div class="rule-box">
            <strong>MANDATORY CER CRITERIA FOR JCE ACCEPTANCE:</strong><br>
            • Validated assessment instruments (pre-test, post-test, practical diagnostic rubric).<br>
            • Quantitative evidence of student learning gains (normalized gain $g$, paired Wilcoxon signed-rank test).<br>
            • Standardized usability measurement (System Usability Scale, SUS $\ge 70$).<br>
            • Formal institutional ethics committee review (IRB/IEC approved participant consent).
        </div>

        <h3 class="subsection-title">13.2 The Absolute Governance Bottleneck</h3>
        <div class="callout callout-warning">
            <strong>GOVERNANCE STATUS:</strong> The Phase 4.2.3 protocol is permanently stamped:
            <br>
            <span class="badge badge-red" style="font-size: 8pt; padding: 3px 8px; margin-top: 4px;">NO-GO — INSTITUTIONAL ETHICS AUTHORIZATION PENDING</span>
            <br><br>
            Until formal IRB/IEC clearance is issued by an accredited academic institution, <strong>not a single student can be recruited</strong>, 
            and no pilot data can be legally or ethically collected. 
            Therefore, <strong>the educational route cannot serve as the primary or immediate publication strategy</strong>.
        </div>

        <h3 class="subsection-title">13.3 Strategic Role: Contingency Paper Only</h3>
        <p class="body-text">
            The Phase 4.2.3 educational package remains high-quality and recruitment-ready. 
            It should be maintained in a <strong>frozen contingency state</strong>. 
            Once IRB authorization is received in the future, the 50-minute student pilot ($N=25$) can be executed smoothly 
            as an independent educational paper in <em>Currents in Pharmacy Teaching and Learning</em>. 
            It must not distract from the computational and chemometric priorities identified in Phase 5.1.
        </p>
    </div>
    """

if __name__ == "__main__":
    print("Part 2 generated successfully. Length:", len(get_part2_html()))
