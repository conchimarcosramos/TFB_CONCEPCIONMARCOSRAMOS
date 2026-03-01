-- GESTTATION - Script de inicialización de base de datos
-- Proyecto Final de Bàtxelor - Universitat Carlemany
-- Estudiante: Marcos Ramos, María de la Concepción

-- Tabla USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
    correo_electronico VARCHAR(255) NOT NULL UNIQUE,
    clave_hash VARCHAR(255) NOT NULL,
    rol_usuario VARCHAR(50) DEFAULT 'docente',
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla EMPRESAS
CREATE TABLE IF NOT EXISTS empresas (
    id_empresa SERIAL PRIMARY KEY,
    nombre_fiscal VARCHAR(255) NOT NULL,
    nombre_comercial VARCHAR(255),
    nif_cif VARCHAR(20) UNIQUE,
    direccion TEXT,
    persona_contacto VARCHAR(255),
    correo_electronico VARCHAR(255),
    telefono VARCHAR(20),
    plataformas TEXT,
    tarifa_hora NUMERIC(10, 2),
    forma_pago VARCHAR(100),
    plazo_pago INTEGER,
    notas TEXT,
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla DOCENTES
CREATE TABLE IF NOT EXISTS docentes (
    id_docente SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefono VARCHAR(20),
    especialidad VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    es_admin BOOLEAN DEFAULT FALSE,
    id_usuario INTEGER UNIQUE REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla CURSOS
CREATE TABLE IF NOT EXISTS cursos (
    id_curso SERIAL PRIMARY KEY,
    codigo_curso VARCHAR(50) NOT NULL UNIQUE,
    nombre_curso VARCHAR(255) NOT NULL,
    horas_curso INTEGER NOT NULL,
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla ASIGNACIONES_CURSO
CREATE TABLE IF NOT EXISTS asignaciones_curso (
    id_asignacion SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_empresa INTEGER NOT NULL REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    id_curso INTEGER NOT NULL REFERENCES cursos(id_curso) ON DELETE CASCADE,
    url_plataforma VARCHAR(500),
    usuario_plataforma VARCHAR(100),
    clave_plataforma VARCHAR(255),
    hora_entrada TIME,
    hora_salida TIME,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    codigo_accion VARCHAR(100),
    codigo_grupo VARCHAR(100),
    plan_formativo VARCHAR(255),
    estado_asignacion VARCHAR(50) DEFAULT 'activa',
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla ESTUDIANTES
CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    id_asignacion INTEGER NOT NULL REFERENCES asignaciones_curso(id_asignacion) ON DELETE CASCADE,
    nombre_alumno VARCHAR(255) NOT NULL,
    correo_electronico VARCHAR(255),
    matricula VARCHAR(100),
    estado_alumno VARCHAR(50) DEFAULT 'activo',
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla CALIFICACIONES
CREATE TABLE IF NOT EXISTS calificaciones (
    id_calificacion SERIAL PRIMARY KEY,
    id_asignacion INTEGER NOT NULL REFERENCES asignaciones_curso(id_asignacion) ON DELETE CASCADE,
    id_estudiante INTEGER NOT NULL REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    nombre_prueba VARCHAR(255) NOT NULL,
    elemento_nota VARCHAR(255),
    nota_final NUMERIC(5, 2),
    fecha_prueba DATE,
    tipo_prueba VARCHAR(100),
    peso_nota NUMERIC(5, 2),
    fecha_importacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla ASISTENCIA
CREATE TABLE IF NOT EXISTS asistencia (
    id_asistencia SERIAL PRIMARY KEY,
    id_asignacion INTEGER NOT NULL REFERENCES asignaciones_curso(id_asignacion) ON DELETE CASCADE,
    id_estudiante INTEGER NOT NULL REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE,
    fecha_clase DATE NOT NULL,
    presente BOOLEAN DEFAULT TRUE,
    horas_asistidas NUMERIC(5, 2),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla MODELOS_PAGO
CREATE TABLE IF NOT EXISTS modelos_pago (
    id_modelo_pago SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    nombre_modelo VARCHAR(255) NOT NULL,
    tipo_modelo VARCHAR(100),
    parametros TEXT,
    vigente_desde DATE,
    vigente_hasta DATE,
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla INGRESOS
CREATE TABLE IF NOT EXISTS ingresos (
    id_ingreso SERIAL PRIMARY KEY,
    id_asignacion INTEGER NOT NULL REFERENCES asignaciones_curso(id_asignacion) ON DELETE CASCADE,
    id_empresa INTEGER NOT NULL REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    id_modelo_pago INTEGER REFERENCES modelos_pago(id_modelo_pago),
    cantidad NUMERIC(10, 2) NOT NULL,
    desglose TEXT,
    fecha_calculo DATE DEFAULT CURRENT_DATE,
    estado_ingreso VARCHAR(50) DEFAULT 'previsto',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla IMPORTACIONES
CREATE TABLE IF NOT EXISTS importaciones (
    id_importacion SERIAL PRIMARY KEY,
    id_asignacion INTEGER NOT NULL REFERENCES asignaciones_curso(id_asignacion) ON DELETE CASCADE,
    archivo_origen VARCHAR(500),
    fecha_importacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    num_registros INTEGER,
    cambios TEXT
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_asignaciones_usuario ON asignaciones_curso(id_usuario);
CREATE INDEX idx_asignaciones_empresa ON asignaciones_curso(id_empresa);
CREATE INDEX idx_asignaciones_curso ON asignaciones_curso(id_curso);
CREATE INDEX idx_estudiantes_asignacion ON estudiantes(id_asignacion);
CREATE INDEX idx_calificaciones_asignacion ON calificaciones(id_asignacion);
CREATE INDEX idx_calificaciones_estudiante ON calificaciones(id_estudiante);
CREATE INDEX idx_asistencia_asignacion ON asistencia(id_asignacion);
CREATE INDEX idx_asistencia_estudiante ON asistencia(id_estudiante);
CREATE INDEX idx_ingresos_asignacion ON ingresos(id_asignacion);

-- Usuario de prueba (password: gesttation2026)
-- Hash generado con werkzeug (scrypt)
-- Lo dejé en texto plano en el comentario para no olvidarme durante el desarrollo
-- IMPORTANTE: En producción esto se crearía de forma segura
INSERT INTO usuarios (nombre_usuario, correo_electronico, clave_hash, rol_usuario)
VALUES ('admin', 'admin@gesttation.local', 
        'scrypt:32768:8:1$0tzg3gjeb2aGPGxV$a9a234fb85b51d2ed50b1498613b72f610ef5fed521312026eca7d571c6d76621d640dc90a735a8f4ee971facb1ec683b092216b623fc04a514c5ca0d7be9faf', 
        'docente')
ON CONFLICT (nombre_usuario) DO NOTHING;

-- Datos de ejemplo, NIF inventados pero con el formato correcto
INSERT INTO empresas (nombre_fiscal, nombre_comercial, nif_cif, tarifa_hora, forma_pago, plazo_pago)
VALUES 
    ('Centro Formativo Andorra SL', 'CFA', 'A12345678', 25.00, 'Transferencia', 30),
    ('Academia Online Virtual', 'AOV', 'B87654321', 22.50, 'Transferencia', 15)
ON CONFLICT (nif_cif) DO NOTHING;

-- Cursos reales que he impartido en algunas ocasiones del catálogo de SEPE
INSERT INTO cursos (codigo_curso, nombre_curso, horas_curso)
VALUES 
    ('IFCD084PO', 'Hacking Ético y Ciberseguridad', 60),
    ('IFCD052PO', 'Programación en Java', 210),
    ('COMT115PO', 'E-Business: Desarrollo de Negocio Online', 60),
    ('IFCT049PO', 'Experto en Virtualización con VMware y Microsoft', 170),
    ('IFCD009PO', 'Gestión de Contenidos Digitales', 60)
ON CONFLICT (codigo_curso) DO NOTHING;

INSERT INTO asignaciones_curso (
    id_usuario, id_empresa, id_curso, 
    fecha_inicio, fecha_fin, 
    hora_entrada, hora_salida,
    codigo_accion, codigo_grupo, 
    plan_formativo, estado_asignacion,
    url_plataforma
)
SELECT 
    u.id_usuario, 
    e.id_empresa, 
    c.id_curso,
    '2026-01-15'::DATE,
    '2026-03-30'::DATE,
    '16:00:00'::TIME,
    '21:00:00'::TIME,
    'ACC-2026-001',
    'GRUPO-A',
    'Plan Formativo 2026',
    'activa',
    'https://moodle.ejemplo.com'
FROM usuarios u, empresas e, cursos c
WHERE u.nombre_usuario = 'admin' 
  AND e.nif_cif = 'A12345678'
  AND c.codigo_curso = 'IFCD084PO'
LIMIT 1
ON CONFLICT DO NOTHING;

-- Estudiantes de ejemplo para la asignación
INSERT INTO estudiantes (id_asignacion, nombre_alumno, correo_electronico, matricula, estado_alumno)
SELECT 
    a.id_asignacion,
    'Estudiante ' || generate_series,
    'estudiante' || generate_series || '@ejemplo.com',
    'MAT' || LPAD(generate_series::TEXT, 4, '0'),
    'activo'
FROM asignaciones_curso a
CROSS JOIN generate_series(1, 15)
WHERE a.codigo_accion = 'ACC-2026-001'
LIMIT 15;