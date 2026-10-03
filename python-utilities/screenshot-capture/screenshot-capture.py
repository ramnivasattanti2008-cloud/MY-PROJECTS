"""
Screenshot Capture - Take screenshots using Pillow and Windows GDI.
Full screen or region selection. Auto-saves with timestamp filenames.
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

try:
    import win32gui
    import win32ui
    import win32con
    import win32api
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

from PIL import Image


def get_virtual_screen_size():
    """Get the virtual screen dimensions (all monitors)."""
    try:
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        return left, top, width, height
    except Exception:
        return 0, 0, 1920, 1080


def capture_full_screen() -> Image.Image:
    """
    Capture the entire virtual screen (all monitors) using Windows GDI.
    """
    if not WIN32_AVAILABLE:
        raise RuntimeError("win32gui/win32ui required. Install: pip install pywin32")

    left, top, width, height = get_virtual_screen_size()

    # Create device context
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    memdc = hdc.CreateCompatibleDC()

    # Create bitmap
    hbitmap = win32ui.CreateBitmap()
    hbitmap.CreateCompatibleBitmap(hdc, width, height)
    memdc.SelectObject(hbitmap)

    # Copy screen content
    MEMDC = win32con.SRCCOPY
    memdc.BitBlt((0, 0), (width, height), hdc, (left, top), MEMDC)

    # Convert to PIL Image
    bmpinfo = hbitmap.GetInfo()
    bmpstr = hbitmap.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )

    # Cleanup
    win32gui.DeleteObject(hbitmap.GetHandle())
    memdc.DeleteDC()
    hdc.DeleteDC()

    return img


def capture_primary_screen() -> Image.Image:
    """
    Capture only the primary monitor using Pillow's MS-ScreenCapture.
    Falls back to full virtual screen if unavailable.
    """
    try:
        # Pillow 9.1+ supports screen capture on Windows
        img = ImageGrab.grab()
        return img
    except Exception:
        return capture_full_screen()


def capture_region(x: int, y: int, width: int, height: int) -> Image.Image:
    """
    Capture a specific region of the screen.

    Args:
        x: Left coordinate
        y: Top coordinate
        width: Region width in pixels
        height: Region height in pixels
    """
    if not WIN32_AVAILABLE:
        raise RuntimeError("win32gui/win32ui required. Install: pip install pywin32")

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    memdc = hdc.CreateCompatibleDC()

    hbitmap = win32ui.CreateBitmap()
    hbitmap.CreateCompatibleBitmap(hdc, width, height)
    memdc.SelectObject(hbitmap)

    MEMDC = win32con.SRCCOPY
    memdc.BitBlt((0, 0), (width, height), hdc, (x, y), MEMDC)

    bmpinfo = hbitmap.GetInfo()
    bmpstr = hbitmap.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )

    win32gui.DeleteObject(hbitmap.GetHandle())
    memdc.DeleteDC()
    hdc.DeleteDC()

    return img


def capture_window(window_title: str = None) -> Image.Image:
    """
    Capture a specific window by title, or the foreground window if None.
    """
    if not WIN32_AVAILABLE:
        raise RuntimeError("win32gui/win32ui required. Install: pip install pywin32")

    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd == 0:
            # Try partial match
            windows = []
            def enum_callback(h, _):
                title = win32gui.GetWindowText(h)
                if title and window_title.lower() in title.lower():
                    windows.append(h)
                return True
            win32gui.EnumWindows(enum_callback, None)
            if windows:
                hwnd = windows[0]
            else:
                raise ValueError(f"Window not found: '{window_title}'")
    else:
        hwnd = win32gui.GetForegroundWindow()

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    hdc = win32gui.GetDC(hwnd)
    memdc = win32ui.CreateDCFromHandle(hdc).CreateCompatibleDC()

    hbitmap = win32ui.CreateBitmap()
    hbitmap.CreateCompatibleBitmap(win32ui.CreateDCFromHandle(hdc), width, height)
    memdc.SelectObject(hbitmap)
    MEMDC = win32con.SRCCOPY
    memdc.BitBlt((0, 0), (width, height), win32ui.CreateDCFromHandle(hdc), (0, 0), MEMDC)

    bmpinfo = hbitmap.GetInfo()
    bmpstr = hbitmap.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )

    win32gui.DeleteObject(hbitmap.GetHandle())
    memdc.DeleteDC()
    hdc.DeleteDC()

    return img


def list_windows():
    """List all open window titles."""
    if not WIN32_AVAILABLE:
        print("win32gui not available")
        return
    windows = []
    def enum_callback(h, _):
        title = win32gui.GetWindowText(h)
        if title and win32gui.IsWindowVisible(h):
            windows.append(title)
        return True
    win32gui.EnumWindows(enum_callback, None)
    for w in windows[:30]:
        print(f"  {w}")


def save_screenshot(img: Image.Image, output_path: str = None,
                   format: str = None, quality: int = 95) -> str:
    """
    Save screenshot to file with timestamp if no path given.
    Returns the actual path saved.
    """
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"screenshot_{timestamp}.png"

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    save_kwargs = {}
    fmt = format or Path(output_path).suffix.lstrip('.').upper()
    if fmt in ('JPEG', 'JPG'):
        save_kwargs['format'] = 'JPEG'
        save_kwargs['quality'] = quality
        save_kwargs['optimize'] = True
        img = img.convert('RGB')
    elif fmt == 'PNG':
        save_kwargs['format'] = 'PNG'
    elif fmt == 'WEBP':
        save_kwargs['format'] = 'WebP'
        save_kwargs['quality'] = quality

    img.save(output_path, **save_kwargs)
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Screenshot Capture - Take screenshots on Windows',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Capture full screen, save with timestamp
  python screenshot-capture.py

  # Capture full screen to specific file
  python screenshot-capture.py -o my_screenshot.png

  # Capture a region (x, y, width, height)
  python screenshot-capture.py -o region.png --region 100 100 800 600

  # Capture specific window
  python screenshot-capture.py -o window.png --window "Notepad"

  # Capture foreground window
  python screenshot-capture.py -o active.png --window-active

  # List open windows
  python screenshot-capture.py --list-windows

  # Save as JPEG with quality
  python screenshot-capture.py -o screenshot.jpg --format JPEG --quality 85
'''
    )
    parser.add_argument('-o', '--output', help='Output file path (auto timestamp if omitted)')
    parser.add_argument('--region', nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'),
                        help='Region: x y width height')
    parser.add_argument('--window', metavar='TITLE',
                        help='Capture specific window by title (partial match)')
    parser.add_argument('--window-active', action='store_true',
                        help='Capture the currently active/foreground window')
    parser.add_argument('--full', action='store_true',
                        help='Capture full virtual screen (all monitors)')
    parser.add_argument('--format', choices=['PNG', 'JPEG', 'WebP'],
                        help='Output format (default: PNG)')
    parser.add_argument('-q', '--quality', type=int, default=95,
                        help='JPEG/WebP quality 1-100 (default: 95)')
    parser.add_argument('--list-windows', action='store_true',
                        help='List open window titles')

    args = parser.parse_args()

    if args.list_windows:
        print("Open windows:")
        list_windows()
        return

    if not WIN32_AVAILABLE:
        print("ERROR: pywin32 is required for screenshot capture on Windows.")
        print("Install it with: pip install pywin32")
        sys.exit(1)

    print("Capturing screenshot...", end=' ')
    try:
        if args.region:
            x, y, w, h = args.region
            print(f"region ({x}, {y}, {w}x{h})")
            img = capture_region(x, y, w, h)
        elif args.window:
            print(f"window: '{args.window}'")
            img = capture_window(args.window)
        elif args.window_active:
            title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            print(f"active window: '{title}'")
            img = capture_window()
        elif args.full:
            print("full virtual screen (all monitors)")
            img = capture_full_screen()
        else:
            print("primary screen")
            img = capture_primary_screen()

        path = save_screenshot(img, args.output, args.format, args.quality)
        size_kb = os.path.getsize(path) // 1024
        print(f"Saved: {path} ({img.size[0]}x{img.size[1]}, {size_kb}KB)")

    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
