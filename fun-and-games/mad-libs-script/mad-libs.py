#!/usr/bin/env python3
"""
Mad Libs Generator - Classic Word Game
Fill in the blanks with hilarious words and create funny stories!
"""

import random
import sys
import os
import time

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    class Fore:
        RED = WHITE = CYAN = MAGENTA = YELLOW = GREEN = BLUE = RESET = LIGHTBLACK_EX = LIGHTRED_EX = LIGHTGREEN_EX = LIGHTYELLOW_EX = LIGHTBLUE_EX = LIGHTMAGENTA_EX = ''
    class Style:
        BRIGHT = RESET_ALL = DIM = NORMAL = ''

def print_color(text, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{text}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_intro():
    clear_screen()
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║    ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ███████╗     ║
    ║    ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██╔════╝     ║
    ║    ███████╗███████║███████║██████╔╝██║   ██║███████╗     ║
    ║    ╚════██║██╔══██║██╔══██║██╔══██╗██║   ██║╚════██║     ║
    ║    ███████║██║  ██║██║  ██║██║  ██║╚██████╔╝███████║     ║
    ║    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ║
    ║                                                           ║
    ║                    📖 MAD LIBS! 📖                        ║
    ║                                                           ║
    ║           The Classic Word-Filling Fun Game!              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.MAGENTA, Style.BRIGHT)
    print()
    print_color("    Fill in the blanks with words and create hilarious stories!", Fore.CYAN)
    print_color("    Perfect for hours of giggles and creative writing! 🎭\n", Fore.CYAN)
    print()

STORY_TEMPLATES = {
    "space_adventure": {
        "title": "🚀 Space Adventure",
        "blanks": [
            ("verb ending in -ing", "verb"),
            ("adjective", "adjective"),
            ("plural noun", "plural_noun"),
            ("animal", "animal"),
            ("food", "food"),
            ("planet name", "noun"),
            ("famous person", "name"),
            ("adjective", "adjective"),
            ("body part", "body_part"),
            ("number", "number"),
            ("verb", "verb"),
            ("comic book character", "name"),
            ("exclamation", "exclamation"),
        ],
        "template": """
    ╔═══════════════════════════════════════════════════════════╗
    ║              🚀 A SPACE ADVENTURE STORY 🚀                ║
    ╚═══════════════════════════════════════════════════════════╝

    Today I went to the planet Mars in my {adjective} rocket ship!
    My mission was to {verb ending in -ing} the alien {plural noun}.

    When I arrived, I saw a {adjective} {animal} eating a giant {food}.
    It looked at me with its {body part} and said:
    "Welcome to {planet name}, Earthling!"

    Suddenly, {famous person} appeared riding a {adjective} unicorn!
    "Quick! We have exactly {number} minutes before the {animal} wakes up!"
    we must {verb} the secret treasure before {comic book character} finds it!

    "{exclamation}!" I shouted as we zoomed back to Earth.
    What a {adjective} day in space!
        """
    },

    "dragon_tale": {
        "title": "🐉 The Dragon's Tale",
        "blanks": [
            ("adjective", "adjective"),
            ("color", "adjective"),
            ("animal", "animal"),
            ("plural noun", "plural_noun"),
            ("verb", "verb"),
            ("food", "food"),
            ("place", "place"),
            ("famous person", "name"),
            ("adjective", "adjective"),
            ("magical creature", "noun"),
            ("verb ending in -ing", "verb"),
            ("number", "number"),
            ("exclamation", "exclamation"),
        ],
        "template": """
    ╔═══════════════════════════════════════════════════════════╗
    ║                🐉 THE DRAGON'S TALE 🐉                    ║
    ╚═══════════════════════════════════════════════════════════╝

    Once upon a time, in a {adjective} kingdom far, far away,
    there lived a {color} dragon who loved to eat {plural noun}.

    One day, the dragon decided to {verb} all the {food} in the kingdom!
    The king was so worried that he hired {famous person} to help.

    They traveled to the mysterious {place} where the dragon lived.
    "Hello, {adjective} dragon!" said {famous person}.

    But the dragon wasn't scary at all! It was actually a friendly
    {magical creature} who loved {verb ending in -ing}!

    They became best friends and had {number} adventures together.
    "{exclamation}!" they shouted as they flew into the sunset.

    The end! 🐲✨
        """
    },

    "superhero": {
        "title": "🦸 My Superhero Life",
        "blanks": [
            ("adjective", "adjective"),
            ("superpower", "noun"),
            ("animal", "animal"),
            ("color", "adjective"),
            ("verb ending in -ing", "verb"),
            ("villain name", "name"),
            ("place", "place"),
            ("food", "food"),
            ("famous person", "name"),
            ("adjective", "adjective"),
            ("object", "noun"),
            ("exclamation", "exclamation"),
            ("number", "number"),
        ],
        "template": """
    ╔═══════════════════════════════════════════════════════════╗
    ║               🦸 MY SUPERHERO LIFE 🦸                      ║
    ╚═══════════════════════════════════════════════════════════╝

    My name is Captain {animal} and I have the power of {superpower}!
    My cape is {color} and I wear it while I'm {verb ending in -ing}.

    My greatest enemy is the evil {villain name}, who plans to
    destroy all the {food} in {place}!

    I knew I had to stop them, so I called my sidekick
    {famous person} for help. Together we are {adjective} and mighty!

    Using my magical {object}, I defeated {villain name} and saved the day!
    "{exclamation}!" everyone cheered as I flew away.

    I've saved the world {number} times now, and I'm just getting started!

    To be continued... 🦸‍♂️💪
        """
    },

    "cooking_disaster": {
        "title": "🍳 The Great Cooking Disaster",
        "blanks": [
            ("food", "food"),
            ("kitchen tool", "noun"),
            ("adjective", "adjective"),
            ("animal", "animal"),
            ("verb past tense", "verb"),
            ("place", "place"),
            ("famous person", "name"),
            ("liquid", "noun"),
            ("verb", "verb"),
            ("adjective", "adjective"),
            ("exclamation", "exclamation"),
            ("number", "number"),
        ],
        "template": """
    ╔═══════════════════════════════════════════════════════════╗
    ║            🍳 THE GREAT COOKING DISASTER 🍳                ║
    ╚═══════════════════════════════════════════════════════════╝

    Today I decided to cook the perfect {food} using my new {kitchen tool}!
    Everything was going {adjective} until the {animal} walked into the kitchen.

    Suddenly, the {animal} {verb past tense} the entire pot of ingredients!
    I ran to the {place} and called for {famous person} to help.

    "Quick, throw the {liquid}!" they shouted.
    I {verb} the whole bottle and suddenly everything exploded!

    The kitchen was covered in {adjective} {food} everywhere!
    "{exclamation}!" I screamed as I cleaned up for the next {number} hours.

    Note to self: Never cook when {animal}s are around! 🐱🍳
        """
    },

    "zoo_escape": {
        "title": "🦁 Zoo Escape",
        "blanks": [
            ("animal", "animal"),
            ("adjective", "adjective"),
            ("plural noun", "plural_noun"),
            ("food", "food"),
            ("place", "place"),
            ("famous person", "name"),
            ("verb ending in -ing", "verb"),
            ("body part", "body_part"),
            ("adjective", "adjective"),
            ("vehicle", "noun"),
            ("exclamation", "exclamation"),
            ("number", "number"),
        ],
        "template": """
    ╔═══════════════════════════════════════════════════════════╗
    ║                  🦁 ZOO ESCAPE 🦁                         ║
    ╚═══════════════════════════════════════════════════════════╝

    The other day, the most {adjective} {animal} escaped from the zoo!
    It had eaten all the {plural noun} and decided to go on an adventure.

    First, it went to the {food} factory and stole {number} pizzas.
    Then it wandered through the {place}, scaring everyone!

    {famous person} tried to help catch it by {verb ending in -ing}
    near the {animal}'s favorite spot.

    The {animal} was too fast! It jumped into a {vehicle}
    and drove away with its {body part} hanging out the window!

    "{exclamation}!" shouted the zookeeper as the {animal} disappeared.

    The {adjective} {animal} was never seen again... or was it? 👀
        """
    },
}

def get_word_type_prompt(word_type):
    """Get a user-friendly prompt for each word type"""
    prompts = {
        "verb": "Enter a VERB (action word like 'run', 'eat', 'jump'): ",
        "verb ending in -ing": "Enter a VERB ENDING IN -ING (like 'running', 'eating', 'jumping'): ",
        "verb past tense": "Enter a VERB IN PAST TENSE (like 'ran', 'ate', 'jumped'): ",
        "adjective": "Enter an ADJECTIVE (describing word like 'big', 'silly', 'purple'): ",
        "plural noun": "Enter a PLURAL NOUN (like 'cats', 'trees', 'pizzas'): ",
        "animal": "Enter an ANIMAL (like 'dog', 'elephant', 'penguin'): ",
        "food": "Enter a FOOD (like 'pizza', 'banana', 'chocolate'): ",
        "noun": "Enter a NOUN (person, place, or thing like 'house', 'queen', 'star'): ",
        "place": "Enter a PLACE (like 'Paris', 'school', 'beach'): ",
        "name": "Enter a NAME (famous person or any name): ",
        "body part": "Enter a BODY PART (like 'nose', 'foot', 'tail'): ",
        "color": "Enter a COLOR (like 'red', 'blue', 'rainbow'): ",
        "number": "Enter a NUMBER (like '42', '100', 'infinite'): ",
        "exclamation": "Enter an EXCLAMATION (like 'Wow!', 'Oops!', 'Yikes!'): ",
        "superpower": "Enter a SUPERPOWER (like 'flight', 'invisibility', 'superspeed'): ",
        "liquid": "Enter a LIQUID (like 'water', 'juice', 'lava'): ",
        "object": "Enter an OBJECT (like 'key', 'wand', 'hammer'): ",
        "vehicle": "Enter a VEHICLE (like 'car', 'bike', 'spaceship'): ",
        "kitchen tool": "Enter a KITCHEN TOOL (like 'spoon', 'pan', 'blender'): ",
        "magical creature": "Enter a MAGICAL CREATURE (like 'unicorn', 'fairy', 'phoenix'): ",
        "comic book character": "Enter a COMIC BOOK CHARACTER (like 'Batman', 'Spider-Man', 'Wonder Woman'): ",
    }
    return prompts.get(word_type, f"Enter a {word_type}: ")

def get_word(word_type):
    """Get a word from the user"""
    prompt = get_word_type_prompt(word_type)

    colors = {
        "verb": Fore.GREEN,
        "verb ending in -ing": Fore.GREEN,
        "verb past tense": Fore.GREEN,
        "adjective": Fore.YELLOW,
        "plural noun": Fore.CYAN,
        "animal": Fore.MAGENTA,
        "food": Fore.RED,
        "noun": Fore.WHITE,
        "place": Fore.BLUE,
        "name": Fore.LIGHTMAGENTA_EX,
        "body part": Fore.LIGHTRED_EX,
        "color": Fore.YELLOW,
        "number": Fore.LIGHTGREEN_EX,
        "exclamation": Fore.LIGHTYELLOW_EX,
        "superpower": Fore.LIGHTBLUE_EX,
        "liquid": Fore.LIGHTBLUE_EX,
        "object": Fore.LIGHTMAGENTA_EX,
        "vehicle": Fore.LIGHTRED_EX,
        "kitchen tool": Fore.LIGHTGREEN_EX,
        "magical creature": Fore.LIGHTMAGENTA_EX,
        "comic book character": Fore.LIGHTYELLOW_EX,
    }

    color = colors.get(word_type, Fore.WHITE)

    while True:
        print_color(f"\n    🎯 {prompt}", color, Style.BRIGHT)
        print_color("    > ", Fore.GREEN)
        word = input().strip()

        if word:
            return word
        else:
            print_color("    ⚠️  Please enter a word! ⚠️", Fore.RED)

def play_story(story_key):
    """Play through a single story"""
    story = STORY_TEMPLATES[story_key]

    clear_screen()
    print_color(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║              {story['title']:<40} ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║   Fill in the blanks to create your hilarious story!      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.CYAN, Style.BRIGHT)

    words = {}
    total = len(story['blanks'])

    for i, (description, word_type) in enumerate(story['blanks'], 1):
        print_color(f"\n    [{i}/{total}] Word {i} of {total}", Fore.YELLOW)
        print_color(f"    Looking for: {description.upper()}", Fore.MAGENTA, Style.BRIGHT)
        words[description] = get_word(word_type)

    # Generate the story
    clear_screen()

    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                   📖 YOUR STORY 📖                        ║
    ║                                                           ║
    ║              Get ready to laugh out loud!                 ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.YELLOW, Style.BRIGHT)

    time.sleep(1)

    # Replace all the blanks
    story_text = story['template']
    for description, word in words.items():
        story_text = story_text.replace('{' + description + '}', word.upper())

    print(story_text)

    # Animation effect
    print_color("\n    🎉 STORY COMPLETE! 🎉", Fore.GREEN, Style.BRIGHT)
    print_color("    Isn't it hilarious?! 😂\n", Fore.YELLOW)

def display_menu():
    """Display the story selection menu"""
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    📚 CHOOSE A STORY 📚                  ║
    ╠═══════════════════════════════════════════════════════════╣
    """, Fore.CYAN)

    for i, (key, story) in enumerate(STORY_TEMPLATES.items(), 1):
        print_color(f"    │  [{i}] {story['title']:<45} │", Fore.YELLOW)

    print_color("    │  [A] 🎲 Play All Stories!                           │", Fore.MAGENTA)
    print_color("    │  [R] 🎯 Random Story                                │", Fore.GREEN)
    print_color("    │  [Q] 🚪 Quit                                         │", Fore.RED)
    print_color("    ╚═══════════════════════════════════════════════════════════╝", Fore.CYAN)
    print()

def main():
    display_intro()

    stories = list(STORY_TEMPLATES.keys())

    while True:
        display_menu()
        print_color("    Enter your choice: ", Fore.GREEN, Style.BRIGHT)

        try:
            choice = input().strip().lower()
        except EOFError:
            break

        if choice in ['q', 'quit', 'exit', 'bye']:
            print_color("\n    Thanks for playing Mad Libs! See you next time! 👋\n", Fore.CYAN)
            break

        elif choice == 'a':
            # Play all stories
            for key in stories:
                play_story(key)
                print_color("\n    Press ENTER to continue to the next story...", Fore.YELLOW)
                input()
                clear_screen()
            print_color("\n    🎉 YOU COMPLETED ALL STORIES! 🎉\n", Fore.GREEN, Style.BRIGHT)

        elif choice == 'r':
            # Random story
            key = random.choice(stories)
            play_story(key)
            print_color("\n    Press ENTER to continue...", Fore.YELLOW)
            input()
            clear_screen()

        elif choice.isdigit() and 1 <= int(choice) <= len(stories):
            key = stories[int(choice) - 1]
            play_story(key)
            print_color("\n    Press ENTER to continue...", Fore.YELLOW)
            input()
            clear_screen()

        else:
            print_color(f"\n    ⚠️  Invalid choice! Please enter 1-{len(stories)}, A, R, or Q. ⚠️\n", Fore.RED)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n\n    👋 Game interrupted! See you next time!\n", Fore.CYAN)
        sys.exit(0)
