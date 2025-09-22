# Modelo de Mensajes de Contacto
from datetime import datetime
from backend.database import db

class ContactMessage(db.Model):
    """Modelo para mensajes de contacto"""
    __tablename__ = 'contact_message'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    servicio = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    leido = db.Column(db.Boolean, default=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    respuesta = db.Column(db.Text)
    fecha_respuesta = db.Column(db.DateTime)

    def __repr__(self):
        return f'<ContactMessage {self.nombre} - {self.email}>'
