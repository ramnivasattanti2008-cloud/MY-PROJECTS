# Flask Wiki

A dark-themed collaborative wiki built with Flask and Markdown.

## Features

- Create and edit wiki pages
- Full Markdown support with code highlighting
- Search functionality
- Sidebar navigation
- Category organization
- 404 page handling
- Dark amber theme

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## Routes

- `/` - Home page
- `/wiki/<slug>` - View a wiki page
- `/create` - Create new page
- `/edit/<slug>` - Edit existing page
- `/search?q=<query>` - Search pages

## Pre-loaded Pages

The wiki comes with sample pages:
- Home - Welcome page
- Flask Guide - Python Flask tutorial
- Markdown Syntax - Markdown reference
