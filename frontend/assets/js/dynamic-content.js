// Cargar contenido dinámico desde la API
window.NoelMorenoDynamicContent = {
    // Inicializar carga de contenido
    init: function() {
        this.loadProjects();
        this.loadTestimonials();
        this.loadBlogPosts();
    },
    
    // Cargar proyectos dinámicamente
    async loadProjects() {
        try {
            console.log('🔄 Cargando proyectos desde API...');
            const projects = await NoelMorenoAPI.getProjects();
            
            if (projects && projects.length > 0) {
                this.renderProjects(projects);
                console.log('✅ Proyectos cargados:', projects.length);
            } else {
                console.log('⚠️ No se encontraron proyectos en la API');
            }
        } catch (error) {
            console.error('❌ Error cargando proyectos:', error);
            // Mantener proyectos hardcodeados como fallback
        }
    },
    
    // Renderizar proyectos en el DOM
    renderProjects: function(projects) {
        const projectsGrid = document.querySelector('.projects-grid');
        
        if (!projectsGrid) {
            console.log('⚠️ No se encontró el contenedor de proyectos');
            return;
        }
        
        // Limpiar contenido existente
        projectsGrid.innerHTML = '';
        
        // Renderizar cada proyecto
        projects.forEach(project => {
            const projectCard = this.createProjectCard(project);
            projectsGrid.appendChild(projectCard);
        });
    },
    
    // Crear tarjeta de proyecto
    createProjectCard: function(project) {
        const card = document.createElement('div');
        card.className = 'project-card';
        
        card.innerHTML = `
            <div class="project-image">
                <img src="${project.imagen_url || 'https://via.placeholder.com/400x300/4A90E2/FFFFFF?text=Proyecto'}" 
                     alt="${project.titulo}" 
                     onerror="this.src='https://via.placeholder.com/400x300/4A90E2/FFFFFF?text=Proyecto'">
            </div>
            <div class="project-content">
                <h3 class="project-title">${project.titulo}</h3>
                <p class="project-description">
                    <strong>Problema:</strong> ${project.descripcion_problema}
                </p>
                <p class="project-description">
                    <strong>Solución:</strong> ${project.descripcion_solucion}
                </p>
                <p class="project-description">
                    <strong>Resultados:</strong> ${project.resultados}
                </p>
                ${project.cliente ? `<p class="project-client"><strong>Cliente:</strong> ${project.cliente}</p>` : ''}
                ${project.tecnologias ? `<p class="project-tech"><strong>Tecnologías:</strong> ${project.tecnologias}</p>` : ''}
                ${project.duracion ? `<p class="project-duration"><strong>Duración:</strong> ${project.duracion}</p>` : ''}
            </div>
        `;
        
        return card;
    },
    
    // Cargar testimonios dinámicamente
    async loadTestimonials() {
        try {
            console.log('🔄 Cargando testimonios desde API...');
            const testimonials = await NoelMorenoAPI.getTestimonials();
            
            if (testimonials && testimonials.length > 0) {
                this.renderTestimonials(testimonials);
                console.log('✅ Testimonios cargados:', testimonials.length);
            } else {
                console.log('⚠️ No se encontraron testimonios en la API');
            }
        } catch (error) {
            console.error('❌ Error cargando testimonios:', error);
        }
    },
    
    // Renderizar testimonios en el DOM
    renderTestimonials: function(testimonials) {
        const testimonialsGrid = document.querySelector('.testimonials-grid');
        
        if (!testimonialsGrid) {
            console.log('⚠️ No se encontró el contenedor de testimonios');
            return;
        }
        
        // Limpiar contenido existente
        testimonialsGrid.innerHTML = '';
        
        // Renderizar cada testimonio
        testimonials.forEach(testimonial => {
            const testimonialCard = this.createTestimonialCard(testimonial);
            testimonialsGrid.appendChild(testimonialCard);
        });
    },
    
    // Crear tarjeta de testimonio
    createTestimonialCard: function(testimonial) {
        const card = document.createElement('div');
        card.className = 'testimonial-card';
        
        card.innerHTML = `
            <div class="testimonial-content">
                <p class="testimonial-text">"${testimonial.testimonio}"</p>
            </div>
            <div class="testimonial-author">
                <div class="author-info">
                    <h4 class="author-name">${testimonial.nombre_cliente}</h4>
                    <p class="author-role">${testimonial.cargo}, ${testimonial.empresa}</p>
                    ${testimonial.proyecto_relacionado ? `<p class="author-project">Proyecto: ${testimonial.proyecto_relacionado}</p>` : ''}
                </div>
            </div>
        `;
        
        return card;
    },
    
    // Cargar posts del blog dinámicamente
    async loadBlogPosts() {
        try {
            console.log('🔄 Cargando posts del blog desde API...');
            const posts = await NoelMorenoAPI.getBlogPosts();
            
            if (posts && posts.length > 0) {
                this.renderBlogPosts(posts);
                console.log('✅ Posts del blog cargados:', posts.length);
            } else {
                console.log('⚠️ No se encontraron posts del blog en la API');
            }
        } catch (error) {
            console.error('❌ Error cargando blog:', error);
        }
    },
    
    // Renderizar posts del blog en el DOM
    renderBlogPosts: function(posts) {
        const blogGrid = document.querySelector('.blog-grid');
        
        if (!blogGrid) {
            console.log('⚠️ No se encontró el contenedor del blog');
            return;
        }
        
        // Limpiar contenido existente
        blogGrid.innerHTML = '';
        
        // Renderizar cada post
        posts.forEach(post => {
            const blogCard = this.createBlogCard(post);
            blogGrid.appendChild(blogCard);
        });
    },
    
    // Crear tarjeta de blog
    createBlogCard: function(post) {
        const card = document.createElement('article');
        card.className = 'blog-card';
        
        const publishDate = post.fecha_publicacion 
            ? new Date(post.fecha_publicacion).toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            })
            : 'Fecha no disponible';
        
        card.innerHTML = `
            <div class="blog-image">
                <img src="${post.imagen_url || 'https://via.placeholder.com/400x250/4A90E2/FFFFFF?text=Blog+Post'}" 
                     alt="${post.titulo}" 
                     onerror="this.src='https://via.placeholder.com/400x250/4A90E2/FFFFFF?text=Blog+Post'">
            </div>
            <div class="blog-content">
                <h3 class="blog-title">${post.titulo}</h3>
                <p class="blog-excerpt">${post.resumen}</p>
                <div class="blog-meta">
                    <span class="blog-date">${publishDate}</span>
                    <span class="blog-category">${post.categoria || 'General'}</span>
                    ${post.tiempo_lectura ? `<span class="blog-read-time">${post.tiempo_lectura} min lectura</span>` : ''}
                </div>
                <div class="blog-tags">
                    ${post.tags ? post.tags.map(tag => `<span class="blog-tag">${tag}</span>`).join('') : ''}
                </div>
            </div>
        `;
        
        return card;
    }
};


