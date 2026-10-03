# JSON to Model Generator

Convert JSON data to typed data models in Python, TypeScript, or Go. Perfect for quickly creating type-safe models from API responses or JSON schemas.

## Features

- **Python**: Generate `@dataclass` models
- **TypeScript**: Generate `interface` definitions
- **Go**: Generate `struct` definitions
- **Nested objects**: Automatic nested type generation
- **Arrays**: Handle arrays of primitives and objects
- **Type inference**: Automatic type detection from values
- **Naming conventions**: Auto-convert snake_case/camelCase/PascalCase

## Installation

```bash
# No dependencies required (uses stdlib only)
pip install -r requirements.txt  # optional
```

## Usage

### Basic Usage

```bash
# Python (default)
python json-to-model.py data.json -o models.py

# TypeScript
python json-to-model.py data.json --typescript -o models.ts

# Go
python json-to-model.py data.json --go -o models.go

# All formats at once
python json-to-model.py data.json --all
```

### From stdin

```bash
# Pipe JSON
curl https://api.example.com/user | python json-to-model.py - --python

# Or with heredoc
cat <<'EOF' | python json-to-model.py - --typescript
{"name": "John", "age": 30, "address": {"city": "NYC"}}
EOF
```

### Custom Model Name

```bash
python json-to-model.py data.json --python --class-name UserProfile -o user.py
```

## Examples

### Input JSON

```json
{
  "user_id": 123,
  "full_name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "profile": {
    "avatar_url": "https://example.com/avatar.png",
    "bio": "Software developer"
  },
  "tags": ["python", "typescript", "go"],
  "projects": [
    {"name": "API Client", "status": "active"}
  ]
}
```

### Python Output

```python
"""Generated data models from data.json."""

from dataclasses import dataclass
from typing import Any

@dataclass
class Profile:
    """Data model for Profile."""
    avatar_url: str
    bio: str

@dataclass
class Project:
    """Data model for Project."""
    name: str
    status: str

@dataclass
class User:
    """Data model for User."""
    user_id: int
    full_name: str
    email: str
    is_active: bool
    profile: Profile
    tags: list[str]
    projects: list[Project]
```

### TypeScript Output

```typescript
// Generated from data.json

export interface Profile {
    avatarUrl?: string;
    bio?: string;
}

export interface Project {
    name?: string;
    status?: string;
}

export interface User {
    userId?: number;
    fullName?: string;
    email?: string;
    isActive?: boolean;
    profile?: Profile;
    tags?: string[];
    projects?: Project[];
}
```

### Go Output

```go
// Generated from data.json

package models

type Profile struct {
    AvatarUrl string `json:"avatar_url"`
    Bio       string `json:"bio"`
}

type Project struct {
    Name   string `json:"name"`
    Status string `json:"status"`
}

type User struct {
    UserId   int64      `json:"user_id"`
    FullName string    `json:"full_name"`
    Email    string    `json:"email"`
    IsActive bool      `json:"is_active"`
    Profile  Profile   `json:"profile"`
    Tags     []string  `json:"tags"`
    Projects []*Project `json:"projects"`
}
```

## Options

| Flag | Description |
|------|-------------|
| `input` | Input JSON file (or `-` for stdin) |
| `-p, --python` | Generate Python dataclasses |
| `-t, --typescript` | Generate TypeScript interfaces |
| `-g, --go` | Generate Go structs |
| `-c, --class-name` | Custom name for root model |
| `-o, --output` | Output file path |
| `-a, --all` | Generate all language outputs |

## Type Mapping

| JSON Type | Python | TypeScript | Go |
|-----------|--------|------------|-----|
| `string` | `str` | `string` | `string` |
| `number` | `int`/`float` | `number` | `int64`/`float64` |
| `boolean` | `bool` | `boolean` | `bool` |
| `null` | `None` | `null` | `interface{}` |
| `array` | `list[T]` | `T[]` | `[]T` |
| `object` | `dict[str, Any]` | `Record<string, unknown>` | `map[string]interface{}` |
