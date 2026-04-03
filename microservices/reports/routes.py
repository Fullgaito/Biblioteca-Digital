from flask import jsonify, request
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

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
    @app.route('/reports/loans/most-borrowed-books', methods=['GET'])
    @requiere_token
    def get_most_borrowed_books(): #muestra los libros más prestados, ordenados por cantidad de préstamos
        return jsonify(most_borrowed_books())
    
    @app.route('/reports/loans/total-loans', methods=['GET'])
    @requiere_token
    def get_total_loans(): #muestra el total de préstamos realizados en la biblioteca, lo que puede ayudar a evaluar la popularidad general de los servicios de préstamo y la demanda de libros.
        return jsonify(total_loans())
    
    #Fines
    @app.route('/reports/fines/top-users-fines', methods=['GET'])
    @requiere_token
    def get_top_users_fines(): #muestra los usuarios con más multas, ordenados por cantidad de multas o monto total de multas, lo que puede ayudar a identificar a los usuarios que tienen un historial de incumplimiento en la devolución de libros o el pago de multas.
        return jsonify(users_with_most_fines())
    
    @app.route('/reports/fines/total-fines', methods=['GET'])
    @requiere_token
    def get_total_fines(): #muestra el total de multas generadas en la biblioteca, lo que puede ayudar a evaluar la efectividad de las políticas de sanción y el comportamiento de los usuarios.

        return jsonify(total_fines())
    @app.route('/reports/fines/total-fines-amount', methods=['GET'])
    @requiere_token
    def get_total_fines_amount(): #muestra el monto total de multas generadas en la biblioteca, lo que puede ayudar a evaluar el impacto financiero de las multas y la efectividad de las políticas de sanción.
        return jsonify(total_fines_amount())
    
    #Sales
    @app.route('/reports/sales/most-sold-books', methods=['GET'])
    @requiere_token
    def get_most_sold_books(): #muestra los libros más vendidos, ordenados por cantidad de ventas, lo que puede ayudar a identificar las tendencias de compra y los títulos más populares entre los clientes.
        return jsonify(most_sold_books())
    @app.route('/reports/sales/total-sales', methods=['GET'])
    @requiere_token
    def get_total_sales(): #muestra el total de ventas realizadas en la librería, lo que puede ayudar a evaluar el rendimiento general del negocio y la demanda de libros.
        return jsonify(total_sales())
    @app.route('/reports/sales/total-revenue', methods=['GET'])
    @requiere_token
    def get_total_revenue(): #muestra el total de ingresos generados por las ventas de libros, lo que puede ayudar a evaluar la rentabilidad del negocio y la efectividad de las estrategias de precios y marketing.
        return jsonify(total_revenue())
    
    #Tipo dashboard general
    @app.route('/reports/dashboard', methods=['GET'])
    @requiere_token
    def get_dashboard(): #muestra un resumen general de los informes de préstamos, multas y ventas, lo que puede proporcionar una visión rápida del rendimiento de la biblioteca en diferentes áreas y ayudar a identificar áreas de mejora o éxito.
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