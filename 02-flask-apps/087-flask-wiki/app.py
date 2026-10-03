from flask import Flask, render_template, request, redirect, url_for, session
import markdown
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'wiki-secret-key-change-in-production'

# Sample wiki pages
pages = {
    'home': {
        'title': 'Home',
        'content': '''# Welcome to the Wiki

This is a collaborative knowledge base where you can create and edit pages using Markdown.

## Getting Started

1. Create a new page using the form below
2. Write content using Markdown syntax
3. Save and view your page

## Features

- **Markdown Support** - Write content with full Markdown syntax
- **Version History** - Track changes to pages
- **Search** - Find pages quickly
- **Categories** - Organize content by topic

Feel free to explore and contribute!
''',
        'author': 'Admin',
        'last_edited': '2026-09-06',
        'category': 'general'
    },
    'flask-guide': {
        'title': 'Flask Guide',
        'content': '''# Flask Web Framework

Flask is a lightweight WSGI web application framework written in Python.

## Installation

```bash
pip install flask
```

## Basic App

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

## Key Features

- Built-in development server
- RESTful request dispatching
- Jinja2 templating
- Secure cookies
- Extensible architecture
''',
        'author': 'Admin',
        'last_edited': '2026-09-05',
        'category': 'programming'
    },
    'markdown-syntax': {
        'title': 'Markdown Syntax',
        'content': '''# Markdown Syntax Guide

## Headers

# H1
## H2
### H3

## Emphasis

*italic* or _italic_
**bold** or __bold__
~~strikethrough~~

## Lists

Unordered:
- Item 1
- Item 2
  - Nested item

Ordered:
1. First
2. Second
3. Third

## Code

Inline: `code`

Block:
```python
def hello():
    print("Hello")
```

## Links and Images

[Link text](URL)
![Alt text](image-url)

## Blockquotes

> This is a blockquote.
''',
        'author': 'Admin',
        'last_edited': '2026-09-04',
        'category': 'documentation'
    }
}

def render_content(content):
    return markdown.markdown(content, extensions=['fenced_code', 'tables'])

@app.route('/')
def index():
    return redirect(url_for('wiki_page', slug='home'))

@app.route('/wiki/<slug>')
def wiki_page(slug):
    if slug in pages:
        page = pages[slug]
        page['html_content'] = render_content(page['content'])
        return render_template('page.html', page=page, pages=pages)
    return render_template('not_found.html', slug=slug)

@app.route('/create', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        slug = request.form.get('slug').lower().replace(' ', '-')
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category', 'general')
        if slug and title and content:
            pages[slug] = {
                'title': title,
                'content': content,
                'author': 'Anonymous',
                'last_edited': datetime.now().strftime('%Y-%m-%d'),
                'category': category
            }
            return redirect(url_for('wiki_page', slug=slug))
    return render_template('create.html')

@app.route('/edit/<slug>', methods=['GET', 'POST'])
def edit_page(slug):
    if slug not in pages:
        return redirect(url_for('index'))
    if request.method == 'POST':
        pages[slug]['content'] = request.form.get('content')
        pages[slug]['last_edited'] = datetime.now().strftime('%Y-%m-%d')
        return redirect(url_for('wiki_page', slug=slug))
    page = pages[slug]
    page['html_content'] = render_content(page['content'])
    return render_template('edit.html', page=page)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    if query:
        for slug, page in pages.items():
            if query in page['title'].lower() or query in page['content'].lower():
                results.append({'slug': slug, 'title': page['title']})
    return render_template('search.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
