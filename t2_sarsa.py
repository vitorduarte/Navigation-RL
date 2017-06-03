import rlpy
import random
import numpy as np
import matplotlib.pyplot as plt

def main():
    episodes = 8000
    gama = 1
    alpha = 0.01
    epsilon = 0.01

    rewards = []
    eps = list(range(0,episodes))
    board = rlpy.MapState(7, 10)
    print(board.q_val)
    for i in range(0, episodes):
        actual_state = board.states[3][0]
        sum_reward = 0
        i = 0

        while actual_state.pos != (3,7):
            actual_pos = actual_state.pos

            if(random.random() > epsilon):
                next_state = board.get_next_state(actual_pos[0], actual_pos[1])
            else:
                next_state = board.get_next_state(actual_pos[0], actual_pos[1], explore=True)

            new_q = actual_state.q_val + alpha*(next_state.reward + gama*next_state.q_val - actual_state.q_val)
            sum_reward += next_state.reward
            i+=1
            board.change_q(actual_state.pos, new_q)

            #print(board.q_val)
            if i==10000000:
                break
            actual_state = next_state

        rewards.append(sum_reward)
    print(board.q_val)
    print(rewards[episodes-1])
    plt.plot(eps,rewards)
    plt.show()

def init_q_states(heigth, width):
    states_map = np.empty((heigth, width), dtype=object)
    q_val = np.empty((heigth, width), dtype=np.uint8)
    for i in range (0, heigth):
        for j in range (0, width):
            states_map[i][j] = rlpy.State(-1, (i,j), random.randint(0,3))

    for i in range (0, heigth):
        for j in range (0, width):
            q_val[i][j] = states_map[i][j].q_val

    print(q_val)
if __name__ == '__main__':
    main()