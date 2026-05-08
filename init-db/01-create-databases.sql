-- Script de inicialización de MySQL
-- Crea las bases de datos necesarias para todos los microservicios que usan MySQL

-- Base de datos para el microservicio de books (ya se crea vía MYSQL_DATABASE)
-- CREATE DATABASE IF NOT EXISTS biblioteca_digital;

-- Base de datos para el api-gateway (Laravel)
CREATE DATABASE IF NOT EXISTS biblioteca_gateway;

-- Otorgar privilegios completos al usuario root sobre ambas bases de datos
GRANT ALL PRIVILEGES ON biblioteca_digital.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON biblioteca_gateway.* TO 'root'@'%';
FLUSH PRIVILEGES;
