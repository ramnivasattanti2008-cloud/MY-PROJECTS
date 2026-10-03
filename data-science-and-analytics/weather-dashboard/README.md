# Weather Dashboard

A beautiful Streamlit application that displays weather information for multiple cities side by side, using the free Open-Meteo API (no API key required).

## Features

- **Multiple City Support**: Compare weather for up to 6 cities simultaneously
- **7-Day Forecasts**: View detailed forecasts for each city
- **Interactive Charts**: Temperature and precipitation comparison charts using Plotly
- **Weather Icons**: Visual weather indicators for current conditions
- **Fahrenheit/Celsius Toggle**: Switch between temperature units
- **Quick City Selection**: Pre-configured popular cities for fast access
- **Responsive Design**: Clean, modern UI with gradient cards

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
# Run the Streamlit app
streamlit run app.py

# Or with a specific port
streamlit run app.py --server.port 8501
```

The dashboard will open in your browser at http://localhost:8500

## Usage

1. **Add Cities**: Use the sidebar to search for cities or select from popular cities
2. **Remove Cities**: Click the × button next to any city to remove it
3. **Toggle Units**: Switch between Celsius and Fahrenheit in the sidebar
4. **View Details**: Select a city from the dropdown to see detailed metrics
5. **Compare Charts**: View temperature and precipitation comparison charts

## API

This app uses the **Open-Meteo API**, a free weather API that requires no API key.

### Endpoints Used

- **Geocoding**: `https://geocoding-api.open-meteo.com/v1/search`
- **Weather**: `https://api.open-meteo.com/v1/forecast`

## Project Structure

```
weather-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

## Dependencies

- **Streamlit**: Web app framework
- **Requests**: HTTP library for API calls
- **Pandas**: Data manipulation
- **Plotly**: Interactive charts

## Screenshots

The dashboard features:
- Gradient weather cards showing current conditions
- Side-by-side city comparison
- Temperature trend line charts
- Precipitation bar charts
- Detailed 7-day forecast tables
