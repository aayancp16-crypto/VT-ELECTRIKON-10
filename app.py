from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------------------------
# Database Initialization
# ---------------------------
def init_db():
    conn = sqlite3.connect('database.db')
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

# ---------------------------
# Handle HEAD requests globally
# ---------------------------
@app.before_request
def handle_head():
    if request.method == 'HEAD':
        return '', 200  # Empty response for HEAD requests

# ---------------------------
# Home Page
# ---------------------------
@app.route('/', methods=['GET', 'HEAD'])
def home():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()
    except Exception as e:
        print("Database error:", e)
        products = []
    return render_template('index.html', products=products)

# ---------------------------
# Buy Product
# ---------------------------
@app.route('/buy/<int:product_id>', methods=['GET', 'HEAD'])
def buy(product_id):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT stock FROM products WHERE id=?", (product_id,))
        stock = c.fetchone()[0]
        if stock > 0:
            c.execute("UPDATE products SET stock = stock - 1 WHERE id=?", (product_id,))
            conn.commit()
            message = "Order placed successfully!"
        else:
            message = "Out of stock!"
        conn.close()
    except Exception as e:
        print("Error processing order:", e)
        message = "Error placing order."
    return message

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
