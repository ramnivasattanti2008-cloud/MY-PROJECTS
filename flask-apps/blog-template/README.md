# Flask Blog Template

A complete blog application with posts, categories, tags, comments, and Markdown support.

## Features

- Create and edit posts with Markdown
- Categories and tags system
- Comment system with moderation
- User authentication (admin)
- Search functionality
- Featured posts
- View count tracking
- Admin dashboard
- Responsive dark theme

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
6. Admin login: `admin@example.com` / `admin123`

## Routes

### Public
- `/` - Blog homepage with posts
- `/post/<slug>` - Individual post
- `/category/<slug>` - Posts by category
- `/tag/<slug>` - Posts by tag
- `/search?q=` - Search posts

### Auth
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout

### Admin (requires admin login)
- `/admin` - Dashboard
- `/admin/posts` - Manage posts
- `/admin/post/new` - Create post
- `/admin/post/<id>/edit` - Edit post
- `/admin/comments` - Moderate comments

## Markdown Support

Posts support full Markdown:
- Headers (#, ##, ###)
- Bold, italic, links
- Code blocks with syntax highlighting
- Lists, blockquotes
- Images

## Project Structure

```
blog-template/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── static/
│   ├── css/style.css  # All styles
│   └── js/main.js     # JavaScript
└── templates/
    ├── base.html       # Base template
    ├── auth/           # Auth pages
    ├── blog/           # Blog pages
    └── admin/          # Admin pages
```

## Customization

- Edit `app.py` to modify blog name, add categories
- Update CSS variables in `style.css` for colors
- Add new templates as needed
