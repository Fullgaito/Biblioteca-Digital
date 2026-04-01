from flask import jsonify, request
from models import Book, db
from functools import wraps
import os
internal_api_key = os.getenv('INTERNAL_API_KEY')

def requiere_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-Internal-API-Key')
        internal_api_key = os.getenv('INTERNAL_API_KEY')  

        print("HEADER:", api_key)
        print("ENV:", internal_api_key)

        if not api_key or api_key != internal_api_key:
            return jsonify({'error': 'Unauthorized'}), 401

        return f(*args, **kwargs)
    return decorated

def register_routes(app):
    @app.route('/books', methods=['GET'])
    @requiere_token
    def get_books():
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books]), 200

    @app.route('/books/<int:id>', methods=['GET'])
    @requiere_token
    def get_book(id):
        book = Book.query.get_or_404(id)
        return jsonify(book.to_dict()), 200
    
    @app.route('/books', methods=['POST'])
    @requiere_token
    def create_book():
        data = request.get_json()

        if not data or 'title' not in data or 'author' not in data:
            return jsonify({'error': 'Title and author are required'}), 400
        book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),
            description=data.get('description'),
            category=data.get('category'),
            available=data.get('available', True),
            quantity=data.get('quantity', 1)
        )
        db.session.add(book)
        db.session.commit()
        return jsonify(book.to_dict()), 201
    
    @app.route('/books/<int:id>', methods=['PUT'])
    @requiere_token
    def update_book(id):
        book = Book.query.get_or_404(id)
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.isbn = data.get('isbn', book.isbn)
        book.description = data.get('description', book.description)
        book.category = data.get('category', book.category)
        book.available = data.get('available', book.available)
        book.quantity = data.get('quantity', book.quantity)

        db.session.commit()
        return jsonify(book.to_dict()), 200
    @app.route('/books/<int:id>', methods=['DELETE'])
    @requiere_token
    def delete_book(id):
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': f'Book {id} deleted'}), 200