/**
 * SimuPharma Particle Size Analyzer Digital Twin v2.0
 * Log-normal distribution simulation with D-values, span, SSA, fault modes
 */
document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    const MATERIALS = {
        Lactose: { name: 'Lactose Monohydrate', d50: 60, sigma: 0.45, ri: 1.533, density: 1.54, category: 'Excipient' },
        MCC: { name: 'Microcrystalline Cellulose', d50: 90, sigma: 0.55, ri: 1.544, density: 1.50, category: 'Excipient' },
        Paracetamol_Micronized: { name: 'Micronized Paracetamol', d50: 5, sigma: 0.40, ri: 1.620, density: 1.29, category: 'API' },
        Starch: { name: 'Corn Starch', d50: 15, sigma: 0.35, ri: 1.530, density: 1.50, category: 'Excipient' },
        API_Coarse: { name: 'Coarse API Powder', d50: 150, sigma: 0.50, ri: 1.600, density: 1.40, category: 'API' },
        Magnesium_Stearate: { name: 'Magnesium Stearate', d50: 8, sigma: 0.50, ri: 1.480, density: 1.04, category: 'Lubricant' },
        Silica: { name: 'Colloidal Silica', d50: 0.02, sigma: 0.30, ri: 1.458, density: 2.20, category: 'Glidant' },
        Emulsion: { name: 'Lipid Emulsion', d50: 0.3, sigma: 0.25, ri: 1.460, density: 0.92, category: 'Dosage Form' },
        Granules: { name: 'Wet Granulation', d50: 300, sigma: 0.55, ri: 1.544, density: 1.45, category: 'Granule' },
        Spray_Dried: { name: 'Spray-Dried Powder', d50: 25, sigma: 0.40, ri: 1.550, density: 1.35, category: 'Powder' }
    };

    const FAULTS = {
        none: { bimodal: false, noiseMul: 1, shift: 0 },
        bubbles: { bimodal: false, noiseMul: 3, shift: 0, extraPeak: { d50: 800, sigma: 0.6, weight: 0.15 } },
        'dirty-cell': { bimodal: false, noiseMul: 4, shift: 0 },
        agglomeration: { bimodal: true, noiseMul: 1.5, shift: 0, extraPeak: { d50Mul: 5, sigma: 0.4, weight: 0.3 } }
    };

    const STATE = {
        systemReady: false, wizardStep: 1, selectedSample: 'Lactose',
        dispersion: 'wet', pumpSpeed: 2500, opticalModel: 'mie',
        fault: 'none', isMeasuring: false, instantMode: false,
        lastResult: null, difficulty: 'beginner', chartType: 'volume'
    };

    const $ = (s) => document.querySelector(s);
    const $$ = (s) => document.querySelectorAll(s);
    let psaChart = null;

    function toast(msg, type = 'info') {
        const c = $('#toast-container'), t = document.createElement('div');
        const colors = { info: '#3b82f6', success: '#22c55e', warning: '#f59e0b', error: '#ef4444' };
        t.innerHTML = `<i class="fas fa-${({ info: 'info-circle', success: 'check-circle', warning: 'exclamation-triangle', error: 'times-circle' })[type]}"></i><span>${msg}</span>`;
        t.style.cssText = `display:flex;align-items:center;gap:10px;padding:12px 20px;border-radius:10px;margin-bottom:8px;font-size:13px;color:#fff;background:${colors[type]};animation:slideIn .3s ease`;
        c.appendChild(t);
        setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 300); }, 4000);
    }

    function addLog(msg, type = 'info') {
        const log = $('#log-content'); if (!log) return;
        const colors = { info: '#3b82f6', success: '#22c55e', warning: '#f59e0b', error: '#ef4444' };
        log.innerHTML += `<div style="font-size:11px;padding:3px 0;color:${colors[type]};font-family:'JetBrains Mono',monospace"><span style="color:#64748b">[${new Date().toLocaleTimeString()}]</span> ${msg}</div>`;
        log.scrollTop = log.scrollHeight;
    }

    // Log-normal distribution PDF
    function logNormalPDF(x, mu, sigma) {
        if (x <= 0) return 0;
        const lnX = Math.log(x);
        return (1 / (x * sigma * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * Math.pow((lnX - mu) / sigma, 2));
    }

    // Generate particle size distribution
    function generateDistribution() {
        const mat = MATERIALS[STATE.selectedSample];
        if (!mat) return null;
        const fault = FAULTS[STATE.fault];

        const mu = Math.log(mat.d50);
        const sigma = mat.sigma;

        // Generate size bins (logarithmic)
        const minSize = Math.max(0.01, mat.d50 * 0.01);
        const maxSize = mat.d50 * 20;
        const bins = [];
        let size = minSize;
        while (size < maxSize) {
            bins.push(parseFloat(size.toPrecision(3)));
            size *= 1.122; // ~10 bins per decade
        }

        // Calculate volume distribution
        let volumePct = bins.map(s => {
            let vol = logNormalPDF(s, mu, sigma);
            // Add fault effects
            if (fault.extraPeak) {
                if (fault.bimodal) {
                    const agglMu = Math.log(mat.d50 * fault.extraPeak.d50Mul);
                    vol = vol * (1 - fault.extraPeak.weight) +
                        logNormalPDF(s, agglMu, fault.extraPeak.sigma) * fault.extraPeak.weight;
                } else if (fault.extraPeak.d50) {
                    vol += logNormalPDF(s, Math.log(fault.extraPeak.d50), fault.extraPeak.sigma) * fault.extraPeak.weight;
                }
            }
            // Add noise
            vol += (Math.random() - 0.5) * vol * 0.02 * fault.noiseMul;
            return Math.max(0, vol);
        });

        // Normalize to 100%
        const total = volumePct.reduce((a, b) => a + b, 0);
        volumePct = volumePct.map(v => (v / total) * 100);

        // Calculate cumulative
        let cumulative = [];
        let runningSum = 0;
        for (let i = 0; i < volumePct.length; i++) {
            runningSum += volumePct[i];
            cumulative.push(runningSum);
        }

        // Calculate D-values by interpolation
        const findDx = (pct) => {
            for (let i = 1; i < cumulative.length; i++) {
                if (cumulative[i] >= pct) {
                    const frac = (pct - cumulative[i - 1]) / (cumulative[i] - cumulative[i - 1]);
                    return bins[i - 1] + frac * (bins[i] - bins[i - 1]);
                }
            }
            return bins[bins.length - 1];
        };

        const d10 = findDx(10);
        const d50 = findDx(50);
        const d90 = findDx(90);
        const span = (d90 - d10) / d50;

        // Mean, Mode, Uniformity, SSA
        let mean = 0, mode = 0, modeMax = 0;
        for (let i = 0; i < bins.length; i++) {
            mean += bins[i] * volumePct[i] / 100;
            if (volumePct[i] > modeMax) { modeMax = volumePct[i]; mode = bins[i]; }
        }

        // Uniformity (relative width)
        let uniformity = 0;
        for (let i = 0; i < bins.length; i++) {
            uniformity += Math.abs(bins[i] - d50) * volumePct[i] / 100;
        }
        uniformity = uniformity / d50;

        // SSA (specific surface area, m²/g)
        const ssa = 6 / (mat.density * d50 * 1e-4); // simplified

        // Obscuration (simulated)
        const obscuration = 8 + Math.random() * 12;

        return {
            material: mat, bins, volumePct, cumulative, d10, d50, d90,
            span, mean, mode, uniformity, ssa, obscuration,
            // Number distribution (needs volume→number conversion via d³)
            numberPct: volumePct.map((v, i) => {
                const num = v / Math.pow(bins[i], 3);
                return num;
            })
        };
    }

    // Normalize number distribution
    function normalizeNumberPct(data) {
        const total = data.numberPct.reduce((a, b) => a + b, 0);
        return data.numberPct.map(n => (n / total) * 100);
    }

    // Chart
    function initChart() {
        const ctx = $('#hplc-chart');
        if (!ctx) return;
        psaChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [], datasets: [
                    { type: 'bar', label: 'Volume %', data: [], backgroundColor: 'rgba(59,130,246,0.6)', borderColor: '#3b82f6', borderWidth: 1, barPercentage: 1.0, categoryPercentage: 1.0, order: 2 },
                    { type: 'line', label: 'Cumulative %', data: [], borderColor: '#22c55e', borderWidth: 2, pointRadius: 0, fill: false, yAxisID: 'y1', order: 1 }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                animation: { duration: 600 },
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: { display: true, position: 'top', labels: { color: '#94a3b8', font: { size: 11 } } },
                    tooltip: {
                        backgroundColor: 'rgba(15,23,42,0.95)', borderColor: '#334155', borderWidth: 1, padding: 10,
                        callbacks: {
                            title: (ctx) => `Size: ${ctx[0].label} µm`,
                            label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(2)}%`
                        }
                    },
                    zoom: { zoom: { wheel: { enabled: true }, mode: 'x' }, pan: { enabled: true, mode: 'x' } }
                },
                scales: {
                    x: { title: { display: true, text: 'Particle Size (µm)', color: '#94a3b8' }, grid: { color: 'rgba(148,163,184,0.08)' }, ticks: { color: '#64748b', maxTicksLimit: 15, font: { size: 10 } } },
                    y: { title: { display: true, text: 'Volume %', color: '#94a3b8' }, min: 0, grid: { color: 'rgba(148,163,184,0.08)' }, ticks: { color: '#64748b' } },
                    y1: { title: { display: true, text: 'Cumulative %', color: '#22c55e' }, position: 'right', min: 0, max: 100, grid: { drawOnChartArea: false }, ticks: { color: '#22c55e' } }
                }
            }
        });
    }

    function updateChart(data) {
        if (!psaChart || !data) return;
        const labels = data.bins.map(b => b < 1 ? b.toFixed(3) : b < 10 ? b.toFixed(1) : Math.round(b));
        psaChart.data.labels = labels;

        if (STATE.chartType === 'volume') {
            psaChart.data.datasets[0].data = data.volumePct;
            psaChart.data.datasets[0].label = 'Volume %';
            psaChart.data.datasets[1].data = data.cumulative;
            psaChart.options.scales.y.title.text = 'Volume %';
        } else if (STATE.chartType === 'cumulative') {
            psaChart.data.datasets[0].data = data.cumulative;
            psaChart.data.datasets[0].label = 'Cumulative Volume %';
            psaChart.data.datasets[1].data = [];
            psaChart.options.scales.y.title.text = 'Cumulative %';
        } else if (STATE.chartType === 'number') {
            psaChart.data.datasets[0].data = normalizeNumberPct(data);
            psaChart.data.datasets[0].label = 'Number %';
            psaChart.data.datasets[1].data = [];
            psaChart.options.scales.y.title.text = 'Number %';
        }
        psaChart.update();
    }

    function updateResults(data) {
        if (!data) return;
        const fmt = (v) => v < 1 ? v.toFixed(3) : v < 10 ? v.toFixed(2) : v.toFixed(1);
        $('#live-d10').textContent = fmt(data.d10);
        $('#live-d50').textContent = fmt(data.d50);
        $('#live-d90').textContent = fmt(data.d90);
        $('#metric-mean').textContent = fmt(data.mean) + ' µm';
        $('#metric-d50').textContent = fmt(data.d50) + ' µm';
        $('#metric-mode').textContent = fmt(data.mode) + ' µm';
        $('#metric-span').textContent = data.span.toFixed(2);
        $('#metric-uniformity').textContent = data.uniformity.toFixed(3);
        $('#metric-ssa').textContent = data.ssa.toFixed(2) + ' m²/g';
        $('#live-obscuration').textContent = data.obscuration.toFixed(1);
        $('#qs-obscuration').textContent = data.obscuration.toFixed(1) + '%';
        $('#qs-d50').textContent = fmt(data.d50);

        // Spec checks
        const d50Pass = data.d50 >= 10 && data.d50 <= 50;
        const d90Pass = data.d90 < 100;
        const spanPass = data.span < 3.0;
        setSpecResult('spec-d50', d50Pass, fmt(data.d50));
        setSpecResult('spec-d90', d90Pass, fmt(data.d90));
        setSpecResult('spec-span', spanPass, data.span.toFixed(2));

        // Sample info
        const m = data.material;
        $('#sample-name').textContent = m.name;
    }

    function setSpecResult(id, pass, value) {
        const el = document.getElementById(id);
        if (!el) return;
        el.textContent = `${value} ${pass ? '✓' : '✗'}`;
        el.className = `pass-fail ${pass ? 'pass' : 'fail'}`;
    }

    // Wizard
    function goToWizardStep(step) {
        STATE.wizardStep = step;
        $$('.wizard-step').forEach((ws, i) => { ws.classList.toggle('active', i < step); ws.classList.toggle('completed', i < step - 1); });
        $$('.wizard-panel').forEach((wp, i) => wp.classList.toggle('active', i === step - 1));
        $('#wizard-prev-btn').disabled = step <= 1;
        $('#wizard-next-btn').classList.toggle('hidden', step >= 4);
        $('#wizard-finish-btn').classList.toggle('hidden', step < 4);
    }

    function laserOn() {
        $('#btn-laser-on').disabled = true;
        addLog('▶ He–Ne laser ignition (632.8 nm, Class 3R)', 'info');
        addLog('  Gas discharge tube energizing — neon atoms excited by helium collisions', 'info');
        addLog('  Coherent red beam used for Mie scattering / Fraunhofer diffraction', 'info');

        let power = 0;
        let phase = 0;
        const iv = setInterval(() => {
            // Non-linear stabilization mimicking real gas laser
            if (power < 40) power += 6;
            else if (power < 80) power += 3;
            else power += 1;
            if (power > 100) power = 100;
            const mW = (power / 100 * 5).toFixed(1);
            $('#status-power').textContent = mW + ' mW';

            if (power >= 20 && phase === 0) {
                phase = 1;
                addLog('  Plasma ignited — He-Ne population inversion achieved', 'info');
                addLog('  Output power rising: ' + mW + ' mW', 'info');
            }
            if (power >= 60 && phase === 1) {
                phase = 2;
                addLog('  TEM₀₀ mode stabilizing — beam profile Gaussian', 'info');
                addLog('  Beam divergence: < 1 mrad | Coherence length: ~30 cm', 'info');
            }
            if (power >= 90 && phase === 2) {
                phase = 3;
                addLog('  Power fluctuation: ±0.1% (within spec: ±2%)', 'info');
            }

            if (power >= 100) {
                clearInterval(iv);
                $('#status-laser').textContent = '✓ Stable'; $('#status-laser').className = 'status-value complete';
                $('#status-power').textContent = '5.0 mW'; $('#status-power').className = 'status-value complete';
                $('#laser-dot').style.background = '#ef4444';
                $('#laser-status-text').textContent = 'Stable (632.8 nm)'; $('#laser-status-text').style.color = '#ef4444';
                $('#qs-laser').textContent = 'Stable';
                addLog('✓ Laser stabilized: 5.0 mW at 632.8 nm', 'success');
                addLog('  Polarization: vertical | Beam Ø: 0.8 mm', 'success');
                toast('He–Ne laser ready — 5.0 mW, stable output', 'success');
                $('#wizard-next-btn').disabled = false;
                $('#btn-align').disabled = false;
            }
        }, 40);
    }

    function autoAlign() {
        $('#btn-align').disabled = true;
        addLog('▶ Auto-aligning optical system...', 'info');
        addLog('  Adjusting Fourier transform lens position', 'info');
        addLog('  Optimizing detector ring signal pattern', 'info');

        let progress = 0;
        let phase = 0;
        const fill = $('#align-progress-fill'), text = $('#align-progress-text');
        const iv = setInterval(() => {
            progress += 1.5;
            fill.style.width = Math.min(100, progress) + '%';
            text.textContent = Math.round(Math.min(100, progress)) + '%';

            if (progress >= 15 && phase === 0) {
                phase = 1;
                addLog('  Centering laser beam on detector array...', 'info');
                addLog('  Central detector (0.02°): signal maximizing', 'info');
            }
            if (progress >= 40 && phase === 1) {
                phase = 2;
                addLog('  Low-angle detectors (0.02–20°): calibrating', 'info');
                addLog('  These detect large particles (> 10 µm) via Fraunhofer diffraction', 'info');
            }
            if (progress >= 65 && phase === 2) {
                phase = 3;
                addLog('  High-angle detectors (20–144°): calibrating', 'info');
                addLog('  These detect fine particles (< 1 µm) via Mie scattering', 'info');
            }
            if (progress >= 85 && phase === 3) {
                phase = 4;
                addLog('  Back-scatter detector (174°): signal nominal', 'info');
                addLog('  Alignment quality: 98.7% (spec: > 95%)', 'info');
            }

            if (progress >= 100) {
                clearInterval(iv);
                fill.style.width = '100%';
                text.textContent = '100%';
                addLog('✓ Optical alignment complete — all 52 detectors calibrated', 'success');
                addLog('  Angular range: 0.02° to 174° | Alignment quality: 98.7%', 'success');
                toast('Optical alignment passed', 'success');
                $('#wizard-next-btn').disabled = false;
                $('#btn-background').disabled = false;
            }
        }, 40);
    }

    function measureBackground() {
        $('#btn-background').disabled = true;
        addLog('▶ Measuring background scattering (no sample in cell)...', 'info');
        addLog('  This baseline subtraction removes optical noise from results', 'info');

        let progress = 0;
        let phase = 0;
        const iv = setInterval(() => {
            progress += 2;

            if (progress >= 20 && phase === 0) {
                phase = 1;
                addLog('  Detector noise floor: 0.0002% obscuration — excellent', 'info');
            }
            if (progress >= 50 && phase === 1) {
                phase = 2;
                addLog('  Checking dispersant clarity (DI water): clean', 'info');
                addLog('  Stray light level: < 0.01% of beam intensity', 'info');
            }
            if (progress >= 80 && phase === 2) {
                phase = 3;
                addLog('  Detector linearity verified across all 52 elements', 'info');
                addLog('  Background stored — will subtract from sample measurements', 'info');
            }

            if (progress >= 100) {
                clearInterval(iv);
                $('#status-background').textContent = '✓ Clean'; $('#status-background').className = 'status-value complete';
                addLog('✓ Background measurement complete — system baseline set', 'success');
                addLog('  Noise floor: 0.0002% | Stray light: < 0.01%', 'success');
                toast('Background OK — system ready for samples', 'success');
                $('#wizard-next-btn').disabled = false;
                goToWizardStep(4);
            }
        }, 40);
    }

    function finishWizard() {
        STATE.systemReady = true;
        $('#system-status-chip').innerHTML = '<span class="status-dot online"></span><span>System Ready</span>';
        $$('.view').forEach(v => v.classList.remove('active'));
        $('#main-screen-view').classList.add('active');
        closeAllModals();
        $('#run-button').disabled = false;
        addLog('System startup complete — ready for measurement', 'success');
        toast('PSA ready!', 'success');
        const m = MATERIALS[STATE.selectedSample];
        if (m) { $('#sample-name').textContent = m.name; $('#live-dispersion').textContent = STATE.dispersion === 'wet' ? 'Wet' : 'Dry'; }
        // Resize chart after view becomes visible (fixes 0×0 init bug)
        setTimeout(() => { if (psaChart) psaChart.resize(); }, 100);
    }

    function startMeasurement() {
        if (STATE.isMeasuring) return;
        STATE.isMeasuring = true;
        STATE._measureAnim = null;
        $('#run-button').disabled = true; $('#stop-button').disabled = false; $('#sst-report-button').disabled = true;
        $('#screen-title').textContent = 'Scanning...';
        $('#run-status-indicator').classList.add('running');
        addLog('Measurement started — ' + MATERIALS[STATE.selectedSample]?.name, 'info');
        addLog('Laser diffraction scan in progress...', 'info');
        toast('Measurement started', 'info');

        // Pre-generate the full distribution data
        const fullData = generateDistribution();
        if (!fullData) { stopMeasurement(); return; }

        const totalBins = fullData.bins.length;
        const duration = STATE.instantMode ? 500 : 8000;
        const start = Date.now();
        const fill = $('#timer-progress-fill');
        const fmt = (v) => v < 1 ? v.toFixed(3) : v < 10 ? v.toFixed(2) : v.toFixed(1);

        // Disable chart animation for smooth progressive updates
        if (psaChart) psaChart.options.animation = false;

        let lastRevealedBin = 0;
        let logPhase = 0;

        const animate = () => {
            if (!STATE.isMeasuring) return;

            const elapsed = Date.now() - start;
            const progress = Math.min(1, elapsed / duration);

            // Update timer
            fill.style.width = (progress * 100) + '%';
            const sec = (elapsed / 1000).toFixed(1);
            $('#elapsed-time').textContent = sec < 10 ? `00:0${sec}` : `00:${sec}`;

            // Calculate how many bins to reveal (ease-in-out for realism)
            const easedProgress = progress < 0.5
                ? 2 * progress * progress
                : 1 - Math.pow(-2 * progress + 2, 2) / 2;
            const binsToReveal = Math.floor(easedProgress * totalBins);

            if (binsToReveal > lastRevealedBin) {
                lastRevealedBin = binsToReveal;

                // Build partial data arrays
                const partialBins = fullData.bins.slice(0, binsToReveal);
                const partialVolume = fullData.volumePct.slice(0, binsToReveal);

                // Calculate partial cumulative
                let runSum = 0;
                const partialCumul = partialVolume.map(v => { runSum += v; return runSum; });

                // Calculate live D-values from partial cumulative
                const findPartialDx = (pct) => {
                    for (let i = 1; i < partialCumul.length; i++) {
                        if (partialCumul[i] >= pct) {
                            const frac = (pct - partialCumul[i - 1]) / (partialCumul[i] - partialCumul[i - 1]);
                            return partialBins[i - 1] + frac * (partialBins[i] - partialBins[i - 1]);
                        }
                    }
                    return null;
                };

                // Update chart with partial data
                const labels = partialBins.map(b => b < 1 ? b.toFixed(3) : b < 10 ? b.toFixed(1) : Math.round(b));
                if (psaChart) {
                    psaChart.data.labels = labels;
                    psaChart.data.datasets[0].data = partialVolume;
                    psaChart.data.datasets[1].data = partialCumul;
                    psaChart.update('none');
                }

                // Update live D-values as they become available
                const d10 = findPartialDx(10);
                const d50 = findPartialDx(50);
                const d90 = findPartialDx(90);

                // Add jitter during scan to simulate real measurement noise
                const jitter = (1 - progress) * 0.15;

                if (d10 !== null) {
                    const v = d10 * (1 + (Math.random() - 0.5) * jitter);
                    $('#live-d10').textContent = fmt(v);
                }
                if (d50 !== null) {
                    const v = d50 * (1 + (Math.random() - 0.5) * jitter);
                    $('#live-d50').textContent = fmt(v);
                    $('#qs-d50').textContent = fmt(v);
                }
                if (d90 !== null) {
                    const v = d90 * (1 + (Math.random() - 0.5) * jitter);
                    $('#live-d90').textContent = fmt(v);
                }

                // Progressive obscuration
                const liveObscuration = fullData.obscuration * progress * (1 + (Math.random() - 0.5) * 0.05);
                $('#live-obscuration').textContent = liveObscuration.toFixed(1);
                $('#qs-obscuration').textContent = liveObscuration.toFixed(1) + '%';

                // Phase-based log messages
                if (progress > 0.1 && logPhase === 0) {
                    logPhase = 1;
                    addLog('  Low-angle detectors acquiring — large particles...', 'info');
                }
                if (progress > 0.4 && logPhase === 1) {
                    logPhase = 2;
                    addLog('  Mid-angle detectors acquiring — medium particles...', 'info');
                }
                if (progress > 0.7 && logPhase === 2) {
                    logPhase = 3;
                    addLog('  High-angle detectors acquiring — fine particles...', 'info');
                }
                if (progress > 0.9 && logPhase === 3) {
                    logPhase = 4;
                    addLog('  Back-scatter detector check — sub-micron range...', 'info');
                }
            }

            // Update scan status
            const scanPct = Math.round(progress * 100);
            $('#screen-title').textContent = `Scanning... ${scanPct}%`;

            if (elapsed >= duration) {
                completeMeasurement(fullData);
                return;
            }

            STATE._measureAnim = requestAnimationFrame(animate);
        };

        STATE._measureAnim = requestAnimationFrame(animate);
    }

    function completeMeasurement(fullData) {
        STATE.isMeasuring = false;

        // If no data passed (shouldn't happen), generate fresh
        const data = fullData || generateDistribution();
        STATE.lastResult = data;

        // Re-enable chart animation and do final update
        if (psaChart) psaChart.options.animation = { duration: 600 };
        updateChart(data);
        updateResults(data);

        $('#run-button').disabled = false; $('#stop-button').disabled = true; $('#sst-report-button').disabled = false;
        $('#screen-title').textContent = 'Complete';
        $('#run-status-indicator').classList.remove('running');

        const fmt = (v) => v < 1 ? v.toFixed(3) : v.toFixed(1);
        addLog(`✓ Scan complete — ${data.bins.length} size channels measured`, 'success');
        addLog(`D10=${fmt(data.d10)} µm, D50=${fmt(data.d50)} µm, D90=${fmt(data.d90)} µm`, 'success');
        addLog(`Span=${data.span.toFixed(2)}, Uniformity=${data.uniformity.toFixed(3)}`, 'info');
        toast(`D50 = ${fmt(data.d50)} µm`, 'success');
    }

    function stopMeasurement() {
        STATE.isMeasuring = false;
        if (STATE._measureAnim) { cancelAnimationFrame(STATE._measureAnim); STATE._measureAnim = null; }
        $('#run-button').disabled = false; $('#stop-button').disabled = true;
        $('#screen-title').textContent = 'Stopped';
        $('#run-status-indicator').classList.remove('running');
        if (psaChart) psaChart.options.animation = { duration: 600 };
        addLog('Measurement stopped', 'warning');
    }

    function resetMeasurement() {
        stopMeasurement();
        STATE.lastResult = null;
        if (psaChart) { psaChart.data.labels = []; psaChart.data.datasets.forEach(d => d.data = []); psaChart.update(); }
        ['live-d10', 'live-d50', 'live-d90', 'metric-mean', 'metric-d50', 'metric-mode', 'metric-span', 'metric-uniformity', 'metric-ssa'].forEach(id => { const el = document.getElementById(id); if (el) el.textContent = '--'; });
        $('#elapsed-time').textContent = '00:00.0'; $('#timer-progress-fill').style.width = '0%';
        $('#screen-title').textContent = 'Ready'; $('#qs-d50').textContent = '--'; $('#qs-obscuration').textContent = '--';
        addLog('System reset', 'info');
    }

    function generateReport() {
        const data = STATE.lastResult;
        if (!data) { toast('Run a measurement first', 'warning'); return; }
        const fmt = (v) => v < 1 ? v.toFixed(3) : v.toFixed(1);
        $('#report-body').innerHTML = `
            <div style="border-bottom:1px solid #334155;padding-bottom:12px;margin-bottom:12px">
                <h4 style="color:#fff;margin:0">${data.material.name} — Particle Size Report</h4>
                <div style="font-size:12px;color:#94a3b8;margin-top:4px">Category: ${data.material.category} | RI: ${data.material.ri} | Density: ${data.material.density} g/cm³</div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px">
                <div class="d-value-card"><div class="d-label">D10</div><div class="d-number">${fmt(data.d10)}</div><div class="d-unit">µm</div></div>
                <div class="d-value-card"><div class="d-label">D50</div><div class="d-number">${fmt(data.d50)}</div><div class="d-unit">µm</div></div>
                <div class="d-value-card"><div class="d-label">D90</div><div class="d-number">${fmt(data.d90)}</div><div class="d-unit">µm</div></div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:13px">
                <div class="metric-row"><span class="metric-label">Span:</span><span class="metric-value">${data.span.toFixed(2)}</span></div>
                <div class="metric-row"><span class="metric-label">Uniformity:</span><span class="metric-value">${data.uniformity.toFixed(3)}</span></div>
                <div class="metric-row"><span class="metric-label">Mean:</span><span class="metric-value">${fmt(data.mean)} µm</span></div>
                <div class="metric-row"><span class="metric-label">Mode:</span><span class="metric-value">${fmt(data.mode)} µm</span></div>
                <div class="metric-row"><span class="metric-label">SSA:</span><span class="metric-value">${data.ssa.toFixed(2)} m²/g</span></div>
                <div class="metric-row"><span class="metric-label">Obscuration:</span><span class="metric-value">${data.obscuration.toFixed(1)}%</span></div>
                <div class="metric-row"><span class="metric-label">Dispersion:</span><span class="metric-value">${STATE.dispersion}</span></div>
                <div class="metric-row"><span class="metric-label">Optical Model:</span><span class="metric-value">${STATE.opticalModel}</span></div>
            </div>`;
        openModal('sst-modal');
    }

    function exportData() {
        const data = STATE.lastResult;
        if (!data) { toast('No data to export', 'warning'); return; }
        let csv = 'Size (µm),Volume %,Cumulative %\n';
        data.bins.forEach((b, i) => { csv += `${b},${data.volumePct[i].toFixed(4)},${data.cumulative[i].toFixed(4)}\n`; });
        const blob = new Blob([csv], { type: 'text/csv' });
        const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
        a.download = `PSA_${STATE.selectedSample}_${Date.now()}.csv`; a.click();
        toast('Data exported', 'success');
    }

    function openModal(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.classList.remove('hidden');
            $('#modal-backdrop')?.classList.remove('hidden');
            requestAnimationFrame(() => modal.classList.add('visible'));
        }
    }
    function closeAllModals() {
        $$('.modal').forEach(m => { m.classList.remove('visible'); m.classList.add('hidden'); });
        $('#modal-backdrop')?.classList.add('hidden');
    }

    function applySettings() {
        const sample = $('#sample-select'); if (sample) STATE.selectedSample = sample.value;
        const disp = document.querySelector('input[name=dispersion]:checked'); if (disp) STATE.dispersion = disp.value;
        const pump = $('#pump-number'); if (pump) STATE.pumpSpeed = parseInt(pump.value);
        const model = document.querySelector('input[name=optical-model]:checked'); if (model) STATE.opticalModel = model.value;
        const fault = document.querySelector('input[name=fault-type]:checked'); if (fault) STATE.fault = fault.value;

        const m = MATERIALS[STATE.selectedSample];
        if (m) { $('#sample-name').textContent = m.name; addLog(`Sample: ${m.name}`, 'info'); }
        $('#live-dispersion').textContent = STATE.dispersion === 'wet' ? 'Wet' : 'Dry';
        $('#live-pump').textContent = STATE.pumpSpeed;
        $('#live-model').textContent = STATE.opticalModel === 'mie' ? 'Mie' : 'Fraunhofer';
        if (STATE.fault !== 'none') addLog(`Fault simulation: ${STATE.fault}`, 'warning');
    }

    function bindEvents() {
        $$('.hotspot').forEach(hs => hs.addEventListener('click', () => {
            const t = hs.dataset.controls;
            if (t === 'screen-view') {
                if (!STATE.systemReady) { toast('Start the system first', 'warning'); return; }
                $$('.view').forEach(v => v.classList.remove('active'));
                $('#main-screen-view').classList.add('active');
                // Resize chart after view switch
                setTimeout(() => { if (psaChart) psaChart.resize(); }, 100);
            } else if (t) openModal(t);
        }));

        $('#hotspot-setup')?.addEventListener('click', () => openModal('setup-modal'));
        $('#btn-laser-on')?.addEventListener('click', laserOn);
        $('#btn-align')?.addEventListener('click', autoAlign);
        $('#btn-background')?.addEventListener('click', measureBackground);
        $('#wizard-prev-btn')?.addEventListener('click', () => { if (STATE.wizardStep > 1) goToWizardStep(STATE.wizardStep - 1); });
        $('#wizard-next-btn')?.addEventListener('click', () => { if (STATE.wizardStep < 4) goToWizardStep(STATE.wizardStep + 1); });
        $('#wizard-finish-btn')?.addEventListener('click', finishWizard);
        $('#back-to-main-view-button')?.addEventListener('click', () => { $$('.view').forEach(v => v.classList.remove('active')); $('#hplc-main-view').classList.add('active'); });

        $('#run-button')?.addEventListener('click', startMeasurement);
        $('#stop-button')?.addEventListener('click', stopMeasurement);
        $('#reset-button')?.addEventListener('click', resetMeasurement);
        $('#instant-mode-toggle')?.addEventListener('change', (e) => { STATE.instantMode = e.target.checked; });
        $('#fault-mode-toggle')?.addEventListener('change', (e) => { if (e.target.checked) openModal('fault-selector-modal'); else STATE.fault = 'none'; });
        $('#sst-report-button')?.addEventListener('click', generateReport);
        $('#export-data-btn')?.addEventListener('click', exportData);
        $('#screenshot-btn')?.addEventListener('click', () => {
            const url = psaChart?.toBase64Image();
            if (url) { const a = document.createElement('a'); a.href = url; a.download = 'psa_distribution.png'; a.click(); }
        });

        // Chart type toggle
        $$('#chart-type-toggle button').forEach(btn => btn.addEventListener('click', () => {
            $$('#chart-type-toggle button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            STATE.chartType = btn.dataset.type;
            if (STATE.lastResult) updateChart(STATE.lastResult);
        }));

        // Zoom
        $('#zoom-in-btn')?.addEventListener('click', () => psaChart?.zoom(1.2));
        $('#zoom-out-btn')?.addEventListener('click', () => psaChart?.zoom(0.8));
        $('#reset-zoom-btn')?.addEventListener('click', () => psaChart?.resetZoom());

        $$('.modal-close-btn').forEach(b => b.addEventListener('click', closeAllModals));
        $('#modal-backdrop')?.addEventListener('click', closeAllModals);
        $$('.modal-confirm-btn').forEach(b => b.addEventListener('click', () => { applySettings(); closeAllModals(); }));

        $$('.column-card').forEach(card => card.addEventListener('click', () => {
            card.closest('.column-cards')?.querySelectorAll('.column-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        }));
        $$('.range-with-input').forEach(g => {
            const r = g.querySelector('input[type=range]'), n = g.querySelector('input[type=number]');
            if (r && n) { r.addEventListener('input', () => n.value = r.value); n.addEventListener('input', () => r.value = n.value); }
        });
        $$('.difficulty-btn').forEach(b => b.addEventListener('click', () => {
            $$('.difficulty-btn').forEach(x => x.classList.remove('active')); b.classList.add('active'); STATE.difficulty = b.dataset.level;
        }));
        $('#clear-log-btn')?.addEventListener('click', () => { $('#log-content').innerHTML = ''; });
        $('#fullscreen-button')?.addEventListener('click', () => {
            if (!document.fullscreenElement) document.documentElement.requestFullscreen(); else document.exitFullscreen();
        });
    }

    function updateClock() {
        const el = $('#system-time'); if (el) el.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function init() {
        initChart();
        bindEvents();
        updateClock();
        setInterval(updateClock, 30000);
        const style = document.createElement('style');
        style.textContent = '@keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}';
        document.head.appendChild(style);
        addLog('Particle Size Analyzer Digital Twin v2.0 initialized', 'success');
        addLog('Click "System Startup" to begin', 'info');
    }

    init();
});