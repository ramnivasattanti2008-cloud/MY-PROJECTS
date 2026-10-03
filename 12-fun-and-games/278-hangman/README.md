# Hangman Game

A classic word guessing game with ASCII art and multiple word categories.

## How to Play

1. **Run the game:**
   ```bash
   python hangman.py
   ```

2. **Choose a Category:**
   - Animals
   - Countries
   - Foods
   - Sports
   - Movies
   - Technology
   - Random

3. **Gameplay:**
   - The computer picks a word and shows you blanks
   - Guess letters one at a time
   - Correct guesses reveal the letter positions
   - Wrong guesses build the hangman (6 stages)
   - Win by guessing the word before the hangman is complete!

## Features

- 6 unique word categories
- ASCII art hangman visualization
- Tracks wins and losses across sessions
- Shows guessed letters
- Clear console display
- Win rate statistics

## Requirements

- Python 3.x (standard library only)
- No external dependencies

## Game Preview

```
==================================================
         H A N G M A N
==================================================

  Category: Animals

    ┌─────┐
    │     │
    │     O
    │    /│\
    │    /
    │
    ═══════

  Word: _ _ _ _ _ _ _ _ _ _

  Guessed letters: A E I

  Remaining attempts: 2

  Wins: 5  |  Losses: 2
```

## Game Rules

| Wrong Guesses | Result |
|---------------|--------|
| 0 | Start |
| 1-5 | Still playing |
| 6 | Game Over |

## Code Structure

- `HANGMAN_STAGES` - ASCII art for each stage
- `WORD_CATEGORIES` - Dictionary of words by category
- `choose_category()` - Display category menu
- `select_word()` - Pick random word
- `display_game()` - Render game state
- `get_guess()` - Get valid letter input
- `check_guess()` - Verify letter in word
- `update_word_display()` - Reveal letters
