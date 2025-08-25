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
    try:
        response = requests.get(f"{API_URL}/products/featured")
        response.raise_for_status() # Lanza una excepción para errores de HTTP (4xx o 5xx)
        products = response.json()
        return render_template('index.html', products=products)
    except requests.exceptions.RequestException as e:
        flash(f"Error al conectar con la API: {e}", "danger")
        return render_template('index.html', products=[])

@app.route('/products')
def products():
    # TODO: Implementar página de productos
    # Obtener lista de productos de la API
    try:
        response = requests.get(f"{API_URL}/products")
        response.raise_for_status()
        products = response.json()
        return render_template('products.html', products=products)
    except requests.exceptions.RequestException as e:
        flash(f"Error al conectar con la API: {e}", "danger")
        return render_template('products.html', products=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: Implementar lógica de login
        # Enviar datos a la API de autenticación
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
        try:
            response = api_request('auth/login', 'POST', {'email': email, 'password': password})
            if response and response.status_code == 200:
                session['user_id'] = response.json().get('user_id')
                session['username'] = response.json().get('username')
                flash("Has iniciado sesión correctamente.", "success")
                return redirect(url_for('index'))
            else:
                flash("Credenciales inválidas. Por favor, inténtalo de nuevo.", "danger")
        except requests.exceptions.RequestException:
            flash("No se pudo conectar con el servicio de autenticación.", "danger")
    return render_template('login.html')
      

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO: Implementar lógica de registro
        # Enviar datos a la API de registro
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            response = api_request('auth/register', 'POST', {'email': email, 'password': password})
            if response and response.status_code == 201:
                flash("Registro exitoso. ¡Ahora puedes iniciar sesión!", "success")
                return redirect(url_for('login'))
            else:
                flash("Error al registrarse. El usuario ya podría existir.", "danger")
        except requests.exceptions.RequestException:
            flash("No se pudo conectar con el servicio de registro.", "danger")
    return render_template('register.html')

@app.route('/cart')
def cart():
    # TODO: Implementar página del carrito
    # Obtener carrito del usuario de la API
    if not is_logged_in():
        flash("Por favor, inicia sesión para ver tu carrito.", "info")
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    try:
        response = api_request(f'cart/{user_id}')
        if response and response.status_code == 200:
            cart_items = response.json()
            return render_template('cart.html', cart_items=cart_items)
        else:
            flash("Error al cargar el carrito. Puede que esté vacío.", "info")
            return render_template('cart.html', cart_items=[])
    except requests.exceptions.RequestException:
        flash("No se pudo conectar con el servicio del carrito.", "danger")
        return render_template('cart.html', cart_items=[])

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # TODO: Implementar agregar producto al carrito
    # Enviar request a la API
    if not is_logged_in():
        flash("Debes iniciar sesión para agregar productos al carrito.", "info")
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    try:
        response = api_request(f'cart/{user_id}/add', 'POST', {'product_id': product_id})
        if response and response.status_code == 200:
            flash("Producto agregado al carrito exitosamente.", "success")
        else:
            flash("No se pudo agregar el producto al carrito.", "danger")
    except requests.exceptions.RequestException:
        flash("Error al conectar con el servicio del carrito.", "danger")
    
    return redirect(url_for('products'))

@app.route('/logout')
def logout():
    # TODO: Implementar logout
    # Limpiar sesión
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for('index'))

# TODO: Función helper para hacer requests a la API
def api_request(endpoint, method='GET', data=None):
    # TODO: Implementar función para hacer requests a la API
    full_url = f"{API_URL}/{endpoint}"
    try:
        if method == 'POST':
            response = requests.post(full_url, json=data)
        elif method == 'GET':
            response = requests.get(full_url)
        # Puedes añadir otros métodos HTTP aquí si los necesitas
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición a la API: {e}")
        return None

# TODO: Función para verificar si el usuario está logueado
def is_logged_in():
    # TODO: Verificar si hay sesión activa
    return 'user_id' in session

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)