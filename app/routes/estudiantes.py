"""
Gestión de estudiantes.

Los estudiantes están siempre vinculados a una asignación concreta.
Aquí gestiono altas, bajas, finalizaciones y su estado general.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Estudiante, AsignacionCurso
from app.routes.auth import login_requerido

# Blueprint específico de estudiantes
estudiantes_bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')


@estudiantes_bp.route('/asignacion/<int:id_asignacion>')
@login_requerido
def listar(id_asignacion):
    """Lista estudiantes de una asignación específica"""
    
    asignacion = AsignacionCurso.query.get_or_404(id_asignacion)
    
    # Verifico que sea del docente actual
    if asignacion.id_usuario != session.get('usuario_id'):
        flash('No tienes permisos para ver estos estudiantes', 'error')
        return redirect(url_for('asignaciones.listar'))
    
    estudiantes = (Estudiante.query
                   .filter_by(id_asignacion=id_asignacion)
                   .order_by(Estudiante.nombre_alumno)
                   .all())
    
    return render_template(
        'estudiantes/listar.html',
        estudiantes=estudiantes,
        asignacion=asignacion
    )


@estudiantes_bp.route('/nuevo/<int:id_asignacion>', methods=['GET', 'POST'])
@login_requerido
def nuevo(id_asignacion):
    """Añadir estudiante a una asignación"""
    
    asignacion = AsignacionCurso.query.get_or_404(id_asignacion)
    
    if asignacion.id_usuario != session.get('usuario_id'):
        flash('No tienes permisos', 'error')
        return redirect(url_for('asignaciones.listar'))
    
    if request.method == 'POST':
        estudiante = Estudiante(
            id_asignacion=id_asignacion,
            nombre_alumno=request.form.get('nombre_alumno'),
            correo_electronico=request.form.get('correo_electronico'),
            matricula=request.form.get('matricula'),
            estado_alumno=request.form.get('estado_alumno', 'activo')
        )
        
        try:
            db.session.add(estudiante)
            db.session.commit()
            flash(f'Estudiante "{estudiante.nombre_alumno}" añadido correctamente', 'success')
            return redirect(url_for('estudiantes.listar', id_asignacion=id_asignacion))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al añadir estudiante: {str(e)}', 'error')
    
    return render_template(
        'estudiantes/formulario.html',
        estudiante=None,
        asignacion=asignacion
    )


@estudiantes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar(id):
    """Editar datos de un estudiante"""
    
    estudiante = Estudiante.query.get_or_404(id)
    asignacion = estudiante.asignacion
    
    if asignacion.id_usuario != session.get('usuario_id'):
        flash('No tienes permisos', 'error')
        return redirect(url_for('asignaciones.listar'))
    
    if request.method == 'POST':
        estudiante.nombre_alumno = request.form.get('nombre_alumno')
        estudiante.correo_electronico = request.form.get('correo_electronico')
        estudiante.matricula = request.form.get('matricula')
        estudiante.estado_alumno = request.form.get('estado_alumno')
        
        try:
            db.session.commit()
            flash(f'Estudiante "{estudiante.nombre_alumno}" actualizado', 'success')
            return redirect(url_for('estudiantes.listar', id_asignacion=asignacion.id_asignacion))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    return render_template(
        'estudiantes/formulario.html',
        estudiante=estudiante,
        asignacion=asignacion
    )


@estudiantes_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_requerido
def eliminar(id):
    """Eliminar estudiante"""
    
    estudiante = Estudiante.query.get_or_404(id)
    asignacion = estudiante.asignacion
    
    if asignacion.id_usuario != session.get('usuario_id'):
        flash('No tienes permisos', 'error')
        return redirect(url_for('asignaciones.listar'))
    
    nombre = estudiante.nombre_alumno
    id_asignacion = estudiante.id_asignacion
    
    try:
        db.session.delete(estudiante)
        db.session.commit()
        flash(f'Estudiante "{nombre}" eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'error')
    
    return redirect(url_for('estudiantes.listar', id_asignacion=id_asignacion))


@estudiantes_bp.route('/cambiar_estado/<int:id>/<nuevo_estado>', methods=['POST'])
@login_requerido
def cambiar_estado(id, nuevo_estado):
    """
    Cambio rápido de estado de un estudiante.
    
    Esto lo añadí porque es muy común marcar estudiantes como
    finalizados o dados de baja sin tener que editar todo el formulario.
    """
    
    estudiante = Estudiante.query.get_or_404(id)
    asignacion = estudiante.asignacion
    
    if asignacion.id_usuario != session.get('usuario_id'):
        flash('No tienes permisos', 'error')
        return redirect(url_for('asignaciones.listar'))
    
    estados_validos = ['activo', 'baja', 'finalizado']
    if nuevo_estado not in estados_validos:
        flash('Estado no válido', 'error')
        return redirect(url_for('estudiantes.listar', id_asignacion=asignacion.id_asignacion))
    
    estudiante.estado_alumno = nuevo_estado
    
    try:
        db.session.commit()
        flash(f'{estudiante.nombre_alumno} marcado como {nuevo_estado}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('estudiantes.listar', id_asignacion=asignacion.id_asignacion))
