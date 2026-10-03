# CryptoTracker

A real-time cryptocurrency price tracker using Flask and the CoinGecko API.

## Features

- Live cryptocurrency prices for top coins
- Price change indicators (1h, 24h, 7d)
- Interactive sparkline charts showing 7-day trends
- Market cap and rank display
- Responsive grid layout

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to: http://localhost:5001

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/cryptos?limit=N` - Get top N cryptocurrencies
- `GET /api/crypto/<id>` - Get price history for a specific coin

## Technologies

- Flask 3.0
- CoinGecko API (free, no key required)
- Vanilla JavaScript for frontend

## Rate Limits

CoinGecko free tier allows ~10-30 requests per minute. The app includes basic error handling for rate limits.
