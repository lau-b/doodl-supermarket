import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import utils

dir_path = f'{utils.get_project_root()}/data/processed/'

def concatenate_files(dir_path):
    '''dir_path is the path to the directory where are stored the cleaned
       csv to be concatenated. The function concatenates the csv files and 
       returns a DataFrame'''
    list_of_files = os.listdir(dir_path)
    conc_df = pd.DataFrame({'timestamp':[], 'customer_no':[], 'location_t':[], 'location_t+1':[]})

    for filename in list_of_files:
        filepath = dir_path + filename
        df = pd.read_csv(filepath, sep=';', index_col=0, parse_dates=True)
        conc_df = pd.concat([conc_df, df])
        return conc_df

def calculate_prob_matrix(conc_df):
    '''conc_df is a DataFrame (must have state_t and state_t+1 states as columns). 
        The function calclates and returns the probabily matrix'''
    prob_matrix = pd.crosstab(conc_df['location_t'], conc_df['location_t+1'], normalize=0).round(3)
    return prob_matrix
    