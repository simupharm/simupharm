/**
 * ============================================================================
 * SimuPharma Advanced Mass Spectrometer Digital Twin v2.0
 * ============================================================================
 * Features:
 * - Realistic EI/ESI/APCI fragmentation simulation
 * - 10 pharmaceutical compound library with real fragmentation patterns
 * - Isotope pattern calculation (M, M+1, M+2)
 * - Startup wizard (vacuum pump-down → source heating → auto-tune)
 * - Fault simulation (air leak, dirty source, weak detector)
 * - Interactive Chart.js stick spectrum
 * - Library search, report generation, data export
 * ============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // ========================================================================
    // COMPOUND LIBRARY — Real Pharmaceutical Fragmentation Data
    // ========================================================================
    const COMPOUND_LIBRARY = {
        Paracetamol: {
            name: 'Paracetamol (Acetaminophen)', formula: 'C8H9NO2', mw: 151.16,
            cas: '103-90-2', category: 'Analgesic',
            fragments: [
                { mz: 151, intensity: 25, assignment: 'M⁺ (molecular ion)' },
                { mz: 109, intensity: 100, assignment: '[M-COCH2]⁺ (loss of ketene)' },
                { mz: 80, intensity: 45, assignment: '[M-COCH2-CHO]⁺' },
                { mz: 108, intensity: 30, assignment: '[M-COCH3]⁺ (loss of acetyl)' },
                { mz: 43, intensity: 60, assignment: 'CH3CO⁺ (acetyl cation)' },
                { mz: 65, intensity: 15, assignment: 'C5H5⁺ (cyclopentadienyl)' },
                { mz: 52, intensity: 10, assignment: 'C3H2NO⁺' },
                { mz: 81, intensity: 20, assignment: 'C5H5O⁺' }
            ],
            elements: { C: 8, H: 9, N: 1, O: 2 }
        },
        Aspirin: {
            name: 'Aspirin (Acetylsalicylic Acid)', formula: 'C9H8O4', mw: 180.16,
            cas: '50-78-2', category: 'NSAID',
            fragments: [
                { mz: 180, intensity: 15, assignment: 'M⁺ (molecular ion)' },
                { mz: 138, intensity: 55, assignment: '[M-COCH2]⁺ (loss of ketene)' },
                { mz: 120, intensity: 100, assignment: '[M-CH3COOH]⁺ (loss of acetic acid)' },
                { mz: 92, intensity: 40, assignment: '[M-CH3COOH-CO]⁺' },
                { mz: 43, intensity: 80, assignment: 'CH3CO⁺ (acetyl cation)' },
                { mz: 64, intensity: 20, assignment: 'C5H4⁺' },
                { mz: 39, intensity: 25, assignment: 'C3H3⁺' }
            ],
            elements: { C: 9, H: 8, O: 4 }
        },
        Caffeine: {
            name: 'Caffeine', formula: 'C8H10N4O2', mw: 194.19,
            cas: '58-08-2', category: 'Alkaloid',
            fragments: [
                { mz: 194, intensity: 100, assignment: 'M⁺ (molecular ion)' },
                { mz: 109, intensity: 35, assignment: '[M-C2H5N2O]⁺' },
                { mz: 82, intensity: 25, assignment: '[M-C3H4N2O2]⁺' },
                { mz: 67, intensity: 50, assignment: 'C3H3N2⁺' },
                { mz: 55, intensity: 30, assignment: 'C2H3N2⁺' },
                { mz: 42, intensity: 20, assignment: 'C2H4NO⁺ / NCO⁺' },
                { mz: 137, intensity: 15, assignment: '[M-C2H3NO]⁺' }
            ],
            elements: { C: 8, H: 10, N: 4, O: 2 }
        },
        Ibuprofen: {
            name: 'Ibuprofen', formula: 'C13H18O2', mw: 206.28,
            cas: '15687-27-1', category: 'NSAID',
            fragments: [
                { mz: 206, intensity: 20, assignment: 'M⁺ (molecular ion)' },
                { mz: 161, intensity: 100, assignment: '[M-COOH]⁺ (loss of carboxyl)' },
                { mz: 119, intensity: 30, assignment: '[M-C4H7O2]⁺' },
                { mz: 91, intensity: 25, assignment: 'C7H7⁺ (tropylium)' },
                { mz: 77, intensity: 15, assignment: 'C6H5⁺ (phenyl)' },
                { mz: 163, intensity: 40, assignment: '[M-C2H3O]⁺' },
                { mz: 145, intensity: 10, assignment: '[M-C2H3O-H2O]⁺' }
            ],
            elements: { C: 13, H: 18, O: 2 }
        },
        Diclofenac: {
            name: 'Diclofenac', formula: 'C14H11Cl2NO2', mw: 295.15,
            cas: '15307-86-5', category: 'NSAID',
            fragments: [
                { mz: 295, intensity: 15, assignment: 'M⁺ (molecular ion) ³⁵Cl₂' },
                { mz: 297, intensity: 10, assignment: 'M+2 (³⁵Cl³⁷Cl)' },
                { mz: 250, intensity: 100, assignment: '[M-COOH]⁺' },
                { mz: 214, intensity: 60, assignment: '[M-COOH-HCl]⁺' },
                { mz: 215, intensity: 20, assignment: '[M-COOH-Cl+H]⁺' },
                { mz: 179, intensity: 30, assignment: '[M-COOH-2HCl+H]⁺' },
                { mz: 152, intensity: 15, assignment: 'C8H7ClNO⁺' }
            ],
            elements: { C: 14, H: 11, Cl: 2, N: 1, O: 2 }
        },
        Metformin: {
            name: 'Metformin HCl', formula: 'C4H11N5', mw: 129.16,
            cas: '657-24-9', category: 'Antidiabetic',
            fragments: [
                { mz: 130, intensity: 20, assignment: '[M+H]⁺' },
                { mz: 129, intensity: 10, assignment: 'M⁺ (molecular ion)' },
                { mz: 113, intensity: 5, assignment: '[M-NH2]⁺' },
                { mz: 88, intensity: 40, assignment: '[M-CH3NH]⁺' },
                { mz: 71, intensity: 100, assignment: 'C2H5N3⁺ (guanidine fragment)' },
                { mz: 60, intensity: 80, assignment: 'CH4N3⁺' },
                { mz: 44, intensity: 50, assignment: 'CH2N2⁺' }
            ],
            elements: { C: 4, H: 11, N: 5 }
        },
        Omeprazole: {
            name: 'Omeprazole', formula: 'C17H19N3O3S', mw: 345.42,
            cas: '73590-58-6', category: 'PPI',
            fragments: [
                { mz: 345, intensity: 10, assignment: 'M⁺ (molecular ion)' },
                { mz: 329, intensity: 5, assignment: '[M-O]⁺' },
                { mz: 297, intensity: 30, assignment: '[M-SO]⁺ (or similar)' },
                { mz: 198, intensity: 70, assignment: 'Benzimidazole portion' },
                { mz: 180, intensity: 40, assignment: '[198-H2O]⁺' },
                { mz: 151, intensity: 25, assignment: 'Pyridine-methyl fragment' },
                { mz: 136, intensity: 100, assignment: 'Pyridine ring fragment' }
            ],
            elements: { C: 17, H: 19, N: 3, O: 3, S: 1 }
        },
        Amoxicillin: {
            name: 'Amoxicillin', formula: 'C16H19N3O5S', mw: 365.40,
            cas: '26787-78-0', category: 'Antibiotic',
            fragments: [
                { mz: 366, intensity: 15, assignment: '[M+H]⁺' },
                { mz: 349, intensity: 50, assignment: '[M+H-NH3]⁺' },
                { mz: 208, intensity: 40, assignment: 'Thiazolidine ring fragment' },
                { mz: 189, intensity: 30, assignment: '[208-NH3]⁺' },
                { mz: 160, intensity: 100, assignment: 'Aminobenzoyl fragment' },
                { mz: 114, intensity: 60, assignment: 'β-lactam ring fragment' },
                { mz: 107, intensity: 20, assignment: 'p-Hydroxyphenyl⁺' }
            ],
            elements: { C: 16, H: 19, N: 3, O: 5, S: 1 }
        },
        Ciprofloxacin: {
            name: 'Ciprofloxacin', formula: 'C17H18FN3O3', mw: 331.34,
            cas: '85721-33-1', category: 'Antibiotic',
            fragments: [
                { mz: 332, intensity: 30, assignment: '[M+H]⁺' },
                { mz: 314, intensity: 40, assignment: '[M+H-H2O]⁺' },
                { mz: 288, intensity: 100, assignment: '[M+H-CO2]⁺' },
                { mz: 245, intensity: 50, assignment: '[M-piperazine]⁺' },
                { mz: 231, intensity: 25, assignment: 'Quinolone core⁺' },
                { mz: 204, intensity: 15, assignment: '[Quinolone-HCN]⁺' }
            ],
            elements: { C: 17, H: 18, F: 1, N: 3, O: 3 }
        },
        Atorvastatin: {
            name: 'Atorvastatin', formula: 'C33H35FN2O5', mw: 558.64,
            cas: '134523-00-5', category: 'Statin',
            fragments: [
                { mz: 559, intensity: 20, assignment: '[M+H]⁺' },
                { mz: 541, intensity: 15, assignment: '[M+H-H2O]⁺' },
                { mz: 440, intensity: 100, assignment: '[M+H-side chain]⁺' },
                { mz: 422, intensity: 40, assignment: '[440-H2O]⁺' },
                { mz: 380, intensity: 30, assignment: 'Pyrrole substructure' },
                { mz: 292, intensity: 15, assignment: 'Phenyl-pyrrole core' },
                { mz: 250, intensity: 10, assignment: 'Further fragmentation' }
            ],
            elements: { C: 33, H: 35, F: 1, N: 2, O: 5 }
        }
    };

    // Isotope data for calculation
    const ISOTOPE_DATA = {
        C: { mass: 12, m1: 0.0111, m2: 0 },
        H: { mass: 1, m1: 0.000115, m2: 0 },
        N: { mass: 14, m1: 0.00366, m2: 0 },
        O: { mass: 16, m1: 0.000038, m2: 0.00205 },
        S: { mass: 32, m1: 0.0076, m2: 0.0442 },
        Cl: { mass: 35, m1: 0, m2: 0.3240 },
        F: { mass: 19, m1: 0, m2: 0 },
        Br: { mass: 79, m1: 0, m2: 0.9730 }
    };

    // Fault definitions
    const FAULTS = {
        none: { noise: 1, sensitivity: 1, extraPeaks: [] },
        'air-leak': {
            noise: 2.5, sensitivity: 0.7, extraPeaks: [
                { mz: 18, intensity: 40, assignment: 'H₂O⁺ (air leak)' },
                { mz: 28, intensity: 85, assignment: 'N₂⁺ (air leak)' },
                { mz: 32, intensity: 45, assignment: 'O₂⁺ (air leak)' },
                { mz: 44, intensity: 20, assignment: 'CO₂⁺ (air leak)' }
            ]
        },
        'dirty-source': {
            noise: 4, sensitivity: 0.5, extraPeaks: [
                { mz: 149, intensity: 30, assignment: 'Phthalate contaminant' },
                { mz: 167, intensity: 15, assignment: 'Phthalate contaminant' },
                { mz: 279, intensity: 10, assignment: 'Column bleed (siloxane)' }
            ]
        },
        'low-em': { noise: 1.5, sensitivity: 0.3, extraPeaks: [] }
    };

    // ========================================================================
    // APPLICATION STATE
    // ========================================================================
    const STATE = {
        systemReady: false,
        wizardStep: 1,
        ionMode: 'EI',
        analyzerType: 'quadrupole',
        inletType: 'direct',
        selectedCompound: 'Paracetamol',
        sourceTemp: 200,
        electronEnergy: 70,
        emVoltage: 1600,
        mzStart: 50,
        mzEnd: 600,
        scanSpeed: 5,
        currentFault: 'none',
        isScanning: false,
        isPaused: false,
        instantMode: false,
        lastScanData: null,
        difficulty: 'beginner',
        scanTimer: null,
        elapsedMs: 0
    };

    // ========================================================================
    // DOM CACHE
    // ========================================================================
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    let msChart = null;

    // ========================================================================
    // ISOTOPE PATTERN CALCULATION
    // ========================================================================
    function calculateIsotopePattern(elements) {
        let m1Contribution = 0;
        let m2Contribution = 0;
        for (const [el, count] of Object.entries(elements)) {
            const iso = ISOTOPE_DATA[el];
            if (!iso) continue;
            m1Contribution += count * iso.m1;
            m2Contribution += count * iso.m2;
        }
        // Binomial approximation
        const m0 = 100;
        const m1 = m1Contribution * 100;
        const m2 = (m2Contribution + (m1Contribution * m1Contribution / 2)) * 100;
        return [
            { label: 'M', intensity: m0 },
            { label: 'M+1', intensity: Math.round(m1 * 10) / 10 },
            { label: 'M+2', intensity: Math.round(m2 * 10) / 10 }
        ];
    }

    // ========================================================================
    // SPECTRUM GENERATION
    // ========================================================================
    function generateSpectrum() {
        const compound = COMPOUND_LIBRARY[STATE.selectedCompound];
        if (!compound) return null;

        const fault = FAULTS[STATE.currentFault];
        let fragments = [...compound.fragments];

        // Add fault-specific extra peaks
        if (fault.extraPeaks.length > 0) {
            fragments = [...fault.extraPeaks, ...fragments];
        }

        // Apply ionization mode effects
        if (STATE.ionMode === 'ESI') {
            // ESI: soft ionization — strong [M+H]+ with minimal fragmentation
            fragments = fragments.map(f => {
                if (f.mz === Math.round(compound.mw)) {
                    return { ...f, mz: f.mz + 1, intensity: 100, assignment: '[M+H]⁺' };
                }
                return { ...f, intensity: Math.round(f.intensity * 0.2) };
            });
            // Add protonated molecular ion if not present
            const mhMz = Math.round(compound.mw) + 1;
            if (!fragments.find(f => f.mz === mhMz)) {
                fragments.unshift({ mz: mhMz, intensity: 100, assignment: '[M+H]⁺' });
            }
        } else if (STATE.ionMode === 'APCI') {
            // APCI: medium fragmentation
            fragments = fragments.map(f => ({
                ...f, intensity: Math.round(f.intensity * (f.mz > compound.mw * 0.5 ? 1.2 : 0.6))
            }));
        }

        // Apply sensitivity and noise from faults
        fragments = fragments.map(f => ({
            ...f,
            intensity: Math.max(1, Math.round(f.intensity * fault.sensitivity +
                (Math.random() - 0.5) * fault.noise * 5))
        })).filter(f => f.intensity > 0);

        // Add noise floor
        const noiseFloor = [];
        for (let mz = STATE.mzStart; mz <= STATE.mzEnd; mz += Math.random() * 20 + 5) {
            noiseFloor.push({
                mz: Math.round(mz),
                intensity: Math.round(Math.random() * fault.noise * 2),
                assignment: ''
            });
        }

        // Normalize to base peak = 100%
        const allFrags = [...fragments, ...noiseFloor];
        const maxI = Math.max(...allFrags.map(f => f.intensity));
        const normalized = allFrags.map(f => ({
            ...f,
            intensity: Math.round((f.intensity / maxI) * 100)
        })).filter(f => f.intensity >= 1);

        // Sort by m/z
        normalized.sort((a, b) => a.mz - b.mz);

        // Calculate isotope pattern
        const isotopes = calculateIsotopePattern(compound.elements);

        return {
            compound: compound,
            fragments: normalized.filter(f => f.assignment),
            allPeaks: normalized,
            isotopes: isotopes,
            basePeak: fragments.reduce((max, f) => f.intensity > max.intensity ? f : max, fragments[0]),
            molecularIon: Math.round(compound.mw)
        };
    }

    // ========================================================================
    // CHART INITIALIZATION & UPDATE
    // ========================================================================
    function initChart() {
        const ctx = $('#hplc-chart');
        if (!ctx) return;

        msChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Relative Intensity (%)',
                    data: [],
                    backgroundColor: 'rgba(59,130,246,0.8)',
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    barThickness: 2,
                    maxBarThickness: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 600, easing: 'easeOutQuart' },
                interaction: { mode: 'nearest', axis: 'x', intersect: false },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15,23,42,0.95)',
                        titleFont: { family: 'JetBrains Mono', size: 12 },
                        bodyFont: { family: 'Inter', size: 11 },
                        borderColor: '#334155', borderWidth: 1,
                        padding: 10,
                        callbacks: {
                            title: (ctx) => `m/z ${ctx[0].label}`,
                            label: (ctx) => {
                                const peak = STATE.lastScanData?.allPeaks.find(p => p.mz == ctx.label);
                                const lines = [`Intensity: ${ctx.raw}%`];
                                if (peak?.assignment) lines.push(`${peak.assignment}`);
                                return lines;
                            }
                        }
                    },
                    zoom: {
                        zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'x' },
                        pan: { enabled: true, mode: 'x' }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'm/z', color: '#94a3b8', font: { family: 'Inter', size: 12 } },
                        grid: { color: 'rgba(148,163,184,0.08)' },
                        ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 }, maxTicksLimit: 20 }
                    },
                    y: {
                        title: { display: true, text: 'Relative Intensity (%)', color: '#94a3b8', font: { family: 'Inter', size: 12 } },
                        min: 0, max: 110,
                        grid: { color: 'rgba(148,163,184,0.08)' },
                        ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } }
                    }
                }
            }
        });
    }

    function updateChart(data) {
        if (!msChart || !data) return;
        msChart.data.labels = data.allPeaks.map(p => p.mz);
        msChart.data.datasets[0].data = data.allPeaks.map(p => p.intensity);
        // Color base peak differently
        msChart.data.datasets[0].backgroundColor = data.allPeaks.map(p =>
            p.assignment ? 'rgba(59,130,246,0.9)' : 'rgba(100,116,139,0.3)'
        );
        msChart.update();
    }

    // ========================================================================
    // FRAGMENT TABLE
    // ========================================================================
    function updateFragmentTable(data) {
        const tbody = $('#fragment-tbody');
        if (!tbody || !data) return;
        const frags = data.fragments.sort((a, b) => b.intensity - a.intensity).slice(0, 12);
        tbody.innerHTML = frags.map(f => `
            <tr>
                <td style="font-weight:600;color:#3b82f6">${f.mz}</td>
                <td>${f.intensity}%</td>
                <td style="font-family:Inter;font-size:11px;color:#94a3b8">${f.assignment}</td>
                <td class="bar-cell"><div class="frag-bar" style="width:${f.intensity}%"></div></td>
            </tr>
        `).join('');
    }

    // ========================================================================
    // ISOTOPE PATTERN DISPLAY
    // ========================================================================
    function updateIsotopeDisplay(data) {
        const container = $('#isotope-bars');
        const patternDiv = $('#isotope-pattern-display');
        if (!container || !data) return;
        patternDiv.querySelector('h6').textContent = `Isotope Pattern — ${data.compound.formula}`;
        const maxI = Math.max(...data.isotopes.map(i => i.intensity));
        container.innerHTML = data.isotopes.map(iso => {
            const h = Math.max(4, (iso.intensity / maxI) * 50);
            return `<div class="bar" style="height:${h}px"><span>${iso.intensity.toFixed(1)}%</span></div>`;
        }).join('');
        // Add labels below
        container.innerHTML += `<div style="display:flex;gap:3px;margin-top:4px;font-size:9px;color:#64748b">
            ${data.isotopes.map(i => `<span style="width:18px;text-align:center">${i.label}</span>`).join('')}
        </div>`;
    }

    // ========================================================================
    // MOLECULAR ION INFO
    // ========================================================================
    function updateMolIonInfo(data) {
        if (!data) return;
        $('#molecular-ion-mz').textContent = data.molecularIon;
        $('#mol-formula').textContent = data.compound.formula;
        $('#mol-weight').textContent = data.compound.mw.toFixed(2);
    }

    // ========================================================================
    // TOAST NOTIFICATION
    // ========================================================================
    function toast(message, type = 'info') {
        const container = $('#toast-container');
        const t = document.createElement('div');
        t.className = `toast ${type}`;
        const icons = { info: 'info-circle', success: 'check-circle', warning: 'exclamation-triangle', error: 'times-circle' };
        t.innerHTML = `<i class="fas fa-${icons[type]}"></i><span>${message}</span>`;
        t.style.cssText = 'display:flex;align-items:center;gap:10px;padding:12px 20px;border-radius:10px;margin-bottom:8px;font-size:13px;color:#fff;animation:slideIn 0.3s ease;';
        const colors = { info: '#3b82f6', success: '#22c55e', warning: '#f59e0b', error: '#ef4444' };
        t.style.background = colors[type];
        container.appendChild(t);
        setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 300); }, 4000);
    }

    // ========================================================================
    // LOG SYSTEM
    // ========================================================================
    function addLog(msg, type = 'info') {
        const log = $('#log-content');
        if (!log) return;
        const time = new Date().toLocaleTimeString();
        const colors = { info: '#3b82f6', success: '#22c55e', warning: '#f59e0b', error: '#ef4444' };
        log.innerHTML += `<div style="font-size:11px;padding:3px 0;color:${colors[type] || '#94a3b8'};font-family:'JetBrains Mono',monospace">
            <span style="color:#64748b">[${time}]</span> ${msg}</div>`;
        log.scrollTop = log.scrollHeight;
    }

    // ========================================================================
    // STARTUP WIZARD
    // ========================================================================
    function goToWizardStep(step) {
        STATE.wizardStep = step;
        $$('.wizard-step').forEach((ws, i) => {
            ws.classList.toggle('active', i < step);
            ws.classList.toggle('completed', i < step - 1);
        });
        $$('.wizard-panel').forEach((wp, i) => wp.classList.toggle('active', i === step - 1));
        $('#wizard-prev-btn').disabled = step <= 1;
        $('#wizard-next-btn').classList.toggle('hidden', step >= 4);
        $('#wizard-finish-btn').classList.toggle('hidden', step < 4);
    }

    function runPumpDown() {
        $('#btn-pumpdown').disabled = true;
        addLog('▶ Fore-pump (rotary vane) started — roughing vacuum', 'info');
        addLog('  Target: < 5 × 10⁻⁶ Torr for EI operation', 'info');
        toast('Starting vacuum pump-down sequence...', 'info');

        // Realistic pressure decay: atmospheric → rough → high → ultra-high
        let pressure = 760; // Start at atmospheric (Torr)
        let elapsed = 0;
        const stages = [
            { name: 'Roughing', pump: 'Rotary Vane', target: 0.1, rate: 0.88, next: 30 },
            { name: 'High Vacuum', pump: 'Turbo-molecular', target: 1e-4, rate: 0.82, next: 60 },
            { name: 'Ultra-High Vacuum', pump: 'Turbo + Ion Gauge', target: 2.4e-6, rate: 0.90, next: 100 }
        ];
        let stageIdx = 0;

        const formatPressure = (p) => {
            if (p >= 1) return p.toFixed(1) + ' Torr';
            if (p >= 0.001) return (p * 1000).toFixed(1) + ' mTorr';
            const exp = Math.floor(Math.log10(p));
            const mantissa = p / Math.pow(10, exp);
            return mantissa.toFixed(1) + ' × 10' + (exp < 0 ? '⁻' : '') + Math.abs(exp).toString().split('').map(d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]).join('') + ' Torr';
        };

        const interval = setInterval(() => {
            elapsed += 2;
            const stage = stages[stageIdx];
            pressure *= stage.rate;
            if (pressure < stage.target) pressure = stage.target;

            // Update live pressure display
            $('#status-vacuum').textContent = formatPressure(pressure);

            if (stageIdx === 0 && pressure <= stages[0].target) {
                stageIdx = 1;
                $('#status-forepump').textContent = '✓ Running';
                $('#status-forepump').className = 'status-value complete';
                $('#status-turbo').textContent = 'Accelerating...';
                $('#status-turbo').className = 'status-value progress';
                addLog('  Roughing complete — switching to turbo-molecular pump', 'info');
                addLog('  Turbo rotor accelerating to 60,000 RPM...', 'info');
            }
            if (stageIdx === 1 && pressure <= stages[1].target) {
                stageIdx = 2;
                $('#status-turbo').textContent = '✓ 60,000 RPM';
                $('#status-turbo').className = 'status-value complete';
                addLog('  High vacuum reached — ion gauge activated', 'info');
                addLog('  Monitoring for outgassing...', 'info');
            }
            if (stageIdx === 2 && pressure <= stages[2].target) {
                clearInterval(interval);
                $('#status-vacuum').textContent = '✓ 2.4 × 10⁻⁶ Torr';
                $('#status-vacuum').className = 'status-value complete';
                $('#qs-vacuum').textContent = '2.4e-6';
                addLog('✓ Operating vacuum achieved: 2.4 × 10⁻⁶ Torr', 'success');
                addLog('  Leak rate < 10⁻⁹ Torr·L/s — within specification', 'success');
                toast('Vacuum system ready', 'success');
                $('#wizard-next-btn').disabled = false;
                $('#btn-heat-source').disabled = false;
            }
        }, 80);
    }

    function runSourceHeat() {
        $('#btn-heat-source').disabled = true;
        const target = STATE.sourceTemp;
        addLog('▶ Heating EI ion source to ' + target + '°C', 'info');
        addLog('  70 eV electron beam will fragment molecules into characteristic ions', 'info');
        addLog('  Higher source temp → cleaner spectra (reduces memory effects)', 'info');

        let temp = 25;
        let filamentCurrent = 0;
        const circle = $('#eq-progress-circle');
        const circumference = 2 * Math.PI * 45;
        if (circle) { circle.style.strokeDasharray = circumference; circle.style.strokeDashoffset = circumference; }

        const interval = setInterval(() => {
            // Realistic Newton-style heating curve (fast at first, slowing near target)
            const delta = (target - temp) * 0.04;
            temp += Math.max(delta, 0.5);
            if (temp > target) temp = target;

            // Filament current ramps with temperature
            filamentCurrent = Math.min(3.5, (temp / target) * 3.5);

            const pct = (temp - 25) / (target - 25);
            $('#eq-temp-display').textContent = Math.round(temp);
            if (circle) circle.style.strokeDashoffset = circumference * (1 - pct);
            $('#qs-source-temp').textContent = Math.round(temp) + '°C';

            // Educational milestones
            if (Math.round(temp) === 100 && pct < 0.5) {
                addLog('  100°C — residual water/solvent evaporating from source', 'info');
            }
            if (Math.round(temp) === 150 && pct < 0.8) {
                addLog('  150°C — filament current: ' + filamentCurrent.toFixed(1) + ' A (emission stabilizing)', 'info');
            }

            if (temp >= target) {
                clearInterval(interval);
                $('#eq-filament-status').textContent = '✓ ' + filamentCurrent.toFixed(1) + ' A';
                addLog('✓ Ion source at ' + target + '°C — thermal equilibrium reached', 'success');
                addLog('  Filament emission current: ' + filamentCurrent.toFixed(1) + ' A (stable)', 'success');
                addLog('  Repeller voltage: +10 V, Focus lens: -50 V', 'success');
                toast('Ion source ready — filament stable', 'success');
                $('#wizard-next-btn').disabled = false;
                $('#btn-autotune').disabled = false;
            }
        }, 60);
    }

    function runAutoTune() {
        $('#btn-autotune').disabled = true;
        addLog('▶ Auto-tune initiated with PFTBA (perfluorotributylamine) standard', 'info');
        addLog('  PFTBA produces known fragment ions at m/z 69, 219, 502', 'info');
        addLog('  These masses span the full scan range for optimal calibration', 'info');
        toast('Auto-tuning mass calibration...', 'info');

        let progress = 0;
        const fill = $('#tune-progress-fill');
        const text = $('#tune-progress-text');
        let phase = 0; // 0=mass cal, 1=resolution, 2=sensitivity, 3=done

        const interval = setInterval(() => {
            progress += 1.2;
            fill.style.width = Math.min(progress, 100) + '%';
            text.textContent = Math.round(Math.min(progress, 100)) + '%';

            // Phase 1: Mass calibration (0-35%)
            if (progress >= 10 && phase === 0) {
                phase = 0.5;
                $('#status-mass-cal').textContent = 'Scanning PFTBA...';
                $('#status-mass-cal').className = 'status-value';
                addLog('  Scanning PFTBA reference peaks...', 'info');
            }
            if (progress >= 20 && phase === 0.5) {
                phase = 0.6;
                addLog('  m/z 69 (CF₃⁺): measured 68.99 → Δ = -0.01 Da ✓', 'info');
            }
            if (progress >= 28 && phase === 0.6) {
                phase = 0.7;
                addLog('  m/z 219 (C₄F₉⁺): measured 218.98 → Δ = -0.02 Da ✓', 'info');
            }
            if (progress >= 35 && phase < 1) {
                phase = 1;
                addLog('  m/z 502 (C₁₂F₂₇N⁺): measured 502.01 → Δ = +0.01 Da ✓', 'info');
                $('#status-mass-cal').textContent = '✓ ±0.02 Da';
                $('#status-mass-cal').className = 'status-value complete';
                addLog('✓ Mass calibration PASSED — accuracy ±0.02 Da across range', 'success');
            }

            // Phase 2: Resolution test (35-65%)
            if (progress >= 45 && phase === 1) {
                phase = 1.5;
                $('#status-resolution').textContent = 'Testing FWHM...';
                $('#status-resolution').className = 'status-value';
                addLog('  Measuring peak width at half-height (FWHM)...', 'info');
            }
            if (progress >= 55 && phase === 1.5) {
                phase = 1.6;
                addLog('  m/z 219: FWHM = 0.65 Da → Unit resolution achieved', 'info');
                addLog('  Peak shape: Gaussian (symmetry factor 1.02)', 'info');
            }
            if (progress >= 65 && phase < 2) {
                phase = 2;
                $('#status-resolution').textContent = '✓ 0.65 Da FWHM';
                $('#status-resolution').className = 'status-value complete';
                addLog('✓ Resolution PASSED — unit mass resolution confirmed', 'success');
            }

            // Phase 3: Sensitivity test (65-95%)
            if (progress >= 75 && phase === 2) {
                phase = 2.5;
                $('#status-sensitivity').textContent = 'Testing S/N...';
                $('#status-sensitivity').className = 'status-value';
                addLog('  Injecting 25 pg octafluoronaphthalene (OFN)...', 'info');
                addLog('  Monitoring m/z 272 signal-to-noise ratio...', 'info');
            }
            if (progress >= 90 && phase === 2.5) {
                phase = 2.6;
                addLog('  OFN m/z 272: S/N = 842:1 (spec: > 100:1)', 'info');
            }

            if (progress >= 100) {
                clearInterval(interval);
                fill.style.width = '100%';
                text.textContent = '100%';
                $('#status-sensitivity').textContent = '✓ S/N 842:1';
                $('#status-sensitivity').className = 'status-value complete';
                addLog('✓ Sensitivity PASSED — 25 pg OFN, S/N = 842:1', 'success');
                addLog('═══════════════════════════════════════════', 'success');
                addLog('  AUTO-TUNE COMPLETE — All tests passed', 'success');
                addLog('  Mass accuracy: ±0.02 Da | Resolution: 0.65 Da FWHM', 'success');
                addLog('  Sensitivity: 25 pg OFN S/N 842:1', 'success');
                addLog('═══════════════════════════════════════════', 'success');
                toast('Auto-tune complete — all tests passed', 'success');
                $('#wizard-next-btn').disabled = false;
                goToWizardStep(4);
            }
        }, 50);
    }

    function finishWizard() {
        STATE.systemReady = true;
        const chip = $('#system-status-chip');
        chip.innerHTML = '<span class="status-dot online"></span><span>System Ready</span>';

        // Switch to screen view
        $$('.view').forEach(v => v.classList.remove('active'));
        $('#main-screen-view').classList.add('active');
        closeModal('setup-modal');
        $('#run-button').disabled = false;
        addLog('System startup complete — ready for acquisition', 'success');
        toast('Mass Spectrometer ready for acquisition!', 'success');

        // Update sample name
        const compound = COMPOUND_LIBRARY[STATE.selectedCompound];
        if (compound) $('#sample-name').textContent = compound.name;

        // Resize chart after view becomes visible (fixes 0×0 init bug)
        setTimeout(() => { if (msChart) msChart.resize(); }, 100);
    }

    // ========================================================================
    // SCAN SIMULATION — Real-Time Progressive m/z Sweep
    // ========================================================================
    function startScan() {
        if (STATE.isScanning) return;
        STATE.isScanning = true;
        STATE.isPaused = false;
        STATE.elapsedMs = 0;
        STATE._scanAnim = null;

        $('#run-button').disabled = true;
        $('#stop-button').disabled = false;
        $('#pause-button').disabled = false;
        $('#sst-report-button').disabled = true;
        $('#run-status-indicator').classList.add('running');
        $('#screen-title').textContent = 'Acquiring...';

        addLog(`Scan started: ${STATE.ionMode} mode, m/z ${STATE.mzStart}–${STATE.mzEnd}`, 'info');
        toast('Acquisition started', 'info');

        const compound = COMPOUND_LIBRARY[STATE.selectedCompound];
        if (compound) {
            addLog(`Sample: ${compound.name} (MW ${compound.mw})`, 'info');
            $('#sample-name').textContent = compound.name;
        }

        // Pre-generate the full spectrum data
        const fullData = generateSpectrum();
        if (!fullData) { stopScan(); return; }

        // Sort all peaks by m/z for progressive reveal
        const sortedPeaks = [...fullData.allPeaks].sort((a, b) => a.mz - b.mz);
        const sortedFragments = [...fullData.fragments].sort((a, b) => a.mz - b.mz);

        const scanDuration = STATE.instantMode ? 500 : 8000;
        const startTime = Date.now();
        const fill = $('#timer-progress-fill');
        const mzRange = STATE.mzEnd - STATE.mzStart;

        // Disable chart animation for smooth updates
        if (msChart) msChart.options.animation = false;

        // Clear fragment table
        const tbody = $('#fragment-tbody');
        if (tbody) tbody.innerHTML = '';

        let lastMzRevealed = STATE.mzStart;
        let revealedFragCount = 0;
        let logPhase = 0;
        let pauseOffset = 0;
        let pauseStart = 0;

        const animate = () => {
            if (!STATE.isScanning) return;

            if (STATE.isPaused) {
                if (!pauseStart) pauseStart = Date.now();
                STATE._scanAnim = requestAnimationFrame(animate);
                return;
            }
            if (pauseStart) {
                pauseOffset += Date.now() - pauseStart;
                pauseStart = 0;
            }

            const elapsed = Date.now() - startTime - pauseOffset;
            const progress = Math.min(1, elapsed / scanDuration);
            STATE.elapsedMs = elapsed;

            // Update timer
            const sec = (elapsed / 1000).toFixed(1);
            $('#elapsed-time').textContent = sec < 10 ? `00:0${sec}` : `00:${sec}`;
            fill.style.width = (progress * 100) + '%';

            // Calculate current m/z position of the sweep
            const currentMz = STATE.mzStart + progress * mzRange;

            if (currentMz > lastMzRevealed) {
                lastMzRevealed = currentMz;

                // Reveal peaks up to current m/z
                const revealedPeaks = sortedPeaks.filter(p => p.mz <= currentMz);

                // Update chart with revealed peaks
                if (msChart && revealedPeaks.length > 0) {
                    msChart.data.labels = revealedPeaks.map(p => p.mz);
                    msChart.data.datasets[0].data = revealedPeaks.map(p => p.intensity);
                    msChart.data.datasets[0].backgroundColor = revealedPeaks.map(p =>
                        p.assignment ? 'rgba(59,130,246,0.9)' : 'rgba(100,116,139,0.3)'
                    );
                    msChart.update('none');
                }

                // Progressive fragment table population
                const newFrags = sortedFragments.filter(f => f.mz <= currentMz);
                if (newFrags.length > revealedFragCount && tbody) {
                    for (let i = revealedFragCount; i < newFrags.length; i++) {
                        const f = newFrags[i];
                        const row = document.createElement('tr');
                        row.style.animation = 'slideIn 0.3s ease';
                        row.innerHTML = `
                            <td style="font-weight:600;color:#3b82f6">${f.mz}</td>
                            <td>${f.intensity}%</td>
                            <td style="font-family:Inter;font-size:11px;color:#94a3b8">${f.assignment}</td>
                            <td class="bar-cell"><div class="frag-bar" style="width:${f.intensity}%"></div></td>
                        `;
                        tbody.appendChild(row);
                    }
                    revealedFragCount = newFrags.length;
                }

                // Update molecular ion info when we reach that m/z
                if (currentMz >= fullData.molecularIon) {
                    $('#molecular-ion-mz').textContent = fullData.molecularIon;
                    $('#mol-formula').textContent = fullData.compound.formula;
                    $('#mol-weight').textContent = fullData.compound.mw.toFixed(2);
                }

                // Update isotope pattern when we cross molecular ion region
                if (currentMz >= fullData.molecularIon && logPhase < 5) {
                    updateIsotopeDisplay(fullData);
                    logPhase = 5;
                }

                // Phase-based log messages
                if (progress > 0.05 && logPhase === 0) {
                    logPhase = 1;
                    addLog(`  Scanning m/z ${STATE.mzStart}–${Math.round(currentMz)}...`, 'info');
                }
                if (progress > 0.25 && logPhase === 1) {
                    logPhase = 2;
                    addLog(`  Sweep at m/z ${Math.round(currentMz)} — ${revealedFragCount} peaks detected`, 'info');
                }
                if (progress > 0.5 && logPhase === 2) {
                    logPhase = 3;
                    addLog(`  Mid-range scan m/z ${Math.round(currentMz)} — acquiring...`, 'info');
                }
                if (progress > 0.8 && logPhase === 3) {
                    logPhase = 4;
                    addLog(`  High-mass region m/z ${Math.round(currentMz)} — finalizing...`, 'info');
                }
            }

            // Update scan status
            const scanPct = Math.round(progress * 100);
            $('#screen-title').textContent = `Scanning m/z ${Math.round(currentMz)} (${scanPct}%)`;

            if (elapsed >= scanDuration) {
                completeScan(fullData);
                return;
            }

            STATE._scanAnim = requestAnimationFrame(animate);
        };

        STATE._scanAnim = requestAnimationFrame(animate);
    }

    function completeScan(fullData) {
        STATE.isScanning = false;
        if (STATE._scanAnim) { cancelAnimationFrame(STATE._scanAnim); STATE._scanAnim = null; }

        // Use pre-generated data or generate fresh
        const data = fullData || generateSpectrum();
        STATE.lastScanData = data;

        // Re-enable chart animation and do final update
        if (msChart) msChart.options.animation = { duration: 400 };
        updateChart(data);
        updateFragmentTable(data);
        updateIsotopeDisplay(data);
        updateMolIonInfo(data);

        // UI updates
        $('#run-button').disabled = false;
        $('#stop-button').disabled = true;
        $('#pause-button').disabled = true;
        $('#sst-report-button').disabled = false;
        $('#run-status-indicator').classList.remove('running');
        $('#screen-title').textContent = 'Scan Complete';

        addLog(`✓ Scan complete — ${data.fragments.length} peaks identified`, 'success');
        addLog(`Base peak: m/z ${data.basePeak.mz} (${data.basePeak.assignment})`, 'info');
        addLog(`Molecular ion: m/z ${data.molecularIon}`, 'info');
        toast(`Scan complete — base peak m/z ${data.basePeak.mz}`, 'success');
    }

    function stopScan() {
        STATE.isScanning = false;
        STATE.isPaused = false;
        if (STATE._scanAnim) { cancelAnimationFrame(STATE._scanAnim); STATE._scanAnim = null; }
        if (msChart) msChart.options.animation = { duration: 400 };
        $('#run-button').disabled = false;
        $('#stop-button').disabled = true;
        $('#pause-button').disabled = true;
        $('#run-status-indicator').classList.remove('running');
        $('#screen-title').textContent = 'Stopped';
        addLog('Scan stopped by operator', 'warning');
    }

    function pauseScan() {
        STATE.isPaused = !STATE.isPaused;
        $('#pause-button').innerHTML = STATE.isPaused ?
            '<i class="fas fa-play"></i> Resume' : '<i class="fas fa-pause"></i> Pause';
        $('#screen-title').textContent = STATE.isPaused ? 'Paused' : 'Acquiring...';
        addLog(STATE.isPaused ? 'Scan paused' : 'Scan resumed', 'info');
    }

    function resetScan() {
        stopScan();
        STATE.lastScanData = null;
        if (msChart) {
            msChart.data.labels = [];
            msChart.data.datasets[0].data = [];
            msChart.update();
        }
        $('#fragment-tbody').innerHTML = '<tr><td colspan="4" style="color:#64748b;text-align:center;padding:20px">Run scan to see fragments</td></tr>';
        $('#molecular-ion-mz').textContent = '--';
        $('#mol-formula').textContent = '--';
        $('#mol-weight').textContent = '--';
        $('#elapsed-time').textContent = '00:00.0';
        $('#timer-progress-fill').style.width = '0%';
        $('#screen-title').textContent = 'Ready';
        addLog('System reset', 'info');
    }

    // ========================================================================
    // MODAL MANAGEMENT
    // ========================================================================
    function openModal(id) {
        const modal = document.getElementById(id);
        const backdrop = $('#modal-backdrop');
        if (modal) {
            modal.classList.remove('hidden');
            backdrop.classList.remove('hidden');
            // Trigger reflow then add visible for CSS transition (opacity 0→1, scale animation)
            requestAnimationFrame(() => modal.classList.add('visible'));
        }
    }

    function closeModal(id) {
        const modal = document.getElementById(id);
        const backdrop = $('#modal-backdrop');
        if (modal) {
            modal.classList.remove('visible');
            setTimeout(() => modal.classList.add('hidden'), 300);
        }
        // Close backdrop if no other modals are visible
        setTimeout(() => {
            const anyOpen = document.querySelector('.modal.visible');
            if (!anyOpen && backdrop) backdrop.classList.add('hidden');
        }, 300);
    }

    function closeAllModals() {
        $$('.modal').forEach(m => {
            m.classList.remove('visible');
            m.classList.add('hidden');
        });
        $('#modal-backdrop')?.classList.add('hidden');
    }

    // ========================================================================
    // REPORT GENERATION
    // ========================================================================
    function generateReport() {
        const data = STATE.lastScanData;
        if (!data) { toast('Run a scan first', 'warning'); return; }

        const reportBody = $('#report-body');
        reportBody.innerHTML = `
            <div style="border-bottom:1px solid #334155;padding-bottom:12px;margin-bottom:12px">
                <h4 style="color:#fff;margin:0">${data.compound.name}</h4>
                <div style="display:flex;gap:20px;font-size:12px;color:#94a3b8;margin-top:6px">
                    <span>Formula: <b style="color:#cbd5e1">${data.compound.formula}</b></span>
                    <span>MW: <b style="color:#cbd5e1">${data.compound.mw}</b></span>
                    <span>CAS: <b style="color:#cbd5e1">${data.compound.cas}</b></span>
                    <span>Mode: <b style="color:#cbd5e1">${STATE.ionMode}</b></span>
                </div>
            </div>
            <h5 style="color:#94a3b8;margin:8px 0;font-size:12px;text-transform:uppercase;letter-spacing:1px">Fragment Ions</h5>
            <table class="fragment-table">
                <thead><tr><th>m/z</th><th>Rel. %</th><th>Assignment</th></tr></thead>
                <tbody>
                    ${data.fragments.sort((a, b) => b.intensity - a.intensity).map(f => `
                        <tr><td style="color:#3b82f6;font-weight:600">${f.mz}</td><td>${f.intensity}%</td><td style="font-family:Inter">${f.assignment}</td></tr>
                    `).join('')}
                </tbody>
            </table>
            <h5 style="color:#94a3b8;margin:12px 0 8px;font-size:12px;text-transform:uppercase;letter-spacing:1px">Isotope Pattern</h5>
            <div style="display:flex;gap:12px;font-size:13px;color:#cbd5e1;font-family:'JetBrains Mono'">
                ${data.isotopes.map(i => `<span>${i.label}: ${i.intensity.toFixed(1)}%</span>`).join('')}
            </div>
        `;
        openModal('sst-modal');
    }

    // ========================================================================
    // DATA EXPORT
    // ========================================================================
    function exportData() {
        const data = STATE.lastScanData;
        if (!data) { toast('No data to export', 'warning'); return; }

        let csv = 'm/z,Relative Intensity (%),Assignment\n';
        data.allPeaks.forEach(p => {
            csv += `${p.mz},${p.intensity},"${p.assignment || ''}"\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `MS_${STATE.selectedCompound}_${STATE.ionMode}_${Date.now()}.csv`;
        a.click();
        URL.revokeObjectURL(a.href);
        toast('Data exported as CSV', 'success');
        addLog('Data exported', 'info');
    }

    // ========================================================================
    // CLOCK
    // ========================================================================
    function updateClock() {
        const now = new Date();
        const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const el = $('#system-time');
        if (el) el.textContent = time;
    }

    // ========================================================================
    // EVENT BINDING
    // ========================================================================
    function bindEvents() {
        // Hotspots — instrument view
        $$('.hotspot').forEach(hs => {
            hs.addEventListener('click', () => {
                const target = hs.dataset.controls;
                if (target === 'screen-view') {
                    if (!STATE.systemReady) {
                        toast('Start the system first', 'warning');
                        return;
                    }
                    $$('.view').forEach(v => v.classList.remove('active'));
                    $('#main-screen-view').classList.add('active');
                    // Resize chart after view switch
                    setTimeout(() => { if (msChart) msChart.resize(); }, 100);
                } else if (target) {
                    openModal(target);
                }
            });
        });

        // Startup button
        $('#hotspot-setup')?.addEventListener('click', () => openModal('setup-modal'));

        // Wizard buttons
        $('#btn-pumpdown')?.addEventListener('click', runPumpDown);
        $('#btn-heat-source')?.addEventListener('click', runSourceHeat);
        $('#btn-autotune')?.addEventListener('click', runAutoTune);
        $('#wizard-prev-btn')?.addEventListener('click', () => {
            if (STATE.wizardStep > 1) goToWizardStep(STATE.wizardStep - 1);
        });
        $('#wizard-next-btn')?.addEventListener('click', () => {
            if (STATE.wizardStep < 4) goToWizardStep(STATE.wizardStep + 1);
        });
        $('#wizard-finish-btn')?.addEventListener('click', finishWizard);

        // Back button
        $('#back-to-main-view-button')?.addEventListener('click', () => {
            $$('.view').forEach(v => v.classList.remove('active'));
            $('#hplc-main-view').classList.add('active');
        });

        // Scan controls
        $('#run-button')?.addEventListener('click', startScan);
        $('#stop-button')?.addEventListener('click', stopScan);
        $('#pause-button')?.addEventListener('click', pauseScan);
        $('#reset-button')?.addEventListener('click', resetScan);

        // Instant mode toggle
        $('#instant-mode-toggle')?.addEventListener('change', (e) => {
            STATE.instantMode = e.target.checked;
            addLog('Instant mode ' + (STATE.instantMode ? 'enabled' : 'disabled'), 'info');
        });

        // Fault mode toggle
        $('#fault-mode-toggle')?.addEventListener('change', (e) => {
            if (e.target.checked) openModal('fault-selector-modal');
            else { STATE.currentFault = 'none'; addLog('Fault simulation disabled', 'info'); }
        });

        // Modal close buttons
        $$('.modal-close-btn').forEach(btn => {
            btn.addEventListener('click', () => closeAllModals());
        });
        $('#modal-backdrop')?.addEventListener('click', closeAllModals);

        // Modal confirm buttons
        $$('.modal-confirm-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                applyModalSettings();
                closeAllModals();
            });
        });

        // Chart tools
        $('#zoom-in-btn')?.addEventListener('click', () => msChart?.zoom(1.2));
        $('#zoom-out-btn')?.addEventListener('click', () => msChart?.zoom(0.8));
        $('#reset-zoom-btn')?.addEventListener('click', () => msChart?.resetZoom());
        $('#export-data-btn')?.addEventListener('click', exportData);
        $('#screenshot-btn')?.addEventListener('click', () => {
            const url = msChart?.toBase64Image();
            if (url) { const a = document.createElement('a'); a.href = url; a.download = 'mass_spectrum.png'; a.click(); }
        });

        // Report / Library search
        $('#sst-report-button')?.addEventListener('click', generateReport);
        $('#overlay-std-button')?.addEventListener('click', librarySearch);

        // Clear log
        $('#clear-log-btn')?.addEventListener('click', () => { $('#log-content').innerHTML = ''; });

        // Fullscreen
        $('#fullscreen-button')?.addEventListener('click', () => {
            if (!document.fullscreenElement) document.documentElement.requestFullscreen();
            else document.exitFullscreen();
        });

        // Difficulty selector
        $$('.difficulty-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                $$('.difficulty-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                STATE.difficulty = btn.dataset.level;
                addLog(`Difficulty set to ${STATE.difficulty}`, 'info');
            });
        });

        // Column card selection (ion mode, analyzer, inlet, fault)
        $$('.column-card').forEach(card => {
            card.addEventListener('click', () => {
                const parent = card.closest('.column-cards');
                parent.querySelectorAll('.column-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
            });
        });

        // Sync range+number inputs
        $$('.range-with-input').forEach(group => {
            const range = group.querySelector('input[type=range]');
            const num = group.querySelector('input[type=number]');
            if (range && num) {
                range.addEventListener('input', () => { num.value = range.value; });
                num.addEventListener('input', () => { range.value = num.value; });
            }
        });

        // Gain mode buttons
        $$('[data-gain]').forEach(btn => {
            btn.addEventListener('click', () => {
                $$('[data-gain]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
    }

    function applyModalSettings() {
        // Ion mode
        const ionMode = document.querySelector('input[name=ion-mode]:checked');
        if (ionMode) {
            STATE.ionMode = ionMode.value;
            $('#live-ion-mode').textContent = STATE.ionMode;
            $('#qs-scan-mode').textContent = STATE.ionMode;
            addLog(`Ionization mode: ${STATE.ionMode}`, 'info');
        }

        // Analyzer
        const analyzer = document.querySelector('input[name=analyzer-type]:checked');
        if (analyzer) STATE.analyzerType = analyzer.value;

        // Inlet
        const inlet = document.querySelector('input[name=inlet-type]:checked');
        if (inlet) STATE.inletType = inlet.value;

        // Sample
        const sample = $('#sample-select');
        if (sample && sample.value) {
            STATE.selectedCompound = sample.value;
            const c = COMPOUND_LIBRARY[STATE.selectedCompound];
            if (c) {
                $('#sample-name').textContent = c.name;
                addLog(`Sample loaded: ${c.name}`, 'info');
                toast(`Sample: ${c.name}`, 'success');
            }
        }

        // Source temp
        const st = $('#source-temp-number');
        if (st) { STATE.sourceTemp = parseInt(st.value); $('#live-source-temp').textContent = STATE.sourceTemp; }

        // Electron energy
        const ee = $('#electron-energy-number');
        if (ee) { STATE.electronEnergy = parseInt(ee.value); $('#live-ee').textContent = STATE.electronEnergy; }

        // EM voltage
        const em = $('#em-voltage-number');
        if (em) STATE.emVoltage = parseInt(em.value);

        // m/z range
        const mzS = $('#mz-start-input');
        const mzE = $('#mz-end-input');
        if (mzS && mzE) {
            STATE.mzStart = parseInt(mzS.value);
            STATE.mzEnd = parseInt(mzE.value);
            $('#live-mz-range').textContent = `${STATE.mzStart}–${STATE.mzEnd}`;
        }

        // Scan speed
        const ss = $('#scan-speed-number');
        if (ss) STATE.scanSpeed = parseInt(ss.value);

        // Fault
        const fault = document.querySelector('input[name=fault-type]:checked');
        if (fault) {
            STATE.currentFault = fault.value;
            if (fault.value !== 'none') addLog(`Fault simulation: ${fault.value}`, 'warning');
        }
    }

    // ========================================================================
    // LIBRARY SEARCH
    // ========================================================================
    function librarySearch() {
        if (!STATE.lastScanData) { toast('Run a scan first', 'warning'); return; }
        const data = STATE.lastScanData;
        const results = [];

        for (const [key, lib] of Object.entries(COMPOUND_LIBRARY)) {
            let score = 0;
            let matches = 0;
            for (const libFrag of lib.fragments) {
                const scanMatch = data.allPeaks.find(p => Math.abs(p.mz - libFrag.mz) <= 1 && p.intensity > 3);
                if (scanMatch) { matches++; score += Math.min(scanMatch.intensity, libFrag.intensity); }
            }
            if (matches > 0) {
                results.push({ name: lib.name, formula: lib.formula, mw: lib.mw, score: Math.round(score / lib.fragments.length), matches, total: lib.fragments.length });
            }
        }

        results.sort((a, b) => b.score - a.score);

        const reportBody = $('#report-body');
        reportBody.innerHTML = `
            <h4 style="color:#fff;margin:0 0 12px">Library Search Results</h4>
            <table class="fragment-table">
                <thead><tr><th>Compound</th><th>Formula</th><th>MW</th><th>Match</th><th>Score</th></tr></thead>
                <tbody>
                    ${results.slice(0, 8).map((r, i) => `
                        <tr style="${i === 0 ? 'background:rgba(34,197,94,0.08)' : ''}">
                            <td style="color:${i === 0 ? '#22c55e' : '#cbd5e1'};font-weight:${i === 0 ? '700' : '400'}">${r.name}</td>
                            <td>${r.formula}</td>
                            <td>${r.mw}</td>
                            <td>${r.matches}/${r.total}</td>
                            <td style="font-weight:700;color:${r.score > 60 ? '#22c55e' : r.score > 30 ? '#f59e0b' : '#ef4444'}">${r.score}%</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        openModal('sst-modal');
        addLog('Library search completed — best match: ' + results[0]?.name, 'success');
    }

    // ========================================================================
    // INITIALIZATION
    // ========================================================================
    function init() {
        initChart();
        bindEvents();
        updateClock();
        setInterval(updateClock, 30000);
        addLog('Mass Spectrometer Digital Twin v2.0 initialized', 'success');
        addLog('Click "System Startup" to begin', 'info');

        // Quick CSS animation for toasts
        const style = document.createElement('style');
        style.textContent = '@keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}';
        document.head.appendChild(style);
    }

    init();
});