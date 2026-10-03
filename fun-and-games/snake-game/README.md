# Snake Game

A classic arcade snake game built with Python's turtle graphics module.

## How to Play

1. **Run the game:**
   ```bash
   python snake-game.py
   ```

2. **Controls:**
   - Arrow Keys (Up, Down, Left, Right) to move the snake
   - SPACE to restart after game over
   - ESC to quit

3. **Objective:**
   - Eat the red food to grow longer
   - Avoid hitting the walls or yourself
   - Each food eaten = 10 points

## Features

- Smooth snake movement with turtle graphics
- Score tracking with high score persistence
- Collision detection (walls and self)
- Snake grows when eating food
- Game over screen with restart option
- Clean, well-commented code

## Requirements

- Python 3.x (turtle module is built-in)
- No external dependencies

## Game Preview

```
+----------------------------------+
|        Score: 30 | High: 50      |
|                                  |
|     [Snake moving around]        |
|                                  |
|              (o) <- Food         |
|                                  |
+----------------------------------+
```

## Code Structure

- `setup_screen()` - Initialize game window
- `create_snake()` - Create initial snake
- `create_food()` - Spawn food at random location
- `move_snake()` - Update snake positions
- `check_collision()` - Detect wall/self collisions
- `check_food_collision()` - Detect food eating
- `grow_snake()` - Add segment when eating
- `update_score()` - Refresh score display
