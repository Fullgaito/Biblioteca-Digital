import requests
import os

def get_sales():
    headers={
        "X-Internal-API-Key": os.getenv("INTERNAL_API_KEY")
    }
    sales_base_url = os.getenv('SALES_SERVICE_URL', os.getenv('SALES_URL'))
    response=requests.get(f"{sales_base_url}/sales", headers=headers)
    return response.json().get('data', []) if response.status_code == 200 else []