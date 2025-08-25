// TODO: Agregar funcionalidad JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Escucha clics en el botón de "Agregar al Carrito"
    document.querySelectorAll('form[action*="/add-to-cart/"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const productId = this.action.split('/').pop();
            addToCart(productId);
        });
    });
});

// TODO: Función para agregar productos al carrito con AJAX
function addToCart(productId) {
    console.log(`Intentando agregar el producto ${productId} al carrito...`);
    // Usamos 'fetch' para enviar una petición POST a la API
    // El 'window.location.origin' asegura que la URL es absoluta
    fetch(`${window.location.origin}/add-to-cart/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        // Si la respuesta no es exitosa, lanza un error
        return response.json().then(errorData => {
            throw new Error(errorData.error || 'Error al agregar el producto al carrito.');
        });
    })
    .then(data => {
        // Muestra un mensaje de éxito
        console.log("Respuesta de la API:", data);
        alert('Producto agregado al carrito con éxito!');
        // Puedes actualizar el estado de la UI aquí, como el contador del carrito
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
    });
}

// TODO: Función para actualizar cantidad en el carrito (futura implementación)
function updateCartQuantity(itemId, quantity) {
    // La implementación de esta función dependerá del diseño del carrito
    console.log(`Actualizando la cantidad del item ${itemId} a ${quantity}`);
}

// TODO: Función para remover items del carrito (futura implementación)
function removeFromCart(itemId) {
    // La implementación de esta función dependerá del diseño del carrito
    console.log(`Removiendo el item ${itemId} del carrito`);
}