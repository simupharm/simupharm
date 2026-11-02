/* ================================================================
   CERTIFICATE GENERATOR — jsPDF-powered PDF certificate
   Generates branded certificate after quiz completion
   ================================================================ */
(function () {
    'use strict';

    function generateCertificate(studentName, score, totalQuestions, instruments) {
        if (typeof window.jspdf === 'undefined') {
            console.warn('jsPDF not loaded');
            return;
        }

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });

        const W = 297; // A4 landscape width
        const H = 210; // A4 landscape height
        const percentage = Math.round((score / totalQuestions) * 100);
        const date = new Date().toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric'
        });

        // ---- Background ----
        doc.setFillColor(248, 250, 252); // gray-50
        doc.rect(0, 0, W, H, 'F');

        // Decorative border
        doc.setDrawColor(37, 99, 235); // blue-600
        doc.setLineWidth(2);
        doc.roundedRect(10, 10, W - 20, H - 20, 6, 6, 'S');

        doc.setDrawColor(124, 58, 237); // purple-600
        doc.setLineWidth(0.5);
        doc.roundedRect(14, 14, W - 28, H - 28, 4, 4, 'S');

        // ---- Header gradient bar ----
        for (let i = 0; i < 8; i++) {
            const r = Math.round(37 + (124 - 37) * (i / 7));
            const g = Math.round(99 + (58 - 99) * (i / 7));
            const b = Math.round(235 + (237 - 235) * (i / 7));
            doc.setFillColor(r, g, b);
            doc.rect(14, 14 + i * 0.8, W - 28, 0.8, 'F');
        }

        // ---- Logo / Brand ----
        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(37, 99, 235);
        doc.text('SimuPharma', W / 2, 35, { align: 'center' });

        doc.setFontSize(8);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(100, 116, 139);
        doc.text('Virtual Pharmaceutical Laboratory', W / 2, 41, { align: 'center' });

        // ---- Title ----
        doc.setFontSize(28);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(30, 41, 59); // gray-800
        doc.text('Certificate of Achievement', W / 2, 62, { align: 'center' });

        // Decorative line
        doc.setDrawColor(37, 99, 235);
        doc.setLineWidth(1);
        doc.line(W / 2 - 50, 67, W / 2 + 50, 67);

        // ---- Body ----
        doc.setFontSize(11);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(100, 116, 139);
        doc.text('This is to certify that', W / 2, 82, { align: 'center' });

        // Student name
        doc.setFontSize(24);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(37, 99, 235);
        doc.text(studentName, W / 2, 96, { align: 'center' });

        // Underline
        const nameWidth = doc.getTextWidth(studentName);
        doc.setDrawColor(37, 99, 235);
        doc.setLineWidth(0.3);
        doc.line(W / 2 - nameWidth / 2, 98, W / 2 + nameWidth / 2, 98);

        // Description
        doc.setFontSize(11);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(100, 116, 139);
        doc.text(
            'has successfully demonstrated proficiency in pharmaceutical analytical',
            W / 2, 110, { align: 'center' }
        );
        doc.text(
            `instrumentation by scoring ${score}/${totalQuestions} (${percentage}%) on the SimuPharma Assessment.`,
            W / 2, 117, { align: 'center' }
        );

        // Instruments covered
        if (instruments && instruments.length > 0) {
            doc.setFontSize(9);
            doc.setTextColor(71, 85, 105);
            doc.text('Instruments Covered: ' + instruments.join(' · '), W / 2, 128, { align: 'center' });
        }

        // ---- Score badge ----
        const badgeX = W / 2;
        const badgeY = 143;

        // Circle
        doc.setFillColor(37, 99, 235);
        doc.circle(badgeX, badgeY, 14, 'F');

        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(255, 255, 255);
        doc.text(`${percentage}%`, badgeX, badgeY + 2, { align: 'center' });

        doc.setFontSize(6);
        doc.text('SCORE', badgeX, badgeY + 7, { align: 'center' });

        // ---- Footer ----
        // Date
        doc.setFontSize(9);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(100, 116, 139);
        doc.text(`Date: ${date}`, 50, 178, { align: 'center' });

        // Seal
        doc.setDrawColor(124, 58, 237);
        doc.setLineWidth(1);
        doc.circle(W / 2, 178, 10, 'S');
        doc.setFontSize(6);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(124, 58, 237);
        doc.text('VERIFIED', W / 2, 177, { align: 'center' });
        doc.text('✓', W / 2, 182, { align: 'center' });

        // Signature line
        doc.setDrawColor(203, 213, 225);
        doc.setLineWidth(0.3);
        doc.line(W - 90, 175, W - 40, 175);
        doc.setFontSize(8);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(100, 116, 139);
        doc.text('SimuPharma Team', W - 65, 181, { align: 'center' });

        // ---- Bottom bar ----
        doc.setFontSize(7);
        doc.setTextColor(148, 163, 184);
        doc.text('simupharma.com | Virtual Pharmaceutical Laboratory | © 2025', W / 2, H - 14, { align: 'center' });

        // ---- Save ----
        doc.save(`SimuPharma_Certificate_${studentName.replace(/\s+/g, '_')}.pdf`);
    }

    // Expose globally
    window.SimuCertificate = { generate: generateCertificate };

    // Auto-attach to quiz results (listen for quiz completion)
    function attachToQuiz() {
        // Watch for quiz completion and add certificate button
        const observer = new MutationObserver((mutations) => {
            for (const m of mutations) {
                for (const node of m.addedNodes) {
                    if (node.nodeType === 1 && node.textContent?.includes('Quiz Complete')) {
                        const score = parseInt(node.querySelector('[style*="border-radius:50%"]')?.textContent);
                        if (score !== undefined) {
                            // Add certificate button
                            const btn = document.createElement('button');
                            btn.className = 'btn btn-ghost btn-lg';
                            btn.style.marginTop = '12px';
                            btn.innerHTML = '<i class="fas fa-certificate"></i> <span>Download Certificate</span>';
                            btn.addEventListener('click', () => {
                                const name = prompt('Enter your name for the certificate:');
                                if (name) {
                                    generateCertificate(
                                        name,
                                        score,
                                        20,
                                        ['HPLC', 'FTIR', 'GC', 'UV-Vis', 'Mass Spectrometry']
                                    );
                                }
                            });
                            // Find the try again button and add certificate button next to it
                            const tryAgainBtn = node.querySelector('.btn');
                            if (tryAgainBtn) {
                                tryAgainBtn.parentNode.insertBefore(btn, tryAgainBtn.nextSibling);
                            }
                        }
                    }
                }
            }
        });

        const quizContainer = document.querySelector('.quiz-container');
        if (quizContainer) {
            observer.observe(quizContainer, { childList: true, subtree: true });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', attachToQuiz);
    } else {
        attachToQuiz();
    }
})();
