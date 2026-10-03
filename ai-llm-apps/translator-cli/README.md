# Translator CLI

A Python command-line tool for translating text between languages using Google Translate.

## Features

- **Multiple language support**: 100+ languages supported
- **Auto-detect language**: Automatically detect source language
- **Verbose output**: Show detailed translation information
- **JSON output**: Machine-readable output format
- **Interactive mode**: Continuous translation mode
- **File input**: Translate content from files
- **Language detection**: Identify the language of any text
- **Pronunciation**: Show pronunciation for translated text

## Installation

```bash
pip install -r requirements.txt
```

Note: Requires the `googletrans` library.

## Usage

### Basic translation

```bash
# English to Spanish
python translator-cli.py "Hello world" -t es

# Auto-detect source, translate to French
python translator-cli.py "Bonjour le monde" -t fr

# Specify source language
python translator-cli.py "Hola" -s es -t en
```

### Verbose output

```bash
python translator-cli.py "Hello" -t ja -v
```

### JSON output

```bash
python translator-cli.py "Hello world" -t es -j
```

### Read from file

```bash
python translator-cli.py -f input.txt -t de
```

### Detect language

```bash
python translator-cli.py --detect "This is a test"
# Output: Language: EN (english), Confidence: 100.0%
```

### List all languages

```bash
python translator-cli.py --list-languages
```

### Interactive mode

```bash
python translator-cli.py --interactive
```

## Common Language Codes

| Code | Language |
|------|----------|
| en | English |
| es | Spanish |
| fr | French |
| de | German |
| it | Italian |
| pt | Portuguese |
| ru | Russian |
| ja | Japanese |
| ko | Korean |
| zh-cn | Chinese (Simplified) |
| zh-tw | Chinese (Traditional) |
| ar | Arabic |
| hi | Hindi |
| ta | Tamil |
| te | Telugu |
| ml | Malayalam |
| kn | Kannada |
| mr | Marathi |
| bn | Bengali |
| pa | Punjabi |
| ur | Urdu |
| gu | Gujarati |

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `text` | - | Text to translate |
| `--file` | `-f` | Read text from file |
| `--source` | `-s` | Source language (default: auto) |
| `--to` | `-t` | Target language (required) |
| `--detect` | - | Detect language of text |
| `--list-languages` | - | List all supported languages |
| `--verbose` | `-v` | Verbose output with details |
| `--json` | `-j` | Output as JSON |
| `--interactive` | `-i` | Interactive translation mode |

## Examples

### Quick translations

```bash
# Greetings
python translator-cli.py "Good morning" -t ja
python translator-cli.py "Thank you" -t hi
python translator-cli.py "How are you?" -t fr

# Technical terms
python translator-cli.py "Hello World" -t es
python translator-cli.py "Open source" -t de
```

### Batch translation with file

```bash
# Create a file with text
echo "Hello, how are you today?" > text.txt

# Translate the file
python translator-cli.py -f text.txt -t es
```

### Script-friendly output

```bash
# Get just the translation
python translator-cli.py "Hello" -t es

# Get JSON for parsing
python translator-cli.py "Hello" -t es -j
```

## Interactive Mode Commands

In interactive mode (`-i`), use these commands:

| Command | Description |
|---------|-------------|
| `:lang <code>` | Set target language |
| `:source <code>` | Set source language |
| `:detect` | Detect language of input |
| `:list` | List all languages |
| `:quit` | Exit interactive mode |

## JSON Output Format

```json
{
  "source_lang": "en",
  "dest_lang": "es",
  "original": "Hello world",
  "translated": "Hola mundo",
  "pronunciation": null
}
```

## Troubleshooting

### googletrans not working

If you encounter issues with `googletrans`, try:

```bash
# Option 1: Install specific version
pip install googletrans==4.0.0-rc1

# Option 2: Use alternative package
pip install googletrans-new
```

### Rate limiting

Google Translate has rate limits. If you hit them, wait a few seconds and try again.

## License

MIT License
