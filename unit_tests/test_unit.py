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
from sentiment_analysis import sentiment_analysis
import tkinter as tk
from tkinter import ttk
import tweepy
import os
from google.cloud import language


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
    API_KEY = os.environ.get("TWITTER_API_KEY")
    API_SECRET = os.environ.get("TWITTER_API_SECRET")
    ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Tweepy Authentication
    AUTH = tweepy.OAuthHandler(API_KEY, API_SECRET)
    AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    # Access the API
    API = tweepy.API(AUTH, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    
    # Test values
    test_id_num = 822215347419770882; #MeganMParsons
    user = API.get_user(test_id_num)
    test_tweet = 'Test tweet'
    test_tweet_complex = 'Stronger together! @swetalk & \
    @AnitaB_org  members at the 2020 Congressional Reception! #SWEAdvocacy'
    test_tweet_url = 'https://bit.ly/3mWsCcw'     
    
    def test_user_type(self):
        assert type(self.user) is tweepy.models.User
        
    def test_nonexistent_user(self):
        with pytest.raises(tweepy.TweepError):
            self.API.get_user('asjldfkaowgehnaoifnaosiejf')
    
    

class TestNLP:
    # Access the Google NLP API
    CLIENT = language.LanguageServiceClient()
    
    def test_sentiment_analysis_score_neg(self):
        negative_tweet = 'COVID-19 is a terrible and devastating illness.'
        sentiment = sentiment_analysis(negative_tweet)
        assert sentiment.score == pytest.approx(-0.8)
        
    def test_sentiment_analysis_mag_pos(self):
        negative_tweet = 'COVID-19 is a terrible and devastating illness.'
        sentiment = sentiment_analysis(negative_tweet)
        assert sentiment.magnitude == pytest.approx(0.8)
        
    def test_sentiment_analysis_score_pos(self):
        positive_tweet = 'Scientists are optimistic about the potential for \
        a COVID-19 vaccine soon.'
        sentiment = sentiment_analysis(positive_tweet)
        assert sentiment.score == pytest.approx(0.3)
        
    def test_sentiment_analysis_mag_neut_pos(self):
        positive_tweet = 'Scientists are optimistic about the potential for \
        a COVID-19 vaccine soon.'
        sentiment = sentiment_analysis(positive_tweet)
        assert sentiment.magnitude == pytest.approx(0.3)    
    
    def test_sentiment_analysis_score_neut(self):
        neutral_tweet = 'As scientists, we always strive to issue \
        statements of fact regarding current events.'
        sentiment = sentiment_analysis(neutral_tweet)
        assert sentiment.score == pytest.approx(0)
        
    def test_sentiment_analysis_mag_neut(self):
        neutral_tweet = 'As scientists, we always strive to issue \
        statements of fact regarding current events.'
        sentiment = sentiment_analysis(neutral_tweet)
        assert sentiment.magnitude == pytest.approx(0)
    
    