import copy
import math
import tkinter as tk
from tkinter import messagebox

X = "X"
O = "O"
EMPTY = None
user = None
ai = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for cell in row:
            if cell:
                count += 1
    return ai if count % 2 != 0 else user

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    curr_player = player(board)
    result_board = copy.deepcopy(board)
    (i, j) = action
    result_board[i][j] = curr_player
    return result_board

def get_horizontal_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    return None

def get_vertical_winner(board):
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    return None

def get_diagonal_winner(board):
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    return get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_winner(board)

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0

def maxValue(state, alpha, beta):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, minValue(result(state, action), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def minValue(state, alpha, beta):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, maxValue(result(state, action), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    best_action = None
    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            value = minValue(result(board, action), -math.inf, math.inf)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = maxValue(result(board, action), -math.inf, math.inf)
            if value < best_value:
                best_value = value
                best_action = action
    return best_action

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = initial_state()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self.ai_turn = False
        self.root.withdraw()  # Hide the main window
        self.choose_player()

    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                                   command=lambda i=i, j=j: self.on_click(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def choose_player(self):
        global user, ai
        self.choice_window = tk.Toplevel(self.root)
        self.choice_window.title("Choose Player")
        self.choice_window.geometry("300x200")  # Set the size of the window

        tk.Label(self.choice_window, text="Choose your player:", font=("Arial", 14)).pack(pady=20)

        tk.Button(self.choice_window, text="X", font=("Arial", 14), command=lambda: self.set_player(X)).pack(side=tk.LEFT, padx=20)
        tk.Button(self.choice_window, text="O", font=("Arial", 14), command=lambda: self.set_player(O)).pack(side=tk.RIGHT, padx=20)

        self.center_window(self.choice_window)

    def set_player(self, choice):
        global user, ai
        user = choice
        ai = O if user == X else X
        self.choice_window.destroy()
        self.choose_first_player()

    def choose_first_player(self):
        self.first_player_window = tk.Toplevel(self.root)
        self.first_player_window.title("Choose First Player")
        self.first_player_window.geometry("300x200")  # Set the size of the window

        tk.Label(self.first_player_window, text="Who goes first?", font=("Arial", 14)).pack(pady=20)

        tk.Button(self.first_player_window, text="You", font=("Arial", 14), command=lambda: self.set_first_player(user)).pack(side=tk.LEFT, padx=20)
        tk.Button(self.first_player_window, text="AI", font=("Arial", 14), command=lambda: self.set_first_player(ai)).pack(side=tk.RIGHT, padx=20)

        self.center_window(self.first_player_window)

    def set_first_player(self, first_player):
        self.first_player_window.destroy()
        if first_player == ai:
            self.ai_turn = True
            self.ai_move()
        self.root.deiconify()  # Show the main window

    def on_click(self, i, j):
        if self.board[i][j] is EMPTY and not self.ai_turn:
            self.board = result(self.board, (i, j))
            self.update_buttons()
            if terminal(self.board):
                self.end_game()
            else:
                self.ai_turn = True
                self.ai_move()

    def ai_move(self):
        move = minimax(self.board)
        self.board = result(self.board, move)
        self.update_buttons()
        if terminal(self.board):
            self.end_game()
        self.ai_turn = False

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i][j] if self.board[i][j] is not None else "")

    def end_game(self):
        self.end_game_window = tk.Toplevel(self.root)
        self.end_game_window.title("Game Over")
        self.end_game_window.geometry("300x200")  # Set the size of the window

        win = winner(self.board)
        if win:
            message = f"{win} wins!"
        else:
            message = "Draw!"

        tk.Label(self.end_game_window, text=message, font=("Arial", 14)).pack(pady=20)
        tk.Button(self.end_game_window, text="OK", font=("Arial", 14), command=self.root.quit).pack(pady=20)

        self.center_window(self.end_game_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()