from locust import HttpUser, task, between
from random import randint, choice

class BibliotecaUser(HttpUser):

    wait_time = between(1, 3)

    # Lista de tokens (5 usuarios distintos)
    TOKENS = [
        "3|3WZ124uJDjkZOW73lFHJcRiGmiED8rs2sn6Cks1Kf26ac008",
        "2|9MZKgVk3A9dTcjj4nlpcYr9dtcL9Af7CradMvoh3a71f3ab0",
        "4|lbRKUCvl2cTRAhGsmVnKP4HGs9xjYQwK3KMW66im610bc78e",
        "5|ax4HAXvlku6Ng4l6Fqtsr1l3ivITUEE9X1nii7sV6c3f8fba",
    ]

    created_book_ids = []

    def on_start(self):
        #Cada usuario toma un token aleatorio
        self.token = choice(self.TOKENS)

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    # GET - Obtener todos los libros
    @task(3)
    def get_books(self):
        self.client.get("/api/books", headers=self.get_headers())

    # GET - Obtener libro específico
    @task(2)
    def get_book_by_id(self):
        if not self.created_book_ids:
            return  # No hay libros creados para obtener
        book_id = choice(self.created_book_ids)
        self.client.get(f"/api/books/{book_id}", headers=self.get_headers())

    # POST - Crear libro (para poblar BD)
    @task(1)
    def create_book(self):
        data = {
            "title": f"Libro Test {randint(1, 1000)}",
            "author": "Autor Test",
            "isbn": f"{randint(100000,999999)}",
            "description": "Libro generado por prueba de carga",
            "category": "Ficción",
            "available": True,
            "unit_price": randint(10000, 70000)
        }
        response = self.client.post("/api/books", json=data, headers=self.get_headers())
        if response.status_code in [200, 201]:
            try:
                book = response.json().get('data', response.json())
                book_id = book.get('id') if isinstance(book, dict) else None
                if book_id and book_id not in self.created_book_ids:
                    self.created_book_ids.append(book_id)
            except Exception:
                pass

    # PUT - Actualizar libro
    @task(1)
    def update_book(self):
        if not self.created_book_ids:
            return  # No hay libros creados para actualizar
        book_id = choice(self.created_book_ids)
        data = {
            "title": f"Libro Actualizado {randint(1, 1000)}",
            "author": "Autor Actualizado"
        }
        self.client.put(f"/api/books/{book_id}", json=data, headers=self.get_headers())

    # DELETE - Eliminar libro
    @task(1)
    def delete_book(self):
        if not self.created_book_ids:
            return  # No hay libros creados para eliminar
        
        book_id = choice(self.created_book_ids)
        response = self.client.delete(f"/api/books/{book_id}", headers=self.get_headers())
        if response.status_code in [200, 204]:  # Si se eliminó correctamente
            if book_id in self.created_book_ids:
                self.created_book_ids.remove(book_id)
        

    # GET - Préstamos
    @task(1)
    def get_loans(self):
        self.client.get("/api/loans", headers=self.get_headers())

    # GET - Multas
    @task(1)
    def get_fines(self):
        self.client.get("/api/fines", headers=self.get_headers())

    # GET - Reportes
    @task(1)
    def get_reports(self):
        self.client.get("/api/reports/dashboard", headers=self.get_headers())

    # GET - Perfil usuario
    @task(1)
    def get_profile(self):
        self.client.get("/api/me", headers=self.get_headers())