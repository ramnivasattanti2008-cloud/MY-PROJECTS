import { useState, useEffect } from 'react';

interface WeatherData {
  temperature: number;
  humidity: number;
  windSpeed: number;
  weatherCode: number;
  isDay: boolean;
}

interface GeocodingResult {
  name: string;
  country: string;
  latitude: number;
  longitude: number;
}

const WEATHER_CODES: Record<number, { description: string; icon: string }> = {
  0: { description: 'Clear sky', icon: '☀️' },
  1: { description: 'Mainly clear', icon: '🌤️' },
  2: { description: 'Partly cloudy', icon: '⛅' },
  3: { description: 'Overcast', icon: '☁️' },
  45: { description: 'Foggy', icon: '🌫️' },
  48: { description: 'Depositing rime fog', icon: '🌫️' },
  51: { description: 'Light drizzle', icon: '🌧️' },
  53: { description: 'Moderate drizzle', icon: '🌧️' },
  55: { description: 'Dense drizzle', icon: '🌧️' },
  61: { description: 'Slight rain', icon: '🌧️' },
  63: { description: 'Moderate rain', icon: '🌧️' },
  65: { description: 'Heavy rain', icon: '🌧️' },
  71: { description: 'Slight snow', icon: '🌨️' },
  73: { description: 'Moderate snow', icon: '🌨️' },
  75: { description: 'Heavy snow', icon: '❄️' },
  77: { description: 'Snow grains', icon: '❄️' },
  80: { description: 'Slight rain showers', icon: '🌦️' },
  81: { description: 'Moderate rain showers', icon: '🌦️' },
  82: { description: 'Violent rain showers', icon: '🌦️' },
  85: { description: 'Slight snow showers', icon: '🌨️' },
  86: { description: 'Heavy snow showers', icon: '🌨️' },
  95: { description: 'Thunderstorm', icon: '⛈️' },
  96: { description: 'Thunderstorm with hail', icon: '⛈️' },
  99: { description: 'Thunderstorm with heavy hail', icon: '⛈️' },
};

export default function App() {
  const [city, setCity] = useState('Bangalore');
  const [inputCity, setInputCity] = useState('');
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [location, setLocation] = useState<GeocodingResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchWeather = async (cityName: string) => {
    setLoading(true);
    setError('');
    setWeather(null);
    setLocation(null);

    try {
      const geoResponse = await fetch(
        `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(cityName)}&count=1`
      );
      const geoData = await geoResponse.json();

      if (!geoData.results || geoData.results.length === 0) {
        setError('City not found. Please try another name.');
        return;
      }

      const { latitude, longitude, name, country } = geoData.results[0];
      setLocation({ name, country, latitude, longitude });

      const weatherResponse = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,is_day`
      );
      const weatherData = await weatherResponse.json();

      setWeather({
        temperature: weatherData.current.temperature_2m,
        humidity: weatherData.current.relative_humidity_2m,
        windSpeed: weatherData.current.wind_speed_10m,
        weatherCode: weatherData.current.weather_code,
        isDay: weatherData.current.is_day === 1,
      });
    } catch {
      setError('Failed to fetch weather data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWeather(city);
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputCity.trim()) {
      setCity(inputCity.trim());
      fetchWeather(inputCity.trim());
      setInputCity('');
    }
  };

  const weatherInfo = weather ? WEATHER_CODES[weather.weatherCode] || WEATHER_CODES[0] : null;

  return (
    <div style={styles.container}>
      <div style={styles.widget}>
        <h1 style={styles.title}>Weather Widget</h1>

        <form onSubmit={handleSearch} style={styles.searchForm}>
          <input
            type="text"
            placeholder="Enter city name..."
            value={inputCity}
            onChange={(e) => setInputCity(e.target.value)}
            style={styles.input}
          />
          <button type="submit" style={styles.searchBtn} disabled={loading}>
            Search
          </button>
        </form>

        {loading && (
          <div style={styles.loading}>
            <div style={styles.spinner}></div>
          </div>
        )}

        {error && <p style={styles.error}>{error}</p>}

        {weather && location && weatherInfo && (
          <div style={styles.weatherCard}>
            <div style={styles.location}>
              <h2 style={styles.cityName}>{location.name}</h2>
              <span style={styles.country}>{location.country}</span>
            </div>

            <div style={styles.mainWeather}>
              <span style={styles.weatherIcon}>{weatherInfo.icon}</span>
              <span style={styles.temperature}>{Math.round(weather.temperature)}°C</span>
            </div>

            <p style={styles.description}>{weatherInfo.description}</p>

            <div style={styles.details}>
              <div style={styles.detailItem}>
                <span style={styles.detailIcon}>💧</span>
                <span style={styles.detailLabel}>Humidity</span>
                <span style={styles.detailValue}>{weather.humidity}%</span>
              </div>
              <div style={styles.detailItem}>
                <span style={styles.detailIcon}>💨</span>
                <span style={styles.detailLabel}>Wind</span>
                <span style={styles.detailValue}>{Math.round(weather.windSpeed)} km/h</span>
              </div>
            </div>
          </div>
        )}

        <p style={styles.credit}>
          Data from <a href="https://open-meteo.com/" style={styles.link}>Open-Meteo</a>
        </p>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#0f0f0f',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    padding: '1rem',
  },
  widget: {
    backgroundColor: '#1a1a1a',
    borderRadius: '24px',
    padding: '2rem',
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
    maxWidth: '400px',
    width: '100%',
    textAlign: 'center',
  },
  title: {
    color: '#fff',
    fontSize: '1.5rem',
    fontWeight: '600',
    marginBottom: '1.5rem',
  },
  searchForm: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '1.5rem',
  },
  input: {
    flex: 1,
    padding: '0.75rem 1rem',
    fontSize: '1rem',
    borderRadius: '12px',
    border: '1px solid #333',
    backgroundColor: '#222',
    color: '#fff',
    outline: 'none',
  },
  searchBtn: {
    padding: '0.75rem 1.25rem',
    fontSize: '1rem',
    fontWeight: '600',
    borderRadius: '12px',
    border: 'none',
    backgroundColor: '#667eea',
    color: '#fff',
    cursor: 'pointer',
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    padding: '2rem',
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '3px solid #333',
    borderTopColor: '#667eea',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  error: {
    color: '#ef4444',
    marginBottom: '1rem',
  },
  weatherCard: {
    padding: '1.5rem',
    backgroundColor: '#222',
    borderRadius: '16px',
  },
  location: {
    marginBottom: '1rem',
  },
  cityName: {
    color: '#fff',
    fontSize: '1.5rem',
    fontWeight: '700',
    margin: 0,
  },
  country: {
    color: '#888',
    fontSize: '0.875rem',
  },
  mainWeather: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
    marginBottom: '0.5rem',
  },
  weatherIcon: {
    fontSize: '4rem',
  },
  temperature: {
    color: '#fff',
    fontSize: '3.5rem',
    fontWeight: '700',
  },
  description: {
    color: '#aaa',
    fontSize: '1rem',
    marginBottom: '1.5rem',
  },
  details: {
    display: 'flex',
    justifyContent: 'space-around',
    borderTop: '1px solid #333',
    paddingTop: '1rem',
  },
  detailItem: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '0.25rem',
  },
  detailIcon: {
    fontSize: '1.5rem',
  },
  detailLabel: {
    color: '#888',
    fontSize: '0.75rem',
    textTransform: 'uppercase',
  },
  detailValue: {
    color: '#fff',
    fontSize: '1rem',
    fontWeight: '600',
  },
  credit: {
    marginTop: '1.5rem',
    color: '#555',
    fontSize: '0.75rem',
  },
  link: {
    color: '#667eea',
    textDecoration: 'none',
  },
};
