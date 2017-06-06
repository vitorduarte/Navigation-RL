import numpy as np
import random
import sys

class State(object):
    """Class State
            @pos - postition off state in 2D
            @q_val - rewards for 4 possible movements
                        [0] - Up
                        [1] - Right
                        [2] - Down
                        [3] - Left """
    def __init__(self, reward=-1, pos=(0,0)):
        self.pos = pos
        self.reward = reward
        self.q_val = np.empty((1,4))
        self.q_val.fill(reward)
        self.q_val = self.q_val.reshape(4)

    """@direction - string that describes what position reward change
            'u' or 0 - Up
            'r' or 1 - Right
            'd' or 2 - Down
            'l' or 3 - Left """
    def change_q_val(self, direction, new_reward):
        if (direction == 'u') or (direction == 0):
            self.q_val[0] = new_reward
        elif (direction == 'r') or (direction == 1):
            self.q_val[1] = new_reward
        elif (direction == 'd') or (direction == 2):
            self.q_val[2] = new_reward
        elif (direction == 'l') or (direction == 3):
            self.q_val[3] = new_reward
        else:
            print('INVALID DIRECTION')

    def max_q_val_idx(self):
        return self.q_val.argmax()

class MapState(object):
    """Class MapState
            @height - heigth of state matrix
            @width - width of state matrix
            @reward - rewards that initialize this map state """
    def __init__(self, heigth, width, reward=-1):
        self.states = np.empty((heigth, width), dtype=object)
        self.q_val = np.empty((heigth, width), dtype=object)
        self.rewards = np.empty((heigth, width), dtype=np.int16)



        for i in range (0, heigth):
            for j in range (0, width):
                self.states[i][j] = State(reward, (i,j))
                self.q_val[i][j] = self.states[i][j].q_val
                self.rewards[i][j] = self.states[i][j].reward


    def change_q_val(self, pos, direction, new_reward):
        """Change q_val of a state in specific position to a specific direction of movement
            @pos - position of state
            @direction - direction of vector |0-Up|1-Right|2-Down|3-Left|
            @new_reward - new value of reward"""
        self.states[pos[0], pos[1]].change_q_val(direction, new_reward)
        self.q_val[pos[0], pos[1]] = self.states[pos[0], pos[1]].q_val


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

    def print_map(self):
        max_row = self.states.shape[0]
        max_col = self.states.shape[1]
        print('\n')
        for row in range(0, max_row):
            text_row=''
            for col in range(0, max_col):
                dir_mov = self.get_mov_dir(row, col)
                #print('(',row,', ', col, ') - ', dir_mov)
                if dir_mov == 0:
                    text_row += 'UP\t'
                elif dir_mov == 1:
                    text_row += 'RIGHT\t'
                elif dir_mov == 2:
                    text_row += 'DOWN\t'
                else:
                    text_row += 'LEFT\t'
            print(text_row)
            print('\n')

    def show_map(self, start_position, end_position):
        positions = []
        actual_state = self.states[start_position[0]][start_position[1]]

        while True:
            actual_pos = actual_state.pos
            next_state = self.get_next_state(actual_pos[0], actual_pos[1])
            positions.append(actual_pos)
            if actual_pos == end_position:
                break
            actual_state = next_state

        positions.append(actual_pos)
        return positions

    def get_mov_dir(self, row, col):
        max_row = self.states.shape[0]
        max_col = self.states.shape[1]

        state = self.states[row, col]
        mov_dir = state.max_q_val_idx()

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

