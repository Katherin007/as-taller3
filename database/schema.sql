-- TODO: Definir las tablas del sistema
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Tabla de usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Tabla de productos  
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    image_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Tabla de carritos
CREATE TABLE carts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Tabla de items del carrito
CREATE TABLE cart_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cart_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    added_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- TODO: Agregar índices y restricciones de clave foránea
-- Índice en la clave foránea user_id para búsquedas eficientes
CREATE INDEX IF NOT EXISTS idx_carts_user_id ON carts(user_id);
-- Clave foránea para la tabla de carritos
ALTER TABLE carts
    ADD CONSTRAINT fk_carts_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- Índices en las claves foráneas de los items del carrito para búsquedas eficientes
CREATE INDEX IF NOT EXISTS idx_cart_items_cart_id ON cart_items(cart_id);
CREATE INDEX IF NOT EXISTS idx_cart_items_product_id ON cart_items(product_id);
-- Claves foráneas para la tabla de items del carrito
ALTER TABLE cart_items
    ADD CONSTRAINT fk_cart_items_cart_id FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_cart_items_product_id FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE;

-- Restricción para evitar que un mismo producto se añada dos veces al mismo carrito
ALTER TABLE cart_items
    ADD CONSTRAINT unique_cart_product UNIQUE (cart_id, product_id);

-- Disparador para actualizar la fecha de modificación en la tabla de carritos
CREATE OR REPLACE TRIGGER update_carts_updated_at_trigger
BEFORE UPDATE ON carts
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- TODO: Insertar datos de prueba
INSERT INTO users (username, email, password_hash) VALUES
('juanperez', 'juan.perez@example.com', 'hashed_password_for_juan');

-- Insertar productos de prueba
INSERT INTO products (name, description, price, stock, image_url) VALUES
('Camiseta de Algodón', 'Camiseta básica de alta calidad, 100% algodón.', 25.00, 100, 'https://example.com/images/camiseta.jpg'),
('Pantalón Vaquero', 'Pantalón vaquero de corte recto, clásico y duradero.', 65.50, 50, 'https://example.com/images/vaquero.jpg'),
('Zapatillas Deportivas', 'Zapatillas cómodas y ligeras, ideales para correr.', 89.99, 75, 'https://example.com/images/zapatillas.jpg');

-- Insertar un carrito para el usuario de prueba
INSERT INTO carts (user_id) VALUES
((SELECT id FROM users WHERE username = 'juanperez'));

-- Insertar items en el carrito del usuario
INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
((SELECT id FROM carts WHERE user_id = (SELECT id FROM users WHERE username = 'juanperez')),
 (SELECT id FROM products WHERE name = 'Camiseta de Algodón'), 2),
((SELECT id FROM carts WHERE user_id = (SELECT id FROM users WHERE username = 'juanperez')),
 (SELECT id FROM products WHERE name = 'Zapatillas Deportivas'), 1);
