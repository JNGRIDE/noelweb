// API Client para Noel Moreno Website
window.NoelMorenoAPI = {
    // Configuración base
    baseURL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://localhost:5000/api' 
        : '/api',
    
    // Función genérica para hacer requests
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Obtener proyectos
    async getProjects() {
        try {
            return await this.request('/projects');
        } catch (error) {
            console.error('Error cargando proyectos:', error);
            return [];
        }
    },
    
    // Obtener testimonios
    async getTestimonials() {
        try {
            return await this.request('/testimonials');
        } catch (error) {
            console.error('Error cargando testimonios:', error);
            return [];
        }
    },
    
    // Obtener posts del blog
    async getBlogPosts() {
        try {
            return await this.request('/blog');
        } catch (error) {
            console.error('Error cargando blog:', error);
            return [];
        }
    },
    
    // Obtener un post específico del blog
    async getBlogPost(slug) {
        try {
            return await this.request(`/blog/${slug}`);
        } catch (error) {
            console.error('Error cargando post:', error);
            return null;
        }
    },
    
    // Enviar mensaje de contacto
    async sendContactMessage(data) {
        try {
            return await this.request('/contact', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        } catch (error) {
            console.error('Error enviando mensaje:', error);
            throw error;
        }
    }
};


