# Modelo de Testimonios
from datetime import datetime
from backend.database import db

class Testimonial(db.Model):
    """Modelo para testimonios de clientes"""
    __tablename__ = 'testimonial'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(150))
    cargo = db.Column(db.String(100))
    testimonio = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(500))
    activo = db.Column(db.Boolean, default=True)
    orden = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    calificacion = db.Column(db.Integer, default=5)
    proyecto_relacionado = db.Column(db.String(200))

    def __repr__(self):
        return f'<Testimonial {self.nombre_cliente} - {self.empresa}>'
