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
CREATE TABLE shifts (
    shift_id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    role VARCHAR(50) NOT NULL,
    CHECK (end_time > start_time),
    CHECK (role IN ('Barista', 'Shift Lead', 'Cook'))

);
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    net_sales DECIMAL(10,2) NOT NULL CHECK (net_sales >= 0),
    tips DECIMAL(10,2) NOT NULL CHECK (tips >= 0),
    sale_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    CHECK (subtotal >= 0)
    
);
CREATE TABLE sales_items (
    sale_item_id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL REFERENCES sales(sale_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity DECIMAL(10,2) NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    size_label VARCHAR(50) NOT NULL,
    CHECK (size_label IN ('12oz', '16oz'))
);
CREATE TABLE waste (
    waste_id SERIAL PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES stores(store_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity DECIMAL(10,2) NOT NULL CHECK (quantity > 0),
    reason VARCHAR(255) NOT NULL,
    waste_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
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
    CHECK (received_time IS NULL OR received_time >= order_time),
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'received', 'canceled'))
);
