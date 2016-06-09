import pdb
import sys
import json
import urllib2

def save_all_summaries(years, bill_nums, congress):
    for i in range(len(years)):
        num_bills = bill_nums[i]
        year = years[i]
        for bill_num in range(1, num_bills+1):
            fname = 'data/summaries/%d_%d.txt' %(year, bill_num)
            f = open(fname, 'w')
            s = get_summary(congress, year, bill_num)
            s = s.encode('utf-8')
            f.write(s)
            f.close()
            print("Done with summary for %d/%d" %(year, bill_num))

def write_all_summaries(years, bill_nums, congress, fname='data/all_summaries.csv'):
    f = open(fname, 'a')
    for t in yield_all_summaries(years, bill_nums, congress):
        f.write(t+'\n')

def write_all_topics(years, bill_nums, congress, fname='data/all_topics.csv'):
    f = open(fname, 'a')
    all_topics = set()
    for t in yield_all_topics(years, bill_nums, congress):
        f.write(t+'\n')
    print("Done")

def yield_all_topics(years, bill_nums, congress):
    topic_set = set()
    for i in range(len(years)):
        num_bills = bill_nums[i]
        year = years[i]
        for bill_num in range(1, num_bills+1):
            t = get_topic(congress, year, bill_num)
            yield(t)
            topic_set.add(t)
            print("Done with %d/%d" %(year, bill_num))

def get_topic(congress, year, vote_num):
    vote_json = get_vote_json(congress, year, vote_num)
    if vote_json['category'] == 'nomination' or (vote_json['category'] == 'cloture' and 'nomination' in vote_json):
        return 'Nomination'
    else:
        bill_type = vote_json['bill']['type']
        bill_num = int(vote_json['bill']['number'])
        bill_json = get_bill_json(congress, bill_type, bill_num)
        return bill_json['subjects_top_term']

def get_summary(congress, year, vote_num):
    vote_json = get_vote_json(congress, year, vote_num)
    if vote_json['category'] == 'nomination' or (vote_json['category'] == 'cloture' and 'nomination' in vote_json):
        return vote_json['question']
    #elif vote_json['category'] == 'amendment':
    #    amend_type = vote_json['amendment']['type']
    #    amend_num = int(vote_json['amendment']['number'])
    #    amend_json = get_amendment_json(congress, amend_type, amend_num)
    #    return amend_json['purpose']
    else:
        bill_type = vote_json['bill']['type']
        bill_num = int(vote_json['bill']['number'])
        bill_json = get_bill_json(congress, bill_type, bill_num)
        return bill_json['summary']['text']

def get_vote_json(congress, year, bill_num):
    url = 'https://www.govtrack.us/data/congress/%d/votes/%d/s%d/data.json' \
          %(congress, year, bill_num)
    vote_json = json.load(urllib2.urlopen(url))
    return vote_json

def get_amendment_json(congress, amend_type, amend_num):
    url = 'https://www.govtrack.us/data/congress/%d/amendments/%samdt/%samdt%d/data.json' \
          %(congress, amend_type, amend_type, amend_num)
    amend_json = json.load(urllib2.urlopen(url))
    return amend_json

def get_bill_json(congress, bill_type, bill_num):
    url = 'https://www.govtrack.us/data/congress/%d/bills/%s/%s%d/data.json' \
          %(congress, bill_type, bill_type, bill_num)
    bill_json = json.load(urllib2.urlopen(url))
    return bill_json

def get_sum_bill(bill_json):
    pass

if __name__ == '__main__':
    pass
