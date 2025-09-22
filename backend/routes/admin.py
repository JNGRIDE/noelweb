# Rutas del Panel de Administración
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from backend.models import ContactMessage, Project, Testimonial, BlogPost, User
from backend.database import db
from datetime import datetime, timedelta
import logging

admin_bp = Blueprint('admin_panel', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def index():
    """Redirigir al dashboard"""
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del administrador"""
    try:
        # Estadísticas generales
        stats = {
            'total_messages': ContactMessage.query.count(),
            'unread_messages': ContactMessage.query.filter_by(leido=False).count(),
            'active_projects': Project.query.filter_by(activo=True).count(),
            'active_testimonials': Testimonial.query.filter_by(activo=True).count(),
            'published_posts': BlogPost.query.filter_by(publicado=True).count(),
            'total_users': User.query.count()
        }
        
        # Mensajes recientes
        recent_messages = ContactMessage.query.order_by(
            ContactMessage.fecha.desc()
        ).limit(5).all()
        
        # Proyectos recientes
        recent_projects = Project.query.filter_by(activo=True).order_by(
            Project.fecha_creacion.desc()
        ).limit(3).all()
        
        # Estadísticas de los últimos 30 días
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        monthly_stats = {
            'messages_this_month': ContactMessage.query.filter(
                ContactMessage.fecha >= thirty_days_ago
            ).count(),
            'projects_created': Project.query.filter(
                Project.fecha_creacion >= thirty_days_ago
            ).count()
        }
        
        return render_template('admin/dashboard.html', 
                             stats=stats,
                             recent_messages=recent_messages,
                             recent_projects=recent_projects,
                             monthly_stats=monthly_stats)
                             
    except Exception as e:
        logging.error(f"Error en dashboard: {str(e)}")
        flash('Error al cargar el dashboard', 'error')
        return redirect(url_for('auth.admin_login'))

@admin_bp.route('/messages')
@login_required
def messages():
    """Gestión de mensajes de contacto"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # Filtros
        filter_read = request.args.get('read', 'all')
        filter_service = request.args.get('service', 'all')
        
        query = ContactMessage.query
        
        if filter_read == 'unread':
            query = query.filter_by(leido=False)
        elif filter_read == 'read':
            query = query.filter_by(leido=True)
            
        if filter_service != 'all':
            query = query.filter_by(servicio=filter_service)
        
        messages = query.order_by(ContactMessage.fecha.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Servicios únicos para filtro
        services = db.session.query(ContactMessage.servicio).distinct().all()
        services = [s[0] for s in services if s[0]]
        
        return render_template('admin/messages.html',
                             messages=messages,
                             services=services,
                             current_filters={
                                 'read': filter_read,
                                 'service': filter_service
                             })
                             
    except Exception as e:
        logging.error(f"Error en mensajes: {str(e)}")
        flash('Error al cargar los mensajes', 'error')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/messages/<int:message_id>')
@login_required
def view_message(message_id):
    """Ver mensaje específico"""
    try:
        message = ContactMessage.query.get_or_404(message_id)
        
        # Marcar como leído
        if not message.leido:
            message.leido = True
            db.session.commit()
        
        return render_template('admin/message_detail.html', message=message)
        
    except Exception as e:
        logging.error(f"Error al ver mensaje {message_id}: {str(e)}")
        flash('Error al cargar el mensaje', 'error')
        return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    """Eliminar mensaje"""
    try:
        message = ContactMessage.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        
        flash('Mensaje eliminado correctamente', 'success')
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Mensaje eliminado'})
        else:
            return redirect(url_for('admin.messages'))
            
    except Exception as e:
        logging.error(f"Error al eliminar mensaje {message_id}: {str(e)}")
        flash('Error al eliminar el mensaje', 'error')
        
        if request.is_json:
            return jsonify({'success': False, 'message': 'Error al eliminar'}), 500
        else:
            return redirect(url_for('admin.messages'))

@admin_bp.route('/projects')
@login_required
def projects():
    """Gestión de proyectos"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # Filtros
        filter_active = request.args.get('active', 'all')
        filter_category = request.args.get('category', 'all')
        
        query = Project.query
        
        if filter_active == 'active':
            query = query.filter_by(activo=True)
        elif filter_active == 'inactive':
            query = query.filter_by(activo=False)
            
        if filter_category != 'all':
            query = query.filter_by(categoria=filter_category)
        
        projects = query.order_by(Project.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Categorías únicas para filtro
        categories = db.session.query(Project.categoria).distinct().all()
        categories = [c[0] for c in categories if c[0]]
        
        return render_template('admin/projects.html',
                             projects=projects,
                             categories=categories,
                             current_filters={
                                 'active': filter_active,
                                 'category': filter_category
                             })
                             
    except Exception as e:
        logging.error(f"Error en proyectos: {str(e)}")
        flash('Error al cargar los proyectos', 'error')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/testimonials')
@login_required
def testimonials():
    """Gestión de testimonios"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # Filtros
        filter_active = request.args.get('active', 'all')
        
        query = Testimonial.query
        
        if filter_active == 'active':
            query = query.filter_by(activo=True)
        elif filter_active == 'inactive':
            query = query.filter_by(activo=False)
        
        testimonials = query.order_by(Testimonial.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('admin/testimonials.html',
                             testimonials=testimonials,
                             current_filters={'active': filter_active})
                             
    except Exception as e:
        logging.error(f"Error en testimonios: {str(e)}")
        flash('Error al cargar los testimonios', 'error')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/blog')
@login_required
def blog():
    """Gestión del blog"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        # Filtros
        filter_published = request.args.get('published', 'all')
        filter_category = request.args.get('category', 'all')
        
        query = BlogPost.query
        
        if filter_published == 'published':
            query = query.filter_by(publicado=True)
        elif filter_published == 'draft':
            query = query.filter_by(publicado=False)
            
        if filter_category != 'all':
            query = query.filter_by(categoria=filter_category)
        
        posts = query.order_by(BlogPost.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Categorías únicas para filtro
        categories = db.session.query(BlogPost.categoria).distinct().all()
        categories = [c[0] for c in categories if c[0]]
        
        return render_template('admin/blog.html',
                             posts=posts,
                             categories=categories,
                             current_filters={
                                 'published': filter_published,
                                 'category': filter_category
                             })
                             
    except Exception as e:
        logging.error(f"Error en blog: {str(e)}")
        flash('Error al cargar el blog', 'error')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/settings')
@login_required
def settings():
    """Configuración del sistema"""
    try:
        # Obtener estadísticas del sistema
        system_stats = {
            'total_users': User.query.count(),
            'admin_users': User.query.filter_by(is_admin=True).count(),
            'last_backup': 'N/A',  # Implementar sistema de backups
            'database_size': 'N/A'  # Implementar cálculo de tamaño
        }
        
        return render_template('admin/settings.html', stats=system_stats)
        
    except Exception as e:
        logging.error(f"Error en configuración: {str(e)}")
        flash('Error al cargar la configuración', 'error')
        return redirect(url_for('admin.dashboard'))

# Rutas API para el dashboard
@admin_bp.route('/api/stats')
@login_required
def api_stats():
    """API para obtener estadísticas en tiempo real"""
    try:
        stats = {
            'total_messages': ContactMessage.query.count(),
            'unread_messages': ContactMessage.query.filter_by(leido=False).count(),
            'active_projects': Project.query.filter_by(activo=True).count(),
            'active_testimonials': Testimonial.query.filter_by(activo=True).count(),
            'published_posts': BlogPost.query.filter_by(publicado=True).count(),
            'total_users': User.query.count()
        }
        
        # Estadísticas de los últimos 7 días
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        weekly_stats = {
            'messages_this_week': ContactMessage.query.filter(
                ContactMessage.fecha >= seven_days_ago
            ).count(),
            'projects_created': Project.query.filter(
                Project.fecha_creacion >= seven_days_ago
            ).count()
        }
        
        return jsonify({
            'success': True,
            'stats': stats,
            'weekly_stats': weekly_stats
        })
        
    except Exception as e:
        logging.error(f"Error en API stats: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener estadísticas'
        }), 500

@admin_bp.route('/api/recent-activity')
@login_required
def api_recent_activity():
    """API para obtener actividad reciente"""
    try:
        # Mensajes recientes
        recent_messages = ContactMessage.query.order_by(
            ContactMessage.fecha.desc()
        ).limit(5).all()
        
        messages_data = []
        for msg in recent_messages:
            messages_data.append({
                'id': msg.id,
                'nombre': msg.nombre,
                'email': msg.email,
                'servicio': msg.servicio,
                'fecha': msg.fecha.isoformat(),
                'leido': msg.leido
            })
        
        return jsonify({
            'success': True,
            'messages': messages_data
        })
        
    except Exception as e:
        logging.error(f"Error en API recent activity: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener actividad reciente'
        }), 500
