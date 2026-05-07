import pytest


@pytest.fixture(scope="session")
def django_db_setup(django_test_environment, django_db_blocker):
    """
    Reemplaza el fixture por defecto de pytest-django para crear las tablas
    con syncdb en lugar de depender de migraciones previas.

    scope='session' -> las tablas se crean una vez para toda la sesion;
    cada test con @pytest.mark.django_db obtiene su propio rollback.
    """
    from django.core.management import call_command

    with django_db_blocker.unblock():
        call_command("migrate", "--run-syncdb", verbosity=0)