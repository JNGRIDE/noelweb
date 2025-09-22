// Animaciones y efectos visuales
window.NoelMorenoAnimations = {
    // Configuración de Intersection Observer
    observerOptions: {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    },

    // Inicializar animaciones
    init: function() {
        this.initScrollAnimations();
        this.initCounterAnimations();
        this.initParallaxEffect();
        this.initLazyLoading();
    },

    // Animaciones al hacer scroll
    initScrollAnimations: function() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, this.observerOptions);

        // Observar elementos para animaciones
        const animateElements = document.querySelectorAll(
            '.service-card, .project-card, .testimonial-card, .blog-card, .about-content'
        );
        
        animateElements.forEach(el => {
            observer.observe(el);
        });
    },

    // Animaciones de contador
    initCounterAnimations: function() {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const statNumber = entry.target.querySelector('.stat-number');
                    const text = statNumber.textContent;
                    const target = parseInt(text.replace(/[^\d]/g, ''));
                    
                    this.animateCounter(statNumber, target, text.includes('%'));
                    statsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.stat').forEach(stat => {
            statsObserver.observe(stat);
        });
    },

    // Función para animar contadores
    animateCounter: function(element, target, isPercentage) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current) + (isPercentage ? '%' : '+');
        }, 20);
    },

    // Efecto parallax
    initParallaxEffect: function() {
        const hero = document.querySelector('.hero');
        const heroPattern = document.querySelector('.hero-pattern');
        
        if (hero && heroPattern) {
            const handleScroll = NoelMorenoUtils.throttle(() => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                heroPattern.style.transform = `translateY(${rate}px)`;
            }, 16); // ~60fps

            window.addEventListener('scroll', handleScroll);
        }
    },

    // Lazy loading para imágenes
    initLazyLoading: function() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => {
            imageObserver.observe(img);
        });
    },

    // Animaciones de entrada suave
    initRevealAnimations: function() {
        const revealElements = document.querySelectorAll(
            '.service-card, .project-card, .testimonial-card, .blog-card'
        );
        
        revealElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            element.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        });

        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        revealElements.forEach(element => {
            revealObserver.observe(element);
        });
    }
};
