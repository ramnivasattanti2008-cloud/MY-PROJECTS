"""
URL Shortener
Shorten URLs using TinyURL's free API and copy to clipboard.

Usage:
    python url-shortener.py <url> [--copy]
    python url-shortener.py [--batch] [urls_file.txt]
"""

import sys
import json
import clipboard
import validators
from pathlib import Path
from datetime import datetime

# Try to import requests; fallback to urllib if not available
try:
    import requests
    USE_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.parse
    import urllib.error
    USE_REQUESTS = False


# TinyURL API endpoint
TINYURL_API = "https://tinyurl.com/api-create.php"


def validate_url(url: str) -> bool:
    """
    Validate if a string is a proper URL.

    Args:
        url: URL string to validate

    Returns:
        True if valid URL, False otherwise
    """
    return validators.url(url)


def shorten_url(url: str) -> dict:
    """
    Shorten a URL using TinyURL API.

    Args:
        url: The URL to shorten

    Returns:
        Dictionary with 'success', 'original', 'shortened', and 'error' keys
    """
    result = {
        "success": False,
        "original": url,
        "shortened": None,
        "error": None
    }

    # Validate URL first
    if not validate_url(url):
        result["error"] = "Invalid URL format"
        return result

    try:
        if USE_REQUESTS:
            # Using requests library
            response = requests.get(
                TINYURL_API,
                params={"url": url},
                timeout=10
            )
            response.raise_for_status()
            result["shortened"] = response.text.strip()
        else:
            # Using urllib fallback
            params = urllib.parse.urlencode({"url": url})
            full_url = f"{TINYURL_API}?{params}"
            with urllib.request.urlopen(full_url, timeout=10) as response:
                result["shortened"] = response.read().decode().strip()

        result["success"] = True

    except requests.exceptions.Timeout:
        result["error"] = "Request timed out"
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection error - check internet"
    except requests.exceptions.HTTPError as e:
        result["error"] = f"HTTP error: {e}"
    except Exception as e:
        result["error"] = f"Error: {str(e)}"

    return result


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to system clipboard.

    Args:
        text: Text to copy

    Returns:
        True if successful, False otherwise
    """
    try:
        clipboard.copy(text)
        return True
    except Exception as e:
        print(f"  (Clipboard error: {e})")
        return False


def save_to_history(entry: dict, history_file: Path):
    """
    Save a URL shortening entry to history file.

    Args:
        entry: Dictionary with URL info
        history_file: Path to history file
    """
    try:
        history_file.parent.mkdir(parents=True, exist_ok=True)

        # Read existing history or create new
        if history_file.exists():
            with open(history_file, "r") as f:
                history = json.load(f)
        else:
            history = []

        # Add new entry
        entry["timestamp"] = datetime.now().isoformat()
        history.append(entry)

        # Keep only last 100 entries
        history = history[-100:]

        # Write back
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)

    except Exception as e:
        print(f"  (History save error: {e})")


def load_urls_from_file(filepath: str) -> list:
    """
    Load URLs from a text file (one URL per line).

    Args:
        filepath: Path to the text file

    Returns:
        List of URLs (empty lines and comments filtered)
    """
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()

        urls = []
        for line in lines:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith("#"):
                urls.append(line)

        return urls

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def process_urls(urls: list, copy_to_clip: bool = True, save_history: bool = True) -> list:
    """
    Process a list of URLs to shorten them.

    Args:
        urls: List of URLs to shorten
        copy_to_clip: Whether to copy shortened URLs to clipboard
        save_history: Whether to save to history

    Returns:
        List of result dictionaries
    """
    results = []
    history_file = Path.home() / ".url_shortener_history.json"

    print(f"\nProcessing {len(urls)} URL(s)...")
    print("-" * 50)

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Shortening: {url}")

        result = shorten_url(url)

        if result["success"]:
            print(f"  Original: {result['original']}")
            print(f"  Shortened: {result['shortened']}")

            if copy_to_clip:
                if copy_to_clipboard(result["shortened"]):
                    print("  Copied to clipboard!")

            if save_history:
                save_to_history(result, history_file)
        else:
            print(f"  Error: {result['error']}")

        results.append(result)

    return results


def print_summary(results: list):
    """
    Print a summary of URL shortening results.

    Args:
        results: List of result dictionaries
    """
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"  Total URLs processed: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print("=" * 50)


def main():
    """Main function to run the URL shortener."""
    print("=" * 50)
    print("URL SHORTENER")
    print("Shorten URLs using TinyURL API")
    print("=" * 50)

    # Parse command line arguments
    args = sys.argv[1:]

    # Check for flags
    copy_to_clip = True
    batch_mode = False

    if "--no-copy" in args:
        copy_to_clip = False
        args.remove("--no-copy")

    if "--batch" in args:
        batch_mode = True
        args.remove("--batch")

    # Process based on mode
    if batch_mode or len(args) == 1 and Path(args[0]).exists():
        # Batch mode - read from file
        filepath = args[0] if args else "urls.txt"
        urls = load_urls_from_file(filepath)

        if not urls:
            print("\nNo URLs found. Create a file with one URL per line.")
            print("Example urls.txt:")
            print("  https://example.com/very/long/url/that/needs/shortening")
            print("  https://another-example.com/page")
            return

        results = process_urls(urls, copy_to_clip=copy_to_clip)

    elif len(args) >= 1:
        # Single URL mode
        url = args[0]
        results = process_urls([url], copy_to_clip=copy_to_clip)

    else:
        # Interactive mode
        print("\nEnter URLs to shorten (one at a time)")
        print("Commands:")
        print("  paste - Shorten URL from clipboard")
        print("  batch - Enter batch mode")
        print("  quit  - Exit program")
        print("-" * 40)

        urls_to_process = []

        while True:
            user_input = input("\nURL: ").strip()

            if user_input.lower() == "quit":
                break
            elif user_input.lower() == "batch":
                # Process collected URLs and switch to batch
                if urls_to_process:
                    results = process_urls(urls_to_process, copy_to_clip=copy_to_clip)
                    print_summary(results)
                urls_to_process = []
                print("Enter URLs (one per line, empty line to process):")
                while True:
                    line = input().strip()
                    if not line:
                        break
                    urls_to_process.append(line)
                if urls_to_process:
                    results = process_urls(urls_to_process, copy_to_clip=copy_to_clip)
                    print_summary(results)
                urls_to_process = []
            elif user_input.lower() == "paste":
                try:
                    clipboard_content = clipboard.paste()
                    if clipboard_content:
                        print(f"  Clipboard: {clipboard_content}")
                        urls_to_process.append(clipboard_content)
                        result = shorten_url(clipboard_content)
                        if result["success"]:
                            print(f"  Shortened: {result['shortened']}")
                            if copy_to_clip:
                                copy_to_clipboard(result['shortened'])
                                print("  Copied to clipboard!")
                        else:
                            print(f"  Error: {result['error']}")
                    else:
                        print("  Clipboard is empty")
                except Exception as e:
                    print(f"  Clipboard error: {e}")
            elif user_input:
                urls_to_process.append(user_input)
                result = shorten_url(user_input)
                if result["success"]:
                    print(f"  Shortened: {result['shortened']}")
                    if copy_to_clip:
                        copy_to_clipboard(result['shortened'])
                        print("  Copied to clipboard!")
                else:
                    print(f"  Error: {result['error']}")

        # Process any remaining URLs
        if urls_to_process:
            results = process_urls(urls_to_process, copy_to_clip=copy_to_clip)
            print_summary(results)

        print("\nGoodbye!")
        return

    # Print summary for non-interactive modes
    print_summary(results)


if __name__ == "__main__":
    main()
