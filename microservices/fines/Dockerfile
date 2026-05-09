FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para psycopg2 y curl (wait-for-it)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto Django completo (contiene manage.py, fines/, fines_service/)
COPY fines_service/ .

# Agregar wait-for-it para esperar a que PostgreSQL esté listo
RUN curl -o /usr/local/bin/wait-for-it.sh \
    https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh

EXPOSE 8001

# Esperar a PostgreSQL, aplicar migraciones y arrancar el servidor
CMD ["sh", "-c", \
  "/usr/local/bin/wait-for-it.sh postgres_db:5432 -t 60 -- \
  python manage.py migrate --noinput && \
  python manage.py runserver 0.0.0.0:8001"]