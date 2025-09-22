# Modelo de Proyectos
from datetime import datetime
from backend.database import db

class Project(db.Model):
    """Modelo para proyectos mostrados en la web"""
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion_problema = db.Column(db.Text, nullable=False)
    descripcion_solucion = db.Column(db.Text, nullable=False)
    resultados = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(500))
    categoria = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cliente = db.Column(db.String(150))
    tecnologias = db.Column(db.String(200))
    duracion = db.Column(db.String(50))

    def __repr__(self):
        return f'<Project {self.titulo}>'
