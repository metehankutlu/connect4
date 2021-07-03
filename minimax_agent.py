import numpy as np
import random

from util import drop_piece, is_terminal_node, get_reward, is_valid_location

class MinimaxAgent:
    def __init__(self, mark, config, reward_cfg, color, n_steps=3):
        self.config = config
        self.reward_cfg = reward_cfg
        self.mark = mark
        self.n_steps = n_steps
        self.color = color

    def score_move(self, grid, mark, col):
        '''
            Uses minimax to calculate value of dropping piece in selected column
        '''
        next_grid = drop_piece(grid, col, mark, self.config)
        alpha = -np.Inf
        beta = np.Inf
        score = self.minimax(next_grid, self.n_steps-1, False, mark, alpha, beta)
        return score

    def minimax(self, node, depth, maximizingPlayer, mark, alpha, beta):
        '''
            Minimax implementation
        '''
        is_terminal = is_terminal_node(node, self.config)
        if depth == 0 or is_terminal:
            return get_reward(node, mark, self.config, self.reward_cfg)
        valid_moves = [c for c in range(self.config.columns) if is_valid_location(node, c)]
        if maximizingPlayer:
            value = -np.Inf
            for col in valid_moves:
                child = drop_piece(node, col, mark, self.config)
                value = max(value, self.minimax(child, depth-1, False, mark, alpha, beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = np.Inf
            for col in valid_moves:
                child = drop_piece(node, col, mark%2+1, self.config)
                value = min(value, self.minimax(child, depth-1, True, mark, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def choose_action(self, board):
        '''
            Finds the best action based on the position
        '''
        valid_moves = [col for col in range(self.config.columns) if is_valid_location(board, col)]
        # Use the heuristic to assign a score to each possible board in the next step
        scores = dict(zip(valid_moves, [self.score_move(board, self.mark, col) for col in valid_moves]))
        # Get a list of columns (moves) that maximize the heuristic
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        # Select at random from the maximizing columns
        return random.choice(max_cols)