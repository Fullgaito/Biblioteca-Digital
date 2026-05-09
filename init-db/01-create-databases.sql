-- Script de inicialización de MySQL
-- Crea las bases de datos adicionales necesarias
-- Nota: books_db ya se crea automáticamente vía MYSQL_DATABASE en docker-compose

-- Base de datos para el api-gateway (Laravel)
CREATE DATABASE IF NOT EXISTS biblioteca_gateway;

-- Otorgar privilegios completos al usuario root sobre todas las bases de datos
GRANT ALL PRIVILEGES ON books_db.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON biblioteca_gateway.* TO 'root'@'%';
FLUSH PRIVILEGES;
