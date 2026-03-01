from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Asistencia, Estudiante, AsignacionCurso

asistencia_bp = Blueprint('asistencia', __name__, template_folder='../templates')

@asistencia_bp.route('/')
def listar_asistencia():
    asistencias = Asistencia.query.all()
    return render_template('asistencia/listar.html', asistencias=asistencias)

@asistencia_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_asistencia():
    if request.method == 'POST':
        # Lógica para guardar asistencia
        flash('Asistencia registrada correctamente', 'success')
        return redirect(url_for('asistencia.listar_asistencia'))
    
    asignaciones = AsignacionCurso.query.all()
    return render_template('asistencia/nueva.html', asignaciones=asignaciones)
