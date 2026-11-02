/* ================================================================
   SimuPharma AUTONOMOUS AI Lab Assistant — Agentic Function Calling
   
   Upgraded from simple chat to a full AUTONOMOUS AGENT that can:
   - Run instrument simulations via Gemini function calling
   - Execute multi-step experiments autonomously
   - Track student mastery adaptively
   - Show real-time tool execution feedback in chat

   Powered by Gemini 2.0 Flash with tool_use / function calling
   ================================================================ */
(function () {
    'use strict';

    // ---- Configuration ----
    // Models tried in order: newest first, with fallbacks
    const GEMINI_MODELS = ['gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-1.5-flash-latest', 'gemini-1.5-flash'];
    let currentModelIndex = 0;
    let lastApiError = '';
    const GEMINI_API_BASE = 'https://generativelanguage.googleapis.com/v1beta/models';
    const MAX_HISTORY = 20;
    const MAX_AGENT_LOOPS = 8;   // Safety limit on function calling loops
    const LS_KEY_API = 'simupharma_gemini_key';
    const LS_KEY_MODE = 'simupharma_chat_mode';
    const BACKEND_BASE = window.location.origin.includes('localhost')
        ? 'http://localhost:8000'
        : window.location.origin;

    // ---- Backend AI Status ----
    let backendAiAvailable = false;

    async function checkBackendAI() {
        try {
            const resp = await fetch(`${BACKEND_BASE}/api/v1/ai/status`, { signal: AbortSignal.timeout(5000) });
            if (resp.ok) {
                const data = await resp.json();
                backendAiAvailable = data.has_key === true;
                return backendAiAvailable;
            }
        } catch (e) {
            console.warn('[SimuBot] Backend AI check failed:', e.message);
        }
        return false;
    }

    // ---- Page Context Detection ----
    function detectPageContext() {
        const path = window.location.pathname.toLowerCase();
        const file = path.split('/').pop() || 'index.html';
        const contextMap = {
            'hplc_simulator.html': { instrument: 'HPLC Simulator', desc: 'The student is actively using the HPLC simulator.' },
            'hplc.html': { instrument: 'HPLC Info Page', desc: 'The student is reading about HPLC.' },
            'ftir_simulator.html': { instrument: 'FTIR Simulator', desc: 'The student is using the FTIR simulator.' },
            'ftir.html': { instrument: 'FTIR Info Page', desc: 'The student is reading about FTIR spectroscopy.' },
            'uv_vis_simulator.html': { instrument: 'UV-Vis Simulator', desc: 'The student is using the UV-Vis spectrophotometer simulator.' },
            'uv_vis.html': { instrument: 'UV-Vis Info Page', desc: 'The student is reading about UV-Vis spectroscopy.' },
            'gc_simulator.html': { instrument: 'GC Simulator', desc: 'The student is using the Gas Chromatography simulator.' },
            'gc.html': { instrument: 'GC Info Page', desc: 'The student is reading about Gas Chromatography.' },
            'mass_spec_simulator.html': { instrument: 'Mass Spectrometry Simulator', desc: 'The student is using the Mass Spectrometry simulator.' },
            'mass_spec.html': { instrument: 'Mass Spec Info Page', desc: 'The student is reading about Mass Spectrometry.' },
            'polarimeter_simulator.html': { instrument: 'Polarimeter Simulator', desc: 'The student is using the Polarimeter simulator.' },
            'polarimeter.html': { instrument: 'Polarimeter Info Page', desc: 'The student is reading about Polarimetry.' },
            'psa_simulator.html': { instrument: 'PSA Simulator', desc: 'The student is using the Particle Size Analyzer simulator.' },
            'psa.html': { instrument: 'PSA Info Page', desc: 'The student is reading about Particle Size Analysis.' },
            'quiz.html': { instrument: 'Quiz Section', desc: 'The student is in the quiz/assessment section.' },
            'instruments.html': { instrument: 'Instruments Gallery', desc: 'The student is browsing the instruments gallery.' },
            'dashboard.html': { instrument: 'Dashboard', desc: 'The student is viewing their learning dashboard.' },
            'experiment.html': { instrument: 'Experiment Page', desc: 'The student is on the experiment page.' },
            'index.html': { instrument: 'Home Page', desc: 'The student is on the SimuPharma homepage.' }
        };
        return contextMap[file] || { instrument: 'SimuPharma', desc: 'The student is browsing SimuPharma.' };
    }

    // ---- Tool Declarations for Gemini Function Calling ----
    const TOOL_DECLARATIONS = [
        {
            name: "run_uvvis",
            description: "Run a UV-Vis spectroscopy simulation using Beer-Lambert Law. Generates absorption spectrum. Use for quantitative analysis and chromophore identification.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_id: { type: "STRING", description: "Compound to analyze (e.g., 'paracetamol', 'aspirin', 'caffeine')" },
                    concentration: { type: "NUMBER", description: "Concentration in mol/L (default: 0.001)" },
                    path_length: { type: "NUMBER", description: "Path length in cm (default: 1.0)" }
                },
                required: ["compound_id"]
            }
        },
        {
            name: "run_ftir",
            description: "Run an FTIR spectroscopy simulation. Generates infrared spectrum with functional group assignments. Use for molecular structure identification.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_id: { type: "STRING", description: "Compound to analyze" }
                },
                required: ["compound_id"]
            }
        },
        {
            name: "run_hplc",
            description: "Run an HPLC chromatography simulation. Generates chromatogram with retention times. Use for separation and purity analysis.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_id: { type: "STRING", description: "Compound to analyze" },
                    flow_rate: { type: "NUMBER", description: "Flow rate in mL/min (default: 1.0)" }
                },
                required: ["compound_id"]
            }
        },
        {
            name: "run_gc",
            description: "Run a Gas Chromatography simulation. Use for volatile compound and residual solvent analysis.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_id: { type: "STRING", description: "Compound to analyze" },
                    initial_temp: { type: "NUMBER", description: "Initial oven temperature °C (default: 40)" },
                    final_temp: { type: "NUMBER", description: "Final oven temperature °C (default: 280)" }
                },
                required: ["compound_id"]
            }
        },
        {
            name: "run_mass_spec",
            description: "Run a Mass Spectrometry simulation. Generates mass spectrum with m/z values and fragmentation patterns. Use for molecular weight and structure.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_id: { type: "STRING", description: "Compound to analyze" },
                    ionization_mode: { type: "STRING", description: "Ionization mode: 'EI' or 'ESI' (default: 'EI')" }
                },
                required: ["compound_id"]
            }
        },
        {
            name: "run_polarimeter",
            description: "Run a polarimetry measurement. Calculates optical rotation for chiral compounds.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_id: { type: "STRING", description: "Compound to analyze" },
                    concentration: { type: "NUMBER", description: "Concentration in g/mL (default: 0.1)" }
                },
                required: ["compound_id"]
            }
        },
        {
            name: "run_psa",
            description: "Run a Particle Size Analysis simulation. Generates particle size distribution with D10/D50/D90 values.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_id: { type: "STRING", description: "Compound to analyze" },
                    mean_size: { type: "NUMBER", description: "Mean particle size in μm (default: 50)" }
                },
                required: ["compound_id"]
            }
        },
        {
            name: "search_compound",
            description: "Search the pharmaceutical compound database by name, formula, CAS number, or category. Returns matching compounds.",
            parameters: {
                type: "OBJECT",
                properties: {
                    query: { type: "STRING", description: "Search query (name, formula, CAS, or category like 'Antibiotic')" }
                },
                required: ["query"]
            }
        },
        {
            name: "get_compound_info",
            description: "Get detailed information about a specific compound including spectral data, molecular weight, formula, and therapeutic class.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_id: { type: "STRING", description: "Compound ID (e.g., 'paracetamol', 'aspirin')" }
                },
                required: ["compound_id"]
            }
        },
        {
            name: "identify_unknown",
            description: "Use spectral matching engine to identify an unknown compound from spectral data. Provide peaks from UV-Vis, FTIR, and/or Mass Spec.",
            parameters: {
                type: "OBJECT",
                properties: {
                    uvvis_peaks: { type: "ARRAY", description: "UV-Vis peaks: [{wavelength, absorbance}]", items: { type: "OBJECT" } },
                    ftir_peaks: { type: "ARRAY", description: "FTIR peaks: [{wavenumber}]", items: { type: "OBJECT" } },
                    ms_fragments: { type: "ARRAY", description: "MS fragments: [{mz, intensity}]", items: { type: "OBJECT" } },
                    molecular_weight: { type: "NUMBER", description: "Known molecular weight (if any)" }
                },
                required: []
            }
        },
        {
            name: "compare_compounds",
            description: "Compare two compounds across all instruments. Returns differences in spectra, molecular weight, and properties.",
            parameters: {
                type: "OBJECT",
                properties: {
                    compound_a: { type: "STRING", description: "First compound ID" },
                    compound_b: { type: "STRING", description: "Second compound ID" }
                },
                required: ["compound_a", "compound_b"]
            }
        },
        {
            name: "get_learning_suggestion",
            description: "Get AI-recommended next activity for the student based on their mastery level. Returns what instrument to study and what type of activity.",
            parameters: {
                type: "OBJECT",
                properties: {},
                required: []
            }
        }
    ];

    // ---- Tool emoji and label mapping ----
    const TOOL_UI = {
        run_uvvis: { emoji: '☀️', label: 'UV-Vis Spectroscopy', color: '#f59e0b' },
        run_ftir: { emoji: '🌊', label: 'FTIR Spectroscopy', color: '#3b82f6' },
        run_hplc: { emoji: '💧', label: 'HPLC Chromatography', color: '#06b6d4' },
        run_gc: { emoji: '🔥', label: 'Gas Chromatography', color: '#ef4444' },
        run_mass_spec: { emoji: '⚛️', label: 'Mass Spectrometry', color: '#8b5cf6' },
        run_polarimeter: { emoji: '🔄', label: 'Polarimetry', color: '#10b981' },
        run_psa: { emoji: '🔬', label: 'Particle Size Analysis', color: '#ec4899' },
        search_compound: { emoji: '🔍', label: 'Searching Compounds', color: '#6366f1' },
        get_compound_info: { emoji: '📋', label: 'Getting Compound Info', color: '#64748b' },
        identify_unknown: { emoji: '🧬', label: 'Spectral Matching', color: '#14b8a6' },
        compare_compounds: { emoji: '⚖️', label: 'Comparing Compounds', color: '#f97316' },
        get_learning_suggestion: { emoji: '🎯', label: 'Getting Recommendation', color: '#a855f7' }
    };

    // ---- Build System Prompt (Agentic) ----
    function buildSystemPrompt(mode) {
        const ctx = detectPageContext();
        const modeInstruction = mode === 'beginner'
            ? 'Use simple language, everyday analogies, and step-by-step explanations. Avoid jargon unless you explain it.'
            : 'Use proper technical terminology, include equations where relevant, reference pharmacopeial standards (USP, IP, BP), and discuss advanced concepts.';

        return `You are NeuroLab AI, the autonomous AI lab instructor for SimuPharma — a virtual pharmaceutical lab.

You have direct access to 7 instruments and can run experiments. When asked to analyze or compare compounds, USE YOUR TOOLS — don't just describe, actually call the functions. When you run instrument tools, the student will see interactive spectrum/chromatogram charts rendered inline from the data you return.

Context: ${ctx.desc} (Page: ${ctx.instrument})
${modeInstruction}

TEACHING STYLE:
- Be a warm, encouraging teacher. Use the student's results to teach concepts.
- After running instruments, reference the visual chart: "Notice the peak at 243nm in the spectrum above..."
- Ask ONE follow-up question to test understanding: "What functional group causes that strong absorption at 1650 cm⁻¹?"
- Celebrate milestones: "Great — you've now used 3 different instruments! You're becoming a real analyst."
- Suggest next steps: "Now try comparing this with a structurally similar drug to see the differences."

Tools: UV-Vis, FTIR, HPLC, GC, Mass Spec, Polarimeter, PSA
You can: search compounds, get compound info, identify unknowns from spectra, compare compounds, suggest learning paths.

Compound IDs: paracetamol, aspirin, ibuprofen, amoxicillin, ciprofloxacin, metformin, ranitidine, caffeine, diclofenac, atorvastatin, omeprazole, amlodipine, losartan, ascorbic_acid, chloramphenicol, sulfamethoxazole, phenol, benzocaine, lidocaine, dextrose, sucrose

Rules: Use markdown, be concise, chain tool calls when needed, explain results with teaching focus.`;
    }

    // ---- Execute Tool via Backend API ----
    async function executeToolOnBackend(toolName, args) {
        try {
            const response = await fetch(`${BACKEND_BASE}/api/neural/agent/execute-tool`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tool_name: toolName, arguments: args })
            });

            if (response.ok) {
                return await response.json();
            }

            // Backend might not be running — fallback to direct API
            console.warn('Backend not available, using fallback');
            return await executeToolFallback(toolName, args);
        } catch (e) {
            console.warn('Backend error, using fallback:', e);
            return await executeToolFallback(toolName, args);
        }
    }

    // ---- Fallback: Direct tool execution when backend is offline ----
    async function executeToolFallback(toolName, args) {
        // For search/info, we can provide basic responses
        if (toolName === 'search_compound') {
            return { results: [{ note: "Connect to backend for live search. Try running: uvicorn backend.main:app --reload --port 8000" }], total: 0 };
        }
        if (toolName === 'get_learning_suggestion') {
            return { recommended_instrument: "uvvis", instrument_label: "UV-Vis Spectroscopy", action: "Start with UV-Vis — it's the foundation of pharmaceutical analysis", current_mastery: 0 };
        }
        // For instrument simulations, try backend simulation endpoints directly
        const simEndpoints = {
            run_uvvis: '/api/simulate/uvvis',
            run_ftir: '/api/simulate/ftir',
            run_hplc: '/api/simulate/hplc',
            run_gc: '/api/simulate/gc',
            run_mass_spec: '/api/simulate/mass-spec/compound',
            run_polarimeter: '/api/simulate/polarimeter',
            run_psa: '/api/simulate/psa'
        };
        const endpoint = simEndpoints[toolName];
        if (endpoint) {
            try {
                const body = {};
                if (args.compound_id) body.compound_id = args.compound_id;
                if (args.concentration) body.concentration = args.concentration;
                const r = await fetch(`${BACKEND_BASE}${endpoint}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });
                if (r.ok) return await r.json();
            } catch (e) { /* fall through */ }
        }
        return { note: `Tool ${toolName} executed. Start the backend for full results: uvicorn backend.main:app --reload --port 8000` };
    }

    // ---- Simple Markdown Renderer ----
    function renderMarkdown(text) {
        let html = text
            .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
            .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
            .replace(/^### (.+)$/gm, '<h4>$1</h4>')
            .replace(/^[\-\*] (.+)$/gm, '<li>$1</li>')
            .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
            .replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');

        if (!html.startsWith('<')) html = '<p>' + html + '</p>';
        else if (!html.startsWith('<p>') && !html.startsWith('<h') && !html.startsWith('<ul') && !html.startsWith('<pre>')) {
            html = '<p>' + html + '</p>';
        }
        return html;
    }

    // ---- Create Agent Action Card (shown during tool execution) ----
    function createActionCard(toolName, args) {
        const tool = TOOL_UI[toolName] || { emoji: '🔧', label: toolName, color: '#64748b' };
        const card = document.createElement('div');
        card.className = 'agent-action-card';
        card.style.cssText = `
            display:flex; align-items:center; gap:10px; padding:10px 14px; margin:6px 0;
            border-radius:12px; font-size:13px;
            background: linear-gradient(135deg, ${tool.color}15, ${tool.color}08);
            border: 1px solid ${tool.color}30;
            color: ${tool.color};
            animation: agentPulse 1.5s ease-in-out infinite;
        `;

        let detail = '';
        if (args.compound_id) detail = ` — ${args.compound_id}`;
        else if (args.query) detail = ` — "${args.query}"`;
        else if (args.compound_a && args.compound_b) detail = ` — ${args.compound_a} vs ${args.compound_b}`;

        card.innerHTML = `
            <span style="font-size:20px">${tool.emoji}</span>
            <div>
                <strong>${tool.label}</strong>${detail}
                <div style="font-size:11px;opacity:0.7;margin-top:2px">Executing autonomously...</div>
            </div>
            <span class="agent-spinner"></span>
        `;
        return card;
    }

    // ---- Mark Action Card as Complete ----
    function completeActionCard(card, success = true) {
        const spinner = card.querySelector('.agent-spinner');
        if (spinner) spinner.remove();
        card.style.animation = 'none';
        const statusDot = document.createElement('span');
        statusDot.style.cssText = `margin-left:auto;font-size:16px;`;
        statusDot.textContent = success ? '✅' : '⚠️';
        card.appendChild(statusDot);
        const detail = card.querySelector('div > div:last-child');
        if (detail) detail.textContent = success ? 'Complete' : 'Error — check backend';
    }

    // ---- Inline Spectrum/Chromatogram Chart Renderer ----
    function renderSpectrumChart(toolName, toolResult) {
        console.log('[NeuroLab Chart] renderSpectrumChart called:', toolName, 'Chart.js:', typeof Chart !== 'undefined', 'toolResult keys:', toolResult ? Object.keys(toolResult) : 'null');
        if (!toolResult || toolResult.error) return null;

        // Determine chart data points based on tool type
        const res = toolResult.result || toolResult;
        let dataPoints = [];
        let title = '';
        let xLabel = '';
        let yLabel = '';
        let chartColor = '#f59e0b';
        let reverseX = false;
        let isBarChart = false;

        try {
            if (toolName === 'run_uvvis') {
                const peaks = toolResult.peaks_found || [];
                const lambdaMax = toolResult.lambda_max || 0;
                title = `UV-Vis Spectrum — λmax ${lambdaMax} nm`;
                xLabel = 'Wavelength (nm)'; yLabel = 'Absorbance'; chartColor = '#f59e0b';
                for (let wl = 200; wl <= 400; wl += 2) {
                    let abs = 0;
                    peaks.forEach(p => {
                        const c = p.wavelength_nm || 250, eps = p.molar_absorptivity || 10000, sig = 15;
                        abs += (eps * (toolResult.concentration || 0.001) * (toolResult.path_length || 1)) * Math.exp(-0.5 * ((wl - c) / sig) ** 2);
                    });
                    dataPoints.push({ x: wl, y: abs });
                }
            } else if (toolName === 'run_ftir') {
                const groups = toolResult.functional_groups || [];
                title = `FTIR — ${groups.length} functional groups`;
                xLabel = 'Wavenumber (cm⁻¹)'; yLabel = 'Transmittance (%)'; chartColor = '#3b82f6'; reverseX = true;
                for (let wn = 4000; wn >= 400; wn -= 10) {
                    let t = 95 + Math.random() * 3;
                    groups.forEach(g => {
                        const c = g.wavenumber_cm1 || 1700, d = g.intensity === 'strong' ? 70 : g.intensity === 'medium' ? 45 : 25;
                        t -= d * Math.exp(-0.5 * ((wn - c) / 30) ** 2);
                    });
                    dataPoints.push({ x: wn, y: Math.max(0, t) });
                }
            } else if (toolName === 'run_hplc') {
                const peaks = res?.peaks || res?.chromatogram_peaks || [];
                title = `HPLC — ${toolResult.compound || ''}`; xLabel = 'Retention Time (min)'; yLabel = 'Signal (mAU)'; chartColor = '#06b6d4';
                const maxT = Math.max(15, ...peaks.map(p => (p.retention_time || p.rt || 5) + 3));
                for (let t = 0; t <= maxT; t += 0.1) {
                    let sig = Math.random() * 0.5;
                    peaks.forEach(p => { const rt = p.retention_time || p.rt || 5, h = p.height || p.area || 1000, w = p.width || 0.3; sig += h * Math.exp(-0.5 * ((t - rt) / (w / 2.354)) ** 2); });
                    dataPoints.push({ x: +(t.toFixed(2)), y: +(sig.toFixed(2)) });
                }
            } else if (toolName === 'run_gc') {
                const peaks = res?.peaks || res?.chromatogram_peaks || [];
                title = `GC — ${toolResult.compound || ''}`; xLabel = 'Retention Time (min)'; yLabel = 'Signal'; chartColor = '#ef4444';
                const maxT = Math.max(20, ...peaks.map(p => (p.retention_time || p.rt || 8) + 3));
                for (let t = 0; t <= maxT; t += 0.15) {
                    let sig = Math.random() * 0.3;
                    peaks.forEach(p => { const rt = p.retention_time || p.rt || 8, h = p.height || 500, w = p.width || 0.25; sig += h * Math.exp(-0.5 * ((t - rt) / (w / 2.354)) ** 2); });
                    dataPoints.push({ x: +(t.toFixed(2)), y: +(sig.toFixed(2)) });
                }
            } else if (toolName === 'run_mass_spec') {
                const frags = res?.fragments || res?.peaks || toolResult.fragments || [];
                title = `Mass Spec — ${toolResult.compound || ''}`; xLabel = 'm/z'; yLabel = 'Intensity (%)'; chartColor = '#8b5cf6'; isBarChart = true;
                frags.forEach(f => dataPoints.push({ x: f.mz || f.mass || 0, y: f.relative_intensity || f.intensity || 0 }));
            } else if (toolName === 'run_psa') {
                const d50 = res?.d50 || toolResult.d50 || 50;
                title = `PSA — D50: ${d50} μm`; xLabel = 'Particle Size (μm)'; yLabel = 'Volume (%)'; chartColor = '#ec4899';
                const dist = res?.distribution || res?.size_distribution || [];
                if (dist.length > 0) { dist.forEach(d => dataPoints.push({ x: d.size || d.diameter, y: d.frequency || d.volume_pct || 0 })); }
                else { for (let s = 0.1; s <= d50 * 4; s += d50 * 0.05) { const sig = d50 * 0.4; dataPoints.push({ x: +(s.toFixed(1)), y: +(100 * Math.exp(-0.5 * (Math.log(s / d50) / (Math.log(sig / d50) || 0.5)) ** 2)).toFixed(2) }); } }
            } else if (toolName === 'run_polarimeter') {
                title = `Polarimeter — ${toolResult.compound || ''}`; chartColor = '#10b981';
                // Polarimeter doesn't produce a curve — show a data card instead
                const rotation = toolResult.observed_rotation || toolResult.specific_rotation || 0;
                const container = document.createElement('div');
                container.className = 'agent-chart-wrap';
                container.style.cssText = 'margin:8px 0 4px;padding:14px;border-radius:12px;background:rgba(15,23,42,0.7);border:1px solid rgba(16,185,129,0.2);';
                container.innerHTML = `<div style="text-align:center"><div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">Polarimeter Result</div><div style="font-size:28px;font-weight:800;color:#10b981">[α] = ${typeof rotation === 'number' ? rotation.toFixed(2) : rotation}°</div><div style="font-size:11px;color:#94a3b8;margin-top:4px">${toolResult.compound || 'Compound'} · ${toolResult.direction || ''}</div></div>`;
                return container;
            }
        } catch (e) {
            console.warn('[NeuroLab] Chart data error:', e);
            return null;
        }

        if (dataPoints.length === 0 && !isBarChart) return null;

        // ---- Container ----
        const container = document.createElement('div');
        container.className = 'agent-chart-wrap';
        container.style.cssText = `margin:8px 0 4px;padding:10px;border-radius:12px;background:rgba(15,23,42,0.7);border:1px solid rgba(255,255,255,0.06);cursor:pointer;transition:all 0.3s ease;`;

        // ------- Try Chart.js first, else SVG fallback -------
        if (typeof Chart !== 'undefined') {
            const canvas = document.createElement('canvas');
            canvas.width = 380; canvas.height = 170;
            canvas.style.cssText = 'width:100%;height:170px;';
            container.appendChild(canvas);

            let expanded = false;
            container.addEventListener('click', () => { expanded = !expanded; canvas.style.height = expanded ? '300px' : '170px'; });

            // Build Chart.js config
            let config;
            if (isBarChart) {
                config = { type: 'bar', data: { labels: dataPoints.map(d => d.x), datasets: [{ data: dataPoints.map(d => d.y), backgroundColor: chartColor + 'b3', borderColor: chartColor, borderWidth: 1 }] }, options: chartOptions(xLabel, yLabel, title, reverseX) };
            } else {
                config = { type: 'line', data: { datasets: [{ data: dataPoints, borderColor: chartColor, backgroundColor: chartColor + '1a', borderWidth: 2, fill: true, pointRadius: 0, tension: 0.4 }] }, options: chartOptions(xLabel, yLabel, title, reverseX) };
            }
            setTimeout(() => { try { new Chart(canvas, config); } catch (e) { console.warn('[NeuroLab] Chart.js error:', e); } }, 50);
        } else {
            // ---- SVG Fallback ---- Always renders, no library needed
            const W = 380, H = 160, PAD = 30;
            const plotW = W - PAD * 2, plotH = H - PAD * 1.5;

            let svgContent = '';
            // Title
            svgContent += `<text x="${W/2}" y="14" font-size="11" fill="#94a3b8" text-anchor="middle" font-weight="600" font-family="Inter,system-ui,sans-serif">${title}</text>`;
            // Axes
            svgContent += `<line x1="${PAD}" y1="${H-PAD}" x2="${W-PAD}" y2="${H-PAD}" stroke="#334155" stroke-width="1"/>`;
            svgContent += `<line x1="${PAD}" y1="${PAD/2+10}" x2="${PAD}" y2="${H-PAD}" stroke="#334155" stroke-width="1"/>`;
            // Axis labels
            svgContent += `<text x="${W/2}" y="${H-4}" font-size="9" fill="#64748b" text-anchor="middle" font-family="Inter,system-ui,sans-serif">${xLabel}</text>`;
            svgContent += `<text x="8" y="${H/2}" font-size="9" fill="#64748b" text-anchor="middle" font-family="Inter,system-ui,sans-serif" transform="rotate(-90,8,${H/2})">${yLabel}</text>`;

            if (isBarChart && dataPoints.length > 0) {
                // Bar chart
                const maxY = Math.max(...dataPoints.map(d => d.y), 1);
                const barW = Math.max(2, plotW / dataPoints.length - 2);
                dataPoints.forEach((d, i) => {
                    const bx = PAD + (i / dataPoints.length) * plotW;
                    const bh = (d.y / maxY) * plotH;
                    const by = H - PAD - bh;
                    svgContent += `<rect x="${bx}" y="${by}" width="${barW}" height="${bh}" fill="${chartColor}" opacity="0.7" rx="1"/>`;
                    if (dataPoints.length <= 20) svgContent += `<text x="${bx + barW/2}" y="${H-PAD+10}" font-size="7" fill="#64748b" text-anchor="middle">${d.x}</text>`;
                });
            } else if (dataPoints.length > 0) {
                // Line chart as SVG path
                const xs = dataPoints.map(d => d.x);
                const ys = dataPoints.map(d => d.y);
                const minX = Math.min(...xs), maxX = Math.max(...xs);
                const minY = 0, maxY = Math.max(...ys, 0.001);
                const scaleX = v => PAD + ((v - minX) / (maxX - minX || 1)) * plotW;
                const scaleY = v => (H - PAD) - ((v - minY) / (maxY - minY || 1)) * plotH;

                // Build path
                let pathD = '';
                let fillD = '';
                const pts = reverseX ? [...dataPoints].reverse() : dataPoints;
                pts.forEach((p, i) => {
                    const px = scaleX(p.x), py = scaleY(p.y);
                    pathD += (i === 0 ? `M${px},${py}` : ` L${px},${py}`);
                });
                // Fill area
                const firstPt = reverseX ? pts[0] : pts[0];
                const lastPt = reverseX ? pts[pts.length-1] : pts[pts.length-1];
                fillD = pathD + ` L${scaleX(lastPt.x)},${H-PAD} L${scaleX(firstPt.x)},${H-PAD} Z`;
                svgContent += `<path d="${fillD}" fill="${chartColor}" opacity="0.1"/>`;
                svgContent += `<path d="${pathD}" fill="none" stroke="${chartColor}" stroke-width="1.5"/>`;

                // X-axis ticks (5 ticks)
                for (let i = 0; i <= 4; i++) {
                    const val = reverseX ? maxX - (i/4) * (maxX - minX) : minX + (i/4) * (maxX - minX);
                    const tx = PAD + (i/4) * plotW;
                    svgContent += `<text x="${tx}" y="${H-PAD+12}" font-size="8" fill="#64748b" text-anchor="middle">${Math.round(val)}</text>`;
                }
                // Y-axis ticks (3 ticks)
                for (let i = 0; i <= 2; i++) {
                    const val = minY + (i/2) * (maxY - minY);
                    const ty = scaleY(val);
                    svgContent += `<text x="${PAD-4}" y="${ty+3}" font-size="8" fill="#64748b" text-anchor="end">${val < 10 ? val.toFixed(2) : Math.round(val)}</text>`;
                    svgContent += `<line x1="${PAD}" y1="${ty}" x2="${W-PAD}" y2="${ty}" stroke="#1e293b" stroke-width="0.5" stroke-dasharray="3"/>`;
                }
            }

            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
            svg.style.cssText = 'width:100%;height:auto;';
            svg.innerHTML = svgContent;
            container.appendChild(svg);
        }

        // Add "Open in Simulator" link
        const simLinks = {
            run_uvvis: 'uv_vis_simulator.html', run_ftir: 'ftir_simulator.html',
            run_hplc: 'hplc_simulator.html', run_gc: 'gc_simulator.html',
            run_mass_spec: 'mass_spec_simulator.html', run_psa: 'psa_simulator.html'
        };
        if (simLinks[toolName]) {
            const link = document.createElement('a');
            link.href = simLinks[toolName];
            link.style.cssText = `display:inline-flex;align-items:center;gap:4px;margin-top:6px;font-size:0.65rem;color:#60a5fa;text-decoration:none;font-weight:500;`;
            link.innerHTML = '<i class="fas fa-external-link-alt"></i> Open in full simulator';
            link.addEventListener('click', e => e.stopPropagation());
            container.appendChild(link);
        }

        return container;
    }

    // ---- Chart Builders for Each Instrument ----

    function buildUVVisChart(toolResult, res) {
        // Generate spectrum curve from peaks
        const peaks = toolResult.peaks_found || [];
        const lambdaMax = toolResult.lambda_max || 0;
        const data = [];
        for (let wl = 200; wl <= 400; wl += 2) {
            let absorbance = 0;
            peaks.forEach(p => {
                const center = p.wavelength_nm || 250;
                const epsilon = p.molar_absorptivity || 10000;
                const sigma = 15;
                absorbance += (epsilon * (toolResult.concentration || 0.001) * (toolResult.path_length || 1)) *
                    Math.exp(-0.5 * Math.pow((wl - center) / sigma, 2));
            });
            data.push({ x: wl, y: Math.round(absorbance * 10000) / 10000 });
        }
        return {
            type: 'line',
            data: {
                datasets: [{
                    data: data, borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.1)',
                    borderWidth: 2, fill: true, pointRadius: 0, tension: 0.4
                }]
            },
            options: chartOptions('Wavelength (nm)', 'Absorbance', `UV-Vis — λmax ${lambdaMax} nm`)
        };
    }

    function buildFTIRChart(toolResult, res) {
        const groups = toolResult.functional_groups || [];
        const data = [];
        for (let wn = 4000; wn >= 400; wn -= 10) {
            let transmittance = 95 + Math.random() * 3;
            groups.forEach(g => {
                const center = g.wavenumber_cm1 || 1700;
                const depth = g.intensity === 'strong' ? 70 : g.intensity === 'medium' ? 45 : 25;
                const sigma = 30;
                transmittance -= depth * Math.exp(-0.5 * Math.pow((wn - center) / sigma, 2));
            });
            data.push({ x: wn, y: Math.max(0, transmittance) });
        }
        return {
            type: 'line',
            data: {
                datasets: [{
                    data: data, borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.08)',
                    borderWidth: 1.5, fill: true, pointRadius: 0, tension: 0.3
                }]
            },
            options: chartOptions('Wavenumber (cm⁻¹)', 'Transmittance (%)',
                `FTIR — ${groups.length} functional groups`, true)
        };
    }

    function buildHPLCChart(toolResult, res) {
        const peaks = res?.peaks || res?.chromatogram_peaks || [];
        const data = [];
        const maxTime = Math.max(15, ...peaks.map(p => (p.retention_time || p.rt || 5) + 3));
        for (let t = 0; t <= maxTime; t += 0.1) {
            let signal = Math.random() * 0.5;
            peaks.forEach(p => {
                const rt = p.retention_time || p.rt || 5;
                const height = p.height || p.area || 1000;
                const w = p.width || 0.3;
                signal += height * Math.exp(-0.5 * Math.pow((t - rt) / (w / 2.354), 2));
            });
            data.push({ x: Math.round(t * 100) / 100, y: Math.round(signal * 100) / 100 });
        }
        return {
            type: 'line',
            data: {
                datasets: [{
                    data: data, borderColor: '#06b6d4', backgroundColor: 'rgba(6,182,212,0.1)',
                    borderWidth: 1.5, fill: true, pointRadius: 0, tension: 0.2
                }]
            },
            options: chartOptions('Retention Time (min)', 'Signal (mAU)', `HPLC — ${toolResult.compound || ''}`)
        };
    }

    function buildGCChart(toolResult, res) {
        const peaks = res?.peaks || res?.chromatogram_peaks || [];
        const data = [];
        const maxTime = Math.max(20, ...peaks.map(p => (p.retention_time || p.rt || 8) + 3));
        for (let t = 0; t <= maxTime; t += 0.15) {
            let signal = Math.random() * 0.3;
            peaks.forEach(p => {
                const rt = p.retention_time || p.rt || 8;
                const height = p.height || 500;
                const w = p.width || 0.25;
                signal += height * Math.exp(-0.5 * Math.pow((t - rt) / (w / 2.354), 2));
            });
            data.push({ x: Math.round(t * 100) / 100, y: Math.round(signal * 100) / 100 });
        }
        return {
            type: 'line',
            data: {
                datasets: [{
                    data: data, borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.08)',
                    borderWidth: 1.5, fill: true, pointRadius: 0, tension: 0.2
                }]
            },
            options: chartOptions('Retention Time (min)', 'Signal', `GC — ${toolResult.compound || ''}`)
        };
    }

    function buildMassSpecChart(toolResult, res) {
        const fragments = res?.fragments || res?.peaks || toolResult.fragments || [];
        const labels = fragments.map(f => f.mz || f.mass || 0);
        const intensities = fragments.map(f => f.relative_intensity || f.intensity || 0);
        return {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: intensities, backgroundColor: 'rgba(139,92,246,0.7)',
                    borderColor: '#8b5cf6', borderWidth: 1
                }]
            },
            options: chartOptions('m/z', 'Relative Intensity (%)', `Mass Spec — ${toolResult.compound || ''}`)
        };
    }

    function buildPSAChart(toolResult, res) {
        const dist = res?.distribution || res?.size_distribution || [];
        const d50 = res?.d50 || toolResult.d50 || 50;
        let data;
        if (dist.length > 0) {
            data = dist.map(d => ({ x: d.size || d.diameter, y: d.frequency || d.volume_pct || 0 }));
        } else {
            // Generate synthetic distribution from D50
            data = [];
            for (let s = 0.1; s <= d50 * 4; s += d50 * 0.05) {
                const sigma = d50 * 0.4;
                const y = 100 * Math.exp(-0.5 * Math.pow(Math.log(s / d50) / (Math.log(sigma / d50) || 0.5), 2));
                data.push({ x: Math.round(s * 10) / 10, y: Math.round(y * 100) / 100 });
            }
        }
        return {
            type: 'line',
            data: {
                datasets: [{
                    data: data, borderColor: '#ec4899', backgroundColor: 'rgba(236,72,153,0.1)',
                    borderWidth: 2, fill: true, pointRadius: 0, tension: 0.4
                }]
            },
            options: chartOptions('Particle Size (μm)', 'Volume (%)', `PSA — D50: ${d50} μm`)
        };
    }

    // ---- Shared Chart Options ----
    function chartOptions(xLabel, yLabel, title, reverseX = false) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 600, easing: 'easeOutQuart' },
            plugins: {
                legend: { display: false },
                title: {
                    display: true, text: title,
                    color: '#94a3b8', font: { size: 11, weight: '600', family: 'Inter, system-ui' },
                    padding: { bottom: 8 }
                },
                tooltip: {
                    backgroundColor: 'rgba(15,23,42,0.95)', titleColor: '#e2e8f0',
                    bodyColor: '#94a3b8', borderColor: 'rgba(99,102,241,0.2)', borderWidth: 1,
                    cornerRadius: 8, padding: 8, bodyFont: { size: 11 }
                }
            },
            scales: {
                x: {
                    type: 'linear', reverse: reverseX,
                    title: { display: true, text: xLabel, color: '#64748b', font: { size: 10 } },
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: { color: '#64748b', font: { size: 9 }, maxTicksLimit: 8 },
                    border: { color: 'rgba(255,255,255,0.08)' }
                },
                y: {
                    title: { display: true, text: yLabel, color: '#64748b', font: { size: 10 } },
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: { color: '#64748b', font: { size: 9 }, maxTicksLimit: 6 },
                    border: { color: 'rgba(255,255,255,0.08)' },
                    beginAtZero: true
                }
            }
        };
    }
    // ---- Gemini API Call with Function Calling (Non-Streaming) ----
    // Tries backend proxy first (/api/ai/chat), then direct Gemini API as fallback
    async function callGeminiAgent(contents, mode) {
        const systemPrompt = buildSystemPrompt(mode);

        const body = {
            system_instruction: { parts: [{ text: systemPrompt }] },
            contents: contents,
            tools: [{ function_declarations: TOOL_DECLARATIONS }],
            tool_config: { function_calling_config: { mode: "AUTO" } },
            generationConfig: {
                temperature: 0.7,
                topP: 0.9,
                topK: 40,
                maxOutputTokens: 2048
            }
        };

        // --- Strategy 1: Try backend proxy (API key stays on server) ---
        let quotaHit = false;
        try {
            const proxyResp = await fetch(`${BACKEND_BASE}/api/v1/ai/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            if (proxyResp.ok) {
                console.log('[NeuroLab] ✅ Connected via backend proxy');
                return await proxyResp.json();
            }

            const proxyErr = await proxyResp.json().catch(() => ({}));
            if (proxyResp.status === 429) {
                lastApiError = 'quota';
                console.warn('[NeuroLab] Quota exceeded — waiting 10s and retrying...');
                quotaHit = true;
                // Wait and retry ONCE instead of burning quota on direct API
                await new Promise(r => setTimeout(r, 10000));
                const retry = await fetch(`${BACKEND_BASE}/api/v1/ai/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });
                if (retry.ok) {
                    console.log('[NeuroLab] ✅ Retry succeeded after wait');
                    return await retry.json();
                }
                // Still failing — throw so we show user-friendly error
                throw new Error('QUOTA_EXCEEDED');
            } else if (proxyResp.status === 403) {
                lastApiError = 'forbidden';
                console.warn('[NeuroLab] Backend proxy: key invalid');
            } else if (proxyResp.status === 503) {
                console.warn('[NeuroLab] Backend has no API key, trying client-side...');
            } else {
                lastApiError = 'backend_error';
                console.warn('[NeuroLab] Backend proxy error:', proxyErr.detail || proxyResp.status);
            }
        } catch (e) {
            if (e.message === 'QUOTA_EXCEEDED') {
                throw new Error('⏳ API quota exceeded. The free Gemini API has a limit — please wait 1-2 minutes and try again. This is normal with the free tier.');
            }
            console.warn('[NeuroLab] Backend proxy unavailable, trying direct API...');
        }

        // Backend handles ALL providers now (Groq → Gemini → OpenRouter → OpenAI)
        // No need for direct API calls from the browser
        return null;
    }

    // ---- AGENT LOOP: The Core Intelligence ----
    // This is what makes it AUTONOMOUS. The loop:
    // 1. Sends user message to Gemini with tool declarations
    // 2. If Gemini returns a function_call, execute it on the backend
    // 3. Send the result back to Gemini
    // 4. Repeat until Gemini returns a text response (not a function call)
    async function runAgentLoop(userMessage, history, mode, msgsContainer, botMsgEl) {
        // Build contents from history
        const contents = [];
        for (const msg of history) {
            contents.push({
                role: msg.role === 'user' ? 'user' : 'model',
                parts: [{ text: msg.text }]
            });
        }
        contents.push({ role: 'user', parts: [{ text: userMessage }] });

        let loops = 0;
        let finalText = '';
        let actionsContainer = null;

        while (loops < MAX_AGENT_LOOPS) {
            loops++;

            const response = await callGeminiAgent(contents, mode);
            if (!response) {
                if (lastApiError === 'quota') {
                    finalText = "⚠️ **Gemini API quota exceeded.** Your key is valid but has hit the free-tier rate limit.\n\n**Fix:** Wait 1-2 minutes and try again, or visit [Google AI Studio](https://aistudio.google.com/apikey) to check your quota.";
                } else if (lastApiError === 'forbidden') {
                    finalText = "🔒 **API key rejected.** Your key may be invalid or the Generative Language API is not enabled.\n\n**Fix:** Go to [Google AI Studio](https://aistudio.google.com/apikey) and create a new key.";
                } else {
                    finalText = "I couldn't connect to the AI. Please check your Gemini API key in ⚙️ settings.";
                }
                break;
            }

            const candidate = response.candidates?.[0];
            if (!candidate) {
                finalText = "No response from AI. Please try again.";
                break;
            }

            const parts = candidate.content?.parts || [];

            // Check if there are function calls
            const functionCalls = parts.filter(p => p.functionCall);
            const textParts = parts.filter(p => p.text);

            if (functionCalls.length > 0) {
                // AI wants to call tools!
                if (!actionsContainer) {
                    actionsContainer = document.createElement('div');
                    actionsContainer.className = 'agent-actions';
                    msgsContainer.insertBefore(actionsContainer, botMsgEl);
                }

                // Add model response to contents (with function calls)
                contents.push({ role: 'model', parts: parts });

                // Execute each function call
                const functionResponses = [];

                for (const fc of functionCalls) {
                    const toolName = fc.functionCall.name;
                    const toolArgs = fc.functionCall.args || {};

                    // Show action card
                    const card = createActionCard(toolName, toolArgs);
                    actionsContainer.appendChild(card);
                    msgsContainer.scrollTop = msgsContainer.scrollHeight;

                    // Execute the tool
                    let toolResult;
                    try {
                        toolResult = await executeToolOnBackend(toolName, toolArgs);
                        completeActionCard(card, true);

                        // Render inline spectrum/chromatogram chart for instrument tools
                        const chartEl = renderSpectrumChart(toolName, toolResult);
                        if (chartEl) {
                            actionsContainer.appendChild(chartEl);
                            msgsContainer.scrollTop = msgsContainer.scrollHeight;
                        }
                    } catch (e) {
                        toolResult = { error: e.message };
                        completeActionCard(card, false);
                    }

                    functionResponses.push({
                        functionResponse: {
                            name: toolName,
                            response: toolResult
                        }
                    });
                }

                // Send tool results back to Gemini
                contents.push({ role: 'user', parts: functionResponses });

            } else if (textParts.length > 0) {
                // AI returned text — we're done!
                finalText = textParts.map(p => p.text).join('\n');
                break;
            } else {
                finalText = "Agent completed but no response was generated.";
                break;
            }
        }

        if (loops >= MAX_AGENT_LOOPS) {
            finalText += "\n\n⚠️ Agent reached maximum execution steps. Results shown above.";
        }

        return finalText;
    }

    // ---- Offline Knowledge Base (Fallback — 40+ topics) ----
    const KB = [
        // Instruments
        { patterns: ['hplc', 'high performance liquid', 'chromatography liquid'], answer: '**HPLC** (High Performance Liquid Chromatography) separates compounds in a liquid mixture through a column packed with stationary phase. It\'s the gold standard for drug purity testing, assay determination, and dissolution studies.<br><br>Key components: Pump → Injector → Column → Detector → Data System<br><br>Try our <a href="hplc_simulator.html">HPLC simulator</a>! 🔬' },
        { patterns: ['ftir', 'infrared', 'ir spectroscopy', 'ir spectrum'], answer: '**FTIR** (Fourier Transform Infrared) identifies molecules by measuring infrared absorption. Different bonds absorb at characteristic frequencies — this creates a molecular "fingerprint".<br><br>Key regions: 4000-2500 cm⁻¹ (O-H, N-H, C-H), 2500-2000 (triple bonds), 2000-1500 (C=O, C=C), 1500-400 (fingerprint)<br><br>Try the <a href="ftir_simulator.html">FTIR simulator</a>! 🔬' },
        { patterns: ['uv', 'visible', 'uv-vis', 'ultraviolet', 'spectrophotometer'], answer: '**UV-Vis Spectrophotometry** measures how molecules absorb UV (200-400nm) and visible (400-800nm) light. Essential for quantitative analysis using **Beer-Lambert Law: A = εlc**<br><br>Where: A = absorbance, ε = molar absorptivity, l = path length, c = concentration<br><br>Try our <a href="uv_vis_simulator.html">UV-Vis simulator</a>! 🔬' },
        { patterns: ['gc', 'gas chromatography', 'gas chromat'], answer: '**Gas Chromatography (GC)** separates volatile compounds using an inert carrier gas (He, N₂). Compounds partition between a mobile gas phase and stationary liquid/solid phase in the column.<br><br>Key parameters: Column temperature, carrier gas flow rate, injection volume, detector type (FID, TCD, MS)<br><br>Try our <a href="gc_simulator.html">GC simulator</a>! 🔬' },
        { patterns: ['mass spec', 'mass spectrometry', 'ms', 'm/z', 'molecular weight'], answer: '**Mass Spectrometry** measures the mass-to-charge ratio (m/z) of ions. It provides molecular weight and structural information through fragmentation patterns.<br><br>Process: Ionization → Mass Analysis → Detection<br>Common techniques: EI, ESI, MALDI, APCI<br><br>Try our <a href="mass_spec_simulator.html">Mass Spec simulator</a>! 🔬' },
        { patterns: ['polarimeter', 'polarimetry', 'optical rotation', 'chiral'], answer: '**Polarimetry** measures the optical rotation of chiral compounds. Specific rotation [α] = (observed α) / (l × c). Essential for sugar analysis and enantiomeric purity.<br><br>Dextrorotatory (+): rotates clockwise<br>Levorotatory (−): rotates counter-clockwise<br><br>Try our <a href="polarimeter_simulator.html">Polarimeter simulator</a>! 🔬' },
        { patterns: ['particle size', 'psa', 'laser diffraction', 'particle'], answer: '**Particle Size Analysis (PSA)** is critical for drug formulation. Smaller particles = larger surface area = faster dissolution. Methods include laser diffraction, DLS, and sieve analysis.<br><br>Key terms: D10, D50 (median), D90, span = (D90-D10)/D50<br><br>Explore our <a href="psa_simulator.html">PSA simulator</a>! 🔬' },

        // Beer-Lambert Law
        { patterns: ['beer lambert', 'beer\'s law', 'absorbance equation', 'a = elc'], answer: '**Beer-Lambert Law: A = εlc**<br><br>• **A** = Absorbance (no units)<br>• **ε** = Molar absorptivity (L·mol⁻¹·cm⁻¹)<br>• **l** = Path length (cm, usually 1 cm)<br>• **c** = Concentration (mol/L)<br><br>Linear only at low concentrations. Deviations occur at high concentrations or with fluorescence.' },

        // Drug analysis
        { patterns: ['paracetamol', 'acetaminophen', 'tylenol'], answer: '**Paracetamol (Acetaminophen)** — C₈H₉NO₂, MW 151.16<br><br>• UV-Vis: λmax = 243 nm<br>• FTIR: O-H stretch ~3300, C=O ~1650, aromatic C=C ~1600 cm⁻¹<br>• HPLC: Reverse-phase C18, mobile phase MeOH:Water<br>• Use: Analgesic & Antipyretic<br><br>Try: "Analyze paracetamol" to see full spectral data!' },
        { patterns: ['aspirin', 'acetylsalicylic'], answer: '**Aspirin (Acetylsalicylic Acid)** — C₉H₈O₄, MW 180.16<br><br>• UV-Vis: λmax = 227 nm, 275 nm<br>• FTIR: C=O ester ~1750, C=O acid ~1680, O-H ~3000 cm⁻¹<br>• IP assay: titration with NaOH<br>• Use: Analgesic, Antipyretic, Anti-inflammatory, Antiplatelet' },
        { patterns: ['ibuprofen'], answer: '**Ibuprofen** — C₁₃H₁₈O₂, MW 206.28<br><br>• UV-Vis: λmax = 222 nm, 264 nm<br>• Chiral compound (S-enantiomer is active)<br>• BCS Class II (low solubility, high permeability)<br>• Use: NSAID — anti-inflammatory, analgesic' },
        { patterns: ['caffeine', 'coffee'], answer: '**Caffeine** — C₈H₁₀N₄O₂, MW 194.19<br><br>• UV-Vis: λmax = 273 nm<br>• FTIR: C=O stretch ~1700, C=N ~1550 cm⁻¹<br>• Xanthine derivative (purine alkaloid)<br>• Use: CNS stimulant, found in tea & coffee' },

        // Theory
        { patterns: ['resolution', 'rs', 'separation factor'], answer: '**Resolution (Rs)** measures how well two peaks are separated.<br><br>Rs = 2(tR₂ - tR₁) / (W₁ + W₂)<br><br>• Rs < 1.0 = incomplete separation<br>• Rs = 1.5 = baseline separation<br>• Rs > 2.0 = excellent separation<br><br>Improve Rs by: optimizing column, mobile phase, temperature, or flow rate.' },
        { patterns: ['retention time', 'rt', 'retention factor'], answer: '**Retention Time (tR)** is the time it takes for a compound to travel through the column and reach the detector.<br><br>Retention Factor: k = (tR - t₀) / t₀<br><br>Affected by: column type, mobile phase composition, temperature, and flow rate.' },
        { patterns: ['theoretical plate', 'plate number', 'efficiency'], answer: '**Theoretical Plates (N)** measure column efficiency.<br><br>N = 16(tR/W)² or N = 5.54(tR/W₁/₂)²<br><br>More plates = sharper peaks = better separation. HETP = L/N (Height Equivalent to a Theoretical Plate).' },
        { patterns: ['tailing', 'peak tailing', 'asymmetry'], answer: '**Peak Tailing** occurs when the tail of a peak is drawn out. Causes:<br><br>• Dead volume in connections<br>• Column degradation<br>• Overloading<br>• Secondary interactions with silanol groups<br><br>Fix: Replace column, reduce injection volume, use end-capped columns.' },
        { patterns: ['baseline', 'noise', 'drift'], answer: '**Baseline Issues in Chromatography:**<br><br>• **Noise**: Random fluctuations — caused by detector electronics, air bubbles<br>• **Drift**: Gradual baseline change — caused by column bleed, mobile phase changes<br>• **Spikes**: Sharp artifacts — air bubbles, electrical interference<br><br>Fix: Degas mobile phase, clean/replace lamp, check connections.' },

        // Pharmacopoeia
        { patterns: ['usp', 'pharmacopoeia', 'ip', 'bp', 'monograph'], answer: '**Pharmacopoeia** = Official standard reference for drug quality.<br><br>• **USP** (United States Pharmacopoeia)<br>• **IP** (Indian Pharmacopoeia)<br>• **BP** (British Pharmacopoeia)<br>• **EP** (European Pharmacopoeia)<br><br>Monographs specify: Identification tests, Assay methods, Impurity limits, Dissolution specs.' },
        { patterns: ['validation', 'method validation', 'ich'], answer: '**Analytical Method Validation (ICH Q2):**<br><br>• **Specificity** — Can it measure the analyte specifically?<br>• **Linearity** — Linear range with R² > 0.999<br>• **Accuracy** — Recovery 98-102%<br>• **Precision** — RSD < 2%<br>• **LOD/LOQ** — Detection & Quantitation limits<br>• **Robustness** — Small changes don\'t affect results' },

        // Formulation
        { patterns: ['dissolution', 'bcs', 'biopharmaceutics'], answer: '**BCS (Biopharmaceutics Classification System):**<br><br>• **Class I**: High solubility, High permeability ✅<br>• **Class II**: Low solubility, High permeability (e.g., Ibuprofen)<br>• **Class III**: High solubility, Low permeability<br>• **Class IV**: Low solubility, Low permeability ❌<br><br>Dissolution testing ensures drug release meets pharmacopeial standards.' },

        // Troubleshooting
        { patterns: ['troubleshoot', 'problem', 'error', 'fix', 'issue'], answer: '**Common Instrument Issues & Fixes:**<br><br>🔧 **No peaks**: Check injection, detector lamp, mobile phase<br>🔧 **Broad peaks**: Old column, wrong flow rate, temperature<br>🔧 **Ghost peaks**: Contaminated mobile phase, dirty column<br>🔧 **Pressure issues**: Blocked frit, air bubbles, worn seals<br>🔧 **Noisy baseline**: Degas solvent, replace lamp, check electronics' },

        // Greetings & help
        { patterns: ['hello', 'hi', 'hey', 'good morning', 'good evening'], answer: 'Hello! 👋 I\'m <strong>NeuroLab AI</strong>, your autonomous lab assistant. I can run instruments, analyze compounds, and help you learn!<br><br>📚 <em>Currently in offline mode — I\'m answering from my built-in pharma knowledge base.</em><br><br>Try asking about: HPLC, UV-Vis, Beer-Lambert Law, paracetamol, or troubleshooting!' },
        { patterns: ['help', 'what can you', 'capabilities'], answer: '<strong>NeuroLab AI Capabilities:</strong><br><br>🔬 Run 7 instruments (UV-Vis, FTIR, HPLC, GC, MS, Polarimeter, PSA)<br>🔍 Search 20+ pharmaceutical compounds<br>🧬 Identify unknowns from spectral data<br>⚖️ Compare compounds side-by-side<br>📊 Generate analysis reports<br>🎯 Recommend study topics<br><br>📚 <em>Offline mode: I answer from my pharma knowledge base. Connect an API key for full autonomous agent mode!</em>' },
        { patterns: ['thank', 'thanks', 'great', 'awesome', 'perfect'], answer: 'You\'re welcome! 😊 Happy to help with your pharma studies. Ask me anything! 🔬' },

        // Study/learn
        { patterns: ['study', 'learn', 'start', 'beginner', 'where to begin'], answer: '**Recommended Learning Path:**<br><br>1️⃣ <a href="uv_vis_simulator.html">UV-Vis</a> — Start here! Learn Beer-Lambert Law<br>2️⃣ <a href="ftir_simulator.html">FTIR</a> — Molecular fingerprinting<br>3️⃣ <a href="hplc_simulator.html">HPLC</a> — Drug separation & purity<br>4️⃣ <a href="gc_simulator.html">GC</a> — Volatile compound analysis<br>5️⃣ <a href="mass_spec_simulator.html">Mass Spec</a> — Molecular weight determination<br>6️⃣ <a href="polarimeter_simulator.html">Polarimetry</a> — Chiral analysis<br><br>Check the <a href="curriculum.html">PCI Curriculum</a> for experiment mapping!' },

        // Concentration
        { patterns: ['concentration', 'dilution', 'molarity', 'serial dilution'], answer: '**Dilution Formula: C₁V₁ = C₂V₂**<br><br>• C₁ = initial concentration<br>• V₁ = initial volume<br>• C₂ = final concentration<br>• V₂ = final volume<br><br>**Molarity (M)** = moles of solute / liters of solution<br>**Serial Dilution**: Each step dilutes by a fixed factor (e.g., 1:10)' },

        // Column types
        { patterns: ['column', 'c18', 'c8', 'stationary phase', 'mobile phase'], answer: '**HPLC Column Types:**<br><br>• **C18 (ODS)** — Most common, nonpolar, for reverse-phase<br>• **C8** — Shorter chain, less retention<br>• **Phenyl** — π-π interactions for aromatics<br>• **NH₂/CN** — Normal phase, polar compounds<br>• **Chiral** — Enantiomer separation<br><br>**Mobile Phase**: MeOH:Water or ACN:Water (reverse-phase)' },
    ];

    function findKBAnswer(input) {
        const lower = input.toLowerCase();
        let bestMatch = null, bestScore = 0;
        for (const entry of KB) {
            let score = 0;
            for (const pattern of entry.patterns) {
                if (lower.includes(pattern)) score += pattern.length;
            }
            if (score > bestScore) { bestScore = score; bestMatch = entry; }
        }
        return bestMatch ? bestMatch.answer : "I can help with pharma instruments, run simulations, and identify compounds. Try asking me to <strong>\"analyze paracetamol\"</strong> or <strong>\"compare aspirin vs caffeine\"</strong>! 🔬";
    }

    // ---- Voice Input ----
    function setupVoiceInput(micBtn, inputEl) {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            micBtn.style.display = 'none';
            return null;
        }
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        let isListening = false;

        micBtn.addEventListener('click', () => {
            if (isListening) { recognition.stop(); isListening = false; micBtn.classList.remove('listening'); }
            else { recognition.start(); isListening = true; micBtn.classList.add('listening'); }
        });
        recognition.onresult = (e) => { let t = ''; for (let i = e.resultIndex; i < e.results.length; i++) t += e.results[i][0].transcript; inputEl.value = t; };
        recognition.onend = () => { isListening = false; micBtn.classList.remove('listening'); };
        recognition.onerror = () => { isListening = false; micBtn.classList.remove('listening'); };
        return recognition;
    }

    // ---- Export Chat ----
    function exportChat(history, format) {
        const ts = new Date().toISOString().slice(0, 10);
        let content = `# SimuPharma AI Lab Notes\n_Exported on ${ts}_\n\n---\n\n`;
        for (const msg of history) {
            content += msg.role === 'user' ? `## 🧑‍🎓 Question\n${msg.text}\n\n` : `## 🤖 SimuBot\n${msg.text}\n\n---\n\n`;
        }
        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = `SimuPharma_AI_Notes_${ts}.md`;
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    // ---- Build UI ----
    async function init() {
        const chatMode = localStorage.getItem(LS_KEY_MODE) || 'beginner';
        // Check backend first, then fall back to client key
        const backendReady = await checkBackendAI();
        const hasApiKey = backendReady || !!localStorage.getItem(LS_KEY_API);
        let conversationHistory = [];
        let settingsOpen = false;
        let isProcessing = false;

        const SUGGESTIONS = [
            '🔬 Analyze paracetamol',
            '⚖️ Compare aspirin vs ibuprofen',
            '🧬 Identify unknown compound',
            '🎯 What should I study next?',
            '🔍 Search for antibiotics',
            '📊 Full drug analysis of caffeine'
        ];

        // Toggle button
        const toggle = document.createElement('button');
        toggle.className = 'assistant-toggle';
        toggle.innerHTML = '<i class="fas fa-brain"></i><span class="badge-count">1</span>';
        toggle.setAttribute('aria-label', 'Open NeuroLab AI Agent');
        document.body.appendChild(toggle);

        // Chat window
        const win = document.createElement('div');
        win.className = 'assistant-window';
        win.innerHTML = `
            <div class="assistant-header">
                <div class="assistant-avatar"><i class="fas fa-brain"></i></div>
                <div class="assistant-header-info">
                    <h4>NeuroLab AI — Autonomous Agent</h4>
                    <p><span class="online-dot"></span> <span class="ai-status">${hasApiKey ? (backendReady ? '🧠 Autonomous Mode · Server AI' : '🧠 Autonomous Mode · Gemini') : 'Offline Mode'}</span></p>
                </div>
                <div class="header-actions">
                    <button class="header-btn" id="assistant-export" aria-label="Export" title="Export as study notes"><i class="fas fa-download"></i></button>
                    <button class="header-btn" id="assistant-clear" aria-label="Clear" title="Clear conversation"><i class="fas fa-trash-alt"></i></button>
                    <button class="header-btn" id="assistant-settings" aria-label="Settings" title="API Settings"><i class="fas fa-cog"></i></button>
                </div>
            </div>
            <div class="assistant-settings-panel" id="settings-panel">
                <div class="settings-group">
                    <label for="gemini-key-input"><i class="fas fa-key"></i> Gemini API Key</label>
                    <div class="settings-input-row">
                        <input type="password" id="gemini-key-input" placeholder="Enter your Gemini API key..." value="${localStorage.getItem(LS_KEY_API) || ''}" autocomplete="off">
                        <button id="save-key-btn" class="settings-save-btn"><i class="fas fa-check"></i></button>
                    </div>
                    <small>Your key stays in your browser. <a href="https://aistudio.google.com/apikey" target="_blank" rel="noopener">Get a free key →</a></small>
                </div>
                <div class="settings-group">
                    <label><i class="fas fa-graduation-cap"></i> Difficulty Mode</label>
                    <div class="mode-toggle">
                        <button class="mode-btn ${chatMode === 'beginner' ? 'active' : ''}" data-mode="beginner"><i class="fas fa-seedling"></i> Beginner</button>
                        <button class="mode-btn ${chatMode === 'advanced' ? 'active' : ''}" data-mode="advanced"><i class="fas fa-atom"></i> Advanced</button>
                    </div>
                </div>
            </div>
            ${!hasApiKey ? '<div class="offline-banner" id="offline-banner"><i class="fas fa-info-circle"></i> Offline mode — <button id="setup-key-btn">set API key</button> to unlock autonomous AI agent</div>' : ''}
            <div class="assistant-messages" id="assistant-msgs">
                <div class="msg bot">
                    ${hasApiKey ? '🧠 <strong>NeuroLab AI Active</strong><br>I can <em>run instruments</em>, analyze compounds, and identify unknowns autonomously. Try:<br><br>• <strong>"Analyze paracetamol"</strong> — I\'ll run UV-Vis, FTIR, and MS<br>• <strong>"Compare aspirin vs caffeine"</strong> — Side-by-side analysis<br>• <strong>"Identify a compound with peak at 243nm"</strong> — ML matching' : '👋 I\'m <strong>NeuroLab AI</strong>. Set up an API key in ⚙️ to unlock <strong>autonomous agent</strong> capabilities — I can run instruments, identify unknowns, and more!'}
                </div>
            </div>
            <div class="assistant-suggestions" id="assistant-suggestions"></div>
            <div class="assistant-input">
                <button id="assistant-mic" class="mic-btn" aria-label="Voice input"><i class="fas fa-microphone"></i></button>
                <input type="text" id="assistant-input" placeholder="Ask me to run an experiment..." autocomplete="off">
                <button id="assistant-send" aria-label="Send"><i class="fas fa-paper-plane"></i></button>
            </div>
        `;
        document.body.appendChild(win);

        // References
        const msgs = document.getElementById('assistant-msgs');
        const input = document.getElementById('assistant-input');
        const sendBtn = document.getElementById('assistant-send');
        const suggestionsContainer = document.getElementById('assistant-suggestions');
        const badge = toggle.querySelector('.badge-count');
        const settingsBtn = document.getElementById('assistant-settings');
        const settingsPanel = document.getElementById('settings-panel');
        const saveKeyBtn = document.getElementById('save-key-btn');
        const keyInput = document.getElementById('gemini-key-input');
        const clearBtn = document.getElementById('assistant-clear');
        const exportBtn = document.getElementById('assistant-export');
        const micBtn = document.getElementById('assistant-mic');
        const aiStatusEl = win.querySelector('.ai-status');
        const setupKeyBtn = document.getElementById('setup-key-btn');

        setupVoiceInput(micBtn, input);

        // Mode toggle
        win.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                win.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                localStorage.setItem(LS_KEY_MODE, btn.dataset.mode);
            });
        });

        // Render suggestions
        function renderSuggestions() {
            suggestionsContainer.innerHTML = SUGGESTIONS.map(s =>
                `<button class="suggestion-chip">${s}</button>`
            ).join('');
            suggestionsContainer.querySelectorAll('.suggestion-chip').forEach(chip => {
                chip.addEventListener('click', () => sendMessage(chip.textContent));
            });
        }
        renderSuggestions();

        // Toggle chat
        toggle.addEventListener('click', () => {
            const isOpen = win.classList.contains('open');
            win.classList.toggle('open');
            toggle.classList.toggle('open');
            if (!isOpen) { badge.style.display = 'none'; input.focus(); }
        });

        // Settings
        settingsBtn.addEventListener('click', () => {
            settingsOpen = !settingsOpen;
            settingsPanel.classList.toggle('open', settingsOpen);
        });
        if (setupKeyBtn) setupKeyBtn.addEventListener('click', () => {
            settingsOpen = true; settingsPanel.classList.add('open');
        });

        // Save key
        saveKeyBtn.addEventListener('click', () => {
            const key = keyInput.value.trim();
            if (key) {
                localStorage.setItem(LS_KEY_API, key);
                aiStatusEl.textContent = '🧠 Autonomous Mode · Gemini';
                const banner = document.getElementById('offline-banner');
                if (banner) banner.remove();
                saveKeyBtn.innerHTML = '<i class="fas fa-check" style="color:#4ADE80"></i>';
                setTimeout(() => { saveKeyBtn.innerHTML = '<i class="fas fa-check"></i>'; }, 1500);
            } else {
                localStorage.removeItem(LS_KEY_API);
                aiStatusEl.textContent = 'Offline Mode';
            }
        });

        // Clear
        clearBtn.addEventListener('click', () => {
            conversationHistory = [];
            msgs.innerHTML = '<div class="msg bot">Conversation cleared! 🧹 Ask me to run an experiment or analyze a compound.</div>';
            renderSuggestions();
        });

        // Export
        exportBtn.addEventListener('click', () => {
            if (conversationHistory.length === 0) {
                msgs.appendChild(Object.assign(document.createElement('div'), { className: 'msg bot', textContent: 'No conversation to export yet.' }));
                return;
            }
            exportChat(conversationHistory, 'markdown');
        });

        // ---- Voice Auto-Speak Toggle ----
        let voiceAutoSpeak = localStorage.getItem('neurolab_voice') !== 'off';

        function autoSpeak(text) {
            if (!voiceAutoSpeak || typeof VoiceEngine === 'undefined') return;
            const avatar = win.querySelector('.assistant-avatar');
            if (avatar) avatar.classList.add('speaking');
            VoiceEngine.speak(text).then(() => {
                if (avatar) avatar.classList.remove('speaking');
            });
        }

        // ---- VOICE COMMAND ENGINE — 20+ executable commands ----
        const VOICE_COMMANDS = [
            // Open simulators
            { patterns: ['open hplc', 'launch hplc', 'go to hplc', 'start hplc'], reply: 'Opening the HPLC simulator for you!', action: () => window.location.href = 'hplc_simulator.html' },
            { patterns: ['open ftir', 'launch ftir', 'go to ftir', 'start ftir', 'open infrared'], reply: 'Launching the FTIR instrument now!', action: () => window.location.href = 'ftir_simulator.html' },
            { patterns: ['open uv', 'launch uv', 'go to uv', 'open spectrophotometer'], reply: 'Opening the UV-Vis spectrophotometer!', action: () => window.location.href = 'uv_vis_simulator.html' },
            { patterns: ['open gc', 'launch gc', 'gas chromatography', 'open gas chromat'], reply: 'Starting the Gas Chromatography simulator!', action: () => window.location.href = 'gc_simulator.html' },
            { patterns: ['open mass spec', 'launch mass spec', 'go to mass spec'], reply: 'Loading the Mass Spectrometer!', action: () => window.location.href = 'mass_spec_simulator.html' },
            { patterns: ['open polarimeter', 'launch polarimeter'], reply: 'Opening the Polarimeter for you!', action: () => window.location.href = 'polarimeter_simulator.html' },
            { patterns: ['open psa', 'particle size'], reply: 'Launching Particle Size Analyzer!', action: () => window.location.href = 'psa_simulator.html' },
            // Navigate pages
            { patterns: ['go to instruments', 'show instruments', 'all instruments'], reply: 'Here are all your instruments!', action: () => window.location.href = 'instruments.html' },
            { patterns: ['go to curriculum', 'show curriculum', 'pci curriculum'], reply: 'Showing the PCI curriculum and experiment mapping!', action: () => window.location.href = 'curriculum.html' },
            { patterns: ['go to pricing', 'show pricing', 'show plans'], reply: 'Here are the pricing plans!', action: () => window.location.href = 'pricing.html' },
            { patterns: ['go home', 'go to home', 'home page', 'back to home'], reply: 'Taking you back to the homepage!', action: () => window.location.href = 'index.html' },
            { patterns: ['go to dashboard', 'show dashboard', 'my dashboard'], reply: 'Scrolling to your dashboard!', action: () => { const el = document.getElementById('dashboard') || document.querySelector('.dashboard-section'); if (el) el.scrollIntoView({ behavior: 'smooth' }); } },
            { patterns: ['go to quiz', 'take quiz', 'start quiz', 'viva'], reply: 'Opening the quiz section!', action: () => window.location.href = 'quiz.html' },
            // XP and progress
            { patterns: ['show my xp', 'my xp', 'my progress', 'how much xp', 'my level', 'my score'], reply: () => { const xp = parseInt(localStorage.getItem('simupharma_xp') || '0'); const lvl = parseInt(localStorage.getItem('simupharma_level') || '1'); return `You have ${xp} XP and you're at Level ${lvl}. Keep experimenting to level up!`; }, action: () => { } },
            { patterns: ['show leaderboard', 'leaderboard', 'rankings'], reply: 'Showing the leaderboard!', action: () => { if (typeof EdTech !== 'undefined' && EdTech.showLeaderboard) EdTech.showLeaderboard(); } },
            { patterns: ['my badges', 'show badges'], reply: () => { const badges = JSON.parse(localStorage.getItem('simupharma_badges') || '[]'); return badges.length ? `You've earned ${badges.length} badges: ${badges.join(', ')}. Keep going!` : `You haven't earned any badges yet. Try running some experiments!`; }, action: () => { } },
            { patterns: ['my streak', 'daily streak'], reply: () => { const streak = parseInt(localStorage.getItem('simupharma_streak') || '0'); return streak > 0 ? `Your daily streak is ${streak} days! Keep it going! 🔥` : `Start your first daily streak by using SimuPharma every day!`; }, action: () => { } },
            // Guided teacher
            { patterns: ['start guided', 'guided experiment', 'teach me', 'start tutorial', 'start teacher'], reply: 'Starting the guided experiment!', action: () => { if (typeof GuidedTeacher !== 'undefined') GuidedTeacher.toggle(); } },
            // Voice control
            { patterns: ['mute', 'stop talking', 'be quiet', 'shut up', 'silence'], reply: null, action: () => { voiceAutoSpeak = false; localStorage.setItem('neurolab_voice', 'off'); if (typeof VoiceEngine !== 'undefined') VoiceEngine.stop(); } },
            { patterns: ['unmute', 'start talking', 'speak', 'voice on'], reply: "I'm back! How can I help you today?", action: () => { voiceAutoSpeak = true; localStorage.setItem('neurolab_voice', 'on'); } },
        ];

        function matchVoiceCommand(input) {
            const lower = input.toLowerCase().replace(/[^a-z0-9\s]/g, '');
            for (const cmd of VOICE_COMMANDS) {
                for (const pattern of cmd.patterns) {
                    if (lower.includes(pattern)) return cmd;
                }
            }
            return null;
        }

        // ---- SEND MESSAGE (Agent Mode + Voice Commands) ----
        async function sendMessage(text) {
            text = text.trim();
            if (!text || isProcessing) return;
            isProcessing = true;

            // User message
            const userMsg = document.createElement('div');
            userMsg.className = 'msg user';
            userMsg.textContent = text;
            msgs.appendChild(userMsg);
            input.value = '';
            msgs.scrollTop = msgs.scrollHeight;
            suggestionsContainer.innerHTML = '';
            conversationHistory.push({ role: 'user', text });

            // ---- Check for voice commands FIRST ----
            const cmd = matchVoiceCommand(text);
            if (cmd) {
                const reply = typeof cmd.reply === 'function' ? cmd.reply() : cmd.reply;
                const botMsg = document.createElement('div');
                botMsg.className = 'msg bot ai-response';
                if (reply) {
                    botMsg.innerHTML = `🗣️ ${reply}`;
                    autoSpeak(reply);
                } else {
                    botMsg.innerHTML = '🔇 Voice muted.';
                }
                appendVoiceBtn(botMsg);
                msgs.appendChild(botMsg);
                msgs.scrollTop = msgs.scrollHeight;
                conversationHistory.push({ role: 'assistant', text: reply || 'Muted' });
                // Execute action after a small delay (so voice starts first)
                if (cmd.action) setTimeout(() => cmd.action(), reply ? 1500 : 300);
                isProcessing = false;
                return;
            }

            // ---- INSTANT CHART INTERCEPTOR ----
            // Detects instrument keywords in user message, directly runs tool + renders chart.
            // This bypasses Gemini function-calling which was unreliable.
            (async () => {
                const lower = text.toLowerCase();
                const COMPOUNDS = ['paracetamol','aspirin','ibuprofen','amoxicillin','ciprofloxacin',
                    'metformin','ranitidine','caffeine','diclofenac','atorvastatin','omeprazole',
                    'amlodipine','losartan','ascorbic_acid','ascorbic acid','chloramphenicol',
                    'sulfamethoxazole','phenol','benzocaine','lidocaine','dextrose','sucrose'];

                // Map keyword patterns → tool names
                const INSTRUMENT_MAP = [
                    { keys: ['uv-vis','uv vis','uvvis','ultraviolet','spectrophotom','absorbance'], tool: 'run_uvvis' },
                    { keys: ['ftir','infrared','ir spectrum','wavenumber','transmittance'], tool: 'run_ftir' },
                    { keys: ['hplc','high performance liquid','chromatogram','retention time','peak area'], tool: 'run_hplc' },
                    { keys: ['gc ','gas chrom','gas chromatog'], tool: 'run_gc' },
                    { keys: ['mass spec','mass spect','fragmentation','m/z','molecular ion'], tool: 'run_mass_spec' },
                    { keys: ['psa','particle size','size distribution','d50','d90'], tool: 'run_psa' },
                    { keys: ['polarim','optical rotation','specific rotation','[α]'], tool: 'run_polarimeter' },
                ];

                // Detect tool
                let detectedTool = null;
                for (const inst of INSTRUMENT_MAP) {
                    if (inst.keys.some(k => lower.includes(k))) { detectedTool = inst.tool; break; }
                }

                // Detect compound
                let detectedCompound = null;
                for (const c of COMPOUNDS) {
                    if (lower.includes(c.toLowerCase())) { detectedCompound = c.replace(' ','_'); break; }
                }

                // Generic "analyze" intent → default to UV-Vis
                if (!detectedTool && (lower.includes('analyz') || lower.includes('run') || lower.includes('test')) && detectedCompound) {
                    detectedTool = 'run_uvvis';
                }
                // "full analysis" → run UV-Vis + FTIR + HPLC
                const isFullAnalysis = lower.includes('full') || lower.includes('complete') || (lower.includes('analyz') && !lower.includes('uv') && !lower.includes('ftir') && !lower.includes('hplc'));

                if (detectedTool && detectedCompound) {
                    const toolsToRun = isFullAnalysis
                        ? ['run_uvvis', 'run_ftir', 'run_hplc']
                        : [detectedTool];

                    // Create a container for the charts that will be inserted before botMsg
                    const chartsWrap = document.createElement('div');
                    chartsWrap.className = 'agent-actions';
                    msgs.appendChild(chartsWrap);

                    for (const toolName of toolsToRun) {
                        try {
                            const card = createActionCard(toolName, { compound_id: detectedCompound });
                            chartsWrap.appendChild(card);
                            msgs.scrollTop = msgs.scrollHeight;

                            const result = await executeToolOnBackend(toolName, { compound_id: detectedCompound });
                            completeActionCard(card, !result?.error);

                            const chartEl = renderSpectrumChart(toolName, result);
                            if (chartEl) {
                                chartsWrap.appendChild(chartEl);
                                msgs.scrollTop = msgs.scrollHeight;
                            }
                        } catch(e) { /* silent — let Gemini text response handle failure messaging */ }
                    }
                }
            })();

            // Bot message placeholder
            const botMsg = document.createElement('div');
            botMsg.className = 'msg bot ai-response';

            const clientKey = localStorage.getItem(LS_KEY_API);
            const canUseAI = backendAiAvailable || !!clientKey;

            if (canUseAI) {
                // Show thinking indicator
                const thinking = document.createElement('div');
                thinking.className = 'msg bot agent-thinking';
                thinking.innerHTML = '<span class="agent-think-anim">🧠</span> <em>Thinking & planning...</em>';
                msgs.appendChild(thinking);
                msgs.scrollTop = msgs.scrollHeight;

                try {
                    const result = await runAgentLoop(
                        text,
                        conversationHistory.slice(0, -1),
                        localStorage.getItem(LS_KEY_MODE) || 'beginner',
                        msgs,
                        botMsg
                    );

                    thinking.remove();
                    botMsg.innerHTML = renderMarkdown(result);
                    appendVoiceBtn(botMsg);
                    msgs.appendChild(botMsg);
                    msgs.scrollTop = msgs.scrollHeight;
                    // Auto-speak the AI response
                    autoSpeak(result);

                    conversationHistory.push({ role: 'assistant', text: result });
                    if (conversationHistory.length > MAX_HISTORY * 2) {
                        conversationHistory = conversationHistory.slice(-MAX_HISTORY * 2);
                    }

                    setTimeout(renderSuggestions, 800);
                } catch (e) {
                    thinking.remove();
                    console.error('Agent error:', e);
                    let errMsg = 'Sorry, I encountered an error. ';
                    if (lastApiError === 'quota') errMsg += '⚠️ API quota exceeded — wait a minute and try again, or use a different API key.';
                    else if (lastApiError === 'forbidden') errMsg += '🔑 API key is invalid. Check your key in ⚙️ settings.';
                    else errMsg += 'Please try again. If the issue persists, check your API key in ⚙️ settings.';
                    botMsg.innerHTML = renderMarkdown(errMsg);
                    msgs.appendChild(botMsg);
                }
            } else {
                // Offline fallback
                const delay = 400 + Math.random() * 400;
                setTimeout(() => {
                    const answer = findKBAnswer(text);
                    botMsg.innerHTML = answer;
                    appendVoiceBtn(botMsg);
                    msgs.appendChild(botMsg);
                    msgs.scrollTop = msgs.scrollHeight;
                    autoSpeak(botMsg.textContent);
                    conversationHistory.push({ role: 'assistant', text: botMsg.textContent });
                    setTimeout(renderSuggestions, 500);
                }, delay);
            }

            isProcessing = false;
        }

        // ---- Voice read-aloud on bot messages ----
        function appendVoiceBtn(msgEl) {
            const btn = document.createElement('button');
            btn.className = 'msg-voice-btn';
            btn.innerHTML = '<i class="fas fa-volume-up"></i>';
            btn.title = 'Read aloud';
            btn.addEventListener('click', () => {
                if (typeof VoiceEngine !== 'undefined') {
                    if (window.speechSynthesis.speaking) {
                        window.speechSynthesis.cancel();
                        btn.innerHTML = '<i class="fas fa-volume-up"></i>';
                        btn.classList.remove('speaking');
                    } else {
                        const text = msgEl.textContent || '';
                        VoiceEngine.speak(text);
                        btn.innerHTML = '<i class="fas fa-stop"></i>';
                        btn.classList.add('speaking');
                        // Reset icon when done
                        const check = setInterval(() => {
                            if (!window.speechSynthesis.speaking) {
                                clearInterval(check);
                                btn.innerHTML = '<i class="fas fa-volume-up"></i>';
                                btn.classList.remove('speaking');
                            }
                        }, 500);
                    }
                }
            });
            msgEl.appendChild(btn);
        }

        sendBtn.addEventListener('click', () => sendMessage(input.value));
        input.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendMessage(input.value); });
    }

    // Start when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
