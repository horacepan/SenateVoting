import urllib.parse
import pdb
from bs4 import BeautifulSoup as bs4
import os
import requests

def is_absolute(url):
    return urllib.parse.urlparse(url).netloc != ""

def get_subject(year, bill_num):
    url = 'https://www.govtrack.us/congress/votes/114-%d/s%d' %(year, bill_num)
    return get_area(url)

def get_area(url):
    base_url =  'https://www.govtrack.us'

    resp = requests.get(url)
    soup = bs4(resp.text, 'lxml')
    div = soup.find('div', {'id': 'vote_explainer'})
    links = div.findAll('a')
    if len(links) == 0:
        return "Nomination" 

    for a in links:
        #print(a)
        if is_absolute(a['href']):
            #print('is absolute')
            next_url = a['href']
        else:
            #print('relative')
            next_url = base_url + a['href']
        #print("current url: %s\nnext url: " %url, next_url)
        if 'members' in next_url:
            continue
        elif 'govtrack.us' in next_url:
            return get_from(next_url)
        else:
            continue
    raise Exception("Couldnt find link to follow!", url)
        
def get_from(url):
    resp = requests.get(url)
    soup = bs4(resp.text, 'lxml')
    data = soup.find('dt', text='Subject Areas').findNextSibling('dd')
    area = data.findAll('a')[0].contents[0]
    return area

if __name__ == '__main__':
    years = [2015, 2016]
  
    i = 284
    fhandle = open('topics.csv', 'a')
    #fhandle.write('row_num, year, bill_num\n')
    for y in years:
        dirname = 'data/%d' %y
        num_bills = len(os.listdir(dirname))  
        if y == 2015:
            start = 285
        else:
            start = 1
        for bill_num in range(start, num_bills+1):
            subject = get_subject(y, bill_num)
            new_line = '%d,%d,%d,%s\n' %(i, y, bill_num, subject)
            print(new_line)
            fhandle.write(new_line)
            i += 1

