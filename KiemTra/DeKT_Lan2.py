import copy
import math
import random
import numpy as np

X = "X"
O = "O"
EMPTY = None
user = None
ai = None
move_history = []

# Câu 1: Hiển thị bàn cờ
def display_board(board):
    board_size = len(board)
    print("\n" + "-" * (4 * board_size - 1))
    for row in board:
        print(" | ".join([cell if cell else " " for cell in row]))
        print("-" * (4 * board_size - 1))

# Câu 2: Tạo bàn cờ kích thước linh hoạt
def initial_state(n):
    return [[EMPTY for _ in range(n)] for _ in range(n)]

def player(board):
    count = sum(cell is not None for row in board for cell in row)
    return X if count % 2 == 0 else O

def actions(board):
    return {(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == EMPTY}

def result(board, action):
    current_player = player(board)
    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = current_player
    move_history.append((current_player, action))
    return new_board

def get_horizontal_winner(board):
    for row in board:
        if row[0] and all(cell == row[0] for cell in row):
            return row[0]
    return None

def get_vertical_winner(board):
    for col in range(len(board)):
        if board[0][col] and all(board[row][col] == board[0][col] for row in range(len(board))):
            return board[0][col]
    return None

def get_diagonal_winner(board):
    if board[0][0] and all(board[i][i] == board[0][0] for i in range(len(board))):
        return board[0][0]
    if board[0][len(board)-1] and all(board[i][len(board)-1-i] == board[0][len(board)-1] for i in range(len(board))):
        return board[0][len(board)-1]
    return None

def winner(board):
    return get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_winner(board)

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def play_game(board_size, two_player_mode):
    global move_history, ai
    move_history = []
    board = initial_state(board_size)
    current_player = X
    ai = O if not two_player_mode else None  # Gán máy chơi quân cờ O

    while True:
        display_board(board)
        if terminal(board):
            game_winner = winner(board)
            if game_winner:
                print(f"Game Over: {game_winner} wins!")
            else:
                print("Game Over: It's a tie!")
            break

        print(f"{current_player}'s turn.")
        if not two_player_mode and current_player == ai:
            print("Machine is thinking...")
            move = minimax(board)
        else:
            while True:
                try:
                    i = int(input("Enter row (0-based index): "))
                    j = int(input("Enter col (0-based index): "))
                    if (i, j) in actions(board):
                        move = (i, j)
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter valid integers for row and column.")

        board = result(board, move)
        current_player = O if current_player == X else X

    print("Move history:")
    for move in move_history:
        print(move)

    if input("Play again? (y/n): ").lower() == 'y':
        board_size = int(input("Enter board size: "))
        two_player_mode = input("Two-player mode? (y/n): ").lower() == 'y'
        play_game(board_size, two_player_mode)

def minimax(board):
    current_player = player(board)

    def max_value(state):
        if terminal(state):
            return utility(state)
        v = -math.inf
        for action in actions(state):
            v = max(v, min_value(result(state, action)))
        return v

    def min_value(state):
        if terminal(state):
            return utility(state)
        v = math.inf
        for action in actions(state):
            v = min(v, max_value(result(state, action)))
        return v

    best_action = None
    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action

    return best_action

if __name__ == "__main__":
    board_size = int(input("Enter board size: "))
    two_player_mode = input("Two-player mode? (y/n): ").lower() == 'y'
    play_game(board_size, two_player_mode)
