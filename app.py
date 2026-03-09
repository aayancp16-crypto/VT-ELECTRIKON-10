# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "vt-electrikon-secret"

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price REAL,
                    stock INTEGER,
                    image TEXT
                )''')
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products)

# Add to cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(product_id)
    return redirect(url_for("cart"))

# Cart page
@app.route('/cart')
def cart():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    cart_items = []
    total = 0
    if "cart" in session:
        for pid in session["cart"]:
            c.execute("SELECT * FROM products WHERE id=?", (pid,))
            product = c.fetchone()
            if product:
                cart_items.append(product)
                total += product[2]
    conn.close()
    return render_template("cart.html", cart_items=cart_items, total=total)

# Checkout (dummy for now)
@app.route('/checkout')
def checkout():
    return "Payment system will be integrated here."

if __name__ == "__main__":
       port = int(os.environ.get("PORT", 5000))  # Use Render's port or default to 5000 locally
       app.run(host="0.0.0.0", port=port)
   


