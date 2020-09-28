#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tweepy Test
@author: MeganParsons
"""

import tweepy
import os

# Fetch Twitter API key and access token from environment variables
api_key = os.environ.get("TWITTER_API_KEY")
api_secret = os.environ.get("TWITTER_API_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Authentication
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

# Access the API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Get the User object and Catch Errors
print('########### TEST 01 #################################')
ids = ['MeganMParsons','SWE_grad','asjldfkaowgehnaoifnaosiejf']
for id in ids:
  try:
    user = api.get_user(id)
    print('Screen Name: ', user.screen_name)
    print('Followers Count: ', user.followers_count)
    for friend in user.friends():
      print(friend.screen_name)
  except tweepy.TweepError:
    print('User handle', id, 'does not exist.')
    break

print('########### TEST 02 #################################')

# Pull home timeline associated with personal account @MeganMParsons
user = api.get_user('MeganMParsons')
public_tweets = api.home_timeline(tweet_mode='extended')
for tweet in public_tweets:
    print(tweet.full_text)     # UPDATE: Full text
    print('\n\n')

# Pull recent statuses from user specified
id = 'SWE_grad'
count = 5
page = 1
public_tweets = api.user_timeline(id,count=count, page=page, tweet_mode='extended')
for tweet in public_tweets:
  print(tweet.full_text)
  print('\n\n')

print('########### TEST 03 #################################')
# Use Cursor object to process first 5 statuses
for status in tweepy.Cursor(api.user_timeline, id=id, tweet_mode='extended').items(5):
  if hasattr(status, 'retweeted_status'):   # Check if retweet
    try:
      print(status.retweeted_status.text, '\n')
    except AttributeError:
      print(status.retweeted_status.full_text, '\n')
  else:
    try:
      print(status.extended_tweet['full_text'], '\n')
    except AttributeError:
      print(status.full_text, '\n')

print('########### TEST 04 #################################')
# Search for specific query and return results
query = '#COVID-19'
max_tweets = 10
result_type = 'recent'
lang = 'en'
tweet_mode = 'extended'
for status in tweepy.Cursor(api.search, q=query, count=max_tweets, lang=lang, result_type=result_type, tweet_mode=tweet_mode).items(max_tweets):
  if hasattr(status, 'retweeted_status'):   # Check if retweet
    try:
      print(status.retweeted_status.text, '\n')
    except AttributeError:
      print(status.retweeted_status.full_text, '\n')
  else:
    try:
      print(status.extended_tweet.full_text, '\n')
    except AttributeError:
      print(status.full_text, '\n')