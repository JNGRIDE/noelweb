# Aplicación principal de Noel Moreno Website
import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS

# Importar configuración
from config import config

# Importar base de datos
from backend.database import db

# Inicializar extensiones
login_manager = LoginManager()

def create_app(config_name='default'):
    """Factory function para crear la aplicación"""
    app = Flask(__name__, template_folder='backend/templates')
    
    # Configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    
    # Configuración de Login Manager
    login_manager.login_view = 'auth.admin_login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from backend.models import User
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    from backend.routes import main_bp, api_bp, auth_bp
    from backend.routes.admin import admin_bp
    from backend.static_handler import static_bp
    app.register_blueprint(static_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # Ruta raíz que redirige al frontend
    @app.route('/')
    def root():
        return redirect('/static/index.html')
    
    # Definir clases para Flask-Admin
    from backend.models import User, ContactMessage, Project, Testimonial, BlogPost
    
    class SecureAdminIndexView(AdminIndexView):
        """Vista personalizada para el dashboard del admin"""
        def is_accessible(self):
            from flask_login import current_user
            return current_user.is_authenticated and current_user.is_admin
        
        def inaccessible_callback(self, name, **kwargs):
            from flask import redirect, url_for, request
            return redirect(url_for('auth.admin_login', next=request.url))
    
    class SecureModelView(ModelView):
        """Vista segura para el panel de administración"""
        def is_accessible(self):
            from flask_login import current_user
            return current_user.is_authenticated and current_user.is_admin
        
        def inaccessible_callback(self, name, **kwargs):
            from flask import redirect, url_for, request
            return redirect(url_for('auth.admin_login', next=request.url))
    
    # Inicializar Flask Admin con configuración personalizada
    admin = Admin(
        app, 
        name='Noel Moreno Admin',
        template_mode='bootstrap4',
        url='/admin-flask',
        index_view=SecureAdminIndexView(
            name='Dashboard',
            url='/admin-flask'
        )
    )
    
    class ContactMessageView(SecureModelView):
        """Vista personalizada para mensajes de contacto"""
        column_list = ['fecha', 'nombre', 'email', 'servicio', 'leido']
        column_labels = {
            'fecha': 'Fecha',
            'nombre': 'Nombre',
            'email': 'Email',
            'servicio': 'Servicio',
            'leido': 'Leído',
            'mensaje': 'Mensaje'
        }
        column_filters = ['fecha', 'servicio', 'leido']
        column_searchable_list = ['nombre', 'email', 'mensaje']
        
        def on_model_change(self, form, model, is_created):
            if not is_created:
                model.leido = True
    
    
    # Agregar vistas al admin
    admin.add_view(ContactMessageView(ContactMessage, db.session, name='Mensajes'))
    admin.add_view(SecureModelView(Project, db.session, name='Proyectos'))
    admin.add_view(SecureModelView(Testimonial, db.session, name='Testimonios'))
    admin.add_view(SecureModelView(BlogPost, db.session, name='Blog'))
    
    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
        create_admin_user()
        create_sample_data()
    
    return app

def create_admin_user():
    """Crear usuario administrador por defecto"""
    from backend.models import User
    
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@noelmoreno.com',
            is_admin=True
        )
        admin_user.set_password('admin123')  # Cambiar en producción
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Usuario administrador creado:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("   ⚠️  CAMBIAR LA CONTRASEÑA EN PRODUCCIÓN")

def create_sample_data():
    """Crear datos de ejemplo"""
    from backend.models import Project, Testimonial
    
    # Verificar si ya existen datos
    if Project.query.first() is not None:
        return
    
    # Proyectos de ejemplo
    projects = [
        Project(
            titulo="Sistema POS para Farmacia",
            descripcion_problema="La farmacia necesitaba un sistema que integrara ventas, inventario y facturación electrónica.",
            descripcion_solucion="Desarrollé un sistema completo con módulos de ventas, control de medicamentos y reportes automáticos.",
            resultados="40% reducción en tiempo de facturación, 25% mejora en control de inventario.",
            imagen_url="https://via.placeholder.com/400x300/4A90E2/FFFFFF?text=Sistema+POS",
            categoria="POS",
            orden=1,
            cliente="Farmacia San José",
            tecnologias="Python, Flask, SQLite, HTML/CSS/JS",
            duracion="2 meses"
        ),
        Project(
            titulo="Gestión de Inventario para Tienda",
            descripcion_problema="Pérdida de productos por falta de control y compras innecesarias.",
            descripcion_solucion="Sistema de inventario con códigos de barras, alertas automáticas y análisis de rotación.",
            resultados="60% reducción en productos perdidos, 30% optimización en compras.",
            imagen_url="https://via.placeholder.com/400x300/4A90E2/FFFFFF?text=Inventario+Digital",
            categoria="Inventario",
            orden=2,
            cliente="Supermercado El Ahorro",
            tecnologias="Python, Django, PostgreSQL, React",
            duracion="3 meses"
        ),
        Project(
            titulo="Automatización de Reportes",
            descripcion_problema="Tiempo excesivo en la elaboración manual de reportes mensuales.",
            descripcion_solucion="Dashboard automatizado con reportes en tiempo real y alertas personalizadas.",
            resultados="80% reducción en tiempo de reportes, decisiones más rápidas y precisas.",
            imagen_url="https://via.placeholder.com/400x300/4A90E2/FFFFFF?text=Reportes+Automaticos",
            categoria="Reportes",
            orden=3,
            cliente="Boutique Elegance",
            tecnologias="Python, FastAPI, MongoDB, Vue.js",
            duracion="1 mes"
        )
    ]
    
    # Testimonios de ejemplo
    testimonials = [
        Testimonial(
            nombre_cliente="María González",
            empresa="Farmacia San José",
            cargo="Propietaria",
            testimonio="Noel transformó completamente nuestro negocio. El sistema POS que desarrolló nos ahorra horas de trabajo diario y nos da visibilidad total de nuestras ventas.",
            orden=1,
            calificacion=5,
            proyecto_relacionado="Sistema POS para Farmacia"
        ),
        Testimonial(
            nombre_cliente="Carlos Rodríguez",
            empresa="Supermercado El Ahorro",
            cargo="Gerente",
            testimonio="La gestión de inventario que implementó Noel nos ayudó a reducir pérdidas significativamente. Ahora sabemos exactamente qué tenemos y qué necesitamos comprar.",
            orden=2,
            calificacion=5,
            proyecto_relacionado="Gestión de Inventario para Tienda"
        ),
        Testimonial(
            nombre_cliente="Ana Martínez",
            empresa="Boutique Elegance",
            cargo="Dueña",
            testimonio="Excelente profesional. Entiende las necesidades reales de los pequeños negocios y crea soluciones prácticas y accesibles. Totalmente recomendado.",
            orden=3,
            calificacion=5,
            proyecto_relacionado="Automatización de Reportes"
        )
    ]
    
    # Agregar datos a la base de datos
    for project in projects:
        db.session.add(project)
    
    for testimonial in testimonials:
        db.session.add(testimonial)
    
    db.session.commit()
    print("✅ Datos de ejemplo creados")

# Crear aplicación
app = create_app()

if __name__ == '__main__':
    print("\n🚀 Backend de Noel Moreno iniciado")
    print("📊 Panel de administración: http://localhost:5000/admin")
    print("🔐 Usuario: admin / Contraseña: admin123")
    print("🌐 Frontend: http://localhost:5000/static/index.html")
    print("📡 API disponible en: http://localhost:5000/api/")
    print("\n⚠️  IMPORTANTE: Cambiar contraseña en producción")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
