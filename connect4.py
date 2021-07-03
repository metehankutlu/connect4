import pygame
import numpy as np
import os
from util import is_terminal_node, get_reward, drop_piece

class Connect4Env():
    def __init__(self, config, width=700, height=700):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.config = config
        self.cell_width = self.width//self.config.columns
        self.cell_height = self.height//(self.config.rows + 1)

        self.board_color = (102, 190, 230)
        self.bg_color = (25,27,65)

        self.fps = 60

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Connect 4')

        self.board_cell_image = pygame.image.load(
            os.path.join('Assets', 'board_cell.png')
        )
        self.board_cell = pygame.transform.scale(
            self.board_cell_image, 
            (self.cell_width, self.cell_height)
        )
        self.board_cell.fill(self.board_color, special_flags=pygame.BLEND_ADD)
        self.quit = False
        self.done = False
        self.winner = None

    def set_players(self, p1, p2):
        self.players = (p1, p2)

    def get_current_player(self):
        return self.players[self.turn]

    def render(self, cursor_pos=None):
        self.clock.tick(self.fps)
        self.window.fill(self.bg_color)

        if cursor_pos != None:
            cursor = pygame.Surface((self.cell_width, self.height)) 
            cursor.set_alpha(128)
            current_player = self.get_current_player()
            cursor.fill(current_player.color)
            cursor_x = cursor_pos*self.cell_width
            self.window.blit(cursor, (cursor_x, 0))

            pygame.draw.ellipse(
                self.window, 
                current_player.color, 
                (cursor_x, 0, self.cell_width, self.cell_height)
            )

        for row in range(self.config.rows):
            for col in range(self.config.columns):
                if self.board[row][col] != 0:
                    cell_x = col*self.cell_width
                    cell_y = row*self.cell_height + self.cell_height
                    pygame.draw.ellipse(
                        self.window, 
                        self.players[int(self.board[row][col]) - 1].color, 
                        (cell_x, cell_y,self.cell_width, self.cell_height)
                    )
                self.window.blit(
                    self.board_cell, 
                    (self.cell_width*col, self.cell_height*(row+1))
                )

        pygame.display.update()

    def show_result(self):
        self.clock.tick(self.fps)
        if self.winner != None:
            font = pygame.font.SysFont('monospace', 50)

            label = font.render('Player ' + str(self.winner + 1) + ' wins!!', 1, (255,255,255))
            label_size = label.get_size()
            pygame.draw.rect(self.window, self.players[self.winner].color, (
                0, 0,
                self.width, label_size[1] + 40
            ))
            self.window.blit(label, (self.width//2-label_size[0]//2, 20))
            pygame.display.update()

    def step(self, col):

        self.board = drop_piece(self.board, col, self.turn+1, self.config)

        if is_terminal_node(self.board, self.config):
            self.done = True
            self.winner = self.turn

        reward = get_reward(
            self.board, 
            self.turn+1, 
            self.config, 
            self.players[self.turn].reward_cfg
        )

        self.turn += 1
        self.turn = self.turn % 2

        return self.board, reward

    def reset(self):
        self.board = np.zeros((self.config.rows, self.config.columns))
        self.turn = 0
        self.done = False
        self.winner = None
        return self.board