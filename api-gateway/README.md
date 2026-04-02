# 📚 Biblioteca Digital - Servicio de Autenticación (Laravel) y api gateway

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
  "quantity": 30
}
```

#### 📤 Response

```json
{
  "author": "Gabriel García Márquez",
  "available": true,
  "category": "Realismo Mágico",
  "description": "La épica historia de la familia Buendía en el remoto pueblo de Macondo, donde lo fantástico y lo real convergen en una narrativa maestra.",
  "id": 3,
  "isbn": "978-0307474728",
  "quantity": 30,
  "title": "Cien años de soledad"
}
```

---

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
    "title": "Cien años de soledad"
  },
  {
    "author": "Antoine de Saint-Exupéry",
    "available": true,
    "category": "infantil",
    "description": "Historia filosófica sobre la vida y la amistad",
    "id": 2,
    "isbn": "9780156012195",
    "quantity": 10,
    "title": "El principito"
  },
  {
    "author": "Gabriel García Márquez",
    "available": true,
    "category": "Realismo Mágico",
    "description": "La épica historia de la familia Buendía en el remoto pueblo de Macondo, donde lo fantástico y lo real convergen en una narrativa maestra.",
    "id": 3,
    "isbn": "978-0307474728",
    "quantity": 30,
    "title": "Cien años de soledad"
  }
]
```

---

### 🔹 Obtener Libro

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
  "quantity": 10,
  "title": "El principito"
}
```

---

### 🔹 Actualización de un libro

**PUT** `/api/books/{id}`

Permite la actualización de la información correspondiente de un libro en especifico indicando el id correspondiente

#### 📥 Request

```json
{
  "title": "Cien años de soledad",
  "author": "Gabriel García Márquez",
  "isbn": "978-0307474728",
  "description": "La épica historia de la familia Buendía en el remoto pueblo de Macondo, donde lo fantástico y lo real convergen en una narrativa maestra.",
  "available": true,
  "category": "Novela",
  "quantity": 30
}
```

#### 📤 Response

```json
{
  "author": "Gabriel García Márquez",
  "available": true,
  "category": "Novela",
  "description": "La épica historia de la familia Buendía en el remoto pueblo de Macondo, donde lo fantástico y lo real convergen en una narrativa maestra.",
  "id": 3,
  "isbn": "978-0307474728",
  "quantity": 30,
  "title": "Cien años de soledad"
}
```

---

### 🔹 Eliminación de un libro

**DELETE** `/api/books/{id}`

Permite la eliminación definitiva de un libro ya creado con su id correspondiente


#### 📤 Response

```json
{
  "message": "Book 3 deleted"
}
```

---

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

#### 📤 Response

```json
{
  "message": "Loan created successfully",
  "id": "69cdc5fa291d7ccc67c54308"
}
```

---

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
  },
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

---

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

---

### 🔹 Obtener los prestamos por id de usuario

**GET** `/api/loans/user/1`

Permite obtener la información asociada a un prestamo por usuario


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

---

### 🔹 Retorno de un prestamo

**PUT** `/api/loans/69cd46cbcc9b4262db9cde2f/return`

Permite registrar de forma oportuna cuando se realiza la entrega de un prestamo de un libro


#### 📤 Response

```json
{
  "message": "Book returned successfully",
  "loan": {
    "_id": "69cd46cbcc9b4262db9cde2f",
    "book_id": 1,
    "user_id": 1,
    "status": "returned",
    "loan_date": "2026-04-01T16:24:43.398Z",
    "__v": 0,
    "return_date": "2026-04-02T02:56:21.660Z"
  },
  "fine_created": false
}
```

---

## 🧠 Arquitectura

Este servicio forma parte de una arquitectura basada en **microservicios**, donde:

* Laravel gestiona la autenticación
* Laravel funciona como un api gateway para la comunicación con los demás microservicios
* La comunicación se realiza mediante APIs REST

---

## ⚠️ Notas importantes

* El token debe enviarse en cada petición protegida
* Las contraseñas se almacenan encriptadas
* El sistema utiliza autenticación basada en tokens (Bearer)

---

## 📌 Autor

Sergio Alejandro Gaitan Quintero