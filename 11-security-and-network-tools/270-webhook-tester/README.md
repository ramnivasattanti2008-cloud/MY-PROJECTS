# Webhook Tester

A Flask application to receive, store, and display webhook payloads. Useful for testing webhooks during development.

## Features

- Receive and display webhook payloads
- View headers, body, and timestamp
- Real-time updates (auto-refresh)
- Delete individual webhooks or clear all
- REST API for programmatic access
- Dark theme UI

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The application will be available at:
- Web UI: `http://localhost:5000/`
- Webhook endpoint: `http://localhost:5000/webhook`

## Web UI

Open `http://localhost:5000/` in your browser to see:
- List of received webhooks
- Auto-refresh every 5 seconds
- Click "Refresh" to manually update
- Click "Delete" to remove individual webhooks
- Click "Clear All" to remove all stored webhooks

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/health
```

### Receive a Webhook
```bash
# Send any webhook to the endpoint
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"event": "user.created", "data": {"id": 123, "name": "John"}}'

# With custom path
curl -X POST http://localhost:5000/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d '{"ref": "refs/heads/main", "commits": []}'

# With form data
curl -X POST http://localhost:5000/webhook \
  -d "key=value" \
  -d "name=test"

# With query parameters
curl -X POST "http://localhost:5000/webhook?source=test&token=abc123"
```

### Get All Webhooks
```bash
curl http://localhost:5000/api/webhooks
```

### Get Single Webhook
```bash
curl http://localhost:5000/api/webhooks/1
```

### Get Latest Webhook
```bash
curl http://localhost:5000/api/webhooks/latest
```

### Delete Single Webhook
```bash
curl -X DELETE http://localhost:5000/api/webhooks/1
```

### Clear All Webhooks
```bash
curl -X POST http://localhost:5000/api/webhooks/clear
```

## Usage Examples

### Testing GitHub Webhooks
```bash
# Start the server, then in another terminal:
curl -X POST http://localhost:5000/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -H "X-GitHub-Delivery: $(uuidgen)" \
  -d '{
    "ref": "refs/heads/main",
    "commits": [{"message": "Fix bug"}],
    "pusher": {"name": "octocat"}
  }'
```

### Testing Stripe Webhooks (simulated)
```bash
curl -X POST http://localhost:5000/webhook/stripe \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: test_signature" \
  -d '{
    "type": "checkout.session.completed",
    "data": {"object": {"id": "cs_test_123", "amount_total": 2000}}
  }'
```

### Testing Slack Webhooks (simulated)
```bash
curl -X POST http://localhost:5000/webhook/slack \
  -H "Content-Type: application/json" \
  -d '{
    "type": "url_verification",
    "challenge": "test_challenge"
  }'
```

## Response Format

### Webhook Received (POST)
```json
{
  "success": true,
  "message": "Webhook received",
  "webhook_id": 1
}
```

### Webhook List (GET /api/webhooks)
```json
{
  "success": true,
  "count": 2,
  "webhooks": [
    {
      "id": 1,
      "timestamp": "2024-01-01T12:00:00.000000",
      "method": "POST",
      "path": "/webhook",
      "content_type": "application/json"
    }
  ]
}
```

### Single Webhook (GET /api/webhooks/:id)
```json
{
  "success": true,
  "webhook": {
    "id": 1,
    "timestamp": "2024-01-01T12:00:00.000000",
    "method": "POST",
    "path": "/webhook",
    "headers": {...},
    "query_params": {...},
    "body": {...},
    "body_raw": "..."
  }
}
```

## Storage

Webhooks are stored in-memory (limited to 100 most recent). They will be lost on server restart.

## Use Cases

1. **Local Development**: Test webhook integrations without deploying
2. **Debugging**: Inspect webhook payloads during development
3. **CI/CD Testing**: Verify webhook signatures and payloads
4. **Integration Testing**: Capture and verify webhook behavior

## Security Notes

- This is a development tool - not for production use
- No authentication on webhook endpoints
- Webhooks are stored in memory (not persistent)
- Consider adding authentication for sensitive testing
