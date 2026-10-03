# Screenshot Tool

A Python script for capturing screenshots with hotkey support. Supports full screen and region capture on Windows and macOS.

## Features

- Full screen capture with one keypress
- Region capture (drag to select area)
- Global hotkey support (works even when script is in background)
- Automatic timestamp naming
- Configurable save location
- Interactive menu mode for manual control

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Hotkey Mode)
```bash
python screenshot-tool.py
```

**Hotkeys:**
- **F12** - Take full screen screenshot
- **F11** - Take region screenshot
- **Q** - Quit the program

### Change Save Location
```bash
python screenshot-tool.py "C:\MyScreenshots"
```

### Manual Mode
When prompted, choose manual mode to access the menu:
```
1 - Full screen screenshot
2 - Region screenshot
3 - Change save directory
Q - Quit
```

## Requirements

- Python 3.6 or higher
- **Windows**: mss, pyautogui, keyboard
- **macOS**: Pillow (for basic capture)

## Default Save Locations

- **Windows**: `C:\Users\<username>\Pictures\Screenshots`
- **macOS**: `~/Pictures/Screenshots`

## Example Output

```
==================================================
SCREENSHOT TOOL
Capture screenshots with hotkey support
==================================================

Save directory: C:\Users\Username\Pictures\Screenshots

Hotkeys:
  F12 - Full screen screenshot
  F11 - Region screenshot
  Q   - Quit
--------------------------------------------------
Listening for hotkeys... (Press Q to quit)

Screenshot saved!
  File: screenshot_2024-01-15_14-30-00.png
  Location: C:\Users\Username\Pictures\Screenshots
  Size: 245.3 KB
  Full path: C:\Users\Username\Pictures\Screenshots\screenshot_2024-01-15_14-30-00.png
```

## Tips

- Add the script to startup for always-available screenshots
- Use region capture for quick annotations
- Screenshots are automatically named with timestamps for easy sorting
