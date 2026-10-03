#!/usr/bin/env python3
"""
Fortune Cookie - A virtual fortune cookie generator
Get random fortunes with beautiful ASCII art presentation!
"""

import random
import time

# Fortune collection organized by category
FORTUNES = {
    "wisdom": [
        ("The best time to plant a tree was 20 years ago. The second best time is now.", "Ancient Proverb"),
        ("A journey of a thousand miles begins with a single step.", "Lao Tzu"),
        ("The fool doth think they are wise, but the wise man knows himself to be a fool.", "William Shakespeare"),
        ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
        ("The only true wisdom is in knowing you know nothing.", "Socrates"),
        ("Life is what happens when you're busy making other plans.", "John Lennon"),
        ("The mind is everything. What you think you become.", "Buddha"),
        ("Happiness is not something ready-made. It comes from your own actions.", "Dalai Lama"),
        ("The only impossible journey is the one you never begin.", "Tony Robbins"),
        ("When you know better you do better.", "Maya Angelou"),
        ("The greatest glory in living lies not in never falling, but in rising every time we fall.", "Nelson Mandela"),
        ("It is not the strongest of the species that survives, nor the most intelligent.", "Charles Darwin"),
        ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
        ("If you look at what you have in life, you'll always have more.", "Oprah Winfrey"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ],
    "humor": [
        ("You will trip over a tree in a forest where no one can see you.", "Unknown"),
        ("Your code will compile successfully on the first try. (This is a lie.)", "Developer's Curse"),
        ("A beautiful person will confuse you in the next 24 hours.", "Mysterious Fortune"),
        ("You will finally clean out that one drawer... eventually.", "Household Prophecy"),
        ("Your favorite show will release a new season when you least expect it!", "Streaming Fortune"),
        ("Someone will mispronounce your name today. Smile and correct them kindly.", "Social Wisdom"),
        ("You will find money in an old pocket. Spend it on something unnecessary!", "Financial Fortune"),
        ("A Wi-Fi signal will appear from nowhere. Connect quickly!", "Digital Prophecy"),
        ("Your battery will last until the critical moment. Then it won't.", "Tech Wisdom"),
        ("You will successfully resist the urge to check your phone. For at least 5 minutes.", "Digital Detox Fortune"),
        ("A coworker will ask 'Quick question' and it will not be quick.", "Office Prophecy"),
        ("Your快递 is out for delivery. It will be delivered. Eventually.", "Delivery Fortune"),
        ("Someone will tell you 'We should catch up!' and you both will forget.", "Social Media Prophecy"),
        ("You will remember the thing you forgot right after the meeting ends.", "Memory Fortune"),
        ("Your favorite restaurant will be closed for cleaning. On the one day you craved it.", "Culinary Prophecy"),
    ],
    "motivation": [
        ("You are capable of amazing things you haven't even imagined yet.", "Inner Voice"),
        ("Every expert was once a beginner. Keep learning!", "Growth Mindset"),
        ("Your potential is limitless. Don't let fear hold you back.", "Motivation Card"),
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("The secret of getting ahead is getting started.", "Mark Twain"),
        ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
        ("Your limitation—it's only your imagination.", "Fitness Fortune"),
        ("Push yourself, because no one else is going to do it for you.", "Daily Motivation"),
        ("Great things never come from comfort zones.", "Dream Big"),
        ("Dream it. Wish it. Do it.", "Action Fortune"),
        ("Success doesn't just find you. You have to go out and get it.", "Entrepreneur's Wisdom"),
        ("The harder you work for something, the greater you'll feel when you achieve it.", "Work Ethic Fortune"),
        ("Don't stop when you're tired. Stop when you're done.", "Persistence Card"),
        ("Wake up with determination. Go to bed with satisfaction.", "Daily Wisdom"),
    ],
    "love": [
        ("Love is not about possession, it's about appreciation.", "Relationship Wisdom"),
        ("You will meet someone who makes your heart skip a beat.", "Romantic Fortune"),
        ("The best relationship is one where your love for each other exceeds your need for each other.", "Relationship Card"),
        ("You are worthy of love, respect, and happiness.", "Self-Love Fortune"),
        ("A kind word from a stranger will brighten your day.", "Social Love"),
        ("Someone is thinking about you right now. Smiling.", "Distant Love"),
        ("Your soulmate is closer than you think. Look around you.", "Love Prophecy"),
        ("True love waits, but it never stops searching for you.", "Patience in Love"),
        ("The love you give is the love you receive.", "Karmic Love"),
        ("You will reconnect with an old friend. Reach out!", "Friendship Fortune"),
        ("Love is not finding someone to live with, it's finding someone you can't live without.", "Heart Wisdom"),
        ("Your kindness will attract wonderful people to your life.", "Attraction Fortune"),
        ("A small gesture of love will make someone's day today.", "Pay It Forward"),
        ("Family bonds will bring unexpected joy this season.", "Family Fortune"),
        ("You will learn to love yourself before you can fully love others.", "Self-Discovery"),
    ],
    "success": [
        ("Your hard work will pay off in unexpected ways.", "Success Fortune"),
        ("Opportunity will knock. Be ready to answer!", "Opportunity Card"),
        ("The project you're dreading will become your greatest achievement.", "Career Prophecy"),
        ("Your creativity will peak in the coming days. Use it wisely!", "Creative Fortune"),
        ("A mentor will notice your potential and offer guidance.", "Career Wisdom"),
        ("Trust your instincts. They've led you right so far.", "Intuition Card"),
        ("Your persistence will inspire others around you.", "Leadership Fortune"),
        ("Big changes are coming. Embrace them with open arms!", "Change Fortune"),
        ("The risk you almost didn't take is the one that will change everything.", "Risk Taker's Fortune"),
        ("Your reputation for reliability will open new doors.", "Professional Wisdom"),
        ("A long-held goal will finally come to fruition.", "Achievement Fortune"),
        ("You will discover a hidden talent you never knew you had.", "Self-Discovery Card"),
        ("Your next interview will be successful. Be yourself!", "Career Fortune"),
        ("Financial abundance is heading your way. Prepare!", "Prosperity Fortune"),
        ("The recognition you've been working for is just around the corner.", "Achievement Prophecy"),
    ],
}

# Fun facts to display after fortunes
FUN_FACTS = [
    "Honey never spoils. Archaeologists have found 3,000-year-old honey that's still edible!",
    "A group of flamingos is called a 'flamboyance'.",
    "Octopuses have three hearts and blue blood.",
    "Bananas are berries, but strawberries aren't.",
    "The shortest war in history lasted 38-45 minutes between Britain and Zanzibar in 1896.",
    "A day on Venus is longer than a year on Venus.",
    "Cows have best friends and get stressed when separated.",
    "The inventor of the Pringles can is buried in one.",
    "Sea otters hold hands when they sleep to keep from drifting apart.",
    "The unicorn is the national animal of Scotland.",
    "The first oranges weren't orange - they were green!",
    "Dolphins have names for each other.",
    "A jiffy is an actual unit of time: 1/100th of a second.",
    "Butterflies taste with their feet.",
    "The moon has moonquakes.",
    "Elephants are the only animals that can't jump.",
    "A cloud can weigh more than a million pounds.",
    "Sharks existed before trees.",
    "The shortest war lasted 38 minutes between Britain and Zanzibar.",
    "Your stomach gets a new lining every 3-4 days to avoid digesting itself.",
    "The Eiffel Tower can be 15 cm taller during hot days due to thermal expansion.",
    "Venus is the only planet that spins clockwise.",
    "The死不瞑目 word 'set' has the most definitions in the English language.",
    "Kleenex was originally marketed as a filter for gas masks.",
    "Avocados were named after the Aztec word for testicle.",
]

# ASCII Art
FORTUNE_COOKIE_ART = r"""
     .-""""""-.
   .'          '.
  /   O      O   \
 :           `    :
 |                |
 :    .------.    :
  \  '        '  /
   '.          .'
     '-......-'
"""

CRACKED_COOKIE_ART = r"""
      _.-''-._
    .'        '.
   /   O    O   \
  :       __     :
  |     .'  '.   |
  :   /   ||   \ :
   \ |    ||    |/
    '.  __||__  .'
      '-.__||__.-'
       \  ||  /
        '-''-'
"""

BOX_ART = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   YOUR FORTUNE:                                            ║
║                                                            ║
║"""

BOX_BOTTOM = """
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""

def print_slow(text, delay=0.03):
    """Print text with a typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_lucky_numbers():
    """Generate random lucky numbers"""
    return sorted(random.sample(range(1, 50), 5))

def get_fortune():
    """Get a random fortune from any category"""
    category = random.choice(list(FORTUNES.keys()))
    fortune, source = random.choice(FORTUNES[category])
    return fortune, source, category

def print_fortune_cookie():
    """Display the fortune cookie experience"""
    # Introduction
    print("\n" + "=" * 60)
    print("         🌟  FORTUNE COOKIE  🌟".center(50))
    print("=" * 60)
    print("\nClose your eyes and think of a question...")
    input("\nPress Enter when you're ready to reveal your fortune...")

    # Show cracking animation
    print("\n" + FORTUNE_COOKIE_ART)
    print("Cracking open the fortune cookie...")
    time.sleep(0.5)

    # Transition to cracked cookie
    print("\r" + " " * 40 + "\r" + CRACKED_COOKIE_ART)
    print("\n")

    # Get and display fortune
    fortune, source, category = get_fortune()
    lucky_numbers = get_lucky_numbers()
    fun_fact = random.choice(FUN_FACTS)

    # Display fortune in box
    print(BOX_ART)

    # Word wrap the fortune
    max_width = 52
    words = fortune.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Center each line
    for line in lines:
        padding = (54 - len(line)) // 2
        print(f"║{' ' * padding}{line}{' ' * (54 - padding - len(line))}║")

    print(f"║                                                            ║")
    print(f"║   - {source}".ljust(61) + "║")
    print(BOX_BOTTOM)

    # Display metadata
    print(f"\n   📂 Category: {category.capitalize()}")
    print(f"   🍀 Lucky Numbers: {', '.join(map(str, lucky_numbers))}")
    print(f"\n   💡 Fun Fact: {fun_fact}")

    print("\n" + "-" * 60)

def main():
    """Main function to run the fortune cookie"""
    print("\n" + "🌟" * 20)
    print("   Welcome to the Fortune Cookie Machine!")
    print("🌟" * 20)

    while True:
        print_fortune_cookie()

        # Ask if user wants another fortune
        try:
            response = input("\nWould you like another fortune? (y/n): ").strip().lower()
            if response not in ['y', 'yes', 'yeah', 'yep', 'sure', 'ok']:
                print("\n" + "=" * 60)
                print("   Thank you for visiting the Fortune Cookie!")
                print("   May your day be filled with wonder! ✨")
                print("=" * 60 + "\n")
                break
            # Clear screen effect (cross-platform)
            print("\n" + "\n".join(["" for _ in range(30)]))
        except (KeyboardInterrupt, EOFError):
            print("\n\n\n   Thanks for playing! Goodbye! 👋\n")
            break

if __name__ == "__main__":
    main()
