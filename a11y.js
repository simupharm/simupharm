/* ================================================================
   ACCESSIBILITY MODE — a11y.js
   Font size, high contrast, reduced motion, keyboard shortcuts
   ================================================================ */
(function () {
    'use strict';

    const STORAGE_KEY = 'simupharma-a11y';

    // Load saved settings
    function loadSettings() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
        } catch { return {}; }
    }

    function saveSettings(settings) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    }

    function init() {
        const settings = loadSettings();

        // Build toolbar
        const toolbar = document.createElement('div');
        toolbar.className = 'a11y-toolbar';
        toolbar.innerHTML = `
            <div class="a11y-panel" id="a11y-panel">
                <h4><i class="fas fa-universal-access"></i> Accessibility</h4>

                <div class="a11y-option">
                    <label><i class="fas fa-text-height"></i> Font Size</label>
                    <div class="font-size-controls">
                        <button data-size="normal" title="Normal">A</button>
                        <button data-size="lg" title="Large">A+</button>
                        <button data-size="xl" title="Extra Large">A++</button>
                    </div>
                </div>

                <div class="a11y-option">
                    <label><i class="fas fa-adjust"></i> High Contrast</label>
                    <button class="a11y-switch" id="a11y-contrast" aria-label="Toggle high contrast"></button>
                </div>

                <div class="a11y-option">
                    <label><i class="fas fa-flag"></i> Reduce Motion</label>
                    <button class="a11y-switch" id="a11y-motion" aria-label="Toggle reduced motion"></button>
                </div>

                <div class="a11y-shortcut-hint">
                    Press <kbd>Alt</kbd>+<kbd>A</kbd> to toggle this panel
                </div>
            </div>
            <button class="a11y-toggle" id="a11y-toggle" aria-label="Accessibility Settings">
                <i class="fas fa-universal-access"></i>
            </button>
        `;
        document.body.appendChild(toolbar);

        const panel = document.getElementById('a11y-panel');
        const toggleBtn = document.getElementById('a11y-toggle');
        const contrastBtn = document.getElementById('a11y-contrast');
        const motionBtn = document.getElementById('a11y-motion');
        const fontBtns = toolbar.querySelectorAll('[data-size]');

        // Toggle panel
        toggleBtn.addEventListener('click', () => {
            panel.classList.toggle('open');
        });

        // Keyboard shortcut Alt+A
        document.addEventListener('keydown', (e) => {
            if (e.altKey && e.key.toLowerCase() === 'a') {
                e.preventDefault();
                panel.classList.toggle('open');
            }
        });

        // Font size
        function setFontSize(size) {
            document.body.classList.remove('font-lg', 'font-xl');
            if (size === 'lg') document.body.classList.add('font-lg');
            if (size === 'xl') document.body.classList.add('font-xl');

            fontBtns.forEach(b => b.classList.toggle('active', b.dataset.size === size));
            settings.fontSize = size;
            saveSettings(settings);
        }

        fontBtns.forEach(btn => {
            btn.addEventListener('click', () => setFontSize(btn.dataset.size));
        });

        // High contrast
        function setContrast(on) {
            document.body.classList.toggle('high-contrast', on);
            contrastBtn.classList.toggle('on', on);
            settings.highContrast = on;
            saveSettings(settings);
        }

        contrastBtn.addEventListener('click', () => {
            setContrast(!settings.highContrast);
        });

        // Reduced motion
        function setReducedMotion(on) {
            document.body.classList.toggle('reduce-motion', on);
            motionBtn.classList.toggle('on', on);
            settings.reducedMotion = on;
            saveSettings(settings);
        }

        motionBtn.addEventListener('click', () => {
            setReducedMotion(!settings.reducedMotion);
        });

        // Apply saved settings
        if (settings.fontSize) setFontSize(settings.fontSize);
        else setFontSize('normal');
        if (settings.highContrast) setContrast(true);
        if (settings.reducedMotion) setReducedMotion(true);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
