from django.test import TestCase,Client
from decimal import Decimal
# Create your tests here.
class FinesAPITests(TestCase):
    def setUp(self):
        """
        setUp se ejecuta automáticamente ANTES de cada prueba.
        Aquí preparamos el cliente, los headers y datos base.
        """
        self.client = Client()
        self.auth_headers = {"HTTP_X_INTERNAL_API_KEY": "test-key-fines"}
        
        # OJO AQUÍ: Hemos añadido el slash final ('/fines/')
        response = self.client.post(
            "/fines/", 
            data={"user_id": 1, "loan_id": "loan-abc", "days_late": 3},
            content_type="application/json",
            **self.auth_headers,
        )
        
        # 💡 TRUCO DE DEBUG: Si la petición falla, imprimimos el error real del servidor
        if response.status_code != 201:
            print(f"\n--- ERROR EN SETUP ---")
            print(f"Status Code: {response.status_code}")
            print(f"Respuesta del servidor: {response.content.decode('utf-8')}")
            print(f"----------------------\n")
            
        # Guardamos el ID para usarlo en las otras pruebas
        self.multa_en_bd = response.json()["id"]

    def test_monto_calculado_correctamente(self):
        """El monto debe ser days_late × 580 según la lógica de views.py."""
        r = self.client.post(
            "/fines",
            data={"user_id": 2, "loan_id": "loan-002", "days_late": 4},
            content_type="application/json",
            **self.auth_headers,
        )
        self.assertEqual(r.status_code, 201) # En TestCase usamos self.assertEqual en vez de assert

        # Verificar el monto consultando la multa recién creada
        fine_id = r.json()["id"]
        detalle = self.client.get(f"/fines/{fine_id}", **self.auth_headers)
        body = detalle.json()
        
        self.assertEqual(Decimal(str(body["amount"])), Decimal("2320.00"))  # 4 × 580

    def test_pagar_multa_retorna_200(self):
        r = self.client.put(f"/fines/{self.multa_en_bd}/pay", **self.auth_headers)
        self.assertEqual(r.status_code, 200)

    def test_pagar_multa_cambia_estado_a_paid(self):
        # 1. Ejecutamos la acción de pagar
        self.client.put(f"/fines/{self.multa_en_bd}/pay", **self.auth_headers)

        # 2. Consultamos el estado actual
        detalle = self.client.get(f"/fines/{self.multa_en_bd}", **self.auth_headers)
        body = detalle.json()
        
        # 3. Verificamos que el estado cambió
        self.assertEqual(body["status"], "paid")