# Regex Extractor

A Python utility for extracting emails, phone numbers, URLs, IP addresses, and more from text files or pasted input using regular expressions.

## Features

- **20+ Built-in Patterns**: Pre-built regex for common data types
- **Custom Patterns**: Use your own regex patterns
- **File or Text Input**: Read from file or paste text directly
- **Validation**: Basic validation for extracted data
- **Sanitization**: Redact sensitive information
- **Domain Extraction**: Extract unique domains from URLs
- **Statistics**: Count all pattern occurrences

## Installation

```bash
# No external dependencies required
pip install -r requirements.txt
```

## Usage

### Extract Emails

```bash
python regex-extractor.py data.txt --emails
```

### Extract Multiple Types

```bash
python regex-extractor.py data.txt --emails --urls --phones
```

### Extract All Patterns

```bash
python regex-extractor.py data.txt --all
```

### Custom Pattern

```bash
python regex-extractor.py data.txt --pattern "\d{4}-\d{4}-\d{4}"
```

### Statistics

```bash
python regex-extractor.py data.txt --stats
```

### Sanitize (Redact Sensitive Data)

```bash
python regex-extractor.py data.txt --sanitize
```

### Extract Unique Domains

```bash
python regex-extractor.py data.txt --domains
```

### Use with Piped Input

```bash
echo "Contact us at support@example.com" | python regex-extractor.py -
```

## Available Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| `email` | Email addresses | user@example.com |
| `phone_us` | US phone numbers | (555) 123-4567 |
| `phone_international` | International phones | +91-9876543210 |
| `url` | HTTP/HTTPS URLs | https://example.com |
| `ipv4` | IPv4 addresses | 192.168.1.1 |
| `ipv6` | IPv6 addresses | 2001:db8::1 |
| `date_iso` | ISO dates | 2024-01-15 |
| `date_us` | US dates | 01/15/2024 |
| `time_24h` | 24-hour time | 14:30:45 |
| `credit_card` | Card numbers | 4111111111111111 |
| `ssn` | US SSN | 123-45-6789 |
| `zip_us` | US ZIP codes | 12345-6789 |
| `hex_color` | Hex colors | #ff0000 |
| `mac_address` | MAC addresses | 00:1A:2B:3C:4D:5E |
| `uuid` | UUID/GUID | 550e8400-e29b-41d4 |
| `hashtag` | Hashtags | #Python |
| `mention` | @mentions | @username |
| `money_usd` | USD amounts | $1,234.56 |
| `percentage` | Percentages | 42% |
| `words` | Individual words | Hello |
| `numbers` | Numbers | 42, -3.14 |

## Output Examples

### Statistics Output

```
Extraction Statistics (File: log.txt)
============================================================
  email                :  245 matches
  ipv4                 :   89 matches
  url                  :   34 matches
  phone_us             :   12 matches
  date_iso             :    8 matches
```

### Sanitized Output

Input:
```
Contact john@example.com or call 555-123-4567.
SSN: 123-45-6789 is on file.
```

Output:
```
Contact [REDACTED] or call [REDACTED].
SSN: [REDACTED] is on file.
```

## Regex Educational Examples

### Email Pattern Explained

```python
r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
```

- `\b` - Word boundary
- `[A-Za-z0-9._%+-]+` - Local part (letters, numbers, dots, etc.)
- `@` - Literal @ symbol
- `[A-Za-z0-9.-]+` - Domain name
- `\.[A-Z|a-z]{2,}` - TLD (2+ letters)
- `\b` - Word boundary

### IPv4 Pattern Explained

```python
r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
```

- `25[0-5]` - 250-255
- `2[0-4][0-9]` - 200-249
- `[01]?[0-9][0-9]?` - 0-199
- Each group separated by dots, repeated 3 times

## Use Cases

1. **Data Mining**: Extract contacts from documents
2. **Log Analysis**: Find IPs and URLs in server logs
3. **Data Cleaning**: Sanitize sensitive information
4. **SEO Analysis**: Find and count URLs
5. **Contact Gathering**: Build email lists from text
6. **Validation**: Verify data format compliance

## License

MIT License - Educational purposes
