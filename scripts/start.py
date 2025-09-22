#!/usr/bin/env python3
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
        
        print("\n🚀 Backend de Noel Moreno iniciado")
        print("📊 Panel de administración: http://localhost:5000/admin")
        print("🔐 Usuario: admin / Contraseña: admin123")
        print("🌐 Frontend: http://localhost:5000/static/index.html")
        print("📡 API disponible en: http://localhost:5000/api/")
        print("\n⚠️  IMPORTANTE: Cambiar contraseña en producción")
        print("=" * 50)
        
        # Iniciar servidor
        app.run(debug=True, host='0.0.0.0', port=5000)
