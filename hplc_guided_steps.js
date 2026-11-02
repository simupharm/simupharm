/* ================================================================
   HPLC Guided Experiment — "Assay of Paracetamol by RP-HPLC"
   
   Step-by-step teaching config for the GuidedTeacher engine.
   Loaded after guided_teacher.js and voice_engine.js.
   ================================================================ */
document.addEventListener('DOMContentLoaded', () => {
    // Only init if GuidedTeacher exists
    if (typeof GuidedTeacher === 'undefined') return;

    const HPLC_GUIDED_STEPS = [
        {
            id: 'intro',
            title: 'Welcome to HPLC',
            icon: 'flask',
            instruction: `Welcome to the <strong>High-Performance Liquid Chromatography (HPLC)</strong> simulator. Today we'll perform a reverse-phase HPLC analysis of <strong>Paracetamol</strong>.<br><br>HPLC separates compounds in a liquid mixture by pumping them at high pressure through a column packed with tiny solid particles. Different compounds interact differently with the column, causing them to elute (come out) at different times.`,
            speak: 'Welcome to the HPLC simulator. Today we will perform a reverse-phase HPLC analysis of Paracetamol. HPLC separates compounds in a liquid mixture by pumping them at high pressure through a column packed with tiny solid particles. Different compounds interact differently with the column, causing them to elute at different times.',
            highlight: '#hplc-main-view .instrument-container',
            action: 'Look at the HPLC instrument overview. Click Next when ready.',
            theory: 'HPLC was developed in the 1960s and has become the most widely used analytical technique in pharmaceutical analysis. It is used for drug assay, impurity profiling, dissolution testing, and stability studies. The Indian Pharmacopoeia (IP) and USP both require HPLC methods for most drug monographs.'
        },
        {
            id: 'startup',
            title: 'System Startup',
            icon: 'power-off',
            instruction: `First, we need to <strong>power on the HPLC system</strong>. In a real lab, you'd check that all modules are connected, solvent lines are in the bottles, and the waste container is not full.<br><br>Click the <strong>System Startup</strong> button to begin the startup sequence.`,
            speak: 'First, we need to power on the HPLC system. In a real lab, you would check that all modules are connected, the solvent lines are in the bottles, and the waste container is not full. Click the System Startup button to begin.',
            highlight: '#hotspot-setup',
            action: 'Click the "System Startup" button on the instrument.',
            theory: 'Before powering on an HPLC, always ensure: 1) Solvent bottles are filled and properly capped with line filters submerged. 2) The waste bottle is not full. 3) All fluidic connections are tight. 4) The column is connected in the correct flow direction (check the arrow). A dry pump can be damaged quickly.'
        },
        {
            id: 'mobile_phase',
            title: 'Mobile Phase Configuration',
            icon: 'vial',
            instruction: `Now let's configure the <strong>mobile phase</strong>. For Paracetamol analysis, we'll use a <strong>60:40 mixture of Methanol and Water</strong>.<br><br>The mobile phase is the liquid that carries your sample through the column. Its composition determines how well compounds separate.<br><br>Click the <strong>Mobile Phase</strong> hotspot on the instrument.`,
            speak: 'Now let us configure the mobile phase. For Paracetamol, we will use a 60 to 40 mixture of Methanol and Water. The mobile phase carries your sample through the column. Its composition determines how well the compounds separate. Click the Mobile Phase hotspot.',
            highlight: '#hotspot-solvents',
            action: 'Click the Mobile Phase hotspot to configure solvents.',
            theory: 'Why 60:40 Methanol:Water? Paracetamol has a logP of 0.46, meaning it is slightly hydrophobic. A moderate organic content (60% methanol) provides good retention without excessive run time. Increasing organic content (e.g., 80:20) would make paracetamol elute faster but could reduce separation from related substances. Water is the weak solvent in reverse-phase HPLC because it has low eluting strength on C18 columns.'
        },
        {
            id: 'pump_config',
            title: 'Pump & Flow Rate Setup',
            icon: 'cogs',
            instruction: `Set the <strong>flow rate to 1.0 mL/min</strong>. This is the standard flow rate for a 4.6 mm internal diameter column.<br><br>Higher flow rates reduce analysis time but increase back-pressure and may reduce chromatographic resolution. The injection volume should be <strong>20 µL</strong>, which is standard for analytical HPLC.<br><br>Click the <strong>Pump</strong> hotspot to configure.`,
            speak: 'Set the flow rate to 1.0 milliliters per minute. This is standard for a 4.6 millimeter column. Higher flow rates reduce analysis time but increase pressure and may reduce resolution. Set the injection volume to 20 microliters. Click the Pump hotspot to configure.',
            highlight: '#hotspot-pump',
            action: 'Click the Pump hotspot. Set flow rate = 1.0 mL/min, injection volume = 20 µL.',
            theory: 'The relationship between flow rate and pressure follows Darcys Law: ΔP = (ηFL)/(Kπr²), where η is mobile phase viscosity, F is flow rate, L is column length, K is column permeability, and r is column radius. Doubling the flow rate approximately doubles the pressure. The Van Deemter equation shows that there is an optimum flow rate that gives the best plate count — typically around 1.0 mL/min for 5µm particles.'
        },
        {
            id: 'column_selection',
            title: 'Column Selection & Temperature',
            icon: 'thermometer-half',
            instruction: `Select the <strong>C18 reverse-phase column</strong> (250 × 4.6 mm, 5 µm). C18 columns have octadecyl carbon chains bonded to silica particles — they retain non-polar compounds and are the workhorse of pharmaceutical analysis.<br><br>Set the column temperature to <strong>30°C</strong>. Temperature control ensures reproducible retention times.`,
            speak: 'Select the C18 reverse-phase column. C18 columns have 18-carbon chains bonded to silica. They retain non-polar compounds and are the most common column in pharmaceutical analysis. Set the column temperature to 30 degrees Celsius for reproducible results.',
            highlight: '#hotspot-column',
            action: 'Click the Column hotspot. Select C18, set temperature = 30°C.',
            theory: 'Why C18? In reverse-phase HPLC, the stationary phase is non-polar (C18 chains) and the mobile phase is polar (water + organic modifier). Non-polar analytes are retained longer. Paracetamol, with moderate hydrophobicity (logP = 0.46), has adequate retention on C18. Column temperature affects: 1) Mobile phase viscosity (lower viscosity at higher temperature reduces pressure), 2) Retention time (typically decreases 1-2% per °C increase), 3) Selectivity (can change peak elution order). 30°C is a standard starting point recommended by USP.'
        },
        {
            id: 'detector_setup',
            title: 'UV Detector Configuration',
            icon: 'sun',
            instruction: `Set the UV detector wavelength to <strong>243 nm</strong>. This is the <strong>lambda-max (λmax)</strong> of Paracetamol — the wavelength where it absorbs UV light most strongly, giving maximum sensitivity.<br><br>Click the <strong>UV Detector</strong> hotspot.`,
            speak: 'Set the UV detector wavelength to 243 nanometers. This is the lambda-max of Paracetamol — the wavelength where it absorbs light most strongly, giving maximum sensitivity for detection. Click the UV Detector hotspot.',
            highlight: '#hotspot-detector',
            action: 'Click the Detector hotspot. Set wavelength = 243 nm.',
            theory: 'Beer-Lambert Law: A = εlc, where A is absorbance, ε is molar absorptivity, l is path length (1 cm in detector flow cell), and c is concentration. At λmax, ε is highest, so sensitivity is maximized. Paracetamol has ε = 13,500 L/mol·cm at 243 nm. Some IP methods specify 257 nm for paracetamol — this is an alternative λmax. Using 243 nm gives slightly better sensitivity. Always check the pharmacopeial monograph for the official detection wavelength.'
        },
        {
            id: 'compound_select',
            title: 'Sample Selection',
            icon: 'flask',
            instruction: `Now we need to select our sample. In the Pump & Autosampler configuration, select <strong>Paracetamol Standard</strong> from the sample vial dropdown.<br><br>In a real analysis, you would prepare a standard solution by dissolving an accurately weighed quantity of Paracetamol reference standard in the mobile phase.`,
            speak: 'Select Paracetamol Standard from the sample vial dropdown. In a real lab, you would prepare a standard solution by accurately weighing the reference standard and dissolving it in the mobile phase.',
            highlight: '#hotspot-pump',
            action: 'Open Pump config → select "Paracetamol Standard" from the Sample Vial dropdown.',
            theory: 'Sample preparation is critical in HPLC. For a standard solution: 1) Weigh accurately (~10 mg) using an analytical balance. 2) Transfer to a volumetric flask (100 mL). 3) Dissolve in a small portion of mobile phase. 4) Make up to volume. 5) Filter through a 0.45 µm membrane filter (PVDF or nylon). Particulate matter can clog the column and frit, causing high backpressure and poor peak shapes.'
        },
        {
            id: 'run_screen',
            title: 'Navigate to Run Screen',
            icon: 'desktop',
            instruction: `Click the <strong>Instrument Screen</strong> hotspot to enter the chromatogram view. This is where you'll see the real-time chromatogram, run controls, and live instrument parameters.<br><br>This is equivalent to switching to the data acquisition software on a real HPLC.`,
            speak: 'Click the Instrument Screen hotspot to enter the chromatogram view. This is where you will see the real-time chromatogram and run controls. This is equivalent to the data acquisition software on a real HPLC.',
            highlight: '#hotspot-screen',
            action: 'Click the "Instrument Screen" hotspot to enter run mode.'
        },
        {
            id: 'start_run',
            title: 'Start the Analysis',
            icon: 'play',
            instruction: `Everything is configured. Click the green <strong>Run</strong> button to inject the sample and begin data acquisition.<br><br>Watch the chromatogram develop in real-time! The detector signal (absorbance in mAU) is plotted against time (minutes). You should see the Paracetamol peak appear.<br><br>💡 <strong>Tip:</strong> Toggle "Instant Result" if you want to skip the real-time animation.`,
            speak: 'Everything is configured. Click the green Run button to inject the sample and begin data acquisition. Watch the chromatogram develop in real-time! The detector signal is plotted against time. You should see the Paracetamol peak appear.',
            highlight: '#run-button',
            action: 'Click the "Run" button to start the analysis.',
            theory: 'When you press Run: 1) The autosampler needle draws sample from the vial. 2) The sample is loaded into a sample loop (fixed volume). 3) The injection valve switches, and mobile phase sweeps the sample onto the column. 4) Compounds travel through the column at different rates based on their interaction with the C18 stationary phase. 5) As they elute, the UV detector measures their absorbance. 6) The signal is recorded as a chromatogram.'
        },
        {
            id: 'interpret_results',
            title: 'Interpret the Chromatogram',
            icon: 'chart-line',
            instruction: `Excellent! Look at the chromatogram. The <strong>Paracetamol peak</strong> should appear at approximately <strong>3.2 minutes</strong> (retention time).<br><br>Key parameters to note:<br>• <strong>Retention Time (RT):</strong> Time from injection to peak maximum<br>• <strong>Peak Area:</strong> Proportional to the amount of compound<br>• <strong>Peak Height:</strong> Maximum detector response<br>• <strong>Tailing Factor:</strong> Should be < 1.5 (USP requirement)`,
            speak: 'Excellent! Look at the chromatogram. The Paracetamol peak should appear at approximately 3.2 minutes. Key parameters include: Retention time, which is the time from injection to peak maximum. Peak area, which is proportional to the amount of compound. And tailing factor, which should be less than 1.5 per USP requirements.',
            highlight: '.chromatogram-section',
            action: 'Observe the chromatogram. Note the retention time and peak shape.',
            theory: 'Quantification in HPLC uses the external standard method: 1) Run a standard solution of known concentration. 2) Record its peak area. 3) Run the sample. 4) Calculate: Amount = (Area_sample / Area_standard) × Concentration_standard × Dilution factor. For related substances testing, individual impurity peaks are compared to the principal peak using relative area percentages. IP and USP specify acceptance limits for each known and unknown impurity.'
        },
        {
            id: 'sst',
            title: 'System Suitability Testing (SST)',
            icon: 'clipboard-check',
            instruction: `Finally, check the <strong>System Suitability Test (SST)</strong> parameters. USP General Chapter <621> requires these before any analytical run is valid:<br><br>• <strong>Resolution (R):</strong> ≥ 2.0 between adjacent peaks<br>• <strong>Tailing Factor (T):</strong> ≤ 1.5<br>• <strong>Theoretical Plates (N):</strong> ≥ 2000<br>• <strong>%RSD:</strong> ≤ 2.0% (for replicate injections)<br><br>Click the <strong>SST Report</strong> button to view results.`,
            speak: 'Finally, check the System Suitability Test parameters. USP requires: Resolution greater than 2.0, Tailing Factor less than 1.5, Theoretical Plates greater than 2000, and percent RSD less than 2%. Click the SST Report button to view results.',
            highlight: '#sst-report-button',
            action: 'Click "SST Report" to view system suitability parameters.',
            theory: 'System Suitability Testing (SST) ensures the chromatographic system is performing adequately for the intended analysis. It is performed BEFORE running actual samples. If SST fails, results are invalid. Theoretical plates N = 16(tR/W)² where tR is retention time and W is peak width at base. Tailing factor T = W₀.₀₅/(2f) where W₀.₀₅ is width at 5% height and f is the front half-width. Resolution Rs = 2(tR₂ - tR₁)/(W₁ + W₂). These parameters are calculated automatically by the data system.'
        },
        {
            id: 'completion',
            title: 'Experiment Complete!',
            icon: 'trophy',
            instruction: `<strong>Congratulations!</strong> You have successfully completed an HPLC analysis of Paracetamol using the reverse-phase method.<br><br>You now understand:<br>• Mobile phase selection and its effect on separation<br>• Column selection and temperature control<br>• UV detector wavelength optimization<br>• Chromatogram interpretation<br>• System suitability testing per USP guidelines`,
            speak: 'Congratulations! You have successfully completed an HPLC analysis of Paracetamol using the reverse-phase method. You now understand mobile phase selection, column configuration, detector setup, chromatogram interpretation, and system suitability testing.',
            highlight: null,
            completion: {
                title: 'HPLC Analysis Complete!',
                message: 'You\'ve mastered the basics of RP-HPLC analysis. Try changing parameters and observing how the chromatogram changes.'
            }
        }
    ];

    GuidedTeacher.init({
        title: 'Assay of Paracetamol by RP-HPLC',
        steps: HPLC_GUIDED_STEPS,
        voiceEnabled: true,
        onComplete: () => {
            // Track completion
            const progress = JSON.parse(localStorage.getItem('simupharma_progress') || '{}');
            progress.hplc_guided = true;
            progress.guided_completed = (progress.guided_completed || 0) + 1;
            localStorage.setItem('simupharma_progress', JSON.stringify(progress));
        }
    });
});
