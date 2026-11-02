/**
 * ============================================================================
 * SimuPharma Advanced HPLC Simulator v2.0
 * ============================================================================
 * A professional-grade, physics-based HPLC training simulator
 * 
 * Features:
 * - Van Deemter equation for peak efficiency
 * - Darcy's Law for pressure calculations
 * - Realistic chromatographic behavior
 * - Fault injection for troubleshooting training
 * - System Suitability Testing (SST)
 * - Multi-compound library with pharmacopeial data
 * 
 * Author: SimuPharma Development Team
 * Version: 2.0.0
 * ============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // ========================================================================
    // CONFIGURATION & CONSTANTS
    // ========================================================================

    const CONFIG = {
        // Instrument limits
        maxPressure: 400,           // bar
        minPressure: 0,
        maxFlowRate: 5.0,           // mL/min
        minFlowRate: 0.1,
        maxColumnTemp: 80,          // °C
        minColumnTemp: 20,
        maxWavelength: 800,         // nm
        minWavelength: 190,

        // Standard conditions (for comparison)
        standardFlowRate: 1.0,
        standardTemp: 30,
        standardWavelength: 254,

        // Simulation parameters
        dataPointsPerRun: 1000,
        baselineNoiseLevel: 0.3,
        pressureUpdateInterval: 100,    // ms
        temperatureStabilizationTime: 5000, // ms

        // Animation speeds (multipliers)
        realTimeSpeed: 1,
        fastSpeed: 10,
        instantSpeed: 1000,

        // Van Deemter equation constants (typical for 5µm particles)
        vanDeemter: {
            A: 1.0,      // Eddy diffusion term (µm)
            B: 5.0,      // Longitudinal diffusion term (µm²/s)
            C: 0.05      // Mass transfer term (s)
        },

        // Darcy's Law constants for pressure calculation
        darcy: {
            columnLength: 250,       // mm
            columnInnerDiameter: 4.6, // mm
            particleSize: 5,         // µm
            porosity: 0.4,
            permeability: 1e-13,     // m²
            viscosityWater: 0.89,    // cP at 25°C
            viscosityMethanol: 0.54, // cP at 25°C
            viscosityAcetonitrile: 0.34 // cP at 25°C
        },

        // Column specifications
        columns: {
            C18: {
                name: 'C18 (ODS)',
                length: 250,
                innerDiameter: 4.6,
                particleSize: 5,
                theoreticalPlates: 15000,
                pressureFactor: 1.0,
                retentionFactor: 1.0,
                selectivityFactor: 1.0
            },
            C8: {
                name: 'C8',
                length: 150,
                innerDiameter: 4.6,
                particleSize: 5,
                theoreticalPlates: 10000,
                pressureFactor: 0.8,
                retentionFactor: 0.85,
                selectivityFactor: 0.95
            },
            Phenyl: {
                name: 'Phenyl',
                length: 250,
                innerDiameter: 4.6,
                particleSize: 5,
                theoreticalPlates: 12000,
                pressureFactor: 1.1,
                retentionFactor: 1.1,
                selectivityFactor: 1.15
            },
            HILIC: {
                name: 'HILIC',
                length: 150,
                innerDiameter: 4.6,
                particleSize: 3,
                theoreticalPlates: 18000,
                pressureFactor: 1.5,
                retentionFactor: 0.6,
                selectivityFactor: 0.8
            }
        },

        // Fault simulation parameters
        faults: {
            none: {
                name: 'Normal Operation',
                noiseMultiplier: 1,
                pressureEffect: 0,
                rtShift: 0,
                tailingFactor: 1.0,
                efficiencyLoss: 0
            },
            air_bubble: {
                name: 'Air Bubble in System',
                noiseMultiplier: 5,
                pressureEffect: -20,
                rtShift: 0.1,
                tailingFactor: 1.2,
                efficiencyLoss: 0.3,
                symptoms: ['Irregular baseline', 'Pressure spikes', 'RT variation']
            },
            column_degradation: {
                name: 'Column Degradation',
                noiseMultiplier: 1.5,
                pressureEffect: 30,
                rtShift: -0.2,
                tailingFactor: 2.5,
                efficiencyLoss: 0.5,
                symptoms: ['Peak tailing', 'Reduced resolution', 'Increased pressure']
            },
            leak: {
                name: 'System Leak',
                noiseMultiplier: 2,
                pressureEffect: -50,
                rtShift: 0.3,
                tailingFactor: 1.1,
                efficiencyLoss: 0.2,
                symptoms: ['Pressure drop', 'RT increase', 'Poor reproducibility']
            },
            contamination: {
                name: 'Mobile Phase Contamination',
                noiseMultiplier: 3,
                pressureEffect: 5,
                rtShift: 0,
                tailingFactor: 1.3,
                efficiencyLoss: 0.2,
                ghostPeaks: true,
                symptoms: ['Ghost peaks', 'Elevated baseline', 'New peaks appearing']
            },
            lamp_failure: {
                name: 'Detector Lamp Issue',
                noiseMultiplier: 8,
                pressureEffect: 0,
                rtShift: 0,
                tailingFactor: 1.0,
                efficiencyLoss: 0,
                signalReduction: 0.5,
                symptoms: ['Noisy baseline', 'Reduced sensitivity', 'Signal drift']
            }
        },

        // SST Acceptance criteria (USP guidelines)
        sstCriteria: {
            resolution: { min: 2.0, label: 'Resolution (R)' },
            tailingFactor: { max: 1.5, label: 'Tailing Factor (T)' },
            theoreticalPlates: { min: 2000, label: 'Plate Count (N)' },
            rsd: { max: 2.0, label: '%RSD' },
            capacityFactor: { min: 1.0, label: "Capacity Factor (k')" }
        }
    };

    // ========================================================================
    // SOLVENT & MOBILE PHASE PROPERTIES
    // ========================================================================

    const SOLVENT_PROPERTIES = {
        // Channel B (Organic) solvents
        organic: {
            acetonitrile: {
                name: 'Acetonitrile', abbrev: 'ACN',
                viscosity: 0.34,       // cP at 25°C
                uvCutoff: 190,         // nm
                eluentStrength: 1.0,   // relative
                mixViscosityMax: 0.89, // max viscosity of water-ACN mix (at ~30% ACN)
                boilingPoint: 82,
                miscibility: 'full'
            },
            methanol: {
                name: 'Methanol', abbrev: 'MeOH',
                viscosity: 0.54,
                uvCutoff: 205,
                eluentStrength: 0.73,
                mixViscosityMax: 1.63,  // Water-MeOH mix gets very viscous
                boilingPoint: 65,
                miscibility: 'full'
            },
            thf: {
                name: 'Tetrahydrofuran', abbrev: 'THF',
                viscosity: 0.46,
                uvCutoff: 215,
                eluentStrength: 1.25,
                mixViscosityMax: 1.2,
                boilingPoint: 66,
                miscibility: 'full'
            },
            ipa: {
                name: 'Isopropanol', abbrev: 'IPA',
                viscosity: 2.04,
                uvCutoff: 205,
                eluentStrength: 0.82,
                mixViscosityMax: 3.5,   // Very high mix viscosity
                boilingPoint: 82,
                miscibility: 'full'
            }
        },
        // Channel A (Aqueous) solvents
        aqueous: {
            water: { name: 'Water (HPLC Grade)', isBuffer: false, phRange: [5.5, 8.0] },
            phosphate_buffer: { name: 'Phosphate Buffer', isBuffer: true, phRange: [2.1, 3.1], phRange2: [6.2, 8.2] },
            acetate_buffer: { name: 'Acetate Buffer', isBuffer: true, phRange: [3.8, 5.8] },
            formate_buffer: { name: 'Ammonium Formate Buffer', isBuffer: true, phRange: [2.8, 4.8] },
            citrate_buffer: { name: 'Citrate Buffer', isBuffer: true, phRange: [2.1, 6.4] },
            tris_buffer: { name: 'Tris-HCl Buffer', isBuffer: true, phRange: [7.0, 9.0] }
        }
    };

    const ADDITIVE_INFO = {
        none: { name: 'None', desc: 'No additive selected.', phEffect: 0 },
        tfa: { name: 'TFA', desc: 'Ion-pairing agent for peptide/protein separations. Improves peak shape of basic compounds. pH ~2.0.', phEffect: -5.0, concRange: [0.01, 0.1] },
        formic_acid: { name: 'Formic Acid', desc: 'MS-compatible acid modifier. Good for LC-MS applications. pH ~2.7.', phEffect: -4.3, concRange: [0.05, 0.5] },
        acetic_acid: { name: 'Acetic Acid', desc: 'Mild acid modifier. Commonly used with acetate buffers. pH ~3.5.', phEffect: -3.5, concRange: [0.05, 1.0] },
        tea: { name: 'Triethylamine', desc: 'Basic modifier. Reduces tailing of basic compounds on silica-based columns.', phEffect: 3.0, concRange: [0.05, 0.2] },
        ammonium_formate: { name: 'Ammonium Formate', desc: 'MS-compatible buffer salt. pH 3.0-5.0 range.', phEffect: -1.0, concRange: [1, 50] },
        ammonium_acetate: { name: 'Ammonium Acetate', desc: 'MS-compatible buffer salt. pH 3.5-5.5 range.', phEffect: -0.5, concRange: [1, 50] },
        phosphoric_acid: { name: 'Phosphoric Acid', desc: 'Strong acid modifier for low pH reverse-phase. NOT MS-compatible.', phEffect: -5.0, concRange: [0.01, 0.1] }
    };

    // ========================================================================
    // CHART.JS PEAK ANNOTATION PLUGIN
    // Draws named peak labels, RT annotations, integration shading, and area
    // values directly on the chromatogram canvas after each render.
    // ========================================================================

    const peakAnnotationPlugin = {
        id: 'peakAnnotations',
        afterDraw(chart) {
            const annotations = chart.peakAnnotations;
            if (!annotations || annotations.length === 0) return;

            const ctx = chart.ctx;
            const xScale = chart.scales.x;
            const yScale = chart.scales.y;
            const chartArea = chart.chartArea;

            // Color palette for integration shading
            const colors = [
                { r: 59, g: 130, b: 246 },   // blue
                { r: 34, g: 197, b: 94 },     // green
                { r: 245, g: 158, b: 11 },    // amber
                { r: 239, g: 68, b: 68 },     // red
                { r: 99, g: 102, b: 241 },    // indigo
                { r: 6, g: 182, b: 212 },     // cyan
                { r: 168, g: 85, b: 247 },    // purple
                { r: 236, g: 72, b: 153 }     // pink
            ];

            annotations.forEach((peak, index) => {
                const color = colors[index % colors.length];
                const peakX = xScale.getPixelForValue(peak.rt);
                const peakY = yScale.getPixelForValue(peak.height);
                const baselineY = yScale.getPixelForValue(0);

                // Skip if peak is outside chart area
                if (peakX < chartArea.left || peakX > chartArea.right) return;

                // --- Integration Shading ---
                const sigma = peak.sigma || peak.peakWidth / 2.355;
                const startTime = peak.rt - 3 * sigma;
                const endTime = peak.rt + 3 * sigma;
                const startX = Math.max(xScale.getPixelForValue(startTime), chartArea.left);
                const endX = Math.min(xScale.getPixelForValue(endTime), chartArea.right);

                // Draw filled area under peak
                ctx.save();
                ctx.beginPath();
                const steps = 40;
                for (let s = 0; s <= steps; s++) {
                    const t = startTime + (endTime - startTime) * (s / steps);
                    const px = xScale.getPixelForValue(t);
                    // Gaussian shape
                    const diff = t - peak.rt;
                    const py = yScale.getPixelForValue(
                        peak.height * Math.exp(-(diff * diff) / (2 * sigma * sigma))
                    );
                    if (s === 0) ctx.moveTo(px, baselineY);
                    ctx.lineTo(px, py);
                }
                ctx.lineTo(endX, baselineY);
                ctx.closePath();

                // Gradient fill
                const gradient = ctx.createLinearGradient(0, peakY, 0, baselineY);
                gradient.addColorStop(0, `rgba(${color.r}, ${color.g}, ${color.b}, 0.35)`);
                gradient.addColorStop(1, `rgba(${color.r}, ${color.g}, ${color.b}, 0.05)`);
                ctx.fillStyle = gradient;
                ctx.fill();

                // Integration start/end markers (vertical dashed lines)
                ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, 0.5)`;
                ctx.lineWidth = 1;
                ctx.setLineDash([3, 3]);
                ctx.beginPath();
                ctx.moveTo(startX, baselineY);
                ctx.lineTo(startX, yScale.getPixelForValue(2));
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(endX, baselineY);
                ctx.lineTo(endX, yScale.getPixelForValue(2));
                ctx.stroke();
                ctx.setLineDash([]);
                ctx.restore();

                // --- Peak Apex Drop Line ---
                ctx.save();
                ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, 0.6)`;
                ctx.lineWidth = 1;
                ctx.setLineDash([4, 4]);
                ctx.beginPath();
                ctx.moveTo(peakX, peakY);
                ctx.lineTo(peakX, baselineY);
                ctx.stroke();
                ctx.setLineDash([]);
                ctx.restore();

                // --- Compound Name Label ---
                const labelY = peakY - 22;
                const labelText = peak.name || `Peak ${index + 1}`;

                ctx.save();
                ctx.font = 'bold 10px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'bottom';

                // Background pill for label
                const textWidth = ctx.measureText(labelText).width;
                const pillX = peakX - textWidth / 2 - 6;
                const pillY = labelY - 12;
                const pillW = textWidth + 12;
                const pillH = 16;

                ctx.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, 0.85)`;
                ctx.beginPath();
                ctx.roundRect(pillX, pillY, pillW, pillH, 4);
                ctx.fill();

                // Label text
                ctx.fillStyle = '#ffffff';
                ctx.fillText(labelText, peakX, labelY);

                // Connecting line from label to peak
                ctx.strokeStyle = `rgba(${color.r}, ${color.g}, ${color.b}, 0.6)`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(peakX, pillY + pillH);
                ctx.lineTo(peakX, peakY - 2);
                ctx.stroke();
                ctx.restore();

                // --- RT Label (below name) ---
                ctx.save();
                ctx.font = '9px "JetBrains Mono", monospace';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'top';
                ctx.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, 0.9)`;
                ctx.fillText(`RT ${peak.rt.toFixed(3)}`, peakX, pillY + pillH + 2);
                ctx.restore();

                // --- Area label (at base of peak, small) ---
                ctx.save();
                ctx.font = '8px "JetBrains Mono", monospace';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'bottom';
                ctx.fillStyle = 'rgba(148, 163, 184, 0.7)';
                const areaVal = peak.area || (peak.height * sigma * 2.507);
                ctx.fillText(`A=${areaVal.toFixed(0)}`, peakX, baselineY - 2);
                ctx.restore();
            });
        }
    };

    // ========================================================================
    // COMPOUND LIBRARY - Pharmacopeial Data
    // ========================================================================

    const COMPOUND_LIBRARY = {
        Caffeine: {
            name: 'Caffeine',
            category: 'Alkaloid (Xanthine)',
            molecularWeight: 194.19,
            formula: 'C8H10N4O2',
            casNumber: '58-08-2',
            standardRt: 3.5,           // minutes at standard conditions
            logP: -0.07,               // Partition coefficient
            pKa: 10.4,
            S: 3.5,                    // Solvent strength parameter (LSS model)
            lambdaMax: 273,            // nm
            molarAbsorptivity: 9800,   // L/(mol·cm)
            height: 100,               // relative response
            peakWidth: 0.18,           // minutes (at half height)
            asymmetry: 1.0,            // peak symmetry factor
            solubility: 'Freely soluble in water',
            pharmacopeialRef: 'USP, BP, IP'
        },
        Paracetamol: {
            name: 'Paracetamol (Acetaminophen)',
            category: 'Analgesic/Antipyretic',
            molecularWeight: 151.16,
            formula: 'C8H9NO2',
            casNumber: '103-90-2',
            standardRt: 2.8,
            logP: 0.46,
            pKa: 9.38,
            S: 4.0,                    // Solvent strength parameter
            lambdaMax: 243,
            molarAbsorptivity: 13500,
            height: 85,
            peakWidth: 0.16,
            asymmetry: 1.0,
            solubility: 'Slightly soluble in water',
            pharmacopeialRef: 'USP, BP, IP'
        },
        Aspirin: {
            name: 'Aspirin (Acetylsalicylic Acid)',
            category: 'NSAID',
            molecularWeight: 180.16,
            formula: 'C9H8O4',
            casNumber: '50-78-2',
            standardRt: 6.2,
            logP: 1.19,
            pKa: 3.5,
            S: 5.0,                    // Solvent strength parameter
            lambdaMax: 230,
            molarAbsorptivity: 8400,
            height: 90,
            peakWidth: 0.22,
            asymmetry: 1.05,
            solubility: 'Slightly soluble in water',
            pharmacopeialRef: 'USP, BP, IP',
            degradationProduct: 'Salicylic Acid'
        },
        Ibuprofen: {
            name: 'Ibuprofen',
            category: 'NSAID',
            molecularWeight: 206.28,
            formula: 'C13H18O2',
            casNumber: '15687-27-1',
            standardRt: 9.0,
            logP: 3.97,
            pKa: 4.91,
            S: 6.5,                    // Solvent strength parameter
            lambdaMax: 220,
            molarAbsorptivity: 5600,
            height: 95,
            peakWidth: 0.28,
            asymmetry: 1.1,
            solubility: 'Practically insoluble in water',
            pharmacopeialRef: 'USP, BP, IP'
        },
        Metformin: {
            name: 'Metformin HCl',
            category: 'Antidiabetic (Biguanide)',
            molecularWeight: 165.63,
            formula: 'C4H11N5·HCl',
            casNumber: '1115-70-4',
            standardRt: 1.5,
            logP: -1.43,
            pKa: 12.4,
            S: 2.5,                    // Solvent strength parameter
            lambdaMax: 232,
            molarAbsorptivity: 7200,
            height: 70,
            peakWidth: 0.20,
            asymmetry: 1.2,
            solubility: 'Freely soluble in water',
            pharmacopeialRef: 'USP, BP, IP'
        },
        Atenolol: {
            name: 'Atenolol',
            category: 'Beta-blocker',
            molecularWeight: 266.34,
            formula: 'C14H22N2O3',
            casNumber: '29122-68-7',
            standardRt: 2.2,
            logP: 0.16,
            pKa: 9.6,
            S: 3.8,                    // Solvent strength parameter
            lambdaMax: 225,
            molarAbsorptivity: 8900,
            height: 75,
            peakWidth: 0.17,
            asymmetry: 1.0,
            solubility: 'Sparingly soluble in water',
            pharmacopeialRef: 'USP, BP, IP'
        },
        Amlodipine: {
            name: 'Amlodipine Besylate',
            category: 'Calcium Channel Blocker',
            molecularWeight: 567.05,
            formula: 'C20H25ClN2O5·C6H6O3S',
            casNumber: '111470-99-6',
            standardRt: 7.5,
            logP: 3.0,
            pKa: 8.6,
            S: 5.8,                    // Solvent strength parameter
            lambdaMax: 360,
            molarAbsorptivity: 4200,
            height: 80,
            peakWidth: 0.25,
            asymmetry: 1.15,
            solubility: 'Slightly soluble in water',
            pharmacopeialRef: 'USP, BP'
        },
        Omeprazole: {
            name: 'Omeprazole',
            category: 'Proton Pump Inhibitor',
            molecularWeight: 345.42,
            formula: 'C17H19N3O3S',
            casNumber: '73590-58-6',
            standardRt: 5.8,
            logP: 2.23,
            pKa: 4.0,
            S: 5.2,                    // Solvent strength parameter
            lambdaMax: 302,
            molarAbsorptivity: 12300,
            height: 88,
            peakWidth: 0.24,
            asymmetry: 1.08,
            solubility: 'Very slightly soluble in water',
            pharmacopeialRef: 'USP, BP, IP',
            lightSensitive: true
        },
        Ciprofloxacin: {
            name: 'Ciprofloxacin HCl',
            category: 'Fluoroquinolone Antibiotic',
            molecularWeight: 367.80,
            formula: 'C17H18FN3O3·HCl',
            casNumber: '86393-32-0',
            standardRt: 4.5,
            logP: 0.28,
            pKa: 6.09,
            S: 4.2,                    // Solvent strength parameter
            lambdaMax: 278,
            molarAbsorptivity: 14500,
            height: 92,
            peakWidth: 0.21,
            asymmetry: 1.05,
            solubility: 'Sparingly soluble in water',
            pharmacopeialRef: 'USP, BP, IP'
        },
        Losartan: {
            name: 'Losartan Potassium',
            category: 'ARB (Antihypertensive)',
            molecularWeight: 461.00,
            formula: 'C22H22ClKN6O',
            casNumber: '124750-99-8',
            standardRt: 8.2,
            logP: 4.01,
            pKa: 4.9,
            S: 6.2,                    // Solvent strength parameter
            lambdaMax: 234,
            molarAbsorptivity: 9800,
            height: 85,
            peakWidth: 0.26,
            asymmetry: 1.12,
            solubility: 'Freely soluble in water',
            pharmacopeialRef: 'USP, BP'
        },
        SalicylicAcid: {
            name: 'Salicylic Acid',
            category: 'Degradation Product / Keratolytic',
            molecularWeight: 138.12,
            formula: 'C7H6O3',
            casNumber: '69-72-7',
            standardRt: 4.8,
            logP: 2.26,
            pKa: 2.97,
            S: 4.8,                    // Solvent strength parameter
            lambdaMax: 234,
            molarAbsorptivity: 7600,
            height: 45,
            peakWidth: 0.19,
            asymmetry: 1.02,
            solubility: 'Slightly soluble in water',
            pharmacopeialRef: 'USP, BP',
            isImpurity: true
        }
    };

    // ========================================================================
    // UTILITY FUNCTIONS
    // ========================================================================

    const Utils = {
        /**
         * Generate Gaussian random number (Box-Muller transform)
         */
        gaussianRandom(mean = 0, stdev = 1) {
            const u = 1 - Math.random();
            const v = Math.random();
            const z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
            return z * stdev + mean;
        },

        /**
         * Clamp value between min and max
         */
        clamp(value, min, max) {
            return Math.min(Math.max(value, min), max);
        },

        /**
         * Linear interpolation
         */
        lerp(a, b, t) {
            return a + (b - a) * t;
        },

        /**
         * Format time as MM:SS.s
         */
        formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = (seconds % 60).toFixed(1);
            return `${String(mins).padStart(2, '0')}:${String(secs).padStart(4, '0')}`;
        },

        /**
         * Format number with specified decimals
         */
        formatNumber(value, decimals = 2) {
            return Number(value).toFixed(decimals);
        },

        /**
         * Debounce function
         */
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        /**
         * Generate unique ID
         */
        generateId() {
            return 'id_' + Math.random().toString(36).substr(2, 9);
        },

        /**
         * Deep clone object
         */
        deepClone(obj) {
            return JSON.parse(JSON.stringify(obj));
        },

        /**
         * Calculate area under curve (trapezoidal rule)
         */
        calculateAUC(data) {
            let area = 0;
            for (let i = 1; i < data.length; i++) {
                const dt = data[i].x - data[i - 1].x;
                const avgHeight = (data[i].y + data[i - 1].y) / 2;
                area += dt * avgHeight;
            }
            return area;
        },

        /**
         * Find peaks in data
         */
        findPeaks(data, threshold = 5) {
            const peaks = [];
            for (let i = 1; i < data.length - 1; i++) {
                if (data[i].y > threshold &&
                    data[i].y > data[i - 1].y &&
                    data[i].y > data[i + 1].y) {
                    peaks.push({
                        index: i,
                        x: data[i].x,
                        y: data[i].y
                    });
                }
            }
            return peaks;
        }
    };

    // ========================================================================
    // PHYSICS ENGINE
    // ========================================================================

    const PhysicsEngine = {
        /**
         * Calculate mobile phase viscosity based on composition
         * Uses empirical mixing rule for water-organic mixtures
         */
        calculateViscosity(percentB, organicType = 'acetonitrile') {
            const viscosityA = CONFIG.darcy.viscosityWater;
            // Use SOLVENT_PROPERTIES for dynamic viscosity lookup
            const solventProps = SOLVENT_PROPERTIES.organic[organicType];
            const viscosityB = solventProps ? solventProps.viscosity : CONFIG.darcy.viscosityAcetonitrile;

            // Non-linear mixing - viscosity maximum occurs around 20-40% organic
            const fractionB = percentB / 100;
            const fractionA = 1 - fractionB;

            // Empirical equation for viscosity of water-organic mixtures
            // Uses Grunberg-Nissan style mixing with excess viscosity term
            const lnViscosity = fractionA * Math.log(viscosityA) +
                fractionB * Math.log(viscosityB) +
                fractionA * fractionB * (0.5 - 0.2 * fractionB);

            return Math.exp(lnViscosity);
        },

        /**
         * Calculate system pressure using Darcy's Law
         * ΔP = (η × L × u) / (K × ε²)
         */
        calculatePressure(flowRate, percentB, columnType, temperature, organicSolvent = 'acetonitrile') {
            const column = CONFIG.columns[columnType];
            const viscosity = this.calculateViscosity(percentB, organicSolvent);

            // Temperature correction (viscosity decreases ~2% per °C)
            const tempCorrection = Math.exp(-0.02 * (temperature - 25));
            const correctedViscosity = viscosity * tempCorrection;

            // Convert flow rate from mL/min to m³/s
            const flowRateSI = flowRate / 60000000;

            // Cross-sectional area
            const radius = column.innerDiameter / 2000; // Convert mm to m
            const area = Math.PI * radius * radius;

            // Linear velocity
            const linearVelocity = flowRateSI / (area * CONFIG.darcy.porosity);

            // Kozeny-Carman equation for pressure drop
            const particleSizeM = column.particleSize / 1000000;
            const columnLengthM = column.length / 1000;

            // Simplified pressure calculation (bar)
            const basePressure = 150 * correctedViscosity * flowRate *
                column.pressureFactor *
                (columnLengthM / 0.25) * // Normalize to 250mm
                Math.pow(5 / column.particleSize, 2); // Particle size effect

            return Utils.clamp(basePressure, 0, CONFIG.maxPressure);
        },

        /**
         * Van Deemter equation for plate height calculation
         * H = A + B/u + C×u
         * Where u is linear velocity
         */
        calculatePlateHeight(flowRate, columnType) {
            const column = CONFIG.columns[columnType];
            const { A, B, C } = CONFIG.vanDeemter;

            // Estimate linear velocity (simplified)
            const u = flowRate / 1.0; // Normalize to standard flow

            // Van Deemter equation
            const H = A + B / u + C * u;

            return H;
        },

        /**
         * Calculate theoretical plates from Van Deemter
         * N = L / H
         */
        calculateTheoreticalPlates(flowRate, columnType) {
            const column = CONFIG.columns[columnType];
            const H = this.calculatePlateHeight(flowRate, columnType);
            const N = (column.length * 1000) / H; // L in µm

            return Math.round(N);
        },

        /**
         * Calculate retention time with all factors
         * Uses Linear Solvent Strength (LSS) model for gradient elution:
         *   ln(k) = ln(k_w) - S × φ
         * where k_w is the retention factor in pure water, S is the solvent
         * strength parameter, and φ is the organic fraction (0-1).
         * 
         * For gradient mode, numerically integrates migration through column:
         *   ∫(1/t_R(φ(t))) dt = 1 when compound elutes
         */
        calculateRetentionTime(compound, params) {
            const { flowRate, columnTemp, columnType, gradientProgram, getPercentBAtTime } = params;
            const column = CONFIG.columns[columnType];

            // Base retention time at standard conditions (50% B, isocratic)
            let baseRt = compound.standardRt;

            // Flow rate effect (inverse relationship)
            baseRt *= (CONFIG.standardFlowRate / flowRate);

            // Temperature effect (Van't Hoff equation approximation)
            const tempFactor = Math.exp(0.025 * (CONFIG.standardTemp - columnTemp));
            baseRt *= tempFactor;

            // Column type effect
            baseRt *= column.retentionFactor;

            // Hydrophobicity effect (logP based)
            const logPEffect = 1 + (compound.logP - 1) * 0.05 * (column.selectivityFactor - 1);
            baseRt *= logPEffect;

            // Void time estimate (dead time)
            const t0 = 0.5 * (CONFIG.standardFlowRate / flowRate);

            // Solvent strength parameter (use compound's S or estimate from logP)
            const S = compound.S || (2 + compound.logP * 1.2);

            // Check if we have a real gradient or isocratic conditions
            const isGradient = gradientProgram && gradientProgram.length > 1 &&
                gradientProgram.some(step => step.percentB !== gradientProgram[0].percentB);

            if (!isGradient || !getPercentBAtTime) {
                // Isocratic mode — use the initial %B to adjust retention
                const percentB = (gradientProgram && gradientProgram.length > 0)
                    ? gradientProgram[0].percentB : 50;
                const phi = percentB / 100;
                const phiRef = 0.50; // Reference condition (50% B)

                // LSS isocratic adjustment: k changes exponentially with φ
                const kAdjust = Math.exp(-S * (phi - phiRef));
                const rt = t0 + (baseRt - t0) * kAdjust;
                return Math.max(t0 + 0.1, rt);
            }

            // ================================================================
            // GRADIENT MODE — LSS Numerical Integration
            // ================================================================
            // We integrate the fraction of column length traversed by the
            // compound. The compound elutes when the integral reaches 1.0.
            //
            // At any time t, the instantaneous retention time if conditions
            // were frozen at that %B would be:
            //   tR_inst(φ) = t0 + (tR_ref - t0) × exp(-S × (φ - φ_ref))
            //
            // The fraction of column traversed per unit time = 1 / tR_inst(φ(t))
            // Compound elutes when: ∫₀^tR  dt / tR_inst(φ(t)) = 1

            const phiRef = 0.50;
            const kRef = (baseRt - t0) / t0; // Capacity factor at reference %B

            // Numerical integration with small time steps
            const dt = 0.01; // 0.01 minute steps (0.6 seconds)
            const maxTime = 30; // Maximum search time (minutes)
            let integral = 0;
            let tElute = maxTime;

            for (let t = 0; t < maxTime; t += dt) {
                const phi = getPercentBAtTime(t) / 100;

                // Instantaneous capacity factor at this φ
                const k_inst = kRef * Math.exp(-S * (phi - phiRef));

                // Instantaneous retention time if conditions were frozen
                const tR_inst = t0 * (1 + k_inst);

                // Accumulate fraction of column traversed
                integral += dt / tR_inst;

                // Compound elutes when integral reaches 1.0
                if (integral >= 1.0) {
                    tElute = t;
                    break;
                }
            }

            return Math.max(t0 + 0.1, tElute);
        },

        /**
         * Calculate peak width for gradient elution
         * Gradient peaks are compressed — the focusing effect:
         *   W_gradient ≈ (t0 / S) × (1 + k_e) × (4 / √N)
         * where k_e is the instantaneous k at elution time
         */
        calculateGradientPeakWidth(compound, retentionTime, theoreticalPlates, params) {
            const { gradientProgram, flowRate, getPercentBAtTime } = params;
            const S = compound.S || (2 + compound.logP * 1.2);
            const t0 = 0.5 * (CONFIG.standardFlowRate / flowRate);

            // Check if gradient mode
            const isGradient = gradientProgram && gradientProgram.length > 1 &&
                gradientProgram.some(step => step.percentB !== gradientProgram[0].percentB) &&
                getPercentBAtTime;

            if (!isGradient) {
                // Isocratic — use standard peak width
                return this.calculatePeakWidth(retentionTime, theoreticalPlates, compound.asymmetry);
            }

            // Gradient peak width (LSS model)
            // Get φ at elution time to calculate instantaneous k
            const phiAtElution = getPercentBAtTime(retentionTime) / 100;
            const phiRef = 0.50;
            const kRef = (compound.standardRt * CONFIG.standardFlowRate / flowRate - t0) / t0;
            const k_e = kRef * Math.exp(-S * (phiAtElution - phiRef));

            // Gradient compression factor:
            // In gradient mode, the band is compressed because the tail of the peak
            // experiences stronger solvent than the front.
            // W_grad ≈ 4 × t0 × (1 + k_e) / √N
            // This is typically 2-4× narrower than isocratic
            const sigma = t0 * (1 + Math.min(k_e, 5)) / Math.sqrt(theoreticalPlates);
            const baseWidth = 4 * sigma;

            // Apply asymmetry
            return baseWidth * (1 + (compound.asymmetry - 1) * 0.3);
        },

        /**
         * Calculate peak width using theoretical plates
         * w = 4 × tR / √N
         */
        calculatePeakWidth(retentionTime, theoreticalPlates, asymmetry = 1.0) {
            const sigma = retentionTime / Math.sqrt(theoreticalPlates);
            const baseWidth = 4 * sigma;

            // Asymmetry affects apparent width
            return baseWidth * (1 + (asymmetry - 1) * 0.3);
        },

        /**
         * Calculate resolution between two peaks
         * R = 2(tR2 - tR1) / (w1 + w2)
         */
        calculateResolution(rt1, rt2, w1, w2) {
            return 2 * Math.abs(rt2 - rt1) / (w1 + w2);
        },

        /**
         * Generate Gaussian peak shape
         * With optional asymmetry (EMG - Exponentially Modified Gaussian)
         */
        generatePeakShape(time, rt, sigma, height, asymmetry = 1.0) {
            if (asymmetry === 1.0) {
                // Pure Gaussian
                const exponent = -Math.pow(time - rt, 2) / (2 * sigma * sigma);
                return height * Math.exp(exponent);
            } else {
                // EMG for tailing peaks
                const tau = sigma * (asymmetry - 1) * 0.5;
                const z = (time - rt) / sigma - sigma / tau;

                if (tau > 0 && z > -5) {
                    const emg = (sigma / tau) * Math.sqrt(Math.PI / 2) *
                        Math.exp(0.5 * Math.pow(sigma / tau, 2) - (time - rt) / tau) *
                        (1 + this.erf(z / Math.sqrt(2)));
                    return height * emg * 0.3; // Normalize
                }
                return height * Math.exp(-Math.pow(time - rt, 2) / (2 * sigma * sigma));
            }
        },

        /**
         * Error function approximation (for EMG calculation)
         */
        erf(x) {
            const a1 = 0.254829592;
            const a2 = -0.284496736;
            const a3 = 1.421413741;
            const a4 = -1.453152027;
            const a5 = 1.061405429;
            const p = 0.3275911;

            const sign = x < 0 ? -1 : 1;
            x = Math.abs(x);

            const t = 1.0 / (1.0 + p * x);
            const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

            return sign * y;
        },

        /**
         * Calculate detector response based on wavelength and compound
         */
        calculateDetectorResponse(compound, wavelength) {
            // Simplified UV absorption model
            const lambdaMax = compound.lambdaMax;
            const bandwidth = 30; // nm

            // Gaussian absorption profile
            const exponent = -Math.pow(wavelength - lambdaMax, 2) / (2 * bandwidth * bandwidth);
            const relativeResponse = Math.exp(exponent);

            return relativeResponse * (compound.molarAbsorptivity / 10000);
        }
    };

    // ========================================================================
    // TOAST NOTIFICATION SYSTEM
    // ========================================================================

    const Toast = {
        container: null,

        init() {
            this.container = document.getElementById('toast-container');
            if (!this.container) {
                this.container = document.createElement('div');
                this.container.id = 'toast-container';
                document.body.appendChild(this.container);
            }
        },

        show(message, type = 'info', duration = 3000) {
            if (!this.container) this.init();

            const toast = document.createElement('div');
            toast.className = `toast ${type}`;

            const icons = {
                success: 'fa-check-circle',
                error: 'fa-exclamation-circle',
                warning: 'fa-exclamation-triangle',
                info: 'fa-info-circle'
            };

            toast.innerHTML = `
                <i class="fas ${icons[type] || icons.info}"></i>
                <span class="toast-message">${message}</span>
            `;

            this.container.appendChild(toast);

            // Auto remove
            setTimeout(() => {
                toast.style.animation = 'fadeOut 0.3s ease forwards';
                setTimeout(() => toast.remove(), 300);
            }, duration);

            return toast;
        },

        success(message, duration) {
            return this.show(message, 'success', duration);
        },

        error(message, duration) {
            return this.show(message, 'error', duration);
        },

        warning(message, duration) {
            return this.show(message, 'warning', duration);
        },

        info(message, duration) {
            return this.show(message, 'info', duration);
        }
    };

    // ========================================================================
    // LOADING OVERLAY
    // ========================================================================

    const LoadingOverlay = {
        element: null,
        textElement: null,

        init() {
            this.element = document.getElementById('loading-overlay');
            this.textElement = document.getElementById('loading-text');
        },

        show(message = 'Loading...') {
            if (!this.element) this.init();
            if (this.textElement) this.textElement.textContent = message;
            if (this.element) this.element.classList.remove('hidden');
        },

        hide() {
            if (this.element) this.element.classList.add('hidden');
        },

        update(message) {
            if (this.textElement) this.textElement.textContent = message;
        }
    };

    // ========================================================================
    // MAIN APPLICATION CLASS
    // ========================================================================

    class App {
        constructor() {
            this.ui = null;
            this.simulation = null;
            this.difficultyLevel = 'beginner';
            this.soundEnabled = true;
            this.initialized = false;
        }

        async init() {
            try {
                LoadingOverlay.show('Initializing SimuPharma...');

                // Initialize toast system
                Toast.init();

                // Initialize UI
                this.ui = new UI(this);
                await this.ui.init();

                // Initialize simulation engine
                this.simulation = new Simulation(this.ui, this);

                // Bind difficulty selector
                this.bindDifficultySelector();

                // Hide loading overlay
                LoadingOverlay.hide();

                this.initialized = true;
                Toast.success('SimuPharma initialized successfully!');

            } catch (error) {
                console.error('Initialization error:', error);
                LoadingOverlay.hide();
                Toast.error('Failed to initialize. Please refresh the page.');
            }
        }

        bindDifficultySelector() {
            const buttons = document.querySelectorAll('.difficulty-btn');
            buttons.forEach(btn => {
                btn.addEventListener('click', () => {
                    buttons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    this.setDifficulty(btn.dataset.level);
                });
            });
        }

        setDifficulty(level) {
            this.difficultyLevel = level;

            // Adjust UI based on difficulty
            switch (level) {
                case 'beginner':
                    // Show all hints and tooltips
                    document.querySelectorAll('.hotspot-tooltip').forEach(el => el.style.display = 'block');
                    Toast.info('Beginner mode: All hints enabled');
                    break;
                case 'intermediate':
                    // Reduce hints
                    Toast.info('Intermediate mode: Reduced assistance');
                    break;
                case 'advanced':
                    // Minimal guidance
                    Toast.info('Advanced mode: Minimal guidance - Good luck!');
                    break;
            }

            if (this.simulation) {
                this.simulation.setDifficulty(level);
            }
        }

        runSimulation() {
            if (this.simulation) {
                this.simulation.start();
            }
        }

        stopSimulation() {
            if (this.simulation) {
                this.simulation.stop();
            }
        }

        pauseSimulation() {
            if (this.simulation) {
                this.simulation.pause();
            }
        }

        resetSimulation() {
            if (this.simulation) {
                this.simulation.reset();
            }
        }

        toggleStandardOverlay() {
            if (this.simulation) {
                this.simulation.toggleStandardOverlay();
            }
        }

        runSST() {
            if (this.simulation) {
                this.simulation.calculateSST();
            }
        }

        setFault(faultType) {
            if (this.simulation) {
                this.simulation.setFault(faultType);
            }
        }
    }

    // ========================================================================
    // UI CLASS - User Interface Management
    // ========================================================================

    class UI {
        constructor(app) {
            this.app = app;
            this.elements = {};
            this.charts = {};
            this.audio = {};
            this.wizardStep = 1;
            this.currentModal = null;
        }

        async init() {
            this.cacheElements();
            this.initAudio();
            await this.initCharts();
            this.bindEventListeners();
            this.startClock();
            this.initGradientPreview();
        }

        cacheElements() {
            this.elements = {
                // Views
                mainView: document.getElementById('hplc-main-view'),
                screenView: document.getElementById('main-screen-view'),

                // Modals
                backdrop: document.getElementById('modal-backdrop'),
                modals: document.querySelectorAll('.modal'),
                setupModal: document.getElementById('setup-modal'),
                pumpModal: document.getElementById('pump-modal'),
                columnModal: document.getElementById('column-modal'),
                detectorModal: document.getElementById('detector-modal'),
                confirmationModal: document.getElementById('confirmation-modal'),
                resultsModal: document.getElementById('results-modal'),
                sstModal: document.getElementById('sst-modal'),
                faultModal: document.getElementById('fault-modal'),

                // Hotspots
                hotspots: document.querySelectorAll('.hotspot'),
                setupTrigger: document.getElementById('hotspot-setup'),

                // Status displays
                systemStatusChip: document.getElementById('system-status-chip'),
                screenTitle: document.getElementById('screen-title'),
                runStatusIndicator: document.getElementById('run-status-indicator'),
                systemTime: document.getElementById('system-time'),

                // Quick stats
                qsSolventLevel: document.getElementById('qs-solvent-level'),
                qsPressure: document.getElementById('qs-pressure'),
                qsTemp: document.getElementById('qs-temp'),
                qsRuntime: document.getElementById('qs-runtime'),

                // Screen readouts
                screenFlowRate: document.getElementById('screen-flow-rate'),
                screenPressure: document.getElementById('screen-pressure'),
                screenColumnTemp: document.getElementById('screen-column-temp'),
                liveFlowRate: document.getElementById('live-flow-rate'),
                liveColumnTemp: document.getElementById('live-column-temp'),
                liveWavelength: document.getElementById('live-wavelength'),
                liveInjectionVol: document.getElementById('live-injection-vol'),
                elapsedTime: document.getElementById('elapsed-time'),
                totalRunTime: document.getElementById('total-run-time'),
                timerProgressFill: document.getElementById('timer-progress-fill'),

                // Gauge elements
                gaugeNeedle: document.getElementById('gauge-needle'),
                gaugeValueArc: document.getElementById('gauge-value-arc'),
                thermoFillLevel: document.getElementById('thermo-fill-level'),
                thermoTargetMarker: document.getElementById('thermo-target-marker'),

                // Pump channels
                pumpABar: document.getElementById('pump-a-bar'),
                pumpBBar: document.getElementById('pump-b-bar'),
                pumpAPercent: document.getElementById('pump-a-percent'),
                pumpBPercent: document.getElementById('pump-b-percent'),
                flowAnimation: document.getElementById('flow-animation'),

                // Method info
                methodName: document.getElementById('method-name'),
                sampleName: document.getElementById('sample-name'),

                // Log panel
                logContent: document.getElementById('log-content'),
                clearLogBtn: document.getElementById('clear-log-btn'),

                // Controls
                controls: {
                    flowRate: {
                        input: document.getElementById('flow-rate-input'),
                        number: document.getElementById('flow-rate-number')
                    },
                    columnTemp: {
                        input: document.getElementById('column-temp-input'),
                        display: document.getElementById('column-temp-display')
                    },
                    wavelength: {
                        input: document.getElementById('wavelength-input'),
                        number: document.getElementById('wavelength-number'),
                        marker: document.getElementById('wavelength-marker')
                    },
                    injectionVol: {
                        input: document.getElementById('injection-vol-input'),
                        number: document.getElementById('injection-vol-number')
                    },
                    concentration: {
                        input: document.getElementById('concentration-input'),
                        number: document.getElementById('concentration-number')
                    },
                    columnType: document.querySelectorAll('input[name="column-type"]'),
                    sample: document.getElementById('sample-select'),
                    instantMode: document.getElementById('instant-mode-toggle'),
                    faultMode: document.getElementById('fault-mode-toggle'),
                    gradientTableBody: document.getElementById('gradient-table-body')
                },

                // Buttons
                buttons: {
                    run: document.getElementById('run-button'),
                    stop: document.getElementById('stop-button'),
                    pause: document.getElementById('pause-button'),
                    reset: document.getElementById('reset-button'),
                    overlayStandard: document.getElementById('overlay-std-button'),
                    sstReport: document.getElementById('sst-report-button'),
                    backToMain: document.getElementById('back-to-main-view-button'),
                    fullscreen: document.getElementById('fullscreen-button'),
                    confirmRun: document.getElementById('confirm-run-button'),
                    modifyParams: document.getElementById('modify-params-button'),
                    wizardPrev: document.getElementById('wizard-prev-btn'),
                    wizardNext: document.getElementById('wizard-next-btn'),
                    wizardFinish: document.getElementById('wizard-finish-btn'),
                    addGradientRow: document.getElementById('add-gradient-row'),
                    applyFault: document.getElementById('apply-fault-btn'),
                    exportResults: document.getElementById('export-results-btn'),
                    exportSST: document.getElementById('export-sst-btn')
                },

                // Chart tools
                chartTools: {
                    zoomIn: document.getElementById('zoom-in-btn'),
                    zoomOut: document.getElementById('zoom-out-btn'),
                    resetZoom: document.getElementById('reset-zoom-btn'),
                    toggleIntegration: document.getElementById('toggle-integration-btn'),
                    togglePeaks: document.getElementById('toggle-peaks-btn'),
                    exportData: document.getElementById('export-data-btn'),
                    screenshot: document.getElementById('screenshot-btn')
                },

                // Wizard elements
                wizardSteps: document.querySelectorAll('.wizard-step'),
                wizardConnectors: document.querySelectorAll('.wizard-connector'),
                wizardPanels: document.querySelectorAll('.wizard-panel'),

                // Confirmation
                confirmationList: document.getElementById('confirmation-list'),

                // Results
                resultsTableContainer: document.getElementById('results-table-container'),
                resultRuntime: document.getElementById('result-runtime'),
                resultPeaks: document.getElementById('result-peaks'),
                resultStatus: document.getElementById('result-status'),

                // SST
                sstTableBody: document.getElementById('sst-table-body'),
                sstMethodName: document.getElementById('sst-method-name'),
                sstDate: document.getElementById('sst-date'),
                sstVerdict: document.getElementById('sst-verdict'),

                // Startup wizard
                startupProgressFill: document.getElementById('startup-progress-fill')
            };
        }

        initAudio() {
            this.audio = {
                click: document.getElementById('audio-click'),
                pumpStart: document.getElementById('audio-pump-start'),
                pumpLoop: document.getElementById('audio-pump-loop'),
                analysisComplete: document.getElementById('audio-analysis-complete'),
                error: document.getElementById('audio-error'),
                beep: document.getElementById('audio-beep')
            };
        }

        async initCharts() {
            // Register peak annotation plugin
            Chart.register(peakAnnotationPlugin);

            // Main chromatogram chart
            const ctx = document.getElementById('hplc-chart');
            if (ctx) {
                this.charts.main = new Chart(ctx, this.getMainChartConfig());
            }

            // Gradient preview chart (in modal)
            const gradientCtx = document.getElementById('gradient-modal-chart');
            if (gradientCtx) {
                this.charts.gradientModal = new Chart(gradientCtx, this.getGradientChartConfig());
            }

            // Mini gradient preview (in left panel)
            const gradientPreviewCtx = document.getElementById('gradient-preview-chart');
            if (gradientPreviewCtx) {
                this.charts.gradientPreview = new Chart(gradientPreviewCtx, this.getGradientChartConfig(true));
            }
        }

        getMainChartConfig() {
            return {
                type: 'line',
                data: {
                    datasets: [
                        {
                            label: 'Signal',
                            borderColor: '#3b82f6',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            fill: true,
                            borderWidth: 2,
                            tension: 0.1,
                            pointRadius: 0,
                            data: []
                        },
                        {
                            label: 'Standard',
                            borderColor: '#f59e0b',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            tension: 0.1,
                            pointRadius: 0,
                            data: [],
                            hidden: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: false,
                    interaction: {
                        mode: 'index',
                        intersect: false
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            enabled: true,
                            backgroundColor: 'rgba(26, 34, 56, 0.9)',
                            titleColor: '#f1f5f9',
                            bodyColor: '#94a3b8',
                            borderColor: 'rgba(255, 255, 255, 0.1)',
                            borderWidth: 1,
                            callbacks: {
                                label: (context) => {
                                    return `${context.parsed.y.toFixed(2)} mAU`;
                                },
                                title: (contexts) => {
                                    return `Time: ${contexts[0].parsed.x.toFixed(3)} min`;
                                }
                            }
                        },
                        zoom: {
                            zoom: {
                                wheel: { enabled: true },
                                pinch: { enabled: true },
                                mode: 'xy'
                            },
                            pan: {
                                enabled: true,
                                mode: 'xy'
                            }
                        }
                    },
                    scales: {
                        x: {
                            type: 'linear',
                            min: 0,
                            max: 15,
                            title: {
                                display: true,
                                text: 'Time (min)',
                                color: '#94a3b8',
                                font: { size: 12 }
                            },
                            ticks: {
                                color: '#64748b',
                                font: { family: "'JetBrains Mono', monospace" }
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.05)'
                            }
                        },
                        y: {
                            min: -5,
                            max: 150,
                            title: {
                                display: true,
                                text: 'Absorbance (mAU)',
                                color: '#94a3b8',
                                font: { size: 12 }
                            },
                            ticks: {
                                color: '#64748b',
                                font: { family: "'JetBrains Mono', monospace" }
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.05)'
                            }
                        }
                    }
                }
            };
        }

        getGradientChartConfig(mini = false) {
            return {
                type: 'line',
                data: {
                    datasets: [
                        {
                            label: '%B',
                            borderColor: '#2196F3',
                            backgroundColor: 'rgba(33, 150, 243, 0.2)',
                            fill: true,
                            borderWidth: 2,
                            tension: 0,
                            pointRadius: mini ? 0 : 4,
                            pointBackgroundColor: '#2196F3',
                            data: []
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            type: 'linear',
                            min: 0,
                            title: {
                                display: !mini,
                                text: 'Time (min)',
                                color: '#94a3b8'
                            },
                            ticks: { color: '#64748b', display: !mini },
                            grid: { color: 'rgba(255, 255, 255, 0.05)' }
                        },
                        y: {
                            min: 0,
                            max: 100,
                            title: {
                                display: !mini,
                                text: '%B',
                                color: '#94a3b8'
                            },
                            ticks: { color: '#64748b', display: !mini },
                            grid: { color: 'rgba(255, 255, 255, 0.05)' }
                        }
                    }
                }
            };
        }

        initGradientPreview() {
            this.updateGradientCharts();
        }

        bindEventListeners() {
            // Hotspot clicks
            this.elements.hotspots.forEach(hotspot => {
                hotspot.addEventListener('click', () => this.handleHotspotClick(hotspot));
            });

            // Setup trigger (special hotspot)
            if (this.elements.setupTrigger) {
                this.elements.setupTrigger.addEventListener('click', () => {
                    this.playSound('click');
                    this.showModal('setup-modal');
                });
            }

            // Modal close buttons
            document.querySelectorAll('.modal-close-btn').forEach(btn => {
                btn.addEventListener('click', () => this.hideAllModals());
            });

            // Modal confirm buttons
            document.querySelectorAll('.modal-confirm-btn').forEach(btn => {
                btn.addEventListener('click', () => this.hideAllModals());
            });

            // Backdrop click to close
            if (this.elements.backdrop) {
                this.elements.backdrop.addEventListener('click', () => this.hideAllModals());
            }

            // Wizard navigation
            this.bindWizardEvents();

            // Control inputs
            this.bindControlInputs();

            // Button clicks
            this.bindButtonEvents();

            // Chart tools
            this.bindChartTools();

            // Temperature presets
            this.bindTempPresets();

            // Wavelength presets
            this.bindWavelengthPresets();

            // Column cards
            this.bindColumnCards();

            // Gradient table
            this.bindGradientTable();

            // Mobile phase configuration (Industry-grade)
            this.bindMobilePhaseControls();

            // Sample preparation workflow
            this.bindSamplePrepControls();

            // Fault mode toggle
            if (this.elements.controls.faultMode) {
                this.elements.controls.faultMode.addEventListener('change', (e) => {
                    if (e.target.checked) {
                        this.showModal('fault-modal');
                    } else {
                        this.app.setFault('none');
                    }
                });
            }

            // Clear log button
            if (this.elements.clearLogBtn) {
                this.elements.clearLogBtn.addEventListener('click', () => this.clearLog());
            }
        }

        handleHotspotClick(hotspot) {
            this.playSound('click');

            const hotspotId = hotspot.id;
            const controlsModal = hotspot.dataset.controls;

            if (hotspotId === 'hotspot-screen') {
                // Check if system is ready
                if (!this.app.simulation || !this.app.simulation.state.isSystemReady) {
                    Toast.warning('System not ready. Complete the startup wizard first.');
                    return;
                }
                this.showConfirmation();
            } else if (controlsModal) {
                this.showModal(controlsModal);
            }
        }

        bindWizardEvents() {
            // Wizard previous button
            if (this.elements.buttons.wizardPrev) {
                this.elements.buttons.wizardPrev.addEventListener('click', () => {
                    if (this.wizardStep > 1) {
                        this.goToWizardStep(this.wizardStep - 1);
                    }
                });
            }

            // Wizard next button
            if (this.elements.buttons.wizardNext) {
                this.elements.buttons.wizardNext.addEventListener('click', () => {
                    if (this.wizardStep < 4) {
                        this.goToWizardStep(this.wizardStep + 1);
                    }
                });
            }

            // Wizard finish button
            if (this.elements.buttons.wizardFinish) {
                this.elements.buttons.wizardFinish.addEventListener('click', () => {
                    this.finishWizard();
                });
            }

            // Step 1: Refill button
            const btnRefill = document.getElementById('btn-refill');
            if (btnRefill) {
                btnRefill.addEventListener('click', () => this.handleRefill());
            }

            // Step 1: Degas button
            const btnDegas = document.getElementById('btn-degas');
            if (btnDegas) {
                btnDegas.addEventListener('click', () => this.handleDegas());
            }

            // Step 2: Purge valve toggle
            const purgeValve = document.getElementById('purge-valve-toggle');
            if (purgeValve) {
                purgeValve.addEventListener('change', (e) => this.handlePurgeValve(e.target.checked));
            }

            // Step 2: Prime button
            const btnPrime = document.getElementById('btn-prime');
            if (btnPrime) {
                btnPrime.addEventListener('click', () => this.handlePrime());
            }

            // Step 3: Equilibrate button
            const btnEquilibrate = document.getElementById('btn-equilibrate');
            if (btnEquilibrate) {
                btnEquilibrate.addEventListener('click', () => this.handleEquilibrate());
            }
        }

        handleRefill() {
            const btn = document.getElementById('btn-refill');
            const videoStep = document.getElementById('video-step-1');
            const overlay = document.getElementById('overlay-step-1');
            const statusA = document.getElementById('status-bottle-a');
            const statusB = document.getElementById('status-bottle-b');

            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Filling...';

            // Show video, hide overlay
            if (overlay) overlay.classList.add('hidden');
            if (videoStep) {
                videoStep.play();
            }

            // Animate status updates
            setTimeout(() => {
                if (statusA) {
                    statusA.textContent = 'Filled';
                    statusA.className = 'status-value complete';
                }
            }, 2000);

            setTimeout(() => {
                if (statusB) {
                    statusB.textContent = 'Filled';
                    statusB.className = 'status-value complete';
                }
            }, 4000);

            setTimeout(() => {
                btn.innerHTML = '<i class="fas fa-check"></i> Filled';
                if (videoStep) videoStep.pause();

                // Enable degas button
                const btnDegas = document.getElementById('btn-degas');
                if (btnDegas) btnDegas.disabled = false;

                this.addLog('Solvent bottles filled (A: Water, B: Acetonitrile)', 'success');
            }, 6000);
        }

        handleDegas() {
            const btn = document.getElementById('btn-degas');
            const statusDegas = document.getElementById('status-degas');
            const videoFill = document.getElementById('video-fill');
            const videoBubbling = document.getElementById('video-degas-visual');

            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Degassing...';

            if (statusDegas) {
                statusDegas.textContent = 'In Progress';
                statusDegas.className = 'status-value progress';
            }

            // Logic to swap the visual elements
            if (videoFill && videoBubbling) {
                videoFill.style.display = 'none';      // Hide filling video
                videoFill.pause();                    // Ensure it's stopped

                videoBubbling.style.display = 'block'; // Show bubbling video
                videoBubbling.currentTime = 0;         // Reset to start
                videoBubbling.play();                  // Play it
            }

            setTimeout(() => {
                btn.innerHTML = '<i class="fas fa-check"></i> Degassed';
                if (statusDegas) {
                    statusDegas.textContent = 'Complete';
                    statusDegas.className = 'status-value complete';
                }

                if (videoBubbling) videoBubbling.pause();

                this.elements.buttons.wizardNext.disabled = false;
                this.markWizardStepComplete(1);

                this.addLog('Mobile phase degassed using helium sparging', 'success');
                Toast.success('Step 1 complete! Click Next to continue.');
            }, 6000);
        }

        handlePurgeValve(isOpen) {
            const valveStatus = document.getElementById('valve-status');
            const btnPrime = document.getElementById('btn-prime');
            const warning = document.getElementById('valve-warning');

            if (this.app.simulation) {
                this.app.simulation.state.purgeValveOpen = isOpen;
            }

            if (valveStatus) {
                valveStatus.textContent = isOpen ? 'OPEN' : 'CLOSED';
            }

            if (btnPrime) {
                btnPrime.disabled = !isOpen;
            }

            // Show warning if valve is open after priming
            if (warning && this.app.simulation?.state.linesPrimed && isOpen) {
                // Show warning
            }

            this.addLog(`Purge valve ${isOpen ? 'OPENED' : 'CLOSED'}`, isOpen ? 'warning' : 'info');
        }

        handlePrime() {
            const btn = document.getElementById('btn-prime');
            const progressFill = document.getElementById('purge-progress-fill');
            const progressText = document.getElementById('purge-progress-text');
            const videoStep = document.getElementById('video-step-2');
            const overlay = document.getElementById('overlay-step-2');

            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Purging...';

            if (overlay) overlay.classList.add('hidden');
            if (videoStep) videoStep.play();

            this.playSound('pumpLoop');

            let progress = 0;
            const interval = setInterval(() => {
                progress += 1;
                if (progressFill) progressFill.style.width = `${progress}%`;
                if (progressText) progressText.textContent = `${progress}%`;

                if (progress >= 100) {
                    clearInterval(interval);
                    this.stopSound('pumpLoop');

                    if (videoStep) videoStep.pause();
                    btn.innerHTML = '<i class="fas fa-check"></i> Primed';

                    // Check if valve is still open
                    const valveToggle = document.getElementById('purge-valve-toggle');
                    if (valveToggle && valveToggle.checked) {
                        Toast.warning('Lines primed! Close the purge valve to continue.');
                        const warning = document.getElementById('valve-warning');
                        if (warning) warning.classList.remove('hidden');

                        // Wait for valve to be closed
                        const checkValve = setInterval(() => {
                            if (!valveToggle.checked) {
                                clearInterval(checkValve);
                                this.finishPriming();
                            }
                        }, 500);
                    } else {
                        this.finishPriming();
                    }
                }
            }, 80); // 8 seconds total
        }

        finishPriming() {
            if (this.app.simulation) {
                this.app.simulation.state.linesPrimed = true;
            }

            this.elements.buttons.wizardNext.disabled = false;
            this.markWizardStepComplete(2);

            const warning = document.getElementById('valve-warning');
            if (warning) warning.classList.add('hidden');

            this.addLog('Pump lines primed successfully - air removed from system', 'success');
            Toast.success('Step 2 complete! Click Next to continue.');
        }

        handleEquilibrate() {
            const btn = document.getElementById('btn-equilibrate');
            const videoStep = document.getElementById('video-step-3');
            const overlay = document.getElementById('overlay-step-3');
            const eqProgressCircle = document.getElementById('eq-progress-circle');
            const eqTempDisplay = document.getElementById('eq-temp-display');
            const eqBaselineNoise = document.getElementById('eq-baseline-noise');
            const eqTargetTemp = document.getElementById('eq-target-temp');

            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Equilibrating...';

            if (overlay) overlay.classList.add('hidden');
            if (videoStep) videoStep.play();

            const targetTemp = this.app.simulation?.state.columnTemp || 30;
            if (eqTargetTemp) eqTargetTemp.textContent = `${targetTemp}°C`;

            let currentTemp = 25;
            let progress = 0;
            const circumference = 2 * Math.PI * 45;

            const interval = setInterval(() => {
                progress += 2;
                currentTemp = Utils.lerp(25, targetTemp, progress / 100);

                if (eqTempDisplay) eqTempDisplay.textContent = Math.round(currentTemp);
                if (eqProgressCircle) {
                    const dashOffset = circumference - (progress / 100) * circumference;
                    eqProgressCircle.style.strokeDasharray = `${circumference - dashOffset} ${circumference}`;
                }
                if (eqBaselineNoise) {
                    const noise = Math.max(0.1, 2 - (progress / 50));
                    eqBaselineNoise.textContent = `${noise.toFixed(2)} mAU`;
                }

                if (progress >= 100) {
                    clearInterval(interval);
                    if (videoStep) videoStep.pause();
                    btn.innerHTML = '<i class="fas fa-check"></i> Equilibrated';

                    this.elements.buttons.wizardNext.disabled = false;
                    this.markWizardStepComplete(3);

                    this.addLog(`Column equilibrated at ${targetTemp}°C, baseline stable`, 'success');
                    Toast.success('Step 3 complete! System ready for analysis.');
                }
            }, 60); // ~6 seconds
        }

        goToWizardStep(step) {
            this.wizardStep = step;

            // Update step indicators
            this.elements.wizardSteps.forEach((el, index) => {
                el.classList.remove('active');
                if (index + 1 === step) {
                    el.classList.add('active');
                }
            });

            // Update panels
            this.elements.wizardPanels.forEach((panel, index) => {
                panel.classList.remove('active');
                if (index + 1 === step) {
                    panel.classList.add('active');
                }
            });

            // Update navigation buttons
            this.elements.buttons.wizardPrev.disabled = step === 1;

            if (step === 4) {
                this.elements.buttons.wizardNext.classList.add('hidden');
                this.elements.buttons.wizardFinish.classList.remove('hidden');
                this.elements.buttons.wizardFinish.disabled = false;
            } else {
                this.elements.buttons.wizardNext.classList.remove('hidden');
                this.elements.buttons.wizardFinish.classList.add('hidden');
            }
        }

        markWizardStepComplete(step) {
            const stepElement = this.elements.wizardSteps[step - 1];
            if (stepElement) {
                stepElement.classList.add('completed');
            }

            // Mark connector as completed
            if (step < 4 && this.elements.wizardConnectors[step - 1]) {
                this.elements.wizardConnectors[step - 1].classList.add('completed');
            }
        }

        finishWizard() {
            // Set system as ready
            if (this.app.simulation) {
                this.app.simulation.state.isSystemReady = true;
                this.app.simulation.state.solventsReady = true;
                this.app.simulation.state.linesPrimed = true;
                this.app.simulation.state.columnReady = true;
            }

            // Update UI
            this.hideAllModals();

            // Update startup button appearance
            if (this.elements.setupTrigger) {
                this.elements.setupTrigger.classList.add('ready');
                const text = this.elements.setupTrigger.querySelector('.startup-text');
                if (text) text.textContent = 'System Ready';
                const progress = this.elements.setupTrigger.querySelector('.startup-progress-fill');
                if (progress) progress.style.width = '100%';
            }

            // Update status chip
            if (this.elements.systemStatusChip) {
                const dot = this.elements.systemStatusChip.querySelector('.status-dot');
                const text = this.elements.systemStatusChip.querySelector('span:last-child');
                if (dot) dot.classList.add('online');
                if (text) text.textContent = 'System Online';
            }

            // Enable run button
            if (this.elements.buttons.run) {
                this.elements.buttons.run.disabled = false;
            }

            // Update quick stats
            this.updateQuickStats();

            this.addLog('System startup complete. Instrument ready for analysis.', 'success');
            Toast.success('System ready! You can now run analyses.');
        }

        bindControlInputs() {
            // Flow rate
            const flowInput = this.elements.controls.flowRate?.input;
            const flowNumber = this.elements.controls.flowRate?.number;

            if (flowInput && flowNumber) {
                flowInput.addEventListener('input', (e) => {
                    const value = parseFloat(e.target.value);
                    flowNumber.value = value;
                    this.app.simulation?.setParameter('flowRate', value);
                });

                flowNumber.addEventListener('change', (e) => {
                    const value = Utils.clamp(parseFloat(e.target.value), 0.1, 5.0);
                    flowInput.value = value;
                    e.target.value = value;
                    this.app.simulation?.setParameter('flowRate', value);
                });
            }

            // Column temperature
            const tempInput = this.elements.controls.columnTemp?.input;
            const tempDisplay = this.elements.controls.columnTemp?.display;

            if (tempInput && tempDisplay) {
                tempInput.addEventListener('input', (e) => {
                    const value = parseInt(e.target.value);
                    tempDisplay.textContent = value;
                    this.app.simulation?.setParameter('columnTemp', value);
                });
            }

            // Wavelength
            const wlInput = this.elements.controls.wavelength?.input;
            const wlNumber = this.elements.controls.wavelength?.number;
            const wlMarker = this.elements.controls.wavelength?.marker;

            if (wlInput && wlNumber) {
                const updateWavelength = (value) => {
                    this.app.simulation?.setParameter('wavelength', value);
                    // Update marker position
                    if (wlMarker) {
                        const percent = ((value - 190) / (800 - 190)) * 100;
                        wlMarker.style.left = `${percent}%`;
                    }
                };

                wlInput.addEventListener('input', (e) => {
                    const value = parseInt(e.target.value);
                    wlNumber.value = value;
                    updateWavelength(value);
                });

                wlNumber.addEventListener('change', (e) => {
                    const value = Utils.clamp(parseInt(e.target.value), 190, 800);
                    wlInput.value = value;
                    e.target.value = value;
                    updateWavelength(value);
                });
            }

            // Injection volume
            const injInput = this.elements.controls.injectionVol?.input;
            const injNumber = this.elements.controls.injectionVol?.number;

            if (injInput && injNumber) {
                injInput.addEventListener('input', (e) => {
                    const value = parseInt(e.target.value);
                    injNumber.value = value;
                    this.app.simulation?.setParameter('injectionVolume', value);
                });

                injNumber.addEventListener('change', (e) => {
                    const value = Utils.clamp(parseInt(e.target.value), 1, 100);
                    injInput.value = value;
                    e.target.value = value;
                    this.app.simulation?.setParameter('injectionVolume', value);
                });
            }

            // Concentration
            const concInput = this.elements.controls.concentration?.input;
            const concNumber = this.elements.controls.concentration?.number;

            if (concInput && concNumber) {
                concInput.addEventListener('input', (e) => {
                    const value = parseInt(e.target.value);
                    concNumber.value = value;
                    this.app.simulation?.setParameter('concentration', value);
                });

                concNumber.addEventListener('change', (e) => {
                    const value = Utils.clamp(parseInt(e.target.value), 1, 1000);
                    concInput.value = value;
                    e.target.value = value;
                    this.app.simulation?.setParameter('concentration', value);
                });
            }

            // Sample select
            if (this.elements.controls.sample) {
                this.elements.controls.sample.addEventListener('change', (e) => {
                    this.app.simulation?.setParameter('sample', e.target.value);
                });
            }

            // Instant mode toggle
            if (this.elements.controls.instantMode) {
                this.elements.controls.instantMode.addEventListener('change', (e) => {
                    this.app.simulation?.setParameter('instantMode', e.target.checked);
                });
            }
        }

        bindButtonEvents() {
            // Run button
            this.elements.buttons.run?.addEventListener('click', () => {
                this.playSound('click');
                this.app.runSimulation();
            });

            // Stop button
            this.elements.buttons.stop?.addEventListener('click', () => {
                this.playSound('click');
                this.app.stopSimulation();
            });

            // Pause button
            this.elements.buttons.pause?.addEventListener('click', () => {
                this.playSound('click');
                this.app.pauseSimulation();
            });

            // Reset button
            this.elements.buttons.reset?.addEventListener('click', () => {
                this.playSound('click');
                this.app.resetSimulation();
            });

            // Overlay standard
            this.elements.buttons.overlayStandard?.addEventListener('click', () => {
                this.playSound('click');
                this.app.toggleStandardOverlay();
            });

            // SST Report
            this.elements.buttons.sstReport?.addEventListener('click', () => {
                this.playSound('click');
                this.app.runSST();
            });

            // Back to main view
            this.elements.buttons.backToMain?.addEventListener('click', () => {
                this.playSound('click');
                this.switchView('main');
            });

            // Fullscreen
            this.elements.buttons.fullscreen?.addEventListener('click', () => {
                this.toggleFullscreen();
            });

            // Confirm run
            this.elements.buttons.confirmRun?.addEventListener('click', () => {
                this.hideAllModals();
                this.switchView('screen');
                this.app.runSimulation();
            });

            // Modify params
            this.elements.buttons.modifyParams?.addEventListener('click', () => {
                this.hideAllModals();
            });

            // Apply fault
            this.elements.buttons.applyFault?.addEventListener('click', () => {
                const selectedFault = document.querySelector('input[name="fault-type"]:checked');
                if (selectedFault) {
                    this.app.setFault(selectedFault.value);
                    this.hideAllModals();
                    Toast.info(`Fault simulation: ${CONFIG.faults[selectedFault.value].name}`);
                }
            });

            // Export results
            this.elements.buttons.exportResults?.addEventListener('click', () => {
                this.exportResults();
            });

            // Export SST
            this.elements.buttons.exportSST?.addEventListener('click', () => {
                this.exportSST();
            });
        }

        bindChartTools() {
            // Zoom in
            this.elements.chartTools.zoomIn?.addEventListener('click', () => {
                if (this.charts.main) {
                    this.charts.main.zoom(1.2);
                }
            });

            // Zoom out
            this.elements.chartTools.zoomOut?.addEventListener('click', () => {
                if (this.charts.main) {
                    this.charts.main.zoom(0.8);
                }
            });

            // Reset zoom
            this.elements.chartTools.resetZoom?.addEventListener('click', () => {
                if (this.charts.main) {
                    this.charts.main.resetZoom();
                }
            });

            // Toggle integration (area fill)
            this.elements.chartTools.toggleIntegration?.addEventListener('click', (e) => {
                const btn = e.currentTarget;
                btn.classList.toggle('active');
                if (this.charts.main) {
                    this.charts.main.data.datasets[0].fill = btn.classList.contains('active');
                    this.charts.main.update('none');
                }
            });

            // Toggle peak labels
            this.elements.chartTools.togglePeaks?.addEventListener('click', (e) => {
                e.currentTarget.classList.toggle('active');
                // Toggle peak annotations (would need annotations plugin)
            });

            // Export data
            this.elements.chartTools.exportData?.addEventListener('click', () => {
                this.exportChartData();
            });

            // Screenshot
            this.elements.chartTools.screenshot?.addEventListener('click', () => {
                this.takeScreenshot();
            });
        }

        bindTempPresets() {
            document.querySelectorAll('.temp-preset').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const temp = parseInt(e.currentTarget.dataset.temp);

                    // Update active state
                    document.querySelectorAll('.temp-preset').forEach(b => b.classList.remove('active'));
                    e.currentTarget.classList.add('active');

                    // Update controls
                    if (this.elements.controls.columnTemp?.input) {
                        this.elements.controls.columnTemp.input.value = temp;
                    }
                    if (this.elements.controls.columnTemp?.display) {
                        this.elements.controls.columnTemp.display.textContent = temp;
                    }

                    this.app.simulation?.setParameter('columnTemp', temp);
                });
            });
        }

        bindWavelengthPresets() {
            document.querySelectorAll('.wavelength-preset').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const wavelength = parseInt(e.currentTarget.dataset.wavelength);

                    // Update active state
                    document.querySelectorAll('.wavelength-preset').forEach(b => b.classList.remove('active'));
                    e.currentTarget.classList.add('active');

                    // Update controls
                    if (this.elements.controls.wavelength?.input) {
                        this.elements.controls.wavelength.input.value = wavelength;
                    }
                    if (this.elements.controls.wavelength?.number) {
                        this.elements.controls.wavelength.number.value = wavelength;
                    }

                    // Update marker
                    const marker = this.elements.controls.wavelength?.marker;
                    if (marker) {
                        const percent = ((wavelength - 190) / (800 - 190)) * 100;
                        marker.style.left = `${percent}%`;
                    }

                    this.app.simulation?.setParameter('wavelength', wavelength);
                });
            });
        }

        bindColumnCards() {
            document.querySelectorAll('.column-card').forEach(card => {
                card.addEventListener('click', () => {
                    // Update visual selection
                    document.querySelectorAll('.column-card').forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');

                    // Get column type
                    const input = card.querySelector('input');
                    if (input) {
                        input.checked = true;
                        this.app.simulation?.setParameter('columnType', input.value);

                        // Update column status display
                        this.updateColumnStatus(input.value);
                    }
                });
            });
        }

        updateColumnStatus(columnType) {
            const column = CONFIG.columns[columnType];
            if (!column) return;

            const platesEl = document.getElementById('column-plates');
            const pressureEl = document.getElementById('column-pressure-factor');

            if (platesEl) platesEl.textContent = `~${column.theoreticalPlates.toLocaleString()}`;
            if (pressureEl) pressureEl.textContent = `${column.pressureFactor.toFixed(1)}×`;
        }

        bindGradientTable() {
            // Add gradient row button
            this.elements.buttons.addGradientRow?.addEventListener('click', () => {
                this.addGradientRow();
            });

            // Remove gradient row buttons
            document.querySelectorAll('.remove-gradient-row').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const row = e.currentTarget.closest('tr');
                    if (row) {
                        row.remove();
                        this.updateGradientProgram();
                    }
                });
            });

            // Gradient input changes
            if (this.elements.controls.gradientTableBody) {
                this.elements.controls.gradientTableBody.addEventListener('input', Utils.debounce(() => {
                    this.updateGradientProgram();
                }, 300));
            }
        }

        addGradientRow() {
            const tbody = this.elements.controls.gradientTableBody;
            if (!tbody) return;

            const rowCount = tbody.rows.length;
            const lastRow = tbody.rows[rowCount - 1];
            const lastTime = lastRow ? parseFloat(lastRow.querySelector('.gradient-input').value) : 0;
            const lastPercent = lastRow ? parseFloat(lastRow.querySelectorAll('.gradient-input')[1].value) : 50;

            const newRow = document.createElement('tr');
            newRow.dataset.row = rowCount;
            newRow.innerHTML = `
                <td><input type="number" class="gradient-input" id="gradient_time_${rowCount}" value="${(lastTime + 2).toFixed(1)}" step="0.1"></td>
                <td><input type="number" class="gradient-input" id="gradient_percent_${rowCount}" value="${lastPercent}" min="0" max="100"></td>
                <td>
                    <select class="gradient-curve" id="gradient_curve_${rowCount}">
                        <option value="linear">Linear</option>
                        <option value="step">Step</option>
                    </select>
                </td>
                <td><button class="btn-icon remove-gradient-row"><i class="fas fa-minus"></i></button></td>
            `;

            tbody.appendChild(newRow);

            // Bind remove button
            newRow.querySelector('.remove-gradient-row').addEventListener('click', (e) => {
                e.currentTarget.closest('tr').remove();
                this.updateGradientProgram();
            });

            this.updateGradientProgram();
        }

        updateGradientProgram() {
            if (!this.app.simulation) return;

            const program = [];
            const rows = this.elements.controls.gradientTableBody?.rows;

            if (rows) {
                for (let i = 0; i < rows.length; i++) {
                    const timeInput = rows[i].querySelector('.gradient-input');
                    const percentInput = rows[i].querySelectorAll('.gradient-input')[1];
                    const curveSelect = rows[i].querySelector('.gradient-curve');

                    if (timeInput && percentInput) {
                        program.push({
                            time: parseFloat(timeInput.value) || 0,
                            percentB: parseFloat(percentInput.value) || 0,
                            curve: curveSelect?.value || 'linear'
                        });
                    }
                }
            }

            // Sort by time
            program.sort((a, b) => a.time - b.time);

            this.app.simulation.setParameter('gradientProgram', program);
            this.updateGradientCharts();
        }

        updateGradientCharts() {
            const program = this.app.simulation?.state.gradientProgram || [];
            const data = program.map(step => ({ x: step.time, y: step.percentB }));

            if (this.charts.gradientModal) {
                this.charts.gradientModal.data.datasets[0].data = data;
                this.charts.gradientModal.update('none');
            }

            if (this.charts.gradientPreview) {
                this.charts.gradientPreview.data.datasets[0].data = data;
                this.charts.gradientPreview.update('none');
            }
        }

        // =========================
        // MOBILE PHASE CONTROLS
        // =========================

        bindMobilePhaseControls() {
            // Solvent A (Aqueous) selection
            const solventASelect = document.getElementById('solvent-a-select');
            const phSection = document.getElementById('ph-control-section');
            const bufferSection = document.getElementById('buffer-conc-section');

            if (solventASelect) {
                solventASelect.addEventListener('change', (e) => {
                    const val = e.target.value;
                    this.app.simulation?.setParameter('mobilePhaseA', val);
                    const aq = SOLVENT_PROPERTIES.aqueous[val];
                    // Show/hide pH and buffer controls
                    if (aq?.isBuffer) {
                        if (phSection) phSection.style.display = '';
                        if (bufferSection) bufferSection.style.display = '';
                    } else {
                        if (phSection) phSection.style.display = 'none';
                        if (bufferSection) bufferSection.style.display = 'none';
                    }
                    this.updateMobilePhaseSummary();
                });
                // Initial visibility
                if (phSection) phSection.style.display = 'none';
                if (bufferSection) bufferSection.style.display = 'none';
            }

            // Solvent B (Organic) card selection
            document.querySelectorAll('.solvent-card').forEach(card => {
                card.addEventListener('click', () => {
                    document.querySelectorAll('.solvent-card').forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');
                    const input = card.querySelector('input');
                    if (input) {
                        input.checked = true;
                        this.app.simulation?.setParameter('mobilePhaseB', input.value);
                        this.checkUVCutoff(input.value);
                        this.updateMobilePhaseSummary();
                    }
                });
            });

            // pH controls
            const phInput = document.getElementById('ph-input');
            const phNumber = document.getElementById('ph-number');
            const phMarker = document.getElementById('ph-marker');

            const updatePH = (val) => {
                this.app.simulation?.setParameter('mobilePhasePH', val);
                if (phMarker) {
                    const percent = ((val - 2.0) / (12.0 - 2.0)) * 100;
                    phMarker.style.left = `${percent}%`;
                }
                const summaryPH = document.getElementById('mp-summary-ph');
                if (summaryPH) summaryPH.textContent = parseFloat(val).toFixed(1);
            };

            if (phInput) {
                phInput.addEventListener('input', (e) => {
                    const v = parseFloat(e.target.value);
                    if (phNumber) phNumber.value = v;
                    updatePH(v);
                });
            }
            if (phNumber) {
                phNumber.addEventListener('change', (e) => {
                    const v = Utils.clamp(parseFloat(e.target.value), 2.0, 12.0);
                    if (phInput) phInput.value = v;
                    e.target.value = v;
                    updatePH(v);
                });
            }

            // pH presets
            document.querySelectorAll('.ph-preset').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const ph = parseFloat(e.currentTarget.dataset.ph);
                    document.querySelectorAll('.ph-preset').forEach(b => b.classList.remove('active'));
                    e.currentTarget.classList.add('active');
                    if (phInput) phInput.value = ph;
                    if (phNumber) phNumber.value = ph;
                    updatePH(ph);
                });
            });

            // Buffer concentration
            const bufConcInput = document.getElementById('buffer-conc-input');
            const bufConcNumber = document.getElementById('buffer-conc-number');
            if (bufConcInput && bufConcNumber) {
                bufConcInput.addEventListener('input', (e) => {
                    bufConcNumber.value = e.target.value;
                    this.app.simulation?.setParameter('bufferConcentration', parseInt(e.target.value));
                });
                bufConcNumber.addEventListener('change', (e) => {
                    const v = Utils.clamp(parseInt(e.target.value), 5, 100);
                    bufConcInput.value = v;
                    e.target.value = v;
                    this.app.simulation?.setParameter('bufferConcentration', v);
                });
            }

            // Additive selection
            const additiveSelect = document.getElementById('additive-select');
            const additiveConcInput = document.getElementById('additive-conc-input');
            const additiveConcNumber = document.getElementById('additive-conc-number');
            const additiveInfoText = document.getElementById('additive-info-text');

            if (additiveSelect) {
                additiveSelect.addEventListener('change', (e) => {
                    const val = e.target.value;
                    this.app.simulation?.setParameter('additive', val);
                    if (additiveInfoText) {
                        additiveInfoText.textContent = ADDITIVE_INFO[val]?.desc || '';
                    }
                    this.updateMobilePhaseSummary();
                });
            }
            if (additiveConcInput && additiveConcNumber) {
                additiveConcInput.addEventListener('input', (e) => {
                    additiveConcNumber.value = e.target.value;
                    this.app.simulation?.setParameter('additiveConcentration', parseFloat(e.target.value));
                });
                additiveConcNumber.addEventListener('change', (e) => {
                    const v = Utils.clamp(parseFloat(e.target.value), 0.01, 1.0);
                    additiveConcInput.value = v;
                    e.target.value = v;
                    this.app.simulation?.setParameter('additiveConcentration', v);
                });
            }

            // Apply mobile phase button
            const applyBtn = document.getElementById('apply-solvents-btn');
            if (applyBtn) {
                applyBtn.addEventListener('click', () => {
                    this.hideAllModals();
                    Toast.success('Mobile phase configuration applied.');
                    this.addLog(`Mobile phase: A=${this.app.simulation?.state.mobilePhaseA}, B=${this.app.simulation?.state.mobilePhaseB}, pH=${this.app.simulation?.state.mobilePhasePH}`, 'info');
                });
            }
        }

        checkUVCutoff(solventB) {
            const warning = document.getElementById('uv-cutoff-warning');
            const warningText = document.getElementById('uv-cutoff-warning-text');
            const solvent = SOLVENT_PROPERTIES.organic[solventB];
            const wavelength = this.app.simulation?.state.wavelength || 254;

            if (solvent && wavelength <= solvent.uvCutoff) {
                if (warning) warning.classList.remove('hidden');
                if (warningText) warningText.textContent = `Warning: Detector wavelength (${wavelength} nm) is at or below the UV cutoff of ${solvent.name} (${solvent.uvCutoff} nm). High baseline absorbance expected.`;
            } else {
                if (warning) warning.classList.add('hidden');
            }
        }

        updateMobilePhaseSummary() {
            const state = this.app.simulation?.state;
            if (!state) return;

            const aq = SOLVENT_PROPERTIES.aqueous[state.mobilePhaseA];
            const org = SOLVENT_PROPERTIES.organic[state.mobilePhaseB];
            const add = ADDITIVE_INFO[state.additive];

            const el = (id) => document.getElementById(id);
            if (el('mp-summary-a')) el('mp-summary-a').textContent = aq?.name || state.mobilePhaseA;
            if (el('mp-summary-b')) el('mp-summary-b').textContent = org?.name || state.mobilePhaseB;
            if (el('mp-summary-ph')) el('mp-summary-ph').textContent = state.mobilePhasePH.toFixed(1);
            if (el('mp-summary-cutoff')) el('mp-summary-cutoff').textContent = org ? `${org.uvCutoff} nm` : '--';
            if (el('mp-summary-additive')) el('mp-summary-additive').textContent = add?.name || 'None';

            // Calculate mix viscosity at 50:50
            if (org && el('mp-summary-viscosity')) {
                const vis = PhysicsEngine.calculateViscosity(50, state.mobilePhaseB);
                el('mp-summary-viscosity').textContent = `${vis.toFixed(2)} cP`;
            }
        }

        // =========================
        // SAMPLE PREPARATION CONTROLS
        // =========================

        bindSamplePrepControls() {
            this.prepStep = 1;

            // Navigation buttons
            const prevBtn = document.getElementById('prep-prev-btn');
            const nextBtn = document.getElementById('prep-next-btn');
            const finishBtn = document.getElementById('prep-finish-btn');

            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    if (this.prepStep > 1) {
                        this.goToPrepStep(this.prepStep - 1);
                    }
                });
            }
            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    if (this.prepStep < 5) {
                        this.goToPrepStep(this.prepStep + 1);
                    }
                });
            }
            if (finishBtn) {
                finishBtn.addEventListener('click', () => {
                    this.finishSamplePrep();
                });
            }

            // Step 1: Weighing
            const btnTare = document.getElementById('btn-tare');
            const btnWeigh = document.getElementById('btn-weigh');

            if (btnTare) {
                btnTare.addEventListener('click', () => {
                    const display = document.getElementById('balance-display');
                    if (display) display.textContent = '0.0000 g';
                    btnTare.innerHTML = '<i class="fas fa-check"></i> Tared';
                    if (btnWeigh) btnWeigh.disabled = false;
                    Toast.info('Balance tared.');
                });
            }
            if (btnWeigh) {
                btnWeigh.addEventListener('click', () => {
                    const target = parseFloat(document.getElementById('target-weight')?.value || 10);
                    // Simulate realistic weighing with small random deviation
                    const actual = target + (Math.random() - 0.5) * 0.2;
                    const prep = this.app.simulation?.state.samplePrepData;
                    if (prep) prep.actualWeight = actual;

                    // Animate balance
                    const display = document.getElementById('balance-display');
                    const sample = document.getElementById('balance-sample');
                    if (sample) sample.classList.add('visible');

                    let displayed = 0;
                    const interval = setInterval(() => {
                        displayed += actual / 20;
                        if (displayed >= actual) {
                            displayed = actual;
                            clearInterval(interval);
                            btnWeigh.innerHTML = '<i class="fas fa-check"></i> Weighed';
                            const result = document.getElementById('weigh-result');
                            const actualEl = document.getElementById('actual-weight');
                            if (result) result.classList.remove('hidden');
                            if (actualEl) actualEl.textContent = `${actual.toFixed(4)} mg`;
                            if (nextBtn) nextBtn.disabled = false;
                            this.markPrepStepComplete(1);
                        }
                        if (display) display.textContent = `${(displayed / 1000).toFixed(4)} g`;
                    }, 100);
                });
            }

            // Step 2: Dissolution
            const btnDissolve = document.getElementById('btn-dissolve');
            const btnSonicate = document.getElementById('btn-sonicate');
            const btnMakeup = document.getElementById('btn-makeup');

            if (btnDissolve) {
                btnDissolve.addEventListener('click', () => {
                    const liquid = document.getElementById('flask-liquid');
                    if (liquid) liquid.style.height = '50%';
                    btnDissolve.innerHTML = '<i class="fas fa-check"></i> Solvent Added';
                    if (btnSonicate) btnSonicate.disabled = false;
                    Toast.info('Solvent added to flask.');
                });
            }
            if (btnSonicate) {
                btnSonicate.addEventListener('click', () => {
                    btnSonicate.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sonicating...';
                    setTimeout(() => {
                        btnSonicate.innerHTML = '<i class="fas fa-check"></i> Sonicated';
                        if (btnMakeup) btnMakeup.disabled = false;
                        Toast.info('Sonication complete. Sample dissolved.');
                    }, 3000);
                });
            }
            if (btnMakeup) {
                btnMakeup.addEventListener('click', () => {
                    const liquid = document.getElementById('flask-liquid');
                    if (liquid) liquid.style.height = '95%';

                    const prep = this.app.simulation?.state.samplePrepData;
                    const flaskVol = parseFloat(document.getElementById('flask-volume')?.value || 100);
                    if (prep) {
                        prep.flaskVolume = flaskVol;
                        // Stock concentration = weight(mg) / volume(mL) * 1000 = µg/mL
                        prep.stockConcentration = (prep.actualWeight || 10) / flaskVol * 1000;
                    }

                    btnMakeup.innerHTML = '<i class="fas fa-check"></i> Volume Made Up';
                    const stockResult = document.getElementById('stock-result');
                    const stockConc = document.getElementById('stock-concentration');
                    if (stockResult) stockResult.classList.remove('hidden');
                    if (stockConc) stockConc.textContent = `${prep?.stockConcentration?.toFixed(1)} µg/mL`;
                    if (nextBtn) nextBtn.disabled = false;
                    this.markPrepStepComplete(2);
                    Toast.success('Stock solution prepared.');
                });
            }

            // Step 3: Dilution calculator
            const dilV1 = document.getElementById('dilution-v1');
            const dilV2 = document.getElementById('dilution-v2');
            const skipToggle = document.getElementById('skip-dilution-toggle');
            const btnDilute = document.getElementById('btn-prepare-dilution');

            const updateDilCalc = () => {
                const prep = this.app.simulation?.state.samplePrepData;
                const c1 = prep?.stockConcentration || 0;
                const v1 = parseFloat(dilV1?.value || 1);
                const v2 = parseFloat(dilV2?.value || 50);
                const c2 = (c1 * v1) / v2;

                document.getElementById('dilution-c1')?.setAttribute('value', c1.toFixed(1));
                if (document.getElementById('dilution-c1')) document.getElementById('dilution-c1').value = c1.toFixed(1);
                const c2El = document.getElementById('dilution-c2');
                const factorEl = document.getElementById('dilution-factor');
                if (c2El) c2El.textContent = `${c2.toFixed(2)} µg/mL`;
                if (factorEl) factorEl.textContent = `1:${(v2/v1).toFixed(0)}`;
            };

            if (dilV1) dilV1.addEventListener('input', updateDilCalc);
            if (dilV2) dilV2.addEventListener('change', updateDilCalc);

            if (skipToggle) {
                skipToggle.addEventListener('change', (e) => {
                    const prep = this.app.simulation?.state.samplePrepData;
                    if (prep) prep.skipDilution = e.target.checked;
                });
            }

            if (btnDilute) {
                btnDilute.addEventListener('click', () => {
                    const prep = this.app.simulation?.state.samplePrepData;
                    if (prep) {
                        if (prep.skipDilution) {
                            prep.finalConcentration = prep.stockConcentration;
                        } else {
                            const v1 = parseFloat(dilV1?.value || 1);
                            const v2 = parseFloat(dilV2?.value || 50);
                            prep.finalConcentration = (prep.stockConcentration || 0) * v1 / v2;
                        }
                    }
                    btnDilute.innerHTML = '<i class="fas fa-check"></i> Dilution Prepared';
                    if (nextBtn) nextBtn.disabled = false;
                    this.markPrepStepComplete(3);
                    Toast.success(`Working solution: ${prep?.finalConcentration?.toFixed(2)} µg/mL`);
                });
            }

            // Step 4: Filtration
            const btnFilter = document.getElementById('btn-filter');
            if (btnFilter) {
                btnFilter.addEventListener('click', () => {
                    btnFilter.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Filtering...';
                    const plunger = document.getElementById('syringe-plunger');
                    const liquid = document.getElementById('syringe-liquid');
                    if (plunger) plunger.style.top = '80px';
                    if (liquid) liquid.style.height = '10%';

                    setTimeout(() => {
                        btnFilter.innerHTML = '<i class="fas fa-check"></i> Filtered';
                        const filterStatus = document.getElementById('filter-status');
                        if (filterStatus) filterStatus.classList.remove('hidden');
                        if (nextBtn) nextBtn.disabled = false;
                        this.markPrepStepComplete(4);
                        Toast.success('Sample filtered through 0.45 µm PVDF.');
                    }, 2500);
                });
            }

            // Step 5: Vial loading
            // Generate tray positions
            const traySelector = document.getElementById('tray-position-selector');
            const trayGrid = document.getElementById('vial-tray-grid');
            if (traySelector) {
                for (let i = 1; i <= 12; i++) {
                    const btn = document.createElement('button');
                    btn.className = 'tray-pos-btn';
                    btn.textContent = i;
                    btn.dataset.position = i;
                    if (i === 1) btn.classList.add('selected');
                    btn.addEventListener('click', () => {
                        document.querySelectorAll('.tray-pos-btn').forEach(b => b.classList.remove('selected'));
                        btn.classList.add('selected');
                        const prep = this.app.simulation?.state.samplePrepData;
                        if (prep) prep.trayPosition = i;
                    });
                    traySelector.appendChild(btn);
                }
            }
            // Generate visual tray grid
            if (trayGrid) {
                for (let i = 1; i <= 12; i++) {
                    const pos = document.createElement('div');
                    pos.className = 'tray-position';
                    pos.textContent = i;
                    pos.dataset.trayPos = i;
                    trayGrid.appendChild(pos);
                }
            }

            const btnLoadVial = document.getElementById('btn-load-vial');
            const btnPlaceVial = document.getElementById('btn-place-vial');
            const vialFillInput = document.getElementById('vial-fill-input');
            const vialFillNumber = document.getElementById('vial-fill-number');

            if (vialFillInput && vialFillNumber) {
                vialFillInput.addEventListener('input', (e) => {
                    vialFillNumber.value = e.target.value;
                });
                vialFillNumber.addEventListener('change', (e) => {
                    vialFillInput.value = e.target.value;
                });
            }

            if (btnLoadVial) {
                btnLoadVial.addEventListener('click', () => {
                    const vialLiquid = document.getElementById('vial-liquid-fill');
                    const fillVol = parseInt(vialFillInput?.value || 500);
                    const fillPercent = Math.min(85, (fillVol / 1500) * 85);
                    if (vialLiquid) vialLiquid.style.height = `${fillPercent}%`;
                    btnLoadVial.innerHTML = '<i class="fas fa-check"></i> Vial Filled & Capped';
                    if (btnPlaceVial) btnPlaceVial.disabled = false;
                    Toast.info('Vial filled and capped.');
                });
            }

            if (btnPlaceVial) {
                btnPlaceVial.addEventListener('click', () => {
                    const prep = this.app.simulation?.state.samplePrepData;
                    const pos = prep?.trayPosition || 1;
                    const trayPos = document.querySelector(`[data-tray-pos="${pos}"]`);
                    if (trayPos) trayPos.classList.add('filled');
                    btnPlaceVial.innerHTML = '<i class="fas fa-check"></i> Placed in Tray';

                    if (finishBtn) {
                        finishBtn.classList.remove('hidden');
                        if (nextBtn) nextBtn.classList.add('hidden');
                    }
                    this.markPrepStepComplete(5);
                    Toast.success(`Vial placed in autosampler position ${pos}.`);
                });
            }
        }

        goToPrepStep(step) {
            this.prepStep = step;
            // Update step indicators
            document.querySelectorAll('.prep-step').forEach((el) => {
                const stepNum = parseInt(el.dataset.prepStep);
                el.classList.remove('active');
                if (stepNum === step) el.classList.add('active');
            });
            // Update panels
            for (let i = 1; i <= 5; i++) {
                const panel = document.getElementById(`prep-step-${i}`);
                if (panel) {
                    panel.classList.remove('active');
                    if (i === step) panel.classList.add('active');
                }
            }
            // Update nav
            const prevBtn = document.getElementById('prep-prev-btn');
            const nextBtn = document.getElementById('prep-next-btn');
            const finishBtn = document.getElementById('prep-finish-btn');
            if (prevBtn) prevBtn.disabled = step === 1;
            if (nextBtn) nextBtn.disabled = true; // Require action to proceed
            if (step === 5) {
                if (nextBtn) nextBtn.classList.add('hidden');
            } else {
                if (nextBtn) nextBtn.classList.remove('hidden');
                if (finishBtn) finishBtn.classList.add('hidden');
            }

            // Auto-update dilution calculator when reaching step 3
            if (step === 3) {
                const c1 = this.app.simulation?.state.samplePrepData?.stockConcentration || 0;
                const c1El = document.getElementById('dilution-c1');
                if (c1El) c1El.value = c1.toFixed(1);
            }
        }

        markPrepStepComplete(step) {
            const stepEl = document.querySelector(`[data-prep-step="${step}"]`);
            if (stepEl) stepEl.classList.add('completed');
            // Mark connector
            const connectors = document.querySelectorAll('.prep-connector');
            if (step <= connectors.length) {
                connectors[step - 1]?.classList.add('completed');
            }
        }

        finishSamplePrep() {
            const prep = this.app.simulation?.state.samplePrepData;
            if (prep) {
                this.app.simulation.state.samplePrepComplete = true;
                // Feed final concentration into simulation
                const finalConc = prep.finalConcentration || prep.stockConcentration || 100;
                this.app.simulation.setParameter('concentration', finalConc);
            }
            this.hideAllModals();
            Toast.success('Sample preparation complete! Concentration updated.');
            this.addLog(`Sample prep complete. Final concentration: ${this.app.simulation?.state.concentration?.toFixed(2)} µg/mL`, 'success');
        }

        // =========================
        // MODAL MANAGEMENT
        // =========================

        showModal(modalId) {
            const modal = document.getElementById(modalId);
            if (!modal) return;

            this.currentModal = modalId;

            // Show backdrop
            if (this.elements.backdrop) {
                this.elements.backdrop.classList.remove('hidden');
            }

            // Show modal with animation
            modal.classList.remove('hidden');
            requestAnimationFrame(() => {
                modal.classList.add('visible');
            });

            // Play any videos in the modal
            const video = modal.querySelector('video');
            if (video) {
                video.play().catch(() => { });
            }
        }

        hideAllModals() {
            this.currentModal = null;

            // Hide backdrop
            if (this.elements.backdrop) {
                this.elements.backdrop.classList.add('hidden');
            }

            // Hide all modals
            this.elements.modals.forEach(modal => {
                modal.classList.remove('visible');
                setTimeout(() => {
                    modal.classList.add('hidden');
                }, 300);

                // Pause any videos
                const video = modal.querySelector('video');
                if (video) {
                    video.pause();
                }
            });
        }

        showConfirmation() {
            const params = this.app.simulation?.getParameters();
            if (!params) return;

            // Build confirmation content
            const container = this.elements.confirmationList;
            if (!container) return;

            container.innerHTML = `
                <div class="param-item">
                    <span class="param-label">Flow Rate</span>
                    <span class="param-value">${params.flowRate.toFixed(2)} mL/min</span>
                </div>
                <div class="param-item">
                    <span class="param-label">Column Temp</span>
                    <span class="param-value">${params.columnTemp}°C</span>
                </div>
                <div class="param-item">
                    <span class="param-label">Wavelength</span>
                    <span class="param-value">${params.wavelength} nm</span>
                </div>
                <div class="param-item">
                    <span class="param-label">Injection Vol</span>
                    <span class="param-value">${params.injectionVolume} µL</span>
                </div>
                <div class="param-item">
                    <span class="param-label">Column</span>
                    <span class="param-value">${params.columnType}</span>
                </div>
                <div class="param-item">
                    <span class="param-label">Sample</span>
                    <span class="param-value">${params.sample}</span>
                </div>
            `;

            this.showModal('confirmation-modal');
        }

        // =========================
        // VIEW MANAGEMENT
        // =========================

        switchView(viewName) {
            if (viewName === 'main') {
                this.elements.mainView?.classList.add('active');
                this.elements.screenView?.classList.remove('active');
            } else if (viewName === 'screen') {
                this.elements.mainView?.classList.remove('active');
                this.elements.screenView?.classList.add('active');
            }
        }

        toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    Toast.error('Fullscreen not available');
                });
            } else {
                document.exitFullscreen();
            }
        }

        // =========================
        // DISPLAY UPDATES
        // =========================

        update(event) {
            const state = event.payload;

            switch (event.type) {
                case 'param_change':
                    this.handleParamChange(state);
                    break;

                case 'data_update':
                    this.updateScreenReadouts(state);
                    this.updateChart(state.chromatogram);
                    break;

                case 'instant_data_update':
                    this.updateScreenReadouts(state);
                    this.animateChart(state.chromatogram);
                    break;

                case 'pressure_update':
                    this.updatePressureGauge(state.currentPressure);
                    break;

                case 'run_start':
                    this.handleRunStart(state);
                    break;

                case 'run_complete':
                    this.handleRunComplete(state);
                    break;

                case 'run_stop':
                    this.handleRunStop(state);
                    break;

                case 'run_pause':
                    this.handleRunPause(state);
                    break;

                case 'reset':
                    this.handleReset(state);
                    break;

                case 'toggle_standard':
                    this.handleStandardToggle(state);
                    break;

                case 'sst_complete':
                    this.showSSTReport(state.sstResults);
                    break;

                case 'fault_triggered':
                    this.handleFaultTriggered(state);
                    break;
            }
        }

        handleParamChange(state) {
            // Update live parameter displays
            if (this.elements.liveFlowRate) {
                this.elements.liveFlowRate.textContent = state.flowRate.toFixed(3);
            }
            if (this.elements.liveColumnTemp) {
                this.elements.liveColumnTemp.textContent = state.columnTemp;
            }
            if (this.elements.liveWavelength) {
                this.elements.liveWavelength.textContent = state.wavelength;
            }
            if (this.elements.liveInjectionVol) {
                this.elements.liveInjectionVol.textContent = state.injectionVolume;
            }
            if (this.elements.sampleName) {
                this.elements.sampleName.textContent = state.sample;
            }
            if (this.elements.methodName) {
                this.elements.methodName.textContent = state.sample === 'Mixture' ? 'Multi-Component Analysis' : `${state.sample} Assay`;
            }

            // Update gradient charts if gradient changed
            if (state.lastChange?.key === 'gradientProgram') {
                this.updateGradientCharts();
            }
        }

        updateScreenReadouts(state) {
            // Flow rate
            if (this.elements.screenFlowRate) {
                this.elements.screenFlowRate.textContent = state.flowRate.toFixed(3);
            }

            // Pressure
            this.updatePressureGauge(state.currentPressure);

            // Temperature
            if (this.elements.screenColumnTemp) {
                this.elements.screenColumnTemp.textContent = state.columnTemp;
            }
            this.updateThermometer(state.columnTemp);

            // Pump channels
            this.updatePumpChannels(state.currentPercentB);

            // Elapsed time
            if (this.elements.elapsedTime) {
                this.elements.elapsedTime.textContent = Utils.formatTime(state.elapsedAnalysisTime);
            }

            // Progress bar
            if (this.elements.timerProgressFill) {
                const totalDuration = this.app.simulation?.getAnalysisDuration() * 60 || 720;
                const progress = (state.elapsedAnalysisTime / totalDuration) * 100;
                this.elements.timerProgressFill.style.width = `${progress}%`;
            }
        }

        updatePressureGauge(pressure) {
            // Text display
            if (this.elements.screenPressure) {
                this.elements.screenPressure.textContent = pressure.toFixed(1);
            }

            // Needle rotation (-90° to 90°)
            if (this.elements.gaugeNeedle) {
                const rotation = -90 + (pressure / CONFIG.maxPressure) * 180;
                this.elements.gaugeNeedle.setAttribute('transform', `rotate(${rotation}, 100, 100)`);
            }

            // Arc dasharray
            if (this.elements.gaugeValueArc) {
                const circumference = 251; // Half circle
                const filled = (pressure / CONFIG.maxPressure) * circumference;
                this.elements.gaugeValueArc.style.strokeDasharray = `${filled} ${circumference}`;
            }

            // Update quick stats
            if (this.elements.qsPressure) {
                this.elements.qsPressure.textContent = `${pressure.toFixed(0)} bar`;
            }
        }

        updateThermometer(temp) {
            // Fill level (20-80°C range)
            if (this.elements.thermoFillLevel) {
                const percent = ((temp - 20) / (80 - 20)) * 100;
                this.elements.thermoFillLevel.style.height = `${percent}%`;
            }

            // Update quick stats
            if (this.elements.qsTemp) {
                this.elements.qsTemp.textContent = `${temp}°C`;
            }
        }

        updatePumpChannels(percentB) {
            const percentA = 100 - percentB;

            if (this.elements.pumpABar) {
                this.elements.pumpABar.style.width = `${percentA}%`;
            }
            if (this.elements.pumpBBar) {
                this.elements.pumpBBar.style.width = `${percentB}%`;
            }
            if (this.elements.pumpAPercent) {
                this.elements.pumpAPercent.textContent = `${percentA.toFixed(0)}%`;
            }
            if (this.elements.pumpBPercent) {
                this.elements.pumpBPercent.textContent = `${percentB.toFixed(0)}%`;
            }
        }

        updateChart(chromatogram) {
            if (!this.charts.main) return;

            this.charts.main.data.datasets[0].data = chromatogram.dataA;
            this.charts.main.options.scales.x.max = this.app.simulation?.getAnalysisDuration() || 15;
            this.charts.main.update('none');
        }

        animateChart(chromatogram) {
            if (!this.charts.main) return;

            this.clearChart();
            this.charts.main.options.scales.x.max = this.app.simulation?.getAnalysisDuration() || 15;
            this.charts.main.update('none');

            const totalPoints = chromatogram.dataA.length;
            let animatedData = [];

            const target = { points: 0 };
            gsap.to(target, {
                points: totalPoints,
                duration: 1.5,
                ease: "power1.inOut",
                onUpdate: () => {
                    animatedData = chromatogram.dataA.slice(0, Math.ceil(target.points));
                    this.charts.main.data.datasets[0].data = animatedData;
                    this.charts.main.update('none');
                }
            });
        }

        clearChart() {
            if (this.charts.main) {
                this.charts.main.data.datasets[0].data = [];
                this.charts.main.data.datasets[1].hidden = true;
                this.charts.main.peakAnnotations = [];
                this.charts.main.update('none');
            }
        }

        handleRunStart(state) {
            this.playSound('pumpStart');
            if (!state.instantMode) {
                this.playSound('pumpLoop');
            }

            // Update status
            if (this.elements.screenTitle) {
                this.elements.screenTitle.textContent = 'Acquiring...';
            }
            if (this.elements.runStatusIndicator) {
                this.elements.runStatusIndicator.classList.add('running');
            }

            // Update buttons
            if (this.elements.buttons.run) this.elements.buttons.run.disabled = true;
            if (this.elements.buttons.stop) this.elements.buttons.stop.disabled = false;
            if (this.elements.buttons.pause) this.elements.buttons.pause.disabled = false;

            // Start flow animation
            if (this.elements.flowAnimation) {
                this.elements.flowAnimation.classList.remove('stopped');
            }

            this.addLog(`Analysis started: ${state.sample}`, 'info');
        }

        handleRunComplete(state) {
            this.stopSound('pumpLoop');
            this.playSound('analysisComplete');

            // Update status
            if (this.elements.screenTitle) {
                this.elements.screenTitle.textContent = 'Complete';
            }
            if (this.elements.runStatusIndicator) {
                this.elements.runStatusIndicator.classList.remove('running');
            }

            // Update buttons
            if (this.elements.buttons.run) this.elements.buttons.run.disabled = false;
            if (this.elements.buttons.stop) this.elements.buttons.stop.disabled = true;
            if (this.elements.buttons.pause) this.elements.buttons.pause.disabled = true;
            if (this.elements.buttons.sstReport) this.elements.buttons.sstReport.disabled = false;

            // Stop flow animation
            if (this.elements.flowAnimation) {
                this.elements.flowAnimation.classList.add('stopped');
            }

            this.addLog('Analysis complete', 'success');

            // Store peak annotations on chart for the plugin
            if (this.charts.main && state.peaks) {
                this.charts.main.peakAnnotations = state.peaks.map(p => ({
                    name: p.name,
                    rt: p.rt,
                    height: p.height,
                    area: p.area,
                    sigma: p.sigma,
                    peakWidth: p.peakWidth
                }));
                this.charts.main.update('none');
            }

            // Show results
            this.showResults(state);
        }

        handleRunStop(state) {
            this.stopSound('pumpLoop');
            this.playSound('error');

            // Update status
            if (this.elements.screenTitle) {
                this.elements.screenTitle.textContent = 'Stopped';
            }
            if (this.elements.runStatusIndicator) {
                this.elements.runStatusIndicator.classList.remove('running');
                this.elements.runStatusIndicator.classList.add('error');
            }

            // Update buttons
            if (this.elements.buttons.run) this.elements.buttons.run.disabled = false;
            if (this.elements.buttons.stop) this.elements.buttons.stop.disabled = true;
            if (this.elements.buttons.pause) this.elements.buttons.pause.disabled = true;

            // Stop flow animation
            if (this.elements.flowAnimation) {
                this.elements.flowAnimation.classList.add('stopped');
            }

            this.addLog('Analysis stopped by user', 'warning');
        }

        handleRunPause(state) {
            this.stopSound('pumpLoop');

            if (this.elements.screenTitle) {
                this.elements.screenTitle.textContent = state.isPaused ? 'Paused' : 'Acquiring...';
            }

            if (state.isPaused) {
                this.addLog('Analysis paused', 'info');
            } else {
                this.playSound('pumpLoop');
                this.addLog('Analysis resumed', 'info');
            }
        }

        handleReset(state) {
            this.stopSound('pumpLoop');
            this.clearChart();

            // Reset status displays
            if (this.elements.screenTitle) {
                this.elements.screenTitle.textContent = 'Ready';
            }
            if (this.elements.runStatusIndicator) {
                this.elements.runStatusIndicator.classList.remove('running', 'error');
            }

            // Reset buttons
            if (this.elements.buttons.run) this.elements.buttons.run.disabled = true;
            if (this.elements.buttons.stop) this.elements.buttons.stop.disabled = true;
            if (this.elements.buttons.pause) this.elements.buttons.pause.disabled = true;
            if (this.elements.buttons.sstReport) this.elements.buttons.sstReport.disabled = true;

            // Reset startup wizard
            this.resetWizard();

            // Switch to main view
            this.switchView('main');

            this.clearLog();
            this.addLog('System reset. Complete startup wizard to begin.', 'info');
        }

        handleStandardToggle(state) {
            if (this.charts.main) {
                const standardData = this.app.simulation?.standardData?.dataA || [];
                this.charts.main.data.datasets[1].data = standardData;
                this.charts.main.data.datasets[1].hidden = !state.showStandard;
                this.charts.main.update('none');
            }

            if (this.elements.buttons.overlayStandard) {
                this.elements.buttons.overlayStandard.classList.toggle('active', state.showStandard);
            }

            this.addLog(state.showStandard ? 'Standard overlay enabled' : 'Standard overlay disabled', 'info');
        }

        handleFaultTriggered(state) {
            const fault = CONFIG.faults[state.currentFault];
            if (fault && state.currentFault !== 'none') {
                Toast.warning(`Fault detected: ${fault.name}`);
                this.addLog(`⚠️ Fault condition: ${fault.name}`, 'error');

                if (fault.symptoms) {
                    fault.symptoms.forEach(symptom => {
                        this.addLog(`  → ${symptom}`, 'warning');
                    });
                }
            }
        }

        resetWizard() {
            this.wizardStep = 1;

            // Reset step indicators
            this.elements.wizardSteps.forEach(el => {
                el.classList.remove('active', 'completed');
            });
            this.elements.wizardSteps[0]?.classList.add('active');

            // Reset connectors
            this.elements.wizardConnectors.forEach(el => {
                el.classList.remove('completed');
            });

            // Reset panels
            this.elements.wizardPanels.forEach((panel, index) => {
                panel.classList.remove('active');
                if (index === 0) panel.classList.add('active');
            });

            // Reset buttons in wizard
            const btnRefill = document.getElementById('btn-refill');
            const btnDegas = document.getElementById('btn-degas');
            const btnPrime = document.getElementById('btn-prime');
            const btnEquilibrate = document.getElementById('btn-equilibrate');

            if (btnRefill) {
                btnRefill.disabled = false;
                btnRefill.innerHTML = '<i class="fas fa-fill-drip"></i> Fill Solvent Bottles';
            }
            if (btnDegas) {
                btnDegas.disabled = true;
                btnDegas.innerHTML = '<i class="fas fa-wind"></i> Degas with Helium';
            }
            if (btnPrime) {
                btnPrime.disabled = true;
                btnPrime.innerHTML = '<i class="fas fa-play"></i> Start Purge (5.0 mL/min)';
            }
            if (btnEquilibrate) {
                btnEquilibrate.disabled = false;
                btnEquilibrate.innerHTML = '<i class="fas fa-play"></i> Start Equilibration';
            }

            // Reset status indicators
            ['status-bottle-a', 'status-bottle-b', 'status-degas'].forEach(id => {
                const el = document.getElementById(id);
                if (el) {
                    el.textContent = id.includes('degas') ? 'Not Started' : 'Empty';
                    el.className = 'status-value pending';
                }
            });

            // Reset progress bars
            const purgeProgress = document.getElementById('purge-progress-fill');
            const purgeText = document.getElementById('purge-progress-text');
            if (purgeProgress) purgeProgress.style.width = '0%';
            if (purgeText) purgeText.textContent = '0%';

            // Reset overlays
            ['overlay-step-1', 'overlay-step-2', 'overlay-step-3'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.remove('hidden');
            });

            // Reset startup button
            if (this.elements.setupTrigger) {
                this.elements.setupTrigger.classList.remove('ready');
                const text = this.elements.setupTrigger.querySelector('.startup-text');
                if (text) text.textContent = 'System Startup';
                const progress = this.elements.setupTrigger.querySelector('.startup-progress-fill');
                if (progress) progress.style.width = '0%';
            }

            // Reset status chip
            if (this.elements.systemStatusChip) {
                const dot = this.elements.systemStatusChip.querySelector('.status-dot');
                const text = this.elements.systemStatusChip.querySelector('span:last-child');
                if (dot) dot.classList.remove('online');
                if (text) text.textContent = 'System Offline';
            }

            // Reset wizard navigation
            if (this.elements.buttons.wizardPrev) this.elements.buttons.wizardPrev.disabled = true;
            if (this.elements.buttons.wizardNext) {
                this.elements.buttons.wizardNext.disabled = true;
                this.elements.buttons.wizardNext.classList.remove('hidden');
            }
            if (this.elements.buttons.wizardFinish) this.elements.buttons.wizardFinish.classList.add('hidden');
        }

        showResults(state) {
            const peaks = state.peaks || [];

            // Calculate total area for %Area
            const totalArea = peaks.reduce((sum, p) => sum + (p.area || p.height * p.peakWidth * 2.507), 0);

            // Reference RT for RRT (first peak)
            const sortedPeaks = [...peaks].sort((a, b) => a.rt - b.rt);
            const refRT = sortedPeaks.length > 0 ? sortedPeaks[0].rt : 1;

            // Update summary
            if (this.elements.resultRuntime) {
                this.elements.resultRuntime.textContent = Utils.formatTime(state.elapsedAnalysisTime);
            }
            if (this.elements.resultPeaks) {
                this.elements.resultPeaks.textContent = peaks.length;
            }
            if (this.elements.resultStatus) {
                this.elements.resultStatus.textContent = 'Pass';
                this.elements.resultStatus.parentElement.querySelector('i').className = 'fas fa-check-circle';
            }

            // Build enhanced results table
            const container = this.elements.resultsTableContainer;
            if (container) {
                let tableHTML = `
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Compound</th>
                                <th>RT (min)</th>
                                <th>RRT</th>
                                <th>Area</th>
                                <th>%Area</th>
                                <th>Height</th>
                                <th>Width</th>
                                <th>Asym.</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                sortedPeaks.forEach((peak, index) => {
                    const area = peak.area || peak.height * peak.peakWidth * 2.507;
                    const pctArea = totalArea > 0 ? (area / totalArea * 100) : 0;
                    const rrt = (peak.rt / refRT).toFixed(2);

                    tableHTML += `
                        <tr>
                            <td>${index + 1}</td>
                            <td><strong>${peak.name || `Peak ${index + 1}`}</strong></td>
                            <td>${peak.rt.toFixed(3)}</td>
                            <td>${rrt}</td>
                            <td>${area.toFixed(0)}</td>
                            <td>${pctArea.toFixed(1)}%</td>
                            <td>${peak.height.toFixed(1)}</td>
                            <td>${peak.peakWidth.toFixed(3)}</td>
                            <td>${(peak.asymmetry || 1.0).toFixed(2)}</td>
                        </tr>
                    `;
                });

                tableHTML += '</tbody></table>';
                container.innerHTML = tableHTML;
            }

            this.showModal('results-modal');
        }

        showSSTReport(sstResults) {
            // Update header info
            if (this.elements.sstMethodName) {
                const sample = this.app.simulation?.state.sample || 'Unknown';
                this.elements.sstMethodName.textContent = sample === 'Mixture' ? 'Multi-Component Analysis' : `${sample} Assay`;
            }
            if (this.elements.sstDate) {
                this.elements.sstDate.textContent = new Date().toLocaleDateString();
            }

            // Build SST table
            const tbody = this.elements.sstTableBody;
            if (tbody) {
                tbody.innerHTML = '';

                let allPass = true;
                sstResults.forEach(peak => {
                    const rowPass = peak.R_pass && peak.T_pass && peak.N_pass;
                    if (!rowPass) allPass = false;

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><strong>${peak.name}</strong></td>
                        <td>${peak.rt.toFixed(3)}</td>
                        <td class="${peak.R_pass ? 'sst-pass' : 'sst-fail'}">${peak.R}</td>
                        <td class="${peak.T_pass ? 'sst-pass' : 'sst-fail'}">${peak.T.toFixed(2)}</td>
                        <td class="${peak.N_pass ? 'sst-pass' : 'sst-fail'}">${peak.N.toLocaleString()}</td>
                        <td class="${rowPass ? 'sst-pass' : 'sst-fail'}">${rowPass ? '✓ PASS' : '✗ FAIL'}</td>
                    `;
                    tbody.appendChild(row);
                });

                // Update verdict
                if (this.elements.sstVerdict) {
                    this.elements.sstVerdict.className = `sst-verdict ${allPass ? 'pass' : 'fail'}`;
                    this.elements.sstVerdict.innerHTML = allPass
                        ? '<i class="fas fa-check-circle"></i> SYSTEM SUITABILITY: PASS'
                        : '<i class="fas fa-times-circle"></i> SYSTEM SUITABILITY: FAIL';
                }
            }

            this.showModal('sst-modal');
        }

        updateQuickStats() {
            if (this.elements.qsSolventLevel) {
                this.elements.qsSolventLevel.textContent = '100%';
            }
            if (this.elements.qsPressure) {
                this.elements.qsPressure.textContent = '0 bar';
            }
            if (this.elements.qsTemp) {
                const temp = this.app.simulation?.state.columnTemp || 30;
                this.elements.qsTemp.textContent = `${temp}°C`;
            }
            if (this.elements.qsRuntime) {
                this.elements.qsRuntime.textContent = '0:00';
            }
        }

        // =========================
        // EXPORT FUNCTIONS
        // =========================

        exportChartData() {
            const data = this.charts.main?.data.datasets[0].data || [];
            if (data.length === 0) {
                Toast.warning('No data to export');
                return;
            }

            let csv = 'Time (min),Absorbance (mAU)\n';
            data.forEach(point => {
                csv += `${point.x.toFixed(4)},${point.y.toFixed(4)}\n`;
            });

            this.downloadFile(csv, 'chromatogram_data.csv', 'text/csv');
            Toast.success('Data exported successfully');
        }

        exportResults() {
            const peaks = this.app.simulation?.liveData?.peaks || [];
            if (peaks.length === 0) {
                Toast.warning('No results to export');
                return;
            }

            let csv = 'Peak Name,Retention Time (min),Area,Height,Peak Width (min)\n';
            peaks.sort((a, b) => a.rt - b.rt).forEach(peak => {
                const area = peak.area || peak.height * peak.peakWidth * 2.507;
                csv += `${peak.name},${peak.rt.toFixed(4)},${area.toFixed(2)},${peak.height.toFixed(2)},${peak.peakWidth.toFixed(4)}\n`;
            });

            this.downloadFile(csv, 'analysis_results.csv', 'text/csv');
            Toast.success('Results exported successfully');
        }

        exportSST() {
            const results = this.app.simulation?.state.sstResults || [];
            if (results.length === 0) {
                Toast.warning('No SST data to export');
                return;
            }

            let csv = 'Peak,RT (min),Resolution,Tailing Factor,Plate Count,Status\n';
            results.forEach(peak => {
                const status = (peak.R_pass && peak.T_pass && peak.N_pass) ? 'PASS' : 'FAIL';
                csv += `${peak.name},${peak.rt.toFixed(4)},${peak.R},${peak.T.toFixed(2)},${peak.N},${status}\n`;
            });

            this.downloadFile(csv, 'sst_report.csv', 'text/csv');
            Toast.success('SST report exported successfully');
        }

        takeScreenshot() {
            const canvas = document.getElementById('hplc-chart');
            if (!canvas) {
                Toast.warning('No chart to capture');
                return;
            }

            const link = document.createElement('a');
            link.download = `chromatogram_${Date.now()}.png`;
            link.href = canvas.toDataURL('image/png');
            link.click();

            Toast.success('Screenshot saved');
        }

        downloadFile(content, filename, mimeType) {
            const blob = new Blob([content], { type: mimeType });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.click();
            URL.revokeObjectURL(url);
        }

        // =========================
        // AUDIO MANAGEMENT
        // =========================

        playSound(soundName) {
            if (!this.app.soundEnabled) return;

            const sound = this.audio[soundName];
            if (sound) {
                sound.currentTime = 0;
                sound.play().catch(() => { });
            }
        }

        stopSound(soundName) {
            const sound = this.audio[soundName];
            if (sound) {
                sound.pause();
                sound.currentTime = 0;
            }
        }

        // =========================
        // LOGGING
        // =========================

        addLog(message, type = 'info') {
            const container = this.elements.logContent;
            if (!container) return;

            const timestamp = new Date().toLocaleTimeString();
            const entry = document.createElement('div');
            entry.className = `log-entry ${type}`;
            entry.innerHTML = `
                <span class="log-timestamp">[${timestamp}]</span>
                <span class="log-message">${message}</span>
            `;

            container.appendChild(entry);
            container.scrollTop = container.scrollHeight;
        }

        clearLog() {
            if (this.elements.logContent) {
                this.elements.logContent.innerHTML = '';
            }
        }

        // =========================
        // CLOCK
        // =========================

        startClock() {
            const updateClock = () => {
                if (this.elements.systemTime) {
                    this.elements.systemTime.textContent = new Date().toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                }
            };

            updateClock();
            setInterval(updateClock, 1000);
        }
    }

    // ========================================================================
    // SIMULATION CLASS - Physics Engine
    // ========================================================================

    class Simulation {
        constructor(ui, app) {
            this.ui = ui;
            this.app = app;
            this.state = {};
            this.liveData = null;
            this.standardData = null;
            this.animationFrameId = null;
            this.pressureInterval = null;
            this.startTime = 0;
            this.difficulty = 'beginner';

            this.reset();
        }

        reset() {
            // Cancel any running simulation
            if (this.state && this.state.runInProgress) {
                this.stop();
            }

            // Initialize state
            this.state = {
                // Method parameters
                flowRate: 1.0,
                columnTemp: 30,
                wavelength: 254,
                injectionVolume: 20,
                concentration: 100,
                columnType: 'C18',
                sample: 'Mixture',
                gradientProgram: [
                    { time: 0, percentB: 10, curve: 'linear' },
                    { time: 8, percentB: 90, curve: 'linear' },
                    { time: 10, percentB: 90, curve: 'linear' },
                    { time: 10.1, percentB: 10, curve: 'step' }
                ],

                // Runtime state
                currentPercentB: 10,
                currentPressure: 0,
                elapsedAnalysisTime: 0,
                runInProgress: false,
                isPaused: false,
                instantMode: false,

                // System state
                isSystemReady: false,
                solventsReady: false,
                linesPrimed: false,
                columnReady: false,
                purgeValveOpen: false,

                // Display state
                showStandard: false,
                lastChange: {},
                sstResults: null,

                // Fault state
                currentFault: 'none',
                faultActive: false,

                // Mobile phase configuration (Industry-grade)
                mobilePhaseA: 'water',
                mobilePhaseB: 'acetonitrile',
                mobilePhaseGrade: 'hplc',
                mobilePhasePH: 7.0,
                bufferConcentration: 20,
                additive: 'none',
                additiveConcentration: 0.1,

                // Sample preparation state
                samplePrepComplete: false,
                samplePrepData: {
                    targetWeight: 10.0,
                    actualWeight: null,
                    material: 'reference_standard',
                    flaskVolume: 100,
                    dissolutionSolvent: 'mobile_phase',
                    stockConcentration: null,
                    dilutionV1: 1.0,
                    dilutionV2: 50,
                    finalConcentration: null,
                    skipDilution: false,
                    filterPoreSize: 0.45,
                    filterMaterial: 'pvdf',
                    vialType: '2ml_clear',
                    vialFillVolume: 500,
                    trayPosition: 1
                }
            };

            // Precalculate standard data
            this.precalculateStandardData();

            // Notify UI
            setTimeout(() => {
                this.notifyUI({ type: 'reset', payload: this.state });
            }, 50);
        }

        setDifficulty(level) {
            this.difficulty = level;
        }

        setParameter(key, value) {
            if (this.state[key] !== value) {
                this.state[key] = value;
                this.state.lastChange = { key, value };
                this.notifyUI({ type: 'param_change', payload: this.state });
            }
        }

        setFault(faultType) {
            this.state.currentFault = faultType;
            this.state.faultActive = faultType !== 'none';

            if (faultType !== 'none') {
                this.notifyUI({ type: 'fault_triggered', payload: this.state });
            }
        }

        getParameters() {
            return { ...this.state };
        }

        getAnalysisDuration(program = null) {
            const gp = program || this.state.gradientProgram;
            if (!gp || gp.length === 0) return 12;
            return Math.max(10, gp[gp.length - 1].time + 2);
        }

        getCurrentPercentB(timeInMinutes) {
            const program = this.state.gradientProgram;
            if (!program || program.length === 0) return 50;

            // Before first point
            if (timeInMinutes <= program[0].time) {
                return program[0].percentB;
            }

            // After last point
            if (timeInMinutes >= program[program.length - 1].time) {
                return program[program.length - 1].percentB;
            }

            // Find the two bracketing points
            for (let i = 1; i < program.length; i++) {
                if (program[i].time >= timeInMinutes) {
                    const prev = program[i - 1];
                    const next = program[i];

                    // Step curve
                    if (next.curve === 'step') {
                        return prev.percentB;
                    }

                    // Linear interpolation
                    const fraction = (timeInMinutes - prev.time) / (next.time - prev.time);
                    return prev.percentB + fraction * (next.percentB - prev.percentB);
                }
            }

            return program[program.length - 1].percentB;
        }

        precalculateStandardData() {
            this.standardData = this.generateChromatogramData({
                flowRate: CONFIG.standardFlowRate,
                columnTemp: CONFIG.standardTemp,
                wavelength: CONFIG.standardWavelength,
                columnType: 'C18',
                sample: 'Mixture',
                gradientProgram: this.state.gradientProgram,
                injectionVolume: 20,
                concentration: 100,
                currentFault: 'none'
            });
        }

        generateChromatogramData(params) {
            const {
                flowRate,
                columnTemp,
                columnType,
                sample,
                gradientProgram,
                wavelength,
                injectionVolume,
                concentration,
                currentFault = 'none'
            } = params;

            // Get compounds to analyze
            let compounds;
            if (sample === 'Mixture') {
                compounds = Object.values(COMPOUND_LIBRARY).filter(c => !c.isImpurity);
            } else if (sample === 'Unknown') {
                // Random compound for unknown
                const allCompounds = Object.values(COMPOUND_LIBRARY).filter(c => !c.isImpurity);
                compounds = [allCompounds[Math.floor(Math.random() * allCompounds.length)]];
            } else if (COMPOUND_LIBRARY[sample]) {
                compounds = [COMPOUND_LIBRARY[sample]];
            } else {
                compounds = [];
            }

            // Get fault parameters
            const fault = CONFIG.faults[currentFault];
            const column = CONFIG.columns[columnType];

            // Calculate theoretical plates
            const N = PhysicsEngine.calculateTheoreticalPlates(flowRate, columnType);
            const effectiveN = N * (1 - (fault?.efficiencyLoss || 0));

            // Create a getPercentBAtTime helper bound to this gradient program
            const getPercentBAtTime = (timeInMinutes) => {
                return this.getCurrentPercentB(timeInMinutes);
            };

            // Calculate peaks
            const calculatedPeaks = compounds.map(compound => {
                // Calculate retention time using LSS gradient physics engine
                const rt = PhysicsEngine.calculateRetentionTime(compound, {
                    flowRate,
                    columnTemp,
                    columnType,
                    gradientProgram,
                    getPercentBAtTime
                });

                // Apply fault-induced RT shift
                const rtWithFault = rt * (1 + (fault?.rtShift || 0));

                // Calculate peak width — gradient-aware (compressed peaks in gradient mode)
                const peakWidth = PhysicsEngine.calculateGradientPeakWidth(
                    compound,
                    rtWithFault,
                    effectiveN,
                    {
                        gradientProgram,
                        flowRate,
                        getPercentBAtTime
                    }
                ) * (fault?.tailingFactor || 1);

                // Calculate response based on wavelength
                const wavelengthResponse = PhysicsEngine.calculateDetectorResponse(compound, wavelength);

                // Calculate height based on concentration and injection volume
                const concentrationFactor = concentration / 100;
                const volumeFactor = injectionVolume / 20;
                const signalReduction = fault?.signalReduction || 1;

                const height = compound.height * wavelengthResponse * concentrationFactor * volumeFactor * signalReduction;

                // Calculate area (Gaussian: Area = Height × σ × √(2π) ≈ Height × width × 2.507 / 4)
                const sigma = peakWidth / 2.355;
                const area = height * sigma * 2.507;

                return {
                    ...compound,
                    rt: rtWithFault,
                    peakWidth,
                    height,
                    area,
                    sigma,
                    asymmetry: compound.asymmetry * (fault?.tailingFactor || 1)
                };
            });

            // Generate chromatogram data points
            const dataPoints = CONFIG.dataPointsPerRun;
            const duration = this.getAnalysisDuration(gradientProgram);
            const dataA = [];

            // Noise level based on fault
            const noiseLevel = CONFIG.baselineNoiseLevel * (fault?.noiseMultiplier || 1);

            // Ghost peaks for contamination fault
            const ghostPeaks = [];
            if (fault?.ghostPeaks) {
                // Add 1-3 random ghost peaks
                const numGhosts = Math.floor(Math.random() * 3) + 1;
                for (let i = 0; i < numGhosts; i++) {
                    ghostPeaks.push({
                        rt: Math.random() * (duration - 2) + 1,
                        height: Math.random() * 15 + 5,
                        sigma: 0.1 + Math.random() * 0.1
                    });
                }
            }

            for (let i = 0; i <= dataPoints; i++) {
                const time = (i / dataPoints) * duration;

                // Baseline with noise + realistic drift
                let signal = Utils.gaussianRandom(0, noiseLevel);

                // Realistic baseline drift — slow sinusoidal wandering + 1/f-like low-frequency noise
                signal += 0.3 * Math.sin(time * 0.15 + 0.7);
                signal += 0.15 * Math.sin(time * 0.47 + 2.1);
                signal += 0.08 * Math.sin(time * 1.3 + 4.5);

                // Gradient-induced baseline shift (absorbance changes with %B)
                const percentBAtTime = getPercentBAtTime(time);
                signal += percentBAtTime * 0.005; // slight upward trend with increasing organic

                // Add baseline drift for some faults
                if (fault?.noiseMultiplier > 2) {
                    signal += Math.sin(time * 0.5) * 2;
                }

                // Add compound peaks
                calculatedPeaks.forEach(peak => {
                    signal += PhysicsEngine.generatePeakShape(
                        time,
                        peak.rt,
                        peak.sigma,
                        peak.height,
                        peak.asymmetry
                    );
                });

                // Add ghost peaks
                ghostPeaks.forEach(ghost => {
                    signal += PhysicsEngine.generatePeakShape(
                        time,
                        ghost.rt,
                        ghost.sigma,
                        ghost.height,
                        1.0
                    );
                });

                // Ensure non-negative
                signal = Math.max(0, signal);

                dataA.push({ x: time, y: signal });
            }

            return {
                dataA,
                peaks: calculatedPeaks
            };
        }

        start() {
            // Validate system ready
            if (!this.state.isSystemReady) {
                Toast.error('System not ready. Complete the startup wizard first.');
                return;
            }

            if (this.state.runInProgress && !this.state.isPaused) {
                return;
            }

            // If resuming from pause
            if (this.state.isPaused) {
                this.state.isPaused = false;
                this.state.runInProgress = true;
                this.animationFrameId = requestAnimationFrame(this._simulationLoop.bind(this));
                this.pressureInterval = setInterval(() => this._updatePressure(), CONFIG.pressureUpdateInterval);
                this.notifyUI({ type: 'run_pause', payload: this.state });
                return;
            }

            // Fresh start
            this.state.runInProgress = true;
            this.state.elapsedAnalysisTime = 0;
            this.state.currentPercentB = this.getCurrentPercentB(0);

            // Generate chromatogram data
            this.liveData = this.generateChromatogramData({
                ...this.state
            });

            this.notifyUI({ type: 'run_start', payload: this.state });

            // Start pressure updates
            this.pressureInterval = setInterval(() => this._updatePressure(), CONFIG.pressureUpdateInterval);

            // Handle instant mode
            if (this.state.instantMode) {
                this.state.elapsedAnalysisTime = this.getAnalysisDuration() * 60;
                this.state.currentPercentB = this.getCurrentPercentB(this.state.elapsedAnalysisTime / 60);
                this.notifyUI({
                    type: 'instant_data_update',
                    payload: {
                        ...this.state,
                        chromatogram: this.liveData
                    }
                });
                this._completeRun();
            } else {
                // Real-time simulation
                this.startTime = 0;
                this.animationFrameId = requestAnimationFrame(this._simulationLoop.bind(this));
            }
        }

        stop() {
            if (!this.state.runInProgress) return;

            this.state.runInProgress = false;
            this.state.isPaused = false;

            cancelAnimationFrame(this.animationFrameId);
            clearInterval(this.pressureInterval);

            // Animate pressure to zero
            gsap.to(this.state, {
                currentPressure: 0,
                duration: 1,
                onUpdate: () => this.notifyUI({ type: 'pressure_update', payload: this.state })
            });

            this.notifyUI({ type: 'run_stop', payload: this.state });
        }

        pause() {
            if (!this.state.runInProgress || this.state.isPaused) {
                // Resume
                if (this.state.isPaused) {
                    this.start();
                }
                return;
            }

            // Pause
            this.state.isPaused = true;
            cancelAnimationFrame(this.animationFrameId);
            clearInterval(this.pressureInterval);

            this.notifyUI({ type: 'run_pause', payload: this.state });
        }

        _simulationLoop(timestamp) {
            if (!this.state.runInProgress || this.state.isPaused) return;

            if (!this.startTime) this.startTime = timestamp;

            const durationSecs = this.getAnalysisDuration() * 60;

            // Calculate elapsed time (real-time)
            this.state.elapsedAnalysisTime = (timestamp - this.startTime) / 1000;

            // Update mobile phase composition
            this.state.currentPercentB = this.getCurrentPercentB(this.state.elapsedAnalysisTime / 60);

            // Check if complete
            if (this.state.elapsedAnalysisTime >= durationSecs) {
                this.state.elapsedAnalysisTime = durationSecs;
                this._completeRun();
                return;
            }

            // Calculate how many data points to show
            const points = Math.ceil((this.state.elapsedAnalysisTime / durationSecs) * this.liveData.dataA.length);

            this.notifyUI({
                type: 'data_update',
                payload: {
                    ...this.state,
                    chromatogram: {
                        dataA: this.liveData.dataA.slice(0, points)
                    }
                }
            });

            this.animationFrameId = requestAnimationFrame(this._simulationLoop.bind(this));
        }

        _updatePressure() {
            // Calculate pressure using physics engine (pass selected organic solvent)
            let pressure = PhysicsEngine.calculatePressure(
                this.state.flowRate,
                this.state.currentPercentB,
                this.state.columnType,
                this.state.columnTemp,
                this.state.mobilePhaseB
            );

            // Apply fault effects
            const fault = CONFIG.faults[this.state.currentFault];
            if (fault) {
                pressure += fault.pressureEffect;
            }

            // Add pump pulsation (simulation of reciprocating pump)
            // Small sine wave modulation based on flow rate
            const pulsationFreq = this.state.flowRate * 2;
            const pulsationAmp = 0.5 * (pressure / 100);
            pressure += Math.sin(Date.now() / 200 * pulsationFreq) * pulsationAmp;

            // Add random electronic noise to pressure transducer
            pressure += Utils.gaussianRandom(0, 0.2);

            // Update state (ensure pressure doesn't go below 0)
            this.state.currentPressure = Math.max(0, pressure);

            // Send update to UI
            this.notifyUI({ type: 'pressure_update', payload: this.state });
        }

        /**
         * Handle run completion
         */
        _completeRun() {
            this.state.runInProgress = false;
            this.state.isPaused = false;

            cancelAnimationFrame(this.animationFrameId);
            clearInterval(this.pressureInterval);

            // Notify UI with final data
            this.notifyUI({
                type: 'run_complete',
                payload: {
                    ...this.state,
                    peaks: this.liveData.peaks
                }
            });

            // Ramp down pressure to zero to simulate pump stopping
            // Using a simple interval to avoid dependency on external animation libraries here if GSAP fails
            const dropInterval = setInterval(() => {
                this.state.currentPressure *= 0.8;
                if (this.state.currentPressure < 1) {
                    this.state.currentPressure = 0;
                    clearInterval(dropInterval);
                }
                this.notifyUI({ type: 'pressure_update', payload: this.state });
            }, 100);
        }

        /**
         * Toggle the standard overlay on/off
         */
        toggleStandardOverlay() {
            this.state.showStandard = !this.state.showStandard;
            this.notifyUI({ type: 'toggle_standard', payload: this.state });
        }

        /**
         * Calculate System Suitability Testing (SST) parameters
         * Calculates N (Plates), T (Tailing), k' (Capacity), and R (Resolution)
         */
        calculateSST() {
            const peaks = this.liveData?.peaks || [];

            if (peaks.length === 0) {
                this.ui.Toast.warning('No peaks detected for SST calculation');
                return;
            }

            const results = peaks.sort((a, b) => a.rt - b.rt).map((peak, index) => {
                // 1. Theoretical Plates (N)
                // USP Method: N = 16 * (tR / W)^2
                const N = 16 * Math.pow(peak.rt / peak.peakWidth, 2);

                // 2. Tailing Factor (T)
                // T = W0.05 / 2f (Simplified here using asymmetry factor from physics engine)
                const T = peak.asymmetry;

                // 3. Capacity Factor (k')
                // k' = (tR - t0) / t0 (Assuming t0 is roughly 10% of standard run or calculated void)
                const t0 = this.getVoidTime();
                const k = (peak.rt - t0) / t0;

                // 4. Resolution (R)
                // R = 2(tR2 - tR1) / (W1 + W2)
                let R = 0;
                let R_pass = true; // First peak implies pass for resolution relative to previous

                if (index > 0) {
                    const prevPeak = peaks[index - 1];
                    R = PhysicsEngine.calculateResolution(prevPeak.rt, peak.rt, prevPeak.peakWidth, peak.peakWidth);

                    // check criteria
                    R_pass = R >= CONFIG.sstCriteria.resolution.min;
                }

                // Check other criteria
                const N_pass = N >= CONFIG.sstCriteria.theoreticalPlates.min;
                const T_pass = T <= CONFIG.sstCriteria.tailingFactor.max;
                const k_pass = k >= CONFIG.sstCriteria.capacityFactor.min;

                return {
                    name: peak.name,
                    rt: peak.rt,
                    peakWidth: peak.peakWidth,
                    N: Math.round(N),
                    N_pass,
                    T: T,
                    T_pass,
                    k: k.toFixed(2),
                    k_pass,
                    R: index === 0 ? '-' : R.toFixed(2),
                    R_pass
                };
            });

            this.state.sstResults = results;
            this.notifyUI({
                type: 'sst_complete',
                payload: { ...this.state, sstResults: results }
            });
        }

        /**
         * Estimate void time (t0) based on column dimensions and flow rate
         */
        getVoidTime() {
            const column = CONFIG.columns[this.state.columnType];
            const radius = column.innerDiameter / 20; // cm
            const length = column.length / 10; // cm

            // Vm ≈ 0.65 * π * r² * L (Total porosity approx 0.65)
            const columnVolume = 0.65 * Math.PI * Math.pow(radius, 2) * length; // mL

            return columnVolume / this.state.flowRate;
        }

        /**
         * Central method to update UI via the App/UI class
         */
        notifyUI(event) {
            if (this.ui && typeof this.ui.update === 'function') {
                this.ui.update(event);
            }
        }
    }

    // ========================================================================
    // INITIALIZATION
    // ========================================================================

    // Create and initialize the application instance
    const app = new App();

    // Expose app to window for debugging/console access if needed
    window.SimuPharma = app;

    // Start the application
    app.init();

});