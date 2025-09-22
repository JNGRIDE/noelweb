# Guía de Instalación - Noel Moreno Website

## 📋 Prerrequisitos

### Software Requerido
- **Python 3.8+** (recomendado 3.9 o superior)
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

### Sistema Operativo
- ✅ **Windows 10/11**
- ✅ **macOS 10.15+**
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+)

### Hardware Mínimo
- **RAM:** 2GB (recomendado 4GB+)
- **Espacio:** 500MB libres
- **CPU:** Dual-core 2GHz+

## 🚀 Instalación Rápida

### 1. Descargar el Proyecto

#### Opción A: Clonar con Git (Recomendado)
```bash
git clone <repository-url>
cd PaginaWPer
```

#### Opción B: Descargar ZIP
1. Descargar el archivo ZIP del repositorio
2. Extraer en una carpeta de tu elección
3. Abrir terminal en la carpeta extraída

### 2. Configurar Entorno Virtual

#### Windows
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

#### macOS/Linux
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

```bash
python run.py
```

¡Listo! La aplicación estará disponible en http://localhost:5000/

## 🔧 Instalación Detallada

### Paso 1: Verificar Python

```bash
# Verificar versión de Python
python --version
# Debe mostrar Python 3.8 o superior

# Si no tienes Python, descargar desde:
# https://www.python.org/downloads/
```

### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Verificar que está activado (debería mostrar (venv) en el prompt)
```

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

### Paso 4: Configurar Variables de Entorno (Opcional)

Crear archivo `.env` en la raíz del proyecto:

```env
# Configuración básica
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion
DATABASE_URL=sqlite:///database/instance/noelmoreno.db

# Configuración de email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion

# Configuración de desarrollo
DEBUG=true
FLASK_ENV=development
```

### Paso 5: Inicializar Base de Datos

La base de datos se crea automáticamente, pero puedes inicializarla manualmente:

```bash
python -c "
from app import create_app
from backend.database import db

app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Base de datos inicializada')
"
```

### Paso 6: Ejecutar la Aplicación

```bash
python run.py
```

Deberías ver:
```
🚀 Backend de Noel Moreno iniciado
📊 Panel de administración: http://localhost:5000/admin
🔐 Usuario: admin / Contraseña: admin123
🌐 Frontend: http://localhost:5000/
📡 API disponible en: http://localhost:5000/api/
```

## ✅ Verificación de la Instalación

### 1. Verificar Frontend
- Abrir navegador en http://localhost:5000/
- Debe mostrar la página principal de Noel Moreno

### 2. Verificar Panel de Administración
- Ir a http://localhost:5000/admin/
- Login con usuario: `admin`, contraseña: `admin123`
- Debe mostrar el dashboard

### 3. Verificar API
- Probar http://localhost:5000/api/projects
- Debe devolver JSON con proyectos

### 4. Verificar Base de Datos
```bash
# Verificar que se crearon los archivos
ls database/instance/
# Debe mostrar: noelmoreno_dev.db
```

## 🔧 Configuración Avanzada

### Cambiar Puerto de la Aplicación

Editar `run.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Cambiar puerto
```

### Configurar Base de Datos Externa

#### PostgreSQL
```python
# En config.py
SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:contraseña@localhost/noelmoreno'
```

#### MySQL
```python
# En config.py
SQLALCHEMY_DATABASE_URI = 'mysql://usuario:contraseña@localhost/noelmoreno'
```

### Configurar Email SMTP

```python
# En config.py o .env
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'tu-email@gmail.com'
MAIL_PASSWORD = 'tu-contraseña-de-aplicacion'
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

```bash
# Verificar que el entorno virtual está activado
# Windows:
where python

# macOS/Linux:
which python

# Debe mostrar ruta a venv/Scripts/python o venv/bin/python

# Si no está activado:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "Port already in use"

```bash
# Encontrar proceso usando el puerto 5000
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# Terminar proceso
# Windows:
taskkill /PID <PID> /F

# macOS/Linux:
kill -9 <PID>

# O cambiar puerto en run.py
```

### Error: "Permission denied"

```bash
# Dar permisos de ejecución (macOS/Linux)
chmod +x run.py

# Windows: Ejecutar PowerShell como administrador
```

### Error de Base de Datos

```bash
# Eliminar base de datos existente
rm database/instance/noelmoreno_dev.db

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

### Error: "No module named 'flask'"

```bash
# Verificar que pip está actualizado
python -m pip install --upgrade pip

# Reinstalar Flask
pip uninstall flask
pip install flask

# O reinstalar todas las dependencias
pip install -r requirements.txt --force-reinstall
```

## 🔄 Actualización del Sistema

### Actualizar Código
```bash
# Si clonaste con Git
git pull origin main

# Reinstalar dependencias si es necesario
pip install -r requirements.txt --upgrade
```

### Actualizar Base de Datos
```bash
# Hacer backup de la base de datos
cp database/instance/noelmoreno_dev.db database/backups/noelmoreno_dev_backup.db

# Aplicar migraciones (si las hay)
python -c "
from app import create_app
from backend.database import db
app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Base de datos actualizada')
"
```

## 🗑️ Desinstalación

### 1. Detener la Aplicación
Presionar `Ctrl+C` en la terminal donde está ejecutándose.

### 2. Desactivar Entorno Virtual
```bash
deactivate
```

### 3. Eliminar Archivos
```bash
# Eliminar carpeta del proyecto
# Windows:
rmdir /s PaginaWPer

# macOS/Linux:
rm -rf PaginaWPer/
```

### 4. Eliminar Entorno Virtual
```bash
# Eliminar carpeta venv
# Windows:
rmdir /s venv

# macOS/Linux:
rm -rf venv/
```

## 📞 Soporte Técnico

Si encuentras problemas durante la instalación:

### 1. Revisar Logs
- Verificar mensajes de error en la terminal
- Revisar logs en `backend/logs/` (si existen)

### 2. Verificar Prerrequisitos
- Python 3.8+ instalado correctamente
- pip actualizado
- Permisos de escritura en la carpeta

### 3. Consultar Documentación
- `README.md` - Información general
- `docs/ARCHITECTURE.md` - Arquitectura del sistema
- `docs/comandos_utiles.md` - Comandos útiles

### 4. Contactar Soporte
- **Email:** jnamgcontacto@gmail.com
- **Teléfono:** +52 3330 23540 40

## 🎯 Próximos Pasos

Después de la instalación exitosa:

1. **Cambiar credenciales por defecto** en producción
2. **Configurar email** para notificaciones
3. **Personalizar contenido** en el panel admin
4. **Configurar backup** automático de base de datos
5. **Implementar tests** para funcionalidades críticas

---

**¡Instalación completada exitosamente! Tu sistema Noel Moreno Website está listo para usar. 🚀**