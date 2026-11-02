/* ================================================================
   STUDENT DASHBOARD — Logic & Charts
   localStorage-based learning analytics
   ================================================================ */
(function () {
    'use strict';

    const STORAGE = {
        PROGRESS: 'simupharma-progress',
        ACTIVITY: 'simupharma-activity'
    };

    const INSTRUMENTS = [
        { id: 'hplc', name: 'HPLC', icon: 'fa-vial', color: 'blue' },
        { id: 'ftir', name: 'FTIR', icon: 'fa-wave-square', color: 'purple' },
        { id: 'uv-vis', name: 'UV-Vis', icon: 'fa-sun', color: 'cyan' },
        { id: 'gc', name: 'Gas Chromatography', icon: 'fa-fire', color: 'orange' },
        { id: 'mass-spec', name: 'Mass Spectrometry', icon: 'fa-atom', color: 'pink' },
        { id: 'polarimeter', name: 'Polarimeter', icon: 'fa-compass', color: 'green' }
    ];

    function getProgress() {
        try { return JSON.parse(localStorage.getItem(STORAGE.PROGRESS)) || {}; } catch { return {}; }
    }

    function getActivity() {
        try { return JSON.parse(localStorage.getItem(STORAGE.ACTIVITY)) || []; } catch { return []; }
    }

    // ---- Stats ----
    function updateStats() {
        const progress = getProgress();
        const activity = getActivity();

        const explored = Object.keys(progress).filter(k => progress[k]?.visited).length;
        const quizzes = activity.filter(a => a.type === 'quiz').length;
        const scores = activity.filter(a => a.type === 'quiz' && a.score != null).map(a => a.score);
        const avgScore = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;
        const totalTime = Object.values(progress).reduce((sum, p) => sum + (p.timeSpent || 0), 0);

        const statInstr = document.getElementById('stat-instruments');
        const statQuizzes = document.getElementById('stat-quizzes');
        const statAvg = document.getElementById('stat-avg-score');
        const statTime = document.getElementById('stat-time');

        if (statInstr) animateNumber(statInstr, explored);
        if (statQuizzes) animateNumber(statQuizzes, quizzes);
        if (statAvg) statAvg.textContent = avgScore + '%';
        if (statTime) statTime.textContent = totalTime >= 60 ? Math.round(totalTime / 60) + ' hrs' : totalTime + ' min';
    }

    function animateNumber(el, target) {
        let current = 0;
        const step = Math.max(1, Math.ceil(target / 30));
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current;
        }, 40);
    }

    // ---- Activity Feed ----
    function renderActivity() {
        const list = document.getElementById('activity-list');
        if (!list) return;

        let activity = getActivity();

        // Add some demo activity if empty
        if (activity.length === 0) {
            activity = [
                { type: 'explore', name: 'HPLC', time: Date.now() - 300000 },
                { type: 'sim', name: 'HPLC Simulator', time: Date.now() - 600000 },
                { type: 'explore', name: 'FTIR', time: Date.now() - 900000 },
                { type: 'quiz', name: 'Instrument Quiz', score: 85, time: Date.now() - 1800000 },
                { type: 'explore', name: 'UV-Vis', time: Date.now() - 3600000 },
            ];
            localStorage.setItem(STORAGE.ACTIVITY, JSON.stringify(activity));
        }

        const recent = activity.slice(-8).reverse();

        list.innerHTML = recent.map(a => {
            const typeClass = a.type;
            const icon = a.type === 'explore' ? 'fa-flask' : a.type === 'quiz' ? 'fa-trophy' : 'fa-play';
            const desc = a.type === 'quiz' ? `Score: ${a.score}%` : a.type === 'sim' ? 'Simulation run' : 'Page visited';
            const timeAgo = getTimeAgo(a.time);

            return `
                <div class="activity-item">
                    <div class="activity-icon ${typeClass}"><i class="fas ${icon}"></i></div>
                    <div class="activity-info">
                        <strong>${a.name}</strong>
                        <small>${desc} · ${timeAgo}</small>
                    </div>
                </div>
            `;
        }).join('');
    }

    function getTimeAgo(ts) {
        const diff = Date.now() - ts;
        const mins = Math.floor(diff / 60000);
        if (mins < 1) return 'just now';
        if (mins < 60) return `${mins}m ago`;
        const hours = Math.floor(mins / 60);
        if (hours < 24) return `${hours}h ago`;
        return `${Math.floor(hours / 24)}d ago`;
    }

    // ---- Mastery Grid ----
    function renderMastery() {
        const grid = document.getElementById('mastery-grid');
        if (!grid) return;

        const progress = getProgress();

        // Demo progress data if empty
        if (Object.keys(progress).length === 0) {
            INSTRUMENTS.forEach((instr, i) => {
                progress[instr.id] = {
                    visited: i < 4,
                    simulations: Math.floor(Math.random() * 5),
                    quizScore: i < 3 ? 60 + Math.floor(Math.random() * 40) : null,
                    timeSpent: Math.floor(Math.random() * 30)
                };
            });
            localStorage.setItem(STORAGE.PROGRESS, JSON.stringify(progress));
        }

        grid.innerHTML = INSTRUMENTS.map(instr => {
            const p = progress[instr.id] || {};
            const masteryPct = calculateMastery(p);
            const level = masteryPct >= 80 ? 'advanced' : masteryPct >= 40 ? 'intermediate' : masteryPct > 0 ? 'novice' : 'locked';
            const levelText = level.charAt(0).toUpperCase() + level.slice(1);

            return `
                <div class="mastery-item">
                    <div class="mastery-header">
                        <strong><i class="fas ${instr.icon}" style="margin-right:6px;opacity:0.5"></i>${instr.name}</strong>
                        <span class="mastery-level ${level}">${levelText}</span>
                    </div>
                    <div class="mastery-bar">
                        <div class="mastery-bar-fill ${instr.color}" style="width: ${masteryPct}%"></div>
                    </div>
                </div>
            `;
        }).join('');
    }

    function calculateMastery(p) {
        let score = 0;
        if (p.visited) score += 20;
        if (p.simulations > 0) score += Math.min(p.simulations * 15, 30);
        if (p.quizScore) score += Math.min(p.quizScore / 2, 50);
        return Math.min(score, 100);
    }

    // ---- Progress Chart ----
    function drawProgressChart() {
        const canvas = document.getElementById('progress-chart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const W = canvas.width;
        const H = canvas.height;

        // Demo data: last 7 days
        const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Today'];
        const values = [1, 2, 2, 3, 3, 5, 6]; // instruments explored
        const maxVal = Math.max(...values, 6);

        ctx.clearRect(0, 0, W, H);

        const padL = 40, padR = 20, padT = 20, padB = 35;
        const chartW = W - padL - padR;
        const chartH = H - padT - padB;

        // Grid lines
        ctx.strokeStyle = '#F1F5F9';
        ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const y = padT + (chartH / 4) * i;
            ctx.beginPath();
            ctx.moveTo(padL, y);
            ctx.lineTo(W - padR, y);
            ctx.stroke();

            // Y labels
            ctx.fillStyle = '#94A3B8';
            ctx.font = '10px Inter, sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(Math.round(maxVal - (maxVal / 4) * i), padL - 8, y + 4);
        }

        // X labels
        ctx.textAlign = 'center';
        labels.forEach((label, i) => {
            const x = padL + (chartW / (labels.length - 1)) * i;
            ctx.fillStyle = '#94A3B8';
            ctx.font = '10px Inter, sans-serif';
            ctx.fillText(label, x, H - 10);
        });

        // Area fill
        const gradient = ctx.createLinearGradient(0, padT, 0, padT + chartH);
        gradient.addColorStop(0, '#3B82F640');
        gradient.addColorStop(1, '#3B82F600');

        ctx.beginPath();
        values.forEach((v, i) => {
            const x = padL + (chartW / (values.length - 1)) * i;
            const y = padT + chartH - (v / maxVal) * chartH;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.lineTo(padL + chartW, padT + chartH);
        ctx.lineTo(padL, padT + chartH);
        ctx.fillStyle = gradient;
        ctx.fill();

        // Line
        ctx.beginPath();
        values.forEach((v, i) => {
            const x = padL + (chartW / (values.length - 1)) * i;
            const y = padT + chartH - (v / maxVal) * chartH;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.strokeStyle = '#3B82F6';
        ctx.lineWidth = 2.5;
        ctx.lineJoin = 'round';
        ctx.stroke();

        // Dots
        values.forEach((v, i) => {
            const x = padL + (chartW / (values.length - 1)) * i;
            const y = padT + chartH - (v / maxVal) * chartH;

            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#3B82F6';
            ctx.fill();
            ctx.beginPath();
            ctx.arc(x, y, 2, 0, Math.PI * 2);
            ctx.fillStyle = 'white';
            ctx.fill();
        });
    }

    // ---- Report Export ----
    function setupExport() {
        const btn = document.getElementById('btn-export-report');
        if (!btn) return;

        btn.addEventListener('click', () => {
            if (typeof window.jspdf === 'undefined') {
                alert('Report generation library is loading. Please try again in a moment.');
                return;
            }

            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

            const progress = getProgress();
            const activity = getActivity();

            // Header
            doc.setFillColor(37, 99, 235);
            doc.rect(0, 0, 210, 30, 'F');
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(18);
            doc.setFont('helvetica', 'bold');
            doc.text('SimuPharma — Student Progress Report', 105, 18, { align: 'center' });

            // Date
            doc.setTextColor(100, 116, 139);
            doc.setFontSize(9);
            doc.setFont('helvetica', 'normal');
            doc.text('Generated: ' + new Date().toLocaleDateString(), 15, 40);

            // Summary stats
            doc.setFontSize(12);
            doc.setFont('helvetica', 'bold');
            doc.setTextColor(30, 41, 59);
            doc.text('Learning Summary', 15, 52);

            const explored = Object.keys(progress).filter(k => progress[k]?.visited).length;
            const totalSims = Object.values(progress).reduce((s, p) => s + (p.simulations || 0), 0);
            const scores = activity.filter(a => a.type === 'quiz' && a.score).map(a => a.score);
            const avgScore = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;

            doc.setFontSize(10);
            doc.setFont('helvetica', 'normal');
            const summaryLines = [
                `Instruments Explored: ${explored} / ${INSTRUMENTS.length}`,
                `Total Simulations Run: ${totalSims}`,
                `Quizzes Completed: ${scores.length}`,
                `Average Quiz Score: ${avgScore}%`
            ];
            summaryLines.forEach((line, i) => {
                doc.text(line, 15, 60 + i * 7);
            });

            // Instrument breakdown
            let y = 95;
            doc.setFontSize(12);
            doc.setFont('helvetica', 'bold');
            doc.text('Instrument Breakdown', 15, y);
            y += 8;

            doc.setFontSize(9);
            doc.setFont('helvetica', 'normal');
            INSTRUMENTS.forEach(instr => {
                const p = progress[instr.id] || {};
                const mastery = calculateMastery(p);
                doc.text(`${instr.name}: ${mastery}% mastery | ${p.simulations || 0} simulations | Quiz: ${p.quizScore || 'N/A'}%`, 15, y);
                y += 6;
            });

            // Footer
            doc.setFontSize(7);
            doc.setTextColor(148, 163, 184);
            doc.text('SimuPharma — Virtual Pharmaceutical Laboratory | simupharma.com', 105, 285, { align: 'center' });

            doc.save('SimuPharma_Progress_Report.pdf');
        });
    }

    // ---- Reset ----
    function setupReset() {
        const btn = document.getElementById('btn-reset-progress');
        if (!btn) return;

        btn.addEventListener('click', () => {
            if (confirm('Reset all progress? This cannot be undone.')) {
                localStorage.removeItem(STORAGE.PROGRESS);
                localStorage.removeItem(STORAGE.ACTIVITY);
                location.reload();
            }
        });
    }

    // ---- Init ----
    function init() {
        updateStats();
        renderActivity();
        renderMastery();
        drawProgressChart();
        setupExport();
        setupReset();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
