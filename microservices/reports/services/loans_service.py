import requests
import os

def get_loans():
    headers={
        "X-Internal-API-Key": os.getenv("INTERNAL_API_KEY")
    }
    loans_base_url = os.getenv('LOANS_SERVICE_URL', os.getenv('LOANS_URL'))
    response=requests.get(f"{loans_base_url}/loans", headers=headers)
    if response.status_code != 200:
        return []

    data = response.json()
    if isinstance(data, dict):
        return data.get('data', [])
    if isinstance(data, list):
        return data
    return []