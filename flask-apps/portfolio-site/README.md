# Portfolio Site Flask Template

A modern, dark-themed portfolio template built with Flask.

## Features

- Hero section with animated avatar
- About page with skills and experience timeline
- Projects grid with hover effects
- Project detail pages
- Contact form with database storage
- Responsive design
- Smooth animations
- Skills progress bars

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

- `/` - Home page with hero and featured projects
- `/about` - About page with skills and experience
- `/projects` - All projects grid
- `/project/<id>` - Individual project detail
- `/contact` - Contact form

## Project Structure

```
portfolio-site/
├── app.py              # Flask application with portfolio data
├── requirements.txt
├── static/
│   ├── css/style.css   # Dark theme styles
│   └── js/main.js      # JavaScript functionality
├── templates/
│   ├── base.html       # Base template with nav/footer
│   ├── index.html      # Home page
│   ├── about.html      # About page
│   ├── projects.html   # Projects grid
│   ├── project_detail.html  # Project detail
│   └── contact.html    # Contact form
└── README.md
```

## Customization

Edit `app.py`:
- `PROJECTS` list - Add your projects
- `SKILLS` dict - Update your skills
- `SKILLS_LEVELS` list - Set skill levels

Colors can be customized in `static/css/style.css` CSS variables.
