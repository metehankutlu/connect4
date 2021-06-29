import numpy as np
import random
from functools import partial

class Config:
    def __init__(self, rows, columns, inarow):
        self.rows = rows
        self.columns = columns
        self.inarow = inarow

class Obs:
    def __init__(self, board, mark):
        self.board = board
        self.mark = mark

class Agent:
    def __init__(self, mark, config):
        self.config = config
        self.mark = mark

    def chose_action(self, board):
        obs = Obs(board.flatten(), self.mark)
        return my_agent(obs, self.config)

N_STEPS = 3

def drop_piece(grid, col, mark, config):
    '''
        Gets board at next step if agent drops piece in selected column
    '''
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = mark
    return next_grid

def check_window(window, num_discs, piece, config):
    '''
        Helper function for get_heuristic: checks if window satisfies heuristic conditions
    '''
    return (window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs)

def count_windows(grid, num_discs, piece, config):
    '''
        Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
    '''
    num_windows = 0
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[row, col:col+config.inarow])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.inarow, col])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    return num_windows

def is_terminal_window(window, config):
    '''
        Helper function for minimax: checks if agent or opponent has four in a row in the window
    '''
    return window.count(1) == config.inarow or window.count(2) == config.inarow

def is_terminal_node(grid, config):
    '''
        Helper function for minimax: checks if game has ended
    '''
    # Check for draw 
    if list(grid[0, :]).count(0) == 0:
        return True
    # Check for win: horizontal, vertical, or diagonal
    # horizontal 
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[row, col:col+config.inarow])
            if is_terminal_window(window, config):
                return True
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.inarow, col])
            if is_terminal_window(window, config):
                return True
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if is_terminal_window(window, config):
                return True
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if is_terminal_window(window, config):
                return True
    return False

def get_heuristic(grid, mark, config):
    '''
        Helper function for score_move: calculates value of heuristic for grid
    '''
    A = 1e6
    B = 1e2
    C = 1
    D = -10
    E = -1e3
    F = -1e11
    num_twos = count_windows(grid, 2, mark, config)
    num_threes = count_windows(grid, 3, mark, config)
    num_fours = count_windows(grid, 4, mark, config)
    #num_twos_opp = count_windows(grid, 2, mark%2+1, config)
    num_threes_opp = count_windows(grid, 3, mark%2+1, config)
    num_fours_opp = count_windows(grid, 4, mark%2+1, config)
    score = A*num_fours + B*num_threes + C*num_twos + E*num_threes_opp + F*num_fours_opp
    return score


def score_move(grid, mark, config, nsteps, col):
    '''
        Uses minimax to calculate value of dropping piece in selected column
    '''
    next_grid = drop_piece(grid, col, mark, config)
    alpha = -np.Inf
    beta = np.Inf
    score = minimax(next_grid, nsteps-1, False, mark, config, alpha, beta)
    return score

def minimax(node, depth, maximizingPlayer, mark, config, alpha, beta):
    '''
        Minimax implementation
    '''
    is_terminal = is_terminal_node(node, config)
    if depth == 0 or is_terminal:
        return get_heuristic(node, mark, config)
    valid_moves = [c for c in range(config.columns) if node[0][c] == 0]
    if maximizingPlayer:
        value = -np.Inf
        for col in valid_moves:
            child = drop_piece(node, col, mark, config)
            value = max(value, minimax(child, depth-1, False, mark, config, alpha, beta))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = np.Inf
        for col in valid_moves:
            child = drop_piece(node, col, mark%2+1, config)
            value = min(value, minimax(child, depth-1, True, mark, config, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def my_agent(obs, config):
    '''
        Finds the best action based on the position
    '''
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    # Convert the board to a 2D grid
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    transform = partial(score_move, grid, obs.mark, config, N_STEPS)
    # Use the heuristic to assign a score to each possible board in the next step
    scores = dict(zip(valid_moves, [transform(col) for col in valid_moves]))
    # Get a list of columns (moves) that maximize the heuristic
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    # Select at random from the maximizing columns
    return random.choice(max_cols)