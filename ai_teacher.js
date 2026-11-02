/* ================================================================
   SimuPharma AI Teacher — Proactive Welcome + Avatar + Suggestions
   
   Makes NeuroLab AI feel like a real human-like teacher:
   - Animated floating avatar that speaks and pulses
   - Context-aware welcome greeting on every page
   - Smart experiment suggestions based on current page
   - Demo mode for pitch presentations
   ================================================================ */
const AITeacher = (() => {
    'use strict';

    // ---- Configuration ----
    const WELCOME_DELAY = 1500;       // ms after page load
    const TOAST_DURATION = 8000;      // ms toast stays visible
    const SUGGESTION_DELAY = 3000;    // ms before suggestion appears
    const LS_KEY_WELCOMED = 'simupharma_welcomed_pages';
    const LS_KEY_VOICE_ON = 'neurolab_voice';

    // ---- Page-specific welcome messages ----
    const WELCOMES = {
        'index.html': {
            greeting: "Welcome to SimuPharma! 🧪",
            message: "I'm NeuroLab, your AI lab instructor. Click my icon to run experiments, analyze compounds, or ask anything about pharmaceutical analysis.",
            icon: "fas fa-flask"
        },
        'hplc_simulator.html': {
            greeting: "HPLC Simulator Ready! 💧",
            message: "Great choice — HPLC is the gold standard for drug purity testing. Try selecting a compound and adjusting the flow rate. I'll help interpret results.",
            icon: "fas fa-tint",
            suggestion: { text: "Analyze paracetamol purity", cmd: "Run HPLC analysis for paracetamol and explain the chromatogram" }
        },
        'ftir_simulator.html': {
            greeting: "FTIR Spectrometer Online! 🌊",
            message: "FTIR reveals molecular fingerprints. Each peak tells a story about functional groups. Let me guide you through interpretation.",
            icon: "fas fa-wave-square",
            suggestion: { text: "Identify aspirin functional groups", cmd: "Run FTIR for aspirin and explain each functional group peak" }
        },
        'uv_vis_simulator.html': {
            greeting: "UV-Vis Spectrophotometer! ☀️",
            message: "Perfect for quantitative analysis using Beer-Lambert Law. Try varying the concentration to see how absorbance changes.",
            icon: "fas fa-sun",
            suggestion: { text: "Build a calibration curve", cmd: "Run UV-Vis for paracetamol at concentrations 0.0005, 0.001, and 0.002 mol/L" }
        },
        'gc_simulator.html': {
            greeting: "Gas Chromatograph Ready! 🔥",
            message: "GC separates volatile compounds using temperature programming. Watch how oven temperature affects retention times.",
            icon: "fas fa-fire",
            suggestion: { text: "Analyze volatile solvents", cmd: "Run GC analysis for caffeine and explain the temperature program" }
        },
        'mass_spec_simulator.html': {
            greeting: "Mass Spectrometer Armed! ⚛️",
            message: "Mass spec reveals molecular weight and fragmentation patterns. The m/z values are clues to molecular structure.",
            icon: "fas fa-atom",
            suggestion: { text: "Determine molecular weight", cmd: "Run mass spec for ibuprofen in EI mode and explain the fragmentation pattern" }
        },
        'polarimeter_simulator.html': {
            greeting: "Polarimeter Aligned! 🔄",
            message: "Polarimetry measures optical rotation of chiral compounds. Essential for enantiomeric purity of drugs like ibuprofen.",
            icon: "fas fa-sync-alt",
            suggestion: { text: "Measure optical rotation", cmd: "Measure the optical rotation of dextrose and explain chirality" }
        },
        'psa_simulator.html': {
            greeting: "Particle Size Analyzer! 🔬",
            message: "Particle size directly impacts drug dissolution and bioavailability. Smaller particles = faster absorption.",
            icon: "fas fa-microscope",
            suggestion: { text: "Analyze particle distribution", cmd: "Run particle size analysis and explain D10, D50, D90 values" }
        },
        'quiz.html': {
            greeting: "Quiz Time! 🎯",
            message: "Let's test your knowledge! I'll grade your answers and explain the concepts behind each question.",
            icon: "fas fa-question-circle"
        },
        'instruments.html': {
            greeting: "Instrument Gallery! 🏗️",
            message: "Browse all 7 instruments. Each uses real physics engines — not just animations. Click any to start experimenting.",
            icon: "fas fa-th-large"
        },
        'dashboard.html': {
            greeting: "Your Dashboard! 📊",
            message: "Track your progress across all instruments. I'll suggest what to study next based on your mastery levels.",
            icon: "fas fa-chart-bar"
        },
        'leaderboard.html': {
            greeting: "Leaderboard! 🏆",
            message: "See how you rank against other students. Earn XP by running experiments and completing quizzes.",
            icon: "fas fa-trophy"
        },
        'faculty.html': {
            greeting: "Faculty Dashboard! 🎓",
            message: "Track student progress, view mastery heatmaps, and generate NAAC reports for your institution.",
            icon: "fas fa-chalkboard-teacher"
        }
    };

    // ---- State ----
    let avatarEl = null;
    let toastEl = null;
    let initialized = false;

    // ---- Create Floating Avatar ----
    function createAvatar() {
        avatarEl = document.createElement('div');
        avatarEl.id = 'ai-teacher-avatar';
        avatarEl.innerHTML = `
            <div class="ai-avatar-inner">
                <div class="ai-avatar-face">
                    <i class="fas fa-brain"></i>
                </div>
                <div class="ai-avatar-ring"></div>
                <div class="ai-avatar-pulse"></div>
            </div>
            <div class="ai-avatar-label">NeuroLab</div>
        `;

        // Click to open chat
        avatarEl.addEventListener('click', () => {
            const toggleBtn = document.querySelector('.assistant-toggle');
            if (toggleBtn) toggleBtn.click();
        });

        document.body.appendChild(avatarEl);
    }

    // ---- Show Welcome Toast ----
    function showWelcomeToast(welcome) {
        if (toastEl) toastEl.remove();

        toastEl = document.createElement('div');
        toastEl.className = 'ai-welcome-toast';
        toastEl.innerHTML = `
            <div class="toast-icon"><i class="${welcome.icon}"></i></div>
            <div class="toast-content">
                <strong>${welcome.greeting}</strong>
                <p>${welcome.message}</p>
            </div>
            <button class="toast-close" aria-label="Close">
                <i class="fas fa-times"></i>
            </button>
        `;

        const closeBtn = toastEl.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            toastEl.classList.add('toast-exit');
            setTimeout(() => toastEl.remove(), 300);
        });

        document.body.appendChild(toastEl);

        // Trigger entrance animation
        requestAnimationFrame(() => {
            requestAnimationFrame(() => toastEl.classList.add('toast-visible'));
        });

        // Auto-dismiss
        setTimeout(() => {
            if (toastEl && toastEl.parentElement) {
                toastEl.classList.add('toast-exit');
                setTimeout(() => { if (toastEl) toastEl.remove(); }, 300);
            }
        }, TOAST_DURATION);

        // Speak the greeting if voice is enabled
        if (localStorage.getItem(LS_KEY_VOICE_ON) !== 'off' && typeof VoiceEngine !== 'undefined') {
            setTimeout(() => {
                if (avatarEl) avatarEl.classList.add('speaking');
                VoiceEngine.speak(`${welcome.greeting.replace(/[🧪💧🌊☀️🔥⚛️🔄🔬🎯🏗️📊🏆🎓]/g, '')} ${welcome.message}`).then(() => {
                    if (avatarEl) avatarEl.classList.remove('speaking');
                });
            }, 500);
        }
    }

    // ---- Show Experiment Suggestion ----
    function showSuggestion(suggestion) {
        if (!suggestion) return;

        const sugEl = document.createElement('div');
        sugEl.className = 'ai-suggestion-flyout';
        sugEl.innerHTML = `
            <div class="sug-icon"><i class="fas fa-lightbulb"></i></div>
            <div class="sug-body">
                <strong>Try this experiment:</strong>
                <p>${suggestion.text}</p>
            </div>
            <button class="sug-run-btn">
                <i class="fas fa-play"></i> Run
            </button>
        `;

        sugEl.querySelector('.sug-run-btn').addEventListener('click', () => {
            // Open chat and auto-send the command
            const toggleBtn = document.querySelector('.assistant-toggle');
            const chatWindow = document.querySelector('.assistant-window');
            if (toggleBtn && chatWindow && !chatWindow.classList.contains('open')) {
                toggleBtn.click();
            }
            setTimeout(() => {
                const input = document.getElementById('assistant-input');
                const sendBtn = document.getElementById('assistant-send');
                if (input && sendBtn) {
                    input.value = suggestion.cmd;
                    sendBtn.click();
                }
            }, 500);
            sugEl.classList.add('toast-exit');
            setTimeout(() => sugEl.remove(), 300);
        });

        document.body.appendChild(sugEl);
        requestAnimationFrame(() => {
            requestAnimationFrame(() => sugEl.classList.add('toast-visible'));
        });

        // Auto-dismiss after 12s
        setTimeout(() => {
            if (sugEl && sugEl.parentElement) {
                sugEl.classList.add('toast-exit');
                setTimeout(() => { if (sugEl) sugEl.remove(); }, 300);
            }
        }, 12000);
    }

    // ---- Detect Current Page ----
    function getCurrentPage() {
        const path = window.location.pathname.toLowerCase();
        return path.split('/').pop() || 'index.html';
    }

    // ---- Check if Already Welcomed on This Page ----
    function hasBeenWelcomed(page) {
        try {
            const welcomed = JSON.parse(localStorage.getItem(LS_KEY_WELCOMED) || '{}');
            const today = new Date().toDateString();
            return welcomed[page] === today;
        } catch { return false; }
    }

    function markWelcomed(page) {
        try {
            const welcomed = JSON.parse(localStorage.getItem(LS_KEY_WELCOMED) || '{}');
            welcomed[page] = new Date().toDateString();
            localStorage.setItem(LS_KEY_WELCOMED, JSON.stringify(welcomed));
        } catch { /* ignore */ }
    }

    // ---- Demo Mode (for Pitch) ----
    function startDemo() {
        // Open chat
        const toggleBtn = document.querySelector('.assistant-toggle');
        const chatWindow = document.querySelector('.assistant-window');
        if (toggleBtn && chatWindow && !chatWindow.classList.contains('open')) {
            toggleBtn.click();
        }

        // Show welcome toast
        showWelcomeToast({
            greeting: "🎬 Live Demo Mode!",
            message: "Watch NeuroLab AI autonomously analyze a drug compound with real physics engines...",
            icon: "fas fa-play-circle"
        });

        // Auto-send multi-instrument analysis
        setTimeout(() => {
            const input = document.getElementById('assistant-input');
            const sendBtn = document.getElementById('assistant-send');
            if (input && sendBtn) {
                input.value = "Run a complete pharmaceutical analysis of paracetamol: UV-Vis spectrum, FTIR for functional groups, HPLC purity check, and Mass Spec for molecular weight confirmation. Show me everything.";
                sendBtn.click();
            }
        }, 2000);
    }

    // ---- Initialize ----
    function init() {
        if (initialized) return;
        initialized = true;

        const page = getCurrentPage();
        const welcome = WELCOMES[page];

        // Create avatar on all pages
        createAvatar();

        // Show welcome if not already done today for this page
        if (welcome && !hasBeenWelcomed(page)) {
            setTimeout(() => {
                showWelcomeToast(welcome);
                markWelcomed(page);
            }, WELCOME_DELAY);

            // Show suggestion after welcome
            if (welcome.suggestion) {
                setTimeout(() => {
                    showSuggestion(welcome.suggestion);
                }, WELCOME_DELAY + SUGGESTION_DELAY + 1000);
            }
        }
    }

    // Start when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        setTimeout(init, 200);
    }

    // ---- Public API ----
    return {
        startDemo,
        showSuggestion,
        showWelcomeToast,
        get avatar() { return avatarEl; }
    };
})();
