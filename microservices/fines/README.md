# Microservicio de Multas - Sistema de Biblioteca Digital

Microservicio REST desarrollado en **Django 5.2** con **Django REST Framework** y **PostgreSQL** para gestionar multas por retraso en devolución de libros. Parte de una arquitectura de microservicios que recibe notificaciones del servicio de préstamos (Express).

---


## 🛠 Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.x | Lenguaje de programación |
| **Django** | 5.2.12 | Framework web completo |
| **Django REST Framework** | 3.17.1 | API REST toolkit |
| **PostgreSQL** | - | Base de datos relacional |
| **psycopg2-binary** | 2.9.11 | Adaptador PostgreSQL |
| **python-dotenv** | 1.2.2 | Gestión de variables de entorno |
| **sqlparse** | 0.5.5 | Parser SQL (dependencia Django) |

---

## 🏗 Arquitectura

```
┌─────────────────┐
│  API Gateway    │
│   (Laravel)     │
└────────┬────────┘
         │
         ├─────────────► Microservicio LOANS (Express)
         │                        │
         │                        └──► POST /fines (crear multa)
         │                                   ↓
         └─────────────► Microservicio FINES (Django/PostgreSQL)
                                     │
                                     ├── GET /fines (listar todas)
                                     ├── GET /fines/:id (obtener una)
                                     ├── GET /fines/user/:user_id
                                     └── PUT /fines/:id/pay (pagar)
```

**Flujo típico:**
1. Usuario devuelve libro con retraso en **LOANS** (Express)
2. **LOANS** calcula días de retraso
3. **LOANS** llama `POST /fines` en **FINES** (Django)
4. **FINES** crea multa con `amount = days_late * 580`
5. Usuario consulta multas pendientes
6. Usuario paga multa → `PUT /fines/:id/pay`

---

## 📁 Estructura del Proyecto

```
fines/
├── fines_service/                   # Proyecto Django principal
│   ├── fines/                       # App Django "fines"
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py     # Migración inicial (tabla Fine)
│   │   │   └── 0002_remove_fine_created_at.py  # Elimina created_at
│   │   ├── __init__.py
│   │   ├── admin.py                # Configuración admin de Django
│   │   ├── apps.py                 # Configuración de la app
│   │   ├── middleware.py           # Middleware vacío (AuthN no implementada)
│   │   ├── models.py               # Modelo Fine (ORM)
│   │   ├── serializers.py          # Serializador DRF
│   │   ├── tests.py                # Tests unitarios (vacío)
│   │   └── views.py                # Vistas/controladores API
│   │
│   ├── fines_service/              # Configuración del proyecto
│   │   ├── __init__.py
│   │   ├── settings.py             # Settings de Django
│   │   ├── urls.py                 # Rutas principales
│   │   ├── wsgi.py                 # WSGI para deployment
│   │   └── asgi.py                 # ASGI para deployment
│   │
│   ├── manage.py                   # CLI de Django
│   └── .env                        # Variables de entorno
│
├── venv/                            # Entorno virtual Python (no subir a Git)
└── requirements.txt                 # Dependencias del proyecto
```

---

## 🚀 Instalación

### 1. Prerequisitos

```bash
# Verificar Python 3.x instalado
python --version

# Verificar PostgreSQL instalado y corriendo
psql --version
sudo systemctl status postgresql
```

### 2. Crear entorno virtual

```bash
cd fines
python -m venv venv

# Activar el entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- `Django==5.2.12`
- `djangorestframework==3.17.1`
- `psycopg2-binary==2.9.11`
- `python-dotenv==1.2.2`
- `sqlparse==0.5.5`
- `tzdata==2025.3`

### 4. Configurar PostgreSQL desde la consola de PostgreSQL

```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE fines_db;
CREATE USER postgres WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE fines_db TO postgres;

# Salir
\q
```

**Nota:** Si `postgres` ya existe como superusuario, solo crea la base de datos:
```sql
CREATE DATABASE fines_db;
```

### 5. Aplicar migraciones

```bash
cd fines_service
python manage.py migrate
```

Salida esperada:
```
Operations to perform:
  Apply all migrations: fines
Running migrations:
  Applying fines.0001_initial... OK
  Applying fines.0002_remove_fine_created_at... OK
```

### 6. Iniciar el servidor

```bash
python manage.py runserver 8001
```

Salida esperada:
```
Django version 5.2.12, using settings 'fines_service.settings'
Starting development server at http://127.0.0.1:8001/
Quit the server with CONTROL-C.
```

---

## ⚙️ Configuración

### Variables de entorno (`.env`)

Ubicación: `/fines_service/.env`

```env
# PostgreSQL
DB_NAME=fines_db
DB_USER=postgres
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432

# Autenticación interna
INTERNAL_API_KEY=123
```

**⚠️ Importante:** El archivo `.env` NO debe subirse a Git.

### Configuración en `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

INSTALLED_APPS = [
    # ... apps de Django por defecto
    'rest_framework',  # Django REST Framework
    'fines',           # App de multas
]

MIDDLEWARE = [
    # ... middlewares de Django por defecto
    'fines.middleware.InternalAPIKeyMiddleware',  # ⚠️ MIDDLEWARE VACÍO
]
```

---

### Comandos útiles

```bash
# Ver migraciones aplicadas
python manage.py showmigrations

# Crear nueva migración después de modificar models.py
python manage.py makemigrations

# Aplicar migraciones pendientes
python manage.py migrate

# Revertir migración
python manage.py migrate fines 0001_initial

# Ver SQL de una migración
python manage.py sqlmigrate fines 0001
```

---

## 🔌 Endpoints REST

**Base URL:** `http://localhost:8001`


---

### 1. Crear multa

**POST** `/fines`

**Headers esperados (no validados actualmente):**
```
X-Internal-API-Key: 123
Content-Type: application/json
```

**Body:**
```json
{
  "user_id": 101,
  "loan_id": "507f1f77bcf86cd799439011",
  "days_late": 5
}
```

**Lógica de cálculo:**
```python
amount = days_late * 580  # $580 por día de retraso
```

**Respuesta exitosa (201):**
```json
{
  "message": "Fine created",
  "id": 1
}
```

**Errores posibles:**
- `400`: Campos faltantes (`user_id`, `loan_id` o `days_late`)

---

### 2. Listar todas las multas

**GET** `/fines`

**Ejemplo:**
```bash
curl http://localhost:8001/fines
```

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "user_id": 101,
    "loan_id": "507f1f77bcf86cd799439011",
    "amount": "2900.00",
    "days_late": 5,
    "status": "pending",
    "paid_at": null
  },
  {
    "id": 2,
    "user_id": 102,
    "loan_id": "507f191e810c19729de860ea",
    "amount": "1160.00",
    "days_late": 2,
    "status": "paid",
    "paid_at": "2025-04-03T10:30:00Z"
  }
]
```

---

### 3. Obtener multa por ID

**GET** `/fines/:id`

**Ejemplo:**
```bash
curl http://localhost:8001/fines/1
```

**Respuesta (200):**
```json
{
  "id": 1,
  "user_id": 101,
  "loan_id": "507f1f77bcf86cd799439011",
  "days_late": 5,
  "amount": "2900.00",
  "status": "pending",
  "paid_at": null
}
```

**Error (404):**
```json
{
  "error": "Not found"
}
```

---

### 4. Obtener multas de un usuario

**GET** `/fines/user/:user_id`

**Ejemplo:**
```bash
curl http://localhost:8001/fines/user/101
```

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "user_id": 101,
    "loan_id": "507f1f77bcf86cd799439011",
    "amount": "2900.00",
    "days_late": 5,
    "status": "pending",
    "paid_at": null
  },
  {
    "id": 3,
    "user_id": 101,
    "loan_id": "507f1f77bcf86cd799439012",
    "amount": "580.00",
    "days_late": 1,
    "status": "paid",
    "paid_at": "2025-04-01T15:20:00Z"
  }
]
```

**Nota:** Devuelve array vacío `[]` si el usuario no tiene multas (no es error 404).

---

### 5. Pagar multa

**PUT** `/fines/:id/pay`

**Ejemplo:**
```bash
curl -X PUT http://localhost:8001/fines/1/pay
```

**Lógica:**
```python
fine.status = 'paid'
fine.paid_at = timezone.now()  # Timestamp actual UTC
fine.save()
```

**Respuesta exitosa (200):**
```json
{
  "message": "Fine paid"
}
```

**Errores posibles:**
- `400`: Multa ya pagada (`"error": "Already paid"`)
- `404`: Multa no encontrada (`"error": "Not found"`)

---

## 💼 Lógica de Negocio

### Cálculo de multa

```python
# En views.py - línea 21
amount = days_late * 580
```

**Fórmula:**
- **Tarifa diaria:** $580 COP (colombianos)
- **Ejemplos:**
  - 1 día de retraso → $580
  - 5 días de retraso → $2,900
  - 10 días de retraso → $5,800


### Estados de multa

```python
status = 'pending'  # Recién creada
status = 'paid'     # Pagada
```

**Flujo de estados:**
```
[Creación] → pending → [Pago] → paid
```

No hay estados intermedios ni multas canceladas/perdonadas.

### Timestamp de pago

```python
# Al pagar (PUT /fines/:id/pay)
fine.paid_at = timezone.now()  # UTC
```

Django usa `USE_TZ = True` por defecto, almacenando timestamps en UTC.

---

## 🔐 Autenticación


**Configuración en `settings.py`:**
```python
MIDDLEWARE = [
    # ...
    'fines.middleware.InternalAPIKeyMiddleware',  # ← Registrado
]
```

### Campos calculados

```python
# En views.py - línea 21
amount = days_late * 580
```

El monto NO se almacena en el request, se calcula server-side. Esto evita que el cliente manipule el precio.


### Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `relation "fines_fine" does not exist` | Migraciones no aplicadas | `python manage.py migrate` |
| `FATAL: password authentication failed` | Credenciales incorrectas en .env | Verificar DB_PASSWORD |
| `Port 8001 already in use` | Otro proceso usando el puerto | `lsof -i :8080` y matar proceso |
| `could not connect to server` | PostgreSQL no está corriendo | `sudo systemctl start postgresql` |
| `No module named 'psycopg2'` | Dependencias no instaladas | `pip install -r requirements.txt` |


**Versión del documento:** 1.0  
**Fecha:** Abril 2026  
**Autor:** Análisis del microservicio `fines` para sistema de biblioteca digital