import time
import pandas as pd
import numpy as np
import utils
from probability_matrix import calculate_prob_matrix
from probability_matrix import concatenate_files
from probability_matrix import calculate_starting_probability
from datetime import date
import cv2

TILE_SIZE = 32
OFS = 150
MARKET = """
#######DDDDDDDDDDDDD#
C..................D#
...................D#
C.......DDDDDDDDD..D#
...................##
#.TTTTTTTTTT..TTTT.##
#.TTTTTTTTTT..TTTT.##
#...................G
#.YYYYYSSSS..SSS....G
#.YYYYYSSSS..SSS..###
#.................###
#...................G
#.BBBBBBBBBBBBBB....G
#####################
""".strip()

class Customer:
    '''single customer that can move in the supermarket randomly
       according to a probability matrix'''
    def __init__(self, id, initial_state, prob_matrix, image):
        self.id = id
        self.state = np.random.choice(
            list(initial_state.index),
            p=initial_state)
        self.matrix = prob_matrix
        self.previous = initial_state
        self.x = 10
        self.y = 10
        self.image = image[7 * 32: 8 * 32, 2 * 32: 3 * 32]

    def __repr__(self):
        state = f'Customer {self.id} in state {self.state}. {self.x, self.y} END \n'

        return state

    def next_state(self):
        '''prob_matrix is the prbability matrix of the supermaket states
        (floats). Returns the next state of the customer according to the
        current state and the values of the prob matrix '''
        prob_line = np.array([self.matrix.loc[
            self.matrix.index.get_level_values(0) == self.state]]).reshape(-1)
        next_st = np.random.choice(
            ['checkout', 'dairy', 'drinks', 'fruit', 'spices'],
            # TODO: we could also try to get a list of column names instead.
            p=prob_line)
        self.previous = self.state
        self.state = next_st
        return next_st

    def update_position(self, state):
        if state == 'dairy':
            self.x = 6
            self.y = 13
        elif state == 'drinks':
            self.x = 2
            self.y = 17
        elif state == 'spices':
            self.x = 9
            self.y = 11
        elif state == 'fruit':
            self.x = 11
            self.y = 8
        elif state == 'checkout':
            self.x = 3
            self.y = 2

    def is_active(self):
        if (self.state == 'checkout') and (self.previous == self.state):
            return False
        else:
            return True

    def draw(self, frame):
        frame[
            self.x * 32 + OFS: (self.x + 1) * 32 + OFS,
            self.y * 32 + OFS: (self.y + 1) * 32 + OFS
        ] = self.image

    def get_current_state(self):
        return self.state

    def get_previous_state(self):
        return self.previous


class Doodlmarket:

    def __init__(self, closes_at, image):
        self.date = date.today()
        self.minute = 0
        self.customers = []
        self.opens_at = 7
        self.closes_at = closes_at
        self.unique_customers = 0
        self.probability_matrix = prob_matrix
        self.name = 'MarcoMarkt'
        self.initial_state_probability = initial_state_probability
        self.image = image

    def __repr__(self):
        return f'Welcome to {self.name}. Enjoy your shopping. \n \
        Currently there are {len(self.customers)} customers in here. \n \
        Please keep a distance of at least 1.5 meters. \n \
        Its {self.get_time()} o\'clock.'

    def get_state_of_customers(self):
        states = []
        for customer in self.customers:  # TODO: make a list comprehension
            states.append(customer.get_current_state())
        return states

    def get_time(self):
        day = self.date.strftime('%Y-%m-%d')
        hour = self.opens_at + self.minute // 60
        minute = self.minute % 60
        return f'{day} {hour:02d}:{minute:02d}:00'

    def next_minute(self):
        for customer in self.customers:
            customer.next_state()
        self.minute += 1

    def create_customers(self):
        # every minute there can enter a maximum of 5 new customers
        amount = [0, 1, 2, 3, 4]
        p = [0.3, 0.35, 0.2, 0.1, 0.05]  # this was us trying to calculate 100%
        new_customers = np.random.choice(amount, p=p)

        for customer in range(new_customers):
            self.unique_customers += 1
            self.customers.append(Customer(
                self.unique_customers,
                self.initial_state_probability,
                self.probability_matrix,
                self.image))

        return '???'

    def remove_customers(self):
        for customer in self.customers:
            if customer.state == 'checkout':
                self.customers.remove(customer)

    def record_customer_location(self):
        filepath = f'{utils.get_project_root()}/data/output/marcomarkt.csv'
        for customer in self.customers:
            with open(filepath, 'a') as f:
                f.write(f'{self.get_time()},{customer.id},{customer.state}\n')

    def is_open(self):
        open_minutes = (self.closes_at - self.opens_at) * 60
        return self.minute <= open_minutes

class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tile   : a numpy array containing the tile image
        """
        self.tiles = tiles
        self.contents = [list(row) for row in layout.split("\n")]
        self.xsize = len(self.contents[0])
        self.ysize = len(self.contents)
        self.image = np.zeros(
            (self.ysize * TILE_SIZE, self.xsize * TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.tiles[0:32, 0:32]
        elif char == "G":
            return self.tiles[7 * 32: 8 * 32, 3 * 32: 4 * 32]
        elif char == "C":
            return self.tiles[2 * 32: 3 * 32, 8 * 32: 9 * 32]
        elif char == 'B':
            return self.tiles[0 * 32: 1 * 32, 4 * 32: 5 * 32]
        elif char == 'D':
            return self.tiles[3 * 32: 4 * 32, 13 * 32: 14 * 32]
        elif char == 'S':
            return self.tiles[5 * 32: 6 * 32, 9 * 32: 10 * 32]
        elif char == 'T':
            return self.tiles[5 * 32: 6 * 32, 6 * 32: 7 * 32]
        elif char == 'Y':
            return self.tiles[6 * 32: 7 * 32, 9 * 32: 10 * 32]
        else:
            return self.tiles[32:64, 64:96]

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                bm = self.get_tile(tile)
                self.image[
                    y * TILE_SIZE: (y + 1) * TILE_SIZE,
                    x * TILE_SIZE: (x + 1) * TILE_SIZE,
                ] = bm

    def draw(self, frame, offset=OFS):
        """
        draws the image into a frame
        offset pixels from the top left corner
        """
        frame[
            OFS: OFS + self.image.shape[0], OFS: OFS + self.image.shape[1]
        ] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


# QUESTION: where to put this?
dir_path = f'{utils.get_project_root()}/data/processed/'
df = concatenate_files(dir_path)
initial_state_probability = calculate_starting_probability(df)
prob_matrix = calculate_prob_matrix(df)


if __name__ == '__main__':

    # for i in range(100):
    # creating the header for our output file, that we fill during the simulation
    with open(f'{utils.get_project_root()}/data/output/marcomarkt.csv', 'w') as file:
        file.write(f'timestamp,customer_no,location\n')

    background = np.zeros((700, 1000, 3), np.uint8)
    tiles = cv2.imread(f'{utils.get_project_root()}/img/tiles.png')
    market_map = SupermarketMap(MARKET, tiles)

    lidl = Doodlmarket(closes_at=9, image=tiles)

    while lidl.is_open():  # is the shop open? TODO: write boolean function for that

        frame = background.copy()
        market_map.draw(frame)

        lidl.create_customers()
        lidl.record_customer_location()
        # movement here without adding 1 to the time
        lidl.remove_customers()
        for customer in lidl.customers:
                customer.update_position(customer.next_state())
                customer.draw(frame)

        # lidl.record_customer_location()

        lidl.next_minute()
        cv2.imshow("frame", frame)

        key = chr(cv2.waitKey(1) & 0xFF)
        if key == "q":
            break
        elif key in ('w', 'a', 's', 'd', 'c'):
            cust.move(key)

    cv2.destroyAllWindows()
