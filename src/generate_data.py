def generate_shifts():
    shifts = []
    for shift_id in range(1, num_shifts + 1):
        employee_id = random.randint(1, num_employees)
        store_id = random.randint(1, num_stores)
        start_time = fake.date_time_between(start_date='-30d', end_date='now')
        end_time = start_time + timedelta(hours=random.randint(4, 8))
        shifts.append((shift_id, employee_id, store_id, start_time, end_time))
    return shifts

def generate_sales():
    sales = []
    for sale_id in range(1, num_sales + 1):
        store_id = random.randint(1, num_stores)
        sale_time = fake.date_time_between(start_date='-30d', end_date='now')
        total_amount = round(random.uniform(5.0, 100.0), 2)
        sales.append((sale_id, store_id, sale_time, total_amount))
    return sales
def generate_sales_items():
    sales_items = []
    for sale_id in range(1, num_sales + 1):
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            product_id = random.randint(1, num_products)
            quantity = random.randint(1, 3)
            price = round(random.uniform(1.0, 20.0), 2)
            sales_items.append((sale_id, product_id, quantity, price))
    return sales_items
def generate_waste():
    waste = []
    for _ in range(num_waste_records):
        store_id = random.randint(1, num_stores)
        product_id = random.randint(1, num_products)
        waste_time = fake.date_time_between(start_date='-30d', end_date='now')
        quantity = random.randint(1, 10)
        waste.append((store_id, product_id, waste_time, quantity))
    return waste