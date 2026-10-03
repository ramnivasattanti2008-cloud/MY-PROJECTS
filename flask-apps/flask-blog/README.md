# Blog Flask App

A Flask blog application with markdown support and comments.

## Features

- Create, edit, and delete posts
- Full Markdown support (tables, code blocks, blockquotes)
- Comment system with author names
- Clean, readable typography
- SQLite persistence

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Run

Visit `http://localhost:5000`

The database file `blog.db` will be created automatically.

## Markdown Syntax

- **Bold**: `**text**`
- *Italic*: `*text*`
- `Code`: backticks
- Code blocks: triple backticks with language
- Blockquotes: `>`
- Lists: `- item`
- Tables: standard markdown tables
