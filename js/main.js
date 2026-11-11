/**
 * Cairo Artisan Bakery — Interactive JS
 * Handles: mobile nav toggle, category filtering, scroll header shadow,
 *          scroll-reveal animations, contact form demo behavior
 */

(function () {
    'use strict';

    /* ─── Mobile Navigation Toggle ─── */
    const navToggle = document.querySelector('.nav-toggle');
    const navList   = document.getElementById('nav-menu');

    if (navToggle && navList) {
        navToggle.addEventListener('click', function () {
            const expanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', String(!expanded));
            navList.classList.toggle('open');
        });

        // Close menu when a link is clicked
        navList.querySelectorAll('.nav-link').forEach(function (link) {
            link.addEventListener('click', function () {
                navToggle.setAttribute('aria-expanded', 'false');
                navList.classList.remove('open');
            });
        });

        // Close on Escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && navList.classList.contains('open')) {
                navToggle.setAttribute('aria-expanded', 'false');
                navList.classList.remove('open');
                navToggle.focus();
            }
        });
    }

    /* ─── Header Shadow on Scroll ─── */
    const header = document.querySelector('.site-header');
    let lastScroll = 0;

    function updateHeader() {
        const currentScroll = window.pageYOffset;
        if (header) {
            header.classList.toggle('scrolled', currentScroll > 20);
        }
        lastScroll = currentScroll;
    }
    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();

    /* ─── Scroll-Reveal Animation ─── */
    const revealElements = document.querySelectorAll('.reveal');

    function checkReveal() {
        const windowHeight = window.innerHeight;
        const revealPoint = 100;

        revealElements.forEach(function (el) {
            const elementTop = el.getBoundingClientRect().top;
            if (elementTop < windowHeight - revealPoint) {
                el.classList.add('visible');
            }
        });
    }

    window.addEventListener('scroll', checkReveal, { passive: true });
    // Run once on load in case elements are already in view
    window.addEventListener('load', checkReveal);

    /* ─── Category Filter Tabs ─── */
    function applyFilter(category) {
        const tabs = document.querySelectorAll('.tab-btn');
        const cards = document.querySelectorAll('.product-card');

        tabs.forEach(function (b) {
            b.classList.remove('active');
            b.setAttribute('aria-pressed', 'false');
        });

        const activeTab = document.querySelector(`.tab-btn[data-tab="${category}"]`);
        if (activeTab) {
            activeTab.classList.add('active');
            activeTab.setAttribute('aria-pressed', 'true');
        }

        cards.forEach(function (card) {
            const cardCat = card.dataset.category;
            if (category === 'all' || cardCat === category) {
                card.classList.remove('filtered-out');
            } else {
                card.classList.add('filtered-out');
            }
        });
    }

    document.querySelectorAll('.tab-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            applyFilter(this.dataset.tab);
        });
    });

    /* ─── Contact Form Demo Behavior ─── */
    const contactForm = document.getElementById('contact-form');
    const formSuccess = document.getElementById('form-success');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Basic client-side validation
            const name     = document.getElementById('name');
            const phone    = document.getElementById('phone');
            const message  = document.getElementById('message');
            let isValid    = true;

            [name, phone, message].forEach(function (field) {
                field.classList.remove('input-error');
                if (!field.value.trim()) {
                    field.classList.add('input-error');
                    isValid = false;
                }
            });

            if (!isValid) return;

            // Simulate submission — show success message
            contactForm.classList.add('hidden');
            if (formSuccess) {
                formSuccess.classList.remove('hidden');
                formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }

    /* ─── Smooth Scroll for Anchor Links (fallback) ─── */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                const headerHeight = header ? header.offsetHeight : 0;
                const targetPosition = targetEl.getBoundingClientRect().top + window.pageYOffset - headerHeight - 16;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });
            }
        });
    });

    /* ─── Active Nav Link Highlighting ─── */
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link:not(.btn-nav)');

    function highlightNav() {
        const scrollPos = window.pageYOffset + 120;

        sections.forEach(function (section) {
            const sectionTop    = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId     = section.getAttribute('id');

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(function (link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNav, { passive: true });
    highlightNav();

})();
