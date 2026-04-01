# Microservicio de Gestión de Libros

Microservicio desarrollado en **Flask** para la gestión de libros de una biblioteca digital. Este servicio forma parte de una arquitectura de microservicios y proporciona operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para la entidad `Book`.

## 📋 Tabla de Contenidos

- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelo de Datos](#modelo-de-datos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Migraciones de Base de Datos](#migraciones-de-base-de-datos)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Autenticación](#autenticación)
- [Características](#características)

## 🚀 Tecnologías

- **Python 3.11**
- **Flask 3.1.3** - Framework web minimalista
- **Flask-SQLAlchemy 3.1.1** - ORM para manejo de base de datos
- **Flask-Migrate 4.1.0** - Gestión de migraciones de base de datos (Alembic)
- **Flask-CORS 6.0.2** - Manejo de CORS para peticiones cross-origin
- **PyMySQL 1.1.2** - Driver MySQL para Python
- **python-dotenv 1.2.2** - Carga de variables de entorno desde archivo `.env`

## 🏗️ Arquitectura

Este microservicio sigue una arquitectura modular basada en el patrón MVC (Modelo-Vista-Controlador) adaptado para APIs REST:

```
┌─────────────────┐
│   Client/API    │
│    Gateway      │
└────────┬────────┘
         │ HTTP/REST
         │ X-Internal-API-Key
         ↓
┌─────────────────┐
│  Flask Routes   │ ← routes.py (Controladores)
├─────────────────┤
│  Business Logic │ ← Decoradores de autenticación
├─────────────────┤
│   ORM Layer     │ ← models.py (SQLAlchemy)
├─────────────────┤
│   MySQL DB      │ ← books_db
└─────────────────┘
```

## 📁 Estructura del Proyecto

```
books/
│
├── app.py                  # Punto de entrada de la aplicación
├── config.py               # Configuración de la aplicación
├── models.py               # Modelos de base de datos (ORM)
├── routes.py               # Definición de rutas y endpoints
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (no versionado)
│
├── migrations/             # Migraciones de Alembic
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   ├── README
│   └── versions/           # Historial de migraciones
│       ├── 7078ac70a7cb_creacion_de_tablas.py
│       ├── 63c11c692ff8_migraciones.py
│       └── e59c552cec57_modificaciones.py
│
└── venv/                   # Entorno virtual (no versionado)
```

### Descripción de Archivos Principales

- **`app.py`**: Inicializa la aplicación Flask, configura extensiones (SQLAlchemy, Migrate, CORS) y registra las rutas.
- **`config.py`**: Define la clase `Config` que carga variables de entorno y configura la conexión a la base de datos.
- **`models.py`**: Define el modelo `Book` con SQLAlchemy, incluyendo el esquema de tabla y el método `to_dict()`.
- **`routes.py`**: Implementa los endpoints REST y el decorador `@requiere_token` para autenticación.

## 📊 Modelo de Datos

### Entidad: `Book`

| Campo        | Tipo        | Descripción                                  | Restricciones           |
|--------------|-------------|----------------------------------------------|-------------------------|
| `id`         | Integer     | Identificador único del libro                | Primary Key, Auto-increment |
| `title`      | String(255) | Título del libro                             | NOT NULL                |
| `author`     | String(255) | Autor del libro                              | NOT NULL                |
| `isbn`       | String(20)  | Código ISBN del libro                        | UNIQUE, Nullable        |
| `description`| Text        | Descripción o sinopsis del libro             | Nullable                |
| `category`   | String(50)  | Categoría del libro                          | Nullable                |
| `available`  | Boolean     | Indica si el libro está disponible           | Default: True, NOT NULL |
| `quantity`   | Integer     | Cantidad total de ejemplares disponibles     | Default: 1, NOT NULL    |

**Tabla**: `books`

**Método auxiliar**: `to_dict()` serializa la instancia del modelo a un diccionario JSON.

## ⚙️ Instalación

### Requisitos Previos

- Python 3.11+
- MySQL Server 5.7+ o MariaDB
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio** (o descomprimir el proyecto):
   ```bash
   cd books
   ```

2. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**:
   - En Windows (Git Bash):
     ```bash
     source venv/Scripts/activate
     ```
   - En Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=books_db
DB_USER=root
DB_PASSWORD=

# Security
INTERNAL_API_KEY=123
SECRET_KEY=your-secret-key-here

# Database URL (SQLAlchemy)
DATABASE_URL=mysql+pymysql://root:@localhost/books_db
```

### Configuración de Base de Datos

1. **Crear la base de datos en MySQL**:
   ```sql
   CREATE DATABASE books_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Verificar la conexión** editando `DATABASE_URL` en el archivo `.env` según tu configuración local:
   ```
   DATABASE_URL=mysql+pymysql://usuario:contraseña@host:puerto/nombre_db
   ```

## 🗄️ Migraciones de Base de Datos

Este proyecto utiliza **Flask-Migrate** (wrapper de Alembic) para gestionar el esquema de la base de datos.

### Inicializar Migraciones (si es necesario)

```bash
flask db init
```

### Crear una Nueva Migración

Después de modificar los modelos en `models.py`:

```bash
flask db migrate -m "Descripción del cambio"
```

### Aplicar Migraciones

```bash
flask db upgrade
```

### Historial de Migraciones

El proyecto incluye las siguientes migraciones ya aplicadas:

1. **`7078ac70a7cb_creacion_de_tablas.py`** - Creación inicial de la tabla `books`
2. **`63c11c692ff8_migraciones.py`** - Migración intermedia
3. **`e59c552cec57_modificaciones.py`** - Modificaciones al esquema

### Revertir una Migración

```bash
flask db downgrade
```

## 🚀 Uso

### Ejecutar el Servidor de Desarrollo

```bash
python app.py
```

El servidor se iniciará en `http://127.0.0.1:5000` por defecto.

**Nota**: El servidor está configurado con `debug=True` y `use_reloader=False` para facilitar el desarrollo.


## 📡 API Endpoints

Todos los endpoints requieren el header de autenticación `X-Internal-API-Key`.

### **GET** `/books`

Obtiene la lista completa de libros.

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "El Quijote",
    "author": "Miguel de Cervantes",
    "isbn": "978-8424936464",
    "description": "Las aventuras de Don Quijote de la Mancha",
    "category": "Clásicos",
    "available": true,
    "quantity": 5
  }
]
```

---

### **GET** `/books/<id>`

Obtiene un libro específico por su ID.

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "El Quijote",
  "author": "Miguel de Cervantes",
  "isbn": "978-8424936464",
  "description": "Las aventuras de Don Quijote de la Mancha",
  "category": "Clásicos",
  "available": true,
  "quantity": 5
}
```

**Errores**:
- `404 Not Found` - El libro no existe

---

### **POST** `/books`

Crea un nuevo libro.

**Request Body**:
```json
{
  "title": "Cien Años de Soledad",
  "author": "Gabriel García Márquez",
  "isbn": "978-0307474728",
  "description": "La historia de la familia Buendía",
  "category": "Literatura Latinoamericana",
  "available": true,
  "quantity": 3
}
```

**Campos requeridos**: `title`, `author`

**Response** (201 Created):
```json
{
  "id": 2,
  "title": "Cien Años de Soledad",
  "author": "Gabriel García Márquez",
  "isbn": "978-0307474728",
  "description": "La historia de la familia Buendía",
  "category": "Literatura Latinoamericana",
  "available": true,
  "quantity": 3
}
```

**Errores**:
- `400 Bad Request` - Faltan campos requeridos

---

### **PUT** `/books/<id>`

Actualiza un libro existente.

**Request Body** (campos opcionales):
```json
{
  "title": "Don Quijote de la Mancha (Edición Anotada)",
  "quantity": 10,
  "available": true
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Don Quijote de la Mancha (Edición Anotada)",
  "author": "Miguel de Cervantes",
  "isbn": "978-8424936464",
  "description": "Las aventuras de Don Quijote de la Mancha",
  "category": "Clásicos",
  "available": true,
  "quantity": 10
}
```

**Errores**:
- `400 Bad Request` - No se proporcionaron datos
- `404 Not Found` - El libro no existe

---

### **DELETE** `/books/<id>`

Elimina un libro por su ID.

**Response** (200 OK):
```json
{
  "message": "Book 1 deleted"
}
```

**Errores**:
- `404 Not Found` - El libro no existe

## 🔐 Autenticación

Este microservicio utiliza un mecanismo de autenticación basado en **API Key** para comunicación entre servicios internos.

### Funcionamiento

1. Todas las rutas están protegidas con el decorador `@requiere_token`.
2. El cliente debe enviar el header `X-Internal-API-Key` en cada petición.
3. El valor del header se compara con la variable de entorno `INTERNAL_API_KEY`.

### Ejemplo de Petición

```bash
curl -X GET http://localhost:5000/books \
  -H "X-Internal-API-Key: 123"
```

### Respuesta de Error de Autenticación

```json
{
  "error": "Unauthorized"
}
```

**Código HTTP**: `401 Unauthorized`

## ✨ Características

### Implementadas

- ✅ **CRUD Completo**: Operaciones Create, Read, Update, Delete para libros
- ✅ **Autenticación por API Key**: Protección de endpoints con header personalizado
- ✅ **CORS Habilitado**: Permite peticiones desde diferentes orígenes
- ✅ **ORM con SQLAlchemy**: Abstracción de base de datos y consultas SQL
- ✅ **Migraciones Automáticas**: Gestión de esquema con Flask-Migrate/Alembic
- ✅ **Serialización JSON**: Método `to_dict()` para respuestas consistentes
- ✅ **Validación de Datos**: Validación de campos requeridos en POST
- ✅ **Manejo de Errores**: Respuestas HTTP apropiadas (404, 400, 401, 200, 201)
- ✅ **Configuración por Variables de Entorno**: Uso de `.env` para configuración flexible
- ✅ **Logging de Debug**: Prints de headers y variables de entorno para depuración

### Mejoras Potenciales

- 🔄 **Paginación**: Implementar paginación en `GET /books` para grandes volúmenes de datos
- 🔄 **Filtrado y Búsqueda**: Agregar query parameters para filtrar por autor, categoría, ISBN
- 🔄 **Validación Avanzada**: Usar Marshmallow o Pydantic para validación de schemas
- 🔄 **Rate Limiting**: Limitar número de peticiones por IP/API Key
- 🔄 **Logging Estructurado**: Implementar logging con niveles (INFO, ERROR, WARNING)
- 🔄 **Testing**: Agregar pruebas unitarias y de integración con pytest
- 🔄 **Documentación OpenAPI/Swagger**: Generar documentación interactiva de la API
- 🔄 **Health Check Endpoint**: Endpoint `/health` para monitoreo del servicio
- 🔄 **Docker**: Containerizar el servicio con Dockerfile y docker-compose

---

## 📝 Notas Adicionales

### Depuración

El archivo `routes.py` incluye prints de debug que muestran:
- El header `X-Internal-API-Key` recibido
- El valor de la variable de entorno `INTERNAL_API_KEY`

Estos prints deben eliminarse o reemplazarse con logging apropiado en producción.

### Seguridad

⚠️ **Importante**: 
- Cambiar el valor de `INTERNAL_API_KEY` en producción a un valor seguro y aleatorio.
- Nunca commitear el archivo `.env` al repositorio Git.
- Usar variables de entorno del sistema 

### Base de Datos

- El modelo actual permite múltiples ejemplares del mismo libro controlados por el campo `quantity`.

---

**Desarrollado con Flask para una arquitectura de microservicios de biblioteca digital.**