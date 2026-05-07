"""
Settings exclusivos para pruebas — reemplaza PostgreSQL con SQLite en memoria.
pytest.ini apunta aquí vía DJANGO_SETTINGS_MODULE = fines_service.settings_test
"""

import os

SECRET_KEY = "test-secret-key-no-usar-en-produccion"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "fines",
]

# Solo el middleware de autenticación interna; el resto no aplica en tests
MIDDLEWARE = [
    "fines.middleware.InternalAPIKeyMiddleware",
]

ROOT_URLCONF = "fines_service.urls"

# SQLite en memoria: no requiere PostgreSQL ni variables de entorno
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Clave interna fija para los tests
os.environ.setdefault("INTERNAL_API_KEY", "test-key-fines")