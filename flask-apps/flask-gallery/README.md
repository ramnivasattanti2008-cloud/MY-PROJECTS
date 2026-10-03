# Flask Image Gallery

A simple image gallery application with categories.

## Features

- Upload images with title and description
- Organize images by category
- Filter by category
- Delete images
- Modern grid layout

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Open http://localhost:5000 in your browser.

## Routes

- `/` - View all images (filter by category)
- `/upload` - Upload a new image
- `/delete/<id>` - Delete an image

## Static Files

Images are stored in `static/uploads/`. Make sure this directory exists.
