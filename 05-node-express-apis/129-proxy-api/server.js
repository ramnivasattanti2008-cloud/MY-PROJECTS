const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3002;

app.use(cors());
app.use(express.json());

// Proxy configuration
const PROXY_ROUTES = {
  '/proxy/github': {
    baseURL: 'https://api.github.com',
    headers: { 'Accept': 'application/vnd.github.v3+json' }
  },
  '/proxy/weather': {
    baseURL: 'https://api.open-meteo.com/v1',
    headers: {}
  },
  '/proxy/nominatim': {
    baseURL: 'https://nominatim.openstreetmap.org',
    headers: { 'Accept': 'application/json' }
  }
};

// Generic proxy handler
async function proxyRequest(req, res, config) {
  try {
    const { baseURL, headers } = config;
    const path = req.params[0] || '';
    const queryParams = req.query;

    const response = await axios({
      method: req.method,
      url: `${baseURL}${path}`,
      params: queryParams,
      data: req.method !== 'GET' ? req.body : undefined,
      headers: {
        ...headers,
        'User-Agent': 'Express-Proxy/1.0'
      },
      timeout: 30000
    });

    res.json({
      success: true,
      data: response.data,
      status: response.status
    });
  } catch (err) {
    if (err.response) {
      return res.status(err.response.status).json({
        success: false,
        error: 'Upstream API error',
        details: err.response.data
      });
    }
    res.status(500).json({
      success: false,
      error: 'Proxy request failed',
      message: err.message
    });
  }
}

// GitHub proxy
app.all('/proxy/github/*', (req, res) => {
  proxyRequest(req, res, PROXY_ROUTES['/proxy/github']);
});

// Weather proxy
app.all('/proxy/weather/*', (req, res) => {
  proxyRequest(req, res, PROXY_ROUTES['/proxy/weather']);
});

// Nominatim (geocoding) proxy
app.all('/proxy/nominatim/*', (req, res) => {
  proxyRequest(req, res, PROXY_ROUTES['/proxy/nominatim']);
});

// Convenience endpoints
// GET /api/github/user/:username - Get GitHub user info
app.get('/api/github/user/:username', async (req, res) => {
  try {
    const { username } = req.params;
    const response = await axios.get(`https://api.github.com/users/${username}`, {
      headers: {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Express-Proxy/1.0'
      }
    });

    res.json({
      success: true,
      data: {
        login: response.data.login,
        name: response.data.name,
        bio: response.data.bio,
        public_repos: response.data.public_repos,
        followers: response.data.followers,
        following: response.data.following,
        avatar_url: response.data.avatar_url
      }
    });
  } catch (err) {
    if (err.response?.status === 404) {
      return res.status(404).json({ success: false, error: 'User not found' });
    }
    res.status(500).json({ success: false, error: 'Failed to fetch GitHub user' });
  }
});

// GET /api/weather?lat=...&lon=... - Get current weather
app.get('/api/weather', async (req, res) => {
  try {
    const { lat, lon } = req.query;

    if (!lat || !lon) {
      return res.status(400).json({
        success: false,
        error: 'Latitude and longitude are required'
      });
    }

    const response = await axios.get('https://api.open-meteo.com/v1/forecast', {
      params: {
        latitude: lat,
        longitude: lon,
        current_weather: true
      }
    });

    const weather = response.data.current_weather;
    res.json({
      success: true,
      data: {
        temperature: weather.temperature,
        windspeed: weather.windspeed,
        winddirection: weather.winddirection,
        weathercode: weather.weathercode,
        time: weather.time
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Failed to fetch weather' });
  }
});

// Routes info
app.get('/routes', (req, res) => {
  res.json({
    success: true,
    data: {
      routes: [
        { endpoint: 'GET /api/github/user/:username', description: 'Get GitHub user info' },
        { endpoint: 'GET /api/weather?lat=&lon=', description: 'Get current weather' },
        { endpoint: '* /proxy/github/*', description: 'Proxy to GitHub API' },
        { endpoint: '* /proxy/weather/*', description: 'Proxy to Open-Meteo API' },
        { endpoint: '* /proxy/nominatim/*', description: 'Proxy to Nominatim geocoding' }
      ]
    }
  });
});

app.listen(PORT, () => {
  console.log(`Proxy API running on http://localhost:${PORT}`);
});
