# Image Metadata Viewer

A Python utility for extracting and displaying EXIF metadata from images, including camera information, GPS coordinates, and camera settings.

## Features

- **EXIF Data Extraction**: Reads all EXIF tags from images
- **Camera Information**: Make, model, software, lens details
- **Camera Settings**: Exposure time, aperture, ISO, focal length
- **GPS Coordinates**: Extracts latitude, longitude, altitude with Google Maps link
- **Date/Time**: Original, digitized, and modified timestamps
- **JSON Export**: Export all metadata for further processing

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### View All Metadata

```bash
python image-metadata.py photo.jpg
```

### Export as JSON

```bash
python image-metadata.py photo.jpg -o metadata.json
```

### GPS Only

```bash
python image-metadata.py photo.jpg --gps-only
```

### Camera Info Only

```bash
python image-metadata.py photo.jpg --camera-only
```

## Supported Formats

- JPEG (most common for photos with EXIF)
- PNG (limited EXIF support)
- TIFF
- WebP
- Other formats supported by Pillow

## EXIF Tags Extracted

| Category | Tags |
|----------|------|
| Camera | Make, Model, Software, Lens |
| Settings | Exposure, Aperture, ISO, Focal Length |
| GPS | Latitude, Longitude, Altitude, Timestamp |
| Date/Time | Original, Digitized, Modified |
| Image | Dimensions, Color Mode, Orientation |

## Output Example

```
📷 IMAGE INFORMATION
   File: vacation.jpg
   Format: JPEG
   Size: 4032 x 3024 pixels
   Mode: RGB
   File size: 3,456,789 bytes (3.3 MB)
   EXIF data: Yes

📷 CAMERA INFORMATION
   Make: Apple
   Model: iPhone 14 Pro
   Software: 17.0

⚙️  CAMERA SETTINGS
   Exposure: 1/120 sec
   Aperture: f/1.8
   ISO: 100
   Focal Length: 6.9mm

📅 DATE/TIME
   Original: 2024:07:15 14:30:45

📍 GPS LOCATION
   Latitude: 37.774929
   Longitude: -122.419415
   Google Maps: https://www.google.com/maps?q=37.774929,-122.419415
```

## Privacy Note

EXIF metadata can reveal sensitive information:
- Exact GPS location where photo was taken
- Device make and model
- Date and time of photo

Consider stripping EXIF data before sharing photos online using tools like `exiftool`.

## Library Used

- **Pillow**: Python Imaging Library for image handling and EXIF extraction

## License

MIT License - Educational purposes
