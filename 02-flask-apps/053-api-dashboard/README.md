# API Dashboard

A Flask-based dashboard to manage API keys and monitor API usage statistics.

## Features

- Create and manage API keys
- View API usage statistics
- Monitor request logs
- Track response times
- Error rate monitoring
- Top endpoints and IPs
- Rate limit configuration
- Key expiration management

## Installation

```bash
cd api-dashboard
pip install -r requirements.txt
python app.py
```

## Usage

1. Open http://localhost:5005
2. Create API keys from the Keys page
3. View real-time API statistics on the Dashboard
4. Monitor request logs and performance

## Routes

- `/dashboard` - Main dashboard with stats overview
- `/keys` - Manage API keys
- `/keys/create` - Create new API key
- `/keys/<key_id>/toggle` - Enable/disable key
- `/keys/<key_id>/delete` - Delete API key
- `/logs` - View request logs
- `/endpoints` - List API endpoints
- `/stats` - Detailed statistics
- `/api/simulate` - Simulate API request (POST)

## Database

Uses SQLite database `api_dashboard.db` with tables:
- `api_keys` - API key management
- `api_logs` - Request logs
- `endpoints` - API endpoint registry
