const fs = require('fs');
const vm = require('vm');

const scriptContent = fs.readFileSync('hplc_simulator_script.js', 'utf8');

// Create mock browser DOM environment so hplc_simulator_script.js doesn't fail on window/document/gsap
const sandbox = {
    window: {},
    document: {
        addEventListener: () => {},
        getElementById: () => null,
        querySelector: () => null,
        querySelectorAll: () => []
    },
    navigator: { userAgent: 'Node.js/Test-Environment' },
    console: console,
    Math: Math,
    setTimeout: setTimeout,
    clearTimeout: clearTimeout,
    setInterval: setInterval,
    clearInterval: clearInterval,
    gsap: { to: () => {} }
};
sandbox.window = sandbox;

vm.createContext(sandbox);

// Wrap script to expose CONFIG, COMPOUND_LIBRARY, PhysicsEngine, Simulation
const wrappedCode = scriptContent + `
;globalThis.EXPORTS = {
    CONFIG: typeof CONFIG !== 'undefined' ? CONFIG : null,
    COMPOUND_LIBRARY: typeof COMPOUND_LIBRARY !== 'undefined' ? COMPOUND_LIBRARY : null,
    PhysicsEngine: typeof PhysicsEngine !== 'undefined' ? PhysicsEngine : null,
    Simulation: typeof Simulation !== 'undefined' ? Simulation : null
};
`;

try {
    vm.runInContext(wrappedCode, sandbox);
    console.log("Successfully evaluated hplc_simulator_script.js!");
    const { CONFIG, COMPOUND_LIBRARY, PhysicsEngine, Simulation } = sandbox.globalThis.EXPORTS;
    
    console.log("CONFIG columns:", Object.keys(CONFIG.columns));
    console.log("COMPOUND_LIBRARY count:", Object.keys(COMPOUND_LIBRARY).length);
    console.log("Compounds:", Object.keys(COMPOUND_LIBRARY));
    
    // Test calculateRetentionTime for Paracetamol, Caffeine, Aspirin, Ibuprofen
    const analytes = ['Paracetamol', 'Caffeine', 'Aspirin', 'Ibuprofen'];
    console.log("\n--- Testing Standard Isocratic Conditions (50% B, 1.0 mL/min, 30C, C18) ---");
    analytes.forEach(name => {
        const compound = COMPOUND_LIBRARY[name];
        const rt = PhysicsEngine.calculateRetentionTime(compound, {
            flowRate: 1.0,
            columnTemp: 30,
            columnType: 'C18',
            gradientProgram: [{ time: 0, percentB: 50 }, { time: 10, percentB: 50 }],
            getPercentBAtTime: (t) => 50
        });
        const plates = PhysicsEngine.calculateTheoreticalPlates(1.0, 'C18');
        const width = PhysicsEngine.calculatePeakWidth(rt, plates, compound.asymmetry);
        console.log(`  ${name.padEnd(12)}: tR = ${rt.toFixed(3)} min, width = ${width.toFixed(4)} min, plates = ${plates}`);
    });

    console.log("\n--- Testing Gradient Conditions (10% to 70% B over 10 min, 1.0 mL/min, 30C, C18) ---");
    const getPercentB = (t) => {
        if (t <= 0) return 10;
        if (t >= 10) return 70;
        return 10 + (60 / 10) * t;
    };
    analytes.forEach(name => {
        const compound = COMPOUND_LIBRARY[name];
        const rt = PhysicsEngine.calculateRetentionTime(compound, {
            flowRate: 1.0,
            columnTemp: 30,
            columnType: 'C18',
            gradientProgram: [{ time: 0, percentB: 10 }, { time: 10, percentB: 70 }],
            getPercentBAtTime: getPercentB
        });
        console.log(`  ${name.padEnd(12)}: Gradient tR = ${rt.toFixed(3)} min`);
    });

    console.log("\n--- Testing Pressure Calculation ---");
    [10, 30, 50, 70, 90].forEach(pctB => {
        const p = PhysicsEngine.calculatePressure(1.0, pctB, 'C18', 30, 'acetonitrile');
        console.log(`  ACN %B = ${pctB}%: Pressure = ${p.toFixed(1)} bar`);
    });

} catch (e) {
    console.error("Execution error:", e);
}
