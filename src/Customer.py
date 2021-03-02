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
    def __init__(self, name, initial_state, budget = 100):
        self.name = name 
        self.state = initial_state 
        self.budget = budget 

    def __repr__(self):
        state = f'Customer {self.name} in state {self.state}.\n'
        budget = f'The budget of customer {self.name} amount to {self.budget}'
        return state + budget

    def next_state(self, prob_matrix):
        '''prob_matrix is the prbability matrix of the supermaket states (floats)
        Returns the next state of the customer according to the current state and the
        values of the prob matrix '''
        prob_line = np.array([prob_matrix.loc[prob_matrix.index.get_level_values(0) == self.state]]).reshape(-1)
        #print(prob_line)
        #print(prob_line.sum())
        next_st = np.random.choice(['checkout', 'dairy', 'drinks', 'fruit', 'spices'], p=prob_line)
        return next_st
        


cust1 = Customer('Alex', 'spices')
#print(cust1)
next = cust1.next_state(prob_matrix)
print(next)

        