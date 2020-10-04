#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLP Test

@author: MeganParsons
"""

# Import Google Client Library and Instantiate a Client
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
client = language.LanguageServiceClient()
# Import Tweepy
import tweepy
# General Imports
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