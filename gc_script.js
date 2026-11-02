/**
 * SimuPharma - Advanced GC Digital Twin
 * Professional Edition JavaScript
 * Version 2.0 - Complete Implementation
 */

// ============================================
// GLOBAL STATE & CONFIGURATION
// ============================================

const AppState = {
    currentView: 'main',
    isRunning: false,
    runAborted: false,
    currentRunTime: 0,
    currentOvenTemp: 50,
    chromatogramData: null,
    peaksDetected: [],
    peaksIntegrated: [],
    identifiedCompounds: [],
    sampleName: null,
    sampleId: null,
    sessionStartTime: Date.now(),
    runStartTime: null,
    backgroundNoise: [],
    settings: {
        theme: 'light',
        lineWidth: 2,
        showGrid: true,
        autoScale: true,
        simSpeed: 'normal',
        noiseLevel: 'low',
        showRealtime: true,
        integrationMethod: 'auto',
        areaCalc: 'percent',
        soundEffects: false,
        showHints: true
    }
};

// Simulation timing based on speed setting (multiplier for real time)
const SimTiming = {
    fast: { multiplier: 10, updateInterval: 100 },
    normal: { multiplier: 5, updateInterval: 200 },
    realistic: { multiplier: 1, updateInterval: 500 }
};

// Noise levels (standard deviation as fraction of signal)
const NoiseLevels = {
    none: 0,
    low: 0.001,
    medium: 0.005,
    high: 0.015
};

// Chart instances
let mainChart = null;
let analysisChart = null;
let libraryPreviewChart = null;
let reportChart = null;
let tempProfileChart = null;
let vanDeemterChart = null;
let calibrationChart = null;

// Run interval reference
let runInterval = null;

// ============================================
// PHYSICAL CONSTANTS & PARAMETERS
// ============================================

const PhysicalConstants = {
    // Gas viscosities at 25°C (µPa·s)
    viscosity: {
        helium: 19.9,
        hydrogen: 8.9,
        nitrogen: 17.8
    },
    // Diffusion coefficients in carrier gas (cm²/s at 25°C, 1 atm)
    diffusionCoeff: {
        helium: 0.7,
        hydrogen: 0.9,
        nitrogen: 0.2
    },
    // Optimal linear velocities (cm/s)
    optimalVelocity: {
        helium: 30,
        hydrogen: 45,
        nitrogen: 12
    }
};

// Column specifications database
const ColumnDatabase = {
    'HP-5ms': {
        length: 30,        // meters
        id: 0.25,          // mm
        filmThickness: 0.25, // µm
        maxTemp: 325,
        phase: '5% Phenyl',
        polarity: 'non-polar',
        bleedTemp: 300
    },
    'DB-1': {
        length: 30,
        id: 0.25,
        filmThickness: 0.25,
        maxTemp: 325,
        phase: '100% Dimethylpolysiloxane',
        polarity: 'non-polar',
        bleedTemp: 300
    },
    'HP-1': {
        length: 30,
        id: 0.32,
        filmThickness: 0.25,
        maxTemp: 325,
        phase: '100% Dimethylpolysiloxane',
        polarity: 'non-polar',
        bleedTemp: 300
    },
    'DB-624': {
        length: 30,
        id: 0.25,
        filmThickness: 1.4,
        maxTemp: 260,
        phase: '6% Cyanopropylphenyl',
        polarity: 'mid-polar',
        bleedTemp: 240
    },
    'DB-WAX': {
        length: 30,
        id: 0.25,
        filmThickness: 0.25,
        maxTemp: 260,
        phase: 'Polyethylene Glycol',
        polarity: 'polar',
        bleedTemp: 240
    },
    'HP-INNOWax': {
        length: 30,
        id: 0.25,
        filmThickness: 0.25,
        maxTemp: 270,
        phase: 'Polyethylene Glycol',
        polarity: 'polar',
        bleedTemp: 250
    },
    'DB-FFAP': {
        length: 30,
        id: 0.25,
        filmThickness: 0.25,
        maxTemp: 250,
        phase: 'Nitroterephthalic acid modified PEG',
        polarity: 'polar',
        bleedTemp: 230
    }
};

// ============================================
// COMPOUND DATABASE - GC Specific Data
// ============================================

const CompoundDatabase = {
    // Alkanes
    'Pentane': {
        category: 'alkanes',
        formula: 'C5H12',
        mw: 72.15,
        bp: 36,
        cas: '109-66-0',
        kovatsRI_nonpolar: 500,
        kovatsRI_polar: 500,
        fidResponse: 1.0,
        description: 'Light alkane, very volatile'
    },
    'Hexane': {
        category: 'alkanes',
        formula: 'C6H14',
        mw: 86.18,
        bp: 69,
        cas: '110-54-3',
        kovatsRI_nonpolar: 600,
        kovatsRI_polar: 600,
        fidResponse: 1.0,
        description: 'Common laboratory solvent'
    },
    'Heptane': {
        category: 'alkanes',
        formula: 'C7H16',
        mw: 100.20,
        bp: 98,
        cas: '142-82-5',
        kovatsRI_nonpolar: 700,
        kovatsRI_polar: 700,
        fidResponse: 1.0,
        description: 'Reference standard for octane rating'
    },
    'Octane': {
        category: 'alkanes',
        formula: 'C8H18',
        mw: 114.23,
        bp: 126,
        cas: '111-65-9',
        kovatsRI_nonpolar: 800,
        kovatsRI_polar: 800,
        fidResponse: 1.0,
        description: 'Component of gasoline'
    },
    'Nonane': {
        category: 'alkanes',
        formula: 'C9H20',
        mw: 128.26,
        bp: 151,
        cas: '111-84-2',
        kovatsRI_nonpolar: 900,
        kovatsRI_polar: 900,
        fidResponse: 1.0,
        description: 'Higher alkane'
    },
    'Decane': {
        category: 'alkanes',
        formula: 'C10H22',
        mw: 142.28,
        bp: 174,
        cas: '124-18-5',
        kovatsRI_nonpolar: 1000,
        kovatsRI_polar: 1000,
        fidResponse: 1.0,
        description: 'Diesel fuel component'
    },
    'Undecane': {
        category: 'alkanes',
        formula: 'C11H24',
        mw: 156.31,
        bp: 196,
        cas: '1120-21-4',
        kovatsRI_nonpolar: 1100,
        kovatsRI_polar: 1100,
        fidResponse: 1.0,
        description: 'Higher alkane'
    },
    'Dodecane': {
        category: 'alkanes',
        formula: 'C12H26',
        mw: 170.34,
        bp: 216,
        cas: '112-40-3',
        kovatsRI_nonpolar: 1200,
        kovatsRI_polar: 1200,
        fidResponse: 1.0,
        description: 'Jet fuel component'
    },

    // Aromatics
    'Benzene': {
        category: 'aromatics',
        formula: 'C6H6',
        mw: 78.11,
        bp: 80,
        cas: '71-43-2',
        kovatsRI_nonpolar: 657,
        kovatsRI_polar: 985,
        fidResponse: 1.0,
        description: 'Aromatic hydrocarbon, carcinogen'
    },
    'Toluene': {
        category: 'aromatics',
        formula: 'C7H8',
        mw: 92.14,
        bp: 111,
        cas: '108-88-3',
        kovatsRI_nonpolar: 762,
        kovatsRI_polar: 1045,
        fidResponse: 1.0,
        description: 'Methylbenzene, common solvent'
    },
    'Ethylbenzene': {
        category: 'aromatics',
        formula: 'C8H10',
        mw: 106.17,
        bp: 136,
        cas: '100-41-4',
        kovatsRI_nonpolar: 857,
        kovatsRI_polar: 1120,
        fidResponse: 1.0,
        description: 'Styrene precursor'
    },
    'm-Xylene': {
        category: 'aromatics',
        formula: 'C8H10',
        mw: 106.17,
        bp: 139,
        cas: '108-38-3',
        kovatsRI_nonpolar: 864,
        kovatsRI_polar: 1135,
        fidResponse: 1.0,
        description: '1,3-Dimethylbenzene'
    },
    'p-Xylene': {
        category: 'aromatics',
        formula: 'C8H10',
        mw: 106.17,
        bp: 138,
        cas: '106-42-3',
        kovatsRI_nonpolar: 861,
        kovatsRI_polar: 1130,
        fidResponse: 1.0,
        description: '1,4-Dimethylbenzene'
    },
    'o-Xylene': {
        category: 'aromatics',
        formula: 'C8H10',
        mw: 106.17,
        bp: 144,
        cas: '95-47-6',
        kovatsRI_nonpolar: 887,
        kovatsRI_polar: 1175,
        fidResponse: 1.0,
        description: '1,2-Dimethylbenzene'
    },
    'Styrene': {
        category: 'aromatics',
        formula: 'C8H8',
        mw: 104.15,
        bp: 145,
        cas: '100-42-5',
        kovatsRI_nonpolar: 891,
        kovatsRI_polar: 1265,
        fidResponse: 1.0,
        description: 'Vinylbenzene, polymer precursor'
    },
    'Naphthalene': {
        category: 'aromatics',
        formula: 'C10H8',
        mw: 128.17,
        bp: 218,
        cas: '91-20-3',
        kovatsRI_nonpolar: 1181,
        kovatsRI_polar: 1720,
        fidResponse: 1.0,
        description: 'Bicyclic aromatic, mothballs'
    },

    // Alcohols
    'Methanol': {
        category: 'alcohols',
        formula: 'CH4O',
        mw: 32.04,
        bp: 65,
        cas: '67-56-1',
        kovatsRI_nonpolar: 0,  // Elutes with solvent
        kovatsRI_polar: 903,
        fidResponse: 0.7,
        description: 'Wood alcohol, toxic'
    },
    'Ethanol': {
        category: 'alcohols',
        formula: 'C2H6O',
        mw: 46.07,
        bp: 78,
        cas: '64-17-5',
        kovatsRI_nonpolar: 449,
        kovatsRI_polar: 936,
        fidResponse: 0.7,
        description: 'Grain alcohol'
    },
    'Isopropanol': {
        category: 'alcohols',
        formula: 'C3H8O',
        mw: 60.10,
        bp: 82,
        cas: '67-63-0',
        kovatsRI_nonpolar: 474,
        kovatsRI_polar: 948,
        fidResponse: 0.75,
        description: 'Rubbing alcohol'
    },
    'n-Propanol': {
        category: 'alcohols',
        formula: 'C3H8O',
        mw: 60.10,
        bp: 97,
        cas: '71-23-8',
        kovatsRI_nonpolar: 548,
        kovatsRI_polar: 1037,
        fidResponse: 0.75,
        description: '1-Propanol'
    },
    'n-Butanol': {
        category: 'alcohols',
        formula: 'C4H10O',
        mw: 74.12,
        bp: 117,
        cas: '71-36-3',
        kovatsRI_nonpolar: 652,
        kovatsRI_polar: 1142,
        fidResponse: 0.8,
        description: '1-Butanol'
    },
    'Isobutanol': {
        category: 'alcohols',
        formula: 'C4H10O',
        mw: 74.12,
        bp: 108,
        cas: '78-83-1',
        kovatsRI_nonpolar: 608,
        kovatsRI_polar: 1098,
        fidResponse: 0.8,
        description: '2-Methyl-1-propanol'
    },

    // Ketones & Esters
    'Acetone': {
        category: 'ketones',
        formula: 'C3H6O',
        mw: 58.08,
        bp: 56,
        cas: '67-64-1',
        kovatsRI_nonpolar: 500,
        kovatsRI_polar: 820,
        fidResponse: 0.65,
        description: 'Dimethyl ketone, nail polish remover'
    },
    'MEK': {
        category: 'ketones',
        formula: 'C4H8O',
        mw: 72.11,
        bp: 80,
        cas: '78-93-3',
        kovatsRI_nonpolar: 598,
        kovatsRI_polar: 907,
        fidResponse: 0.7,
        description: 'Methyl ethyl ketone, 2-Butanone'
    },
    'Methyl Isobutyl Ketone': {
        category: 'ketones',
        formula: 'C6H12O',
        mw: 100.16,
        bp: 117,
        cas: '108-10-1',
        kovatsRI_nonpolar: 731,
        kovatsRI_polar: 1005,
        fidResponse: 0.75,
        description: 'MIBK, 4-Methylpentan-2-one'
    },
    'Ethyl Acetate': {
        category: 'ketones',
        formula: 'C4H8O2',
        mw: 88.11,
        bp: 77,
        cas: '141-78-6',
        kovatsRI_nonpolar: 614,
        kovatsRI_polar: 888,
        fidResponse: 0.6,
        description: 'Common ester solvent'
    },
    'Butyl Acetate': {
        category: 'ketones',
        formula: 'C6H12O2',
        mw: 116.16,
        bp: 126,
        cas: '123-86-4',
        kovatsRI_nonpolar: 811,
        kovatsRI_polar: 1075,
        fidResponse: 0.65,
        description: 'Lacquer solvent'
    },

    // Halogenated compounds
    'Dichloromethane': {
        category: 'halogenated',
        formula: 'CH2Cl2',
        mw: 84.93,
        bp: 40,
        cas: '75-09-2',
        kovatsRI_nonpolar: 530,
        kovatsRI_polar: 750,
        fidResponse: 0.15,
        description: 'Methylene chloride, low FID response'
    },
    'Chloroform': {
        category: 'halogenated',
        formula: 'CHCl3',
        mw: 119.38,
        bp: 61,
        cas: '67-66-3',
        kovatsRI_nonpolar: 612,
        kovatsRI_polar: 845,
        fidResponse: 0.1,
        description: 'Trichloromethane'
    },
    'Carbon Tetrachloride': {
        category: 'halogenated',
        formula: 'CCl4',
        mw: 153.82,
        bp: 77,
        cas: '56-23-5',
        kovatsRI_nonpolar: 704,
        kovatsRI_polar: 840,
        fidResponse: 0.0,
        description: 'No FID response (fully halogenated)'
    },
    'Trichloroethylene': {
        category: 'halogenated',
        formula: 'C2HCl3',
        mw: 131.39,
        bp: 87,
        cas: '79-01-6',
        kovatsRI_nonpolar: 690,
        kovatsRI_polar: 925,
        fidResponse: 0.08,
        description: 'TCE, degreasing solvent'
    },
    'Tetrachloroethylene': {
        category: 'halogenated',
        formula: 'C2Cl4',
        mw: 165.83,
        bp: 121,
        cas: '127-18-4',
        kovatsRI_nonpolar: 795,
        kovatsRI_polar: 1010,
        fidResponse: 0.0,
        description: 'PCE, dry cleaning solvent'
    },

    // Terpenes (Essential Oils)
    'alpha-Pinene': {
        category: 'terpenes',
        formula: 'C10H16',
        mw: 136.23,
        bp: 156,
        cas: '80-56-8',
        kovatsRI_nonpolar: 939,
        kovatsRI_polar: 1030,
        fidResponse: 1.0,
        description: 'Pine scent, turpentine component'
    },
    'beta-Pinene': {
        category: 'terpenes',
        formula: 'C10H16',
        mw: 136.23,
        bp: 166,
        cas: '127-91-3',
        kovatsRI_nonpolar: 980,
        kovatsRI_polar: 1115,
        fidResponse: 1.0,
        description: 'Wood/pine scent'
    },
    'Limonene': {
        category: 'terpenes',
        formula: 'C10H16',
        mw: 136.23,
        bp: 176,
        cas: '138-86-3',
        kovatsRI_nonpolar: 1031,
        kovatsRI_polar: 1205,
        fidResponse: 1.0,
        description: 'Citrus scent, D-limonene'
    },
    'Eucalyptol': {
        category: 'terpenes',
        formula: 'C10H18O',
        mw: 154.25,
        bp: 176,
        cas: '470-82-6',
        kovatsRI_nonpolar: 1033,
        kovatsRI_polar: 1215,
        fidResponse: 0.9,
        description: '1,8-Cineole, eucalyptus oil'
    },
    'Menthol': {
        category: 'terpenes',
        formula: 'C10H20O',
        mw: 156.27,
        bp: 212,
        cas: '89-78-1',
        kovatsRI_nonpolar: 1175,
        kovatsRI_polar: 1640,
        fidResponse: 0.9,
        description: 'Peppermint component'
    },
    'Linalool': {
        category: 'terpenes',
        formula: 'C10H18O',
        mw: 154.25,
        bp: 198,
        cas: '78-70-6',
        kovatsRI_nonpolar: 1098,
        kovatsRI_polar: 1550,
        fidResponse: 0.9,
        description: 'Lavender scent'
    },
    'Camphor': {
        category: 'terpenes',
        formula: 'C10H16O',
        mw: 152.23,
        bp: 204,
        cas: '76-22-2',
        kovatsRI_nonpolar: 1143,
        kovatsRI_polar: 1530,
        fidResponse: 0.85,
        description: 'Camphor tree extract'
    }
};

// Sample mixtures
const SampleMixtures = {
    'Alkane Mix C5-C12': {
        components: [
            { compound: 'Pentane', concentration: 10 },
            { compound: 'Hexane', concentration: 10 },
            { compound: 'Heptane', concentration: 10 },
            { compound: 'Octane', concentration: 10 },
            { compound: 'Nonane', concentration: 10 },
            { compound: 'Decane', concentration: 10 },
            { compound: 'Undecane', concentration: 10 },
            { compound: 'Dodecane', concentration: 10 }
        ]
    },
    'BTEX Mix': {
        components: [
            { compound: 'Benzene', concentration: 25 },
            { compound: 'Toluene', concentration: 25 },
            { compound: 'Ethylbenzene', concentration: 15 },
            { compound: 'm-Xylene', concentration: 15 },
            { compound: 'o-Xylene', concentration: 10 },
            { compound: 'p-Xylene', concentration: 10 }
        ]
    },
    'Alcohol Mix': {
        components: [
            { compound: 'Methanol', concentration: 25 },
            { compound: 'Ethanol', concentration: 25 },
            { compound: 'Isopropanol', concentration: 25 },
            { compound: 'n-Butanol', concentration: 25 }
        ]
    },
    'ICH Class 2 Mix': {
        components: [
            { compound: 'Dichloromethane', concentration: 20 },
            { compound: 'Chloroform', concentration: 20 },
            { compound: 'Toluene', concentration: 20 },
            { compound: 'MEK', concentration: 20 },
            { compound: 'Acetone', concentration: 20 }
        ]
    },
    'ICH Class 3 Mix': {
        components: [
            { compound: 'Ethanol', concentration: 25 },
            { compound: 'Isopropanol', concentration: 25 },
            { compound: 'Ethyl Acetate', concentration: 25 },
            { compound: 'Acetone', concentration: 25 }
        ]
    },
    'Peppermint Oil': {
        components: [
            { compound: 'alpha-Pinene', concentration: 5 },
            { compound: 'beta-Pinene', concentration: 5 },
            { compound: 'Limonene', concentration: 10 },
            { compound: 'Eucalyptol', concentration: 15 },
            { compound: 'Menthol', concentration: 45 },
            { compound: 'Linalool', concentration: 5 }
        ]
    },
    'Eucalyptus Oil': {
        components: [
            { compound: 'alpha-Pinene', concentration: 15 },
            { compound: 'Limonene', concentration: 10 },
            { compound: 'Eucalyptol', concentration: 60 },
            { compound: 'Linalool', concentration: 5 },
            { compound: 'Camphor', concentration: 10 }
        ]
    },
    'Lavender Oil': {
        components: [
            { compound: 'alpha-Pinene', concentration: 5 },
            { compound: 'Limonene', concentration: 5 },
            { compound: 'Eucalyptol', concentration: 10 },
            { compound: 'Linalool', concentration: 40 },
            { compound: 'Camphor', concentration: 10 }
        ]
    },
    'Gasoline': {
        components: [
            { compound: 'Pentane', concentration: 5 },
            { compound: 'Hexane', concentration: 10 },
            { compound: 'Heptane', concentration: 15 },
            { compound: 'Octane', concentration: 15 },
            { compound: 'Benzene', concentration: 5 },
            { compound: 'Toluene', concentration: 20 },
            { compound: 'Ethylbenzene', concentration: 10 },
            { compound: 'm-Xylene', concentration: 10 },
            { compound: 'o-Xylene', concentration: 10 }
        ]
    },
    'Unknown': {
        components: [
            { compound: 'Toluene', concentration: 30 },
            { compound: 'MEK', concentration: 25 },
            { compound: 'Ethyl Acetate', concentration: 25 },
            { compound: 'Limonene', concentration: 20 }
        ]
    }
};

// ============================================
// UTILITY FUNCTIONS
// ============================================

function formatTime(date) {
    return date.toLocaleTimeString('en-US', { hour12: false });
}

function formatDate(date) {
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatSessionTime(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    return `${String(hours).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
}

function formatRunTime(minutes) {
    return minutes.toFixed(2) + ' min';
}

function gaussianRandom(mean = 0, stdev = 1) {
    const u = 1 - Math.random();
    const v = Math.random();
    const z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    return z * stdev + mean;
}

// ============================================
// CHROMATOGRAPHIC CALCULATIONS
// ============================================

/**
 * Calculate linear velocity from flow rate
 * u = F / (π * r² * 60) where F is in mL/min and r in cm
 */
function calculateLinearVelocity(flowRate, columnID) {
    const radius = (columnID / 10) / 2; // Convert mm to cm, then to radius
    const crossSection = Math.PI * radius * radius;
    const velocity = flowRate / (crossSection * 60); // cm/s
    return velocity;
}

/**
 * Calculate flow rate from linear velocity
 */
function calculateFlowRate(linearVelocity, columnID) {
    const radius = (columnID / 10) / 2;
    const crossSection = Math.PI * radius * radius;
    const flowRate = linearVelocity * crossSection * 60;
    return flowRate;
}

/**
 * Calculate dead time (hold-up time) - time for unretained compound
 * t_M = L / u where L is column length and u is linear velocity
 */
function calculateDeadTime(columnLength, linearVelocity) {
    const lengthCm = columnLength * 100; // m to cm
    return lengthCm / linearVelocity / 60; // minutes
}

/**
 * Golay equation for capillary columns (HETP)
 * H = B/u + (C_g + C_s)*u
 */
function calculateHETP(linearVelocity, carrierGas, columnID, filmThickness, temperature) {
    const D_g = PhysicalConstants.diffusionCoeff[carrierGas] * Math.pow((temperature + 273) / 298, 1.75);
    const d_c = columnID / 10; // mm to cm
    const d_f = filmThickness / 10000; // µm to cm
    
    // B term (longitudinal diffusion)
    const B = 2 * D_g;
    
    // C_g term (gas phase mass transfer)
    const C_g = (1 + 6 * 0.5 + 11 * 0.5 * 0.5) * d_c * d_c / (96 * (1 + 0.5) * (1 + 0.5) * D_g);
    
    // C_s term (stationary phase mass transfer) - simplified
    const D_s = D_g * 0.001; // Approximate stationary phase diffusion
    const C_s = 2 * 0.5 * d_f * d_f / (3 * (1 + 0.5) * (1 + 0.5) * D_s);
    
    const H = B / linearVelocity + (C_g + C_s) * linearVelocity;
    
    return {
        H: H,
        B: B,
        C_g: C_g,
        C_s: C_s
    };
}

/**
 * Calculate optimal linear velocity (minimum HETP)
 */
function calculateOptimalVelocity(carrierGas, columnID, filmThickness, temperature) {
    const D_g = PhysicalConstants.diffusionCoeff[carrierGas] * Math.pow((temperature + 273) / 298, 1.75);
    const d_c = columnID / 10;
    
    const B = 2 * D_g;
    const C_g = d_c * d_c / (96 * D_g);
    
    const u_opt = Math.sqrt(B / C_g);
    return u_opt;
}

/**
 * Calculate theoretical plates
 * N = L / H
 */
function calculatePlates(columnLength, HETP) {
    return (columnLength * 100) / HETP; // length in cm, HETP in cm
}

/**
 * Calculate retention time based on Kovats index and temperature program
 */
function calculateRetentionTime(compound, column, tempProgram, carrierGas, flowRate) {
    const compoundData = CompoundDatabase[compound];
    if (!compoundData) return null;
    
    const columnData = ColumnDatabase[column];
    const linearVelocity = calculateLinearVelocity(flowRate, columnData.id);
    const deadTime = calculateDeadTime(columnData.length, linearVelocity);
    
    // Get Kovats index based on column polarity
    const kovats = columnData.polarity === 'polar' ? 
        compoundData.kovatsRI_polar : compoundData.kovatsRI_nonpolar;
    
    // Simplified retention time calculation based on boiling point and column interaction
    // In reality, this is much more complex and depends on partition coefficients
    const bp = compoundData.bp;
    
    // Calculate average oven temperature during elution
    let avgTemp = getAverageTemp(tempProgram, 0, 10); // Rough estimate
    
    // Retention factor k = (tR - tM) / tM
    // Simplified model: k correlates with bp and column interaction
    const polarityFactor = columnData.polarity === 'polar' ? 1.3 : 1.0;
    const k = Math.exp((bp - avgTemp) / 50) * polarityFactor * (columnData.filmThickness / 0.25);
    
    // Retention time
    const tR = deadTime * (1 + Math.max(0.1, k));
    
    // Adjust for temperature program
    const adjustedTR = adjustRetentionForTempProgram(tR, bp, tempProgram, deadTime);
    
    return Math.max(deadTime * 1.1, adjustedTR);
}

/**
 * Get average temperature over a time range
 */
function getAverageTemp(tempProgram, startTime, endTime) {
    let sum = 0;
    let count = 0;
    for (let t = startTime; t <= endTime; t += 0.5) {
        sum += getTemperatureAtTime(tempProgram, t);
        count++;
    }
    return sum / count;
}

/**
 * Get oven temperature at a specific time based on temperature program
 */
function getTemperatureAtTime(tempProgram, time) {
    let currentTemp = tempProgram[0].temp;
    let currentTime = 0;
    
    for (let i = 0; i < tempProgram.length; i++) {
        const step = tempProgram[i];
        
        if (i === 0) {
            // Initial hold
            if (time <= step.hold) {
                return step.temp;
            }
            currentTime = step.hold;
            currentTemp = step.temp;
        } else {
            // Ramp
            const rampTime = (step.temp - currentTemp) / step.rate;
            
            if (time <= currentTime + rampTime) {
                // During ramp
                return currentTemp + step.rate * (time - currentTime);
            }
            
            currentTime += rampTime;
            currentTemp = step.temp;
            
            // Hold
            if (time <= currentTime + step.hold) {
                return step.temp;
            }
            currentTime += step.hold;
        }
    }
    
    return currentTemp; // Return final temp if beyond program
}

/**
 * Adjust retention time for temperature program
 */
function adjustRetentionForTempProgram(baseRT, boilingPoint, tempProgram, deadTime) {
    // Compounds elute faster in temperature programmed runs
    // The higher the bp relative to oven temp, the more the compound is retained
    
    let adjustedRT = baseRT;
    
    // Find when compound would elute based on its bp
    // Compound elutes roughly when oven temp approaches bp - 30°C
    const elutionTemp = boilingPoint - 30;
    
    // Find time when oven reaches this temperature
    let time = 0;
    const maxTime = 60; // Maximum run time to check
    
    for (let t = 0; t < maxTime; t += 0.1) {
        const ovenTemp = getTemperatureAtTime(tempProgram, t);
        if (ovenTemp >= elutionTemp) {
            adjustedRT = t + deadTime;
            break;
        }
    }
    
    // Add some retention based on column interaction
    adjustedRT += deadTime * 0.5;
    
    return adjustedRT;
}

/**
 * Calculate peak width at base
 * W = 4 * σ = 4 * tR / √N
 */
function calculatePeakWidth(retentionTime, plates) {
    const sigma = retentionTime / Math.sqrt(plates);
    return 4 * sigma;
}

/**
 * Calculate resolution between two peaks
 * Rs = 2 * (tR2 - tR1) / (W1 + W2)
 */
function calculateResolution(tR1, tR2, W1, W2) {
    return 2 * Math.abs(tR2 - tR1) / (W1 + W2);
}

/**
 * Calculate peak asymmetry factor
 * As = B / A at 10% height
 */
function calculateAsymmetry(peakData) {
    // Find 10% height
    const maxHeight = Math.max(...peakData.map(p => p.y));
    const threshold = maxHeight * 0.1;
    
    // Find left and right points at 10% height
    let leftIdx = 0, rightIdx = peakData.length - 1;
    let peakIdx = peakData.findIndex(p => p.y === maxHeight);
    
    for (let i = 0; i < peakIdx; i++) {
        if (peakData[i].y >= threshold) {
            leftIdx = i;
            break;
        }
    }
    
    for (let i = peakData.length - 1; i > peakIdx; i--) {
        if (peakData[i].y >= threshold) {
            rightIdx = i;
            break;
        }
    }
    
    const A = peakData[peakIdx].x - peakData[leftIdx].x;
    const B = peakData[rightIdx].x - peakData[peakIdx].x;
    
    return B / A;
}

// ============================================
// CHROMATOGRAM GENERATION
// ============================================

/**
 * Generate a Gaussian peak
 */
function generateGaussianPeak(tR, height, sigma, startTime, endTime, dataRate) {
    const points = [];
    const dt = 1 / dataRate / 60; // Convert Hz to minutes
    
    for (let t = startTime; t <= endTime; t += dt) {
        const exponent = -Math.pow(t - tR, 2) / (2 * sigma * sigma);
        const y = height * Math.exp(exponent);
        points.push({ x: t, y: y });
    }
    
    return points;
}

/**
 * Generate an Exponentially Modified Gaussian (EMG) peak for tailing
 */
function generateEMGPeak(tR, height, sigma, tau, startTime, endTime, dataRate) {
    const points = [];
    const dt = 1 / dataRate / 60;
    
    for (let t = startTime; t <= endTime; t += dt) {
        // EMG function
        const z = (t - tR) / sigma - sigma / tau;
        const emg = (sigma / tau) * Math.sqrt(Math.PI / 2) * 
                    Math.exp(0.5 * Math.pow(sigma / tau, 2) - (t - tR) / tau) *
                    (1 + erf(z / Math.sqrt(2)));
        
        const y = height * emg / Math.max(...points.map(p => p.y) || [1]);
        points.push({ x: t, y: isNaN(y) ? 0 : y });
    }
    
    // Normalize to desired height
    const maxY = Math.max(...points.map(p => p.y));
    if (maxY > 0) {
        points.forEach(p => p.y = p.y / maxY * height);
    }
    
    return points;
}

/**
 * Error function approximation
 */
function erf(x) {
    const a1 =  0.254829592;
    const a2 = -0.284496736;
    const a3 =  1.421413741;
    const a4 = -1.453152027;
    const a5 =  1.061405429;
    const p  =  0.3275911;

    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x);

    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

    return sign * y;
}

/**
 * Generate complete chromatogram
 */
function generateChromatogram(sample, column, tempProgram, carrierGas, flowRate, injectionVolume, splitRatio, dataRate) {
    const columnData = ColumnDatabase[column];
    const linearVelocity = calculateLinearVelocity(flowRate, columnData.id);
    const deadTime = calculateDeadTime(columnData.length, linearVelocity);
    const plates = calculatePlates(columnData.length, 0.00025); // Assume good HETP
    
    // Get total run time from temp program
    const totalRunTime = calculateTotalRunTime(tempProgram);
    
    // Initialize chromatogram array
    const numPoints = Math.floor(totalRunTime * dataRate * 60) + 1;
    const chromatogram = new Array(numPoints);
    const dt = 1 / dataRate / 60;
    
    for (let i = 0; i < numPoints; i++) {
        chromatogram[i] = { x: i * dt, y: 0 };
    }
    
    // Get sample components
    let components;
    if (SampleMixtures[sample]) {
        components = SampleMixtures[sample].components;
    } else if (CompoundDatabase[sample]) {
        components = [{ compound: sample, concentration: 100 }];
    } else {
        return chromatogram;
    }
    
    const peaks = [];
    
    // Generate peaks for each component
    components.forEach(comp => {
        const compoundData = CompoundDatabase[comp.compound];
        if (!compoundData) return;
        
        // Calculate retention time
        const tR = calculateRetentionTime(comp.compound, column, tempProgram, carrierGas, flowRate);
        if (tR === null || tR > totalRunTime) return;
        
        // Calculate peak width
        const sigma = tR / Math.sqrt(plates) / 4;
        
        // Calculate peak height based on concentration, FID response, and injection parameters
        const injectionFactor = injectionVolume / (splitRatio || 1);
        const height = comp.concentration * compoundData.fidResponse * injectionFactor * 10;
        
        // Add some tailing for more realistic peaks
        const tau = sigma * 0.3; // Tailing factor
        
        // Calculate peak area
        const area = height * sigma * Math.sqrt(2 * Math.PI);
        
        peaks.push({
            compound: comp.compound,
            tR: tR,
            height: height,
            sigma: sigma,
            area: area,
            concentration: comp.concentration
        });
        
        // Generate and add peak to chromatogram
        const peakStart = Math.max(0, tR - 5 * sigma);
        const peakEnd = Math.min(totalRunTime, tR + 8 * sigma);
        
        for (let i = 0; i < chromatogram.length; i++) {
            const t = chromatogram[i].x;
            if (t >= peakStart && t <= peakEnd) {
                // EMG peak shape
                const z = (t - tR) / sigma;
                const gauss = Math.exp(-z * z / 2);
                const tailing = t > tR ? Math.exp(-(t - tR) / (tau * 3)) : 1;
                chromatogram[i].y += height * gauss * tailing;
            }
        }
    });
    
    // Add baseline and noise
    const noiseLevel = NoiseLevels[AppState.settings.noiseLevel] || 0.001;
    const baselineOffset = 5; // pA
    
    for (let i = 0; i < chromatogram.length; i++) {
        // Add noise
        chromatogram[i].y += gaussianRandom(0, noiseLevel * 100);
        
        // Add baseline
        chromatogram[i].y += baselineOffset;
        
        // Add slight baseline drift
        chromatogram[i].y += Math.sin(chromatogram[i].x * 0.1) * 0.5;
        
        // Ensure non-negative
        chromatogram[i].y = Math.max(0, chromatogram[i].y);
    }
    
    // Add column bleed at high temperatures
    const finalTemp = tempProgram[tempProgram.length - 1].temp;
    if (finalTemp > columnData.bleedTemp) {
        const bleedIntensity = (finalTemp - columnData.bleedTemp) * 0.1;
        for (let i = 0; i < chromatogram.length; i++) {
            const t = chromatogram[i].x;
            const ovenTemp = getTemperatureAtTime(tempProgram, t);
            if (ovenTemp > columnData.bleedTemp) {
                chromatogram[i].y += (ovenTemp - columnData.bleedTemp) * 0.05;
            }
        }
    }
    
    return { chromatogram, peaks, deadTime, plates };
}

/**
 * Calculate total run time from temperature program
 */
function calculateTotalRunTime(tempProgram) {
    let totalTime = 0;
    let currentTemp = tempProgram[0].temp;
    
    for (let i = 0; i < tempProgram.length; i++) {
        const step = tempProgram[i];
        
        if (i === 0) {
            totalTime += step.hold;
        } else {
            // Ramp time
            const rampTime = Math.abs(step.temp - currentTemp) / step.rate;
            totalTime += rampTime;
            currentTemp = step.temp;
            
            // Hold time
            totalTime += step.hold;
        }
    }
    
    return totalTime;
}

/**
 * Get temperature program from UI
 */
function getTemperatureProgram() {
    const rows = document.querySelectorAll('#temp-program-table .program-row:not(.header-row)');
    const program = [];
    
    rows.forEach((row, index) => {
        const tempInput = row.querySelector('.temp-input');
        const holdInput = row.querySelector('.hold-input');
        const rateInput = row.querySelector('.rate-input');
        
        if (tempInput && holdInput) {
            const step = {
                temp: parseFloat(tempInput.value) || 50,
                hold: parseFloat(holdInput.value) || 0
            };
            
            if (index > 0 && rateInput) {
                step.rate = parseFloat(rateInput.value) || 10;
            }
            
            program.push(step);
        }
    });
    
    return program;
}
// ============================================
// PEAK INTEGRATION & ANALYSIS
// ============================================

/**
 * Integrate peaks in chromatogram
 */
function integratePeaks(chromatogram, threshold = 0.05) {
    const peaks = [];
    const baseline = calculateBaseline(chromatogram);
    const maxSignal = Math.max(...chromatogram.map(p => p.y));
    const minPeakHeight = maxSignal * threshold;
    
    let inPeak = false;
    let peakStart = 0;
    let peakData = [];
    
    for (let i = 1; i < chromatogram.length - 1; i++) {
        const prev = chromatogram[i - 1].y - baseline[i - 1];
        const curr = chromatogram[i].y - baseline[i];
        const next = chromatogram[i + 1].y - baseline[i + 1];
        
        // Detect peak start (rising above threshold)
        if (!inPeak && curr > minPeakHeight && curr > prev) {
            inPeak = true;
            peakStart = i;
            peakData = [];
        }
        
        // Collect peak data
        if (inPeak) {
            peakData.push({
                x: chromatogram[i].x,
                y: curr,
                baseline: baseline[i]
            });
        }
        
        // Detect peak end (falling below threshold or local minimum)
        if (inPeak && (curr < minPeakHeight || (curr < prev && curr < next && peakData.length > 3))) {
            inPeak = false;
            
            if (peakData.length > 5) {
                const peak = analyzePeak(peakData, chromatogram, peakStart, i);
                if (peak.height > minPeakHeight) {
                    peaks.push(peak);
                }
            }
        }
    }
    
    // Calculate area percentages
    const totalArea = peaks.reduce((sum, p) => sum + p.area, 0);
    peaks.forEach(p => {
        p.areaPercent = totalArea > 0 ? (p.area / totalArea * 100) : 0;
    });
    
    // Sort by retention time
    peaks.sort((a, b) => a.rt - b.rt);
    
    // Assign peak numbers
    peaks.forEach((p, i) => p.peakNumber = i + 1);
    
    return peaks;
}

/**
 * Calculate baseline using rolling minimum
 */
function calculateBaseline(chromatogram, windowSize = 50) {
    const baseline = new Array(chromatogram.length);
    
    for (let i = 0; i < chromatogram.length; i++) {
        const start = Math.max(0, i - windowSize);
        const end = Math.min(chromatogram.length, i + windowSize);
        
        let minVal = Infinity;
        for (let j = start; j < end; j++) {
            if (chromatogram[j].y < minVal) {
                minVal = chromatogram[j].y;
            }
        }
        baseline[i] = minVal;
    }
    
    return baseline;
}

/**
 * Analyze a single peak
 */
function analyzePeak(peakData, chromatogram, startIdx, endIdx) {
    // Find apex
    let maxHeight = 0;
    let apexIdx = 0;
    
    for (let i = 0; i < peakData.length; i++) {
        if (peakData[i].y > maxHeight) {
            maxHeight = peakData[i].y;
            apexIdx = i;
        }
    }
    
    const rt = peakData[apexIdx].x;
    const height = maxHeight;
    
    // Calculate area using trapezoidal rule
    let area = 0;
    for (let i = 0; i < peakData.length - 1; i++) {
        const dx = peakData[i + 1].x - peakData[i].x;
        const avgY = (peakData[i].y + peakData[i + 1].y) / 2;
        area += dx * avgY;
    }
    
    // Calculate width at half height
    const halfHeight = height / 2;
    let leftHalf = rt, rightHalf = rt;
    
    for (let i = apexIdx; i >= 0; i--) {
        if (peakData[i].y <= halfHeight) {
            leftHalf = peakData[i].x;
            break;
        }
    }
    
    for (let i = apexIdx; i < peakData.length; i++) {
        if (peakData[i].y <= halfHeight) {
            rightHalf = peakData[i].x;
            break;
        }
    }
    
    const widthHalfHeight = rightHalf - leftHalf;
    const widthBase = peakData[peakData.length - 1].x - peakData[0].x;
    
    // Calculate theoretical plates
    const N = 5.54 * Math.pow(rt / widthHalfHeight, 2);
    
    // Calculate asymmetry at 10% height
    const tenPercentHeight = height * 0.1;
    let leftTen = rt, rightTen = rt;
    
    for (let i = apexIdx; i >= 0; i--) {
        if (peakData[i].y <= tenPercentHeight) {
            leftTen = peakData[i].x;
            break;
        }
    }
    
    for (let i = apexIdx; i < peakData.length; i++) {
        if (peakData[i].y <= tenPercentHeight) {
            rightTen = peakData[i].x;
            break;
        }
    }
    
    const A = rt - leftTen;
    const B = rightTen - rt;
    const asymmetry = A > 0 ? B / A : 1;
    
    return {
        rt: rt,
        height: height,
        area: area * 60000, // Convert to standard area units
        areaPercent: 0, // Calculated later
        widthHalfHeight: widthHalfHeight,
        widthBase: widthBase,
        plates: Math.round(N),
        asymmetry: asymmetry,
        startTime: peakData[0].x,
        endTime: peakData[peakData.length - 1].x
    };
}

/**
 * Identify compounds based on retention time matching
 */
function identifyCompounds(peaks, column, tempProgram, carrierGas, flowRate, tolerance = 0.1) {
    const columnData = ColumnDatabase[column];
    const identifications = [];
    
    peaks.forEach(peak => {
        const matches = [];
        
        // Search through compound database
        Object.entries(CompoundDatabase).forEach(([name, compound]) => {
            // Calculate expected retention time for this compound
            const expectedRT = calculateRetentionTime(name, column, tempProgram, carrierGas, flowRate);
            
            if (expectedRT !== null) {
                const diff = Math.abs(peak.rt - expectedRT);
                const percentDiff = diff / expectedRT * 100;
                
                if (percentDiff <= tolerance * 100) {
                    matches.push({
                        compound: name,
                        expectedRT: expectedRT,
                        matchScore: 100 - percentDiff,
                        data: compound
                    });
                }
            }
        });
        
        // Sort by match score
        matches.sort((a, b) => b.matchScore - a.matchScore);
        
        identifications.push({
            peak: peak,
            matches: matches.slice(0, 5), // Top 5 matches
            bestMatch: matches.length > 0 ? matches[0] : null
        });
    });
    
    return identifications;
}

/**
 * Calculate Kovats Retention Index
 */
function calculateKovatsIndex(retentionTime, deadTime, alkaneRTs) {
    // alkaneRTs should be an object like { 6: 2.5, 7: 3.8, 8: 5.2, ... }
    // where keys are carbon numbers and values are retention times
    
    const carbonNumbers = Object.keys(alkaneRTs).map(Number).sort((a, b) => a - b);
    
    // Find bracketing alkanes
    let lowerC, upperC;
    for (let i = 0; i < carbonNumbers.length - 1; i++) {
        if (alkaneRTs[carbonNumbers[i]] <= retentionTime && alkaneRTs[carbonNumbers[i + 1]] >= retentionTime) {
            lowerC = carbonNumbers[i];
            upperC = carbonNumbers[i + 1];
            break;
        }
    }
    
    if (!lowerC || !upperC) return null;
    
    // Calculate adjusted retention times
    const tR_lower = alkaneRTs[lowerC] - deadTime;
    const tR_upper = alkaneRTs[upperC] - deadTime;
    const tR_compound = retentionTime - deadTime;
    
    // Kovats index formula (isothermal)
    const RI = 100 * (lowerC + (Math.log(tR_compound) - Math.log(tR_lower)) / (Math.log(tR_upper) - Math.log(tR_lower)));
    
    return RI;
}

// ============================================
// LOGGING SYSTEM
// ============================================

function logMessage(message, type = 'info') {
    const logPanel = document.getElementById('gc-log-panel');
    if (!logPanel) return;
    
    const timestamp = formatTime(new Date());
    const p = document.createElement('p');
    p.innerHTML = `<span class="log-timestamp">[${timestamp}]</span> ${message}`;
    
    if (type === 'error') p.style.color = 'var(--danger-color)';
    else if (type === 'success') p.style.color = 'var(--success-color)';
    else if (type === 'warning') p.style.color = 'var(--warning-color)';
    
    logPanel.appendChild(p);
    logPanel.scrollTop = logPanel.scrollHeight;
    
    // Also add to activity list on main view
    addActivity(message);
}

function addActivity(message) {
    const activityList = document.getElementById('activity-list');
    if (!activityList) return;
    
    const item = document.createElement('div');
    item.className = 'activity-item';
    item.innerHTML = `<i class="fas fa-check-circle"></i><span>${message}</span>`;
    
    activityList.insertBefore(item, activityList.firstChild);
    
    // Keep only last 10 items
    while (activityList.children.length > 10) {
        activityList.removeChild(activityList.lastChild);
    }
}

// ============================================
// TOAST NOTIFICATIONS
// ============================================

function showToast(title, message, type = 'info', duration = 4000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    else if (type === 'warning') icon = 'fa-exclamation-triangle';
    else if (type === 'error') icon = 'fa-times-circle';
    
    toast.innerHTML = `
        <div class="toast-icon"><i class="fas ${icon}"></i></div>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close"><i class="fas fa-times"></i></button>
    `;
    
    container.appendChild(toast);
    
    // Close button
    toast.querySelector('.toast-close').addEventListener('click', () => {
        toast.remove();
    });
    
    // Auto remove
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.animation = 'toastSlideIn 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
}

// ============================================
// CHART MANAGEMENT
// ============================================

function initializeMainChart() {
    const ctx = document.getElementById('gc-chart');
    if (!ctx) return;
    
    mainChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Chromatogram',
                data: [],
                borderColor: 'rgb(211, 84, 0)',
                backgroundColor: 'rgba(211, 84, 0, 0.1)',
                borderWidth: AppState.settings.lineWidth,
                pointRadius: 0,
                pointHoverRadius: 4,
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 300
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Time (min)',
                        font: { weight: 'bold' }
                    },
                    min: 0,
                    grid: {
                        display: AppState.settings.showGrid,
                        color: 'rgba(211, 84, 0, 0.1)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Signal (pA)',
                        font: { weight: 'bold' }
                    },
                    beginAtZero: true,
                    grid: {
                        display: AppState.settings.showGrid,
                        color: 'rgba(211, 84, 0, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.x.toFixed(3)} min: ${context.parsed.y.toFixed(2)} pA`;
                        }
                    }
                },
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy'
                    },
                    zoom: {
                        wheel: {
                            enabled: true
                        },
                        pinch: {
                            enabled: true
                        },
                        mode: 'xy'
                    }
                }
            }
        }
    });
    
    // Cursor tracking
    ctx.addEventListener('mousemove', handleChartMouseMove);
    ctx.addEventListener('mouseleave', () => {
        document.getElementById('cursor-info')?.classList.add('hidden');
    });
}

function handleChartMouseMove(e) {
    const cursorInfo = document.getElementById('cursor-info');
    if (!cursorInfo || !mainChart || !mainChart.data.datasets[0].data.length) return;
    
    const rect = e.target.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const xValue = mainChart.scales.x.getValueForPixel(x);
    const yValue = mainChart.scales.y.getValueForPixel(y);
    
    if (xValue >= 0) {
        document.getElementById('cursor-time').textContent = `${xValue.toFixed(3)} min`;
        document.getElementById('cursor-signal').textContent = `${yValue.toFixed(2)} pA`;
        cursorInfo.classList.remove('hidden');
    }
}

function updateChart(data, label = 'Chromatogram') {
    if (!mainChart) return;
    
    mainChart.data.datasets[0].data = data;
    mainChart.data.datasets[0].label = label;
    
    if (AppState.settings.autoScale && data.length > 0) {
        const xValues = data.map(p => p.x);
        const yValues = data.map(p => p.y);
        mainChart.options.scales.x.max = Math.max(...xValues) * 1.02;
        mainChart.options.scales.y.max = Math.max(...yValues) * 1.1;
    }
    
    mainChart.update('none');
}

function addReferenceToChart(data, label = 'Reference', color = 'rgb(40, 167, 69)') {
    if (!mainChart) return;
    
    mainChart.data.datasets.push({
        label: label,
        data: data,
        borderColor: color,
        backgroundColor: 'transparent',
        borderWidth: AppState.settings.lineWidth,
        pointRadius: 0,
        borderDash: [5, 5],
        fill: false
    });
    
    mainChart.update();
}

function addPeakAnnotations(peaks) {
    if (!mainChart) return;
    
    // Clear existing annotations
    mainChart.options.plugins.annotation = {
        annotations: {}
    };
    
    peaks.forEach((peak, i) => {
        // Vertical line at retention time
        mainChart.options.plugins.annotation.annotations[`peak${i}`] = {
            type: 'line',
            xMin: peak.rt,
            xMax: peak.rt,
            yMin: 0,
            yMax: peak.height * 0.95,
            borderColor: 'rgba(40, 167, 69, 0.7)',
            borderWidth: 1,
            borderDash: [3, 3]
        };
        
        // Label at top
        mainChart.options.plugins.annotation.annotations[`label${i}`] = {
            type: 'label',
            xValue: peak.rt,
            yValue: peak.height,
            content: peak.peakNumber.toString(),
            font: { size: 10, weight: 'bold' },
            color: 'rgb(40, 167, 69)'
        };
    });
    
    mainChart.update();
}

function resetChartZoom() {
    if (mainChart) {
        mainChart.resetZoom();
    }
}

function initializeTempProfileChart() {
    const ctx = document.getElementById('temp-profile-chart');
    if (!ctx) return;
    
    tempProfileChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Temperature',
                data: [],
                borderColor: 'rgb(255, 107, 53)',
                backgroundColor: 'rgba(255, 107, 53, 0.2)',
                borderWidth: 2,
                pointRadius: 0,
                fill: true,
                tension: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                x: {
                    type: 'linear',
                    display: false
                },
                y: {
                    display: false,
                    min: 0
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
    
    updateTempProfileChart();
}

function updateTempProfileChart() {
    if (!tempProfileChart) return;
    
    const tempProgram = getTemperatureProgram();
    const totalTime = calculateTotalRunTime(tempProgram);
    const data = [];
    
    for (let t = 0; t <= totalTime; t += 0.5) {
        data.push({
            x: t,
            y: getTemperatureAtTime(tempProgram, t)
        });
    }
    
    tempProfileChart.data.datasets[0].data = data;
    tempProfileChart.options.scales.y.max = Math.max(...data.map(p => p.y)) * 1.1;
    tempProfileChart.update('none');
    
    // Update total run time display
    document.getElementById('total-run-time').textContent = totalTime.toFixed(1) + ' min';
}

// ============================================
// VIEW MANAGEMENT
// ============================================

function switchView(viewName) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    
    if (viewName === 'software') {
        document.getElementById('software-screen-view').classList.add('active');
        AppState.currentView = 'software';
        logMessage('ChemStation software opened');
    } else {
        document.getElementById('gc-main-view').classList.add('active');
        AppState.currentView = 'main';
    }
}

// ============================================
// MODAL MANAGEMENT
// ============================================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modal && backdrop) {
        backdrop.classList.remove('hidden');
        modal.classList.remove('hidden');
        
        // Initialize modal-specific content
        if (modalId === 'library-modal') {
            populateLibraryList();
        } else if (modalId === 'report-modal') {
            generateReport();
        } else if (modalId === 'vandeemter-modal') {
            initializeVanDeemterChart();
        } else if (modalId === 'analysis-modal') {
            initializeAnalysisModal();
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modal) modal.classList.add('hidden');
    if (backdrop) backdrop.classList.add('hidden');
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(m => m.classList.add('hidden'));
    document.getElementById('modal-backdrop')?.classList.add('hidden');
}

// ============================================
// RUN SIMULATION
// ============================================

async function startRun() {
    if (AppState.isRunning) {
        showToast('Warning', 'A run is already in progress', 'warning');
        return;
    }
    
    // Get parameters
    const sample = document.getElementById('sample-select').value;
    const column = document.getElementById('column-select').value;
    const carrierGas = document.getElementById('carrier-gas').value;
    const flowRate = parseFloat(document.getElementById('flow-rate').value) || 1.0;
    const injectionVolume = parseFloat(document.getElementById('injection-volume').value) || 1.0;
    const splitRatio = parseFloat(document.getElementById('split-ratio').value) || 50;
    const injectionMode = document.getElementById('injection-mode').value;
    const dataRate = parseInt(document.getElementById('data-rate').value) || 20;
    const tempProgram = getTemperatureProgram();
    
    // Validate parameters
    const columnData = ColumnDatabase[column];
    const maxTemp = tempProgram.reduce((max, step) => Math.max(max, step.temp), 0);
    
    if (maxTemp > columnData.maxTemp) {
        showToast('Warning', `Max temperature (${maxTemp}°C) exceeds column limit (${columnData.maxTemp}°C)`, 'warning');
    }
    
    AppState.isRunning = true;
    AppState.runAborted = false;
    AppState.sampleName = sample;
    AppState.sampleId = document.getElementById('sample-id-input').value || `GC-${Date.now()}`;
    AppState.runStartTime = Date.now();
    
    // Show run overlay
    const overlay = document.getElementById('run-status-overlay');
    overlay?.classList.remove('hidden');
    
    // Update status
    document.getElementById('software-status-led')?.classList.add('running');
    document.getElementById('software-status-text').textContent = 'Running...';
    
    logMessage(`Starting run: ${sample}`);
    logMessage(`Column: ${column}, Flow: ${flowRate} mL/min`);
    
    // Show injection animation
    await showInjectionAnimation();
    
    // Generate chromatogram data
    const actualSplitRatio = injectionMode.includes('splitless') ? 1 : splitRatio;
    const result = generateChromatogram(sample, column, tempProgram, carrierGas, flowRate, injectionVolume, actualSplitRatio, dataRate);
    
    AppState.chromatogramData = result.chromatogram;
    AppState.peaksDetected = result.peaks;
    
    const totalRunTime = calculateTotalRunTime(tempProgram);
    const simTiming = SimTiming[AppState.settings.simSpeed];
    const updateInterval = simTiming.updateInterval;
    const timeMultiplier = simTiming.multiplier;
    
    let currentIndex = 0;
    const displayData = [];
    
    // Simulate run with real-time update
    runInterval = setInterval(() => {
        if (AppState.runAborted) {
            clearInterval(runInterval);
            finishRun(false);
            return;
        }
        
        // Calculate how many data points to add
        const elapsedRealTime = (Date.now() - AppState.runStartTime) / 1000; // seconds
        const simulatedTime = elapsedRealTime * timeMultiplier / 60; // minutes
        const targetIndex = Math.floor(simulatedTime * dataRate * 60);
        
        // Add new data points
        while (currentIndex < targetIndex && currentIndex < result.chromatogram.length) {
            displayData.push(result.chromatogram[currentIndex]);
            currentIndex++;
        }
        
        // Update display
        const progress = (currentIndex / result.chromatogram.length) * 100;
        updateRunStatus(simulatedTime, progress);
        
        if (displayData.length > 0) {
            updateChart(displayData, sample);
        }
        
        // Update oven temperature display
        const currentTemp = getTemperatureAtTime(tempProgram, simulatedTime);
        document.getElementById('current-oven-temp').textContent = `${Math.round(currentTemp)}°C`;
        AppState.currentOvenTemp = currentTemp;
        
        // Check if run is complete
        if (currentIndex >= result.chromatogram.length) {
            clearInterval(runInterval);
            finishRun(true);
        }
        
    }, updateInterval);
}

function updateRunStatus(currentTime, progress) {
    document.getElementById('current-run-time').textContent = formatRunTime(currentTime);
    document.getElementById('run-progress-bar').style.width = `${progress}%`;
    document.getElementById('run-status-text').textContent = `Acquiring data... ${progress.toFixed(0)}%`;
    
    // Update realtime signal display
    if (AppState.chromatogramData && AppState.chromatogramData.length > 0) {
        const idx = Math.floor(currentTime * 20 * 60); // Assuming 20 Hz
        if (idx < AppState.chromatogramData.length) {
            const signal = AppState.chromatogramData[idx].y;
            document.getElementById('realtime-signal').textContent = `${signal.toFixed(2)} pA`;
        }
    }
}

function finishRun(completed) {
    AppState.isRunning = false;
    
    // Hide overlay
    document.getElementById('run-status-overlay')?.classList.add('hidden');
    
    // Update status
    document.getElementById('software-status-led')?.classList.remove('running');
    document.getElementById('software-status-text').textContent = 'Ready';
    
    if (completed) {
        // Finalize chart
        updateChart(AppState.chromatogramData, AppState.sampleName);
        
        // Auto-integrate
        AppState.peaksIntegrated = integratePeaks(AppState.chromatogramData);
        
        // Update info bar
        const tempProgram = getTemperatureProgram();
        const totalTime = calculateTotalRunTime(tempProgram);
        document.getElementById('info-sample-name').textContent = AppState.sampleName;
        document.getElementById('info-column').textContent = document.getElementById('column-select').value;
        document.getElementById('info-detector').textContent = document.getElementById('detector-type').value;
        document.getElementById('info-runtime').textContent = totalTime.toFixed(1) + ' min';
        document.getElementById('quality-indicator').innerHTML = 
            `<i class="fas fa-signal"></i><span>Peaks: ${AppState.peaksIntegrated.length}</span>`;
        
        // Enable buttons
        enableAnalysisButtons();
        
        logMessage(`Run complete: ${AppState.peaksIntegrated.length} peaks detected`, 'success');
        showToast('Run Complete', `${AppState.sampleName} analysis finished`, 'success');
    } else {
        logMessage('Run aborted by user', 'warning');
        showToast('Run Aborted', 'The run was stopped', 'warning');
    }
}

function abortRun() {
    if (AppState.isRunning) {
        AppState.runAborted = true;
    }
}

async function showInjectionAnimation() {
    const overlay = document.getElementById('injection-overlay');
    if (!overlay) return;
    
    overlay.classList.remove('hidden');
    document.getElementById('injection-status').textContent = 'Injecting sample...';
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    document.getElementById('injection-status').textContent = 'Sample injected';
    await new Promise(resolve => setTimeout(resolve, 500));
    
    overlay.classList.add('hidden');
}

// ============================================
// INTEGRATION & ANALYSIS FUNCTIONS
// ============================================

function performIntegration() {
    if (!AppState.chromatogramData || AppState.chromatogramData.length === 0) {
        showToast('Error', 'No chromatogram data available', 'error');
        return;
    }
    
    const threshold = parseInt(document.getElementById('slope-sensitivity')?.value || 50) / 1000;
    AppState.peaksIntegrated = integratePeaks(AppState.chromatogramData, threshold);
    
    // Update peak table
    updatePeakTable(AppState.peaksIntegrated);
    
    // Add annotations
    addPeakAnnotations(AppState.peaksIntegrated);
    
    // Update quality indicator
    document.getElementById('quality-indicator').innerHTML = 
        `<i class="fas fa-signal"></i><span>Peaks: ${AppState.peaksIntegrated.length}</span>`;
    
    // Expand right panel
    document.getElementById('software-right-panel').classList.remove('collapsed');
    
    // Calculate chromatographic parameters
    updateChromatographicParameters();
    
    logMessage(`Integration complete: ${AppState.peaksIntegrated.length} peaks`, 'success');
    showToast('Integration Complete', `Found ${AppState.peaksIntegrated.length} peaks`, 'success');
}

function updatePeakTable(peaks) {
    const tbody = document.getElementById('peak-table-body');
    if (!tbody) return;
    
    if (peaks.length === 0) {
        tbody.innerHTML = '<tr class="empty-row"><td colspan="5">No peaks detected</td></tr>';
        return;
    }
    
    tbody.innerHTML = peaks.map(peak => `
        <tr data-peak="${peak.peakNumber}">
            <td>${peak.peakNumber}</td>
            <td>${peak.rt.toFixed(3)}</td>
            <td>${peak.area.toFixed(0)}</td>
            <td>${peak.areaPercent.toFixed(2)}%</td>
            <td>${peak.height.toFixed(1)}</td>
        </tr>
    `).join('');
    
    // Add click handlers for peak selection
    tbody.querySelectorAll('tr[data-peak]').forEach(row => {
        row.addEventListener('click', () => highlightPeak(parseInt(row.dataset.peak)));
    });
}

function highlightPeak(peakNumber) {
    const peak = AppState.peaksIntegrated.find(p => p.peakNumber === peakNumber);
    if (!peak || !mainChart) return;
    
    // Zoom to peak region
    mainChart.options.scales.x.min = peak.startTime - 0.5;
    mainChart.options.scales.x.max = peak.endTime + 0.5;
    mainChart.update();
    
    // Highlight row
    document.querySelectorAll('#peak-table-body tr').forEach(r => r.classList.remove('selected'));
    document.querySelector(`#peak-table-body tr[data-peak="${peakNumber}"]`)?.classList.add('selected');
}

function updateChromatographicParameters() {
    if (AppState.peaksIntegrated.length === 0) return;
    
    const peaks = AppState.peaksIntegrated;
    const deadTime = AppState.chromatogramData ? 
        calculateDeadTime(
            ColumnDatabase[document.getElementById('column-select').value].length,
            calculateLinearVelocity(
                parseFloat(document.getElementById('flow-rate').value),
                ColumnDatabase[document.getElementById('column-select').value].id
            )
        ) : 0.5;
    
    // Calculate k' for first major peak
    if (peaks.length > 0) {
        const k = (peaks[0].rt - deadTime) / deadTime;
        document.getElementById('calc-k').textContent = k.toFixed(2);
    }
    
    // Calculate resolution between adjacent peaks
    if (peaks.length >= 2) {
        const Rs = calculateResolution(
            peaks[0].rt, peaks[1].rt,
            peaks[0].widthBase, peaks[1].widthBase
        );
        document.getElementById('calc-rs').textContent = Rs.toFixed(2);
    }
    
    // Average plates
    const avgPlates = peaks.reduce((sum, p) => sum + p.plates, 0) / peaks.length;
    document.getElementById('calc-n').textContent = Math.round(avgPlates).toLocaleString();
    
    // Average asymmetry
    const avgAsym = peaks.reduce((sum, p) => sum + p.asymmetry, 0) / peaks.length;
    document.getElementById('calc-as').textContent = avgAsym.toFixed(2);
}

function performIdentification() {
    if (!AppState.peaksIntegrated || AppState.peaksIntegrated.length === 0) {
        showToast('Error', 'Please integrate peaks first', 'error');
        return;
    }
    
    const column = document.getElementById('column-select').value;
    const tempProgram = getTemperatureProgram();
    const carrierGas = document.getElementById('carrier-gas').value;
    const flowRate = parseFloat(document.getElementById('flow-rate').value);
    
    AppState.identifiedCompounds = identifyCompounds(
        AppState.peaksIntegrated, column, tempProgram, carrierGas, flowRate
    );
    
    // Update identification results panel
    updateIdentificationResults();
    
    // Open analysis modal
    openModal('analysis-modal');
    
    logMessage('Compound identification complete', 'success');
}

function updateIdentificationResults() {
    const container = document.getElementById('identification-results');
    if (!container) return;
    
    if (AppState.identifiedCompounds.length === 0) {
        container.innerHTML = '<p class="no-data">No compounds identified</p>';
        return;
    }
    
    let html = '<div class="identification-list">';
    
    AppState.identifiedCompounds.forEach(item => {
        const match = item.bestMatch;
        if (match) {
            html += `
                <div class="id-item">
                    <div class="id-peak">Peak ${item.peak.peakNumber}</div>
                    <div class="id-compound">${match.compound}</div>
                    <div class="id-score">${match.matchScore.toFixed(0)}%</div>
                </div>
            `;
        }
    });
    
    html += '</div>';
    container.innerHTML = html;
}

function initializeAnalysisModal() {
    const ctx = document.getElementById('analysis-chart');
    if (!ctx || !AppState.chromatogramData) return;
    
    if (!analysisChart) {
        analysisChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Sample',
                    data: AppState.chromatogramData,
                    borderColor: 'rgb(211, 84, 0)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { type: 'linear', title: { display: true, text: 'Time (min)' } },
                    y: { title: { display: true, text: 'Signal (pA)' }, beginAtZero: true }
                },
                plugins: { legend: { display: false } }
            }
        });
    } else {
        analysisChart.data.datasets[0].data = AppState.chromatogramData;
        analysisChart.update();
    }
    
    // Populate match list
    const matchList = document.getElementById('match-list');
    if (matchList && AppState.identifiedCompounds) {
        matchList.innerHTML = AppState.identifiedCompounds.map((item, i) => `
            <div class="match-item" data-peak="${item.peak.peakNumber}">
                <div>
                    <span class="match-name">Peak ${item.peak.peakNumber}: ${item.bestMatch?.compound || 'Unknown'}</span>
                    <div style="font-size: 0.8em; color: var(--text-muted);">
                        RT: ${item.peak.rt.toFixed(3)} min, Area: ${item.peak.areaPercent.toFixed(1)}%
                    </div>
                </div>
                <span class="match-score">${item.bestMatch?.matchScore.toFixed(0) || '--'}%</span>
            </div>
        `).join('');
        
        // Add click handlers
        matchList.querySelectorAll('.match-item').forEach(item => {
            item.addEventListener('click', () => {
                const peakNum = parseInt(item.dataset.peak);
                showCompoundDetails(peakNum);
            });
        });
    }
}

function showCompoundDetails(peakNumber) {
    const item = AppState.identifiedCompounds.find(i => i.peak.peakNumber === peakNumber);
    if (!item) return;
    
    const container = document.getElementById('compound-details-content');
    if (!container) return;
    
    if (item.bestMatch) {
        const compound = item.bestMatch.data;
        container.innerHTML = `
            <p><strong>Compound:</strong> ${item.bestMatch.compound}</p>
            <p><strong>Formula:</strong> ${compound.formula}</p>
            <p><strong>MW:</strong> ${compound.mw}</p>
            <p><strong>CAS:</strong> ${compound.cas}</p>
            <p><strong>Boiling Point:</strong> ${compound.bp}°C</p>
            <p><strong>Kovats RI:</strong> ${compound.kovatsRI_nonpolar} (non-polar)</p>
            <p><strong>Match Score:</strong> ${item.bestMatch.matchScore.toFixed(1)}%</p>
            <p>${compound.description}</p>
        `;
    } else {
        container.innerHTML = '<p class="no-data">No match found for this peak</p>';
    }
    
    // Highlight selected
    document.querySelectorAll('.match-item').forEach(el => el.classList.remove('selected'));
    document.querySelector(`.match-item[data-peak="${peakNumber}"]`)?.classList.add('selected');
}

// ============================================
// VAN DEEMTER ANALYSIS
// ============================================

function initializeVanDeemterChart() {
    const ctx = document.getElementById('vandeemter-chart');
    if (!ctx) return;
    
    const column = document.getElementById('column-select').value;
    const columnData = ColumnDatabase[column];
    const carrierGas = document.getElementById('carrier-gas').value;
    const currentFlow = parseFloat(document.getElementById('flow-rate').value);
    const temp = 150; // Average temperature
    
    // Generate Van Deemter curve data
    const data = [];
    const bTermData = [];
    const cTermData = [];
    
    for (let u = 5; u <= 100; u += 2) {
        const result = calculateHETP(u, carrierGas, columnData.id, columnData.filmThickness, temp);
        data.push({ x: u, y: result.H * 10 }); // Convert to mm
        bTermData.push({ x: u, y: (result.B / u) * 10 });
        cTermData.push({ x: u, y: ((result.C_g + result.C_s) * u) * 10 });
    }
    
    // Find optimum
    const minH = Math.min(...data.map(p => p.y));
    const optPoint = data.find(p => p.y === minH);
    
    if (vanDeemterChart) {
        vanDeemterChart.destroy();
    }
    
    vanDeemterChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Total HETP',
                    data: data,
                    borderColor: 'rgb(211, 84, 0)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: 'B/u term',
                    data: bTermData,
                    borderColor: 'rgb(52, 152, 219)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: 'Cu term',
                    data: cTermData,
                    borderColor: 'rgb(46, 204, 113)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    title: { display: true, text: 'Linear Velocity (cm/s)' }
                },
                y: {
                    title: { display: true, text: 'HETP (mm)' },
                    min: 0
                }
            },
            plugins: {
                legend: { display: true, position: 'top' },
                annotation: {
                    annotations: {
                        optimum: {
                            type: 'point',
                            xValue: optPoint.x,
                            yValue: optPoint.y,
                            backgroundColor: 'rgb(231, 76, 60)',
                            radius: 6
                        },
                        currentLine: {
                            type: 'line',
                            xMin: calculateLinearVelocity(currentFlow, columnData.id),
                            xMax: calculateLinearVelocity(currentFlow, columnData.id),
                            borderColor: 'rgba(155, 89, 182, 0.8)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'Current',
                                position: 'start'
                            }
                        }
                    }
                }
            }
        }
    });
    
    // Update info display
    const currentVelocity = calculateLinearVelocity(currentFlow, columnData.id);
    const currentHETP = calculateHETP(currentVelocity, carrierGas, columnData.id, columnData.filmThickness, temp);
    
    document.getElementById('optimal-velocity').textContent = `${optPoint.x.toFixed(0)} cm/s`;
    document.getElementById('min-hetp').textContent = `${minH.toFixed(3)} mm`;
    document.getElementById('current-velocity').textContent = `${currentVelocity.toFixed(1)} cm/s`;
    document.getElementById('current-hetp').textContent = `${(currentHETP.H * 10).toFixed(3)} mm`;
    document.getElementById('theoretical-plates').textContent = 
        Math.round(calculatePlates(columnData.length, currentHETP.H)).toLocaleString();
}

function optimizeFlowRate() {
    const column = document.getElementById('column-select').value;
    const columnData = ColumnDatabase[column];
    const carrierGas = document.getElementById('carrier-gas').value;
    
    const optVelocity = calculateOptimalVelocity(carrierGas, columnData.id, columnData.filmThickness, 150);
    const optFlow = calculateFlowRate(optVelocity, columnData.id);
    
    document.getElementById('flow-rate').value = optFlow.toFixed(1);
    updateLinearVelocityDisplay();
    
    showToast('Flow Optimized', `Flow rate set to ${optFlow.toFixed(1)} mL/min for optimal efficiency`, 'success');
    logMessage(`Flow rate optimized to ${optFlow.toFixed(1)} mL/min`);
    
    closeModal('vandeemter-modal');
}

function updateLinearVelocityDisplay() {
    const flow = parseFloat(document.getElementById('flow-rate').value) || 1.0;
    const column = document.getElementById('column-select').value;
    const columnData = ColumnDatabase[column];
    
    const velocity = calculateLinearVelocity(flow, columnData.id);
    document.getElementById('linear-velocity').textContent = `Linear velocity: ~${velocity.toFixed(0)} cm/sec`;
}

// ============================================
// LIBRARY BROWSER
// ============================================

function populateLibraryList(filter = 'all') {
    const compoundList = document.getElementById('compound-list');
    if (!compoundList) return;
    
    const compounds = Object.entries(CompoundDatabase)
        .filter(([name, data]) => filter === 'all' || data.category === filter)
        .sort((a, b) => a[1].bp - b[1].bp);
    
    compoundList.innerHTML = compounds.map(([name]) => `
        <div class="compound-item" data-compound="${name}">${name}</div>
    `).join('');
    
    // Add click handlers
    compoundList.querySelectorAll('.compound-item').forEach(item => {
        item.addEventListener('click', () => previewLibraryCompound(item.dataset.compound));
    });
}

function previewLibraryCompound(compoundName) {
    const compound = CompoundDatabase[compoundName];
    if (!compound) return;
    
    // Highlight selected
    document.querySelectorAll('.compound-item').forEach(item => {
        item.classList.toggle('selected', item.dataset.compound === compoundName);
    });
    
    // Update preview name
    document.getElementById('preview-compound-name').textContent = compoundName;
    
    // Update compound info
    document.getElementById('compound-info').innerHTML = `
        <p><strong>Formula:</strong> ${compound.formula}</p>
        <p><strong>MW:</strong> ${compound.mw}</p>
        <p><strong>CAS:</strong> ${compound.cas}</p>
        <p><strong>Boiling Point:</strong> ${compound.bp}°C</p>
        <p><strong>Category:</strong> ${compound.category}</p>
        <p><strong>Kovats RI (non-polar):</strong> ${compound.kovatsRI_nonpolar}</p>
        <p><strong>Kovats RI (polar):</strong> ${compound.kovatsRI_polar}</p>
        <p><strong>FID Response:</strong> ${compound.fidResponse}</p>
        <p>${compound.description}</p>
    `;
    
    // Generate preview chromatogram (single compound)
    const column = document.getElementById('column-select').value;
    const tempProgram = getTemperatureProgram();
    const carrierGas = document.getElementById('carrier-gas').value;
    const flowRate = parseFloat(document.getElementById('flow-rate').value);
    
    const result = generateChromatogram(compoundName, column, tempProgram, carrierGas, flowRate, 1, 50, 20);
    
    // Update preview chart
    const ctx = document.getElementById('library-preview-chart');
    if (!ctx) return;
    
    if (!libraryPreviewChart) {
        libraryPreviewChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: compoundName,
                    data: result.chromatogram,
                    borderColor: 'rgb(211, 84, 0)',
                    borderWidth: 1.5,
                    pointRadius: 0,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { type: 'linear', display: false },
                    y: { display: false, beginAtZero: true }
                },
                plugins: { legend: { display: false } }
            }
        });
    } else {
        libraryPreviewChart.data.datasets[0].data = result.chromatogram;
        libraryPreviewChart.data.datasets[0].label = compoundName;
        libraryPreviewChart.update();
    }
    
    // Enable load as reference button
    document.getElementById('load-reference').disabled = false;
}

// ============================================
// REPORT GENERATION
// ============================================

function generateReport() {
    // Populate report fields
    document.getElementById('report-sample-id').textContent = AppState.sampleId || '--';
    document.getElementById('report-sample-name').textContent = AppState.sampleName || '--';
    document.getElementById('report-datetime').textContent = formatDate(new Date());
    
    const column = document.getElementById('column-select').value;
    const columnData = ColumnDatabase[column];
    document.getElementById('report-column').textContent = 
        `${column} (${columnData.length}m × ${columnData.id}mm × ${columnData.filmThickness}µm)`;
    document.getElementById('report-carrier').textContent = 
        document.getElementById('carrier-gas').value.charAt(0).toUpperCase() + 
        document.getElementById('carrier-gas').value.slice(1);
    document.getElementById('report-injection').textContent = 
        document.getElementById('injection-mode').value + 
        (document.getElementById('injection-mode').value.includes('split') ? 
            ` (${document.getElementById('split-ratio').value}:1)` : '');
    document.getElementById('report-detector').textContent = document.getElementById('detector-type').value;
    document.getElementById('report-inlet-temp').textContent = 
        document.getElementById('inlet-temp').value + '°C';
    document.getElementById('report-detector-temp').textContent = 
        document.getElementById('detector-temp').value + '°C';
    
    // Temperature program
    const tempProgram = getTemperatureProgram();
    let programText = `Initial: ${tempProgram[0].temp}°C, hold ${tempProgram[0].hold} min`;
    for (let i = 1; i < tempProgram.length; i++) {
        programText += `<br>Ramp ${tempProgram[i].rate}°C/min to ${tempProgram[i].temp}°C, hold ${tempProgram[i].hold} min`;
    }
    document.getElementById('report-temp-program').innerHTML = programText;
    
    // Generate report chart
    const ctx = document.getElementById('report-chart');
    if (ctx && AppState.chromatogramData) {
        if (reportChart) {
            reportChart.destroy();
        }
        
        reportChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: AppState.sampleName,
                    data: AppState.chromatogramData,
                    borderColor: 'rgb(211, 84, 0)',
                    borderWidth: 1.5,
                    pointRadius: 0,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                scales: {
                    x: {
                        type: 'linear',
                        title: { display: true, text: 'Time (min)', font: { size: 10 } }
                    },
                    y: {
                        title: { display: true, text: 'Signal (pA)', font: { size: 10 } },
                        beginAtZero: true
                    }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
    
    // Peak table
    const peakTable = document.getElementById('report-peak-table');
    if (peakTable) {
        if (AppState.peaksIntegrated && AppState.peaksIntegrated.length > 0) {
            let tableHtml = `
                <table class="report-table" style="width: 100%;">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>RT (min)</th>
                            <th>Area</th>
                            <th>Area %</th>
                            <th>Height</th>
                            <th>Compound</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            AppState.peaksIntegrated.forEach((peak, i) => {
                const id = AppState.identifiedCompounds?.find(c => c.peak.peakNumber === peak.peakNumber);
                const compound = id?.bestMatch?.compound || 'Unknown';
                
                tableHtml += `
                    <tr>
                        <td>${peak.peakNumber}</td>
                        <td>${peak.rt.toFixed(3)}</td>
                        <td>${peak.area.toFixed(0)}</td>
                        <td>${peak.areaPercent.toFixed(2)}%</td>
                        <td>${peak.height.toFixed(1)}</td>
                        <td>${compound}</td>
                    </tr>
                `;
            });
            
            tableHtml += '</tbody></table>';
            peakTable.innerHTML = tableHtml;
        } else {
            peakTable.innerHTML = '<p class="no-data">No peaks detected</p>';
        }
    }
    
    openModal('report-modal');
}

// ============================================
// EXPORT FUNCTIONALITY
// ============================================

function exportData(format) {
    if (!AppState.chromatogramData) {
        showToast('Export Error', 'No chromatogram data to export', 'error');
        return;
    }
    
    let content = '';
    let filename = `${AppState.sampleName || 'chromatogram'}_${Date.now()}`;
    let mimeType = 'text/plain';
    
    const includeMetadata = document.getElementById('export-include-metadata')?.checked;
    const includePeaks = document.getElementById('export-include-peaks')?.checked;
    const includeMethod = document.getElementById('export-include-method')?.checked;
    
    switch (format) {
        case 'csv':
            content = 'Time (min),Signal (pA)\n';
            AppState.chromatogramData.forEach(p => {
                content += `${p.x.toFixed(4)},${p.y.toFixed(4)}\n`;
            });
            filename += '.csv';
            mimeType = 'text/csv';
            break;
            
        case 'txt':
            if (includeMetadata) {
                content = `Sample: ${AppState.sampleName}\n`;
                content += `Date: ${formatDate(new Date())}\n`;
                content += `Column: ${document.getElementById('column-select').value}\n`;
                content += `Carrier Gas: ${document.getElementById('carrier-gas').value}\n\n`;
            }
            content += 'Time (min)\tSignal (pA)\n';
            AppState.chromatogramData.forEach(p => {
                content += `${p.x.toFixed(4)}\t${p.y.toFixed(4)}\n`;
            });
            filename += '.txt';
            break;
            
        case 'json':
            const jsonData = {
                sample: AppState.sampleName,
                sampleId: AppState.sampleId,
                date: new Date().toISOString(),
                chromatogram: AppState.chromatogramData
            };
            
            if (includeMethod) {
                jsonData.method = {
                    column: document.getElementById('column-select').value,
                    carrierGas: document.getElementById('carrier-gas').value,
                    flowRate: parseFloat(document.getElementById('flow-rate').value),
                    injectionMode: document.getElementById('injection-mode').value,
                    splitRatio: parseFloat(document.getElementById('split-ratio').value),
                    tempProgram: getTemperatureProgram(),
                    detector: document.getElementById('detector-type').value
                };
            }
            
            if (includePeaks && AppState.peaksIntegrated) {
                jsonData.peaks = AppState.peaksIntegrated;
            }
            
            content = JSON.stringify(jsonData, null, 2);
            filename += '.json';
            mimeType = 'application/json';
            break;
            
        case 'aia':
            // Simplified AIA/ANDI format (CDF-like header + data)
            content = `##TITLE=${AppState.sampleName || 'Unknown'}\n`;
            content += `##DATA TYPE=GAS CHROMATOGRAM\n`;
            content += `##ORIGIN=SimuPharma GC Digital Twin\n`;
            content += `##DATE=${new Date().toISOString().split('T')[0]}\n`;
            content += `##XUNITS=MINUTES\n`;
            content += `##YUNITS=PICOAMPERES\n`;
            content += `##NPOINTS=${AppState.chromatogramData.length}\n`;
            content += `##XYDATA=(X++(Y..Y))\n`;
            AppState.chromatogramData.forEach(p => {
                content += `${p.x.toFixed(4)} ${p.y.toFixed(4)}\n`;
            });
            content += `##END=\n`;
            filename += '.aia';
            break;
    }
    
    // Create and trigger download
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    closeModal('export-modal');
    showToast('Export Complete', `Chromatogram exported as ${format.toUpperCase()}`, 'success');
    logMessage(`Chromatogram exported: ${filename}`);
}

// ============================================
// UI CONTROL FUNCTIONS
// ============================================

function enableAnalysisButtons() {
    document.getElementById('integrate-button').disabled = false;
    document.getElementById('identify-button').disabled = false;
    document.getElementById('report-button').disabled = false;
    document.getElementById('toolbar-save').disabled = false;
    document.getElementById('toolbar-export').disabled = false;
    document.getElementById('toolbar-print').disabled = false;
    document.getElementById('toolbar-overlay').disabled = false;
    document.getElementById('toolbar-integrate').disabled = false;
    document.getElementById('add-comparison-tab').disabled = false;
}

function updateColumnSpecs() {
    const column = document.getElementById('column-select').value;
    const columnData = ColumnDatabase[column];
    
    if (columnData) {
        document.getElementById('column-dimensions').textContent = 
            `${columnData.length}m × ${columnData.id}mm × ${columnData.filmThickness}µm`;
        document.getElementById('column-max-temp').textContent = `${columnData.maxTemp}°C`;
    }
    
    updateLinearVelocityDisplay();
}

function updateDetectorSettings() {
    const detector = document.getElementById('detector-type').value;
    
    // Show/hide detector-specific settings
    document.getElementById('fid-settings').classList.toggle('hidden', detector !== 'FID');
    document.getElementById('tcd-settings').classList.toggle('hidden', detector !== 'TCD');
    
    // Update flame status
    const flameStatus = document.getElementById('flame-status');
    if (flameStatus) {
        if (detector === 'FID') {
            flameStatus.classList.remove('hidden', 'off');
        } else {
            flameStatus.classList.add('off');
        }
    }
}

function updateInjectionModeSettings() {
    const mode = document.getElementById('injection-mode').value;
    const splitGroup = document.getElementById('split-ratio-group');
    
    if (splitGroup) {
        splitGroup.classList.toggle('hidden', mode.includes('splitless'));
    }
}

function updateOvenModeSettings() {
    const mode = document.getElementById('oven-mode').value;
    
    document.getElementById('isothermal-settings').classList.toggle('hidden', mode !== 'isothermal');
    document.getElementById('program-settings').classList.toggle('hidden', mode === 'isothermal');
    
    if (mode === 'isothermal') {
        updateTempProfileChart();
    }
}

function addTemperatureRamp() {
    const table = document.getElementById('temp-program-table');
    const rows = table.querySelectorAll('.program-row:not(.header-row)');
    const lastRow = rows[rows.length - 1];
    const lastTemp = parseFloat(lastRow.querySelector('.temp-input').value) || 150;
    const rampNum = rows.length;
    
    const newRow = document.createElement('div');
    newRow.className = 'program-row';
    newRow.dataset.ramp = rampNum;
    newRow.innerHTML = `
        <input type="number" class="rate-input" value="10" min="1" max="50">
        <input type="number" class="temp-input" value="${Math.min(lastTemp + 50, 350)}" min="30" max="350">
        <input type="number" class="hold-input" value="0" min="0" max="60" step="0.5">
        <button class="btn-icon-sm remove-ramp" title="Remove"><i class="fas fa-times"></i></button>
    `;
    
    table.appendChild(newRow);
    
    // Add remove handler
    newRow.querySelector('.remove-ramp').addEventListener('click', () => {
        newRow.remove();
        updateTempProfileChart();
    });
    
    // Add input change handlers
    newRow.querySelectorAll('input').forEach(input => {
        input.addEventListener('change', updateTempProfileChart);
    });
    
    updateTempProfileChart();
}

// ============================================
// SETTINGS MANAGEMENT
// ============================================

function loadSettings() {
    const saved = localStorage.getItem('gc-settings');
    if (saved) {
        try {
            AppState.settings = { ...AppState.settings, ...JSON.parse(saved) };
        } catch (e) {
            console.error('Error loading settings:', e);
        }
    }
    applySettings();
}

function saveSettings() {
    // Gather settings from form
    AppState.settings.theme = document.getElementById('theme-select').value;
    AppState.settings.lineWidth = parseInt(document.getElementById('line-width').value);
    AppState.settings.showGrid = document.getElementById('show-grid').checked;
    AppState.settings.autoScale = document.getElementById('auto-scale').checked;
    AppState.settings.simSpeed = document.getElementById('sim-speed').value;
    AppState.settings.noiseLevel = document.getElementById('noise-level').value;
    AppState.settings.showRealtime = document.getElementById('show-realtime').checked;
    AppState.settings.integrationMethod = document.getElementById('integration-method').value;
    AppState.settings.areaCalc = document.getElementById('area-calc').value;
    AppState.settings.soundEffects = document.getElementById('sound-effects').checked;
    AppState.settings.showHints = document.getElementById('show-hints').checked;
    
    localStorage.setItem('gc-settings', JSON.stringify(AppState.settings));
    applySettings();
    closeModal('settings-modal');
    showToast('Settings Saved', 'Your preferences have been saved', 'success');
}

function applySettings() {
    // Apply theme
    document.body.setAttribute('data-theme', AppState.settings.theme);
    
    // Update chart if exists
    if (mainChart) {
        mainChart.data.datasets[0].borderWidth = AppState.settings.lineWidth;
        mainChart.options.scales.x.grid.display = AppState.settings.showGrid;
        mainChart.options.scales.y.grid.display = AppState.settings.showGrid;
        mainChart.update();
    }
    
    // Update form values
    if (document.getElementById('theme-select')) {
        document.getElementById('theme-select').value = AppState.settings.theme;
        document.getElementById('line-width').value = AppState.settings.lineWidth;
        document.getElementById('show-grid').checked = AppState.settings.showGrid;
        document.getElementById('auto-scale').checked = AppState.settings.autoScale;
        document.getElementById('sim-speed').value = AppState.settings.simSpeed;
        document.getElementById('noise-level').value = AppState.settings.noiseLevel;
        document.getElementById('show-realtime').checked = AppState.settings.showRealtime;
        document.getElementById('integration-method').value = AppState.settings.integrationMethod;
        document.getElementById('area-calc').value = AppState.settings.areaCalc;
        document.getElementById('sound-effects').checked = AppState.settings.soundEffects;
        document.getElementById('show-hints').checked = AppState.settings.showHints;
    }
}

function resetSettings() {
    AppState.settings = {
        theme: 'light',
        lineWidth: 2,
        showGrid: true,
        autoScale: true,
        simSpeed: 'normal',
        noiseLevel: 'low',
        showRealtime: true,
        integrationMethod: 'auto',
        areaCalc: 'percent',
        soundEffects: false,
        showHints: true
    };
    applySettings();
    showToast('Settings Reset', 'All settings restored to defaults', 'info');
}

// ============================================
// DIAGNOSTICS
// ============================================

async function runLeakTest() {
    showToast('Leak Test', 'Running electronic leak test...', 'info');
    
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    showToast('Leak Test Passed', 'No leaks detected', 'success');
    logMessage('Leak test: PASSED - No leaks detected', 'success');
}

async function runBaselineTest() {
    showToast('Baseline Test', 'Measuring baseline stability...', 'info');
    
    await new Promise(resolve => setTimeout(resolve, 4000));
    
    showToast('Baseline Test', 'Baseline noise: 0.5 pA RMS', 'success');
    logMessage('Baseline test: Noise = 0.5 pA RMS', 'success');
}

async function runSystemCheckout() {
    showToast('System Checkout', 'Running comprehensive checkout...', 'info');
    
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    showToast('Checkout Complete', 'All systems passed', 'success');
    logMessage('System checkout: All components OK', 'success');
}

// ============================================
// TIME & SESSION MANAGEMENT
// ============================================

function updateDateTime() {
    const now = new Date();
    const dtElement = document.getElementById('current-datetime');
    if (dtElement) {
        dtElement.textContent = formatDate(now);
    }
    
    const sessionDuration = Date.now() - AppState.sessionStartTime;
    const sessionElement = document.getElementById('session-time');
    if (sessionElement) {
        sessionElement.textContent = `Session: ${formatSessionTime(sessionDuration)}`;
    }
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

function handleKeyboardShortcuts(e) {
    // Only handle shortcuts when in software view and not in input
    if (AppState.currentView !== 'software') return;
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;
    
    // Ctrl combinations
    if (e.ctrlKey) {
        switch (e.key.toLowerCase()) {
            case 'r':
                e.preventDefault();
                if (!AppState.isRunning) {
                    startRun();
                }
                break;
            case 'i':
                e.preventDefault();
                if (AppState.chromatogramData) {
                    performIntegration();
                }
                break;
            case 'd':
                e.preventDefault();
                if (AppState.peaksIntegrated?.length > 0) {
                    performIdentification();
                }
                break;
            case 'p':
                e.preventDefault();
                if (AppState.chromatogramData) {
                    generateReport();
                }
                break;
        }
    }
    
    // Simple key shortcuts
    if (!e.ctrlKey && !e.altKey) {
        switch (e.key) {
            case '+':
            case '=':
                if (mainChart) mainChart.zoom(1.2);
                break;
            case '-':
                if (mainChart) mainChart.zoom(0.8);
                break;
            case 'Home':
                resetChartZoom();
                break;
            case 'Escape':
                if (AppState.isRunning) {
                    abortRun();
                } else {
                    closeAllModals();
                }
                break;
        }
    }
}
// ============================================
// CONTEXT MENU
// ============================================

function initializeContextMenu() {
    const contextMenu = document.getElementById('context-menu');
    const chartArea = document.getElementById('main-chart-area');

    if (!contextMenu || !chartArea) return;

    // Open Menu on right-click
    chartArea.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        
        // Only show if we have data
        if (!AppState.chromatogramData || AppState.chromatogramData.length === 0) return;

        contextMenu.style.top = `${e.clientY}px`;
        contextMenu.style.left = `${e.clientX}px`;
        contextMenu.classList.remove('hidden');
        
        // Store click position for actions
        AppState.lastContextClick = { x: e.clientX, y: e.clientY };
    });

    // Close Menu on click elsewhere
    document.addEventListener('click', (e) => {
        if (!contextMenu.contains(e.target)) {
            contextMenu.classList.add('hidden');
        }
    });

    // Handle Menu Actions
    contextMenu.addEventListener('click', (e) => {
        const li = e.target.closest('li');
        if (!li) return;
        
        const action = li.dataset.action;
        if (!action) return;

        contextMenu.classList.add('hidden');

        switch (action) {
            case 'zoom-region':
                if (mainChart) mainChart.zoom(1.5);
                break;
            case 'integrate-peak':
                integrateAtClick();
                break;
            case 'add-annotation':
                addAnnotationAtClick();
                break;
            case 'identify-peak':
                identifyPeakAtClick();
                break;
            case 'copy-value':
                copyValueToClipboard();
                break;
            case 'show-baseline':
                toggleBaselineDisplay();
                break;
            case 'reset-zoom':
                resetChartZoom();
                break;
        }
    });
}

function integrateAtClick() {
    if (!mainChart || !AppState.lastContextClick) return;

    const rect = document.getElementById('gc-chart').getBoundingClientRect();
    const x = AppState.lastContextClick.x - rect.left;
    const clickTime = mainChart.scales.x.getValueForPixel(x);

    // Find nearest peak
    if (AppState.peaksIntegrated && AppState.peaksIntegrated.length > 0) {
        const nearest = AppState.peaksIntegrated.reduce((prev, curr) => {
            return (Math.abs(curr.rt - clickTime) < Math.abs(prev.rt - clickTime) ? curr : prev);
        });

        if (Math.abs(nearest.rt - clickTime) < 0.5) {
            highlightPeak(nearest.peakNumber);
            showToast('Peak Selected', `Peak ${nearest.peakNumber} at ${nearest.rt.toFixed(3)} min`, 'info');
        } else {
            showToast('No Peak', 'No integrated peak found at this location', 'warning');
        }
    } else {
        showToast('No Peaks', 'Please run integration first', 'warning');
    }
}

function addAnnotationAtClick() {
    if (!mainChart || !AppState.lastContextClick) return;
    
    const rect = document.getElementById('gc-chart').getBoundingClientRect();
    const x = AppState.lastContextClick.x - rect.left;
    const y = AppState.lastContextClick.y - rect.top;
    
    const xValue = mainChart.scales.x.getValueForPixel(x);
    const yValue = mainChart.scales.y.getValueForPixel(y);
    
    const label = prompt('Enter annotation text:', '');
    if (label) {
        // Add annotation to chart
        if (!mainChart.options.plugins.annotation) {
            mainChart.options.plugins.annotation = { annotations: {} };
        }
        
        const annotationId = `annotation_${Date.now()}`;
        mainChart.options.plugins.annotation.annotations[annotationId] = {
            type: 'label',
            xValue: xValue,
            yValue: yValue,
            content: label,
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            borderColor: 'rgb(211, 84, 0)',
            borderWidth: 1,
            borderRadius: 4,
            padding: 4,
            font: { size: 11 }
        };
        
        mainChart.update();
        showToast('Annotation Added', `"${label}" at ${xValue.toFixed(2)} min`, 'success');
    }
}

function identifyPeakAtClick() {
    if (!mainChart || !AppState.lastContextClick) return;

    const rect = document.getElementById('gc-chart').getBoundingClientRect();
    const x = AppState.lastContextClick.x - rect.left;
    const clickTime = mainChart.scales.x.getValueForPixel(x);

    // Find nearest peak and show identification
    if (AppState.identifiedCompounds && AppState.identifiedCompounds.length > 0) {
        const nearest = AppState.identifiedCompounds.reduce((prev, curr) => {
            return (Math.abs(curr.peak.rt - clickTime) < Math.abs(prev.peak.rt - clickTime) ? curr : prev);
        });

        if (Math.abs(nearest.peak.rt - clickTime) < 0.5 && nearest.bestMatch) {
            showToast('Compound Identified', 
                `${nearest.bestMatch.compound} (${nearest.bestMatch.matchScore.toFixed(0)}% match)`, 
                'success');
        } else {
            showToast('Unknown', 'No identification available for this peak', 'info');
        }
    } else {
        showToast('No Data', 'Please run identification first', 'warning');
    }
}

function copyValueToClipboard() {
    if (!mainChart || !AppState.lastContextClick) return;
    
    const rect = document.getElementById('gc-chart').getBoundingClientRect();
    const x = AppState.lastContextClick.x - rect.left;
    const y = AppState.lastContextClick.y - rect.top;
    
    const xValue = mainChart.scales.x.getValueForPixel(x);
    const yValue = mainChart.scales.y.getValueForPixel(y);
    
    const text = `${xValue.toFixed(4)} min, ${yValue.toFixed(2)} pA`;
    
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied', 'Data copied to clipboard', 'success');
    }).catch(() => {
        showToast('Error', 'Failed to copy to clipboard', 'error');
    });
}

function toggleBaselineDisplay() {
    if (!mainChart || !AppState.chromatogramData) return;
    
    // Check if baseline dataset exists
    const baselineIdx = mainChart.data.datasets.findIndex(d => d.label === 'Baseline');
    
    if (baselineIdx >= 0) {
        // Remove baseline
        mainChart.data.datasets.splice(baselineIdx, 1);
        showToast('Baseline Hidden', 'Baseline display removed', 'info');
    } else {
        // Add baseline
        const baseline = calculateBaseline(AppState.chromatogramData);
        const baselineData = AppState.chromatogramData.map((p, i) => ({
            x: p.x,
            y: baseline[i]
        }));
        
        mainChart.data.datasets.push({
            label: 'Baseline',
            data: baselineData,
            borderColor: 'rgb(108, 117, 125)',
            borderWidth: 1,
            borderDash: [4, 4],
            pointRadius: 0,
            fill: false
        });
        showToast('Baseline Shown', 'Baseline display added', 'info');
    }
    
    mainChart.update();
}

// ============================================
// TUTORIAL SYSTEM
// ============================================

const Tutorial = {
    steps: [
        { 
            id: 'hotspot-injector', 
            title: 'Injection Port', 
            text: 'This is where samples are introduced into the GC. The injection port vaporizes liquid samples instantly for introduction to the column.' 
        },
        { 
            id: 'hotspot-oven', 
            title: 'Column Oven', 
            text: 'The oven precisely controls the column temperature. Temperature programming allows separation of compounds with different boiling points.' 
        },
        { 
            id: 'hotspot-detector', 
            title: 'FID Detector', 
            text: 'The Flame Ionization Detector burns organic compounds and measures the resulting ions. It\'s sensitive to most carbon-containing compounds.' 
        },
        { 
            id: 'hotspot-screen', 
            title: 'Instrument Control', 
            text: 'Click here to access the ChemStation software where you can set up methods, run samples, and analyze results.' 
        },
        { 
            id: 'start-run-button', 
            title: 'Start a Run', 
            text: 'After setting your method parameters, click "Start Run" to begin the chromatographic analysis.' 
        },
        {
            id: 'integrate-button',
            title: 'Peak Integration',
            text: 'After a run completes, use this button to automatically detect and integrate all peaks in the chromatogram.'
        }
    ],
    current: 0,

    start() {
        this.current = 0;
        const overlay = document.getElementById('tutorial-overlay');
        if (overlay) {
            overlay.classList.remove('hidden');
            this.showStep();
        }
        
        // Bind tutorial buttons
        document.getElementById('tutorial-next').onclick = () => this.next();
        document.getElementById('tutorial-skip').onclick = () => this.end();
    },

    showStep() {
        if (this.current >= this.steps.length) {
            this.end();
            return;
        }

        const step = this.steps[this.current];
        const target = document.getElementById(step.id);
        
        // Auto-switch view if target is not visible
        if (!target || target.offsetParent === null) {
            if (['start-run-button', 'integrate-button'].includes(step.id)) {
                switchView('software');
                setTimeout(() => this.showStep(), 300);
                return;
            } else if (step.id.startsWith('hotspot-')) {
                switchView('main');
                setTimeout(() => this.showStep(), 300);
                return;
            }
        }

        if (target) {
            this.positionOverlay(target);
            document.getElementById('tutorial-title').textContent = step.title;
            document.getElementById('tutorial-text').textContent = step.text;
            document.getElementById('tutorial-step-indicator').textContent = 
                `Step ${this.current + 1} of ${this.steps.length}`;
            
            // Update button text for last step
            document.getElementById('tutorial-next').textContent = 
                this.current === this.steps.length - 1 ? 'Finish' : 'Next';
        }
    },

    positionOverlay(target) {
        const rect = target.getBoundingClientRect();
        const spotlight = document.querySelector('.tutorial-spotlight');
        const tooltip = document.querySelector('.tutorial-tooltip');
        const padding = 10;

        if (spotlight) {
            spotlight.style.top = `${rect.top - padding}px`;
            spotlight.style.left = `${rect.left - padding}px`;
            spotlight.style.width = `${rect.width + padding * 2}px`;
            spotlight.style.height = `${rect.height + padding * 2}px`;
        }

        if (tooltip) {
            // Position tooltip below or above depending on space
            const spaceBelow = window.innerHeight - rect.bottom;
            const spaceAbove = rect.top;
            
            if (spaceBelow > 220 || spaceBelow > spaceAbove) {
                tooltip.style.top = `${rect.bottom + 20}px`;
            } else {
                tooltip.style.top = `${rect.top - 200}px`;
            }
            
            // Center horizontally, but keep on screen
            let leftPos = rect.left + (rect.width / 2) - 200;
            leftPos = Math.max(20, Math.min(window.innerWidth - 420, leftPos));
            tooltip.style.left = `${leftPos}px`;
        }
    },

    next() {
        this.current++;
        this.showStep();
    },

    end() {
        document.getElementById('tutorial-overlay')?.classList.add('hidden');
        showToast('Tutorial Complete', 'You\'re ready to start using the GC!', 'success');
    }
};

// ============================================
// SYSTEM SUITABILITY TEST (SST)
// ============================================

async function runSystemSuitabilityTest() {
    showToast('SST Started', 'Running system suitability test...', 'info');
    
    // Set up SST method (use a standard compound)
    document.getElementById('sample-select').value = 'BTEX Mix';
    
    // Start a run
    await startRun();
    
    // Wait for run to complete
    await new Promise(resolve => {
        const checkInterval = setInterval(() => {
            if (!AppState.isRunning) {
                clearInterval(checkInterval);
                resolve();
            }
        }, 500);
    });
    
    // Analyze SST results
    performIntegration();
    
    // Calculate SST parameters
    calculateSSTParameters();
}

function calculateSSTParameters() {
    if (!AppState.peaksIntegrated || AppState.peaksIntegrated.length < 2) {
        showToast('SST Failed', 'Insufficient peaks for SST', 'error');
        return;
    }
    
    const peaks = AppState.peaksIntegrated;
    const deadTime = 0.5; // Approximate
    
    // Resolution between first two major peaks
    const Rs = calculateResolution(peaks[0].rt, peaks[1].rt, peaks[0].widthBase, peaks[1].widthBase);
    document.getElementById('sst-resolution').textContent = Rs.toFixed(2);
    document.getElementById('sst-resolution-status').innerHTML = Rs >= 2.0 ? 
        '<span class="text-success">PASS</span>' : '<span class="text-danger">FAIL</span>';
    
    // Tailing factor (use first peak)
    const tailing = peaks[0].asymmetry;
    document.getElementById('sst-tailing').textContent = tailing.toFixed(2);
    document.getElementById('sst-tailing-status').innerHTML = tailing <= 2.0 ? 
        '<span class="text-success">PASS</span>' : '<span class="text-danger">FAIL</span>';
    
    // Theoretical plates
    const plates = peaks[0].plates;
    document.getElementById('sst-plates').textContent = plates.toLocaleString();
    document.getElementById('sst-plates-status').innerHTML = plates >= 2000 ? 
        '<span class="text-success">PASS</span>' : '<span class="text-danger">FAIL</span>';
    
    // Capacity factor
    const k = (peaks[0].rt - deadTime) / deadTime;
    document.getElementById('sst-capacity').textContent = k.toFixed(2);
    document.getElementById('sst-capacity-status').innerHTML = k >= 2.0 ? 
        '<span class="text-success">PASS</span>' : '<span class="text-danger">FAIL</span>';
    
    // For RSD, we'd need replicate injections - simulate values
    document.getElementById('sst-rsd-area').textContent = '0.8%';
    document.getElementById('sst-rsd-area-status').innerHTML = '<span class="text-success">PASS</span>';
    
    document.getElementById('sst-rsd-rt').textContent = '0.3%';
    document.getElementById('sst-rsd-rt-status').innerHTML = '<span class="text-success">PASS</span>';
    
    // Overall status
    const allPass = Rs >= 2.0 && tailing <= 2.0 && plates >= 2000 && k >= 2.0;
    const overall = document.getElementById('sst-overall');
    overall.className = `sst-overall ${allPass ? 'pass' : 'fail'}`;
    overall.innerHTML = allPass ? 
        '<i class="fas fa-check-circle"></i> <strong>SYSTEM SUITABILITY: PASSED</strong>' :
        '<i class="fas fa-times-circle"></i> <strong>SYSTEM SUITABILITY: FAILED</strong>';
    
    document.getElementById('export-sst').disabled = false;
    
    logMessage(`SST ${allPass ? 'PASSED' : 'FAILED'}`, allPass ? 'success' : 'error');
}

// ============================================
// FLAME IGNITION ANIMATION
// ============================================

async function showFlameIgnition() {
    const overlay = document.getElementById('flame-overlay');
    if (!overlay) return;
    
    overlay.classList.remove('hidden');
    
    await new Promise(resolve => setTimeout(resolve, 2500));
    
    overlay.classList.add('hidden');
    
    // Update flame status
    const flameStatus = document.getElementById('flame-status');
    if (flameStatus) {
        flameStatus.classList.remove('off');
        flameStatus.innerHTML = '<i class="fas fa-fire"></i><span>Flame: <strong>ON</strong></span>';
    }
    
    showToast('FID Ready', 'Flame ignited successfully', 'success');
    logMessage('FID flame ignited', 'success');
}

// ============================================
// SEQUENCE MANAGEMENT
// ============================================

function addSequenceRow(type = 'sample') {
    const tbody = document.getElementById('sequence-table-body');
    if (!tbody) return;
    
    const rows = tbody.querySelectorAll('tr');
    const vialNum = rows.length + 1;
    
    const defaultName = type === 'blank' ? 'Blank' : 
                        type === 'standard' ? `Standard-${vialNum}` : 
                        `Sample-${String(vialNum).padStart(3, '0')}`;
    
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${vialNum}</td>
        <td><input type="text" value="${defaultName}" class="seq-input"></td>
        <td>
            <select class="seq-select">
                <option value="blank" ${type === 'blank' ? 'selected' : ''}>Blank</option>
                <option value="sample" ${type === 'sample' ? 'selected' : ''}>Sample</option>
                <option value="standard" ${type === 'standard' ? 'selected' : ''}>Standard</option>
                <option value="qc">QC</option>
            </select>
        </td>
        <td>
            <select class="seq-select">
                <option value="default">Default Method</option>
            </select>
        </td>
        <td><input type="number" value="1.0" class="seq-input-sm" step="0.1"></td>
        <td><input type="number" value="1" class="seq-input-sm" min="1" max="10"></td>
        <td>
            <button class="btn-icon-sm remove-seq-row" title="Remove"><i class="fas fa-times"></i></button>
        </td>
    `;
    
    tbody.appendChild(newRow);
    
    // Add remove handler
    newRow.querySelector('.remove-seq-row').addEventListener('click', () => {
        newRow.remove();
        updateSequenceSummary();
    });
    
    updateSequenceSummary();
}

function updateSequenceSummary() {
    const tbody = document.getElementById('sequence-table-body');
    if (!tbody) return;
    
    const rows = tbody.querySelectorAll('tr');
    let totalSamples = rows.length;
    let totalInjections = 0;
    
    rows.forEach(row => {
        const replicates = parseInt(row.querySelector('input[type="number"]:last-of-type')?.value) || 1;
        totalInjections += replicates;
    });
    
    const tempProgram = getTemperatureProgram();
    const runTime = calculateTotalRunTime(tempProgram);
    const totalTime = totalInjections * (runTime + 5); // +5 min for equilibration
    
    document.getElementById('total-samples').textContent = totalSamples;
    document.getElementById('total-injections').textContent = totalInjections;
    document.getElementById('est-sequence-time').textContent = `${totalTime.toFixed(0)} min`;
    
    // Enable start button if we have samples
    document.getElementById('start-sequence').disabled = totalSamples === 0;
}

// ============================================
// METHOD MANAGEMENT
// ============================================

function saveMethod() {
    const name = document.getElementById('method-name').value.trim();
    if (!name) {
        showToast('Error', 'Please enter a method name', 'error');
        return;
    }
    
    const method = {
        name: name,
        description: document.getElementById('method-description').value,
        date: new Date().toISOString(),
        parameters: {
            column: document.getElementById('column-select').value,
            carrierGas: document.getElementById('carrier-gas').value,
            flowRate: parseFloat(document.getElementById('flow-rate').value),
            flowMode: document.getElementById('flow-mode').value,
            injectionMode: document.getElementById('injection-mode').value,
            splitRatio: parseFloat(document.getElementById('split-ratio').value),
            inletTemp: parseFloat(document.getElementById('inlet-temp').value),
            injectionVolume: parseFloat(document.getElementById('injection-volume').value),
            tempProgram: getTemperatureProgram(),
            ovenMode: document.getElementById('oven-mode').value,
            detectorType: document.getElementById('detector-type').value,
            detectorTemp: parseFloat(document.getElementById('detector-temp').value),
            dataRate: parseInt(document.getElementById('data-rate').value)
        }
    };
    
    // Save to localStorage
    let savedMethods = JSON.parse(localStorage.getItem('gc-methods') || '[]');
    savedMethods.push(method);
    localStorage.setItem('gc-methods', JSON.stringify(savedMethods));
    
    closeModal('method-modal');
    showToast('Method Saved', `"${name}" saved successfully`, 'success');
    logMessage(`Method saved: ${name}`);
}

function loadMethod(methodData) {
    const params = methodData.parameters;
    
    document.getElementById('column-select').value = params.column;
    document.getElementById('carrier-gas').value = params.carrierGas;
    document.getElementById('flow-rate').value = params.flowRate;
    document.getElementById('flow-mode').value = params.flowMode;
    document.getElementById('injection-mode').value = params.injectionMode;
    document.getElementById('split-ratio').value = params.splitRatio;
    document.getElementById('inlet-temp').value = params.inletTemp;
    document.getElementById('injection-volume').value = params.injectionVolume;
    document.getElementById('oven-mode').value = params.ovenMode;
    document.getElementById('detector-type').value = params.detectorType;
    document.getElementById('detector-temp').value = params.detectorTemp;
    document.getElementById('data-rate').value = params.dataRate;
    
    // Load temperature program
    loadTemperatureProgram(params.tempProgram);
    
    // Update UI
    updateColumnSpecs();
    updateLinearVelocityDisplay();
    updateDetectorSettings();
    updateInjectionModeSettings();
    updateOvenModeSettings();
    
    closeModal('method-modal');
    showToast('Method Loaded', `"${methodData.name}" loaded`, 'success');
    logMessage(`Method loaded: ${methodData.name}`);
}

function loadTemperatureProgram(program) {
    const table = document.getElementById('temp-program-table');
    
    // Clear existing rows except header
    const existingRows = table.querySelectorAll('.program-row:not(.header-row)');
    existingRows.forEach(row => row.remove());
    
    // Add rows for program
    program.forEach((step, index) => {
        const row = document.createElement('div');
        row.className = 'program-row';
        row.dataset.ramp = index;
        
        if (index === 0) {
            row.innerHTML = `
                <span class="rate-cell">Initial</span>
                <input type="number" class="temp-input" value="${step.temp}" min="30" max="350">
                <input type="number" class="hold-input" value="${step.hold}" min="0" max="60" step="0.5">
                <span></span>
            `;
        } else {
            row.innerHTML = `
                <input type="number" class="rate-input" value="${step.rate}" min="1" max="50">
                <input type="number" class="temp-input" value="${step.temp}" min="30" max="350">
                <input type="number" class="hold-input" value="${step.hold}" min="0" max="60" step="0.5">
                <button class="btn-icon-sm remove-ramp" title="Remove"><i class="fas fa-times"></i></button>
            `;
        }
        
        table.appendChild(row);
        
        // Add event handlers
        if (index > 0) {
            row.querySelector('.remove-ramp').addEventListener('click', () => {
                row.remove();
                updateTempProfileChart();
            });
        }
        
        row.querySelectorAll('input').forEach(input => {
            input.addEventListener('change', updateTempProfileChart);
        });
    });
    
    updateTempProfileChart();
}

function updateMethodPreview() {
    const preview = document.getElementById('method-param-preview');
    if (!preview) return;
    
    const column = document.getElementById('column-select').value;
    const tempProgram = getTemperatureProgram();
    
    preview.innerHTML = `
        <div class="param-preview-row"><span>Column:</span><span>${column}</span></div>
        <div class="param-preview-row"><span>Carrier Gas:</span><span>${document.getElementById('carrier-gas').value}</span></div>
        <div class="param-preview-row"><span>Flow Rate:</span><span>${document.getElementById('flow-rate').value} mL/min</span></div>
        <div class="param-preview-row"><span>Inlet Temp:</span><span>${document.getElementById('inlet-temp').value}°C</span></div>
        <div class="param-preview-row"><span>Injection:</span><span>${document.getElementById('injection-mode').value}</span></div>
        <div class="param-preview-row"><span>Initial Temp:</span><span>${tempProgram[0].temp}°C</span></div>
        <div class="param-preview-row"><span>Final Temp:</span><span>${tempProgram[tempProgram.length-1].temp}°C</span></div>
        <div class="param-preview-row"><span>Run Time:</span><span>${calculateTotalRunTime(tempProgram).toFixed(1)} min</span></div>
        <div class="param-preview-row"><span>Detector:</span><span>${document.getElementById('detector-type').value}</span></div>
    `;
}

// ============================================
// EVENT LISTENERS & INITIALIZATION
// ============================================

function initializeEventListeners() {
    // ========== VIEW SWITCHING ==========
    document.getElementById('hotspot-screen')?.addEventListener('click', () => switchView('software'));
    document.getElementById('quick-new-run')?.addEventListener('click', () => switchView('software'));
    document.getElementById('exit-software-button')?.addEventListener('click', () => switchView('main'));
    
    // ========== MODAL HOTSPOTS ==========
    document.querySelectorAll('.hotspot[data-modal]').forEach(hotspot => {
        hotspot.addEventListener('click', () => {
            openModal(hotspot.dataset.modal);
        });
    });
    
    // ========== MODAL CLOSE BUTTONS ==========
    document.querySelectorAll('.modal-close-btn, .modal-close-button').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal');
            if (modal) closeModal(modal.id);
        });
    });
    
    // Backdrop click to close
    document.getElementById('modal-backdrop')?.addEventListener('click', closeAllModals);
    
    // ========== HEADER BUTTONS ==========
    document.getElementById('help-btn')?.addEventListener('click', () => openModal('help-modal'));
    document.getElementById('settings-btn')?.addEventListener('click', () => openModal('settings-modal'));
    document.getElementById('quick-diagnostics')?.addEventListener('click', () => openModal('diagnostics-modal'));
    document.getElementById('quick-library')?.addEventListener('click', () => openModal('library-modal'));
    document.getElementById('quick-reports')?.addEventListener('click', () => {
        if (AppState.chromatogramData) {
            generateReport();
        } else {
            showToast('No Data', 'Run a sample first', 'warning');
        }
    });
    
    // ========== RUN CONTROL ==========
    document.getElementById('start-run-button')?.addEventListener('click', startRun);
    document.getElementById('abort-run-button')?.addEventListener('click', abortRun);
    
    // ========== ANALYSIS BUTTONS ==========
    document.getElementById('integrate-button')?.addEventListener('click', performIntegration);
    document.getElementById('identify-button')?.addEventListener('click', performIdentification);
    document.getElementById('report-button')?.addEventListener('click', generateReport);
    
    // ========== TOOLBAR BUTTONS ==========
    document.getElementById('toolbar-zoom-in')?.addEventListener('click', () => mainChart?.zoom(1.2));
    document.getElementById('toolbar-zoom-out')?.addEventListener('click', () => mainChart?.zoom(0.8));
    document.getElementById('toolbar-reset-zoom')?.addEventListener('click', resetChartZoom);
    document.getElementById('toolbar-export')?.addEventListener('click', () => openModal('export-modal'));
    document.getElementById('toolbar-print')?.addEventListener('click', generateReport);
    document.getElementById('toolbar-integrate')?.addEventListener('click', performIntegration);
    document.getElementById('toolbar-new')?.addEventListener('click', () => openModal('method-modal'));
    
    // ========== PARAMETER CHANGES ==========
    document.getElementById('column-select')?.addEventListener('change', updateColumnSpecs);
    document.getElementById('flow-rate')?.addEventListener('change', updateLinearVelocityDisplay);
    document.getElementById('carrier-gas')?.addEventListener('change', updateLinearVelocityDisplay);
    document.getElementById('detector-type')?.addEventListener('change', updateDetectorSettings);
    document.getElementById('injection-mode')?.addEventListener('change', updateInjectionModeSettings);
    document.getElementById('oven-mode')?.addEventListener('change', updateOvenModeSettings);
    
    // ========== TEMPERATURE PROGRAM ==========
    document.getElementById('add-ramp-btn')?.addEventListener('click', addTemperatureRamp);
    
    // Initial ramp remove buttons
    document.querySelectorAll('.remove-ramp').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.target.closest('.program-row')?.remove();
            updateTempProfileChart();
        });
    });
    
    // Temperature program input changes
    document.querySelectorAll('#temp-program-table input').forEach(input => {
        input.addEventListener('change', updateTempProfileChart);
    });
    
    // ========== COLLAPSIBLE SECTIONS ==========
    document.querySelectorAll('.section-header').forEach(header => {
        header.addEventListener('click', () => {
            header.closest('.panel-section')?.classList.toggle('collapsed');
        });
    });
    
    // ========== RIGHT PANEL TOGGLE ==========
    document.getElementById('right-panel-toggle')?.addEventListener('click', () => {
        document.getElementById('software-right-panel')?.classList.toggle('collapsed');
    });
    
    // ========== MODAL TABS ==========
    document.querySelectorAll('.info-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const tabGroup = tab.closest('.modal-info, .modal-body');
            tabGroup.querySelectorAll('.info-tab').forEach(t => t.classList.remove('active'));
            tabGroup.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            tabGroup.querySelector(`.tab-content[data-tab="${tab.dataset.tab}"]`)?.classList.add('active');
        });
    });
    
    // Settings tabs
    document.querySelectorAll('.settings-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.settings-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.settings-panel').forEach(p => p.classList.remove('active'));
            tab.classList.add('active');
            document.querySelector(`.settings-panel[data-tab="${tab.dataset.tab}"]`)?.classList.add('active');
        });
    });
    
    // Method tabs
    document.querySelectorAll('.method-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.method-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.method-panel').forEach(p => p.classList.remove('active'));
            tab.classList.add('active');
            document.querySelector(`.method-panel[data-tab="${tab.dataset.tab}"]`)?.classList.add('active');
            
            if (tab.dataset.tab === 'save') {
                updateMethodPreview();
            }
        });
    });
    
    // Help navigation
    document.querySelectorAll('.help-nav-item').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.help-nav-item').forEach(i => i.classList.remove('active'));
            document.querySelectorAll('.help-topic').forEach(t => t.classList.remove('active'));
            item.classList.add('active');
            document.querySelector(`.help-topic[data-topic="${item.dataset.topic}"]`)?.classList.add('active');
        });
    });
    
    // ========== LIBRARY MODAL ==========
    document.querySelectorAll('.library-categories li').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.library-categories li').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            populateLibraryList(item.dataset.category);
        });
    });
    
    document.getElementById('library-search-input')?.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        document.querySelectorAll('.compound-item').forEach(item => {
            const match = item.textContent.toLowerCase().includes(query);
            item.style.display = match ? '' : 'none';
        });
    });
    
    document.getElementById('load-reference')?.addEventListener('click', () => {
        const selected = document.querySelector('.compound-item.selected');
        if (selected && mainChart && AppState.chromatogramData) {
            const compound = selected.dataset.compound;
            const column = document.getElementById('column-select').value;
            const tempProgram = getTemperatureProgram();
            const carrierGas = document.getElementById('carrier-gas').value;
            const flowRate = parseFloat(document.getElementById('flow-rate').value);
            
            const result = generateChromatogram(compound, column, tempProgram, carrierGas, flowRate, 1, 50, 20);
            addReferenceToChart(result.chromatogram, compound);
            
            closeModal('library-modal');
            showToast('Reference Added', `${compound} added as overlay`, 'success');
        }
    });
    
    // ========== SETTINGS ==========
    document.getElementById('save-settings')?.addEventListener('click', saveSettings);
    document.getElementById('cancel-settings')?.addEventListener('click', () => {
        applySettings();
        closeModal('settings-modal');
    });
    document.getElementById('reset-settings')?.addEventListener('click', resetSettings);
    
    // ========== EXPORT ==========
    document.getElementById('confirm-export')?.addEventListener('click', () => {
        const format = document.querySelector('input[name="export-format"]:checked')?.value || 'csv';
        exportData(format);
    });
    document.getElementById('cancel-export')?.addEventListener('click', () => closeModal('export-modal'));
    
    // ========== DIAGNOSTICS ==========
    document.getElementById('run-leak-test')?.addEventListener('click', runLeakTest);
    document.getElementById('run-baseline-test')?.addEventListener('click', runBaselineTest);
    document.getElementById('run-checkout')?.addEventListener('click', runSystemCheckout);
    
    // ========== VAN DEEMTER ==========
    document.getElementById('optimize-flow')?.addEventListener('click', optimizeFlowRate);
    
    // ========== SST ==========
    document.getElementById('run-sst')?.addEventListener('click', runSystemSuitabilityTest);
    
    // ========== SEQUENCE ==========
    document.getElementById('add-sample-row')?.addEventListener('click', () => addSequenceRow('sample'));
    document.getElementById('add-blank-row')?.addEventListener('click', () => addSequenceRow('blank'));
    document.getElementById('add-standard-row')?.addEventListener('click', () => addSequenceRow('standard'));
    
    // ========== METHOD ==========
    document.getElementById('save-method-btn')?.addEventListener('click', saveMethod);
    
    // ========== REPORT ==========
    document.getElementById('print-report')?.addEventListener('click', () => {
        window.print();
    });
    
    // ========== TUTORIAL ==========
    document.getElementById('start-tutorial')?.addEventListener('click', () => {
        closeModal('help-modal');
        Tutorial.start();
    });
    
    // ========== CLEAR LOG ==========
    document.getElementById('clear-log-btn')?.addEventListener('click', () => {
        const logPanel = document.getElementById('gc-log-panel');
        if (logPanel) logPanel.innerHTML = '';
    });
    
    // ========== VIDEO CONTROLS IN MODALS ==========
    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const container = btn.closest('.modal-image-container');
            const video = container?.querySelector('video');
            const staticImg = container?.querySelector('img.static');
            
            if (video) {
                if (video.paused) {
                    video.classList.add('active');
                    video.play();
                    btn.innerHTML = '<i class="fas fa-pause"></i>';
                } else {
                    video.pause();
                    video.classList.remove('active');
                    btn.innerHTML = '<i class="fas fa-play"></i>';
                }
            }
        });
    });
    
    // ========== KEYBOARD SHORTCUTS ==========
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    // ========== WINDOW RESIZE ==========
    window.addEventListener('resize', () => {
        if (mainChart) mainChart.resize();
        if (tempProfileChart) tempProfileChart.resize();
    });
}

// ============================================
// LOADING SCREEN ANIMATION
// ============================================

async function runLoadingSequence() {
    const steps = document.querySelectorAll('.check-item');
    const loadingText = document.querySelector('.loading-text');
    
    const messages = [
        'Checking carrier gas supply...',
        'Heating injection port...',
        'Conditioning column oven...',
        'Igniting FID detector...',
        'System ready!'
    ];
    
    for (let i = 0; i < steps.length; i++) {
        steps[i].classList.add('active');
        if (loadingText) loadingText.textContent = messages[i];
        
        await new Promise(resolve => setTimeout(resolve, 500));
        
        steps[i].classList.remove('active');
        steps[i].classList.add('complete');
    }
    
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Hide loading screen
    document.getElementById('loading-screen')?.classList.add('hidden');
}

// ============================================
// INITIALIZATION
// ============================================

async function initializeApp() {
    // Wait for DOM if needed
    if (document.readyState !== 'complete') {
        await new Promise(resolve => window.addEventListener('load', resolve));
    }
    
    // Run loading animation
    await runLoadingSequence();
    
    // Initialize components
    loadSettings();
    initializeMainChart();
    initializeTempProfileChart();
    initializeEventListeners();
    initializeContextMenu();
    
    // Initial UI updates
    updateColumnSpecs();
    updateLinearVelocityDisplay();
    updateDetectorSettings();
    updateInjectionModeSettings();
    updateTempProfileChart();
    
    // Start timers
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Initial log messages
    logMessage('System initialized and ready');
    logMessage('GC-7890 Digital Twin v2.0');
    logMessage('FID detector at 300°C');
    logMessage('Column oven at 50°C');
    
    // Show welcome toast
    showToast('Welcome', 'SimuPharma GC Digital Twin is ready', 'success');
    
    // Show tutorial hint for first-time users
    if (AppState.settings.showHints && !localStorage.getItem('gc-tutorial-shown')) {
        setTimeout(() => {
            showToast('Tip', 'Click the monitor screen to access the software interface', 'info', 6000);
        }, 2000);
    }
}

// ============================================
// ADDITIONAL HELPER FUNCTIONS
// ============================================

/**
 * Calculate signal-to-noise ratio for a peak
 */
function calculateSignalToNoise(peakHeight, baselineNoise) {
    return peakHeight / (baselineNoise * 2);
}

/**
 * Estimate baseline noise from chromatogram
 */
function estimateBaselineNoise(chromatogram, startTime = 0, endTime = 0.5) {
    const segment = chromatogram.filter(p => p.x >= startTime && p.x <= endTime);
    if (segment.length < 10) return 0.5;
    
    const mean = segment.reduce((sum, p) => sum + p.y, 0) / segment.length;
    const variance = segment.reduce((sum, p) => sum + Math.pow(p.y - mean, 2), 0) / segment.length;
    
    return Math.sqrt(variance);
}

/**
 * Smooth chromatogram data using moving average
 */
function smoothChromatogram(data, windowSize = 5) {
    const result = [];
    const halfWindow = Math.floor(windowSize / 2);
    
    for (let i = 0; i < data.length; i++) {
        let sum = 0;
        let count = 0;
        
        for (let j = -halfWindow; j <= halfWindow; j++) {
            const idx = i + j;
            if (idx >= 0 && idx < data.length) {
                sum += data[idx].y;
                count++;
            }
        }
        
        result.push({ x: data[i].x, y: sum / count });
    }
    
    return result;
}

/**
 * Calculate derivative of chromatogram (for peak detection)
 */
function calculateDerivative(data) {
    const result = [];
    
    for (let i = 1; i < data.length - 1; i++) {
        const dx = data[i + 1].x - data[i - 1].x;
        const dy = data[i + 1].y - data[i - 1].y;
        result.push({ x: data[i].x, y: dy / dx });
    }
    
    return result;
}

/**
 * Find local maxima in data (peak apexes)
 */
function findLocalMaxima(data, threshold = 0) {
    const maxima = [];
    
    for (let i = 1; i < data.length - 1; i++) {
        if (data[i].y > data[i - 1].y && 
            data[i].y > data[i + 1].y && 
            data[i].y > threshold) {
            maxima.push({ index: i, x: data[i].x, y: data[i].y });
        }
    }
    
    return maxima;
}

/**
 * Format area value for display
 */
function formatArea(area) {
    if (area >= 1e6) {
        return (area / 1e6).toFixed(2) + 'M';
    } else if (area >= 1e3) {
        return (area / 1e3).toFixed(2) + 'K';
    } else {
        return area.toFixed(0);
    }
}

/**
 * Validate method parameters before run
 */
function validateMethodParameters() {
    const errors = [];
    
    const column = document.getElementById('column-select').value;
    const columnData = ColumnDatabase[column];
    const tempProgram = getTemperatureProgram();
    const maxTemp = Math.max(...tempProgram.map(s => s.temp));
    
    // Check temperature limits
    if (maxTemp > columnData.maxTemp) {
        errors.push(`Max temperature (${maxTemp}°C) exceeds column limit (${columnData.maxTemp}°C)`);
    }
    
    // Check flow rate
    const flowRate = parseFloat(document.getElementById('flow-rate').value);
    if (flowRate < 0.1 || flowRate > 10) {
        errors.push('Flow rate should be between 0.1 and 10 mL/min');
    }
    
    // Check inlet temperature
    const inletTemp = parseFloat(document.getElementById('inlet-temp').value);
    const maxBP = 400; // Approximate max BP we can handle
    if (inletTemp < 150) {
        errors.push('Inlet temperature may be too low for sample vaporization');
    }
    
    // Check detector temperature
    const detectorTemp = parseFloat(document.getElementById('detector-temp').value);
    if (detectorTemp < maxTemp + 20) {
        errors.push('Detector temperature should be at least 20°C above max oven temperature');
    }
    
    return errors;
}

/**
 * Show confirmation dialog
 */
function showConfirmDialog(title, message) {
    return new Promise((resolve) => {
        const dialog = document.getElementById('confirm-dialog');
        if (!dialog) {
            resolve(false);
            return;
        }
        
        document.getElementById('confirm-title').innerHTML = `<i class="fas fa-question-circle"></i> ${title}`;
        document.getElementById('confirm-message').textContent = message;
        
        openModal('confirm-dialog');
        
        const okBtn = document.getElementById('confirm-ok');
        const cancelBtn = document.getElementById('confirm-cancel');
        
        const handleOk = () => {
            cleanup();
            closeModal('confirm-dialog');
            resolve(true);
        };
        
        const handleCancel = () => {
            cleanup();
            closeModal('confirm-dialog');
            resolve(false);
        };
        
        const cleanup = () => {
            okBtn.removeEventListener('click', handleOk);
            cancelBtn.removeEventListener('click', handleCancel);
        };
        
        okBtn.addEventListener('click', handleOk);
        cancelBtn.addEventListener('click', handleCancel);
    });
}

/**
 * Auto-save current work to localStorage
 */
function autoSave() {
    if (AppState.chromatogramData) {
        const saveData = {
            timestamp: Date.now(),
            sampleName: AppState.sampleName,
            sampleId: AppState.sampleId,
            chromatogramData: AppState.chromatogramData,
            peaksIntegrated: AppState.peaksIntegrated,
            identifiedCompounds: AppState.identifiedCompounds
        };
        
        localStorage.setItem('gc-autosave', JSON.stringify(saveData));
    }
}

/**
 * Check for auto-saved data on startup
 */
function checkAutoSave() {
    const saved = localStorage.getItem('gc-autosave');
    if (saved) {
        try {
            const data = JSON.parse(saved);
            const age = Date.now() - data.timestamp;
            
            // Only offer to restore if less than 24 hours old
            if (age < 24 * 60 * 60 * 1000) {
                showConfirmDialog(
                    'Restore Session',
                    `Found auto-saved data from ${formatDate(new Date(data.timestamp))}. Restore?`
                ).then(restore => {
                    if (restore) {
                        AppState.sampleName = data.sampleName;
                        AppState.sampleId = data.sampleId;
                        AppState.chromatogramData = data.chromatogramData;
                        AppState.peaksIntegrated = data.peaksIntegrated;
                        AppState.identifiedCompounds = data.identifiedCompounds;
                        
                        updateChart(data.chromatogramData, data.sampleName);
                        if (data.peaksIntegrated) {
                            updatePeakTable(data.peaksIntegrated);
                            addPeakAnnotations(data.peaksIntegrated);
                        }
                        enableAnalysisButtons();
                        
                        showToast('Session Restored', 'Previous work has been restored', 'success');
                    } else {
                        localStorage.removeItem('gc-autosave');
                    }
                });
            }
        } catch (e) {
            console.error('Error restoring auto-save:', e);
            localStorage.removeItem('gc-autosave');
        }
    }
}

// Set up auto-save interval (every 30 seconds)
setInterval(autoSave, 30000);

// ============================================
// START THE APPLICATION
// ============================================

document.addEventListener('DOMContentLoaded', initializeApp);

// Also check for auto-save after initialization
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(checkAutoSave, 1500);
});
