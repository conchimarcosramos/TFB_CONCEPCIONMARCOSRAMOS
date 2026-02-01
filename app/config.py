"""
Configuración de la aplicación.

Aquí centralizo todas las variables de configuración.
En un principio tenía los valores hardcodeados pero luego
descubrí que era mejor usar variables de entorno.
"""

import os
from datetime import timedelta

class Config:
    # Secret key para las sesiones - En producción DEBE cambiar
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-tfb-2026'
    
    # Configuración de la base de datos
    # El formato es: postgresql://usuario:contraseña@host:puerto/nombre_bd
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://gesttation:gesttation2026@db:5432/gesttation'
    
    # Esto lo pongo en False porque SQLAlchemy recomendaba desactivarlo
    # para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)  # 8 horas de clase
    SESSION_COOKIE_SECURE = False  # En producción con HTTPS debe ser True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración para subida de archivos (importación Moodle)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB máximo
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
