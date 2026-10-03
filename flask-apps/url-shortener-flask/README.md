# URL Shortener Flask Application

A simple URL shortener with click tracking and analytics dashboard.

## Features

- Shorten any URL to a 6-character code
- Track click counts for each URL
- Analytics dashboard with statistics
- Recent clicks log with IP and user agent
- REST API for programmatic access
- Modern dark theme UI

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will run at `http://localhost:5000`

## API Endpoints

### Create Short URL
```
POST /api/shorten
Content-Type: application/json

{"url": "https://example.com/very/long/url"}
```

### Get URL Stats
```
GET /api/stats/<short_code>
```

## Project Structure

```
url-shortener-flask/
├── app.py              # Main Flask application
├── templates/
│   ├── index.html      # Home page
│   └── stats.html      # Analytics dashboard
├── requirements.txt
└── README.md
```

## Database

SQLite database (`urlshortener.db`) is automatically created on first run.

## License

MIT License
