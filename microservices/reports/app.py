from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

mongo=PyMongo()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)


    from routes import register_routes
    register_routes(app)
    

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,port=5001)