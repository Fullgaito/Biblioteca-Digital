# Pruebas de Carga - Biblioteca Digital

## Inicio Rápido

### 1. Inicia el API Gateway
```bash
cd ../api-gateway
php artisan serve
```

### 2. Ejecuta Locust con GUI
```bash
locust -f locust_laravel.py --host=http://127.0.0.1:8000
```

### 3. Abre el navegador
Ve a `http://127.0.0.1:8089` y configura:
- **Number of users**: Cantidad de usuarios simultáneos
- **Spawn rate**: Usuarios creados por segundo
- Luego presiona "Start swarming"

## Endpoints Probados

- Autenticación: `/api/register`, `/api/login`
- Libros: `/api/books`, `/api/books/{id}`
- Ventas: `/api/sales`
- Préstamos: `/api/loans`, `/api/loans/user/{id}`
- Multas: `/api/fines`, `/api/fines/user/{id}`
- Reportes: `/api/reports/*`
- Perfil: `/api/me`
