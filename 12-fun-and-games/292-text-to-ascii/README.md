# Image to ASCII Art Converter

Transform any image into stunning ASCII art! Perfect for creating text-based versions of photos, logos, and graphics.

## Features

- Convert images to ASCII characters
- Multiple character sets (simple to detailed)
- Adjustable width and contrast
- Color ASCII output (if terminal supports)
- Save output to file
- Preview before saving

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Basic conversion
python text-to-ascii.py --image photo.jpg

# Custom width
python text-to-ascii.py --image photo.jpg --width 100

# Detailed characters (more gradients)
python text-to-ascii.py --image photo.jpg --chars " ..,:;clodxkO0KXN"

# Save to file
python text-to-ascii.py --image photo.jpg --save output.txt

# Color output (if terminal supports)
python text-to-ascii.py --image photo.jpg --color
```

### Python API

```python
from text_to_ascii import ImageToASCII

converter = ImageToASCII()
converter.load_image("photo.jpg")
ascii_art = converter.convert(width=80, chars="@%#*+=-:. ")
print(ascii_art)
```

## Character Sets

Different character sets produce different effects:

- **Simple**: ` ..::!!@@##` - Quick, basic output
- **Standard**: ` .:-=+*#%@` - Balanced detail
- **Detailed**: ` .',:;!|\\(){}[]~*rz?tycxlcJU0OZXYI5SHVNM` - High detail
- **Blocks**: ` ░▒▓█` - Solid blocks
- **Binary**: `01` - Computer style

## Tips

- Smaller widths produce larger ASCII art
- High-contrast images work best
- Try different character sets for different effects
- Color mode requires a terminal that supports ANSI colors

## Examples

```bash
# Portrait conversion
python text-to-ascii.py --image portrait.jpg --width 60

# Landscape conversion
python text-to-ascii.py --image landscape.jpg --width 120

# Monochrome block style
python text-to-ascii.py --image logo.png --chars " ░▒▓█" --save blocks.txt
```

## Requirements

- Python 3.6+
- Pillow (Python Imaging Library)
