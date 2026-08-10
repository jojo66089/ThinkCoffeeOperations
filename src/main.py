from db import get_db_connection
from generate_data import generate_shifts, generate_sales, generate_waste
from validate import run_all_validations
from load_data import load_all
 
NUM_DAYS = 90
 
def fetch_reference_data():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT store_id, name, neighborhood, opened_date FROM stores"
            )
            stores = cursor.fetchall()

            cursor.execute(
                "SELECT product_id, name, category, size, retail_price, cogs FROM products"
            )
            products = cursor.fetchall()

            cursor.execute(
                "SELECT employee_id, full_name, role, hourly_rate, hire_date, home_store_id "
                "FROM employees"
            )
            employees = cursor.fetchall()

        return stores, products, employees
 
def main():
    print("Reading reference data from the database...")
    stores, products, employees = fetch_reference_data()
 
    if not stores or not products or not employees:
        raise SystemExit(
            "Reference tables are empty. Run 01_schema.sql and "
            "02_seed_reference_data.sql before running main.py."
        )
 
    # dictionaries were used here for easier access.
    employee_dicts = [
    {"employee_id": e[0], "full_name": e[1], "role": e[2],
     "hourly_rate": float(e[3]), "hire_date": e[4], "home_store_id": e[5]}
    for e in employees
    ]
    product_dicts = [
    {"product_id": p[0], "name": p[1], "category": p[2],
     "size": p[3], "retail_price": float(p[4]), "cogs": float(p[5])}
    for p in products   
    ]
 
    print("Generating shifts...")
    shifts, roster = generate_shifts(employee_dicts, num_days=NUM_DAYS)
 
    print("Generating sales and sale items...")
    sales, sale_items = generate_sales(roster, product_dicts, num_days=NUM_DAYS)
 
    print("Generating waste...")
    waste = generate_waste(sales, sale_items, product_dicts, num_days=NUM_DAYS)
 
    print(f"Generated: {len(shifts)} shifts, {len(sales)} sales, "
          f"{len(sale_items)} sale items, {len(waste)} waste events.")
 
    print("Validating...")
    run_all_validations(stores, products, employees, shifts, sales, sale_items, waste)
 
    print("Loading transactional data...")
    # store, products, and employees are already in the database from the   seed script, so we pass empty lists for these tables.
    load_all([], [], [], shifts, sales, sale_items, waste)
 
    print("Done.")
 
 
if __name__ == "__main__":
    main()