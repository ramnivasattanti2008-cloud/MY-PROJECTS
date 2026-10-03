"""
Snake Game - Classic arcade snake game using turtle graphics
Use arrow keys to control the snake. Eat food to grow longer.
"""

import turtle
import time
import random

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20
GAME_SPEED = 0.15  # Lower = faster


def setup_screen():
    """Initialize the game window with title and settings"""
    screen = turtle.Screen()
    screen.title("Snake Game - Use Arrow Keys")
    screen.bgcolor("black")
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.tracer(0)  # Turn off animation for manual control
    return screen


def create_snake():
    """Create the initial snake as a list of turtle segments"""
    snake = []
    for i in range(3):
        segment = turtle.Turtle("square")
        segment.color("lime green")
        segment.penup()
        segment.goto(-i * CELL_SIZE, 0)
        snake.append(segment)
    return snake


def create_food():
    """Create the food item at a random position"""
    food = turtle.Turtle()
    food.shape("circle")
    food.color("red")
    food.penup()
    # Align food position to grid
    x = random.randint(-SCREEN_WIDTH//2 + CELL_SIZE, SCREEN_WIDTH//2 - CELL_SIZE)
    y = random.randint(-SCREEN_HEIGHT//2 + CELL_SIZE, SCREEN_HEIGHT//2 - CELL_SIZE)
    food.goto(x, y)
    return food


def create_score_display():
    """Create the score display at the top of the screen"""
    score_pen = turtle.Turtle()
    score_pen.color("white")
    score_pen.penup()
    score_pen.hideturtle()
    score_pen.goto(0, SCREEN_HEIGHT//2 - 40)
    score_pen.write("Score: 0  |  High Score: 0", align="center",
                    font=("Arial", 20, "bold"))
    return score_pen


def move_snake(snake):
    """Move the snake by updating segment positions"""
    # Move each segment to the position of the one before it
    for i in range(len(snake) - 1, 0, -1):
        new_x = snake[i - 1].xcor()
        new_y = snake[i - 1].ycor()
        snake[i].goto(new_x, new_y)

    # Move the head in the current direction
    snake[0].forward(CELL_SIZE)


def change_direction(new_direction):
    """Change snake direction (prevent 180-degree turns)"""
    global direction
    opposite_directions = {"up": "down", "down": "up", "left": "right", "right": "left"}
    if new_direction != opposite_directions.get(direction):
        direction = new_direction


def set_direction_press(direction_key):
    """Handle arrow key press - set direction based on key"""
    directions_map = {
        "Up": "up",
        "Down": "down",
        "Left": "left",
        "Right": "right"
    }
    new_dir = directions_map.get(direction_key)
    if new_dir:
        change_direction(new_dir)


def check_collision(snake):
    """Check if snake hit wall or itself"""
    head = snake[0]

    # Wall collision
    if (head.xcor() > SCREEN_WIDTH//2 - CELL_SIZE or
        head.xcor() < -SCREEN_WIDTH//2 + CELL_SIZE or
        head.ycor() > SCREEN_HEIGHT//2 - CELL_SIZE or
        head.ycor() < -SCREEN_HEIGHT//2 + CELL_SIZE):
        return True

    # Self collision (check if head touches any body segment)
    for segment in snake[1:]:
        if head.distance(segment) < CELL_SIZE - 5:
            return True

    return False


def check_food_collision(snake, food):
    """Check if snake head ate the food"""
    head = snake[0]
    if head.distance(food) < CELL_SIZE:
        return True
    return False


def grow_snake(snake):
    """Add a new segment to the snake"""
    new_segment = turtle.Turtle("square")
    new_segment.color("lime green")
    new_segment.penup()
    # Position behind the last segment
    new_segment.goto(snake[-1].position())
    snake.append(new_segment)


def reposition_food(food):
    """Move food to a new random location"""
    x = random.randint(-SCREEN_WIDTH//2 + CELL_SIZE, SCREEN_WIDTH//2 - CELL_SIZE)
    y = random.randint(-SCREEN_HEIGHT//2 + CELL_SIZE, SCREEN_HEIGHT//2 - CELL_SIZE)
    food.goto(x, y)


def update_score(score, high_score, score_pen):
    """Update the score display"""
    score_pen.clear()
    score_pen.write(f"Score: {score}  |  High Score: {high_score}",
                    align="center", font=("Arial", 20, "bold"))


def game_over_screen(score, high_score):
    """Display game over message"""
    game_over = turtle.Turtle()
    game_over.color("red")
    game_over.penup()
    game_over.hideturtle()
    game_over.goto(0, 50)
    game_over.write("GAME OVER!", align="center", font=("Arial", 36, "bold"))

    final_score = turtle.Turtle()
    final_score.color("white")
    final_score.penup()
    final_score.hideturtle()
    final_score.goto(0, 0)
    final_score.write(f"Your Score: {score}", align="center", font=("Arial", 24, "normal"))

    instruction = turtle.Turtle()
    instruction.color("yellow")
    instruction.penup()
    instruction.hideturtle()
    instruction.goto(0, -50)
    instruction.write("Press SPACE to play again or ESC to quit",
                      align="center", font=("Arial", 16, "normal"))

    return instruction  # Keep reference to remove later


def hide_game_elements(snake, food, score_pen):
    """Hide all game elements for cleanup"""
    for segment in snake:
        segment.hideturtle()
    food.hideturtle()
    score_pen.clear()


def reset_game(snake, food, score_pen, high_score):
    """Reset game to initial state"""
    global direction
    hide_game_elements(snake, food, score_pen)

    # Create new snake and food
    new_snake = create_snake()
    new_food = create_food()
    direction = "right"

    return new_snake, new_food


def main():
    """Main game loop"""
    global direction
    direction = "right"

    screen = setup_screen()
    score = 0
    high_score = 0

    # Create game elements
    snake = create_snake()
    food = create_food()
    score_pen = create_score_display()

    # Set up keyboard controls
    screen.listen()
    screen.onkeypress(lambda: set_direction_press("Up"), "Up")
    screen.onkeypress(lambda: set_direction_press("Down"), "Down")
    screen.onkeypress(lambda: set_direction_press("Left"), "Left")
    screen.onkeypress(lambda: set_direction_press("Right"), "Right")

    game_running = True

    try:
        while game_running:
            screen.update()
            move_snake(snake)

            # Check for food collision
            if check_food_collision(snake, food):
                score += 10
                if score > high_score:
                    high_score = score
                update_score(score, high_score, score_pen)
                grow_snake(snake)
                reposition_food(food)

            # Check for collision
            if check_collision(snake):
                game_over_turtle = game_over_screen(score, high_score)

                # Wait for restart or quit
                def restart_game():
                    nonlocal score, snake, food, direction
                    game_over_turtle.clear()
                    snake, food = reset_game(snake, food, score_pen, high_score)
                    score = 0
                    direction = "right"
                    update_score(score, high_score, score_pen)

                def quit_game():
                    nonlocal game_running
                    game_running = False

                screen.onkeypress(restart_game, "space")
                screen.onkeypress(quit_game, "Escape")

                # Wait until game is restarted or quit
                while game_running:
                    screen.update()
                    time.sleep(0.1)

            time.sleep(GAME_SPEED)

    except turtle.Terminator:
        print("Game window closed. Thanks for playing!")
    except Exception as e:
        print(f"Game error: {e}")
    finally:
        turtle.bye()


if __name__ == "__main__":
    print("=" * 50)
    print("       SNAKE GAME")
    print("=" * 50)
    print("Controls:")
    print("  Arrow Keys - Move snake")
    print("  SPACE - Restart after game over")
    print("  ESC - Quit game")
    print("=" * 50)
    print("Starting game in 3 seconds...")
    time.sleep(3)
    main()
