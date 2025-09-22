#!/usr/bin/env python3
# Script de configuración para el Backend de Noel Moreno
# Ejecutar con: python setup.py

import os
import sys
import subprocess
import sqlite3
from datetime import datetime

def print_header():
    print("=" * 60)
    print("🚀 CONFIGURACIÓN BACKEND NOEL MORENO")
    print("=" * 60)
    print()

def check_python_version():
    """Verificar versión de Python"""
    print("📋 Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_dependencies():
    """Instalar dependencias de Python"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False

def create_directories():
    """Crear directorios necesarios"""
    print("\n📁 Creando directorios...")
    directories = [
        "static",
        "templates",
        "uploads",
        "logs"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Directorio creado: {directory}")
        else:
            print(f"📁 Directorio ya existe: {directory}")

def copy_frontend_files():
    """Copiar archivos del frontend al directorio static"""
    print("\n📄 Copiando archivos del frontend...")
    
    # Directorio del frontend (un nivel arriba)
    frontend_dir = "../"
    static_dir = "static/"
    
    files_to_copy = [
        "index.html",
        "assets/css/",
        "assets/js/",
        "assets/images/",
        "assets/fonts/"
    ]
    
    import shutil
    
    for file_path in files_to_copy:
        src = os.path.join(frontend_dir, file_path)
        dst = os.path.join(static_dir, file_path)
        
        if os.path.exists(src):
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"✅ Directorio copiado: {file_path}")
            else:
                shutil.copy2(src, dst)
                print(f"✅ Archivo copiado: {file_path}")
        else:
            print(f"⚠️  No encontrado: {file_path}")

def create_env_file():
    """Crear archivo de variables de entorno"""
    print("\n⚙️  Creando archivo de configuración...")
    
    env_content = """# Configuración del Backend Noel Moreno
# Cambiar estos valores en producción

# Clave secreta para Flask (CAMBIAR EN PRODUCCIÓN)
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion

# Configuración de base de datos
DATABASE_URL=sqlite:///noelmoreno.db

# Configuración de email (para notificaciones)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-password-de-app

# Configuración del servidor
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Configuración de seguridad
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado")

def create_startup_script():
    """Crear script de inicio"""
    print("\n🚀 Creando script de inicio...")
    
    startup_content = """#!/usr/bin/env python3
# Script de inicio para el Backend de Noel Moreno

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, create_admin_user, create_sample_data

if __name__ == '__main__':
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        # Crear usuario administrador
        create_admin_user()
        
        # Crear datos de ejemplo
        create_sample_data()
        
        print("\\n🚀 Backend de Noel Moreno iniciado")
        print("📊 Panel de administración: http://localhost:5000/admin")
        print("🔐 Usuario: admin / Contraseña: admin123")
        print("🌐 Frontend: http://localhost:5000/static/index.html")
        print("📡 API disponible en: http://localhost:5000/api/")
        print("\\n⚠️  IMPORTANTE: Cambiar contraseña en producción")
        print("=" * 50)
        
        # Iniciar servidor
        app.run(debug=True, host='0.0.0.0', port=5000)
"""
    
    with open("start.py", "w", encoding="utf-8") as f:
        f.write(startup_content)
    
    # Hacer ejecutable en sistemas Unix
    if os.name != 'nt':
        os.chmod("start.py", 0o755)
    
    print("✅ Script de inicio creado: start.py")

def create_documentation():
    """Crear documentación básica"""
    print("\n📚 Creando documentación...")
    
    doc_content = """# Backend Noel Moreno - Documentación

## 🚀 Inicio Rápido

### 1. Instalación
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar configuración inicial
python setup.py

# Iniciar servidor
python start.py
```

### 2. Acceso
- **Frontend**: http://localhost:5000/static/index.html
- **Panel Admin**: http://localhost:5000/admin
- **API**: http://localhost:5000/api/

### 3. Credenciales por defecto
- **Usuario**: admin
- **Contraseña**: admin123
- ⚠️ **CAMBIAR EN PRODUCCIÓN**

## 📡 API Endpoints

### Formulario de Contacto
```
POST /api/contact
Content-Type: application/json

{
    "nombre": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "telefono": "+52 333 123 4567",
    "servicio": "pos",
    "mensaje": "Necesito un sistema POS para mi tienda"
}
```

### Obtener Proyectos
```
GET /api/projects
```

### Obtener Testimonios
```
GET /api/testimonials
```

### Obtener Artículos del Blog
```
GET /api/blog
```

## 🗄️ Base de Datos

### Modelos Principales
- **User**: Usuarios del sistema
- **ContactMessage**: Mensajes del formulario de contacto
- **Project**: Proyectos mostrados en la web
- **Testimonial**: Testimonios de clientes
- **BlogPost**: Artículos del blog

### Ubicación de la BD
- Archivo: `noelmoreno.db` (SQLite)
- Se crea automáticamente al iniciar

## 🔧 Configuración

### Variables de Entorno (.env)
```
SECRET_KEY=tu-clave-secreta
DEBUG=True
HOST=0.0.0.0
PORT=5000
```

## 🚀 Despliegue en Producción

### 1. Cambiar configuración
- Cambiar `SECRET_KEY` en app.py
- Cambiar contraseña de administrador
- Configurar base de datos PostgreSQL (recomendado)

### 2. Usar servidor WSGI
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Configurar proxy reverso (Nginx)
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🛠️ Desarrollo

### Estructura del Proyecto
```
backend/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
├── setup.py           # Script de configuración
├── start.py           # Script de inicio
├── templates/         # Plantillas HTML
├── static/           # Archivos estáticos (frontend)
├── uploads/          # Archivos subidos
└── noelmoreno.db     # Base de datos SQLite
```

### Comandos Útiles
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en modo desarrollo
python app.py

# Crear backup de la base de datos
cp noelmoreno.db backup_$(date +%Y%m%d).db
```

## 📞 Soporte

Para soporte técnico, contactar a:
- Email: jnamgcontacto@gmail.com
- Teléfono: +52 3330 23540 40

---
**Desarrollado con ❤️ para Noel Moreno**
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(doc_content)
    
    print("✅ Documentación creada: README.md")

def main():
    """Función principal de configuración"""
    print_header()
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Instalar dependencias
    if not install_dependencies():
        return False
    
    # Crear directorios
    create_directories()
    
    # Copiar archivos del frontend
    copy_frontend_files()
    
    # Crear archivo de configuración
    create_env_file()
    
    # Crear script de inicio
    create_startup_script()
    
    # Crear documentación
    create_documentation()
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print()
    print("🚀 Para iniciar el servidor:")
    print("   python start.py")
    print()
    print("🌐 Accesos:")
    print("   Frontend: http://localhost:5000/static/index.html")
    print("   Panel Admin: http://localhost:5000/admin")
    print("   Usuario: admin / Contraseña: admin123")
    print()
    print("⚠️  IMPORTANTE: Cambiar contraseña en producción")
    print("📚 Ver README.md para más información")
    print()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        sys.exit(1)
