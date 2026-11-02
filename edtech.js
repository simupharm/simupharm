/* ================================================================
   SimuPharma EdTech Engine — XP, Badges, Streaks & Lab Notebook
   Provides gamification and lab documentation across all pages.
   ================================================================ */

const EdTech = (() => {
    const LS_KEY = 'simupharma_edtech';

    // ---- Default profile ----
    const DEFAULT = {
        xp: 0,
        level: 1,
        streak: 0,
        lastActive: null,
        badges: [],
        notebooks: [],
        instrumentsUsed: [],
        experimentsCompleted: 0,
        quizzesPassed: 0,
        totalStudyMinutes: 0
    };

    // ---- Badge definitions ----
    const BADGES = [
        { id: 'first_sim', name: 'First Simulation', icon: '🧪', desc: 'Run your first simulation', condition: p => p.experimentsCompleted >= 1, xp: 50 },
        { id: 'explorer', name: 'Explorer', icon: '🔍', desc: 'Use 3 different instruments', condition: p => p.instrumentsUsed.length >= 3, xp: 100 },
        { id: 'hplc_master', name: 'HPLC Expert', icon: '💧', desc: 'Complete 5 HPLC experiments', condition: p => (p.instrumentXP?.hplc || 0) >= 250, xp: 150 },
        { id: 'streak_3', name: 'Hat Trick', icon: '🔥', desc: '3-day study streak', condition: p => p.streak >= 3, xp: 75 },
        { id: 'streak_7', name: 'Weekly Warrior', icon: '⚡', desc: '7-day study streak', condition: p => p.streak >= 7, xp: 200 },
        { id: 'quiz_ace', name: 'Quiz Ace', icon: '🏆', desc: 'Score 90%+ on 3 quizzes', condition: p => p.quizzesPassed >= 3, xp: 150 },
        { id: 'notebook_5', name: 'Lab Scribe', icon: '📓', desc: 'Create 5 lab notebook entries', condition: p => p.notebooks.length >= 5, xp: 100 },
        { id: 'night_owl', name: 'Night Owl', icon: '🦉', desc: 'Study after midnight', condition: p => p.nightStudy === true, xp: 50 },
        { id: 'all_instruments', name: 'Lab Master', icon: '🎓', desc: 'Use all 7 instruments', condition: p => p.instrumentsUsed.length >= 7, xp: 500 },
        { id: 'guided_complete', name: 'Guided Scholar', icon: '📘', desc: 'Complete a guided experiment', condition: p => (p.guided_completed || 0) >= 1, xp: 100 },
    ];

    // ---- XP per level ----
    function xpForLevel(level) { return Math.floor(100 * Math.pow(1.5, level - 1)); }

    // ---- Load / Save ----
    function load() {
        try {
            const raw = localStorage.getItem(LS_KEY);
            return raw ? { ...DEFAULT, ...JSON.parse(raw) } : { ...DEFAULT };
        } catch { return { ...DEFAULT }; }
    }

    function save(profile) {
        localStorage.setItem(LS_KEY, JSON.stringify(profile));
    }

    // ---- Public API ----
    function getProfile() { return load(); }

    function addXP(amount, source = 'general') {
        const p = load();
        p.xp += amount;
        // Level up check
        while (p.xp >= xpForLevel(p.level)) {
            p.xp -= xpForLevel(p.level);
            p.level++;
            showToast(`🎉 Level ${p.level}!`, `You reached Level ${p.level}. Keep going!`);
        }
        // Record instrument XP
        if (source !== 'general') {
            if (!p.instrumentXP) p.instrumentXP = {};
            p.instrumentXP[source] = (p.instrumentXP[source] || 0) + amount;
        }
        save(p);
        checkBadges(p);
        updateUI(p);
        return p;
    }

    function recordInstrument(instrumentId) {
        const p = load();
        if (!p.instrumentsUsed.includes(instrumentId)) {
            p.instrumentsUsed.push(instrumentId);
            addXP(25, instrumentId);
        }
        save(p);
        checkBadges(p);
    }

    function recordExperiment(instrumentId) {
        const p = load();
        p.experimentsCompleted++;
        save(p);
        addXP(50, instrumentId || 'general');
        checkBadges(p);
    }

    function recordQuiz(score, total) {
        const p = load();
        if (score / total >= 0.9) p.quizzesPassed++;
        save(p);
        addXP(Math.round(score / total * 100), 'quiz');
        checkBadges(p);
    }

    function updateStreak() {
        const p = load();
        const today = new Date().toDateString();
        const yesterday = new Date(Date.now() - 86400000).toDateString();

        if (p.lastActive === today) return; // Already counted
        if (p.lastActive === yesterday) {
            p.streak++;
        } else if (p.lastActive !== today) {
            p.streak = 1;
        }
        p.lastActive = today;

        // Night owl check
        if (new Date().getHours() >= 0 && new Date().getHours() < 5) {
            p.nightStudy = true;
        }

        save(p);
        checkBadges(p);
    }

    function checkBadges(profile) {
        const p = profile || load();
        let newBadges = false;
        BADGES.forEach(badge => {
            if (!p.badges.includes(badge.id) && badge.condition(p)) {
                p.badges.push(badge.id);
                newBadges = true;
                showToast(`${badge.icon} Badge Unlocked!`, badge.name);
                p.xp += badge.xp;
            }
        });
        if (newBadges) save(p);
    }

    // ---- Lab Notebook ----
    function createNotebookEntry(data) {
        const p = load();
        const entry = {
            id: Date.now(),
            date: new Date().toISOString(),
            instrument: data.instrument || 'Unknown',
            title: data.title || 'Lab Entry',
            objective: data.objective || '',
            procedure: data.procedure || '',
            observations: data.observations || '',
            results: data.results || '',
            conclusion: data.conclusion || '',
            parameters: data.parameters || {}
        };
        p.notebooks.push(entry);
        save(p);
        checkBadges(p);
        addXP(20, data.instrument?.toLowerCase() || 'general');
        return entry;
    }

    function getNotebooks() { return load().notebooks; }

    function exportNotebookPDF(entryId) {
        const p = load();
        const entry = p.notebooks.find(n => n.id === entryId);
        if (!entry) return;

        // Simple text export (jsPDF if available, else text)
        const text = `
═══════════════════════════════════════════
    SimuPharma — Digital Lab Notebook
═══════════════════════════════════════════

Title:       ${entry.title}
Date:        ${new Date(entry.date).toLocaleDateString()}
Instrument:  ${entry.instrument}

─── Objective ───
${entry.objective}

─── Procedure ───
${entry.procedure}

─── Observations ───
${entry.observations}

─── Results ───
${entry.results}
${entry.parameters ? '\nParameters: ' + JSON.stringify(entry.parameters, null, 2) : ''}

─── Conclusion ───
${entry.conclusion}

═══════════════════════════════════════════
    Generated by SimuPharma EdTech Engine
═══════════════════════════════════════════
`;
        // Download as text
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `lab_notebook_${entry.instrument}_${entry.id}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    }

    // ---- Leaderboard (real API-backed) ----
    async function getLeaderboard() {
        try {
            const res = await fetch('/api/v1/leaderboard');
            if (res.ok) {
                const data = await res.json();
                if (data.leaderboard && data.leaderboard.length > 0) {
                    return data.leaderboard.map((entry, i) => ({
                        name: entry.name,
                        xp: Math.round(entry.avg_mastery_pct * 10),
                        level: Math.max(1, Math.floor(entry.avg_mastery_pct / 20) + 1),
                        badges: Math.floor(entry.quizzes_completed / 2),
                        isUser: false,
                    }));
                }
            }
        } catch { /* Fall through to local data */ }

        // Fallback: local profile only
        const p = load();
        const totalXP = p.xp + (p.level - 1) * 100;
        return [
            { name: 'You', xp: totalXP, level: p.level, badges: p.badges.length, isUser: true },
        ];
    }

    // ---- Toast Notification ----
    function showToast(title, message) {
        const existing = document.querySelector('.edtech-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = 'edtech-toast';
        toast.innerHTML = `
            <div class="edtech-toast-inner">
                <strong>${title}</strong>
                <span>${message}</span>
            </div>
        `;
        document.body.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 3500);
    }

    // ---- Floating XP Bar UI (optional) ----
    function updateUI(profile) {
        const bar = document.getElementById('edtech-xp-bar');
        if (!bar) return;
        const p = profile || load();
        const needed = xpForLevel(p.level);
        const pct = Math.round((p.xp / needed) * 100);
        bar.querySelector('.xp-fill').style.width = pct + '%';
        bar.querySelector('.xp-level').textContent = `Lv. ${p.level}`;
        bar.querySelector('.xp-text').textContent = `${p.xp} / ${needed} XP`;
    }

    function injectXPBar() {
        if (document.getElementById('edtech-xp-bar')) return;

        const p = load();
        const needed = xpForLevel(p.level);
        const pct = Math.round((p.xp / needed) * 100);

        const bar = document.createElement('div');
        bar.id = 'edtech-xp-bar';
        bar.innerHTML = `
            <span class="xp-level">Lv. ${p.level}</span>
            <div class="xp-track"><div class="xp-fill" style="width:${pct}%"></div></div>
            <span class="xp-text">${p.xp} / ${needed} XP</span>
            <span class="xp-streak">${p.streak > 0 ? '🔥' + p.streak : ''}</span>
        `;
        document.body.appendChild(bar);
    }

    // ---- Initialize ----
    function init() {
        updateStreak();
        injectXPBar();
        injectStyles();
    }

    function injectStyles() {
        if (document.getElementById('edtech-styles')) return;
        const style = document.createElement('style');
        style.id = 'edtech-styles';
        style.textContent = `
            #edtech-xp-bar {
                position: fixed;
                bottom: 24px;
                left: 24px;
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 8px 14px;
                background: rgba(15, 23, 42, 0.92);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(59, 130, 246, 0.15);
                border-radius: 12px;
                z-index: 8000;
                font-family: 'Inter', system-ui, sans-serif;
                font-size: 0.72rem;
                color: #94a3b8;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }
            #edtech-xp-bar .xp-level {
                font-weight: 700;
                color: #60a5fa;
                font-size: 0.75rem;
            }
            #edtech-xp-bar .xp-track {
                width: 80px;
                height: 6px;
                background: rgba(255,255,255,0.1);
                border-radius: 3px;
                overflow: hidden;
            }
            #edtech-xp-bar .xp-fill {
                height: 100%;
                background: linear-gradient(90deg, #2563eb, #7c3aed);
                border-radius: 3px;
                transition: width 0.5s ease;
            }
            #edtech-xp-bar .xp-streak {
                font-size: 0.8rem;
            }
            .edtech-toast {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                transform: translateX(120%);
                transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            }
            .edtech-toast.show {
                transform: translateX(0);
            }
            .edtech-toast-inner {
                background: rgba(15, 23, 42, 0.95);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 14px;
                padding: 14px 20px;
                display: flex;
                flex-direction: column;
                gap: 3px;
                font-family: 'Inter', system-ui, sans-serif;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);
                min-width: 220px;
            }
            .edtech-toast-inner strong {
                font-size: 0.85rem;
                color: #f1f5f9;
            }
            .edtech-toast-inner span {
                font-size: 0.75rem;
                color: #94a3b8;
            }
        `;
        document.head.appendChild(style);
    }

    // Auto-init on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    return {
        getProfile,
        addXP,
        recordInstrument,
        recordExperiment,
        recordQuiz,
        updateStreak,
        createNotebookEntry,
        getNotebooks,
        exportNotebookPDF,
        getLeaderboard,
        getBadges: () => BADGES,
        showToast,
        xpForLevel
    };
})();
