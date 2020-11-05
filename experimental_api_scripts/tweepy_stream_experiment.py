#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ece-student
"""

import tweepy
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False
        
def main():
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
    lang='en'
    realDonaldTrump='25073877'
    track='covid,covid19,covid-19,coronavirus,china virus'
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(follow=[realDonaldTrump],track=[track])
    

if __name__ == "__main__":
  main()