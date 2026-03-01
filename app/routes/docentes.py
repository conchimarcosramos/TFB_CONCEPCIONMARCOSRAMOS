"""
Gestión de docentes.

CRUD completo para docentes: listar, crear, editar, eliminar.
Los docentes están vinculados a usuarios del sistema.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Docente, Usuario
from app.routes.auth import login_requerido

bp = Blueprint('docentes', __name__, url_prefix='/docentes')


@bp.route('/')
@login_requerido
def listar():
    """Lista todos los docentes"""
    docentes = Docente.query.order_by(Docente.nombre).all()
    return render_template('docentes/listar.html', docentes=docentes)


@bp.route('/nuevo', methods=['GET', 'POST'])
@login_requerido
def nuevo():
    """Crear nuevo docente"""
    
    if request.method == 'POST':
        # Verificar si el usuario ya tiene un docente asociado
        id_usuario = request.form.get('id_usuario') or None
        if id_usuario:
            docente_existente = Docente.query.filter_by(id_usuario=id_usuario).first()
            if docente_existente:
                flash('Este usuario ya tiene un perfil de docente asociado', 'error')
                usuarios = Usuario.query.order_by(Usuario.nombre_usuario).all()
                return render_template('docentes/formulario.html', docente=None, usuarios=usuarios)
        
        docente = Docente(
            nombre=request.form.get('nombre'),
            email=request.form.get('email'),
            telefono=request.form.get('telefono'),
            especialidad=request.form.get('especialidad'),
            activo=request.form.get('activo') == 'on',
            es_admin=request.form.get('es_admin') == 'on',
            id_usuario=id_usuario
        )
        
        try:
            db.session.add(docente)
            db.session.commit()
            flash(f'Docente "{docente.nombre}" creado correctamente', 'success')
            return redirect(url_for('docentes.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el docente: {str(e)}', 'error')
    
    usuarios = Usuario.query.order_by(Usuario.nombre_usuario).all()
    return render_template('docentes/formulario.html', docente=None, usuarios=usuarios)


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar(id):
    """Editar docente existente"""
    
    docente = Docente.query.get_or_404(id)
    
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario') or None
        
        # Verificar si otro docente ya tiene ese usuario
        if id_usuario and id_usuario != str(docente.id_usuario):
            docente_existente = Docente.query.filter_by(id_usuario=id_usuario).first()
            if docente_existente:
                flash('Este usuario ya tiene un perfil de docente asociado', 'error')
                usuarios = Usuario.query.order_by(Usuario.nombre_usuario).all()
                return render_template('docentes/formulario.html', docente=docente, usuarios=usuarios)
        
        docente.nombre = request.form.get('nombre')
        docente.email = request.form.get('email')
        docente.telefono = request.form.get('telefono')
        docente.especialidad = request.form.get('especialidad')
        docente.activo = request.form.get('activo') == 'on'
        docente.es_admin = request.form.get('es_admin') == 'on'
        docente.id_usuario = id_usuario
        
        try:
            db.session.commit()
            flash(f'Docente "{docente.nombre}" actualizado', 'success')
            return redirect(url_for('docentes.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    usuarios = Usuario.query.order_by(Usuario.nombre_usuario).all()
    return render_template('docentes/formulario.html', docente=docente, usuarios=usuarios)


@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_requerido
def eliminar(id):
    """Eliminar docente"""
    
    docente = Docente.query.get_or_404(id)
    nombre = docente.nombre
    
    try:
        db.session.delete(docente)
        db.session.commit()
        flash(f'Docente "{nombre}" eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'error')
    
    return redirect(url_for('docentes.listar'))


@bp.route('/ver/<int:id>')
@login_requerido
def ver(id):
    """Ver detalle de docente"""
    docente = Docente.query.get_or_404(id)
    return render_template('docentes/detalle.html', docente=docente)


# Para que se pueda importar como docentes_bp en __init__.py
docentes_bp = bp
