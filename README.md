# 📖 Sistema de Biblioteca - Arquitectura de Microservicios

## Descripción General

Sistema de gestión de biblioteca basado en arquitectura de microservicios que permite administrar el catálogo de libros, préstamos, multas, compras e y reportes de libros adquiridos. Desarrollado como proyecto individual para la asignatura de Ingeniería de Software II.

## Arquitectura del Sistema

El sistema está compuesto por un API Gateway y 5 microservicios independientes que se comunican entre sí mediante APIs REST.

### Componentes

- **API Gateway** (Laravel + MySQL): Punto de entrada único, gestión de autenticación y enrutamiento
- **Microservicio de Libros** (Flask + MySQL): Catálogo y disponibilidad de libros
- **Microservicio de Préstamos** (Express + MongoDB): Gestión de préstamos y devoluciones
- **Microservicio de Multas** (Django + PostgreSQL): Cálculo y gestión de multas por atrasos
- **Microservicio de Compras** (Express + Firebase): Registro de adquisiciones al proveedor
- **Microservicio de Reportes** (Flask + MongoDB): Genera múltiples reportes del funcionamiento del sistema

### Diagrama de Arquitectura

![Arquitectura del Sistema](docs/Diagrama-sistema.png)

---
 
## 📁 Estructura del repositorio
 
```
Biblioteca-Digital/
├── api-gateway/                  # Laravel — Auth + Gateway
│   ├── app/Http/Controllers/
│   │   ├── GatewayController.php # Proxy hacia microservicios
│   │   └── UserController.php    # Registro, login, logout
│   └── routes/api.php            # Definición de rutas
│
└── microservices/
    ├── books/                    # Flask + MySQL
    ├── loans/                    # Node.js + MongoDB
    ├── fines/fines_service/      # Django + PostgreSQL
    ├── sales/                    # Node.js + Firebase
    └── reports/                  # Flask (agrega REST)
```
 
---

## Stack Tecnológico

### Frameworks
- Laravel 10.x
- Django 5.0
- Flask 3.0
- Express 4.x

### Bases de Datos
- MySQL 8.0
- PostgreSQL 15
- MongoDB 7.0
- Firebase Realtime Database

### Herramientas
- Git & GitHub
- Thunder Client (pruebas de API)

> También necesitas una cuenta de **Firebase** con una Realtime Database creada y un `serviceAccountKey.json` descargado para el servicio Sales.

## 🔐 Clave interna compartida (`INTERNAL_API_KEY`)
 
Todos los microservicios validan el header `X-Internal-API-Key` para aceptar únicamente peticiones provenientes del API Gateway. Esta clave debe ser **la misma en todos los servicios**.
 
Puedes usar cualquier string seguro. Ejemplo:
 
```
INTERNAL_API_KEY=mi_clave_super_secreta_2024
```
 
> ⚠️ Define esta clave antes de arrancar cualquier servicio. Si no coincide entre servicios, todas las peticiones internas retornarán `401 Unauthorized`.
 
---

## 🚀 Guía de despliegue inicial
 
Sigue el orden indicado: las bases de datos deben estar listas antes de arrancar los servicios, y los microservicios deben estar corriendo antes de iniciar el API Gateway.
 
---
 
### Paso 1 — Clonar el repositorio
 
```bash
git clone https://github.com/Fullgaito/Biblioteca-Digital.git
cd Biblioteca-Digital
```
 
---
 
### Paso 2 — Crear las bases de datos en Laragon
 
#### MySQL (para Books y API Gateway)
 
```sql
CREATE DATABASE books_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE laravel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
 
#### PostgreSQL (para Fines)
 
```bash
psql -U postgres
CREATE DATABASE fines_db;
\q
```
 
#### MongoDB (para Loans)
 
MongoDB crea la base de datos automáticamente al primer uso. Solo asegúrate de que el servidor esté corriendo:
 
```bash
# Linux/macOS
sudo systemctl start mongod
 
# Windows
net start MongoDB
```
 
#### Firebase (para Sales)
 
1. Ve a [Firebase Console](https://console.firebase.google.com/) y crea o selecciona un proyecto.
2. Activa **Realtime Database** en modo prueba.
3. Ve a **Configuración del proyecto → Cuentas de servicio → Generar nueva clave privada**.
4. Descarga el archivo JSON y guárdalo en `microservices/sales/serviceAccountKey.json`.
 
---
 
### Paso 3 — Servicio Books (Flask · Puerto 5000)
 
```bash
cd microservices/books
 
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
 
# Instalar dependencias
pip install -r requirements.txt
```
 
Crear el archivo `.env`:
 
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=books_db
INTERNAL_API_KEY=mi_clave_super_secreta_2024
```
 
Ejecutar migraciones e iniciar:
 
```bash
flask db upgrade
python app.py
```
 
> El servicio quedará disponible en `http://localhost:5000`
 
---
 
### Paso 4 — Servicio Loans (Node.js · Puerto 3002)
 
```bash
cd microservices/loans
npm install
```
 
Crear el archivo `.env`:
 
```env
PORT=3002
MONGO_URI=mongodb://localhost:27017/loans_db
FLASK_URL=http://localhost:5000
FINES_URL=http://localhost:8001
INTERNAL_API_KEY=mi_clave_super_secreta_2024
```
 
Iniciar el servicio:
 
```bash
node server.js
```
 
> El servicio quedará disponible en `http://localhost:3002`
 
---
 
### Paso 5 — Servicio Fines (Django · Puerto 8001)
 
```bash
cd microservices/fines/fines_service
 
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
 
# Instalar dependencias
pip install -r ../requirements.txt
```
 
Crear el archivo `.env` dentro de `fines_service/`:
 
```env
DB_NAME=fines_db
DB_USER=postgres
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432
INTERNAL_API_KEY=mi_clave_super_secreta_2024
```
 
Ejecutar migraciones e iniciar:
 
```bash
python manage.py migrate
python manage.py runserver 8001
```
 
> El servicio quedará disponible en `http://localhost:8001`
 
---
 
### Paso 6 — Servicio Sales (Node.js · Puerto 3001)
 
```bash
cd microservices/sales
npm install
```
 
Crear el archivo `.env`:
 
```env
PORT=3001
FLASK_URL=http://localhost:5000
FIREBASE_DB_URL=https://<tu-proyecto>-default-rtdb.firebaseio.com/
INTERNAL_API_KEY=mi_clave_super_secreta_2024
```
 
> Asegúrate de que `serviceAccountKey.json` ya está en esta carpeta (ver Paso 2 - Firebase).
 
Iniciar el servicio:
 
```bash
node server.js
```
 
> El servicio quedará disponible en `http://localhost:3001`
 
---
 
### Paso 7 — Servicio Reports (Flask · Puerto 5001)
 
```bash
cd microservices/reports
 
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
 
pip install -r requirements.txt
```
 
Crear el archivo `.env`:
 
```env
BOOKS_SERVICE_URL=http://localhost:5000
LOANS_SERVICE_URL=http://localhost:3002
FINES_SERVICE_URL=http://localhost:8001
SALES_SERVICE_URL=http://localhost:3001
INTERNAL_API_KEY=mi_clave_super_secreta_2024
```
 
Iniciar el servicio:
 
```bash
python app.py
```
 
> El servicio quedará disponible en `http://localhost:5001`
 
---
 
### Paso 8 — API Gateway (Laravel · Puerto 8000)
 
```bash
cd api-gateway
composer install
npm install && npm run build       # Compilar assets Vite
```
 
Copiar y editar el archivo de entorno:
 
```bash
cp .env.example .env
php artisan key:generate
```
 
Editar `.env` con los siguientes valores clave:
 
```env
APP_NAME="Biblioteca Digital"
APP_ENV=local
APP_DEBUG=true
APP_URL=http://localhost:8000
 
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=tu_password
 
# Clave interna compartida con todos los microservicios
INTERNAL_API_KEY=mi_clave_super_secreta_2024
```
 
Configurar las URLs de los microservicios en `config/services.php`:
 
```php
'microservices' => [
    'books'   => env('BOOKS_URL',   'http://localhost:5000'),
    'loans'   => env('LOANS_URL',   'http://localhost:3002'),
    'fines'   => env('FINES_URL',   'http://localhost:8001'),
    'sales'   => env('SALES_URL',   'http://localhost:3001'),
    'reports' => env('REPORTS_URL', 'http://localhost:5001'),
],
```
 
O agregar directamente las variables al `.env`:
 
```env
BOOKS_URL=http://localhost:5000
LOANS_URL=http://localhost:3002
FINES_URL=http://localhost:8001
SALES_URL=http://localhost:3001
REPORTS_URL=http://localhost:5001
```
 
Ejecutar migraciones y arrancar:
 
```bash
php artisan migrate
php artisan serve --port=8000
```
 
> El API Gateway quedará disponible en `http://localhost:8000`
 
---

## ✔️ Verificación del despliegue
 
Una vez todos los servicios estén corriendo, verifica con las siguientes peticiones:
 
#### 1. Registrar un usuario
 
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"12345678","password_confirmation":"12345678","cuestion":"color favorito","answer":"azul"}'
```
 
#### 2. Obtener token
 
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"12345678"}'
```
 
#### 3. Verificar catálogo de libros (requiere token)
 
```bash
curl http://localhost:8000/api/books \
  -H "Authorization: Bearer <TOKEN>"
```
 
#### 4. Verificar dashboard de reportes
 
```bash
curl http://localhost:8000/api/reports/dashboard \
  -H "Authorization: Bearer <TOKEN>"
```
 
---
 
## 🗺️ Resumen de puertos
 
| Servicio | Puerto | URL local |
|---|---|---|
| API Gateway | `8000` | `http://localhost:8000` |
| Books | `5000` | `http://localhost:5000` |
| Loans | `3002` | `http://localhost:3002` |
| Fines | `8001` | `http://localhost:8001` |
| Sales | `3001` | `http://localhost:3001` |
| Reports | `5001` | `http://localhost:5001` |
 
---

## 🕵️‍♂️ Pruebas de rendimiento

Se realizó distintas pruebas sobre el sistema en general usando la libreria de Locust proporcionada por Python, realizando pruebas de carga,estrés y de capacidad.

> **Nota**: Documentación completa de las pruebas en [Tests/README.md/](Tests/README.md)

### Pasos para desplegar las pruebas

```bash
cd ../api-gateway
php artisan serve
```

### 2. Ejecuta Locust con GUI
```bash
locust -f locust_laravel.py 
```

### 3. Abre el navegador
Ve a `http://127.0.0.1:8089` y configura:
- **Number of users**: Cantidad de usuarios simultáneos
- **Spawn rate**: Usuarios creados por segundo
- Luego presiona "Start swarming"
 
## 🔑 Autenticación
 
El sistema usa dos capas de autenticación:
 
**Capa externa (clientes → API Gateway):** Laravel Sanctum con tokens Bearer. Los clientes deben incluir el header `Authorization: Bearer <TOKEN>` en todas las peticiones a rutas protegidas.
 
**Capa interna (API Gateway → microservicios):** Cada microservicio valida el header `X-Internal-API-Key`. Solo el Gateway conoce y envía esta clave. Las peticiones que lleguen directamente a los microservicios sin esta clave serán rechazadas con `401 Unauthorized`.

---
 
## 📖 Documentación por servicio
 
Cada microservicio tiene su propio README con detalles de endpoints, modelos de datos y configuración:
 
- [`api-gateway/README.md`](api-gateway/README.md) — Auth, usuarios y rutas del gateway
- [`microservices/books/README.MD`](microservices/books/README.MD) — CRUD de libros
- [`microservices/loans/README.md`](microservices/loans/README.md) — Gestión de préstamos
- [`microservices/fines/README.md`](microservices/fines/README.md) — Gestión de multas
- [`microservices/sales/README.md`](microservices/sales/README.md) — Ventas de libros
- [`microservices/reports/README.md`](microservices/reports/README.md) — Reportes y dashboard
 
---

> **Nota**: Documentación completa de endpoints en [api-gateway/README.md/](api-gateway/README.md)

## ☸️🐋 Documentación detallada para levantar los contenedores

El sistema está completamente contenedorizado usando **Docker** y **Docker Compose**. Esto permite levantar toda la infraestructura (bases de datos y microservicios) con un solo comando, asegurando que todas las dependencias y configuraciones de red estén correctamente establecidas.

### Requisitos Previos

- **Docker** (v20.10 o superior)
- **Docker Compose** (v2.0 o superior)

### Paso 1 — Configuración del entorno

Antes de levantar los contenedores, asegúrate de que **cada microservicio, incluido el api-gateway**, tenga su respectivo archivo `.env` debidamente configurado en su propia carpeta. Además, debes contar con un archivo `.env` en la raíz del proyecto para las variables globales de Docker Compose.

Ejemplo de contenido para el archivo `.env` en la raíz:

```env
# MySQL (Books & API Gateway)
DB_USER=root
DB_PASSWORD=root
DB_NAME=books_db

# PostgreSQL (Fines)
DB_USER_POSTGRES=postgres
DB_PASSWORD_POSTGRES=postgres
DB_NAME_POSTGRES=fines_db

# MongoDB (Loans & Reports)
MONGO_USER=admin
MONGO_PASSWORD=admin
MONGO_DB=loans_db

# Firebase (Sales)
FIREBASE=https://microservicio-ventas-default-rtdb.firebaseio.com/
```

#### Configuración de `.env` por microservicio

A continuación, se detallan los valores recomendados para los archivos `.env` internos de cada carpeta cuando se utiliza Docker:

<details>
<summary>📂 api-gateway/.env</summary>

```env
APP_NAME="Biblioteca Digital"
APP_ENV=local
APP_URL=http://localhost:8000
INTERNAL_API_KEY=123

DB_CONNECTION=mysql
DB_HOST=mysql_db
DB_PORT=3306
DB_DATABASE=biblioteca_gateway
DB_USERNAME=root
DB_PASSWORD=root

BOOKS_SERVICE_URL=http://books-microservice:5000
LOANS_SERVICE_URL=http://loans-microservice:3002
FINES_SERVICE_URL=http://fines-microservice:8001
SALES_SERVICE_URL=http://sales-microservice:3001
REPORTS_SERVICE_URL=http://reports-microservice:5001
```
</details>

<details>
<summary>📂 microservices/books/.env</summary>

```env
FLASK_APP=app.py
FLASK_ENV=production
DB_HOST=mysql_db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=books_db
DATABASE_URL=mysql+pymysql://root:root@mysql_db:3306/books_db
INTERNAL_API_KEY=123
```
</details>

<details>
<summary>📂 microservices/loans/.env</summary>

```env
PORT=3002
MONGO_URI=mongodb://admin:admin@mongo_db:27017/loans_db?authSource=admin
FLASK_URL=http://books-microservice:5000
FINES_URL=http://fines-microservice:8001
INTERNAL_API_KEY=123
```
</details>

<details>
<summary>📂 microservices/fines/fines_service/.env</summary>

```env
DB_NAME=fines_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres_db
DB_PORT=5432
INTERNAL_API_KEY=123
```
</details>

<details>
<summary>📂 microservices/sales/.env</summary>

```env
PORT=3001
FIREBASE_DB_URL=https://microservicio-ventas-default-rtdb.firebaseio.com/
FLASK_URL=http://books-microservice:5000
INTERNAL_API_KEY=123
```
</details>

<details>
<summary>📂 microservices/reports/.env</summary>

```env
PORT=5001
MONGO_URI=mongodb://admin:admin@mongo_db:27017/reports_db?authSource=admin
BOOKS_SERVICE_URL=http://books-microservice:5000
LOANS_SERVICE_URL=http://loans-microservice:3002
FINES_SERVICE_URL=http://fines-microservice:8001
SALES_SERVICE_URL=http://sales-microservice:3001
INTERNAL_API_KEY=123
```
</details>

> **Nota**: El servicio `sales-service` aún requiere el archivo `serviceAccountKey.json` dentro de `microservices/sales/` para funcionar correctamente.

### Paso 2 — Levantar la infraestructura

Desde la raíz del proyecto, ejecuta el siguiente comando:

```bash
docker-compose up --build
```

Este comando realizará lo siguiente:
1.  Construirá las imágenes de cada microservicio usando sus respectivos `Dockerfile`.
2.  Descargará las imágenes oficiales de MySQL, PostgreSQL y MongoDB.
3.  Creará una red interna donde todos los servicios pueden comunicarse por su nombre de contenedor (ej: `http://books-microservice:5000`).
4.  Configurará los volúmenes para que los datos de las bases de datos persistan.

### Comandos útiles

- **Detener los servicios:** `docker-compose down`
- **Ver logs de un servicio:** `docker logs -f <nombre_del_contenedor>`
- **Reiniciar un servicio específico:** `docker-compose restart <nombre_del_servicio>`


## 📝 Instrucciones para probar todos los servicios una vez desplegados.

Para verificar que todos los microservicios están funcionando correctamente a través del API Gateway, puedes utilizar herramientas como **Postman**, **Thunder Client** o comandos `curl`. 

Todas las peticiones deben dirigirse al API Gateway en `http://localhost:8000`.

### 1. Registro e Inicio de Sesión
Antes de probar los microservicios, debes estar autenticado.

**POST** `/api/register`

**Registrar un usuario:**
```json
{
  "name": "Juan Perez",
  "email": "juan@test.com",
  "password": "12345634",
  "password_confirmation": "12345634",
  "cuestion": "color favorito",
  "answer": "verde"
}
```

**POST** `/api/login`

**Iniciar sesión para obtener el Token:**
```json
{
  "email": "juan@test.com",
  "password": "12345634"
}
```
*Copia el valor de `access_token` de la respuesta para las siguientes peticiones.Y ponlo en Authorization Bearer en thunderclient.*

### 2. Probar Microservicio de Libros (Books)

### 🔹 Creación de Libros

**POST** `/api/books`

Permite la creación de libros correspondiente al microservicio creado en Flask

#### 📥 Request

```json
{
  "title": "Cien años de soledad",
  "author": "Gabriel García Márquez",
  "isbn": "978-0307474728",
  "description": "La épica historia de la familia Buendía en el remoto pueblo de Macondo, donde lo fantástico y lo real convergen en una narrativa maestra.",
  "available": true,
  "category": "Realismo Mágico",
  "quantity": 20,
  "unit_price":60000
}
```

### 🔹 Obtener Libros

**GET** `/api/books`

Permite la obtención de libros que previamente ya fueron creados


#### 📤 Response

```json
[
  {
    "author": "Gabriel García Márquez",
    "available": true,
    "category": "novela",
    "description": "Novela icónica de la literatura latinoamericana",
    "id": 1,
    "isbn": "9780307474728",
    "quantity": 20,
    "title": "Cien años de soledad",
    "unit_price":60000
  }
]
```

### 🔹 Obtener un libro

**GET** `/api/books/{id}`

Permite la obtención de un libro junto a su información detallada


#### 📤 Response

```json
{
  "author": "Antoine de Saint-Exupéry",
  "available": true,
  "category": "infantil",
  "description": "Historia filosófica sobre la vida y la amistad",
  "id": 2,
  "isbn": "9780156012195",
  "quantity": 9,
  "title": "El principito",
  "unit_price": 42000
}
```

### 🔹 Actualización de un libro

**PUT** `/api/books/{id}`

Permite la actualización de la información correspondiente de un libro en especifico indicando el id correspondiente

#### 📥 Request

```json
{
  "quantity": 30
}
```

#### 📤 Response

```json
{
  "author": "Gabriel García Márquez",
  "available": true,
  "category": "novela",
  "description": "Novela icónica de la literatura latinoamericana",
  "id": 1,
  "isbn": "9780307474728",
  "quantity": 30,
  "title": "Cien años de soledad",
  "unit_price": 60000
}
```

### 🔹 Eliminación de un libro

**DELETE** `/api/books/{id}`

Permite la eliminación definitiva de un libro ya creado con su id correspondiente


#### 📤 Response

```json
{
  "message": "Book 3 deleted"
}
```

### 3. Probar Microservicio de Préstamos (Loans)

### 🔹 Creación de un prestamo

**POST** `/api/loans`

Permite la creación de prestamos necesitando el id del usuario que lo solicita y el id del libro correspondiente

#### 📥 Request

```json
{
  "user_id":2,
  "book_id":2
}
```

### 🔹 Obtener los prestamos

**GET** `/api/loans`

Permite obtener todos los prestamos que se han realizado


#### 📤 Response

```json
[
  {
    "_id": "69cd46cbcc9b4262db9cde2f",
    "book_id": 1,
    "user_id": 1,
    "status": "active",
    "loan_date": "2026-04-01T16:24:43.398Z",
    "__v": 0
  }
]
```

### 🔹 Obtener los prestamos por id que estan en la BD

**GET** `/api/loans/69cdc5fa291d7ccc67c54308`

Permite obtener la información asociada a un prestamo


#### 📤 Response

```json
{
  "_id": "69cdc5fa291d7ccc67c54308",
  "book_id": 2,
  "user_id": 2,
  "status": "active",
  "loan_date": "2026-04-02T01:27:22.024Z",
  "__v": 0
}
```

### 🔹 Actualización de un prestamo

**PUT** `/api/loans/{id}`

Permite actualizar la información de un prestamo en especifico indicando el id correspondiente

#### 📥 Request

```json
{
  "status": "returned"
}
```

#### 📤 Response

```json
{
  "message": "Loan updated successfully"
}
```

### 🔹 Eliminación de un prestamo

**DELETE** `/api/loans/{id}`

Permite la eliminación definitiva de un prestamo ya creado con su id correspondiente


#### 📤 Response

```json
{
  "message": "Loan deleted successfully"
}
```

### 🔹 Prestamos activos

**PUT** `/api/loans/activos`

Permite visualizar los prestamos que actualmente se encuentran activos


#### 📤 Response

```json
[
  {
    "_id": "69cdc5fa291d7ccc67c54308",
    "book_id": 2,
    "user_id": 2,
    "status": "active",
    "loan_date": "2026-04-02T01:27:22.024Z",
    "__v": 0
  }
]
```

### 4. Probar Microservicio de Multas (Fines)

#### 🔹 Obtener las multas

**GET** `/api/fines`

Permite obtener todas las multas que se han realizado


#### 📤 Response

```json
[
  {
    "_id": "69cd46cbcc9b4262db9cde2f",
    "book_id": 1,
    "user_id": 1,
    "status": "active",
    "loan_date": "2026-04-01T16:24:43.398Z",
    "__v": 0
  }
]
```

### 🔹 Obtener listado de multas

**GET** `/api/fines`

Permite la obtención de las multas existentes mostrando el acumulado a pagar y el estado del mismo


#### 📤 Response

```json
[
  {
    "id": 1,
    "user_id": 2,
    "loan_id": "69cdc5fa291d7ccc67c54308",
    "amount": 1740,
    "days_late": 3,
    "status": "pending",
    "paid_at": null
  }
]
```

### 🔹 Obtener detalle de una multa en particular

**GET** `/api/fines/{id}`

Permite la obtención de una multa en particular pasando su id correspondiente para ver la información respecto a una multa en particular


#### 📤 Response

```json
{
  "id": 1,
  "user_id": 2,
  "loan_id": "69cdc5fa291d7ccc67c54308",
  "days_late": 3,
  "amount": 1740,
  "status": "pending",
  "paid_at": null
}
```

### 🔹 Obtener una multa por usuario

**GET** `/api/fines/user/{user_id}`

Permite la obtención de una multa que tenga un usuario en particular


#### 📤 Response

```json
[
  {
    "id": 1,
    "user_id": 2,
    "loan_id": "69cdc5fa291d7ccc67c54308",
    "amount": 1740,
    "days_late": 3,
    "status": "pending",
    "paid_at": null
  }
]
```

### 🔹 Pago de Multas

**POST** `/api/fines`

Una vez se haga efectivo el pago se pasa a reportar en el sistema que ya el pago fue realizado para no generar intereses y saldar la deuda

#### 📥 Request

```json
{
  "loan_id": "69cdc5fa291d7ccc67c54308"
}
```

#### 📤 Response

```json
{
  "message": "Fine paid"
}
```

### 5. Probar Microservicio de Compras/Ventas (Sales)

### 🔹 Creación de una venta

**POST** `/api/sales`

Permite la creación de una venta vinculandose al servicio de libros

#### 📥 Request

```json
{
  "user_id":1,
  "book_id":1,
  "quantity":4
}
```

#### 📤 Response

```json
{
  "message": "Sale completed",
  "id": "-OpFRQdYXRUIORNwxMYM",
  "total_price": 240000
}
```

### 🔹 Obtener una venta de un usuario en específico

**GET** `/api/sales/user/{userId}`

Permite obtener el detalle de una venta por un usuario en específico

#### 📤 Response

```json
[
  {
    "book_id": 1,
    "created_at": "2026-04-02T23:05:24.283Z",
    "id": "-OpFRQdYXRUIORNwxMYM",
    "quantity": 4,
    "total_price": 240000,
    "user_id": 1
  }
]
```

### 6. Probar Microservicio de Reportes (Reports)

*GET** `/api/reports/most-sold-books`

Muestra los libros más vendidos, ordenados por cantidad de ventas, lo que puede ayudar a identificar las tendencias de compra y los títulos más populares entre los clientes.

#### 📤 Response

```json
[
  {
    "book_id": 1,
    "title": "Cien años de soledad",
    "total_sales": 1
  }
]
```

### 🔹 Obtener el total de ventas realizadas

**GET** `/api/reports/total-sales`

Muestra el total de ventas realizadas en la librería, lo que puede ayudar a evaluar el rendimiento general del negocio y la demanda de libros.

#### 📤 Response

```json
{
  "total_sales": 1
}
```

### 🔹 Obtener los libros más prestados

**GET** `api/reports/dashboard`

Muestra un resumen general de los informes de préstamos, multas y ventas, lo que puede proporcionar una visión rápida del rendimiento de la biblioteca en diferentes áreas y ayudar a identificar áreas de mejora o éxito.

#### 📤 Response

```json
{
  "loans": {
    "top books": [
      {
        "book_id": 1,
        "title": "Cien años de soledad",
        "total loans": 1
      },
      {
        "book_id": 2,
        "title": "El principito",
        "total loans": 1
      }
    ],
    "total": {
      "total_loans": 2
    }
  },
  "fines": {
    "top users": [
      {
        "user_id": 2,
        "total_fines": 1
      }
    ],
    "total": {
      "total_fines": 1
    },
    "total amount": {
      "total_amount": 1740
    }
  },
  "sales": {
    "top books": [
      {
        "book_id": 1,
        "title": "Cien años de soledad",
        "total_sales": 1
      }
    ],
    "total": {
      "total_sales": 1
    },
    "revenue": {
      "total_revenue": 0
    }
  }
}
```

---
## Comunicación entre Microservicios

Los microservicios se comunican mediante HTTP/REST:

- **Préstamos → Libros**: Consulta disponibilidad y ajusta stock al crear o devolver préstamos
- **Préstamos → Multas**: Genera multas por devoluciones atrasadas
- **Compras → Libros**: Descuenta stock al registrar ventas
- **Reportes → Préstamos / Multas / Compras**: Agrega reportes consolidados de actividad


## ⚠️ Notas importantes
 
**Orden de arranque:** Los microservicios deben estar corriendo **antes** de iniciar el API Gateway, ya que este realiza llamadas HTTP a ellos en el momento de las peticiones.
 
**Variables de entorno:** Nunca subas archivos `.env` ni `serviceAccountKey.json` al repositorio. Están incluidos en `.gitignore`.
 
**Entornos virtuales Python:** Cada servicio Python (Books, Fines, Reports) tiene su propio `venv`. No compartas entornos entre servicios.
 
**Firebase:** El archivo `serviceAccountKey.json` contiene credenciales de producción. Trátalo como una contraseña.
 

## Autor

**Sergio Alejandro Gaitán Quintero** - Estudiante de Administración de sistemas informáticos - Universidad Nacional de Colombia
