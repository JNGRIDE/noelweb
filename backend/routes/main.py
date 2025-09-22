# Rutas principales
from flask import Blueprint, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal - redirige al frontend"""
    return redirect('/static/index.html')
