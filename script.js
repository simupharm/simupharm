/* ================================================================
   SIMUPHARMA — PREMIUM STORY-SCROLL ENGINE
   Three.js · GSAP ScrollTrigger · Lenis · 3D Tilt
   Clean · Professional · Competition-Ready
   ================================================================ */

(function () {
    'use strict';

    // ======================== CONFIG ========================
    const CONFIG = {
        // Particle background
        particles: {
            count: 800,
            color: 0x93C5FD,       // blue-300
            colorAlt: 0xA78BFA,    // purple-400
            size: 1.8,
            speed: 0.15,
            connectionDistance: 120,
            mouseInfluence: 60
        },
        // Preloader
        preloader: {
            minDuration: 1800,     // ms
            barSteps: [20, 45, 65, 80, 92, 100]
        },
        // Counters
        counter: {
            duration: 2200,        // ms
            easing: t => 1 - Math.pow(1 - t, 4) // easeOutQuart
        },
        // Header
        header: {
            scrollThreshold: 50
        }
    };

    // ======================== STATE ========================
    const state = {
        mouse: { x: 0, y: 0, nx: 0, ny: 0 },
        scroll: 0,
        isLoaded: false,
        isMobileMenuOpen: false,
        lenis: null,
        scene: null,
        camera: null,
        renderer: null,
        particles: null,
        raf: null,
        sections: []
    };


    // ================================================================
    //  INIT — Entry Point
    // ================================================================
    document.addEventListener('DOMContentLoaded', () => {
        // Register GSAP plugins
        if (typeof gsap !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
            if (typeof ScrollToPlugin !== 'undefined') {
                gsap.registerPlugin(ScrollToPlugin);
            }
        }

        // Start all modules
        initPreloader();
        initLenis();
        initHeader();
        initMobileMenu();
        initNavLinks();
        initDotNav();
        initScrollProgress();
        initThreeBackground();
        initGSAPAnimations();
        initCounters();
        initTiltCards();
        initContactForm();
        initPageSpecific();
        initMouseTracking();
        initInteractiveHero();

        console.log('✅ SimuPharma v3 — All systems initialized');
    });


    // ================================================================
    //  PRELOADER
    // ================================================================
    function initPreloader() {
        const preloader = document.getElementById('preloader');
        if (!preloader) return;

        const barFill = preloader.querySelector('.preloader-bar-fill');
        const statusText = preloader.querySelector('.preloader-status');
        const steps = CONFIG.preloader.barSteps;
        const messages = [
            'Loading virtual instruments…',
            'Calibrating simulations…',
            'Preparing laboratory…',
            'Initializing 3D environment…',
            'Almost ready…',
            'Welcome to SimuPharma'
        ];

        let stepIndex = 0;

        function advanceBar() {
            if (stepIndex >= steps.length) return;
            if (barFill) barFill.style.width = steps[stepIndex] + '%';
            if (statusText) statusText.textContent = messages[stepIndex] || '';
            stepIndex++;

            if (stepIndex < steps.length) {
                setTimeout(advanceBar, 280 + Math.random() * 200);
            }
        }

        advanceBar();

        // Close preloader after minimum duration + window load
        const t0 = performance.now();

        window.addEventListener('load', () => {
            const elapsed = performance.now() - t0;
            const remaining = Math.max(0, CONFIG.preloader.minDuration - elapsed);

            setTimeout(() => {
                // Ensure bar is at 100%
                if (barFill) barFill.style.width = '100%';
                if (statusText) statusText.textContent = 'Welcome to SimuPharma';

                setTimeout(() => {
                    preloader.classList.add('done');
                    state.isLoaded = true;
                    document.body.style.overflow = '';

                    // Trigger hero entrance animations
                    setTimeout(animateHeroEntrance, 200);
                }, 400);
            }, remaining);
        });

        // Prevent scroll during preload
        document.body.style.overflow = 'hidden';
    }


    // ================================================================
    //  LENIS SMOOTH SCROLL
    // ================================================================
    function initLenis() {
        if (typeof Lenis === 'undefined') {
            // Fallback: native smooth scroll
            document.documentElement.style.scrollBehavior = 'smooth';
            return;
        }

        state.lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            orientation: 'vertical',
            gestureOrientation: 'vertical',
            smoothWheel: true,
            wheelMultiplier: 1,
            touchMultiplier: 2,
            infinite: false
        });

        // Connect Lenis to GSAP ScrollTrigger
        state.lenis.on('scroll', ScrollTrigger.update);

        gsap.ticker.add((time) => {
            state.lenis.raf(time * 1000);
        });

        gsap.ticker.lagSmoothing(0);
    }


    // ================================================================
    //  HEADER
    // ================================================================
    function initHeader() {
        const header = document.getElementById('main-header');
        if (!header) return;

        function onScroll() {
            const y = window.scrollY || window.pageYOffset;
            state.scroll = y;

            if (y > CONFIG.header.scrollThreshold) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }

        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll(); // initial check
    }


    // ================================================================
    //  MOBILE MENU
    // ================================================================
    function initMobileMenu() {
        const toggle = document.getElementById('mobile-toggle');
        const menu = document.getElementById('mobile-menu');
        if (!toggle || !menu) return;

        function openMenu() {
            state.isMobileMenuOpen = true;
            toggle.classList.add('active');
            toggle.setAttribute('aria-expanded', 'true');
            menu.classList.add('open');
            menu.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
        }

        function closeMenu() {
            state.isMobileMenuOpen = false;
            toggle.classList.remove('active');
            toggle.setAttribute('aria-expanded', 'false');
            menu.classList.remove('open');
            menu.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }

        toggle.addEventListener('click', () => {
            state.isMobileMenuOpen ? closeMenu() : openMenu();
        });

        // Close on background click
        const bg = menu.querySelector('.mobile-menu-bg');
        if (bg) bg.addEventListener('click', closeMenu);

        // Close on link click
        menu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                closeMenu();
            });
        });

        // Close on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && state.isMobileMenuOpen) closeMenu();
        });
    }


    // ================================================================
    //  NAV LINKS (Smooth scroll to sections)
    // ================================================================
    function initNavLinks() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (!href || href === '#') return;

                const target = document.querySelector(href);
                if (!target) return;

                e.preventDefault();

                const headerH = document.getElementById('main-header')?.offsetHeight || 72;

                if (state.lenis) {
                    state.lenis.scrollTo(target, {
                        offset: -headerH,
                        duration: 1.2
                    });
                } else if (typeof gsap !== 'undefined' && gsap.plugins?.scrollTo) {
                    gsap.to(window, {
                        scrollTo: { y: target, offsetY: headerH },
                        duration: 1,
                        ease: 'power3.out'
                    });
                } else {
                    const top = target.getBoundingClientRect().top + window.pageYOffset - headerH;
                    window.scrollTo({ top, behavior: 'smooth' });
                }

                // Update active nav
                updateActiveNav(href);
            });
        });
    }

    function updateActiveNav(hash) {
        document.querySelectorAll('.nav-link, #dot-nav .dot').forEach(link => {
            const linkHash = link.getAttribute('href');
            if (linkHash === hash) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }


    // ================================================================
    //  DOT NAVIGATION (scroll-aware active state)
    // ================================================================
    function initDotNav() {
        const dots = document.querySelectorAll('#dot-nav .dot');
        if (!dots.length) return;

        // Gather sections that the dots point to
        const sections = [];
        dots.forEach(dot => {
            const href = dot.getAttribute('href');
            const section = document.querySelector(href);
            if (section) sections.push({ el: section, dot, id: href });
        });

        state.sections = sections;

        // On scroll — check which section is in view
        function checkActive() {
            const headerH = 100;
            const scrollY = window.scrollY || window.pageYOffset;
            const windowH = window.innerHeight;

            let currentId = sections[0]?.id || '';

            for (let i = sections.length - 1; i >= 0; i--) {
                const s = sections[i];
                const rect = s.el.getBoundingClientRect();
                if (rect.top <= windowH * 0.4) {
                    currentId = s.id;
                    break;
                }
            }

            // Update dots
            sections.forEach(s => {
                if (s.id === currentId) {
                    s.dot.classList.add('active');
                } else {
                    s.dot.classList.remove('active');
                }
            });

            // Also update header nav links
            document.querySelectorAll('.nav-link').forEach(link => {
                const href = link.getAttribute('href');
                if (href === currentId) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        }

        window.addEventListener('scroll', debounce(checkActive, 30), { passive: true });
        checkActive();
    }


    // ================================================================
    //  SCROLL PROGRESS BAR
    // ================================================================
    function initScrollProgress() {
        const fill = document.querySelector('#scroll-progress .progress-fill');
        if (!fill) return;

        function update() {
            const scrollTop = window.scrollY || window.pageYOffset;
            const docH = document.documentElement.scrollHeight - window.innerHeight;
            const pct = docH > 0 ? (scrollTop / docH) * 100 : 0;
            fill.style.width = pct + '%';
        }

        window.addEventListener('scroll', update, { passive: true });
        update();
    }


    // ================================================================
    //  THREE.JS PARTICLE BACKGROUND
    // ================================================================
    function initThreeBackground() {
        const canvas = document.getElementById('bg-canvas');
        if (!canvas || typeof THREE === 'undefined') return;

        const cfg = CONFIG.particles;

        // Scene setup
        const scene = new THREE.Scene();
        state.scene = scene;

        // Camera
        const camera = new THREE.PerspectiveCamera(
            60,
            window.innerWidth / window.innerHeight,
            1,
            1000
        );
        camera.position.z = 350;
        state.camera = camera;

        // Renderer
        const renderer = new THREE.WebGLRenderer({
            canvas,
            antialias: true,
            alpha: true
        });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setClearColor(0x000000, 0); // transparent
        state.renderer = renderer;

        // Particles
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(cfg.count * 3);
        const colors = new Float32Array(cfg.count * 3);
        const velocities = [];

        const color1 = new THREE.Color(cfg.color);
        const color2 = new THREE.Color(cfg.colorAlt);

        for (let i = 0; i < cfg.count; i++) {
            const i3 = i * 3;
            positions[i3] = (Math.random() - 0.5) * 700;
            positions[i3 + 1] = (Math.random() - 0.5) * 700;
            positions[i3 + 2] = (Math.random() - 0.5) * 400;

            // Random mix of two colors
            const mix = Math.random();
            const col = color1.clone().lerp(color2, mix);
            colors[i3] = col.r;
            colors[i3 + 1] = col.g;
            colors[i3 + 2] = col.b;

            velocities.push({
                x: (Math.random() - 0.5) * cfg.speed,
                y: (Math.random() - 0.5) * cfg.speed,
                z: (Math.random() - 0.5) * cfg.speed * 0.3
            });
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        // Create circular particle texture
        const particleTexture = createParticleTexture();

        const material = new THREE.PointsMaterial({
            size: cfg.size,
            map: particleTexture,
            vertexColors: true,
            transparent: true,
            opacity: 0.6,
            depthWrite: false,
            blending: THREE.NormalBlending
        });

        const points = new THREE.Points(geometry, material);
        scene.add(points);
        state.particles = { points, velocities, geometry };

        // Connection lines (subtle)
        const lineGeom = new THREE.BufferGeometry();
        const lineMat = new THREE.LineBasicMaterial({
            color: 0xBFDBFE,       // blue-200
            transparent: true,
            opacity: 0.08,
            depthWrite: false
        });
        const lines = new THREE.LineSegments(lineGeom, lineMat);
        scene.add(lines);

        // Animation loop
        function animate() {
            state.raf = requestAnimationFrame(animate);

            const pos = geometry.attributes.position.array;

            // Move particles
            for (let i = 0; i < cfg.count; i++) {
                const i3 = i * 3;
                pos[i3] += velocities[i].x;
                pos[i3 + 1] += velocities[i].y;
                pos[i3 + 2] += velocities[i].z;

                // Wrap around boundaries
                if (pos[i3] > 350) pos[i3] = -350;
                if (pos[i3] < -350) pos[i3] = 350;
                if (pos[i3 + 1] > 350) pos[i3 + 1] = -350;
                if (pos[i3 + 1] < -350) pos[i3 + 1] = 350;
                if (pos[i3 + 2] > 200) pos[i3 + 2] = -200;
                if (pos[i3 + 2] < -200) pos[i3 + 2] = 200;
            }

            geometry.attributes.position.needsUpdate = true;

            // Subtle mouse influence on camera
            const targetX = state.mouse.nx * 15;
            const targetY = state.mouse.ny * 10;
            camera.position.x += (targetX - camera.position.x) * 0.02;
            camera.position.y += (-targetY - camera.position.y) * 0.02;
            camera.lookAt(scene.position);

            // Gentle rotation of entire particle field
            points.rotation.y += 0.0002;
            points.rotation.x += 0.0001;

            // Update connections (check every 3rd frame for performance)
            if (Math.random() < 0.33) {
                updateConnections(pos, lineGeom, cfg);
            }

            renderer.render(scene, camera);
        }

        animate();

        // Handle resize
        function onResize() {
            const w = window.innerWidth;
            const h = window.innerHeight;
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            renderer.setSize(w, h);
        }

        window.addEventListener('resize', debounce(onResize, 150));
    }

    function createParticleTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 32;
        canvas.height = 32;
        const ctx = canvas.getContext('2d');
        const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
        gradient.addColorStop(0, 'rgba(255,255,255,1)');
        gradient.addColorStop(0.3, 'rgba(255,255,255,0.8)');
        gradient.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 32, 32);
        const texture = new THREE.CanvasTexture(canvas);
        return texture;
    }

    function updateConnections(positions, lineGeom, cfg) {
        const linePositions = [];
        const maxConnections = 200; // limit for performance
        let connectionCount = 0;

        // Only check a subset of particles for connections
        const step = Math.max(1, Math.floor(cfg.count / 100));

        for (let i = 0; i < cfg.count && connectionCount < maxConnections; i += step) {
            const i3 = i * 3;
            for (let j = i + step; j < cfg.count && connectionCount < maxConnections; j += step) {
                const j3 = j * 3;
                const dx = positions[i3] - positions[j3];
                const dy = positions[i3 + 1] - positions[j3 + 1];
                const dz = positions[i3 + 2] - positions[j3 + 2];
                const dist = dx * dx + dy * dy + dz * dz;

                if (dist < cfg.connectionDistance * cfg.connectionDistance) {
                    linePositions.push(
                        positions[i3], positions[i3 + 1], positions[i3 + 2],
                        positions[j3], positions[j3 + 1], positions[j3 + 2]
                    );
                    connectionCount++;
                }
            }
        }

        lineGeom.setAttribute(
            'position',
            new THREE.Float32BufferAttribute(linePositions, 3)
        );
    }


    // ================================================================
    //  MOUSE TRACKING
    // ================================================================
    function initMouseTracking() {
        window.addEventListener('mousemove', (e) => {
            state.mouse.x = e.clientX;
            state.mouse.y = e.clientY;
            // Normalized (-1 to 1)
            state.mouse.nx = (e.clientX / window.innerWidth) * 2 - 1;
            state.mouse.ny = (e.clientY / window.innerHeight) * 2 - 1;
        }, { passive: true });
    }


    // ================================================================
    //  GSAP SCROLL ANIMATIONS
    // ================================================================
    function initGSAPAnimations() {
        if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;

        // Default settings
        const defaults = {
            duration: 0.9,
            ease: 'power3.out'
        };

        // --- fade-up ---
        gsap.utils.toArray('[data-anim="fade-up"]').forEach(el => {
            const delay = parseFloat(el.dataset.delay) || 0;
            gsap.to(el, {
                scrollTrigger: {
                    trigger: el,
                    start: 'top 88%',
                    toggleActions: 'play none none none'
                },
                y: 0,
                opacity: 1,
                duration: defaults.duration,
                delay,
                ease: defaults.ease
            });
        });

        // --- scale-in ---
        gsap.utils.toArray('[data-anim="scale-in"]').forEach(el => {
            const delay = parseFloat(el.dataset.delay) || 0;
            gsap.to(el, {
                scrollTrigger: {
                    trigger: el,
                    start: 'top 88%',
                    toggleActions: 'play none none none'
                },
                scale: 1,
                opacity: 1,
                duration: 1,
                delay,
                ease: 'power3.out'
            });
        });

        // --- reveal-left ---
        gsap.utils.toArray('[data-anim="reveal-left"]').forEach(el => {
            gsap.to(el, {
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                    toggleActions: 'play none none none'
                },
                x: 0,
                opacity: 1,
                duration: 1,
                ease: 'power3.out'
            });
        });

        // --- reveal-right ---
        gsap.utils.toArray('[data-anim="reveal-right"]').forEach(el => {
            gsap.to(el, {
                scrollTrigger: {
                    trigger: el,
                    start: 'top 85%',
                    toggleActions: 'play none none none'
                },
                x: 0,
                opacity: 1,
                duration: 1,
                ease: 'power3.out'
            });
        });

        // --- card-up (staggered per grid) ---
        const featGrids = document.querySelectorAll('.features-grid');
        featGrids.forEach(grid => {
            const cards = grid.querySelectorAll('[data-anim="card-up"]');
            gsap.to(cards, {
                scrollTrigger: {
                    trigger: grid,
                    start: 'top 82%',
                    toggleActions: 'play none none none'
                },
                y: 0,
                rotateX: 0,
                opacity: 1,
                duration: 0.8,
                stagger: 0.1,
                ease: 'power3.out'
            });
        });

        // --- instr-reveal (staggered) ---
        const instrGrid = document.querySelector('.instr-grid');
        if (instrGrid) {
            const instrCards = instrGrid.querySelectorAll('[data-anim="instr-reveal"]');
            gsap.to(instrCards, {
                scrollTrigger: {
                    trigger: instrGrid,
                    start: 'top 82%',
                    toggleActions: 'play none none none'
                },
                y: 0,
                scale: 1,
                opacity: 1,
                duration: 0.8,
                stagger: 0.12,
                ease: 'power3.out'
            });
        }

        // --- step-reveal (staggered) ---
        const stepsWrapper = document.querySelector('.steps-wrapper');
        if (stepsWrapper) {
            const steps = stepsWrapper.querySelectorAll('[data-anim="step-reveal"]');
            const connectors = stepsWrapper.querySelectorAll('[data-anim="draw-line"]');

            gsap.to(steps, {
                scrollTrigger: {
                    trigger: stepsWrapper,
                    start: 'top 80%',
                    toggleActions: 'play none none none',
                    onEnter: () => {
                        // Trigger ring progress animation
                        steps.forEach(s => s.classList.add('in-view'));
                    }
                },
                y: 0,
                opacity: 1,
                duration: 0.8,
                stagger: 0.2,
                ease: 'power3.out'
            });

            gsap.to(connectors, {
                scrollTrigger: {
                    trigger: stepsWrapper,
                    start: 'top 80%',
                    toggleActions: 'play none none none'
                },
                opacity: 0.4,
                duration: 0.6,
                stagger: 0.3,
                delay: 0.3,
                ease: 'power2.out'
            });
        }

        // --- float (hero floating cards) ---
        gsap.utils.toArray('[data-anim="float"]').forEach(el => {
            const delay = parseFloat(el.dataset.delay) || 0;
            gsap.to(el, {
                scrollTrigger: {
                    trigger: el.closest('.hero-visual') || el,
                    start: 'top 85%',
                    toggleActions: 'play none none none'
                },
                y: 0,
                opacity: 1,
                duration: 0.7,
                delay,
                ease: 'back.out(1.7)'
            });
        });

        // --- counter-up (impact stats) ---
        gsap.utils.toArray('[data-anim="counter-up"]').forEach(el => {
            gsap.to(el, {
                scrollTrigger: {
                    trigger: el,
                    start: 'top 88%',
                    toggleActions: 'play none none none',
                    onEnter: () => {
                        el.classList.add('in-view');
                    }
                },
                y: 0,
                opacity: 1,
                duration: 0.7,
                ease: 'power3.out'
            });
        });

        // --- Parallax for hero background orbs ---
        const orbs = document.querySelectorAll('.gradient-orb');
        orbs.forEach((orb, i) => {
            gsap.to(orb, {
                scrollTrigger: {
                    trigger: '#hero',
                    start: 'top top',
                    end: 'bottom top',
                    scrub: 1
                },
                y: i === 0 ? -100 : -60,
                ease: 'none'
            });
        });

        // --- Hero mockup parallax ---
        const mockup = document.querySelector('.mockup-browser');
        if (mockup) {
            gsap.to(mockup, {
                scrollTrigger: {
                    trigger: '#hero',
                    start: 'top top',
                    end: 'bottom top',
                    scrub: 1
                },
                y: 50,
                ease: 'none'
            });
        }

        // --- Scroll hint fade out ---
        const scrollHint = document.querySelector('.scroll-hint');
        if (scrollHint) {
            gsap.to(scrollHint, {
                scrollTrigger: {
                    trigger: '#hero',
                    start: '15% top',
                    end: '30% top',
                    scrub: true
                },
                opacity: 0,
                y: -20,
                ease: 'none'
            });
        }
    }


    // ================================================================
    //  HERO ENTRANCE (after preloader)
    // ================================================================
    function animateHeroEntrance() {
        if (typeof gsap === 'undefined') return;

        const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

        // Split title into lines for reveal
        const heroTitle = document.querySelector('.hero-title');
        if (heroTitle) {
            splitTextIntoLines(heroTitle);
            const lineInners = heroTitle.querySelectorAll('.line-inner');

            tl.to(lineInners, {
                y: 0,
                duration: 0.9,
                stagger: 0.12,
                ease: 'power4.out'
            }, 0);
        }

        // Badge
        const badge = document.querySelector('.hero-badge');
        if (badge) {
            tl.to(badge, {
                y: 0,
                opacity: 1,
                duration: 0.7
            }, 0);
        }

        // Description
        const desc = document.querySelector('.hero-desc');
        if (desc) {
            tl.to(desc, {
                y: 0,
                opacity: 1,
                duration: 0.7
            }, 0.25);
        }

        // Actions
        const actions = document.querySelector('.hero-actions');
        if (actions) {
            tl.to(actions, {
                y: 0,
                opacity: 1,
                duration: 0.7
            }, 0.4);
        }

        // Metrics
        const metrics = document.querySelector('.hero-metrics');
        if (metrics) {
            tl.to(metrics, {
                y: 0,
                opacity: 1,
                duration: 0.7
            }, 0.55);
        }

        // Visual
        const visual = document.querySelector('.hero-visual');
        if (visual) {
            tl.to(visual, {
                scale: 1,
                opacity: 1,
                duration: 1
            }, 0.15);
        }

        // Floating cards
        document.querySelectorAll('.float-card').forEach((card, i) => {
            tl.to(card, {
                y: 0,
                opacity: 1,
                duration: 0.6,
                ease: 'back.out(1.7)'
            }, 0.7 + i * 0.15);
        });

        // Scroll hint
        const scrollHint = document.querySelector('.scroll-hint');
        if (scrollHint) {
            tl.to(scrollHint, {
                y: 0,
                opacity: 1,
                duration: 0.5
            }, 1.3);
        }
    }

    function splitTextIntoLines(element) {
        const text = element.innerHTML;
        // Split by <br> or by natural word wrapping
        // For now, wrap the text content in spans
        const html = element.innerHTML;

        // Split at <span> boundaries and <br> for clean line wrapping
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;

        // Get all text nodes and inline elements
        const children = Array.from(tempDiv.childNodes);
        let newHTML = '';

        children.forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                // Wrap text lines
                const words = node.textContent.trim();
                if (words) {
                    newHTML += `<span class="line-wrap"><span class="line-inner">${words}</span></span> `;
                }
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                // Wrap element (like <span class="text-gradient">)
                newHTML += `<span class="line-wrap"><span class="line-inner">${node.outerHTML}</span></span> `;
            }
        });

        element.innerHTML = newHTML;
    }


    // ================================================================
    //  COUNTERS
    // ================================================================
    function initCounters() {
        // All elements with data-count
        const counters = document.querySelectorAll('[data-count]');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.getAttribute('data-count'), 10);
                    const suffix = el.getAttribute('data-suffix') || '';
                    animateCounter(el, target, suffix);
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(el => observer.observe(el));
    }

    function animateCounter(element, target, suffix) {
        const cfg = CONFIG.counter;
        const start = performance.now();

        function tick(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / cfg.duration, 1);
            const eased = cfg.easing(progress);
            const current = Math.floor(target * eased);

            element.textContent = formatNumber(current);

            if (progress < 1) {
                requestAnimationFrame(tick);
            } else {
                element.textContent = formatNumber(target);
            }
        }

        requestAnimationFrame(tick);
    }

    function formatNumber(n) {
        if (n >= 10000) {
            return (n / 1000).toFixed(n % 1000 === 0 ? 0 : 1).replace(/\.0$/, '') + 'K';
        }
        return n.toLocaleString();
    }


    // ================================================================
    //  3D TILT EFFECT (on cards)
    // ================================================================
    function initTiltCards() {
        const tiltEls = document.querySelectorAll('[data-tilt]');

        tiltEls.forEach(card => {
            const maxTilt = 6; // degrees
            const scale = 1.02;

            card.addEventListener('mouseenter', () => {
                card.style.transition = 'transform 0.15s ease';
            });

            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;

                const mouseX = e.clientX - centerX;
                const mouseY = e.clientY - centerY;

                const rotateX = (-mouseY / (rect.height / 2)) * maxTilt;
                const rotateY = (mouseX / (rect.width / 2)) * maxTilt;

                card.style.transform =
                    `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(${scale}, ${scale}, ${scale})`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
                card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            });
        });
    }


    // ================================================================
    //  CONTACT FORM
    // ================================================================
    function initContactForm() {
        const form = document.querySelector('.contact-form');
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const btn = form.querySelector('button[type="submit"]');
            const originalHTML = btn.innerHTML;

            // Validate
            const name = form.querySelector('#c-name');
            const email = form.querySelector('#c-email');
            const message = form.querySelector('#c-message');

            if (!name?.value.trim() || !email?.value.trim() || !message?.value.trim()) {
                shakeElement(btn);
                return;
            }

            // Sending state
            btn.disabled = true;
            btn.innerHTML = '<span>Sending…</span> <i class="fas fa-spinner fa-spin"></i>';

            // Simulate send (replace with real API)
            setTimeout(() => {
                btn.innerHTML = '<span>Sent Successfully!</span> <i class="fas fa-check"></i>';
                btn.style.background = '#22C55E';
                form.reset();

                setTimeout(() => {
                    btn.disabled = false;
                    btn.innerHTML = originalHTML;
                    btn.style.background = '';
                }, 3000);
            }, 1500);
        });

        // Floating label focus effect
        form.querySelectorAll('input, textarea').forEach(input => {
            input.addEventListener('focus', () => {
                input.parentElement.classList.add('focused');
            });
            input.addEventListener('blur', () => {
                if (!input.value) {
                    input.parentElement.classList.remove('focused');
                }
            });
        });
    }

    function shakeElement(el) {
        el.style.animation = 'none';
        el.offsetHeight; // trigger reflow
        el.style.animation = 'shake 0.4s ease';
        setTimeout(() => { el.style.animation = ''; }, 400);

        // Add shake keyframes if not exists
        if (!document.getElementById('shake-style')) {
            const style = document.createElement('style');
            style.id = 'shake-style';
            style.textContent = `
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    20% { transform: translateX(-8px); }
                    40% { transform: translateX(8px); }
                    60% { transform: translateX(-4px); }
                    80% { transform: translateX(4px); }
                }
            `;
            document.head.appendChild(style);
        }
    }


    // ================================================================
    //  PAGE-SPECIFIC (Quiz, Tutorials — if on those pages)
    // ================================================================
    function initPageSpecific() {
        // Quiz (if quiz elements exist in the page)
        if (document.getElementById('question-text') && document.getElementById('options-container')) {
            initQuiz();
        }

        // Tutorials
        if (document.getElementById('modal-backdrop')) {
            initTutorials();
        }
    }


    // ================================================================
    //  QUIZ
    // ================================================================
    function initQuiz() {
        const questions = [
            { question: "In HPLC, what does the 'HP' stand for?", options: ["High Purity", "High Pressure", "High Performance", "Both High Pressure & High Performance"], correctAnswer: "Both High Pressure & High Performance" },
            { question: "What physical property does FTIR spectroscopy primarily measure?", options: ["Absorption of UV light", "Molecular mass", "Absorption of Infrared radiation by chemical bonds", "Nuclear spin"], correctAnswer: "Absorption of Infrared radiation by chemical bonds" },
            { question: "Gas Chromatography is most suitable for analyzing compounds that are:", options: ["Highly soluble in water", "Very large proteins", "Volatile or can be vaporized", "Inorganic salts"], correctAnswer: "Volatile or can be vaporized" },
            { question: "The component where separation occurs in HPLC and GC is called the:", options: ["Injector", "Pump", "Column", "Detector"], correctAnswer: "Column" },
            { question: "An FTIR spectrum is typically plotted as % Transmittance vs:", options: ["Time", "Wavenumber (cm⁻¹)", "Wavelength (nm)", "Magnetic Field Strength"], correctAnswer: "Wavenumber (cm⁻¹)" },
            { question: "Which part of a GC system is responsible for heating the column?", options: ["The detector", "The injector", "The oven", "The gas tank"], correctAnswer: "The oven" },
            { question: "In Mass Spectrometry, what does 'm/z' on the x-axis represent?", options: ["Molecular Size", "Magnetic Zone", "Mass-to-charge ratio", "Molecule-to-z-axis ratio"], correctAnswer: "Mass-to-charge ratio" },
            { question: "In the HPLC simulator, increasing the Methanol % in the mobile phase for a C18 column will typically cause the retention time to:", options: ["Increase", "Decrease", "Stay the same", "Become unpredictable"], correctAnswer: "Decrease" },
            { question: "Why is a 'Background Scan' performed before a sample scan in FTIR?", options: ["To heat up the instrument", "To calibrate the laser frequency", "To measure and subtract the spectrum of air (CO₂ and H₂O)", "To clean the sample holder"], correctAnswer: "To measure and subtract the spectrum of air (CO₂ and H₂O)" },
            { question: "In a GC temperature program, what is the 'ramp rate'?", options: ["The speed of the carrier gas", "The rate at which the oven temperature increases", "The speed of the detector", "The rate of sample injection"], correctAnswer: "The rate at which the oven temperature increases" },
            { question: "In a mass spectrum, the peak with the highest m/z value often represents the:", options: ["Smallest fragment", "Solvent", "Base peak", "Molecular ion (the intact molecule)"], correctAnswer: "Molecular ion (the intact molecule)" },
            { question: "In the HPLC simulator, what happens to the peak size if you set the detector wavelength far from the compound's optimal wavelength?", options: ["The peak gets larger", "The peak gets smaller or disappears", "The retention time changes", "The peak splits in two"], correctAnswer: "The peak gets smaller or disappears" },
            { question: "In reverse-phase HPLC, the stationary phase is ___ and the mobile phase is ___.", options: ["Polar, Non-polar", "Non-polar, Polar", "Ionic, Non-ionic", "Acidic, Basic"], correctAnswer: "Non-polar, Polar" },
            { question: "What is the most common detector in Gas Chromatography?", options: ["Thermal Conductivity Detector (TCD)", "Electron Capture Detector (ECD)", "Flame Ionization Detector (FID)", "Mass Spectrometer (MS)"], correctAnswer: "Flame Ionization Detector (FID)" },
            { question: "The region of an FTIR spectrum below 1500 cm⁻¹ is often called the:", options: ["Functional Group Region", "Aromatic Region", "Fingerprint Region", "Hydrogen Bonding Region"], correctAnswer: "Fingerprint Region" },
            { question: "In a mass spectrum, what is the name for the most intense peak?", options: ["Molecular Ion Peak", "Parent Peak", "Fragment Peak", "Base Peak"], correctAnswer: "Base Peak" },
            { question: "The time for a compound to travel from injector to detector in chromatography is called:", options: ["Elution Time", "Dead Time", "Retention Time", "Separation Time"], correctAnswer: "Retention Time" },
            { question: "Which ionization technique in Mass Spectrometry causes extensive fragmentation?", options: ["Electrospray Ionization (ESI)", "Electron Impact (EI)", "Chemical Ionization (CI)", "MALDI"], correctAnswer: "Electron Impact (EI)" },
            { question: "In chromatography, what does the area under a peak represent?", options: ["Molecular weight", "Boiling point", "Concentration", "Purity"], correctAnswer: "Concentration" },
            { question: "A common method for preparing solid samples for FTIR is grinding with:", options: ["Sodium Chloride (NaCl)", "Silicon Dioxide (SiO₂)", "Potassium Bromide (KBr)", "Water (H₂O)"], correctAnswer: "Potassium Bromide (KBr)" }
        ];

        const quizContainer = document.querySelector('.quiz-container');
        const questionText = document.getElementById('question-text');
        const optionsContainer = document.getElementById('options-container');
        const scoreDisplay = document.getElementById('quiz-score');
        const progressBar = document.getElementById('quiz-progress-bar');
        const feedbackText = document.getElementById('feedback-text');

        if (!quizContainer || !questionText) return;

        let currentQuestion = 0;
        let score = 0;

        function loadQuestion() {
            if (feedbackText) feedbackText.textContent = '';

            if (currentQuestion < questions.length) {
                const q = questions[currentQuestion];
                questionText.textContent = q.question;
                optionsContainer.innerHTML = '';

                const shuffledOptions = [...q.options].sort(() => Math.random() - 0.5);

                shuffledOptions.forEach(option => {
                    const btn = document.createElement('button');
                    btn.textContent = option;
                    btn.className = 'option-btn';
                    btn.onclick = () => selectAnswer(btn, option, q.correctAnswer);
                    optionsContainer.appendChild(btn);
                });

                if (progressBar) {
                    progressBar.style.width = `${(currentQuestion / questions.length) * 100}%`;
                }
                if (scoreDisplay) {
                    scoreDisplay.textContent = `Score: ${score}/${questions.length}`;
                }
            } else {
                showResults();
            }
        }

        function selectAnswer(button, selected, correct) {
            const buttons = optionsContainer.querySelectorAll('.option-btn');

            buttons.forEach(btn => {
                btn.disabled = true;
                if (btn.textContent === correct) {
                    btn.classList.add('correct');
                }
            });

            if (selected === correct) {
                score++;
            } else {
                button.classList.add('incorrect');
                if (feedbackText) {
                    feedbackText.textContent = `Correct answer: ${correct}`;
                    feedbackText.style.color = '#EF4444';
                }
            }

            if (scoreDisplay) {
                scoreDisplay.textContent = `Score: ${score}/${questions.length}`;
            }

            setTimeout(() => {
                currentQuestion++;
                loadQuestion();
            }, 2000);
        }

        function showResults() {
            if (progressBar) progressBar.style.width = '100%';
            const percentage = Math.round((score / questions.length) * 100);

            let message = '';
            let emoji = '';
            if (percentage >= 90) { message = 'Excellent! Outstanding performance!'; emoji = '🏆'; }
            else if (percentage >= 70) { message = 'Great job! Well done!'; emoji = '🎉'; }
            else if (percentage >= 50) { message = 'Good effort! Keep learning!'; emoji = '📚'; }
            else { message = "Keep practicing! You'll improve!"; emoji = '💪'; }

            quizContainer.innerHTML = `
                <div style="text-align:center; padding:48px 24px;">
                    <div style="font-size:3rem; margin-bottom:16px;">${emoji}</div>
                    <h2 style="font-family:var(--font-display); font-size:2rem; font-weight:800; color:var(--gray-900); margin-bottom:8px;">
                        Quiz Complete!
                    </h2>
                    <div style="width:100px; height:100px; border-radius:50%; background:var(--gradient-brand);
                        color:white; font-size:1.75rem; font-weight:800; display:flex; align-items:center;
                        justify-content:center; margin:24px auto; box-shadow:var(--sh-blue);">
                        ${score}/${questions.length}
                    </div>
                    <p style="font-size:1.125rem; color:var(--gray-500); margin-bottom:32px;">${message}</p>
                    <button onclick="location.reload()" class="btn btn-primary btn-lg">
                        <span>Try Again</span>
                        <i class="fas fa-redo"></i>
                    </button>
                </div>
            `;
        }

        loadQuestion();
    }


    // ================================================================
    //  TUTORIALS
    // ================================================================
    function initTutorials() {
        const backdrop = document.getElementById('modal-backdrop');
        const modals = document.querySelectorAll('.tutorial-modal');
        const modalBtns = document.querySelectorAll('[data-modal-id]');
        const closeBtns = document.querySelectorAll('.modal-close-btn');

        if (!backdrop) return;

        function openModal(modalId) {
            const modal = document.getElementById(modalId);
            if (!modal) return;
            backdrop.classList.add('is-visible');
            modal.classList.add('is-visible');
            document.body.style.overflow = 'hidden';

            const video = modal.querySelector('video');
            if (video) {
                video.currentTime = 0;
                video.play().catch(() => { });
            }
        }

        function closeModals() {
            backdrop.classList.remove('is-visible');
            modals.forEach(modal => {
                modal.classList.remove('is-visible');
                const video = modal.querySelector('video');
                if (video) {
                    video.pause();
                    video.currentTime = 0;
                }
            });
            document.body.style.overflow = '';
        }

        modalBtns.forEach(btn => {
            btn.addEventListener('click', () => openModal(btn.dataset.modalId));
        });
        backdrop.addEventListener('click', closeModals);
        closeBtns.forEach(btn => btn.addEventListener('click', closeModals));
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModals();
        });
    }


    // ================================================================
    //  UTILITIES
    // ================================================================
    function debounce(fn, wait) {
        let timer;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), wait);
        };
    }


    // ================================================================
    //  HERO TYPEWRITER EFFECT
    // ================================================================
    function initHeroTypewriter() {
        const el = document.getElementById('hero-typewriter');
        if (!el) return;

        const phrases = [
            'HPLC Chromatography',
            'FTIR Spectroscopy',
            'UV-Vis Analysis',
            'Gas Chromatography',
            'Mass Spectrometry',
            'Polarimetry',
            'Particle Size Analysis'
        ];

        let phraseIdx = 0;
        let charIdx = 0;
        let isDeleting = false;
        let speed = 70;

        function tick() {
            const current = phrases[phraseIdx];

            if (!isDeleting) {
                el.textContent = current.substring(0, charIdx + 1);
                charIdx++;
                speed = 60 + Math.random() * 40;

                if (charIdx === current.length) {
                    isDeleting = true;
                    speed = 2000; // pause at end
                }
            } else {
                el.textContent = current.substring(0, charIdx - 1);
                charIdx--;
                speed = 35;

                if (charIdx === 0) {
                    isDeleting = false;
                    phraseIdx = (phraseIdx + 1) % phrases.length;
                    speed = 400; // pause before next
                }
            }

            setTimeout(tick, speed);
        }

        setTimeout(tick, 1500); // start after hero loads
    }


    // ================================================================
    //  LIVE SPECTRUM CANVAS (animated waveform in mockup)
    // ================================================================
    function initLiveSpectrum() {
        const canvas = document.getElementById('live-spectrum-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        // Instrument spectrum profiles
        const profiles = [
            { color: '#2563EB', peaks: [0.3, 0.6, 0.85, 0.55, 0.35] },  // HPLC
            { color: '#7C3AED', peaks: [0.7, 0.4, 0.9, 0.3, 0.65] },    // FTIR
            { color: '#06B6D4', peaks: [0.5, 0.8, 0.45, 0.7, 0.3] },    // UV-Vis
            { color: '#F59E0B', peaks: [0.4, 0.55, 0.7, 0.9, 0.5] }     // GC
        ];

        let currentProfile = 0;
        let targetPeaks = [...profiles[0].peaks];
        let currentPeaks = [...profiles[0].peaks];
        let time = 0;
        let currentColor = profiles[0].color;

        function lerp(a, b, t) {
            return a + (b - a) * t;
        }

        function draw() {
            time += 0.02;
            ctx.clearRect(0, 0, W, H);

            // Smooth interpolate peaks
            for (let i = 0; i < currentPeaks.length; i++) {
                currentPeaks[i] = lerp(currentPeaks[i], targetPeaks[i], 0.02);
            }

            // Draw grid lines
            ctx.strokeStyle = 'rgba(0,0,0,0.04)';
            ctx.lineWidth = 0.5;
            for (let y = 20; y < H; y += 25) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(W, y);
                ctx.stroke();
            }

            // Draw spectrum line
            const gradient = ctx.createLinearGradient(0, 0, 0, H);
            gradient.addColorStop(0, currentColor + '40');
            gradient.addColorStop(1, currentColor + '00');

            ctx.beginPath();
            ctx.moveTo(0, H - 10);

            const segments = W;
            for (let x = 0; x <= segments; x++) {
                const t = x / segments;
                let y = H - 10;

                // Compose peaks
                for (let p = 0; p < currentPeaks.length; p++) {
                    const peakCenter = (p + 1) / (currentPeaks.length + 1);
                    const dist = Math.abs(t - peakCenter);
                    const sigma = 0.06 + Math.sin(time + p) * 0.01;
                    const amplitude = currentPeaks[p] * (H * 0.7);
                    y -= amplitude * Math.exp(-(dist * dist) / (2 * sigma * sigma));
                }

                // Add subtle noise for "live" feel
                y += Math.sin(time * 3 + x * 0.1) * 1.5;

                ctx.lineTo(x, y);
            }

            // Fill area
            ctx.lineTo(W, H - 10);
            ctx.lineTo(0, H - 10);
            ctx.fillStyle = gradient;
            ctx.fill();

            // Redraw stroke line
            ctx.beginPath();
            ctx.moveTo(0, H - 10);
            for (let x = 0; x <= segments; x++) {
                const t = x / segments;
                let y = H - 10;
                for (let p = 0; p < currentPeaks.length; p++) {
                    const peakCenter = (p + 1) / (currentPeaks.length + 1);
                    const dist = Math.abs(t - peakCenter);
                    const sigma = 0.06 + Math.sin(time + p) * 0.01;
                    const amplitude = currentPeaks[p] * (H * 0.7);
                    y -= amplitude * Math.exp(-(dist * dist) / (2 * sigma * sigma));
                }
                y += Math.sin(time * 3 + x * 0.1) * 1.5;
                ctx.lineTo(x, y);
            }
            ctx.strokeStyle = currentColor;
            ctx.lineWidth = 2;
            ctx.stroke();

            // Live scanning line
            const scanX = (time * 30) % W;
            ctx.beginPath();
            ctx.moveTo(scanX, 0);
            ctx.lineTo(scanX, H);
            ctx.strokeStyle = currentColor + '20';
            ctx.lineWidth = 1;
            ctx.stroke();

            requestAnimationFrame(draw);
        }

        draw();

        // Expose method to switch profile
        window._switchSpectrum = function (idx) {
            currentProfile = idx;
            targetPeaks = [...profiles[idx].peaks];
            currentColor = profiles[idx].color;
        };
    }


    // ================================================================
    //  HERO MOLECULE / NODE CANVAS (floating connected nodes)
    // ================================================================
    function initHeroMolecules() {
        const canvas = document.getElementById('hero-molecule-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        let W, H;
        let mouseX = -1000, mouseY = -1000;

        function resize() {
            const rect = canvas.parentElement.getBoundingClientRect();
            W = canvas.width = rect.width;
            H = canvas.height = rect.height;
        }
        resize();
        window.addEventListener('resize', debounce(resize, 200));

        // Track mouse inside hero
        const hero = document.getElementById('hero');
        if (hero) {
            hero.addEventListener('mousemove', (e) => {
                const rect = canvas.getBoundingClientRect();
                mouseX = e.clientX - rect.left;
                mouseY = e.clientY - rect.top;
            });
            hero.addEventListener('mouseleave', () => {
                mouseX = -1000;
                mouseY = -1000;
            });
        }

        // Create nodes
        const NODE_COUNT = 35;
        const nodes = [];
        for (let i = 0; i < NODE_COUNT; i++) {
            nodes.push({
                x: Math.random() * (W || 1200),
                y: Math.random() * (H || 800),
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                r: 3 + Math.random() * 4,
                color: Math.random() > 0.5 ? '#93C5FD' : '#C4B5FD'
            });
        }

        function animate() {
            ctx.clearRect(0, 0, W, H);

            // Update & draw nodes
            nodes.forEach(n => {
                // Mouse repulsion
                const dx = n.x - mouseX;
                const dy = n.y - mouseY;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 150 && dist > 0) {
                    const force = (150 - dist) / 150 * 0.8;
                    n.vx += (dx / dist) * force;
                    n.vy += (dy / dist) * force;
                }

                // Damping
                n.vx *= 0.98;
                n.vy *= 0.98;

                n.x += n.vx;
                n.y += n.vy;

                // Bounds
                if (n.x < 0) { n.x = 0; n.vx *= -0.5; }
                if (n.x > W) { n.x = W; n.vx *= -0.5; }
                if (n.y < 0) { n.y = 0; n.vy *= -0.5; }
                if (n.y > H) { n.y = H; n.vy *= -0.5; }
            });

            // Draw connections
            for (let i = 0; i < nodes.length; i++) {
                for (let j = i + 1; j < nodes.length; j++) {
                    const dx = nodes[i].x - nodes[j].x;
                    const dy = nodes[i].y - nodes[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 160) {
                        const alpha = (1 - dist / 160) * 0.25;
                        ctx.beginPath();
                        ctx.moveTo(nodes[i].x, nodes[i].y);
                        ctx.lineTo(nodes[j].x, nodes[j].y);
                        ctx.strokeStyle = `rgba(147, 197, 253, ${alpha})`;
                        ctx.lineWidth = 1;
                        ctx.stroke();
                    }
                }
            }

            // Draw nodes
            nodes.forEach(n => {
                // Glow
                ctx.beginPath();
                ctx.arc(n.x, n.y, n.r * 2.5, 0, Math.PI * 2);
                ctx.fillStyle = n.color.replace(')', ', 0.1)').replace('rgb', 'rgba').replace('#', '');
                // Use hex with alpha
                const glowGradient = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 3);
                glowGradient.addColorStop(0, n.color + '30');
                glowGradient.addColorStop(1, n.color + '00');
                ctx.fillStyle = glowGradient;
                ctx.fill();

                // Node
                ctx.beginPath();
                ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
                ctx.fillStyle = n.color;
                ctx.fill();
            });

            requestAnimationFrame(animate);
        }

        animate();
    }


    // ================================================================
    //  CYCLING INSTRUMENT MOCKUP
    // ================================================================
    function initCyclingMockup() {
        const instruments = [
            {
                name: 'HPLC Chromatogram',
                icon: 'fa-vial',
                url: 'simupharma.com/hplc',
                color: '#2563EB',
                lambda: '254 nm', abs: '0.847', flow: '1.0 mL/min',
                fc1: 'HPLC Analysis', fc2: 'Peak Detected', fc2sub: 'RT 4.2 min',
                fc3: '98.7% Purity', fc3sub: 'Validated ✓'
            },
            {
                name: 'FTIR Spectrum',
                icon: 'fa-wave-square',
                url: 'simupharma.com/ftir',
                color: '#7C3AED',
                lambda: '1650 cm⁻¹', abs: '0.923', flow: 'KBr Pellet',
                fc1: 'FTIR Scan', fc2: 'Bond Found', fc2sub: 'C=O Stretch',
                fc3: '99.1% Match', fc3sub: 'Library Hit ✓'
            },
            {
                name: 'UV-Vis Absorbance',
                icon: 'fa-sun',
                url: 'simupharma.com/uv-vis',
                color: '#06B6D4',
                lambda: '280 nm', abs: '0.654', flow: '0.8 mL/min',
                fc1: 'UV-Vis Scan', fc2: 'λmax Found', fc2sub: '280 nm',
                fc3: '97.5% Purity', fc3sub: 'Conforms ✓'
            },
            {
                name: 'GC Chromatogram',
                icon: 'fa-fire',
                url: 'simupharma.com/gc',
                color: '#F59E0B',
                lambda: '220 °C', abs: 'FID', flow: '1.5 mL/min',
                fc1: 'GC Analysis', fc2: 'Peak Split', fc2sub: 'RT 6.8 min',
                fc3: '96.3% Purity', fc3sub: 'Identified ✓'
            }
        ];

        let currentIdx = 0;
        let progressVal = 0;

        const urlEl = document.getElementById('mockup-url');
        const labelEl = document.getElementById('mockup-instr-label');
        const lambdaEl = document.getElementById('ro-lambda');
        const absEl = document.getElementById('ro-abs');
        const flowEl = document.getElementById('ro-flow');
        const statusText = document.getElementById('status-text');
        const progressFill = document.getElementById('status-progress-fill');
        const fc1Title = document.getElementById('fc1-title');
        const fc1Sub = document.getElementById('fc1-sub');
        const fc1Ring = document.getElementById('fc1-ring');
        const fc2Title = document.getElementById('fc2-title');
        const fc2Sub = document.getElementById('fc2-sub');
        const fc3Title = document.getElementById('fc3-title');
        const fc3Sub = document.getElementById('fc3-sub');
        const sbItems = document.querySelectorAll('.sb-item[data-instr]');

        if (!urlEl) return;

        function switchInstrument() {
            const instr = instruments[currentIdx];

            // Update mockup
            if (urlEl) urlEl.textContent = instr.url;
            if (labelEl) labelEl.innerHTML = `<i class="fas ${instr.icon}"></i> ${instr.name}`;
            if (lambdaEl) lambdaEl.textContent = instr.lambda;
            if (absEl) absEl.textContent = instr.abs;
            if (flowEl) flowEl.textContent = instr.flow;
            if (statusText) statusText.textContent = `${instr.fc1} Running`;

            // Update float cards
            if (fc1Title) fc1Title.textContent = instr.fc1;
            if (fc1Sub) fc1Sub.textContent = 'Running…';
            if (fc2Title) fc2Title.textContent = instr.fc2;
            if (fc2Sub) fc2Sub.textContent = instr.fc2sub;
            if (fc3Title) fc3Title.textContent = instr.fc3;
            if (fc3Sub) fc3Sub.textContent = instr.fc3sub;

            // Update sidebar active
            sbItems.forEach((item, i) => {
                item.classList.toggle('active', i === currentIdx);
            });

            // Switch spectrum
            if (window._switchSpectrum) {
                window._switchSpectrum(currentIdx);
            }

            // Reset progress
            progressVal = 0;
        }

        // Animate progress bar
        function tickProgress() {
            progressVal += 0.35;
            if (progressFill) progressFill.style.width = Math.min(progressVal, 100) + '%';
            if (fc1Ring) fc1Ring.style.strokeDashoffset = 100 - Math.min(progressVal, 100);

            if (progressVal >= 100) {
                // Switch to next instrument
                if (fc1Sub) fc1Sub.textContent = 'Complete ✓';
                if (statusText) statusText.textContent = 'Analysis Complete';

                setTimeout(() => {
                    currentIdx = (currentIdx + 1) % instruments.length;
                    switchInstrument();
                }, 1200);
            }

            requestAnimationFrame(tickProgress);
        }

        // Sidebar click to switch
        sbItems.forEach((item, i) => {
            item.addEventListener('click', () => {
                currentIdx = i;
                switchInstrument();
            });
        });

        // Start
        switchInstrument();
        setTimeout(tickProgress, 2000);
    }


    // ================================================================
    //  INIT NEW HERO FEATURES (called from main init)
    // ================================================================
    function initInteractiveHero() {
        initHeroTypewriter();
        initLiveSpectrum();
        initHeroMolecules();
        initCyclingMockup();
    }

})();