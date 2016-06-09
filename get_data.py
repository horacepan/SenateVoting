import pdb
import pandas as pd
import os
import numpy as np

def get_all_data():
    all_data = pd.read_csv('data/all_votes.csv')
    all_data = all_data.drop(all_data.columns[0], 1)
    return all_data

def get_all_bills():
    bill = pd.read_csv('data/all_bills.csv')
    return bills

def get_topics():
    topics = pd.read_csv('data/allt.csv')
    index = gen_bill_name_index([2015, 2016], {2015:339, 2016:88})
    topics.index = index
    return topics

def get_all_data_bills():
    years = [2015, 2016]
    num_bills = {2015: 339, 2016: 88}
    df = pd.DataFrame()
    df_senators = pd.read_csv('data/2015/1.csv', skiprows=1, index_col=0)
    df['index'] = gen_bill_name_index(years, num_bills)
    df = df.set_index('index', drop=True)

    senator_ids = []
    for i in df_senators.index:
        df[i] = np.zeros(len(df))
        senator_ids.append(i)

    for y in years:
        for bill_num in range(1, num_bills[y]+1):
            curr_df = pd.read_csv(get_csv_name(y, bill_num), skiprows=1, index_col=0)
            curr_index = '%d_%d' %(y, bill_num)
            for senator in senator_ids:
                vote = convert_vote(curr_df.loc[senator]['vote'])
                df.ix[curr_index, senator] = vote
    return df

def convert_vote(val):
    if val == 'Yea' or val == 'Yes':
        return 1
    else:
        return -1

def gen_bill_name_index(years, bill_nums):
    index = []
    for y in years:
        for b in range(1, bill_nums[y]+1):
            index.append('%d_%d' %(y, b))
    return index 

def get_csv_name(year, bill_num):
    fname = 'data/%d/%d.csv' %(year, bill_num)
    return fname

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

if __name__ == '__main__':
    df = get_all_data_bills()
