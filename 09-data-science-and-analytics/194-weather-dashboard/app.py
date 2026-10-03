"""
Weather Dashboard - Streamlit Application
Uses Open-Meteo API (free, no API key required)
Shows weather for multiple cities side by side with charts and forecasts
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Optional

# Open-Meteo API base URL
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Popular cities for quick selection
POPULAR_CITIES = {
    "New York": {"latitude": 40.7128, "longitude": -74.0060},
    "London": {"latitude": 51.5074, "longitude": -0.1278},
    "Tokyo": {"latitude": 35.6762, "longitude": 139.6503},
    "Paris": {"latitude": 48.8566, "longitude": 2.3522},
    "Sydney": {"latitude": -33.8688, "longitude": 151.2093},
    "Dubai": {"latitude": 25.2048, "longitude": 55.2708},
    "Singapore": {"latitude": 1.3521, "longitude": 103.8198},
    "Mumbai": {"latitude": 19.0760, "longitude": 72.8777},
    "Delhi": {"latitude": 28.7041, "longitude": 77.1025},
    "Bengaluru": {"latitude": 12.9716, "longitude": 77.5946},
    "Berlin": {"latitude": 52.5200, "longitude": 13.4050},
    "Toronto": {"latitude": 43.6532, "longitude": -79.3832},
    "Los Angeles": {"latitude": 34.0522, "longitude": -118.2437},
    "Moscow": {"latitude": 55.7558, "longitude": 37.6173},
    "Beijing": {"latitude": 39.9042, "longitude": 116.4074},
}


def get_coordinates(city_name: str) -> Optional[dict]:
    """Get coordinates for a city using geocoding API."""
    try:
        response = requests.get(GEOCODING_URL, params={"name": city_name, "count": 1}, timeout=5)
        data = response.json()
        if data.get("results"):
            result = data["results"][0]
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "country": result.get("country", ""),
            }
    except Exception:
        pass
    return None


def get_weather_data(lat: float, lon: float) -> Optional[dict]:
    """Fetch weather data from Open-Meteo API."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max",
        "timezone": "auto",
        "forecast_days": 7,
    }
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None


def get_weather_icon(code: int) -> str:
    """Get emoji icon for weather code."""
    icons = {
        0: "☀️",  # Clear sky
        1: "🌤️",  # Mainly clear
        2: "⛅",  # Partly cloudy
        3: "☁️",  # Overcast
        45: "🌫️",  # Fog
        48: "🌫️",  # Depositing rime fog
        51: "🌧️",  # Light drizzle
        53: "🌧️",  # Moderate drizzle
        55: "🌧️",  # Dense drizzle
        61: "🌧️",  # Slight rain
        63: "🌧️",  # Moderate rain
        65: "🌧️",  # Heavy rain
        71: "🌨️",  # Slight snow
        73: "🌨️",  # Moderate snow
        75: "❄️",  # Heavy snow
        77: "❄️",  # Snow grains
        80: "🌦️",  # Slight rain showers
        81: "🌦️",  # Moderate rain showers
        82: "⛈️",  # Violent rain showers
        85: "🌨️",  # Slight snow showers
        86: "❄️",  # Heavy snow showers
        95: "⛈️",  # Thunderstorm
        96: "⛈️",  # Thunderstorm with slight hail
        99: "⛈️",  # Thunderstorm with heavy hail
    }
    return icons.get(code, "🌡️")


def get_weather_description(code: int) -> str:
    """Get description for weather code."""
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Severe thunderstorm",
    }
    return descriptions.get(code, "Unknown")


def kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius (API returns Celsius by default)."""
    return k


def format_temperature(temp: float, unit: str = "C") -> str:
    """Format temperature with unit."""
    if unit == "F":
        temp = temp * 9/5 + 32
    return f"{temp:.1f}°{unit}"


# Page config
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 2rem; }
    .city-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; color: white; }
    .temp-large { font-size: 3rem; font-weight: bold; }
    .weather-icon { font-size: 4rem; text-align: center; }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-title">🌤️ Weather Dashboard</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("⚙️ Settings")
unit = st.sidebar.radio("Temperature Unit", ["Celsius (°C)", "Fahrenheit (°F)"])
unit_key = "F" if unit == "Fahrenheit (°F)" else "C"

# City input
st.sidebar.subheader("🔍 Search City")
city_input = st.sidebar.text_input("Enter city name", placeholder="e.g., London, Tokyo")
search_col, quick_col = st.sidebar.columns(2)

with search_col:
    if st.button("🔍 Search", use_container_width=True):
        if city_input:
            coords = get_coordinates(city_input)
            if coords:
                st.session_state[f"city_{coords['name']}"] = coords
                st.success(f"Added: {coords['name']}, {coords['country']}")
            else:
                st.error("City not found")

with quick_col:
    st.markdown("**Quick Add:**")

# Quick add popular cities
for city, data in list(POPULAR_CITIES.items())[:6]:
    if st.button(city, key=f"btn_{city}", use_container_width=True):
        st.session_state[f"city_{city}"] = {"name": city, **data}

# Initialize session state for cities
if "cities" not in st.session_state:
    # Default cities on first load
    st.session_state.cities = {
        "New York": POPULAR_CITIES["New York"],
        "London": POPULAR_CITIES["London"],
        "Tokyo": POPULAR_CITIES["Tokyo"],
    }
else:
    # Update cities from session state
    st.session_state.cities = {
        key.replace("city_", ""): val for key, val in st.session_state.items()
        if key.startswith("city_") and isinstance(val, dict)
    }

# Remove cities button
st.sidebar.subheader("📍 Active Cities")
cities_to_remove = []
for city in list(st.session_state.cities.keys()):
    col1, col2 = st.sidebar.columns([4, 1])
    col1.write(f"📍 {city}")
    if col2.button("×", key=f"remove_{city}"):
        cities_to_remove.append(city)

for city in cities_to_remove:
    key_to_remove = f"city_{city}"
    if key_to_remove in st.session_state:
        del st.session_state[key_to_remove]
    if city in st.session_state.cities:
        del st.session_state.cities[city]

# Main content
cities = st.session_state.cities

if not cities:
    st.info("👈 Add cities from the sidebar to see weather data")
else:
    # Fetch data for all cities
    weather_data = {}
    for city, coords in cities.items():
        data = get_weather_data(coords["latitude"], coords["longitude"])
        if data:
            weather_data[city] = data

    if weather_data:
        # Current weather cards
        st.subheader("📊 Current Weather")

        cols = st.columns(len(weather_data)) if weather_data else []

        for idx, (city, data) in enumerate(weather_data.items()):
            with cols[idx]:
                daily = data.get("daily", {})
                hourly = data.get("hourly", {})

                current_temp = daily.get("temperature_2m_max", [0])[0] if daily.get("temperature_2m_max") else 0
                current_code = daily.get("weather_code", [0])[0] if daily.get("weather_code") else 0
                min_temp = daily.get("temperature_2m_min", [0])[0] if daily.get("temperature_2m_min") else 0
                max_temp = daily.get("temperature_2m_max", [0])[0] if daily.get("temperature_2m_max") else 0

                icon = get_weather_icon(current_code)
                desc = get_weather_description(current_code)

                # Create card
                st.markdown(f"""
                <div class="city-card">
                    <h2 style="text-align: center; margin-bottom: 0.5rem;">{icon}</h2>
                    <h3 style="text-align: center; margin-bottom: 1rem;">{city}</h3>
                    <p class="temp-large" style="text-align: center;">{format_temperature(current_temp, unit_key)}</p>
                    <p style="text-align: center; opacity: 0.9;">{desc}</p>
                    <p style="text-align: center; margin-top: 1rem;">
                        H: {format_temperature(max_temp, unit_key)} | L: {format_temperature(min_temp, unit_key)}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Temperature comparison chart
        st.subheader("📈 Temperature Comparison (7-Day Forecast)")

        fig = go.Figure()
        colors = px.colors.qualitative.Set2

        for idx, (city, data) in enumerate(weather_data.items()):
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])

            if unit_key == "F":
                max_temps = [t * 9/5 + 32 for t in max_temps]
                min_temps = [t * 9/5 + 32 for t in min_temps]

            fig.add_trace(go.Scatter(
                x=dates, y=max_temps, name=f"{city} (High)",
                line=dict(color=colors[idx % len(colors)], width=3),
                mode="lines+markers"
            ))
            fig.add_trace(go.Scatter(
                x=dates, y=min_temps, name=f"{city} (Low)",
                line=dict(color=colors[idx % len(colors)], width=1, dash="dot"),
                mode="lines+markers"
            ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=f"Temperature ({unit_key})",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            height=400,
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Precipitation chart
        st.subheader("🌧️ Precipitation Forecast")

        fig2 = go.Figure()
        for idx, (city, data) in enumerate(weather_data.items()):
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            precip = daily.get("precipitation_sum", [])

            fig2.add_trace(go.Bar(
                x=dates, y=precip, name=city,
                marker_color=colors[idx % len(colors)]
            ))

        fig2.update_layout(
            xaxis_title="Date",
            yaxis_title="Precipitation (mm)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            height=350,
            template="plotly_white",
            barmode="group"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Detailed city view
        st.markdown("---")
        st.subheader("🔍 Detailed City View")

        selected_city = st.selectbox("Select a city for detailed forecast", list(weather_data.keys()))

        if selected_city:
            data = weather_data[selected_city]
            daily = data.get("daily", {})
            hourly = data.get("hourly", {})

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Max Temp", format_temperature(daily.get("temperature_2m_max", [0])[0], unit_key))
            with col2:
                st.metric("Min Temp", format_temperature(daily.get("temperature_2m_min", [0])[0], unit_key))
            with col3:
                st.metric("Total Precipitation", f"{sum(daily.get('precipitation_sum', [])):.1f} mm")
            with col4:
                st.metric("Max Wind", f"{max(daily.get('wind_speed_10m_max', [0])):.1f} km/h")

            # 7-day forecast table
            st.subheader("📅 7-Day Forecast")

            forecast_df = pd.DataFrame({
                "Date": daily.get("time", []),
                "Weather": [f"{get_weather_icon(code)} {get_weather_description(code)}"
                           for code in daily.get("weather_code", [])],
                f"High ({unit_key})": [f"{t:.1f}°" for t in daily.get("temperature_2m_max", [])],
                f"Low ({unit_key})": [f"{t:.1f}°" for t in daily.get("temperature_2m_min", [])],
                "Precipitation": [f"{p:.1f} mm" for p in daily.get("precipitation_sum", [])],
            })

            st.dataframe(forecast_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("""
---
<p style="text-align: center; color: #888;">
    Weather data provided by <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a> | No API key required
</p>
""", unsafe_allow_html=True)
