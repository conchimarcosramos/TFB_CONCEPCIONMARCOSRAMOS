"""
Gestión de asignaciones de curso.

Las asignaciones son el núcleo de GESTTATION: vinculan docente, empresa
y curso con fechas, horarios y grupo específico.

Una misma formación puede impartirse varias veces (diferentes empresas,
diferentes grupos, diferentes fechas).
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import AsignacionCurso, Empresa, Curso, Estudiante
from app.routes.auth import login_requerido
from datetime import datetime

bp = Blueprint('asignaciones', __name__, url_prefix='/asignaciones')

@bp.route('/')
@login_requerido
def listar():
    """Lista todas las asignaciones del docente"""
    usuario_id = session.get('usuario_id')
    
    # Filtro por estado si viene en la query string
    estado = request.args.get('estado', 'todas')
    
    query = AsignacionCurso.query.filter_by(id_usuario=usuario_id)
    
    if estado != 'todas':
        query = query.filter_by(estado_asignacion=estado)
    
    asignaciones = query.order_by(AsignacionCurso.fecha_inicio.desc()).all()
    
    return render_template('asignaciones/listar.html', 
                         asignaciones=asignaciones,
                         estado_filtro=estado)


@bp.route('/nueva', methods=['GET', 'POST'])
@login_requerido
def nueva():
    """Crear nueva asignación"""
    
    if request.method == 'POST':
        # Convierto las fechas de string a date
        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_fin_str = request.form.get('fecha_fin')
        
        asignacion = AsignacionCurso(
            id_usuario=session.get('usuario_id'),
            id_empresa=request.form.get('id_empresa'),
            id_curso=request.form.get('id_curso'),
            url_plataforma=request.form.get('url_plataforma'),
            usuario_plataforma=request.form.get('usuario_plataforma'),
            clave_plataforma=request.form.get('clave_plataforma'),
            hora_entrada=request.form.get('hora_entrada') or None,
            hora_salida=request.form.get('hora_salida') or None,
            fecha_inicio=datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None,
            fecha_fin=datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None,
            codigo_accion=request.form.get('codigo_accion'),
            codigo_grupo=request.form.get('codigo_grupo'),
            plan_formativo=request.form.get('plan_formativo'),
            estado_asignacion=request.form.get('estado_asignacion', 'activa')
        )
        
        try:
            db.session.add(asignacion)
            db.session.commit()
            flash(f'Asignación "{asignacion.codigo_grupo}" creada correctamente', 'success')
            return redirect(url_for('asignaciones.ver', id=asignacion.id_asignacion))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la asignación: {str(e)}', 'error')
    
    # Cargo empresas y cursos para los selectores
    empresas = Empresa.query.order_by(Empresa.nombre_comercial).all()
    cursos = Curso.query.order_by(Curso.codigo_curso).all()
    
    return render_template('asignaciones/formulario.html', 
                         asignacion=None,
                         empresas=empresas,
                         cursos=cursos)


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar(id):
    """Editar asignación existente"""
    
    asignacion = AsignacionCurso.query.get_or_404(id)
    
    # Verifico que la asignación sea del docente actual
    if asignacion.id_usuario != session.get('usuario_id'):
        flash('No tienes permisos para editar esta asignación', 'error')
        return redirect(url_for('asignaciones.listar'))
    
    if request.method == 'POST':
        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_fin_str = request.form.get('fecha_fin')
        
        asignacion.id_empresa = request.form.get('id_empresa')
        asignacion.id_curso = request.form.get('id_curso')
        asignacion.url_plataforma = request.form.get('url_plataforma')
        asignacion.usuario_plataforma = request.form.get('usuario_plataforma')
        asignacion.clave_plataforma = request.form.get('clave_plataforma')
        asignacion.hora_entrada = request.form.get('hora_entrada') or None
        asignacion.hora_salida = request.form.get('hora_salida') or None
        asignacion.fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
        asignacion.fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None
        asignacion.codigo_accion = request.form.get('codigo_accion')
        asignacion.codigo_grupo = request.form.get('codigo_grupo')
        asignacion.plan_formativo = request.form.get('plan_formativo')
        asignacion.estado_asignacion = request.form.get('estado_asignacion')
        
        try:
            db.session.commit()
            flash(f'Asignación "{asignacion.codigo_grupo}" actualizada', 'success')
            return redirect(url_for('asignaciones.ver', id=asignacion.id_asignacion))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    empresas = Empresa.query.order_by(Empresa.nombre_comercial).all()
    cursos = Curso.query.order_by(Curso.codigo_curso).all()
    
    return render_template('asignaciones/formulario.html',
                         asignacion=asignacion,
                         empresas=empresas,
                         cursos=cursos)


@bp.route('/ver/<int:id>')
@login_requerido
def ver(id):
    """Ver detalle completo de una asignación"""
    
    asignacion = AsignacionCurso.query.get_or_404(id)
    
    # Verifico permisos
    if asignacion.id_usuario != session.get('usuario_id'):
        flash('No tienes permisos para ver esta asignación', 'error')
        return redirect(url_for('asignaciones.listar'))
    
    # Cargo estadísticas básicas
    total_estudiantes = len(asignacion.estudiantes)
    estudiantes_activos = sum(1 for e in asignacion.estudiantes if e.estado_alumno == 'activo')
    estudiantes_finalizados = sum(1 for e in asignacion.estudiantes if e.estado_alumno == 'finalizado')
    
    return render_template('asignaciones/detalle.html',
                         asignacion=asignacion,
                         total_estudiantes=total_estudiantes,
                         estudiantes_activos=estudiantes_activos,
                         estudiantes_finalizados=estudiantes_finalizados)


@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_requerido
def eliminar(id):
    """Eliminar asignación"""
    
    asignacion = AsignacionCurso.query.get_or_404(id)
    
    if asignacion.id_usuario != session.get('usuario_id'):
        flash('No tienes permisos para eliminar esta asignación', 'error')
        return redirect(url_for('asignaciones.listar'))
    
    codigo_grupo = asignacion.codigo_grupo
    
    try:
        db.session.delete(asignacion)
        db.session.commit()
        flash(f'Asignación "{codigo_grupo}" eliminada correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'error')
    
    return redirect(url_for('asignaciones.listar'))
asignaciones_bp = bp
