#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tweepy Test
@author: MeganParsons
"""

import tweepy
import os

api_key = os.environ.get("TWITTER_API_KEY")
api_secret = os.environ.get("TWITTER_API_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Pull home timeline associated with personal account @MeganMParsons
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)