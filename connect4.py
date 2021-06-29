import pygame
import numpy as np
import os
from util import is_terminal_node, Config, Agent

pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Connect 4')

ROW_COUNT = 6
COLUMN_COUNT = 7

AGENT_TURN = 2

CELL_WIDTH = WIDTH//COLUMN_COUNT
CELL_HEIGHT = HEIGHT//(ROW_COUNT + 1)

BOARD_COLOR = (102,190,230)
BACKGROUND_COLOR = (25,27,65)
P_COLORS = [(38,88,113), (122,69,115)]
LABEL_COLOR = (255,255,255)

FPS = 60

BOARD_CELL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'board_cell.png')
)
BOARD_CELL = pygame.transform.scale(BOARD_CELL_IMAGE, (CELL_WIDTH, CELL_HEIGHT))
BOARD_CELL.fill(BOARD_COLOR, special_flags=pygame.BLEND_ADD)

def draw_window(board, cursor_pos, turn):
    '''
        Draws the background, cursor, board outline and current board.
    '''
    WIN.fill(BACKGROUND_COLOR)
    
    cursor = pygame.Surface((CELL_WIDTH,HEIGHT)) 
    cursor.set_alpha(128)
    cursor.fill(P_COLORS[turn])
    WIN.blit(cursor, (cursor_pos*CELL_WIDTH, 0))

    pygame.draw.ellipse(WIN, P_COLORS[turn], (cursor_pos*CELL_WIDTH, 0, CELL_WIDTH, CELL_HEIGHT))

    
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board[row][col] != 0:
                pygame.draw.ellipse(WIN, P_COLORS[int(board[row][col]) - 1], 
                    (col*CELL_WIDTH, row*CELL_HEIGHT + CELL_HEIGHT,CELL_WIDTH, CELL_HEIGHT))
            WIN.blit(BOARD_CELL, (CELL_WIDTH*col, CELL_HEIGHT*(row+1)))

    pygame.display.update()

def create_board():
    '''
        Creates a 2d array containing zeros
    '''
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    '''
        Drops a specified piece to a specified position on the board
    '''
    board[row][col] = piece

def is_valid_location(board, col):
    '''
        Checks if a column is valid
    '''
    return board[0][col] == 0

def get_next_open_row(board, col):
    '''
        Gets the next open position of a column 
    '''
    res = 0
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            res = r
    return res

def main():
    cursor_pos = 0
    turn = 0
    clock = pygame.time.Clock()
    board = create_board()
    config = Config(ROW_COUNT, COLUMN_COUNT, 4)
    font = pygame.font.SysFont('monospace', 50)
    game_over = False
    quit = False
    if AGENT_TURN != 0:
        ai = Agent(AGENT_TURN, config)
    while not game_over:
        clock.tick(FPS)
        if AGENT_TURN == turn + 1:
            action = ai.chose_action(board)
            row = get_next_open_row(board, action)
            drop_piece(board, row, action, turn+1)
            if is_terminal_node(board, config):
                game_over = True
            else:
                turn += 1
                turn = turn % 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                quit = True
            elif event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_a]:
                    if cursor_pos > 0:
                        cursor_pos -= 1
                if keys_pressed[pygame.K_d]:
                    if cursor_pos < COLUMN_COUNT - 1:
                        cursor_pos += 1
                if keys_pressed[pygame.K_SPACE]:
                    if is_valid_location(board, cursor_pos):
                        row = get_next_open_row(board, cursor_pos)
                        drop_piece(board, row, cursor_pos, turn+1)
                        if is_terminal_node(board, config):
                            game_over = True
                        else:
                            turn += 1
                            turn = turn % 2
            elif event.type == pygame.MOUSEMOTION:
                mouse_position = pygame.mouse.get_pos()
                cursor_pos = mouse_position[0]//CELL_WIDTH
            elif event.type == pygame.MOUSEBUTTONUP:
                if is_valid_location(board, cursor_pos):
                    row = get_next_open_row(board, cursor_pos)
                    drop_piece(board, row, cursor_pos, turn+1)
                    if is_terminal_node(board, config):
                        game_over = True
                    else:
                        turn += 1
                        turn = turn % 2
        draw_window(board, cursor_pos, turn)
    while game_over and not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                quit = True
        label = font.render('Player ' + str(turn + 1) + ' wins!!', 1, BOARD_COLOR)
        label_size = label.get_size()
        pygame.draw.rect(WIN, P_COLORS[turn], (
            0, 0,
            WIDTH, label_size[1] + 40
        ))
        WIN.blit(label, (WIDTH//2-label_size[0]//2, 20))
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()