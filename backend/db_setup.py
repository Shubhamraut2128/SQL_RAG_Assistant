import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sales.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE customers(
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE products(
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE orders(
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    amount REAL,
    order_date TEXT
)
""")

cursor.executemany(
"INSERT INTO customers VALUES(?,?,?)",
[(1,'Rahul','Mumbai'),
 (2,'Amit','Pune'),
 (3,'Sneha','Delhi')]
)

cursor.executemany(
"INSERT INTO products VALUES(?,?,?)",
[(1,'Laptop',70000),
 (2,'Mobile',30000),
 (3,'Tablet',25000)]
)

cursor.executemany(
"INSERT INTO orders VALUES(?,?,?,?,?)",
[(1,1,1,70000,'2024-01-10'),
 (2,1,2,30000,'2024-02-11'),
 (3,2,2,30000,'2024-02-15'),
 (4,3,3,25000,'2024-03-01')]
)

conn.commit()
conn.close()

print("✅ New sales.db Created")