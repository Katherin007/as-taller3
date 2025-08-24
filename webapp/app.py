from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
from datetime import datetime

# TODO: Configurar la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave-por-defecto-cambiar')

# TODO: Configurar la URL de la API
API_URL = os.getenv('API_URL', 'http://api:8000')

@app.route('/')
def index():
    # TODO: Implementar página principal
    # Obtener productos destacados de la API
    return render_template('index.html')

@app.route('/products')
def products():
    # TODO: Implementar página de productos
    # Obtener lista de productos de la API
    return render_template('products.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: Implementar lógica de login
        # Enviar datos a la API de autenticación
        pass
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO: Implementar lógica de registro
        # Enviar datos a la API de registro
        pass
    return render_template('register.html')

@app.route('/cart')
def cart():
    # TODO: Implementar página del carrito
    # Obtener carrito del usuario de la API
    return render_template('cart.html')

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # TODO: Implementar agregar producto al carrito
    # Enviar request a la API
    pass

@app.route('/logout')
def logout():
    # TODO: Implementar logout
    # Limpiar sesión
    pass

# TODO: Función helper para hacer requests a la API
def api_request(endpoint, method='GET', data=None, headers=None):
    # TODO: Implementar función para hacer requests a la API
    pass

# TODO: Función para verificar si el usuario está logueado
def is_logged_in():
    # TODO: Verificar si hay sesión activa
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)