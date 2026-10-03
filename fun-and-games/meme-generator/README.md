# Meme Generator

A fun and easy tool to create memes by adding text to images. Perfect for creating classic memes with top and bottom text!

## Features

- Add top and bottom text to any image
- Classic meme styling with Impact font
- Automatic text sizing based on image width
- Preview before saving
- Support for PNG, JPG, and other common formats

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Basic meme with top and bottom text
python meme-generator.py --image photo.jpg --top "When you fix a bug" --bottom "And it creates 10 more"

# Meme with only top text
python meme-generator.py --image photo.jpg --top "Me explaining my code"

# Meme with only bottom text
python meme-generator.py --image photo.jpg --bottom "Nobody:"
```

### Python API

```python
from meme_generator import MemeGenerator

# Create a meme
generator = MemeGenerator()
generator.create_meme(
    image_path="photo.jpg",
    top_text="When the code works",
    bottom_text="But nobody knows why"
)
generator.save("my_meme.png")
```

## Text Styling

The meme generator automatically:
- Centers text horizontally
- Uses white color with black outline for maximum readability
- Scales text size based on image width
- Adds uppercase transformation for classic meme look

## Example Memes

```bash
# Classic "Drake Hotline Bling" format
python meme-generator.py --image drake.jpg --top "Debugging for 2 hours" --bottom "Finally finding the missing semicolon"

# Distracted Boyfriend style
python meme-generator.py --image boyfriend.jpg --top "Writing documentation" --bottom "Reading documentation"

# Change My Mind sign
python meme-generator.py --image sign.jpg --top "Python is the best language"
```

## Tips

1. Use high-resolution images for better quality
2. Keep text short for best results
3. Square or portrait images work best for memes
4. Use simple backgrounds for better text readability

## Requirements

- Python 3.6+
- Pillow (Python Imaging Library)
