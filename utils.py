import urllib.request as libreq
import argparse
import feedparser
from datetime import datetime
import time

def get_catergory(file_path):
    with open(file_path,'r') as f:
        categories = f.readlines()
    categories = [i.replace('\n','') for i in categories]
    
    return categories

def get_feed(url):
    state = False
    while state == False:
        response = libreq.urlopen(url).read()
        feed = feedparser.parse(response)
        if len(feed['entries'])>0:
            state = True
        time.sleep(1)
    return feed
            

def find_start_date_id(start_date_time,catergory):
    base_url = 'http://export.arxiv.org/api/query?search_query=cat:{}&start={}&max_results={}'
    # response = libreq.urlopen(base_url.format(catergory,0,1)).read()
    # feed = feedparser.parse(response)
    feed = get_feed(base_url.format(catergory,0,1))
    if start_date_time > datetime.strptime('2022-06-01','%Y-%m-%d'):
        start_date_id = 8000
    else:
        start_date_id = 0
    currect_time = datetime.strptime(feed['entries'][0]['published'][:10],'%Y-%m-%d')
    

    while currect_time < start_date_time:
        start_date_id += 50
        # response = libreq.urlopen(base_url.format(catergory,start_date_id,1)).read()
        # feed = feedparser.parse(response)
        feed = get_feed(base_url.format(catergory,start_date_id,1))
        # print(feed)
        # if (len(feed['entries'])==0):
        #     print(start_date_id)
        #     print(feed)
        currect_time = datetime.strptime(feed['entries'][0]['published'][:10],'%Y-%m-%d')
        # time.sleep(60)
    
    while currect_time >= start_date_time:
        start_date_id -= 1
        # response = libreq.urlopen(base_url.format(catergory,start_date_id,1)).read()
        # feed = feedparser.parse(response)
        feed = get_feed(base_url.format(catergory,start_date_id,1))
        # if (len(feed['entries'])==0):
        #     print(start_date_id)
        #     print(feed)
        currect_time = datetime.strptime(feed['entries'][0]['published'][:10],'%Y-%m-%d')
        time.sleep(60)
        

    
    return start_date_id+1

def find_end_date_id(end_date_time,catergory,start_date_id=0):
    base_url = 'http://export.arxiv.org/api/query?search_query=cat:{}&start={}&max_results={}'
    # response = libreq.urlopen(base_url.format(catergory,start_date_id,1)).read()
    # feed = feedparser.parse(response)
    feed = get_feed(base_url.format(catergory,start_date_id,1))
        
    end_date_id = start_date_id
    currect_time = datetime.strptime(feed['entries'][0]['published'][:10],'%Y-%m-%d')
    

    while currect_time <= end_date_time:
        end_date_id += 100
        # response = libreq.urlopen(base_url.format(catergory,end_date_id,1)).read()
        # feed = feedparser.parse(response)
        feed = get_feed(base_url.format(catergory,end_date_id,1))
        
        currect_time = datetime.strptime(feed['entries'][0]['published'][:10],'%Y-%m-%d')
        time.sleep(1)
    
    for i in range(100):
        end_date_id -= 1
        # response = libreq.urlopen(base_url.format(catergory,end_date_id,1)).read()
        # feed = feedparser.parse(response)
        feed = get_feed(base_url.format(catergory,end_date_id,1))
        
        currect_time = datetime.strptime(feed['entries'][0]['published'][:10],'%Y-%m-%d')
        time.sleep(1)
        
        if currect_time <= end_date_time:
            break
    
    return end_date_id