#!/usr/bin/env python3
"""
Magic 8-Ball - Virtual Fortune Teller
Ask any yes/no question and receive wisdom from the mystical orb!
"""

import random
import time
import sys
import os

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback colors
    class Fore:
        RED = WHITE = CYAN = MAGENTA = YELLOW = GREEN = BLUE = RESET = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = ''

def print_color(text, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{text}")

def print_shake(text, color=Fore.CYAN):
    frames = [r"\|/", r"/-\\", r"|/|", r"\|-\\"]
    for _ in range(3):
        for frame in frames:
            print_color(f"\r{frame} {text} ", color, Style.BRIGHT)
            time.sleep(0.1)
    print()

def draw_8ball(shaking=False):
    if shaking:
        frames = [
            """
      .-------.
     /   8   /|
    /_______/ |
    |       | |
    |  ???  | /
    |_______|/
            """,
            """
      ,-------,
     ,/   8   ,
    /_______/  ,
    |       |  ,
    |  ???  | ,
    |_______|/,
            """,
        ]
        for frame in frames * 2:
            print_color(frame, Fore.LIGHTBLACK_EX, Style.DIM)
            time.sleep(0.15)
            sys.stdout.write("\033[5A")

    print_color("""
         .--------.
        /|        |\\
       / |        | \\
      /  |        |  \\
     |   |   8    |   |
     |   |        |   |
     |   |   ?    |   |
     |   |        |   |
     |   |________|   |
     |  /          \\  |
     | /            \\ |
     |/              \\|
     \\______________/
    """, Fore.BLUE, Style.BRIGHT)

def display_intro():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     ███████╗ ██████╗ ██████╗  ██████╗  ██████╗ ████████╗  ║
    ║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔═══██╗╚══██╔══╝  ║
    ║     █████╗  ██║   ██║██████╔╝██║  ███╗██║   ██║   ██║     ║
    ║     ██╔══╝  ██║   ██║██╔══██╗██║   ██║██║   ██║   ██║     ║
    ║     ██║     ╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝   ██║     ║
    ║     ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝     ║
    ║                                                           ║
    ║              🔮  The Mystical Oracle  🔮                  ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.CYAN, Style.BRIGHT)
    print()
    print_color("    Ask the oracle any yes/no question and receive", Fore.YELLOW)
    print_color("    wisdom from beyond the veil of time...", Fore.YELLOW)
    print()

def get_response():
    """Return a random Magic 8-Ball response"""
    responses = [
        # Positive
        ("It is certain", Fore.GREEN),
        ("It is decidedly so", Fore.GREEN),
        ("Without a doubt", Fore.GREEN),
        ("Yes, definitely", Fore.GREEN),
        ("You may rely on it", Fore.GREEN),
        ("As I see it, yes", Fore.GREEN),
        ("Most likely", Fore.GREEN),
        ("Outlook good", Fore.GREEN),
        ("Yes", Fore.GREEN),
        ("Signs point to yes", Fore.GREEN),
        # Neutral
        ("Reply hazy, try again", Fore.YELLOW),
        ("Ask again later", Fore.YELLOW),
        ("Better not tell you now", Fore.YELLOW),
        ("Cannot predict now", Fore.YELLOW),
        ("Concentrate and ask again", Fore.YELLOW),
        # Negative
        ("Don't count on it", Fore.RED),
        ("My reply is no", Fore.RED),
        ("My sources say no", Fore.RED),
        ("Outlook not so good", Fore.RED),
        ("Very doubtful", Fore.RED),
        ("Most assuredly not", Fore.RED),
        ("Absolutely not", Fore.RED),
        # Mystical
        ("The spirits whisper... yes", Fore.MAGENTA),
        ("The cosmic energy says no", Fore.MAGENTA),
        ("I sense great uncertainty in the cosmos", Fore.MAGENTA),
        ("The answer lies within you", Fore.CYAN),
        ("The void gazes back... and grins", Fore.MAGENTA),
    ]
    return random.choice(responses)

def display_response(text, color):
    print()
    print_color("    ┌" + "─" * 50 + "┐", Fore.CYAN)
    print_color("    │" + " " * 50 + "│", Fore.CYAN)

    # Center the text
    padding = (50 - len(text)) // 2
    print_color(f"    │{' ' * padding}{text}{' ' * (50 - len(text) - padding)}│", color, Style.BRIGHT)

    print_color("    │" + " " * 50 + "│", Fore.CYAN)
    print_color("    └" + "─" * 50 + "┘", Fore.CYAN)
    print()

def play_shake_animation():
    """Animate the 8-ball shaking"""
    print_color("\n    ✨ Concentrate on your question... ✨\n", Fore.YELLOW)
    time.sleep(1)

    frames = [
        r"  [ shaking  ]",
        r"  [ SHAKING! ]",
        r"  [ SHAKE!   ]",
        r"  [ SHAKING  ]",
        r"  [  SHAKE   ]",
        r"  [ SHAKING! ]",
    ]

    for _ in range(3):
        for frame in frames:
            print_color(f"\r    {frame}", Fore.CYAN, Style.BRIGHT)
            time.sleep(0.15)
        print()

    print_color("\n    💫 The spirits are channeling... 💫", Fore.MAGENTA)
    time.sleep(0.5)

def main():
    display_intro()

    while True:
        print_color("    ╔════════════════════════════════════════════════════╗", Fore.WHITE)
        print_color("    ║  Type your question below (or 'quit' to exit):    ║", Fore.WHITE)
        print_color("    ╚════════════════════════════════════════════════════╝", Fore.WHITE)
        print()
        print_color("    > ", Fore.GREEN, Style.BRIGHT)

        try:
            question = input()
        except EOFError:
            break

        if question.lower().strip() in ['quit', 'exit', 'q', 'bye']:
            print_color("\n    🌟 The oracle bids you farewell! 🌟\n", Fore.CYAN, Style.BRIGHT)
            print_color("    May your path be illuminated by starlight...\n", Fore.YELLOW)
            break

        if not question.strip():
            print_color("\n    ⚠️  The oracle requires a question! ⚠️\n", Fore.RED)
            continue

        if len(question) > 200:
            print_color("\n    ⚠️  The oracle's patience is limited! Keep it under 200 chars. ⚠️\n", Fore.RED)
            continue

        # Clear and show shake animation
        os.system('cls' if os.name == 'nt' else 'clear')

        print_color("""

    ╔═══════════════════════════════════════════════════════════╗
    ║                    🔮 THE ORACLE SPEAKS 🔮                ║
    ╚═══════════════════════════════════════════════════════════╝

        """, Fore.MAGENTA, Style.BRIGHT)

        play_shake_animation()

        response, color = get_response()

        # Draw the 8-ball with answer
        print_color("""
         .--------.
        /|        |\\
       / |        | \\
      /  |        |  \\
     |   |   8    |   |
     |   |        |   |
        """, Fore.BLUE, Style.BRIGHT)

        display_response(response, color)

        # Fun extras
        if "certain" in response.lower() or "definitely" in response.lower() or "yes" in response.lower():
            print_color("    ✨ The stars align in your favor! ✨", Fore.GREEN)
        elif "no" in response.lower() or "doubtful" in response.lower() or "not" in response.lower():
            print_color("    🌙 Perhaps the stars have other plans... 🌙", Fore.RED)
        elif "hazy" in response.lower() or "later" in response.lower() or "uncertain" in response.lower():
            print_color("    🌫️  The mist of fate obscures the answer... 🌫️", Fore.YELLOW)
        else:
            print_color("    ⭐ The cosmic wheel turns in mysterious ways... ⭐", Fore.CYAN)

        print()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n\n    🌟 The oracle respects your time! Farewell! 🌟\n", Fore.CYAN)
        sys.exit(0)
