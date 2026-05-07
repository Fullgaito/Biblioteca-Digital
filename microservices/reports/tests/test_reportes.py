"""
Pruebas unitarias — ms-reports (Flask + PyMongo)
=================================================
Ejecutar desde /microservices/reports/:
    pip install pytest
    pytest tests/test_reports.py -v

Las pruebas NO levantan MongoDB ni llaman a servicios externos.
Cada función de reporte depende de servicios (get_sales, get_fines,
get_loans, get_book_by_id) que se reemplazan con unittest.mock.patch
para devolver datos controlados y deterministas.
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pytest
from flask import Flask
from models import db
from routes import register_routes
from unittest.mock import patch
import os


# ─── Fixture: app y cliente de prueba ─────────────────────────────────────────

@pytest.fixture
def app():
    """
    Instancia Flask mínima con las rutas registradas.
    No inicializa PyMongo porque los servicios externos
    se interceptan con mock antes de que se haga cualquier
    conexión de red.
    """
    _app = Flask(__name__)
    _app.config["TESTING"] = True

    os.environ["INTERNAL_API_KEY"] = "test-key-reports"

    register_routes(_app)
    return _app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers():
    return {"X-Internal-API-Key": "test-key-reports"}

VENTAS_MOCK = [
        {"book_id": 1, "title": "Cien años de soledad", "total_sales": 8},
        {"book_id": 2, "title": "El principito", "total_sales": 5},
        {"book_id": 3, "title": "1984", "total_sales": 10},
]

def test_libros_mas_vendidos(client, auth_headers):
    """Test para /reports/sales/most-sold-books con datos mockeados(simulados)."""
    
    # 1. Mockeamos la respuesta de las ventas
    mock_ventas = [
        {"book_id": 1, "total_sales": 8},
        {"book_id": 2, "total_sales": 5},
        {"book_id": 3, "total_sales": 10},
    ]
    
    # 2. Creamos una pequeña función falsa para simular la respuesta del microservicio de libros
    def mock_get_book(book_id):
        return {"id": book_id, "title": f"Libro Simulado {book_id}", "author": "Autor Mock"}

    # 3. Aplicamos el patch a AMBAS dependencias externas
    with patch("reports.sales_reports.get_sales", return_value=mock_ventas), \
         patch("reports.sales_reports.get_book_by_id", side_effect=mock_get_book):
        
        response = client.get("/reports/sales/most-sold-books", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        
        # El libro con ID 3 tuvo 10 ventas, debe ser el primero
        assert data[2]["book_id"] == 3  
        
        # Verificar que la lista esté ordenada de mayor a menor ventas
        assert data[0]["total_sales"] >= data[1]["total_sales"] >= data[2]["total_sales"]

def test_sin_ventas_retorna_lista_vacia(client, auth_headers):
        with patch("reports.sales_reports.get_sales", return_value=[]):
            r = client.get("/reports/sales/most-sold-books", headers=auth_headers)

        assert r.status_code == 200
        assert r.get_json() == []
def test_total_sales_sin_ventas_retorna_cero( client, auth_headers):
        with patch("reports.sales_reports.get_sales", return_value=[]):
            r = client.get("/reports/sales/total-sales", headers=auth_headers)
        assert r.status_code == 200
        assert r.get_json() == {"total_sales": 0}