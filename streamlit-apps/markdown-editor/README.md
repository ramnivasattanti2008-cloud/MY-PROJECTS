# Markdown Editor

A Streamlit application for writing Markdown with live preview and HTML export.

## Features

- **Live Preview** - See your Markdown rendered in real-time
- **Export to HTML** - Download your document as a standalone HTML file
- **Theme Support** - Light and dark themes
- **Custom Styling** - Option to include CSS styling in exported HTML
- **Word/Character Count** - Track document statistics
- **Quick Reference** - Built-in Markdown syntax reference

## Installation

```bash
cd markdown-editor
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Run `streamlit run app.py`
2. Opens at `http://localhost:8501`
3. Write Markdown in the left panel
4. See live preview on the right
5. Export to HTML when done

## Markdown Support

- Headers (H1-H6)
- Bold, italic, strikethrough
- Ordered and unordered lists
- Code blocks with syntax highlighting
- Tables
- Blockquotes
- Links and images
- Horizontal rules

## Project Structure

```
markdown-editor/
├── app.py          # Main Streamlit application
├── requirements.txt
└── README.md
```
