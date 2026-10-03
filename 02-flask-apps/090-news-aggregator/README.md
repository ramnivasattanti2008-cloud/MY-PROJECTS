# NewsHub - News Aggregator

A news reader application using Flask and NewsAPI.org.

## Features

- Browse top headlines by category (General, Business, Technology, etc.)
- Search for specific topics
- Bookmark articles for later reading
- Responsive card layout with images
- Persistent bookmarks using localStorage

## Setup

1. Get a free API key from [newsapi.org](https://newsapi.org/register)

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your API key:
```bash
# Windows
set NEWS_API_KEY=your_api_key_here

# Linux/Mac
export NEWS_API_KEY=your_api_key_here
```

5. Run the application:
```bash
python app.py
```

6. Open http://localhost:5002 in your browser

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/headlines?category=<cat>` - Get top headlines
- `GET /api/search?q=<query>` - Search articles

## NewsAPI Free Tier Limits

- 100 requests per day
- Only returns articles from the last month
- Limited to US and UK sources for top headlines

## Technologies

- Flask 3.0
- NewsAPI.org
- Vanilla JavaScript
