# E-commerce Flask Template

A complete e-commerce application with products, cart, and checkout flow.

## Features

- Product catalog with categories
- Shopping cart with session storage
- Checkout with order management
- User authentication
- Featured products
- Sale pricing
- Stock tracking
- Responsive dark theme
- AJAX cart updates

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
flask init-db
```

4. Run the application:
```bash
python app.py
```

5. Open http://localhost:5000

## Routes

### Public
- `/` - Homepage with featured products
- `/shop` - All products with filtering
- `/product/<slug>` - Product detail
- `/category/<slug>` - Category products
- `/cart` - Shopping cart
- `/checkout` - Checkout form
- `/order/<order_number>` - Order confirmation

### Auth
- `/login` - User login
- `/register` - User registration
- `/logout` - User logout

## Project Structure

```
ecommerce-starter/
├── app.py              # Main Flask application
├── requirements.txt    # Dependencies
├── static/
│   ├── css/style.css  # All styles
│   └── js/main.js     # JavaScript with cart logic
└── templates/
    ├── base.html       # Base template
    ├── auth/           # Login/Register
    └── shop/          # Shop pages
```

## Cart System

The cart uses Flask sessions for storage:
- Cart persists across page loads
- AJAX updates for seamless UX
- Real-time total calculations
- Free shipping threshold: $50

## Checkout Flow

1. Add items to cart
2. View cart and adjust quantities
3. Fill checkout form
4. Submit order
5. Receive confirmation number

## Stripe Integration

To add payment processing:

1. Install stripe: `pip install stripe`
2. Add Stripe keys
3. Create payment intents in checkout route
4. Add Stripe Elements to checkout template
5. Handle webhook events

See Stripe documentation for full integration.
