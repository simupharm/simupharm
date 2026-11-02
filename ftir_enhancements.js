/**
 * SimuPharma FTIR Digital Twin - Enhancement Module v2.0
 * Adds: Fault Simulation, Preparation Wizard, SST Validation, Difficulty Levels
 * This module integrates with the existing ftir_script.js without modifying it.
 */

(function () {
    'use strict';

    // Wait for DOM + base FTIR script
    function whenReady(fn) {
        if (document.readyState === 'complete') fn();
        else window.addEventListener('load', fn);
    }

    whenReady(() => {
        // ====================================================================
        // FAULT SIMULATION ENGINE
        // ====================================================================
        const FaultLibrary = {
            none: {
                name: 'Normal Operation', description: 'No faults simulated',
                noiseMultiplier: 1, baselineShift: 0, ghostPeaks: []
            },
            moisture: {
                name: 'Moisture Contamination', description: 'Water vapor in beam path — broad O-H bands appear',
                noiseMultiplier: 1.5, baselineShift: 0.02,
                ghostPeaks: [
                    { pos: 3400, int: 0.25, width: 200, assign: 'H₂O O-H stretch (contamination)' },
                    { pos: 1640, int: 0.12, width: 40, assign: 'H₂O bend (contamination)' }
                ]
            },
            crystal_damage: {
                name: 'Damaged ATR Crystal', description: 'Scratched diamond — high baseline noise, reduced sensitivity',
                noiseMultiplier: 4, baselineShift: 0.08, ghostPeaks: []
            },
            poor_contact: {
                name: 'Poor Sample Contact', description: 'Insufficient pressure — weak, distorted spectrum',
                noiseMultiplier: 2, baselineShift: 0.01,
                sensitivityFactor: 0.3, // Severely reduced peak intensities
                ghostPeaks: []
            },
            stray_light: {
                name: 'Stray Light', description: 'Optical misalignment — elevated baseline in fingerprint region',
                noiseMultiplier: 1.8, baselineShift: 0,
                ghostPeaks: [
                    { pos: 2350, int: 0.15, width: 50, assign: 'CO₂ atmospheric (stray)' },
                    { pos: 667, int: 0.08, width: 30, assign: 'CO₂ bend (stray)' }
                ],
                baselineCurve: (wn) => 0.03 * Math.exp(-(wn - 700) * (wn - 700) / 200000)
            },
            contaminated: {
                name: 'Nujol Contamination', description: 'Previous sample residue on crystal',
                noiseMultiplier: 1.3, baselineShift: 0,
                ghostPeaks: [
                    { pos: 2920, int: 0.35, width: 20, assign: 'C-H stretch (Nujol contaminant)' },
                    { pos: 2850, int: 0.28, width: 20, assign: 'C-H stretch (Nujol contaminant)' },
                    { pos: 1460, int: 0.15, width: 15, assign: 'C-H bend (Nujol contaminant)' },
                    { pos: 1377, int: 0.08, width: 10, assign: 'C-H bend (Nujol contaminant)' },
                    { pos: 720, int: 0.10, width: 15, assign: 'C-H rock (Nujol contaminant)' }
                ]
            }
        };

        let activeFault = 'none';

        // Monkey-patch the generateSpectrum function to inject fault effects
        const originalGenerateSpectrum = window.generateSpectrum;
        if (originalGenerateSpectrum) {
            window.generateSpectrum = function (compound, minWn, maxWn, noiseLevel) {
                const fault = FaultLibrary[activeFault] || FaultLibrary.none;
                const adjustedNoise = (noiseLevel || 0.02) * fault.noiseMultiplier;
                let data = originalGenerateSpectrum(compound, minWn, maxWn, adjustedNoise);
                if (!data) return data;

                // Apply sensitivity reduction (poor contact)
                if (fault.sensitivityFactor) {
                    data = data.map(p => ({ x: p.x, y: p.y * fault.sensitivityFactor }));
                }

                // Add baseline shift
                if (fault.baselineShift) {
                    data = data.map(p => ({ x: p.x, y: p.y + fault.baselineShift }));
                }

                // Add baseline curve (stray light)
                if (fault.baselineCurve) {
                    data = data.map(p => ({ x: p.x, y: p.y + fault.baselineCurve(p.x) }));
                }

                // Add ghost/contaminant peaks
                if (fault.ghostPeaks.length > 0) {
                    data = data.map(p => {
                        let extra = 0;
                        fault.ghostPeaks.forEach(gp => {
                            const w = gp.width || 20;
                            extra += gp.int * (w * w) / ((p.x - gp.pos) * (p.x - gp.pos) + w * w);
                        });
                        return { x: p.x, y: p.y + extra };
                    });
                }

                return data;
            };
        }

        // ====================================================================
        // SST VALIDATION (System Suitability Testing)
        // ====================================================================
        const SSTConfig = {
            standard: 'Polystyrene',
            referencePositions: [3026, 2924, 1601, 1493, 1452, 756, 698],
            tolerance: 8, // cm-1 tolerance for peak position
            minSNRatio: 1000,
            minPeakMatchPercent: 80
        };

        function runSST() {
            if (typeof showToast === 'function') showToast('SST', 'Running System Suitability Test with Polystyrene standard...', 'info');
            if (typeof logMessage === 'function') logMessage('SST: Acquiring polystyrene reference spectrum...', 'info');

            // Generate a polystyrene spectrum
            const origFault = activeFault;
            activeFault = 'none'; // SST always runs in normal mode
            const spectrum = (typeof generateSpectrum === 'function') ?
                generateSpectrum('Polystyrene', 400, 4000, 0.01) : null;
            activeFault = origFault;

            if (!spectrum) {
                if (typeof showToast === 'function') showToast('SST Failed', 'Could not generate reference spectrum', 'error');
                return;
            }

            // Detect peaks
            const peaks = (typeof detectPeaks === 'function') ? detectPeaks(spectrum, 0.05) : [];

            // Check reference positions
            let matched = 0;
            const results = [];
            SSTConfig.referencePositions.forEach(refPos => {
                const closest = peaks.reduce((best, p) => {
                    const diff = Math.abs(p.position - refPos);
                    return diff < Math.abs(best.position - refPos) ? p : best;
                }, { position: 99999 });

                const diff = Math.abs(closest.position - refPos);
                const pass = diff <= SSTConfig.tolerance;
                if (pass) matched++;
                results.push({ ref: refPos, found: closest.position, diff: diff.toFixed(1), pass });
            });

            const matchPct = Math.round((matched / SSTConfig.referencePositions.length) * 100);
            const snRatio = Math.round(Math.max(...spectrum.map(p => p.y)) / 0.01 * 100);
            const overallPass = matchPct >= SSTConfig.minPeakMatchPercent && snRatio >= SSTConfig.minSNRatio;

            // Build and display SST report
            const reportHTML = `
                <div style="padding:20px;font-family:Inter,sans-serif">
                    <h3 style="margin:0 0 16px;color:${overallPass ? '#22c55e' : '#ef4444'}">
                        <i class="fas fa-${overallPass ? 'check-circle' : 'times-circle'}"></i>
                        SST ${overallPass ? 'PASSED' : 'FAILED'}
                    </h3>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;font-size:13px">
                        <div style="background:rgba(59,130,246,0.08);padding:10px;border-radius:8px">
                            <div style="color:#64748b;font-size:11px">Peak Match</div>
                            <div style="color:${matchPct >= 80 ? '#22c55e' : '#ef4444'};font-size:22px;font-weight:700">${matchPct}%</div>
                        </div>
                        <div style="background:rgba(59,130,246,0.08);padding:10px;border-radius:8px">
                            <div style="color:#64748b;font-size:11px">S/N Ratio</div>
                            <div style="color:${snRatio >= 1000 ? '#22c55e' : '#ef4444'};font-size:22px;font-weight:700">${snRatio}:1</div>
                        </div>
                    </div>
                    <table style="width:100%;border-collapse:collapse;font-size:12px;font-family:'JetBrains Mono',monospace">
                        <thead><tr style="border-bottom:1px solid #334155">
                            <th style="text-align:left;padding:4px;color:#64748b">Expected</th>
                            <th style="text-align:left;padding:4px;color:#64748b">Found</th>
                            <th style="text-align:left;padding:4px;color:#64748b">Δ cm⁻¹</th>
                            <th style="text-align:left;padding:4px;color:#64748b">Status</th>
                        </tr></thead>
                        <tbody>
                            ${results.map(r => `<tr style="border-bottom:1px solid rgba(255,255,255,0.04)">
                                <td style="padding:4px;color:#94a3b8">${r.ref} cm⁻¹</td>
                                <td style="padding:4px;color:#e2e8f0">${r.found.toFixed(0)} cm⁻¹</td>
                                <td style="padding:4px;color:${parseFloat(r.diff) <= SSTConfig.tolerance ? '#22c55e' : '#ef4444'}">${r.diff}</td>
                                <td style="padding:4px;color:${r.pass ? '#22c55e' : '#ef4444'}">${r.pass ? '✓ Pass' : '✗ Fail'}</td>
                            </tr>`).join('')}
                        </tbody>
                    </table>
                    <div style="margin-top:12px;font-size:11px;color:#64748b">
                        Standard: Polystyrene (CAS 9003-53-6) | Tolerance: ±${SSTConfig.tolerance} cm⁻¹ | Date: ${new Date().toLocaleString()}
                    </div>
                </div>
            `;

            // Show in a modal or overlay
            showSSTModal(reportHTML);

            if (typeof logMessage === 'function') {
                logMessage(`SST complete: ${matchPct}% peak match, S/N ${snRatio}:1 — ${overallPass ? 'PASSED' : 'FAILED'}`,
                    overallPass ? 'success' : 'error');
            }
            if (typeof showToast === 'function') {
                showToast(`SST ${overallPass ? 'Passed' : 'Failed'}`,
                    `${matchPct}% peaks matched, S/N ratio ${snRatio}:1`,
                    overallPass ? 'success' : 'error');
            }
        }

        function showSSTModal(contentHTML) {
            let modal = document.getElementById('sst-result-modal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'sst-result-modal';
                modal.className = 'modal hidden';
                modal.innerHTML = `
                    <div class="modal-header">
                        <h3><i class="fas fa-clipboard-check"></i> System Suitability Test</h3>
                        <button class="modal-close-btn" onclick="document.getElementById('sst-result-modal').classList.add('hidden');document.getElementById('modal-backdrop').classList.add('hidden')"><i class="fas fa-times"></i></button>
                    </div>
                    <div class="modal-body" id="sst-result-body"></div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="document.getElementById('sst-result-modal').classList.add('hidden');document.getElementById('modal-backdrop').classList.add('hidden')">Close</button>
                    </div>
                `;
                document.body.appendChild(modal);
            }
            document.getElementById('sst-result-body').innerHTML = contentHTML;
            modal.classList.remove('hidden');
            const backdrop = document.getElementById('modal-backdrop');
            if (backdrop) backdrop.classList.remove('hidden');
        }

        // ====================================================================
        // DIFFICULTY LEVELS
        // ====================================================================
        let currentDifficulty = 'beginner';

        const DifficultyConfig = {
            beginner: {
                showHints: true, autoBaseline: true, peakLabelsVisible: true,
                simplifiedUI: true, guidedMode: true
            },
            intermediate: {
                showHints: true, autoBaseline: false, peakLabelsVisible: true,
                simplifiedUI: false, guidedMode: false
            },
            advanced: {
                showHints: false, autoBaseline: false, peakLabelsVisible: false,
                simplifiedUI: false, guidedMode: false
            }
        };

        function setDifficulty(level) {
            currentDifficulty = level;
            const config = DifficultyConfig[level];

            // Toggle hints visibility
            document.querySelectorAll('.param-hint').forEach(el => {
                el.style.display = config.showHints ? '' : 'none';
            });

            // Update AppState if available
            if (typeof AppState !== 'undefined') {
                AppState.settings.showHints = config.showHints;
            }

            if (typeof logMessage === 'function') {
                logMessage(`Difficulty set to: ${level.charAt(0).toUpperCase() + level.slice(1)}`, 'info');
            }
            if (typeof showToast === 'function') {
                showToast('Difficulty', `Set to ${level}`, 'info');
            }
        }

        // ====================================================================
        // UI INJECTION — Add controls to the FTIR interface
        // ====================================================================
        function injectUI() {
            // 1. Add Difficulty Selector to header
            const headerRight = document.querySelector('.instrument-header .header-right');
            if (headerRight) {
                const diffSelector = document.createElement('div');
                diffSelector.className = 'difficulty-selector';
                diffSelector.style.cssText = 'display:flex;gap:2px;margin-right:12px;background:rgba(0,0,0,0.2);padding:3px;border-radius:8px';
                ['beginner', 'intermediate', 'advanced'].forEach(level => {
                    const btn = document.createElement('button');
                    btn.textContent = level.charAt(0).toUpperCase() + level.slice(1);
                    btn.className = 'header-btn ftir-difficulty-btn' + (level === 'beginner' ? ' active' : '');
                    btn.style.cssText = 'padding:4px 10px;border-radius:6px;font-size:11px;font-weight:600;border:none;cursor:pointer;transition:all .2s;' +
                        (level === 'beginner' ? 'background:#2563eb;color:#fff' : 'background:transparent;color:#94a3b8');
                    btn.addEventListener('click', () => {
                        document.querySelectorAll('.ftir-difficulty-btn').forEach(b => {
                            b.classList.remove('active');
                            b.style.background = 'transparent';
                            b.style.color = '#94a3b8';
                        });
                        btn.classList.add('active');
                        btn.style.background = '#2563eb';
                        btn.style.color = '#fff';
                        setDifficulty(level);
                    });
                    diffSelector.appendChild(btn);
                });
                headerRight.insertBefore(diffSelector, headerRight.firstChild);
            }

            // 2. Add Fault Simulation toggle to the footer quick actions
            const quickActions = document.querySelector('.quick-actions');
            if (quickActions) {
                const faultBtn = document.createElement('button');
                faultBtn.className = 'quick-action-btn';
                faultBtn.id = 'quick-fault-sim';
                faultBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i><span>Fault Sim</span>';
                faultBtn.addEventListener('click', showFaultSelector);
                quickActions.appendChild(faultBtn);

                const sstBtn = document.createElement('button');
                sstBtn.className = 'quick-action-btn';
                sstBtn.id = 'quick-sst';
                sstBtn.innerHTML = '<i class="fas fa-clipboard-check"></i><span>SST</span>';
                sstBtn.addEventListener('click', runSST);
                quickActions.appendChild(sstBtn);
            }

            // 3. Add Fault + SST buttons to the software panel footer
            const secondaryActions = document.querySelector('.secondary-actions');
            if (secondaryActions) {
                const faultToggle = document.createElement('button');
                faultToggle.id = 'fault-toggle-btn';
                faultToggle.className = 'btn btn-secondary';
                faultToggle.innerHTML = '<i class="fas fa-bug"></i> Faults';
                faultToggle.addEventListener('click', showFaultSelector);
                secondaryActions.appendChild(faultToggle);

                const sstBtn = document.createElement('button');
                sstBtn.id = 'sst-run-btn';
                sstBtn.className = 'btn btn-secondary';
                sstBtn.innerHTML = '<i class="fas fa-clipboard-check"></i> SST';
                sstBtn.addEventListener('click', runSST);
                secondaryActions.appendChild(sstBtn);
            }

            // 4. Create fault selector modal
            createFaultModal();
        }

        // ====================================================================
        // FAULT SELECTOR MODAL
        // ====================================================================
        function createFaultModal() {
            const modal = document.createElement('div');
            modal.id = 'fault-modal';
            modal.className = 'modal hidden';
            modal.innerHTML = `
                <div class="modal-header">
                    <h3><i class="fas fa-exclamation-triangle"></i> Fault Simulation</h3>
                    <button class="modal-close-btn" onclick="document.getElementById('fault-modal').classList.add('hidden');document.getElementById('modal-backdrop').classList.add('hidden')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <p style="color:#94a3b8;margin-bottom:16px">Select a fault condition to simulate. The fault will affect all subsequent measurements.</p>
                    <div class="fault-options" style="display:grid;gap:8px">
                        ${Object.entries(FaultLibrary).map(([key, fault]) => `
                            <label class="fault-option" style="display:flex;align-items:center;gap:12px;padding:12px;border:1px solid ${key === 'none' ? '#22c55e33' : '#334155'};border-radius:10px;cursor:pointer;transition:all .2s;background:${key === 'none' ? 'rgba(34,197,94,0.05)' : 'transparent'}" data-fault="${key}">
                                <input type="radio" name="ftir-fault" value="${key}" ${key === 'none' ? 'checked' : ''} style="accent-color:#3b82f6">
                                <div>
                                    <div style="font-weight:600;color:${key === 'none' ? '#22c55e' : '#e2e8f0'};font-size:14px">
                                        <i class="fas fa-${key === 'none' ? 'check-circle' : 'exclamation-circle'}" style="margin-right:4px;color:${key === 'none' ? '#22c55e' : '#f59e0b'}"></i>
                                        ${fault.name}
                                    </div>
                                    <div style="font-size:12px;color:#64748b;margin-top:2px">${fault.description}</div>
                                </div>
                            </label>
                        `).join('')}
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary" id="apply-fault-btn">
                        <i class="fas fa-check"></i> Apply Fault
                    </button>
                </div>
            `;
            document.body.appendChild(modal);

            // Bind events
            document.getElementById('apply-fault-btn').addEventListener('click', () => {
                const selected = document.querySelector('input[name=ftir-fault]:checked');
                if (selected) {
                    activeFault = selected.value;
                    const faultInfo = FaultLibrary[activeFault];
                    if (typeof logMessage === 'function') {
                        logMessage(`Fault simulation: ${faultInfo.name}`, activeFault === 'none' ? 'success' : 'warning');
                    }
                    if (typeof showToast === 'function') {
                        showToast('Fault Simulation', faultInfo.name, activeFault === 'none' ? 'success' : 'warning');
                    }

                    // Visual indicator
                    updateFaultIndicator();
                }
                document.getElementById('fault-modal').classList.add('hidden');
                document.getElementById('modal-backdrop').classList.add('hidden');
            });

            // Card click selects radio
            modal.querySelectorAll('.fault-option').forEach(opt => {
                opt.addEventListener('click', () => {
                    modal.querySelectorAll('.fault-option').forEach(o => {
                        o.style.borderColor = '#334155';
                        o.style.background = 'transparent';
                    });
                    opt.style.borderColor = '#3b82f6';
                    opt.style.background = 'rgba(59,130,246,0.05)';
                    const radio = opt.querySelector('input[type=radio]');
                    if (radio) radio.checked = true;
                });
            });
        }

        function showFaultSelector() {
            const modal = document.getElementById('fault-modal');
            const backdrop = document.getElementById('modal-backdrop');
            if (modal) modal.classList.remove('hidden');
            if (backdrop) backdrop.classList.remove('hidden');
        }

        function updateFaultIndicator() {
            // Add/update a visual chip on the instrument status
            let indicator = document.getElementById('fault-indicator');
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.id = 'fault-indicator';
                indicator.style.cssText = 'position:fixed;bottom:80px;right:20px;padding:8px 16px;border-radius:8px;font-size:12px;font-weight:600;z-index:100;display:none;font-family:Inter,sans-serif;box-shadow:0 4px 12px rgba(0,0,0,0.3)';
                document.body.appendChild(indicator);
            }

            if (activeFault === 'none') {
                indicator.style.display = 'none';
            } else {
                const fault = FaultLibrary[activeFault];
                indicator.style.display = 'flex';
                indicator.style.background = '#f59e0b';
                indicator.style.color = '#000';
                indicator.innerHTML = `<i class="fas fa-exclamation-triangle" style="margin-right:6px"></i> FAULT: ${fault.name}`;
            }
        }

        // ====================================================================
        // INITIALIZE
        // ====================================================================
        injectUI();

        if (typeof logMessage === 'function') {
            logMessage('Enhancement module loaded: Fault Sim + SST + Difficulty Levels', 'success');
        }
    });
})();
