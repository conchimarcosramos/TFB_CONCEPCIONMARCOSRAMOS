
# gesttation ESTRUCTURA DEL PROYECTO

gesttation/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── empresas.py
│   │   ├── cursos.py
│   │   ├── asignaciones.py
│   │   ├── estudiantes.py
│   │   ├── calificaciones.py
│   │   ├── asistencia.py
│   │   └── ingresos.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── empresas/
│   │   │   ├── listar.html
│   │   │   └── formulario.html
│   │   ├── cursos/
│   │   │   ├── listar.html
│   │   │   └── formulario.html
│   │   └── asignaciones/
│   │       ├── listar.html
│   │       └── formulario.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── postgres/
│   └── init.sql
└── run.py