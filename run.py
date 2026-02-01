"""
GESTTATION - Gestor Integral de Cursos para Docentes
TFB - Universitat Carlemany 2025-2026
Autor: Marcos Ramos, María de la Concepción

Este es el archivo principal que arranca la aplicación Flask.
Lo he separado del __init__.py para poder controlar mejor el entorno
y facilitar el despliegue en Docker.
"""

from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # En desarrollo uso el puerto 3001 porque el 5000 a veces me da problemas
    # En producción esto se configuraría diferente
    port = int(os.environ.get('PORT', 3001))
    
    # Debug en True solo para desarrollo - IMPORTANTE cambiarlo en producción
    app.run(
        host='0.0.0.0',  # Necesario para que Docker lo exponga correctamente
        port=port,
        debug=True
    )