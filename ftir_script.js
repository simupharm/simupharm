/**
 * SimuPharma - Advanced FTIR Digital Twin
 * Professional Edition JavaScript
 * Version 2.0 - Complete Implementation
 */

// ============================================
// GLOBAL STATE & CONFIGURATION
// ============================================

const AppState = {
    currentView: 'main',
    backgroundCollected: false,
    backgroundData: null,
    backgroundTime: null,
    sampleData: null,
    sampleName: null,
    sampleId: null,
    isScanning: false,
    measurementMode: 'single',
    displayMode: 'absorbance',
    samplingMode: 'transmission',  // 'transmission' or 'atr'
    atrCrystal: 'diamond',         // 'diamond', 'znse', or 'ge'
    peaksDetected: [],
    functionalGroups: [],
    libraryMatches: [],
    processingApplied: [],
    sessionStartTime: Date.now(),
    settings: {
        theme: 'light',
        lineWidth: 2,
        showGrid: true,
        autoScale: true,
        defaultScans: 16,
        defaultResolution: 4,
        bkgWarning: true,
        baselineMethod: 'linear',
        smoothPoints: 5,
        peakThreshold: 10,
        simSpeed: 'normal',
        soundEffects: false,
        showHints: true
    }
};

// ATR Crystal Database — real optical properties
const ATR_CRYSTALS = {
    diamond: {
        name: 'Diamond (Type IIa)',
        ri: 2.4,          // Refractive index
        rangeMin: 400,     // Spectral range (cm⁻¹)
        rangeMax: 4000,
        angle: 45,         // Angle of incidence (degrees)
        nBounces: 1,       // Number of internal reflections
        description: 'Universal ATR crystal, chemically inert, scratch resistant',
        advantages: 'Widest spectral range, very durable',
        sampleTypes: 'All sample types including hard materials'
    },
    znse: {
        name: 'Zinc Selenide (ZnSe)',
        ri: 2.43,
        rangeMin: 650,     // ZnSe absorbs below 650 cm⁻¹
        rangeMax: 4000,
        angle: 45,
        nBounces: 1,
        description: 'Good for soft materials and liquids',
        advantages: 'Good sensitivity, moderate cost',
        sampleTypes: 'Liquids, soft polymers, biological samples'
    },
    ge: {
        name: 'Germanium (Ge)',
        ri: 4.0,
        rangeMin: 780,     // Ge absorbs below 780 cm⁻¹
        rangeMax: 4000,
        angle: 45,
        nBounces: 1,
        description: 'High RI for strongly absorbing samples',
        advantages: 'Shallow penetration depth, good for dark/opaque samples',
        sampleTypes: 'Carbon black, rubbers, highly absorbing materials'
    }
};

// Simulation timing based on speed setting
const SimTiming = {
    fast: { scan: 50, background: 500, fft: 200 },
    normal: { scan: 150, background: 1500, fft: 500 },
    realistic: { scan: 400, background: 4000, fft: 1000 }
};

// Chart instances
let mainChart = null;
let analysisChart = null;
let libraryPreviewChart = null;
let reportChart = null;
let interferogramChart = null;

// ============================================
// SPECTRAL DATABASE - Realistic FTIR Data
// ============================================

const SpectralDatabase = {
    // Polymers
    'Polystyrene': {
        category: 'polymer',
        formula: '(C8H8)n',
        mw: '~100,000',
        cas: '9003-53-6',
        description: 'Aromatic polymer, standard calibration material',
        peaks: [
            { pos: 3082, int: 0.15, assign: 'Aromatic C-H stretch' },
            { pos: 3060, int: 0.18, assign: 'Aromatic C-H stretch' },
            { pos: 3026, int: 0.22, assign: 'Aromatic C-H stretch' },
            { pos: 2924, int: 0.35, assign: 'Aliphatic C-H stretch (asym)' },
            { pos: 2850, int: 0.20, assign: 'Aliphatic C-H stretch (sym)' },
            { pos: 1943, int: 0.05, assign: 'Aromatic overtone' },
            { pos: 1871, int: 0.04, assign: 'Aromatic overtone' },
            { pos: 1802, int: 0.05, assign: 'Aromatic overtone' },
            { pos: 1601, int: 0.25, assign: 'Aromatic C=C stretch' },
            { pos: 1583, int: 0.12, assign: 'Aromatic C=C stretch' },
            { pos: 1493, int: 0.45, assign: 'Aromatic C=C stretch' },
            { pos: 1452, int: 0.40, assign: 'CH2 bend' },
            { pos: 1373, int: 0.08, assign: 'CH3 bend' },
            { pos: 1181, int: 0.10, assign: 'C-H in-plane bend' },
            { pos: 1154, int: 0.08, assign: 'C-H in-plane bend' },
            { pos: 1069, int: 0.12, assign: 'C-H in-plane bend' },
            { pos: 1028, int: 0.20, assign: 'C-H in-plane bend' },
            { pos: 906, int: 0.10, assign: 'C-H out-of-plane bend' },
            { pos: 842, int: 0.05, assign: 'C-H out-of-plane bend' },
            { pos: 756, int: 0.55, assign: 'C-H out-of-plane bend (mono)' },
            { pos: 698, int: 0.65, assign: 'Ring out-of-plane bend' },
            { pos: 540, int: 0.15, assign: 'Ring deformation' }
        ]
    },
    'Polyethylene': {
        category: 'polymer',
        formula: '(C2H4)n',
        mw: '~50,000',
        cas: '9002-88-4',
        description: 'Linear aliphatic polymer',
        peaks: [
            { pos: 2915, int: 0.85, assign: 'CH2 asymmetric stretch' },
            { pos: 2848, int: 0.75, assign: 'CH2 symmetric stretch' },
            { pos: 1473, int: 0.35, assign: 'CH2 bend (crystalline)' },
            { pos: 1463, int: 0.30, assign: 'CH2 bend (amorphous)' },
            { pos: 1377, int: 0.08, assign: 'CH3 symmetric bend' },
            { pos: 1366, int: 0.06, assign: 'CH2 wag' },
            { pos: 1304, int: 0.04, assign: 'CH2 twist' },
            { pos: 1176, int: 0.03, assign: 'C-C stretch' },
            { pos: 731, int: 0.25, assign: 'CH2 rock (crystalline)' },
            { pos: 720, int: 0.22, assign: 'CH2 rock' }
        ]
    },
    'Polypropylene': {
        category: 'polymer',
        formula: '(C3H6)n',
        mw: '~80,000',
        cas: '9003-07-0',
        description: 'Isotactic polypropylene',
        peaks: [
            { pos: 2951, int: 0.70, assign: 'CH3 asymmetric stretch' },
            { pos: 2916, int: 0.65, assign: 'CH2 asymmetric stretch' },
            { pos: 2868, int: 0.45, assign: 'CH3 symmetric stretch' },
            { pos: 2838, int: 0.40, assign: 'CH2 symmetric stretch' },
            { pos: 1456, int: 0.45, assign: 'CH3 asymmetric bend' },
            { pos: 1376, int: 0.50, assign: 'CH3 symmetric bend' },
            { pos: 1358, int: 0.20, assign: 'CH bend' },
            { pos: 1167, int: 0.35, assign: 'C-C stretch, CH3 rock' },
            { pos: 998, int: 0.40, assign: 'CH3 rock, C-C stretch' },
            { pos: 973, int: 0.35, assign: 'CH3 rock' },
            { pos: 841, int: 0.30, assign: 'CH2 rock, C-C stretch' },
            { pos: 809, int: 0.15, assign: 'CH2 rock' }
        ]
    },
    'PMMA': {
        category: 'polymer',
        formula: '(C5H8O2)n',
        mw: '~120,000',
        cas: '9011-14-7',
        description: 'Poly(methyl methacrylate), acrylic glass',
        peaks: [
            { pos: 2996, int: 0.25, assign: 'O-CH3 stretch' },
            { pos: 2951, int: 0.30, assign: 'C-CH3 stretch' },
            { pos: 1727, int: 0.95, assign: 'C=O stretch (ester)' },
            { pos: 1483, int: 0.20, assign: 'CH3 bend' },
            { pos: 1448, int: 0.35, assign: 'CH2 bend' },
            { pos: 1388, int: 0.18, assign: 'α-CH3 bend' },
            { pos: 1270, int: 0.45, assign: 'C-O stretch' },
            { pos: 1240, int: 0.50, assign: 'C-O stretch' },
            { pos: 1190, int: 0.55, assign: 'C-O-C stretch' },
            { pos: 1147, int: 0.60, assign: 'C-O-C stretch' },
            { pos: 987, int: 0.25, assign: 'O-CH3 rock' },
            { pos: 842, int: 0.15, assign: 'C-C stretch' },
            { pos: 751, int: 0.20, assign: 'C=O bend' }
        ]
    },
    'PET': {
        category: 'polymer',
        formula: '(C10H8O4)n',
        mw: '~20,000',
        cas: '25038-59-9',
        description: 'Polyethylene terephthalate, polyester',
        peaks: [
            { pos: 2969, int: 0.15, assign: 'C-H stretch' },
            { pos: 1713, int: 0.90, assign: 'C=O stretch (ester)' },
            { pos: 1578, int: 0.12, assign: 'Aromatic C=C' },
            { pos: 1505, int: 0.18, assign: 'Aromatic C=C' },
            { pos: 1453, int: 0.22, assign: 'CH2 bend' },
            { pos: 1408, int: 0.30, assign: 'Aromatic C=C' },
            { pos: 1339, int: 0.25, assign: 'CH2 wag' },
            { pos: 1245, int: 0.75, assign: 'C-O stretch (ester)' },
            { pos: 1118, int: 0.60, assign: 'C-O stretch' },
            { pos: 1095, int: 0.50, assign: 'C-O stretch' },
            { pos: 1018, int: 0.35, assign: 'Aromatic C-H in-plane' },
            { pos: 872, int: 0.25, assign: 'Aromatic C-H out-of-plane' },
            { pos: 793, int: 0.20, assign: 'C=O bend' },
            { pos: 725, int: 0.40, assign: 'Aromatic C-H out-of-plane' }
        ]
    },
    'Nylon': {
        category: 'polymer',
        formula: '(C12H22N2O2)n',
        mw: '~30,000',
        cas: '32131-17-2',
        description: 'Nylon 6,6 polyamide',
        peaks: [
            { pos: 3297, int: 0.55, assign: 'N-H stretch (hydrogen bonded)' },
            { pos: 3080, int: 0.15, assign: 'Amide II overtone' },
            { pos: 2932, int: 0.50, assign: 'CH2 asymmetric stretch' },
            { pos: 2858, int: 0.40, assign: 'CH2 symmetric stretch' },
            { pos: 1635, int: 0.85, assign: 'Amide I (C=O stretch)' },
            { pos: 1537, int: 0.75, assign: 'Amide II (N-H bend + C-N stretch)' },
            { pos: 1463, int: 0.25, assign: 'CH2 bend' },
            { pos: 1417, int: 0.15, assign: 'CH2 bend' },
            { pos: 1372, int: 0.12, assign: 'Amide III' },
            { pos: 1264, int: 0.30, assign: 'Amide III' },
            { pos: 1199, int: 0.18, assign: 'CH2 twist' },
            { pos: 936, int: 0.20, assign: 'C-C stretch' },
            { pos: 688, int: 0.25, assign: 'Amide V (N-H wag)' }
        ]
    },

    // Pharmaceuticals
    'Paracetamol': {
        category: 'pharma',
        formula: 'C8H9NO2',
        mw: '151.16',
        cas: '103-90-2',
        description: 'Acetaminophen, analgesic and antipyretic',
        peaks: [
            { pos: 3326, int: 0.50, assign: 'O-H stretch' },
            { pos: 3162, int: 0.45, assign: 'N-H stretch' },
            { pos: 3107, int: 0.20, assign: 'Aromatic C-H stretch' },
            { pos: 2924, int: 0.12, assign: 'Aliphatic C-H stretch' },
            { pos: 1654, int: 0.75, assign: 'Amide I (C=O stretch)' },
            { pos: 1609, int: 0.45, assign: 'Aromatic C=C stretch' },
            { pos: 1564, int: 0.55, assign: 'Amide II' },
            { pos: 1506, int: 0.60, assign: 'Aromatic C=C stretch' },
            { pos: 1442, int: 0.25, assign: 'CH3 bend' },
            { pos: 1371, int: 0.35, assign: 'C-N stretch' },
            { pos: 1327, int: 0.30, assign: 'O-H bend' },
            { pos: 1260, int: 0.50, assign: 'C-O stretch (phenolic)' },
            { pos: 1227, int: 0.55, assign: 'C-O stretch' },
            { pos: 1173, int: 0.25, assign: 'C-H in-plane bend' },
            { pos: 1108, int: 0.20, assign: 'C-H in-plane bend' },
            { pos: 968, int: 0.15, assign: 'C-H out-of-plane' },
            { pos: 837, int: 0.45, assign: 'C-H out-of-plane (para)' },
            { pos: 807, int: 0.40, assign: 'C-H out-of-plane' },
            { pos: 711, int: 0.15, assign: 'Ring deformation' },
            { pos: 603, int: 0.20, assign: 'Ring deformation' }
        ]
    },
    'Aspirin': {
        category: 'pharma',
        formula: 'C9H8O4',
        mw: '180.16',
        cas: '50-78-2',
        description: 'Acetylsalicylic acid, anti-inflammatory',
        peaks: [
            { pos: 3000, int: 0.20, assign: 'Aromatic C-H stretch' },
            { pos: 2940, int: 0.10, assign: 'Aliphatic C-H stretch' },
            { pos: 1753, int: 0.85, assign: 'C=O stretch (ester)' },
            { pos: 1692, int: 0.90, assign: 'C=O stretch (acid)' },
            { pos: 1606, int: 0.30, assign: 'Aromatic C=C stretch' },
            { pos: 1580, int: 0.25, assign: 'Aromatic C=C stretch' },
            { pos: 1487, int: 0.20, assign: 'Aromatic C=C stretch' },
            { pos: 1459, int: 0.25, assign: 'CH3 bend' },
            { pos: 1370, int: 0.40, assign: 'C-O stretch + OH bend' },
            { pos: 1305, int: 0.35, assign: 'C-O stretch' },
            { pos: 1220, int: 0.65, assign: 'C-O stretch (ester)' },
            { pos: 1186, int: 0.50, assign: 'C-O stretch' },
            { pos: 1093, int: 0.30, assign: 'C-H in-plane bend' },
            { pos: 1013, int: 0.25, assign: 'C-H in-plane bend' },
            { pos: 914, int: 0.15, assign: 'O-H out-of-plane bend' },
            { pos: 839, int: 0.12, assign: 'C-H out-of-plane' },
            { pos: 756, int: 0.35, assign: 'C-H out-of-plane (ortho)' },
            { pos: 706, int: 0.20, assign: 'Ring deformation' }
        ]
    },
    'Ibuprofen': {
        category: 'pharma',
        formula: 'C13H18O2',
        mw: '206.28',
        cas: '15687-27-1',
        description: 'Non-steroidal anti-inflammatory drug',
        peaks: [
            { pos: 2954, int: 0.55, assign: 'CH3 asymmetric stretch' },
            { pos: 2925, int: 0.45, assign: 'CH2 asymmetric stretch' },
            { pos: 2869, int: 0.35, assign: 'CH3 symmetric stretch' },
            { pos: 2729, int: 0.08, assign: 'OH stretch (dimer)' },
            { pos: 1720, int: 0.95, assign: 'C=O stretch (carboxylic acid)' },
            { pos: 1608, int: 0.12, assign: 'Aromatic C=C stretch' },
            { pos: 1512, int: 0.35, assign: 'Aromatic C=C stretch' },
            { pos: 1462, int: 0.40, assign: 'CH3 asymmetric bend' },
            { pos: 1420, int: 0.25, assign: 'O-H bend' },
            { pos: 1380, int: 0.30, assign: 'CH3 symmetric bend' },
            { pos: 1320, int: 0.20, assign: 'C-O stretch' },
            { pos: 1268, int: 0.35, assign: 'C-O stretch' },
            { pos: 1230, int: 0.50, assign: 'C-O stretch (acid)' },
            { pos: 1183, int: 0.25, assign: 'C-H in-plane bend' },
            { pos: 1091, int: 0.18, assign: 'C-C stretch' },
            { pos: 935, int: 0.10, assign: 'O-H out-of-plane bend' },
            { pos: 843, int: 0.30, assign: 'C-H out-of-plane (para)' },
            { pos: 779, int: 0.25, assign: 'C-H out-of-plane' },
            { pos: 667, int: 0.12, assign: 'Ring deformation' }
        ]
    },
    'Caffeine': {
        category: 'pharma',
        formula: 'C8H10N4O2',
        mw: '194.19',
        cas: '58-08-2',
        description: 'Methylxanthine stimulant',
        peaks: [
            { pos: 3111, int: 0.15, assign: 'C-H stretch (imidazole)' },
            { pos: 2953, int: 0.20, assign: 'N-CH3 stretch' },
            { pos: 1698, int: 0.85, assign: 'C=O stretch' },
            { pos: 1652, int: 0.80, assign: 'C=O stretch' },
            { pos: 1599, int: 0.35, assign: 'C=N stretch' },
            { pos: 1548, int: 0.50, assign: 'Imidazole ring stretch' },
            { pos: 1480, int: 0.40, assign: 'CH3 bend' },
            { pos: 1454, int: 0.35, assign: 'CH3 bend' },
            { pos: 1404, int: 0.25, assign: 'C-N stretch' },
            { pos: 1356, int: 0.30, assign: 'C-N stretch' },
            { pos: 1285, int: 0.25, assign: 'Imidazole ring' },
            { pos: 1236, int: 0.20, assign: 'C-N stretch' },
            { pos: 1187, int: 0.15, assign: 'Ring mode' },
            { pos: 1073, int: 0.18, assign: 'C-H in-plane bend' },
            { pos: 1024, int: 0.12, assign: 'Ring breathing' },
            { pos: 974, int: 0.10, assign: 'Ring mode' },
            { pos: 860, int: 0.08, assign: 'Ring mode' },
            { pos: 744, int: 0.20, assign: 'C-H out-of-plane' },
            { pos: 642, int: 0.15, assign: 'Ring deformation' }
        ]
    },

    // Organic Compounds
    'Cellulose Acetate': {
        category: 'organic',
        formula: 'Variable',
        mw: '~30,000',
        cas: '9004-35-7',
        description: 'Cellulose derivative, partially acetylated',
        peaks: [
            { pos: 3480, int: 0.30, assign: 'O-H stretch' },
            { pos: 2940, int: 0.20, assign: 'C-H stretch' },
            { pos: 1740, int: 0.85, assign: 'C=O stretch (ester)' },
            { pos: 1433, int: 0.25, assign: 'CH3 bend' },
            { pos: 1371, int: 0.35, assign: 'CH3 symmetric bend' },
            { pos: 1230, int: 0.70, assign: 'C-O stretch (ester)' },
            { pos: 1160, int: 0.45, assign: 'C-O-C stretch' },
            { pos: 1050, int: 0.60, assign: 'C-O stretch (pyranose)' },
            { pos: 902, int: 0.20, assign: 'Pyranose ring' },
            { pos: 604, int: 0.15, assign: 'C-C-O bend' }
        ]
    },
    'Stearic Acid': {
        category: 'organic',
        formula: 'C18H36O2',
        mw: '284.48',
        cas: '57-11-4',
        description: 'Saturated fatty acid',
        peaks: [
            { pos: 2915, int: 0.90, assign: 'CH2 asymmetric stretch' },
            { pos: 2848, int: 0.85, assign: 'CH2 symmetric stretch' },
            { pos: 1700, int: 0.75, assign: 'C=O stretch (acid dimer)' },
            { pos: 1471, int: 0.30, assign: 'CH2 scissor' },
            { pos: 1430, int: 0.25, assign: 'O-H bend' },
            { pos: 1412, int: 0.20, assign: 'C-O stretch + O-H bend' },
            { pos: 1296, int: 0.35, assign: 'C-O stretch' },
            { pos: 1185, int: 0.20, assign: 'C-O stretch' },
            { pos: 939, int: 0.15, assign: 'O-H out-of-plane bend' },
            { pos: 721, int: 0.40, assign: 'CH2 rock' },
            { pos: 686, int: 0.18, assign: 'O-C=O bend' }
        ]
    },
    'Benzoic Acid': {
        category: 'organic',
        formula: 'C7H6O2',
        mw: '122.12',
        cas: '65-85-0',
        description: 'Aromatic carboxylic acid',
        peaks: [
            { pos: 3070, int: 0.20, assign: 'Aromatic C-H stretch' },
            { pos: 2830, int: 0.25, assign: 'O-H stretch (dimer)' },
            { pos: 2669, int: 0.20, assign: 'O-H stretch (dimer)' },
            { pos: 2554, int: 0.18, assign: 'O-H stretch (dimer)' },
            { pos: 1685, int: 0.90, assign: 'C=O stretch (dimer)' },
            { pos: 1600, int: 0.30, assign: 'Aromatic C=C stretch' },
            { pos: 1583, int: 0.25, assign: 'Aromatic C=C stretch' },
            { pos: 1495, int: 0.15, assign: 'Aromatic C=C stretch' },
            { pos: 1452, int: 0.20, assign: 'Aromatic C=C stretch' },
            { pos: 1422, int: 0.35, assign: 'O-H bend + C-O stretch' },
            { pos: 1323, int: 0.40, assign: 'C-O stretch' },
            { pos: 1289, int: 0.50, assign: 'C-O stretch' },
            { pos: 1178, int: 0.18, assign: 'C-H in-plane bend' },
            { pos: 1127, int: 0.12, assign: 'C-H in-plane bend' },
            { pos: 1073, int: 0.10, assign: 'C-H in-plane bend' },
            { pos: 1026, int: 0.15, assign: 'C-H in-plane bend' },
            { pos: 935, int: 0.25, assign: 'O-H out-of-plane (dimer)' },
            { pos: 808, int: 0.12, assign: 'C-H out-of-plane' },
            { pos: 710, int: 0.50, assign: 'C-H out-of-plane (mono)' },
            { pos: 686, int: 0.20, assign: 'O-C=O bend' }
        ]
    },

    // Inorganic
    'CaCO3': {
        category: 'inorganic',
        formula: 'CaCO3',
        mw: '100.09',
        cas: '471-34-1',
        description: 'Calcium carbonate (calcite)',
        peaks: [
            { pos: 2513, int: 0.15, assign: 'Combination band' },
            { pos: 1796, int: 0.10, assign: 'Combination band' },
            { pos: 1420, int: 0.95, assign: 'CO3 asymmetric stretch (ν3)' },
            { pos: 875, int: 0.45, assign: 'CO3 out-of-plane bend (ν2)' },
            { pos: 712, int: 0.25, assign: 'CO3 in-plane bend (ν4)' }
        ]
    },
    'SiO2': {
        category: 'inorganic',
        formula: 'SiO2',
        mw: '60.08',
        cas: '7631-86-9',
        description: 'Silicon dioxide (silica)',
        peaks: [
            { pos: 1095, int: 0.95, assign: 'Si-O-Si asymmetric stretch' },
            { pos: 802, int: 0.40, assign: 'Si-O-Si symmetric stretch' },
            { pos: 470, int: 0.35, assign: 'Si-O-Si bend' }
        ]
    },
    'TiO2': {
        category: 'inorganic',
        formula: 'TiO2',
        mw: '79.87',
        cas: '13463-67-7',
        description: 'Titanium dioxide (rutile)',
        peaks: [
            { pos: 650, int: 0.40, assign: 'Ti-O stretch' },
            { pos: 510, int: 0.55, assign: 'Ti-O stretch' },
            { pos: 420, int: 0.30, assign: 'Ti-O bend' }
        ]
    },

    // Special
    'Unknown': {
        category: 'special',
        formula: '?',
        mw: '?',
        cas: 'Unknown',
        description: 'Mystery compound for identification practice',
        peaks: [
            { pos: 3350, int: 0.45, assign: 'O-H or N-H stretch' },
            { pos: 2920, int: 0.35, assign: 'C-H stretch' },
            { pos: 1715, int: 0.80, assign: 'C=O stretch' },
            { pos: 1600, int: 0.20, assign: 'Aromatic C=C' },
            { pos: 1450, int: 0.25, assign: 'CH bend' },
            { pos: 1250, int: 0.55, assign: 'C-O stretch' },
            { pos: 1050, int: 0.40, assign: 'C-O stretch' },
            { pos: 700, int: 0.30, assign: 'C-H out-of-plane' }
        ]
    },
    'Epoxy Resin (Kinetic)': {
        category: 'special',
        formula: 'Variable',
        mw: '~400-4000',
        cas: '25068-38-6',
        description: 'Bisphenol A diglycidyl ether epoxy for curing studies',
        peaks: [
            { pos: 3500, int: 0.20, assign: 'O-H stretch (secondary)' },
            { pos: 3056, int: 0.15, assign: 'Aromatic C-H stretch' },
            { pos: 2965, int: 0.30, assign: 'Aliphatic C-H stretch' },
            { pos: 2927, int: 0.25, assign: 'CH2 stretch' },
            { pos: 2871, int: 0.20, assign: 'CH3 stretch' },
            { pos: 1608, int: 0.25, assign: 'Aromatic C=C' },
            { pos: 1580, int: 0.20, assign: 'Aromatic C=C' },
            { pos: 1509, int: 0.50, assign: 'Aromatic C=C' },
            { pos: 1455, int: 0.30, assign: 'CH2 bend' },
            { pos: 1362, int: 0.20, assign: 'CH3 bend' },
            { pos: 1296, int: 0.25, assign: 'C-O stretch' },
            { pos: 1246, int: 0.70, assign: 'Ar-O-C stretch' },
            { pos: 1184, int: 0.30, assign: 'Aromatic C-H bend' },
            { pos: 1107, int: 0.20, assign: 'C-O stretch' },
            { pos: 1036, int: 0.40, assign: 'C-O stretch' },
            { pos: 915, int: 0.35, assign: 'Epoxide ring (characteristic)' },
            { pos: 862, int: 0.25, assign: 'Epoxide ring' },
            { pos: 831, int: 0.45, assign: 'Aromatic C-H out-of-plane' },
            { pos: 771, int: 0.20, assign: 'Aromatic ring' }
        ]
    }
};

// Functional Group Database
const FunctionalGroups = [
    { name: 'Alcohol O-H', range: [3200, 3550], bond: 'O-H stretch', intensity: 'Strong, broad' },
    { name: 'Carboxylic Acid O-H', range: [2500, 3300], bond: 'O-H stretch', intensity: 'Very broad' },
    { name: 'Amine N-H', range: [3300, 3500], bond: 'N-H stretch', intensity: 'Medium' },
    { name: 'Amide N-H', range: [3100, 3500], bond: 'N-H stretch', intensity: 'Medium, broad' },
    { name: 'Alkyne ≡C-H', range: [3260, 3330], bond: '≡C-H stretch', intensity: 'Strong, sharp' },
    { name: 'Aromatic C-H', range: [3000, 3100], bond: '=C-H stretch', intensity: 'Medium, multiple' },
    { name: 'Alkene C-H', range: [3010, 3095], bond: '=C-H stretch', intensity: 'Medium' },
    { name: 'Alkane C-H', range: [2850, 2970], bond: 'C-H stretch', intensity: 'Strong' },
    { name: 'Aldehyde C-H', range: [2700, 2850], bond: 'C-H stretch', intensity: 'Two peaks (Fermi)' },
    { name: 'Nitrile C≡N', range: [2210, 2260], bond: 'C≡N stretch', intensity: 'Strong, sharp' },
    { name: 'Alkyne C≡C', range: [2100, 2260], bond: 'C≡C stretch', intensity: 'Variable' },
    { name: 'Ketone C=O', range: [1705, 1725], bond: 'C=O stretch', intensity: 'Strong' },
    { name: 'Aldehyde C=O', range: [1720, 1740], bond: 'C=O stretch', intensity: 'Strong' },
    { name: 'Ester C=O', range: [1735, 1750], bond: 'C=O stretch', intensity: 'Strong' },
    { name: 'Carboxylic Acid C=O', range: [1700, 1725], bond: 'C=O stretch', intensity: 'Strong' },
    { name: 'Amide C=O', range: [1630, 1690], bond: 'C=O stretch', intensity: 'Strong (Amide I)' },
    { name: 'Aromatic C=C', range: [1450, 1600], bond: 'C=C stretch', intensity: 'Variable' },
    { name: 'Alkene C=C', range: [1620, 1680], bond: 'C=C stretch', intensity: 'Variable' },
    { name: 'Amide N-H bend', range: [1510, 1560], bond: 'N-H bend', intensity: 'Strong (Amide II)' },
    { name: 'Nitro -NO₂', range: [1300, 1550], bond: 'N-O stretch', intensity: 'Strong, two peaks' },
    { name: 'Ester C-O', range: [1150, 1300], bond: 'C-O stretch', intensity: 'Strong' },
    { name: 'Ether C-O', range: [1050, 1150], bond: 'C-O-C stretch', intensity: 'Strong' },
    { name: 'Alcohol C-O', range: [1050, 1150], bond: 'C-O stretch', intensity: 'Strong' },
    { name: 'Carbonate', range: [1400, 1450], bond: 'C-O stretch', intensity: 'Very strong' },
    { name: 'C-Cl', range: [600, 800], bond: 'C-Cl stretch', intensity: 'Strong' },
    { name: 'C-Br', range: [500, 600], bond: 'C-Br stretch', intensity: 'Strong' }
];

// ============================================
// UTILITY FUNCTIONS
// ============================================

function generateSpectrum(compound, minWn = 400, maxWn = 4000, noiseLevel = 0.02) {
    const data = SpectralDatabase[compound];
    if (!data) return null;

    const points = [];
    const step = 2; // 2 cm-1 resolution for smooth curve

    for (let wn = maxWn; wn >= minWn; wn -= step) {
        let absorbance = 0;

        // Calculate contribution from each peak
        data.peaks.forEach(peak => {
            // Lorentzian peak shape
            const width = 15 + Math.random() * 5; // FWHM around 15-20 cm-1
            const contribution = peak.int * (width * width) /
                ((wn - peak.pos) * (wn - peak.pos) + width * width);
            absorbance += contribution;
        });

        // Add baseline slope
        absorbance += (maxWn - wn) * 0.00001;

        // Add noise
        absorbance += (Math.random() - 0.5) * noiseLevel;

        // Ensure positive values
        absorbance = Math.max(0, absorbance);

        points.push({ x: wn, y: absorbance });
    }

    return points;
}

function generateBackground(minWn = 400, maxWn = 4000) {
    const points = [];
    const step = 2;

    for (let wn = maxWn; wn >= minWn; wn -= step) {
        // Single beam has characteristic shape - higher at low wavenumbers
        let intensity = 0.8 + 0.2 * Math.exp(-(wn - 1500) * (wn - 1500) / 2000000);

        // Add atmospheric features (CO2 and H2O)
        // CO2 around 2350 cm-1
        intensity -= 0.1 * Math.exp(-(wn - 2350) * (wn - 2350) / 2000);
        // H2O around 1600 and 3400 cm-1
        intensity -= 0.05 * Math.exp(-(wn - 1630) * (wn - 1630) / 5000);
        intensity -= 0.08 * Math.exp(-(wn - 3400) * (wn - 3400) / 50000);

        // Add small noise
        intensity += (Math.random() - 0.5) * 0.01;
        intensity = Math.max(0.1, intensity);

        points.push({ x: wn, y: intensity });
    }

    return points;
}

function convertToTransmittance(absorbanceData) {
    return absorbanceData.map(point => ({
        x: point.x,
        y: Math.pow(10, -point.y) * 100
    }));
}

function convertToSingleBeam(absorbanceData, background) {
    // This is a simplified conversion
    return absorbanceData.map((point, i) => ({
        x: point.x,
        y: background[i] ? background[i].y * Math.pow(10, -point.y) : 0
    }));
}

function detectPeaks(data, threshold = 0.1) {
    const peaks = [];
    const maxIntensity = Math.max(...data.map(p => p.y));
    const thresholdValue = maxIntensity * threshold;

    for (let i = 2; i < data.length - 2; i++) {
        const current = data[i].y;
        // Check if current point is a local maximum
        if (current > thresholdValue &&
            current > data[i - 1].y && current > data[i + 1].y &&
            current > data[i - 2].y && current > data[i + 2].y) {
            peaks.push({
                position: data[i].x,
                intensity: current.toFixed(3)
            });
        }
    }

    // Sort by intensity descending
    peaks.sort((a, b) => b.intensity - a.intensity);

    // Add assignments based on position
    peaks.forEach(peak => {
        peak.assignment = getAssignment(peak.position);
    });

    return peaks;
}

function getAssignment(wavenumber) {
    for (const fg of FunctionalGroups) {
        if (wavenumber >= fg.range[0] && wavenumber <= fg.range[1]) {
            return fg.name;
        }
    }
    return 'Unknown';
}

function identifyFunctionalGroups(data) {
    const peaks = detectPeaks(data, 0.08);
    const identified = [];

    FunctionalGroups.forEach(fg => {
        const matchingPeaks = peaks.filter(p =>
            p.position >= fg.range[0] && p.position <= fg.range[1]
        );

        if (matchingPeaks.length > 0) {
            identified.push({
                name: fg.name,
                range: `${fg.range[0]}-${fg.range[1]} cm⁻¹`,
                bond: fg.bond,
                intensity: fg.intensity,
                matchedPeaks: matchingPeaks.map(p => p.position)
            });
        }
    });

    return identified;
}

function searchLibrary(sampleData, filter = 'all') {
    const matches = [];
    const samplePeaks = detectPeaks(sampleData, 0.08);

    Object.entries(SpectralDatabase).forEach(([name, compound]) => {
        if (filter !== 'all' && compound.category !== filter) return;

        let score = 0;
        let maxScore = compound.peaks.length;

        // Compare peaks
        compound.peaks.forEach(refPeak => {
            const tolerance = 15; // cm-1
            const match = samplePeaks.find(sp =>
                Math.abs(sp.position - refPeak.pos) <= tolerance
            );
            if (match) {
                // Weight by intensity match
                score += 1 - Math.abs(parseFloat(match.intensity) - refPeak.int) / 2;
            }
        });

        const matchPercent = Math.round((score / maxScore) * 100);

        if (matchPercent > 30) {
            matches.push({
                name: name,
                score: matchPercent,
                category: compound.category,
                formula: compound.formula,
                cas: compound.cas,
                description: compound.description
            });
        }
    });

    // Sort by score
    matches.sort((a, b) => b.score - a.score);

    return matches.slice(0, 10);
}

function applyBaseline(data, method = 'linear') {
    const result = [...data];

    if (method === 'linear') {
        // Simple linear baseline from first to last point
        const slope = (data[data.length - 1].y - data[0].y) / (data.length - 1);
        result.forEach((point, i) => {
            point.y = Math.max(0, point.y - (data[0].y + slope * i));
        });
    } else if (method === 'polynomial') {
        // Quadratic baseline
        const n = data.length;
        const midY = data[Math.floor(n / 2)].y;
        result.forEach((point, i) => {
            const x = (i - n / 2) / (n / 2);
            const baseline = data[0].y + (midY - data[0].y) * (1 - x * x);
            point.y = Math.max(0, point.y - baseline * 0.5);
        });
    }

    return result;
}

function applySmoothing(data, points = 5) {
    const result = [];
    const halfWindow = Math.floor(points / 2);

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

function applyNormalization(data) {
    const maxY = Math.max(...data.map(p => p.y));
    return data.map(p => ({ x: p.x, y: p.y / maxY }));
}

function applyDerivative(data) {
    const result = [];

    for (let i = 1; i < data.length - 1; i++) {
        const dx = data[i + 1].x - data[i - 1].x;
        const dy = data[i + 1].y - data[i - 1].y;
        result.push({ x: data[i].x, y: -dy / dx * 100 }); // Negative for absorbance
    }

    return result;
}

function applyATRCorrection(data, crystalType = 'diamond') {
    // ATR correction using real depth-of-penetration formula:
    //   dp = λ / (2π × n1 × √(sin²θ - (n2/n1)²))
    // where n1 = crystal RI, n2 = sample RI (~1.5), θ = angle
    // Lower wavenumber = longer wavelength = deeper penetration = stronger signal

    const crystal = ATR_CRYSTALS[crystalType] || ATR_CRYSTALS.diamond;
    const n1 = crystal.ri;        // Crystal refractive index
    const n2 = 1.5;               // Average sample refractive index
    const theta = crystal.angle * Math.PI / 180;
    const sinTheta = Math.sin(theta);

    // Reference penetration depth at 1000 cm⁻¹ for normalization
    const refLambda = 10000 / 1000; // 10 microns
    const refDp = refLambda / (2 * Math.PI * n1 * Math.sqrt(sinTheta * sinTheta - (n2 / n1) * (n2 / n1)));

    return data.map(point => {
        // Apply spectral range cutoff for the crystal
        if (point.x < crystal.rangeMin || point.x > crystal.rangeMax) {
            return { x: point.x, y: 0 };
        }

        const lambda = 10000 / point.x; // Convert wavenumber to microns
        const dp = lambda / (2 * Math.PI * n1 * Math.sqrt(sinTheta * sinTheta - (n2 / n1) * (n2 / n1)));

        // ATR effect: intensity scales with penetration depth
        // Normalize to reference depth so mid-range looks similar, but
        // low-wavenumber peaks are enhanced and high-wavenumber peaks are reduced
        const atrFactor = dp / refDp;

        return { x: point.x, y: point.y * atrFactor };
    });
}

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

// ============================================
// LOGGING SYSTEM
// ============================================

function logMessage(message, type = 'info') {
    const logPanel = document.getElementById('ftir-log-panel');
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
    const ctx = document.getElementById('ftir-chart');
    if (!ctx) return;

    mainChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Spectrum',
                data: [],
                borderColor: 'rgb(0, 86, 179)',
                backgroundColor: 'rgba(0, 86, 179, 0.1)',
                borderWidth: AppState.settings.lineWidth,
                pointRadius: 0,
                pointHoverRadius: 5,
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 500
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    type: 'linear',
                    reverse: true,
                    title: {
                        display: true,
                        text: 'Wavenumber (cm⁻¹)',
                        font: { weight: 'bold' }
                    },
                    min: 400,
                    max: 4000,
                    grid: {
                        display: AppState.settings.showGrid,
                        color: 'rgba(0, 86, 179, 0.1)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Absorbance',
                        font: { weight: 'bold' }
                    },
                    beginAtZero: true,
                    grid: {
                        display: AppState.settings.showGrid,
                        color: 'rgba(0, 86, 179, 0.1)'
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
                        label: function (context) {
                            return `${context.parsed.x.toFixed(1)} cm⁻¹: ${context.parsed.y.toFixed(4)}`;
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
    ctx.addEventListener('mousemove', (e) => {
        const cursorInfo = document.getElementById('cursor-info');
        if (!cursorInfo || !mainChart.data.datasets[0].data.length) return;

        const rect = ctx.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const xValue = mainChart.scales.x.getValueForPixel(x);
        const yValue = mainChart.scales.y.getValueForPixel(y);

        if (xValue >= 400 && xValue <= 4000) {
            document.getElementById('cursor-wavenumber').textContent = `${xValue.toFixed(1)} cm⁻¹`;
            document.getElementById('cursor-intensity').textContent = `${yValue.toFixed(4)} Abs`;
            cursorInfo.classList.remove('hidden');
        }
    });

    ctx.addEventListener('mouseleave', () => {
        document.getElementById('cursor-info')?.classList.add('hidden');
    });
}

function updateChart(data, label = 'Spectrum') {
    if (!mainChart) return;

    mainChart.data.datasets[0].data = data;
    mainChart.data.datasets[0].label = label;

    // Update Y-axis label based on display mode
    let yLabel = 'Absorbance';
    if (AppState.displayMode === 'transmittance') yLabel = 'Transmittance (%)';
    else if (AppState.displayMode === 'singlebeam') yLabel = 'Single Beam Intensity';

    mainChart.options.scales.y.title.text = yLabel;

    if (AppState.settings.autoScale && data.length > 0) {
        const yValues = data.map(p => p.y);
        mainChart.options.scales.y.min = Math.min(0, Math.min(...yValues));
        mainChart.options.scales.y.max = Math.max(...yValues) * 1.1;
    }

    mainChart.update();
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

function resetChartZoom() {
    if (mainChart) {
        mainChart.resetZoom();
    }
}

// ============================================
// VIEW MANAGEMENT
// ============================================

function switchView(viewName) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));

    if (viewName === 'software') {
        document.getElementById('software-screen-view').classList.add('active');
        AppState.currentView = 'software';
        logMessage('Software interface opened');
    } else {
        document.getElementById('ftir-main-view').classList.add('active');
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
// BACKGROUND COLLECTION
// ============================================

async function collectBackground() {
    if (AppState.isScanning) return;

    AppState.isScanning = true;
    const scans = parseInt(document.getElementById('scans-input').value) || 16;
    const timing = SimTiming[AppState.settings.simSpeed];

    // Show scanning overlay
    const overlay = document.getElementById('scan-status-overlay');
    overlay?.classList.remove('hidden');

    logMessage('Starting background collection...');
    updateScanStatus('Collecting background...', 0);

    // Simulate scanning process
    for (let i = 1; i <= scans; i++) {
        await new Promise(resolve => setTimeout(resolve, timing.scan));
        const progress = (i / scans) * 100;
        updateScanStatus(`Collecting background...`, progress, `Scan ${i} of ${scans}`);
    }

    // FFT processing
    updateScanStatus('Processing FFT...', 100);
    await new Promise(resolve => setTimeout(resolve, timing.fft));

    // Generate background data
    const minWn = parseInt(document.getElementById('min-wavenumber').value) || 400;
    const maxWn = parseInt(document.getElementById('max-wavenumber').value) || 4000;
    AppState.backgroundData = generateBackground(minWn, maxWn);
    AppState.backgroundTime = new Date();
    AppState.backgroundCollected = true;

    // Update UI
    overlay?.classList.add('hidden');
    updateBackgroundStatus();
    enableMeasurementButtons();

    logMessage('Background collection complete', 'success');
    showToast('Background Collected', `${scans} scans averaged successfully`, 'success');

    AppState.isScanning = false;
}

function updateBackgroundStatus() {
    const statusDiv = document.getElementById('background-status');
    const infoDiv = document.getElementById('background-info');

    if (AppState.backgroundCollected) {
        statusDiv.innerHTML = '<i class="fas fa-check-circle"></i><span>Background ready</span>';
        statusDiv.classList.add('collected');

        infoDiv.classList.remove('hidden');
        document.getElementById('bkg-time').textContent = formatTime(AppState.backgroundTime);
        document.getElementById('bkg-scans').textContent = document.getElementById('scans-input').value;
        document.getElementById('bkg-quality').textContent = 'Excellent';
    } else {
        statusDiv.innerHTML = '<i class="fas fa-times-circle"></i><span>No background collected</span>';
        statusDiv.classList.remove('collected');
        infoDiv.classList.add('hidden');
    }
}

// ============================================
// SAMPLE MEASUREMENT
// ============================================

async function measureSample() {
    if (AppState.isScanning) return;

    if (!AppState.backgroundCollected && AppState.settings.bkgWarning) {
        showToast('Warning', 'Please collect a background first', 'warning');
        return;
    }

    AppState.isScanning = true;
    const sample = document.getElementById('sample-select').value;
    const scans = parseInt(document.getElementById('scans-input').value) || 16;
    const timing = SimTiming[AppState.settings.simSpeed];

    // Show scanning overlay
    const overlay = document.getElementById('scan-status-overlay');
    overlay?.classList.remove('hidden');

    logMessage(`Starting measurement: ${sample}`);
    updateScanStatus('Acquiring sample spectrum...', 0);

    // Update software status
    document.getElementById('software-status-led')?.classList.add('busy');
    document.getElementById('software-status-text').textContent = 'Scanning...';

    // Simulate scanning
    for (let i = 1; i <= scans; i++) {
        await new Promise(resolve => setTimeout(resolve, timing.scan));
        const progress = (i / scans) * 100;
        updateScanStatus('Acquiring sample spectrum...', progress, `Scan ${i} of ${scans}`);
    }

    // FFT processing
    updateScanStatus('Processing FFT...', 100);
    await new Promise(resolve => setTimeout(resolve, timing.fft));

    // Ratioing
    updateScanStatus('Ratioing to background...', 100);
    await new Promise(resolve => setTimeout(resolve, timing.fft / 2));

    // Generate spectrum
    const minWn = parseInt(document.getElementById('min-wavenumber').value) || 400;
    const maxWn = parseInt(document.getElementById('max-wavenumber').value) || 4000;
    const resolution = parseInt(document.getElementById('resolution-select').value) || 4;

    // Noise level based on scans (more scans = less noise)
    const noiseLevel = 0.03 / Math.sqrt(scans / 16);

    AppState.sampleData = generateSpectrum(sample, minWn, maxWn, noiseLevel);

    // Apply ATR correction if in ATR sampling mode
    if (AppState.samplingMode === 'atr') {
        AppState.sampleData = applyATRCorrection(AppState.sampleData, AppState.atrCrystal);
        logMessage(`ATR correction applied (${ATR_CRYSTALS[AppState.atrCrystal].name})`, 'info');
    }

    AppState.sampleName = sample;
    AppState.sampleId = document.getElementById('sample-id-input').value || `SAMPLE-${Date.now()}`;
    AppState.processingApplied = [];

    // Update chart based on display mode
    let displayData = AppState.sampleData;
    if (AppState.displayMode === 'transmittance') {
        displayData = convertToTransmittance(AppState.sampleData);
    } else if (AppState.displayMode === 'singlebeam') {
        displayData = convertToSingleBeam(AppState.sampleData, AppState.backgroundData);
    }

    updateChart(displayData, sample);

    // Hide overlay
    overlay?.classList.add('hidden');

    // Update status
    document.getElementById('software-status-led')?.classList.remove('busy');
    document.getElementById('software-status-text').textContent = 'Ready';

    // Update spectrum info bar
    document.getElementById('info-sample-name').textContent = sample;
    document.getElementById('info-resolution').textContent = `${resolution} cm⁻¹`;
    document.getElementById('info-scans').textContent = `${scans} scans`;
    document.getElementById('info-range').textContent = `${minWn}-${maxWn} cm⁻¹`;

    // Calculate S/N ratio
    const snRatio = Math.round(50 * Math.sqrt(scans / 16) * (4 / resolution));
    document.getElementById('quality-indicator').innerHTML = `<i class="fas fa-signal"></i><span>S/N: ${snRatio}</span>`;

    // Enable buttons
    enableAnalysisButtons();
    enableProcessingButtons();

    logMessage(`Measurement complete: ${sample}`, 'success');
    showToast('Measurement Complete', `${sample} spectrum acquired successfully`, 'success');

    AppState.isScanning = false;
}

function updateScanStatus(text, progress, details = '') {
    document.getElementById('scan-status-text').textContent = text;
    document.getElementById('scan-progress-bar').style.width = `${progress}%`;
    document.getElementById('scan-details').textContent = details;
}

// ============================================
// PROCESSING FUNCTIONS
// ============================================

function applyProcessing(type) {
    if (!AppState.sampleData) return;

    let processedData;

    switch (type) {
        case 'baseline':
            processedData = applyBaseline(AppState.sampleData, AppState.settings.baselineMethod);
            AppState.processingApplied.push('Baseline Correction');
            logMessage('Applied baseline correction');
            break;

        case 'smooth':
            processedData = applySmoothing(AppState.sampleData, AppState.settings.smoothPoints);
            AppState.processingApplied.push('Smoothing');
            logMessage(`Applied ${AppState.settings.smoothPoints}-point smoothing`);
            break;

        case 'normalize':
            processedData = applyNormalization(AppState.sampleData);
            AppState.processingApplied.push('Normalization');
            logMessage('Applied normalization');
            break;

        case 'derivative':
            processedData = applyDerivative(AppState.sampleData);
            AppState.processingApplied.push('1st Derivative');
            logMessage('Applied 1st derivative');
            break;

        case 'atr':
            processedData = applyATRCorrection(AppState.sampleData);
            AppState.processingApplied.push('ATR Correction');
            logMessage('Applied ATR correction');
            break;

        default:
            return;
    }

    AppState.sampleData = processedData;

    // Update display
    let displayData = processedData;
    if (AppState.displayMode === 'transmittance') {
        displayData = convertToTransmittance(processedData);
    }

    updateChart(displayData, AppState.sampleName);
    showToast('Processing Applied', `${type.charAt(0).toUpperCase() + type.slice(1)} completed`, 'success');
}

function findPeaks() {
    if (!AppState.sampleData) return;

    const threshold = AppState.settings.peakThreshold / 100;
    AppState.peaksDetected = detectPeaks(AppState.sampleData, threshold);

    // Update peak table
    updatePeakTable(AppState.peaksDetected);

    // Add peak markers to chart
    addPeakAnnotations(AppState.peaksDetected);

    // Expand right panel
    document.getElementById('software-right-panel').classList.remove('collapsed');

    logMessage(`Found ${AppState.peaksDetected.length} peaks`, 'success');
    showToast('Peak Detection', `Found ${AppState.peaksDetected.length} peaks above threshold`, 'success');
}

function updatePeakTable(peaks) {
    const tbody = document.getElementById('peak-table-body');
    if (!tbody) return;

    if (peaks.length === 0) {
        tbody.innerHTML = '<tr class="empty-row"><td colspan="3">No peaks detected</td></tr>';
        return;
    }

    tbody.innerHTML = peaks.slice(0, 20).map(peak => `
        <tr>
            <td>${peak.position.toFixed(1)}</td>
            <td>${peak.intensity}</td>
            <td>${peak.assignment}</td>
        </tr>
    `).join('');
}

function addPeakAnnotations(peaks) {
    if (!mainChart) return;

    // Clear existing annotations
    mainChart.options.plugins.annotation = {
        annotations: {}
    };

    peaks.slice(0, 15).forEach((peak, i) => {
        mainChart.options.plugins.annotation.annotations[`peak${i}`] = {
            type: 'line',
            xMin: peak.position,
            xMax: peak.position,
            borderColor: 'rgba(220, 53, 69, 0.5)',
            borderWidth: 1,
            borderDash: [2, 2],
            label: {
                display: true,
                content: peak.position.toFixed(0),
                position: 'start',
                font: { size: 9 }
            }
        };
    });

    mainChart.update();
}

// ============================================
// FUNCTIONAL GROUP ANALYSIS
// ============================================

function analyzeFunctionalGroups() {
    if (!AppState.sampleData) return;

    AppState.functionalGroups = identifyFunctionalGroups(AppState.sampleData);

    // Update quick results in right panel
    const quickResults = document.getElementById('fg-quick-results');
    if (quickResults) {
        if (AppState.functionalGroups.length === 0) {
            quickResults.innerHTML = '<p class="no-data">No functional groups identified</p>';
        } else {
            quickResults.innerHTML = AppState.functionalGroups.slice(0, 5).map(fg => `
                <div style="padding: 4px 0; border-bottom: 1px solid var(--border-light);">
                    <strong style="color: var(--primary-color);">${fg.name}</strong>
                    <span style="color: var(--text-muted); font-size: 0.8em; margin-left: 8px;">${fg.range}</span>
                </div>
            `).join('');
        }
    }

    // Expand right panel
    document.getElementById('software-right-panel').classList.remove('collapsed');

    // Open detailed modal
    openFunctionalGroupModal();

    logMessage(`Identified ${AppState.functionalGroups.length} functional groups`, 'success');
}

function openFunctionalGroupModal() {
    const matchList = document.getElementById('fg-match-list');
    if (!matchList) return;

    matchList.innerHTML = AppState.functionalGroups.map(fg => `
        <li class="fg-item">
            <div class="fg-item-header">
                <span class="fg-name">${fg.name}</span>
                <span class="fg-range">${fg.range}</span>
            </div>
            <p class="fg-description">${fg.bond} - ${fg.intensity}</p>
        </li>
    `).join('');

    // Build correlation chart
    buildCorrelationChart();

    openModal('functional-group-modal');
}

function buildCorrelationChart() {
    const container = document.getElementById('correlation-chart-container');
    if (!container) return;

    // Create a visual correlation chart
    const regions = [
        { range: [3200, 3600], label: 'O-H/N-H', color: '#e74c3c' },
        { range: [2800, 3100], label: 'C-H', color: '#3498db' },
        { range: [2100, 2300], label: 'C≡N/C≡C', color: '#9b59b6' },
        { range: [1650, 1800], label: 'C=O', color: '#e67e22' },
        { range: [1400, 1650], label: 'C=C/Ar', color: '#27ae60' },
        { range: [1000, 1300], label: 'C-O', color: '#1abc9c' },
        { range: [600, 900], label: 'C-X', color: '#7f8c8d' }
    ];

    container.innerHTML = `
        <div style="position: relative; height: 100%; padding: 10px;">
            <div style="display: flex; height: 30px; border: 1px solid var(--border-color); border-radius: 4px; overflow: hidden;">
                ${regions.map(r => {
        const width = (r.range[1] - r.range[0]) / 36 * 100;
        const hasMatch = AppState.functionalGroups.some(fg =>
            fg.matchedPeaks && fg.matchedPeaks.some(p => p >= r.range[0] && p <= r.range[1])
        );
        return `<div style="flex: ${width}; background: ${hasMatch ? r.color : '#e0e0e0'}; 
                        display: flex; align-items: center; justify-content: center; 
                        font-size: 10px; color: white; font-weight: bold;
                        ${hasMatch ? '' : 'opacity: 0.3;'}">${r.label}</div>`;
    }).join('')}
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 10px; color: var(--text-muted);">
                <span>4000 cm⁻¹</span>
                <span>400 cm⁻¹</span>
            </div>
        </div>
    `;
}

// ============================================
// LIBRARY SEARCH
// ============================================

function performLibrarySearch() {
    if (!AppState.sampleData) return;

    const filter = document.getElementById('library-filter')?.value || 'all';
    AppState.libraryMatches = searchLibrary(AppState.sampleData, filter);

    // Update quick results
    const quickResults = document.getElementById('library-quick-results');
    if (quickResults) {
        if (AppState.libraryMatches.length === 0) {
            quickResults.innerHTML = '<p class="no-data">No matches found</p>';
        } else {
            const topMatch = AppState.libraryMatches[0];
            quickResults.innerHTML = `
                <div style="padding: 8px; background: var(--success-bg); border-radius: 4px;">
                    <strong style="color: var(--success-color);">${topMatch.name}</strong>
                    <span style="float: right; font-weight: bold; color: var(--success-color);">${topMatch.score}%</span>
                </div>
            `;
        }
    }

    // Expand right panel
    document.getElementById('software-right-panel').classList.remove('collapsed');

    // Open analysis modal
    openAnalysisModal();

    logMessage(`Library search complete: ${AppState.libraryMatches.length} matches`, 'success');
}

function openAnalysisModal() {
    // Initialize analysis chart
    const ctx = document.getElementById('analysis-chart');
    if (ctx && !analysisChart) {
        analysisChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Sample',
                    data: AppState.sampleData,
                    borderColor: 'rgb(0, 86, 179)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        reverse: true,
                        title: { display: true, text: 'Wavenumber (cm⁻¹)' }
                    },
                    y: {
                        title: { display: true, text: 'Absorbance' },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    } else if (analysisChart) {
        analysisChart.data.datasets = [{
            label: 'Sample',
            data: AppState.sampleData,
            borderColor: 'rgb(0, 86, 179)',
            borderWidth: 2,
            pointRadius: 0,
            fill: false
        }];
        analysisChart.update();
    }

    // Populate match list
    const matchList = document.getElementById('match-list');
    if (matchList) {
        matchList.innerHTML = AppState.libraryMatches.map((match, i) => `
            <div class="match-item ${i === 0 ? 'top-match' : ''}" data-compound="${match.name}">
                <span class="match-name">${match.name}</span>
                <span class="match-score">${match.score}%</span>
            </div>
        `).join('');

        // Add click handlers
        matchList.querySelectorAll('.match-item').forEach(item => {
            item.addEventListener('click', () => selectLibraryMatch(item.dataset.compound));
        });
    }

    openModal('analysis-modal');
}

function selectLibraryMatch(compoundName) {
    const compound = SpectralDatabase[compoundName];
    if (!compound) return;

    // Highlight selected
    document.querySelectorAll('.match-item').forEach(item => {
        item.classList.toggle('selected', item.dataset.compound === compoundName);
    });

    // Update details
    const detailsContent = document.getElementById('compound-details-content');
    if (detailsContent) {
        detailsContent.innerHTML = `
            <p><strong>Formula:</strong> ${compound.formula}</p>
            <p><strong>MW:</strong> ${compound.mw}</p>
            <p><strong>CAS:</strong> ${compound.cas}</p>
            <p><strong>Category:</strong> ${compound.category}</p>
            <p>${compound.description}</p>
        `;
    }

    // Add reference spectrum to chart
    if (analysisChart) {
        const refData = generateSpectrum(compoundName, 400, 4000, 0.01);

        // Remove existing reference if any
        if (analysisChart.data.datasets.length > 1) {
            analysisChart.data.datasets.pop();
        }

        analysisChart.data.datasets.push({
            label: compoundName,
            data: refData,
            borderColor: 'rgb(40, 167, 69)',
            borderWidth: 2,
            pointRadius: 0,
            borderDash: [5, 5],
            fill: false
        });

        analysisChart.update();

        // Show reference legend
        document.querySelector('.legend-item.reference')?.classList.remove('hidden');
    }

    // Enable add to overlay button
    document.getElementById('add-to-overlay').disabled = false;
}

// ============================================
// LIBRARY BROWSER
// ============================================

function populateLibraryList(filter = 'all') {
    const compoundList = document.getElementById('compound-list');
    if (!compoundList) return;

    const compounds = Object.entries(SpectralDatabase)
        .filter(([name, data]) => filter === 'all' || data.category === filter)
        .sort((a, b) => a[0].localeCompare(b[0]));

    compoundList.innerHTML = compounds.map(([name]) => `
        <div class="compound-item" data-compound="${name}">${name}</div>
    `).join('');

    // Add click handlers
    compoundList.querySelectorAll('.compound-item').forEach(item => {
        item.addEventListener('click', () => previewLibraryCompound(item.dataset.compound));
    });
}

function previewLibraryCompound(compoundName) {
    const compound = SpectralDatabase[compoundName];
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
        <p><strong>Category:</strong> ${compound.category}</p>
        <p>${compound.description}</p>
    `;

    // Initialize or update preview chart
    const ctx = document.getElementById('library-preview-chart');
    if (!ctx) return;

    const previewData = generateSpectrum(compoundName, 400, 4000, 0.01);

    if (!libraryPreviewChart) {
        libraryPreviewChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: compoundName,
                    data: previewData,
                    borderColor: 'rgb(0, 86, 179)',
                    borderWidth: 1.5,
                    pointRadius: 0,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { type: 'linear', reverse: true, display: false },
                    y: { display: false, beginAtZero: true }
                },
                plugins: { legend: { display: false } }
            }
        });
    } else {
        libraryPreviewChart.data.datasets[0].data = previewData;
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
    document.getElementById('report-resolution').textContent =
        (document.getElementById('resolution-select')?.value || '4') + ' cm⁻¹';
    document.getElementById('report-scans').textContent =
        document.getElementById('scans-input')?.value || '16';
    document.getElementById('report-range').textContent =
        `${document.getElementById('min-wavenumber')?.value || '400'}-${document.getElementById('max-wavenumber')?.value || '4000'} cm⁻¹`;

    // Generate report spectrum chart
    const ctx = document.getElementById('report-chart');
    if (ctx && AppState.sampleData) {
        if (reportChart) {
            reportChart.destroy();
        }

        reportChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: AppState.sampleName,
                    data: AppState.sampleData,
                    borderColor: 'rgb(0, 86, 179)',
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
                        reverse: true,
                        title: { display: true, text: 'Wavenumber (cm⁻¹)', font: { size: 10 } }
                    },
                    y: {
                        title: { display: true, text: 'Absorbance', font: { size: 10 } },
                        beginAtZero: true
                    }
                },
                plugins: { legend: { display: false } }
            }
        });
    }

    // Identification results
    const idResults = document.getElementById('report-identification');
    if (idResults) {
        if (AppState.libraryMatches.length > 0) {
            idResults.innerHTML = `
                <table class="report-table">
                    <tr><td>Top Match:</td><td><strong>${AppState.libraryMatches[0].name}</strong></td></tr>
                    <tr><td>Match Score:</td><td>${AppState.libraryMatches[0].score}%</td></tr>
                    <tr><td>Category:</td><td>${AppState.libraryMatches[0].category}</td></tr>
                </table>
            `;
        } else {
            idResults.innerHTML = '<p class="no-data">No identification performed</p>';
        }
    }

    // Peak table
    const peakTable = document.getElementById('report-peak-table');
    if (peakTable) {
        if (AppState.peaksDetected.length > 0) {
            peakTable.innerHTML = `
                <table class="report-table" style="width: 100%;">
                    <thead><tr><th>Position (cm⁻¹)</th><th>Intensity</th><th>Assignment</th></tr></thead>
                    <tbody>
                        ${AppState.peaksDetected.slice(0, 10).map(p => `
                            <tr><td>${p.position.toFixed(1)}</td><td>${p.intensity}</td><td>${p.assignment}</td></tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
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
    if (!AppState.sampleData) {
        showToast('Export Error', 'No spectrum data to export', 'error');
        return;
    }

    let content = '';
    let filename = `${AppState.sampleName || 'spectrum'}_${Date.now()}`;
    let mimeType = 'text/plain';

    const includeMetadata = document.getElementById('export-include-metadata')?.checked;
    const includePeaks = document.getElementById('export-include-peaks')?.checked;

    switch (format) {
        case 'csv':
            content = 'Wavenumber (cm-1),Absorbance\n';
            AppState.sampleData.forEach(p => {
                content += `${p.x},${p.y}\n`;
            });
            filename += '.csv';
            mimeType = 'text/csv';
            break;

        case 'txt':
            if (includeMetadata) {
                content = `Sample: ${AppState.sampleName}\n`;
                content += `Date: ${formatDate(new Date())}\n`;
                content += `Scans: ${document.getElementById('scans-input')?.value}\n`;
                content += `Resolution: ${document.getElementById('resolution-select')?.value} cm-1\n\n`;
            }
            content += 'Wavenumber\tAbsorbance\n';
            AppState.sampleData.forEach(p => {
                content += `${p.x.toFixed(2)}\t${p.y.toFixed(6)}\n`;
            });
            filename += '.txt';
            break;

        case 'json':
            const jsonData = {
                sample: AppState.sampleName,
                sampleId: AppState.sampleId,
                date: new Date().toISOString(),
                parameters: {
                    scans: parseInt(document.getElementById('scans-input')?.value),
                    resolution: parseInt(document.getElementById('resolution-select')?.value),
                    range: [
                        parseInt(document.getElementById('min-wavenumber')?.value),
                        parseInt(document.getElementById('max-wavenumber')?.value)
                    ]
                },
                spectrum: AppState.sampleData
            };

            if (includePeaks) {
                jsonData.peaks = AppState.peaksDetected;
            }

            content = JSON.stringify(jsonData, null, 2);
            filename += '.json';
            mimeType = 'application/json';
            break;

        case 'jdx':
            content = '##TITLE=' + (AppState.sampleName || 'Unknown') + '\n';
            content += '##JCAMP-DX=4.24\n';
            content += '##DATA TYPE=INFRARED SPECTRUM\n';
            content += '##ORIGIN=SimuPharma FTIR Digital Twin\n';
            content += '##OWNER=\n';
            content += `##DATE=${new Date().toISOString().split('T')[0]}\n`;
            content += '##XUNITS=1/CM\n';
            content += '##YUNITS=ABSORBANCE\n';
            content += `##FIRSTX=${AppState.sampleData[0].x}\n`;
            content += `##LASTX=${AppState.sampleData[AppState.sampleData.length - 1].x}\n`;
            content += `##NPOINTS=${AppState.sampleData.length}\n`;
            content += '##XYDATA=(X++(Y..Y))\n';
            AppState.sampleData.forEach(p => {
                content += `${p.x.toFixed(2)} ${p.y.toFixed(6)}\n`;
            });
            content += '##END=\n';
            filename += '.jdx';
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
    showToast('Export Complete', `Spectrum exported as ${format.toUpperCase()}`, 'success');
    logMessage(`Spectrum exported: ${filename}`);
}

// ============================================
// UI CONTROL FUNCTIONS
// ============================================

function enableMeasurementButtons() {
    document.getElementById('start-button').disabled = false;
    document.getElementById('toolbar-save').disabled = true;
}

function enableAnalysisButtons() {
    document.getElementById('find-groups-button').disabled = false;
    document.getElementById('accept-button').disabled = false;
    document.getElementById('report-button').disabled = false;
    document.getElementById('toolbar-save').disabled = false;
    document.getElementById('toolbar-export').disabled = false;
    document.getElementById('toolbar-print').disabled = false;
    document.getElementById('add-comparison-tab').disabled = false;
}

function enableProcessingButtons() {
    document.getElementById('process-baseline-button').disabled = false;
    document.getElementById('process-smooth-button').disabled = false;
    document.getElementById('process-normalize-button').disabled = false;
    document.getElementById('process-derivative-button').disabled = false;
    document.getElementById('process-peakpick-button').disabled = false;
    document.getElementById('process-atr-correct-button').disabled = false;
}

function updateDisplayMode(mode) {
    AppState.displayMode = mode;

    // Update button states
    document.querySelectorAll('#mode-sp-button, #mode-tr-button, #mode-ab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    if (mode === 'singlebeam') {
        document.getElementById('mode-sp-button')?.classList.add('active');
    } else if (mode === 'transmittance') {
        document.getElementById('mode-tr-button')?.classList.add('active');
    } else {
        document.getElementById('mode-ab-button')?.classList.add('active');
    }

    // Update chart if data exists
    if (AppState.sampleData) {
        let displayData = AppState.sampleData;
        if (mode === 'transmittance') {
            displayData = convertToTransmittance(AppState.sampleData);
        } else if (mode === 'singlebeam' && AppState.backgroundData) {
            displayData = convertToSingleBeam(AppState.sampleData, AppState.backgroundData);
        }
        updateChart(displayData, AppState.sampleName);
    }

    logMessage(`Display mode: ${mode}`);
}

function updateMeasurementMode(mode) {
    AppState.measurementMode = mode;

    document.querySelectorAll('#mode-live-button, #mode-single-button, #mode-kinetic-button').forEach(btn => {
        btn.classList.remove('active');
    });

    document.getElementById(`mode-${mode}-button`)?.classList.add('active');

    // Show/hide kinetic settings
    const kineticSettings = document.getElementById('kinetic-settings');
    if (kineticSettings) {
        kineticSettings.classList.toggle('hidden', mode !== 'kinetic');
    }

    logMessage(`Measurement mode: ${mode}`);
}

// ============================================
// SETTINGS MANAGEMENT
// ============================================

function loadSettings() {
    const saved = localStorage.getItem('ftir-settings');
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
    localStorage.setItem('ftir-settings', JSON.stringify(AppState.settings));
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
    document.getElementById('theme-select').value = AppState.settings.theme;
    document.getElementById('line-width').value = AppState.settings.lineWidth;
    document.getElementById('show-grid').checked = AppState.settings.showGrid;
    document.getElementById('auto-scale').checked = AppState.settings.autoScale;
    document.getElementById('default-scans').value = AppState.settings.defaultScans;
    document.getElementById('default-resolution').value = AppState.settings.defaultResolution;
    document.getElementById('bkg-warning').checked = AppState.settings.bkgWarning;
    document.getElementById('baseline-method').value = AppState.settings.baselineMethod;
    document.getElementById('smooth-points').value = AppState.settings.smoothPoints;
    document.getElementById('peak-threshold').value = AppState.settings.peakThreshold;
    document.getElementById('threshold-value').textContent = AppState.settings.peakThreshold + '%';
    document.getElementById('sim-speed').value = AppState.settings.simSpeed;
    document.getElementById('sound-effects').checked = AppState.settings.soundEffects;
    document.getElementById('show-hints').checked = AppState.settings.showHints;
}

function resetSettings() {
    AppState.settings = {
        theme: 'light',
        lineWidth: 2,
        showGrid: true,
        autoScale: true,
        defaultScans: 16,
        defaultResolution: 4,
        bkgWarning: true,
        baselineMethod: 'linear',
        smoothPoints: 5,
        peakThreshold: 10,
        simSpeed: 'normal',
        soundEffects: false,
        showHints: true
    };
    applySettings();
    showToast('Settings Reset', 'All settings restored to defaults', 'info');
}

// ============================================
// DIAGNOSTICS
// ============================================

async function runSelfTest() {
    showToast('Self-Test', 'Running system diagnostics...', 'info');

    // Simulate test
    await new Promise(resolve => setTimeout(resolve, 2000));

    showToast('Self-Test Complete', 'All systems passed', 'success');
    logMessage('Self-test completed: All systems OK', 'success');
}

async function runPerformanceTest() {
    showToast('Performance Test', 'Testing system performance...', 'info');

    await new Promise(resolve => setTimeout(resolve, 3000));

    showToast('Performance Test', 'S/N ratio: 45000:1, Energy: 98%', 'success');
    logMessage('Performance test: S/N 45000:1, Energy 98%', 'success');
}

async function runValidation() {
    // Automatically select polystyrene and run measurement
    document.getElementById('sample-select').value = 'Polystyrene';

    if (!AppState.backgroundCollected) {
        await collectBackground();
    }

    await measureSample();
    findPeaks();

    // Check for expected polystyrene peaks
    const expectedPeaks = [3026, 2924, 1601, 1493, 1452, 756, 698];
    const foundPeaks = AppState.peaksDetected.map(p => p.position);

    let passCount = 0;
    expectedPeaks.forEach(exp => {
        if (foundPeaks.some(found => Math.abs(found - exp) < 20)) {
            passCount++;
        }
    });

    const passRate = Math.round((passCount / expectedPeaks.length) * 100);

    if (passRate >= 80) {
        showToast('Validation Passed', `Polystyrene validation: ${passRate}% peaks verified`, 'success');
        logMessage(`Validation PASSED: ${passRate}% peaks verified`, 'success');
    } else {
        showToast('Validation Warning', `Only ${passRate}% peaks verified`, 'warning');
        logMessage(`Validation WARNING: ${passRate}% peaks verified`, 'warning');
    }
}

// ============================================
// TIME & SESSION MANAGEMENT
// ============================================

function updateDateTime() {
    const now = new Date();
    document.getElementById('current-datetime').textContent = formatDate(now);

    const sessionDuration = Date.now() - AppState.sessionStartTime;
    document.getElementById('session-time').textContent = `Session: ${formatSessionTime(sessionDuration)}`;
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

function handleKeyboardShortcuts(e) {
    // Only handle shortcuts when in software view
    if (AppState.currentView !== 'software') return;

    // Ctrl combinations
    if (e.ctrlKey) {
        switch (e.key.toLowerCase()) {
            case 'b':
                e.preventDefault();
                collectBackground();
                break;
            case 's':
                e.preventDefault();
                if (AppState.backgroundCollected) {
                    measureSample();
                }
                break;
            case 'f':
                e.preventDefault();
                if (AppState.sampleData) {
                    findPeaks();
                }
                break;
            case 'g':
                e.preventDefault();
                if (AppState.sampleData) {
                    analyzeFunctionalGroups();
                }
                break;
            case 'i':
                e.preventDefault();
                if (AppState.sampleData) {
                    performLibrarySearch();
                }
                break;
            case 'r':
                e.preventDefault();
                resetChartZoom();
                break;
        }
    }

    // Simple key shortcuts
    if (!e.ctrlKey && !e.altKey) {
        switch (e.key) {
            case '+':
            case '=':
                if (mainChart) {
                    mainChart.zoom(1.2);
                }
                break;
            case '-':
                if (mainChart) {
                    mainChart.zoom(0.8);
                }
                break;
            case 'Escape':
                closeAllModals();
                break;
        }
    }
}

// ============================================
// EVENT LISTENERS & INITIALIZATION
// ============================================

function initializeEventListeners() {
    // ==========================================
    // 1. HOTSPOT LOGIC
    // ==========================================

    // Main screen hotspot (Monitor) -> Switch to software view
    const screenHotspot = document.getElementById('hotspot-screen');
    if (screenHotspot) {
        screenHotspot.addEventListener('click', () => switchView('software'));
    }

    // Modal hotspots (ATR, Sample, Optics, etc.)
    document.querySelectorAll('.hotspot[data-modal]').forEach(hotspot => {
        hotspot.addEventListener('click', (e) => {
            e.stopPropagation(); // Stop click from bubbling to background
            const modalId = hotspot.getAttribute('data-modal');
            openModal(modalId);
        });
    });

    // ==========================================
    // 2. VIDEO PLAYER LOGIC (Matches your CSS)
    // ==========================================

    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Find the container holding the video and image
            const container = btn.closest('.modal-image-container');
            const video = container.querySelector('video');
            const icon = btn.querySelector('i');

            if (!video) return;

            if (video.paused) {
                // PLAY STATE
                video.play();
                icon.className = 'fas fa-pause'; // Change icon to pause

                // Add the CSS class defined in your stylesheet
                // This sets opacity: 1 and z-index: 2
                video.classList.add('active');
            } else {
                // PAUSE STATE
                video.pause();
                icon.className = 'fas fa-play'; // Change icon to play

                // Keep the video visible if you want, or hide it by removing 'active'
                // Usually better to keep it visible while paused:
                // video.classList.remove('active'); 
            }
        });
    });

    // ==========================================
    // 3. STANDARD UI NAVIGATION
    // ==========================================

    // View switching buttons
    document.getElementById('quick-new-measurement')?.addEventListener('click', () => switchView('software'));
    document.getElementById('exit-software-button')?.addEventListener('click', () => switchView('main'));

    // Modal Close Logic (With Video Reset)
    document.querySelectorAll('.modal-close-btn, .modal-close-button').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal');

            // If modal has a video, reset it completely
            const video = modal.querySelector('video');
            if (video) {
                video.pause();
                video.currentTime = 0;
                video.classList.remove('active'); // Hide video, show static image

                // Reset icon
                const icon = modal.querySelector('.play-btn i');
                if (icon) icon.className = 'fas fa-play';
            }

            if (modal) closeModal(modal.id);
        });
    });

    // Close on backdrop click
    document.getElementById('modal-backdrop')?.addEventListener('click', closeAllModals);

    // Header buttons
    document.getElementById('help-btn')?.addEventListener('click', () => openModal('help-modal'));
    document.getElementById('settings-btn')?.addEventListener('click', () => openModal('settings-modal'));
    document.getElementById('quick-diagnostics')?.addEventListener('click', () => openModal('diagnostics-modal'));
    document.getElementById('quick-library')?.addEventListener('click', () => openModal('library-modal'));

    // Quick Report Action
    document.getElementById('quick-reports')?.addEventListener('click', () => {
        if (AppState.sampleData) {
            generateReport();
        } else {
            showToast('No Data', 'Collect a spectrum first', 'warning');
        }
    });

    // ==========================================
    // 4. SOFTWARE CONTROLS
    // ==========================================

    // Main Actions
    document.getElementById('background-button')?.addEventListener('click', collectBackground);
    document.getElementById('start-button')?.addEventListener('click', measureSample);

    // Modes
    document.getElementById('mode-live-button')?.addEventListener('click', () => updateMeasurementMode('live'));
    document.getElementById('mode-single-button')?.addEventListener('click', () => updateMeasurementMode('single'));
    document.getElementById('mode-kinetic-button')?.addEventListener('click', () => updateMeasurementMode('kinetic'));

    document.getElementById('mode-sp-button')?.addEventListener('click', () => updateDisplayMode('singlebeam'));
    document.getElementById('mode-tr-button')?.addEventListener('click', () => updateDisplayMode('transmittance'));
    document.getElementById('mode-ab-button')?.addEventListener('click', () => updateDisplayMode('absorbance'));

    // ATR Sampling Mode Toggle
    document.getElementById('sampling-transmission-btn')?.addEventListener('click', () => {
        AppState.samplingMode = 'transmission';
        document.getElementById('sampling-transmission-btn')?.classList.add('active');
        document.getElementById('sampling-atr-btn')?.classList.remove('active');
        document.getElementById('atr-settings-panel')?.classList.add('hidden');
        logMessage('Sampling mode: Transmission');
        showToast('Sampling Mode', 'Switched to Transmission mode', 'info', 2000);
    });

    document.getElementById('sampling-atr-btn')?.addEventListener('click', () => {
        AppState.samplingMode = 'atr';
        document.getElementById('sampling-atr-btn')?.classList.add('active');
        document.getElementById('sampling-transmission-btn')?.classList.remove('active');
        document.getElementById('atr-settings-panel')?.classList.remove('hidden');
        logMessage(`Sampling mode: ATR (${ATR_CRYSTALS[AppState.atrCrystal].name})`);
        showToast('ATR Mode Active', `Crystal: ${ATR_CRYSTALS[AppState.atrCrystal].name}`, 'success', 3000);
    });

    // ATR Crystal Selector
    document.getElementById('atr-crystal-select')?.addEventListener('change', (e) => {
        AppState.atrCrystal = e.target.value;
        const crystal = ATR_CRYSTALS[e.target.value];
        if (crystal) {
            document.getElementById('atr-crystal-ri').textContent = crystal.ri;
            document.getElementById('atr-crystal-use').textContent = crystal.sampleTypes;
            logMessage(`ATR crystal changed to ${crystal.name} (RI: ${crystal.ri}, Range: ${crystal.rangeMin}–${crystal.rangeMax} cm⁻¹)`);
        }
    });

    // Processing Tools
    const processors = {
        'process-baseline-button': 'baseline',
        'process-smooth-button': 'smooth',
        'process-normalize-button': 'normalize',
        'process-derivative-button': 'derivative',
        'process-atr-correct-button': 'atr'
    };

    for (const [id, type] of Object.entries(processors)) {
        document.getElementById(id)?.addEventListener('click', () => applyProcessing(type));
    }

    document.getElementById('process-peakpick-button')?.addEventListener('click', findPeaks);

    // Analysis
    document.getElementById('find-groups-button')?.addEventListener('click', analyzeFunctionalGroups);
    document.getElementById('accept-button')?.addEventListener('click', performLibrarySearch);
    document.getElementById('report-button')?.addEventListener('click', generateReport);

    // Toolbar
    document.getElementById('toolbar-zoom-in')?.addEventListener('click', () => mainChart?.zoom(1.2));
    document.getElementById('toolbar-zoom-out')?.addEventListener('click', () => mainChart?.zoom(0.8));
    document.getElementById('toolbar-reset-zoom')?.addEventListener('click', resetChartZoom);
    document.getElementById('toolbar-export')?.addEventListener('click', () => openModal('export-modal'));
    document.getElementById('toolbar-print')?.addEventListener('click', () => window.print()); // Use native print for toolbar

    // Collapsible Sections
    document.querySelectorAll('.section-header').forEach(header => {
        header.addEventListener('click', () => {
            header.closest('.panel-section')?.classList.toggle('collapsed');
        });
    });

    // Right Panel Toggle
    document.getElementById('right-panel-toggle')?.addEventListener('click', () => {
        document.getElementById('software-right-panel')?.classList.toggle('collapsed');
    });

    // Handle Tabs (Settings, Help, Info)
    const tabGroups = ['.info-tab', '.settings-tab', '.help-nav-item', '.library-categories li'];
    tabGroups.forEach(selector => {
        document.querySelectorAll(selector).forEach(tab => {
            tab.addEventListener('click', function () {
                // Find siblings and remove active
                const siblings = this.parentElement.children;
                for (let sibling of siblings) sibling.classList.remove('active');
                this.classList.add('active');

                // Logic for showing content based on data-tab or data-topic
                const target = this.dataset.tab || this.dataset.topic || this.dataset.category;
                if (target) {
                    const container = this.closest('.modal-body') || document;

                    // Hide all content sections
                    const contentSelector = selector === '.settings-tab' ? '.settings-panel' :
                        selector === '.help-nav-item' ? '.help-topic' :
                            '.tab-content';

                    if (selector === '.library-categories li') {
                        populateLibraryList(target); // Special case for library
                    } else {
                        container.querySelectorAll(contentSelector).forEach(c => c.classList.remove('active'));
                        // Show target
                        const content = container.querySelector(`${contentSelector}[data-tab="${target}"], ${contentSelector}[data-topic="${target}"]`);
                        if (content) content.classList.add('active');
                    }
                }
            });
        });
    });

    // Keyboard Shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

// ============================================
// LOADING SCREEN ANIMATION
// ============================================

async function runLoadingSequence() {
    const steps = document.querySelectorAll('.check-item');
    const loadingText = document.querySelector('.loading-text');

    const messages = [
        'Loading optical components...',
        'Calibrating interferometer...',
        'Initializing detector...',
        'Loading compound library...',
        'System ready!'
    ];

    for (let i = 0; i < steps.length; i++) {
        steps[i].classList.add('active');
        loadingText.textContent = messages[i];

        await new Promise(resolve => setTimeout(resolve, 500));

        steps[i].classList.remove('active');
        steps[i].classList.add('complete');
    }

    await new Promise(resolve => setTimeout(resolve, 300));

    // Hide loading screen
    document.getElementById('loading-screen')?.classList.add('hidden');
}

// ============================================
// MAIN INITIALIZATION
// ============================================

async function initializeApp() {
    // Wait for DOM
    if (document.readyState !== 'complete') {
        await new Promise(resolve => window.addEventListener('load', resolve));
    }

    // Run loading animation
    await runLoadingSequence();

    // Initialize components
    loadSettings();
    initializeMainChart();
    initializeEventListeners();

    // Start timers
    updateDateTime();
    setInterval(updateDateTime, 1000);

    // Initial log message
    logMessage('System initialized and ready');
    logMessage('FTIR-5000 Digital Twin v2.0');

    // Show welcome toast
    showToast('Welcome', 'SimuPharma FTIR Digital Twin is ready', 'success');
}

// Start the application
document.addEventListener('DOMContentLoaded', initializeApp);
// ============================================
// TUTORIAL SYSTEM
// ============================================

const Tutorial = {
    steps: [
        {
            id: 'hotspot-atr',
            title: 'Sample Interface',
            text: 'This is the ATR crystal (Attenuated Total Reflectance). This is where you load your solid or liquid samples for analysis.'
        },
        {
            id: 'hotspot-screen',
            title: 'Instrument Control',
            text: 'Click the monitor to access the main OPUS software interface where you can control parameters and view spectra.'
        },
        {
            id: 'software-header',
            title: 'Software Toolbar',
            text: 'Use the toolbar to manage files, zoom into spectra, overlay data, and export your results.'
        },
        {
            id: 'background-button',
            title: 'Collect Background',
            text: 'CRITICAL STEP: Always collect a background spectrum first to remove atmospheric interferences (CO2 and Water Vapor).'
        },
        {
            id: 'start-button',
            title: 'Measure Sample',
            text: 'Once the background is valid and sample is loaded, click here to acquire your sample spectrum.'
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

        // Bind tutorial buttons if not already bound
        const nextBtn = document.getElementById('tutorial-next');
        const skipBtn = document.getElementById('tutorial-skip');

        if (nextBtn) nextBtn.onclick = () => this.next();
        if (skipBtn) skipBtn.onclick = () => this.end();
    },

    showStep() {
        if (this.current >= this.steps.length) {
            this.end();
            return;
        }

        const step = this.steps[this.current];
        const target = document.getElementById(step.id);

        // Auto-switch view if target is not visible (e.g. asking for software button while in main view)
        if (!target || target.offsetParent === null) {
            if (step.id === 'software-header' || step.id === 'background-button') {
                switchView('software');
                // Allow transition time before positioning
                setTimeout(() => this.showStep(), 300);
                return;
            } else if (step.id === 'hotspot-atr') {
                switchView('main');
                setTimeout(() => this.showStep(), 300);
                return;
            }
        }

        if (target) {
            this.positionOverlay(target);
            document.getElementById('tutorial-title').textContent = step.title;
            document.getElementById('tutorial-text').textContent = step.text;
            document.getElementById('tutorial-step-indicator').textContent = `Step ${this.current + 1} of ${this.steps.length}`;
        }
    },

    positionOverlay(target) {
        const rect = target.getBoundingClientRect();
        const spotlight = document.querySelector('.tutorial-spotlight');
        const tooltip = document.querySelector('.tutorial-tooltip');

        if (spotlight) {
            spotlight.style.top = `${rect.top}px`;
            spotlight.style.left = `${rect.left}px`;
            spotlight.style.width = `${rect.width}px`;
            spotlight.style.height = `${rect.height}px`;
        }

        if (tooltip) {
            // Position tooltip below or above depending on space
            const spaceBelow = window.innerHeight - rect.bottom;
            const topPos = spaceBelow > 200 ? rect.bottom + 20 : rect.top - 200;

            tooltip.style.top = `${topPos}px`;
            // Center horizontally relative to target, but keep on screen
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
    }
};

// ============================================
// CONTEXT MENU LOGIC
// ============================================

function initializeContextMenu() {
    const contextMenu = document.getElementById('context-menu');
    const chartArea = document.getElementById('main-chart-area');

    if (!contextMenu || !chartArea) return;

    // Open Menu
    chartArea.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        // Only show if we have data
        if (!AppState.sampleData) return;

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
        const action = e.target.closest('li')?.dataset.action;
        if (!action) return;

        contextMenu.classList.add('hidden');

        switch (action) {
            case 'reset-zoom':
                resetChartZoom();
                break;
            case 'zoom-region':
                if (mainChart) mainChart.zoom(1.5);
                break;
            case 'mark-peak':
                markPeakAtClick();
                break;
            case 'add-annotation':
                showToast('Annotation', 'Annotation added to report', 'success');
                break;
            case 'copy-value':
                copyValueToClipboard();
                break;
        }
    });
}

function markPeakAtClick() {
    if (!mainChart || !AppState.lastContextClick) return;

    const rect = document.getElementById('ftir-chart').getBoundingClientRect();
    const x = AppState.lastContextClick.x - rect.left;
    const xValue = mainChart.scales.x.getValueForPixel(x);

    // Find nearest peak in data
    const nearest = AppState.peaksDetected.reduce((prev, curr) => {
        return (Math.abs(curr.position - xValue) < Math.abs(prev.position - xValue) ? curr : prev);
    }, { position: -999 });

    if (Math.abs(nearest.position - xValue) < 50) {
        showToast('Peak Marked', `Peak at ${nearest.position.toFixed(1)} cm⁻¹ highlighted`, 'info');
        // Logic to highlight specific annotation could go here
    } else {
        showToast('No Peak', 'No significant peak found at this location', 'warning');
    }
}

function copyValueToClipboard() {
    if (!mainChart || !AppState.lastContextClick) return;

    const rect = document.getElementById('ftir-chart').getBoundingClientRect();
    const x = AppState.lastContextClick.x - rect.left;
    const y = AppState.lastContextClick.y - rect.top;

    const xValue = mainChart.scales.x.getValueForPixel(x);
    const yValue = mainChart.scales.y.getValueForPixel(y);

    const text = `${xValue.toFixed(2)} cm⁻¹, ${yValue.toFixed(4)} A`;

    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied', 'Spectral data copied to clipboard', 'success');
    });
}

// ============================================
// FINAL BOOTSTRAPPER
// ============================================

// Add the context menu listener initialization to the startup sequence
(function () {
    // We hook into the existing window load or init if possible, 
    // or simply run this setup immediately as DOMContentLoaded has likely fired 
    // by the time this script chunk is parsed if appended.
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        initializeContextMenu();
    } else {
        document.addEventListener('DOMContentLoaded', initializeContextMenu);
    }
})();