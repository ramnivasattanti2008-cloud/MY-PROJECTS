# Weather CLI

A Python CLI tool to get weather information for any city using the free Open-Meteo API.

## Features

- No API key required
- Current weather conditions
- Temperature, humidity, pressure
- Wind speed and direction
- UV index
- Visibility
- Support for Celsius and Fahrenheit
- JSON output option

## Installation

```bash
pip install -r requirements/weather-cli-requirements.txt
```

## Usage

### Basic usage

```bash
python weather-cli.py "Bangalore"
python weather-cli.py "London"
python weather-cli.py "New York"
```

### Interactive mode

```bash
python weather-cli.py
# Enter city name: Tokyo
```

### Detailed output

```bash
python weather-cli.py "Bangalore" --detailed
```

### Temperature units

```bash
# Celsius (default)
python weather-cli.py "Bangalore"

# Fahrenheit
python weather-cli.py "Bangalore" --units imperial
```

### JSON output

```bash
python weather-cli.py "Bangalore" --json
```

## Options

| Option | Description |
|--------|-------------|
| `city` | Name of the city (required unless using interactive mode) |
| `--detailed`, `-d` | Show detailed weather information |
| `--units`, `-u` | Temperature units: `metric` (Celsius) or `imperial` (Fahrenheit) |
| `--json` | Output weather data as JSON |

## Example Output

### Standard Output

```
  Weather in Bangalore, India
  ────────────────────────────────────────
  Clear sky
  Day

  Temperature:    28.5°C
  Feels like:     30.2°C
  Humidity:       65%

  Wind:          12.5 km/h from 180°
  UV Index:       8.5
  Visibility:     10.0 km

  Coordinates:   12.9719, 77.5937
```

### Detailed Output

```
  ╔══════════════════════════════════════════╗
  ║     WEATHER REPORT: Bangalore           ║
  ╚══════════════════════════════════════════╝

  Location
  ─────────────────────────────────────────
  City:        Bangalore
  Country:     India
  Coordinates: 12.971900, 77.593700
  Time:        Day

  Current Conditions
  ─────────────────────────────────────────
  Weather:     Clear sky
  Temperature: 28.5°C
  Feels like:  30.2°C

  Atmosphere
  ─────────────────────────────────────────
  Humidity:    65%
  Pressure:    1013 hPa
  Visibility:  10.0 km

  Wind
  ─────────────────────────────────────────
  Speed:       12.5 km/h
  Direction:   S (180°)

  Sun & UV
  ─────────────────────────────────────────
  UV Index:    8.5 (Very High)
```

## API

Uses the free Open-Meteo API:
- Geocoding: https://geocoding-api.open-meteo.com/v1/search
- Weather: https://api.open-meteo.com/v1/forecast

No API key or registration required.
