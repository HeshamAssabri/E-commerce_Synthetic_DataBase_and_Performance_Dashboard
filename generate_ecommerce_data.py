import random
import datetime
from faker import Faker
from faker.providers import internet, lorem, date_time

fake = Faker('en_US')
fake.add_provider(internet)
fake.add_provider(lorem)
fake.add_provider(date_time)

# ----- Configuration -----
NUM_PRODUCTS = 55
NUM_EMPLOYEES = 20
NUM_CUSTOMERS = 250
NUM_ORDERS = 1200
MAX_ORDER_ITEMS = 5
START_DATE = datetime.date(2022, 1, 1)
END_DATE = datetime.date(2025, 3, 1)
REVIEW_PROBABILITY = 0.35

def random_date(start, end):
    return fake.date_between(start_date=start, end_date=end)

def random_datetime(start, end):
    return fake.date_time_between(start_date=start, end_date=end)

def safe_phone():
    """Generate a phone number that fits in VARCHAR(20)."""
    area = random.randint(200, 999)
    exch = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"{area}-{exch}-{line}"

# ---------- EMPLOYEES (with unique emails) ----------
job_levels = [
    ('CEO', 'Executive', 200000, 250000, None),
    ('VP of Sales', 'Executive', 150000, 180000, 'CEO'),
    ('VP of Marketing', 'Executive', 150000, 180000, 'CEO'),
    ('VP of Operations', 'Executive', 150000, 180000, 'CEO'),
    ('Sales Manager', 'Sales', 90000, 110000, 'VP of Sales'),
    ('Marketing Manager', 'Marketing', 90000, 110000, 'VP of Marketing'),
    ('Warehouse Manager', 'Operations', 70000, 85000, 'VP of Operations'),
    ('Customer Service Manager', 'Support', 65000, 80000, 'VP of Operations'),
    ('Senior Sales Rep', 'Sales', 60000, 75000, 'Sales Manager'),
    ('Sales Rep', 'Sales', 45000, 60000, 'Sales Manager'),
    ('Marketing Specialist', 'Marketing', 50000, 65000, 'Marketing Manager'),
    ('Warehouse Associate', 'Operations', 35000, 45000, 'Warehouse Manager'),
    ('Customer Service Rep', 'Support', 35000, 45000, 'Customer Service Manager'),
    ('IT Support', 'IT', 55000, 70000, 'CEO'),
    ('HR Generalist', 'HR', 50000, 65000, 'CEO'),
    ('Accountant', 'Finance', 55000, 70000, 'CEO'),
    ('Sales Rep II', 'Sales', 50000, 65000, 'Sales Manager'),
    ('Warehouse Lead', 'Operations', 45000, 55000, 'Warehouse Manager'),
    ('Marketing Assistant', 'Marketing', 40000, 50000, 'Marketing Manager'),
    ('Receptionist', 'Admin', 30000, 40000, 'HR Generalist')
]

employee_emails = set()
employee_list = []
while len(employee_list) < NUM_EMPLOYEES:
    title, dept, min_sal, max_sal, _ = random.choice(job_levels)
    first = fake.first_name()
    last = fake.last_name()
    email = f"{first.lower()}.{last.lower()}@ecommerce.com"
    if email in employee_emails:
        continue
    employee_emails.add(email)
    phone = safe_phone()
    hire_date = random_date(datetime.date(2015, 1, 1), datetime.date(2024, 12, 31))
    salary = round(random.uniform(min_sal, max_sal), -2)
    employee_list.append({
        'first_name': first,
        'last_name': last,
        'email': email,
        'phone': phone,
        'hire_date': hire_date,
        'job_title': title,
        'salary': salary,
        'department': dept,
        'manager_id': None
    })

# Assign manager_ids (1‑based)
ceo_id = None
for idx, emp in enumerate(employee_list):
    if emp['job_title'] == 'CEO':
        ceo_id = idx+1
        break

for idx, emp in enumerate(employee_list):
    if emp['job_title'] == 'CEO':
        emp['manager_id'] = None
    else:
        possible = [i for i, e in enumerate(employee_list) if e['salary'] > emp['salary'] and i != idx]
        if possible:
            emp['manager_id'] = random.choice(possible) + 1
        else:
            emp['manager_id'] = ceo_id

emp_inserts = []
for emp in employee_list:
    manager_id_val = 'NULL' if emp['manager_id'] is None else emp['manager_id']
    emp_inserts.append(
        f"({emp['first_name']!r}, {emp['last_name']!r}, {emp['email']!r}, {emp['phone']!r}, "
        f"'{emp['hire_date'].strftime('%Y-%m-%d')}', {emp['job_title']!r}, {emp['salary']}, {manager_id_val}, {emp['department']!r})"
    )

# ---------- CUSTOMERS (with unique emails) ----------
genders = ['Male', 'Female', 'Other']
customer_emails = set()
customer_list = []
while len(customer_list) < NUM_CUSTOMERS:
    first = fake.first_name()
    last = fake.last_name()
    email = fake.email()
    if email in customer_emails:
        continue
    customer_emails.add(email)
    phone = safe_phone()
    address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    postal = fake.zipcode()
    country = 'USA'
    reg_date = random_date(datetime.date(2020,1,1), END_DATE)
    dob = random_date(datetime.date(1950,1,1), datetime.date(2005,12,31))
    gender = random.choice(genders)
    active = random.random() < 0.95
    customer_list.append({
        'first': first, 'last': last, 'email': email, 'phone': phone,
        'address': address, 'city': city, 'state': state, 'postal': postal,
        'country': country, 'reg_date': reg_date, 'dob': dob, 'gender': gender, 'active': active
    })

cust_inserts = []
for c in customer_list:
    cust_inserts.append(
        f"({c['first']!r}, {c['last']!r}, {c['email']!r}, {c['phone']!r}, {c['address']!r}, "
        f"{c['city']!r}, {c['state']!r}, {c['postal']!r}, {c['country']!r}, "
        f"'{c['reg_date'].strftime('%Y-%m-%d')}', '{c['dob'].strftime('%Y-%m-%d')}', {c['gender']!r}, {c['active']})"
    )

# ---------- PRODUCTS ----------
product_categories = {
    'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smartwatch', 'Camera', 'Speaker', 'Monitor', 'Keyboard', 'Mouse'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes', 'Socks', 'Hat', 'Scarf', 'Gloves', 'Sweater'],
    'Books': ['Fiction', 'Non-Fiction', 'Science', 'History', 'Biography', 'Children', 'Cooking', 'Travel', 'Self-Help', 'Comics'],
    'Home & Garden': ['Lamp', 'Rug', 'Curtains', 'Pillow', 'Blanket', 'Tool Set', 'Plant Pot', 'Garden Hose', 'Cookware', 'Cutlery'],
    'Sports': ['Yoga Mat', 'Dumbbells', 'Basketball', 'Tennis Racket', 'Running Shoes', 'Water Bottle', 'Bicycle', 'Tent', 'Fishing Rod', 'Ski Goggles'],
    'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'RC Car', 'Lego Set', 'Stuffed Animal', 'Kite', 'Play-Doh', 'Toy Train'],
    'Automotive': ['Car Cover', 'Seat Cover', 'Air Freshener', 'Wax', 'Oil Filter', 'Spark Plug', 'Battery Charger', 'Floor Mat', 'Steering Wheel Cover', 'Dashboard Camera'],
    'Health': ['Vitamins', 'First Aid Kit', 'Thermometer', 'Blood Pressure Monitor', 'Resistance Bands', 'Yoga Block', 'Foam Roller', 'Hand Sanitizer', 'Face Mask', 'Pill Organizer'],
    'Beauty': ['Shampoo', 'Conditioner', 'Lotion', 'Perfume', 'Lipstick', 'Nail Polish', 'Makeup Brush Set', 'Hair Dryer', 'Shaver', 'Sunscreen'],
    'Groceries': ['Coffee', 'Tea', 'Snack Bars', 'Pasta', 'Rice', 'Canned Soup', 'Olive Oil', 'Spices', 'Honey', 'Cereal']
}

suppliers = ['TechSupply Inc.', 'FashionWorld', 'BookDistributors', 'HomeGoods Co.', 'SportEquip', 'ToyBox', 'AutoParts Ltd.', 'HealthPlus', 'BeautyDirect', 'GroceryMart']
product_list = []
for cat, items in product_categories.items():
    for item in items:
        for variant in range(random.randint(1,3)):
            name = f"{item} {fake.word().capitalize()} {random.choice(['Pro','Basic','Deluxe','','2024','Premium'])}".strip()
            desc = fake.sentence(nb_words=12)
            price = round(random.uniform(5, 500), 2)
            cost = round(price * random.uniform(0.4, 0.8), 2)
            supplier = random.choice(suppliers)
            stock = random.randint(10, 500)
            reorder = random.randint(5, 50)
            created = random_date(datetime.date(2021,1,1), datetime.date(2024,12,31))
            active = random.random() < 0.9
            product_list.append({
                'name': name, 'desc': desc, 'cat': cat, 'price': price, 'cost': cost,
                'supplier': supplier, 'stock': stock, 'reorder': reorder, 'created': created, 'active': active
            })
product_list = product_list[:NUM_PRODUCTS]

prod_inserts = []
for p in product_list:
    prod_inserts.append(
        f"({p['name']!r}, {p['desc']!r}, {p['cat']!r}, {p['price']}, {p['cost']}, "
        f"{p['supplier']!r}, {p['stock']}, {p['reorder']}, {p['active']}, '{p['created'].strftime('%Y-%m-%d')}')"
    )

# ---------- ORDERS & ORDER ITEMS ----------
order_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
shipping_carriers = ['FedEx', 'UPS', 'USPS', 'DHL']

order_list = []
order_items_list = []
review_list = []

employee_ids = list(range(1, NUM_EMPLOYEES+1))  # Guaranteed existing IDs

for oid in range(1, NUM_ORDERS+1):
    customer = random.choice(customer_list)
    cust_id = customer_list.index(customer) + 1
    emp_id = random.choice(employee_ids) if random.random() < 0.7 else None
    order_date = random_datetime(START_DATE, END_DATE)
    required = order_date.date() + datetime.timedelta(days=random.randint(3, 10))
    shipped = None
    status = random.choices(order_statuses, weights=[0.05,0.1,0.2,0.6,0.05])[0]
    if status in ['Shipped', 'Delivered']:
        shipped = order_date + datetime.timedelta(days=random.randint(1, 5))
    elif status == 'Cancelled':
        shipped = None
    carrier = random.choice(shipping_carriers)
    freight = round(random.uniform(5, 30), 2)
    if random.random() < 0.1:
        ship_name = fake.name()
        ship_addr = fake.street_address()
        ship_city = fake.city()
        ship_state = fake.state_abbr()
        ship_zip = fake.zipcode()
        ship_country = 'USA'
    else:
        ship_name = f"{customer['first']} {customer['last']}"
        ship_addr = customer['address']
        ship_city = customer['city']
        ship_state = customer['state']
        ship_zip = customer['postal']
        ship_country = customer['country']
    
    num_items = random.randint(1, MAX_ORDER_ITEMS)
    items = []
    total = 0.0
    for _ in range(num_items):
        product = random.choice(product_list)
        prod_id = product_list.index(product) + 1
        qty = random.randint(1, 3)
        unit_price = product['price']
        discount = round(random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20]), 2)
        total_price = qty * unit_price * (1 - discount)
        items.append({
            'order_id': oid,
            'product_id': prod_id,
            'quantity': qty,
            'unit_price': unit_price,
            'discount': discount
        })
        total += total_price
    total += freight
    
    shipped_date_str = 'NULL'
    if shipped:
        shipped_date_str = f"'{shipped.date().strftime('%Y-%m-%d')}'"
    
    order_list.append({
        'customer_id': cust_id,
        'employee_id': emp_id if emp_id else 'NULL',
        'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
        'required_date': required.strftime('%Y-%m-%d'),
        'shipped_date': shipped_date_str,
        'ship_via': carrier,
        'freight': freight,
        'ship_name': ship_name,
        'ship_address': ship_addr,
        'ship_city': ship_city,
        'ship_state': ship_state,
        'ship_postal_code': ship_zip,
        'ship_country': ship_country,
        'status': status,
        'total_amount': round(total, 2)
    })
    
    for it in items:
        order_items_list.append(it)
    
    if status == 'Delivered' and random.random() < REVIEW_PROBABILITY:
        item_to_review = random.choice(items)
        review_date = order_date + datetime.timedelta(days=random.randint(1, 30))
        rating = random.randint(1,5)
        if random.random() < 0.7:
            rating = random.randint(4,5)
        text = fake.paragraph(nb_sentences=2) if random.random() < 0.8 else None
        review_list.append({
            'product_id': item_to_review['product_id'],
            'customer_id': cust_id,
            'rating': rating,
            'review_text': text,
            'review_date': review_date.strftime('%Y-%m-%d %H:%M:%S'),
            'is_verified': 'TRUE'
        })

order_inserts = []
for o in order_list:
    order_inserts.append(
        f"({o['customer_id']}, {o['employee_id']}, '{o['order_date']}', '{o['required_date']}', "
        f"{o['shipped_date']}, {o['ship_via']!r}, {o['freight']}, {o['ship_name']!r}, "
        f"{o['ship_address']!r}, {o['ship_city']!r}, {o['ship_state']!r}, {o['ship_postal_code']!r}, "
        f"{o['ship_country']!r}, {o['status']!r}, {o['total_amount']})"
    )

order_item_inserts = []
for oi in order_items_list:
    order_item_inserts.append(
        f"({oi['order_id']}, {oi['product_id']}, {oi['quantity']}, {oi['unit_price']}, {oi['discount']})"
    )

review_inserts = []
for r in review_list:
    text = r['review_text']
    if text is None:
        text = 'NULL'
    else:
        text = f"'{text}'"
    review_inserts.append(
        f"({r['product_id']}, {r['customer_id']}, {r['rating']}, {text}, '{r['review_date']}', {r['is_verified']})"
    )

# ---------- WRITE SQL FILE ----------
with open('ecommerce_data.sql', 'w') as f:
    f.write("USE assabri_shop;\n\n")
    # Disable all foreign key checks for the entire import
    f.write("SET FOREIGN_KEY_CHECKS=0;\n\n")
    
    f.write("-- Employees\n")
    f.write("INSERT INTO employees (first_name, last_name, email, phone, hire_date, job_title, salary, manager_id, department) VALUES\n")
    f.write(",\n".join(emp_inserts))
    f.write(";\n\n")
    
    f.write("-- Customers\n")
    f.write("INSERT INTO customers (first_name, last_name, email, phone, address, city, state, postal_code, country, registration_date, date_of_birth, gender, is_active) VALUES\n")
    f.write(",\n".join(cust_inserts))
    f.write(";\n\n")
    
    f.write("-- Products\n")
    f.write("INSERT INTO products (product_name, product_description, category, unit_price, cost, supplier, stock_quantity, reorder_level, is_active, created_at) VALUES\n")
    f.write(",\n".join(prod_inserts))
    f.write(";\n\n")
    
    f.write("-- Orders\n")
    f.write("INSERT INTO orders (customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_state, ship_postal_code, ship_country, status, total_amount) VALUES\n")
    f.write(",\n".join(order_inserts))
    f.write(";\n\n")
    
    f.write("-- Order Items\n")
    f.write("INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount) VALUES\n")
    f.write(",\n".join(order_item_inserts))
    f.write(";\n\n")
    
    f.write("-- Reviews\n")
    f.write("INSERT INTO reviews (product_id, customer_id, rating, review_text, review_date, is_verified_purchase) VALUES\n")
    f.write(",\n".join(review_inserts))
    f.write(";\n\n")
    
    # Re-enable foreign key checks after all data is inserted
    f.write("SET FOREIGN_KEY_CHECKS=1;\n")

print("Generated ecommerce_data.sql successfully!")