import time
import pandas as pd
import numpy as np
import utils
from probability_matrix import calculate_prob_matrix
from probability_matrix import concatenate_files
from probability_matrix import calculate_starting_probability
from datetime import date


class Customer:
    '''single customer that can move in the supermarket randomly
       according to a probability matrix'''
    def __init__(self, id, initial_state, prob_matrix, budget=100):
        self.id = id
        self.state = np.random.choice(
            list(initial_state.index),
            p=initial_state)
        self.budget = budget
        self.matrix = prob_matrix
        self.previous = initial_state

    def __repr__(self):
        state = f'Customer {self.id} in state {self.state}.\n'
        budget = f'The budget of customer {self.id} amount to {self.budget}'
        return state + budget

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
        self.date = date.today()
        self.minute = 0
        self.customers = []
        self.opens_at = 7
        self.unique_customers = 0
        self.probability_matrix = prob_matrix
        self.name = 'MarcoMarkt'
        self.initial_state_probability = initial_state_probability

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
        self.minute += 1
        for customer in self.customers:
            customer.next_state()

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
                self.probability_matrix))

        return '???'  # QUESTION @Malte: What to return here?

    def remove_customers(self):
        for customer in self.customers:
            if customer.state == 'checkout' and customer.previous == 'checkout':  #TODO: do we need the prev check?
                self.customers.remove(customer)

    def record_customer_location(self):
        filepath = f'{utils.get_project_root()}/data/output/marcomarkt.csv'
        for customer in self.customers:
            with open(filepath, 'a') as f:
                f.write(f'{self.get_time()},{customer.id},{customer.state}\n')


# QUESTION: where to put this?
dir_path = f'{utils.get_project_root()}/data/processed/'
df = concatenate_files(dir_path)
initial_state_probability = calculate_starting_probability(df)
prob_matrix = calculate_prob_matrix(df)


if __name__ == '__main__':

    # creating the header for our output file, that we fill during the simulation
    with open(f'{utils.get_project_root()}/data/output/marcomarkt.csv', 'w') as file:
        file.write(f'timestamp,customer_no,location\n')

    lidl = Doodlmarket()

    i = 0
    while i < 120:  # is the shop open? TODO: write boolean function for that

        lidl.create_customers()

        lidl.next_minute()

        lidl.remove_customers()

        lidl.record_customer_location()

        i += 1
