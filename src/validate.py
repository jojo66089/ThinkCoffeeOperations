from datetime import time

STORE_OPEN = time(7, 0)    # 7:00 AM
STORE_CLOSE = time(19, 0)  # 7:00 PM


class ValidationError(Exception):
    pass


def validate_negative(sale_items, waste):
    errors = []
    for si in sale_items:
        sale_item_id, _, _, quantity, _, _ = si
        if quantity <= 0:
            errors.append(f"sale_item {sale_item_id}: non-positive quantity {quantity}")
    for w in waste:
        waste_id = w[0]
        quantity_wasted = w[4]
        if quantity_wasted <= 0:
            errors.append(f"waste {waste_id}: non-positive quantity_wasted {quantity_wasted}")
    return errors


def validate_sale_time(sales):
    errors = []
    for s in sales:
        sale_id = s[0]
        sale_timestamp = s[3]
        t = sale_timestamp.time()
        if t < STORE_OPEN or t > STORE_CLOSE:
            errors.append(f"sale {sale_id}: timestamp {sale_timestamp} outside store hours")
    return errors


def validate_employee_shift(sales, shifts):
    scheduled = {
        (sh[1], sh[2], sh[3])  # (employee_id, store_id, shift_date)
        for sh in shifts
    }
    errors = []
    for s in sales:
        sale_id, store_id, employee_id, sale_timestamp = s[0], s[1], s[2], s[3]
        key = (employee_id, store_id, sale_timestamp.date())
        if key not in scheduled:
            errors.append(
                f"sale {sale_id}: employee {employee_id} not on shift at "
                f"store {store_id} on {sale_timestamp.date()}"
            )
    return errors


def validate_foreign_keys(sale_items, sales, waste, products, employees, stores):
    product_ids = {p[0] for p in products}
    employee_ids = {e[0] for e in employees}
    store_ids = {s[0] for s in stores}
    sale_ids = {s[0] for s in sales}
    sale_item_ids = {si[0] for si in sale_items}

    errors = []

    for si in sale_items:
        sale_item_id, sale_id, product_id = si[0], si[1], si[2]
        if sale_id not in sale_ids:
            errors.append(f"sale_item {sale_item_id}: sale_id {sale_id} not in sales")
        if product_id not in product_ids:
            errors.append(f"sale_item {sale_item_id}: product_id {product_id} not in products")

    for s in sales:
        sale_id, store_id, employee_id = s[0], s[1], s[2]
        if store_id not in store_ids:
            errors.append(f"sale {sale_id}: store_id {store_id} not in stores")
        if employee_id not in employee_ids:
            errors.append(f"sale {sale_id}: employee_id {employee_id} not in employees")

    for w in waste:
        waste_id, sale_item_id, store_id, product_id = w[0], w[1], w[2], w[3]
        if store_id not in store_ids:
            errors.append(f"waste {waste_id}: store_id {store_id} not in stores")
        if product_id not in product_ids:
            errors.append(f"waste {waste_id}: product_id {product_id} not in products")
        # sale_item_id is nullable (pre-sale drops); only check when present
        if sale_item_id is not None and sale_item_id not in sale_item_ids:
            errors.append(f"waste {waste_id}: sale_item_id {sale_item_id} not in sale_items")

    return errors


def validate_negative_prices(products, sale_items, sales):
    errors = []
    for p in products:
        product_id, retail_price, cogs = p[0], p[4], p[5]
        if retail_price < 0:
            errors.append(f"product {product_id}: negative retail_price {retail_price}")
        if cogs < 0:
            errors.append(f"product {product_id}: negative cogs {cogs}")
    for si in sale_items:
        sale_item_id, unit_price = si[0], si[4]
        if unit_price < 0:
            errors.append(f"sale_item {sale_item_id}: negative unit_price_at_sale {unit_price}")
    for s in sales:
        sale_id, subtotal, tip_amount, net_sales = s[0], s[4], s[5], s[6]
        if subtotal < 0:
            errors.append(f"sale {sale_id}: negative subtotal {subtotal}")
        if tip_amount < 0:
            errors.append(f"sale {sale_id}: negative tip_amount {tip_amount}")
        if net_sales < 0:
            errors.append(f"sale {sale_id}: negative net_sales {net_sales}")
    return errors


def validate_columns_populated(stores, products, employees):
    errors = []

    for s in stores:
        store_id, name, neighborhood, opened_date = s
        for label, value in (("name", name), ("neighborhood", neighborhood),
                              ("opened_date", opened_date)):
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"store {store_id}: missing {label}")

    for p in products:
        product_id, name, category, size, retail_price, cogs = p
        for label, value in (("name", name), ("category", category),
                              ("retail_price", retail_price), ("cogs", cogs)):
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"product {product_id}: missing {label}")

    for e in employees:
        employee_id, full_name, role, hourly_rate, hire_date, home_store_id = e
        for label, value in (("full_name", full_name), ("role", role),
                              ("hourly_rate", hourly_rate), ("hire_date", hire_date),
                              ("home_store_id", home_store_id)):
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"employee {employee_id}: missing {label}")

    return errors


def run_all_validations(stores, products, employees, shifts, sales, sale_items, waste):
    all_errors = []
    all_errors += validate_columns_populated(stores, products, employees)
    all_errors += validate_foreign_keys(sale_items, sales, waste, products, employees, stores)
    all_errors += validate_negative(sale_items, waste)
    all_errors += validate_negative_prices(products, sale_items, sales)
    all_errors += validate_sale_time(sales)
    all_errors += validate_employee_shift(sales, shifts)

    if all_errors:
        preview = "\n".join(f"  - {e}" for e in all_errors[:25])
        more = f"\n  ... and {len(all_errors) - 25} more" if len(all_errors) > 25 else ""
        raise ValidationError(
            f"{len(all_errors)} validation error(s) before load:\n{preview}{more}"
        )

    print("All validations passed.")