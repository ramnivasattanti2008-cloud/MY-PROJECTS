# Flask CMS

Simple CMS with pages, posts, and basic admin panel.

## Setup

```bash
cd flask-cms
pip install -r requirements.txt
python app.py
```

## Features

- Static pages with slugs
- Blog posts with publish toggle
- Admin panel for managing content
- SQLite database
- Automatic sample content on first run

## Routes

Public:
- `/` - Blog post listing
- `/page/<slug>` - Static page view
- `/post/<slug>` - Blog post view

Admin:
- `/admin` - Admin dashboard
- `/admin/page/new` - Create page
- `/admin/post/new` - Create post
- `/admin/post/<id>/toggle` - Toggle publish status
- `/admin/page/<id>/delete` - Delete page
- `/admin/post/<id>/delete` - Delete post

## Database

Uses SQLite (`cms.db`). Auto-creates tables and sample content on first run.
