import requests
import os

def get_loans():
    headers={
        "X-Internal-API-Key": os.getenv("INTERNAL_API_KEY")
    }
    response=requests.get(f"{os.getenv('LOANS_SERVICE_URL')}/loans", headers=headers)
    return response.json() if response.status_code == 200 else []