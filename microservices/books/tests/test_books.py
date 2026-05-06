"""
Las pruebas usan una BD SQLite en memoria para no depender
de MySQL ni de variables de entorno externas.
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pytest
from flask import Flask
from models import db, Book
from routes import register_routes


# ─── Fixture: app y cliente de prueba ─────────────────────────────────────────

@pytest.fixture
def app():
    """
    Crea una instancia de Flask completamente aislada para cada prueba.
    - BD SQLite en memoria → no requiere MySQL ni .env
    - INTERNAL_API_KEY fija para no depender del entorno
    - Crea y destruye las tablas en cada test
    """
    _app = Flask(__name__)
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Clave interna fija para las pruebas
    import os
    os.environ["INTERNAL_API_KEY"] = "test-key-123"

    db.init_app(_app)
    register_routes(_app)

    with _app.app_context():
        db.create_all()
        yield _app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Cabeceras con la clave interna válida."""
    return {"X-Internal-API-Key": "test-key-123"}


@pytest.fixture
def libro_en_bd(app, auth_headers, client):
    """
    Inserta un libro de ejemplo y devuelve su diccionario.
    Útil para pruebas que necesitan un libro existente.
    """
    payload = {
        "title":       "Cien años de soledad",
        "author":      "Gabriel García Márquez",
        "isbn":        "978-0-06-088328-7",
        "description": "Novela del realismo mágico",
        "category":    "Ficción",
        "available":   True,
        "quantity":    5,
        "unit_price":  35000.0,
    }
    r = client.post("/books", json=payload, headers=auth_headers)
    return r.get_json()


#Pruebas unitarias para ms-books
def test_crear_libro_retorna_201(client, auth_headers):
        payload = {
            "title":      "El principito",
            "author":     "Antoine de Saint-Exupéry",
            "unit_price": 20000.0,
        }
        response = client.post("/books", json=payload, headers=auth_headers)

        assert response.status_code == 201

def test_decrementar_stock_insuficiente_retorna_400(client, auth_headers, libro_en_bd):
        book_id = libro_en_bd["id"]   # tiene quantity=5

        # Intentar restar más de lo que hay
        response = client.put(
            f"/books/{book_id}/decrement",
            json={"quantity": 10},
            headers=auth_headers,
        )
        body = response.get_json()

        assert response.status_code == 400
        assert "error" in body

def test_crear_libro_sin_title_retorna_400(client, auth_headers):
        payload = {"author": "Autor sin título", "unit_price": 10000.0}
        response = client.post("/books", json=payload, headers=auth_headers)

        assert response.status_code == 400