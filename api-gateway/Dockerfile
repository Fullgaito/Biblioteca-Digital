FROM php:8.2-cli

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    curl \
    libpq-dev \
    libzip-dev \
    zip \
    && docker-php-ext-install pdo pdo_mysql zip

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias Laravel
RUN composer install

# Permisos Laravel
RUN chmod -R 777 storage bootstrap/cache

# Agregar wait-for-it para esperar a MySQL
RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x wait-for-it.sh

# Exponer puerto
EXPOSE 8000

# Comando de inicio - espera a MySQL antes de migrar
CMD sh -c "./wait-for-it.sh mysql_db:3306 -t 60 -- \
php artisan key:generate --force && \
php artisan migrate --force && \
php artisan config:clear && \
php artisan cache:clear && \
php artisan serve --host=0.0.0.0 --port=8000"