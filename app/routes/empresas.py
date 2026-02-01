"""
Gestión de empresas.

CRUD completo: listar, crear, editar, eliminar.
Las empresas son fundamentales porque de ellas dependen las tarifas
y las condiciones de pago.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Empresa
from app.routes.auth import login_requerido

bp = Blueprint('empresas', __name__, url_prefix='/empresas')

@bp.route('/')
@login_requerido
def listar():
    """Lista todas las empresas"""
    empresas = Empresa.query.order_by(Empresa.nombre_comercial).all()
    return render_template('empresas/listar.html', empresas=empresas)


@bp.route('/nueva', methods=['GET', 'POST'])
@login_requerido
def nueva():
    """Crear nueva empresa"""
    
    if request.method == 'POST':
        empresa = Empresa(
            nombre_fiscal=request.form.get('nombre_fiscal'),
            nombre_comercial=request.form.get('nombre_comercial'),
            nif_cif=request.form.get('nif_cif'),
            direccion=request.form.get('direccion'),
            persona_contacto=request.form.get('persona_contacto'),
            correo_electronico=request.form.get('correo_electronico'),
            telefono=request.form.get('telefono'),
            plataformas=request.form.get('plataformas'),
            tarifa_hora=request.form.get('tarifa_hora') or None,
            forma_pago=request.form.get('forma_pago'),
            plazo_pago=request.form.get('plazo_pago') or None,
            notas=request.form.get('notas')
        )
        
        try:
            db.session.add(empresa)
            db.session.commit()
            flash(f'Empresa "{empresa.nombre_comercial or empresa.nombre_fiscal}" creada correctamente', 'success')
            return redirect(url_for('empresas.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la empresa: {str(e)}', 'error')
    
    return render_template('empresas/formulario.html', empresa=None)


@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar(id):
    """Editar empresa existente"""
    
    empresa = Empresa.query.get_or_404(id)
    
    if request.method == 'POST':
        empresa.nombre_fiscal = request.form.get('nombre_fiscal')
        empresa.nombre_comercial = request.form.get('nombre_comercial')
        empresa.nif_cif = request.form.get('nif_cif')
        empresa.direccion = request.form.get('direccion')
        empresa.persona_contacto = request.form.get('persona_contacto')
        empresa.correo_electronico = request.form.get('correo_electronico')
        empresa.telefono = request.form.get('telefono')
        empresa.plataformas = request.form.get('plataformas')
        empresa.tarifa_hora = request.form.get('tarifa_hora') or None
        empresa.forma_pago = request.form.get('forma_pago')
        empresa.plazo_pago = request.form.get('plazo_pago') or None
        empresa.notas = request.form.get('notas')
        
        try:
            db.session.commit()
            flash(f'Empresa "{empresa.nombre_comercial or empresa.nombre_fiscal}" actualizada', 'success')
            return redirect(url_for('empresas.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'error')
    
    return render_template('empresas/formulario.html', empresa=empresa)


@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_requerido
def eliminar(id):
    """Eliminar empresa"""
    
    empresa = Empresa.query.get_or_404(id)
    nombre = empresa.nombre_comercial or empresa.nombre_fiscal
    
    try:
        db.session.delete(empresa)
        db.session.commit()
        flash(f'Empresa "{nombre}" eliminada correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}. Puede que tenga asignaciones asociadas.', 'error')
    
    return redirect(url_for('empresas.listar'))


@bp.route('/ver/<int:id>')
@login_requerido
def ver(id):
    """Ver detalle de empresa con sus asignaciones"""
    empresa = Empresa.query.get_or_404(id)
    return render_template('empresas/detalle.html', empresa=empresa)

# Para que se pueda importar como empresas_bp en __init__.py
empresas_bp = bp
