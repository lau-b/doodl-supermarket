import random
import time
import pandas as pd

class Customer:
    '''single customer that can move in the supermarket randomly
       according to a probability matrix'''
    def __init__(self, name, initial_state, budget = 100):
        self.name = name 
        self.state = initial_state 
        self.budget = budget 

    def __repr__(self):
        state = f'Customer {self.name} in state {self.state}.'
        budget = f'The budget of customer {self.name} amount to {self.budget}'
        return state + '\t' + budget


cust1 = Customer('Alex', 'fruit')
        