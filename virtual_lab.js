/* ================================================================
   VIRTUAL LAB — Next-Gen 3D Pharmaceutical Laboratory
   Three.js r160+ | Advanced Physics | Cinematic Camera | PBR Materials
   ================================================================ */
(function () {
    'use strict';

    const currentPage = window.location.pathname.split('/').pop();
    if (currentPage !== 'instruments.html') return;

    // ===================== CONFIGURATION =====================
    const CONFIG = {
        movement: {
            speed: 5.5,
            runMultiplier: 1.8,
            smoothness: 0.12,
            rotationSpeed: 0.18
        },
        camera: {
            fov: 65,
            near: 0.1,
            far: 60,
            followDistance: 8,
            followHeight: 5,
            lookAheadDistance: 2,
            smoothness: 0.1,
            transitionDuration: 1.6
        },
        graphics: {
            shadows: true,
            antialias: true,
            maxPixelRatio: 2,
            toneMapping: true,
            fog: { near: 16, far: 28 }
        },
        interaction: {
            hoverDistance: 15,
            clickRadius: 12,
            outlineThickness: 0.035
        }
    };

    // ===================== ADVANCED STATE MANAGER =====================
    const LabStore = {
        isMovementEnabled: true,
        activeInstrument: null,
        hoveredInstrument: null,
        cameraMode: 'follow', // 'follow' | 'transitioning' | 'instrument'
        isRunning: false,
        characterState: 'idle', // 'idle' | 'walking' | 'running'
        _listeners: new Map(),
        _history: [],

        subscribe(key, fn) {
            if (!this._listeners.has(key)) this._listeners.set(key, []);
            this._listeners.get(key).push(fn);
            return () => this.unsubscribe(key, fn);
        },

        unsubscribe(key, fn) {
            const listeners = this._listeners.get(key);
            if (listeners) {
                const idx = listeners.indexOf(fn);
                if (idx > -1) listeners.splice(idx, 1);
            }
        },

        _notify(key) {
            const listeners = this._listeners.get(key);
            if (listeners) listeners.forEach(fn => fn(this[key], this));
            this._history.push({ key, value: this[key], timestamp: Date.now() });
            if (this._history.length > 50) this._history.shift();
        },

        setState(key, value) {
            if (this[key] !== value) {
                this[key] = value;
                this._notify(key);
            }
        },

        enableMovement() { this.setState('isMovementEnabled', true); },
        disableMovement() { this.setState('isMovementEnabled', false); },

        focusInstrument(id) {
            this.setState('activeInstrument', id);
            this.disableMovement();
        },

        exitInstrument() {
            this.setState('activeInstrument', null);
        },

        setHovered(id) {
            this.setState('hoveredInstrument', id);
        },

        setCameraMode(mode) {
            this.setState('cameraMode', mode);
        },

        setCharacterState(state) {
            this.setState('characterState', state);
        }
    };

    // ===================== ENHANCED INSTRUMENTS DATA =====================
    const INSTRUMENTS = [
        {
            id: 'hplc',
            name: 'HPLC System',
            fullName: 'High Performance Liquid Chromatography',
            description: 'Separates, identifies, and quantifies components in liquid mixtures',
            category: 'Chromatography',
            color: '#B8D8E8',
            outlineColor: '#1A4D6D',
            glowColor: '#7BC8F0',
            href: 'hplc.html',
            benchPos: [-5, 0, -6],
            icon: '📊',
            cameraPose: {
                position: [-4, 3.5, -3],
                lookAt: [-5, 1.4, -6],
                fov: 55
            },
            ui: {
                icon: '📊',
                params: [
                    { name: 'Mobile Phase Flow', min: 0.1, max: 2.0, default: 1.0, unit: 'mL/min', icon: '💧' },
                    { name: 'Column Temperature', min: 20, max: 60, default: 30, unit: '°C', icon: '🌡️' },
                    { name: 'Detection Wavelength', min: 190, max: 800, default: 254, unit: 'nm', icon: '🌈' },
                    { name: 'Injection Volume', min: 1, max: 100, default: 20, unit: 'µL', icon: '💉' }
                ]
            },
            parts: [
                { type: 'box', size: [0.9, 1.3, 0.7], pos: [0, 0.65, 0], color: '#B8D8E8', roughness: 0.3, metalness: 0.6 },
                { type: 'cylinder', args: [0.07, 0.07, 0.9, 16], pos: [-0.25, 1.1, 0], color: '#E8DFF5', roughness: 0.2, metalness: 0.8 },
                { type: 'box', size: [0.35, 0.25, 0.35], pos: [0, 1.4, 0], color: '#C8E6C9', emissive: '#4CAF50', emissiveIntensity: 0.2 },
                { type: 'cylinder', args: [0.14, 0.14, 0.3, 16], pos: [0.55, 0.25, 0], color: '#F5E6CC', transparent: true, opacity: 0.7 },
                { type: 'box', size: [0.8, 0.05, 0.6], pos: [0, -0.025, 0], color: '#2D2D2D', roughness: 0.1, metalness: 0.9 }
            ]
        },
        {
            id: 'ftir',
            name: 'FTIR Spectrometer',
            fullName: 'Fourier Transform Infrared Spectroscopy',
            description: 'Identifies chemical bonds and molecular structures via IR absorption',
            category: 'Spectroscopy',
            color: '#E8DFF5',
            outlineColor: '#5B3A7D',
            glowColor: '#D4A5F5',
            href: 'ftir.html',
            benchPos: [-1.5, 0, -6],
            icon: '🌊',
            cameraPose: {
                position: [-0.5, 3.5, -3],
                lookAt: [-1.5, 1.2, -6],
                fov: 55
            },
            ui: {
                icon: '🌊',
                params: [
                    { name: 'Resolution', min: 1, max: 16, default: 4, unit: 'cm⁻¹', icon: '📐' },
                    { name: 'Scan Range', min: 400, max: 4000, default: 4000, unit: 'cm⁻¹', icon: '📊' },
                    { name: 'Number of Scans', min: 1, max: 128, default: 32, unit: 'scans', icon: '🔄' }
                ]
            },
            parts: [
                { type: 'box', size: [1.3, 0.7, 0.9], pos: [0, 0.35, 0], color: '#E8DFF5', roughness: 0.4, metalness: 0.5 },
                { type: 'box', size: [0.35, 0.35, 0.35], pos: [-0.55, 0.85, 0], color: '#FF6B6B', emissive: '#FF4444', emissiveIntensity: 0.3 },
                { type: 'box', size: [0.25, 0.25, 0.25], pos: [0, 0.85, 0], color: '#C8E6C9', roughness: 0.2, metalness: 0.7 },
                { type: 'cylinder', args: [0.12, 0.12, 0.18, 16], pos: [0.5, 0.85, 0], color: '#B8D8E8', emissive: '#0891B2', emissiveIntensity: 0.2 },
                { type: 'box', size: [0.25, 0.08, 0.25], pos: [0, 0.9, 0.35], color: '#F5E6CC', roughness: 0.3 }
            ]
        },
        {
            id: 'gc',
            name: 'Gas Chromatograph',
            fullName: 'Gas Chromatography',
            description: 'Separates and analyzes volatile compounds in gas phase',
            category: 'Chromatography',
            color: '#F5E6CC',
            outlineColor: '#8B6F47',
            glowColor: '#FFD966',
            href: 'gc.html',
            benchPos: [3, 0, -6],
            icon: '🔥',
            cameraPose: {
                position: [4, 3.5, -3],
                lookAt: [3, 1.2, -6],
                fov: 55
            },
            ui: {
                icon: '🔥',
                params: [
                    { name: 'Oven Temperature', min: 50, max: 350, default: 150, unit: '°C', icon: '🔥' },
                    { name: 'Carrier Gas Flow', min: 0.5, max: 5.0, default: 1.5, unit: 'mL/min', icon: '💨' },
                    { name: 'Injection Volume', min: 0.1, max: 5.0, default: 1.0, unit: 'µL', icon: '💉' },
                    { name: 'Split Ratio', min: 1, max: 200, default: 50, unit: ':1', icon: '⚡' }
                ]
            },
            parts: [
                { type: 'box', size: [1.1, 1.1, 0.9], pos: [0, 0.55, 0], color: '#F5E6CC', roughness: 0.35, metalness: 0.55 },
                { type: 'cylinder', args: [0.05, 0.05, 0.7, 16], pos: [0, 0.55, 0], color: '#F8BBD0', roughness: 0.3 },
                { type: 'box', size: [0.25, 0.25, 0.25], pos: [0, 1.2, 0], color: '#FF6B6B', emissive: '#DC2626', emissiveIntensity: 0.4 },
                { type: 'box', size: [0.3, 0.2, 0.3], pos: [0.55, 1.1, 0], color: '#C8E6C9', emissive: '#10B981', emissiveIntensity: 0.3 },
                { type: 'cylinder', args: [0.18, 0.18, 0.7, 16], pos: [0.9, 0.35, 0], color: '#94A3B8', roughness: 0.2, metalness: 0.8 }
            ]
        },
        {
            id: 'mass-spec',
            name: 'Mass Spectrometer',
            fullName: 'Mass Spectrometry',
            description: 'Measures mass-to-charge ratio of ions for molecular identification',
            category: 'Spectrometry',
            color: '#C8E6C9',
            outlineColor: '#2D5A3D',
            glowColor: '#81C784',
            href: 'mass_spec.html',
            benchPos: [6, 0, -6],
            icon: '⚛️',
            cameraPose: {
                position: [7, 3.5, -3],
                lookAt: [6, 1.2, -6],
                fov: 55
            },
            ui: {
                icon: '⚛️',
                params: [
                    { name: 'Ion Source Voltage', min: 10, max: 200, default: 70, unit: 'eV', icon: '⚡' },
                    { name: 'Mass Range', min: 50, max: 2000, default: 1000, unit: 'm/z', icon: '⚖️' },
                    { name: 'Scan Speed', min: 100, max: 10000, default: 1000, unit: 'amu/s', icon: '⏱️' }
                ]
            },
            parts: [
                { type: 'box', size: [1.5, 0.9, 0.8], pos: [0, 0.45, 0], color: '#C8E6C9', roughness: 0.3, metalness: 0.6 },
                { type: 'box', size: [0.55, 0.35, 0.35], pos: [-0.55, 1.0, 0], color: '#B8D8E8', emissive: '#3B82F6', emissiveIntensity: 0.2 },
                { type: 'cylinder', args: [0.14, 0.14, 0.35, 16], pos: [0.35, 1.0, 0], color: '#E8DFF5', roughness: 0.25 },
                { type: 'box', size: [0.7, 0.5, 0.6], pos: [0, 0.55, 0], color: '#F5E6CC', roughness: 0.4 }
            ]
        },
        {
            id: 'uv-vis',
            name: 'UV-Vis Spectrophotometer',
            fullName: 'UV-Visible Spectroscopy',
            description: 'Measures light absorption in UV-visible spectrum for quantification',
            category: 'Spectroscopy',
            color: '#F8BBD0',
            outlineColor: '#7D2D4A',
            glowColor: '#FCE4EC',
            href: 'uv_vis.html',
            benchPos: [-3.5, 0, 0],
            icon: '☀️',
            cameraPose: {
                position: [-2.5, 3.5, 3],
                lookAt: [-3.5, 1.2, 0],
                fov: 55
            },
            ui: {
                icon: '☀️',
                params: [
                    { name: 'Wavelength', min: 190, max: 1100, default: 540, unit: 'nm', icon: '🌈' },
                    { name: 'Slit Width', min: 0.5, max: 5.0, default: 2.0, unit: 'nm', icon: '📏' },
                    { name: 'Scan Speed', min: 10, max: 1000, default: 200, unit: 'nm/min', icon: '⏩' }
                ]
            },
            parts: [
                { type: 'box', size: [1.3, 0.5, 0.7], pos: [0, 0.25, 0], color: '#F8BBD0', roughness: 0.35, metalness: 0.5 },
                { type: 'box', size: [0.15, 0.15, 0.15], pos: [-0.5, 0.55, 0], color: '#FFF9C4', emissive: '#FDD835', emissiveIntensity: 0.5 },
                { type: 'box', size: [0.18, 0.3, 0.18], pos: [0, 0.55, 0], color: '#B8D8E8', transparent: true, opacity: 0.6 },
                { type: 'cylinder', args: [0.1, 0.1, 0.15, 16], pos: [0.5, 0.55, 0], color: '#94A3B8', roughness: 0.2, metalness: 0.8 },
                { type: 'box', size: [0.7, 0.25, 0.5], pos: [0, 0.75, 0], color: '#1E293B', emissive: '#3B82F6', emissiveIntensity: 0.15 }
            ]
        },
        {
            id: 'polarimeter',
            name: 'Polarimeter',
            fullName: 'Polarimetry',
            description: 'Measures optical rotation of chiral compounds',
            category: 'Optical',
            color: '#C8E6C9',
            outlineColor: '#2D5A3D',
            glowColor: '#A5D6A7',
            href: 'polarimeter.html',
            benchPos: [0, 0, 0],
            icon: '🧭',
            cameraPose: {
                position: [1, 3.5, 3],
                lookAt: [0, 1.2, 0],
                fov: 55
            },
            ui: {
                icon: '🧭',
                params: [
                    { name: 'Wavelength', min: 365, max: 633, default: 589, unit: 'nm', icon: '💡' },
                    { name: 'Temperature', min: 15, max: 35, default: 25, unit: '°C', icon: '🌡️' },
                    { name: 'Tube Length', min: 5, max: 20, default: 10, unit: 'cm', icon: '📏' }
                ]
            },
            parts: [
                { type: 'box', size: [1.1, 0.4, 0.45], pos: [0, 0.2, 0], color: '#C8E6C9', roughness: 0.3, metalness: 0.6 },
                { type: 'cylinder', args: [0.18, 0.18, 0.9, 16], pos: [0, 0.4, 0], color: '#E8DFF5', transparent: true, opacity: 0.8 },
                { type: 'box', size: [0.25, 0.18, 0.25], pos: [-0.45, 0.6, 0], color: '#FFB74D', emissive: '#FF9800', emissiveIntensity: 0.3 },
                { type: 'box', size: [0.25, 0.18, 0.25], pos: [0.45, 0.6, 0], color: '#B8D8E8', emissive: '#0891B2', emissiveIntensity: 0.2 }
            ]
        },
        {
            id: 'psa',
            name: 'Particle Size Analyzer',
            fullName: 'Particle Size Analysis',
            description: 'Determines particle size distribution using laser diffraction',
            category: 'Physical',
            color: '#F8BBD0',
            outlineColor: '#7D2D4A',
            glowColor: '#F8BBD0',
            href: 'psa.html',
            benchPos: [3.5, 0, 0],
            icon: '🔬',
            cameraPose: {
                position: [4.5, 3.5, 3],
                lookAt: [3.5, 1.2, 0],
                fov: 55
            },
            ui: {
                icon: '🔬',
                params: [
                    { name: 'Dispersant Type', min: 0, max: 3, default: 1, unit: '', icon: '💧', options: ['Water', 'Ethanol', 'Hexane', 'Air'] },
                    { name: 'Obscuration', min: 5, max: 30, default: 15, unit: '%', icon: '🌫️' },
                    { name: 'Stirrer Speed', min: 500, max: 3000, default: 1500, unit: 'rpm', icon: '🌀' }
                ]
            },
            parts: [
                { type: 'box', size: [1.0, 0.8, 0.7], pos: [0, 0.4, 0], color: '#F8BBD0', roughness: 0.35, metalness: 0.55 },
                { type: 'box', size: [0.35, 0.35, 0.35], pos: [0, 0.95, 0], color: '#E8DFF5', emissive: '#9C27B0', emissiveIntensity: 0.2 },
                { type: 'cylinder', args: [0.08, 0.08, 0.35, 16], pos: [0.35, 0.55, 0.25], color: '#C8E6C9', transparent: true, opacity: 0.7 },
                { type: 'box', size: [0.8, 0.05, 0.6], pos: [0, -0.025, 0], color: '#2D2D2D', roughness: 0.1, metalness: 0.9 }
            ]
        }
    ];

    // ===================== THREE.JS GLOBALS =====================
    let scene, camera, renderer, clock, animationId;
    let composer, bloomPass, fxaaPass;
    let toonGradientMap;
    let characterGroup, characterTargetRotation = 0;
    let characterMixer, walkAction, idleAction;
    let instrumentMeshes = [];
    let collisionBoxes = [];
    let particleSystem;

    // Camera system
    let cameraOffset, cameraLookOffset, currentCamPos, currentLookAt;
    let cameraRig;

    // Performance monitoring
    let lastFrameTime = performance.now();
    let fps = 60;
    let frameCount = 0;

    // ===================== KEYBOARD & MOUSE STATE =====================
    const pressedKeys = new Set();
    const mouse = { x: 0, y: 0, normalizedX: 0, normalizedY: 0 };

    document.addEventListener('keydown', e => {
        pressedKeys.add(e.code);
        if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') {
            LabStore.setCharacterState('running');
        }
    });

    document.addEventListener('keyup', e => {
        pressedKeys.delete(e.code);
        if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') {
            const isMoving = pressedKeys.has('KeyW') || pressedKeys.has('KeyS') ||
                pressedKeys.has('KeyA') || pressedKeys.has('KeyD');
            LabStore.setCharacterState(isMoving ? 'walking' : 'idle');
        }
    });

    document.addEventListener('mousemove', e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        mouse.normalizedX = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.normalizedY = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    // ===================== ADVANCED TOON SHADER MATERIALS =====================
    function createToonGradientMap() {
        const width = 5;
        const data = new Uint8Array(width * 4);

        // Multi-level toon shading
        const levels = [
            [80, 80, 90],      // Deep shadow
            [140, 140, 155],   // Shadow
            [200, 200, 215],   // Mid-tone
            [235, 235, 245],   // Highlight
            [255, 255, 255]    // Bright highlight
        ];

        levels.forEach((rgb, i) => {
            data[i * 4] = rgb[0];
            data[i * 4 + 1] = rgb[1];
            data[i * 4 + 2] = rgb[2];
            data[i * 4 + 3] = 255;
        });

        const tex = new THREE.DataTexture(data, width, 1, THREE.RGBAFormat);
        tex.minFilter = THREE.NearestFilter;
        tex.magFilter = THREE.NearestFilter;
        tex.needsUpdate = true;
        return tex;
    }

    function makeToonMaterial(config) {
        const baseConfig = {
            color: new THREE.Color(config.color || '#FFFFFF'),
            gradientMap: toonGradientMap,
            roughness: config.roughness !== undefined ? config.roughness : 0.8,
            metalness: config.metalness !== undefined ? config.metalness : 0.2,
            transparent: config.transparent || false,
            opacity: config.opacity !== undefined ? config.opacity : 1,
            emissive: config.emissive ? new THREE.Color(config.emissive) : new THREE.Color(0x000000),
            emissiveIntensity: config.emissiveIntensity || 0
        };

        // Use Standard material with toon shading for better PBR
        return new THREE.MeshStandardMaterial(baseConfig);
    }

    // ===================== ENHANCED OUTLINE SYSTEM =====================
    function addOutline(mesh, color = '#2D2D2D', thickness = CONFIG.interaction.outlineThickness) {
        const geo = mesh.geometry.clone();
        const mat = new THREE.MeshBasicMaterial({
            color: new THREE.Color(color),
            side: THREE.BackSide,
            transparent: true,
            opacity: 0.8
        });
        const outline = new THREE.Mesh(geo, mat);
        outline.scale.multiplyScalar(1 + thickness);
        outline.position.copy(mesh.position);
        outline.rotation.copy(mesh.rotation);
        outline.renderOrder = -1;
        outline.userData.isOutline = true;
        return outline;
    }

    // ===================== PARTICLE SYSTEM =====================
    function createParticleSystem() {
        const particleCount = 100;
        const positions = new Float32Array(particleCount * 3);
        const velocities = new Float32Array(particleCount * 3);

        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 18;
            positions[i * 3 + 1] = Math.random() * 4;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 16;

            velocities[i * 3] = (Math.random() - 0.5) * 0.02;
            velocities[i * 3 + 1] = Math.random() * 0.01 + 0.005;
            velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.02;
        }

        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));

        const material = new THREE.PointsMaterial({
            color: 0xE8DFF5,
            size: 0.05,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending
        });

        const particles = new THREE.Points(geometry, material);
        particles.userData.velocities = velocities;
        scene.add(particles);
        return particles;
    }

    function updateParticles(delta) {
        if (!particleSystem) return;

        const positions = particleSystem.geometry.attributes.position.array;
        const velocities = particleSystem.userData.velocities;

        for (let i = 0; i < positions.length; i += 3) {
            positions[i] += velocities[i];
            positions[i + 1] += velocities[i + 1];
            positions[i + 2] += velocities[i + 2];

            // Reset particles that go too high
            if (positions[i + 1] > 4) {
                positions[i + 1] = 0;
                positions[i] = (Math.random() - 0.5) * 18;
                positions[i + 2] = (Math.random() - 0.5) * 16;
            }
        }

        particleSystem.geometry.attributes.position.needsUpdate = true;
    }

    // ===================== ADVANCED LAB ENVIRONMENT =====================
    function createLabRoom() {
        const W = 18, D = 16, H = 4.5;

        // Enhanced floor with normal map simulation
        const floorGeo = new THREE.PlaneGeometry(W, D, 50, 50);
        const floorMat = new THREE.MeshStandardMaterial({
            color: '#E8E0F0',
            roughness: 0.8,
            metalness: 0.1
        });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        scene.add(floor);

        // Advanced grid system
        const gridHelper = new THREE.GridHelper(W, 36, '#C8B8D8', '#E0D8EC');
        gridHelper.position.y = 0.01;
        gridHelper.material.opacity = 0.25;
        gridHelper.material.transparent = true;
        scene.add(gridHelper);

        // Ceiling with recessed lighting
        const ceilGeo = new THREE.PlaneGeometry(W, D);
        const ceilMat = makeToonMaterial({ color: '#F5F0FA', roughness: 0.9 });
        const ceil = new THREE.Mesh(ceilGeo, ceilMat);
        ceil.rotation.x = Math.PI / 2;
        ceil.position.y = H;
        ceil.receiveShadow = true;
        scene.add(ceil);

        // Enhanced walls with panels
        createWallSection(0, H / 2, -D / 2, W, H, 0.2, 0, '#E0D8EC');
        createWallSection(-W / 2, H / 2, 0, D, H, 0.2, Math.PI / 2, '#D8D0E4');
        createWallSection(W / 2, H / 2, 0, D, H, 0.2, -Math.PI / 2, '#D8D0E4');

        // Front wall with modern door
        createDoorway(0, D / 2);

        // Decorative elements
        createCeilingLights(W, D, H);
        createWallPanels();
        createLabSignage();
    }

    function createWallSection(x, y, z, width, height, depth, rotY, color) {
        const wall = new THREE.Mesh(
            new THREE.BoxGeometry(width, height, depth),
            makeToonMaterial({ color, roughness: 0.85, metalness: 0.05 })
        );
        wall.position.set(x, y, z);
        wall.rotation.y = rotY;
        wall.receiveShadow = true;
        wall.castShadow = true;
        scene.add(wall);

        // Add collision box
        const box = new THREE.Box3().setFromObject(wall);
        box.expandByScalar(0.3);
        collisionBoxes.push(box);
    }

    function createDoorway(x, z) {
        const doorWidth = 2.2, doorHeight = 2.6;

        // Door frame
        const frameMat = makeToonMaterial({ color: '#B8A8C8', roughness: 0.3, metalness: 0.6 });

        // Left frame
        const leftFrame = new THREE.Mesh(new THREE.BoxGeometry(0.12, doorHeight, 0.12), frameMat);
        leftFrame.position.set(x - doorWidth / 2, doorHeight / 2, z);
        scene.add(leftFrame);

        // Right frame
        const rightFrame = new THREE.Mesh(new THREE.BoxGeometry(0.12, doorHeight, 0.12), frameMat);
        rightFrame.position.set(x + doorWidth / 2, doorHeight / 2, z);
        scene.add(rightFrame);

        // Top frame
        const topFrame = new THREE.Mesh(new THREE.BoxGeometry(doorWidth + 0.24, 0.12, 0.12), frameMat);
        topFrame.position.set(x, doorHeight, z);
        scene.add(topFrame);

        // Glass door
        const doorGlass = new THREE.Mesh(
            new THREE.BoxGeometry(doorWidth, doorHeight, 0.05),
            new THREE.MeshPhysicalMaterial({
                color: '#B8D8E8',
                transparent: true,
                opacity: 0.3,
                roughness: 0.1,
                metalness: 0.9,
                transmission: 0.9,
                thickness: 0.5
            })
        );
        doorGlass.position.set(x, doorHeight / 2, z);
        scene.add(doorGlass);
    }

    function createCeilingLights(W, D, H) {
        const lightPositions = [
            [-5, -3], [-5, 3], [0, -3], [0, 3], [5, -3], [5, 3]
        ];

        lightPositions.forEach(([x, z]) => {
            const lightBox = new THREE.Mesh(
                new THREE.BoxGeometry(2.5, 0.08, 0.5),
                new THREE.MeshBasicMaterial({
                    color: '#FFFEF0',
                    emissive: '#FFFEF0',
                    emissiveIntensity: 1
                })
            );
            lightBox.position.set(x, H - 0.04, z);
            scene.add(lightBox);

            // Add point light for each fixture
            const pointLight = new THREE.PointLight('#FFFEF0', 0.4, 8);
            pointLight.position.set(x, H - 0.2, z);
            pointLight.castShadow = true;
            pointLight.shadow.mapSize.width = 512;
            pointLight.shadow.mapSize.height = 512;
            scene.add(pointLight);
        });
    }

    function createWallPanels() {
        const panelMat = makeToonMaterial({ color: '#F8BBD0', roughness: 0.4, metalness: 0.3 });

        for (let i = 0; i < 3; i++) {
            const panel = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.03, 1.0), panelMat);
            panel.position.set(-8 + i * 1.8, 2, -7.9);
            scene.add(panel);
        }
    }

    function createLabSignage() {
        const signGeo = new THREE.BoxGeometry(1.2, 0.4, 0.08);
        const signMat = makeToonMaterial({
            color: '#F8BBD0',
            emissive: '#F8BBD0',
            emissiveIntensity: 0.2
        });
        const sign = new THREE.Mesh(signGeo, signMat);
        sign.position.set(0, 3.8, 7.9);
        scene.add(sign);

        // Add "Virtual Lab" text using sprites
        createTextSprite('VIRTUAL LAB', 0, 3.8, 7.85);
    }

    function createTextSprite(text, x, y, z) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 512;
        canvas.height = 128;

        ctx.fillStyle = '#4A3B6B';
        ctx.font = 'bold 48px "Plus Jakarta Sans", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(text, 256, 64);

        const texture = new THREE.CanvasTexture(canvas);
        const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Sprite(spriteMat);
        sprite.scale.set(1.0, 0.25, 1);
        sprite.position.set(x, y, z);
        scene.add(sprite);
    }

    // ===================== ENHANCED BENCH SYSTEM =====================
    function createBench(x, z, width, depth) {
        const group = new THREE.Group();

        // Top surface with edge detail
        const topGeo = new THREE.BoxGeometry(width, 0.08, depth);
        const top = new THREE.Mesh(topGeo, makeToonMaterial({
            color: '#F5E6CC',
            roughness: 0.6,
            metalness: 0.3
        }));
        top.position.y = 0.92;
        top.castShadow = true;
        top.receiveShadow = true;
        group.add(top);

        // Edge trim
        const edgeTrim = new THREE.Mesh(
            new THREE.BoxGeometry(width + 0.02, 0.04, depth + 0.02),
            makeToonMaterial({ color: '#E8D8B8', roughness: 0.5, metalness: 0.4 })
        );
        edgeTrim.position.y = 0.96;
        group.add(edgeTrim);

        // Modern legs
        const legMat = makeToonMaterial({ color: '#B8D8E8', roughness: 0.3, metalness: 0.7 });
        const legHeight = 0.88;
        const legPositions = [
            [-width / 2 + 0.15, -depth / 2 + 0.15],
            [width / 2 - 0.15, -depth / 2 + 0.15],
            [-width / 2 + 0.15, depth / 2 - 0.15],
            [width / 2 - 0.15, depth / 2 - 0.15]
        ];

        legPositions.forEach(([ox, oz]) => {
            const leg = new THREE.Mesh(
                new THREE.CylinderGeometry(0.05, 0.05, legHeight, 12),
                legMat
            );
            leg.position.set(ox, legHeight / 2, oz);
            leg.castShadow = true;
            group.add(leg);

            // Leg caps
            const cap = new THREE.Mesh(
                new THREE.CylinderGeometry(0.06, 0.06, 0.02, 12),
                legMat
            );
            cap.position.set(ox, legHeight, oz);
            group.add(cap);
        });

        // Storage shelf
        const shelf = new THREE.Mesh(
            new THREE.BoxGeometry(width - 0.2, 0.04, depth - 0.2),
            makeToonMaterial({ color: '#E8DFF5', roughness: 0.7 })
        );
        shelf.position.y = 0.4;
        shelf.castShadow = true;
        shelf.receiveShadow = true;
        group.add(shelf);

        // Cable management
        const cableChannel = new THREE.Mesh(
            new THREE.BoxGeometry(width - 0.3, 0.08, 0.1),
            makeToonMaterial({ color: '#9B8BB8', roughness: 0.8 })
        );
        cableChannel.position.set(0, 0.88, -depth / 2 + 0.05);
        group.add(cableChannel);

        group.position.set(x, 0, z);
        scene.add(group);

        // Collision
        const benchBox = new THREE.Box3(
            new THREE.Vector3(x - width / 2 - 0.3, 0, z - depth / 2 - 0.3),
            new THREE.Vector3(x + width / 2 + 0.3, 1.2, z + depth / 2 + 0.3)
        );
        collisionBoxes.push(benchBox);
    }

    // ===================== ADVANCED CHARACTER (With Animation) =====================
    function createCharacter() {
        characterGroup = new THREE.Group();

        // Body with better proportions
        const bodyGeo = new THREE.CapsuleGeometry(0.28, 0.7, 12, 24);
        const body = new THREE.Mesh(bodyGeo, makeToonMaterial({
            color: '#B8D8E8',
            roughness: 0.7,
            metalness: 0.2
        }));
        body.position.y = 0.85;
        body.castShadow = true;
        characterGroup.add(body);
        characterGroup.add(addOutline(body, '#2D2D2D', 0.045));

        // Head with better shape
        const headGeo = new THREE.SphereGeometry(0.24, 24, 24);
        const head = new THREE.Mesh(headGeo, makeToonMaterial({
            color: '#F5E6CC',
            roughness: 0.8
        }));
        head.position.y = 1.42;
        head.castShadow = true;
        characterGroup.add(head);
        characterGroup.add(addOutline(head, '#2D2D2D', 0.045));

        // Hair with style
        const hairGeo = new THREE.SphereGeometry(0.26, 24, 24, 0, Math.PI * 2, 0, Math.PI * 0.6);
        const hair = new THREE.Mesh(hairGeo, makeToonMaterial({
            color: '#E8DFF5',
            roughness: 0.9
        }));
        hair.position.y = 1.45;
        characterGroup.add(hair);

        // Anime-style eyes
        createCharacterEyes();

        // Lab coat with details
        createLabCoat();

        // Legs with shoes
        createCharacterLegs();

        // Arms
        createCharacterArms();

        characterGroup.position.set(0, 0, 6);
        characterGroup.castShadow = true;
        scene.add(characterGroup);

        // Simple bob animation
        characterGroup.userData.bobPhase = 0;
    }

    function createCharacterEyes() {
        const eyeGeo = new THREE.SphereGeometry(0.035, 12, 12);
        const eyeMat = new THREE.MeshBasicMaterial({ color: '#2D2D2D' });

        const leftEye = new THREE.Mesh(eyeGeo, eyeMat);
        leftEye.position.set(-0.09, 1.44, 0.21);
        characterGroup.add(leftEye);

        const rightEye = new THREE.Mesh(eyeGeo, eyeMat);
        rightEye.position.set(0.09, 1.44, 0.21);
        characterGroup.add(rightEye);

        // Eye highlights
        const highlightGeo = new THREE.SphereGeometry(0.015, 8, 8);
        const highlightMat = new THREE.MeshBasicMaterial({ color: '#FFFFFF' });

        const leftHighlight = new THREE.Mesh(highlightGeo, highlightMat);
        leftHighlight.position.set(-0.08, 1.46, 0.23);
        characterGroup.add(leftHighlight);

        const rightHighlight = new THREE.Mesh(highlightGeo, highlightMat);
        rightHighlight.position.set(0.10, 1.46, 0.23);
        characterGroup.add(rightHighlight);
    }

    function createLabCoat() {
        const coatGeo = new THREE.BoxGeometry(0.58, 0.5, 0.32);
        const coat = new THREE.Mesh(coatGeo, makeToonMaterial({
            color: '#FFFFFF',
            roughness: 0.85
        }));
        coat.position.y = 0.45;
        coat.castShadow = true;
        characterGroup.add(coat);
        characterGroup.add(addOutline(coat, '#2D2D2D', 0.04));

        // Coat buttons
        for (let i = 0; i < 3; i++) {
            const button = new THREE.Mesh(
                new THREE.SphereGeometry(0.02, 8, 8),
                new THREE.MeshBasicMaterial({ color: '#B8D8E8' })
            );
            button.position.set(0, 0.6 - i * 0.15, 0.17);
            characterGroup.add(button);
        }

        // Collar
        const collarGeo = new THREE.BoxGeometry(0.6, 0.1, 0.05);
        const collar = new THREE.Mesh(collarGeo, makeToonMaterial({ color: '#F0F0F0' }));
        collar.position.set(0, 1.15, 0.15);
        characterGroup.add(collar);
    }

    function createCharacterLegs() {
        const legGeo = new THREE.CylinderGeometry(0.07, 0.07, 0.4, 12);
        const legMat = makeToonMaterial({ color: '#C8E6C9', roughness: 0.8 });

        const leftLeg = new THREE.Mesh(legGeo, legMat);
        leftLeg.position.set(-0.12, 0.2, 0);
        leftLeg.castShadow = true;
        characterGroup.add(leftLeg);
        characterGroup.userData.leftLeg = leftLeg;

        const rightLeg = new THREE.Mesh(legGeo, legMat);
        rightLeg.position.set(0.12, 0.2, 0);
        rightLeg.castShadow = true;
        characterGroup.add(rightLeg);
        characterGroup.userData.rightLeg = rightLeg;

        // Shoes
        const shoeGeo = new THREE.BoxGeometry(0.12, 0.05, 0.18);
        const shoeMat = makeToonMaterial({ color: '#64748B', roughness: 0.5, metalness: 0.3 });

        const leftShoe = new THREE.Mesh(shoeGeo, shoeMat);
        leftShoe.position.set(-0.12, 0.025, 0.03);
        leftShoe.castShadow = true;
        characterGroup.add(leftShoe);

        const rightShoe = new THREE.Mesh(shoeGeo, shoeMat);
        rightShoe.position.set(0.12, 0.025, 0.03);
        rightShoe.castShadow = true;
        characterGroup.add(rightShoe);
    }

    function createCharacterArms() {
        const armGeo = new THREE.CapsuleGeometry(0.05, 0.35, 8, 16);
        const armMat = makeToonMaterial({ color: '#FFFFFF', roughness: 0.85 });

        const leftArm = new THREE.Mesh(armGeo, armMat);
        leftArm.position.set(-0.35, 0.8, 0);
        leftArm.rotation.z = 0.3;
        leftArm.castShadow = true;
        characterGroup.add(leftArm);
        characterGroup.userData.leftArm = leftArm;

        const rightArm = new THREE.Mesh(armGeo, armMat);
        rightArm.position.set(0.35, 0.8, 0);
        rightArm.rotation.z = -0.3;
        rightArm.castShadow = true;
        characterGroup.add(rightArm);
        characterGroup.userData.rightArm = rightArm;
    }

    function updateCharacterAnimation(delta) {
        if (!characterGroup) return;

        const state = LabStore.characterState;
        const phase = characterGroup.userData.bobPhase || 0;

        if (state === 'walking' || state === 'running') {
            // Walking/running animation
            const speed = state === 'running' ? 8 : 5;
            const armSwing = state === 'running' ? 0.6 : 0.4;
            const legSwing = state === 'running' ? 0.5 : 0.3;

            characterGroup.userData.bobPhase = phase + delta * speed;
            const bob = Math.sin(characterGroup.userData.bobPhase);

            // Bob up and down
            characterGroup.position.y = Math.abs(bob) * 0.05;

            // Swing arms
            if (characterGroup.userData.leftArm) {
                characterGroup.userData.leftArm.rotation.x = bob * armSwing;
                characterGroup.userData.rightArm.rotation.x = -bob * armSwing;
            }

            // Swing legs
            if (characterGroup.userData.leftLeg) {
                characterGroup.userData.leftLeg.rotation.x = bob * legSwing;
                characterGroup.userData.rightLeg.rotation.x = -bob * legSwing;
            }
        } else {
            // Idle breathing animation
            characterGroup.userData.bobPhase = phase + delta * 1.5;
            const breathe = Math.sin(characterGroup.userData.bobPhase);
            characterGroup.position.y = breathe * 0.01;
        }
    }

    // ===================== ENHANCED INSTRUMENTS =====================
    function createInstrumentMesh(instrData) {
        const group = new THREE.Group();
        const benchY = 0.96;

        // Animated glow ring
        const ringGeo = new THREE.RingGeometry(0.55, 0.75, 48);
        const ringMat = new THREE.MeshBasicMaterial({
            color: new THREE.Color(instrData.glowColor),
            transparent: true,
            opacity: 0,
            side: THREE.DoubleSide,
            blending: THREE.AdditiveBlending
        });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.rotation.x = -Math.PI / 2;
        ring.position.y = 0.01;
        ring.userData.baseOpacity = 0.25;
        group.add(ring);
        group.userData.glowRing = ring;

        // Platform disc with metallic finish
        const disc = new THREE.Mesh(
            new THREE.CylinderGeometry(0.52, 0.52, 0.06, 48),
            makeToonMaterial({
                color: instrData.color,
                roughness: 0.3,
                metalness: 0.7
            })
        );
        disc.position.y = 0.03;
        disc.castShadow = true;
        disc.receiveShadow = true;
        group.add(disc);

        // Parts with enhanced materials
        const outlineMeshes = [];
        instrData.parts.forEach((part, idx) => {
            let geo;
            if (part.type === 'box') {
                geo = new THREE.BoxGeometry(...part.size);
            } else if (part.type === 'cylinder') {
                geo = new THREE.CylinderGeometry(...part.args);
            } else if (part.type === 'sphere') {
                geo = new THREE.SphereGeometry(...part.args);
            }

            const mesh = new THREE.Mesh(geo, makeToonMaterial(part));
            mesh.position.set(...part.pos);
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            group.add(mesh);

            const outline = addOutline(mesh, instrData.outlineColor, 0.03);
            group.add(outline);
            outlineMeshes.push(outline);
        });

        group.position.set(instrData.benchPos[0], benchY + instrData.benchPos[1], instrData.benchPos[2]);
        group.userData = {
            baseY: benchY + instrData.benchPos[1],
            floatOffset: Math.random() * Math.PI * 2,
            instrId: instrData.id,
            rotationSpeed: 0.001 + Math.random() * 0.001
        };
        scene.add(group);

        const box = new THREE.Box3().setFromObject(group);
        instrumentMeshes.push({ group, data: instrData, boundingBox: box, outlineMeshes });
    }

    // ===================== ADVANCED HOVER & INTERACTION =====================
    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    let currentHoverEntry = null;

    function onPointerMove(event) {
        if (LabStore.cameraMode !== 'follow') return;
        const rect = renderer.domElement.getBoundingClientRect();
        pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    }

    function updateHover() {
        if (LabStore.cameraMode !== 'follow') return;
        raycaster.setFromCamera(pointer, camera);

        let closest = null;
        let closestDist = Infinity;

        for (const entry of instrumentMeshes) {
            const hit = new THREE.Vector3();
            if (raycaster.ray.intersectBox(entry.boundingBox, hit)) {
                const d = camera.position.distanceTo(hit);
                if (d < closestDist && d < CONFIG.interaction.hoverDistance) {
                    closestDist = d;
                    closest = entry;
                }
            }
        }

        if (closest !== currentHoverEntry) {
            // Unhover previous
            if (currentHoverEntry) {
                gsap.to(currentHoverEntry.group.scale, {
                    x: 1, y: 1, z: 1,
                    duration: 0.3,
                    ease: 'back.out(1.2)'
                });
                currentHoverEntry.outlineMeshes.forEach(m => {
                    gsap.to(m.material.color, {
                        r: new THREE.Color(currentHoverEntry.data.outlineColor).r,
                        g: new THREE.Color(currentHoverEntry.data.outlineColor).g,
                        b: new THREE.Color(currentHoverEntry.data.outlineColor).b,
                        duration: 0.3
                    });
                });
                if (currentHoverEntry.group.userData.glowRing) {
                    gsap.to(currentHoverEntry.group.userData.glowRing.material, {
                        opacity: 0,
                        duration: 0.3
                    });
                }
                LabStore.setHovered(null);
            }

            currentHoverEntry = closest;

            // Hover new
            if (currentHoverEntry) {
                gsap.to(currentHoverEntry.group.scale, {
                    x: 1.06, y: 1.06, z: 1.06,
                    duration: 0.3,
                    ease: 'back.out(1.7)'
                });
                currentHoverEntry.outlineMeshes.forEach(m => {
                    gsap.to(m.material.color, {
                        r: 1, g: 0.84, b: 0,
                        duration: 0.3
                    });
                });
                if (currentHoverEntry.group.userData.glowRing) {
                    gsap.to(currentHoverEntry.group.userData.glowRing.material, {
                        opacity: currentHoverEntry.group.userData.glowRing.userData.baseOpacity,
                        duration: 0.3
                    });
                }
                LabStore.setHovered(currentHoverEntry.data.id);

                // Haptic feedback if supported
                if (navigator.vibrate) navigator.vibrate(10);
            }
        }

        updateTooltip();
    }

    function updateTooltip() {
        const tooltip = document.getElementById('vlab-tooltip');
        if (!tooltip) return;

        if (currentHoverEntry && LabStore.cameraMode === 'follow') {
            const d = currentHoverEntry.data;
            tooltip.innerHTML = `
                <span class="vlab-tooltip-icon">${d.icon}</span>
                <span class="vlab-tooltip-name">${d.name}</span>
                <span class="vlab-tooltip-sub">${d.description}</span>
                <span class="vlab-tooltip-hint">Click to interact →</span>
            `;
            tooltip.classList.add('visible');
        } else {
            tooltip.classList.remove('visible');
        }
    }

    function onCanvasClick(event) {
        if (LabStore.cameraMode !== 'follow') return;
        if (currentHoverEntry) {
            LabStore.focusInstrument(currentHoverEntry.data.id);
            cameraTransition(currentHoverEntry.data);

            // Click sound effect (you can add audio here)
            if (navigator.vibrate) navigator.vibrate([10, 20, 10]);
        }
    }

    // ===================== CINEMATIC CAMERA SYSTEM =====================
    function cameraTransition(instrData) {
        LabStore.setCameraMode('transitioning');

        const targetPos = new THREE.Vector3(...instrData.cameraPose.position);
        const targetLookAt = new THREE.Vector3(...instrData.cameraPose.lookAt);
        const targetFov = instrData.cameraPose.fov || CONFIG.camera.fov;

        // Animate camera with cinematic easing
        gsap.to(camera.position, {
            x: targetPos.x,
            y: targetPos.y,
            z: targetPos.z,
            duration: CONFIG.camera.transitionDuration,
            ease: 'power2.inOut',
            onUpdate: () => {
                currentLookAt.lerp(targetLookAt, 0.06);
                camera.lookAt(currentLookAt);
            },
            onComplete: () => {
                currentLookAt.copy(targetLookAt);
                camera.lookAt(currentLookAt);
                LabStore.setCameraMode('instrument');
                showInstrumentHUD(instrData);
            }
        });

        gsap.to(camera, {
            fov: targetFov,
            duration: CONFIG.camera.transitionDuration,
            ease: 'power2.inOut',
            onUpdate: () => camera.updateProjectionMatrix()
        });
    }

    function cameraReturnToFollow() {
        LabStore.setCameraMode('transitioning');
        hideInstrumentHUD();

        const charPos = characterGroup.position.clone();
        const targetPos = charPos.clone().add(cameraOffset);
        const targetLookAt = charPos.clone().add(cameraLookOffset);

        gsap.to(camera.position, {
            x: targetPos.x,
            y: targetPos.y,
            z: targetPos.z,
            duration: CONFIG.camera.transitionDuration,
            ease: 'power2.inOut',
            onUpdate: () => {
                currentLookAt.lerp(targetLookAt, 0.06);
                camera.lookAt(currentLookAt);
            },
            onComplete: () => {
                currentLookAt.copy(targetLookAt);
                LabStore.setCameraMode('follow');
                LabStore.enableMovement();
            }
        });

        gsap.to(camera, {
            fov: CONFIG.camera.fov,
            duration: CONFIG.camera.transitionDuration,
            ease: 'power2.inOut',
            onUpdate: () => camera.updateProjectionMatrix()
        });
    }

    // ===================== ADVANCED INSTRUMENT HUD =====================
    function showInstrumentHUD(instrData) {
        const hud = document.getElementById('vlab-instrument-hud');
        if (!hud) return;

        const paramsHTML = instrData.ui.params.map((p, idx) => `
            <div class="hud-param" data-param-index="${idx}">
                <label>
                    ${p.icon ? `<i>${p.icon}</i>` : ''}
                    ${p.name}
                </label>
                <input 
                    type="range" 
                    min="${p.min}" 
                    max="${p.max}" 
                    value="${p.default}" 
                    step="${(p.max - p.min) / 100}"
                    class="hud-slider" 
                    data-unit="${p.unit}"
                    ${p.options ? `data-options='${JSON.stringify(p.options)}'` : ''}
                >
                <span class="hud-value">${p.default}${p.unit}</span>
            </div>
        `).join('');

        hud.innerHTML = `
            <div class="hud-panel animate-in">
                <div class="hud-header">
                    <span class="hud-icon">${instrData.ui.icon}</span>
                    <div class="hud-title-wrapper">
                        <h2 class="hud-title">${instrData.name}</h2>
                        <p class="hud-subtitle">${instrData.fullName}</p>
                    </div>
                </div>
                <div class="hud-params">
                    ${paramsHTML}
                </div>
                <div class="hud-actions">
                    <button class="hud-btn hud-btn-run" id="hud-run-btn">
                        <i class="fas fa-play"></i> Run Analysis
                    </button>
                    <button class="hud-btn hud-btn-sim" id="hud-sim-btn">
                        <i class="fas fa-flask"></i> Open Full Simulator
                    </button>
                    <button class="hud-btn hud-btn-back" id="hud-back-btn">
                        <i class="fas fa-arrow-left"></i> Back to Lab
                    </button>
                </div>
            </div>
        `;

        hud.classList.add('active');

        // Enhanced slider interactivity
        hud.querySelectorAll('.hud-slider').forEach((slider, idx) => {
            const param = instrData.ui.params[idx];

            slider.addEventListener('input', e => {
                let displayValue = parseFloat(e.target.value);

                if (param.options) {
                    const options = JSON.parse(e.target.dataset.options);
                    const index = Math.round(displayValue);
                    e.target.nextElementSibling.textContent = options[index];
                } else {
                    displayValue = displayValue.toFixed(1);
                    e.target.nextElementSibling.textContent = `${displayValue}${param.unit}`;
                }
            });

            // Add haptic feedback
            slider.addEventListener('change', () => {
                if (navigator.vibrate) navigator.vibrate(5);
            });
        });

        // Button handlers
        document.getElementById('hud-run-btn')?.addEventListener('click', () => {
            console.log(`[Virtual Lab] Running analysis on ${instrData.name}`);
            const btn = document.getElementById('hud-run-btn');
            if (btn) {
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
                btn.disabled = true;

                setTimeout(() => {
                    btn.innerHTML = '<i class="fas fa-check"></i> Analysis Complete!';
                    setTimeout(() => {
                        btn.innerHTML = '<i class="fas fa-play"></i> Run Analysis';
                        btn.disabled = false;
                    }, 2000);
                }, 3000);
            }
        });

        document.getElementById('hud-sim-btn')?.addEventListener('click', () => {
            // Transition overlay
            const overlay = document.getElementById('vlab-transition-overlay');
            if (overlay) {
                overlay.classList.add('active');
                setTimeout(() => {
                    window.location.href = instrData.href;
                }, 400);
            } else {
                window.location.href = instrData.href;
            }
        });

        document.getElementById('hud-back-btn')?.addEventListener('click', () => {
            LabStore.exitInstrument();
            cameraReturnToFollow();
        });
    }

    function hideInstrumentHUD() {
        const hud = document.getElementById('vlab-instrument-hud');
        if (hud) {
            const panel = hud.querySelector('.hud-panel');
            if (panel) panel.classList.replace('animate-in', 'animate-out');
            setTimeout(() => {
                hud.classList.remove('active');
            }, 500);
        }
    }

    // ===================== PHYSICS & COLLISION =====================
    function checkCollision(pos) {
        const pBox = new THREE.Box3(
            new THREE.Vector3(pos.x - 0.32, 0, pos.z - 0.32),
            new THREE.Vector3(pos.x + 0.32, 1.8, pos.z + 0.32)
        );

        for (const box of collisionBoxes) {
            if (pBox.intersectsBox(box)) return true;
        }
        return false;
    }

    // ===================== LOADING MANAGEMENT =====================
    function showLoading() {
        const el = document.getElementById('vlab-loading');
        if (el) {
            el.style.display = 'flex';

            // Simulate loading progress
            const progressBar = el.querySelector('.loading-progress-bar');
            if (progressBar) {
                let progress = 0;
                const interval = setInterval(() => {
                    progress += Math.random() * 15;
                    if (progress > 100) progress = 100;
                    progressBar.style.width = progress + '%';
                    if (progress >= 100) clearInterval(interval);
                }, 150);
            }
        }
    }

    function hideLoading() {
        const el = document.getElementById('vlab-loading');
        if (el) {
            setTimeout(() => {
                el.classList.add('hidden');
                setTimeout(() => {
                    el.style.display = 'none';
                }, 600);
            }, 500);
        }
    }

    // ===================== PERFORMANCE MONITOR =====================
    function updatePerformanceStats() {
        const now = performance.now();
        frameCount++;

        if (now >= lastFrameTime + 1000) {
            fps = Math.round((frameCount * 1000) / (now - lastFrameTime));
            frameCount = 0;
            lastFrameTime = now;

            // Update FPS display if exists
            const fpsEl = document.getElementById('vlab-fps');
            if (fpsEl) fpsEl.textContent = `FPS: ${fps}`;
        }
    }

    // ===================== MAIN ANIMATION LOOP =====================
    function animate() {
        animationId = requestAnimationFrame(animate);

        const delta = Math.min(clock.getDelta(), 0.1); // Cap delta to prevent physics issues
        const elapsed = clock.elapsedTime;

        updatePerformanceStats();

        // ---- Character Movement ----
        if (LabStore.isMovementEnabled && LabStore.cameraMode === 'follow' && characterGroup) {
            let speed = CONFIG.movement.speed;
            const isRunning = pressedKeys.has('ShiftLeft') || pressedKeys.has('ShiftRight');
            if (isRunning) speed *= CONFIG.movement.runMultiplier;

            let moveX = 0, moveZ = 0;

            if (pressedKeys.has('KeyW') || pressedKeys.has('ArrowUp')) moveZ = -1;
            if (pressedKeys.has('KeyS') || pressedKeys.has('ArrowDown')) moveZ = 1;
            if (pressedKeys.has('KeyA') || pressedKeys.has('ArrowLeft')) moveX = -1;
            if (pressedKeys.has('KeyD') || pressedKeys.has('ArrowRight')) moveX = 1;

            const isMoving = moveX !== 0 || moveZ !== 0;

            // Update character state
            if (isMoving) {
                LabStore.setCharacterState(isRunning ? 'running' : 'walking');
            } else {
                LabStore.setCharacterState('idle');
            }

            if (isMoving) {
                // Camera-relative movement
                const camForward = new THREE.Vector3();
                camera.getWorldDirection(camForward);
                camForward.y = 0;
                camForward.normalize();

                const camRight = new THREE.Vector3();
                camRight.crossVectors(camForward, new THREE.Vector3(0, 1, 0)).normalize();

                const moveDir = new THREE.Vector3();
                moveDir.addScaledVector(camForward, -moveZ);
                moveDir.addScaledVector(camRight, moveX);
                moveDir.normalize();

                const newPos = characterGroup.position.clone();
                newPos.x += moveDir.x * speed * delta;
                newPos.z += moveDir.z * speed * delta;

                if (!checkCollision(newPos)) {
                    characterGroup.position.copy(newPos);
                } else {
                    // Smooth sliding along walls
                    const slideX = characterGroup.position.clone();
                    slideX.x = newPos.x;
                    if (!checkCollision(slideX)) {
                        characterGroup.position.copy(slideX);
                    } else {
                        const slideZ = characterGroup.position.clone();
                        slideZ.z = newPos.z;
                        if (!checkCollision(slideZ)) {
                            characterGroup.position.copy(slideZ);
                        }
                    }
                }

                // Smooth rotation
                characterTargetRotation = Math.atan2(moveDir.x, moveDir.z);
            }

            // Lerp rotation
            const currentRot = characterGroup.rotation.y;
            const diff = characterTargetRotation - currentRot;
            const wrapped = Math.atan2(Math.sin(diff), Math.cos(diff));
            characterGroup.rotation.y += wrapped * CONFIG.movement.rotationSpeed;
        }

        // Update character animation
        updateCharacterAnimation(delta);

        // ---- Dynamic Camera Follow ----
        if (LabStore.cameraMode === 'follow' && characterGroup) {
            const charPos = characterGroup.position.clone();

            // Look-ahead based on movement
            const lookAhead = new THREE.Vector3();
            if (LabStore.characterState !== 'idle') {
                const forward = new THREE.Vector3(0, 0, -1);
                forward.applyQuaternion(characterGroup.quaternion);
                lookAhead.copy(forward).multiplyScalar(CONFIG.camera.lookAheadDistance);
            }

            const rotatedOffset = cameraOffset.clone().applyAxisAngle(
                new THREE.Vector3(0, 1, 0),
                characterGroup.rotation.y
            );

            const targetCamPos = charPos.clone().add(rotatedOffset);
            const targetCamLook = charPos.clone().add(cameraLookOffset).add(lookAhead);

            currentCamPos.lerp(targetCamPos, CONFIG.camera.smoothness);
            currentLookAt.lerp(targetCamLook, CONFIG.camera.smoothness);

            camera.position.copy(currentCamPos);
            camera.lookAt(currentLookAt);
        }

        // ---- Instrument animations ----
        instrumentMeshes.forEach(entry => {
            const g = entry.group;

            // Floating animation
            if (g.userData.baseY !== undefined) {
                g.position.y = g.userData.baseY + Math.sin(elapsed * 1.5 + g.userData.floatOffset) * 0.04;
            }

            // Subtle rotation
            if (g.userData.rotationSpeed) {
                g.rotation.y += g.userData.rotationSpeed;
            }

            // Pulsing glow
            if (g.userData.glowRing && g.userData.glowRing.material.opacity > 0) {
                const pulse = Math.sin(elapsed * 2) * 0.5 + 0.5;
                const baseOpacity = g.userData.glowRing.userData.baseOpacity || 0.25;
                g.userData.glowRing.material.opacity = baseOpacity * (0.7 + pulse * 0.3);
            }
        });

        // ---- Particle system update ----
        updateParticles(delta);

        // ---- Hover detection ----
        updateHover();

        renderer.render(scene, camera);
    }

    // ===================== INITIALIZATION =====================
    function init() {
        if (typeof THREE === 'undefined') {
            console.error('[Virtual Lab] Three.js not loaded');
            return;
        }

        if (typeof gsap === 'undefined') {
            console.warn('[Virtual Lab] GSAP not loaded, animations may be limited');
        }

        const container = document.getElementById('vlab-container');
        if (!container) {
            console.error('[Virtual Lab] Container element not found');
            return;
        }

        showLoading();

        clock = new THREE.Clock();
        toonGradientMap = createToonGradientMap();

        // Initialize camera vectors
        cameraOffset = new THREE.Vector3(0, CONFIG.camera.followHeight, CONFIG.camera.followDistance);
        cameraLookOffset = new THREE.Vector3(0, 1.6, 0);
        currentCamPos = new THREE.Vector3();
        currentLookAt = new THREE.Vector3();

        // Scene setup
        scene = new THREE.Scene();
        scene.background = new THREE.Color('#F0EBF8');
        scene.fog = new THREE.Fog('#F0EBF8', CONFIG.graphics.fog.near, CONFIG.graphics.fog.far);

        // Camera
        camera = new THREE.PerspectiveCamera(
            CONFIG.camera.fov,
            window.innerWidth / window.innerHeight,
            CONFIG.camera.near,
            CONFIG.camera.far
        );
        camera.position.set(0, 5, 14);

        // Renderer
        const canvas = document.getElementById('vlab-canvas');
        renderer = new THREE.WebGLRenderer({
            canvas,
            antialias: CONFIG.graphics.antialias,
            powerPreference: 'high-performance'
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, CONFIG.graphics.maxPixelRatio));

        if (CONFIG.graphics.shadows) {
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        }

        if (CONFIG.graphics.toneMapping) {
            renderer.toneMapping = THREE.ACESFilmicToneMapping;
            renderer.toneMappingExposure = 1.0;
        }

        renderer.outputColorSpace = THREE.SRGBColorSpace;

        // Lighting system
        const ambient = new THREE.AmbientLight('#E8DFF5', 0.5);
        scene.add(ambient);

        const mainLight = new THREE.DirectionalLight('#FFFEF0', 1.3);
        mainLight.position.set(6, 12, 8);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        mainLight.shadow.camera.near = 0.5;
        mainLight.shadow.camera.far = 50;
        mainLight.shadow.camera.left = -15;
        mainLight.shadow.camera.right = 15;
        mainLight.shadow.camera.top = 15;
        mainLight.shadow.camera.bottom = -15;
        mainLight.shadow.bias = -0.0001;
        scene.add(mainLight);

        const fillLight = new THREE.DirectionalLight('#B8D8E8', 0.4);
        fillLight.position.set(-5, 4, -5);
        scene.add(fillLight);

        const rimLight = new THREE.DirectionalLight('#F8BBD0', 0.3);
        rimLight.position.set(0, 8, -10);
        scene.add(rimLight);

        // Build environment
        console.log('[Virtual Lab] Building environment...');
        createLabRoom();
        createBench(-3, -6, 8, 1.2);
        createBench(4.5, -6, 5, 1.2);
        createBench(0, 0, 9, 1.2);

        // Create character
        console.log('[Virtual Lab] Creating character...');
        createCharacter();

        // Create instruments
        console.log('[Virtual Lab] Creating instruments...');
        INSTRUMENTS.forEach(instr => createInstrumentMesh(instr));

        // Particle system
        particleSystem = createParticleSystem();

        // Initialize camera position
        const charPos = characterGroup.position.clone();
        currentCamPos.copy(charPos.clone().add(cameraOffset));
        currentLookAt.copy(charPos.clone().add(cameraLookOffset));
        camera.position.copy(currentCamPos);
        camera.lookAt(currentLookAt);

        // Event listeners
        canvas.addEventListener('pointermove', onPointerMove, { passive: true });
        canvas.addEventListener('click', onCanvasClick);

        // ESC to exit instrument view
        document.addEventListener('keydown', e => {
            if (e.code === 'Escape' && LabStore.cameraMode === 'instrument') {
                LabStore.exitInstrument();
                cameraReturnToFollow();
            }
        });

        // Responsive resize
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }, { passive: true });

        // Visibility change handling
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                clock.stop();
            } else {
                clock.start();
            }
        });

        console.log('[Virtual Lab] Initialization complete');
        hideLoading();

        // Start animation loop
        animate();

        // Show enter prompt after brief delay
        setTimeout(() => {
            const prompt = document.getElementById('vlab-enter-prompt');
            if (prompt) prompt.classList.remove('hidden');
        }, 800);
    }

    // ===================== AUTO-START =====================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();