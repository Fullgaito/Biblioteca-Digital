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

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD sh -c "php artisan key:generate --force && \
php artisan migrate --force && \
php artisan config:clear && \
php artisan cache:clear && \
php artisan serve --host=0.0.0.0 --port=8000"