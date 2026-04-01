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
    category = db.Column(db.String(50), nullable=True)   # referencia al servicio Categorías
    available   = db.Column(db.Boolean, default=True, nullable=False)
    quantity    = db.Column(db.Integer, default=1, nullable=False)  # cantidad total de ejemplares

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'author':      self.author,
            'isbn':        self.isbn,
            'description': self.description,
            'category': self.category,
            'available':   self.available,
            'quantity':    self.quantity
        }