# Comandos Útiles - Noel Moreno Website

## 🚀 Comandos de Desarrollo

### Iniciar el Servidor

```bash
# Desarrollo (con recarga automática)
python run.py

# Desarrollo con puerto específico
python run.py --port 8080

# Producción con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Producción con uWSGI
uwsgi --http :5000 --module app:app --processes 4 --threads 2
```

### Gestión de Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Desactivar entorno virtual
deactivate

# Eliminar entorno virtual
rm -rf venv/  # macOS/Linux
rmdir /s venv  # Windows
```

### Instalación de Dependencias

```bash
# Instalar dependencias
pip install -r requirements.txt

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Instalar dependencia específica
pip install flask

# Desinstalar dependencia
pip uninstall flask

# Ver dependencias instaladas
pip list

# Ver dependencias con versiones
pip freeze

# Limpiar caché de pip
pip cache purge
```

## 🗄️ Comandos de Base de Datos

### Gestión de Base de Datos

```bash
# Crear todas las tablas
python -c "
from app import create_app
from backend.database import db
app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Tablas creadas')
"

# Eliminar todas las tablas
python -c "
from app import create_app
from backend.database import db
app = create_app()
with app.app_context():
    db.drop_all()
    print('✅ Tablas eliminadas')
"

# Recrear base de datos
python -c "
from app import create_app
from backend.database import db
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    print('✅ Base de datos recreada')
"
```

### Backup y Restauración

```bash
# Crear backup de base de datos
cp database/instance/noelmoreno_dev.db database/backups/backup_$(date +%Y%m%d_%H%M%S).db

# Restaurar desde backup
cp database/backups/backup_20250120_143022.db database/instance/noelmoreno_dev.db

# Listar backups
ls -la database/backups/
```

### Consultas de Base de Datos

```bash
# Acceder a SQLite directamente
sqlite3 database/instance/noelmoreno_dev.db

# Consultas útiles en SQLite:
# .tables                    - Listar tablas
# .schema table_name         - Ver estructura de tabla
# SELECT * FROM user;        - Ver usuarios
# SELECT * FROM project;     - Ver proyectos
# .quit                     - Salir
```

## 🧪 Comandos de Testing

### Ejecutar Tests

```bash
# Ejecutar todos los tests
python -m pytest tests/

# Ejecutar tests específicos
python -m pytest tests/test_api.py

# Ejecutar con verbose
python -m pytest tests/ -v

# Ejecutar con coverage
python -m pytest --cov=backend tests/

# Ejecutar tests en paralelo
python -m pytest tests/ -n auto
```

### Crear Tests

```bash
# Crear test básico
python -c "
import unittest
from app import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_projects_api(self):
        response = self.client.get('/api/projects')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
"
```

## 🔧 Comandos de Configuración

### Variables de Entorno

```bash
# Crear archivo .env
cat > .env << EOF
SECRET_KEY=tu-clave-secreta-super-segura
DATABASE_URL=sqlite:///database/instance/noelmoreno.db
DEBUG=true
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña
EOF

# Cargar variables de entorno
# Windows:
set DEBUG=true

# macOS/Linux:
export DEBUG=true
```

### Configuración de Usuarios

```bash
# Crear usuario administrador
python -c "
from app import create_app
from backend.models import User
from backend.database import db

app = create_app()
with app.app_context():
    user = User(username='admin', email='admin@noelmoreno.com', is_admin=True)
    user.set_password('nueva-contraseña-segura')
    db.session.add(user)
    db.session.commit()
    print('✅ Usuario admin creado')
"

# Cambiar contraseña de usuario
python -c "
from app import create_app
from backend.models import User
from backend.database import db

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        user.set_password('nueva-contraseña')
        db.session.commit()
        print('✅ Contraseña actualizada')
    else:
        print('❌ Usuario no encontrado')
"
```

## 📊 Comandos de Monitoreo

### Logs y Debugging

```bash
# Ejecutar con logs detallados
FLASK_DEBUG=1 python run.py

# Guardar logs en archivo
python run.py > server.log 2>&1

# Ver logs en tiempo real
tail -f server.log

# Buscar errores en logs
grep -i error server.log

# Ver logs del sistema (Linux/macOS)
journalctl -u noel-moreno-website -f
```

### Verificar Estado del Sistema

```bash
# Verificar puertos en uso
netstat -tulpn | grep :5000  # Linux/macOS
netstat -ano | findstr :5000  # Windows

# Verificar procesos Python
ps aux | grep python  # Linux/macOS
tasklist | findstr python  # Windows

# Verificar uso de memoria
free -h  # Linux
vm_stat  # macOS
```

## 🚀 Comandos de Despliegue

### Preparar para Producción

```bash
# Instalar dependencias de producción
pip install gunicorn

# Crear archivo de configuración para Gunicorn
cat > gunicorn.conf.py << EOF
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
EOF

# Ejecutar con Gunicorn
gunicorn -c gunicorn.conf.py app:app
```

### Docker

```bash
# Crear Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
EOF

# Construir imagen
docker build -t noel-moreno-website .

# Ejecutar contenedor
docker run -p 5000:5000 noel-moreno-website

# Ejecutar en segundo plano
docker run -d -p 5000:5000 --name noel-website noel-moreno-website
```

## 🔄 Comandos de Mantenimiento

### Limpieza del Sistema

```bash
# Limpiar archivos temporales
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Limpiar logs antiguos
find backend/logs/ -name "*.log" -mtime +30 -delete

# Limpiar backups antiguos
find database/backups/ -name "*.db" -mtime +90 -delete

# Limpiar caché de pip
pip cache purge
```

### Actualización del Sistema

```bash
# Actualizar código desde Git
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Verificar compatibilidad
python -c "
import sys
print(f'Python version: {sys.version}')
import flask
print(f'Flask version: {flask.__version__}')
"
```

## 🛠️ Comandos de Desarrollo Avanzado

### Profiling y Optimización

```bash
# Profiling de memoria
python -m memory_profiler app.py

# Profiling de tiempo
python -m cProfile -o profile.stats run.py

# Analizar profile
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(10)
"
```

### Análisis de Código

```bash
# Linting con flake8
pip install flake8
flake8 backend/

# Formateo de código con black
pip install black
black backend/

# Verificación de tipos con mypy
pip install mypy
mypy backend/
```

## 📱 Comandos de API

### Probar APIs

```bash
# Probar API de proyectos
curl http://localhost:5000/api/projects

# Probar API de testimonios
curl http://localhost:5000/api/testimonials

# Probar API de blog
curl http://localhost:5000/api/blog

# Enviar mensaje de contacto
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "servicio": "pos",
    "mensaje": "Hola, me interesa un sistema POS"
  }'
```

### Autenticación

```bash
# Login (obtener token)
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'

# Usar token en requests
curl -H "Authorization: Bearer <token>" http://localhost:5000/admin/
```

## 🎯 Comandos de Utilidad

### Información del Sistema

```bash
# Información del proyecto
python -c "
from app import create_app
app = create_app()
print(f'App name: {app.name}')
print(f'Debug mode: {app.debug}')
print(f'Environment: {app.config.get(\"ENV\", \"production\")}')
"

# Verificar configuración
python -c "
from config import config
print('Available configurations:')
for key in config.keys():
    print(f'  - {key}')
"

# Estadísticas de la base de datos
python -c "
from app import create_app
from backend.models import User, Project, Testimonial, BlogPost, ContactMessage
from backend.database import db

app = create_app()
with app.app_context():
    print(f'Users: {User.query.count()}')
    print(f'Projects: {Project.query.count()}')
    print(f'Testimonials: {Testimonial.query.count()}')
    print(f'Blog posts: {BlogPost.query.count()}')
    print(f'Contact messages: {ContactMessage.query.count()}')
"
```

### Generar Datos de Prueba

```bash
# Crear datos de ejemplo
python -c "
from app import create_app
from backend.models import Project, Testimonial
from backend.database import db

app = create_app()
with app.app_context():
    # Verificar si ya existen datos
    if Project.query.count() == 0:
        # Crear proyectos de ejemplo
        projects = [
            Project(
                titulo='Sistema POS para Farmacia',
                descripcion_problema='Necesidad de integración de ventas e inventario',
                descripcion_solucion='Sistema completo con módulos integrados',
                resultados='40% reducción en tiempo de facturación',
                categoria='POS',
                cliente='Farmacia San José',
                tecnologias='Python, Flask, SQLite',
                duracion='2 meses'
            )
        ]
        
        for project in projects:
            db.session.add(project)
        
        db.session.commit()
        print('✅ Datos de ejemplo creados')
    else:
        print('ℹ️ Datos de ejemplo ya existen')
"
```

---

**Estos comandos te ayudarán a gestionar eficientemente tu sistema Noel Moreno Website. Para más información, consulta la documentación en `/docs/`.**