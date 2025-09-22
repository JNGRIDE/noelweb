# Rutas de Autenticación Mejoradas
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from backend.models import User
from backend.database import db
from datetime import datetime
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Página de login mejorada para administradores"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            if request.is_json:
                data = request.get_json()
                username = data.get('username', '').strip()
                password = data.get('password', '')
            else:
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '')
            
            # Validaciones básicas
            if not username or not password:
                if request.is_json:
                    return jsonify({
                        'success': False,
                        'message': 'Usuario y contraseña son requeridos'
                    }), 400
                else:
                    flash('Usuario y contraseña son requeridos', 'error')
                    return render_template('admin/login.html')
            
            # Buscar usuario
            user = User.query.filter_by(username=username, is_admin=True).first()
            
            if user and user.check_password(password):
                # Actualizar último login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Iniciar sesión
                login_user(user, remember=True)
                
                # Log del login exitoso
                logging.info(f"Login exitoso para usuario admin: {username}")
                
                if request.is_json:
                    return jsonify({
                        'success': True,
                        'message': 'Login exitoso',
                        'redirect': '/admin/dashboard'
                    })
                else:
                    next_page = request.args.get('next', '/admin/dashboard')
                    return redirect(next_page)
            else:
                # Log del intento fallido
                logging.warning(f"Intento de login fallido para usuario: {username}")
                
                if request.is_json:
                    return jsonify({
                        'success': False,
                        'message': 'Credenciales incorrectas'
                    }), 401
                else:
                    flash('Usuario o contraseña incorrectos', 'error')
                    
        except Exception as e:
            logging.error(f"Error en login: {str(e)}")
            if request.is_json:
                return jsonify({
                    'success': False,
                    'message': 'Error interno del servidor'
                }), 500
            else:
                flash('Error interno del servidor', 'error')
    
    return render_template('admin/login.html')

@auth_bp.route('/admin/logout')
@login_required
def admin_logout():
    """Cerrar sesión del administrador"""
    try:
        username = current_user.username if current_user.is_authenticated else 'desconocido'
        logout_user()
        session.clear()
        
        # Log del logout
        logging.info(f"Logout exitoso para usuario: {username}")
        
        flash('Sesión cerrada correctamente', 'success')
        return redirect(url_for('auth.admin_login'))
    except Exception as e:
        logging.error(f"Error en logout: {str(e)}")
        return redirect(url_for('auth.admin_login'))

@auth_bp.route('/admin/check-session')
@login_required
def check_session():
    """Verificar estado de la sesión"""
    return jsonify({
        'authenticated': current_user.is_authenticated,
        'is_admin': current_user.is_admin if current_user.is_authenticated else False,
        'username': current_user.username if current_user.is_authenticated else None
    })

# Ruta de login legacy (para compatibilidad)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta legacy - redirige al nuevo sistema"""
    return redirect(url_for('auth.admin_login'))

@auth_bp.route('/logout')
def logout():
    """Ruta legacy - redirige al nuevo sistema"""
    return redirect(url_for('auth.admin_logout'))
