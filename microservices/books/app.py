import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db

app= Flask(__name__)
app.config.from_object(Config)

# Log para validar la configuración de base de datos
print(f"DEBUG: SQLALCHEMY_DATABASE_URI is {app.config.get('SQLALCHEMY_DATABASE_URI')}")
print(f"DEBUG: DB_HOST is {os.getenv('DB_HOST')}")

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

import models
import routes

routes.register_routes(app)

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)