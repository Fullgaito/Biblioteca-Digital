# Microservicio de Préstamos - Sistema de Biblioteca Digital

Microservicio REST desarrollado en **Node.js/Express** con **MongoDB/Mongoose** para gestionar préstamos de libros en una biblioteca digital. Parte de una arquitectura de microservicios que se comunica con servicios de libros (Flask) y multas (Django).

## 🛠 Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Node.js** | - | Runtime JavaScript |
| **Express** | 5.2.1 | Framework web minimalista |
| **Mongoose** | 9.3.3 | ODM para MongoDB |
| **MongoDB** | - | Base de datos NoSQL |
| **dotenv** | 17.3.1 | Gestión de variables de entorno |
| **cors** | 2.8.6 | Manejo de CORS |

---

## 🏗 Arquitectura

```
┌─────────────────┐
│  API Gateway    │
│   (Laravel)     │
└────────┬────────┘
         │
         ├─────────────► Microservicio LOANS (Express/MongoDB)
         │                        │
         │                        ├──► GET libros → Flask
         │                        ├──► PUT stock ↓/↑ → Flask
         │                        └──► POST multas → Django
         │
         ├─────────────► Microservicio BOOKS (Flask)
         └─────────────► Microservicio FINES (Django)
```

**Comunicación entre servicios:**
- Requests HTTP con `fetch` nativo de Node.js
- Autenticación mediante header `X-Internal-API-Key`
- Gestión de rollback en caso de fallos

---

## 📁 Estructura del Proyecto

```
loans/
├── models/
│   └── loan.js              # Esquema Mongoose del préstamo
├── routes/
│   └── loans.js             # Rutas y controladores REST
├── node_modules/            # Dependencias (no subir a Git)
├── .env                     # Variables de entorno (no subir a Git)
├── server.js                # Punto de entrada de la aplicación
├── package.json             # Configuración del proyecto y dependencias
└── package-lock.json        # Lock de versiones exactas
```

---

## 💾 Modelo de Datos

### Esquema `Loan` (Mongoose)

```javascript
{
  book_id: Number,          // ID del libro (referencia a microservicio Flask)
  user_id: Number,          // ID del usuario
  loan_date: Date,          // Fecha de préstamo (auto: Date.now)
  return_date: Date,        // Fecha de devolución (null si activo)
  status: String            // 'active' | 'returned' (default: 'active')
}
```

---

## 🚀 Instalación

### 1. Clonar/extraer el proyecto

```bash
cd loans
```

### 2. Instalar dependencias

```bash
npm install
```

Esto instalará:
- `express@5.2.1`
- `mongoose@9.3.3`
- `dotenv@17.3.1`
- `cors@2.8.6`

### 3. Configurar MongoDB

Asegúrate de tener MongoDB corriendo localmente:

```bash
# Verificar que MongoDB esté activo
sudo systemctl status mongod

# Iniciar MongoDB si no está corriendo
sudo systemctl start mongod

# Crear la base de datos (opcional, se crea automáticamente)
mongosh
use loans_db
```

### 4. Iniciar el servidor

```bash
node server.js
```

Salida esperada:
```
Conectado a MongoDB
Servidor corriendo en puerto 3002
```

---

## ⚙️ Configuración

### Variables de entorno (`.env`)

```env
# MongoDB
MONGO_URI=mongodb://127.0.0.1:27017/loans_db

# Puerto del microservicio
PORT=3002

# Clave de autenticación interna
INTERNAL_API_KEY=123

# URLs de otros microservicios
FLASK_URL=http://localhost:5000        # Microservicio de libros
FINES_URL=http://localhost:8001        # Microservicio de multas
```

**⚠️ Importante:** El archivo `.env` NO debe subirse a Git. Añadir a `.gitignore`:

```gitignore
.env
node_modules/
```

---

## 🔌 Endpoints REST

Todas las rutas requieren autenticación mediante header `X-Internal-API-Key`.

### 1. Registrar un nuevo préstamo

**POST** `/loans`

**Headers:**
```
X-Internal-API-Key: 123
Content-Type: application/json
```

**Body:**
```json
{
  "user_id": 101,
  "book_id": 5
}
```

**Flujo de operación:**
1. Valida que el usuario no tenga ya ese libro prestado activo
2. Consulta disponibilidad del libro en Flask (`GET /books/:id`)
3. Valida que haya stock (`quantity > 0`)
4. Decrementa stock en Flask (`PUT /books/:id/decrement`)
5. Crea el préstamo en MongoDB
6. **Rollback:** Si falla el guardado, incrementa stock nuevamente

**Respuesta exitosa (201):**
```json
{
  "message": "Loan created successfully",
  "id": "507f1f77bcf86cd799439011"
}
```

**Errores posibles:**
- `400`: Campos faltantes, usuario ya tiene el libro, sin stock
- `401`: API Key inválida
- `404`: Libro no encontrado en Flask
- `500`: Error de conexión o guardado

---

### 2. Listar todos los préstamos

**GET** `/loans`

**Headers:**
```
X-Internal-API-Key: 123
```

**Respuesta (200):**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "book_id": 5,
    "user_id": 101,
    "loan_date": "2025-04-01T10:30:00.000Z",
    "return_date": null,
    "status": "active"
  },
  {
    "_id": "507f191e810c19729de860ea",
    "book_id": 3,
    "user_id": 102,
    "loan_date": "2025-03-28T14:20:00.000Z",
    "return_date": "2025-04-01T09:15:00.000Z",
    "status": "returned"
  }
]
```

---

### 3. Devolver un libro

**PUT** `/loans/:id/return`

**Headers:**
```
X-Internal-API-Key: 123
```

**Ejemplo:**
```
PUT /loans/507f1f77bcf86cd799439011/return
```

**Flujo de operación:**
1. Busca el préstamo por ID
2. Valida que no esté ya devuelto
3. Incrementa stock en Flask (`PUT /books/:book_id/increment`)
4. Calcula días de retraso con `calculateDaysLate()` ⚠️ (función no implementada en el código)
5. Si hay retraso, crea multa en Django (`POST /fines`)
6. Actualiza préstamo: `status = 'returned'`, `return_date = now()`

**Respuesta (200):**
```json
{
  "message": "Book returned successfully",
  "loan": {
    "_id": "507f1f77bcf86cd799439011",
    "book_id": 5,
    "user_id": 101,
    "loan_date": "2025-04-01T10:30:00.000Z",
    "return_date": "2025-04-03T16:45:00.000Z",
    "status": "returned"
  },
  "fine_created": false
}
```

**Errores posibles:**
- `400`: Préstamo ya devuelto
- `404`: Préstamo no encontrado
- `500`: Error al actualizar stock o crear multa

---

### 4. Obtener préstamos por usuario

**GET** `/loans/usuario/:user_id`

**Headers:**
```
X-Internal-API-Key: 123
```

**Ejemplo:**
```
GET /loans/usuario/507f1f77bcf86cd799439011
```

**Respuesta (200):**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "book_id": 5,
    "user_id": 101,
    "loan_date": "2025-04-01T10:30:00.000Z",
    "return_date": null,
    "status": "active"
  }
]
```

**Error (404):**
```json
{
  "error": "No loans found for this user"
}
```

---

### 5. Obtener préstamos activos

**GET** `/loans/activos`

**Headers:**
```
X-Internal-API-Key: 123
```

**Respuesta (200):**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "book_id": 5,
    "user_id": 101,
    "loan_date": "2025-04-01T10:30:00.000Z",
    "return_date": null,
    "status": "active"
  }
]
```

---

## 🔄 Flujo de Operaciones

### Creación de préstamo (con rollback)

```
1. Cliente → POST /loans {user_id, book_id}
   ↓
2. Validar datos y préstamo no duplicado
   ↓
3. Consultar libro → GET Flask/books/:id
   ↓
4. Validar stock disponible
   ↓
5. Decrementar stock → PUT Flask/books/:id/decrement
   ↓ [SI FALLA AQUÍ]
6. Guardar préstamo en MongoDB
   ↓ [CATCH ERROR]
7. ROLLBACK: → PUT Flask/books/:id/increment
   ↓
8. Responder 201 con ID del préstamo
```

### Devolución de libro (con multa)

```
1. Cliente → PUT /loans/:id/return
   ↓
2. Buscar préstamo en MongoDB
   ↓
3. Validar que esté activo
   ↓
4. Incrementar stock → PUT Flask/books/:book_id/increment
   ↓
5. Calcular días de retraso (calculateDaysLate)
   ↓ [SI daysLate > 0]
6. Crear multa → POST Django/fines
   ↓
7. Actualizar préstamo: status='returned', return_date=now()
   ↓
8. Responder 200 con loan y fine_created
```

---

## 🔐 Autenticación

### Middleware `authInternal`

```javascript
const authInternal = function (req, res, next) {
    const apiKey = req.headers['x-internal-api-key'];
    const internalKey = process.env.INTERNAL_API_KEY;

    if (!apiKey || apiKey !== internalKey) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    next();
};
```

**Uso en todas las rutas:**
```javascript
router.post('/', authInternal, async (req, res) => { ... });
router.get('/', authInternal, async (req, res) => { ... });
```

**Ejemplo de request con autenticación:**

```bash
curl -X POST http://localhost:3000/loans \
  -H "X-Internal-API-Key: 123" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 101, "book_id": 5}'
```

## 📝 Notas Técnicas

### Diferencias con otros microservicios

| Aspecto | LOANS (Express) | BOOKS (Flask) |
|---------|----------------|---------------|
| Lenguaje | JavaScript | Python |
| Framework | Express 5.2.1 | Flask 3.1.3 |
| BD | MongoDB (NoSQL) | MySQL (SQL) |
| ORM/ODM | Mongoose | SQLAlchemy |
| Tipado | Schemas Mongoose | Modelos SQLAlchemy |

### Comunicación inter-servicios

```javascript
// Patrón de comunicación con Flask
const response = await fetch(`${process.env.FLASK_URL}/books/${book_id}`, {
    headers: {
        'Content-Type': 'application/json',
        'X-Internal-API-Key': process.env.INTERNAL_API_KEY
    }
});

if (!response.ok) {
    throw new Error(`Flask responded with ${response.status}`);
}

const book = await response.json();
```

### Gestión de errores en rollback

```javascript
try {
    // Operación principal
    await decrementStock();
    await saveLoan();
} catch (error) {
    // ⚠️ Si el rollback también falla, el sistema queda inconsistente
    await incrementStock(); // Puede fallar silenciosamente
    return res.status(500).json({ error: error.message });
}

```

### Probar endpoints con curl

```
```

### Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Cannot connect to MongoDB` | MongoDB no está corriendo | `sudo systemctl start mongod` |
| `Unauthorized` | API Key incorrecta | Verificar header y .env |
| `Book not found` | Flask no responde | Verificar que Flask esté en puerto 5000 |
| `Error updating stock` | Endpoint de Flask incorrecto | Verificar logs de Flask |

---

**Versión del documento:** 1.0  
**Fecha:** Abril 2026  
**Autor:** Análisis del microservicio `loans` para sistema de biblioteca digital