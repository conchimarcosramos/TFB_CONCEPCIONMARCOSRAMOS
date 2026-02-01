"""
Modelos de datos de GESTTATION.

Aquí defino las clases que representan las tablas de la BD.
SQLAlchemy hace todo el trabajo pesado de mapeo objeto-relacional.

Al principio intenté hacer queries SQL directas pero esto es mucho más limpio
aunque la curva de aprendizaje fue un poco dura.
"""

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    correo_electronico = db.Column(db.String(255), unique=True, nullable=False)
    clave_hash = db.Column(db.String(255), nullable=False)
    rol_usuario = db.Column(db.String(50), default='docente')
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    asignaciones = db.relationship('AsignacionCurso', backref='docente', lazy=True)
    modelos_pago = db.relationship('ModeloPago', backref='usuario', lazy=True)
    
    def establecer_clave(self, password):
        """Genero el hash de la contraseña usando werkzeug (scrypt por defecto)"""
        self.clave_hash = generate_password_hash(password)
    
    def verificar_clave(self, password):
        """Compruebo si la contraseña es correcta"""
        return check_password_hash(self.clave_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'


class Empresa(db.Model):
    __tablename__ = 'empresas'
    
    id_empresa = db.Column(db.Integer, primary_key=True)
    nombre_fiscal = db.Column(db.String(255), nullable=False)
    nombre_comercial = db.Column(db.String(255))
    nif_cif = db.Column(db.String(20), unique=True)
    direccion = db.Column(db.Text)
    persona_contacto = db.Column(db.String(255))
    correo_electronico = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    plataformas = db.Column(db.Text)  # Guardado como texto separado por comas
    tarifa_hora = db.Column(db.Numeric(10, 2))
    forma_pago = db.Column(db.String(100))
    plazo_pago = db.Column(db.Integer)  # En días
    notas = db.Column(db.Text)
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    asignaciones = db.relationship('AsignacionCurso', backref='empresa', lazy=True)
    ingresos = db.relationship('Ingreso', backref='empresa', lazy=True)
    
    def __repr__(self):
        return f'<Empresa {self.nombre_comercial or self.nombre_fiscal}>'


class Curso(db.Model):
    __tablename__ = 'cursos'
    
    id_curso = db.Column(db.Integer, primary_key=True)
    codigo_curso = db.Column(db.String(50), unique=True, nullable=False)
    nombre_curso = db.Column(db.String(255), nullable=False)
    horas_curso = db.Column(db.Integer, nullable=False)
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    asignaciones = db.relationship('AsignacionCurso', backref='curso', lazy=True)
    
    def __repr__(self):
        return f'<Curso {self.codigo_curso}: {self.nombre_curso}>'


class AsignacionCurso(db.Model):
    __tablename__ = 'asignaciones_curso'
    
    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id_empresa'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id_curso'), nullable=False)
    
    # Datos de la plataforma
    url_plataforma = db.Column(db.String(500))
    usuario_plataforma = db.Column(db.String(100))
    clave_plataforma = db.Column(db.String(255))
    
    # Horarios
    hora_entrada = db.Column(db.Time)
    hora_salida = db.Column(db.Time)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    
    # Identificación de la acción formativa
    codigo_accion = db.Column(db.String(100))
    codigo_grupo = db.Column(db.String(100))
    plan_formativo = db.Column(db.String(255))
    estado_asignacion = db.Column(db.String(50), default='activa')
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    estudiantes = db.relationship('Estudiante', backref='asignacion', lazy=True, cascade='all, delete-orphan')
    calificaciones = db.relationship('Calificacion', backref='asignacion', lazy=True, cascade='all, delete-orphan')
    asistencias = db.relationship('Asistencia', backref='asignacion', lazy=True, cascade='all, delete-orphan')
    ingresos = db.relationship('Ingreso', backref='asignacion', lazy=True)
    importaciones = db.relationship('Importacion', backref='asignacion', lazy=True)
    
    def calcular_horas_totales(self):
        """Calcula las horas totales entre fecha inicio y fin según el horario"""
        if not self.fecha_inicio or not self.fecha_fin or not self.hora_entrada or not self.hora_salida:
            return 0
        # TODO: Implementar cálculo real considerando días lectivos
        # Por ahora retorno las horas del curso
        return self.curso.horas_curso if self.curso else 0
    
    def __repr__(self):
        return f'<Asignacion {self.codigo_grupo}: {self.curso.codigo_curso if self.curso else "N/A"}>'


class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    
    id_estudiante = db.Column(db.Integer, primary_key=True)
    id_asignacion = db.Column(db.Integer, db.ForeignKey('asignaciones_curso.id_asignacion'), nullable=False)
    nombre_alumno = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255))
    matricula = db.Column(db.String(100))
    estado_alumno = db.Column(db.String(50), default='activo')  # activo, baja, finalizado
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    calificaciones = db.relationship('Calificacion', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    asistencias = db.relationship('Asistencia', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Estudiante {self.nombre_alumno}>'


class Calificacion(db.Model):
    __tablename__ = 'calificaciones'
    
    id_calificacion = db.Column(db.Integer, primary_key=True)
    id_asignacion = db.Column(db.Integer, db.ForeignKey('asignaciones_curso.id_asignacion'), nullable=False)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiantes.id_estudiante'), nullable=False)
    nombre_prueba = db.Column(db.String(255), nullable=False)
    elemento_nota = db.Column(db.String(255))
    nota_final = db.Column(db.Numeric(5, 2))
    fecha_prueba = db.Column(db.Date)
    tipo_prueba = db.Column(db.String(100))  # examen, tarea, participación, etc.
    peso_nota = db.Column(db.Numeric(5, 2))  # Porcentaje de peso en la nota final
    fecha_importacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Calificacion {self.nombre_prueba}: {self.nota_final}>'


class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    
    id_asistencia = db.Column(db.Integer, primary_key=True)
    id_asignacion = db.Column(db.Integer, db.ForeignKey('asignaciones_curso.id_asignacion'), nullable=False)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiantes.id_estudiante'), nullable=False)
    fecha_clase = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, default=True)
    horas_asistidas = db.Column(db.Numeric(5, 2))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Asistencia {self.fecha_clase}: {"Presente" if self.presente else "Ausente"}>'


class ModeloPago(db.Model):
    __tablename__ = 'modelos_pago'
    
    id_modelo_pago = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    nombre_modelo = db.Column(db.String(255), nullable=False)
    tipo_modelo = db.Column(db.String(100))  # por_hora, fijo_mensual, por_alumno, etc.
    parametros = db.Column(db.Text)  # JSON con configuración específica
    vigente_desde = db.Column(db.Date)
    vigente_hasta = db.Column(db.Date)
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ingresos = db.relationship('Ingreso', backref='modelo_pago', lazy=True)
    
    def __repr__(self):
        return f'<ModeloPago {self.nombre_modelo}>'


class Ingreso(db.Model):
    __tablename__ = 'ingresos'
    
    id_ingreso = db.Column(db.Integer, primary_key=True)
    id_asignacion = db.Column(db.Integer, db.ForeignKey('asignaciones_curso.id_asignacion'), nullable=False)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresas.id_empresa'), nullable=False)
    id_modelo_pago = db.Column(db.Integer, db.ForeignKey('modelos_pago.id_modelo_pago'))
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    desglose = db.Column(db.Text)  # Explicación del cálculo
    fecha_calculo = db.Column(db.Date, default=datetime.utcnow)
    estado_ingreso = db.Column(db.String(50), default='previsto')  # previsto, facturado, cobrado
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ingreso {self.cantidad}€ - {self.estado_ingreso}>'


class Importacion(db.Model):
    __tablename__ = 'importaciones'
    
    id_importacion = db.Column(db.Integer, primary_key=True)
    id_asignacion = db.Column(db.Integer, db.ForeignKey('asignaciones_curso.id_asignacion'), nullable=False)
    archivo_origen = db.Column(db.String(500))
    fecha_importacion = db.Column(db.DateTime, default=datetime.utcnow)
    num_registros = db.Column(db.Integer)
    cambios = db.Column(db.Text)  # Log de lo que se importó
    
    def __repr__(self):
        return f'<Importacion {self.archivo_origen}: {self.num_registros} registros>'
