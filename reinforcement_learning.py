import rlpy
import random
import numpy as np
import matplotlib.pyplot as plt
import time

def main():
    return_sarsa = rl_algorithm('SARSA', 400, 1, 0.5, 0.01)
    eps_sarsa = return_sarsa[0]
    rewards_sarsa = return_sarsa[1]
    max_reward_sarsa = return_sarsa[2]

    return_q = rl_algorithm('Qlearning', 400, 1, 0.5, 0.01)
    eps_q = return_q[0]
    rewards_q = return_q[1]
    max_reward_q = return_q[2]

    print('-/-/- SARSA -/-/-')
    print('Reward to the last episode: ',rewards_sarsa[-1])
    print('Max reward: ', max_reward_sarsa)

    print('\n\n-/-/- Q LEARNING -/-/-')
    print('Reward to the last episode: ',rewards_q[-1])
    print('Max reward: ', max_reward_q)

    plt.figure('Episodes x Rewards')
    plt.subplot(211)
    plt.title('SARSA')
    plt.plot(eps_sarsa, rewards_sarsa)
    #plt.xlabel('Episodes')
    plt.ylabel('Reward')

    plt.subplot(212)
    plt.title('Q-Learning')
    plt.plot(eps_q, rewards_q)
    plt.xlabel('Episodes')
    plt.ylabel('Reward')
    plt.show()


    #Run the algorithm of Reinforcement Learning
    #   @name - 'SARSA' / 'Qlearning' / 'MonteCarlo'
def rl_algorithm(name, episodes, gama, alpha, epsilon):
    rewards = []
    eps = list(range(0,episodes))
    board = rlpy.MapState(7, 10)
    max_reward = -10000

    for i in range(0, episodes):
        #Start point
        actual_state = board.states[3][0]
        sum_reward = 0

        while actual_state.pos != (3,7):
            actual_pos = actual_state.pos
            actual_idx_max = actual_state.max_q_val_idx()
            actual_max = actual_state.q_val[actual_idx_max]

            if(random.random() > epsilon):
                next_state = board.get_next_state(actual_pos[0], actual_pos[1])
            else:
                next_state = board.get_next_state(actual_pos[0], actual_pos[1], explore=True)

            if name == 'SARSA':
                next_idx_max = next_state.max_q_val_idx()
                next_max = next_state.q_val[next_idx_max]

            elif name == 'Qlearning':
                aux_state = board.get_next_state(actual_pos[0], actual_pos[1])
                next_idx_max = aux_state.max_q_val_idx()
                next_max = aux_state.q_val[next_idx_max]

            new_reward = actual_max + alpha*(-1 + gama*next_max - actual_max)

            sum_reward -= 1

            board.change_q_val(actual_pos, actual_idx_max , new_reward)
            actual_state = next_state

        if(sum_reward > max_reward):
            max_reward = sum_reward

        rewards.append(sum_reward)

    board.show_map()
    return [eps, rewards, max_reward]


if __name__ == '__main__':
    main()

