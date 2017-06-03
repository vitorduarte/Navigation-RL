import rlpy
import random
import numpy as np
import matplotlib.pyplot as plt

def main():
    episodes = 800
    gama = 1
    alpha = 0.8
    epsilon = 0.01
    max_reward = -10000

    rewards = []
    eps = list(range(0,episodes))
    board = rlpy.MapState(7, 10)

    for i in range(0, episodes):
        actual_state = board.states[3][0]
        sum_reward = 0
        i = 0

        while actual_state.pos != (3,7):
            actual_pos = actual_state.pos
            actual_idx_max = actual_state.max_reward_idx()
            actual_max = actual_state.rewards[actual_idx_max]

            if(random.random() > epsilon):
                next_state = board.get_next_state(actual_pos[0], actual_pos[1])
            else:
                next_state = board.get_next_state(actual_pos[0], actual_pos[1], explore=True)

            next_idx_max = next_state.max_reward_idx()
            next_max = next_state.rewards[next_idx_max]

            new_reward = actual_max + alpha*(-1 + gama*next_max - actual_max)

            sum_reward -= 1
            i+=1

            board.change_reward(actual_pos, actual_idx_max , new_reward)


            actual_state = next_state
        if(sum_reward > max_reward):
            max_reward = sum_reward
        rewards.append(sum_reward)

    print('Reward to the last episode: ',rewards[episodes-1])
    print('Max reward: ', max_reward)
    plt.plot(eps,rewards)
    plt.show()

if __name__ == '__main__':
    main()