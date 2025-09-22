# Backend - Noel Moreno Website

API REST y panel de administración para el sistema web de Noel Moreno.

## 🏗️ Estructura

```
backend/
├── models/              # Modelos de base de datos
│   ├── user.py         # Modelo de usuario
│   ├── project.py      # Modelo de proyecto
│   ├── testimonial.py  # Modelo de testimonio
│   ├── blog.py         # Modelo de blog
│   └── contact.py      # Modelo de contacto
├── routes/              # Rutas de la API
│   ├── api.py          # Endpoints de la API
│   ├── auth.py         # Autenticación
│   └── main.py         # Rutas principales
├── templates/           # Templates del panel admin
│   └── admin/          # Templates del panel admin
├── static/              # Archivos estáticos del backend
│   └── admin/          # CSS del panel admin
├── utils/               # Utilidades
├── uploads/             # Archivos subidos
├── logs/                # Archivos de log
└── database.py          # Configuración de base de datos
```

## 🚀 Funcionalidades

### API REST
- **Proyectos:** CRUD completo para gestión de proyectos
- **Testimonios:** Gestión de testimonios de clientes
- **Blog:** Sistema de blog con posts
- **Contacto:** Procesamiento de formularios de contacto

### Panel de Administración
- **Dashboard:** Estadísticas y resumen del sistema
- **Gestión de contenido:** CRUD para todos los modelos
- **Autenticación:** Sistema de login seguro
- **Interfaz moderna:** Bootstrap 5 con estilos personalizados

### Modelos de Datos
- **User:** Gestión de usuarios y administradores
- **Project:** Proyectos con detalles completos
- **Testimonial:** Testimonios con calificaciones
- **BlogPost:** Posts del blog con categorías y tags
- **ContactMessage:** Mensajes de contacto

## 🔧 Configuración

### Variables de Entorno
```bash
SECRET_KEY=clave-secreta
DATABASE_URL=sqlite:///database/instance/noelmoreno.db
MAIL_USERNAME=email@ejemplo.com
MAIL_PASSWORD=contraseña
```

### Configuración de Base de Datos
La base de datos se configura automáticamente usando SQLAlchemy. Los modelos se crean al inicializar la aplicación.

## 📡 API Endpoints

### Proyectos
- `GET /api/projects` - Listar proyectos activos
- `GET /api/admin/projects` - Listar todos los proyectos (admin)

### Testimonios
- `GET /api/testimonials` - Listar testimonios activos
- `GET /api/admin/testimonials` - Listar todos los testimonios (admin)

### Blog
- `GET /api/blog` - Listar posts publicados
- `GET /api/blog/{slug}` - Obtener post específico
- `GET /api/admin/blog` - Listar todos los posts (admin)

### Contacto
- `POST /api/contact` - Enviar mensaje
- `GET /api/admin/messages` - Listar mensajes (admin)
- `GET /api/admin/messages/{id}` - Obtener mensaje específico (admin)
- `POST /api/admin/messages/{id}/mark-read` - Marcar como leído (admin)
- `DELETE /api/admin/messages/{id}` - Eliminar mensaje (admin)

## 🔒 Seguridad

- **Autenticación:** Flask-Login para sesiones
- **Autorización:** Verificación de permisos en panel admin
- **Validación:** Validación robusta de inputs
- **CSRF:** Protección CSRF habilitada
- **Rate Limiting:** Protección contra ataques de fuerza bruta

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Tests con coverage
python -m pytest --cov=backend tests/
```

## 📊 Monitoreo

- **Logs estructurados** para debugging
- **Métricas de rendimiento** en tiempo real
- **Health checks** para el sistema
- **Alertas** para errores críticos

---

**Backend desarrollado con Flask para Noel Moreno Website**