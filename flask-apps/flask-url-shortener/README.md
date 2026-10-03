# Flask URL Shortener

A modern URL shortener with custom short codes, click tracking, and analytics dashboard.

## Features

- Create shortened URLs with custom short codes
- Track clicks with detailed analytics
- View statistics for each URL
- Dark theme UI
- RESTful API endpoints

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

The app will start on `http://localhost:5001`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create` | Create a shortened URL |
| GET | `/<short_code>` | Redirect to original URL |
| GET | `/dashboard` | View analytics dashboard |
| GET | `/stats/<short_code>` | View URL statistics |
| GET | `/api/urls` | List all URLs (JSON) |
| DELETE | `/api/urls/<short_code>` | Delete a URL |

## Routes

- `/` - Home page with URL shortener form
- `/dashboard` - Analytics dashboard
- `/stats/<short_code>` - Detailed stats for a URL

## Database

SQLite database (`urlshortener.db`) is automatically created on first run.
