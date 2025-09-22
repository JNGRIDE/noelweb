// Manejo de formularios
window.NoelMorenoForms = {
    // Inicializar formularios
    init: function() {
        this.initContactForm();
        this.initFormValidation();
    },

    // Formulario de contacto
    initContactForm: function() {
        const contactForm = document.querySelector('.contact-form');
        
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleContactForm(contactForm);
            });
        }
    },

    // Manejar envío del formulario de contacto
    handleContactForm: function(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Validación
        if (!this.validateContactForm(data)) {
            return;
        }
        
        // Mostrar loading
        const submitBtn = form.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Enviando...';
        submitBtn.disabled = true;
        
        // Enviar al backend
        this.sendToBackend(data)
            .then(response => {
                if (response.success) {
                    NoelMorenoUtils.showNotification(
                        response.message || '¡Mensaje enviado correctamente! Te contactaremos pronto.', 
                        'success'
                    );
                    form.reset();
                } else {
                    NoelMorenoUtils.showNotification(
                        response.message || 'Error al enviar el mensaje. Inténtalo de nuevo.', 
                        'error'
                    );
                }
            })
            .catch(error => {
                console.error('Error:', error);
                NoelMorenoUtils.showNotification(
                    'Error de conexión. Verifica tu internet e inténtalo de nuevo.', 
                    'error'
                );
            })
            .finally(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
    },

    // Enviar datos al backend
    sendToBackend: function(data) {
        return NoelMorenoAPI.sendContactMessage(data);
    },

    // Validar formulario de contacto
    validateContactForm: function(data) {
        const errors = [];
        
        if (!data.nombre || data.nombre.trim().length < 2) {
            errors.push('El nombre debe tener al menos 2 caracteres');
        }
        
        if (!data.email || !NoelMorenoUtils.isValidEmail(data.email)) {
            errors.push('Por favor, ingresa un email válido');
        }
        
        if (!data.servicio) {
            errors.push('Por favor, selecciona un servicio');
        }
        
        if (!data.mensaje || data.mensaje.trim().length < 10) {
            errors.push('El mensaje debe tener al menos 10 caracteres');
        }
        
        if (errors.length > 0) {
            NoelMorenoUtils.showNotification(
                errors.join('. '), 
                'error'
            );
            return false;
        }
        
        return true;
    },

    // Inicializar validación de formularios
    initFormValidation: function() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                // Validación en tiempo real
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
                
                // Limpiar errores al escribir
                input.addEventListener('input', () => {
                    this.clearFieldError(input);
                });
            });
        });
    },

    // Validar campo individual
    validateField: function(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let errorMessage = '';
        
        switch (fieldName) {
            case 'nombre':
                if (value.length < 2) {
                    isValid = false;
                    errorMessage = 'El nombre debe tener al menos 2 caracteres';
                }
                break;
                
            case 'email':
                if (!NoelMorenoUtils.isValidEmail(value)) {
                    isValid = false;
                    errorMessage = 'Por favor, ingresa un email válido';
                }
                break;
                
            case 'telefono':
                if (value && !/^[\+]?[0-9\s\-\(\)]{10,}$/.test(value)) {
                    isValid = false;
                    errorMessage = 'Por favor, ingresa un teléfono válido';
                }
                break;
                
            case 'mensaje':
                if (value.length < 10) {
                    isValid = false;
                    errorMessage = 'El mensaje debe tener al menos 10 caracteres';
                }
                break;
        }
        
        if (!isValid) {
            this.showFieldError(field, errorMessage);
        } else {
            this.clearFieldError(field);
        }
        
        return isValid;
    },

    // Mostrar error en campo
    showFieldError: function(field, message) {
        this.clearFieldError(field);
        
        field.classList.add('error');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            color: #f44336;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        `;
        
        field.parentNode.appendChild(errorDiv);
    },

    // Limpiar error de campo
    clearFieldError: function(field) {
        field.classList.remove('error');
        
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }
};
