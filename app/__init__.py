"""
Inicialización de la aplicación Flask
GESTTATION - Gestor Integral de Cursos para Docentes
TFB 2025-2026 - Universitat Carlemany
"""
"""
Inicialización de la aplicación Flask
GESTTATION - Gestor Integral de Cursos para Docentes
TFB 2025-2026 - Universitat Carlemany
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# Ruta base del paquete app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Ruta raíz del proyecto (un nivel arriba de app/)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

# Inicializar la base de datos
db = SQLAlchemy()

def create_app():
    """
    Crear y configurar la aplicación Flask
    """
    app = Flask(
        __name__,
        template_folder=os.path.join(PROJECT_ROOT, 'templates'),
        static_folder=os.path.join(BASE_DIR, 'static')
    )

    # Cargar configuración
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)

    # Registrar blueprints
    with app.app_context():
        from app.routes import register_blueprints
        register_blueprints(app)

        # Crear las tablas en la base de datos si no existen
        db.create_all()

    return app
