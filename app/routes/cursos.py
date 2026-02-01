"""
Gestión de cursos

Aquí mantengo el catálogo de cursos que imparto.
Los códigos son los oficiales del SEPE (tipo IFCD084PO).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Curso
from app.routes.auth import login_requerido

cursos_bp = Blueprint('cursos', __name__)


@cursos_bp.route('/')
@login_requerido
def listar():
    """Lista todos los cursos ordenados por código"""
    cursos = Curso.query.order_by(Curso.codigo_curso).all()
    return render_template('cursos/listar.html', cursos=cursos)


@cursos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_requerido
def nuevo():
    """Formulario para crear un curso nuevo"""
    if request.method == 'POST':
        codigo = request.form.get('codigo_curso', '').strip()
        
        # Compruebo que no exista ya
        if Curso.query.filter_by(codigo_curso=codigo).first():
            flash(f'Ya hay un curso con código {codigo}', 'error')
            return render_template('cursos/formulario.html')
        
        try:
            curso = Curso(
                codigo_curso=codigo,
                nombre_curso=request.form.get('nombre_curso', '').strip(),
                horas_curso=int(request.form.get('horas_curso', 0))
            )
            db.session.add(curso)
            db.session.commit()
            flash(f'Curso {codigo} creado', 'success')
            return redirect(url_for('cursos.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('cursos/formulario.html')


@cursos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar(id):
    """Editar un curso"""
    curso = Curso.query.get_or_404(id)
    
    if request.method == 'POST':
        codigo = request.form.get('codigo_curso', '').strip()
        
        # Verifico que el código no esté duplicado (excluyendo el actual)
        otro = Curso.query.filter_by(codigo_curso=codigo).first()
        if otro and otro.id_curso != id:
            flash(f'Ya existe otro curso con código {codigo}', 'error')
            return render_template('cursos/formulario.html', curso=curso)
        
        try:
            curso.codigo_curso = codigo
            curso.nombre_curso = request.form.get('nombre_curso', '').strip()
            curso.horas_curso = int(request.form.get('horas_curso', 0))
            db.session.commit()
            flash(f'Curso {codigo} actualizado', 'success')
            return redirect(url_for('cursos.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('cursos/formulario.html', curso=curso)


@cursos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_requerido
def eliminar(id):
    """Borrar un curso (solo si no tiene asignaciones)"""
    curso = Curso.query.get_or_404(id)
    
    # No dejo borrar si tiene asignaciones porque perdería datos
    if curso.asignaciones:
        flash(f'No puedo borrar {curso.codigo_curso}, tiene asignaciones', 'error')
        return redirect(url_for('cursos.listar'))
    
    try:
        codigo = curso.codigo_curso
        db.session.delete(curso)
        db.session.commit()
        flash(f'Curso {codigo} eliminado', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al borrar: {str(e)}', 'error')
    
    return redirect(url_for('cursos.listar'))
