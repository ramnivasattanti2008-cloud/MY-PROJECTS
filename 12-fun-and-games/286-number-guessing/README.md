# Number Guessing Game - Computer Edition

A twist on the classic guessing game where YOU think of a number and the computer tries to guess it!

## How to Play

1. **Run the game:**
   ```bash
   python number-guessing.py
   ```

2. **Think of a number** between 1 and 100 (don't tell the computer!)

3. **Answer the computer's guesses:**
   - `H` or `HIGHER` - Your number is greater than the guess
   - `L` or `LOWER` - Your number is less than the guess
   - `C` or `CORRECT` - The computer got it!

4. **Watch the computer** intelligently narrow down the possibilities using binary search!

## Features

- **Binary Search Algorithm** - The computer uses optimal strategy to find your number
- **Real-time progress tracking** - Shows remaining range and eliminated possibilities
- **Guess history** - Visual display of all previous guesses with arrows
- **Performance rating** - Rates the computer's efficiency
- **Session statistics** - Tracks games played and average guesses

## Why Binary Search?

Binary search is one of the most efficient search algorithms. For a range of 1-100:

| Guesses Needed | Range Size |
|----------------|------------|
| 1 | 100 |
| 2 | 50 |
| 3 | 25 |
| 4 | 13 |
| 5 | 7 |
| 6 | 4 |
| 7 | 2 |

The computer will **always** find any number in 7 guesses or fewer!

## Game Preview

```
============================================================
        🎯 NUMBER GUESSING - COMPUTER EDITION 🎯
============================================================

  THINK OF A NUMBER BETWEEN 1 AND 100
  I (the computer) will try to guess it!

  Attempt #3
  ══════════════════════

  🤔 My guess: 63 🤔

  Range: 51 - 75 (25 possibilities)
  Eliminated: 75.0% of possibilities

  📝 Guess History:
     88↓ 56↑ 63

  🤔 Is your number HIGHER, LOWER, or CORRECT?
     My guess: 63

  Your answer (H/L/C): _
```

## Requirements

- Python 3.x (standard library only)
- No external dependencies

## Algorithm

The computer uses the **binary search** algorithm:

1. Start with the full range (1-100)
2. Guess the middle of the range
3. If wrong, eliminate half the remaining numbers
4. Repeat until correct

This guarantees the computer will find any number in log₂(n) guesses.
