import requests
import os

def get_book_by_id(book_id):
    headers={
        "X-Internal-API-Key": os.getenv("INTERNAL_API_KEY")
    }
    books_base_url = os.getenv('BOOKS_SERVICE_URL', os.getenv('BOOKS_URL'))
    response=requests.get(f"{books_base_url}/books/{book_id}", headers=headers)
    return response.json() if response.status_code == 200 else None