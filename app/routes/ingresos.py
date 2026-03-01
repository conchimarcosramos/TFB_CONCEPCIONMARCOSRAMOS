from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Ingreso, AsignacionCurso, Empresa, ModeloPago

ingresos_bp = Blueprint('ingresos', __name__, template_folder='../templates')

@ingresos_bp.route('/')
def listar_ingresos():
    ingresos = Ingreso.query.all()
    return render_template('ingresos/listar.html', ingresos=ingresos)

@ingresos_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_ingreso():
    if request.method == 'POST':
        # Lógica para guardar ingreso
        flash('Ingreso registrado correctamente', 'success')
        return redirect(url_for('ingresos.listar_ingresos'))
    
    asignaciones = AsignacionCurso.query.all()
    empresas = Empresa.query.all()
    modelos = ModeloPago.query.all()
    return render_template('ingresos/nuevo.html', asignaciones=asignaciones, empresas=empresas, modelos=modelos)
