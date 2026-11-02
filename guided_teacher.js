/* ================================================================
   SimuPharma Guided Teacher — Reusable Step-by-Step Engine
   
   Works with any simulator. Each simulator provides a steps config.
   Uses VoiceEngine for Jarvis-like narration.
   ================================================================ */
const GuidedTeacher = (() => {
    'use strict';

    let steps = [];
    let currentStep = 0;
    let active = false;
    let panel = null;
    let spotlight = null;
    let overlay = null;
    let voiceEnabled = true;
    let experimentTitle = '';
    let onComplete = null;

    // ---- Create UI ----
    function createUI() {
        // Launch button
        const launchBtn = document.createElement('button');
        launchBtn.className = 'gt-launch-btn';
        launchBtn.id = 'gt-launch';
        launchBtn.innerHTML = '<i class="fas fa-chalkboard-teacher"></i>';
        document.body.appendChild(launchBtn);

        // Teacher panel
        panel = document.createElement('div');
        panel.className = 'guided-teacher-panel';
        panel.id = 'gt-panel';
        // Add minimize tab (visible when minimized)
        const minTab = document.createElement('div');
        minTab.className = 'gt-minimize-tab';
        minTab.innerHTML = '<i class="fas fa-chalkboard-teacher"></i><span>Teacher</span>';
        panel.appendChild(minTab);
        document.body.appendChild(panel);

        // Click minimize tab to expand
        minTab.addEventListener('click', (e) => {
            e.stopPropagation();
            panel.classList.remove('minimized');
        });
        // Click anywhere on minimized panel to expand
        panel.addEventListener('click', (e) => {
            if (panel.classList.contains('minimized')) {
                panel.classList.remove('minimized');
            }
        });

        // Spotlight overlay
        overlay = document.createElement('div');
        overlay.className = 'gt-overlay';
        overlay.id = 'gt-overlay';
        document.body.appendChild(overlay);

        spotlight = document.createElement('div');
        spotlight.className = 'gt-spotlight';
        spotlight.id = 'gt-spotlight';
        spotlight.style.display = 'none';
        document.body.appendChild(spotlight);

        // Event: launch
        launchBtn.addEventListener('click', () => {
            if (active) {
                close();
            } else {
                start();
            }
        });
    }

    // ---- Render current step ----
    function renderStep() {
        if (!panel || currentStep >= steps.length) return;

        const step = steps[currentStep];
        const progress = ((currentStep + 1) / steps.length * 100).toFixed(0);
        const isLast = currentStep === steps.length - 1;
        const isFirst = currentStep === 0;

        panel.innerHTML = `
            <div class="gt-header">
                <div class="gt-avatar" id="gt-avatar">🧑‍🔬</div>
                <div class="gt-header-info">
                    <h3>Lab Teacher</h3>
                    <p>${experimentTitle}</p>
                </div>
                <div class="gt-header-actions">
                    <button class="gt-header-btn" id="gt-minimize" title="Minimize">
                        <i class="fas fa-window-minimize"></i>
                    </button>
                    <button class="gt-header-btn ${voiceEnabled ? 'active' : ''}" id="gt-voice-toggle" title="Toggle voice">
                        <i class="fas fa-volume-${voiceEnabled ? 'up' : 'mute'}"></i>
                    </button>
                    <button class="gt-header-btn" id="gt-close" title="Close teacher">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>

            <div class="gt-progress">
                <div class="gt-progress-info">
                    <span class="gt-step-counter">Step ${currentStep + 1} of ${steps.length}</span>
                    <span class="gt-progress-pct">${progress}%</span>
                </div>
                <div class="gt-progress-bar">
                    <div class="gt-progress-fill" style="width: ${progress}%"></div>
                </div>
            </div>

            <div class="gt-content">
                <div class="gt-step-title">
                    <span class="step-icon"><i class="fas fa-${step.icon || 'flask'}"></i></span>
                    ${step.title}
                </div>

                <div class="gt-instruction">${step.instruction}</div>

                ${step.theory ? `
                    <div class="gt-theory" id="gt-theory">
                        <div class="gt-theory-header">
                            <i class="fas fa-chevron-right"></i>
                            <span>💡 Why? — Science Behind This Step</span>
                        </div>
                        <div class="gt-theory-content">
                            <p>${step.theory}</p>
                        </div>
                    </div>
                ` : ''}

                ${step.action ? `
                    <div class="gt-action">
                        <div class="gt-action-icon"><i class="fas fa-hand-pointer"></i></div>
                        <div class="gt-action-text">${step.action}</div>
                    </div>
                ` : ''}

                ${isLast && step.completion ? `
                    <div class="gt-completion">
                        <div class="gt-completion-icon">🏆</div>
                        <h3>${step.completion.title || 'Experiment Complete!'}</h3>
                        <p>${step.completion.message || ''}</p>
                        <div class="gt-score">
                            <i class="fas fa-star"></i> Guided experiment completed successfully
                        </div>
                    </div>
                ` : ''}
            </div>

            <div class="gt-footer">
                ${!isFirst ? '<button class="gt-btn gt-btn-prev" id="gt-prev"><i class="fas fa-arrow-left"></i> Back</button>' : ''}
                <button class="gt-btn gt-btn-next" id="gt-next">
                    ${isLast ? '<i class="fas fa-check"></i> Finish' : 'Next Step <i class="fas fa-arrow-right"></i>'}
                </button>
            </div>
        `;

        // Events
        const closeBtn = panel.querySelector('#gt-close');
        closeBtn?.addEventListener('click', close);

        const minimizeBtn = panel.querySelector('#gt-minimize');
        minimizeBtn?.addEventListener('click', () => {
            panel.classList.add('minimized');
        });

        const prevBtn = panel.querySelector('#gt-prev');
        prevBtn?.addEventListener('click', prevStep);

        const nextBtn = panel.querySelector('#gt-next');
        nextBtn?.addEventListener('click', () => {
            if (isLast) {
                complete();
            } else {
                nextStep();
            }
        });

        const voiceToggle = panel.querySelector('#gt-voice-toggle');
        voiceToggle?.addEventListener('click', () => {
            voiceEnabled = !voiceEnabled;
            if (typeof VoiceEngine !== 'undefined') VoiceEngine.enabled = voiceEnabled;
            renderStep(); // Re-render to update icon
        });

        const theoryCard = panel.querySelector('#gt-theory');
        theoryCard?.addEventListener('click', () => {
            theoryCard.classList.toggle('expanded');
        });

        // Highlight target element
        updateSpotlight(step.highlight);

        // Speak instruction
        if (voiceEnabled && typeof VoiceEngine !== 'undefined' && step.speak) {
            const avatar = panel.querySelector('#gt-avatar');
            VoiceEngine.onSpeakStart = () => avatar?.classList.add('speaking');
            VoiceEngine.onSpeakEnd = () => avatar?.classList.remove('speaking');
            VoiceEngine.speak(step.speak);
        }
    }

    // ---- Spotlight an element ----
    function updateSpotlight(selector) {
        if (!spotlight) return;

        if (!selector) {
            spotlight.style.display = 'none';
            overlay.classList.remove('active');
            return;
        }

        const target = document.querySelector(selector);
        if (!target) {
            spotlight.style.display = 'none';
            overlay.classList.remove('active');
            return;
        }

        const rect = target.getBoundingClientRect();
        const pad = 8;

        spotlight.style.display = 'block';
        spotlight.style.top = (rect.top - pad) + 'px';
        spotlight.style.left = (rect.left - pad) + 'px';
        spotlight.style.width = (rect.width + pad * 2) + 'px';
        spotlight.style.height = (rect.height + pad * 2) + 'px';
        overlay.classList.add('active');

        // Scroll element into view if needed
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // ---- Navigation ----
    function nextStep() {
        if (currentStep < steps.length - 1) {
            if (typeof VoiceEngine !== 'undefined') VoiceEngine.stop();
            currentStep++;
            renderStep();
        }
    }

    function prevStep() {
        if (currentStep > 0) {
            if (typeof VoiceEngine !== 'undefined') VoiceEngine.stop();
            currentStep--;
            renderStep();
        }
    }

    // ---- Start / Close / Complete ----
    function start() {
        currentStep = 0;
        active = true;
        panel.classList.add('active');
        renderStep();

        const launchBtn = document.getElementById('gt-launch');
        if (launchBtn) {
            launchBtn.innerHTML = '<i class="fas fa-times"></i>';
        }
    }

    function close() {
        active = false;
        panel.classList.remove('active');
        overlay.classList.remove('active');
        if (spotlight) spotlight.style.display = 'none';
        if (typeof VoiceEngine !== 'undefined') VoiceEngine.stop();

        const launchBtn = document.getElementById('gt-launch');
        if (launchBtn) {
            launchBtn.innerHTML = '<i class="fas fa-chalkboard-teacher"></i>';
        }
    }

    function complete() {
        if (typeof VoiceEngine !== 'undefined') {
            VoiceEngine.speak('Congratulations! You have successfully completed this guided experiment.');
        }

        // Save completion to localStorage
        const completions = JSON.parse(localStorage.getItem('gt_completions') || '{}');
        completions[experimentTitle] = {
            completed: true,
            date: new Date().toISOString(),
            steps: steps.length
        };
        localStorage.setItem('gt_completions', JSON.stringify(completions));

        if (onComplete) onComplete();

        setTimeout(() => close(), 4000);
    }

    // ---- Public: Initialize with steps config ----
    function init(config) {
        steps = config.steps || [];
        experimentTitle = config.title || 'Guided Experiment';
        onComplete = config.onComplete || null;
        voiceEnabled = config.voiceEnabled !== false;

        createUI();
    }

    return { init, start, close, nextStep, prevStep };
})();
