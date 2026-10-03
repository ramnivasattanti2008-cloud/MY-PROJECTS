import { useState } from 'react';

interface WeatherData {
  temp: number;
  humidity: number;
  windSpeed: number;
  description: string;
  icon: string;
  city: string;
}

const ICON_MAP: Record<number, string> = {
  0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️',
  45: '🌫️', 48: '🌫️',
  51: '🌧️', 53: '🌧️', 55: '🌧️',
  61: '🌧️', 63: '🌧️', 65: '🌧️',
  71: '🌨️', 73: '🌨️', 75: '🌨️',
  80: '🌦️', 81: '🌦️', 82: '🌦️',
  95: '⛈️', 96: '⛈️', 99: '⛈️',
};

function getIcon(code: number): string {
  return ICON_MAP[code] ?? '🌡️';
}

async function fetchWeather(city: string): Promise<WeatherData> {
  const geoRes = await fetch(
    `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1`
  );
  const geoData = await geoRes.json();
  if (!geoData.results?.length) throw new Error('City not found');
  const { latitude, longitude, name, country } = geoData.results[0];

  const weatherRes = await fetch(
    `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=auto`
  );
  const weatherData = await weatherRes.json();
  const current = weatherData.current;

  return {
    temp: Math.round(current.temperature_2m),
    humidity: current.relative_humidity_2m,
    windSpeed: Math.round(current.wind_speed_10m),
    description: getDescription(current.weather_code),
    icon: getIcon(current.weather_code),
    city: `${name}, ${country}`,
  };
}

function getDescription(code: number): string {
  const descriptions: Record<number, string> = {
    0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
    45: 'Fog', 48: 'Depositing rime fog',
    51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
    61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
    71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
    80: 'Slight showers', 81: 'Moderate showers', 82: 'Violent showers',
    95: 'Thunderstorm', 96: 'Thunderstorm with hail', 99: 'Severe thunderstorm',
  };
  return descriptions[code] ?? 'Unknown';
}

export default function App() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!city.trim()) return;
    setLoading(true);
    setError('');
    try {
      const data = await fetchWeather(city);
      setWeather(data);
    } catch {
      setError('City not found. Try another name.');
      setWeather(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Weather</h1>
        <form onSubmit={search} style={styles.form}>
          <input
            style={styles.input}
            placeholder="Enter city..."
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
          <button style={styles.btn} type="submit" disabled={loading}>
            {loading ? '...' : 'Search'}
          </button>
        </form>
        {error && <p style={styles.error}>{error}</p>}
        {weather && (
          <div style={styles.result}>
            <div style={styles.icon}>{weather.icon}</div>
            <div style={styles.temp}>{weather.temp}°C</div>
            <div style={styles.city}>{weather.city}</div>
            <div style={styles.desc}>{weather.description}</div>
            <div style={styles.details}>
              <span>💧 {weather.humidity}%</span>
              <span>💨 {weather.windSpeed} km/h</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    background: '#0f0f0f',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'system-ui, sans-serif',
    color: '#fff',
    padding: 16,
  },
  card: {
    background: '#1a1a1a',
    borderRadius: 16,
    padding: 40,
    textAlign: 'center',
    boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
    width: '100%',
    maxWidth: 400,
  },
  title: { fontSize: 28, fontWeight: 700, marginBottom: 24, color: '#e0e0e0' },
  form: { display: 'flex', gap: 8, marginBottom: 24 },
  input: {
    flex: 1,
    padding: '12px 16px',
    fontSize: 16,
    border: '1px solid #333',
    borderRadius: 8,
    background: '#0f0f0f',
    color: '#fff',
    outline: 'none',
  },
  btn: {
    padding: '12px 20px',
    fontSize: 16,
    fontWeight: 600,
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer',
    background: '#7c3aed',
    color: '#fff',
  },
  error: { color: '#f87171', marginBottom: 16 },
  result: { marginTop: 8 },
  icon: { fontSize: 72, marginBottom: 8 },
  temp: { fontSize: 56, fontWeight: 700, color: '#a78bfa' },
  city: { fontSize: 18, fontWeight: 500, marginTop: 8, color: '#ccc' },
  desc: { fontSize: 16, color: '#888', marginTop: 4, marginBottom: 16 },
  details: { display: 'flex', gap: 24, justifyContent: 'center', fontSize: 16 },
};
