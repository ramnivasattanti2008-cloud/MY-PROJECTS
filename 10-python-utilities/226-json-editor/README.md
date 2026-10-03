# JSON Editor

An interactive command-line tool for viewing, adding, editing, and deleting keys in JSON files.

## Features

- **Interactive CLI**: Full-screen editing experience
- **View**: Display entire JSON or specific paths
- **Set**: Update existing values
- **Add**: Insert new key-value pairs
- **Delete**: Remove keys
- **Search**: Find keys and values containing text
- **Structure**: View hierarchical tree of JSON structure
- **Non-interactive Mode**: Use flags for scripting

## Installation

```bash
# No external dependencies required
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
python json-editor.py config.json
```

Commands in interactive mode:

| Command | Description |
|---------|-------------|
| `view [path]` | View JSON (optionally at path) |
| `set <path> <value>` | Set a value |
| `add <path> <key> <value>` | Add new key-value |
| `delete <path>` | Delete a key |
| `search <query>` | Search for key/value |
| `structure` | Show structure tree |
| `save [path]` | Save to file |
| `quit` | Exit editor |

### Non-Interactive Mode

```bash
# View entire file
python json-editor.py data.json --view

# View specific path
python json-editor.py data.json --view "user.settings.theme"

# Set a value
python json-editor.py data.json --set "user.name" '"John Doe"'

# Search
python json-editor.py data.json --search "color"

# Show structure
python json-editor.py data.json --structure
```

## Path Notation

The editor uses dot notation for nested keys and bracket notation for arrays:

```
user.profile.name           # Nested key
items[0].title              # Array element
data[0].tags[1]             # Nested array
```

## Examples

### View Data

```bash
$ python json-editor.py data.json
json> view
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "settings": {
    "theme": "dark",
    "language": "en"
  }
}
```

### Edit Values

```bash
json> set settings.theme "light"
json> view settings
{
  "theme": "light",
  "language": "en"
}
```

### Add New Data

```bash
json> add settings volume 75
json> view settings
{
  "theme": "light",
  "language": "en",
  "volume": 75
}
```

### Search

```bash
json> search name
Found 2 matches:
  users[0].name
  users[1].name
```

### View Structure

```bash
json> structure
├── users (list)
│   └── [list of 2 items]
│       └── id: 1
│       └── name: "Alice"
└── settings (dict)
    └── theme: "dark"
    └── language: "en"
```

## JSON Value Syntax

When setting values, use proper JSON syntax:

- Strings: `"hello"` or `'hello'`
- Numbers: `42` or `3.14`
- Booleans: `true` or `false`
- Null: `null`
- Arrays: `[1, 2, 3]`
- Objects: `{"key": "value"}`

## Use Cases

1. **Configuration Files**: Edit JSON config files without a text editor
2. **API Testing**: Modify JSON request bodies
3. **Data Exploration**: Quickly inspect large JSON files
4. **Automation**: Script JSON modifications

## License

MIT License - Educational purposes
