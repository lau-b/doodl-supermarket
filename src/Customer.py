import random
import time
import pandas as pd
import numpy as np
import utils
from probability_matrix import calculate_prob_matrix, concatenate_files

dir_path = f'{utils.get_project_root()}/data/processed/'
prob_matrix = calculate_prob_matrix(concatenate_files(dir_path))

#print(matrix)
class Customer:
    '''single customer that can move in the supermarket randomly
       according to a probability matrix'''
    def __init__(self, name, initial_state,  prob_matrix, budget = 100):
        self.name = name 
        self.state = initial_state 
        self.budget = budget 
        self.matrix = prob_matrix
        self.previous = initial_state

    def __repr__(self):
        state = f'Customer {self.name} in state {self.state}.\n'
        budget = f'The budget of customer {self.name} amount to {self.budget}'
        return state + budget

    def next_state(self):
        '''prob_matrix is the prbability matrix of the supermaket states (floats)
        Returns the next state of the customer according to the current state and the
        values of the prob matrix '''
        prob_line = np.array([self.matrix.loc[self.matrix.index.get_level_values(0) == self.state]]).reshape(-1)
        next_st = np.random.choice(['checkout', 'dairy', 'drinks', 'fruit', 'spices'], p=prob_line)
        print(prob_line)
        self.previous = self.state
        self.state = next_st
        return next_st

    def is_active(self):
        if (self.state == 'checkout') and (self.previous == self.state):
            return False
        else:
            return True

    def get_current_state(self):
        return self.state

    def get_previous_state(self):
        return self.previous


        


cust1 = Customer('Alex', 'dairy', prob_matrix)
#print(cust1)
while True:
    next = cust1.next_state()
    time.sleep(1)
    print('Is active?', cust1.is_active())
    if cust1.get_current_state() == 'checkout' and cust1.get_previous_state() == 'checkout':
        print('Previous state =', cust1.get_previous_state())
        print('Current state =', cust1.get_current_state())
        break

        