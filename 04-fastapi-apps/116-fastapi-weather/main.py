"""
FastAPI Weather API - Proxies Open-Meteo (free, no API key required)
Endpoints: Current weather, hourly forecast, daily forecast
"""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import httpx

# Open-Meteo API base URL
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1"

# FastAPI App
app = FastAPI(
    title="Weather API",
    description="Weather API proxying Open-Meteo. Free, no API key required.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models for responses
class CurrentWeather(BaseModel):
    temperature: float = Field(..., description="Temperature in Celsius")
    apparent_temperature: float = Field(..., description="Feels-like temperature")
    humidity: int = Field(..., ge=0, le=100, description="Relative humidity %")
    precipitation: float = Field(default=0, description="Precipitation in mm")
    rain: float = Field(default=0, description="Rain in mm")
    snowfall: float = Field(default=0, description="Snowfall in cm")
    weather_code: int = Field(..., description="WMO weather code")
    weather_description: str = Field(..., description="Human-readable weather")
    cloud_cover: int = Field(..., ge=0, le=100, description="Cloud cover %")
    wind_speed: float = Field(..., description="Wind speed km/h")
    wind_direction: int = Field(..., ge=0, le=360, description="Wind direction degrees")
    is_day: bool = Field(..., description="Day or night")

class HourlyForecast(BaseModel):
    time: List[str] = Field(..., description="Timestamps")
    temperature: List[float] = Field(..., description="Temperature in Celsius")
    apparent_temperature: List[float] = Field(..., description="Feels-like temperature")
    humidity: List[int] = Field(..., description="Relative humidity %")
    precipitation_probability: List[int] = Field(..., description="Precipitation probability %")
    precipitation: List[float] = Field(..., description="Precipitation in mm")
    weather_code: List[int] = Field(..., description="WMO weather codes")
    cloud_cover: List[int] = Field(..., description="Cloud cover %")
    wind_speed: List[float] = Field(..., description="Wind speed km/h")

class DailyForecast(BaseModel):
    time: List[str] = Field(..., description="Dates")
    temperature_max: List[float] = Field(..., description="Max temperature Celsius")
    temperature_min: List[float] = Field(..., description="Min temperature Celsius")
    apparent_temperature_max: List[float] = Field(..., description="Max feels-like temp")
    apparent_temperature_min: List[float] = Field(..., description="Min feels-like temp")
    sunrise: List[str] = Field(..., description="Sunrise times")
    sunset: List[str] = Field(..., description="Sunset times")
    precipitation_sum: List[float] = Field(..., description="Total precipitation mm")
    precipitation_probability_max: List[int] = Field(..., description="Max precipitation prob %")
    weather_code: List[int] = Field(..., description="WMO weather codes")
    wind_speed_max: List[float] = Field(..., description="Max wind speed km/h")

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    current: CurrentWeather
    hourly: Optional[HourlyForecast] = None
    daily: Optional[DailyForecast] = None
    model_config = ConfigDict(from_attributes=True)

class GeocodingResult(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    country: str
    admin1: Optional[str] = None
    admin2: Optional[str] = None
    timezone: str

class ForecastParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    current: bool = Field(default=True, description="Include current weather")
    hourly: bool = Field(default=False, description="Include hourly forecast")
    daily: bool = Field(default=False, description="Include daily forecast")
    temperature_unit: str = Field(default="celsius", pattern="^(celsius|fahrenheit)$")
    wind_speed_unit: str = Field(default="kmh", pattern="^(kmh|ms|mph|kn)$")
    precipitation_unit: str = Field(default="mm", pattern="^(mm|inch)$")
    timezone: str = Field(default="auto")
    forecast_days: int = Field(default=7, ge=1, le=16)
    past_days: int = Field(default=0, ge=0, le=92)

# Weather code descriptions (WMO Code 0-99)
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
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
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
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

def get_weather_description(code: int) -> str:
    """Get human-readable weather description from WMO code"""
    return WEATHER_CODES.get(code, f"Unknown ({code})")

async def fetch_weather(params: dict) -> dict:
    """Fetch weather data from Open-Meteo API"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{OPEN_METEO_BASE_URL}/forecast", params=params)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Open-Meteo API error: {response.status_code}"
            )
        return response.json()

def parse_current_weather(data: dict) -> CurrentWeather:
    """Parse current weather from API response"""
    current = data.get("current", {})
    return CurrentWeather(
        temperature=current.get("temperature_2m", 0),
        apparent_temperature=current.get("apparent_temperature", 0),
        humidity=current.get("relative_humidity_2m", 0),
        precipitation=current.get("precipitation", 0),
        rain=current.get("rain", 0),
        snowfall=current.get("snowfall", 0),
        weather_code=current.get("weather_code", 0),
        weather_description=get_weather_description(current.get("weather_code", 0)),
        cloud_cover=current.get("cloud_cover", 0),
        wind_speed=current.get("wind_speed_10m", 0),
        wind_direction=current.get("wind_direction_10m", 0),
        is_day=current.get("is_day", 1) == 1
    )

def parse_hourly_forecast(data: dict) -> HourlyForecast:
    """Parse hourly forecast from API response"""
    hourly = data.get("hourly", {})
    return HourlyForecast(
        time=hourly.get("time", []),
        temperature=hourly.get("temperature_2m", []),
        apparent_temperature=hourly.get("apparent_temperature", []),
        humidity=hourly.get("relative_humidity_2m", []),
        precipitation_probability=hourly.get("precipitation_probability", []),
        precipitation=hourly.get("precipitation", []),
        weather_code=hourly.get("weather_code", []),
        cloud_cover=hourly.get("cloud_cover", []),
        wind_speed=hourly.get("wind_speed_10m", [])
    )

def parse_daily_forecast(data: dict) -> DailyForecast:
    """Parse daily forecast from API response"""
    daily = data.get("daily", {})
    return DailyForecast(
        time=daily.get("time", []),
        temperature_max=daily.get("temperature_2m_max", []),
        temperature_min=daily.get("temperature_2m_min", []),
        apparent_temperature_max=daily.get("apparent_temperature_max", []),
        apparent_temperature_min=daily.get("apparent_temperature_min", []),
        sunrise=daily.get("sunrise", []),
        sunset=daily.get("sunset", []),
        precipitation_sum=daily.get("precipitation_sum", []),
        precipitation_probability_max=daily.get("precipitation_probability_max", []),
        weather_code=daily.get("weather_code", []),
        wind_speed_max=daily.get("wind_speed_10m_max", [])
    )

# ==================== API ENDPOINTS ====================

@app.get("/", tags=["Info"])
async def root():
    """API information"""
    return {
        "name": "Weather API",
        "version": "1.0.0",
        "description": "Free weather API proxying Open-Meteo",
        "docs": "/docs",
        "endpoints": {
            "current": "/weather/current?latitude=X&longitude=Y",
            "forecast": "/weather/forecast?latitude=X&longitude=Y",
            "search": "/geocoding/search?q=CityName",
            "weather_codes": "/weather/codes"
        }
    }

@app.get("/weather/codes", tags=["Weather"])
async def get_weather_codes():
    """Get all WMO weather codes with descriptions"""
    return [
        {"code": code, "description": desc}
        for code, desc in WEATHER_CODES.items()
    ]

@app.get("/weather/current", response_model=WeatherResponse, tags=["Weather"])
async def get_current_weather(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude"),
    timezone: str = Query("auto", description="Timezone (auto for local)"),
    temperature_unit: str = Query("celsius", pattern="^(celsius|fahrenheit)$"),
    wind_speed_unit: str = Query("kmh", pattern="^(kmh|ms|mph|kn)$"),
):
    """
    Get current weather for a location.

    No API key required - uses Open-Meteo's free API.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "precipitation", "rain", "snowfall", "weather_code",
            "cloud_cover", "wind_speed_10m", "wind_direction_10m", "is_day"
        ],
        "timezone": timezone,
        "temperature_unit": temperature_unit,
        "wind_speed_unit": wind_speed_unit,
    }

    data = await fetch_weather(params)

    return WeatherResponse(
        latitude=data["latitude"],
        longitude=data["longitude"],
        timezone=data["timezone"],
        current=parse_current_weather(data)
    )

@app.get("/weather/forecast", response_model=WeatherResponse, tags=["Weather"])
async def get_weather_forecast(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude"),
    include_current: bool = Query(True, description="Include current weather"),
    include_hourly: bool = Query(False, description="Include hourly forecast"),
    include_daily: bool = Query(True, description="Include daily forecast"),
    timezone: str = Query("auto", description="Timezone"),
    temperature_unit: str = Query("celsius", pattern="^(celsius|fahrenheit)$"),
    wind_speed_unit: str = Query("kmh", pattern="^(kmh|ms|mph|kn)$"),
    precipitation_unit: str = Query("mm", pattern="^(mm|inch)$"),
    forecast_days: int = Query(7, ge=1, le=16, description="Forecast days (1-16)"),
    past_days: int = Query(0, ge=0, le=92, description="Past days to include (0-92)"),
):
    """
    Get weather forecast for a location.

    - include_current: Current conditions
    - include_hourly: Hourly data for each day (24 hours)
    - include_daily: Daily summaries
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "temperature_unit": temperature_unit,
        "wind_speed_unit": wind_speed_unit,
        "precipitation_unit": precipitation_unit,
        "forecast_days": forecast_days,
        "past_days": past_days,
    }

    # Build current parameters
    if include_current:
        params["current"] = [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "precipitation", "rain", "snowfall", "weather_code",
            "cloud_cover", "wind_speed_10m", "wind_direction_10m", "is_day"
        ]

    # Build hourly parameters
    if include_hourly:
        params["hourly"] = [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "precipitation", "precipitation_probability", "weather_code",
            "cloud_cover", "wind_speed_10m"
        ]

    # Build daily parameters
    if include_daily:
        params["daily"] = [
            "temperature_2m_max", "temperature_2m_min",
            "apparent_temperature_max", "apparent_temperature_min",
            "sunrise", "sunset", "precipitation_sum",
            "precipitation_probability_max", "weather_code", "wind_speed_10m_max"
        ]

    data = await fetch_weather(params)

    response = WeatherResponse(
        latitude=data["latitude"],
        longitude=data["longitude"],
        timezone=data["timezone"],
        current=parse_current_weather(data) if include_current else None,
        hourly=parse_hourly_forecast(data) if include_hourly else None,
        daily=parse_daily_forecast(data) if include_daily else None
    )

    return response

@app.get("/weather/forecast/hourly", response_model=HourlyForecast, tags=["Weather"])
async def get_hourly_forecast(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    hours: int = Query(24, ge=1, le=168, description="Hours of forecast (max 168 = 7 days)"),
    timezone: str = Query("auto"),
    temperature_unit: str = Query("celsius", pattern="^(celsius|fahrenheit)$"),
):
    """Get hourly forecast for the next N hours"""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "precipitation", "precipitation_probability", "weather_code",
            "cloud_cover", "wind_speed_10m"
        ],
        "forecast_days": min(7, (hours + 23) // 24),
        "timezone": timezone,
        "temperature_unit": temperature_unit,
    }

    data = await fetch_weather(params)
    return parse_hourly_forecast(data)

@app.get("/weather/forecast/daily", response_model=DailyForecast, tags=["Weather"])
async def get_daily_forecast(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    days: int = Query(7, ge=1, le=16),
    timezone: str = Query("auto"),
    temperature_unit: str = Query("celsius", pattern="^(celsius|fahrenheit)$"),
):
    """Get daily forecast for the next N days"""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max", "temperature_2m_min",
            "apparent_temperature_max", "apparent_temperature_min",
            "sunrise", "sunset", "precipitation_sum",
            "precipitation_probability_max", "weather_code", "wind_speed_10m_max"
        ],
        "forecast_days": days,
        "timezone": timezone,
        "temperature_unit": temperature_unit,
    }

    data = await fetch_weather(params)
    return parse_daily_forecast(data)

# ==================== GEOCODING ====================

@app.get("/geocoding/search", response_model=List[GeocodingResult], tags=["Geocoding"])
async def search_locations(
    q: str = Query(..., min_length=2, description="Search query (city name)"),
    limit: int = Query(10, ge=1, le=100, description="Max results"),
    language: str = Query("en", description="Response language"),
):
    """
    Search for locations by name.

    Use this to find latitude/longitude for a city.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": q,
                "count": limit,
                "language": language,
                "format": "json"
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Geocoding API error"
            )

        data = response.json()
        results = data.get("results", [])

        return [
            GeocodingResult(
                id=r["id"],
                name=r["name"],
                latitude=r["latitude"],
                longitude=r["longitude"],
                country=r.get("country", ""),
                admin1=r.get("admin1"),
                admin2=r.get("admin2"),
                timezone=r.get("timezone", "")
            )
            for r in results
        ]

@app.get("/geocoding/reverse", response_model=GeocodingResult, tags=["Geocoding"])
async def reverse_geocode(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    """
    Get location name from coordinates.

    Finds the nearest named location to the given coordinates.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": latitude,
                "lon": longitude,
                "format": "json"
            },
            headers={"User-Agent": "WeatherAPI/1.0"}
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Reverse geocoding error"
            )

        data = response.json()
        if not data or "error" in data:
            raise HTTPException(status_code=404, detail="Location not found")

        address = data.get("address", {})

        return GeocodingResult(
            id=0,
            name=address.get("city") or address.get("town") or address.get("village") or data.get("display_name", ""),
            latitude=latitude,
            longitude=longitude,
            country=address.get("country", ""),
            admin1=address.get("state"),
            admin2=address.get("county"),
            timezone=""
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
