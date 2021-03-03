import random
import time
import pandas as pd
import numpy as np
import utils
from probability_matrix import calculate_prob_matrix, concatenate_files

#print(matrix)
class Customer:
    '''single customer that can move in the supermarket randomly
       according to a probability matrix'''
    def __init__(self, id, initial_state,  prob_matrix, budget = 100):
        self.id = id
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
        # next_st = np.random.choice(['list_of_locations_from the supermarket'], p=prob_line)
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



class Doodlmarket:

    def __init__(self):
        # self.time = Time.localtime()
        self.minute = 0
        self.customers = []
        self.opens_at = 7
        self.unique_customers = 0
        # self.locations = [] # which areas are there in the market
        self.probability_matrix = prob_matrix
        self.name = 'MarcoMarkt'

    def __repr__(self):
        return f'Welcome to {self.name}. Enjoy your shopping. \n \
        Currently there are {len(self.customers)} customers in here. \n \
        Please keep a distance of at least 1.5 meters. \n Its {self.get_time()} o\'clock.'


    def get_state_of_customers(self):
        states = []
        for customer in self.customers: # TODO: make a list comprehension out of this.
            states.append(customer.get_current_state())
        return states


    def get_time(self):
        """ returns the current time in 'HH:mm:SS'
        """
        hour = self.opens_at + self.minute // 60
        minute = self.minute % 60
        return f'{hour:02d}:{minute:02d}'


    def next_minute(self):
        self.minute += 1

        for customer in self.customers:

            # call the fuction that moves the customers => new states
            customer.next_state()

            # call the fucntion that tells us which customer left the store (customer has transition from checkout to checkout)
            print(customer.id, customer.state)

    def create_customers(self):

        # every minute there can enter a maximum of 5 new customers
        amount = [1, 2, 3, 4, 5]
        p = [0.3, 0.35, 0.2, 0.1, 0.05] # this was us trying to calculate 100%
        new_customers = np.random.choice(amount, p=p)

        for customer in range(new_customers):
            self.unique_customers += 1
            self.customers.append(Customer(
                self.unique_customers,
                'dairy', # TODO: use starting location function
                self.probability_matrix))      # TODO: use self.probability_matrix

        return '???' # QUESTION @Malte: What to return here?

    # def remove_customers(self):


dir_path = f'{utils.get_project_root()}/data/processed/'
prob_matrix = calculate_prob_matrix(concatenate_files(dir_path))

# simulation
if __name__ == '__main__':

    lidl = Doodlmarket()
    i = 0

    while i < 15: # is the shop open? TODO: write voolean function for that

        # create customer(s) who enters the store
        print(lidl)

        lidl.create_customers()

        lidl.next_minute()
            # next_minute calls customer.move()

        # lidl.remove_customers()


        i += 1

        print('################### \n')


# cust1 = Customer('Alex', 'dairy', prob_matrix)
# #print(cust1)
# while True:
#     next = cust1.next_state()
#     time.sleep(1)
#     print('Is active?', cust1.is_active())
#     if cust1.get_current_state() == 'checkout' and cust1.get_previous_state() == 'checkout':
#         print('Previous state =', cust1.get_previous_state())
#         print('Current state =', cust1.get_current_state())
#         break

