#!/usr/bin/env python3
"""
Rock Paper Scissors - Classic RPS Game
Challenge the computer in an epic battle of rock, paper, scissors!
Best of N rounds - how long can your streak survive?
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
        RED = WHITE = CYAN = MAGENTA = YELLOW = GREEN = BLUE = RESET = LIGHTBLACK_EX = LIGHTRED_EX = LIGHTGREEN_EX = LIGHTYELLOW_EX = ''
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
    ║   ███████╗███╗   ██╗██╗███████╗███████╗██╗ ██████╗ ███╗   ║
    ║   ██╔════╝████╗  ██║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ║
    ║   █████╗  ██╔██╗ ██║██║███████╗███████╗██║██║   ██║██╔██╗ ║
    ║   ██╔══╝  ██║╚██╗██║██║╚════██║╚════██║██║██║   ██║╚██╔╝ ║
    ║   ███████╗██║ ╚████║██║███████║███████║██║╚██████╔╝ ██║  ║
    ║   ╚══════╝╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝  ╚═╝  ║
    ║                                                           ║
    ║              ✊✋✌️  ROCK PAPER SCISSORS  ✊✋✌️              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.CYAN, Style.BRIGHT)
    print()
    print_color("    Challenge the computer in the ultimate showdown!", Fore.YELLOW)
    print_color("    Choose your weapon and may the odds be ever in your favor!\n", Fore.YELLOW)
    print()

ASCII_ART = {
    'rock': r"""
        _______
    ---'   ____)
          (_____)
          (_____)
          (____)
    ---.__(___)
    """,
    'paper': r"""
         _______
    ---'    ____)____
               ______)
              _______)
             _______)
    ---.__________)
    """,
    'scissors': r"""
        _______
    ---'   ____)____
              ______)
           __________)
          (____)
    ---.__(___)
    """
}

def display_ascii(choice):
    art = ASCII_ART.get(choice, "")
    colors = {
        'rock': Fore.RED,
        'paper': Fore.BLUE,
        'scissors': Fore.MAGENTA
    }
    print_color(art, colors.get(choice, Fore.WHITE), Style.BRIGHT)

def display_battle(player_choice, computer_choice, result):
    """Show the battle animation and result"""
    print()
    print_color("    ⚔️" * 25, Fore.YELLOW)
    print()

    # Show both choices
    print_color("    YOUR CHOICE:", Fore.GREEN, Style.BRIGHT)
    display_ascii(player_choice)

    print_color("    VS", Fore.RED, Style.BRIGHT)

    print_color("    COMPUTER'S CHOICE:", Fore.RED, Style.BRIGHT)
    display_ascii(computer_choice)

    print_color("    ⚔️" * 25, Fore.YELLOW)
    print()

def determine_winner(player, computer):
    """Determine the winner of a round"""
    if player == computer:
        return 'tie'
    elif (player == 'rock' and computer == 'scissors') or \
         (player == 'paper' and computer == 'rock') or \
         (player == 'scissors' and computer == 'paper'):
        return 'win'
    else:
        return 'lose'

def display_result(result, win_streak):
    """Display the round result"""
    if result == 'win':
        print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║            🏆 YOU WIN! CONGRATULATIONS! 🏆               ║
    ║                                                           ║
    ║           Current Win Streak: """, Fore.GREEN, Style.BRIGHT)
        print(f"{win_streak} 🔥" if win_streak >= 3 else "")
        print_color("""                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.GREEN)
    elif result == 'lose':
        print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║               💀 YOU LOSE! BETTER LUCK NEXT TIME! 💀     ║
    ║                                                           ║
    ║                    Win Streak Lost!                       ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.RED, Style.BRIGHT)
    else:
        print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║                    🤝 IT'S A TIE! 🤝                      ║
    ║                                                           ║
    ║                 No points awarded this round              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.YELLOW, Style.BRIGHT)

def display_scoreboard(player_wins, computer_wins, ties, win_streak, best_streak, target):
    """Display the current scoreboard"""
    player_progress = "█" * player_wins + "░" * max(0, target - player_wins - computer_wins - ties)
    computer_progress = "█" * computer_wins + "░" * max(0, target - player_wins - computer_wins - ties)

    print_color(f"""
    ┌─────────────────────────────────────────────────────────┐
    │                    📊 SCOREBOARD 📊                     │
    ├─────────────────────────────────────────────────────────┤
    │  YOU:      {player_progress} {player_wins}/{target}                       │
    │  COMPUTER: {computer_progress} {computer_wins}/{target}                       │
    │  TIES: {ties}                                                 │
    ├─────────────────────────────────────────────────────────┤
    │  Current Streak: {win_streak:2d} | Best Streak: {best_streak:2d}                 │
    └─────────────────────────────────────────────────────────┘
    """, Fore.CYAN)

def get_player_choice():
    """Get and validate player's choice"""
    print_color("""
    ┌─────────────────────────────────────────────────────────┐
    │  [1] ✊ ROCK                                            │
    │  [2] ✋ PAPER                                           │
    │  [3] ✌️ SCISSORS                                        │
    │  [R] 📊 View Rules                                      │
    │  [Q] 🚪 Quit                                            │
    └─────────────────────────────────────────────────────────┘
    """, Fore.WHITE)
    print()
    print_color("    Enter your choice (1/2/3/R/Q): ", Fore.GREEN, Style.BRIGHT)

    choice = input().strip().lower()

    choices = {'1': 'rock', '2': 'paper', '3': 'scissors', 'rock': 'rock', 'paper': 'paper', 'scissors': 'scissors'}

    if choice == 'r':
        show_rules()
        return None
    elif choice in ['q', 'quit', 'exit']:
        return 'quit'
    elif choice in choices:
        return choices[choice]
    else:
        print_color("\n    ⚠️  Invalid choice! Please enter 1, 2, or 3. ⚠️\n", Fore.RED)
        return None

def show_rules():
    clear_screen()
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                      📜 GAME RULES 📜                     ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║   The game is simple:                                     ║
    ║                                                           ║
    ║   ✊ ROCK beats ✌️ SCISSORS                                ║
    ║   ✋ PAPER beats ✊ ROCK                                   ║
    ║   ✌️ SCISSORS beats ✋ PAPER                              ║
    ║                                                           ║
    ║   First to win """, Fore.YELLOW, Style.BRIGHT)
    print(f"{N_ROUNDS}", end='')
    print_color(""".rounds wins the match!                          ║
    ║                                                           ║
    ║   Build your win streak for bonus bragging rights!        ║
    ║   Ties don't count - you'll replay the round!             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.YELLOW)
    print()

def get_target_rounds():
    """Ask player how many rounds they want to play"""
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                   🎯 MATCH SETUP 🎯                       ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║   How many rounds would you like to play?                  ║
    ║                                                           ║
    ║   [1] Quick Match (3 rounds) ⚡                          ║
    ║   [2] Standard Match (5 rounds) 🎮                        ║
    ║   [3] Epic Battle (7 rounds) 🔥                          ║
    ║   [4] Custom (enter a number)                             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.CYAN)
    print()
    print_color("    Enter your choice (1/2/3/4): ", Fore.GREEN, Style.BRIGHT)

    try:
        choice = input().strip()
        if choice == '1':
            return 3
        elif choice == '2':
            return 5
        elif choice == '3':
            return 7
        elif choice == '4':
            print_color("    Enter number of rounds (1-21): ", Fore.YELLOW)
            n = int(input().strip())
            return max(1, min(21, n))
        else:
            return 5
    except ValueError:
        return 5

N_ROUNDS = 5

def play_game():
    global N_ROUNDS

    N_ROUNDS = get_target_rounds()
    clear_screen()

    print_color(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                  ⚔️ BATTLE BEGIN! ⚔️                       ║
    ║                                                           ║
    ║           Best of {N_ROUNDS} rounds - may the best player win!          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.YELLOW, Style.BRIGHT)

    player_wins = 0
    computer_wins = 0
    ties = 0
    win_streak = 0
    best_streak = 0
    round_num = 1

    while player_wins < (N_ROUNDS + 1) // 2 + 1 and computer_wins < (N_ROUNDS + 1) // 2 + 1:
        # Check if match is decided
        remaining_for_player = (N_ROUNDS + 1) // 2 + 1 - player_wins
        remaining_for_computer = (N_ROUNDS + 1) // 2 + 1 - computer_wins

        if player_wins >= (N_ROUNDS + 1) // 2 + 1:
            break
        if computer_wins >= (N_ROUNDS + 1) // 2 + 1:
            break

        print()
        print_color(f"    ┌─────────────────────────────────────────────────┐", Fore.CYAN)
        print_color(f"    │           ROUND {round_num} OF {N_ROUNDS}                              │", Fore.CYAN, Style.BRIGHT)
        print_color(f"    └─────────────────────────────────────────────────┘", Fore.CYAN)

        display_scoreboard(player_wins, computer_wins, ties, win_streak, best_streak, N_ROUNDS)

        # Get player's choice
        player_choice = None
        while player_choice is None:
            player_choice = get_player_choice()
            if player_choice == 'quit':
                print_color("\n    Thanks for playing! See you next time! 👋\n", Fore.CYAN)
                return

        # Computer choice
        computer_choice = random.choice(['rock', 'paper', 'scissors'])

        # Countdown
        print_color("\n    Get ready...", Fore.YELLOW)
        for i in range(3, 0, -1):
            print_color(f"    {i}...", Fore.RED, Style.BRIGHT)
            time.sleep(0.5)

        clear_screen()

        print_color(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    ⚔️ ROUND {round_num} ⚔️                          ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.MAGENTA, Style.BRIGHT)

        display_battle(player_choice, computer_choice, None)

        result = determine_winner(player_choice, computer_choice)

        if result == 'win':
            player_wins += 1
            win_streak += 1
            best_streak = max(best_streak, win_streak)
        elif result == 'lose':
            computer_wins += 1
            win_streak = 0
        else:
            ties += 1

        display_result(result, win_streak)

        round_num += 1

        if player_wins >= (N_ROUNDS + 1) // 2 + 1 or computer_wins >= (N_ROUNDS + 1) // 2 + 1:
            break

        print_color("    Press ENTER to continue to the next round...", Fore.YELLOW)
        input()
        clear_screen()

    # Final results
    clear_screen()
    print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                   🏆 MATCH COMPLETE! 🏆                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.YELLOW, Style.BRIGHT)

    display_scoreboard(player_wins, computer_wins, ties, win_streak, best_streak, N_ROUNDS)

    print()
    if player_wins > computer_wins:
        print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║            🎉🎉🎉 YOU ARE THE CHAMPION! 🎉🎉🎉            ║
    ║                                                           ║
    ║              The crowd goes wild! 🏆🎊🥳                 ║
    ║                                                           ║
    ║            Best Win Streak: """, Fore.GREEN, Style.BRIGHT)
        print(f"{best_streak} 🔥")
        print_color("""                                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.GREEN)
    else:
        print_color("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║            😢 THE COMPUTER WINS... 😢                     ║
    ║                                                           ║
    ║             But champions never give up!                   ║
    ║                                                           ║
    ║            Best Win Streak: """, Fore.RED, Style.BRIGHT)
        print(f"{best_streak} 🔥")
        print_color("""                                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """, Fore.RED)

    print()
    print_color("    Would you like to play again? (y/n): ", Fore.CYAN)
    choice = input().strip().lower()
    if choice == 'y':
        play_game()

def main():
    try:
        play_game()
    except KeyboardInterrupt:
        print_color("\n\n    👋 Game interrupted! See you next time!\n", Fore.CYAN)
        sys.exit(0)

if __name__ == "__main__":
    main()
