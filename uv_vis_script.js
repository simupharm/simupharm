/**
 * SimuPharma Advanced UV-Vis Spectrophotometer Simulator v2.0
 * Physics-based engine with Beer-Lambert Law, Gaussian peak modeling,
 * compound library, 4 analysis modes, fault simulation
 */
document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // ========================================================================
    // COMPOUND LIBRARY — Pharmacopeial Data
    // ========================================================================
    const COMPOUNDS = {
        paracetamol: {
            name: 'Paracetamol', category: 'Analgesic', mw: 151.16, formula: 'C₈H₉NO₂', cas: '103-90-2',
            solvent: 'water', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 245, width: 18, epsilon: 13500, label: 'π→π*' },
                { center: 300, width: 25, epsilon: 1800, label: 'n→π*' }
            ]
        },
        caffeine: {
            name: 'Caffeine', category: 'CNS Stimulant', mw: 194.19, formula: 'C₈H₁₀N₄O₂', cas: '58-08-2',
            solvent: 'water', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 205, width: 12, epsilon: 11200, label: 'π→π*' },
                { center: 273, width: 16, epsilon: 10400, label: 'π→π*' }
            ]
        },
        aspirin: {
            name: 'Aspirin', category: 'NSAID', mw: 180.16, formula: 'C₉H₈O₄', cas: '50-78-2',
            solvent: 'methanol', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 228, width: 15, epsilon: 9800, label: 'π→π*' },
                { center: 276, width: 20, epsilon: 1500, label: 'n→π*' }
            ]
        },
        ibuprofen: {
            name: 'Ibuprofen', category: 'NSAID', mw: 206.28, formula: 'C₁₃H₁₈O₂', cas: '15687-27-1',
            solvent: 'methanol', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 222, width: 14, epsilon: 8600, label: 'π→π*' },
                { center: 264, width: 18, epsilon: 450, label: 'n→π*' }
            ]
        },
        diclofenac: {
            name: 'Diclofenac Sodium', category: 'NSAID', mw: 318.13, formula: 'C₁₄H₁₀Cl₂NNaO₂', cas: '15307-79-6',
            solvent: 'water', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 276, width: 16, epsilon: 9650, label: 'π→π*' },
                { center: 215, width: 12, epsilon: 14200, label: 'π→π*' }
            ]
        },
        metformin: {
            name: 'Metformin HCl', category: 'Antidiabetic', mw: 165.63, formula: 'C₄H₁₂ClN₅', cas: '1115-70-4',
            solvent: 'water', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 233, width: 14, epsilon: 12900, label: 'π→π*' }
            ]
        },
        ranitidine: {
            name: 'Ranitidine HCl', category: 'H₂ Blocker', mw: 350.87, formula: 'C₁₃H₂₃ClN₄O₃S', cas: '66357-59-3',
            solvent: 'water', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 230, width: 14, epsilon: 7200, label: 'π→π*' },
                { center: 314, width: 20, epsilon: 7800, label: 'n→π*' }
            ]
        },
        amlodipine: {
            name: 'Amlodipine Besylate', category: 'Ca²⁺ Blocker', mw: 567.05, formula: 'C₂₆H₃₁ClN₂O₈S', cas: '111470-99-6',
            solvent: 'methanol', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 238, width: 16, epsilon: 15800, label: 'π→π*' },
                { center: 366, width: 24, epsilon: 7200, label: 'n→π*' }
            ]
        },
        losartan: {
            name: 'Losartan Potassium', category: 'ARB', mw: 461.00, formula: 'C₂₂H₂₂ClKN₆O', cas: '124750-99-8',
            solvent: 'water', pharmacopeialRef: 'IP, USP',
            peaks: [
                { center: 205, width: 12, epsilon: 22000, label: 'π→π*' },
                { center: 254, width: 16, epsilon: 4500, label: 'π→π*' }
            ]
        },
        ciprofloxacin: {
            name: 'Ciprofloxacin HCl', category: 'Fluoroquinolone', mw: 367.80, formula: 'C₁₇H₁₉ClFN₃O₃', cas: '86393-32-0',
            solvent: 'water', pharmacopeialRef: 'IP, BP, USP',
            peaks: [
                { center: 278, width: 16, epsilon: 14500, label: 'π→π*' },
                { center: 320, width: 18, epsilon: 5600, label: 'n→π*' }
            ]
        }
    };

    // Solvent UV cutoffs (nm)
    const SOLVENT_CUTOFFS = { water: 190, methanol: 210, ethanol: 210, acetonitrile: 190, hexane: 200, chloroform: 245 };

    // Fault effects
    const FAULTS = {
        none: { noise: 1, absShift: 0, scatter: 0, baseline: 0, label: 'Normal' },
        dirty_cuvette: { noise: 2.5, absShift: 0.05, scatter: 0.08, baseline: 0.03, label: 'Dirty Cuvette' },
        air_bubble: { noise: 4, absShift: -0.1, scatter: 0.15, baseline: 0, label: 'Air Bubble' },
        lamp_aging: { noise: 1.8, absShift: 0, scatter: 0, baseline: 0.02, label: 'Lamp Aging', intensityLoss: 0.3 },
        stray_light: { noise: 1.2, absShift: 0, scatter: 0, baseline: 0, label: 'Stray Light', strayPct: 0.02 },
        wrong_solvent: { noise: 1.5, absShift: 0, scatter: 0, baseline: 0.15, label: 'Wrong Solvent' }
    };

    // ========================================================================
    // STATE
    // ========================================================================
    const state = {
        powerOn: false,
        currentView: 'instrument',
        activeMode: 'scan',
        difficulty: 'beginner',
        selectedCompound: null,
        instrumentSettings: {
            uvSource: 'deuterium', visSource: 'tungsten', sourceSwitch: 'auto',
            gratingType: 'holographic', slitWidth: 1.0,
            cuvetteMaterial: 'quartz', pathLength: 1.0, refSolvent: 'water',
            detectorType: 'pmt', integrationTime: 200, sensitivity: 'medium'
        },
        scanData: [],
        calibData: { standards: [], regression: null },
        kineticsData: [],
        activeFault: 'none',
        scanning: false,
        kineticsRunning: false,
        zoom: 1,
        showTransmittance: false,
        detectedPeaks: [],
        blanked: false
    };

    // ========================================================================
    // DOM REFERENCES
    // ========================================================================
    const $ = (id) => document.getElementById(id);
    const $$ = (sel) => document.querySelectorAll(sel);

    const views = { instrument: $('instrument-view'), analysis: $('analysis-view') };
    const spectrumCanvas = $('spectrum-canvas');
    const calibCanvas = $('calibration-canvas');
    const specCtx = spectrumCanvas.getContext('2d');
    const calCtx = calibCanvas.getContext('2d');

    // ========================================================================
    // PHYSICS ENGINE — Beer-Lambert & Gaussian Peak Modeling
    // ========================================================================
    function calculateAbsorbance(compound, wavelength, concentration, pathLength) {
        if (!compound) return 0;
        const concMolar = (concentration / 1000) / compound.mw; // mg/L → mol/L
        let totalAbs = 0;
        for (const peak of compound.peaks) {
            const gaussian = Math.exp(-Math.pow(wavelength - peak.center, 2) / (2 * Math.pow(peak.width, 2)));
            totalAbs += peak.epsilon * pathLength * concMolar * gaussian;
        }
        return totalAbs;
    }

    function applyFaultEffects(absorbance, wavelength, fault) {
        const f = FAULTS[fault];
        let a = absorbance + f.absShift + f.baseline;
        // Scatter increases at shorter wavelengths
        a += f.scatter * Math.pow(300 / Math.max(wavelength, 200), 4);
        // Stray light caps absorbance
        if (f.strayPct) { a = -Math.log10(Math.pow(10, -a) + f.strayPct); }
        // Intensity loss
        if (f.intensityLoss) { a *= (1 + f.intensityLoss * 0.5); }
        // Noise
        const noiseLevel = 0.002 * f.noise * (state.instrumentSettings.sensitivity === 'high' ? 0.5 : state.instrumentSettings.sensitivity === 'low' ? 2 : 1);
        a += (Math.random() - 0.5) * noiseLevel;
        return Math.max(0, a);
    }

    function generateSpectrum(compound, concentration, startWl, endWl) {
        const data = [];
        const pL = state.instrumentSettings.pathLength;
        const solventCutoff = SOLVENT_CUTOFFS[state.instrumentSettings.refSolvent] || 190;
        const cuvetteCutoff = state.instrumentSettings.cuvetteMaterial === 'quartz' ? 190 :
            state.instrumentSettings.cuvetteMaterial === 'glass' ? 340 : 380;
        const effectiveCutoff = Math.max(solventCutoff, cuvetteCutoff);

        for (let wl = startWl; wl <= endWl; wl += 0.5) {
            let abs = calculateAbsorbance(compound, wl, concentration, pL);
            abs = applyFaultEffects(abs, wl, state.activeFault);
            // Below cutoff: add large absorption
            if (wl < effectiveCutoff) { abs += 3.0 * Math.exp(-(wl - effectiveCutoff) / 5); }
            data.push({ wl, abs: Math.max(0, Math.min(abs, 4.0)) });
        }
        return data;
    }

    function detectPeaks(data) {
        const peaks = [];
        for (let i = 2; i < data.length - 2; i++) {
            if (data[i].abs > data[i - 1].abs && data[i].abs > data[i + 1].abs &&
                data[i].abs > data[i - 2].abs && data[i].abs > data[i + 2].abs &&
                data[i].abs > 0.01) {
                // Check not too close to existing peak
                const tooClose = peaks.some(p => Math.abs(p.wl - data[i].wl) < 10);
                if (!tooClose) peaks.push({ wl: data[i].wl, abs: data[i].abs });
            }
        }
        return peaks.sort((a, b) => b.abs - a.abs).slice(0, 6);
    }

    function linearRegression(points) {
        const n = points.length;
        let sx = 0, sy = 0, sxy = 0, sx2 = 0;
        for (const p of points) { sx += p.x; sy += p.y; sxy += p.x * p.y; sx2 += p.x * p.x; }
        const slope = (n * sxy - sx * sy) / (n * sx2 - sx * sx);
        const intercept = (sy - slope * sx) / n;
        let ssr = 0, sst = 0;
        const yMean = sy / n;
        for (const p of points) { ssr += Math.pow(p.y - (slope * p.x + intercept), 2); sst += Math.pow(p.y - yMean, 2); }
        const r2 = sst === 0 ? 1 : 1 - ssr / sst;
        return { slope, intercept, r2 };
    }

    // ========================================================================
    // CANVAS RENDERING — Spectrum
    // ========================================================================
    function drawSpectrum() {
        const canvas = spectrumCanvas;
        const ctx = specCtx;
        const W = canvas.width;
        const H = canvas.height;
        ctx.clearRect(0, 0, W, H);

        const pad = { top: 40, right: 30, bottom: 50, left: 65 };
        const plotW = W - pad.left - pad.right;
        const plotH = H - pad.top - pad.bottom;

        // Background
        ctx.fillStyle = '#0a0f18';
        ctx.fillRect(0, 0, W, H);

        // Grid
        ctx.strokeStyle = 'rgba(255,255,255,0.06)';
        ctx.lineWidth = 0.5;
        for (let i = 0; i <= 8; i++) {
            const y = pad.top + (plotH / 8) * i;
            ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(W - pad.right, y); ctx.stroke();
        }
        for (let i = 0; i <= 10; i++) {
            const x = pad.left + (plotW / 10) * i;
            ctx.beginPath(); ctx.moveTo(x, pad.top); ctx.lineTo(x, pad.top + plotH); ctx.stroke();
        }

        // Axes
        ctx.strokeStyle = 'rgba(255,255,255,0.15)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(pad.left, pad.top); ctx.lineTo(pad.left, pad.top + plotH);
        ctx.lineTo(W - pad.right, pad.top + plotH);
        ctx.stroke();

        const data = state.scanData;
        if (data.length === 0) {
            ctx.fillStyle = '#64748b'; ctx.font = '14px Inter';
            ctx.textAlign = 'center';
            ctx.fillText('No data — Run a scan to begin', W / 2, H / 2);
            drawAxisLabels(ctx, pad, plotW, plotH, W, H, 190, 400, 0, 1);
            return;
        }

        // Determine ranges
        const minWl = data[0].wl;
        const maxWl = data[data.length - 1].wl;
        let maxAbs = Math.max(0.1, ...data.map(d => d.abs)) * 1.15 / state.zoom;
        if (state.showTransmittance) maxAbs = 100;

        drawAxisLabels(ctx, pad, plotW, plotH, W, H, minWl, maxWl, 0, maxAbs);

        // Draw spectrum line
        const gradient = ctx.createLinearGradient(pad.left, pad.top, pad.left, pad.top + plotH);
        gradient.addColorStop(0, 'rgba(0, 180, 216, 0.3)');
        gradient.addColorStop(1, 'rgba(0, 180, 216, 0)');

        ctx.beginPath();
        let firstMove = true;
        for (const d of data) {
            const x = pad.left + ((d.wl - minWl) / (maxWl - minWl)) * plotW;
            let yVal = state.showTransmittance ? Math.pow(10, -d.abs) * 100 : d.abs;
            const y = pad.top + plotH - (yVal / maxAbs) * plotH;
            if (firstMove) { ctx.moveTo(x, y); firstMove = false; }
            else ctx.lineTo(x, y);
        }
        // Fill
        ctx.lineTo(pad.left + plotW, pad.top + plotH);
        ctx.lineTo(pad.left, pad.top + plotH);
        ctx.fillStyle = gradient;
        ctx.fill();

        // Stroke line
        ctx.beginPath(); firstMove = true;
        for (const d of data) {
            const x = pad.left + ((d.wl - minWl) / (maxWl - minWl)) * plotW;
            let yVal = state.showTransmittance ? Math.pow(10, -d.abs) * 100 : d.abs;
            const y = pad.top + plotH - (yVal / maxAbs) * plotH;
            if (firstMove) { ctx.moveTo(x, y); firstMove = false; }
            else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = '#00b4d8';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Draw peaks
        for (const peak of state.detectedPeaks) {
            const px = pad.left + ((peak.wl - minWl) / (maxWl - minWl)) * plotW;
            let yVal = state.showTransmittance ? Math.pow(10, -peak.abs) * 100 : peak.abs;
            const py = pad.top + plotH - (yVal / maxAbs) * plotH;
            // Marker
            ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#ef4444'; ctx.fill();
            // Label
            ctx.fillStyle = '#fbbf24'; ctx.font = '11px JetBrains Mono';
            ctx.textAlign = 'center';
            ctx.fillText(`${peak.wl.toFixed(1)} nm`, px, py - 12);
            ctx.fillText(`${peak.abs.toFixed(3)}`, px, py - 24);
        }

        // Title
        ctx.fillStyle = '#94a3b8'; ctx.font = '12px Inter'; ctx.textAlign = 'left';
        const titleText = state.selectedCompound ?
            `${state.selectedCompound.name} — UV-Vis Spectrum` : 'UV-Vis Spectrum';
        ctx.fillText(titleText, pad.left + 8, pad.top - 12);
    }

    function drawAxisLabels(ctx, pad, plotW, plotH, W, H, minWl, maxWl, minY, maxY) {
        ctx.fillStyle = '#94a3b8'; ctx.font = '10px JetBrains Mono'; ctx.textAlign = 'center';
        // X axis
        const xSteps = 8;
        for (let i = 0; i <= xSteps; i++) {
            const wl = minWl + (maxWl - minWl) * i / xSteps;
            const x = pad.left + (plotW / xSteps) * i;
            ctx.fillText(wl.toFixed(0), x, pad.top + plotH + 18);
        }
        ctx.fillStyle = '#64748b'; ctx.font = '11px Inter';
        ctx.fillText('Wavelength (nm)', pad.left + plotW / 2, H - 8);

        // Y axis
        ctx.textAlign = 'right'; ctx.fillStyle = '#94a3b8'; ctx.font = '10px JetBrains Mono';
        const ySteps = 5;
        for (let i = 0; i <= ySteps; i++) {
            const v = minY + (maxY - minY) * i / ySteps;
            const y = pad.top + plotH - (plotH / ySteps) * i;
            ctx.fillText(v.toFixed(state.showTransmittance ? 0 : 2), pad.left - 8, y + 4);
        }
        ctx.save(); ctx.translate(14, pad.top + plotH / 2); ctx.rotate(-Math.PI / 2);
        ctx.fillStyle = '#64748b'; ctx.font = '11px Inter'; ctx.textAlign = 'center';
        ctx.fillText(state.showTransmittance ? '% Transmittance' : 'Absorbance', 0, 0);
        ctx.restore();
    }

    // ========================================================================
    // CANVAS — Calibration Curve
    // ========================================================================
    function drawCalibration() {
        const ctx = calCtx;
        const W = calibCanvas.width; const H = calibCanvas.height;
        ctx.clearRect(0, 0, W, H);
        const pad = { top: 40, right: 30, bottom: 50, left: 65 };
        const plotW = W - pad.left - pad.right;
        const plotH = H - pad.top - pad.bottom;

        ctx.fillStyle = '#0a0f18'; ctx.fillRect(0, 0, W, H);

        const stds = state.calibData.standards;
        if (stds.length === 0) {
            ctx.fillStyle = '#64748b'; ctx.font = '14px Inter'; ctx.textAlign = 'center';
            ctx.fillText('Run calibration to see curve', W / 2, H / 2);
            return;
        }

        const maxConc = Math.max(...stds.map(s => s.x)) * 1.2;
        const maxAbs = Math.max(...stds.map(s => s.y)) * 1.2;

        // Grid + axes
        ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 0.5;
        for (let i = 0; i <= 5; i++) {
            const y = pad.top + (plotH / 5) * i;
            ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(W - pad.right, y); ctx.stroke();
            const x = pad.left + (plotW / 5) * i;
            ctx.beginPath(); ctx.moveTo(x, pad.top); ctx.lineTo(x, pad.top + plotH); ctx.stroke();
        }
        ctx.strokeStyle = 'rgba(255,255,255,0.15)'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(pad.left, pad.top); ctx.lineTo(pad.left, pad.top + plotH);
        ctx.lineTo(W - pad.right, pad.top + plotH); ctx.stroke();

        // Axis labels
        ctx.fillStyle = '#94a3b8'; ctx.font = '10px JetBrains Mono'; ctx.textAlign = 'center';
        for (let i = 0; i <= 5; i++) {
            const c = (maxConc / 5) * i;
            ctx.fillText(c.toFixed(1), pad.left + (plotW / 5) * i, pad.top + plotH + 18);
        }
        ctx.fillStyle = '#64748b'; ctx.font = '11px Inter';
        ctx.fillText('Concentration (mg/L)', pad.left + plotW / 2, H - 8);
        ctx.textAlign = 'right'; ctx.fillStyle = '#94a3b8'; ctx.font = '10px JetBrains Mono';
        for (let i = 0; i <= 5; i++) {
            const a = (maxAbs / 5) * i;
            ctx.fillText(a.toFixed(3), pad.left - 8, pad.top + plotH - (plotH / 5) * i + 4);
        }

        // Regression line
        if (state.calibData.regression) {
            const reg = state.calibData.regression;
            ctx.beginPath();
            const x1 = pad.left;
            const y1 = pad.top + plotH - ((reg.intercept) / maxAbs) * plotH;
            const x2 = pad.left + plotW;
            const y2 = pad.top + plotH - ((reg.slope * maxConc + reg.intercept) / maxAbs) * plotH;
            ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
            ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2; ctx.setLineDash([6, 4]); ctx.stroke();
            ctx.setLineDash([]);
        }

        // Points
        for (const s of stds) {
            const px = pad.left + (s.x / maxConc) * plotW;
            const py = pad.top + plotH - (s.y / maxAbs) * plotH;
            ctx.beginPath(); ctx.arc(px, py, 6, 0, Math.PI * 2);
            ctx.fillStyle = '#00b4d8'; ctx.fill();
            ctx.strokeStyle = '#0a0f18'; ctx.lineWidth = 2; ctx.stroke();
        }

        // Title
        ctx.fillStyle = '#94a3b8'; ctx.font = '12px Inter'; ctx.textAlign = 'left';
        ctx.fillText('Calibration Curve — Beer-Lambert Law', pad.left + 8, pad.top - 12);
    }

    // ========================================================================
    // UI INTERACTIONS
    // ========================================================================
    function toast(msg, type = 'info') {
        const t = document.createElement('div');
        t.className = `toast ${type}`;
        t.textContent = msg;
        $('toast-container').appendChild(t);
        setTimeout(() => { t.classList.add('hiding'); setTimeout(() => t.remove(), 300); }, 3000);
    }

    function switchView(view) {
        state.currentView = view;
        Object.values(views).forEach(v => v.classList.remove('active'));
        views[view].classList.add('active');
    }

    function switchMode(mode) {
        state.activeMode = mode;
        $$('.mode-tab').forEach(t => t.classList.toggle('active', t.dataset.mode === mode));
        $$('.mode-panel').forEach(p => p.classList.toggle('hidden', p.dataset.for !== mode));
    }

    function openModal(id) {
        const m = $(id);
        if (m) m.classList.add('active');
    }
    function closeModal(el) {
        el.closest('.modal-overlay').classList.remove('active');
    }

    function updateDisplay(wl, abs) {
        $('disp-wavelength').textContent = wl.toFixed(1) + ' nm';
        $('disp-absorbance').textContent = abs.toFixed(3);
        $('disp-transmittance').textContent = (Math.pow(10, -abs) * 100).toFixed(1) + '%';
    }

    function updateQuickStats() {
        const s = state.instrumentSettings;
        const srcLabel = s.sourceSwitch === 'uv' ? 'D₂' : s.sourceSwitch === 'vis' ? 'W' : 'D₂ + W';
        $('qs-source').textContent = srcLabel;
        $('qs-path').textContent = s.pathLength + ' cm';
        $('qs-compound').textContent = state.selectedCompound ? state.selectedCompound.name : 'None';
    }

    function populateCompounds() {
        const sel = $('compound-select');
        for (const [key, c] of Object.entries(COMPOUNDS)) {
            const opt = document.createElement('option');
            opt.value = key; opt.textContent = c.name;
            sel.appendChild(opt);
        }
    }

    function selectCompound(key) {
        state.selectedCompound = COMPOUNDS[key] || null;
        const info = $('compound-info');
        if (state.selectedCompound) {
            const c = state.selectedCompound;
            $('ci-mw').textContent = c.mw.toFixed(2);
            $('ci-formula').textContent = c.formula;
            $('ci-lambda').textContent = c.peaks.map(p => p.center + ' nm').join(', ');
            $('ci-category').textContent = c.category;
            info.style.display = 'block';
            // Update cuvette color
            const hue = (c.peaks[0].center - 190) / (800 - 190) * 300;
            $('cuvette-liquid').style.background = `hsla(${hue}, 70%, 50%, 0.5)`;
        } else {
            info.style.display = 'none';
        }
        updateQuickStats();
    }

    function updatePeakTable() {
        const tbody = $('peak-tbody');
        if (state.detectedPeaks.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="empty-msg">No peaks detected</td></tr>';
            return;
        }
        const compound = state.selectedCompound;
        tbody.innerHTML = state.detectedPeaks.map((p, i) => {
            const concMolar = compound ? (parseFloat($('scan-conc')?.value || 10) / 1000) / compound.mw : 0;
            const epsilon = concMolar > 0 && state.instrumentSettings.pathLength > 0 ?
                (p.abs / (state.instrumentSettings.pathLength * concMolar)).toFixed(0) : '—';
            return `<tr><td>${i + 1}</td><td>${p.wl.toFixed(1)}</td><td>${p.abs.toFixed(3)}</td><td>${epsilon}</td></tr>`;
        }).join('');
    }

    // ========================================================================
    // ANALYSIS ACTIONS
    // ========================================================================
    async function runScan() {
        if (!state.selectedCompound) { toast('Select a compound first', 'warning'); return; }
        if (state.scanning) return;
        if (!state.blanked) { toast('Auto-zero the instrument first (set blank)', 'warning'); return; }

        state.scanning = true;
        const startWl = parseInt($('scan-start').value) || 190;
        const endWl = parseInt($('scan-end').value) || 400;
        const conc = parseFloat($('scan-conc').value) || 10;
        const speed = $('scan-speed').value;
        const totalPoints = (endWl - startWl) / 0.5;
        const speedMs = speed === 'fast' ? 2 : speed === 'medium' ? 8 : 30;

        $('scan-progress').style.display = 'flex';
        $('disp-status').textContent = 'Scanning...';
        $('status-dot').className = 'fas fa-circle scanning';
        state.scanData = [];
        state.detectedPeaks = [];

        const fullData = generateSpectrum(state.selectedCompound, conc, startWl, endWl);

        for (let i = 0; i < fullData.length; i++) {
            state.scanData.push(fullData[i]);
            if (i % 5 === 0) {
                const pct = (i / fullData.length * 100).toFixed(0);
                $('scan-progress-fill').style.width = pct + '%';
                $('scan-progress-text').textContent = `Scanning... ${fullData[i].wl.toFixed(0)} nm (${pct}%)`;
                updateDisplay(fullData[i].wl, fullData[i].abs);
                drawSpectrum();
                await new Promise(r => setTimeout(r, speedMs));
            }
        }
        state.scanData = fullData;

        // Detect peaks
        state.detectedPeaks = detectPeaks(fullData);
        drawSpectrum();
        updatePeakTable();
        updateCalcDisplay();

        $('scan-progress').style.display = 'none';
        $('disp-status').textContent = 'Scan Complete';
        $('status-dot').className = 'fas fa-circle';
        state.scanning = false;
        toast(`Scan complete: ${state.detectedPeaks.length} peak(s) found`, 'success');

        // Auto-set cal wavelength to λmax
        if (state.detectedPeaks.length > 0) {
            const lmax = state.detectedPeaks[0].wl;
            $('qs-wavelength').textContent = lmax.toFixed(0) + ' nm';
            if ($('cal-wavelength')) $('cal-wavelength').value = lmax.toFixed(0);
            if ($('fixed-wavelength')) $('fixed-wavelength').value = lmax.toFixed(0);
            if ($('kin-wavelength')) $('kin-wavelength').value = lmax.toFixed(0);
        }
    }

    function measureFixed() {
        if (!state.selectedCompound) { toast('Select a compound first', 'warning'); return; }
        if (!state.blanked) { toast('Auto-zero first', 'warning'); return; }
        const wl = parseFloat($('fixed-wavelength').value) || 254;
        const conc = parseFloat($('fixed-conc').value) || 10;
        let abs = calculateAbsorbance(state.selectedCompound, wl, conc, state.instrumentSettings.pathLength);
        abs = applyFaultEffects(abs, wl, state.activeFault);
        abs = Math.max(0, Math.min(abs, 4));

        $('fixed-result').style.display = 'block';
        $('fixed-abs-value').textContent = abs.toFixed(4);
        $('fixed-trans-value').textContent = (Math.pow(10, -abs) * 100).toFixed(2) + '% T';
        updateDisplay(wl, abs);
        toast(`Measured at ${wl} nm: Abs = ${abs.toFixed(4)}`, 'success');
    }

    async function runKinetics() {
        if (!state.selectedCompound) { toast('Select a compound first', 'warning'); return; }
        if (!state.blanked) { toast('Auto-zero first', 'warning'); return; }
        state.kineticsRunning = true;
        $('btn-start-kinetics').disabled = true;
        $('btn-stop-kinetics').disabled = false;
        $('disp-status').textContent = 'Monitoring...';
        $('status-dot').className = 'fas fa-circle scanning';

        const wl = parseFloat($('kin-wavelength').value) || 254;
        const duration = parseInt($('kin-duration').value) || 60;
        const rateConst = $('kin-rate').value === 'slow' ? 0.01 : $('kin-rate').value === 'fast' ? 0.15 : 0.05;
        const initConc = 10;
        state.scanData = [];
        state.detectedPeaks = [];

        const startTime = Date.now();
        const updateInterval = 200;

        const loop = () => {
            if (!state.kineticsRunning) return;
            const elapsed = (Date.now() - startTime) / 1000;
            if (elapsed > duration) { stopKinetics(); return; }

            const conc = initConc * Math.exp(-rateConst * elapsed);
            let abs = calculateAbsorbance(state.selectedCompound, wl, conc, state.instrumentSettings.pathLength);
            abs = applyFaultEffects(abs, wl, state.activeFault);
            state.scanData.push({ wl: elapsed, abs: Math.max(0, abs) });
            updateDisplay(wl, abs);
            drawKineticsPlot();
            setTimeout(loop, updateInterval);
        };
        loop();
    }

    function stopKinetics() {
        state.kineticsRunning = false;
        $('btn-start-kinetics').disabled = false;
        $('btn-stop-kinetics').disabled = true;
        $('disp-status').textContent = 'Ready';
        $('status-dot').className = 'fas fa-circle';
        toast('Kinetics monitoring complete', 'success');
    }

    function drawKineticsPlot() {
        const ctx = specCtx;
        const W = spectrumCanvas.width; const H = spectrumCanvas.height;
        ctx.clearRect(0, 0, W, H);
        const pad = { top: 40, right: 30, bottom: 50, left: 65 };
        const plotW = W - pad.left - pad.right;
        const plotH = H - pad.top - pad.bottom;
        ctx.fillStyle = '#0a0f18'; ctx.fillRect(0, 0, W, H);

        const data = state.scanData;
        if (data.length < 2) return;

        const maxT = Math.max(...data.map(d => d.wl)) * 1.1 || 60;
        const maxA = Math.max(0.1, ...data.map(d => d.abs)) * 1.15;

        // Grid
        ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 0.5;
        for (let i = 0; i <= 5; i++) {
            const y = pad.top + (plotH / 5) * i;
            ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(W - pad.right, y); ctx.stroke();
        }
        ctx.strokeStyle = 'rgba(255,255,255,0.15)'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(pad.left, pad.top); ctx.lineTo(pad.left, pad.top + plotH);
        ctx.lineTo(W - pad.right, pad.top + plotH); ctx.stroke();

        // Axes labels
        ctx.fillStyle = '#64748b'; ctx.font = '11px Inter'; ctx.textAlign = 'center';
        ctx.fillText('Time (s)', pad.left + plotW / 2, H - 8);
        ctx.save(); ctx.translate(14, pad.top + plotH / 2); ctx.rotate(-Math.PI / 2);
        ctx.fillText('Absorbance', 0, 0); ctx.restore();

        // Line
        ctx.beginPath();
        data.forEach((d, i) => {
            const x = pad.left + (d.wl / maxT) * plotW;
            const y = pad.top + plotH - (d.abs / maxA) * plotH;
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        });
        ctx.strokeStyle = '#10b981'; ctx.lineWidth = 2; ctx.stroke();

        ctx.fillStyle = '#94a3b8'; ctx.font = '12px Inter'; ctx.textAlign = 'left';
        ctx.fillText('Kinetics — Absorbance vs Time', pad.left + 8, pad.top - 12);
    }

    function runCalibration() {
        if (!state.selectedCompound) { toast('Select a compound first', 'warning'); return; }
        if (!state.blanked) { toast('Auto-zero first', 'warning'); return; }
        const wl = parseFloat($('cal-wavelength').value) || 254;
        const concentrations = [2, 4, 6, 8, 10];
        const pL = state.instrumentSettings.pathLength;

        state.calibData.standards = concentrations.map(c => {
            let abs = calculateAbsorbance(state.selectedCompound, wl, c, pL);
            abs = applyFaultEffects(abs, wl, state.activeFault);
            return { x: c, y: Math.max(0, abs) };
        });

        state.calibData.regression = linearRegression(state.calibData.standards);
        const reg = state.calibData.regression;

        // Show calibration canvas
        spectrumCanvas.style.display = 'none';
        calibCanvas.style.display = 'block';
        $$('.canvas-tab').forEach(t => t.classList.toggle('active', t.dataset.canvas === 'calibration'));

        drawCalibration();
        $('btn-measure-unknown').disabled = false;

        // Update calc display
        const calcDiv = $('calc-display');
        calcDiv.innerHTML = `
            <div class="equation">A = ${reg.slope.toFixed(4)}·C + ${reg.intercept.toFixed(4)}</div>
            <p style="color:#94a3b8;font-size:0.85em">R² = <strong style="color:${reg.r2 > 0.999 ? '#10b981' : '#f59e0b'}">${reg.r2.toFixed(6)}</strong></p>
            <p style="color:#64748b;font-size:0.78em">LOD = ${(3.3 * 0.002 / reg.slope).toFixed(3)} mg/L</p>
            <p style="color:#64748b;font-size:0.78em">LOQ = ${(10 * 0.002 / reg.slope).toFixed(3)} mg/L</p>`;

        // Update validation
        const vl = $('validation-list');
        const lod = 3.3 * 0.002 / reg.slope;
        const loq = 10 * 0.002 / reg.slope;
        vl.innerHTML = `
            <div class="val-item"><span>λ Accuracy</span><span class="val-status pass">± 0.3 nm ✓</span></div>
            <div class="val-item"><span>Abs Accuracy</span><span class="val-status pass">± 0.003 ✓</span></div>
            <div class="val-item"><span>Linearity (R²)</span><span class="val-status ${reg.r2 > 0.999 ? 'pass' : 'fail'}">${reg.r2.toFixed(5)} ${reg.r2 > 0.999 ? '✓' : '✗'}</span></div>
            <div class="val-item"><span>LOD</span><span class="val-status pass">${lod.toFixed(3)} mg/L</span></div>
            <div class="val-item"><span>LOQ</span><span class="val-status pass">${loq.toFixed(3)} mg/L</span></div>`;

        toast('Calibration complete — 5 standards measured', 'success');
    }

    function measureUnknown() {
        if (!state.calibData.regression) { toast('Run calibration first', 'warning'); return; }
        const trueConc = parseFloat($('cal-unknown').value) || 5.5;
        const wl = parseFloat($('cal-wavelength').value) || 254;
        let abs = calculateAbsorbance(state.selectedCompound, wl, trueConc, state.instrumentSettings.pathLength);
        abs = applyFaultEffects(abs, wl, state.activeFault);
        const reg = state.calibData.regression;
        const calcConc = (abs - reg.intercept) / reg.slope;
        const error = ((calcConc - trueConc) / trueConc * 100).toFixed(2);

        const res = $('cal-results');
        res.style.display = 'block';
        res.innerHTML = `<p>Absorbance: <strong>${abs.toFixed(4)}</strong></p>
            <p>Calculated: <strong>${calcConc.toFixed(3)} mg/L</strong></p>
            <p>True: <strong>${trueConc.toFixed(1)} mg/L</strong></p>
            <p>Error: <strong style="color:${Math.abs(error) < 2 ? '#10b981' : '#ef4444'}">${error}%</strong></p>`;
        toast(`Unknown analyzed: ${calcConc.toFixed(3)} mg/L (error: ${error}%)`, 'success');
    }

    function updateCalcDisplay() {
        if (state.detectedPeaks.length === 0) return;
        const compound = state.selectedCompound;
        if (!compound) return;
        const primary = state.detectedPeaks[0];
        const calcDiv = $('calc-display');
        calcDiv.innerHTML = `
            <p style="font-size:0.85em;color:#94a3b8">Primary Peak:</p>
            <div class="equation">λmax = ${primary.wl.toFixed(1)} nm</div>
            <div class="equation">Abs = ${primary.abs.toFixed(4)}</div>
            <p style="font-size:0.78em;color:#64748b;margin-top:6px">A = εlc (Beer-Lambert Law)</p>
            <p style="font-size:0.78em;color:#64748b">Path: ${state.instrumentSettings.pathLength} cm</p>`;
    }

    // ========================================================================
    // EVENT LISTENERS
    // ========================================================================
    function init() {
        populateCompounds();
        drawSpectrum();

        // Power
        $('btn-power').addEventListener('click', () => {
            state.powerOn = !state.powerOn;
            if (state.powerOn) {
                $('lamp-glow').style.animationPlayState = 'running';
                document.querySelectorAll('.beam-line').forEach(b => b.classList.add('active'));
                $('disp-status').textContent = 'Ready';
                $('status-dot').className = 'fas fa-circle';
                toast('Spectrophotometer powered ON', 'success');
            } else {
                $('lamp-glow').style.animationPlayState = 'paused';
                document.querySelectorAll('.beam-line').forEach(b => b.classList.remove('active'));
                $('disp-status').textContent = 'OFF';
                $('status-dot').className = 'fas fa-circle error';
                toast('Spectrophotometer powered OFF', 'warning');
            }
        });

        // Auto-zero
        $('btn-autozero').addEventListener('click', () => {
            if (!state.powerOn) { toast('Power on the instrument first', 'warning'); return; }
            state.blanked = true;
            $('disp-status').textContent = 'Blanked';
            updateDisplay(254, 0);
            toast('Auto-zero complete — baseline set', 'success');
        });

        // Enter analysis screen
        $('btn-enter-screen').addEventListener('click', () => {
            if (!state.powerOn) { toast('Power on the instrument first', 'warning'); return; }
            switchView('analysis');
        });
        $('back-to-instrument').addEventListener('click', () => switchView('instrument'));

        // Mode tabs
        $$('.mode-tab').forEach(tab => tab.addEventListener('click', () => switchMode(tab.dataset.mode)));

        // Compound select
        $('compound-select').addEventListener('change', (e) => selectCompound(e.target.value));

        // Hotspots → modals
        $$('.hotspot').forEach(hs => hs.addEventListener('click', () => {
            const modalId = hs.dataset.modal;
            if (modalId) openModal(modalId);
        }));

        // Modal close
        $$('[data-close]').forEach(btn => btn.addEventListener('click', function () { closeModal(this); }));
        $$('.modal-overlay').forEach(ov => ov.addEventListener('click', function (e) {
            if (e.target === this) this.classList.remove('active');
        }));

        // Analysis actions
        $('btn-run-scan').addEventListener('click', runScan);
        $('btn-clear-scan').addEventListener('click', () => {
            state.scanData = []; state.detectedPeaks = [];
            drawSpectrum(); updatePeakTable();
            $('calc-display').innerHTML = '<p class="calc-placeholder">Run a measurement to see results</p>';
        });
        $('btn-measure-fixed').addEventListener('click', measureFixed);
        $('btn-start-kinetics').addEventListener('click', runKinetics);
        $('btn-stop-kinetics').addEventListener('click', stopKinetics);
        $('btn-run-calibration').addEventListener('click', runCalibration);
        $('btn-measure-unknown').addEventListener('click', measureUnknown);

        // Canvas tabs
        $$('.canvas-tab').forEach(tab => tab.addEventListener('click', () => {
            $$('.canvas-tab').forEach(t => t.classList.toggle('active', t === tab));
            if (tab.dataset.canvas === 'spectrum') {
                spectrumCanvas.style.display = 'block'; calibCanvas.style.display = 'none';
                drawSpectrum();
            } else {
                spectrumCanvas.style.display = 'none'; calibCanvas.style.display = 'block';
                drawCalibration();
            }
        }));

        // Toggle Abs/T
        $('btn-toggle-axis').addEventListener('click', () => {
            state.showTransmittance = !state.showTransmittance;
            drawSpectrum();
            toast(state.showTransmittance ? 'Showing %Transmittance' : 'Showing Absorbance', 'info');
        });

        // Zoom
        $('btn-zoom-in').addEventListener('click', () => { state.zoom = Math.min(state.zoom * 1.5, 10); drawSpectrum(); });
        $('btn-zoom-out').addEventListener('click', () => { state.zoom = Math.max(state.zoom / 1.5, 0.5); drawSpectrum(); });
        $('btn-reset-zoom').addEventListener('click', () => { state.zoom = 1; drawSpectrum(); });

        // Difficulty
        $$('.difficulty-btn').forEach(btn => btn.addEventListener('click', () => {
            $$('.difficulty-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.difficulty = btn.dataset.level;
            $('fault-section').style.display = btn.dataset.level === 'advanced' ? 'block' : 'none';
            toast(`Difficulty: ${btn.dataset.level}`, 'info');
        }));

        // Fault select
        $('fault-select').addEventListener('change', (e) => { state.activeFault = e.target.value; });

        // Slider live updates
        $('slit-width').addEventListener('input', (e) => {
            $('slit-width-val').textContent = parseFloat(e.target.value).toFixed(1) + ' nm';
            state.instrumentSettings.slitWidth = parseFloat(e.target.value);
        });
        $('integration-time').addEventListener('input', (e) => {
            $('integration-time-val').textContent = e.target.value + ' ms';
            state.instrumentSettings.integrationTime = parseInt(e.target.value);
        });

        // Settings sync from modals
        $$('.modal-apply').forEach(btn => btn.addEventListener('click', () => {
            const s = state.instrumentSettings;
            s.uvSource = $('uv-source').value;
            s.visSource = $('vis-source').value;
            s.sourceSwitch = $('source-switch').value;
            s.gratingType = $('grating-type').value;
            s.cuvetteMaterial = $('cuvette-material').value;
            s.pathLength = parseFloat($('path-length').value);
            s.refSolvent = $('ref-solvent').value;
            s.detectorType = $('detector-type').value;
            s.sensitivity = $('detector-sensitivity').value;
            updateQuickStats();
            toast('Settings applied', 'success');
        }));

        // Fullscreen
        $('btn-fullscreen')?.addEventListener('click', () => {
            if (!document.fullscreenElement) document.documentElement.requestFullscreen();
            else document.exitFullscreen();
        });

        // Export
        $('btn-export-data')?.addEventListener('click', () => {
            if (state.scanData.length === 0) { toast('No data to export', 'warning'); return; }
            let csv = 'Wavelength (nm),Absorbance,%Transmittance\n';
            for (const d of state.scanData) {
                csv += `${d.wl.toFixed(1)},${d.abs.toFixed(4)},${(Math.pow(10, -d.abs) * 100).toFixed(2)}\n`;
            }
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href = url;
            a.download = `uvvis_${state.selectedCompound?.name || 'data'}_${Date.now()}.csv`;
            a.click(); URL.revokeObjectURL(url);
            toast('Data exported as CSV', 'success');
        });

        // Tutorial
        $('tutorial-btn')?.addEventListener('click', startTutorial);

        // Auto power on after 1s
        setTimeout(() => { $('btn-power').click(); }, 800);
    }

    function startTutorial() {
        if (typeof Shepherd === 'undefined') return;
        const tour = new Shepherd.Tour({
            useModalOverlay: true,
            defaultStepOptions: { classes: 'shepherd-tour', scrollTo: { behavior: 'smooth', block: 'center' }, cancelIcon: { enabled: true } }
        });
        tour.addStep({ title: 'Welcome!', text: 'This is the SimuPharma UV-Vis Spectrophotometer Simulator. Let\'s learn how it works!', buttons: [{ text: 'Next', action: tour.next }] });
        tour.addStep({ title: 'Light Source', text: 'The spectrophotometer uses a Deuterium lamp for UV and a Tungsten lamp for visible light. Click the hotspot to configure.', attachTo: { element: '#hotspot-source', on: 'bottom' }, buttons: [{ text: 'Back', action: tour.back }, { text: 'Next', action: tour.next }] });
        tour.addStep({ title: 'Monochromator', text: 'The monochromator uses a diffraction grating to select a specific wavelength from the white light. Slit width controls resolution vs sensitivity.', attachTo: { element: '#hotspot-mono', on: 'bottom' }, buttons: [{ text: 'Back', action: tour.back }, { text: 'Next', action: tour.next }] });
        tour.addStep({ title: 'Sample Compartment', text: 'Your sample in a cuvette is placed here. The Beer-Lambert Law (A = εlc) governs how much light is absorbed.', attachTo: { element: '#hotspot-sample', on: 'bottom' }, buttons: [{ text: 'Back', action: tour.back }, { text: 'Next', action: tour.next }] });
        tour.addStep({ title: 'Detector', text: 'The PMT detector measures the transmitted light intensity. The ratio vs blank gives absorbance.', attachTo: { element: '#hotspot-detector', on: 'bottom' }, buttons: [{ text: 'Back', action: tour.back }, { text: 'Next', action: tour.next }] });
        tour.addStep({ title: 'Start Analyzing!', text: '1) Power on → 2) Auto-zero → 3) Open Analysis screen → 4) Select compound → 5) Run scan. Try it!', buttons: [{ text: 'Finish', action: tour.complete }] });
        tour.start();
    }

    init();
});