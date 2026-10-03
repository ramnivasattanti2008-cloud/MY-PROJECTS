# Image Cropper Tool

Crop images with interactive selection or CLI using exact coordinates.

## Features

- **Interactive Mode**: Visual click-and-drag selection with preview
- **Pixel Coordinates**: Crop using exact pixel values
- **Percentage Coordinates**: Crop using relative percentages (0-100)
- **Batch Processing**: Crop all images in a directory
- **Multiple Formats**: Supports PNG, JPG, JPEG, BMP, WebP, TIFF, GIF

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Default)

```bash
python image-cropper.py -i photo.jpg -o cropped.jpg
```

Opens a visual editor where you can:
- Click and drag to select crop region
- Double-click to select full image
- Press ESC to cancel

### CLI with Pixel Coordinates

```bash
python image-cropper.py -i photo.jpg -o cropped.jpg -c 100,100,400,400
```

### CLI with Percentage Coordinates

```bash
python image-cropper.py -i photo.jpg -o cropped.jpg -p 10,10,90,90
```

### Using Individual Coordinate Flags

```bash
python image-cropper.py -i photo.jpg -o cropped.jpg --left 100 --top 100 --right 400 --bottom 400
```

### Batch Processing

```bash
# Crop all images in directory with same coordinates
python image-cropper.py -i ./photos/ -o ./cropped/ -c 50,50,750,550
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Input image file or directory | Required |
| `-o, --output` | Output file or directory | Required |
| `-c, --coords` | Region as left,top,right,bottom (pixels) | - |
| `-p, --percent` | Region as left,top,right,bottom (percent) | - |
| `--left` | Left coordinate | - |
| `--top` | Top coordinate | - |
| `--right` | Right coordinate | - |
| `--bottom` | Bottom coordinate | - |

## Coordinate Systems

### Pixel Coordinates

Absolute pixel values from image origin (top-left corner).

Example: `-c 100,100,400,400` crops from pixel (100,100) to (400,400).

### Percentage Coordinates

Relative values from 0-100 representing the percentage of image dimensions.

Example: `-p 10,10,90,90` crops 10% margin on all sides.

### Interactive Mode

- Click and drag to draw selection rectangle
- Selection shows coordinates in preview
- Double-click to select entire image
- ESC cancels without cropping

## Programmatic Usage

```python
from image_cropper import ImageCropper

cropper = ImageCropper()

# Pixel coordinates
cropper.crop('input.jpg', 'output.jpg',
             left=100, top=100, right=400, bottom=400)

# Percentage coordinates
cropper.crop_percent('input.jpg', 'output.jpg',
                     left_pct=10, top_pct=10,
                     right_pct=90, bottom_pct=90)

# Batch processing
results = cropper.batch_crop('./photos/', './cropped/',
                              left=0, top=0, right=800, bottom=600)
```

## Common Use Cases

### Remove Header/Footer

```bash
# Remove 50px from top and bottom
python image-cropper.py -i photo.jpg -o cropped.jpg -c 0,50,WIDTH,HEIGHT-50
```

### Square Crop (Center)

```bash
# For a 1920x1080 image, crop to 1080x1080 square
python image-cropper.py -i photo.jpg -o cropped.jpg -c 420,0,1500,1080
```

### Crop to 16:9

```bash
# Remove top/bottom to get 16:9 from any image
python image-cropper.py -i photo.jpg -o cropped.jpg -p 0,12.5,100,87.5
```

## Notes

- Coordinates are clamped to image boundaries
- Output directory is created automatically for batch processing
- Original image is not modified
- Image aspect ratio can change based on crop region
