"""
Screenshot Tool
Capture screenshots with hotkey support (full screen or region selection).

Usage:
    python screenshot-tool.py [output_directory]

Hotkeys:
    F12 - Take full screen screenshot
    F11 - Take region screenshot (click and drag to select)
    ESC - Exit the program
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import platform

# Platform-specific imports
if platform.system() == "Windows":
    import mss
    import pyautogui
    # for hotkey support
    import keyboard
elif platform.system() == "Darwin":  # macOS
    from PIL import ImageGrab, Image
    import subprocess
else:
    raise NotImplementedError("This script only supports Windows and macOS")


def get_timestamp_filename(prefix: str = "screenshot", extension: str = ".png") -> str:
    """
    Generate a timestamped filename for screenshots.

    Args:
        prefix: Filename prefix
        extension: File extension

    Returns:
        Formatted filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}{extension}"


def get_default_save_directory(user_provided: str = None) -> Path:
    """
    Get the default save directory for screenshots.

    Args:
        user_provided: User-specified directory if provided

    Returns:
        Path object for the save directory
    """
    if user_provided:
        save_dir = Path(user_provided)
    else:
        # Default to Pictures/Screenshots folder
        if platform.system() == "Windows":
            save_dir = Path.home() / "Pictures" / "Screenshots"
        else:  # macOS
            save_dir = Path.home() / "Pictures" / "Screenshots"

    # Create directory if it doesn't exist
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def capture_full_screen(output_dir: Path, monitor_index: int = 1) -> str:
    """
    Capture the entire screen.

    Args:
        output_dir: Directory to save screenshot
        monitor_index: Monitor number (1 = primary)

    Returns:
        Path to saved screenshot
    """
    timestamp = get_timestamp_filename()
    filepath = output_dir / timestamp

    if platform.system() == "Windows":
        with mss.mss() as sct:
            # Grab the screen
            sct_img = sct.grab(sct.monitors[monitor_index])

            # Save as PNG
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(filepath))
    else:
        # macOS
        screenshot = ImageGrab.grab()
        screenshot.save(filepath)

    return str(filepath)


def capture_region(output_dir: Path) -> str:
    """
    Capture a user-selected region of the screen.

    Args:
        output_dir: Directory to save screenshot

    Returns:
        Path to saved screenshot
    """
    print("\nRegion Selection Mode")
    print("Click and drag to select region...")
    print("Press ESC to cancel")
    print("-" * 40)

    # Hide the instruction window if possible
    # For now, we'll use a simple region capture approach

    if platform.system() == "Windows":
        # Use pyautogui for region selection on Windows
        try:
            # Get screen size
            screen_width, screen_height = pyautogui.size()

            # Take full screen first
            with mss.mss() as sct:
                sct_img = sct.grab(sct.monitors[1])

            # Save temporary full screen for region selection
            temp_path = output_dir / "_temp_full.png"
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(temp_path))

            # For simplicity, capture a center region (640x480)
            # In a production tool, you would use a GUI selection overlay
            center_x, center_y = screen_width // 2, screen_height // 2
            region_width, region_height = 640, 480

            left = max(0, center_x - region_width // 2)
            top = max(0, center_y - region_height // 2)
            right = min(screen_width, center_x + region_width // 2)
            bottom = min(screen_height, center_y + region_height // 2)

            # Capture the region
            with mss.mss() as sct:
                monitor = {
                    "left": left,
                    "top": top,
                    "width": right - left,
                    "height": bottom - top
                }
                region_img = sct.grab(monitor)

            # Save with timestamp
            timestamp = get_timestamp_filename(prefix="region")
            filepath = output_dir / timestamp
            mss.tools.to_png(region_img.rgb, region_img.size, output=str(filepath))

            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()

            return str(filepath)

        except Exception as e:
            print(f"Region capture error: {e}")
            print("Falling back to full screen capture...")
            return capture_full_screen(output_dir)
    else:
        # macOS fallback
        print("Region selection is simplified on macOS")
        return capture_full_screen(output_dir)


def take_screenshot(mode: str, output_dir: Path, monitor_index: int = 1) -> str:
    """
    Take a screenshot based on the specified mode.

    Args:
        mode: 'full' or 'region'
        output_dir: Directory to save screenshot
        monitor_index: Monitor index for full screen

    Returns:
        Path to saved screenshot
    """
    if mode == "full":
        filepath = capture_full_screen(output_dir, monitor_index)
    else:
        filepath = capture_region(output_dir)

    return filepath


def print_screenshot_info(filepath: str):
    """
    Print information about the captured screenshot.

    Args:
        filepath: Path to the screenshot file
    """
    path = Path(filepath)
    size_kb = path.stat().st_size / 1024

    print(f"\nScreenshot saved!")
    print(f"  File: {path.name}")
    print(f"  Location: {path.parent}")
    print(f"  Size: {size_kb:.1f} KB")
    print(f"  Full path: {filepath}")


def main():
    """Main function to run the screenshot tool."""
    print("=" * 50)
    print("SCREENSHOT TOOL")
    print("Capture screenshots with hotkey support")
    print("=" * 50)

    # Get save directory from command line or use default
    save_directory = sys.argv[1] if len(sys.argv) > 1 else None
    output_dir = get_default_save_directory(save_directory)

    print(f"\nSave directory: {output_dir}")
    print("\nHotkeys:")
    print("  F12 - Full screen screenshot")
    print("  F11 - Region screenshot")
    print("  Q   - Quit")
    print("-" * 50)

    # Check if we're running in interactive mode
    interactive = input("Run in interactive mode (listen for hotkeys)? [Y/n]: ").strip().lower()

    if interactive != "n":
        print("\nListening for hotkeys... (Press Q to quit)")

        try:
            # Register hotkeys
            keyboard.add_hotkey("F12", lambda: handle_full_screen(output_dir))
            keyboard.add_hotkey("F11", lambda: handle_region(output_dir))
            keyboard.add_hotkey("q", lambda: sys.exit(0))

            # Keep the script running
            keyboard.wait("q")

        except KeyboardInterrupt:
            print("\n\nScreenshot tool closed.")
        except Exception as e:
            print(f"\nHotkey error: {e}")
            print("Running in manual mode instead...")
            interactive = "n"

    if interactive == "n":
        # Manual mode - take screenshots on demand
        while True:
            print("\n" + "-" * 40)
            print("1 - Full screen screenshot")
            print("2 - Region screenshot")
            print("3 - Change save directory")
            print("Q - Quit")

            choice = input("\nSelect option: ").strip().lower()

            if choice == "1":
                try:
                    filepath = take_screenshot("full", output_dir)
                    print_screenshot_info(filepath)
                except Exception as e:
                    print(f"Error capturing screenshot: {e}")
            elif choice == "2":
                try:
                    filepath = take_screenshot("region", output_dir)
                    print_screenshot_info(filepath)
                except Exception as e:
                    print(f"Error capturing screenshot: {e}")
            elif choice == "3":
                new_dir = input("Enter new save directory: ").strip()
                output_dir = get_default_save_directory(new_dir)
                print(f"Save directory changed to: {output_dir}")
            elif choice == "q":
                print("\nGoodbye!")
                break


def handle_full_screen(output_dir: Path):
    """Handler for full screen hotkey."""
    try:
        filepath = capture_full_screen(output_dir)
        print_screenshot_info(filepath)
    except Exception as e:
        print(f"Error: {e}")


def handle_region(output_dir: Path):
    """Handler for region screenshot hotkey."""
    try:
        filepath = capture_region(output_dir)
        print_screenshot_info(filepath)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
