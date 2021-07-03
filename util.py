import numpy as np
import random

class Config:
    def __init__(self, rows, columns, inarow=4):
        self.rows = rows
        self.columns = columns
        self.inarow = inarow

class RewardConfig:
    def __init__(self, rew2, rew3, rew4, rew2opp, rew3opp, rew4opp):
        self.rew2 = rew2
        self.rew3 = rew3
        self.rew4 = rew4
        self.rew2opp = rew2opp
        self.rew3opp = rew3opp
        self.rew4opp = rew4opp

def get_reward(grid, mark, config, reward_cfg):
    score = 0
    if reward_cfg.rew2 != 0:
        num_twos = count_windows(grid, 2, mark, config)
        score += reward_cfg.rew2*num_twos
    if reward_cfg.rew3 != 0:
        num_threes = count_windows(grid, 3, mark, config)
        score += reward_cfg.rew3*num_threes
    if reward_cfg.rew4 != 0:
        num_fours = count_windows(grid, 4, mark, config)
        score += reward_cfg.rew4*num_fours
    if reward_cfg.rew2opp != 0:
        num_twos_opp = count_windows(grid, 2, mark%2+1, config)
        score += reward_cfg.rew2opp*num_twos_opp
    if reward_cfg.rew3opp != 0:
        num_threes_opp = count_windows(grid, 3, mark%2+1, config)
        score += reward_cfg.rew3opp*num_threes_opp
    if reward_cfg.rew4opp != 0:
        num_fours_opp = count_windows(grid, 4, mark%2+1, config)
        score += reward_cfg.rew4opp*num_fours_opp
    return score

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

def is_valid_location(board, col):
    '''
        Checks if a column is valid
    '''
    return board[0][col] == 0

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


