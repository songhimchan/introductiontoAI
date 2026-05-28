import sqlite3
import random
from datetime import datetime, timedelta

def create_db():
    conn = sqlite3.connect('local_shop.db')
    c = conn.cursor()

    # Create tables
    c.execute('''DROP TABLE IF EXISTS sales''')
    c.execute('''DROP TABLE IF EXISTS customers''')
    c.execute('''DROP TABLE IF EXISTS products''')

    c.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            sale_date DATE NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')

    # Mock Data Generation
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'Chris', 'Sarah', 'Matthew', 'Jessica', 'David', 'Ashley', 'Daniel', 'Amanda', 'James', 'Melissa', 'Robert', 'Stephanie', 'William', 'Rebecca', 'Joseph', 'Laura', 'Kevin', 'Michelle', 'Brian', 'Angela', 'Edward', 'Rachel']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte']

    categories = ['Electronics', 'Clothing', 'Home', 'Toys', 'Sports', 'Books', 'Beauty', 'Grocery']
    adjectives = ['Smart', 'Wireless', 'Portable', 'Ergonomic', 'Durable', 'Classic', 'Modern', 'Eco-friendly', 'Premium', 'Compact', 'Luxury', 'Essential', 'Pro', 'Basic', 'Advanced']
    nouns = ['Phone', 'Laptop', 'Headphones', 'Speaker', 'Monitor', 'Jacket', 'T-Shirt', 'Blender', 'Vacuum', 'Bicycle', 'Watch', 'Tablet', 'Camera', 'Keyboard', 'Mouse', 'Desk', 'Chair']

    num_customers = 500
    num_products = 200
    num_sales = 15000

    customers = []
    for _ in range(num_customers):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        email = f"{fn.lower()}.{ln.lower()}{random.randint(1,9999)}@example.com"
        city = random.choice(cities)
        customers.append((fn, ln, email, city))

    products = []
    for _ in range(num_products):
        name = f"{random.choice(adjectives)} {random.choice(nouns)}"
        category = random.choice(categories)
        price = round(random.uniform(5.0, 1500.0), 2)
        stock = random.randint(50, 1000)
        products.append((name, category, price, stock))

    c.executemany('INSERT INTO customers (first_name, last_name, email, city) VALUES (?, ?, ?, ?)', customers)
    c.executemany('INSERT INTO products (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)', products)

    # Sales
    sales = []
    start_date = datetime(2022, 1, 1)
    for _ in range(num_sales):
        customer_id = random.randint(1, num_customers)
        product_id = random.randint(1, num_products)
        qty = random.randint(1, 10)
        days_offset = random.randint(0, 1000) # Roughly ~3 years of data
        sale_date = (start_date + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        sales.append((customer_id, product_id, qty, sale_date))

    c.executemany('INSERT INTO sales (customer_id, product_id, quantity, sale_date) VALUES (?, ?, ?, ?)', sales)

    conn.commit()
    conn.close()
    print("Database local_shop.db created and populated with mock data.")

if __name__ == '__main__':
    create_db()
