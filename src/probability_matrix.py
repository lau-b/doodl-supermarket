import os
import pandas as pd

def concatenate_files(dir_path):
    '''dir_path is the path to the directory where are stored the cleaned
       csv to be concatenated. The function concatenates the csv files and
       returns a DataFrame'''
    list_of_files = os.listdir(dir_path)
    conc_df = pd.DataFrame({
        'customer_no': [],
        'location_t': [],
        'location_t+1': []})

    for filename in list_of_files:
        filepath = dir_path + filename
        _df = pd.read_csv(filepath, sep=',', index_col=1, parse_dates=True)
        conc_df = pd.concat([conc_df, _df])

    return conc_df


def calculate_prob_matrix(conc_df):

    '''conc_df is a DataFrame (must have state_t and state_t+1 states as
       columns). The function calclates and returns the probabily matrix'''
    prob_matrix = pd.crosstab(
        conc_df['location_t'],
        conc_df['location_t+1'],
        normalize=0)
    return prob_matrix


def calculate_starting_probability(conc_df):
    '''calculates the probabilty for a customer to spawn in a certain area
    '''
    conc_df['date'] = conc_df.index.date
    conc_df = conc_df.drop(columns='location_t+1')
    conc_df = conc_df.groupby(['date', 'customer_no']).first()
    return conc_df['location_t'].value_counts(normalize=1)

