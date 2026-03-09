import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    brand TEXT,
    price REAL,
    stock INTEGER,
    image TEXT
)
''')

# Insert sample products
products = [
    ("Digital Timer", "Multispan", 1200, 5, "timer.jpg"),
    ("Voltage Protector", "Sibass Electric", 850, 3, "protector.jpg"),
    ("Energy Meter", "Multispan", 1500, 2, "meter.jpg"),
    ("MCB Switch", "Sibass Electric", 250, 10, "mcb.jpg")
]

c.executemany("INSERT INTO products (name, brand, price, stock, image) VALUES (?, ?, ?, ?, ?)", products)

conn.commit()
conn.close()

print("products.db created with sample data!")
