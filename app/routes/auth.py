"""
Rutas de autenticación.

Login, logout y gestión de sesiones.
He usado sesiones de Flask en lugar de JWT porque para un solo usuario
me pareció más sencillo y no necesito API stateless por ahora.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Pantalla de inicio de sesión"""
    
    if request.method == 'POST':
        nombre_usuario = request.form.get('usuario')
        password = request.form.get('password')
        
        # Busco el usuario en la BD
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        
        # Verifico credenciales
        if usuario and usuario.verificar_clave(password):
            # Guardo en sesión
            session['usuario_id'] = usuario.id_usuario
            session['nombre_usuario'] = usuario.nombre_usuario
            session.permanent = True  # Para que use PERMANENT_SESSION_LIFETIME
            
            flash(f'¡Bienvenido/a {usuario.nombre_usuario}!', 'success')
            return redirect(url_for('dashboard.mostrar'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Cierre de sesión"""
    nombre = session.get('nombre_usuario', 'Usuario')
    session.clear()
    flash(f'Hasta pronto, {nombre}', 'info')
    return redirect(url_for('auth.login'))


def login_requerido(f):
    """
    Decorador para proteger rutas que requieren autenticación.
    Lo uso en lugar de Flask-Login porque me pareció innecesario
    añadir otra dependencia para un solo usuario.
    Si en el futuro amplio a multi-usuario podría migrar a Flask-Login sin mucho esfuerzo.
    """
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    
    return decorated_function