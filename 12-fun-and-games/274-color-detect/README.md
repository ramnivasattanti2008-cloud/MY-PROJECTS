# Color Detector

Upload any image and discover its dominant colors! Perfect for designers, artists, and anyone curious about color palettes.

## Features

- Upload any image (PNG, JPG, BMP, GIF)
- Extract dominant colors automatically
- Display color information with hex codes
- Create beautiful color palettes
- Copy hex codes to clipboard
- Save color palette as image

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Basic color detection
python color-detect.py --image photo.jpg

# Show top 10 colors
python color-detect.py --image photo.jpg --count 10

# Save palette to file
python color-detect.py --image photo.jpg --save palette.png

# Interactive mode
python color-detect.py -i
```

### Python API

```python
from color_detect import ColorDetector

detector = ColorDetector("photo.jpg")
colors = detector.get_dominant_colors(5)

for color in colors:
    print(f"RGB: {color.rgb}, Hex: {color.hex}, Percentage: {color.percentage}%")

detector.save_palette("my_palette.png")
```

## Example Output

```
Analyzing image: photo.jpg
Image size: 1920x1080

Top 5 Dominant Colors:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ■  #FF6B6B  RGB(255, 107, 107)  24.5%
  ■  #4ECDC4  RGB( 78, 205, 196)  18.3%
  ■  #45B7D1  RGB( 69, 183, 209)  15.7%
  ■  #96CEB4  RGB(150, 206, 180)  12.1%
  ■  #FFEAA7  RGB(255, 234, 167)   8.9%

Color Palette:
[■■■■■■■■■■] ████████████████████
```

## Color Matching

The tool also identifies the closest color name from a curated list including:
- Primary colors (red, blue, yellow)
- Secondary colors (orange, purple, green)
- Extended named colors (coral, turquoise, lavender, etc.)

## Tips

- Higher resolution images give more accurate results
- Images with fewer distinct colors will have higher percentages
- Try different `--count` values to find the right balance
- Use `--save` to create a palette image for reference

## Requirements

- Python 3.6+
- Pillow (image processing)
- NumPy (numerical operations)
