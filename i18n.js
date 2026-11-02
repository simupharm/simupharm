/* ================================================================
   INTERNATIONALIZATION (i18n) — English + Hindi
   ================================================================ */
(function () {
    'use strict';

    const STORAGE_KEY = 'simupharma-lang';
    const DEFAULT_LANG = 'en';

    const translations = {
        en: {
            'nav.home': 'Home',
            'nav.about': 'About',
            'nav.instruments': 'Instruments',
            'nav.quiz': 'Quiz',
            'nav.contact': 'Contact',
            'hero.badge': '🏆 Award-Winning Research Platform',
            'hero.title.1': 'The Future of',
            'hero.title.2': 'Pharmaceutical',
            'hero.title.3': 'Education is Here',
            'hero.desc': 'Bridge the gap between theory and practice with interactive, scientifically accurate simulations of advanced analytical instruments. Built for students, educators, and researchers.',
            'hero.cta1': 'Explore Instruments',
            'hero.cta2': 'See How It Works',
            'hero.simulate': 'Simulate:',
            'metrics.instruments': 'Instruments',
            'metrics.students': 'Students',
            'metrics.institutions': 'Institutions',
            'about.label': 'About SimuPharma',
            'about.title': 'Redefining How Pharmacy Students Learn',
            'features.label': 'Features',
            'features.title': 'Why SimuPharma Stands Out',
            'process.label': 'How It Works',
            'process.title': 'From Theory to Practice in Three Steps',
            'instruments.label': 'Virtual Laboratory',
            'instruments.title': 'Explore Our Instruments',
            'impact.label': 'Our Impact',
            'impact.title': 'Transforming Education Across the Globe',
            'quiz.label': 'Test Your Knowledge',
            'quiz.title': 'Interactive Assessments',
            'contact.label': 'Get In Touch',
            'contact.title': "Let's Connect",
            'cta.title': 'Ready to Transform Your Learning?',
            'footer.tagline': 'Transforming pharmaceutical education through innovative virtual simulations.',
            'lang.switch': '🇮🇳 हिंदी'
        },
        hi: {
            'nav.home': 'होम',
            'nav.about': 'हमारे बारे में',
            'nav.instruments': 'उपकरण',
            'nav.quiz': 'क्विज़',
            'nav.contact': 'संपर्क',
            'hero.badge': '🏆 पुरस्कार विजेता अनुसंधान मंच',
            'hero.title.1': 'भविष्य यहाँ है',
            'hero.title.2': 'फार्मास्यूटिकल',
            'hero.title.3': 'शिक्षा का',
            'hero.desc': 'उन्नत विश्लेषणात्मक उपकरणों के इंटरैक्टिव, वैज्ञानिक रूप से सटीक सिमुलेशन के साथ सिद्धांत और व्यवहार के बीच की खाई को पाटें। छात्रों, शिक्षकों और शोधकर्ताओं के लिए बनाया गया।',
            'hero.cta1': 'उपकरण देखें',
            'hero.cta2': 'कैसे काम करता है',
            'hero.simulate': 'अनुकरण:',
            'metrics.instruments': 'उपकरण',
            'metrics.students': 'छात्र',
            'metrics.institutions': 'संस्थान',
            'about.label': 'सिमुफार्मा के बारे में',
            'about.title': 'फार्मेसी छात्रों की शिक्षा में क्रांति',
            'features.label': 'विशेषताएं',
            'features.title': 'सिमुफार्मा क्यों अलग है',
            'process.label': 'कैसे काम करता है',
            'process.title': 'तीन चरणों में सिद्धांत से अभ्यास तक',
            'instruments.label': 'वर्चुअल प्रयोगशाला',
            'instruments.title': 'हमारे उपकरण देखें',
            'impact.label': 'हमारा प्रभाव',
            'impact.title': 'विश्वभर में शिक्षा में बदलाव',
            'quiz.label': 'अपना ज्ञान परखें',
            'quiz.title': 'इंटरैक्टिव मूल्यांकन',
            'contact.label': 'संपर्क करें',
            'contact.title': 'जुड़ें हमसे',
            'cta.title': 'अपनी शिक्षा बदलने के लिए तैयार?',
            'footer.tagline': 'नवीन आभासी सिमुलेशन के माध्यम से फार्मास्यूटिकल शिक्षा में बदलाव।',
            'lang.switch': '🇬🇧 English'
        }
    };

    function getCurrentLang() {
        return localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;
    }

    function setLang(lang) {
        localStorage.setItem(STORAGE_KEY, lang);
        applyTranslations(lang);
        // Update switch button text
        const switchBtn = document.getElementById('lang-switch');
        if (switchBtn) {
            switchBtn.textContent = translations[lang]['lang.switch'];
        }
    }

    function applyTranslations(lang) {
        const dict = translations[lang];
        if (!dict) return;

        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (dict[key]) {
                el.textContent = dict[key];
            }
        });

        document.querySelectorAll('[data-i18n-html]').forEach(el => {
            const key = el.getAttribute('data-i18n-html');
            if (dict[key]) {
                el.innerHTML = dict[key];
            }
        });
    }

    function init() {
        // Add language switch button to header
        const headerCta = document.querySelector('.header-cta');
        if (headerCta) {
            const langBtn = document.createElement('button');
            langBtn.id = 'lang-switch';
            langBtn.className = 'btn btn-sm';
            langBtn.style.cssText = 'background:transparent;color:var(--gray-600);border:1px solid var(--gray-300);padding:8px 14px;font-size:0.75rem;border-radius:20px;cursor:pointer;margin-right:8px;font-weight:600;transition:all 0.2s ease;';
            const currentLang = getCurrentLang();
            langBtn.textContent = translations[currentLang]['lang.switch'];
            headerCta.parentNode.insertBefore(langBtn, headerCta);

            langBtn.addEventListener('click', () => {
                const newLang = getCurrentLang() === 'en' ? 'hi' : 'en';
                setLang(newLang);
            });

            langBtn.addEventListener('mouseenter', () => {
                langBtn.style.borderColor = '#3B82F6';
                langBtn.style.color = '#3B82F6';
            });
            langBtn.addEventListener('mouseleave', () => {
                langBtn.style.borderColor = '#D1D5DB';
                langBtn.style.color = '#6B7280';
            });
        }

        // Apply saved language
        const savedLang = getCurrentLang();
        if (savedLang !== DEFAULT_LANG) {
            applyTranslations(savedLang);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose for external use
    window.SimuI18n = { setLang, getCurrentLang, translations };
})();
