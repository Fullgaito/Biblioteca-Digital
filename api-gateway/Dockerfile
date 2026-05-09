FROM php:8.2-cli

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    curl \
    libzip-dev \
    libxml2-dev \
    zip \
    && docker-php-ext-install pdo pdo_mysql zip xml \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Instalar wait-for-it.sh (antes de copiar el código para mejor caché)
RUN curl -o /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh

# Necesario para correr composer como root
ENV COMPOSER_ALLOW_SUPERUSER=1

# Directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Asegurar que el archivo .env exista (si no existe, lo crea del example)
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Instalar dependencias Laravel
RUN composer install --no-dev --optimize-autoloader --no-interaction --no-scripts

# SOLUCIÓN AL ERROR: Crear estructura de storage y bootstrap antes del chmod
RUN mkdir -p storage/framework/cache/data \
    storage/framework/sessions \
    storage/framework/views \
    storage/logs \
    bootstrap/cache && \
    chmod -R 777 storage bootstrap/cache

# Exponer puerto
EXPOSE 8000

# Comando de inicio corregido
CMD ["sh", "-c", "wait-for-it.sh mysql_db:3306 -t 60 -- \
    php artisan key:generate --force && \
    php artisan config:cache && \
    php artisan migrate --force && \
    php artisan serve --host=0.0.0.0 --port=8000"]