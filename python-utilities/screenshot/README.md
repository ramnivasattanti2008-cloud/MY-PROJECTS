# Screenshot Tool

Take screenshots - full screen or with interactive region selection.

## Features

- **Full Screen Capture**: Screenshot your entire display(s)
- **Interactive Region Selection**: Click and drag to select an area
- **Coordinate-based Capture**: Specify exact pixel coordinates
- **Custom Output**: Choose filename and save location
- **Capture Delay**: Set a timer before capturing
- **Cursor Capture**: Optionally include mouse cursor
- **Multiple Formats**: PNG, JPG, BMP output

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Region Selection (Default)

```bash
python screenshot.py
```

Click and drag to select the region you want to capture. Press ESC to cancel.

### Full Screen Capture

```bash
python screenshot.py -f
```

### Region Selection Mode

```bash
python screenshot.py -r
```

### Specific Coordinates

```bash
# Format: left,top,right,bottom
python screenshot.py -c 100,100,800,600
```

### Custom Output

```bash
# Custom filename
python screenshot.py -f -o my_screenshot.png

# Custom directory
python screenshot.py -f -d ./captures/

# Both
python screenshot.py -f -d ./captures/ -o important.png
```

### Delayed Capture

```bash
# 3 second delay (useful for capturing menus, tooltips)
python screenshot.py -f --delay 3
```

### Include Cursor

```bash
python screenshot.py -f --cursor
```

### Change Format

```bash
python screenshot.py -f --format jpg
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --full` | Capture full screen | False |
| `-r, --region` | Interactive region selection | False |
| `-c, --coords` | Region as left,top,right,bottom | - |
| `-o, --output` | Output filename | Auto-generated |
| `-d, --directory` | Save directory | ~/Pictures/Screenshots |
| `--delay` | Delay before capture (seconds) | 0 |
| `--cursor` | Include cursor in capture | False |
| `--format` | Output format (png/jpg/bmp) | png |

## Programmatic Usage

```python
from screenshot import ScreenshotTool

tool = ScreenshotTool()

# Full screen
path = tool.capture_full_screen()

# Specific region
path = tool.capture_region((100, 100, 800, 600))

# Custom save path
path = tool.capture_full_screen('screenshot.png')

# Custom directory
tool.default_save_dir = './captures/'
path = tool.capture_full_screen()

# Interactive selection
bbox = tool.interactive_region_select()
if bbox:
    path = tool.capture_region(bbox)
```

## Region Selection

The interactive region selector:
- Creates a full-screen overlay
- Click and drag to draw a selection rectangle
- Release to capture the selected region
- Press ESC to cancel
- Minimum selection size: 5x5 pixels

## Coordinate System

Coordinates use standard screen coordinates:
- `(0, 0)` = top-left corner
- Positive X increases to the right
- Positive Y increases downward

Example: `100,100,800,600` captures from pixel (100,100) to (800,600).

## Default Save Location

Screenshots are saved to:
- Windows: `~/Pictures/Screenshots/`
- macOS: `~/Pictures/Screenshots/`
- Linux: `~/Pictures/Screenshots/`

Default filename format: `screenshot_YYYYMMDD_HHMMSS.png`

## Notes

- On multi-monitor setups, full screen captures all monitors
- PNG format recommended for screenshots (lossless)
- Cursor capture may not work on all systems
