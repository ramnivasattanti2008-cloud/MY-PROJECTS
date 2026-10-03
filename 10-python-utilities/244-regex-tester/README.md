# Regex Tester

Interactive regex pattern testing with highlighted matches and detailed group information.

## Features

- Interactive mode for exploring regex patterns
- One-shot mode for scripting/CI integration
- Match highlighting with colors
- Captured group display
- Named group support
- Multiple flag support (IGNORECASE, MULTILINE, DOTALL, VERBOSE)
- Detailed match position and content info

## Installation

```bash
pip install -r requirements.txt
# (No external dependencies required)
```

## Usage

### Interactive Mode

```bash
python regex-tester.py
```

In interactive mode:
1. Enter a pattern ending with `/` to set the regex
2. Enter text to search
3. Matches are displayed with highlighting

Commands:
- `:q` or `:quit` - Exit
- `:flags <flags>` - Set flags (i, m, s, x)
- `:clear` - Clear current text
- `:help` - Show help

### One-Shot Mode

```bash
# Basic usage
python regex-tester.py -p "pattern" -t "text to search"

# Case insensitive
python regex-tester.py -p "hello" -t "HELLO World" -i

# With flags
python regex-tester.py -p "\\\\d+" -t "abc 123 def" -f i

# Quiet mode (exit code only)
python regex-tester.py -p "error" -t "no error here" -q
```

## Flags

| Flag | Short | Description |
|------|-------|-------------|
| `re.IGNORECASE` | `i` | Case-insensitive matching |
| `re.MULTILINE` | `m` | `^` and `$` match line boundaries |
| `re.DOTALL` | `s` | `.` matches any character including newline |
| `re.VERBOSE` | `x` | Ignore whitespace, allow comments |

## Examples

### Email Validation

```
> /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\\.[a-zA-Z]{2,}/
> john.doe@example.com

==============================================================
Found 1 matches
==============================================================

[Match 1] Position: 0-20
  Full match: 'john.doe@example.com'
```

### Phone Numbers

```
> /\\\\d{3}-\\\\d{3}-\\\\d{4}/
> Call 555-123-4567 or 555-987-6543

[Match 1] Position: 5-16
  Full match: '555-123-4567'

[Match 2] Position: 21-32
  Full match: '555-987-6543'
```

### Named Groups

```
> /(?P<year>\\\\d{4})-(?P<month>\\\\d{2})-(?P<day>\\\\d{2})/
> Date: 2024-01-15

[Match 1] Position: 6-16
  Full match: '2024-01-15'
  Named groups:
    year: '2024'
    month: '01'
    day: '15'
```

### Interactive Session

```
Regex Tester - Interactive Mode
==================================================
Commands:
  :q, :quit          - Exit
  :flags <flags>     - Set flags (i, m, s, x)
  :clear             - Clear text
  :help              - Show this help
==================================================

> /\\\\d+/
Pattern: \\d+

> some text with 123 numbers 456
==============================================================
Found 2 matches
==============================================================

[Match 1] Position: 14-17
  Full match: '123'

[Match 2] Position: 27-30
  Full match: '456'

> :flags i
Flags set: i

> HELLO world hello World
==============================================================
Found 3 matches
==============================================================
```

## Return Codes

- `0`: Pattern matched at least once
- `1`: No matches found or error occurred

Useful for scripting:
```bash
if python regex-tester.py -p "error" -t "$log_content" -q; then
    echo "Found errors!"
fi
```

## Syntax Notes

- Use raw strings or escape backslashes: `\\d+` or `\\\\d+`
- In shell, escape appropriately for your shell
- Patterns without `/` delimiter are treated as text input
