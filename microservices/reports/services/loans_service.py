import requests
import os

def get_loans():
    headers={
        "X-Internal-API-Key": os.getenv("INTERNAL_API_KEY")
    }
    response=requests.get(f"{os.getenv('LOANS_URL')}/loans", headers=headers)
    if response.status_code != 200:
        return []

    data = response.json()
    if isinstance(data, dict):
        return data.get('data', [])
    if isinstance(data, list):
        return data
    return []