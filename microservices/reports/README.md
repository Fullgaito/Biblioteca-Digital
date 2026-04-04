# 📊 Microservicio de reportes

Microservicio encargado de **agregar y consolidar datos** de los demás servicios del sistema Biblioteca Digital para generar reportes estadísticos desarrollado en **Flask**. No tiene base de datos propia, pero se usa una en MongoDB para guardar registros que puedan ser utilizados en procesos analítica; consulta en tiempo real los microservicios de libros, préstamos, multas y ventas a través de HTTP REST.

---

## 🧰 Stack tecnológico

| Tecnología | Uso |
|---|---|
| Python 3 | Runtime |
| Flask | Framework HTTP |
| requests / httpx | Comunicación HTTP con otros servicios |
| dotenv | Variables de entorno |

---

## 📁 Estructura del proyecto

```
reports/
├── reports/
│   ├── fines_reports.py      # Lógica de reportes de multas
│   ├── loans_reports.py      # Lógica de reportes de préstamos
│   └── sales_reports.py      # Lógica de reportes de ventas
├── services/
│   ├── books_service.py      # Cliente HTTP → Books Service
│   ├── fines_service.py      # Cliente HTTP → Fines Service
│   ├── loans_service.py      # Cliente HTTP → Loans Service
│   └── sales_service.py      # Cliente HTTP → Sales Service
├── app.py                    # Punto de entrada Flask
├── config.py                 # Configuración y variables de entorno
├── models.py                 # Modelos / estructuras de datos
├── routes.py                 # Registro de blueprints/rutas
├── requirements.txt
└── .env
```

---

## ⚙️ Variables de entorno

Crea un archivo `.env` en la raíz del servicio:

```env
BOOKS_SERVICE_URL=http://localhost:5000
LOANS_SERVICE_URL=http://localhost:3002
FINES_SERVICE_URL=http://localhost:8001
SALES_SERVICE_URL=http://localhost:3001
```

| Variable | Servicio destino | Puerto por defecto |
|---|---|---|
| `BOOKS_SERVICE_URL` | Books (Flask) | `5000` |
| `LOANS_SERVICE_URL` | Loans (Node.js) | `3002` |
| `FINES_SERVICE_URL` | Fines (Django) | `8001` |
| `SALES_SERVICE_URL` | Sales (Node.js) | `3001` |

---

## 🚀 Instalación y ejecución

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

El servicio quedará disponible en `http://localhost:5001`.

---

## 🔗 Comunicación entre servicios

Reports no persiste datos propios. Cada endpoint realiza llamadas HTTP a los servicios correspondientes, agrega la información y devuelve el resultado calculado.

```
                   ┌──────────────────────┐
                   │   Reports Service    │
                   │      (:5001)         │
                   └──────────┬───────────┘
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼                   ▼
  Books (:5000)       Loans (:3002)       Fines (:8001)       Sales (:3001)
  Flask + MySQL       Node + MongoDB      Django + PgSQL      Node + Firebase
```

---

## 📌 Endpoints

Base URL: `/api/reports`

---

### 🔹 Dashboard general

**`GET`** `/api/reports/dashboard`

Retorna un resumen consolidado del sistema: préstamos, multas y ventas en una sola respuesta. Útil como vista principal de métricas.

#### Response `200 OK`

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

### 🔹 Libros más vendidos

**`GET`** `/api/reports/most-sold-books`

Retorna los libros ordenados por cantidad de ventas, combinando datos del servicio de ventas y el catálogo de libros.

#### Response `200 OK`

```json
[
  {
    "book_id": 1,
    "title": "Cien años de soledad",
    "total_sales": 1
  }
]
```

---

### 🔹 Total de ventas

**`GET`** `/api/reports/total-sales`

Retorna el número total de transacciones de venta registradas.

#### Response `200 OK`

```json
{
  "total_sales": 1
}
```

---

### 🔹 Total de ingresos

**`GET`** `/api/reports/total-revenue`

Retorna la suma de todos los ingresos generados por ventas de libros.

#### Response `200 OK`

```json
{
  "total_revenue": 0
}
```

---

### 🔹 Total de préstamos

**`GET`** `/api/reports/total-loans`

Retorna el número total de préstamos realizados en la biblioteca.

#### Response `200 OK`

```json
{
  "total_loans": 2
}
```

---

### 🔹 Libros más prestados

**`GET`** `/api/reports/most-borrowed-books`

Retorna los libros ordenados por cantidad de préstamos, combinando datos del servicio de préstamos y el catálogo de libros.

#### Response `200 OK`

```json
[
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
]
```

---

### 🔹 Total de multas

**`GET`** `/api/reports/total-fines`

Retorna el número total de multas generadas en la biblioteca.

#### Response `200 OK`

```json
{
  "total_fines": 1
}
```

---

### 🔹 Monto total de multas

**`GET`** `/api/reports/total-fines-amount`

Retorna la suma del monto económico de todas las multas registradas.

#### Response `200 OK`

```json
{
  "total_amount": 1740
}
```

---

### 🔹 Usuarios con más multas

**`GET`** `/api/reports/top-users-fines`

Retorna los usuarios ordenados por cantidad de multas acumuladas, útil para identificar patrones de incumplimiento.

#### Response `200 OK`

```json
[
  {
    "user_id": 2,
    "total_fines": 1
  }
]
```

---

## 🗺️ Resumen de endpoints

| Método | Endpoint | Descripción | Servicios consultados |
|---|---|---|---|
| GET | `/api/reports/dashboard` | Resumen general del sistema | Books, Loans, Fines, Sales |
| GET | `/api/reports/most-sold-books` | Libros más vendidos | Books, Sales |
| GET | `/api/reports/total-sales` | Total de ventas | Sales |
| GET | `/api/reports/total-revenue` | Total de ingresos | Sales |
| GET | `/api/reports/total-loans` | Total de préstamos | Loans |
| GET | `/api/reports/most-borrowed-books` | Libros más prestados | Books, Loans |
| GET | `/api/reports/total-fines` | Total de multas | Fines |
| GET | `/api/reports/total-fines-amount` | Monto total de multas | Fines |
| GET | `/api/reports/top-users-fines` | Usuarios con más multas | Fines |

---

## 🧩 Integración con el API Gateway

Este servicio es consumido a través del **API Gateway (Laravel)**, el cual autentica las peticiones antes de redirigirlas.

```
Cliente  ──►  API Gateway (:8080)  ──►  Reports Service (:5001)
```
