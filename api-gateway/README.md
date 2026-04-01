# 📚 Biblioteca Digital - Servicio de Autenticación (Laravel)

Este servicio gestiona la autenticación de usuarios dentro del sistema de biblioteca digital, incluyendo registro, inicio de sesión, cierre de sesión y recuperación de contraseña.

---

## 🚀 Tecnologías utilizadas

* Laravel
* PHP
* MySQL
* Laravel Sanctum (Autenticación con tokens)

---

## 📌 Endpoints disponibles

### 🔹 Registro de usuario

**POST** `/api/register`

Permite crear un nuevo usuario en el sistema.

#### 📥 Request

```json
{
  "name": "Sergio Gaitan",
  "email": "sergio@test.com",
  "password": "12345678",
  "password_confirmation": "12345678",
  "cuestion": "color favorito",
  "answer": "azul"
}
```

#### 📤 Response

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "Sergio Gaitan",
    "email": "sergio@test.com"
  }
}
```

---

### 🔹 Login

**POST** `/api/login`

Permite autenticar un usuario y obtener un token.

#### 📥 Request

```json
{
  "email": "sergio@test.com",
  "password": "12345678"
}
```

#### 📤 Response

```json
{
  "access_token": "TOKEN_GENERADO",
  "token_type": "Bearer"
}
```

---

### 🔹 Obtener usuario autenticado

**GET** `/api/me`

Retorna la información del usuario autenticado.

#### 🔐 Headers

```
Authorization: Bearer TOKEN_GENERADO
```

#### 📤 Response

```json
{
  "id": 1,
  "name": "Sergio Gaitan",
  "email": "sergio@test.com"
}
```

---

### 🔹 Logout

**POST** `/api/logout`

Cierra la sesión del usuario autenticado.

#### 🔐 Headers

```
Authorization: Bearer TOKEN_GENERADO
```

#### 📤 Response

```json
{
  "message": "Cierre de sesión exitoso"
}
```

---

### 🔹 Recuperar contraseña

**POST** `/api/forgot-password`

Permite actualizar la contraseña mediante pregunta de seguridad.

#### 📥 Request

```json
{
  "email": "sergio@test.com",
  "pregunta": "color favorito",
  "respuesta": "azul",
  "new_password": "87654321"
}
```

#### 📤 Response

```json
{
  "message": "Contraseña actualizada correctamente"
}
```

---

## 🧠 Arquitectura

Este servicio forma parte de una arquitectura basada en **microservicios**, donde:

* Laravel gestiona la autenticación
* Otros servicios (como préstamos, libros, multas) consumen el `user_id`
* La comunicación se realiza mediante APIs REST

---

## ⚠️ Notas importantes

* El token debe enviarse en cada petición protegida
* Las contraseñas se almacenan encriptadas
* El sistema utiliza autenticación basada en tokens (Bearer)

---

## 📌 Autor

Sergio Alejandro Gaitan Quintero