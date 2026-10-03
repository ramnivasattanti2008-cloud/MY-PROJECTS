"""
Hangman Game - Word guessing game with ASCII art stages
Choose from multiple word categories: Animals, Countries, Foods, Sports, Movies
"""

import random
import os

# ASCII art for hangman stages (0-6 wrong guesses)
HANGMAN_STAGES = [
    # Stage 0 - Empty
    """
    ┌─────┐
    │     │
    │
    │
    │
    │
    ═══════
    """,
    # Stage 1 - Head
    """
    ┌─────┐
    │     │
    │     O
    │
    │
    │
    ═══════
    """,
    # Stage 2 - Body
    """
    ┌─────┐
    │     │
    │     O
    │     │
    │
    │
    ═══════
    """,
    # Stage 3 - Left arm
    """
    ┌─────┐
    │     │
    │     O
    │    /│
    │
    │
    ═══════
    """,
    # Stage 4 - Right arm
    """
    ┌─────┐
    │     │
    │     O
    │    /│\\
    │
    │
    ═══════
    """,
    # Stage 5 - Left leg
    """
    ┌─────┐
    │     │
    │     O
    │    /│\\
    │    /
    │
    ═══════
    """,
    # Stage 6 - Right leg (GAME OVER)
    """
    ┌─────┐
    │     │
    │     O
    │    /│\\
    │    / \\
    │
    ═══════
    """
]

# Word categories with words
WORD_CATEGORIES = {
    "Animals": [
        "ELEPHANT", "GIRAFFE", "PENGUIN", "DOLPHIN", "KANGAROO",
        "BUTTERFLY", "CROCODILE", "FLAMINGO", "OCTOPUS", "CHEETAH",
        "PANTHER", "GORILLA", "LEOPARD", "HAMSTER", "TORTOISE"
    ],
    "Countries": [
        "AUSTRALIA", "BRAZIL", "CANADA", "GERMANY", "ICELAND",
        "JAPAN", "MEXICO", "NORWAY", "PORTUGAL", "THAILAND",
        "ARGENTINA", "BELGIUM", "COLOMBIA", "DENMARK", "FINLAND"
    ],
    "Foods": [
        "SPAGHETTI", "CHOCOLATE", "AVOCADO", "PINEAPPLE", "BROCCOLI",
        "PANCACKES", "WAFFLES", "SANDWICH", "SALAD", "STRAWBERRY",
        "BISCUIT", "CUCUMBER", "DUMPLING", "GRAPEFRUIT", "MUSHROOM"
    ],
    "Sports": [
        "BASKETBALL", "FOOTBALL", "BASEBALL", "VOLLEYBALL", "SWIMMING",
        "TENNIS", "HOCKEY", "GOLF", "BOXING", "CYCLING",
        "ARCHERY", "BADMINTON", "CRICKET", "SKIING", "SURFING"
    ],
    "Movies": [
        "AVENGERS", "TITANIC", "GLADIATOR", "INCEPTION", "BATMAN",
        "SPIDERMAN", "FROZEN", "TOYSTORY", "JURASSIC", "STARWARS",
        "MATRIX", "PSYCHO", "VERTIGO", "CASABLANCA", "CHARIOTS"
    ],
    "Technology": [
        "COMPUTER", "KEYBOARD", "MONITOR", "INTERNET", "SOFTWARE",
        "DATABASE", "ALGORITHM", "FUNCTION", "VARIABLE", "NETWORK",
        "BROWSER", "FIRMWARE", "HARDWARE", "PROTOCOL", "TERMINAL"
    ]
}

MAX_WRONG = 6  # Number of allowed wrong guesses


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def choose_category():
    """Display category menu and return selected category"""
    clear_screen()
    print("=" * 50)
    print("         H A N G M A N")
    print("=" * 50)
    print("\nChoose a category:\n")

    categories = list(WORD_CATEGORIES.keys())
    for i, category in enumerate(categories, 1):
        word_count = len(WORD_CATEGORIES[category])
        print(f"  {i}. {category} ({word_count} words)")

    print(f"  0. Random category")
    print()

    while True:
        try:
            choice = input("Enter your choice (0-6): ").strip()
            if choice == "":
                continue
            choice_num = int(choice)
            if choice_num == 0:
                return random.choice(categories)
            elif 1 <= choice_num <= len(categories):
                return categories[choice_num - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")


def select_word(category):
    """Select a random word from the chosen category"""
    words = WORD_CATEGORIES[category]
    return random.choice(words)


def create_word_display(word):
    """Create the hidden word display (e.g., _ _ _ _ _ _)"""
    return ["_" for _ in word]


def display_game(word_display, wrong_guesses, category, guessed_letters):
    """Display the current game state"""
    clear_screen()
    print("=" * 50)
    print("         H A N G M A N")
    print("=" * 50)

    # Show category
    print(f"\n  Category: {category}")
    print()

    # Show hangman stage
    print(HANGMAN_STAGES[wrong_guesses])
    print()

    # Show word with blanks
    print("  Word: ", end="")
    for letter in word_display:
        print(f"{letter} ", end="")
    print()

    # Show guessed letters
    if guessed_letters:
        print(f"\n  Guessed letters: {' '.join(sorted(guessed_letters))}")

    # Show remaining attempts
    remaining = MAX_WRONG - wrong_guesses
    print(f"\n  Remaining attempts: {remaining}")

    # Show score
    print(f"\n  Wins: {wins}  |  Losses: {losses}")


def get_guess(guessed_letters):
    """Get a valid letter guess from the player"""
    while True:
        guess = input("\n  Enter a letter: ").strip().upper()
        if len(guess) != 1:
            print("  Please enter exactly one letter.")
        elif not guess.isalpha():
            print("  Please enter a letter (A-Z).")
        elif guess in guessed_letters:
            print(f"  You already guessed '{guess}'. Try another letter.")
        else:
            return guess


def check_guess(word, guess):
    """Check if the guessed letter is in the word"""
    return guess in word


def update_word_display(word, word_display, guess):
    """Update the word display with correctly guessed letters"""
    for i, letter in enumerate(word):
        if letter == guess:
            word_display[i] = guess


def is_word_guessed(word_display, word):
    """Check if the word is fully revealed"""
    return "_" not in word_display


def play_again():
    """Ask if player wants to play again"""
    while True:
        response = input("\n  Play again? (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("  Please enter 'y' or 'n'.")


# Global score variables
wins = 0
losses = 0


def main():
    """Main game loop"""
    global wins, losses

    while True:
        # Choose category
        category = choose_category()

        # Select word
        word = select_word(category)
        word_display = create_word_display(word)

        # Game state
        wrong_guesses = 0
        guessed_letters = set()

        # Main game loop
        while wrong_guesses < MAX_WRONG:
            display_game(word_display, wrong_guesses, category, guessed_letters)

            # Get player's guess
            guess = get_guess(guessed_letters)
            guessed_letters.add(guess)

            # Check if guess is correct
            if check_guess(word, guess):
                update_word_display(word, word_display, guess)
                display_game(word_display, wrong_guesses, category, guessed_letters)

                # Check for win
                if is_word_guessed(word_display, word):
                    wins += 1
                    print("\n  🎉 CONGRATULATIONS! You won! 🎉")
                    print(f"  The word was: {word}")
                    break
            else:
                wrong_guesses += 1
                display_game(word_display, wrong_guesses, category, guessed_letters)

                # Check for loss
                if wrong_guesses >= MAX_WRONG:
                    losses += 1
                    print("\n  💀 GAME OVER! You lost! 💀")
                    print(f"  The word was: {word}")

        # Ask to play again
        if not play_again():
            clear_screen()
            print("=" * 50)
            print("         GAME STATS")
            print("=" * 50)
            print(f"\n  Total Wins: {wins}")
            print(f"  Total Losses: {losses}")
            if wins + losses > 0:
                win_rate = (wins / (wins + losses)) * 100
                print(f"  Win Rate: {win_rate:.1f}%")
            print("\n  Thanks for playing Hangman!")
            print("=" * 50)
            break


if __name__ == "__main__":
    print("=" * 50)
    print("       H A N G M A N")
    print("=" * 50)
    print("\nGuess the word before the hangman is complete!")
    print("You have 6 wrong guesses before you lose.")
    print()
    input("Press ENTER to start...")
    main()
