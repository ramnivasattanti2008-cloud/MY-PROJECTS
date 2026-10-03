# Link Vault

A link bookmarking and organization app. Save URLs with titles, descriptions, and tags. Search, filter, and track visits.

## Features

- Add links with URL, title, and description
- Tag links with multiple tags
- Search links by title, URL, description, or tags
- Filter by tag
- Mark favorites
- Track visit counts
- Collection statistics
- Pre-seeded demo links

## Tech Stack

- **Backend**: Flask, Flask-CORS, SQLite
- **Frontend**: React, TypeScript
- **Database**: SQLite (auto-created with demo data)

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API runs on `http://localhost:5005`

### Frontend

```bash
cd frontend
npm install
npm start
```

The app runs on `http://localhost:3004`

## Demo Data

Pre-seeded with links to popular developer resources:
- GitHub, Stack Overflow, MDN Web Docs, Flask, React

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/links` | List all links |
| POST | `/api/links` | Add a new link |
| GET | `/api/links/<id>` | Get link details |
| PUT | `/api/links/<id>` | Update a link |
| DELETE | `/api/links/<id>` | Delete a link |
| POST | `/api/links/<id>/visit` | Track a visit |
| POST | `/api/links/<id>/favorite` | Toggle favorite |
| GET | `/api/tags` | List all tags with counts |
| GET | `/api/stats` | Get collection statistics |

## Query Parameters

- `?search=<term>` - Search by title, description, URL, or tags
- `?tag=<tagname>` - Filter by tag
- `?favorites=true` - Show only favorites
