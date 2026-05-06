from locust import HttpUser, task, between
from random import randint, choice
import threading

class BibliotecaUser(HttpUser):

    wait_time = between(1, 3)

    TOKENS = [
        "3|3WZ124uJDjkZOW73lFHJcRiGmiED8rs2sn6Cks1Kf26ac008",
        "2|9MZKgVk3A9dTcjj4nlpcYr9dtcL9Af7CradMvoh3a71f3ab0",
        "4|lbRKUCvl2cTRAhGsmVnKP4HGs9xjYQwK3KMW66im610bc78e",
        "5|ax4HAXvlku6Ng4l6Fqtsr1l3ivITUEE9X1nii7sV6c3f8fba",
    ]

    # Lista e instancia — cada usuario tiene la suya propia
    def on_start(self):
        self.token = choice(self.TOKENS)
        self.created_book_ids = []          
        self.created_loan_ids = []
        self.created_fine_ids = []
        self._lock = threading.Lock()       

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    @task(3)
    def get_books(self):
        self.client.get("/api/books", headers=self.get_headers())

    @task(2)
    def get_book_by_id(self):
        with self._lock:
            if not self.created_book_ids:
                return
            book_id = choice(self.created_book_ids)
        self.client.get(f"/api/books/{book_id}", headers=self.get_headers())

    @task(1)
    def create_book(self):
        data = {
            "title": f"Libro Test {randint(1, 1000)}",
            "author": "Autor Test",
            "isbn": f"{randint(100000, 999999)}",
            "description": "Libro generado por prueba de carga",
            "category": "Ficción",
            "available": True,
            "unit_price": randint(10000, 70000)
        }
        response = self.client.post("/api/books", json=data, headers=self.get_headers())
        if response.status_code in [200, 201]:
            try:
                body = response.json()
                book = body.get('data', body)
                book_id = book.get('id') if isinstance(book, dict) else None
                if book_id:
                    with self._lock:
                        if book_id not in self.created_book_ids:
                            self.created_book_ids.append(book_id)
            except Exception:
                pass

    @task(1)
    def create_sale(self):
        with self._lock:
            if not self.created_book_ids:
                return
            book_id = choice(self.created_book_ids)
        
        data = {
            "book_id": book_id,
            "quantity": randint(1, 3),
            "customer_name": "Cliente Locust"
        }
        self.client.post("/api/sales", json=data, headers=self.get_headers())

    @task(1)
    def update_book(self):
        with self._lock:
            if not self.created_book_ids:
                return
            book_id = choice(self.created_book_ids)
        
        data = {
            "title": f"Libro Actualizado {randint(1, 1000)}",
            "author": "Autor Actualizado",
            "isbn": f"{randint(100000, 999999)}",
            "description": "Libro actualizado por prueba de carga",
            "category": "No Ficción",
            "available": False,
            "unit_price": randint(15000, 80000)
        }
        self.client.put(f"/api/books/{book_id}", json=data, headers=self.get_headers())

    @task(1)
    def get_dashboard_reports(self):
        self.client.get("/api/reports/dashboard", headers=self.get_headers())
    
    @task(1)
    def get_total_sales(self):
        self.client.get("/api/reports/total-sales", headers=self.get_headers())

    @task(1)
    def get_most_sold_books_report(self):
        self.client.get("/api/reports/most-sold-books", headers=self.get_headers())

    @task(1)
    def get_profile(self):
        self.client.get("/api/me", headers=self.get_headers())

    @task(1)
    def delete_book(self):
        with self._lock:
            if not self.created_book_ids:
                return
            book_id = choice(self.created_book_ids)
        
        response = self.client.delete(f"/api/books/{book_id}", headers=self.get_headers())
        if response.status_code == 204:
            with self._lock:
                if book_id in self.created_book_ids:
                    self.created_book_ids.remove(book_id)
