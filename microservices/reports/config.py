import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    BOOKS_SERVICE_URL = os.getenv('BOOKS_SERVICE_URL', os.getenv('BOOKS_URL'))
    LOANS_SERVICE_URL = os.getenv('LOANS_SERVICE_URL', os.getenv('LOANS_URL'))
    FINES_SERVICE_URL = os.getenv('FINES_SERVICE_URL', os.getenv('FINES_URL'))
    SALES_SERVICE_URL = os.getenv('SALES_SERVICE_URL', os.getenv('SALES_URL'))
    INTERNAL_API_KEY = os.getenv('INTERNAL_API_KEY')
    