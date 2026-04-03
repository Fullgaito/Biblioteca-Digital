from flask import jsonify, request
from functools import wraps
import os

# Loans
from reports.loans_reports import most_borrowed_books, total_loans

# Fines
from reports.fines_reports import users_with_most_fines, total_fines, total_fines_amount

# Sales
from reports.sales_reports import most_sold_books, total_sales, total_revenue

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
    #Loans
    @app.route('/api/reports/most_borrowed_books', methods=['GET'])
    @requiere_token
    def get_most_borrowed_books():
        return jsonify(most_borrowed_books())
    
    @app.route('/api/reports/total_loans', methods=['GET'])
    @requiere_token
    def get_total_loans():
        return jsonify(total_loans())
    
    #Fines
    @app.route('/api/reports/top-users-fines', methods=['GET'])
    @requiere_token
    def get_top_users_fines():
        return jsonify(users_with_most_fines())
    
    @app.route('/api/reports/total_fines', methods=['GET'])
    @requiere_token
    def get_total_fines():
        return jsonify(total_fines())
    @app.route('/api/reports/total-fines-amount', methods=['GET'])
    @requiere_token
    def get_total_fines_amount():
        return jsonify(total_fines_amount())
    
    #Sales
    @app.route('/api/reports/most-sold-books', methods=['GET'])
    @requiere_token
    def get_most_sold_books():
        return jsonify(most_sold_books())
    @app.route('/api/reports/total-sales', methods=['GET'])
    @requiere_token
    def get_total_sales():
        return jsonify(total_sales())
    @app.route('/api/reports/total-revenue', methods=['GET'])
    @requiere_token
    def get_total_revenue():
        return jsonify(total_revenue())
    
    #Tipo dashboard general
    @app.route('/api/reports/dashboard', methods=['GET'])
    def get_dashboard():
        return jsonify({
            "loans": {
                "top books": most_borrowed_books(),
                "total": total_loans()
            },
            "fines": {
                "top users": users_with_most_fines(),
                "total": total_fines(),
                "total amount": total_fines_amount()
            },
            "sales": {
                "top books": most_sold_books(),
                "total": total_sales(),
                "revenue": total_revenue() #muestra el total de ingresos generados por las ventas de libros
            }

        })