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
# General Imports
import os

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

def preprocess_tweet(status):
  # Search for specific query and return results
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

def main():
  
  query = '#COVID-19'
  max_tweets = 2
  result_type = 'recent'
  lang = 'en'
  tweet_mode = 'extended'

  for status in tweepy.Cursor(api.search, q=query, count=max_tweets, lang=lang, result_type=result_type, tweet_mode=tweet_mode).items(max_tweets):
    status = preprocess_tweet(status)
    print(status)


  # Return Tweets of interest


if __name__ == "__main__":
  main()
