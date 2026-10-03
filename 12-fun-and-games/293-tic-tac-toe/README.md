# Tic-Tac-Toe

Play against an unbeatable AI opponent using the Minimax algorithm with alpha-beta pruning!

## How to Play

1. **Run the game:**
   ```bash
   python tic-tac-toe.py
   ```

2. **Gameplay:**
   - You are X, the computer is O
   - Take turns placing marks on the 3x3 grid
   - Use positions 1-9 to indicate where to place your mark
   - First to get 3 in a row (horizontal, vertical, or diagonal) wins

3. **Tip:** The AI is unbeatable! Your best outcome is a draw.

## Features

- **Minimax Algorithm** - The AI plays perfectly using game theory
- **Alpha-Beta Pruning** - Optimized decision tree search
- **Random First Turn** - Game varies each time you play
- **Statistics Tracking** - Tracks wins, losses, and draws
- **Visual Board** - Clean ASCII art board with position numbers

## Game Preview

```
==================================================
       TIC-TAC-TOE vs UNBEATABLE AI
==================================================

  You are X | Computer is O
  Use positions 1-9 to place your mark

  ┌───────┬───────┬───────┐
  │   X   │   2   │   O   │
  ├───────┼───────┼───────┤
  │   4   │   X   │   6   │
  ├───────┼───────┼───────┤
  │   O   │   8   │   9   │
  └───────┴───────┴───────┘

  YOUR TURN
  Enter position (1-9): _
```

## The Minimax Algorithm

The AI uses the **Minimax** algorithm to make optimal decisions:

1. **Simulate all possible moves** to the end of the game
2. **Score each outcome**: Win = +10, Lose = -10, Draw = 0
3. **Minimize losses** on the player's turn
4. **Maximize wins** on the AI's turn
5. **Choose the move** with the best guaranteed outcome

### Alpha-Beta Pruning

Alpha-beta pruning optimizes minimax by:
- Tracking `alpha` (best score for maximizing player)
- Tracking `beta` (best score for minimizing player)
- **Pruning** branches that can't affect the outcome

This makes the AI think faster without affecting its correctness.

## Requirements

- Python 3.x (standard library only)
- No external dependencies

## Can You Beat the AI?

The AI is mathematically unbeatable because:
- Tic-Tac-Toe has a finite game tree
- With perfect play, the game is always a draw
- The AI never makes mistakes

Your goal: **Don't lose!**
