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
# General Imports
import os
import pandas as pd
import matplotlib.pyplot as plt 

# Pandas Settings
pd.set_option('max_colwidth', 280)  # Capture full tweet
pd.set_option("display.max_rows", None, "display.max_columns", None)

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

  def tweet_polarity(tweet_data):
    h1 = plt.hist(tweet_data['Sentiment_Score'], bins='auto')
    plt.title('COVID-19 Sentiment Distribution for {}'.format(tweet_data['ID']))
    plt.xlabel('Sentiment Score')
    

  def visualize(tweet_data):
      tweet_polarity(tweet_data)    # Overview of Tweet Data




def main():
    
  # Process COVID-19 Data
  location = covid.getLocationByCountryCode("US", timelines=True)
  raw_data = location[0]['timelines']['confirmed']['timeline']
  covid_data = pd.DataFrame.from_dict(raw_data, orient = 'index')
  covid_data = covid_data.reset_index()
  covid_data.columns = ['Date','Confirmed Cases']
  covid_data['Date'] = pd.to_datetime(covid_data.Date, format='%Y-%m-%dT%H:%M:%SZ')

 
  # Create dataframe
  tweet_data = pd.DataFrame()
  date = []
  content = []
  sentiment_score = []
  sentiment_mag = []
  i=0

  # Twitter Handles of Interest
  realDonaldTrump = '25073877'
  CDCgov = '146569971'
  
  # Search Parameters
  query = 'from:CDCgov'
  max_tweets = 10
  result_type = 'recent'
  lang = 'en'
  tweet_mode = 'extended'
  since_id = '2020-02-01'
  counter = 0
  
  # ID from query search
  sep = ':'
  handle = query.split(sep, 1)[-1]


  # for status in tweepy.Cursor(api.user_timeline, id=realDonaldTrump, since_id=since_id, tweet_mode='extended').items():
  #   tweet = preprocess_tweet(status)
  #   counter += 1
  #   print(counter)
  #   if any(keyword in tweet for keyword in ('COVID', 'covid', 'China virus')):
  #     sentiment = sentiment_analysis(tweet)
  #     print(status.created_at, '\t', tweet, '\nSentiment:', sentiment.score, sentiment.magnitude, '\n\n')


  #   if counter == max_tweets:
  #     break

  for status in tweepy.Cursor(api.search, q=query, count=max_tweets, lang=lang, result_type=result_type, tweet_mode=tweet_mode).items():
    tweet = preprocess_tweet(status)
    counter += 1
    print(counter)
    if any(keyword in tweet for keyword in ('COVID', 'covid', 'China virus')):
      sentiment = sentiment_analysis(tweet)
      print(tweet, sentiment.score)
      #Store values
      df = pd.DataFrame({'Date':[status.created_at],
        'ID':handle,
        'Tweet':tweet,
        'Sentiment_Score':[sentiment.score],
        'Sentiment_Magnitude':[sentiment.magnitude]})
      print(df)
      tweet_data = tweet_data.append(df, ignore_index=True)
      print(tweet_data)

    if counter == max_tweets:
     break

  print(tweet_data)

  visualize(tweet_data)


if __name__ == "__main__":
  main()
