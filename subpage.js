/* ================================================================
   SIMUPHARMA — SUB-PAGE SHARED SCRIPT
   Handles: Mobile menu, scroll animations, page transitions
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ---- Page Entrance Animation ----
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.4s ease';
    requestAnimationFrame(() => {
        document.body.style.opacity = '1';
    });


    // ---- Mobile Menu Toggle ----
    const toggle = document.getElementById('sp-mobile-toggle') || document.getElementById('hamburger');
    const mobileMenu = document.getElementById('sp-mobile-menu');

    if (toggle && mobileMenu) {
        toggle.addEventListener('click', () => {
            const isOpen = mobileMenu.classList.contains('open');
            mobileMenu.classList.toggle('open');
            toggle.classList.toggle('active');
            toggle.setAttribute('aria-expanded', !isOpen);
            document.body.style.overflow = isOpen ? '' : 'hidden';
        });

        const bg = mobileMenu.querySelector('.mobile-menu-bg');
        if (bg) {
            bg.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                toggle.classList.remove('active');
                toggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            });
        }

        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                toggle.classList.remove('active');
                toggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            });
        });
    }


    // ---- Scroll Entrance Animations ----
    const animElements = document.querySelectorAll('.fade-in-up');

    if (animElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -40px 0px'
        });

        animElements.forEach(el => observer.observe(el));
    }


    // ---- Header scroll effect (works with both .sp-header and .site-header) ----
    const header = document.querySelector('.sp-header') || document.querySelector('.site-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 60) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }, { passive: true });
    }


    // ---- Page Transitions (intercept internal links) ----
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a[href]');
        if (!link) return;

        const href = link.getAttribute('href');

        // Skip external links, anchors, and special protocols
        if (!href || href.startsWith('#') || href.startsWith('http') ||
            href.startsWith('mailto') || href.startsWith('tel') ||
            link.target === '_blank') return;

        // Only handle local .html links
        if (href.endsWith('.html') || href === '/' || href === './') {
            e.preventDefault();

            // Fade out
            document.body.style.opacity = '0';
            document.body.style.transform = 'translateY(-8px)';

            setTimeout(() => {
                window.location.href = href;
            }, 300);
        }
    });

});

