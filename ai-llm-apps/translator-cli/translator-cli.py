#!/usr/bin/env python3
"""
Translator CLI - Command-line translator using Google Translate.
Translate text between languages with ease.
Usage: python translator-cli.py [text] [options]
"""

import sys
import argparse
from typing import Optional, List, Dict

# Try to import googletrans, fall back to alternative if not available
try:
    from googletrans import Translator, LANGUAGES
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False
    LANGUAGES = {
        'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic',
        'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian',
        'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan',
        'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese', 'zh-tw': 'chinese (traditional)',
        'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish',
        'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian',
        'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian',
        'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek',
        'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian',
        'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian',
        'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish',
        'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada',
        'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)',
        'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian',
        'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy',
        'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori',
        'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar', 'ne': 'nepali',
        'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish',
        'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian',
        'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho',
        'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak',
        'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese',
        'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil',
        'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian',
        'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh',
        'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'
    }


def list_languages():
    """List all supported languages."""
    print("\nSupported Languages:")
    print("-" * 40)

    # Sort by language code
    codes = sorted(LANGUAGES.keys())
    for i, code in enumerate(codes, 1):
        name = LANGUAGES[code]
        # Two columns
        if i % 2 == 1:
            print(f"  {code:10} {name:<20}", end='')
        else:
            print(f"  {code:10} {name:<20}")

    if len(codes) % 2 == 1:
        print()  # Newline for odd count

    print("-" * 40)
    print(f"Total: {len(codes)} languages\n")


def detect_language(text: str) -> Optional[Dict]:
    """Detect the language of the given text."""
    if not GOOGLETRANS_AVAILABLE:
        print("Error: googletrans library not installed.")
        print("Install with: pip install googletrans==4.0.0-rc1")
        return None

    try:
        translator = Translator()
        detection = translator.detect(text)
        return {
            'lang': detection.lang,
            'confidence': detection.confidence,
            'name': LANGUAGES.get(detection.lang, 'Unknown')
        }
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None


def translate_text(text: str, dest: str, src: str = 'auto') -> Optional[str]:
    """Translate text from source to destination language."""
    if not GOOGLETRANS_AVAILABLE:
        print("Error: googletrans library not installed.")
        print("Install with: pip install googletrans==4.0.0-rc1")
        return None

    try:
        translator = Translator()
        result = translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception as e:
        print(f"Error translating: {e}")
        return None


def get_translation_result(text: str, dest: str, src: str = 'auto') -> Optional[Dict]:
    """Get detailed translation result."""
    if not GOOGLETRANS_AVAILABLE:
        print("Error: googletrans library not installed.")
        print("Install with: pip install googletrans==4.0.0-rc1")
        return None

    try:
        translator = Translator()
        result = translator.translate(text, src=src, dest=dest)
        return {
            'source_lang': result.src,
            'dest_lang': result.dest,
            'original': result.origin,
            'translated': result.text,
            'pronunciation': getattr(result, 'pronunciation', None)
        }
    except Exception as e:
        print(f"Error translating: {e}")
        return None


def print_result(result: Dict, verbose: bool = False):
    """Print translation result."""
    if verbose:
        print(f"\nSource Language : {result['source_lang'].upper()} ({LANGUAGES.get(result['source_lang'], 'Unknown')})")
        print(f"Target Language : {result['dest_lang'].upper()} ({LANGUAGES.get(result['dest_lang'], 'Unknown')})")
        print(f"\nOriginal Text   :")
        print(f"  {result['original']}")
        print(f"\nTranslated Text :")
        print(f"  {result['translated']}")
        if result.get('pronunciation'):
            print(f"\nPronunciation   : {result['pronunciation']}")
    else:
        print(result['translated'])


def main():
    parser = argparse.ArgumentParser(
        description="Translator CLI - Translate text between languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Hello world" -t es
  %(prog)s "Bonjour" -t en --verbose
  %(prog)s "Hola" -s es -t ja
  %(prog)s --detect "This is a test"
  %(prog)s --list-languages
  %(prog)s --interactive
        """
    )

    # Input options
    parser.add_argument('text', nargs='?', help='Text to translate')
    parser.add_argument('-f', '--file', help='Read text from file')

    # Language options
    parser.add_argument('-s', '--source', default='auto', help='Source language (default: auto-detect)')
    parser.add_argument('-t', '--to', '--target', dest='target', required=False,
                        help='Target language code (e.g., es, fr, ja)')
    parser.add_argument('--list-languages', action='store_true', help='List all supported languages')
    parser.add_argument('--detect', metavar='TEXT', help='Detect language of text')

    # Output options
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output with details')
    parser.add_argument('-j', '--json', action='store_true', help='Output as JSON')

    # Interactive mode
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive translation mode')

    args = parser.parse_args()

    # List languages
    if args.list_languages:
        list_languages()
        return 0

    # Detect language
    if args.detect:
        result = detect_language(args.detect)
        if result:
            print(f"\nLanguage: {result['lang'].upper()} ({result['name']})")
            print(f"Confidence: {result['confidence'] * 100:.1f}%")
        return 0

    # Check if googletrans is available
    if not GOOGLETRANS_AVAILABLE:
        print("Error: googletrans library is not installed.")
        print("\nPlease install it with:")
        print("  pip install googletrans==4.0.0-rc1")
        print("\nOr upgrade to a newer version:")
        print("  pip install googletranslation3")
        return 1

    # Interactive mode
    if args.interactive:
        print("\nInteractive Translation Mode")
        print("=" * 40)
        print("Commands:")
        print("  :lang <code> - Set target language")
        print("  :source <code> - Set source language")
        print("  :detect - Detect source language")
        print("  :list - List all languages")
        print("  :quit - Exit")
        print("=" * 40)

        target_lang = 'es'  # Default
        source_lang = 'auto'

        while True:
            try:
                text = input(f"\n[{source_lang} -> {target_lang}]> ").strip()

                if not text:
                    continue

                if text == ':quit':
                    print("Goodbye!")
                    break

                if text == ':list':
                    list_languages()
                    continue

                if text.startswith(':lang '):
                    target_lang = text.split()[1]
                    print(f"Target language set to: {target_lang} ({LANGUAGES.get(target_lang, 'Unknown')})")
                    continue

                if text.startswith(':source '):
                    source_lang = text.split()[1]
                    print(f"Source language set to: {source_lang} ({LANGUAGES.get(source_lang, 'Unknown')})")
                    continue

                if text == ':detect':
                    detection = detect_language(text)
                    if detection:
                        print(f"Detected: {detection['lang'].upper()} ({detection['name']})")
                    continue

                result = get_translation_result(text, target_lang, source_lang)
                if result:
                    print_result(result, verbose=True)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                break

        return 0

    # Normal translation mode
    if args.target is None:
        parser.print_help()
        print("\nNote: Use -t/--to to specify target language")
        print("      Use --list-languages to see all available languages")
        return 1

    # Get text to translate
    text = None
    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            return 1
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1

    if not text:
        print("Error: No text to translate. Provide text as argument or use -f/--file")
        return 1

    # Perform translation
    result = get_translation_result(text, args.target, args.source)

    if result:
        if args.json:
            import json
            output = {
                'source_lang': result['source_lang'],
                'dest_lang': result['dest_lang'],
                'original': result['original'],
                'translated': result['translated'],
            }
            if result.get('pronunciation'):
                output['pronunciation'] = result['pronunciation']
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print_result(result, verbose=args.verbose)
    else:
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
