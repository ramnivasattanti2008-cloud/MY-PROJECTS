"""
Tic-Tac-Toe - Play against an AI opponent with Minimax algorithm
The AI is unbeatable! Can you manage a draw?
"""

import os
import random

# Game symbols
PLAYER = 'X'
AI = 'O'
EMPTY = ' '

# Winning combinations (rows, columns, diagonals)
WIN_COMBINATIONS = [
    [0, 1, 2],  # Top row
    [3, 4, 5],  # Middle row
    [6, 7, 8],  # Bottom row
    [0, 3, 6],  # Left column
    [1, 4, 7],  # Middle column
    [2, 5, 8],  # Right column
    [0, 4, 8],  # Diagonal top-left to bottom-right
    [2, 4, 6],  # Diagonal top-right to bottom-left
]


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Display game header"""
    print("=" * 50)
    print("       TIC-TAC-TOE vs UNBEATABLE AI")
    print("=" * 50)


def create_board():
    """Create an empty game board"""
    return [EMPTY] * 9


def print_board(board):
    """Display the game board with numbers for positions"""
    clear_screen()
    print_header()

    # Instructions
    print("\n  You are X | Computer is O")
    print("  Use positions 1-9 to place your mark\n")

    # Board display
    print("  ┌───────┬───────┬───────┐")
    for row in range(3):
        cells = []
        for col in range(3):
            index = row * 3 + col
            cell = board[index]
            # Show position numbers for empty cells
            display = cell if cell != EMPTY else str(index + 1)
            cells.append(f" {display} ")
        print(f"  │{cells[0]}│{cells[1]}│{cells[2]}│")
        if row < 2:
            print("  ├───────┼───────┼───────┤")
    print("  └───────┴───────┴───────┘")
    print()


def check_winner(board, player):
    """Check if the given player has won"""
    for combo in WIN_COMBINATIONS:
        if all(board[i] == player for i in combo):
            return True
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)"""
    return EMPTY not in board


def get_empty_cells(board):
    """Get list of empty cell positions"""
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def minimax(board, is_maximizing, alpha, beta):
    """
    Minimax algorithm with alpha-beta pruning for optimal AI moves.
    This makes the AI unbeatable!

    Args:
        board: Current game board state
        is_maximizing: True if AI's turn (trying to maximize score)
        alpha: Best score AI can guarantee
        beta: Best score opponent can guarantee

    Returns:
        Score of the board position
    """
    # Base cases - check for terminal states
    if check_winner(board, AI):
        return 10  # AI wins (good for AI)
    if check_winner(board, PLAYER):
        return -10  # Player wins (bad for AI)
    if is_board_full(board):
        return 0  # Draw

    empty_cells = get_empty_cells(board)

    if is_maximizing:
        # AI's turn - try to maximize score
        best_score = float('-inf')
        for cell in empty_cells:
            board[cell] = AI
            score = minimax(board, False, alpha, beta)
            board[cell] = EMPTY
            best_score = max(score, best_score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Beta cutoff
        return best_score
    else:
        # Player's turn - try to minimize score
        best_score = float('inf')
        for cell in empty_cells:
            board[cell] = PLAYER
            score = minimax(board, True, alpha, beta)
            board[cell] = EMPTY
            best_score = min(score, best_score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cutoff
        return best_score


def get_ai_move(board):
    """
    Get the best move for the AI using Minimax algorithm.
    This ensures the AI plays optimally.
    """
    best_score = float('-inf')
    best_move = None

    for cell in get_empty_cells(board):
        board[cell] = AI
        score = minimax(board, False, float('-inf'), float('inf'))
        board[cell] = EMPTY

        if score > best_score:
            best_score = score
            best_move = cell

    return best_move


def get_player_move(board):
    """Get and validate player's move"""
    while True:
        try:
            move = input("  Enter position (1-9): ").strip()
            position = int(move) - 1

            if position < 0 or position > 8:
                print("  Please enter a number between 1 and 9.")
                continue

            if board[position] != EMPTY:
                print("  That position is already taken!")
                continue

            return position
        except ValueError:
            print("  Please enter a valid number (1-9).")


def announce_result(board):
    """Announce the game result"""
    if check_winner(board, PLAYER):
        print("  🎉 YOU WIN! Congratulations!")
        return 'PLAYER'
    elif check_winner(board, AI):
        print("  🤖 AI WINS! The AI is unbeatable!")
        return 'AI'
    else:
        print("  🤝 IT'S A DRAW! Well played!")
        return 'DRAW'


def print_stats(wins, losses, draws):
    """Display game statistics"""
    total = wins + losses + draws
    if total > 0:
        print(f"\n  📊 Statistics:")
        print(f"     Wins: {wins} | Losses: {losses} | Draws: {draws}")
        if draws > 0:
            print(f"     (You won {wins} out of {total} games)")
    print()


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


def main():
    """Main game loop"""
    wins = 0
    losses = 0
    draws = 0

    while True:
        board = create_board()
        game_over = False
        player_turn = random.choice([True, False])  # Random first turn

        if player_turn:
            print("\n  🎲 You go first!")
        else:
            print("\n  🤖 AI goes first!")

        input("\n  Press ENTER to start...")
        print_board(board)

        # Main game loop
        while not game_over:
            if player_turn:
                # Player's turn
                print("  YOUR TURN")
                move = get_player_move(board)
                board[move] = PLAYER
            else:
                # AI's turn
                print("  AI is thinking...")
                import time
                time.sleep(0.5)  # Small delay for dramatic effect
                move = get_ai_move(board)
                board[move] = AI

            print_board(board)

            # Check for game end
            if check_winner(board, PLAYER) or check_winner(board, AI) or is_board_full(board):
                result = announce_result(board)
                if result == 'PLAYER':
                    wins += 1
                elif result == 'AI':
                    losses += 1
                else:
                    draws += 1
                print_stats(wins, losses, draws)
                game_over = True
            else:
                # Switch turns
                player_turn = not player_turn

        if not play_again():
            break

    # Final goodbye
    clear_screen()
    print_header()
    print("\n  Thanks for playing!")
    print_stats(wins, losses, draws)
    print("  See you next time! 👋")
    print("=" * 50)


if __name__ == "__main__":
    print("\n  Welcome to Tic-Tac-Toe!")
    print("  Can you beat the unbeatable AI? (Spoiler: You can't!)")
    print("  Try to get a draw at least!")
    input("\n  Press ENTER to start...")
    main()
