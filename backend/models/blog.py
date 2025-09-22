# Modelo de Blog
from datetime import datetime
from backend.database import db

class BlogPost(db.Model):
    """Modelo para artículos del blog"""
    __tablename__ = 'blog_post'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    resumen = db.Column(db.Text)
    imagen_url = db.Column(db.String(500))
    categoria = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    publicado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_publicacion = db.Column(db.DateTime)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    vistas = db.Column(db.Integer, default=0)
    autor = db.Column(db.String(100), default='Noel Moreno')
    tiempo_lectura = db.Column(db.Integer)  # en minutos

    def __repr__(self):
        return f'<BlogPost {self.titulo}>'
