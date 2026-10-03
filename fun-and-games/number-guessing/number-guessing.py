"""
Number Guessing Game - Computer guesses YOUR number!
Uses binary search algorithm to efficiently find your secret number.
Watch as the computer intelligently narrows down the possibilities.
"""

import random
import time
import os

MIN_NUMBER = 1
MAX_NUMBER = 100


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Display the game header"""
    print("=" * 60)
    print("        🎯 NUMBER GUESSING - COMPUTER EDITION 🎯")
    print("=" * 60)


def print_instructions():
    """Display game instructions"""
    print("\n  THINK OF A NUMBER BETWEEN", MIN_NUMBER, "AND", MAX_NUMBER)
    print("  I (the computer) will try to guess it!")
    print("\n  After each guess, tell me if your number is:")
    print("    - HIGHER than my guess")
    print("    - LOWER than my guess")
    print("    - CORRECT if I got it!")
    print()


def get_player_number():
    """Have player think of a number"""
    print("\n  When you've thought of your number, press ENTER...")
    input()
    print("\n  Great! Let's begin...")
    time.sleep(1)


def print_separator():
    """Print a visual separator"""
    print("-" * 60)


def binary_search_guess(low, high):
    """Make a guess using binary search strategy"""
    # Optimal guess is the middle of the range
    guess = (low + high) // 2
    return guess


def get_player_response(guess):
    """Get player's response to the guess"""
    print(f"\n  🤔 Is your number HIGHER, LOWER, or CORRECT?")
    print(f"     My guess: {guess}")
    print()

    while True:
        response = input("  Your answer (H/L/C): ").strip().upper()

        if response in ('H', 'HIGHER'):
            return 'HIGHER'
        elif response in ('L', 'LOWER'):
            return 'LOWER'
        elif response in ('C', 'CORRECT'):
            return 'CORRECT'
        else:
            print("  Please enter H (Higher), L (Lower), or C (Correct)")


def display_guess_history(guesses):
    """Display the history of all guesses made"""
    if len(guesses) > 1:
        print("\n  📝 Guess History:")
        print("  ", end="")
        for i, (guess, response) in enumerate(guesses[:-1], 1):
            # Show arrows to indicate direction
            arrow = "↑" if response == 'HIGHER' else "↓"
            print(f"{guess}{arrow} ", end="")
        print()


def display_progress(low, high, total_guesses):
    """Show the current range being searched"""
    range_size = high - low + 1
    # Calculate how much of the range is eliminated
    total_range = MAX_NUMBER - MIN_NUMBER + 1
    eliminated = ((total_range - range_size) / total_range) * 100
    print(f"\n  Range: {low} - {high} ({range_size} possibilities)")
    print(f"  Eliminated: {eliminated:.1f}% of possibilities")


def print_final_result(guess, num_guesses):
    """Display the final winning message"""
    print()
    print("=" * 60)
    print(f"  🎉 I GOT IT! Your number is {guess}! 🎉")
    print("=" * 60)

    # Performance rating based on number of guesses
    # Binary search should find any number in at most 7 guesses for 1-100
    if num_guesses == 1:
        rating = "LUCKY!"
    elif num_guesses <= 5:
        rating = "EXCELLENT!"
    elif num_guesses <= 7:
        rating = "GREAT!"
    else:
        rating = "GOOD!"

    print(f"\n  Total guesses: {num_guesses}")
    print(f"  Performance: {rating}")
    print()


def play_again():
    """Ask if player wants to play again"""
    while True:
        response = input("  Play again? (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("  Please enter 'y' or 'n'.")


def main():
    """Main game loop"""
    total_games = 0
    total_guesses = 0
    all_games_history = []

    while True:
        clear_screen()
        print_header()

        total_games += 1
        guesses_this_game = []

        print_instructions()
        get_player_number()

        # Initialize search range
        low = MIN_NUMBER
        high = MAX_NUMBER
        num_guesses = 0

        print_separator()

        # Main game loop
        while True:
            num_guesses += 1

            # Make guess using binary search
            guess = binary_search_guess(low, high)

            # Store in history
            guesses_this_game.append((guess, None))

            # Show progress
            print(f"\n  Attempt #{num_guesses}")
            print(f"  ══════════════════════")
            print(f"\n  🤔 My guess: {guess} 🤔")
            display_progress(low, high, num_guesses)

            # Get player's response
            response = get_player_response(guess)

            # Update the last guess in history with response
            guesses_this_game[-1] = (guess, response)

            # Display updated history
            display_guess_history(guesses_this_game)

            if response == 'CORRECT':
                print_final_result(guess, num_guesses)
                total_guesses += num_guesses
                all_games_history.append((num_guesses, guess))
                break

            # Adjust search range
            if response == 'HIGHER':
                low = guess + 1
            else:  # LOWER
                high = guess - 1

            # Sanity check
            if low > high:
                print("\n  ⚠️  Something went wrong! The range is invalid.")
                print("  Make sure you answered correctly (H/L/C).")
                break

            time.sleep(0.5)

        # Show stats if multiple games
        if total_games > 1:
            avg_guesses = total_guesses / total_games
            print(f"\n  📊 Session Stats:")
            print(f"     Games played: {total_games}")
            print(f"     Total guesses: {total_guesses}")
            print(f"     Average guesses per game: {avg_guesses:.2f}")

        print_separator()

        if not play_again():
            break

    # Final goodbye
    clear_screen()
    print_header()
    print("\n  Thanks for playing!")
    print(f"\n  Final Stats:")
    print(f"     Games played: {total_games}")
    print(f"     Total guesses: {total_guesses}")
    if total_games > 0:
        print(f"     Average guesses per game: {total_guesses/total_games:.2f}")
    print("\n  See you next time! 👋")
    print("=" * 60)


if __name__ == "__main__":
    print_header()
    print("\n  Welcome to the Computer Number Guessing Game!")
    print("  I'll use binary search to find your number efficiently!")
    input("\n  Press ENTER to start...")
    main()
