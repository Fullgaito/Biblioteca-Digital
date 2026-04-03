from flask import Flask
from routes import reports_bp
from dotenv import load_dotenv
from config import Config
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cargar config
    app.config.from_object(Config)

    # Inicializar DB
    db.init_app(app)

    # Registrar rutas
    app.register_blueprint(reports_bp)

    return app


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()  # solo si luego agregas modelos

    app.run(port=5005, debug=True)