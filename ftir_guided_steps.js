/* ================================================================
   FTIR Guided Experiment — "Identification of Paracetamol by FTIR"
   
   Step-by-step teaching config for the GuidedTeacher engine.
   Loaded after guided_teacher.js and voice_engine.js.
   ================================================================ */
document.addEventListener('DOMContentLoaded', () => {
    if (typeof GuidedTeacher === 'undefined') return;

    const FTIR_GUIDED_STEPS = [
        {
            id: 'intro',
            title: 'Welcome to FTIR',
            icon: 'wave-square',
            instruction: `Welcome to the <strong>Fourier Transform Infrared (FTIR)</strong> spectrometer simulator. Today we'll identify <strong>Paracetamol</strong> by its infrared spectrum.<br><br>FTIR works by passing infrared light through a sample. Different chemical bonds absorb specific frequencies of IR light, creating a unique "fingerprint" spectrum for each compound.`,
            speak: 'Welcome to the FTIR spectrometer simulator. Today we will identify Paracetamol by its infrared spectrum. FTIR works by passing infrared light through a sample. Different chemical bonds absorb specific frequencies, creating a unique fingerprint spectrum for each compound.',
            highlight: '#ftir-main-view .instrument-display-area',
            action: 'Observe the FTIR instrument. Click Next when ready.',
            theory: 'FTIR spectroscopy is based on molecular vibrations. When IR radiation matches the natural frequency of a bond vibration, the molecule absorbs that energy. The resulting absorption spectrum reveals the functional groups present. The Fourier Transform technique uses an interferometer to measure all wavelengths simultaneously, making it much faster than old dispersive instruments.'
        },
        {
            id: 'system_check',
            title: 'System Check',
            icon: 'stethoscope',
            instruction: `Before any measurement, we need to verify the instrument is working correctly. The FTIR has several key components:<br><br>• <strong>Globar IR Source</strong> — ceramic element heated to ~1100°C<br>• <strong>Michelson Interferometer</strong> — splits and recombines the IR beam<br>• <strong>DTGS Detector</strong> — measures the intensity of transmitted light<br>• <strong>HeNe Laser</strong> — provides precise wavelength reference`,
            speak: 'Before any measurement, we verify the instrument. The FTIR has a Globar IR source heated to 1100 degrees, a Michelson interferometer that splits and recombines the IR beam, a D T G S detector, and a Helium Neon laser for wavelength reference.',
            highlight: '#hotspot-interferometer',
            action: 'Click the Interferometer hotspot to check instrument status.',
            theory: 'The Michelson interferometer is the heart of the FTIR. It contains a beamsplitter (KBr or ZnSe) that splits the IR beam into two paths. One mirror is fixed, the other moves. When the beams recombine, they create an interference pattern (interferogram). The Fourier Transform converts this time-domain signal into a frequency-domain spectrum.'
        },
        {
            id: 'background',
            title: 'Collect Background Spectrum',
            icon: 'adjust',
            instruction: `The first critical step is collecting a <strong>background spectrum</strong>. This measures the instrument response <strong>without any sample</strong> — it captures atmospheric CO₂, water vapor, and instrument characteristics.<br><br>The sample spectrum will be <strong>ratioed against this background</strong> to remove these contributions.<br><br>Click the <strong>Instrument Screen</strong> to enter the software view, then click <strong>"Collect Background"</strong>.`,
            speak: 'The first critical step is collecting a background spectrum without any sample. This measures atmospheric CO2, water vapor, and instrument characteristics. The sample spectrum will be ratioed against this background to remove these contributions. Enter the software view and click Collect Background.',
            highlight: '#hotspot-screen',
            action: 'Go to Software view → Click "Collect Background".',
            theory: 'Why background subtraction? IR spectroscopy is sensitive to atmospheric gases. CO2 has strong absorptions at 2349 cm⁻¹ and 667 cm⁻¹. Water vapor absorbs broadly at 3500-3800 cm⁻¹ and 1400-1900 cm⁻¹. Without background subtraction, these would interfere with your sample spectrum. The background should be renewed every 30 minutes or when conditions change.'
        },
        {
            id: 'sample_prep',
            title: 'Prepare the ATR Sample',
            icon: 'flask',
            instruction: `Now prepare the sample on the <strong>ATR (Attenuated Total Reflectance)</strong> accessory.<br><br>For ATR measurements:<br>• Place a small amount of Paracetamol powder on the <strong>diamond crystal</strong><br>• Apply pressure with the clamp to ensure good contact<br>• The IR beam bounces off the crystal surface, penetrating ~2 µm into the sample<br><br>Click the <strong>ATR Accessory</strong> hotspot.`,
            speak: 'Now prepare the sample on the ATR accessory. Place a small amount of Paracetamol powder on the diamond crystal and apply pressure with the clamp. The IR beam bounces off the crystal, penetrating about 2 micrometers into the sample. Click the ATR Accessory hotspot.',
            highlight: '#hotspot-atr',
            action: 'Click the ATR hotspot. Select Paracetamol as the sample.',
            theory: 'ATR is the most popular sampling technique in modern FTIR. The IR beam enters the crystal at an angle greater than the critical angle, causing total internal reflection. An evanescent wave penetrates a few micrometers into the sample at the crystal surface. Advantages: minimal sample preparation, works with solids/liquids/powders, non-destructive. Diamond ATR is preferred for hard samples because of its hardness (Mohs 10) and wide spectral range.'
        },
        {
            id: 'measure_sample',
            title: 'Measure Sample Spectrum',
            icon: 'play',
            instruction: `With the background collected and sample in place, click <strong>"Measure Sample"</strong> to acquire the sample spectrum.<br><br>The instrument will collect <strong>16 scans</strong> at <strong>4 cm⁻¹ resolution</strong> and automatically ratio against the background.<br><br>Watch the interferogram build up as scans are accumulated!`,
            speak: 'Click Measure Sample to acquire the spectrum. The instrument will collect 16 scans at 4 wavenumber resolution and automatically ratio against the background. Watch the interferogram build up as scans accumulate.',
            highlight: '#hotspot-screen',
            action: 'In Software view → Click "Measure Sample".',
            theory: 'Why 16 scans? Signal averaging improves the signal-to-noise ratio (SNR) by √n, where n is the number of scans. 16 scans gives 4× improvement over a single scan. For routine analysis, 16-32 scans is standard. Research applications may use 64-256 scans. Resolution of 4 cm⁻¹ is standard for most pharmaceutical applications — higher resolution (2 or 1 cm⁻¹) is rarely needed and increases measurement time.'
        },
        {
            id: 'view_spectrum',
            title: 'View the IR Spectrum',
            icon: 'chart-line',
            instruction: `Excellent! The spectrum is displayed. For Paracetamol, look for these key absorptions:<br><br>• <strong>3325 cm⁻¹</strong> — N-H stretch (amide)<br>• <strong>3160 cm⁻¹</strong> — O-H stretch (phenol)<br>• <strong>1654 cm⁻¹</strong> — C=O stretch (amide I band)<br>• <strong>1565 cm⁻¹</strong> — N-H bend (amide II band)<br>• <strong>1506 cm⁻¹</strong> — Aromatic C=C stretch<br>• <strong>1227 cm⁻¹</strong> — C-O stretch (phenol)`,
            speak: 'The spectrum is displayed. For Paracetamol, key absorptions include: N H stretch at 3325 wavenumbers, O H stretch at 3160, the amide carbonyl at 1654, N H bend at 1565, aromatic C C at 1506, and C O stretch at 1227 wavenumbers.',
            highlight: '.software-chart-area',
            action: 'Observe the spectrum. Note the major peaks.',
            theory: 'Paracetamol (acetaminophen) is N-(4-hydroxyphenyl)acetamide. Its IR spectrum shows: the amide N-H stretch as a sharp peak near 3325 cm⁻¹, the phenolic O-H as a broader absorption near 3160 cm⁻¹, and the characteristic amide I (C=O stretch) and amide II (N-H bend coupled with C-N stretch) bands. The fingerprint region below 1500 cm⁻¹ is unique to each compound and essential for identification.'
        },
        {
            id: 'peak_pick',
            title: 'Peak Detection',
            icon: 'crosshairs',
            instruction: `Use the <strong>Find Peaks</strong> tool to automatically detect and label all significant peaks in the spectrum.<br><br>The software uses a peak-picking algorithm based on the second derivative — it identifies intensity minima (maxima in absorbance) and labels them with their wavenumber positions.`,
            speak: 'Use the Find Peaks tool to automatically detect and label all significant peaks. The software identifies peaks using a second derivative algorithm and labels them with their wavenumber positions.',
            highlight: '#find-peaks-btn',
            action: 'Click "Find Peaks" in the toolbar.',
            theory: 'Peak detection in FTIR uses the second derivative method. The second derivative of a Lorentzian or Gaussian peak has a minimum (negative) at the peak center. This is more reliable than simply finding minima in the transmittance spectrum, especially for overlapping peaks. The threshold setting controls sensitivity — too low detects noise, too high misses weak peaks.'
        },
        {
            id: 'functional_groups',
            title: 'Functional Group Analysis',
            icon: 'atom',
            instruction: `Now click <strong>"Functional Groups"</strong> to correlate the detected peaks with known functional group absorptions.<br><br>This automated analysis matches peak positions against the IR correlation table and identifies: O-H, N-H, C-H, C=O, C=C, C-O, and other functional groups.`,
            speak: 'Click Functional Groups to correlate detected peaks with known functional group absorptions. The analysis identifies O H, N H, C H, carbonyl, and other groups by matching peaks against the IR correlation table.',
            highlight: '#functional-group-btn',
            action: 'Click "Functional Groups" to run the analysis.',
            theory: 'IR correlation tables map wavenumber ranges to functional groups. Key regions: 4000-2500 cm⁻¹ (X-H stretches: O-H, N-H, C-H), 2500-2000 cm⁻¹ (triple bonds: C≡C, C≡N), 2000-1500 cm⁻¹ (double bonds: C=O, C=C, C=N), 1500-400 cm⁻¹ (fingerprint region: C-O, C-N, C-Cl bends). The fingerprint region below 1500 cm⁻¹ is unique for each compound.'
        },
        {
            id: 'library_search',
            title: 'Library Search & Identification',
            icon: 'search',
            instruction: `The most powerful identification tool: <strong>Library Search</strong>. This compares your measured spectrum against a database of reference spectra and calculates a <strong>match quality (%)</strong>.<br><br>Click <strong>"Identify"</strong> to run the search. Paracetamol should appear as the top match with >95% confidence.`,
            speak: 'Now use Library Search, the most powerful identification tool. This compares your spectrum against a database of references and calculates match quality. Click Identify to run the search. Paracetamol should be the top match with over 95 percent confidence.',
            highlight: '#identify-btn',
            action: 'Click "Identify" to run the library search.',
            theory: 'Spectral library searching uses mathematical algorithms to compare spectra. Common methods: 1) First derivative correlation — reduces baseline effects. 2) Euclidean distance — measures point-by-point difference. 3) Hit Quality Index (HQI) — normalized 0-100%, >95% is excellent match. Pharmacopeias (IP, USP) require that the IR spectrum of a sample "corresponds" to the reference standard spectrum for identity confirmation.'
        },
        {
            id: 'completion',
            title: 'Experiment Complete!',
            icon: 'trophy',
            instruction: `<strong>Congratulations!</strong> You have successfully identified Paracetamol using FTIR spectroscopy.<br><br>You now understand:<br>• Background collection and why it's essential<br>• ATR sampling technique<br>• Reading IR spectra and identifying key functional groups<br>• Using library search for compound identification<br>• Pharmacopeial IR identity testing`,
            speak: 'Congratulations! You have successfully identified Paracetamol using FTIR spectroscopy. You now understand background collection, ATR sampling, reading IR spectra, functional group identification, and library search for compound identification.',
            highlight: null,
            completion: {
                title: 'FTIR Analysis Complete!',
                message: 'You\'ve mastered FTIR identification. Try different compounds and observe how their spectra differ!'
            }
        }
    ];

    GuidedTeacher.init({
        title: 'Identification of Paracetamol by FTIR',
        steps: FTIR_GUIDED_STEPS,
        voiceEnabled: true,
        onComplete: () => {
            const progress = JSON.parse(localStorage.getItem('simupharma_progress') || '{}');
            progress.ftir_guided = true;
            progress.guided_completed = (progress.guided_completed || 0) + 1;
            localStorage.setItem('simupharma_progress', JSON.stringify(progress));
        }
    });
});
