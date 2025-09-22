# Manejador de archivos estáticos
from flask import Blueprint, send_from_directory, abort
import os

static_bp = Blueprint('static_files', __name__)

# Obtener la ruta absoluta del directorio frontend
# Buscar el directorio frontend desde la raíz del proyecto
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)  # Subir un nivel desde backend/
FRONTEND_DIR = os.path.join(project_root, 'frontend')

# Verificar que el directorio frontend existe
if not os.path.exists(FRONTEND_DIR):
    print(f"⚠️  ADVERTENCIA: Directorio frontend no encontrado en {FRONTEND_DIR}")
    print("   Asegúrate de que el directorio frontend existe en la raíz del proyecto")

@static_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos del frontend"""
    print(f"Intentando servir: {filename}")
    print(f"Directorio frontend: {FRONTEND_DIR}")
    print(f"Directorio existe: {os.path.exists(FRONTEND_DIR)}")
    
    # Verificar que el directorio existe
    if not os.path.exists(FRONTEND_DIR):
        print(f"Error: Directorio frontend no existe: {FRONTEND_DIR}")
        abort(404)
    
    # Verificar que el archivo existe
    file_path = os.path.join(FRONTEND_DIR, filename)
    if not os.path.exists(file_path):
        print(f"Error: Archivo no existe: {file_path}")
        abort(404)
    
    # Servir el archivo
    try:
        return send_from_directory(FRONTEND_DIR, filename)
    except Exception as e:
        print(f"Error al servir archivo: {e}")
        abort(404)

@static_bp.route('/assets/<path:filename>')
def serve_assets(filename):
    """Servir archivos de assets (CSS, JS, imágenes)"""
    print(f"Intentando servir asset: {filename}")
    print(f"Directorio frontend: {FRONTEND_DIR}")
    
    # Verificar que el directorio existe
    if not os.path.exists(FRONTEND_DIR):
        print(f"Error: Directorio frontend no existe: {FRONTEND_DIR}")
        abort(404)
    
    # Verificar que el archivo existe
    file_path = os.path.join(FRONTEND_DIR, 'assets', filename)
    if not os.path.exists(file_path):
        print(f"Error: Asset no existe: {file_path}")
        abort(404)
    
    # Servir el archivo
    try:
        return send_from_directory(os.path.join(FRONTEND_DIR, 'assets'), filename)
    except Exception as e:
        print(f"Error al servir asset: {e}")
        abort(404)

@static_bp.route('/')
def serve_index():
    """Servir página principal"""
    print(f"Sirviendo página principal desde: {FRONTEND_DIR}")
    
    # Verificar que el directorio existe
    if not os.path.exists(FRONTEND_DIR):
        print(f"Error: Directorio frontend no existe: {FRONTEND_DIR}")
        abort(404)
    
    # Servir index.html
    try:
        return send_from_directory(FRONTEND_DIR, 'index.html')
    except Exception as e:
        print(f"Error al servir index.html: {e}")
        abort(404)
