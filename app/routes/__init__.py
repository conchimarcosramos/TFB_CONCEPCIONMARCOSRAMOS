"""
Registro de blueprints

Al principio tenía todo en un solo archivo y era un caos.
Con blueprints cada módulo va por separado y es más fácil de mantener.
A ultima hora añado docentes porque es un módulo que se va a usar mucho para asignar cursos, calificaciones, etc.
"""
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.empresas import empresas_bp
from app.routes.cursos import cursos_bp
from app.routes.asignaciones import asignaciones_bp
from app.routes.estudiantes import estudiantes_bp
from app.routes.calificaciones import calificaciones_bp
from app.routes.asistencia import asistencia_bp  
from app.routes.ingresos import ingresos_bp
from app.routes.docentes import docentes_bp


def register_blueprints(app):
    """
    Registra todos los blueprints en la app.
    Los prefijos URL los pongo aquí para tenerlos centralizados.
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(empresas_bp, url_prefix='/empresas')
    app.register_blueprint(cursos_bp, url_prefix='/cursos')
    app.register_blueprint(asignaciones_bp, url_prefix='/asignaciones')
    app.register_blueprint(estudiantes_bp, url_prefix='/estudiantes')
    app.register_blueprint(calificaciones_bp, url_prefix='/calificaciones')
    app.register_blueprint(asistencia_bp, url_prefix='/asistencia')  
    app.register_blueprint(ingresos_bp, url_prefix='/ingresos')
    app.register_blueprint(docentes_bp, url_prefix='/docentes')       