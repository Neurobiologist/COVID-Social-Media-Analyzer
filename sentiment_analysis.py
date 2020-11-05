#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentiment Analysis Project
@author: MeganParsons
"""

# Import GUI package
import tkinter as tk
from tkinter import ttk
# General Imports
import os
import datetime
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import numpy as np
# Import Google Client Library
from google.cloud import language
# Import Tweepy
import tweepy
# Import COVID-19 Data API
import COVID19Py

# Pandas Settings
pd.set_option('max_colwidth', 280)  # Capture full tweet
pd.set_option("display.max_rows", None, "display.max_columns", None)
# Handle date time conversions between pandas and matplotlib
register_matplotlib_converters()

# Fetch Twitter API key and access token from environment variables
API_KEY = os.environ.get("TWITTER_API_KEY")
API_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Tweepy Authentication
AUTH = tweepy.OAuthHandler(API_KEY, API_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Access the Tweepy API
API = tweepy.API(AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# Access the Google NLP API
CLIENT = language.LanguageServiceClient()
# Access the COVID19Py API
COVID = COVID19Py.COVID19(
    url='https://covid19-api.kamaropoulos.com')   # Mirror


def preprocess_tweet(status):
    ''' Return full text of tweet '''
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
    ''' Sentiment analysis on input '''
    document = language.types.Document(
        content=tweet,
        type='PLAIN_TEXT')

    response = CLIENT.analyze_sentiment(
        document=document,
        encoding_type='UTF32',
    )

    sentiment = response.document_sentiment

    return sentiment


def evaluate(score):
    ''' Sentiment analysis interpretation '''
    if score > 0.2:
        return '+'
    if -0.2 <= score <= 0.2:
        return ' '
    return 'v'


def mkr(interp):
    ''' Assign marker based on interpretation '''
    if interp == '+':
        return 'b'
    if interp == ' ':
        return 'k'
    return 'r'


def tweet_polarity(tweet_data):
    ''' Plot histogram of tweet data '''
    plt.hist(tweet_data['Sentiment_Score'], bins='auto')
    plt.title(
        'COVID-19 Sentiment Distribution for @{}'.format(tweet_data['ID'][0]))
    plt.xlabel('Sentiment Score')
    plt.xlim(-1, 1)
    plt.show()
    plt.savefig('tweet_data.png')


def covid_plot(tweet_data, covid_data):
    ''' Create plot of COVID-19 data '''
    _, ax_plot = plt.subplots(2, 1, sharex=True, figsize=(20, 10))
    ax_plot[0].plot(covid_data['Date'], covid_data['Confirmed Cases'])
    ax_plot[0].set_title('Cases of COVID-19 in the United States')
    ax_plot[0].set_ylabel('Confirmed Cases of COVID-19')

    # Create plot of Twitter Sentiment and Magnitude Data
    for x_idx, y_idx, sent_idx, color_idx, marker_idx in zip(
            tweet_data['Date'].to_list(),
            tweet_data['Sentiment_Mag'].to_list(),
            100 * np.ones(len(
                tweet_data['Marker Color'].to_list())),
            tweet_data['Marker Color'].to_list(),
            tweet_data['Interpretation'].to_list()):
        ax_plot[1].scatter(
            x_idx,
            y_idx,
            s=sent_idx,
            c=color_idx,
            marker=marker_idx)
    ax_plot[1].set_title('COVID-19 Tweet Sentiment')
    ax_plot[1].set_ylabel('Sentiment Magnitude')
    ax_plot[1].tick_params(axis='x', rotation=45)

    # Format plots
    plt.tight_layout()
    plt.xlabel('Date')
    plt.show()
    plt.savefig('covid_plot.png')


def visualize(tweet_data, covid_data):
    ''' Create visualizations of data '''
    tweet_polarity(tweet_data)    # Overview of Tweet Data
    covid_plot(tweet_data, covid_data)


def select_fn(acct):
    ''' Administrivia for acct '''
    print(acct.get())


def main():
    ''' COVID-19 Correlator '''
    # Dropdown Menu for Twitter Account Selection
    # Create window
    window = tk.Tk()
    window.title('Select Twitter Account to Analyze')
    window.geometry('250x200')

    # Instructions
    ttk.Label(window, text="Select Twitter Account to Analyze:",
              font=("Times New Roman", 10)).grid(column=0,
                                                 row=5, padx=10, pady=25)

    # Create Combobox
    acct = tk.StringVar()
    selection = ttk.Combobox(
        window, width=27, textvariable=acct, state='readonly')

    # Dropdown Options
    selection['values'] = ('realDonaldTrump', 'CDCgov',
                           'JoeBiden', 'CDCDirector')
    selection.grid(column=0, row=6)
    selection.bind('<<ComboboxSelected>>', select_fn(acct))
    selection.current(0)

    button = tk.Button(window, text="Analyze", command=window.destroy)
    button.grid(column=0, row=8)

    window.mainloop()

    # Process COVID-19 Data
    location = COVID.getLocationByCountryCode("US", timelines=True)
    raw_data = location[0]['timelines']['confirmed']['timeline']
    covid_data = pd.DataFrame.from_dict(raw_data, orient='index')
    covid_data = covid_data.reset_index()
    covid_data.columns = ['Date', 'Confirmed Cases']
    covid_data['Date'] = pd.to_datetime(
        covid_data.Date, format='%Y-%m-%dT%H:%M:%SZ')

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
    for status in tweepy.Cursor(
            API.search,
            q=query,
            count=max_tweets,
            lang=lang,
            result_type=result_type,
            tweet_mode=tweet_mode).items(max_tweets):
        tweet = preprocess_tweet(status)
        if any(keyword in tweet for keyword in (
                'COVID', 'covid', 'China virus', 'coronavirus')):

            # Sentiment analysis
            sentiment = sentiment_analysis(tweet)

            # Date Time format
            date_time_str = str(status.created_at)
            date_time = datetime.datetime.strptime(
                date_time_str, '%Y-%m-%d %H:%M:%S')

            # Store values
            pd_df = pd.DataFrame({'Date': [date_time],
                                  'ID': handle,
                                  'Tweet': tweet,
                                  'Sentiment_Score': [sentiment.score],
                                  'Sentiment_Mag': [sentiment.magnitude]})
            tweet_data = tweet_data.append(pd_df, ignore_index=True)

    tweet_data['Date'] = pd.to_datetime(
        tweet_data['Date'], format='%Y-%m-%d %H:%M:%S')
    tweet_data['Interpretation'] = tweet_data.apply(lambda row: evaluate(
        row['Sentiment_Score']), axis=1)
    tweet_data['Marker Color'] = tweet_data.apply(
        lambda row: mkr(row['Interpretation']), axis=1)

    visualize(tweet_data, covid_data)


if __name__ == "__main__":
    main()
