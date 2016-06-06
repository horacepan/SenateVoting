import pandas as pd
import os
import numpy as np

def get_all_data():
    all_data = pd.read_csv('data/all_votes.csv')
    all_data = all_data.drop(all_data.columns[0], 1)
    return all_data

def get_senators_matrix():
    data = get_all_data()
    dropped = data.drop(['id', 'name', 'party'], 1)
    return dropped.as_matrix()

def get_vote_matrix():
    senators_matrix = get_senators_matrix()
    return senators_matrix.T

def get_data(years=None):
    if years == None:
        years = [2015, 2016]

    all_data = pd.DataFrame()
    df_15_1 = pd.read_csv('data/2015/1.csv', skiprows=1)
    all_data['id'] = df_15_1['person']
    all_data['name'] = df_15_1['name']
    all_data['party'] = df_15_1['party']
    for y in years:
        dirname = 'data/%d' %y
        num_bills = len(os.listdir(dirname))
        for i in range(1, num_bills+1):
            fname = '%s/%d.csv' %(dirname, i)
            df = pd.read_csv(fname, skiprows=1)
            all_data['%d_%d' %(y, i)] = df['vote'].apply(convert_vote)

    all_data['party'] = all_data['party'].apply(convert_party)
    all_data.sort_index(by='party')
    return all_data

def convert_vote(val):
    if val in ['Yea', 'Yes']:
        return 1
    else:
        # treat missing votes/not voting as nays
        return -1

def convert_party(val):
    if val == 'Democrat':
        return 'D'
    if val == 'Republican':
        return 'R'
    if val == 'Independent':
        return 'I'

def get_bill_title(years):
    pass
