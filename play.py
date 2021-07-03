import time
import pygame
from connect4 import Connect4Env
from minimax_agent import MinimaxAgent
from user_io import UserIO
from util import Config, RewardConfig

def main():
    config = Config(6, 7)
    reward_cfg = RewardConfig(1, 1e2, 1e6, -10, -1e3, -1e11)
    p1_color = (38,88,113)
    p2_color = (122,69,115)

    env = Connect4Env(config)
    user_io = UserIO(env)

    p1 = MinimaxAgent(1, config, reward_cfg, p1_color)
    # p1 = user_io
    p2 = MinimaxAgent(2, config, reward_cfg, p2_color)

    env.set_players(p1, p2)

    while not env.quit:

        if env.winner == None:
            state = env.reset()

        while not env.done:
            current_player = env.get_current_player()
            action = current_player.choose_action(state)
            state_, reward = env.step(action)
            state = state_
            user_io.handle_quit_and_reset()
            env.render()

        if env.winner != None:
            env.show_result()
            user_io.handle_quit_and_reset()

    pygame.quit()

if __name__ == '__main__':
    main()