import { useState } from 'react'

interface WeatherData {
  temperature: number
  humidity: number
  windSpeed: number
  weatherCode: number
  isDay: boolean
}

interface GeocodingResult {
  name: string
  latitude: number
  longitude: number
  country: string
  admin1?: string
}

const weatherDescriptions: Record<number, { description: string; icon: string }> = {
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
  75: { description: 'Heavy snow', icon: '🌨️' },
  80: { description: 'Slight rain showers', icon: '🌦️' },
  81: { description: 'Moderate rain showers', icon: '🌦️' },
  82: { description: 'Violent rain showers', icon: '⛈️' },
  95: { description: 'Thunderstorm', icon: '⛈️' },
  96: { description: 'Thunderstorm with hail', icon: '⛈️' },
  99: { description: 'Thunderstorm with heavy hail', icon: '⛈️' },
}

function App() {
  const [city, setCity] = useState('')
  const [weather, setWeather] = useState<WeatherData | null>(null)
  const [locationName, setLocationName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const searchWeather = async () => {
    if (!city.trim()) return

    setLoading(true)
    setError('')
    setWeather(null)

    try {
      // Geocoding: convert city name to coordinates
      const geoResponse = await fetch(
        `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1`
      )
      const geoData = await geoResponse.json()

      if (!geoData.results || geoData.results.length === 0) {
        setError('City not found. Please try another search.')
        setLoading(false)
        return
      }

      const location: GeocodingResult = geoData.results[0]
      setLocationName(`${location.name}${location.admin1 ? `, ${location.admin1}` : ''}, ${location.country}`)

      // Fetch weather data
      const weatherResponse = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${location.latitude}&longitude=${location.longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,is_day`
      )
      const weatherData = await weatherResponse.json()

      setWeather({
        temperature: weatherData.current.temperature_2m,
        humidity: weatherData.current.relative_humidity_2m,
        windSpeed: weatherData.current.wind_speed_10m,
        weatherCode: weatherData.current.weather_code,
        isDay: weatherData.current.is_day === 1,
      })
    } catch {
      setError('Failed to fetch weather data. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      searchWeather()
    }
  }

  const weatherInfo = weather ? weatherDescriptions[weather.weatherCode] || weatherDescriptions[0] : null

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Weather App</h1>
        <p style={styles.subtitle}>Search weather by city name</p>

        <div style={styles.searchContainer}>
          <input
            type="text"
            placeholder="Enter city name..."
            value={city}
            onChange={(e) => setCity(e.target.value)}
            onKeyPress={handleKeyPress}
            style={styles.input}
          />
          <button onClick={searchWeather} disabled={loading} style={styles.button}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        {weather && weatherInfo && (
          <div style={styles.weatherCard}>
            <div style={styles.location}>{locationName}</div>
            <div style={styles.icon}>{weatherInfo.icon}</div>
            <div style={styles.temperature}>{Math.round(weather.temperature)}°C</div>
            <div style={styles.description}>{weatherInfo.description}</div>

            <div style={styles.details}>
              <div style={styles.detailItem}>
                <span style={styles.detailLabel}>Humidity</span>
                <span style={styles.detailValue}>{weather.humidity}%</span>
              </div>
              <div style={styles.detailItem}>
                <span style={styles.detailLabel}>Wind Speed</span>
                <span style={styles.detailValue}>{weather.windSpeed} km/h</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#667eea',
    backgroundImage: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    padding: '20px',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '20px',
    padding: '40px',
    width: '100%',
    maxWidth: '400px',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
    textAlign: 'center' as const,
  },
  title: {
    color: '#1a202c',
    fontSize: '28px',
    marginBottom: '8px',
    fontWeight: 700,
  },
  subtitle: {
    color: '#718096',
    fontSize: '14px',
    marginBottom: '24px',
  },
  searchContainer: {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px',
  },
  input: {
    flex: 1,
    padding: '14px 16px',
    border: '2px solid #e2e8f0',
    borderRadius: '10px',
    fontSize: '16px',
    outline: 'none',
    transition: 'border-color 0.2s',
  },
  button: {
    padding: '14px 24px',
    backgroundColor: '#667eea',
    color: '#ffffff',
    border: 'none',
    borderRadius: '10px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  error: {
    color: '#e53e3e',
    backgroundColor: '#fed7d7',
    padding: '12px',
    borderRadius: '8px',
    marginBottom: '16px',
    fontSize: '14px',
  },
  weatherCard: {
    marginTop: '20px',
    padding: '24px',
    backgroundColor: '#f7fafc',
    borderRadius: '16px',
  },
  location: {
    fontSize: '16px',
    color: '#4a5568',
    marginBottom: '12px',
  },
  icon: {
    fontSize: '64px',
    marginBottom: '8px',
  },
  temperature: {
    fontSize: '48px',
    fontWeight: 700,
    color: '#1a202c',
    marginBottom: '8px',
  },
  description: {
    fontSize: '18px',
    color: '#4a5568',
    marginBottom: '20px',
  },
  details: {
    display: 'flex',
    justifyContent: 'space-around',
    paddingTop: '16px',
    borderTop: '1px solid #e2e8f0',
  },
  detailItem: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
  },
  detailLabel: {
    fontSize: '12px',
    color: '#718096',
    marginBottom: '4px',
  },
  detailValue: {
    fontSize: '18px',
    fontWeight: 600,
    color: '#1a202c',
  },
}

export default App
