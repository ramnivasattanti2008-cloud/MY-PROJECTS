# Screenshot Capture

Take screenshots on Windows using Pillow and Windows GDI. Full screen, specific monitors, region selection, or window capture.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Full Screen Capture

```bash
# Capture primary screen, auto-save with timestamp
python screenshot-capture.py

# Save to specific file
python screenshot-capture.py -o my_screenshot.png

# Capture all monitors (virtual screen)
python screenshot-capture.py -o all_screens.png --full
```

### Region Capture

```bash
# Capture a region: x y width height
python screenshot-capture.py -o region.png --region 100 100 800 600

# Capture 1920x1080 region starting at (0, 0)
python screenshot-capture.py -o top_left.png --region 0 0 1920 1080
```

### Window Capture

```bash
# Capture specific window by title (partial match)
python screenshot-capture.py -o notepad.png --window "Notepad"

# Capture currently active/foreground window
python screenshot-capture.py -o active.png --window-active

# List all open window titles
python screenshot-capture.py --list-windows
```

### Output Options

```bash
# Save as JPEG
python screenshot-capture.py -o shot.jpg --format JPEG --quality 85

# Save as WebP
python screenshot-capture.py -o shot.webp --format WebP --quality 90
```

## Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output file path. Auto-generates timestamped filename if omitted |
| `--region X Y W H` | Capture region: left, top, width, height in pixels |
| `--window TITLE` | Capture window by title (partial match supported) |
| `--window-active` | Capture the foreground/active window |
| `--full` | Capture full virtual screen (all monitors combined) |
| `--format` | Output format: PNG (default), JPEG, WebP |
| `-q, --quality` | Quality for JPEG/WebP 1-100 (default: 95) |
| `--list-windows` | List all open window titles |

## Auto-generated Filename

When `-o` is omitted, files are saved as:
```
screenshot_YYYYMMDD_HHMMSS.png
```

Example: `screenshot_20260906_143052.png`

## Requirements

- **Windows** (uses Windows GDI API via `pywin32`)
- Python 3.8+
- Pillow 10+
- pywin32 306+

## Notes

- `--full` captures all monitors as one combined image, useful for multi-monitor setups
- `--region` uses absolute screen coordinates (0,0 is top-left of primary screen)
- `--window` does partial title matching, so `--window "Notepad"` matches "Untitled - Notepad"
- Screenshots are captured at native screen resolution
