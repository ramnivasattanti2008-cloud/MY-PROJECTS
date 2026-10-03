# Rock Paper Scissors

The classic game with an epic twist! Challenge the computer in best-of-N rounds with ASCII art, win streaks, and bragging rights.

## Features

- **ASCII Art Choices** - Visual rock, paper, and scissors
- **Best of N Rounds** - Choose your match length (3, 5, 7, or custom)
- **Win Streak Tracker** - Track consecutive wins
- **Best Streak Records** - Remember your best performance
- **Animated Battles** - Countdown and dramatic reveals
- **Scoreboard** - Live progress visualization
- **Best Streak Badges** - Fire emoji at 3+ streak!

## Installation

```bash
# Install colorama for colored output
pip install colorama

# Run the game
python rock-paper-scissors.py
```

## Usage

```bash
python rock-paper-scissors.py
```

### Game Rules

```
✊ ROCK beats ✌️ SCISSORS
✋ PAPER beats ✊ ROCK  
✌️ SCISSORS beats ✋ PAPER
```

### Match Options

1. **Quick Match** - Best of 3 rounds
2. **Standard Match** - Best of 5 rounds
3. **Epic Battle** - Best of 7 rounds
4. **Custom** - Choose any odd number (1-21)

## Sample Battle

```
    ⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️

    YOUR CHOICE:
        _______
    ---'   ____)
          (_____)
          (_____)
          (____)
    ---.__(___)

    VS

    COMPUTER'S CHOICE:
         _______
    ---'    ____)____
               ______)
              _______)
             _______)
    ---.__________)

    ⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️⚔️

    ╔═══════════════════════════════════════════════════════════╗
    ║            🏆 YOU WIN! CONGRATULATIONS! 🏆                ║
    ║                 Current Win Streak: 4 🔥                   ║
    ╚═══════════════════════════════════════════════════════════╝
```

## Menu Options

- `[1]` Choose Rock
- `[2]` Choose Paper
- `[3]` Choose Scissors
- `[R]` View Rules
- `[Q]` Quit

## Requirements

- Python 3.6+
- colorama (optional, for colored output)

## Tips

- Ties don't count - the round replays!
- Build your win streak for bragging rights
- The computer uses pure randomness - fair play!

## License

MIT License - May the best player win!
