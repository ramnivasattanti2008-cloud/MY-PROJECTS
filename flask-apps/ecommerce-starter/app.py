from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, EmailField, TextAreaField, IntegerField, DecimalField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    products = db.relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Decimal(10, 2), nullable=False)
    sale_price = db.Column(db.Decimal(10, 2))
    sku = db.Column(db.String(50), unique=True)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(200))
    images = db.Column(db.Text)  # JSON string of additional images
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.price

    @property
    def in_stock(self):
        return self.stock > 0


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='pending')
    subtotal = db.Column(db.Decimal(10, 2), nullable=False)
    shipping = db.Column(db.Decimal(10, 2), default=0)
    tax = db.Column(db.Decimal(10, 2), default=0)
    total = db.Column(db.Decimal(10, 2), nullable=False)
    shipping_name = db.Column(db.String(100))
    shipping_address = db.Column(db.Text)
    shipping_city = db.Column(db.String(100))
    shipping_state = db.Column(db.String(100))
    shipping_zip = db.Column(db.String(20))
    shipping_country = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Decimal(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Decimal(10, 2), nullable=False)


class CartItem:
    def __init__(self, product_id, name, price, quantity=1, image=None):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.quantity = quantity
        self.image = image

    @property
    def total(self):
        return self.price * self.quantity


# Forms
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class CheckoutForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    country = SelectField('Country', choices=[
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('UK', 'United Kingdom'),
        ('AU', 'Australia'),
    ], default='US')
    notes = TextAreaField('Order Notes')
    submit = SubmitField('Place Order')


# Cart helpers
def get_cart():
    return session.get('cart', {})


def save_cart(cart):
    session['cart'] = cart
    session.modified = True


def add_to_cart(product_id, quantity=1):
    cart = get_cart()
    product = Product.query.get(product_id)

    if not product:
        return False

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.current_price),
            'quantity': quantity,
            'image': product.image
        }

    save_cart(cart)
    return True


def update_cart_item(product_id, quantity):
    cart = get_cart()
    if str(product_id) in cart:
        if quantity > 0:
            cart[str(product_id)]['quantity'] = quantity
        else:
            del cart[str(product_id)]
        save_cart(cart)
        return True
    return False


def remove_from_cart(product_id):
    cart = get_cart()
    if str(product_id) in cart:
        del cart[str(product_id)]
        save_cart(cart)
        return True
    return False


def clear_cart():
    save_cart({})


def get_cart_total():
    cart = get_cart()
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    shipping = 9.99 if subtotal < 50 and subtotal > 0 else 0
    tax = subtotal * 0.08
    total = subtotal + shipping + tax
    return {'subtotal': subtotal, 'shipping': shipping, 'tax': tax, 'total': total}


# Routes - Public
@app.route('/')
def index():
    featured = Product.query.filter_by(is_featured=True, is_active=True).limit(8).all()
    categories = Category.query.all()
    new_arrivals = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(4).all()
    return render_template('shop/index.html', featured=featured, categories=categories, new_arrivals=new_arrivals)


@app.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    per_page = 12

    category_slug = request.args.get('category')
    search_query = request.args.get('q')

    query = Product.query.filter_by(is_active=True)

    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
        else:
            category = None
    else:
        category = None

    if search_query:
        query = query.filter(Product.name.contains(search_query))

    products = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=per_page)
    categories = Category.query.all()

    return render_template('shop/shop.html', products=products, categories=categories, category=category, search=search_query)


@app.route('/product/<slug>')
def product(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    related = Product.query.filter(Product.category_id == product.category_id, Product.id != product.id, is_active=True).limit(4).all()
    return render_template('shop/product.html', product=product, related=related)


@app.route('/category/<slug>')
def category(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(category_id=cat.id, is_active=True).paginate(page=page, per_page=12)
    categories = Category.query.all()
    return render_template('shop/shop.html', products=products, categories=categories, category=cat)


@app.route('/cart')
def cart():
    cart_items = list(get_cart().values())
    totals = get_cart_total()
    return render_template('shop/cart.html', cart_items=cart_items, **totals)


@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if add_to_cart(product_id, quantity):
        cart_count = sum(item['quantity'] for item in get_cart().values())
        return jsonify({'success': True, 'cart_count': cart_count})
    return jsonify({'success': False, 'error': 'Product not found'})


@app.route('/api/cart/update', methods=['POST'])
def api_cart_update():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if update_cart_item(product_id, quantity):
        totals = get_cart_total()
        return jsonify({'success': True, **totals})
    return jsonify({'success': False, 'error': 'Update failed'})


@app.route('/api/cart/remove', methods=['POST'])
def api_cart_remove():
    data = request.get_json()
    product_id = data.get('product_id')

    if remove_from_cart(product_id):
        totals = get_cart_total()
        cart_count = sum(item['quantity'] for item in get_cart().values())
        return jsonify({'success': True, 'cart_count': cart_count, **totals})
    return jsonify({'success': False, 'error': 'Remove failed'})


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = list(get_cart().values())
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('shop'))

    totals = get_cart_total()
    form = CheckoutForm()

    if form.validate_on_submit():
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

        order = Order(
            order_number=order_number,
            user_id=current_user.id if current_user.is_authenticated else None,
            status='pending',
            subtotal=totals['subtotal'],
            shipping=totals['shipping'],
            tax=totals['tax'],
            total=totals['total'],
            shipping_name=f"{form.first_name.data} {form.last_name.data}",
            shipping_address=form.address.data,
            shipping_city=form.city.data,
            shipping_state=form.state.data,
            shipping_zip=form.zip_code.data,
            shipping_country=form.country.data,
            notes=form.notes.data
        )

        for item in cart_items:
            order.items.append(OrderItem(
                product_id=item['product_id'],
                product_name=item['name'],
                product_price=item['price'],
                quantity=item['quantity'],
                total=item['price'] * item['quantity']
            ))

        db.session.add(order)
        db.session.commit()

        clear_cart()
        session['last_order'] = order_number
        flash(f'Order {order_number} placed successfully!', 'success')
        return redirect(url_for('order_confirmation', order_number=order_number))

    return render_template('shop/checkout.html', form=form, cart_items=cart_items, **totals)


@app.route('/order/<order_number>')
def order_confirmation(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    return render_template('shop/order_confirmation.html', order=order)


# Routes - Auth
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid email or password', 'error')

    return render_template('auth/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.context_processor
def inject_cart():
    cart_count = sum(item['quantity'] for item in get_cart().values())
    return dict(cart_count=cart_count)


@app.cli.command('init-db')
def init_db():
    db.create_all()

    # Create admin
    if not User.query.filter_by(email='admin@shop.com').first():
        admin = User(email='admin@shop.com', first_name='Admin', last_name='User', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)

    # Categories
    cats = [
        {'name': 'Electronics', 'slug': 'electronics', 'description': 'Latest gadgets and electronics'},
        {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel'},
        {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Home and garden essentials'},
        {'name': 'Sports', 'slug': 'sports', 'description': 'Sports equipment and gear'},
    ]
    for cat in cats:
        if not Category.query.filter_by(slug=cat['slug']).first():
            db.session.add(Category(**cat))

    # Sample products
    products = [
        {'name': 'Wireless Headphones', 'slug': 'wireless-headphones', 'price': 149.99, 'sale_price': 129.99, 'sku': 'WH-001', 'stock': 50, 'is_featured': True, 'category_id': 1, 'description': 'Premium wireless headphones with noise cancellation and 30-hour battery life.'},
        {'name': 'Smart Watch Pro', 'slug': 'smart-watch-pro', 'price': 299.99, 'sku': 'SW-001', 'stock': 30, 'is_featured': True, 'category_id': 1, 'description': 'Advanced smartwatch with health monitoring and GPS.'},
        {'name': 'Bluetooth Speaker', 'slug': 'bluetooth-speaker', 'price': 79.99, 'sku': 'BS-001', 'stock': 100, 'is_featured': True, 'category_id': 1, 'description': 'Portable Bluetooth speaker with rich bass and waterproof design.'},
        {'name': 'Premium T-Shirt', 'slug': 'premium-tshirt', 'price': 29.99, 'sku': 'PT-001', 'stock': 200, 'is_featured': True, 'category_id': 2, 'description': 'Soft and comfortable premium cotton t-shirt.'},
        {'name': 'Denim Jacket', 'slug': 'denim-jacket', 'price': 89.99, 'sale_price': 69.99, 'sku': 'DJ-001', 'stock': 40, 'is_featured': True, 'category_id': 2, 'description': 'Classic denim jacket with modern fit.'},
        {'name': 'Running Shoes', 'slug': 'running-shoes', 'price': 119.99, 'sku': 'RS-001', 'stock': 60, 'is_featured': True, 'category_id': 4, 'description': 'Lightweight running shoes with superior cushioning.'},
    ]
    for prod in products:
        if not Product.query.filter_by(slug=prod['slug']).first():
            db.session.add(Product(**prod))

    db.session.commit()
    print('Database initialized. Admin: admin@shop.com / admin123')


if __name__ == '__main__':
    app.run(debug=True)
