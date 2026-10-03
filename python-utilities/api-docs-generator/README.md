# API Documentation Generator

Auto-generate API documentation from Python docstrings. Scans Python files, extracts function signatures, type hints, and docstrings to create comprehensive documentation.

## Features

- Parse Python AST to extract accurate signatures
- Extract type hints from function parameters
- Parse docstrings (Google/NumPy style)
- Generate Markdown documentation
- Generate OpenAPI-compatible spec
- Export JSON for custom processing
- Scan directories with glob patterns
- Support for classes, methods, and standalone functions
- Track decorators (Flask/Django routes, etc.)

## Installation

```bash
# No dependencies required (uses stdlib ast)
pip install -r requirements.txt  # optional: colorama for syntax highlighting
```

## Usage

```bash
# Generate docs for a single file
python api-docs-generator.py myapi.py -o docs.md

# Scan a directory
python api-docs-generator.py ./src -o api-docs.md

# Generate OpenAPI spec
python api-docs-generator.py ./src -f openapi -o openapi.json

# JSON export for custom processing
python api-docs-generator.py ./src -f json -o data.json

# Verbose mode
python api-docs-generator.py ./src -v
```

## Output Formats

### Markdown (default)

Generates structured Markdown with:
- Table of contents
- Module sections
- Class and method documentation
- Parameter documentation
- Return value documentation

### OpenAPI

Generates OpenAPI 3.1.0 compatible JSON:
- Path definitions
- HTTP method detection from decorators
- Parameter documentation
- Response documentation

### JSON

Structured JSON output for custom processing or integration with other tools.

## Docstring Format

Supports Google-style docstrings:

```python
def create_user(name: str, email: str, role: str = "user") -> dict:
    """
    Create a new user in the system.

    Args:
        name: Full name of the user
        email: Valid email address
        role: User role (default: "user")

    Returns:
        Dictionary with user data including ID

    Raises:
        ValueError: If email is invalid
        RuntimeError: If database connection fails
    """
    pass
```

## Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output file path |
| `-f, --format` | Output format: markdown, openapi, json |
| `-t, --title` | Documentation title |
| `-p, --pattern` | File pattern to match (default: *.py) |
| `-v, --verbose` | Verbose output |

## Examples

### Flask API

```python
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> dict:
    """
    Get user by ID.

    Args:
        user_id: The user's unique identifier

    Returns:
        User object with name and email
    """
    return {"name": "John", "email": "john@example.com"}
```

Generates OpenAPI path:
```json
{
  "/myapi/get_user": {
    "get": {
      "summary": "Get user by ID.",
      "parameters": [{"name": "user_id", "description": "The user's unique identifier"}],
      "responses": {"200": {"description": "User object with name and email"}}
    }
  }
}
```
