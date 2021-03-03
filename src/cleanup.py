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
    # out of the supermarket 'cause it closes. Those transitions are identified
    # by the looks of (any state != checkout) --> NaN. These will be deleted.

    # We need to append the transition information for the thieves until the
    # store closes
    df = replace_thief_entries(df)

    # Since checkout is a absorbing state, we want for every customer to have a
    # transition that looks like (checkout) --> (checkout).
    df.replace(np.nan, 'checkout', regex=True, inplace=True)
    df = df.drop(axis=1, columns=['customer_no'])
    return df

def replace_thief_entries(df):

    thieves = df.loc[(df['location_t'] != 'checkout') & (df['location_t+1'].isna())]

    # we have to delete the untries from the original df
    df.drop(thieves.index, inplace=True)

    # creating a temporary df that we will append to the original later
    thief_df = pd.DataFrame({'timestamp': [],
                             'customer_no': [],
                             'location_t': [],
                             'location_t+1': []})

    # Define the time the store closes each day
    end = f'{thieves.index.get_level_values(1).date.min()} 21:50:00'

    for index, values in thieves.iterrows():
        start = index[1]
        temp_df = pd.DataFrame({
            'timestamp': pd.date_range(start=start, end=end, freq='1min'),
            'customer_no': values[0],
            'location_t': values[1],
            'location_t+1': values[1]})

        thief_df = pd.concat([thief_df, temp_df])

    # we need to make thieves look like the original df to be able to append it
    thief_df.reset_index(inplace=True)
    thief_df = thief_df.set_index(keys=['customer_no', 'timestamp'], drop=False)
    thief_df = thief_df.drop(axis=1, columns=['index', 'timestamp'])

    return df.append(thief_df)


# get a list of files in data/raw
dir_path = f'{utils.get_project_root()}/data/raw/'
list_of_files = os.listdir(dir_path)

for filename in list_of_files:
    filepath = f'{utils.get_project_root()}/data/raw/{filename}'
    df = pd.read_csv(filepath, sep=';', index_col=0, parse_dates=True)
    df = clean_data(df)
    df.to_csv(f'{utils.get_project_root()}/data/processed/{filename}')
