# HTTP Request Logger

A browser-based tool to log and inspect HTTP requests. Use the browser's fetch API to make requests and view formatted request/response history.

## Features

- **All HTTP Methods**: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- **Custom Headers**: Add as many headers as needed
- **Request Body**: JSON editor with syntax display
- **Response Viewer**: Formatted JSON with syntax highlighting
- **Request History**: Persisted to localStorage
- **Replay Requests**: Click history items to reload
- **Export History**: Download as JSON file
- **Response Headers**: View all response headers
- **Dark Theme**: Easy on the eyes design
- **Responsive**: Works on mobile and desktop

## Usage

### Basic Usage

1. Open `request-logger.html` in a browser
2. Enter a URL
3. Select HTTP method
4. Add headers if needed
5. Add body for POST/PUT/PATCH
6. Click "Send Request"
7. View formatted response

### Managing Headers

- Edit existing header rows
- Click "+ Add Header" to add more
- Click "x" to remove a header (clears if last row)

### Response Body

- JSON responses are pretty-printed
- Response size and timing shown
- Status code with color indicator:
  - Green: 2xx success
  - Yellow: 3xx redirect
  - Red: 4xx/5xx error

### History

- All requests saved to browser localStorage
- Click any history item to reload that request
- Clear all with "Clear All" button
- Export history as JSON

## Example Requests

### GET Request

```javascript
// Fetch users from JSONPlaceholder
URL: https://jsonplaceholder.typicode.com/users
Method: GET
Headers: (leave default or remove Content-Type)
Body: (empty)
```

### POST Request

```javascript
// Create a post
URL: https://jsonplaceholder.typicode.com/posts
Method: POST
Headers: Content-Type: application/json
Body:
{
  "title": "My Post",
  "body": "Post content here",
  "userId": 1
}
```

### PUT Request

```javascript
// Update a post
URL: https://jsonplaceholder.typicode.com/posts/1
Method: PUT
Headers: Content-Type: application/json
Body:
{
  "id": 1,
  "title": "Updated Title",
  "body": "Updated content",
  "userId": 1
}
```

### DELETE Request

```javascript
// Delete a post
URL: https://jsonplaceholder.typicode.com/posts/1
Method: DELETE
```

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge 80+
- Firefox 75+
- Safari 13.1+
- Opera 67+

## Tips

### Testing APIs

Great for testing:
- REST APIs
- GraphQL endpoints
- WebSocket upgrades
- CORS-enabled endpoints

### Common Headers

| Header | Value | Use Case |
|--------|-------|----------|
| Content-Type | application/json | JSON requests |
| Authorization | Bearer token | Authenticated requests |
| Accept | application/json | Expect JSON response |
| X-API-Key | your-api-key | API key authentication |

### CORS Note

Browser fetch requests are subject to CORS. For APIs that don't support CORS, you'll need:
- A CORS proxy
- Server-side request tool
- Browser with CORS disabled (not recommended)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter (in URL field) | Send request |
| Ctrl+Enter | Send request |

## Data Privacy

All data is stored locally in your browser:
- No server communication
- No data leaves your browser
- Clear browser data to remove history

## Files

```
request-logger/
  request-logger.html  # Main application
  README.md            # This file
```

## License

MIT License - Use freely for personal and commercial projects.
