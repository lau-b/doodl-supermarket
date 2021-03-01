import pandas as pd
import numpy as np
import utils
import os

def clean_data(df):
    # we have to do the resampling and filling with respect to the cusomter
    df = df.groupby('customer_no').resample('1min').ffill()

    # creates the transition from one location to the next one.
    df['location_t+1'] = df.groupby(df['customer_no']).shift(-1)
    # also renaming the location column for consistency reasons
    df = df.rename(columns={'location': 'location_t'})

    # There are customers in the dataset, who leave the supermarket without
    # visiting the checkout. Those are either thieves or they are kicked
    # out of the supermarket because it closes. Those transitions are identified
    # by the looks of (any state != checkout) --> NaN. These will be deleted.
    thieves = df.loc[(df['location_t'] != 'checkout') &
                     (df['location_t+1'].isna())]
    df.drop(thieves.index, inplace=True)

    # Since checkout is a absorbing state, we want for every customer to have a
    # transition that looks like (checkout) --> (checkout).
    df.replace(np.nan, 'checkout', regex=True, inplace=True)
    return df


# get a list of files in data/raw
dir_path = f'{utils.get_project_root()}/data/raw/'
list_of_files = os.listdir(dir_path)

for filename in list_of_files:
    filepath = f'{utils.get_project_root()}/data/raw/{filename}'
    df = pd.read_csv(filepath, sep=';', index_col=0, parse_dates=True)
    df = clean_data(df)
    df.to_csv(f'{utils.get_project_root()}/data/processed/{filename}')
