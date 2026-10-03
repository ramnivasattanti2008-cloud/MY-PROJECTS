# Django E-Commerce

A starter e-commerce application with products, cart, and checkout.

## Features

- Product catalog with categories
- Shopping cart with session storage
- Basic checkout flow
- Order management
- User accounts

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample products (optional)
python manage.py loaddata products.json

# Run development server
python manage.py runserver
```

## Usage

1. Browse products in the store
2. Add items to cart
3. Proceed to checkout
4. Place order
5. View order history
