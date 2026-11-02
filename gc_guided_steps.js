/* ================================================================
   GC Guided Experiment — "Residual Solvent Analysis by GC"
   
   Step-by-step teaching config for the GuidedTeacher engine.
   Loaded after guided_teacher.js and voice_engine.js.
   ================================================================ */
document.addEventListener('DOMContentLoaded', () => {
    if (typeof GuidedTeacher === 'undefined') return;

    const GC_GUIDED_STEPS = [
        {
            id: 'intro',
            title: 'Welcome to Gas Chromatography',
            icon: 'fire',
            instruction: `Welcome to the <strong>Gas Chromatograph (GC)</strong> simulator. Today we'll perform <strong>residual solvent analysis</strong> — a critical USP/ICH requirement for pharmaceutical products.<br><br>GC separates volatile compounds by vaporizing them and carrying them through a heated column with a carrier gas. Different compounds interact with the column coating and elute at different times.`,
            speak: 'Welcome to the Gas Chromatograph simulator. Today we will perform residual solvent analysis, a critical USP and ICH requirement for pharmaceutical products. GC separates volatile compounds by vaporizing them and carrying them through a heated column using a carrier gas.',
            highlight: '#gc-main-view .instrument-display-area',
            action: 'Observe the GC instrument. Click Next when ready.',
            theory: 'Gas Chromatography was invented in 1952 by James and Martin. It is the gold standard for analyzing volatile and semi-volatile compounds. In pharma, GC is mandatory (USP <467>, ICH Q3C) for testing residual solvents — organic solvents remaining from manufacturing. Class 1 solvents (benzene, carbon tetrachloride) are toxic and must be avoided. Class 2 has limited exposure. Class 3 solvents (ethanol, acetone) are low toxicity.'
        },
        {
            id: 'carrier_gas',
            title: 'Carrier Gas Setup',
            icon: 'wind',
            instruction: `The <strong>carrier gas</strong> (mobile phase in GC) pushes the sample through the column. We'll use <strong>Helium</strong> — the most common carrier gas for GC-FID.<br><br>Check that:<br>• Gas line pressure is adequate (~60 psi tank pressure)<br>• No leaks at connections<br>• Flow rate is set correctly<br><br>Click the <strong>Carrier Gas</strong> hotspot.`,
            speak: 'The carrier gas pushes the sample through the column. We will use Helium, the most common carrier for GC with FID detection. Check that gas pressure is adequate, there are no leaks, and flow rate is correct. Click the Carrier Gas hotspot.',
            highlight: '#hotspot-gas',
            action: 'Click the Carrier Gas hotspot to verify gas supply.',
            theory: 'Carrier gas choices: Helium — most popular, inert, good efficiency, but expensive. Hydrogen — best efficiency (fastest analysis), flammable risk. Nitrogen — cheapest, but gives worst peak efficiency at high flow rates. For FID detection, helium or hydrogen is preferred because nitrogen reduces FID sensitivity. The carrier gas must be ultra-high purity (>99.999%) to avoid baseline noise and column degradation.'
        },
        {
            id: 'inlet_config',
            title: 'Injection Port Configuration',
            icon: 'syringe',
            instruction: `Configure the <strong>split/splitless inlet</strong>:<br><br>• <strong>Mode:</strong> Split (50:1 ratio) — diverts most of the sample to waste, preventing column overload<br>• <strong>Inlet Temperature:</strong> 250°C — must be hot enough to vaporize all sample components<br>• <strong>Injection Volume:</strong> 1.0 µL — standard for liquid injection<br><br>Click the <strong>Injection Port</strong> hotspot.`,
            speak: 'Configure the split splitless inlet. Set split mode at 50 to 1 ratio, inlet temperature to 250 degrees Celsius to vaporize the sample, and injection volume to 1 microliter. Click the Injection Port hotspot.',
            highlight: '#hotspot-injector',
            action: 'Click the Injection Port hotspot. Set split 50:1, 250°C, 1 µL.',
            theory: 'Split injection: The sample vaporizes in the hot liner, mixes with carrier gas, and is split — only a fraction (1/50 at 50:1 ratio) enters the column. This prevents column overload for concentrated samples. Splitless mode: All sample enters the column — used for trace analysis where maximum sensitivity is needed. The inlet temperature should be 20-50°C above the boiling point of the highest-boiling analyte.'
        },
        {
            id: 'column_setup',
            title: 'Column Selection',
            icon: 'ring',
            instruction: `Select the column for residual solvents. We'll use:<br><br>• <strong>Column:</strong> DB-624 (6% cyanopropylphenyl / 94% dimethylpolysiloxane)<br>• <strong>Dimensions:</strong> 30 m × 0.53 mm × 3.0 µm<br>• <strong>Purpose:</strong> Designed specifically for volatile organic compounds (VOCs)<br><br>Click the <strong>Column</strong> hotspot.`,
            speak: 'Select the D B 624 column, which is designed specifically for volatile organic compounds. Its dimensions are 30 meters by 0.53 millimeters with 3 micrometer film thickness. Click the Column hotspot.',
            highlight: '#hotspot-column',
            action: 'Click the Column hotspot. Select DB-624.',
            theory: 'Column selection depends on analyte polarity: Non-polar columns (DB-1, HP-5) — hydrocarbons, non-polar analytes. Mid-polarity (DB-624) — VOCs, residual solvents. Polar (DB-WAX, DB-FFAP) — alcohols, fatty acids, flavors. For residual solvents (USP <467>), DB-624 or G43 phase is specified. Wide bore columns (0.53 mm ID) are preferred for headspace analysis because they tolerate larger injection volumes.'
        },
        {
            id: 'oven_program',
            title: 'Temperature Program',
            icon: 'temperature-high',
            instruction: `The oven temperature program controls separation. For residual solvents:<br><br>• <strong>Initial:</strong> 40°C, hold 2 min (let light solvents elute)<br>• <strong>Ramp 1:</strong> 10°C/min to 150°C (separate mid-boiling solvents)<br>• <strong>Ramp 2:</strong> 15°C/min to 250°C, hold 5 min (elute heavy solvents)<br><br>Click the <strong>Column Oven</strong> hotspot.`,
            speak: 'Program the oven temperature. Start at 40 degrees and hold for 2 minutes, then ramp at 10 degrees per minute to 150, then 15 degrees per minute to 250 with a 5 minute hold. Click the Column Oven hotspot.',
            highlight: '#hotspot-oven',
            action: 'Click the Oven hotspot. Set the temperature program.',
            theory: 'Temperature programming is essential for separating compounds with a wide boiling point range. At low temperature, light solvents (methanol BP 65°C, acetone BP 56°C) separate well. Higher temperatures elute heavier solvents (DMF BP 153°C, DMSO BP 189°C). The hold time at the final temperature ensures all compounds elute ("column cleanup"). Too fast a ramp reduces resolution; too slow wastes time.'
        },
        {
            id: 'detector_setup',
            title: 'FID Detector Setup',
            icon: 'fire-alt',
            instruction: `Set up the <strong>Flame Ionization Detector (FID)</strong>:<br><br>• <strong>Detector Temperature:</strong> 300°C (must exceed highest oven temp)<br>• <strong>H₂ Flow:</strong> 40 mL/min<br>• <strong>Air Flow:</strong> 400 mL/min<br>• <strong>Makeup Gas:</strong> 25 mL/min (N₂)<br><br>Click the <strong>FID Detector</strong> hotspot.`,
            speak: 'Set up the Flame Ionization Detector. Temperature 300 degrees, hydrogen flow 40 milliliters per minute, air flow 400, and nitrogen makeup gas at 25 milliliters per minute. Click the FID Detector hotspot.',
            highlight: '#hotspot-detector',
            action: 'Click the Detector hotspot. Configure FID settings.',
            theory: 'FID principle: Organic compounds burn in the hydrogen/air flame, producing ions (CHO⁺). These ions are collected by an electrode, generating a current proportional to the number of carbon atoms. FID is nearly universal for organic compounds (responds to anything with C-H bonds), has excellent linearity (10⁷ range), and is very sensitive (~10 pg). It does NOT respond to: water, CO₂, N₂, O₂, CS₂, H₂S, noble gases, or fully halogenated/oxidized compounds.'
        },
        {
            id: 'run_screen',
            title: 'Enter Run Mode',
            icon: 'desktop',
            instruction: `Click the <strong>Instrument Control</strong> screen to enter the ChemStation software view. This is where you'll configure the sample, start the run, and view the real-time chromatogram.`,
            speak: 'Click the Instrument Control screen to enter the ChemStation software. Here you will configure the sample, start the acquisition, and view the real-time chromatogram.',
            highlight: '#hotspot-screen',
            action: 'Click the screen hotspot to enter software view.'
        },
        {
            id: 'start_run',
            title: 'Start the Analysis',
            icon: 'play',
            instruction: `Select an appropriate sample (e.g., <strong>ICH Class 2 Mix</strong> or <strong>Alcohol Mix</strong>) and click <strong>"Start Run"</strong>.<br><br>Watch the chromatogram develop! Each peak represents a different solvent. The FID signal (in picoamps) is plotted against time. Peaks appear in order of boiling point — lighter solvents elute first.`,
            speak: 'Select a sample such as ICH Class 2 Mix and click Start Run. Watch the chromatogram develop. Each peak represents a different solvent. Lighter solvents with lower boiling points elute first.',
            highlight: '#start-run-button',
            action: 'Select sample → Click "Start Run".',
            theory: 'During a GC run: The sample is injected and vaporized in the hot inlet. The carrier gas sweeps vapors onto the column. Inside the column, compounds partition between the gas phase (mobile) and the liquid film (stationary). Less volatile compounds spend more time in the stationary phase, so they elute later. The temperature ramp gradually increases column temperature, forcing heavier compounds off the column.'
        },
        {
            id: 'interpret',
            title: 'Interpret the Chromatogram',
            icon: 'chart-line',
            instruction: `After the run completes, click <strong>"Integrate"</strong> to detect and quantify peaks. Then click <strong>"Identify"</strong> to match peaks against the compound library.<br><br>Key parameters:<br>• <strong>Retention Time:</strong> Identifies the compound<br>• <strong>Peak Area:</strong> Proportional to concentration<br>• <strong>Resolution:</strong> Should be >1.5 between adjacent peaks`,
            speak: 'After the run, click Integrate to detect peaks, then Identify to match against the library. Key parameters include retention time for identification, peak area for quantification, and resolution which should exceed 1.5 between adjacent peaks.',
            highlight: '#integrate-button',
            action: 'Click "Integrate" then "Identify" to analyze results.',
            theory: 'Quantification in residual solvents uses the Standard Solution Comparison method (USP <467>). Prepare standard solutions at the ICH concentration limit for each solvent. If the sample peak area < standard peak area at the limit concentration, the solvent passes. ICH limits: Class 1 solvents have ppm-level limits (e.g., benzene ≤ 2 ppm). Class 2 limits range from 50-3880 ppm. Class 3 solvents are limited to 5000 ppm each.'
        },
        {
            id: 'completion',
            title: 'Experiment Complete!',
            icon: 'trophy',
            instruction: `<strong>Congratulations!</strong> You have successfully completed a GC analysis for residual solvents.<br><br>You now understand:<br>• Carrier gas selection and flow setup<br>• Split/splitless injection modes<br>• Temperature programming for separation<br>• FID detector operation and response<br>• Chromatogram interpretation and peak identification<br>• ICH/USP residual solvent requirements`,
            speak: 'Congratulations! You have successfully completed a GC residual solvent analysis. You now understand carrier gas setup, injection modes, temperature programming, FID detection, chromatogram interpretation, and I C H requirements.',
            highlight: null,
            completion: {
                title: 'GC Analysis Complete!',
                message: 'You\'ve mastered GC fundamentals. Try different samples and observe how temperature programs affect separation!'
            }
        }
    ];

    GuidedTeacher.init({
        title: 'Residual Solvent Analysis by GC',
        steps: GC_GUIDED_STEPS,
        voiceEnabled: true,
        onComplete: () => {
            const progress = JSON.parse(localStorage.getItem('simupharma_progress') || '{}');
            progress.gc_guided = true;
            progress.guided_completed = (progress.guided_completed || 0) + 1;
            localStorage.setItem('simupharma_progress', JSON.stringify(progress));
        }
    });
});
