import numpy as np
import random

class State(object):
    """docstring for State"""
    def __init__(self, reward, pos=(0,0), q_val=0):
        self.pos = pos
        self.q_val = q_val
        self.reward = reward

    def change_q(self, new_q):
        self.q_val = new_q

class MapState(object):
    """docstring for Map"""
    def __init__(self, heigth, width, reward=-1, min_q=0, max_q=3):
        self.states = np.empty((heigth, width), dtype=object)
        self.rewards = np.empty((heigth, width), dtype=np.int16)
        self.q_val = np.empty((heigth, width), dtype=np.uint8)

        for i in range (0, heigth):
            for j in range (0, width):
                self.states[i][j] = State(reward,
                                            (i,j),
                                            random.randint(min_q, max_q))
                self.rewards[i][j] = self.states[i][j].reward
                self.q_val[i][j] = self.states[i][j].q_val

    def change_q(self, pos, new_value):
        self.q_val[pos[0], pos[1]] = new_value
        self.states[pos[0], pos[1]].q_val = new_value

    def get_next_state(self, row, col):
        max_row = self.states.shape[0]
        max_col = self.states.shape[1]


        if (max_row > row) and (max_col > col):
            actual_state = self.states[row, col]
            q = round(actual_state.q_val)

            #Up
            if q == 0:
                if row != 0:
                    next_state = self.states[row-1, col]
                else:
                    next_state = actual_state
            #Right
            elif q == 1:
                if col != (max_col-1):
                    next_state = self.states[row, col+1]
                else:
                    next_state = actual_state
            #Left
            elif q == 2:
                if col != 0:
                    next_state = self.states[row, col-1]
                else:
                    next_state = actual_state

            #Down
            elif q == 3:
                if row != (max_row-1):
                    next_state = self.states[row+1, col]
                else:
                    next_state = actual_state

            else:
                print("DIMENSION ERROR!")

        else:
            next_state = -1

        return next_state