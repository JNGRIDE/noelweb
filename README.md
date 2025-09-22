# Noel Moreno Website

Sistema web completo para Noel Moreno - Especialista en soluciones digitales para pequeños negocios.

## 🚀 Características

### Frontend
- **Diseño moderno y responsive** con identidad visual profesional
- **Contenido dinámico** cargado desde API
- **Formulario de contacto** funcional con validación
- **Animaciones suaves** y efectos visuales
- **Optimizado para SEO** y rendimiento

### Backend
- **API REST** completa con Flask
- **Panel de administración** con Flask-Admin
- **Base de datos** SQLite con SQLAlchemy
- **Autenticación** segura con Flask-Login
- **Gestión de contenido** para proyectos, testimonios y blog

### Panel de Administración
- **Dashboard** con estadísticas en tiempo real
- **Gestión de proyectos** con CRUD completo
- **Administración de testimonios** y mensajes
- **Sistema de blog** integrado
- **Interfaz moderna** con Bootstrap 5

## 📁 Estructura del Proyecto

```
PaginaWPer/
├── app.py                     # Aplicación principal Flask
├── config.py                  # Configuración unificada
├── run.py                     # Script de inicio
├── requirements.txt           # Dependencias Python
├── README.md                  # Este archivo
│
├── frontend/                  # Frontend estático
│   ├── index.html            # Página principal
│   └── assets/               # Recursos estáticos
│       ├── css/              # Hojas de estilo
│       ├── js/               # Scripts JavaScript
│       ├── images/           # Imágenes
│       └── fonts/            # Fuentes
│
├── backend/                   # Backend API
│   ├── models/               # Modelos de base de datos
│   │   ├── user.py          # Modelo de usuario
│   │   ├── project.py       # Modelo de proyecto
│   │   ├── testimonial.py   # Modelo de testimonio
│   │   ├── blog.py          # Modelo de blog
│   │   └── contact.py       # Modelo de contacto
│   ├── routes/               # Rutas de la API
│   │   ├── api.py           # Endpoints de la API
│   │   ├── auth.py          # Autenticación
│   │   └── main.py          # Rutas principales
│   ├── templates/            # Templates del admin
│   │   └── admin/           # Templates del panel admin
│   ├── static/               # Archivos estáticos del backend
│   │   └── admin/           # CSS del panel admin
│   └── utils/                # Utilidades
│
├── database/                  # Base de datos
│   ├── instance/             # Archivos de base de datos
│   ├── migrations/           # Migraciones
│   └── backups/              # Respaldos
│
├── docs/                      # Documentación
│   ├── ARCHITECTURE.md       # Arquitectura del sistema
│   ├── INSTALACION.md        # Guía de instalación
│   └── comandos_utiles.md    # Comandos útiles
│
├── scripts/                   # Scripts de utilidad
│   ├── setup.py              # Configuración inicial
│   └── start.py              # Script de inicio
│
└── tests/                     # Tests
    ├── fixtures/              # Datos de prueba
    └── __init__.py           # Inicialización de tests
```

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8+
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd PaginaWPer
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno (opcional):**
```bash
# Crear archivo .env
SECRET_KEY=tu-clave-secreta-super-segura
DATABASE_URL=sqlite:///database/instance/noelmoreno.db
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
```

4. **Ejecutar la aplicación:**
```bash
python run.py
```

## 🌐 Uso

### URLs Disponibles
- **Frontend:** http://localhost:5000/
- **Panel de Administración (Personalizado):** http://localhost:5000/admin/
- **Panel Flask-Admin:** http://localhost:5000/admin-flask/
- **API:** http://localhost:5000/api/
- **Login:** http://localhost:5000/admin/login

### Credenciales por Defecto
- **Usuario:** admin
- **Contraseña:** admin123

⚠️ **IMPORTANTE:** Cambiar las credenciales por defecto en producción.

## 🔧 Configuración

### Entornos Disponibles
- **Development:** Configuración para desarrollo local
- **Production:** Configuración optimizada para producción
- **Testing:** Configuración para ejecutar tests

### Variables de Entorno
```bash
# Configuración básica
SECRET_KEY=clave-secreta-para-sesiones
DATABASE_URL=url-de-base-de-datos

# Configuración de email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu-email
MAIL_PASSWORD=tu-contraseña

# Configuración de producción
DEBUG=False
LOG_TO_STDOUT=True
```

## 📊 API Endpoints

### Proyectos
- `GET /api/projects` - Obtener todos los proyectos
- `POST /api/projects` - Crear nuevo proyecto
- `GET /api/projects/{id}` - Obtener proyecto específico
- `PUT /api/projects/{id}` - Actualizar proyecto
- `DELETE /api/projects/{id}` - Eliminar proyecto

### Testimonios
- `GET /api/testimonials` - Obtener todos los testimonios
- `POST /api/testimonials` - Crear nuevo testimonio

### Blog
- `GET /api/blog` - Obtener posts del blog
- `GET /api/blog/{slug}` - Obtener post específico

### Contacto
- `POST /api/contact` - Enviar mensaje de contacto

## 🧪 Testing

```bash
# Ejecutar todos los tests
python -m pytest tests/

# Ejecutar tests específicos
python -m pytest tests/test_api.py

# Ejecutar con coverage
python -m pytest --cov=backend tests/
```

## 🚀 Despliegue

### Desarrollo
```bash
python run.py
```

### Producción
```bash
# Usar WSGI server como Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# O usar uWSGI
uwsgi --http :5000 --module app:app --processes 4 --threads 2
```

## 📈 Rendimiento

### Optimizaciones Implementadas
- **Caché de consultas** SQLAlchemy
- **Compresión de assets** estáticos
- **Lazy loading** de imágenes
- **Minificación** de CSS y JavaScript
- **CDN** para recursos estáticos

### Monitoreo
- **Logs estructurados** para debugging
- **Métricas de rendimiento** en tiempo real
- **Health checks** para el sistema

## 🔒 Seguridad

### Medidas Implementadas
- **Autenticación** con Flask-Login
- **Protección CSRF** habilitada
- **Validación de inputs** robusta
- **Sanitización** de datos
- **Rate limiting** para APIs
- **Headers de seguridad** configurados

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Changelog

### v1.0.0 (2025-01-20)
- ✅ Sistema completo implementado
- ✅ Frontend dinámico conectado con API
- ✅ Panel de administración funcional
- ✅ Base de datos optimizada
- ✅ Documentación completa

## 📞 Soporte

Para soporte técnico o consultas:
- **Email:** jnamgcontacto@gmail.com
- **Teléfono:** +52 3330 23540 40
- **Ubicación:** Zapopan, Jalisco, México

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Desarrollado con ❤️ para pequeños negocios por Noel Moreno**