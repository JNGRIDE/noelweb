# Rutas de la API Mejoradas
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from backend.models import ContactMessage, Project, Testimonial, BlogPost, User
from backend.database import db
from datetime import datetime, timedelta
import logging

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/contact', methods=['POST'])
def contact_form():
    """API para procesar formulario de contacto"""
    try:
        data = request.get_json()
        
        # Validación básica
        required_fields = ['nombre', 'email', 'servicio', 'mensaje']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'El campo {field} es requerido'
                }), 400
        
        # Crear nuevo mensaje
        message = ContactMessage(
            nombre=data['nombre'],
            email=data['email'],
            telefono=data.get('telefono', ''),
            servicio=data['servicio'],
            mensaje=data['mensaje'],
            ip_address=request.remote_addr
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mensaje enviado correctamente. Te contactaremos pronto.'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error al enviar el mensaje. Inténtalo de nuevo.'
        }), 500

@api_bp.route('/projects')
def get_projects():
    """API para obtener proyectos activos"""
    projects = Project.query.filter_by(activo=True).order_by(Project.orden).all()
    
    projects_data = []
    for project in projects:
        projects_data.append({
            'id': project.id,
            'titulo': project.titulo,
            'descripcion_problema': project.descripcion_problema,
            'descripcion_solucion': project.descripcion_solucion,
            'resultados': project.resultados,
            'imagen_url': project.imagen_url,
            'categoria': project.categoria,
            'cliente': getattr(project, 'cliente', None),
            'tecnologias': getattr(project, 'tecnologias', None),
            'duracion': getattr(project, 'duracion', None)
        })
    
    return jsonify(projects_data)

@api_bp.route('/testimonials')
def get_testimonials():
    """API para obtener testimonios activos"""
    testimonials = Testimonial.query.filter_by(activo=True).order_by(Testimonial.orden).all()
    
    testimonials_data = []
    for testimonial in testimonials:
        testimonials_data.append({
            'id': testimonial.id,
            'nombre_cliente': testimonial.nombre_cliente,
            'empresa': testimonial.empresa,
            'cargo': testimonial.cargo,
            'testimonio': testimonial.testimonio,
            'imagen_url': testimonial.imagen_url,
            'calificacion': getattr(testimonial, 'calificacion', 5),
            'proyecto_relacionado': getattr(testimonial, 'proyecto_relacionado', None)
        })
    
    return jsonify(testimonials_data)

@api_bp.route('/blog')
def get_blog_posts():
    """API para obtener artículos del blog"""
    posts = BlogPost.query.filter_by(publicado=True).order_by(BlogPost.fecha_publicacion.desc()).limit(6).all()
    
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'titulo': post.titulo,
            'slug': post.slug,
            'resumen': post.resumen,
            'imagen_url': post.imagen_url,
            'categoria': post.categoria,
            'tags': post.tags.split(',') if post.tags else [],
            'fecha_publicacion': post.fecha_publicacion.isoformat() if post.fecha_publicacion else None,
            'autor': getattr(post, 'autor', 'Noel Moreno'),
            'tiempo_lectura': getattr(post, 'tiempo_lectura', None),
            'vistas': post.vistas
        })
    
    return jsonify(posts_data)

@api_bp.route('/blog/<slug>')
def get_blog_post(slug):
    """API para obtener un artículo específico del blog"""
    post = BlogPost.query.filter_by(slug=slug, publicado=True).first()
    
    if not post:
        return jsonify({
            'success': False,
            'message': 'Artículo no encontrado'
        }), 404
    
    # Incrementar contador de vistas
    post.vistas += 1
    db.session.commit()
    
    return jsonify({
        'id': post.id,
        'titulo': post.titulo,
        'slug': post.slug,
        'contenido': post.contenido,
        'resumen': post.resumen,
        'imagen_url': post.imagen_url,
        'categoria': post.categoria,
        'tags': post.tags.split(',') if post.tags else [],
        'fecha_publicacion': post.fecha_publicacion.isoformat() if post.fecha_publicacion else None,
        'autor': getattr(post, 'autor', 'Noel Moreno'),
        'tiempo_lectura': getattr(post, 'tiempo_lectura', None),
        'vistas': post.vistas
    })

@api_bp.route('/dashboard/stats')
def get_dashboard_stats():
    """API para obtener estadísticas del dashboard"""
    try:
        stats = {
            'contact_count': ContactMessage.query.count(),
            'project_count': Project.query.filter_by(activo=True).count(),
            'testimonial_count': Testimonial.query.filter_by(activo=True).count(),
            'blog_count': BlogPost.query.filter_by(publicado=True).count()
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al obtener estadísticas'
        }), 500

@api_bp.route('/dashboard/recent-messages')
def get_recent_messages():
    """API para obtener mensajes recientes"""
    try:
        messages = ContactMessage.query.order_by(ContactMessage.fecha.desc()).limit(5).all()
        messages_data = []
        for message in messages:
            messages_data.append({
                'id': message.id,
                'nombre': message.nombre,
                'email': message.email,
                'mensaje': message.mensaje,
                'fecha': message.fecha.isoformat(),
                'leido': message.leido,
                'servicio': message.servicio
            })
        return jsonify(messages_data)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al obtener mensajes recientes'
        }), 500

# ==========================================
# RUTAS API DEL ADMINISTRADOR
# ==========================================

@api_bp.route('/admin/messages', methods=['GET'])
@login_required
def admin_get_messages():
    """API para obtener mensajes con paginación y filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
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
        
        messages_data = []
        for message in messages.items:
            messages_data.append({
                'id': message.id,
                'nombre': message.nombre,
                'email': message.email,
                'telefono': message.telefono,
                'servicio': message.servicio,
                'mensaje': message.mensaje,
                'fecha': message.fecha.isoformat(),
                'leido': message.leido,
                'ip_address': message.ip_address
            })
        
        return jsonify({
            'success': True,
            'messages': messages_data,
            'pagination': {
                'page': messages.page,
                'pages': messages.pages,
                'per_page': messages.per_page,
                'total': messages.total,
                'has_next': messages.has_next,
                'has_prev': messages.has_prev
            }
        })
        
    except Exception as e:
        logging.error(f"Error en API admin messages: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener mensajes'
        }), 500

@api_bp.route('/admin/messages/<int:message_id>', methods=['GET'])
@login_required
def admin_get_message(message_id):
    """API para obtener un mensaje específico"""
    try:
        message = ContactMessage.query.get_or_404(message_id)
        
        return jsonify({
            'success': True,
            'message': {
                'id': message.id,
                'nombre': message.nombre,
                'email': message.email,
                'telefono': message.telefono,
                'servicio': message.servicio,
                'mensaje': message.mensaje,
                'fecha': message.fecha.isoformat(),
                'leido': message.leido,
                'ip_address': message.ip_address
            }
        })
        
    except Exception as e:
        logging.error(f"Error en API admin message {message_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener el mensaje'
        }), 500

@api_bp.route('/admin/messages/<int:message_id>/mark-read', methods=['POST'])
@login_required
def admin_mark_message_read(message_id):
    """API para marcar un mensaje como leído"""
    try:
        message = ContactMessage.query.get_or_404(message_id)
        message.leido = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mensaje marcado como leído'
        })
        
    except Exception as e:
        logging.error(f"Error en API mark message read {message_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al marcar el mensaje'
        }), 500

@api_bp.route('/admin/messages/<int:message_id>', methods=['DELETE'])
@login_required
def admin_delete_message(message_id):
    """API para eliminar un mensaje"""
    try:
        message = ContactMessage.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mensaje eliminado correctamente'
        })
        
    except Exception as e:
        logging.error(f"Error en API delete message {message_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al eliminar el mensaje'
        }), 500

@api_bp.route('/admin/projects', methods=['GET'])
@login_required
def admin_get_projects():
    """API para obtener proyectos con paginación y filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
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
        
        projects_data = []
        for project in projects.items:
            projects_data.append({
                'id': project.id,
                'titulo': project.titulo,
                'descripcion_problema': project.descripcion_problema,
                'descripcion_solucion': project.descripcion_solucion,
                'resultados': project.resultados,
                'imagen_url': project.imagen_url,
                'categoria': project.categoria,
                'cliente': project.cliente,
                'tecnologias': project.tecnologias,
                'duracion': project.duracion,
                'activo': project.activo,
                'orden': project.orden,
                'fecha_creacion': project.fecha_creacion.isoformat() if project.fecha_creacion else None
            })
        
        return jsonify({
            'success': True,
            'projects': projects_data,
            'pagination': {
                'page': projects.page,
                'pages': projects.pages,
                'per_page': projects.per_page,
                'total': projects.total,
                'has_next': projects.has_next,
                'has_prev': projects.has_prev
            }
        })
        
    except Exception as e:
        logging.error(f"Error en API admin projects: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener proyectos'
        }), 500

@api_bp.route('/admin/testimonials', methods=['GET'])
@login_required
def admin_get_testimonials():
    """API para obtener testimonios con paginación y filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        filter_active = request.args.get('active', 'all')
        
        query = Testimonial.query
        
        if filter_active == 'active':
            query = query.filter_by(activo=True)
        elif filter_active == 'inactive':
            query = query.filter_by(activo=False)
        
        testimonials = query.order_by(Testimonial.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        testimonials_data = []
        for testimonial in testimonials.items:
            testimonials_data.append({
                'id': testimonial.id,
                'nombre_cliente': testimonial.nombre_cliente,
                'empresa': testimonial.empresa,
                'cargo': testimonial.cargo,
                'testimonio': testimonial.testimonio,
                'imagen_url': testimonial.imagen_url,
                'calificacion': testimonial.calificacion,
                'proyecto_relacionado': testimonial.proyecto_relacionado,
                'activo': testimonial.activo,
                'orden': testimonial.orden,
                'fecha_creacion': testimonial.fecha_creacion.isoformat() if testimonial.fecha_creacion else None
            })
        
        return jsonify({
            'success': True,
            'testimonials': testimonials_data,
            'pagination': {
                'page': testimonials.page,
                'pages': testimonials.pages,
                'per_page': testimonials.per_page,
                'total': testimonials.total,
                'has_next': testimonials.has_next,
                'has_prev': testimonials.has_prev
            }
        })
        
    except Exception as e:
        logging.error(f"Error en API admin testimonials: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener testimonios'
        }), 500

@api_bp.route('/admin/blog', methods=['GET'])
@login_required
def admin_get_blog_posts():
    """API para obtener artículos del blog con paginación y filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
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
        
        posts_data = []
        for post in posts.items:
            posts_data.append({
                'id': post.id,
                'titulo': post.titulo,
                'slug': post.slug,
                'resumen': post.resumen,
                'contenido': post.contenido,
                'imagen_url': post.imagen_url,
                'categoria': post.categoria,
                'tags': post.tags.split(',') if post.tags else [],
                'publicado': post.publicado,
                'vistas': post.vistas,
                'fecha_creacion': post.fecha_creacion.isoformat() if post.fecha_creacion else None,
                'fecha_publicacion': post.fecha_publicacion.isoformat() if post.fecha_publicacion else None
            })
        
        return jsonify({
            'success': True,
            'posts': posts_data,
            'pagination': {
                'page': posts.page,
                'pages': posts.pages,
                'per_page': posts.per_page,
                'total': posts.total,
                'has_next': posts.has_next,
                'has_prev': posts.has_prev
            }
        })
        
    except Exception as e:
        logging.error(f"Error en API admin blog: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener artículos del blog'
        }), 500

@api_bp.route('/admin/analytics', methods=['GET'])
@login_required
def admin_get_analytics():
    """API para obtener analytics y estadísticas detalladas"""
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
        
        # Estadísticas por período
        now = datetime.utcnow()
        periods = {
            'today': now - timedelta(days=1),
            'week': now - timedelta(weeks=1),
            'month': now - timedelta(days=30),
            'year': now - timedelta(days=365)
        }
        
        period_stats = {}
        for period_name, start_date in periods.items():
            period_stats[period_name] = {
                'messages': ContactMessage.query.filter(ContactMessage.fecha >= start_date).count(),
                'projects': Project.query.filter(Project.fecha_creacion >= start_date).count()
            }
        
        # Mensajes por servicio
        service_stats = db.session.query(
            ContactMessage.servicio,
            db.func.count(ContactMessage.id)
        ).group_by(ContactMessage.servicio).all()
        
        services_data = []
        for service, count in service_stats:
            if service:  # Solo incluir servicios no nulos
                services_data.append({
                    'service': service,
                    'count': count
                })
        
        return jsonify({
            'success': True,
            'stats': stats,
            'period_stats': period_stats,
            'services': services_data
        })
        
    except Exception as e:
        logging.error(f"Error en API admin analytics: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al obtener analytics'
        }), 500
