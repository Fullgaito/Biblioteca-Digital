FROM python:3.11-slim

# Establecemos el directorio de trabajo
WORKDIR /app

#Instalacion de dependencias del sistema para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copiamos requirements e instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos todo el proyecto al contenedor
COPY . .

# Agregamos wait-for-it para esperar a que la base de datos esté lista antes de iniciar la aplicación
RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh

#Exponemos el puerto en el que la aplicación se ejecutará
EXPOSE 5000

# comando de arranque de la aplicación, utilizando wait-for-it para esperar a que la base de datos esté lista, aplica migraciones y levanta Gunicorn
CMD ["sh", "-c", "./wait-for-it.sh mysql_db:3306 -- flask db upgrade && gunicorn --bind 0.0.0.0:5000 app:app"]