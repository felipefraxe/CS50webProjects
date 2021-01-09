"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None


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
    i = 0
    for row in board:
        for cell in row:
            if cell != EMPTY:
                i += 1
    if i % 2 == 0:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = deepcopy(board)
    if result[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid action")

    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2]) and (board[i][0] != EMPTY):
            return board[i][0]

        if (board[0][i] == board[1][i] == board[2][i]) and (board[0][i] != EMPTY):
            return board[0][i]

    if (board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]) and board[1][1] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        score = -math.inf
        optimal = None

        for action in actions(board):
            minval = min_value(result(board, action))

            if minval > score:
                score = minval
                optimal = action

        return optimal

    elif player(board) == O:
        score = math.inf
        optimal = None

        for action in actions(board):
            maxval = max_value(result(board, action))

            if maxval < score:
                score = maxval
                optimal = action

        return optimal