#!/usr/bin/env python3
"""
Joke Teller - Random Jokes & Facts
Get a random joke or fun fact delivered with style!
"""

import random
import sys
import os
import urllib.request
import json

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    class Fore:
        RED = WHITE = CYAN = MAGENTA = YELLOW = GREEN = BLUE = RESET = LIGHTBLACK_EX = LIGHTGREEN_EX = LIGHTYELLOW_EX = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = NORMAL = ''

def print_color(text, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{text}")

def display_intro():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗   ║
    ║   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║   ║
    ║   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║   ║
    ║   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║   ║
    ║   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝   ║
    ║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝    ║
    ║                                                           ║
    ║              😂 Random Jokes & Fun Facts 😂               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.YELLOW, Style.BRIGHT)
    print()
    print_color("    Get ready to laugh with jokes and learn fun facts!", Fore.CYAN)
    print()

def get_joke_from_api():
    """Fetch a joke from the Official Joke API"""
    try:
        url = "https://official-joke-api.appspot.com/jokes/random"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                'type': 'two-part',
                'setup': data['setup'],
                'punchline': data['punchline']
            }
    except Exception as e:
        return None

def get_programming_joke():
    """Fetch a programming joke from JokeAPI"""
    try:
        url = "https://v2.jokeapi.dev/joke/Programming?type=twopart"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data.get('type') == 'twopart':
                return {
                    'type': 'two-part',
                    'setup': data['setup'],
                    'punchline': data['punchline']
                }
    except Exception:
        pass
    return None

def get_fact():
    """Get a random fun fact"""
    facts = [
        ("Did you know?", "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still edible! 🍯"),
        ("Fun Fact:", "Octopuses have three hearts and blue blood! 🐙"),
        ("Mind-blowing:", "A day on Venus is longer than a year on Venus! ☀️"),
        ("Surprising:", "Bananas are berries, but strawberries aren't! 🍌🍓"),
        ("Tech Trivia:", "The first computer virus was created in 1983 and was called the 'Elk Cloner'! 💻"),
        ("Science:", "Water can boil and freeze at the same time under the right pressure (triple point)! 💧"),
        ("History:", "Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid! 🏛️"),
        ("Nature:", "Cows have best friends and get stressed when separated! 🐄"),
        ("Space:", "There are more trees on Earth than stars in the Milky Way! 🌳⭐"),
        ("Random:", "The shortest war in history lasted 38-45 minutes between Britain and Zanzibar in 1896! ⚔️"),
        ("Food:", "Peanuts aren't nuts - they're legumes! 🥜"),
        ("Animal:", "Dolphins have names for each other! 🐬"),
        ("Tech:", "The first 1GB hard drive weighed about 550 pounds! 💾"),
        ("Ocean:", "We have explored less than 5% of the ocean! 🌊"),
        ("Sleep:", "Humans are the only mammals that voluntarily delay sleep! 😴"),
        ("Brain:", "Your brain uses about 10% of its capacity... wait, that's a myth! Actually, you use all of it! 🧠"),
        ("Language:", "'Go' is the most complex word in the English language! 📚"),
        ("Solar:", "The Sun's core is about 27 million degrees Fahrenheit! ☀️"),
        ("Music:", "Happy Birthday is the most recognized song in the world! 🎂"),
        ("Internet:", "The first emoji was created in 1999 in Japan! 📱"),
        ("Coffee:", "Finland drinks the most coffee per capita! ☕"),
        ("Bees:", "A bee can fly up to 15 miles per hour and visit 50-100 flowers per day! 🐝"),
        ("Time:", "There's no autumn in the Galactic Calendar - just a very dramatic Tuesday! 🌌"),
        ("Pineapple:", "Pineapples take about 2 years to grow! 🍍"),
        ("Sharks:", "Sharks existed before trees! 🦈🌳"),
    ]
    return random.choice(facts)

def display_joke(joke):
    """Display a joke with formatting"""
    print()
    print_color("    ┌" + "─" * 56 + "┐", Fore.CYAN)
    print_color("    │" + " " * 56 + "│", Fore.CYAN)
    print_color("    │  😂 JOKE TIME! 😂                               │", Fore.YELLOW, Style.BRIGHT)
    print_color("    │" + " " * 56 + "│", Fore.CYAN)
    print_color("    └" + "─" * 56 + "┘", Fore.CYAN)
    print()

    # Type out the setup
    print_color("    📢 ", Fore.GREEN, Style.BRIGHT)
    setup = joke['setup']
    for i, char in enumerate(setup):
        print(char, end='', flush=True)
        if i % 5 == 0:
            time.sleep(0.01)
    print()
    print()

    # Dramatic pause
    print_color("    ⏳ Prepare for impact...", Fore.YELLOW)
    for i in range(3):
        print_color(f"    💫", Fore.MAGENTA, Style.BRIGHT)
        time.sleep(0.5)

    print()
    print_color("    😆 ", Fore.RED, Style.BRIGHT)
    punchline = joke['punchline']
    for i, char in enumerate(punchline):
        print(char, end='', flush=True)
        if i % 5 == 0:
            time.sleep(0.01)
    print()
    print()
    print_color("    🤣😂🤣", Fore.YELLOW, Style.BRIGHT)
    print()

def display_fact(category, fact):
    """Display a fun fact with formatting"""
    print()
    print_color("    ┌" + "─" * 56 + "┐", Fore.CYAN)
    print_color("    │" + " " * 56 + "│", Fore.CYAN)
    print_color("    │  💡 DID YOU KNOW? 💡                            │", Fore.CYAN, Style.BRIGHT)
    print_color("    │" + " " * 56 + "│", Fore.CYAN)
    print_color("    └" + "─" * 56 + "┘", Fore.CYAN)
    print()
    print_color(f"    📚 {category}", Fore.YELLOW, Style.BRIGHT)
    print()
    print_color(f"    {fact}", Fore.GREEN)
    print()

def display_menu():
    print_color("""
    ┌─────────────────────────────────────────────────────────┐
    │  What would you like?                                   │
    ├─────────────────────────────────────────────────────────┤
    │  [1] 🎭 Random Joke                                     │
    │  [2] 💻 Programming Joke                                │
    │  [3] 💡 Random Fun Fact                                 │
    │  [4] 🎲 Mix it up!                                      │
    │  [5] 🚪 Quit                                             │
    └─────────────────────────────────────────────────────────┘
    """, Fore.WHITE)
    print()
    print_color("    Enter your choice: ", Fore.GREEN, Style.BRIGHT)

def main():
    import time

    display_intro()
    joke_count = 0
    fact_count = 0

    while True:
        display_menu()

        try:
            choice = input().strip()
        except EOFError:
            break

        if choice == '5' or choice.lower() in ['quit', 'exit', 'q', 'bye']:
            print_color("\n    😢 No more jokes for you today!", Fore.YELLOW)
            print_color(f"    You laughed {joke_count} times and learned {fact_count} facts!", Fore.CYAN)
            print_color("    See you next time! 👋\n", Fore.GREEN, Style.BRIGHT)
            break

        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == '1':
            joke_count += 1
            joke = get_joke_from_api()
            if joke:
                display_joke(joke)
            else:
                # Fallback jokes
                fallback_jokes = [
                    {'setup': "Why don't scientists trust atoms?", 'punchline': "Because they make up everything!"},
                    {'setup': "Why did the scarecrow win an award?", 'punchline': "He was outstanding in his field!"},
                    {'setup': "What do you call a fake noodle?", 'punchline': "An impasta!"},
                    {'setup': "Why don't eggs tell jokes?", 'punchline': "They'd crack each other up!"},
                    {'setup': "What do you call a bear with no teeth?", 'punchline': "A gummy bear!"},
                ]
                display_joke(random.choice(fallback_jokes))

        elif choice == '2':
            joke_count += 1
            joke = get_programming_joke()
            if joke:
                display_joke(joke)
            else:
                # Fallback programming jokes
                fallback_jokes = [
                    {'setup': "Why do Java developers wear glasses?", 'punchline': "Because they can't C#!"},
                    {'setup': "How many programmers does it take to change a light bulb?", 'punchline': "None - that's a hardware problem!"},
                    {'setup': "Why was the JavaScript developer sad?", 'punchline': "Because he didn't Node how to Express himself!"},
                    {'setup': "What's a programmer's favorite hangout place?", 'punchline': "Foo Bar!"},
                    {'setup': "Why do Python programmers prefer snakes?", 'punchline': "Because they slither gracefully!"},
                ]
                display_joke(random.choice(fallback_jokes))

        elif choice == '3':
            fact_count += 1
            category, fact = get_fact()
            display_fact(category, fact)

        elif choice == '4':
            # Mix it up randomly
            option = random.randint(1, 3)
            if option == 1:
                joke_count += 1
                joke = get_joke_from_api()
                if joke:
                    display_joke(joke)
                else:
                    display_joke(random.choice([
                        {'setup': "Why don't scientists trust atoms?", 'punchline': "Because they make up everything!"},
                        {'setup': "What's a dog's favorite programming language?", 'punchline': "Bark!"},
                    ]))
            elif option == 2:
                fact_count += 1
                category, fact = get_fact()
                display_fact(category, fact)
            else:
                joke_count += 1
                joke = get_programming_joke()
                if joke:
                    display_joke(joke)
                else:
                    display_joke({'setup': "Why do programmers prefer dark mode?", 'punchline': "Because light attracts bugs!"})
        else:
            print_color("\n    ⚠️  Invalid choice! Please enter 1-5. ⚠️\n", Fore.RED)

        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n\n    👋 Interrupted! See you next time!\n", Fore.CYAN)
        sys.exit(0)
