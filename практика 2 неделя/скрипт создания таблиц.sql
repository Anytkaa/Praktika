-- 1. Таблица контрагентов (заказчики)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    inn VARCHAR(12),
    address TEXT,
    phone VARCHAR(20),
    buyer BOOLEAN, 
    salesman BOOLEAN 
);

-- 2. Таблица готовой продукции
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL, 
    unit VARCHAR(20) NOT NULL, 
    price DECIMAL(18, 2) 
);

-- 3. Таблица материалов
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL, 
    unit VARCHAR(20) NOT NULL, 
    price DECIMAL(18, 2) 
);

-- 4. Таблица спецификаций 
CREATE TABLE specifications (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL 
);

-- 5. Таблица состава спецификации
CREATE TABLE specifications_materials (
    id SERIAL PRIMARY KEY,
    spec_id INTEGER NOT NULL REFERENCES specifications(id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(id),
    quantity DECIMAL(18, 4) NOT NULL CHECK (quantity > 0) 
);

-- 6. Таблица заказов от клиентов
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    number VARCHAR(50) UNIQUE NOT NULL, 
    total DECIMAL(18, 2) 
);

-- 7. Таблица состава заказа 
CREATE TABLE orders_products (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity DECIMAL(18, 2) NOT NULL CHECK (quantity > 0),
    price DECIMAL(18, 2) NOT NULL, 
    sum DECIMAL(18, 2) GENERATED ALWAYS AS (quantity * price) STORED 
);

-- 8. Таблица производственных заказов 
CREATE TABLE productions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    number VARCHAR(50) UNIQUE NOT NULL, 
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity DECIMAL(18, 2) NOT NULL CHECK (quantity > 0) 
);

-- 9. Таблица расхода материалов на производство
CREATE TABLE productions_materials (
    id SERIAL PRIMARY KEY,
    production_id INTEGER NOT NULL REFERENCES productions(id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(id),
    quantity DECIMAL(18, 4) NOT NULL CHECK (quantity > 0) 
);