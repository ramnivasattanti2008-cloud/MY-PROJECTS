#!/usr/bin/env python3
"""
Image Metadata Viewer - Extract and display EXIF metadata from images.

This script reads and displays EXIF (Exchangeable Image File Format) metadata
from images taken by digital cameras and smartphones.

Educational Purpose:
- Demonstrates EXIF metadata structure
- Shows how to extract GPS coordinates from photos
- Explains camera settings and their meanings
- Teaches image processing with Pillow

Author: Educational Example
License: MIT
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    print("Error: Pillow library not installed.")
    print("Run: pip install Pillow")
    sys.exit(1)


class ImageMetadataViewer:
    """
    Extract and display EXIF metadata from images.

    Supports JPEG, PNG, TIFF, and other common image formats.
    """

    def __init__(self, image_path: str):
        """
        Initialize the viewer with an image file.

        Args:
            image_path: Path to the image file
        """
        self.image_path = Path(image_path)

        if not self.image_path.exists():
            raise FileNotFoundError(f"Image not found: {self.image_path}")

        self.image = None
        self.exif_data = None
        self._load_image()

    def _load_image(self):
        """Load the image and extract EXIF data."""
        try:
            self.image = Image.open(self.image_path)

            # Extract EXIF data (only works for JPEG, PNG, TIFF, etc.)
            if hasattr(self.image, '_getexif') and self.image._getexif():
                self.exif_data = self.image._getexif()
            else:
                self.exif_data = {}

        except Exception as e:
            raise ValueError(f"Error opening image: {e}")

    def get_all_metadata(self) -> dict:
        """
        Get all EXIF metadata as a dictionary.

        Returns:
            Dictionary mapping TAG names to values
        """
        if not self.exif_data:
            return {}

        metadata = {}
        for tag_id, value in self.exif_data.items():
            tag_name = TAGS.get(tag_id, f"Unknown ({tag_id})")
            metadata[tag_name] = self._convert_value(value)

        return metadata

    def _convert_value(self, value):
        """Convert EXIF values to human-readable format."""
        if isinstance(value, tuple) and len(value) == 2:
            # Rational numbers (like 1/100 second exposure)
            try:
                return f"{value[0]}/{value[1]} ({value[0]/value[1]:.4f})"
            except (ValueError, ZeroDivisionError):
                return value

        if isinstance(value, bytes):
            # Try to decode as string
            try:
                return value.decode('utf-8', errors='replace')
            except:
                return f"<{len(value)} bytes>"

        return value

    def get_camera_info(self) -> dict:
        """Extract camera-specific information."""
        if not self.exif_data:
            return {}

        camera_info = {}

        # Camera make and model
        camera_info['make'] = self.exif_data.get(271, 'Unknown')
        camera_info['model'] = self.exif_data.get(272, 'Unknown')

        # Software
        camera_info['software'] = self.exif_data.get(305, 'Unknown')

        # Date/Time
        camera_info['datetime'] = self.exif_data.get(306, 'Unknown')
        camera_info['datetime_original'] = self.exif_data.get(36867, 'Unknown')
        camera_info['datetime_digitized'] = self.exif_data.get(36868, 'Unknown')

        # Settings
        camera_info['exposure_time'] = self._format_exposure(
            self.exif_data.get(33434) or self.exif_data.get(282)
        )
        camera_info['f_number'] = self._format_f_number(
            self.exif_data.get(33437) or self.exif_data.get(388)
        )
        camera_info['iso'] = self.exif_data.get(34855, 'Unknown')
        camera_info['focal_length'] = self._format_focal_length(
            self.exif_data.get(37386) or self.exif_data.get(41989)
        )

        # Lens info
        camera_info['lens_make'] = self.exif_data.get(42035, 'Unknown')
        camera_info['lens_model'] = self.exif_data.get(42036, 'Unknown')

        return {k: v for k, v in camera_info.items() if v and v != 'Unknown'}

    def _format_exposure(self, value) -> Optional[str]:
        """Format exposure time as a fraction."""
        if not value:
            return None
        if isinstance(value, tuple):
            return f"1/{int(value[0]/value[1] + 0.5)} sec"
        return str(value)

    def _format_f_number(self, value) -> Optional[str]:
        """Format f-number (aperture)."""
        if not value:
            return None
        if isinstance(value, tuple):
            return f"f/{value[0]/value[1]:.1f}"
        return f"f/{value}"

    def _format_focal_length(self, value) -> Optional[str]:
        """Format focal length."""
        if not value:
            return None
        if isinstance(value, tuple):
            return f"{value[0]/value[1]:.1f}mm"
        return f"{value}mm"

    def get_gps_coordinates(self) -> Optional[dict]:
        """
        Extract GPS coordinates from EXIF data.

        Returns:
            Dictionary with latitude, longitude, and altitude, or None
        """
        if not self.exif_data:
            return None

        # GPS IFD tag
        gps_ifd = self.exif_data.get(34853)
        if not gps_ifd:
            return None

        gps_info = {}
        for tag_id, value in gps_ifd.items():
            tag_name = GPSTAGS.get(tag_id, str(tag_id))
            gps_info[tag_name] = value

        # Extract latitude
        lat = self._convert_gps_coordinate(
            gps_info.get('GPSLatitude'),
            gps_info.get('GPSLatitudeRef')
        )

        # Extract longitude
        lon = self._convert_gps_coordinate(
            gps_info.get('GPSLongitude'),
            gps_info.get('GPSLongitudeRef')
        )

        # Extract altitude
        altitude = None
        if 'GPSAltitude' in gps_info:
            alt = gps_info['GPSAltitude']
            if isinstance(alt, tuple):
                altitude = alt[0] / alt[1]
            else:
                altitude = alt

        if lat is not None and lon is not None:
            return {
                'latitude': lat,
                'longitude': lon,
                'altitude': altitude,
                'latitude_ref': gps_info.get('GPSLatitudeRef'),
                'longitude_ref': gps_info.get('GPSLongitudeRef'),
                'google_maps_url': f"https://www.google.com/maps?q={lat},{lon}"
            }

        return None

    def _convert_gps_coordinate(self, coord, ref) -> Optional[float]:
        """Convert GPS coordinate tuple to decimal degrees."""
        if not coord or not ref:
            return None

        try:
            degrees = coord[0][0] / coord[0][1]
            minutes = coord[1][0] / coord[1][1]
            seconds = coord[2][0] / coord[2][1]

            decimal = degrees + minutes / 60 + seconds / 3600

            # Apply direction
            if ref in ['S', 'W']:
                decimal = -decimal

            return round(decimal, 6)
        except (TypeError, ZeroDivisionError, IndexError):
            return None

    def get_image_info(self) -> dict:
        """Get basic image information."""
        return {
            'filename': self.image_path.name,
            'format': self.image.format,
            'mode': self.image.mode,
            'size': self.image.size,
            'width': self.image.width,
            'height': self.image.height,
            'file_size': self.image_path.stat().st_size,
            'has_exif': bool(self.exif_data),
        }

    def print_report(self):
        """Print a formatted metadata report."""
        print("\n" + "=" * 60)
        print("IMAGE METADATA REPORT")
        print("=" * 60)

        # Image info
        info = self.get_image_info()
        print(f"\n📷 IMAGE INFORMATION")
        print(f"   File: {info['filename']}")
        print(f"   Format: {info['format']}")
        print(f"   Size: {info['width']} x {info['height']} pixels")
        print(f"   Mode: {info['mode']}")
        print(f"   File size: {info['file_size']:,} bytes ({info['file_size']/1024:.1f} KB)")
        print(f"   EXIF data: {'Yes' if info['has_exif'] else 'No'}")

        # Camera info
        camera = self.get_camera_info()
        if camera:
            print(f"\n📷 CAMERA INFORMATION")
            if 'make' in camera:
                print(f"   Make: {camera['make']}")
            if 'model' in camera:
                print(f"   Model: {camera['model']}")
            if 'software' in camera:
                print(f"   Software: {camera['software']}")
            if 'lens_make' in camera and camera['lens_make'] != 'Unknown':
                print(f"   Lens: {camera['lens_make']} {camera['lens_model']}")

        # Settings
        settings_found = False
        settings_str = "\n⚙️  CAMERA SETTINGS"
        if camera.get('exposure_time'):
            settings_str += f"\n   Exposure: {camera['exposure_time']}"
            settings_found = True
        if camera.get('f_number'):
            settings_str += f"\n   Aperture: {camera['f_number']}"
            settings_found = True
        if camera.get('iso'):
            settings_str += f"\n   ISO: {camera['iso']}"
            settings_found = True
        if camera.get('focal_length'):
            settings_str += f"\n   Focal Length: {camera['focal_length']}"
            settings_found = True
        if settings_found:
            print(settings_str)

        # Date/Time
        if camera.get('datetime_original'):
            print(f"\n📅 DATE/TIME")
            print(f"   Original: {camera['datetime_original']}")
            if camera.get('datetime_digitized') and camera['datetime_digitized'] != camera.get('datetime_original'):
                print(f"   Digitized: {camera['datetime_digitized']}")

        # GPS
        gps = self.get_gps_coordinates()
        if gps:
            print(f"\n📍 GPS LOCATION")
            print(f"   Latitude: {gps['latitude']}")
            print(f"   Longitude: {gps['longitude']}")
            if gps.get('altitude'):
                print(f"   Altitude: {gps['altitude']}m")
            print(f"   Google Maps: {gps['google_maps_url']}")
        else:
            print(f"\n📍 GPS LOCATION: Not available")

        # All metadata
        if self.exif_data:
            print(f"\n📋 ALL EXIF TAGS ({len(self.exif_data)} tags)")
            for tag_id, value in list(self.exif_data.items())[:20]:
                tag_name = TAGS.get(tag_id, f"Unknown ({tag_id})")
                display_value = self._convert_value(value)
                # Truncate long values
                if isinstance(display_value, str) and len(display_value) > 50:
                    display_value = display_value[:50] + "..."
                print(f"   {tag_name}: {display_value}")

            if len(self.exif_data) > 20:
                print(f"   ... and {len(self.exif_data) - 20} more tags")

        print("\n" + "=" * 60)

    def export_json(self, output_path: str):
        """Export metadata as JSON."""
        import json

        metadata = {
            'image_info': self.get_image_info(),
            'camera_info': self.get_camera_info(),
            'gps_coordinates': self.get_gps_coordinates(),
            'all_tags': self.get_all_metadata(),
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

        print(f"Metadata exported: {output_path}")


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Extract and display EXIF metadata from images.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported formats: JPEG, PNG, TIFF, WebP, and more

Examples:
  View metadata for an image:
    python image-metadata.py photo.jpg

  Export metadata as JSON:
    python image-metadata.py photo.jpg -o metadata.json

  Show only GPS location:
    python image-metadata.py photo.jpg --gps-only

  Show camera settings:
    python image-metadata.py photo.jpg --camera-only
        """
    )

    parser.add_argument('image', help='Path to the image file')
    parser.add_argument('-o', '--output', help='Output file for JSON export')
    parser.add_argument('--gps-only', action='store_true',
                        help='Show only GPS coordinates')
    parser.add_argument('--camera-only', action='store_true',
                        help='Show only camera information')

    args = parser.parse_args()

    try:
        viewer = ImageMetadataViewer(args.image)

        if args.gps_only:
            gps = viewer.get_gps_coordinates()
            if gps:
                print(f"\nGPS Coordinates: {gps['latitude']}, {gps['longitude']}")
                if gps.get('altitude'):
                    print(f"Altitude: {gps['altitude']}m")
                print(f"Google Maps: {gps['google_maps_url']}")
            else:
                print("No GPS data found in this image.")
        elif args.camera_only:
            camera = viewer.get_camera_info()
            print(f"\nCamera: {camera.get('make', 'Unknown')} {camera.get('model', 'Unknown')}")
            if camera.get('lens_model'):
                print(f"Lens: {camera['lens_model']}")
            print(f"Settings: {camera.get('exposure_time', 'N/A')}, "
                  f"{camera.get('f_number', 'N/A')}, "
                  f"ISO {camera.get('iso', 'N/A')}")
        elif args.output:
            viewer.export_json(args.output)
        else:
            viewer.print_report()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
