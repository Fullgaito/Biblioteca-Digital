import pytest
from decimal import Decimal


@pytest.fixture
def client():
    from django.test import Client
    return Client()


@pytest.fixture
def auth_headers():
    return {"HTTP_X_INTERNAL_API_KEY": "test-key-fines"}


@pytest.fixture
def multa_en_bd(db, client, auth_headers):
    r = client.post(
        "/fines",
        data={"user_id": 1, "loan_id": "loan-abc", "days_late": 3},
        content_type="application/json",
        **auth_headers,
    )
    assert r.status_code == 201
    return r.json()["id"]


@pytest.mark.django_db
def test_monto_calculado_correctamente(client, auth_headers):
    r = client.post(
        "/fines",
        data={"user_id": 2, "loan_id": "loan-002", "days_late": 4},
        content_type="application/json",
        **auth_headers,
    )
    assert r.status_code == 201
    fine_id = r.json()["id"]
    detalle = client.get(f"/fines/{fine_id}", **auth_headers)
    body = detalle.json()
    assert Decimal(str(body["amount"])) == Decimal("2320.00")


@pytest.mark.django_db
def test_pagar_multa_retorna_200(client, auth_headers, multa_en_bd):
    r = client.put(f"/fines/{multa_en_bd}/pay", **auth_headers)
    assert r.status_code == 200


@pytest.mark.django_db
def test_pagar_multa_cambia_estado_a_paid(client, auth_headers, multa_en_bd):
    client.put(f"/fines/{multa_en_bd}/pay", **auth_headers)
    detalle = client.get(f"/fines/{multa_en_bd}", **auth_headers)
    body = detalle.json()
    assert body["status"] == "paid"