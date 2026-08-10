CREATE INDEX idx_sales_sale_time ON sales(store_id, sale_time);
CREATE INDEX idx_sales_items_sale ON sales_items(sale_id);
CREATE INDEX idx_shifts_employee_date ON shifts(employee_id, start_time);
CREATE INDEX idx_shifts_store_date ON shifts(store_id, start_time);
CREATE INDEX idx_waste_store_product ON waste(store_id, waste_time);