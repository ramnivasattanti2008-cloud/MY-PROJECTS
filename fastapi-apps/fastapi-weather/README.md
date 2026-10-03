# FastAPI Weather API

A free weather API that proxies Open-Meteo. No API key required.

## Features

- Current weather conditions
- Hourly forecast (up to 7 days)
- Daily forecast (up to 16 days)
- Geocoding (search for cities)
- Reverse geocoding (coordinates to location)
- Multiple units (Celsius/Fahrenheit, km/h/mph)
- Auto-generated API documentation at `/docs`

## Installation

```bash
cd fastapi-weather
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Get Current Weather

```bash
# By coordinates (London)
curl "http://localhost:8000/weather/current?latitude=51.5074&longitude=-0.1278"

# In Fahrenheit
curl "http://localhost:8000/weather/current?latitude=51.5074&longitude=-0.1278&temperature_unit=fahrenheit"

# In mph
curl "http://localhost:8000/weather/current?latitude=51.5074&longitude=-0.1278&wind_speed_unit=mph"
```

### Get Full Forecast

```bash
# Get 7-day forecast with current + daily
curl "http://localhost:8000/weather/forecast?latitude=51.5074&longitude=-0.1278"

# Include hourly data
curl "http://localhost:8000/weather/forecast?latitude=51.5074&longitude=-0.1278&include_hourly=true"

# 3-day forecast
curl "http://localhost:8000/weather/forecast?latitude=51.5074&longitude=-0.1278&forecast_days=3"
```

### Get Hourly Forecast

```bash
# Next 48 hours
curl "http://localhost:8000/weather/forecast/hourly?latitude=51.5074&longitude=-0.1278&hours=48"
```

### Get Daily Forecast

```bash
# Next 5 days
curl "http://localhost:8000/weather/forecast/daily?latitude=51.5074&longitude=-0.1278&days=5"
```

### Search Locations

```bash
# Search for a city
curl "http://localhost:8000/geocoding/search?q=Bangalore"

# Get more results
curl "http://localhost:8000/geocoding/search?q=Delhi&limit=5"
```

### Reverse Geocoding

```bash
# Get location name from coordinates
curl "http://localhost:8000/geocoding/reverse?latitude=12.9716&longitude=77.5946"
```

### Weather Codes

```bash
# Get all weather codes
curl http://localhost:8000/weather/codes
```

## Example Responses

### Current Weather

```json
{
  "latitude": 51.5074,
  "longitude": -0.1278,
  "timezone": "Europe/London",
  "current": {
    "temperature": 15.2,
    "apparent_temperature": 13.8,
    "humidity": 72,
    "precipitation": 0.0,
    "rain": 0.0,
    "snowfall": 0.0,
    "weather_code": 3,
    "weather_description": "Overcast",
    "cloud_cover": 88,
    "wind_speed": 18.5,
    "wind_direction": 225,
    "is_day": true
  }
}
```

### Daily Forecast

```json
{
  "latitude": 51.5074,
  "longitude": -0.1278,
  "timezone": "Europe/London",
  "daily": {
    "time": ["2024-01-15", "2024-01-16"],
    "temperature_max": [15.2, 16.1],
    "temperature_min": [8.5, 9.2],
    "apparent_temperature_max": [13.8, 14.5],
    "apparent_temperature_min": [6.2, 7.1],
    "sunrise": ["2024-01-15T08:02", "2024-01-16T08:01"],
    "sunset": ["2024-01-15T16:24", "2024-01-16T16:26"],
    "precipitation_sum": [2.5, 0.0],
    "precipitation_probability_max": [65, 12],
    "weather_code": [61, 0],
    "wind_speed_max": [22.3, 15.1]
  }
}
```

## Weather Codes

| Code | Description |
|------|-------------|
| 0 | Clear sky |
| 1 | Mainly clear |
| 2 | Partly cloudy |
| 3 | Overcast |
| 45 | Fog |
| 51-57 | Drizzle |
| 61-67 | Rain |
| 71-77 | Snow |
| 80-82 | Rain showers |
| 85-86 | Snow showers |
| 95-99 | Thunderstorm |

## Units

| Parameter | Options |
|-----------|--------|
| Temperature | celsius, fahrenheit |
| Wind speed | kmh, ms, mph, kn |
| Precipitation | mm, inch |

## Use Case Examples

### Get weather for a city (full flow)

```bash
# 1. Search for the city
curl "http://localhost:8000/geocoding/search?q=Berlin"

# 2. Use the coordinates from result
curl "http://localhost:8000/weather/forecast?latitude=52.52&longitude=13.41&include_hourly=true"
```

### Build a weather dashboard

```bash
# Get current weather
curl "http://localhost:8000/weather/current?latitude=40.71&longitude=-74.01"

# Get 7-day forecast
curl "http://localhost:8000/weather/forecast/daily?latitude=40.71&longitude=-74.01"
```

## Project Structure

```
fastapi-weather/
├── main.py           # Main application code
├── requirements.txt  # Python dependencies
├── README.md         # This file
```

## License

MIT
