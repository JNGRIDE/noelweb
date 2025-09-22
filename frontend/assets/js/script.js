// Aplicación principal - Noel Moreno
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todos los módulos
    NoelMorenoNavigation.init();
    NoelMorenoAnimations.init();
    NoelMorenoForms.init();
    
    // Cargar contenido dinámico desde la API
    NoelMorenoDynamicContent.init();
    
    // Inicializar botones CTA
    NoelMorenoNavigation.initCTAButtons();
    
    // Inicializar animaciones de revelado
    NoelMorenoAnimations.initRevealAnimations();
    
    console.log('🚀 Noel Moreno Website - Cargado correctamente');
});

// Funciones adicionales para funcionalidades futuras
window.NoelMoreno = {
    // Función para abrir modal de proyecto
    openProjectModal: function(projectId) {
        console.log('Abriendo modal para proyecto:', projectId);
        // Implementar modal de proyecto
    },
    
    // Función para filtrar proyectos
    filterProjects: function(category) {
        console.log('Filtrando proyectos por:', category);
        // Implementar filtrado de proyectos
    },
    
    // Función para enviar formulario de contacto
    submitContactForm: function(formData) {
        console.log('Enviando formulario:', formData);
        // Implementar envío real al backend
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({ success: true, message: 'Mensaje enviado correctamente' });
            }, 1000);
        });
    }
};
