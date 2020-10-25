#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentiment Analysis Project

@author: MeganParsons
"""

# Import Google Client Library and Instantiate a Client
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
# Import Tweepy
import tweepy
# Import COVID-19 Data API
import COVID19Py
# Import GUI package
import tkinter as tk 
from tkinter import ttk
# General Imports
import os
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import datetime

# Pandas Settings
pd.set_option('max_colwidth', 280)  # Capture full tweet
pd.set_option("display.max_rows", None, "display.max_columns", None)
# Handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Fetch Twitter API key and access token from environment variables
api_key = os.environ.get("TWITTER_API_KEY")
api_secret = os.environ.get("TWITTER_API_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Tweepy Authentication
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

# Access the Tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# Access the Google NLP API
client = language.LanguageServiceClient()
# Access the COVID19Py API
covid = COVID19Py.COVID19(url="https://cvtapi.nl")

def preprocess_tweet(status):
  # Return full text of tweet
  if hasattr(status, 'retweeted_status'):   # Check if retweet
    try:
      status = status.retweeted_status.text
    except AttributeError:
      status = status.retweeted_status.full_text
  else:
    try:
      status = status.extended_tweet.full_text
    except AttributeError:
      status = status.full_text

  return status

def sentiment_analysis(tweet):
  # Sentiment analysis on input
  document = language.types.Document(
  content=tweet, 
  type=enums.Document.Type.PLAIN_TEXT)

  response = client.analyze_sentiment(
    document=document,
    encoding_type='UTF32',
    )

  sentiment = response.document_sentiment

  return sentiment

def eval(score, mag):
    # Sentiment analysis interpretation
    if score > 0.2:
        return '+'
    elif score < 0.2 and score > -0.2:
        return ' '
    else:
        return 'v'
    
def mkr(interp):
    if interp == '+':
        return 'b'
    elif interp == 'o':
        return 'k'
    else:
        return 'r'

def tweet_polarity(tweet_data):
    h1 = plt.hist(tweet_data['Sentiment_Score'], bins='auto')
    plt.title('COVID-19 Sentiment Distribution for @{}'.format(tweet_data['ID'][0]))
    plt.xlabel('Sentiment Score')
    plt.xlim(-1,1)
    plt.show()
    plt.savefig('tweet_data.png')
    
def covid_plot(tweet_data, covid_data):
    # Create plot of COVID-19 data   
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(20, 10))
    ax[0].plot(covid_data['Date'], covid_data['Confirmed Cases'])
    ax[0].set_title('Cases of COVID-19 in the United States')
    ax[0].set_ylabel('Confirmed Cases of COVID-19')
    
    # Create plot of Twitter Sentiment and Magnitude Data
    for x, y, s, c, m in zip(tweet_data['Date'].to_list(), tweet_data['Sentiment_Magnitude'].to_list(), 100*np.ones(len(tweet_data['Marker Color'].to_list())), tweet_data['Marker Color'].to_list(), tweet_data['Interpretation'].to_list()):
        ax[1].scatter(x, y, s=s, c=c, marker=m) 
    ax[1].set_title('COVID-19 Tweet Sentiment')
    ax[1].set_ylabel('Sentiment Magnitude')
    ax[1].tick_params(axis='x', rotation=45)
    
    # Format plots
    plt.tight_layout() 
    plt.xlabel('Date')
    plt.show()
    plt.savefig('covid_plot.png')
    
    
def visualize(tweet_data, covid_data):
    tweet_polarity(tweet_data)    # Overview of Tweet Data
    covid_plot(tweet_data, covid_data)
    
def select_fn(acct):
    print(acct.get())

def main():
    # Dropdown Menu for Twitter Account Selection
    # Create window 
    window = tk.Tk() 
    window.title('Select Twitter Account to Analyze') 
    window.geometry('250x200') 
        
    # Instructions 
    ttk.Label(window, text = "Select Twitter Account to Analyze:", 
              font = ("Times New Roman", 10)).grid(column = 0, 
              row = 5, padx = 10, pady = 25) 
      
    # Create Combobox 
    acct = tk.StringVar() 
    selection = ttk.Combobox(window, width = 27, textvariable = acct, state='readonly') 
    
    # Dropdown Options
    selection['values'] = ('realDonaldTrump','CDCgov','JoeBiden','CDCDirector')
    selection.grid(column=0, row=6)
    selection.bind('<<ComboboxSelected>>',select_fn(acct))
    selection.current(0)
    
    
    button = tk.Button(window, text = "Analyze", command = window.destroy)
    button.grid(column=0,row=8)

    window.mainloop()
       
    # Process COVID-19 Data
    location = covid.getLocationByCountryCode("US", timelines=True)
    raw_data = location[0]['timelines']['confirmed']['timeline']
    covid_data = pd.DataFrame.from_dict(raw_data, orient = 'index')
    covid_data = covid_data.reset_index()
    covid_data.columns = ['Date','Confirmed Cases']
    covid_data['Date'] = pd.to_datetime(covid_data.Date, format='%Y-%m-%dT%H:%M:%SZ')

    # Create dataframe
    tweet_data = pd.DataFrame()
      
    # Search Parameters
    query = 'from:{}'.format(acct.get())
    max_tweets = 3000
    result_type = 'recent'
    lang = 'en'
    tweet_mode = 'extended'
      
    # ID from query search
    sep = ':'
    handle = query.split(sep, 1)[-1]
    
    # Process Twitter Data
    for status in tweepy.Cursor(api.search, q=query, count=max_tweets, lang=lang, result_type=result_type, tweet_mode=tweet_mode).items(max_tweets):
        tweet = preprocess_tweet(status)
        if any(keyword in tweet for keyword in ('COVID', 'covid', 'China virus', 'coronavirus')):
            
          # Sentiment analysis
          sentiment = sentiment_analysis(tweet)
          
          # Date Time format
          date_time_str = str(status.created_at)
          date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

          #Store values
          df = pd.DataFrame({'Date':[date_time],
            'ID':handle,
            'Tweet':tweet,
            'Sentiment_Score':[sentiment.score],
            'Sentiment_Magnitude':[sentiment.magnitude]})
          tweet_data = tweet_data.append(df, ignore_index=True)
    
    tweet_data['Date'] = pd.to_datetime(tweet_data['Date'], format='%Y-%m-%d %H:%M:%S')
    tweet_data['Interpretation'] = tweet_data.apply(lambda row : eval(row['Sentiment_Score'], row['Sentiment_Magnitude']), axis=1)
    tweet_data['Marker Color'] = tweet_data.apply(lambda row : mkr(row['Interpretation']), axis=1)
  
    visualize(tweet_data, covid_data)


if __name__ == "__main__":
  main()
