import numpy as np
import random
import sys

class State(object):
    """Class State
            @pos - postition off state in 2D
            @rewards - rewards for 4 possible movements
                        [0] - Up
                        [1] - Right
                        [2] - Down
                        [3] - Left """
    def __init__(self, reward=-1, pos=(0,0)):
        self.pos = pos
        #self.q_val = q_val
        self.rewards = np.empty((1,4))
        self.rewards.fill(reward)
        self.rewards = self.rewards.reshape(4)

    """@direction - string that describes what position reward change
            'u' or 0 - Up
            'r' or 1 - Right
            'd' or 2 - Down
            'l' or 3 - Left """
    def change_reward(self, direction, new_reward):
        if (direction == 'u') or (direction == 0):
            self.rewards[0] = new_reward
        elif (direction == 'r') or (direction == 1):
            self.rewards[1] = new_reward
        elif (direction == 'd') or (direction == 2):
            self.rewards[2] = new_reward
        elif (direction == 'l') or (direction == 3):
            self.rewards[3] = new_reward
        else:
            print('INVALID DIRECTION')

    def max_reward_idx(self):
        return self.rewards.argmax()

class MapState(object):
    """docstring for Map"""
    def __init__(self, heigth, width, reward=-1):
        self.states = np.empty((heigth, width), dtype=object)
        self.rewards = np.empty((heigth, width), dtype=object)


        for i in range (0, heigth):
            for j in range (0, width):
                self.states[i][j] = State(reward, (i,j))
                self.rewards[i][j] = self.states[i][j].rewards


    def change_reward(self, pos, direction, new_reward):
        self.states[pos[0], pos[1]].change_reward(direction, new_reward)
        self.rewards[pos[0], pos[1]] = self.states[pos[0], pos[1]].rewards

    def get_next_state(self, row, col, wind=True, explore=False):
        max_row = self.states.shape[0]
        max_col = self.states.shape[1]

        if (max_row > row) and (max_col > col):
            actual_state = self.states[row, col]

            if explore ==True:
                dir_mov = random.randint(0, 3)
            else:
                dir_mov = self.get_mov_dir(row, col)

            if wind==True:
                wind_mvmt = generate_wind(row,col)
            else:
                wind_mvmt = 0

            #Up
            if dir_mov == 0:
                movement_row = wind_mvmt-1
                movement_col = 0
            #Right
            elif dir_mov  == 1:
                movement_row = wind_mvmt
                movement_col = 1

            #Down
            elif dir_mov  == 2:
                movement_row = wind_mvmt+1
                movement_col = 0

            #Left
            elif dir_mov == 3:
                movement_row = wind_mvmt
                movement_col = -1

            else:
                print("ERROR!")

            new_row = row + movement_row
            new_col = col + movement_col

            if new_row >= max_row:
                new_row = max_row-1

            if new_row < 0:
                new_row = 0

            if new_col >= max_col:
                new_col = max_col-1

            if new_col < 0:
                new_col = 0

            next_state = self.states[new_row, new_col]

        else:
            next_state = -1

        return next_state

    def get_mov_dir(self, row, col):
        max_row = self.states.shape[0]
        max_col = self.states.shape[1]

        state = self.states[row, col]
        mov_dir = state.max_reward_idx()

        if mov_dir == 2 and (row+1 >= max_row):
            mov_dir = 0
        if mov_dir == 0 and (row-1 < 0):
            mov_dir = 0
        if mov_dir == 1 and (col+1 >= max_col):
            mov_dir = 0
        if mov_dir == 3 and (col-1 < 0):
            mov_dir = 0

        return mov_dir

def generate_wind(row,col):
    if (2 < col < 6) or col == 8:
            wind_mvmt = -1
    elif 5 < col < 8:
            wind_mvmt = -2
    else:
        wind_mvmt = 0

    return wind_mvmt

