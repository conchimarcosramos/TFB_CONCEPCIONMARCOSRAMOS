# Dockerfile para GESTTATION
# Uso Python 3.11-slim para mantener la imagen ligera
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y compilación
# gcc: necesario para compilar algunas dependencias de Python
# postgresql-client: útil para debugging de la BD
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python, requirements.txt 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar toda la aplicación
COPY . .

#Puerto que usa Flask en run.py
EXPOSE 3001

#Comando de inicio
CMD ["python", "run.py"]