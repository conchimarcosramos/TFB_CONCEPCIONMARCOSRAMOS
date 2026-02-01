"""
Dashboard principal del docente.

Aquí muestro un resumen de todo: asignaciones activas,
cursos próximos, ingresos del mes, etc.
"""

from flask import Blueprint, render_template, session
from app import db
from app.models import AsignacionCurso, Empresa, Curso, Estudiante, Ingreso
from app.routes.auth import login_requerido
from sqlalchemy import func, extract
from datetime import datetime, date

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_requerido
def mostrar():
    """Pantalla principal tras el login"""
    
    usuario_id = session.get('usuario_id')
    
    # Asignaciones activas
    asignaciones_activas = AsignacionCurso.query.filter_by(
        id_usuario=usuario_id,
        estado_asignacion='activa'
    ).order_by(AsignacionCurso.fecha_inicio.desc()).all()
    
    # Totales generales
    total_empresas = Empresa.query.count()
    total_cursos = Curso.query.count()
    
    # Total estudiantes en asignaciones activas
    total_estudiantes = db.session.query(func.count(Estudiante.id_estudiante))\
        .join(AsignacionCurso)\
        .filter(AsignacionCurso.id_usuario == usuario_id)\
        .filter(AsignacionCurso.estado_asignacion == 'activa')\
        .scalar() or 0
    
    # Ingresos del mes actual
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    ingresos_mes = db.session.query(func.sum(Ingreso.cantidad))\
        .join(AsignacionCurso)\
        .filter(AsignacionCurso.id_usuario == usuario_id)\
        .filter(extract('month', Ingreso.fecha_calculo) == mes_actual)\
        .filter(extract('year', Ingreso.fecha_calculo) == año_actual)\
        .scalar() or 0
    
    # Próximas asignaciones (que empiezan pronto)
    hoy = date.today()
    proximas_asignaciones = AsignacionCurso.query.filter_by(
        id_usuario=usuario_id
    ).filter(
        AsignacionCurso.fecha_inicio > hoy
    ).order_by(AsignacionCurso.fecha_inicio).limit(5).all()
    
    return render_template('dashboard.html',
        asignaciones_activas=asignaciones_activas,
        proximas_asignaciones=proximas_asignaciones,
        total_empresas=total_empresas,
        total_cursos=total_cursos,
        total_estudiantes=total_estudiantes,
        ingresos_mes=float(ingresos_mes),
        nombre_usuario=session.get('nombre_usuario')
    )

# Alias para mantener consistencia con otros módulos
dashboard_bp = bp
