import requests
import os

def get_fines():
    headers={
        "X-Internal-API-Key": os.getenv("INTERNAL_API_KEY")
    }
    response=requests.get(f"{os.getenv('FINES_URL')}/fines", headers=headers)
    if response.status_code != 200:
        return []

    data = response.json()
    if isinstance(data, dict):
        return data.get('data', [])
    if isinstance(data, list):
        return data
    return []