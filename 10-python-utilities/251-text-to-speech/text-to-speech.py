"""
Text to Speech Converter
Convert text to speech using gTTS (Google Text-to-Speech) and save as MP3.

Usage:
    python text-to-speech.py [text] [--output FILE] [--lang LANG] [--slow]
    python text-to-speech.py --file TEXTFILE [--output FILE]
    python text-to-speech.py --interactive
"""

import os
import sys
import clipboard
from pathlib import Path
from datetime import datetime

# Try to import gTTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


# Available languages (partial list of supported languages)
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh-CN": "Chinese (Simplified)",
    "hi": "Hindi",
    "ar": "Arabic",
    "nl": "Dutch",
    "pl": "Polish",
    "tr": "Turkish",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
}


def get_default_output_dir() -> Path:
    """
    Get the default output directory for audio files.

    Returns:
        Path object for the output directory
    """
    output_dir = Path.home() / "Documents" / "Audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_filename(prefix: str = "tts") -> str:
    """
    Generate a timestamped filename for the audio file.

    Args:
        prefix: Filename prefix

    Returns:
        Formatted filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.mp3"


def text_to_speech(
    text: str,
    output_file: str = None,
    language: str = "en",
    slow: bool = False
) -> str:
    """
    Convert text to speech and save as MP3.

    Args:
        text: Text to convert to speech
        output_file: Output file path (optional)
        language: Language code (default: English)
        slow: Use slower speech rate

    Returns:
        Path to the created audio file

    Raises:
        ImportError: If gTTS is not installed
        ValueError: If text is empty
        Exception: On TTS generation errors
    """
    if not GTTS_AVAILABLE:
        raise ImportError(
            "gTTS is not installed. Install it with:\n"
            "pip install gtts"
        )

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    # Generate output path if not provided
    if output_file is None:
        output_dir = get_default_output_dir()
        output_file = str(output_dir / generate_filename())
    else:
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # Validate language
    if language not in LANGUAGES:
        print(f"Warning: Language '{language}' may not be supported")

    try:
        print(f"\nConverting text to speech...")
        print(f"  Language: {LANGUAGES.get(language, language)}")
        print(f"  Speed: {'Slow' if slow else 'Normal'}")
        print(f"  Characters: {len(text)}")
        print("-" * 40)

        # Create TTS object and save
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(output_file)

        # Get file size
        file_size = Path(output_file).stat().st_size / 1024  # KB

        print(f"\nAudio file created successfully!")
        print(f"  File: {Path(output_file).name}")
        print(f"  Location: {output_file}")
        print(f"  Size: {file_size:.1f} KB")

        return output_file

    except Exception as e:
        raise Exception(f"TTS generation failed: {str(e)}")


def read_text_from_file(filepath: str) -> str:
    """
    Read text content from a file.

    Args:
        filepath: Path to the text file

    Returns:
        File content as string
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(filepath, "r", encoding="latin-1") as f:
            return f.read()


def list_languages():
    """Display list of available languages."""
    print("\nAvailable Languages:")
    print("-" * 30)
    for code, name in sorted(LANGUAGES.items()):
        print(f"  {code:8} - {name}")
    print()


def interactive_mode():
    """Run TTS in interactive mode."""
    print("\nInteractive Text-to-Speech Mode")
    print("-" * 40)
    print("Commands:")
    print("  text <message> - Convert text to speech")
    print("  paste          - Convert clipboard content")
    print("  file <path>    - Convert text from file")
    print("  lang           - List available languages")
    print("  quit           - Exit program")
    print()

    output_dir = get_default_output_dir()
    current_lang = "en"
    current_slow = False

    print(f"Current settings: lang={current_lang}, slow={current_slow}")
    print(f"Output directory: {output_dir}")

    while True:
        try:
            user_input = input("\n> ").strip()

            if not user_input:
                continue

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            argument = parts[1] if len(parts) > 1 else ""

            if command == "quit":
                print("Goodbye!")
                break

            elif command == "text":
                if not argument:
                    print("Usage: text <message>")
                else:
                    try:
                        generate_filename(prefix="tts")
                        output_file = str(output_dir / generate_filename())
                        text_to_speech(
                            argument,
                            output_file=output_file,
                            language=current_lang,
                            slow=current_slow
                        )
                    except Exception as e:
                        print(f"Error: {e}")

            elif command == "paste":
                text = clipboard.paste()
                if not text.strip():
                    print("Clipboard is empty")
                else:
                    print(f"Clipboard content ({len(text)} chars):")
                    print(f"  {text[:100]}{'...' if len(text) > 100 else ''}")
                    try:
                        output_file = str(output_dir / generate_filename())
                        text_to_speech(
                            text,
                            output_file=output_file,
                            language=current_lang,
                            slow=current_slow
                        )
                    except Exception as e:
                        print(f"Error: {e}")

            elif command == "file":
                if not argument:
                    print("Usage: file <path>")
                else:
                    try:
                        text = read_text_from_file(argument)
                        print(f"Read {len(text)} characters from file")
                        output_file = str(output_dir / generate_filename())
                        text_to_speech(
                            text,
                            output_file=output_file,
                            language=current_lang,
                            slow=current_slow
                        )
                    except FileNotFoundError:
                        print(f"File not found: {argument}")
                    except Exception as e:
                        print(f"Error: {e}")

            elif command == "lang":
                list_languages()
                new_lang = input("Enter language code (or press Enter to cancel): ").strip()
                if new_lang in LANGUAGES:
                    current_lang = new_lang
                    print(f"Language set to: {LANGUAGES[new_lang]}")
                elif new_lang:
                    print(f"Unknown language code: {new_lang}")

            elif command == "slow":
                current_slow = not current_slow
                print(f"Slow mode: {'On' if current_slow else 'Off'}")

            elif command == "dir":
                if argument:
                    output_dir = Path(argument)
                    output_dir.mkdir(parents=True, exist_ok=True)
                    print(f"Output directory: {output_dir}")
                else:
                    print(f"Output directory: {output_dir}")

            else:
                # Treat as direct text input
                try:
                    output_file = str(output_dir / generate_filename())
                    text_to_speech(
                        user_input,
                        output_file=output_file,
                        language=current_lang,
                        slow=current_slow
                    )
                except Exception as e:
                    print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


def main():
    """Main function to run the TTS converter."""
    print("=" * 50)
    print("TEXT TO SPEECH CONVERTER")
    print("Convert text to audio using gTTS")
    print("=" * 50)

    # Check for gTTS
    if not GTTS_AVAILABLE:
        print("\nError: gTTS library is not installed.")
        print("\nInstall it with:")
        print("  pip install gtts")
        print("\nOr run in interactive mode to see installation instructions.")
        response = input("\nInstall gTTS now? [y/N]: ").strip().lower()
        if response == "y":
            print("\nInstalling gTTS...")
            os.system("pip install gtts")
            print("\nPlease run the script again.")
        return

    # Parse command line arguments
    args = sys.argv[1:]

    if not args:
        # No arguments - interactive mode
        interactive_mode()
        return

    # Parse arguments
    text = None
    text_file = None
    output_file = None
    language = "en"
    slow = False

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--interactive" or arg == "-i":
            interactive_mode()
            return

        elif arg == "--file" or arg == "-f":
            if i + 1 < len(args):
                text_file = args[i + 1]
                i += 2
            else:
                print("Error: --file requires a path")
                return

        elif arg == "--output" or arg == "-o":
            if i + 1 < len(args):
                output_file = args[i + 1]
                i += 2
            else:
                print("Error: --output requires a file path")
                return

        elif arg == "--lang" or arg == "-l":
            if i + 1 < len(args):
                language = args[i + 1]
                i += 2
            else:
                print("Error: --lang requires a language code")
                return

        elif arg == "--slow":
            slow = True
            i += 1

        elif arg == "--help" or arg == "-h":
            print("\nUsage: python text-to-speech.py [options]")
            print("\nOptions:")
            print("  --interactive, -i    Interactive mode")
            print("  --file, -f <path>    Read text from file")
            print("  --output, -o <file>  Output file path")
            print("  --lang, -l <code>    Language code (default: en)")
            print("  --slow               Slower speech rate")
            print("  --help, -h           Show this help")
            print("\nExamples:")
            print("  python text-to-speech.py \"Hello world\"")
            print("  python text-to-speech.py --file readme.txt --lang es")
            print("  python text-to-speech.py --interactive")
            return

        else:
            # Treat as text
            text = arg
            i += 1

    # Get text to convert
    if text_file:
        print(f"Reading text from file: {text_file}")
        text = read_text_from_file(text_file)
    elif text:
        text = text
    else:
        print("Error: No text provided")
        print("Use --help for usage information")
        return

    # Generate speech
    try:
        result = text_to_speech(
            text=text,
            output_file=output_file,
            language=language,
            slow=slow
        )
        print(f"\nFile saved: {result}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
