import os
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DB_FILE = "products.db"

# Create database and table
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    brand TEXT,
                    price REAL,
                    stock INTEGER,
                    image TEXT
                )''')
    conn.commit()
    conn.close()

# Add sample products if table is empty
def seed_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        products = [
            ("Digital Timer", "Multispan", 1200, 5, "multispan_timer.jpg"),
            ("MCB Switch", "Sibass", 450, 10, "sibass_mcb.jpg")
        ]
        c.executemany("INSERT INTO products (name, brand, price, stock, image) VALUES (?, ?, ?, ?, ?)", products)
        conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT stock FROM products WHERE id=?", (product_id,))
    stock = c.fetchone()
    if stock and stock[0] > 0:
        c.execute("UPDATE products SET stock = stock - 1 WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Item added to cart!"})
    conn.close()
    return jsonify({"status": "error", "message": "Out of stock!"})

if __name__ == '__main__':
    init_db()
    seed_data()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
