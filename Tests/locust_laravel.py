from locust import HttpUser, task, between
from random import randint, choice

class BibliotecaUser(HttpUser):

    wait_time = between(1, 3)

    # 🔑 Lista de tokens (5 usuarios distintos)
    TOKENS = [
        "3|3WZ124uJDjkZOW73lFHJcRiGmiED8rs2sn6Cks1Kf26ac008",
        "2|9MZKgVk3A9dTcjj4nlpcYr9dtcL9Af7CradMvoh3a71f3ab0",
        "4|lbRKUCvl2cTRAhGsmVnKP4HGs9xjYQwK3KMW66im610bc78e",
        "5|ax4HAXvlku6Ng4l6Fqtsr1l3ivITUEE9X1nii7sV6c3f8fba",
    ]

    def on_start(self):
        # 🎯 Cada usuario toma un token aleatorio
        self.token = choice(self.TOKENS)

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    # 🔹 GET - Obtener todos los libros
    @task(3)
    def get_books(self):
        self.client.get("/api/books", headers=self.get_headers())

    # 🔹 GET - Obtener libro específico
    @task(2)
    def get_book_by_id(self):
        book_id = randint(1, 20)
        self.client.get(f"/api/books/{book_id}", headers=self.get_headers())

    # 🔹 POST - Crear libro (para poblar BD)
    @task(1)
    def create_book(self):
        data = {
            "title": f"Libro Test {randint(1, 1000)}",
            "author": "Autor Test",
            "isbn": f"{randint(100000,999999)}",
            "description": "Libro generado por prueba de carga",
            "category_id": 1,
            "available": True
        }
        self.client.post("/api/books", json=data, headers=self.get_headers())

    # 🔹 PUT - Actualizar libro
    @task(1)
    def update_book(self):
        book_id = randint(1, 20)
        data = {
            "title": f"Libro Actualizado {randint(1, 1000)}",
            "author": "Autor Actualizado"
        }
        self.client.put(f"/api/books/{book_id}", json=data, headers=self.get_headers())

    # 🔹 DELETE - Eliminar libro
    @task(1)
    def delete_book(self):
        book_id = randint(1, 20)
        self.client.delete(f"/api/books/{book_id}", headers=self.get_headers())

    # 🔹 GET - Préstamos
    @task(2)
    def get_loans(self):
        self.client.get("/api/loans", headers=self.get_headers())

    # 🔹 GET - Multas
    @task(1)
    def get_fines(self):
        self.client.get("/api/fines", headers=self.get_headers())

    # 🔹 GET - Reportes
    @task(1)
    def get_reports(self):
        self.client.get("/api/reports/dashboard", headers=self.get_headers())

    # 🔹 GET - Perfil usuario
    @task(1)
    def get_profile(self):
        self.client.get("/api/me", headers=self.get_headers())