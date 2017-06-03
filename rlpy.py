import numpy as np
import random
import sys

class State(object):
    """docstring for State"""
    def __init__(self, reward, pos=(0,0), q_val=0):
        self.pos = pos
        self.q_val = q_val
        self.reward = reward

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
        max_q = 1-sys.maxsize
        max_row = self.states.shape[0]
        max_col = self.states.shape[1]

        actual_state = self.states[row, col]

        if row+1 < max_row:
            side_q = self.states[row+1, col].q_val
            if side_q > max_q:
                max_q = side_q
                mov_dir = 2 #Down

        if row-1 >= 0:
            side_q = self.states[row-1, col].q_val
            if side_q > max_q:
                max_q = side_q
                mov_dir = 0 #Up

        if col+1 < max_col:
            side_q = self.states[row, col+1].q_val
            if side_q > max_q:
                max_q = side_q
                mov_dir = 1 #Right

        if col-1 >= 0:
            side_q = self.states[row, col-1].q_val
            if side_q > max_q:
                max_q = side_q
                mov_dir = 3 #Left

        return mov_dir

def generate_wind(row,col):
    if (2 < col < 6) or col == 8:
            wind_mvmt = -1
    elif 5 < col < 8:
            wind_mvmt = -2
    else:
        wind_mvmt = 0

    return wind_mvmt

