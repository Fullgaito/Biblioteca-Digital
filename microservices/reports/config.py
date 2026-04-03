import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    LOANS_URL = os.getenv('LOANS_URL')
    FINES_URL = os.getenv('FINES_URL')
    SALES_URL = os.getenv('SALES_URL')
    INTERNAL_API_KEY = os.getenv('INTERNAL_API_KEY')
    