# SaaS Starter Flask Template

A complete SaaS application starter template with authentication, dashboard, billing, and API key management.

## Features

- User authentication (register, login, logout)
- Password hashing with Werkzeug
- User profile management
- API key generation and management
- Subscription billing (Free/Pro/Enterprise)
- Dashboard with stats and activity
- Settings page with tabs
- Documentation page
- Responsive dark theme
- Flask-Login for session management
- SQLAlchemy for database

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

6. Demo login: `demo@example.com` / `password123`

## Routes

### Public
- `/` - Landing page
- `/register` - User registration
- `/login` - User login

### Authenticated
- `/dashboard` - Main dashboard
- `/projects` - Projects management
- `/api-keys` - API key management
- `/settings` - Account settings
- `/billing` - Subscription & billing
- `/documentation` - API documentation

## Project Structure

```
saas-starter/
├── app.py              # Main Flask application
├── requirements.txt    # Dependencies
├── static/
│   ├── css/style.css   # All styles
│   └── js/main.js      # JavaScript
└── templates/
    ├── base.html       # Base template
    ├── landing.html    # Landing page
    ├── auth/
    │   ├── register.html
    │   └── login.html
    └── dashboard/
        ├── base.html       # Dashboard layout
        ├── index.html      # Dashboard home
        ├── projects.html   # Projects page
        ├── api_keys.html   # API keys page
        ├── settings.html   # Settings page
        ├── billing.html    # Billing page
        └── documentation.html
```

## Stripe Integration

To add Stripe billing:

1. Install stripe: `pip install stripe`
2. Add your Stripe keys to the app
3. Create checkout sessions in the billing routes
4. Add webhook handlers for payment events

See Stripe documentation for full integration guide.
