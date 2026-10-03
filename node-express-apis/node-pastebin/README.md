# Code Pastebin

A simple Express.js code pastebin with syntax highlighting using highlight.js.

## Features

- Create code pastes with syntax highlighting
- Support for 19+ programming languages
- View count tracking
- Raw paste retrieval
- Markdown rendering support

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

The server will start on http://localhost:3001

## API Endpoints

### Create Paste
```bash
POST /api/pastes
Content-Type: application/json

{
  "title": "My Code",
  "content": "console.log('Hello World');",
  "language": "javascript"
}
```

### Get Paste (Highlighted)
```bash
GET /api/pastes/:id
```

### Get Raw Paste
```bash
GET /api/pastes/:id/raw
```

### List All Pastes
```bash
GET /api/pastes
```

### Delete Paste
```bash
DELETE /api/pastes/:id
```

### Get Supported Languages
```bash
GET /api/languages
```

## Supported Languages

- JavaScript / TypeScript
- Python
- Java
- C++ / C#
- Go / Rust
- Ruby / PHP
- SQL
- HTML / CSS
- JSON / YAML / XML
- Markdown
- Bash
- And more...

## Example

```bash
# Create a JavaScript paste
curl -X POST http://localhost:3001/api/pastes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hello World",
    "content": "function greet(name) {\n  return `Hello, ${name}!`;\n}",
    "language": "javascript"
  }'

# Get the paste
curl http://localhost:3001/api/pastes/abc123xyz

# Get raw content
curl http://localhost:3001/api/pastes/abc123xyz/raw
```
