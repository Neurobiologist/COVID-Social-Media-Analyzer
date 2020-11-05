#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 20:12:35 2020

@author: ece-student
"""
# Import statements
import pytest
import unittest
from sentiment_analysis import evaluate
from sentiment_analysis import mkr
import tkinter as tk
from tkinter import ttk
import tweepy
import os


class TestUnit:
    
    # Expected Behavior
    
    def test_evaluate_pos(self):
        assert evaluate(0.5) == '+'
    
    def test_evaluate_neutral(self):
        assert evaluate(0) == ' '
        
    def test_evaluate_edge(self):
        assert evaluate(0.2) == ' '
        
    def test_evaluate_neg(self):
        assert evaluate(-3) == 'v'
        
    def test_mkr_pos(self):
        assert mkr('+') == 'b'
        
    def test_mkr_neutral(self):
        assert mkr(' ') == 'k'
        
    def test_mkr_neg(self):
        assert mkr('v') == 'r'
        
class TestTKinter(unittest.TestCase):
    
    def setUp(self):
        self.app = ttk.Combobox()

    def tearDown(self):
        self.app.destroy()

    def test_button(self):
       # Need to debug. Unit tests for Tk are particularly tricky.
       pass

class TestTweepy:
    
    # Basic | With API Call [Not Recommended] 
    # Fetch Twitter API key and access token from environment variables
    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Authentication
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # Access the API
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    
    # Test values
    test_id_num = 822215347419770882; #MeganMParsons
    test_ids = ['MeganMParsons','SWE_grad','asjldfkaowgehnaoifnaosiejf']
    
    test_tweet = 'Test tweet'
    test_tweet_complex = 'Stronger together! @swetalk & \
    @AnitaB_org  members at the 2020 Congressional Reception! #SWEAdvocacy'
    test_tweet_url = 'https://bit.ly/3mWsCcw'
    
    #@patch.object(tweepy.API, 'get_user', return_value=twitter_data())
    user = api.get_user(test_id_num)
    
    def test_user_type(self):
        assert type(self.user) is tweepy.models.User
        
    def test_nonexistent_user(self):
        with pytest.raises(tweepy.TweepError):
            self.api.get_user('asjldfkaowgehnaoifnaosiejf')
    
    
    
    
    # Advanced
        
    