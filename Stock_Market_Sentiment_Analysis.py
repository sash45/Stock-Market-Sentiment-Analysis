# Import libraries
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
# NLTK VADER for sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer

finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}
tickers = ['AMZN', 'TSLA', 'GOOG']

for ticker in tickers:
    url = finwiz_url + ticker
    req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
    response = urlopen(req) 
    html=BeautifulSoup(response)
    news_table=html.find(id='news-table')
    news_tables[ticker]=news_table
amzn=news_tables['AMZN']
amzn_tr=amzn.findAll('tr')
for i,table_row in enumerate(amzn_tr):
    a_text=table_row.a.text
    td_text=table_row.td.text 
    if i==3:
        break
parsed_news=[]

#Iterate through the news
for file_name,news_table in news_tables.items():
    for x in news_table.findAll('tr'):
        text=x.a.get_text()
        date_scrape=x.td.text.split()
        if len(date_scrape)==1:
            time=date_scrape[0]
        else:
            date=date_scrape[0]
            time=date_scrape[1]
        ticker=file_name.split('-')[0]
        # Append ticker, date, time and headline as a list to the 'parsed_news' list
        parsed_news.append([ticker, date, time, text])
parsed_news

#Instantiate the sentiment intensity analyser
vader=SentimentIntensityAnalyzer()

#Set column names
columns=['ticker','date','time','headline']

#Convert the parsed_news list into dataframe
parsed_and_scored_news=pd.DataFrame(parsed_news,columns=columns)

#Score of the sentiment
score=parsed_and_scored_news['headline'].apply(vader.polarity_scores).tolist()

scores_df=pd.DataFrame(score)

parsed_and_scored_news=parsed_and_scored_news.join(scores_df,rsuffix='_right')

parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date).dt.date

print(parsed_and_scored_news.head())


    
    
    
    