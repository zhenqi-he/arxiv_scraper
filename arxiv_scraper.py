import urllib.request as libreq
import argparse
import feedparser
from datetime import datetime
import pandas as pd
from utils import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--category',required=True)# catergory of paper
    parser.add_argument('--start_date',required=True)# statr_date , format: yyyy-mm-dd , e.g. 2022-01-08
    parser.add_argument('--end_date',required=True)# end_date , format: yyyy-mm-dd , e.g. 2022-01-08

    args = parser.parse_args()
    catergory = args.category
    start_date = args.start_date
    end_date = args.end_date
    
    try:
        start_date_time = datetime.strptime(start_date,'%Y-%m-%d')
        end_date_time = datetime.strptime(end_date,'%Y-%m-%d')
    except:
        print("Wrong Format of start date or end date")
        return 0
    
    if end_date_time < start_date_time:
        print("End date is earlier than start date")
        return 0
    
    cs_categories = get_catergory("./cs_category.txt")
    
    if catergory not in cs_categories:
        print("Wrong Category")
        return 0
    
    
    
    start_date_id = find_start_date_id(start_date_time,catergory)
    end_date_id = find_end_date_id(end_date_time,catergory,start_date_id)
    # start_date_id = 8136
    # end_date_id = 8202
    
    base_url = 'http://export.arxiv.org/api/query?search_query=cat:{}&start={}&max_results={}'.format(catergory,start_date_id,end_date_id-start_date_id)
    response = libreq.urlopen(base_url).read()
    feed = feedparser.parse(response)
    entries = feed['entries']
    
    df = pd.DataFrame({"id":[],"url":[],"published":[],"updated":[],"title":[],"arxiv_comment":[],'summary':[],'authors':[]})
    
    for i in range(len(entries)):
        id = entries[i]['id'].replace("http://arxiv.org/abs/","")[:-3]
        url = entries[i]['link']
        published = entries[i]['published']
        updated = entries[i]['updated']
        title = entries[i]['title']
        try:
            arxiv_comment = entries[i]['arxiv_comment']
        except:
            arxiv_comment = ''
        try:
            
            summary = entries[i]['summary']
        except:
            summary = ''
        authors = ''
        for n,author in enumerate(entries[i]['authors']):
            if n<len(entries[i]['authors'])-1:
                authors += author['name'] + ' ; '
            else:
                authors += author['name'] 
        
        df.loc[i,'id'] = id
        df.loc[i,'url'] = url
        df.loc[i,'published'] = published
        df.loc[i,'updated'] = updated
        df.loc[i,'title'] = title
        df.loc[i,'arxiv_comment'] = arxiv_comment
        df.loc[i,'summary'] = summary
        df.loc[i,'authors'] = authors

    df.to_csv('./{}to{}_cat-{}.csv'.format(start_date,end_date,catergory),index=False)
if __name__ == "__main__":
    main()
            
            
    
        
            
            
