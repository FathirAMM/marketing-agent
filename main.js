document.addEventListener('DOMContentLoaded', () => {
    // Intersection Observer for reveal animations
    const revealOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    document.querySelectorAll('.reveal-text, .reveal-img').forEach(el => {
        revealObserver.observe(el);
    });

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId.startsWith('#')) {
                const target = document.querySelector(targetId);
                if (target) {
                    window.scrollTo({
                        top: target.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            } else if (targetId.includes('index.html#')) {
                // If on another page and going to a section on index.html
                // Standard link behavior is fine, or we could handle it via JS
            }
        });
    });

    // Navbar behavior
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;

    const updateNavbar = () => {
        const currentScrollY = window.scrollY;

        // Hide/Show on scroll direction
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            // Scrolling down & past threshold - hide navbar
            navbar.classList.add('navbar-hidden');
        } else {
            // Scrolling up or at top - show navbar
            navbar.classList.remove('navbar-hidden');
        }

        // Transparency/Padding on scroll
        if (currentScrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }

        lastScrollY = currentScrollY;
    };

    // Initialize state on load
    updateNavbar();

    // Item toggle (Experience & Education)
    document.querySelectorAll('.experience-item.clickable, .education-item.clickable').forEach(item => {
        item.addEventListener('click', () => {
            // Close other expanded items in both lists
            document.querySelectorAll('.experience-item.expanded, .education-item.expanded').forEach(expandedItem => {
                if (expandedItem !== item) {
                    expandedItem.classList.remove('expanded');
                }
            });

            item.classList.toggle('expanded');
        });
    });

    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
            document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
        });

        // Close menu when a link is clicked
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.style.overflow = '';
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !menuToggle.contains(e.target) && navLinks.classList.contains('active')) {
                menuToggle.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // Listen for scroll events
    window.addEventListener('scroll', updateNavbar);

    // Log for verification
    console.log('Portfolio initialized');
});
