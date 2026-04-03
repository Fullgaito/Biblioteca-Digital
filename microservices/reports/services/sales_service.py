import requests
import os

def get_sales():
    headers={
        "X-Internal-API-Key": os.getenv("INTERNAL_API_KEY")
    }
    response=requests.get(f"{os.getenv('SALES_URL')}/sales", headers=headers)
    return response.json().get('data', []) if response.status_code == 200 else []