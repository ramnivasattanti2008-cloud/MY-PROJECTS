#!/usr/bin/env python3
"""
Weather CLI - Get weather information for any city using Open-Meteo API.

Usage:
    Current weather:  python weather-cli.py "Bangalore"
    With details:    python weather-cli.py "Bangalore" --detailed
    Specific units:   python weather-cli.py "Bangalore" --units metric

No API key required - uses the free Open-Meteo API.
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class WeatherData:
    """Stores weather information for a location."""
    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: int
    weather_code: int
    weather_description: str
    is_day: bool
    uv_index: float
    visibility: float
    cloud_cover: int


# Weather code descriptions based on WMO codes
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
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
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def geocode_city(city: str) -> Optional[dict]:
    """
    Get coordinates for a city using Open-Meteo Geocoding API.

    Args:
        city: Name of the city to geocode

    Returns:
        Dictionary with location data or None if not found
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error geocoding city: {e}", file=sys.stderr)
        return None


def get_weather(lat: float, lon: float, units: str = "metric") -> Optional[dict]:
    """
    Get weather data for coordinates using Open-Meteo API.

    Args:
        lat: Latitude
        lon: Longitude
        units: Unit system (metric, imperial, or metric+scandinavian)

    Returns:
        Dictionary with weather data or None if request fails
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "is_day",
        ],
        "hourly": ["uv_index", "visibility"],
        "daily": [],
        "timezone": "auto",
        "forecast_days": 1,
        "temperature_unit": units,
        "wind_speed_unit": "kmh",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}", file=sys.stderr)
        return None


def parse_weather_data(geo_data: dict, weather_data: dict) -> WeatherData:
    """Parse API responses into a WeatherData object."""
    current = weather_data["current"]
    hourly = weather_data["hourly"]

    # Get UV index (first hour)
    uv_index = hourly.get("uv_index", [0])[0] if hourly.get("uv_index") else 0
    visibility = hourly.get("visibility", [0])[0] if hourly.get("visibility") else 0

    weather_code = current.get("weather_code", 0)

    return WeatherData(
        city=geo_data.get("name", "Unknown"),
        country=geo_data.get("country", "Unknown"),
        latitude=geo_data.get("latitude", 0),
        longitude=geo_data.get("longitude", 0),
        temperature=current.get("temperature_2m", 0),
        feels_like=current.get("apparent_temperature", 0),
        humidity=int(current.get("relative_humidity_2m", 0)),
        pressure=int(current.get("surface_pressure", 0)),
        wind_speed=current.get("wind_speed_10m", 0),
        wind_direction=int(current.get("wind_direction_10m", 0)),
        weather_code=weather_code,
        weather_description=WEATHER_CODES.get(weather_code, "Unknown"),
        is_day=bool(current.get("is_day", True)),
        uv_index=uv_index,
        visibility=visibility / 1000 if visibility else 0,  # Convert to km
        cloud_cover=0,  # Not in current API call
    )


def format_weather(weather: WeatherData, units: str = "metric") -> str:
    """Format weather data for display."""
    temp_unit = "C" if units == "metric" else "F"
    wind_unit = "km/h" if units == "metric" else "mph"
    speed_multiplier = 1 if units == "metric" else 1.60934
    wind_speed = weather.wind_speed * speed_multiplier if units == "imperial" else weather.wind_speed

    day_night = "Day" if weather.is_day else "Night"

    lines = [
        "",
        f"  Weather in {weather.city}, {weather.country}",
        f"  {'─' * 40}",
        f"  {weather.weather_description}",
        f"  {day_night}",
        "",
        f"  Temperature:    {weather.temperature:.1f}°{temp_unit}",
        f"  Feels like:     {weather.feels_like:.1f}°{temp_unit}",
        f"  Humidity:       {weather.humidity}%",
        f"  Pressure:       {weather.pressure} hPa",
        "",
        f"  Wind:          {wind_speed:.1f} {wind_unit} from {weather.wind_direction}°",
        f"  UV Index:       {weather.uv_index:.1f}",
        f"  Visibility:     {weather.visibility:.1f} km",
        "",
        f"  Coordinates:   {weather.latitude:.4f}, {weather.longitude:.4f}",
        "",
    ]

    return "\n".join(lines)


def format_detailed_weather(weather: WeatherData, units: str = "metric") -> str:
    """Format detailed weather information."""
    temp_unit = "C" if units == "metric" else "F"
    wind_unit = "km/h" if units == "metric" else "mph"
    speed_multiplier = 1 if units == "metric" else 1.60934
    wind_speed = weather.wind_speed * speed_multiplier if units == "imperial" else weather.wind_speed

    # Wind direction compass
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    compass_idx = round(weather.wind_direction / 22.5) % 16
    compass_dir = directions[compass_idx]

    day_night = "Day" if weather.is_day else "Night"

    # UV risk level
    uv = weather.uv_index
    if uv < 3:
        uv_risk = "Low"
    elif uv < 6:
        uv_risk = "Moderate"
    elif uv < 8:
        uv_risk = "High"
    elif uv < 11:
        uv_risk = "Very High"
    else:
        uv_risk = "Extreme"

    lines = [
        "",
        f"  ╔══════════════════════════════════════════╗",
        f"  ║     WEATHER REPORT: {weather.city:<20} ║",
        f"  ╚══════════════════════════════════════════╝",
        "",
        f"  Location",
        f"  ─────────────────────────────────────────",
        f"  City:        {weather.city}",
        f"  Country:     {weather.country}",
        f"  Coordinates: {weather.latitude:.6f}, {weather.longitude:.6f}",
        f"  Time:        {day_night}",
        "",
        f"  Current Conditions",
        f"  ─────────────────────────────────────────",
        f"  Weather:     {weather.weather_description}",
        f"  Temperature: {weather.temperature:.1f}°{temp_unit}",
        f"  Feels like:  {weather.feels_like:.1f}°{temp_unit}",
        "",
        f"  Atmosphere",
        f"  ─────────────────────────────────────────",
        f"  Humidity:    {weather.humidity}%",
        f"  Pressure:    {weather.pressure} hPa",
        f"  Visibility:  {weather.visibility:.1f} km",
        "",
        f"  Wind",
        f"  ─────────────────────────────────────────",
        f"  Speed:       {wind_speed:.1f} {wind_unit}",
        f"  Direction:   {compass_dir} ({weather.wind_direction}°)",
        "",
        f"  Sun & UV",
        f"  ─────────────────────────────────────────",
        f"  UV Index:    {uv:.1f} ({uv_risk})",
        "",
    ]

    return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Get weather information for any city using Open-Meteo API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "city",
        nargs="?",
        help="Name of the city to get weather for",
    )
    parser.add_argument(
        "--detailed", "-d",
        action="store_true",
        help="Show detailed weather information",
    )
    parser.add_argument(
        "--units", "-u",
        choices=["metric", "imperial"],
        default="metric",
        help="Temperature units (metric=Celsius, imperial=Fahrenheit)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output weather data as JSON",
    )

    args = parser.parse_args()

    # Prompt for city if not provided
    if not args.city:
        args.city = input("Enter city name: ").strip()
        if not args.city:
            print("Error: No city provided", file=sys.stderr)
            return 1

    print(f"Searching for: {args.city}")

    # Geocode the city
    geo_data = geocode_city(args.city)
    if not geo_data:
        print(f"Error: City '{args.city}' not found", file=sys.stderr)
        return 1

    # Get weather data
    weather_data = get_weather(geo_data["latitude"], geo_data["longitude"], args.units)
    if not weather_data:
        print("Error: Could not fetch weather data", file=sys.stderr)
        return 1

    # Parse and display weather
    weather = parse_weather_data(geo_data, weather_data)

    if args.json:
        output = {
            "city": weather.city,
            "country": weather.country,
            "latitude": weather.latitude,
            "longitude": weather.longitude,
            "temperature": weather.temperature,
            "temperature_unit": "C" if args.units == "metric" else "F",
            "feels_like": weather.feels_like,
            "humidity": weather.humidity,
            "pressure": weather.pressure,
            "wind_speed": weather.wind_speed,
            "wind_direction": weather.wind_direction,
            "weather_code": weather.weather_code,
            "weather_description": weather.weather_description,
            "is_day": weather.is_day,
            "uv_index": weather.uv_index,
            "visibility_km": weather.visibility,
        }
        print(json.dumps(output, indent=2))
    elif args.detailed:
        print(format_detailed_weather(weather, args.units))
    else:
        print(format_weather(weather, args.units))

    return 0


if __name__ == "__main__":
    sys.exit(main())
