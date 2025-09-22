// Navegación y menú
window.NoelMorenoNavigation = {
    // Inicializar navegación
    init: function() {
        this.initSmoothScrolling();
        this.initMobileMenu();
        this.initHeaderScroll();
        this.initActiveLinks();
    },

    // Navegación suave
    initSmoothScrolling: function() {
        const navLinks = document.querySelectorAll('a[href^="#"]');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const targetId = link.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    const headerHeight = document.querySelector('.header').offsetHeight;
                    const targetPosition = targetSection.offsetTop - headerHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    },

    // Menú móvil
    initMobileMenu: function() {
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        const navLinks = document.querySelectorAll('.nav-link');
        
        if (hamburger && navMenu) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                navMenu.classList.toggle('active');
            });

            // Cerrar menú al hacer clic en un enlace
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                });
            });

            // Cerrar menú al hacer clic fuera
            document.addEventListener('click', (e) => {
                if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                }
            });
        }
    },

    // Efecto de scroll en el header
    initHeaderScroll: function() {
        const header = document.querySelector('.header');
        
        const handleScroll = NoelMorenoUtils.throttle(() => {
            if (window.scrollY > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }, 16);

        window.addEventListener('scroll', handleScroll);
    },

    // Enlaces activos
    initActiveLinks: function() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        
        const handleScroll = NoelMorenoUtils.throttle(() => {
            let current = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (window.scrollY >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        }, 100);

        window.addEventListener('scroll', handleScroll);
    },

    // Botones de llamada a la acción
    initCTAButtons: function() {
        const ctaButton = document.querySelector('.cta-button');
        const contactBtn = document.querySelector('.contact-btn');
        
        const scrollToContact = () => {
            const contactSection = document.querySelector('#contacto');
            if (contactSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = contactSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        };
        
        if (ctaButton) {
            ctaButton.addEventListener('click', scrollToContact);
        }
        
        if (contactBtn) {
            contactBtn.addEventListener('click', scrollToContact);
        }
    }
};
