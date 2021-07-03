import pygame
from util import RewardConfig, is_valid_location

class UserIO:
    def __init__(self, env, reward_cfg=None, color=(38,88,113)) -> None:
        self.env = env
        self.color = color
        self.cursor_pos = 0
        self.reward_cfg = RewardConfig(0,0,0,0,0,0) if reward_cfg == None else reward_cfg
        

    def handle_quit_and_reset(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.env.done = True
                self.env.quit = True
            elif event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_r]:
                    self.env.done = True
                    self.env.winner = None

    def choose_action(self, board):
        action = -1

        while action < 0 and not self.env.done:
            self.env.render(self.cursor_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.env.done = True
                    self.env.quit = True
                    self.env.winner = None
                elif event.type == pygame.KEYDOWN:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_a]:
                        if self.cursor_pos > 0:
                            self.cursor_pos -= 1
                    if keys_pressed[pygame.K_d]:
                        if self.cursor_pos < self.env.config.columns - 1:
                            self.cursor_pos += 1
                    if keys_pressed[pygame.K_SPACE]:
                        if is_valid_location(board, self.cursor_pos):
                            action = self.cursor_pos
                    if keys_pressed[pygame.K_r]:
                        self.env.done = True
                        self.env.winner = None
                elif event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()
                    self.cursor_pos = mouse_position[0]//self.env.cell_width
                elif event.type == pygame.MOUSEBUTTONUP:
                    if is_valid_location(board, self.cursor_pos):
                        action = self.cursor_pos
        return action