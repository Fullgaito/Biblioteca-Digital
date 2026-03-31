from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255), nullable=False)
    author      = db.Column(db.String(255), nullable=False)
    isbn        = db.Column(db.String(20), unique=True, nullable=True)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.String(50), nullable=True)   # referencia al servicio Categorías
    available   = db.Column(db.Boolean, default=True, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime)
    updated_at  = db.Column(db.DateTime, default=datetime, onupdate=datetime)

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'author':      self.author,
            'isbn':        self.isbn,
            'description': self.description,
            'category_id': self.category_id,
            'available':   self.available,
            'created_at':  self.created_at.isoformat(),
            'updated_at':  self.updated_at.isoformat(),
        }