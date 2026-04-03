import requests
import os

def get_book_by_id(book_id):
    headers={
        "X-Internal-API-Key": os.getenv("INTERNAL_API_KEY")
    }
    response=requests.get(f"{os.getenv('BOOKS_URL')}/books/{book_id}", headers=headers)
    return response.json() if response.status_code == 200 else None