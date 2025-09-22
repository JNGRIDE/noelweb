# Arquitectura del Sistema - Noel Moreno Website

## 🏗️ Visión General

El sistema está diseñado con una arquitectura modular que separa claramente las responsabilidades entre frontend, backend y base de datos.

## 📐 Diagrama de Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │    │     Backend     │    │   Base de       │
│   (Estático)    │◄──►│   (Flask API)   │◄──►│   Datos         │
│                 │    │                 │    │  (SQLite)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Navegador     │    │  Panel Admin    │    │   Archivos      │
│   Web           │    │  (Flask-Admin)  │    │   Estáticos     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Componentes del Sistema

### 1. Frontend (Cliente)
- **Tecnologías:** HTML5, CSS3, JavaScript ES6+
- **Responsabilidades:**
  - Presentación de la interfaz de usuario
  - Interacción con el usuario
  - Consumo de APIs REST
  - Validación del lado del cliente

### 2. Backend (Servidor)
- **Framework:** Flask (Python)
- **Responsabilidades:**
  - Lógica de negocio
  - API REST
  - Autenticación y autorización
  - Manejo de base de datos
  - Panel de administración

### 3. Base de Datos
- **Sistema:** SQLite
- **ORM:** SQLAlchemy
- **Responsabilidades:**
  - Almacenamiento de datos
  - Integridad referencial
  - Transacciones ACID

## 📊 Modelos de Datos

### User (Usuario)
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
```

### Project (Proyecto)
```python
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion_problema = db.Column(db.Text, nullable=False)
    descripcion_solucion = db.Column(db.Text, nullable=False)
    resultados = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(500))
    categoria = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    cliente = db.Column(db.String(150))
    tecnologias = db.Column(db.String(200))
    duracion = db.Column(db.String(50))
```

### Testimonial (Testimonio)
```python
class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    testimonio = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    calificacion = db.Column(db.Integer, default=5)
    proyecto_relacionado = db.Column(db.String(200))
```

### BlogPost (Post del Blog)
```python
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    resumen = db.Column(db.Text, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(500))
    categoria = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    publicado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_publicacion = db.Column(db.DateTime)
    vistas = db.Column(db.Integer, default=0)
    autor = db.Column(db.String(100), default='Noel Moreno')
    tiempo_lectura = db.Column(db.Integer)
```

### ContactMessage (Mensaje de Contacto)
```python
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    servicio = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    leido = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45))
```

## 🔄 Flujo de Datos

### 1. Carga de Página Principal
```
Usuario → Frontend → API (/api/projects) → Base de Datos
                ↓
            Renderizado dinámico
```

### 2. Envío de Formulario de Contacto
```
Usuario → Frontend → API (/api/contact) → Base de Datos
                ↓
            Notificación de éxito/error
```

### 3. Panel de Administración
```
Admin → Login → Panel Admin → CRUD Operations → Base de Datos
                ↓
            Actualización en tiempo real
```

## 🛡️ Seguridad

### Autenticación
- **Flask-Login** para manejo de sesiones
- **Hash de contraseñas** con Werkzeug
- **Sesiones seguras** con cookies HTTPOnly

### Autorización
- **Middleware de autenticación** en rutas protegidas
- **Verificación de permisos** en panel admin
- **Protección CSRF** habilitada

### Validación
- **Validación del lado del servidor** en todas las APIs
- **Sanitización de inputs** para prevenir XSS
- **Rate limiting** para prevenir ataques de fuerza bruta

## ⚡ Rendimiento

### Optimizaciones del Backend
- **Lazy loading** en consultas SQLAlchemy
- **Índices de base de datos** en campos críticos
- **Caché de consultas** para datos frecuentes
- **Paginación** en listados grandes

### Optimizaciones del Frontend
- **Carga asíncrona** de contenido dinámico
- **Compresión de assets** estáticos
- **Minificación** de CSS y JavaScript
- **Lazy loading** de imágenes

## 🔧 Configuración por Entornos

### Desarrollo
```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///noelmoreno_dev.db'
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']
```

### Producción
```python
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
```

### Testing
```python
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
```

## 📈 Escalabilidad

### Estrategias de Escalado

#### Escalado Vertical
- **Mejorar hardware** del servidor
- **Optimizar consultas** de base de datos
- **Implementar caché** en memoria (Redis)

#### Escalado Horizontal
- **Load balancer** para múltiples instancias
- **Base de datos** separada del servidor web
- **CDN** para assets estáticos

### Monitoreo
- **Logs estructurados** para debugging
- **Métricas de rendimiento** en tiempo real
- **Health checks** automáticos
- **Alertas** para errores críticos

## 🔄 Deployment

### Desarrollo Local
```bash
python run.py
```

### Producción
```bash
# Con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Con Docker
docker build -t noel-moreno-website .
docker run -p 5000:5000 noel-moreno-website
```

### CI/CD
- **GitHub Actions** para tests automáticos
- **Deploy automático** en push a main
- **Rollback automático** en caso de errores

## 🧪 Testing

### Estrategia de Testing
- **Tests unitarios** para lógica de negocio
- **Tests de integración** para APIs
- **Tests de interfaz** para frontend
- **Tests de carga** para rendimiento

### Coverage
- **Mínimo 80%** de cobertura de código
- **Tests críticos** para funcionalidades core
- **Tests de regresión** para bugs conocidos

## 📚 Documentación

### Documentación Técnica
- **README.md** - Guía de instalación y uso
- **ARCHITECTURE.md** - Arquitectura del sistema
- **API.md** - Documentación de APIs
- **DEPLOYMENT.md** - Guía de despliegue

### Documentación de Usuario
- **Manual de usuario** para panel admin
- **Guía de configuración** para administradores
- **FAQ** para problemas comunes

---

**Esta arquitectura está diseñada para ser mantenible, escalable y segura, siguiendo las mejores prácticas de desarrollo web moderno.**