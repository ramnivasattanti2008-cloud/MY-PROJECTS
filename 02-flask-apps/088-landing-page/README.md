# Landing Page Flask Template

A modern, dark-themed landing page template built with Flask.

## Features

- Hero section with stats
- Features showcase
- Pricing plans
- Contact form with database storage
- Responsive design
- Smooth animations
- Toast notifications

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

5. Open http://localhost:5000 in your browser.

## Project Structure

```
landing-page/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css   # Dark theme styles
│   └── js/
│       └── main.js     # JavaScript functionality
├── templates/
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── features.html   # Features page
│   ├── pricing.html    # Pricing page
│   └── contact.html    # Contact form page
└── README.md
```

## Routes

- `/` - Home page
- `/features` - Features showcase
- `/pricing` - Pricing plans
- `/contact` - Contact form

## Customization

Update `app.py` with your own:
- Secret key
- Database configuration
- Email settings

Colors can be customized in `static/css/style.css` by modifying the CSS variables.
