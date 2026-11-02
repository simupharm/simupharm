/* ================================================================
   SimuPharma Voice Engine — Jarvis-Like TTS
   
   Shared by both NeuroLab AI and Guided Teacher.
   Uses Web Speech API SpeechSynthesis with a deep male voice.
   ================================================================ */
const VoiceEngine = (() => {
    'use strict';

    // ---- Configuration ----
    const CONFIG = {
        pitch: 0.85,       // Slightly lower for Jarvis feel
        rate: 0.92,        // Measured, confident pace
        volume: 1.0,
        // Preferred voices in order (deep male English voices)
        preferredVoices: [
            'Google UK English Male',
            'Microsoft David',
            'Microsoft David Desktop',
            'Daniel',
            'Microsoft Mark',
            'Google US English',
            'Alex',
            'en-GB-Neural2-B'
        ]
    };

    let enabled = true;
    let selectedVoice = null;
    let speaking = false;
    let currentUtterance = null;
    let onSpeakStart = null;
    let onSpeakEnd = null;
    let voicesLoaded = false;

    // ---- Find the best Jarvis-like voice ----
    function findBestVoice() {
        const voices = speechSynthesis.getVoices();
        if (!voices.length) return null;

        // Try preferred voices first
        for (const preferred of CONFIG.preferredVoices) {
            const found = voices.find(v =>
                v.name.includes(preferred) || v.voiceURI.includes(preferred)
            );
            if (found) return found;
        }

        // Fallback: find any English male voice
        const englishMale = voices.find(v =>
            v.lang.startsWith('en') && v.name.toLowerCase().includes('male')
        );
        if (englishMale) return englishMale;

        // Last resort: any English voice
        const english = voices.find(v => v.lang.startsWith('en'));
        return english || voices[0];
    }

    // ---- Initialize voices (they load asynchronously) ----
    function initVoices() {
        if (typeof speechSynthesis === 'undefined') {
            console.warn('[VoiceEngine] Speech Synthesis not supported');
            enabled = false;
            return;
        }

        const loadVoices = () => {
            selectedVoice = findBestVoice();
            voicesLoaded = true;
            if (selectedVoice) {
                console.log(`[VoiceEngine] Selected voice: ${selectedVoice.name}`);
            }
        };

        // Voices may already be loaded
        if (speechSynthesis.getVoices().length > 0) {
            loadVoices();
        }
        // Chrome loads voices asynchronously
        speechSynthesis.addEventListener('voiceschanged', loadVoices);
    }

    // ---- Speak text ----
    function speak(text, options = {}) {
        if (!enabled || typeof speechSynthesis === 'undefined') return Promise.resolve();

        return new Promise((resolve) => {
            // Cancel any ongoing speech
            stop();

            // Clean text for speech (remove markdown/emoji)
            const cleanText = text
                .replace(/[🧠🔬📊✅⚠️🎯⚖️🔍📋🧬🔄💧☀️🔥⚛️🏆👋🗣️]/g, '')
                .replace(/\*\*(.+?)\*\*/g, '$1')
                .replace(/\*(.+?)\*/g, '$1')
                .replace(/`(.+?)`/g, '$1')
                .replace(/#{1,4}\s/g, '')
                .replace(/\n+/g, '. ')
                .replace(/\s+/g, ' ')
                .trim();

            if (!cleanText) { resolve(); return; }

            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.voice = selectedVoice;
            utterance.pitch = options.pitch || CONFIG.pitch;
            utterance.rate = options.rate || CONFIG.rate;
            utterance.volume = options.volume || CONFIG.volume;
            currentUtterance = utterance;

            utterance.onstart = () => {
                speaking = true;
                if (onSpeakStart) onSpeakStart();
            };

            utterance.onend = () => {
                speaking = false;
                currentUtterance = null;
                if (onSpeakEnd) onSpeakEnd();
                resolve();
            };

            utterance.onerror = (e) => {
                speaking = false;
                currentUtterance = null;
                if (e.error !== 'canceled') {
                    console.warn('[VoiceEngine] Speech error:', e.error);
                }
                resolve();
            };

            speechSynthesis.speak(utterance);
        });
    }

    // ---- Stop speaking ----
    function stop() {
        if (typeof speechSynthesis !== 'undefined') {
            speechSynthesis.cancel();
        }
        speaking = false;
        currentUtterance = null;
    }

    // ---- Toggle enable/disable ----
    function toggle() {
        enabled = !enabled;
        if (!enabled) stop();
        return enabled;
    }

    // Init on load
    initVoices();

    // ---- Public API ----
    return {
        speak,
        stop,
        toggle,
        get enabled() { return enabled; },
        set enabled(val) { enabled = val; if (!val) stop(); },
        get speaking() { return speaking; },
        set onSpeakStart(fn) { onSpeakStart = fn; },
        set onSpeakEnd(fn) { onSpeakEnd = fn; },
        get voiceReady() { return voicesLoaded && !!selectedVoice; },
        get voiceName() { return selectedVoice?.name || 'Default'; }
    };
})();
