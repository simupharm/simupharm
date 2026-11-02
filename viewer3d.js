/* ================================================================
   3D INSTRUMENT VIEWER — Professional Three.js Interactive Models
   Advanced modal-based 3D viewer with enhanced controls & physics
   ================================================================ */
(function () {
    'use strict';

    // Enhanced 3D model definitions with realistic proportions
    const MODELS = {
        hplc: {
            name: 'HPLC System',
            description: 'High-Performance Liquid Chromatography',
            color: 0x2563EB,
            metallic: 0.6,
            roughness: 0.3,
            parts: [
                { type: 'box', size: [2.2, 3.2, 1.6], pos: [0, 0, 0], label: 'Main Unit', color: 0x2563EB, metallic: 0.7 },
                { type: 'cylinder', size: [0.18, 0.18, 2.2], pos: [-0.6, 2.1, 0], label: 'Separation Column', color: 0x1E40AF, metallic: 0.9 },
                { type: 'box', size: [0.9, 0.6, 0.9], pos: [0, 1.9, 0], label: 'UV Detector', color: 0x3B82F6, emissive: 0x1E3A8A },
                { type: 'cylinder', size: [0.35, 0.35, 0.7], pos: [1.3, -0.5, 0], label: 'Mobile Phase Reservoir', color: 0x60A5FA, transparent: true, opacity: 0.6 },
                { type: 'box', size: [2.0, 0.12, 1.4], pos: [0, -1.7, 0], label: 'Support Base', color: 0x1E293B, metallic: 0.8 },
                { type: 'cylinder', size: [0.08, 0.08, 0.5], pos: [0.8, 0.5, 0.6], label: 'Injection Port', color: 0xEF4444 },
                { type: 'box', size: [0.4, 0.3, 0.3], pos: [-1.0, -0.8, 0], label: 'Pump Module', color: 0x475569 }
            ]
        },
        ftir: {
            name: 'FTIR Spectrometer',
            description: 'Fourier Transform Infrared Spectroscopy',
            color: 0x7C3AED,
            metallic: 0.5,
            roughness: 0.4,
            parts: [
                { type: 'box', size: [3.2, 1.6, 2.2], pos: [0, 0, 0], label: 'Optical Bench', color: 0x7C3AED, metallic: 0.6 },
                { type: 'box', size: [0.9, 0.9, 0.9], pos: [-1.6, 1.1, 0], label: 'IR Source (Globar)', color: 0xFF6B35, emissive: 0xFF4500 },
                { type: 'box', size: [0.6, 0.6, 0.6], pos: [0, 1.1, 0], label: 'Michelson Interferometer', color: 0x9333EA, metallic: 0.9 },
                { type: 'cylinder', size: [0.35, 0.35, 0.5], pos: [1.3, 1.1, 0], label: 'MCT Detector', color: 0x06B6D4, emissive: 0x0891B2 },
                { type: 'box', size: [0.7, 0.25, 0.7], pos: [0, 1.3, 0.9], label: 'ATR Sample Stage', color: 0xA855F7, metallic: 0.7 },
                { type: 'sphere', size: [0.15], pos: [-0.4, 0.8, 0.5], label: 'Parabolic Mirror', color: 0xE0E7FF, metallic: 1.0, roughness: 0.1 },
                { type: 'box', size: [0.5, 0.4, 0.4], pos: [1.5, -0.5, 0], label: 'Electronics', color: 0x1E293B }
            ]
        },
        gc: {
            name: 'Gas Chromatograph',
            description: 'Gas Chromatography System',
            color: 0xF59E0B,
            metallic: 0.55,
            roughness: 0.35,
            parts: [
                { type: 'box', size: [2.8, 2.8, 2.2], pos: [0, 0, 0], label: 'Temperature-Controlled Oven', color: 0xF59E0B, metallic: 0.5 },
                { type: 'torus', size: [0.5, 0.08, 16, 32], pos: [0, 0, 0], label: 'Capillary Column (coiled)', color: 0xFBBF24, metallic: 0.8 },
                { type: 'box', size: [0.6, 0.6, 0.6], pos: [0, 1.8, 0], label: 'Split/Splitless Injector', color: 0xDC2626, emissive: 0x991B1B },
                { type: 'box', size: [0.7, 0.5, 0.7], pos: [1.4, 1.5, 0], label: 'FID Detector', color: 0x10B981, emissive: 0x059669 },
                { type: 'cylinder', size: [0.45, 0.45, 1.7], pos: [2.2, -0.3, 0], label: 'Carrier Gas (He)', color: 0x6B7280, metallic: 0.9 },
                { type: 'box', size: [0.4, 0.3, 0.4], pos: [-1.4, 1.6, 0], label: 'Pressure Regulator', color: 0x374151 },
                { type: 'cylinder', size: [0.05, 0.05, 0.8], pos: [0, 0.2, 0.8], label: 'Heating Element', color: 0xFF6347, emissive: 0xFF4500 }
            ]
        },
        'uv-vis': {
            name: 'UV-Vis Spectrophotometer',
            description: 'Ultraviolet-Visible Spectroscopy',
            color: 0x06B6D4,
            metallic: 0.6,
            roughness: 0.3,
            parts: [
                { type: 'box', size: [3.5, 1.1, 1.7], pos: [0, 0, 0], label: 'Optical Pathway', color: 0x06B6D4, metallic: 0.6 },
                { type: 'sphere', size: [0.25], pos: [-1.4, 0.7, 0], label: 'Deuterium Lamp', color: 0xA5F3FC, emissive: 0x67E8F9 },
                { type: 'box', size: [0.5, 0.7, 0.5], pos: [0, 0.7, 0], label: 'Cuvette Chamber', color: 0x0891B2, transparent: true, opacity: 0.5 },
                { type: 'cylinder', size: [0.25, 0.25, 0.4], pos: [1.4, 0.7, 0], label: 'Photomultiplier Tube', color: 0x164E63, metallic: 0.8 },
                { type: 'box', size: [1.8, 0.6, 1.2], pos: [0, 1.4, 0], label: 'LCD Display', color: 0x1E293B, emissive: 0x3B82F6 },
                { type: 'box', size: [0.3, 0.3, 0.2], pos: [-0.6, 0.5, 0], label: 'Monochromator Grating', color: 0xE0F2FE, metallic: 1.0 },
                { type: 'box', size: [0.25, 0.1, 0.25], pos: [0, -0.3, 0.6], label: 'Sample Holder', color: 0x22D3EE }
            ]
        }
    };

    let viewerOpen = false;
    let renderer, scene, camera, controls, animationId, composer;
    let modelGroup, labelSprites = [];

    // Performance monitor
    const stats = { fps: 0, lastTime: performance.now(), frames: 0 };

    function createViewer() {
        const overlay = document.createElement('div');
        overlay.id = 'viewer3d-overlay';
        overlay.className = 'viewer3d-overlay';

        const modal = document.createElement('div');
        modal.className = 'viewer3d-modal';

        modal.innerHTML = `
            <div class="viewer3d-header">
                <div class="viewer3d-title-section">
                    <div class="viewer3d-icon-wrapper">
                        <i class="fas fa-cube"></i>
                    </div>
                    <div>
                        <h3 id="viewer3d-title">3D Model Viewer</h3>
                        <p id="viewer3d-subtitle">Interactive Instrument Visualization</p>
                    </div>
                </div>
                <div class="viewer3d-controls-header">
                    <button id="viewer3d-reset" class="viewer3d-icon-btn" title="Reset View">
                        <i class="fas fa-undo"></i>
                    </button>
                    <button id="viewer3d-fullscreen" class="viewer3d-icon-btn" title="Toggle Fullscreen">
                        <i class="fas fa-expand"></i>
                    </button>
                    <button id="viewer3d-close" class="viewer3d-icon-btn" aria-label="Close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div id="viewer3d-container" class="viewer3d-container">
                <canvas id="viewer3d-canvas"></canvas>
                <div id="viewer3d-loading" class="viewer3d-loading">
                    <div class="viewer3d-spinner"></div>
                    <p>Loading 3D Model...</p>
                </div>
                <div id="viewer3d-fps" class="viewer3d-fps">FPS: --</div>
                <div class="viewer3d-overlay-controls">
                    <div class="control-group">
                        <label><i class="fas fa-adjust"></i> Exposure</label>
                        <input type="range" id="exposure-slider" min="0" max="2" step="0.1" value="1">
                    </div>
                    <div class="control-group">
                        <label><i class="fas fa-sun"></i> Brightness</label>
                        <input type="range" id="brightness-slider" min="0.3" max="2" step="0.1" value="1">
                    </div>
                    <div class="control-group">
                        <button id="toggle-wireframe" class="toggle-btn">
                            <i class="fas fa-border-all"></i> Wireframe
                        </button>
                        <button id="toggle-labels" class="toggle-btn active">
                            <i class="fas fa-tags"></i> Labels
                        </button>
                    </div>
                </div>
            </div>
            <div id="viewer3d-labels" class="viewer3d-labels"></div>
            <div class="viewer3d-footer">
                <div class="viewer3d-instructions">
                    <span><i class="fas fa-mouse"></i> <strong>Left Drag:</strong> Rotate</span>
                    <span><i class="fas fa-mouse"></i> <strong>Right Drag:</strong> Pan</span>
                    <span><i class="fas fa-scroll"></i> <strong>Scroll:</strong> Zoom</span>
                    <span><i class="fas fa-hand-pointer"></i> <strong>Touch:</strong> Pinch & Swipe</span>
                </div>
            </div>
        `;

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // Event listeners
        document.getElementById('viewer3d-close').addEventListener('click', closeViewer);
        document.getElementById('viewer3d-reset').addEventListener('click', resetCamera);
        document.getElementById('viewer3d-fullscreen').addEventListener('click', toggleFullscreen);
        overlay.addEventListener('click', (e) => { if (e.target === overlay) closeViewer(); });

        // Control listeners
        document.getElementById('exposure-slider').addEventListener('input', (e) => {
            if (renderer) renderer.toneMappingExposure = parseFloat(e.target.value);
        });

        document.getElementById('brightness-slider').addEventListener('input', (e) => {
            const lights = scene.children.filter(c => c.isLight);
            lights.forEach(light => {
                if (light.isAmbientLight) light.intensity = parseFloat(e.target.value) * 0.6;
                if (light.isDirectionalLight) light.intensity = parseFloat(e.target.value) * 0.8;
            });
        });

        let wireframeVisible = false;
        document.getElementById('toggle-wireframe').addEventListener('click', function () {
            wireframeVisible = !wireframeVisible;
            this.classList.toggle('active');
            if (modelGroup) {
                modelGroup.traverse(obj => {
                    if (obj.userData.isWireframe) obj.visible = wireframeVisible;
                });
            }
        });

        let labelsVisible = true;
        document.getElementById('toggle-labels').addEventListener('click', function () {
            labelsVisible = !labelsVisible;
            this.classList.toggle('active');
            labelSprites.forEach(sprite => sprite.visible = labelsVisible);
        });

        return { overlay, modal };
    }

    function createTextSprite(text, color = '#2563EB') {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 512;
        canvas.height = 128;

        ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
        ctx.roundRect(10, 10, canvas.width - 20, canvas.height - 20, 15);
        ctx.fill();

        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.roundRect(10, 10, canvas.width - 20, canvas.height - 20, 15);
        ctx.stroke();

        ctx.font = 'bold 48px Arial, sans-serif';
        ctx.fillStyle = color;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(text, canvas.width / 2, canvas.height / 2);

        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.SpriteMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Sprite(material);
        sprite.scale.set(2, 0.5, 1);

        return sprite;
    }

    function openViewer(instrumentId) {
        const model = MODELS[instrumentId];
        if (!model || typeof THREE === 'undefined') {
            console.error('Three.js not loaded or invalid instrument ID');
            return;
        }

        viewerOpen = true;
        labelSprites = [];

        let ui = document.getElementById('viewer3d-overlay');
        if (!ui) {
            const created = createViewer();
            ui = created.overlay;
        }

        // Update title
        document.getElementById('viewer3d-title').textContent = model.name;
        document.getElementById('viewer3d-subtitle').textContent = model.description;

        // Show with animation
        requestAnimationFrame(() => {
            ui.classList.add('active');
        });

        // Setup Three.js
        const container = document.getElementById('viewer3d-container');
        const canvas = document.getElementById('viewer3d-canvas');
        const loading = document.getElementById('viewer3d-loading');

        const width = container.clientWidth;
        const height = container.clientHeight;

        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xF1F5F9);
        scene.fog = new THREE.Fog(0xF1F5F9, 10, 50);

        camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
        camera.position.set(6, 5, 6);

        renderer = new THREE.WebGLRenderer({
            canvas,
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance'
        });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.toneMapping = THREE.ACESFilmicToneMapping;
        renderer.toneMappingExposure = 1.0;

        // Enhanced lighting setup
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainLight.position.set(5, 10, 7);
        mainLight.castShadow = true;
        mainLight.shadow.mapSize.width = 2048;
        mainLight.shadow.mapSize.height = 2048;
        mainLight.shadow.camera.near = 0.5;
        mainLight.shadow.camera.far = 50;
        scene.add(mainLight);

        const fillLight = new THREE.DirectionalLight(0x88CCFF, 0.4);
        fillLight.position.set(-5, 3, -5);
        scene.add(fillLight);

        const rimLight = new THREE.DirectionalLight(0xFFEEDD, 0.3);
        rimLight.position.set(0, 5, -10);
        scene.add(rimLight);

        // Enhanced grid with fade
        const gridHelper = new THREE.GridHelper(12, 24, 0xCBD5E1, 0xE2E8F0);
        gridHelper.position.y = -2.5;
        gridHelper.material.opacity = 0.5;
        gridHelper.material.transparent = true;
        scene.add(gridHelper);

        // Ground plane with shadow
        const groundGeometry = new THREE.PlaneGeometry(50, 50);
        const groundMaterial = new THREE.ShadowMaterial({ opacity: 0.15 });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -2.5;
        ground.receiveShadow = true;
        scene.add(ground);

        // Build enhanced model
        modelGroup = new THREE.Group();
        const labelContainer = document.getElementById('viewer3d-labels');
        labelContainer.innerHTML = '';

        model.parts.forEach((part, i) => {
            let geometry;

            switch (part.type) {
                case 'box':
                    geometry = new THREE.BoxGeometry(...part.size, 1, 1, 1);
                    break;
                case 'cylinder':
                    geometry = new THREE.CylinderGeometry(...part.size, 32);
                    break;
                case 'sphere':
                    geometry = new THREE.SphereGeometry(...part.size, 32, 32);
                    break;
                case 'torus':
                    geometry = new THREE.TorusGeometry(...part.size);
                    break;
                default:
                    geometry = new THREE.BoxGeometry(...part.size);
            }

            const material = new THREE.MeshStandardMaterial({
                color: part.color || model.color,
                metalness: part.metallic !== undefined ? part.metallic : model.metallic,
                roughness: part.roughness !== undefined ? part.roughness : model.roughness,
                transparent: part.transparent || false,
                opacity: part.opacity || 1,
                emissive: part.emissive || 0x000000,
                emissiveIntensity: part.emissive ? 0.3 : 0
            });

            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(...part.pos);
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            modelGroup.add(mesh);

            // Enhanced wireframe
            const wireframeGeometry = new THREE.EdgesGeometry(geometry, 15);
            const wireframeMaterial = new THREE.LineBasicMaterial({
                color: 0x000000,
                opacity: 0.2,
                transparent: true,
                linewidth: 1
            });
            const wireframe = new THREE.LineSegments(wireframeGeometry, wireframeMaterial);
            wireframe.position.copy(mesh.position);
            wireframe.visible = false;
            wireframe.userData.isWireframe = true;
            modelGroup.add(wireframe);

            // 3D Text Labels
            const sprite = createTextSprite(part.label, '#' + (part.color || model.color).toString(16).padStart(6, '0'));
            sprite.position.set(part.pos[0], part.pos[1] + part.size[1] / 2 + 0.8, part.pos[2]);
            labelSprites.push(sprite);
            modelGroup.add(sprite);

            // Label chips in footer
            const chip = document.createElement('span');
            chip.className = 'viewer3d-label-chip';
            chip.style.borderColor = '#' + (part.color || model.color).toString(16).padStart(6, '0');
            chip.innerHTML = `<span class="chip-dot" style="background: #${(part.color || model.color).toString(16).padStart(6, '0')}"></span>${part.label}`;
            labelContainer.appendChild(chip);
        });

        scene.add(modelGroup);

        // OrbitControls (requires OrbitControls.js)
        if (typeof THREE.OrbitControls !== 'undefined') {
            controls = new THREE.OrbitControls(camera, canvas);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.screenSpacePanning = false;
            controls.minDistance = 3;
            controls.maxDistance = 20;
            controls.maxPolarAngle = Math.PI / 1.8;
            controls.autoRotate = true;
            controls.autoRotateSpeed = 0.5;
        }

        // Responsive resize
        const resizeObserver = new ResizeObserver(() => {
            const w = container.clientWidth;
            const h = container.clientHeight;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        });
        resizeObserver.observe(container);

        // Animation loop
        loading.style.display = 'none';

        function animate() {
            if (!viewerOpen) return;
            animationId = requestAnimationFrame(animate);

            // FPS counter
            stats.frames++;
            const now = performance.now();
            if (now >= stats.lastTime + 1000) {
                stats.fps = Math.round((stats.frames * 1000) / (now - stats.lastTime));
                stats.lastTime = now;
                stats.frames = 0;
                document.getElementById('viewer3d-fps').textContent = `FPS: ${stats.fps}`;
            }

            if (controls) controls.update();

            // Gentle floating animation
            if (modelGroup) {
                modelGroup.position.y = Math.sin(Date.now() * 0.0005) * 0.1;
            }

            renderer.render(scene, camera);
        }
        animate();
    }

    function resetCamera() {
        if (camera && controls) {
            camera.position.set(6, 5, 6);
            controls.target.set(0, 0, 0);
            controls.update();
        }
    }

    function toggleFullscreen() {
        const overlay = document.getElementById('viewer3d-overlay');
        const icon = document.querySelector('#viewer3d-fullscreen i');

        if (!document.fullscreenElement) {
            overlay.requestFullscreen();
            icon.classList.replace('fa-expand', 'fa-compress');
        } else {
            document.exitFullscreen();
            icon.classList.replace('fa-compress', 'fa-expand');
        }
    }

    function closeViewer() {
        viewerOpen = false;
        if (animationId) cancelAnimationFrame(animationId);

        const overlay = document.getElementById('viewer3d-overlay');
        if (overlay) overlay.classList.remove('active');

        // Comprehensive cleanup
        setTimeout(() => {
            if (controls) controls.dispose();
            if (renderer) {
                renderer.dispose();
                renderer.forceContextLoss();
            }
            if (scene) {
                scene.traverse(obj => {
                    if (obj.geometry) obj.geometry.dispose();
                    if (obj.material) {
                        if (Array.isArray(obj.material)) {
                            obj.material.forEach(mat => mat.dispose());
                        } else {
                            obj.material.dispose();
                        }
                    }
                    if (obj.texture) obj.texture.dispose();
                });
            }
            labelSprites = [];
            modelGroup = null;
        }, 300);
    }

    // Auto-initialize
    function init() {
        const pageMap = {
            'hplc.html': 'hplc',
            'hplc_simulator.html': 'hplc',
            'ftir.html': 'ftir',
            'ftir_simulator.html': 'ftir',
            'gc.html': 'gc',
            'gc_simulator.html': 'gc',
            'uv_vis.html': 'uv-vis',
            'uv_vis_simulator.html': 'uv-vis'
        };

        const currentPage = window.location.pathname.split('/').pop();
        const instrId = pageMap[currentPage];

        if (instrId && MODELS[instrId] && typeof THREE !== 'undefined') {
            const btn = document.createElement('button');
            btn.className = 'viewer3d-fab';
            btn.innerHTML = '<i class="fas fa-cube"></i><span>View 3D</span>';
            btn.addEventListener('click', () => openViewer(instrId));
            document.body.appendChild(btn);
        }

        // Instrument listing page integration
        if (currentPage === 'instruments.html') {
            document.querySelectorAll('.instrument-card, [class*="card"]').forEach(card => {
                const link = card.querySelector('a')?.href || '';
                for (const [page, id] of Object.entries(pageMap)) {
                    if (link.includes(page.replace('.html', '')) && MODELS[id]) {
                        const viewBtn = document.createElement('button');
                        viewBtn.className = 'viewer3d-card-btn';
                        viewBtn.innerHTML = '<i class="fas fa-cube"></i> View 3D Model';
                        viewBtn.addEventListener('click', (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            openViewer(id);
                        });
                        card.querySelector('.card-footer, .card-actions')?.appendChild(viewBtn) || card.appendChild(viewBtn);
                        break;
                    }
                }
            });
        }
    }

    // Global API
    window.SimuViewer3D = {
        open: openViewer,
        close: closeViewer,
        reset: resetCamera,
        models: MODELS
    };

    // Polyfill for roundRect
    if (typeof CanvasRenderingContext2D !== 'undefined' && !CanvasRenderingContext2D.prototype.roundRect) {
        CanvasRenderingContext2D.prototype.roundRect = function (x, y, w, h, r) {
            this.beginPath();
            this.moveTo(x + r, y);
            this.lineTo(x + w - r, y);
            this.quadraticCurveTo(x + w, y, x + w, y + r);
            this.lineTo(x + w, y + h - r);
            this.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
            this.lineTo(x + r, y + h);
            this.quadraticCurveTo(x, y + h, x, y + h - r);
            this.lineTo(x, y + r);
            this.quadraticCurveTo(x, y, x + r, y);
            this.closePath();
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();