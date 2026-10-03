# GIF Maker Tool

Create animated GIFs from images with adjustable speed, loop, and resize options.

## Features

- **Multiple Input Methods**: Specify files directly or use a directory
- **Adjustable Speed**: Control frame duration via milliseconds or FPS
- **Loop Control**: Infinite loop or specific number of repetitions
- **Smart Resizing**: Resize frames to consistent dimensions
- **Natural Sorting**: Automatically sorts numbered files correctly
- **Preview Mode**: Inspect existing GIF properties and frames
- **Transparency Support**: Handles PNG with alpha channel

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage - Specific Files

```bash
python gif-maker.py frame1.png frame2.png frame3.png -o animation.gif
```

### From Directory

```bash
python gif-maker.py -d ./frames/ -o animation.gif
```

### Speed Control

```bash
# Using milliseconds (500ms = 2 FPS)
python gif-maker.py -d ./frames/ -o animation.gif -t 500

# Using FPS (10 FPS = 100ms per frame)
python gif-maker.py -d ./frames/ -o animation.gif --fps 10

# Fast animation (50ms = 20 FPS)
python gif-maker.py -d ./frames/ -o animation.gif -t 50
```

### Loop Control

```bash
# Infinite loop (default)
python gif-maker.py -d ./frames/ -o animation.gif

# Play once only
python gif-maker.py -d ./frames/ -o animation.gif --no-loop

# Specific number of loops
python gif-maker.py -d ./frames/ -o animation.gif -l 3
```

### Resize Frames

```bash
python gif-maker.py -d ./frames/ -o animation.gif -r 640x480
```

### Pattern Matching (Directory Mode)

```bash
# Only PNG files
python gif-maker.py -d ./frames/ -o animation.gif --pattern "*.png"

# Files starting with "frame"
python gif-maker.py -d ./frames/ -o animation.gif --pattern "frame*"
```

### Preview Existing GIF

```bash
python gif-maker.py -p animation.gif
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `files` | Image files to combine | - |
| `-d, --directory` | Directory containing images | - |
| `-o, --output` | Output GIF filename | `output.gif` |
| `-t, --duration` | Frame duration in ms | `500` |
| `-f, --fps` | Frames per second | - |
| `-l, --loop` | Loop count (0=infinite) | `0` |
| `-n, --no-loop` | Play once only | False |
| `-r, --resize` | WIDTHxHEIGHT | - |
| `--pattern` | File pattern for directory | `*` |
| `-p, --preview` | Preview existing GIF | False |

## Speed Reference

| FPS | Milliseconds |
|-----|--------------|
| 1 | 1000 |
| 2 | 500 |
| 5 | 200 |
| 10 | 100 |
| 15 | 67 |
| 24 | 42 |
| 30 | 33 |
| 60 | 17 |

## Programmatic Usage

```python
from gif_maker import GIFMaker

maker = GIFMaker()

# Basic GIF
maker.make_gif(
    ['frame1.png', 'frame2.png', 'frame3.png'],
    'animation.gif',
    duration=500,  # 500ms per frame
    loop=0  # infinite
)

# From directory
maker.make_gif_from_folder(
    './frames/',
    'animation.gif',
    duration=200,
    loop=0
)

# With resize
maker.make_gif(
    ['frame1.png', 'frame2.png'],
    'animation.gif',
    duration=300,
    resize=(640, 480)
)

# Preview
maker.preview_gif('animation.gif')
```

## Tips

- **Natural Sorting**: Files like `frame1.png`, `frame2.png`, `frame10.png` are sorted correctly
- **Transparency**: PNG with alpha channel gets white background (GIF limitation)
- **File Size**: Smaller frames = smaller GIF. Use `--resize` for optimization
- **Consistent Size**: All frames should be the same size (or use `--resize`)
- **Order Matters**: Files are processed in sorted order

## Common Use Cases

### Animation from Screenshots

```bash
python gif-maker.py -d ./screenshots/ -o demo.gif -t 200 --no-loop
```

### Animated Avatar (Square, Small)

```bash
python gif-maker.py -d ./frames/ -o avatar.gif -r 256x256 -t 100
```

### Slow-motion Effect

```bash
python gif-maker.py -d ./frames/ -o slow.gif -t 1000
```

### Fast Animation

```bash
python gif-maker.py -d ./frames/ -o fast.gif -f 30
```
