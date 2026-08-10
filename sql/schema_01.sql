
--DIMENSION TABLES--
CREATE TABLE stores (
    store_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    neighborhood VARCHAR(100) NOT NULL,
    opened_date DATE NOT NULL
);
 
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    -- size is null for teas, pastries, and bottled drinks (no size).
    size VARCHAR(50) CHECK (size IN ('12oz', '16oz')),
    -- temperature is null for food and bottled drinks.
    temperature VARCHAR(50) CHECK (temperature IN ('hot', 'cold')),
    retail_price DECIMAL(10,2) NOT NULL CHECK (retail_price >= 0),
    cogs DECIMAL(10,2) NOT NULL CHECK (cogs >= 0)
);
 
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Barista', 'Shift Lead', 'Cook')),
    hourly_rate DECIMAL(10,2) NOT NULL CHECK (hourly_rate >= 0),
    hire_date DATE NOT NULL,
    home_store_id INTEGER NOT NULL REFERENCES stores(store_id)
);
 
--INVENTORY TABLES--
CREATE TABLE inventory (
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity_on_hand DECIMAL(10,2) NOT NULL DEFAULT 0,
    reorder_threshold DECIMAL(10,2) NOT NULL,
    last_restocked_at TIMESTAMP,
    PRIMARY KEY (store_id, product_id),
    CHECK (quantity_on_hand >= 0),
    CHECK (reorder_threshold > 0)
);
 
 -- FACT TABLES -- 
CREATE TABLE shifts (
    shift_id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    shift_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    role_worked VARCHAR(50) NOT NULL CHECK (role_worked IN ('Barista', 'Shift Lead', 'Cook')),
    CHECK (end_time > start_time)
);
 
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
    sale_timestamp TIMESTAMP NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    tip_amount DECIMAL(10,2) NOT NULL CHECK (tip_amount >= 0),
    net_sales DECIMAL(10,2) NOT NULL CHECK (net_sales >= 0),
    is_refunded BOOLEAN NOT NULL DEFAULT FALSE
);
 
CREATE TABLE sale_items (
    sale_item_id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(sale_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity DECIMAL(10,2) NOT NULL CHECK (quantity > 0),
    unit_price_at_sale DECIMAL(10,2) NOT NULL CHECK (unit_price_at_sale >= 0),
    -- size_label is null for products with no size.
    size_label VARCHAR(50) CHECK (size_label IN ('12oz', '16oz'))
);
 
CREATE TABLE waste_events (
    waste_id SERIAL PRIMARY KEY,
    -- sale_item_id is null when the waste never became a sale.
    sale_item_id INTEGER REFERENCES sale_items(sale_item_id),
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity_wasted DECIMAL(10,2) NOT NULL CHECK (quantity_wasted > 0),
    reason VARCHAR(255) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
 
CREATE TABLE refunds (
    refund_id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(sale_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity DECIMAL(10,2) NOT NULL CHECK (quantity > 0),
    refund_amount DECIMAL(10,2) NOT NULL CHECK (refund_amount >= 0),
    refund_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
 
CREATE TABLE restock_orders (
    restock_order_id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity DECIMAL(10,2) NOT NULL CHECK (quantity > 0),
    order_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    received_time TIMESTAMP,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'received', 'canceled')),
    CHECK (received_time IS NULL OR received_time >= order_time)
);