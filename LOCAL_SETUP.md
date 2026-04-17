# Setup local (dev) — Biblioteca Digital

Este documento resume el arranque **en local** del API Gateway y microservicios, usando la misma `INTERNAL_API_KEY` en todos.

## Puertos (por defecto)
- **API Gateway (Laravel)**: `http://localhost:8000`
- **Books (Flask)**: `http://localhost:5000`
- **Loans (Node/Express)**: `http://localhost:3002`
- **Fines (Django/DRF)**: `http://localhost:8001`
- **Sales (Node/Express + Firebase)**: `http://localhost:3001`
- **Reports (Flask)**: `http://localhost:5001`

## Variables de entorno (mínimas)

### Valor compartido
- `INTERNAL_API_KEY`: **debe ser idéntica** en gateway + todos los microservicios (se envía como `X-Internal-API-Key`).

### Archivos de ejemplo
- `api-gateway/.env.example`
- `microservices/books/.env.example`
- `microservices/loans/.env.example`
- `microservices/fines/fines_service/.env.example`
- `microservices/sales/.env.example`
- `microservices/reports/.env.example`

## Orden de arranque recomendado
1. Bases de datos (MySQL, MongoDB, PostgreSQL) y Firebase RTDB configurado.
2. **Books** (Flask)
3. **Fines** (Django)
4. **Loans** (Node)
5. **Sales** (Node) + `serviceAccountKey.json`
6. **Reports** (Flask)
7. **API Gateway** (Laravel)

## Smoke test rápido (vía gateway)
1) Registrar usuario:

```bash
curl -X POST http://localhost:8000/api/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test@test.com\",\"password\":\"12345678\",\"password_confirmation\":\"12345678\",\"cuestion\":\"color favorito\",\"answer\":\"azul\"}"
```

2) Login:

```bash
curl -X POST http://localhost:8000/api/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@test.com\",\"password\":\"12345678\"}"
```

3) Listar libros (requiere token):

```bash
curl http://localhost:8000/api/books ^
  -H "Authorization: Bearer <TOKEN>"
```

4) Dashboard de reportes:

```bash
curl http://localhost:8000/api/reports/dashboard ^
  -H "Authorization: Bearer <TOKEN>"
```

