#!/usr/bin/env python3
"""
Truth or Dare - Classic Party Game
The ultimate Truth or Dare experience with multiple players!
Spin the bottle, face the challenges, and discover secrets!
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
        RED = WHITE = CYAN = MAGENTA = YELLOW = GREEN = BLUE = RESET = LIGHTBLACK_EX = LIGHTRED_EX = LIGHTGREEN_EX = LIGHTYELLOW_EX = LIGHTBLUE_EX = LIGHTMAGENTA_EX = LIGHTRED_EX = ''
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
    ║    ███████╗██╗  ██╗██╗    ██╗███████╗██████╗ ███████╗    ║
    ║    ██╔════╝██║  ██║██║    ██║██╔════╝██╔══██╗██╔════╝    ║
    ║    ███████╗███████║██║ █╗ ██║█████╗  ██████╔╝███████╗    ║
    ║    ╚════██║██╔══██║██║███╗██║██╔══╝  ██╔══██╗╚════██║    ║
    ║    ███████║██║  ██║╚███╔███╔╝███████╗██║  ██║███████║    ║
    ║    ╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚══════╝    ║
    ║                                                           ║
    ║              🎭 TRUTH OR DARE! 🎭                        ║
    ║                                                           ║
    ║           The Ultimate Party Game Experience             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.MAGENTA, Style.BRIGHT)
    print()
    print_color("    Dare your friends, uncover secrets, and have a blast!", Fore.CYAN)
    print_color("    Perfect for parties, sleepovers, and boring evenings! 🎉\n", Fore.CYAN)
    print()

TRUTHS = [
    "What's the most embarrassing thing you've ever done in public?",
    "Have you ever had a crush on a friend's partner? Be honest!",
    "What's your biggest fear that you've never told anyone?",
    "What's the meanest thing you've ever said about someone behind their back?",
    "Have you ever cheated on a test? We won't tell!",
    "What's your guilty pleasure that you'd never admit publicly?",
    "Who in this room would you most want to be stuck on a deserted island with?",
    "What's the weirdest dream you've ever had?",
    "Have you ever lied to get out of trouble? What for?",
    "What's the most ridiculous thing on your bucket list?",
    "Have you ever stalked an ex on social media?",
    "What's a secret you've never told anyone in this room?",
    "What's the most childish thing you still do as an adult?",
    "Have you ever been caught doing something embarrassing?",
    "What's your unpopular opinion that might upset people?",
    "What's the biggest lie you've ever told your parents?",
    "Have you ever had a dream about someone in this room?",
    "What's the most money you've ever spent on something ridiculous?",
    "Have you ever broken something and blamed someone else?",
    "What's your most embarrassing childhood memory?",
    "What's a skill you pretend to have but actually don't?",
    "Have you ever said 'I love you' without meaning it?",
    "What's the worst date you've ever been on?",
    "What's your most embarrassing text message mistake?",
    "Have you ever had a crush on someone twice your age?",
    "What's the pettiest reason you've ever ended a relationship?",
    "Have you ever lied about reading a book or watching a movie?",
    "What's the weirdest thing you've ever Googled at 3 AM?",
    "Have you ever pretended to be sick to skip school or work?",
    "What's a rumor you were once spreading about yourself?",
    "What's the most cringey thing in your search history?",
    "Have you ever changed your answer to a multiple choice question and regretted it?",
    "What's your biggest regret in life so far?",
    "What's a habit you have that you'd never admit to a partner?",
    "Have you ever cried during a movie? Which one?",
    "What's the most embarrassing photo on your phone?",
    "Have you ever had a wardrobe malfunction in public?",
    "What's the worst present you've ever received?",
    "Have you ever fallen asleep during an important meeting or class?",
    "What's the most embarrassing song on your playlist?",
]

DARES = [
    "Do your best impression of someone in this room!",
    "Let someone post anything they want on your social media!",
    "Speak in a foreign accent for the next 3 rounds!",
    "Let the group go through your last 5 text messages!",
    "Call your crush right now and tell them you like them!",
    "Eat a spoonful of hot sauce - no complaints allowed!",
    "Do 20 pushups or 30 seconds plank right now!",
    "Let someone style your hair any way they want!",
    "Sing the chorus of the last song you listened to out loud!",
    "Do a dramatic reading of the last text message you sent!",
    "Let the group pick an embarrassing photo to set as your profile picture for 1 hour!",
    "Speak only in questions for the next 3 rounds!",
    "Let someone draw a mustache on your face with a marker!",
    "Do your best celebrity impression - can be anyone!",
    "Recreate a famous painting using only people in the room!",
    "Let the group go through your photo gallery and pick your new profile pic!",
    "Do a cartwheel or attempt one if you can't!",
    "Let someone send a text to anyone in your contacts - you decide who!",
    "Tell a joke - if no one laughs, take a penalty drink!",
    "Text your ex 'I miss you' - show the replies!",
    "Do your best viral TikTok dance move!",
    "Let someone tickle you for 30 seconds straight!",
    "Eat a raw egg - if you refuse, accept a challenge penalty!",
    "Call a random number and sing 'Happy Birthday' if they answer!",
    "Do your best airplane impression around the room!",
    "Let the group create a new, embarrassing email address for you!",
    "Read aloud the last thing you typed on your phone - don't scroll!",
    "Attempt to juggle 3 items from the room for 30 seconds!",
    "Let someone rename you for the rest of the game!",
    "Do your best politician's speech about why pizza is better than ice cream!",
    "Talk in a robot voice for the next 5 minutes!",
    "Let someone hide something in your clothes without you looking!",
    "Attempt to lick your elbow for 30 seconds - don't give up!",
    "Make a poem about the person to your left - out loud!",
    "Let the group give you a new hairstyle using only what's available!",
    "Do an impression of your favorite animal until someone guesses it!",
    "Let someone post a story on your Instagram - no deleting for 24 hours!",
    "Eat a mystery food combination the group creates!",
    "Do the moonwalk across the room - in character!",
    "Let someone braid your hair while you try to continue the game!",
    "Recreate a famous movie scene with props from around the room!",
]

TRUTH_BONUS = [
    "What's the worst thing you've ever said to someone you loved?",
    "Have you ever been in love with two people at the same time?",
    "What's your biggest insecurity?",
    "What's something you're ashamed of about your family?",
    "What's the biggest mistake of your life?",
    "Have you ever betrayed someone's trust? Tell us about it.",
    "What's the most inappropriate thing you've ever done at work or school?",
    "What's a dark secret you'd take to your grave?",
    "Who was your first love and what happened?",
    "What's the cruelest thing you've ever done?",
]

DARE_HARD = [
    "Walk around the block singing 'I Will Survive' at the top of your lungs!",
    "Call your mom and tell her you broke something expensive - no explanation!",
    "Do a handstand against the wall - hold for 30 seconds!",
    "Let someone put ice down your shirt - no complaints!",
    "Go outside and howl at the moon like a werewolf!",
    "Let the group blindfold you and feed you mystery foods!",
    "Do a full split or attempt for 30 seconds!",
    "Let someone put makeup on you while you keep a straight face!",
    "Give a 2-minute stand-up comedy routine - the group is your audience!",
    "Run around the room flapping your arms like a chicken for 1 minute!",
    "Let someone trade one item of clothing with you - they choose!",
    "Speak in rhymes for the next 10 minutes!",
    "Let the group plan your next vacation and you must agree!",
    "Do the worm dance across the floor!",
    "Let someone send a voice message to your boss or teacher!",
    "Spin around 10 times and then try to walk in a straight line!",
    "Let someone tickle you until you laugh - no holding back!",
    "Do an interpretive dance to the most dramatic song you know!",
    "Let the group create a pickup line for you to use on the next person who enters!",
    "Attempt to juggle while reciting the alphabet backwards!",
]

def get_players():
    """Get player names"""
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                   👥 PLAYER SETUP 👥                      ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║   Enter player names, one at a time.                       ║
    ║   Type 'done' when all players have joined.                 ║
    ║   Minimum 2 players required!                              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.CYAN)

    players = []

    while True:
        print_color(f"    Players so far: {len(players)}", Fore.YELLOW)
        if players:
            for i, name in enumerate(players, 1):
                print_color(f"      [{i}] {name}", Fore.GREEN)
        print()
        print_color("    Enter player name (or 'done' to start): ", Fore.GREEN, Style.BRIGHT)

        name = input().strip()

        if name.lower() in ['done', 'start', 'play', 'go']:
            if len(players) >= 2:
                break
            else:
                print_color("\n    ⚠️  You need at least 2 players to play! ⚠️\n", Fore.RED)
        elif name and name.lower() not in [p.lower() for p in players]:
            players.append(name)
            print_color(f"    ✓ {name} has joined the game!\n", Fore.GREEN)
        else:
            print_color("\n    ⚠️  Name already taken or invalid! ⚠️\n", Fore.RED)

    return players

def display_bottle_spin(players):
    """Show spinning bottle animation"""
    for _ in range(3):
        for i in range(len(players)):
            clear_screen()
            print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                🍺 SPINNING THE BOTTLE 🍺                  ║
    ╚═══════════════════════════════════════════════════════════╝
            """, Fore.YELLOW, Style.BRIGHT)

            # Show rotated list
            rotated = players[i:] + players[:i]
            print("\n")
            for j, name in enumerate(rotated):
                if j == 0:
                    print_color(f"       🍻 {name} <-- BOTTLE", Fore.RED, Style.BRIGHT)
                else:
                    print_color(f"           {name}", Fore.CYAN)

            time.sleep(0.3)

    return random.choice(players)

def get_truth_or_dare():
    """Ask player to choose truth or dare"""
    print_color("""
    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │   [1] 🤫 TRUTH  -  Answer honestly (no lying!)        │
    │   [2] 🎯 DARE   -  Complete a challenge!                │
    │                                                         │
    │   [3] 🎲 HARD MODE - Extreme truths and dares!          │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """, Fore.WHITE)
    print()
    print_color("    Make your choice (1/2/3): ", Fore.GREEN, Style.BRIGHT)

    return input().strip()

def display_truth():
    """Display a random truth"""
    truth = random.choice(TRUTHS + TRUTH_BONUS)
    print()
    print_color("    ┌" + "─" * 56 + "┐", Fore.RED)
    print_color("    │" + " " * 56 + "│", Fore.RED)
    print_color("    │  🤫 THE TRUTH:                                    │", Fore.RED, Style.BRIGHT)
    print_color("    │" + " " * 56 + "│", Fore.RED)

    # Wrap text
    words = truth.split()
    line = "    │  "
    for word in words:
        if len(line) + len(word) < 60:
            line += word + " "
        else:
            print_color(line + " " * (60 - len(line)) + "│", Fore.WHITE)
            line = "    │  " + word + " "
    print_color(line + " " * (60 - len(line)) + "│", Fore.WHITE)

    print_color("    │" + " " * 56 + "│", Fore.RED)
    print_color("    └" + "─" * 56 + "┘", Fore.RED)
    print()

def display_dare(hard=False):
    """Display a random dare"""
    if hard:
        dare = random.choice(DARE_HARD)
    else:
        dare = random.choice(DARES)

    print()
    print_color("    ┌" + "─" * 56 + "┐", Fore.GREEN)
    print_color("    │" + " " * 56 + "│", Fore.GREEN)
    print_color("    │  🎯 THE DARE:                                     │", Fore.GREEN, Style.BRIGHT)
    print_color("    │" + " " * 56 + "│", Fore.GREEN)

    # Wrap text
    words = dare.split()
    line = "    │  "
    for word in words:
        if len(line) + len(word) < 60:
            line += word + " "
        else:
            print_color(line + " " * (60 - len(line)) + "│", Fore.WHITE)
            line = "    │  " + word + " "
    print_color(line + " " * (60 - len(line)) + "│", Fore.WHITE)

    print_color("    │" + " " * 56 + "│", Fore.GREEN)
    print_color("    └" + "─" * 56 + "┘", Fore.GREEN)
    print()

def display_turn(player, players):
    """Show whose turn it is"""
    print()
    print_color("    ╔═══════════════════════════════════════════════════════════╗", Fore.MAGENTA)
    print_color("    ║                                                           ║", Fore.MAGENTA)

    # Highlight current player
    padding = (59 - len(f"🎯 {player.upper()}'S TURN")) // 2
    text = f"{' ' * padding}🎯 {player.upper()}'S TURN"
    print_color(f"    ║{text}{' ' * (59 - len(text))}║", Fore.MAGENTA, Style.BRIGHT)

    print_color("    ║                                                           ║", Fore.MAGENTA)
    print_color("    ╚═══════════════════════════════════════════════════════════╝", Fore.MAGENTA)
    print()

    # Show others watching
    others = [p for p in players if p != player]
    if others:
        print_color(f"    👀 Everyone else watches as {player} makes their choice...\n", Fore.YELLOW)

def display_player_scores(scores):
    """Show current scores"""
    print_color("""
    ┌─────────────────────────────────────────────────────────┐
    │                     📊 SCORES 📊                        │
    ├─────────────────────────────────────────────────────────┤
    """, Fore.CYAN)

    if not scores:
        print_color("    │              No points yet - keep playing!              │", Fore.YELLOW)
    else:
        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for i, (player, score) in enumerate(sorted_scores, 1):
            medals = {1: "🥇", 2: "🥈", 3: "🥉"}
            medal = medals.get(i, "  ")
            bar = "█" * min(score, 20) + "░" * max(0, 20 - score)
            print_color(f"    │  {medal} {player:<15} {bar} {score:3d} pts │", Fore.YELLOW)

    print_color("    └─────────────────────────────────────────────────────────┘", Fore.CYAN)

def play_game():
    """Main game loop"""
    players = get_players()
    scores = {player: 0 for player in players}
    turn_count = 0

    clear_screen()
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              🎉 LET THE GAMES BEGIN! 🎉                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.GREEN, Style.BRIGHT)

    print(f"    Players: {', '.join(players)}\n")

    time.sleep(2)

    while True:
        turn_count += 1

        # Display scores
        clear_screen()
        print_color(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    TURN {turn_count}                               ║
    ╚═══════════════════════════════════════════════════════════╝
        """, Fore.CYAN, Style.BRIGHT)

        display_player_scores(scores)

        # Spin bottle to pick player
        current_player = display_bottle_spin(players)

        # Show whose turn
        clear_screen()
        display_turn(current_player, players)

        # Get choice
        choice = get_truth_or_dare()

        if choice == '3':
            # Hard mode
            truth_or_dare = random.choice(['truth', 'dare'])
            hard_mode = True
        else:
            truth_or_dare = 'truth' if choice == '1' else 'dare'
            hard_mode = False

        # Execute
        if truth_or_dare == 'truth':
            display_truth()
            print_color("    ⏳ Take your time to answer honestly...\n", Fore.YELLOW)
        else:
            display_dare(hard_mode)
            print_color("    ⏳ Complete the dare or face the penalty...\n", Fore.YELLOW)

        # Did they complete it?
        print_color("    Did they complete it successfully? (y/n/q for quit): ", Fore.GREEN, Style.BRIGHT)
        response = input().strip().lower()

        if response == 'y':
            scores[current_player] += 10 if hard_mode else 5
            print_color(f"\n    🎉 {current_player} earned points! (+{10 if hard_mode else 5})\n", Fore.GREEN)
        elif response == 'n':
            scores[current_player] -= 2
            print_color(f"\n    😬 {current_player} lost points! (-2)\n", Fore.RED)
        elif response in ['q', 'quit', 'exit']:
            break

        time.sleep(1)

        # Ask to continue
        print_color("    Press ENTER for next turn (or 'q' to quit): ", Fore.YELLOW)
        cont = input().strip().lower()
        if cont in ['q', 'quit', 'exit']:
            break

    # Game over
    clear_screen()
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    🏆 GAME OVER 🏆                       ║
    ╠═══════════════════════════════════════════════════════════╣
    """, Fore.YELLOW, Style.BRIGHT)

    print_color(f"    Total turns played: {turn_count}\n", Fore.CYAN)

    # Sort and display final scores
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if sorted_scores:
        print_color("    FINAL STANDINGS:\n", Fore.CYAN, Style.BRIGHT)

        medals = {0: "🥇", 1: "🥈", 2: "🥉"}

        for i, (player, score) in enumerate(sorted_scores):
            medal = medals.get(i, "  ")
            trophy = "👑" if i == 0 else "   "
            print_color(f"    {medal} {trophy} {player:<15} {score:4d} points",
                       Fore.YELLOW if i == 0 else Fore.WHITE,
                       Style.BRIGHT if i == 0 else Style.NORMAL)

        print()
        winner = sorted_scores[0][0]
        print_color(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         🎉 {winner.upper()} IS THE ULTIMATE TRUTH OR DARE CHAMPION! 🎉    ║
    ║                                                           ║
    ║               Thanks for playing, everyone!               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
        """, Fore.GREEN, Style.BRIGHT)

def main():
    try:
        play_game()
    except KeyboardInterrupt:
        print_color("\n\n    👋 Game interrupted! See you next time!\n", Fore.CYAN)
        sys.exit(0)

if __name__ == "__main__":
    main()
