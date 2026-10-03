from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'ecommerce-secret-key'

PRODUCTS = [
    {'id': 1, 'name': 'Wireless Headphones', 'price': 79.99, 'category': 'Electronics', 'image': 'https://picsum.photos/seed/headphones/300/300'},
    {'id': 2, 'name': 'Smart Watch', 'price': 199.99, 'category': 'Electronics', 'image': 'https://picsum.photos/seed/watch/300/300'},
    {'id': 3, 'name': 'Running Shoes', 'price': 89.99, 'category': 'Sports', 'image': 'https://picsum.photos/seed/shoes/300/300'},
    {'id': 4, 'name': 'Laptop Stand', 'price': 49.99, 'category': 'Office', 'image': 'https://picsum.photos/seed/stand/300/300'},
    {'id': 5, 'name': 'Bluetooth Speaker', 'price': 59.99, 'category': 'Electronics', 'image': 'https://picsum.photos/seed/speaker/300/300'},
    {'id': 6, 'name': 'Yoga Mat', 'price': 34.99, 'category': 'Sports', 'image': 'https://picsum.photos/seed/yoga/300/300'},
]

if 'cart' not in session:
    session['cart'] = []

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return render_template('product.html', product=product)
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = []
    for item in session.get('cart', []):
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            cart_items.append({**product, 'quantity': item['quantity']})
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', [])
    existing = next((item for item in cart if item['id'] == product_id), None)
    if existing:
        existing['quantity'] += 1
    else:
        cart.append({'id': product_id, 'quantity': 1})
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        session['cart'] = []
        return render_template('order_success.html')
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
