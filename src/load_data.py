from psycopg2.extras import execute_values
from db import get_db_connection

def insert_rows(cursor, table, columns, rows):
 if not rows:
        print(f"  {table}: skipping")
        return
 
 column_list = ", ".join(columns)
 sql = f"INSERT INTO {table} ({column_list}) VALUES %s"
 execute_values(cursor, sql, rows)
 print(f"  {table}: inserted {len(rows)} rows")
 
def load_all(stores, products, employees, shifts, sales, sale_items, waste):

    with get_db_connection() as conn:
        try:
            with conn.cursor() as cursor:
    
                insert_rows(cursor, "stores",
                            ["store_id", "name", "neighborhood", "opened_date"],
                            stores)
 
                insert_rows(cursor, "products",
                            ["product_id", "name", "category", "size",
                             "retail_price", "cogs"],
                            products)
 
                insert_rows(cursor, "employees",
                            ["employee_id", "full_name", "role", "hourly_rate",
                             "hire_date", "home_store_id"],
                            employees)
 
                insert_rows(cursor, "shifts",
                            ["shift_id", "employee_id", "store_id", "shift_date",
                             "start_time", "end_time", "role_worked"],
                            shifts)
 
                insert_rows(cursor, "sales",
                            ["sale_id", "store_id", "employee_id", "sale_timestamp",
                             "subtotal", "tip_amount", "net_sales", "is_refunded"],
                            sales)
 
                insert_rows(cursor, "sale_items",
                            ["sale_item_id", "sale_id", "product_id", "quantity",
                             "unit_price_at_sale", "size_label"],
                            sale_items)
 
                insert_rows(cursor, "waste_events",
                            ["waste_id", "sale_item_id", "store_id", "product_id",
                             "quantity_wasted", "reason", "event_timestamp"],
                            waste)
 
            conn.commit()
            print("finished loading.")
 
        except Exception as error:
            conn.rollback()
            print(f"Load failed, Error: {error}")
            raise