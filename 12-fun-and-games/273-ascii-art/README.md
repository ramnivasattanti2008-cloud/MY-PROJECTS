# ASCII Art Generator

A fun CLI tool that converts text into beautiful ASCII art with multiple font styles and color support.

## Features

- Multiple ASCII art fonts (block, banner, avatar, etc.)
- Color output using colorama
- Save art to file
- Copy art to clipboard

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage
python ascii-art.py "Hello World"

# With custom font
python ascii-art.py "Python" --font banner3

# With color
python ascii-art.py "Wow!" --color red --font block

# Save to file
python ascii-art.py "My Art" --save output.txt

# List available fonts
python ascii-art.py --list-fonts

# Interactive mode
python ascii-art.py -i
```

## Available Fonts

- block, banner, standard, avatar, avatar-flipped
- banner3, banner3-flipped, banner4
- digital, doh, epic, eftiwall, fender
- isometric1-4, letters, musical,_peaks
- rusto, rusto-flipped, slblock, small, isometric
- standard, univers, weird

## Available Colors

- red, green, yellow, blue, magenta, cyan, white

## Examples

```bash
python ascii-art.py "Welcome" --color cyan --font banner3
python ascii-art.py "GAME OVER" --color red --font block
python ascii-art.py "Thank You!" --color green --font avatar
```
