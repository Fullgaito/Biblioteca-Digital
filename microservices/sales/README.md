# Microservicio de ventas

Microservicio encargado de gestionar las **ventas de libros** dentro del sistema Biblioteca Digital. Se comunica con el servicio de libros para obtener información del producto y calcula el precio total de cada transacción. Persiste los datos en **Firebase Realtime Database**.

---

## 🧰 Stack tecnológico

| Tecnología | Uso |
|---|---|
| Node.js | Runtime |
| Express | Framework HTTP |
| Firebase Admin SDK | Persistencia (Realtime Database) |
| dotenv | Variables de entorno |
| axios | Comunicación con el servicio de libros |

---

## 📁 Estructura del proyecto

```
sales/
├── routes/
│   └── sales.js          # Definición de endpoints
├── server.js             # Punto de entrada, configuración Express
├── firebase.js           # Inicialización de Firebase Admin
├── serviceAccountKey.json # Credenciales Firebase (no subir a VCS)
├── package.json
├── package-lock.json
└── .env
```

---

## ⚙️ Variables de entorno

Crea un archivo `.env` en la raíz del servicio con las siguientes variables:

```env
PORT=3001
FLASK_URL=http://localhost:5000
FIREBASE_DB_URL=https://microservicio-ventas-default-rtdb.firebaseio.com/
```

| Variable | Descripción |
|---|---|
| `PORT` | Puerto en el que corre el servicio |
| `FLASK_URL` | URL base del microservicio de libros (Books) |
| `FIREBASE_DB_URL` | URL de la instancia de Firebase Realtime Database |

> ⚠️ El archivo `serviceAccountKey.json` contiene las credenciales de Firebase. No debe incluirse en el control de versiones.

---

## 🚀 Instalación y ejecución

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
node server.js
```

El servicio quedará disponible en `http://localhost:3001`.

---

## 🔗 Comunicación entre servicios

Este microservicio depende del **servicio de libros (Books)** para validar la existencia del libro y obtener su precio antes de registrar una venta.

```
Sales Service  ──HTTP GET──►  Books Service (:5000)
     │                              │
     └──── Registra venta ──────►  Firebase RTDB
```

---

## 📌 Endpoints

Base URL: `/api/sales`

---

### 🔹 Crear una venta

**`POST`** `/api/sales`

Registra una nueva venta. Se conecta al servicio de libros para obtener el precio unitario y calcula el `total_price` en función de la cantidad solicitada.

#### Request body

```json
{
  "user_id": 1,
  "book_id": 1,
  "quantity": 4
}
```

| Campo | Tipo | Descripción |
|---|---|---|
| `user_id` | integer | ID del usuario que realiza la compra |
| `book_id` | integer | ID del libro a comprar |
| `quantity` | integer | Cantidad de ejemplares |

#### Response `200 OK`

```json
{
  "message": "Sale completed",
  "id": "-OpFRQdYXRUIORNwxMYM",
  "total_price": 240000
}
```

---

### 🔹 Obtener todas las ventas

**`GET`** `/api/sales`

Retorna el listado completo de ventas registradas en la base de datos.

#### Response `200 OK`

```json
{
  "data": [
    {
      "book_id": 1,
      "created_at": "2026-04-02T23:05:24.283Z",
      "id": "-OpFRQdYXRUIORNwxMYM",
      "quantity": 4,
      "total_price": 240000,
      "user_id": 1
    }
  ]
}
```

---

### 🔹 Obtener una venta por ID

**`GET`** `/api/sales/:id`

Retorna el detalle de una venta específica usando su ID de Firebase.

#### Parámetros de ruta

| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | string | ID de la venta en Firebase (ej: `-OpFRQdYXRUIORNwxMYM`) |

#### Response `200 OK`

```json
{
  "data": {
    "book_id": 1,
    "created_at": "2026-04-02T23:05:24.283Z",
    "id": "-OpFRQdYXRUIORNwxMYM",
    "quantity": 4,
    "total_price": 240000,
    "user_id": 1
  }
}
```

---

### 🔹 Obtener ventas por usuario

**`GET`** `/api/sales/user/:userId`

Retorna todas las ventas realizadas por un usuario específico.

#### Parámetros de ruta

| Parámetro | Tipo | Descripción |
|---|---|---|
| `userId` | integer | ID del usuario |

#### Response `200 OK`

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

---

## 🗄️ Modelo de datos (Firebase RTDB)

Cada venta se almacena bajo la colección `sales` con la siguiente estructura:

```json
{
  "sales": {
    "-OpFRQdYXRUIORNwxMYM": {
      "user_id": 1,
      "book_id": 1,
      "quantity": 4,
      "total_price": 240000,
      "created_at": "2026-04-02T23:05:24.283Z"
    }
  }
}
```

> El ID de cada venta es generado automáticamente por Firebase (push key).

---

## 🧩 Integración con el API Gateway

Este servicio es consumido a través del **API Gateway (Laravel)**, el cual se encarga de autenticar las peticiones antes de redirigirlas a este microservicio.

```
Cliente  ──►  API Gateway (:8080)  ──►  Sales Service (:3001)
```

Las rutas expuestas al exterior siguen el patrón `/api/sales/*` y son accesibles únicamente con un token JWT válido emitido por el gateway.