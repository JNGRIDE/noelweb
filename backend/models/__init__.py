# Importar todos los modelos
from .user import User
from .contact import ContactMessage
from .project import Project
from .testimonial import Testimonial
from .blog import BlogPost

__all__ = ['User', 'ContactMessage', 'Project', 'Testimonial', 'BlogPost']