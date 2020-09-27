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
api = tweepy.API(auth)

# Get the User object
id='SWE_grad'
user = api.get_user(id)
print('Screen Name: ', user.screen_name)
print('Followers Count: ', user.followers_count)
# for friend in user.friends():
#   print(friend.screen_name)

# Pull home timeline associated with personal account @MeganMParsons
public_tweets = api.home_timeline(tweet_mode='extended')
for tweet in public_tweets:
    print(tweet.full_text)     # UPDATE: Full text
    print('\n\n')

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

