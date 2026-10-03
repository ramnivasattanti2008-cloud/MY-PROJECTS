# Simple Blog Flask Application

A minimalist blog with markdown support and commenting system.

## Features

- Create, edit, and delete blog posts
- Markdown support with code highlighting
- Comment system
- Auto-generated URL slugs
- Dark theme design
- Responsive layout

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will run at `http://localhost:5003`

## Markdown Support

The blog supports standard Markdown syntax:

- **Bold** and *italic* text
- `Inline code` and code blocks
- [Links](url)
- Headers (h1-h4)
- Bullet and numbered lists
- Blockquotes
- Tables

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with all posts |
| `/post/<slug>` | GET | View a single post |
| `/create` | GET/POST | Create new post |
| `/post/<slug>/edit` | GET/POST | Edit a post |
| `/post/<slug>/delete` | POST | Delete a post |
| `/post/<slug>/comment` | POST | Add a comment |
| `/post/<slug>/<id>/delete` | POST | Delete a comment |

## Project Structure

```
blog-flask/
├── app.py              # Main Flask application
├── models.py           # Database models
├── templates/
│   ├── index.html      # Home page
│   ├── post.html       # View post
│   ├── create.html     # Create post form
│   ├── edit.html       # Edit post form
│   └── 404.html        # Error page
├── requirements.txt
└── README.md
```

## Database

SQLite database (`blog.db`) is automatically created on first run.

## License

MIT License
