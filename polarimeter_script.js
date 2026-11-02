/**
 * SimuPharma Digital Polarimeter Twin v3.1
 * Physically-accurate 3D optical-rotation simulator
 *
 * PART 1 of 3 — Constants, State, Scene Setup, Optical Components
 *
 * Coordinate convention
 *   Beam axis : +X  (lamp → detector, left → right)
 *   Up        : +Y
 *   Toward cam: +Z
 *
 * Polarisation convention
 *   Transmission axis of the polariser starts vertical (Y).
 *   Optical rotation α rotates the plane about +X.
 *   +α  ⟹  dextrorotatory  (clockwise looking toward the source)
 *   −α  ⟹  levorotatory
 */
document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // ═══════════════════════════════════════════════════════
    //  COMPOUND DATABASE
    //  specificRotation = literature [α]D²⁰ in degrees
    // ═══════════════════════════════════════════════════════
    const COMPOUNDS = {
        Sucrose: { name: 'Sucrose', formula: 'C12H22O11', mw: 342.30, specificRotation: 66.5, solvent: 'Water', cas: '57-50-1' },
        Glucose: { name: 'D-Glucose', formula: 'C6H12O6', mw: 180.16, specificRotation: 52.7, solvent: 'Water', cas: '50-99-7' },
        Fructose: { name: 'D-Fructose', formula: 'C6H12O6', mw: 180.16, specificRotation: -92.0, solvent: 'Water', cas: '57-48-7' },
        Tartaric_L: { name: 'L-(+)-Tartaric Acid', formula: 'C4H6O6', mw: 150.09, specificRotation: 12.0, solvent: 'Water', cas: '87-69-4' },
        Tartaric_D: { name: 'D-(−)-Tartaric Acid', formula: 'C4H6O6', mw: 150.09, specificRotation: -12.0, solvent: 'Water', cas: '147-71-7' },
        Camphor: { name: '(+)-Camphor', formula: 'C10H16O', mw: 152.23, specificRotation: 44.3, solvent: 'Ethanol', cas: '464-49-3' },
        Menthol: { name: '(−)-Menthol', formula: 'C10H20O', mw: 156.27, specificRotation: -50.0, solvent: 'Ethanol', cas: '2216-51-5' },
        Ibuprofen_S: { name: 'S-(+)-Ibuprofen', formula: 'C13H18O2', mw: 206.28, specificRotation: 59.0, solvent: 'Methanol', cas: '51146-56-6' },
        Naproxen_S: { name: 'S-(+)-Naproxen', formula: 'C14H14O3', mw: 230.26, specificRotation: 66.0, solvent: 'CHCl₃', cas: '22204-53-1' },
        Quinine: { name: '(−)-Quinine', formula: 'C20H24N2O2', mw: 324.42, specificRotation: -169.0, solvent: 'Ethanol', cas: '130-95-0' }
    };

    // ═══════════════════════════════════════════════════════
    //  FAULT PROFILES
    //    noise   – σ of Gaussian noise added to α (°)
    //    drift   – systematic offset (°)
    //    flicker – lamp intensity oscillation (0-1)
    // ═══════════════════════════════════════════════════════
    const FAULTS = {
        none: { noise: 0.002, drift: 0, flicker: 0 },
        bubble: { noise: 0.50, drift: 0.30, flicker: 0 },
        'dirty-tube': { noise: 0.10, drift: 0.05, flicker: 0 },
        'weak-lamp': { noise: 0.20, drift: 0.15, flicker: 0.35 }
    };

    // ═══════════════════════════════════════════════════════
    //  OPTICAL BENCH LAYOUT  (X-axis positions)
    // ═══════════════════════════════════════════════════════
    const BENCH = {
        lamp: -4.5,
        lensFront: -3.85,
        polarizer: -2.5,
        sampleStart: -1.65,
        sampleCenter: 0,
        sampleEnd: 1.65,
        analyzer: 2.5,
        detector: 4.5,
        beamY: 0.1          // beam centre-line height
    };

    // ═══════════════════════════════════════════════════════
    //  APPLICATION STATE
    // ═══════════════════════════════════════════════════════
    const STATE = {
        systemReady: false,
        wizardStep: 1,
        selectedSample: 'Sucrose',
        concentration: 0.10,       // g mL⁻¹
        pathLength: 1.0,        // dm
        temperature: 20.0,       // °C
        wavelength: 589.3,      // nm
        fault: 'none',
        isMeasuring: false,
        instantMode: false,
        lastResult: null,
        difficulty: 'beginner',
        _measureAnim: null
    };

    // ═══════════════════════════════════════════════════════
    //  THREE.JS OBJECT REFERENCES
    // ═══════════════════════════════════════════════════════
    let scene, camera, renderer, sceneGroup;

    // Lamp
    let lampHousing, lampGlow, lampLight, lampLens;

    // Polariser & analyser
    //   rotGroup.rotation.x  rotates the transmission axis
    //   around the beam (+X) — physically correct for
    //   showing optical rotation.
    let polarizerRotGroup, analyzerRotGroup;

    // Sample
    let sampleTube, sampleLiquid, chiralGroup;

    // Detector
    let detectorBody, detectorSensor;

    // Beam visualisation  (geometry built in Part 2)
    let beamParticles = null;      // soft glow along axis
    let wavePre = null;      // sinusoidal wave: polariser → sample
    let waveIn = null;      // twisting wave inside sample
    let wavePost = null;      // rotated wave: sample → analyser

    // Interpolation / display
    let animationId = null;
    let beamIntensity = 0;
    let targetBeamIntensity = 0;
    let targetRotationDeg = 0;    // target observed α
    let currentRotationDeg = 0;    // smoothed α for display
    let currentAnalyzerAng = 0;    // analyser disc angle (°)

    // ═══════════════════════════════════════════════════════
    //  CAMERA STATE  (spherical orbit)
    // ═══════════════════════════════════════════════════════
    const cam = {
        dragging: false,
        prevX: 0,
        prevY: 0,
        theta: 0.45,               // azimuthal   (rad)
        phi: 1.10,               // polar from +Y (rad)
        radius: 11,
        minR: 4,
        maxR: 22,
        minPhi: 0.15,
        maxPhi: Math.PI - 0.15,
        autoRotate: true,
        speed: 0.0008,
        target: null                // THREE.Vector3, assigned in initScene
    };

    // ═══════════════════════════════════════════════════════
    //  DOM HELPERS
    // ═══════════════════════════════════════════════════════
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    /** Display a transient toast notification */
    function toast(msg, type = 'info') {
        const box = $('#toast-container');
        if (!box) return;
        const icons = {
            info: 'info-circle', success: 'check-circle',
            warning: 'exclamation-triangle', error: 'times-circle'
        };
        const el = document.createElement('div');
        el.className = `toast ${type}`;
        el.innerHTML = `<i class="fas fa-${icons[type] || 'info-circle'}"></i><span>${msg}</span>`;
        box.appendChild(el);
        setTimeout(() => {
            el.classList.add('removing');
            setTimeout(() => el.remove(), 320);
        }, 4000);
    }

    /** Append a timestamped line to the system log */
    function addLog(msg, type = 'info') {
        const log = $('#log-content');
        if (!log) return;
        const ts = new Date().toLocaleTimeString([], {
            hour: '2-digit', minute: '2-digit', second: '2-digit'
        });
        const row = document.createElement('div');
        row.className = `log-entry ${type}`;
        row.innerHTML = `<span class="log-time">[${ts}]</span>` +
            `<span class="log-msg">${msg}</span>`;
        log.appendChild(row);
        log.scrollTop = log.scrollHeight;
    }

    // ═══════════════════════════════════════════════════════
    //  SCENE INITIALISATION
    // ═══════════════════════════════════════════════════════

    function initScene() {
        const container = $('#viewport-3d');
        if (!container || typeof THREE === 'undefined') {
            console.warn('[Polarimeter] Three.js or #viewport-3d not found');
            return;
        }

        // ── Scene ───────────────────────────────────────────
        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x060a12, 0.04);

        // ── Camera ──────────────────────────────────────────
        const w = container.clientWidth, h = container.clientHeight;
        camera = new THREE.PerspectiveCamera(42, w / h, 0.1, 100);
        cam.target = new THREE.Vector3(0, 0, 0);
        updateCameraFromSpherical();

        // ── Renderer ────────────────────────────────────────
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.2;
        container.insertBefore(renderer.domElement, container.firstChild);

        // ── Lighting ────────────────────────────────────────
        scene.add(new THREE.AmbientLight(0x1a2540, 0.7));

        const keyLight = new THREE.DirectionalLight(0x4488cc, 0.45);
        keyLight.position.set(5, 8, 5);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.set(512, 512);
        scene.add(keyLight);

        scene.add(Object.assign(
            new THREE.DirectionalLight(0x223355, 0.2),
            { position: new THREE.Vector3(-4, 3, -4) }
        ));
        scene.add(Object.assign(
            new THREE.DirectionalLight(0x2244aa, 0.15),
            { position: new THREE.Vector3(-3, 1, -5) }
        ));

        // ── Scene group (houses all optical components) ─────
        sceneGroup = new THREE.Group();
        scene.add(sceneGroup);

        // ── Build static geometry ───────────────────────────
        buildBaseplate();
        buildLamp();
        buildPolarizer(BENCH.polarizer, 0x3b82f6, false);   // fixed polariser
        buildSampleTube();
        buildChiralCenter();
        buildPolarizer(BENCH.analyzer, 0x8b5cf6, true);    // rotatable analyser
        buildDetector();
        // buildLightBeam() is called from Part 2 after
        // wave-geometry helpers are defined.

        // ── Camera interaction ──────────────────────────────
        attachCameraControls(container);

        // ── Responsive resize ───────────────────────────────
        if (typeof ResizeObserver !== 'undefined') {
            new ResizeObserver(() => {
                if (!renderer || !camera) return;
                const cw = container.clientWidth, ch = container.clientHeight;
                camera.aspect = cw / ch;
                camera.updateProjectionMatrix();
                renderer.setSize(cw, ch);
            }).observe(container);
        } else {
            window.addEventListener('resize', () => {
                if (!renderer || !camera || !container) return;
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
        }
    }

    // ── Spherical → Cartesian for camera ────────────────────
    function updateCameraFromSpherical() {
        if (!camera) return;
        const { theta, phi, radius, target: t } = cam;
        camera.position.set(
            t.x + radius * Math.sin(phi) * Math.sin(theta),
            t.y + radius * Math.cos(phi),
            t.z + radius * Math.sin(phi) * Math.cos(theta)
        );
        camera.lookAt(t);
    }

    // ── Camera orbit / zoom listeners ───────────────────────
    function attachCameraControls(el) {
        el.style.touchAction = 'none';          // prevent browser scroll

        // Pointer drag → orbit
        el.addEventListener('pointerdown', (e) => {
            if (e.target.tagName === 'BUTTON') return;
            cam.dragging = true;
            cam.prevX = e.clientX;
            cam.prevY = e.clientY;
            el.setPointerCapture(e.pointerId);
        });
        el.addEventListener('pointermove', (e) => {
            if (!cam.dragging) return;
            const dx = e.clientX - cam.prevX;
            const dy = e.clientY - cam.prevY;
            cam.theta -= dx * 0.005;
            cam.phi = Math.max(cam.minPhi,
                Math.min(cam.maxPhi, cam.phi - dy * 0.005));
            cam.prevX = e.clientX;
            cam.prevY = e.clientY;
            // Disable auto-rotate when user drags
            cam.autoRotate = false;
            const btn = $('#view-animate-btn');
            if (btn) btn.classList.remove('active');
        });
        el.addEventListener('pointerup', () => { cam.dragging = false; });
        el.addEventListener('pointerleave', () => { cam.dragging = false; });

        // Scroll → zoom
        el.addEventListener('wheel', (e) => {
            e.preventDefault();
            cam.radius = Math.max(cam.minR,
                Math.min(cam.maxR, cam.radius + e.deltaY * 0.012));
        }, { passive: false });

        // Touch-pinch zoom
        let lastPinchDist = 0;
        el.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                lastPinchDist = Math.sqrt(dx * dx + dy * dy);
            }
        }, { passive: true });
        el.addEventListener('touchmove', (e) => {
            if (e.touches.length === 2) {
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                const dist = Math.sqrt(dx * dx + dy * dy);
                const delta = lastPinchDist - dist;
                cam.radius = Math.max(cam.minR,
                    Math.min(cam.maxR, cam.radius + delta * 0.03));
                lastPinchDist = dist;
            }
        }, { passive: true });
    }

    // ═══════════════════════════════════════════════════════
    //  OPTICAL COMPONENT BUILDERS
    // ═══════════════════════════════════════════════════════

    /** Dark aluminium base with precision rails & position markers */
    function buildBaseplate() {
        const plateMat = new THREE.MeshStandardMaterial({
            color: 0x141824, roughness: 0.85, metalness: 0.3
        });
        const plate = new THREE.Mesh(
            new THREE.BoxGeometry(14, 0.15, 3), plateMat
        );
        plate.position.set(0, -1.1, 0);
        plate.receiveShadow = true;
        sceneGroup.add(plate);

        // Steel rails
        const railMat = new THREE.MeshStandardMaterial({
            color: 0x3a4255, metalness: 0.85, roughness: 0.25
        });
        const railGeo = new THREE.BoxGeometry(13, 0.05, 0.07);
        [-0.42, 0.42].forEach(z => {
            const r = new THREE.Mesh(railGeo, railMat);
            r.position.set(0, -1.0, z);
            sceneGroup.add(r);
        });

        // Coloured position markers on base
        [
            { x: BENCH.lamp, c: 0xf59e0b },
            { x: BENCH.polarizer, c: 0x3b82f6 },
            { x: BENCH.sampleCenter, c: 0x22c55e },
            { x: BENCH.analyzer, c: 0x8b5cf6 },
            { x: BENCH.detector, c: 0xef4444 }
        ].forEach(({ x, c }) => {
            const m = new THREE.Mesh(
                new THREE.CylinderGeometry(0.05, 0.06, 0.18, 8),
                new THREE.MeshStandardMaterial({
                    color: c, emissive: c, emissiveIntensity: 0.25
                })
            );
            m.position.set(x, -0.92, 0);
            sceneGroup.add(m);
        });
    }

    /** Sodium vapour lamp with housing, heat-sink fins, glow & lens */
    function buildLamp() {
        // Cylindrical housing
        lampHousing = new THREE.Mesh(
            new THREE.CylinderGeometry(0.5, 0.6, 1.4, 16),
            new THREE.MeshStandardMaterial({
                color: 0x2a2a3a, roughness: 0.55, metalness: 0.5
            })
        );
        lampHousing.position.set(BENCH.lamp, BENCH.beamY, 0);
        sceneGroup.add(lampHousing);

        // Heat-sink rings (realism detail)
        const finMat = new THREE.MeshStandardMaterial({
            color: 0x222233, metalness: 0.7, roughness: 0.4
        });
        for (let i = -2; i <= 2; i++) {
            const fin = new THREE.Mesh(
                new THREE.TorusGeometry(0.55, 0.025, 6, 24), finMat
            );
            fin.position.set(BENCH.lamp, BENCH.beamY + i * 0.22, 0);
            fin.rotation.x = Math.PI / 2;
            sceneGroup.add(fin);
        }

        // Glowing Na element (off by default → opacity 0)
        lampGlow = new THREE.Mesh(
            new THREE.SphereGeometry(0.22, 16, 16),
            new THREE.MeshBasicMaterial({
                color: 0xffaa33, transparent: true, opacity: 0
            })
        );
        lampGlow.position.set(BENCH.lamp, BENCH.beamY, 0);
        sceneGroup.add(lampGlow);

        // Point light (off by default → intensity 0)
        lampLight = new THREE.PointLight(0xffaa33, 0, 8);
        lampLight.position.set(BENCH.lamp, BENCH.beamY, 0);
        sceneGroup.add(lampLight);

        // Collimating lens
        lampLens = new THREE.Mesh(
            new THREE.CylinderGeometry(0.32, 0.32, 0.06, 16),
            new THREE.MeshPhysicalMaterial({
                color: 0xffeebb, transparent: true, opacity: 0.2,
                roughness: 0, metalness: 0, transmission: 0.85
            })
        );
        lampLens.position.set(BENCH.lensFront, BENCH.beamY, 0);
        lampLens.rotation.z = Math.PI / 2;      // disc faces beam
        sceneGroup.add(lampLens);
    }

    /**
     * Polariser  or  Analyser
     *
     * Both are structurally identical Nicol-prism / Polaroid discs
     * mounted perpendicular to the beam.
     *
     *   isAnalyzer = false → fixed polariser (transmission axis = Y)
     *   isAnalyzer = true  → rotatable analyser with degree scale
     *
     * The `rotGroup.rotation.x` parameter rotates the transmission
     * axis around the beam (+X).  This is the physically correct
     * axis for optical rotation measurement.
     *
     * Grid lines on the disc show the current transmission axis so
     * the user can SEE how the analyser tilts to match α.
     */
    function buildPolarizer(xPos, color, isAnalyzer) {
        // Fixed outer group (holds mount + scale)
        const base = new THREE.Group();
        base.position.set(xPos, BENCH.beamY, 0);
        sceneGroup.add(base);

        // Mount frame
        base.add(new THREE.Mesh(
            new THREE.BoxGeometry(0.12, 1.65, 1.65),
            new THREE.MeshStandardMaterial({
                color: 0x1c2536, roughness: 0.7, metalness: 0.4
            })
        ));

        // ── Rotation sub-group ──
        // Everything inside here rotates when α changes (analyser)
        const rotGroup = new THREE.Group();
        base.add(rotGroup);

        // Semi-transparent disc
        // CylinderGeometry axis = Y; rotate π/2 about Z → axis = X (beam)
        const disc = new THREE.Mesh(
            new THREE.CylinderGeometry(0.58, 0.58, 0.035, 32),
            new THREE.MeshPhysicalMaterial({
                color, transparent: true, opacity: 0.22,
                roughness: 0.05, metalness: 0.05,
                side: THREE.DoubleSide
            })
        );
        disc.rotation.z = Math.PI / 2;
        rotGroup.add(disc);

        // Grid lines — show the transmission axis
        // Lines are tall in Y, thin, and spread along Z
        // In the un-rotated state they are VERTICAL (Y direction)
        // which represents 0° polarisation.
        const lineMat = new THREE.MeshBasicMaterial({
            color, transparent: true, opacity: 0.4
        });
        for (let i = -4; i <= 4; i++) {
            const bar = new THREE.Mesh(
                new THREE.BoxGeometry(0.004, 0.92, 0.004),
                lineMat
            );
            bar.position.set(0, 0, i * 0.11);
            rotGroup.add(bar);
        }

        // Outer ring
        const ring = new THREE.Mesh(
            new THREE.TorusGeometry(0.58, 0.025, 8, 48),
            new THREE.MeshStandardMaterial({
                color, emissive: color, emissiveIntensity: 0.2
            })
        );
        ring.rotation.y = Math.PI / 2;   // torus plane = YZ
        rotGroup.add(ring);

        // ── Degree scale (analyser only, on the FIXED frame) ──
        if (isAnalyzer) {
            const tickMajor = new THREE.LineBasicMaterial({
                color, transparent: true, opacity: 0.5
            });
            const tickMinor = new THREE.LineBasicMaterial({
                color: 0x94a3b8, transparent: true, opacity: 0.25
            });
            for (let deg = 0; deg < 360; deg += 15) {
                const major = (deg % 45 === 0);
                const rad = deg * Math.PI / 180;
                const r1 = 0.62;
                const r2 = r1 + (major ? 0.10 : 0.05);
                const pts = [
                    new THREE.Vector3(0,
                        r1 * Math.cos(rad), r1 * Math.sin(rad)),
                    new THREE.Vector3(0,
                        r2 * Math.cos(rad), r2 * Math.sin(rad))
                ];
                base.add(new THREE.Line(
                    new THREE.BufferGeometry().setFromPoints(pts),
                    major ? tickMajor : tickMinor
                ));
            }
            // Reference mark at 0° (top)
            const refDot = new THREE.Mesh(
                new THREE.SphereGeometry(0.03, 6, 6),
                new THREE.MeshBasicMaterial({ color })
            );
            refDot.position.set(0, 0.75, 0);
            base.add(refDot);
        }

        // Store reference for animation
        if (isAnalyzer) {
            analyzerRotGroup = rotGroup;
        } else {
            polarizerRotGroup = rotGroup;
        }
    }

    /** Glass observation tube with end-caps and coloured liquid fill */
    function buildSampleTube() {
        const tubeLen = BENCH.sampleEnd - BENCH.sampleStart;
        const y = BENCH.beamY;

        // Glass wall (open-ended cylinder for transparency)
        sampleTube = new THREE.Mesh(
            new THREE.CylinderGeometry(0.34, 0.34, tubeLen, 32, 1, true),
            new THREE.MeshPhysicalMaterial({
                color: 0x88ccff, transparent: true, opacity: 0.10,
                roughness: 0, metalness: 0.05,
                side: THREE.DoubleSide, envMapIntensity: 0.4
            })
        );
        sampleTube.position.set(BENCH.sampleCenter, y, 0);
        sampleTube.rotation.z = Math.PI / 2;        // axis along X
        sceneGroup.add(sampleTube);

        // Metal end-caps
        const capMat = new THREE.MeshStandardMaterial({
            color: 0x3a4560, metalness: 0.65, roughness: 0.35
        });
        [BENCH.sampleStart, BENCH.sampleEnd].forEach(x => {
            const cap = new THREE.Mesh(
                new THREE.CylinderGeometry(0.37, 0.37, 0.09, 32), capMat
            );
            cap.position.set(x, y, 0);
            cap.rotation.z = Math.PI / 2;
            sceneGroup.add(cap);
        });

        // Liquid fill (slightly smaller than glass)
        sampleLiquid = new THREE.Mesh(
            new THREE.CylinderGeometry(0.31, 0.31, tubeLen - 0.15, 32),
            new THREE.MeshPhysicalMaterial({
                color: 0x22c55e, transparent: true, opacity: 0.06,
                roughness: 0.1, metalness: 0
            })
        );
        sampleLiquid.position.set(BENCH.sampleCenter, y, 0);
        sampleLiquid.rotation.z = Math.PI / 2;
        sceneGroup.add(sampleLiquid);
    }

    /**
     * Chiral-centre molecule floating inside the sample tube.
     *
     * Instead of generating a random molecular shape from the
     * chemical formula (which is scientifically misleading),
     * we show an sp³ carbon with FOUR DIFFERENT substituents
     * arranged tetrahedrally.
     *
     * This correctly illustrates the physical origin of
     * optical activity: four distinct groups → no mirror-plane
     * symmetry → the molecule and its mirror image are
     * non-superimposable (chirality).
     */
    function buildChiralCenter() {
        chiralGroup = new THREE.Group();
        chiralGroup.position.set(BENCH.sampleCenter, BENCH.beamY, 0);
        sceneGroup.add(chiralGroup);

        // Central sp³ carbon
        chiralGroup.add(new THREE.Mesh(
            new THREE.SphereGeometry(0.10, 14, 14),
            new THREE.MeshStandardMaterial({
                color: 0x444444, roughness: 0.3, metalness: 0.2
            })
        ));

        // Tetrahedral vertices (normalised, then scaled)
        const raw = [
            [1, 1, 1],
            [-1, -1, 1],
            [-1, 1, -1],
            [1, -1, -1]
        ];
        const armLen = 0.30;
        const verts = raw.map(v => {
            const len = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
            return new THREE.Vector3(
                v[0] / len * armLen,
                v[1] / len * armLen,
                v[2] / len * armLen
            );
        });

        // Four distinct substituent colours → chirality
        const colors = [0xef4444, 0x3b82f6, 0x22c55e, 0xf59e0b];
        const sizes = [0.085, 0.075, 0.065, 0.070];

        verts.forEach((pos, i) => {
            // Bond stick (cylinder from centre to substituent)
            const dir = pos.clone().normalize();
            const bLen = pos.length();
            const bond = new THREE.Mesh(
                new THREE.CylinderGeometry(0.018, 0.018, bLen, 5),
                new THREE.MeshStandardMaterial({
                    color: 0x667788, roughness: 0.5
                })
            );
            bond.position.copy(pos.clone().multiplyScalar(0.5));
            bond.quaternion.setFromUnitVectors(
                new THREE.Vector3(0, 1, 0), dir
            );
            chiralGroup.add(bond);

            // Substituent sphere
            const sphere = new THREE.Mesh(
                new THREE.SphereGeometry(sizes[i], 10, 10),
                new THREE.MeshStandardMaterial({
                    color: colors[i], roughness: 0.3, metalness: 0.15,
                    emissive: colors[i], emissiveIntensity: 0.12
                })
            );
            sphere.position.copy(pos);
            chiralGroup.add(sphere);
        });
    }

    /** Photodetector with sensor window, housing rim & status LED */
    function buildDetector() {
        // Housing
        detectorBody = new THREE.Mesh(
            new THREE.BoxGeometry(0.75, 1.0, 0.75),
            new THREE.MeshStandardMaterial({
                color: 0x1c2536, roughness: 0.6, metalness: 0.5
            })
        );
        detectorBody.position.set(BENCH.detector, BENCH.beamY, 0);
        sceneGroup.add(detectorBody);

        // Circular sensor window facing the beam (−X direction)
        detectorSensor = new THREE.Mesh(
            new THREE.CircleGeometry(0.18, 24),
            new THREE.MeshBasicMaterial({
                color: 0xef4444, transparent: true, opacity: 0.15,
                side: THREE.DoubleSide
            })
        );
        detectorSensor.position.set(
            BENCH.detector - 0.376, BENCH.beamY, 0
        );
        detectorSensor.rotation.y = -Math.PI / 2;
        sceneGroup.add(detectorSensor);

        // Rim around sensor
        const rim = new THREE.Mesh(
            new THREE.TorusGeometry(0.19, 0.02, 6, 24),
            new THREE.MeshStandardMaterial({
                color: 0x334155, metalness: 0.7, roughness: 0.3
            })
        );
        rim.position.copy(detectorSensor.position);
        rim.rotation.y = Math.PI / 2;
        sceneGroup.add(rim);

        // Status LED on top
        const led = new THREE.Mesh(
            new THREE.SphereGeometry(0.04, 8, 8),
            new THREE.MeshBasicMaterial({
                color: 0x22c55e, transparent: true, opacity: 0.3
            })
        );
        led.position.set(BENCH.detector, BENCH.beamY + 0.55, 0);
        sceneGroup.add(led);

        detectorBody.userData = { sensor: detectorSensor, led };
    }


    // ═══════════════════════════════════════════════════════
    //  END OF PART 1
    //
    //  Part 2 continues with:
    //    • Light-beam & polarisation-wave geometry
    //    • Animation loop
    //    • Camera presets (side / front / top / reset)
    //    • HUD updates (mini-dial, polarisation badges)
    //    • Molecule rebuild on sample change
    // ═══════════════════════════════════════════════════════
    // ═══════════════════════════════════════════════════════
    //  PART 2 OF 3
    //  Light-beam visualisation, polarisation waves,
    //  animation loop, camera presets, HUD updates
    // ═══════════════════════════════════════════════════════

    /*  PHYSICS NOTE — Polarisation-plane visualisation
     *
     *  The E-field of plane-polarised light propagating along +X
     *  oscillates in a plane perpendicular to X:
     *
     *    E_y(x,t) = A · sin(kx − ωt) · cos θ
     *    E_z(x,t) = A · sin(kx − ωt) · sin θ
     *
     *  where θ is the polarisation angle measured from +Y.
     *
     *  θ = 0    after the fixed polariser (vertical transmission axis)
     *  θ = α    after the sample (rotated by observed rotation α)
     *
     *  Inside the sample tube θ varies linearly from 0 → α,
     *  producing the characteristic "twisting ribbon" seen in
     *  textbook diagrams of optical rotation.
     *
     *  Sign convention (looking FROM DETECTOR toward source, i.e. −X):
     *    α > 0  ⟹  clockwise      ⟹  dextrorotatory  (+)
     *    α < 0  ⟹  anticlockwise  ⟹  levorotatory    (−)
     *
     *  THREE.js right-hand rule: positive rotation.x goes
     *  Y → Z when looking along +X, which is CLOCKWISE when
     *  looking along −X.  So our convention matches directly:
     *    analyzerRotGroup.rotation.x = +α_rad  ⟹  dextrorotatory  ✓
     */

    // ── Wave visualisation constants ──────────────────────
    const WAVE = Object.freeze({
        k: 8.0,       // spatial freq   (rad / scene-unit)
        omega: 3.5,       // temporal freq   (rad / s)
        amp: 0.22,      // max displacement (scene-units)
        ribbonH: 0.28       // half-height of polarisation ribbon
    });

    const PTS = Object.freeze({
        pre: 36,        // polariser → sample
        sample: 96,        // inside sample tube
        post: 36,        // sample → analyser
        ribbon: 32,        // ribbon resolution per section
        glow: 220        // glow particles along full beam
    });

    // ── Beam-component references (filled by buildLightBeam) ──
    let waveLinePre = null;    // { line, pos, mat, baseOpacity }
    let waveLineSample = null;
    let waveLinePost = null;
    let ribbonPre = null;    // { mesh, pos, mat, baseOpacity }
    let ribbonSample = null;
    let ribbonPost = null;
    let beamGlow = null;    // THREE.Points
    let unpolGroups = [];      // unpolarised-light indicators
    let csIndicators = [];      // cross-section polarisation indicators

    // Camera smooth-transition target (null = idle)
    let camTransition = null;


    // ═══════════════════════════════════════════════════════
    //  GEOMETRY HELPERS
    // ═══════════════════════════════════════════════════════

    /** Pre-allocated Line for a sinusoidal wave segment */
    function makeWaveLine(numPts, color, baseOpacity = 0.75) {
        const pos = new Float32Array(numPts * 3);
        const geo = new THREE.BufferGeometry();
        geo.setAttribute('position',
            new THREE.BufferAttribute(pos, 3));
        const mat = new THREE.LineBasicMaterial({
            color,
            transparent: true,
            opacity: 0,
            linewidth: 1
        });
        const line = new THREE.Line(geo, mat);
        line.frustumCulled = false;
        return { line, pos, mat, baseOpacity };
    }

    /**
     * Triangle-strip ribbon for visualising the polarisation plane.
     *
     * At each x-station two vertices sit on opposite sides of the
     * beam axis, offset by ±ribbonH in the polarisation direction.
     * The connecting quads form a flat ribbon that TWISTS when the
     * polarisation angle θ changes along x — the classic textbook
     * representation of optical rotation.
     */
    function makeRibbon(numPts, color, baseOpacity = 0.09) {
        const verts = numPts * 2;
        const pos = new Float32Array(verts * 3);
        const idx = [];
        for (let i = 0; i < numPts - 1; i++) {
            const a = i * 2, b = a + 1;
            const c = (i + 1) * 2, d = c + 1;
            idx.push(a, c, b, b, c, d);
        }
        const geo = new THREE.BufferGeometry();
        geo.setAttribute('position',
            new THREE.BufferAttribute(pos, 3));
        geo.setIndex(idx);
        const mat = new THREE.MeshBasicMaterial({
            color,
            transparent: true,
            opacity: 0,
            side: THREE.DoubleSide,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.frustumCulled = false;
        return { mesh, pos, mat, baseOpacity };
    }


    // ═══════════════════════════════════════════════════════
    //  BUILD THE COMPLETE LIGHT-BEAM VISUALISATION
    // ═══════════════════════════════════════════════════════

    function buildLightBeam() {
        if (!sceneGroup) return;

        // ── 1. Glow particles along full beam path ──────────
        const gc = PTS.glow;
        const gPos = new Float32Array(gc * 3);
        const xFrom = BENCH.lamp + 0.6;
        const xTo = BENCH.detector - 0.35;
        for (let i = 0; i < gc; i++) {
            const t = i / (gc - 1);
            gPos[i * 3] = xFrom + t * (xTo - xFrom);
            gPos[i * 3 + 1] = BENCH.beamY;
            gPos[i * 3 + 2] = 0;
        }
        const gGeo = new THREE.BufferGeometry();
        gGeo.setAttribute('position',
            new THREE.BufferAttribute(gPos, 3));
        beamGlow = new THREE.Points(gGeo,
            new THREE.PointsMaterial({
                color: 0xffbb44,
                size: 0.05,
                transparent: true,
                opacity: 0,
                blending: THREE.AdditiveBlending,
                sizeAttenuation: true,
                depthWrite: false
            })
        );
        beamGlow.frustumCulled = false;
        sceneGroup.add(beamGlow);

        // ── 2. Unpolarised-light indicators ─────────────────
        //    Small circles with multi-angle lines between
        //    lamp and polariser, showing that unpolarised light
        //    vibrates in ALL directions ⟂ to propagation.
        const uX = [BENCH.lamp + 0.9, BENCH.lamp + 1.4, BENCH.lamp + 1.9];
        const uA = [0, Math.PI / 3, 2 * Math.PI / 3];  // 3 angles
        uX.forEach(x => {
            const g = new THREE.Group();
            g.position.set(x, BENCH.beamY, 0);

            // Small reference circle in YZ plane (⟂ to beam)
            const ring = new THREE.Mesh(
                new THREE.TorusGeometry(0.14, 0.007, 6, 20),
                new THREE.MeshBasicMaterial({
                    color: 0xffbb44, transparent: true,
                    opacity: 0, depthWrite: false
                })
            );
            ring.rotation.z = Math.PI / 2;  // axis Y → X
            g.add(ring);

            // Lines at various angles through the circle
            uA.forEach(a => {
                const r = 0.13;
                const p1 = new THREE.Vector3(
                    0, r * Math.cos(a), r * Math.sin(a));
                const p2 = new THREE.Vector3(
                    0, -r * Math.cos(a), -r * Math.sin(a));
                g.add(new THREE.Line(
                    new THREE.BufferGeometry().setFromPoints([p1, p2]),
                    new THREE.LineBasicMaterial({
                        color: 0xffbb44, transparent: true,
                        opacity: 0
                    })
                ));
            });
            sceneGroup.add(g);
            unpolGroups.push(g);
        });

        // ── 3. Pre-sample wave + ribbon  (polariser → tube) ─
        waveLinePre = makeWaveLine(PTS.pre, 0xffcc55);
        sceneGroup.add(waveLinePre.line);

        ribbonPre = makeRibbon(PTS.ribbon, 0x3b82f6);
        sceneGroup.add(ribbonPre.mesh);

        // ── 4. Sample wave + ribbon  (inside tube, twisting) ─
        waveLineSample = makeWaveLine(PTS.sample, 0xffcc55);
        sceneGroup.add(waveLineSample.line);

        ribbonSample = makeRibbon(PTS.ribbon * 2, 0x22c55e, 0.07);
        sceneGroup.add(ribbonSample.mesh);

        // ── 5. Post-sample wave + ribbon  (tube → analyser) ─
        waveLinePost = makeWaveLine(PTS.post, 0xffcc55);
        sceneGroup.add(waveLinePost.line);

        ribbonPost = makeRibbon(PTS.ribbon, 0x8b5cf6);
        sceneGroup.add(ribbonPost.mesh);

        // ── 6. Cross-section indicators ─────────────────────
        //    A circle + direction line at the polariser exit
        //    and near the analyser entrance.  When viewed "end-on"
        //    (front camera preset), these clearly show how the
        //    polarisation plane has rotated.
        addCSIndicator(BENCH.polarizer + 0.25, 0x3b82f6, 0);    // fixed 0°
        addCSIndicator(BENCH.analyzer - 0.25, 0x8b5cf6, null); // follows α
    }

    /** Cross-section polarisation indicator at position x */
    function addCSIndicator(x, color, fixedAngle) {
        const g = new THREE.Group();
        g.position.set(x, BENCH.beamY, 0);

        // Circle in YZ plane
        const ring = new THREE.Mesh(
            new THREE.TorusGeometry(0.17, 0.009, 6, 24),
            new THREE.MeshBasicMaterial({
                color, transparent: true, opacity: 0, depthWrite: false
            })
        );
        ring.rotation.z = Math.PI / 2;       // axis Y → X (face beam)
        g.add(ring);

        // Direction line (starts vertical = 0° polarisation)
        const r = 0.15;
        const dirLine = new THREE.Line(
            new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(0, r, 0),
                new THREE.Vector3(0, -r, 0)
            ]),
            new THREE.LineBasicMaterial({
                color, transparent: true, opacity: 0, linewidth: 2
            })
        );
        g.add(dirLine);

        // Small dot at +Y end to show direction
        const tip = new THREE.Mesh(
            new THREE.SphereGeometry(0.025, 6, 6),
            new THREE.MeshBasicMaterial({
                color, transparent: true, opacity: 0
            })
        );
        tip.position.set(0, r, 0);
        g.add(tip);

        sceneGroup.add(g);
        csIndicators.push({ group: g, fixedAngle, children: [ring, dirLine, tip] });
    }


    // ═══════════════════════════════════════════════════════
    //  PER-FRAME BEAM UPDATE
    // ═══════════════════════════════════════════════════════

    function updateBeam(time) {
        const I = beamIntensity;          // 0 … 1
        const alphaRad = currentRotationDeg * Math.PI / 180;

        // Skip heavy work when beam is off
        if (I < 0.005) {
            [waveLinePre, waveLineSample, waveLinePost].forEach(w => {
                if (w) w.mat.opacity = 0;
            });
            [ribbonPre, ribbonSample, ribbonPost].forEach(r => {
                if (r) r.mat.opacity = 0;
            });
            if (beamGlow) beamGlow.material.opacity = 0;
            unpolGroups.forEach(g =>
                g.children.forEach(c => { if (c.material) c.material.opacity = 0; }));
            csIndicators.forEach(cs =>
                cs.children.forEach(c => { if (c.material) c.material.opacity = 0; }));
            return;
        }

        // ── θ(x): polarisation angle at beam position x ─────
        //    0 before sample, linearly interpolated inside,
        //    α after sample.
        const xS = BENCH.sampleStart;
        const xE = BENCH.sampleEnd;
        const tubeLen = xE - xS;
        function theta(x) {
            if (x <= xS) return 0;
            if (x >= xE) return alphaRad;
            return alphaRad * (x - xS) / tubeLen;
        }

        // ── Update wave-line positions ──────────────────────
        function fillWave(obj, x0, x1, n) {
            if (!obj) return;
            obj.mat.opacity = I * obj.baseOpacity;
            const { pos } = obj;
            const k = WAVE.k, w = WAVE.omega, A = WAVE.amp;
            for (let i = 0; i < n; i++) {
                const t = i / (n - 1);
                const x = x0 + t * (x1 - x0);
                const th = theta(x);
                const s = A * Math.sin(k * x - w * time);
                pos[i * 3] = x;
                pos[i * 3 + 1] = BENCH.beamY + s * Math.cos(th);
                pos[i * 3 + 2] = s * Math.sin(th);
            }
            obj.line.geometry.attributes.position.needsUpdate = true;
        }

        // ── Update ribbon positions ─────────────────────────
        function fillRibbon(obj, x0, x1, n) {
            if (!obj) return;
            obj.mat.opacity = I * obj.baseOpacity;
            const { pos } = obj;
            const h = WAVE.ribbonH;
            for (let i = 0; i < n; i++) {
                const t = i / (n - 1);
                const x = x0 + t * (x1 - x0);
                const th = theta(x);
                const cT = Math.cos(th), sT = Math.sin(th);
                // Top vertex
                pos[i * 6] = x;
                pos[i * 6 + 1] = BENCH.beamY + h * cT;
                pos[i * 6 + 2] = h * sT;
                // Bottom vertex
                pos[i * 6 + 3] = x;
                pos[i * 6 + 4] = BENCH.beamY - h * cT;
                pos[i * 6 + 5] = -h * sT;
            }
            obj.mesh.geometry.attributes.position.needsUpdate = true;
        }

        const preX0 = BENCH.polarizer + 0.15;
        const preX1 = BENCH.sampleStart;
        const postX0 = BENCH.sampleEnd;
        const postX1 = BENCH.analyzer - 0.15;

        fillWave(waveLinePre, preX0, preX1, PTS.pre);
        fillWave(waveLineSample, xS, xE, PTS.sample);
        fillWave(waveLinePost, postX0, postX1, PTS.post);

        fillRibbon(ribbonPre, preX0, preX1, PTS.ribbon);
        fillRibbon(ribbonSample, xS, xE, PTS.ribbon * 2);
        fillRibbon(ribbonPost, postX0, postX1, PTS.ribbon);

        // ── Glow particles — gentle jitter ──────────────────
        if (beamGlow) {
            beamGlow.material.opacity = I * 0.40;
            const p = beamGlow.geometry.attributes.position.array;
            for (let i = 0; i < PTS.glow; i++) {
                const xi = p[i * 3];           // x stays fixed
                const th = theta(xi);
                const jY = Math.sin(time * 4.0 + i * 0.28) * 0.012 * I;
                const jZ = Math.cos(time * 3.5 + i * 0.45) * 0.012 * I;
                p[i * 3 + 1] = BENCH.beamY + jY * Math.cos(th) - jZ * Math.sin(th);
                p[i * 3 + 2] = jY * Math.sin(th) + jZ * Math.cos(th);
            }
            beamGlow.geometry.attributes.position.needsUpdate = true;
        }

        // ── Unpolarised indicators ──────────────────────────
        unpolGroups.forEach(g => {
            g.children.forEach(c => {
                if (c.material) c.material.opacity = I * 0.30;
            });
        });

        // ── Cross-section indicators ────────────────────────
        csIndicators.forEach(cs => {
            const angle = (cs.fixedAngle !== null) ? cs.fixedAngle : alphaRad;
            // Rotate the whole group around X → tilts the direction
            // line in the YZ plane, showing the polarisation angle
            cs.group.rotation.x = angle;
            cs.children.forEach(c => {
                if (c.material) c.material.opacity = I * 0.50;
            });
        });

        // ── Detector sensor brightness ──────────────────────
        if (detectorSensor) {
            detectorSensor.material.opacity = 0.08 + I * 0.40;
        }
        if (detectorBody && detectorBody.userData) {
            const led = detectorBody.userData.led;
            if (led) {
                led.material.opacity = I > 0.5 ? 0.6 : 0.12;
                led.material.color.setHex(I > 0.5 ? 0x22c55e : 0x64748b);
            }
        }
    }


    // ═══════════════════════════════════════════════════════
    //  CAMERA PRESETS
    // ═══════════════════════════════════════════════════════

    const CAM_PRESETS = Object.freeze({
        //                  θ (azimuth)       φ (polar)        r
        default: { theta: 0.45, phi: 1.10, radius: 11 },
        side: { theta: 0.0, phi: Math.PI / 2, radius: 10 },
        // "Front" = looking FROM DETECTOR along −X toward lamp.
        // This is the standard view for observing optical rotation.
        front: { theta: Math.PI / 2, phi: Math.PI / 2, radius: 7 },
        top: { theta: 0.01, phi: 0.12, radius: 14 }
    });

    function setCameraPreset(name) {
        const p = CAM_PRESETS[name];
        if (!p) return;
        camTransition = { theta: p.theta, phi: p.phi, radius: p.radius };
        cam.autoRotate = false;

        // UI button feedback
        const btnMap = {
            default: '#view-reset-btn',
            side: '#view-side-btn',
            front: '#view-front-btn',
            top: '#view-top-btn'
        };
        $$('.viewport-toolbar button').forEach(b => b.classList.remove('active'));
        const btn = $(btnMap[name]);
        if (btn) btn.classList.add('active');
    }

    function bindViewControls() {
        $('#view-reset-btn')?.addEventListener('click', () => setCameraPreset('default'));
        $('#view-side-btn')?.addEventListener('click', () => setCameraPreset('side'));
        $('#view-front-btn')?.addEventListener('click', () => setCameraPreset('front'));
        $('#view-top-btn')?.addEventListener('click', () => setCameraPreset('top'));
        $('#view-animate-btn')?.addEventListener('click', () => {
            cam.autoRotate = !cam.autoRotate;
            camTransition = null;
            const b = $('#view-animate-btn');
            if (b) b.classList.toggle('active', cam.autoRotate);
            // Deactivate preset buttons
            ['#view-reset-btn', '#view-side-btn',
                '#view-front-btn', '#view-top-btn'
            ].forEach(s => $(s)?.classList.remove('active'));
        });
    }


    // ═══════════════════════════════════════════════════════
    //  HUD UPDATES
    // ═══════════════════════════════════════════════════════

    function updateHUD(deg) {
        const sign = deg > 0.001 ? '+' : '';

        // ── Main rotation readout ───────────────────────────
        const disp = $('#rotation-display');
        if (disp) {
            disp.textContent = `${sign}${deg.toFixed(3)}°`;
            disp.style.color = deg > 0.01 ? '#22c55e'
                : deg < -0.01 ? '#ef4444'
                    : '#e2e8f0';
        }

        // ── Mini-dial SVG needle ────────────────────────────
        //    The needle starts horizontal (3 o'clock = 0°).
        //    Positive α → clockwise from viewer's perspective.
        //    CSS rotate() is clockwise-positive, which matches
        //    the convention when looking from the detector side.
        const needle = document.getElementById('pol-plane-needle');
        if (needle) {
            // Clamp display to ±90° for visual clarity
            const clamp = Math.max(-90, Math.min(90, deg));
            needle.style.transform = `rotate(${clamp}deg)`;
            needle.style.stroke = deg > 0.01 ? '#22c55e'
                : deg < -0.01 ? '#ef4444'
                    : '#3b82f6';
        }

        // ── Plane-angle readout ─────────────────────────────
        const angEl = $('#pol-plane-angle');
        if (angEl) angEl.textContent = `${sign}${deg.toFixed(1)}°`;

        // ── Direction word ──────────────────────────────────
        const dirEl = $('#pol-plane-dir');
        if (dirEl) {
            if (deg > 0.01) {
                dirEl.textContent = 'Dextrorotatory (+)';
                dirEl.className = 'pi-dir dextro';
            } else if (deg < -0.01) {
                dirEl.textContent = 'Levorotatory (−)';
                dirEl.className = 'pi-dir levo';
            } else {
                dirEl.textContent = 'No rotation';
                dirEl.className = 'pi-dir none';
            }
        }

        // ── Polarisation-state badges ───────────────────────
        const psA = $('#ps-alpha');
        if (psA) psA.textContent = deg.toFixed(3);

        const psD = $('#ps-direction');
        if (psD) psD.textContent = deg > 0.01 ? 'Dextro (+)'
            : deg < -0.01 ? 'Levo (−)' : '—';

        const psW = $('#ps-wavelength');
        if (psW) psW.textContent = STATE.wavelength.toFixed(1);

        // Direction-badge dot colour
        const badge = $('#ps-direction-badge');
        if (badge) {
            const dot = badge.querySelector('.psb-dot');
            if (dot) dot.style.background =
                deg > 0.01 ? '#22c55e' : deg < -0.01 ? '#ef4444' : '#64748b';
        }
    }


    // ═══════════════════════════════════════════════════════
    //  MOLECULE REBUILD  (compound change)
    //
    //  Recreates the tetrahedral chiral centre with a
    //  mirrored fourth vertex for (−) compounds, so the
    //  user can SEE the enantiomeric difference.
    // ═══════════════════════════════════════════════════════

    function rebuildChiralCenter() {
        if (!chiralGroup) return;

        // Dispose old geometry
        while (chiralGroup.children.length > 0) {
            const c = chiralGroup.children[0];
            if (c.geometry) c.geometry.dispose();
            if (c.material) c.material.dispose();
            chiralGroup.remove(c);
        }

        const compound = COMPOUNDS[STATE.selectedSample];
        if (!compound) return;

        // Central sp³ carbon
        chiralGroup.add(new THREE.Mesh(
            new THREE.SphereGeometry(0.10, 14, 14),
            new THREE.MeshStandardMaterial({
                color: 0x444444, roughness: 0.3, metalness: 0.2
            })
        ));

        // Tetrahedral vertices — the fourth vertex is MIRRORED
        // for levorotatory compounds to show the R/S difference
        const s = compound.specificRotation >= 0 ? 1 : -1;
        const raw = [
            [1, 1, 1],
            [-1, -1, 1],
            [-1, 1, -1],
            [s, -s, -s]             // enantiomer switch
        ];

        const armLen = 0.30;
        const colors = [0xef4444, 0x3b82f6, 0x22c55e, 0xf59e0b];
        const sizes = [0.085, 0.075, 0.065, 0.070];
        const bondMat = new THREE.MeshStandardMaterial({
            color: 0x667788, roughness: 0.5
        });

        raw.forEach((v, i) => {
            const len = Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
            const dir = new THREE.Vector3(
                v[0] / len, v[1] / len, v[2] / len);
            const pos = dir.clone().multiplyScalar(armLen);

            // Bond cylinder
            const bond = new THREE.Mesh(
                new THREE.CylinderGeometry(0.018, 0.018, armLen, 5),
                bondMat
            );
            bond.position.copy(pos.clone().multiplyScalar(0.5));
            bond.quaternion.setFromUnitVectors(
                new THREE.Vector3(0, 1, 0), dir);
            chiralGroup.add(bond);

            // Substituent sphere
            chiralGroup.add(Object.assign(
                new THREE.Mesh(
                    new THREE.SphereGeometry(sizes[i], 10, 10),
                    new THREE.MeshStandardMaterial({
                        color: colors[i], roughness: 0.3, metalness: 0.15,
                        emissive: colors[i], emissiveIntensity: 0.12
                    })
                ),
                { position: pos }
            ));
        });
    }


    // ═══════════════════════════════════════════════════════
    //  MAIN ANIMATION LOOP
    // ═══════════════════════════════════════════════════════

    function animateScene() {
        animationId = requestAnimationFrame(animateScene);
        const time = performance.now() * 0.001;       // seconds

        // ── 1. Camera ───────────────────────────────────────
        if (camTransition) {
            const r = 0.055;
            cam.theta += (camTransition.theta - cam.theta) * r;
            cam.phi += (camTransition.phi - cam.phi) * r;
            cam.radius += (camTransition.radius - cam.radius) * r;
            if (Math.abs(cam.theta - camTransition.theta) < 0.003 &&
                Math.abs(cam.phi - camTransition.phi) < 0.003 &&
                Math.abs(cam.radius - camTransition.radius) < 0.02) {
                cam.theta = camTransition.theta;
                cam.phi = camTransition.phi;
                cam.radius = camTransition.radius;
                camTransition = null;
            }
        } else if (cam.autoRotate && !cam.dragging) {
            cam.theta += cam.speed;
        }
        updateCameraFromSpherical();

        // ── 2. Smooth beam intensity ────────────────────────
        beamIntensity += (targetBeamIntensity - beamIntensity) * 0.045;

        // ── 3. Smooth rotation angle ────────────────────────
        const rateAlpha = STATE.isMeasuring ? 0.035 : 0.06;
        currentRotationDeg +=
            (targetRotationDeg - currentRotationDeg) * rateAlpha;

        // ── 4. Analyser disc ────────────────────────────────
        if (analyzerRotGroup) {
            const tgtRad = currentRotationDeg * Math.PI / 180;
            currentAnalyzerAng +=
                (tgtRad - currentAnalyzerAng) * 0.04;
            analyzerRotGroup.rotation.x = currentAnalyzerAng;
        }

        // ── 5. Lamp glow + fault flicker ────────────────────
        if (lampGlow) {
            if (beamIntensity > 0.01) {
                const fault = FAULTS[STATE.fault];
                let fm = 1;      // flicker multiplier
                if (fault && fault.flicker > 0) {
                    fm = 1 - fault.flicker * 0.5 *
                        (1 + Math.sin(time * 17.3)) *
                        (1 + Math.sin(time * 23.7)) * 0.25;
                }
                const pulse = 0.85 + 0.15 * Math.sin(time * 2.5);
                lampGlow.material.opacity =
                    beamIntensity * pulse * fm * 0.80;
                if (lampLight)
                    lampLight.intensity =
                        beamIntensity * pulse * fm * 2.5;
            } else {
                lampGlow.material.opacity = 0;
                if (lampLight) lampLight.intensity = 0;
            }
        }

        // ── 6. Molecule tumble ──────────────────────────────
        if (chiralGroup) {
            chiralGroup.rotation.y +=
                STATE.isMeasuring ? 0.016 : 0.004;
            chiralGroup.rotation.x =
                Math.sin(time * 0.40) * 0.10;
            chiralGroup.rotation.z =
                Math.cos(time * 0.28) * 0.07;
        }

        // ── 7. Light beam / waves ───────────────────────────
        updateBeam(time);

        // ── 8. HUD overlay ──────────────────────────────────
        updateHUD(currentRotationDeg);

        // ── 9. Render ───────────────────────────────────────
        if (renderer && scene && camera) {
            renderer.render(scene, camera);
        }
    }


    // ═══════════════════════════════════════════════════════
    //  PUBLIC SETTERS  (called by Part 3 UI/measurement logic)
    // ═══════════════════════════════════════════════════════

    /** Animate toward a target observed rotation (°) */
    function setTargetRotation(degrees) {
        targetRotationDeg = degrees;
    }

    /** Animate beam brightness  (0 = off … 1 = full) */
    function setBeamIntensity(val) {
        targetBeamIntensity = Math.max(0, Math.min(1, val));
    }

    /** Jump immediately to a rotation value (no smooth lerp) */
    function snapRotation(degrees) {
        targetRotationDeg = degrees;
        currentRotationDeg = degrees;
        currentAnalyzerAng = degrees * Math.PI / 180;
        if (analyzerRotGroup)
            analyzerRotGroup.rotation.x = currentAnalyzerAng;
        updateHUD(degrees);
    }


    // ═══════════════════════════════════════════════════════
    //  END OF PART 2
    //
    //  Part 3 continues with:
    //    • Biot's-law calculation engine
    //    • Startup wizard  (lamp → zero → sample → ready)
    //    • Real-time measurement with progressive convergence
    //    • Result display & EE-bar update
    //    • Report generation
    //    • Modal open / close / settings application
    //    • Full event binding
    //    • init()  — calls initScene → buildLightBeam →
    //      bindViewControls → bindEvents → animateScene
    //    • Closing of DOMContentLoaded callback
    // ═══════════════════════════════════════════════════════
    // ═══════════════════════════════════════════════════════
    //  PART 3 OF 3
    //  Biot's-law calculation, startup wizard, measurement
    //  engine, results, report, modals, events, init()
    // ═══════════════════════════════════════════════════════


    // ═══════════════════════════════════════════════════════
    //  BIOT'S LAW CALCULATION ENGINE
    //
    //  α_obs = [α]_λ^T × c × l
    //
    //  where
    //    [α]_λ^T  = specific rotation at wavelength λ and
    //               temperature T
    //    c        = concentration  (g mL⁻¹)
    //    l        = path length    (dm)
    //
    //  Temperature correction (linear approx):
    //    [α]^T ≈ [α]^20 × [1 − 0.0005 × (T − 20)]
    //
    //  Wavelength correction (Drude single-term approx):
    //    [α]_λ ≈ [α]_D × (589.3² / λ²)
    //    (only applied when λ ≠ 589.3 nm)
    //
    //  Gaussian noise is used instead of uniform random
    //  for realistic instrument behaviour.
    // ═══════════════════════════════════════════════════════

    /** Box-Muller Gaussian random, mean 0, stddev σ */
    function gaussRandom(sigma) {
        let u = 0, v = 0;
        while (u === 0) u = Math.random();
        while (v === 0) v = Math.random();
        return sigma * Math.sqrt(-2.0 * Math.log(u)) *
            Math.cos(2.0 * Math.PI * v);
    }

    /**
     * Calculate the observed optical rotation and all
     * derived quantities for the current instrument state.
     *
     * Returns null if no compound is selected.
     */
    function calculateRotation() {
        const compound = COMPOUNDS[STATE.selectedSample];
        if (!compound) return null;

        const fault = FAULTS[STATE.fault] || FAULTS.none;

        // ── Temperature correction ──────────────────────────
        const tempCorr = 1 - 0.0005 * (STATE.temperature - 20);

        // ── Wavelength correction (Drude) ───────────────────
        const lambda = STATE.wavelength;
        const waveCorr = (lambda === 589.3)
            ? 1.0
            : (589.3 * 589.3) / (lambda * lambda);

        // ── Corrected specific rotation ─────────────────────
        const specificCorrected =
            compound.specificRotation * tempCorr * waveCorr;

        // ── Observed rotation: Biot's law ───────────────────
        let observed =
            specificCorrected * STATE.concentration * STATE.pathLength;

        // ── Instrument noise & drift (fault-dependent) ──────
        observed += gaussRandom(fault.noise);
        observed += fault.drift;

        // ── Back-calculate specific rotation from observed ──
        //    (this is what the user would do in the lab)
        const specificMeasured =
            observed / (STATE.concentration * STATE.pathLength);

        // ── Enantiomeric excess ─────────────────────────────
        //    %ee = |[α]_meas / [α]_pure| × 100
        //    using the wave-corrected literature value as pure
        const pureLit = compound.specificRotation * waveCorr;
        const ee = (pureLit !== 0)
            ? Math.min(100,
                Math.abs(specificMeasured / pureLit) * 100)
            : 0;

        // ── Direction / configuration ───────────────────────
        let configuration;
        if (observed > 0.01) configuration = 'Dextrorotatory (+)';
        else if (observed < -0.01) configuration = 'Levorotatory (−)';
        else configuration = 'Optically inactive';

        return {
            observed: parseFloat(observed.toFixed(4)),
            specific: parseFloat(specificMeasured.toFixed(2)),
            specificLit: compound.specificRotation,
            ee: parseFloat(ee.toFixed(1)),
            compound: compound.name,
            configuration,
            wavelength: lambda,
            temperature: STATE.temperature,
            concentration: STATE.concentration,
            pathLength: STATE.pathLength,
            solvent: compound.solvent,
            fault: STATE.fault
        };
    }


    // ═══════════════════════════════════════════════════════
    //  UPDATE RESULT DISPLAYS
    // ═══════════════════════════════════════════════════════

    function updateResultCards(result) {
        if (!result) return;

        const sign = (v) => v > 0 ? '+' : '';

        // ── Left panel live params ──────────────────────────
        setText('live-wavelength', STATE.wavelength.toFixed(1));
        setText('live-path', STATE.pathLength.toFixed(1));
        setText('live-temp', STATE.temperature.toFixed(1));
        setText('live-conc', STATE.concentration.toFixed(3));

        // ── Results card ────────────────────────────────────
        const alphaStr = `${sign(result.observed)}${result.observed.toFixed(3)}°`;
        const specStr = `${sign(result.specific)}${result.specific.toFixed(1)}°`;

        setText('res-alpha', alphaStr);
        setText('res-specific', specStr);
        setText('res-ee', `${result.ee.toFixed(1)}%`);
        setText('res-config', result.configuration);

        // Colour the alpha value
        const alphaEl = document.getElementById('res-alpha');
        if (alphaEl) {
            alphaEl.style.color =
                result.observed > 0.01 ? '#22c55e' :
                    result.observed < -0.01 ? '#ef4444' : '#94a3b8';
        }

        // ── EE bar ──────────────────────────────────────────
        //    Bar centre = 50% = racemic.
        //    Fill extends RIGHT for (+) compounds, LEFT for (−).
        //    Width = ee/2  (so 100% ee fills exactly half the bar).
        const bar = document.getElementById('ee-bar-fill');
        if (bar) {
            const ee = Math.min(100, result.ee);
            const half = ee / 2;                     // % of bar width
            if (result.observed > 0.01) {
                // Dextrorotatory → fill right of centre
                bar.style.left = '50%';
                bar.style.width = half + '%';
                bar.className = 'ee-bar-fill r-form';
            } else if (result.observed < -0.01) {
                // Levorotatory → fill left of centre
                bar.style.left = (50 - half) + '%';
                bar.style.width = half + '%';
                bar.className = 'ee-bar-fill s-form';
            } else {
                // Racemic / inactive
                bar.style.left = '49%';
                bar.style.width = '2%';
                bar.className = 'ee-bar-fill racemic';
            }
        }

        // ── Compound info panel ─────────────────────────────
        const c = COMPOUNDS[STATE.selectedSample];
        if (c) {
            setText('info-name', c.name);
            setText('info-formula', c.formula);
            setText('info-mw', c.mw.toFixed(2) + ' g/mol');
            setText('info-solvent', c.solvent);
            const litSign = c.specificRotation > 0 ? '+' : '';
            setText('info-lit-rotation',
                `${litSign}${c.specificRotation.toFixed(1)}°`);
        }

        // ── Quick-stats bar (instrument view) ───────────────
        setText('qs-rotation', alphaStr);
        setText('qs-temp', STATE.temperature.toFixed(1) + ' °C');
    }

    /** Safe text setter */
    function setText(id, val) {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
    }


    // ═══════════════════════════════════════════════════════
    //  STARTUP WIZARD
    // ═══════════════════════════════════════════════════════

    function goToWizardStep(step) {
        STATE.wizardStep = step;

        $$('.wizard-step').forEach((ws, i) => {
            ws.classList.remove('active', 'completed');
            if (i === step - 1) ws.classList.add('active');
            else if (i < step - 1) ws.classList.add('completed');
        });

        $$('.wizard-connector').forEach((conn, i) => {
            conn.classList.toggle('completed', i < step - 1);
        });

        $$('.wizard-panel').forEach((wp, i) => {
            wp.classList.toggle('active', i === step - 1);
        });

        const prev = $('#wizard-prev-btn');
        const next = $('#wizard-next-btn');
        const fin = $('#wizard-finish-btn');
        if (prev) prev.disabled = (step <= 1);
        if (next) next.classList.toggle('hidden', step >= 4);
        if (fin) fin.classList.toggle('hidden', step < 4);

        // Disable "Next" until the step action is completed
        if (next && step < 4) next.disabled = true;
    }


    // ── Step 1: Lamp warm-up ────────────────────────────────
    function lampWarmUp() {
        const btn = $('#btn-lamp-on');
        if (btn) btn.disabled = true;

        addLog('▶ Sodium vapour lamp igniting…', 'info');
        addLog('  Target: monochromatic 589.3 nm D-line', 'info');

        // Update instrument-view lamp indicator
        const ind = document.getElementById('lamp-indicator');
        if (ind) ind.classList.add('lamp-warming');

        let intensity = 0;
        const iv = setInterval(() => {
            // Non-linear ramp — slow start, faster middle, slow finish
            if (intensity < 30) intensity += 2;
            else if (intensity < 80) intensity += 4;
            else intensity += 1.5;
            if (intensity > 100) intensity = 100;

            setText('status-intensity', Math.round(intensity) + '%');

            // ── 3D scene: lamp glow ramp ────────────────────
            setBeamIntensity(intensity / 100);
            if (lampGlow) {
                lampGlow.material.opacity = (intensity / 100) * 0.80;
            }
            if (lampLight) {
                lampLight.intensity = (intensity / 100) * 2.5;
            }

            if (intensity >= 100) {
                clearInterval(iv);

                setText('status-lamp', '✓ Stable');
                setText('status-intensity', '100%');
                setText('qs-lamp', 'Stable');

                const sLamp = $('#status-lamp');
                const sInt = $('#status-intensity');
                if (sLamp) sLamp.className = 'status-value done';
                if (sInt) sInt.className = 'status-value done';

                if (ind) {
                    ind.classList.remove('lamp-warming');
                    ind.classList.add('lamp-on');
                }
                setText('lamp-status-text', 'Stable — 589.3 nm');

                addLog('✓ Sodium lamp stable — D-line emission locked', 'success');
                toast('Sodium lamp stabilised', 'success');

                const next = $('#wizard-next-btn');
                if (next) next.disabled = false;
                const zero = $('#btn-zero');
                if (zero) zero.disabled = false;
            }
        }, 55);
    }


    // ── Step 2: Zero-point calibration ──────────────────────
    function zeroCalibrate() {
        const btn = $('#btn-zero');
        if (btn) btn.disabled = true;

        addLog('▶ Zero calibration — blank solvent tube inserted', 'info');

        let progress = 0;
        let phase = 0;
        const iv = setInterval(() => {
            progress += 1.5;

            if (progress >= 20 && phase === 0) {
                phase = 1;
                addLog('  Measuring blank reading…', 'info');
            }
            if (progress >= 45 && phase === 1) {
                phase = 2;
                addLog('  Adjusting analyser null point…', 'info');
                // Animate analyser wiggle during calibration
                setTargetRotation(0.3 * Math.sin(progress * 0.3));
            }
            if (progress >= 70 && phase === 2) {
                phase = 3;
                addLog('  Fine-tuning zero position…', 'info');
                setTargetRotation(-0.1 * Math.sin(progress * 0.5));
            }
            if (progress >= 85 && phase === 3) {
                phase = 4;
                addLog('  Verifying stability (3 readings)…', 'info');
                setTargetRotation(0);
            }

            if (progress >= 100) {
                clearInterval(iv);
                snapRotation(0);

                setText('status-zero', '✓ 0.000° ± 0.002°');
                const el = $('#status-zero');
                if (el) el.className = 'status-value done';

                addLog('✓ Zero calibrated: 0.000° ± 0.002°', 'success');
                toast('Zero-point calibration complete', 'success');

                const next = $('#wizard-next-btn');
                if (next) next.disabled = false;
                const load = $('#btn-load-sample');
                if (load) load.disabled = false;
            }
        }, 45);
    }


    // ── Step 3: Load sample ─────────────────────────────────
    function loadSample() {
        const btn = $('#btn-load-sample');
        if (btn) btn.disabled = true;

        const c = COMPOUNDS[STATE.selectedSample];
        addLog(`▶ Loading sample: ${c?.name || 'Unknown'}`, 'info');
        addLog(`  c = ${STATE.concentration.toFixed(3)} g/mL` +
            ` | l = ${STATE.pathLength.toFixed(1)} dm` +
            ` | T = ${STATE.temperature.toFixed(1)} °C`, 'info');
        addLog(`  Solvent: ${c?.solvent || '—'}`, 'info');

        // Rebuild the 3D molecule
        rebuildChiralCenter();

        // Brief delay simulating tube insertion
        setTimeout(() => {
            const name = c?.name || 'Loaded';

            setText('status-sample', name);
            const el = $('#status-sample');
            if (el) el.className = 'status-value done';

            setText('sample-name', name);

            // Liquid colour tint changes slightly per compound
            if (sampleLiquid) {
                const hues = {
                    Sucrose: 0x22c55e, Glucose: 0x3b82f6,
                    Fructose: 0xf59e0b, Tartaric_L: 0x8b5cf6,
                    Tartaric_D: 0xa855f7, Camphor: 0x06b6d4,
                    Menthol: 0x14b8a6, Ibuprofen_S: 0xf43f5e,
                    Naproxen_S: 0xe879f9, Quinine: 0xfbbf24
                };
                const col = hues[STATE.selectedSample] || 0x22c55e;
                sampleLiquid.material.color.setHex(col);
                sampleLiquid.material.opacity = 0.06;
            }

            addLog('✓ Observation tube inserted — temperature equilibrating…', 'info');

            // Temperature equilibration
            setTimeout(() => {
                addLog('✓ Sample at thermal equilibrium', 'success');
                toast(`${name} loaded — ready`, 'success');

                // Auto-advance to step 4
                goToWizardStep(4);
            }, 600);

        }, 500);
    }


    // ── Step 4: Finish wizard ───────────────────────────────
    function finishWizard() {
        STATE.systemReady = true;

        // Update system status chip
        const chip = document.getElementById('system-status-chip');
        if (chip) {
            chip.innerHTML =
                '<span class="status-dot online"></span>' +
                '<span>System Ready</span>';
        }

        // Switch to measurement view
        $$('.view').forEach(v => v.classList.remove('active'));
        $('#main-screen-view').classList.add('active');
        closeAllModals();

        // Enable measure button
        const run = $('#run-button');
        if (run) run.disabled = false;

        // Populate displays
        const c = COMPOUNDS[STATE.selectedSample];
        if (c) {
            setText('sample-name', c.name);
            setText('info-name', c.name);
            setText('info-formula', c.formula);
            setText('info-mw', c.mw.toFixed(2) + ' g/mol');
            setText('info-solvent', c.solvent);
            const ls = c.specificRotation > 0 ? '+' : '';
            setText('info-lit-rotation',
                `${ls}${c.specificRotation.toFixed(1)}°`);
        }
        setText('live-wavelength', STATE.wavelength.toFixed(1));
        setText('live-path', STATE.pathLength.toFixed(1));
        setText('live-temp', STATE.temperature.toFixed(1));
        setText('live-conc', STATE.concentration.toFixed(3));

        addLog('━━━ System startup complete ━━━', 'success');
        addLog('Press MEASURE to begin optical rotation determination', 'info');
        toast('Polarimeter ready for measurement!', 'success');

        // Trigger viewport resize after layout settles
        setTimeout(resizeViewport, 250);
    }

    /** Force a resize of the 3D viewport to match its container */
    function resizeViewport() {
        const container = $('#viewport-3d');
        if (!container || !renderer || !camera) return;
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    }


    // ═══════════════════════════════════════════════════════
    //  MEASUREMENT ENGINE
    //
    //  Simulates the real-time convergence of a polarimetric
    //  measurement.  The displayed rotation starts with large
    //  wobble and progressively stabilises toward the true
    //  Biot's-law value — mimicking a real digital polarimeter.
    //
    //  Fault modes add visible noise and drift.
    //
    //  Duration:
    //    Normal  : 8 seconds  (allows user to observe convergence)
    //    Instant : 0.5 seconds
    // ═══════════════════════════════════════════════════════

    function startMeasurement() {
        if (STATE.isMeasuring) return;
        if (!STATE.systemReady) {
            toast('Complete system startup first', 'warning');
            return;
        }

        STATE.isMeasuring = true;
        STATE._measureAnim = null;

        // Button states
        setBtn('run-button', true);
        setBtn('stop-button', false);
        setBtn('sst-report-button', true);

        setText('screen-title', 'Measuring…');
        const rstatus = $('#run-status-indicator');
        if (rstatus) rstatus.classList.add('running');

        addLog('━━━ Measurement started ━━━', 'info');
        addLog(`  ${COMPOUNDS[STATE.selectedSample]?.name || '—'}` +
            ` | c=${STATE.concentration} g/mL` +
            ` | l=${STATE.pathLength} dm` +
            ` | T=${STATE.temperature}°C`, 'info');
        if (STATE.fault !== 'none') {
            addLog(`  ⚠ Fault active: ${STATE.fault}`, 'warning');
        }

        // Calculate true result
        const target = calculateRotation();
        if (!target) {
            stopMeasurement();
            toast('Calculation error — no compound selected', 'error');
            return;
        }

        setBeamIntensity(1.0);

        const duration = STATE.instantMode ? 500 : 8000;
        const start = performance.now();
        const fill = document.getElementById('timer-progress-fill');
        let logPhase = 0;

        const tick = () => {
            if (!STATE.isMeasuring) return;

            const elapsed = performance.now() - start;
            const progress = Math.min(1, elapsed / duration);
            const t = elapsed * 0.001;         // seconds

            // ── Timer display ───────────────────────────────
            if (fill) fill.style.width = (progress * 100) + '%';
            const sec = t.toFixed(1);
            setText('elapsed-time',
                t < 10 ? `00:0${sec}` : `00:${sec}`);

            // ── Progressive convergence ─────────────────────
            //    Wobble envelope decays as progress → 1
            //    amplitude ∝ (1 − progress)^1.5
            //    frequency decreases over time
            const envelope = Math.pow(1 - progress, 1.5);
            const wobble =
                envelope * 3.0 * Math.sin(t * 12) +
                envelope * 1.5 * Math.sin(t * 7.3) +
                envelope * 0.8 * Math.cos(t * 19);

            // Fault jitter persists even as wobble decays
            const fault = FAULTS[STATE.fault] || FAULTS.none;
            const faultNoise = gaussRandom(fault.noise) * 0.5;
            const faultDrift = fault.drift *
                Math.sin(t * 0.7) * (0.3 + 0.7 * (1 - progress));

            const displayed =
                target.observed * progress +
                wobble * (1 - progress) +
                faultNoise +
                faultDrift * (1 - progress * 0.5);

            setTargetRotation(displayed);

            // ── Phase-based log messages ────────────────────
            if (progress > 0.05 && logPhase === 0) {
                logPhase = 1;
                addLog('  Unpolarised light → polariser…', 'info');
            }
            if (progress > 0.20 && logPhase === 1) {
                logPhase = 2;
                addLog('  Plane-polarised light entering sample tube…', 'info');
            }
            if (progress > 0.40 && logPhase === 2) {
                logPhase = 3;
                addLog('  Chiral molecules rotating polarisation plane…', 'info');
            }
            if (progress > 0.60 && logPhase === 3) {
                logPhase = 4;
                addLog('  Analyser servo tracking rotation angle…', 'info');
            }
            if (progress > 0.80 && logPhase === 4) {
                logPhase = 5;
                addLog('  Signal stabilising — averaging 10 readings…', 'info');
            }
            if (progress > 0.95 && logPhase === 5) {
                logPhase = 6;
                addLog('  Final value locked', 'info');
            }

            // ── Header progress ─────────────────────────────
            setText('screen-title',
                `Measuring… ${Math.round(progress * 100)}%`);

            // ── Completion ──────────────────────────────────
            if (elapsed >= duration) {
                completeMeasurement(target);
                return;
            }

            STATE._measureAnim = requestAnimationFrame(tick);
        };

        STATE._measureAnim = requestAnimationFrame(tick);
    }

    function completeMeasurement(result) {
        STATE.isMeasuring = false;
        if (!result) result = calculateRotation();
        STATE.lastResult = result;

        // Snap to final value
        snapRotation(result.observed);
        updateResultCards(result);

        // Button states
        setBtn('run-button', false);
        setBtn('stop-button', true);
        setBtn('sst-report-button', false);

        setText('screen-title', 'Measurement Complete');
        const rstatus = $('#run-status-indicator');
        if (rstatus) rstatus.classList.remove('running');

        // Logs
        const s = (v) => v > 0 ? '+' : '';
        addLog(`✓ Observed rotation α = ` +
            `${s(result.observed)}${result.observed.toFixed(3)}°`,
            'success');
        addLog(`  Specific rotation [α]D = ` +
            `${s(result.specific)}${result.specific.toFixed(1)}°`,
            'info');
        addLog(`  Enantiomeric excess = ${result.ee.toFixed(1)}%`,
            'info');
        addLog(`  ${result.configuration}`, 'info');
        addLog('━━━ Measurement complete ━━━', 'success');

        toast(`α = ${s(result.observed)}${result.observed.toFixed(3)}°`,
            'success');
    }

    function stopMeasurement() {
        STATE.isMeasuring = false;
        if (STATE._measureAnim) {
            cancelAnimationFrame(STATE._measureAnim);
            STATE._measureAnim = null;
        }

        setBtn('run-button', false);
        setBtn('stop-button', true);

        setText('screen-title', 'Stopped');
        const rstatus = $('#run-status-indicator');
        if (rstatus) rstatus.classList.remove('running');

        addLog('⏹ Measurement stopped by user', 'warning');
    }

    function resetMeasurement() {
        stopMeasurement();
        STATE.lastResult = null;

        snapRotation(0);

        ['res-alpha', 'res-specific', 'res-ee', 'res-config']
            .forEach(id => setText(id, '--'));

        setText('elapsed-time', '00:00.0');
        const fill = document.getElementById('timer-progress-fill');
        if (fill) fill.style.width = '0%';

        setText('screen-title', 'Ready');
        setText('qs-rotation', '--');

        // Reset EE bar
        const bar = document.getElementById('ee-bar-fill');
        if (bar) {
            bar.style.left = '49%';
            bar.style.width = '2%';
            bar.className = 'ee-bar-fill racemic';
        }

        addLog('System reset — ready for new measurement', 'info');
    }

    /** Helper to enable/disable button by ID */
    function setBtn(id, disabled) {
        const el = document.getElementById(id);
        if (el) el.disabled = disabled;
    }


    // ═══════════════════════════════════════════════════════
    //  REPORT GENERATION
    // ═══════════════════════════════════════════════════════

    function generateReport() {
        const r = STATE.lastResult;
        if (!r) {
            toast('Take a measurement first', 'warning');
            return;
        }

        const c = COMPOUNDS[STATE.selectedSample];
        const s = (v) => v > 0 ? '+' : '';
        const now = new Date();
        const date = now.toLocaleDateString('en-GB', {
            day: '2-digit', month: 'short', year: 'numeric'
        });
        const time = now.toLocaleTimeString([], {
            hour: '2-digit', minute: '2-digit'
        });

        // Compare measured vs literature
        const litVal = c ? c.specificRotation : 0;
        const devPct = litVal !== 0
            ? Math.abs((r.specific - litVal) / litVal * 100).toFixed(1)
            : '--';
        const passStr = parseFloat(devPct) < 5
            ? '<span style="color:#22c55e;font-weight:700">PASS</span>'
            : '<span style="color:#ef4444;font-weight:700">DEVIATION &gt; 5%</span>';

        const reportEl = document.getElementById('report-body');
        if (!reportEl) return;

        reportEl.innerHTML = `
            <div class="report-section">
                <h4>Measurement Certificate</h4>
                <table class="report-table">
                    <tr><td>Date / Time</td><td>${date} — ${time}</td></tr>
                    <tr><td>Compound</td><td>${r.compound}</td></tr>
                    <tr><td>Formula</td><td>${c?.formula || '--'}</td></tr>
                    <tr><td>Molecular Weight</td><td>${c ? c.mw.toFixed(2) + ' g/mol' : '--'}</td></tr>
                    <tr><td>Solvent</td><td>${r.solvent}</td></tr>
                    <tr><td>CAS Number</td><td>${c?.cas || '--'}</td></tr>
                </table>
            </div>

            <div class="report-section">
                <h4>Instrument Parameters</h4>
                <table class="report-table">
                    <tr><td>Wavelength (λ)</td><td>${r.wavelength} nm</td></tr>
                    <tr><td>Temperature (T)</td><td>${r.temperature.toFixed(1)} °C</td></tr>
                    <tr><td>Path Length (l)</td><td>${r.pathLength.toFixed(1)} dm</td></tr>
                    <tr><td>Concentration (c)</td><td>${r.concentration.toFixed(3)} g/mL</td></tr>
                    <tr><td>Fault Simulation</td><td>${r.fault === 'none' ? 'None' : r.fault}</td></tr>
                </table>
            </div>

            <div class="report-section">
                <h4>Results</h4>
                <table class="report-table">
                    <tr><td>Observed Rotation (α)</td>
                        <td style="font-size:16px;font-weight:700;color:${r.observed > 0.01 ? '#22c55e' :
                r.observed < -0.01 ? '#ef4444' : '#94a3b8'
            }">${s(r.observed)}${r.observed.toFixed(3)}°</td></tr>
                    <tr><td>Specific Rotation [α]<sub>D</sub><sup>T</sup></td>
                        <td>${s(r.specific)}${r.specific.toFixed(1)}°</td></tr>
                    <tr><td>Literature [α]<sub>D</sub><sup>20</sup></td>
                        <td>${c ? s(litVal) + litVal.toFixed(1) + '°' : '--'}</td></tr>
                    <tr><td>Deviation from Literature</td>
                        <td>${devPct}%</td></tr>
                    <tr><td>Enantiomeric Excess (%ee)</td>
                        <td>${r.ee.toFixed(1)}%</td></tr>
                    <tr><td>Configuration</td>
                        <td>${r.configuration}</td></tr>
                </table>
            </div>

            <div class="report-verdict ${parseFloat(devPct) >= 5 ? 'fail' : ''}">
                <div class="verdict-label">Quality Assessment</div>
                <div class="verdict-value">${passStr}</div>
                <div style="font-size:11px;color:#64748b;margin-top:4px">
                    Biot's Law: [α] = α / (l × c) = ${s(r.observed)}${r.observed.toFixed(3)} / (${r.pathLength.toFixed(1)} × ${r.concentration.toFixed(3)}) = ${s(r.specific)}${r.specific.toFixed(1)}°
                </div>
            </div>
        `;

        openModal('sst-modal');
    }


    // ═══════════════════════════════════════════════════════
    //  MODAL MANAGEMENT
    // ═══════════════════════════════════════════════════════

    function openModal(id) {
        const modal = document.getElementById(id);
        const backdrop = document.getElementById('modal-backdrop');
        if (modal) {
            modal.classList.remove('hidden');
            if (backdrop) backdrop.classList.remove('hidden');
        }
    }

    function closeAllModals() {
        $$('.modal').forEach(m => m.classList.add('hidden'));
        const backdrop = document.getElementById('modal-backdrop');
        if (backdrop) backdrop.classList.add('hidden');
    }


    // ═══════════════════════════════════════════════════════
    //  SETTINGS APPLICATION
    // ═══════════════════════════════════════════════════════

    function applySettings() {
        // ── Sample ──────────────────────────────────────────
        const sampleEl = document.getElementById('sample-select');
        if (sampleEl) STATE.selectedSample = sampleEl.value;

        // ── Concentration ───────────────────────────────────
        const concNum = document.getElementById('conc-number');
        if (concNum) STATE.concentration = parseFloat(concNum.value) || 0.10;

        // ── Path length ─────────────────────────────────────
        const pathNum = document.getElementById('path-number');
        if (pathNum) STATE.pathLength = parseFloat(pathNum.value) || 1.0;

        // ── Temperature (from sample modal) ─────────────────
        const tempNum = document.getElementById('temp-number');
        if (tempNum) STATE.temperature = parseFloat(tempNum.value) || 20.0;

        // ── Temperature (from temp modal) ───────────────────
        const tempModal = document.getElementById('temp-modal-input');
        if (tempModal) {
            STATE.temperature = parseFloat(tempModal.value) || 20.0;
            // Sync the sample-modal temp inputs
            const ti = document.getElementById('temp-input');
            const tn = document.getElementById('temp-number');
            if (ti) ti.value = STATE.temperature;
            if (tn) tn.value = STATE.temperature;
        }

        // ── Wavelength ──────────────────────────────────────
        const waveEl = document.querySelector('input[name=wavelength]:checked');
        if (waveEl) STATE.wavelength = parseFloat(waveEl.value) || 589.3;

        // ── Fault ───────────────────────────────────────────
        const faultEl = document.querySelector('input[name=fault-type]:checked');
        if (faultEl) STATE.fault = faultEl.value;

        // ── Update displays ─────────────────────────────────
        const c = COMPOUNDS[STATE.selectedSample];
        if (c) {
            setText('sample-name', c.name);
            setText('info-name', c.name);
            setText('info-formula', c.formula);
            setText('info-mw', c.mw.toFixed(2) + ' g/mol');
            setText('info-solvent', c.solvent);
            const ls = c.specificRotation > 0 ? '+' : '';
            setText('info-lit-rotation',
                `${ls}${c.specificRotation.toFixed(1)}°`);
            addLog(`Sample: ${c.name} | [α]D = ${ls}${c.specificRotation}°`, 'info');
        }

        setText('live-wavelength', STATE.wavelength.toFixed(1));
        setText('live-path', STATE.pathLength.toFixed(1));
        setText('live-temp', STATE.temperature.toFixed(1));
        setText('live-conc', STATE.concentration.toFixed(3));
        setText('qs-temp', STATE.temperature.toFixed(1) + ' °C');
        setText('temp-display', STATE.temperature.toFixed(1) + '°C');

        if (STATE.fault !== 'none') {
            addLog(`⚠ Fault simulation active: ${STATE.fault}`, 'warning');
            toast(`Fault: ${STATE.fault}`, 'warning');
        }

        // Rebuild 3D molecule for new compound
        rebuildChiralCenter();
    }


    // ═══════════════════════════════════════════════════════
    //  EVENT BINDING
    // ═══════════════════════════════════════════════════════

    function bindEvents() {

        // ── Instrument-view hotspots ────────────────────────
        $$('.hotspot').forEach(hs => {
            hs.addEventListener('click', () => {
                const target = hs.dataset.controls;
                if (target === 'screen-view') {
                    if (!STATE.systemReady) {
                        toast('Complete system startup first', 'warning');
                        return;
                    }
                    $$('.view').forEach(v => v.classList.remove('active'));
                    $('#main-screen-view').classList.add('active');
                    setTimeout(resizeViewport, 150);
                } else if (target) {
                    openModal(target);
                }
            });
        });

        // ── Startup button ──────────────────────────────────
        $('#hotspot-setup')?.addEventListener('click', () => {
            openModal('setup-modal');
        });

        // ── Wizard buttons ──────────────────────────────────
        $('#btn-lamp-on')?.addEventListener('click', lampWarmUp);
        $('#btn-zero')?.addEventListener('click', zeroCalibrate);
        $('#btn-load-sample')?.addEventListener('click', loadSample);

        $('#wizard-prev-btn')?.addEventListener('click', () => {
            if (STATE.wizardStep > 1)
                goToWizardStep(STATE.wizardStep - 1);
        });
        $('#wizard-next-btn')?.addEventListener('click', () => {
            if (STATE.wizardStep < 4)
                goToWizardStep(STATE.wizardStep + 1);
        });
        $('#wizard-finish-btn')?.addEventListener('click', finishWizard);

        // ── Navigation ──────────────────────────────────────
        $('#back-to-main-view-button')?.addEventListener('click', () => {
            $$('.view').forEach(v => v.classList.remove('active'));
            $('#hplc-main-view').classList.add('active');
        });

        // ── Measurement controls ────────────────────────────
        $('#run-button')?.addEventListener('click', startMeasurement);
        $('#stop-button')?.addEventListener('click', stopMeasurement);
        $('#reset-button')?.addEventListener('click', resetMeasurement);

        // ── Toggles ─────────────────────────────────────────
        $('#instant-mode-toggle')?.addEventListener('change', (e) => {
            STATE.instantMode = e.target.checked;
            addLog(e.target.checked
                ? 'Instant mode ON — fast measurement'
                : 'Instant mode OFF — realistic timing', 'info');
        });

        $('#fault-mode-toggle')?.addEventListener('change', (e) => {
            if (e.target.checked) {
                openModal('fault-selector-modal');
            } else {
                STATE.fault = 'none';
                addLog('Fault simulation disabled', 'info');
            }
        });

        // ── Report ──────────────────────────────────────────
        $('#sst-report-button')?.addEventListener('click', generateReport);
        $('#export-report-btn')?.addEventListener('click', () => {
            toast('Report exported (demo)', 'success');
        });

        // ── Modals: close buttons ───────────────────────────
        $$('.modal-close-btn').forEach(b =>
            b.addEventListener('click', closeAllModals));
        $('#modal-backdrop')?.addEventListener('click', closeAllModals);

        // ── Modals: confirm/apply ───────────────────────────
        $$('.modal-confirm-btn').forEach(b =>
            b.addEventListener('click', () => {
                applySettings();
                closeAllModals();
            })
        );

        // ── Column cards (radio-card selection) ─────────────
        $$('.column-card').forEach(card => {
            card.addEventListener('click', () => {
                const group = card.closest('.column-cards');
                if (group) {
                    group.querySelectorAll('.column-card')
                        .forEach(c => c.classList.remove('selected'));
                }
                card.classList.add('selected');
            });
        });

        // ── Range ↔ number sync ─────────────────────────────
        $$('.range-with-input').forEach(group => {
            const range = group.querySelector('input[type=range]');
            const number = group.querySelector('input[type=number]');
            if (range && number) {
                range.addEventListener('input', () => {
                    number.value = range.value;
                });
                number.addEventListener('input', () => {
                    range.value = number.value;
                });
            }
        });

        // ── Difficulty selector ─────────────────────────────
        $$('.difficulty-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                $$('.difficulty-btn').forEach(b =>
                    b.classList.remove('active'));
                btn.classList.add('active');
                STATE.difficulty = btn.dataset.level;
                addLog(`Difficulty: ${btn.dataset.level}`, 'info');
            });
        });

        // ── Temperature presets ─────────────────────────────
        $$('.temp-preset').forEach(btn => {
            btn.addEventListener('click', () => {
                $$('.temp-preset').forEach(b =>
                    b.classList.remove('active'));
                btn.classList.add('active');
                const t = parseFloat(btn.dataset.temp);
                const slider = document.getElementById('temp-modal-input');
                const display = document.getElementById('temp-modal-display');
                if (slider) slider.value = t;
                if (display) display.textContent = t.toFixed(1);
            });
        });

        // Temperature slider live update
        const tempSlider = document.getElementById('temp-modal-input');
        if (tempSlider) {
            tempSlider.addEventListener('input', () => {
                const display =
                    document.getElementById('temp-modal-display');
                if (display)
                    display.textContent =
                        parseFloat(tempSlider.value).toFixed(1);
                // De-activate presets
                $$('.temp-preset').forEach(b =>
                    b.classList.remove('active'));
            });
        }

        // ── Clear log ───────────────────────────────────────
        $('#clear-log-btn')?.addEventListener('click', () => {
            const log = document.getElementById('log-content');
            if (log) log.innerHTML = '';
        });

        // ── Fullscreen ──────────────────────────────────────
        $('#fullscreen-button')?.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen()
                    .catch(() => { });
            } else {
                document.exitFullscreen().catch(() => { });
            }
        });

        // ── Keyboard shortcuts ──────────────────────────────
        document.addEventListener('keydown', (e) => {
            // Ignore when typing in inputs
            if (e.target.tagName === 'INPUT' ||
                e.target.tagName === 'SELECT') return;

            switch (e.key) {
                case ' ':
                case 'Enter':
                    e.preventDefault();
                    if (STATE.isMeasuring) stopMeasurement();
                    else if (STATE.systemReady) startMeasurement();
                    break;
                case 'r':
                case 'R':
                    resetMeasurement();
                    break;
                case '1':
                    setCameraPreset('default');
                    break;
                case '2':
                    setCameraPreset('side');
                    break;
                case '3':
                    setCameraPreset('front');
                    break;
                case '4':
                    setCameraPreset('top');
                    break;
                case 'a':
                case 'A':
                    cam.autoRotate = !cam.autoRotate;
                    camTransition = null;
                    const b = $('#view-animate-btn');
                    if (b) b.classList.toggle('active', cam.autoRotate);
                    break;
                case 'Escape':
                    closeAllModals();
                    break;
            }
        });
    }


    // ═══════════════════════════════════════════════════════
    //  SYSTEM CLOCK
    // ═══════════════════════════════════════════════════════

    function updateClock() {
        const el = document.getElementById('system-time');
        if (el) {
            el.textContent = new Date().toLocaleTimeString([], {
                hour: '2-digit', minute: '2-digit'
            });
        }
    }


    // ═══════════════════════════════════════════════════════
    //  INITIALISATION
    // ═══════════════════════════════════════════════════════

    function init() {
        // 1. Build 3D scene & static components (Part 1)
        initScene();

        // 2. Build light-beam visualisation (Part 2)
        buildLightBeam();

        // 3. Camera preset buttons (Part 2)
        bindViewControls();

        // 4. All UI event listeners (Part 3)
        bindEvents();

        // 5. System clock
        updateClock();
        setInterval(updateClock, 30000);

        // 6. Start render loop (Part 2)
        animateScene();

        // 7. Opening log
        addLog('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'info');
        addLog('SimuPharma Digital Polarimeter Twin v3.1', 'success');
        addLog('3D Optical Rotation System initialised', 'success');
        addLog('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'info');
        addLog('Click "System Startup" to begin', 'info');
        addLog('', 'info');

        // 8. Keyboard shortcut hint
        addLog('Shortcuts: Space=measure  R=reset  1-4=camera  A=auto-rotate  Esc=close', 'info');
    }

    // ── Launch ──────────────────────────────────────────────
    init();

});
// ═══════════════════════════════════════════════════════
//  END OF POLARIMETER SIMULATOR v3.1
// ═══════════════════════════════════════════════════════