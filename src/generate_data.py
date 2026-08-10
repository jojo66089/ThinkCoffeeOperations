import random
from collections import defaultdict
from datetime import date, time, timedelta, datetime

STORE_VOLUME_MULTIPLIER = {
    1: 0.85,   # Nomad
    2: 1.25,   # Hudson Yards and its the busiest store because of commuters
    3: 1.00,   # Mercer 
}
#since labor is distributed based on opening/closing shifts, I created these time buckets to make these shifts more realistic.
#There's a higher probability of sales during the opening hours and a lower probability during the closing hours, thus influencing the weight.
TIME_BUCKETS = [
    # (bucket_start, bucket_end, weight, period)
    (time(7, 0), time(13, 30), 0.40, "opening"),
    (time(14, 0), time(19, 00), 0.10, "closing"),
]
#similrlly, to create a realistic distribution of sales for a coffee shop, there these weights in place to reflect accurate sales (like more coffee sales than pastries, etc)
CATEGORY_WEIGHTS = {
    "Coffee": 0.35,
    "Latte": 0.35,
    "Tea": 0.10,
    "Bottled Beverage": 0.05,
    "Pastry": 0.15,
}
 
SIZE_WEIGHTS = {"12oz": 1, "16oz": 2}  #More large drinks are sold than small drinks, so the weight is higher for 16oz drinks.
BASE_SALES_PER_DAY_PER_STORE = 140  # before the store volume multiplier
 
def generate_shifts(employees, num_days=90, start_date=None):
    if start_date is None:
        start_date = date.today() - timedelta(days=num_days)
 
    employees_by_store = defaultdict(list)
    for emp in employees:
        employees_by_store[emp["home_store_id"]].append(emp)
 
    shifts = []
    roster = {}
    shift_id = 1
 
    for day_offset in range(num_days):
        shift_date = start_date + timedelta(days=day_offset)
        is_weekend = shift_date.weekday() >= 5
 
        open_start = time(8, 0) if is_weekend else time(7, 0)
        open_end = time(15, 0)
        close_start = time(15, 0)
        close_end = time(19, 0)
 
        for store_id, store_roster in employees_by_store.items():
            if len(store_roster) < 3:
                continue  # not enough staff seeded for this store, skip
 
            cook = next((e for e in store_roster if e["role"] == "Cook"), None)
            everyone_else = [e for e in store_roster if e is not cook]
 
            openers = random.sample(everyone_else, min(2, len(everyone_else)))
            opener_ids = [e["employee_id"] for e in openers]
            if cook:
                opener_ids.append(cook["employee_id"])
                shifts.append((shift_id, cook["employee_id"], store_id, shift_date,
                                open_start, open_end, "Cook"))
                shift_id += 1
            for emp in openers:
                shifts.append((shift_id, emp["employee_id"], store_id, shift_date,
                                open_start, open_end, "Barista"))
                shift_id += 1
 
            roster[(store_id, shift_date, "opening")] = {
                "start": open_start, "end": open_end, "employee_ids": opener_ids,
            }
 
            # Closing crew cant be people who opened, if not enough, just pick from the whole roster.
            closing_pool = [e for e in store_roster if e["employee_id"] not in opener_ids]
            if len(closing_pool) < 2:
                closing_pool = store_roster
            closers = random.sample(closing_pool, min(2, len(closing_pool)))
            closer_ids = [e["employee_id"] for e in closers]
            for emp in closers:
                shifts.append((shift_id, emp["employee_id"], store_id, shift_date,
                                close_start, close_end, "Barista"))
                shift_id += 1
 
            roster[(store_id, shift_date, "closing")] = {
                "start": close_start, "end": close_end, "employee_ids": closer_ids,
            }
 
    return shifts, roster
def _pick_product(products_by_category):
    category = random.choices(
        list(CATEGORY_WEIGHTS.keys()), weights=list(CATEGORY_WEIGHTS.values()), k=1
    )[0]
    candidates = products_by_category[category]
 
    if category in ("Coffee", "Latte"):
        size = random.choices(
            list(SIZE_WEIGHTS.keys()), weights=list(SIZE_WEIGHTS.values()), k=1
        )[0]
        candidates = [p for p in candidates if p["size"] == size] or candidates
 
    return random.choice(candidates)
 
 
def _generate_items_for_sale(sale_id, products_by_category, next_item_id):
    items = []
    num_items = random.choices([1, 2, 3], weights=[0.55, 0.30, 0.15], k=1)[0]
 
    for _ in range(num_items):
        product = _pick_product(products_by_category)
        quantity = random.choices([1, 2], weights=[0.85, 0.15], k=1)[0]
        items.append((
            next_item_id(),
            sale_id,
            product["product_id"],
            quantity,
            product["retail_price"],       # show real price, not a random one
            product.get("size"),
        ))
 
    subtotal = sum(item[3] * item[4] for item in items)
    return items, round(subtotal, 2)

def generate_sales(roster, products, num_days=90, start_date=None):
 
    if start_date is None:
        start_date = date.today() - timedelta(days=num_days)
 
    products_by_category = defaultdict(list)
    for p in products:
        products_by_category[p["category"]].append(p)
 
    sales = []
    sale_items = []
    sale_id = 1
    item_id_counter = [1]
 
    def next_item_id():
        val = item_id_counter[0]
        item_id_counter[0] += 1
        return val
 
    store_ids = {store_id for (store_id, _, _) in roster.keys()}
 
    for day_offset in range(num_days):
        shift_date = start_date + timedelta(days=day_offset)
 
        for store_id in store_ids:
            volume_multiplier = STORE_VOLUME_MULTIPLIER.get(store_id, 1.0)
            daily_sales_count = round(BASE_SALES_PER_DAY_PER_STORE * volume_multiplier)
 
            for _ in range(daily_sales_count):
                bucket_start, bucket_end, _, period = random.choices(
                    TIME_BUCKETS, weights=[b[2] for b in TIME_BUCKETS], k=1
                )[0]
 
                shift_info = roster.get((store_id, shift_date, period))
                if not shift_info or not shift_info["employee_ids"]:
                    continue  # nobody was scheduled for this slot, skip the sale
 
                employee_id = random.choice(shift_info["employee_ids"])
 
                # Random timestamp inside the  bucket, but close to the actual shift window so its not outside start_time/end_time.
                effective_start = max(bucket_start, shift_info["start"])
                effective_end = min(bucket_end, shift_info["end"])
                start_dt = datetime.combine(shift_date, effective_start)
                end_dt = datetime.combine(shift_date, effective_end)
                if end_dt <= start_dt:
                    continue
                seconds_range = int((end_dt - start_dt).total_seconds())
                sale_timestamp = start_dt + timedelta(seconds=random.randint(0, seconds_range))
 
                items, subtotal = _generate_items_for_sale(sale_id, products_by_category, next_item_id)
                sale_items.extend(items)
 
                tip_amount = round(subtotal * random.uniform(0.12, 0.22), 2)
                # net_sales starts equal to subtotal here. 
                # Refunds which will be adjusted with net_sales accordingly after.
                net_sales = subtotal
 
                sales.append((
                    sale_id, store_id, employee_id, sale_timestamp,
                    subtotal, tip_amount, net_sales, False,
                ))
                sale_id += 1
 
    return sales, sale_items
WASTE_RATE = 0.02                  # ~2% of sale items become waste, because not every item sold is wasted, but some items are wasted due to spoilage, overproduction, etc.
PRE_SALE_DROP_PROBABILITY = 0.06  #drops tied to no sale, like a customer changing their mind or a barista making a mistake.

REASON_WEIGHTS = {"Remake": 0.70, "Customer Return": 0.30}

def generate_waste(sales, sale_items, products, num_days=90, start_date=None):
    if start_date is None:
        start_date = date.today() - timedelta(days=num_days)
 
    sale_lookup = {s[0]: {"store_id": s[1], "timestamp": s[3]} for s in sales}
 
    waste = []
    waste_id = 1
 
    for item in sale_items:
        sale_item_id, sale_id, product_id, quantity, unit_price, size_label = item
 
        if random.random() >= WASTE_RATE:
            continue
 
        sale_info = sale_lookup.get(sale_id)
        if not sale_info:
            continue
 
        reason = random.choices(
            list(REASON_WEIGHTS.keys()), weights=list(REASON_WEIGHTS.values()), k=1
        )[0]
 
        waste.append((
            waste_id,
            sale_item_id,
            sale_info["store_id"],
            product_id,
            quantity,
            reason,
            sale_info["timestamp"],   # waste happens at the moment the item was made
        ))
        waste_id += 1
 
    # --- Waste with no sale behind it at all ---
    store_ids = {s[1] for s in sales}
    for day_offset in range(num_days):
        shift_date = start_date + timedelta(days=day_offset)
        for store_id in store_ids:
            if random.random() >= PRE_SALE_DROP_PROBABILITY:
                continue
 
            product = random.choice(products)
            event_time = time(random.randint(7, 18), random.randint(0, 59))
            event_timestamp = datetime.combine(shift_date, event_time)
 
            waste.append((
                waste_id,
                None,                       # sale_item_id: it never became a sale
                store_id,
                product["product_id"],
                1,
                "Dropped before sale",
                event_timestamp,
            ))
            waste_id += 1
 
    return waste