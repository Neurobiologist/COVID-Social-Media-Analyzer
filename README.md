# EC601-Project02
The purpose of this assignment is to explore the Twitter API and Google Cloud Natural Language ("NLP") API.

# Table of Contents
1. [Securing API Keys](#Securing-API-Keys)
2. [Twitter API: Tweepy](#Twitter-API-Tweepy)
3. [Google NLP API](#Google-NLP-API)
3. [Future Direction](#Future-Direction)
4. [References](#References)
5. [Product Mission](#Product-Mission)
6. [User Story](#User-Story)
7. [Software Implementation & Results](#Software-Implementation-Results)

<a name="Securing-API-Keys"></a>
## Securing API Keys
There were a few options available to secure the API keys used in this demo. The most rudimentary method to _attempt_ to keep API keys secure is to remove them prior to pushing code to GitHub. This method is not at all technically challenging, but it's falliable and prone to human error; therefore, this method is not recommended [[1]](#1). In fact, this type of negligence is responsible for exposed keys in over 100,000 repositories with thousands of new instances every day [[2]](#2). Another potential method of securing API keys involves storing credentials in a separate file in the repository and adding that file to the .gitignore [[3]](#3). This is also a straightforward solution. However, Google best practices for securing API keys recommends that API keys should not be stored in files located inside the application's source tree [[4]](#4). Given these best practices and recommendations, I took a different approach.

My setup includes Conda to manage virtual environments. The Conda documentation includes a section on how to save environment variables [[5]](#5). I used this information to write a Bash script that activates environment variables containing my Twitter API key, API secret, access token, access token secret, and the JSON path to my Google application credentials every time I activate the project environment. A separate Bash script was written to deactivate these environment variables. This way, none of this sensitive information is included in the source code or source tree, and it is not at risk of being uploaded to a GitHub repository. In addition, this method makes it easy to share and collaborate if other contributors use the same nomenclature for their respective API keys and save their personal keys to their own environment variables.

<a name="Twitter-API-Tweepy"></a>
## Twitter API: Tweepy
To verify that I set up the Bash scripts and Tweepy API correctly, I ran a modified "Hello Tweepy" example given in the Tweepy API Introduction [[6]](#6). The example successfully downloads 20 tweets from my 'Home' timeline and prints them to the console. I further modified this code to print my screen name, followers count, and friends list. Twitter also has a useful Cursor object that handles pagination, or the process of iterating through information. I experimented with the Cursor object by iterating through 5 statuses in my timeline.

I noticed that all of my tweets were truncated when printed. As it turns out, there have been changes to the number of allowable characters in certain circumstances over time, and the standard Tweepy API methods allow for a 'compact' or 'extended' parameter, which contains either a truncated or untruncated version of the tweets, respectively [[7]](#7). If the aim is to use information on Twitter for sentiment analysis, we want to ensure that we have the full context of each tweet to be used. Even when applying this initial fix, I noticed that certain tweets were still truncated. As it turns out, retweets must be handled separately with a try/except block, and the code for the handling of this section has been adapted from the Tweepy documentation on Extended Tweets [[7]](#7).

The most useful Tweepy method to gather tweets for sentiment analysis is likely API.search, which "returns a collection of relevant Tweets matching a specified query" [[8]](#8). This method takes a search query and returns search results, with additional parameters to restrict this search to different geographical regions, languages, and type of results (recent vs. popular). Tweepy requires several modifications to return the untruncated version of tweets, starting with the <code>extended_tweet</code> parameter. Then, to access the full tweets, I modified the aforementioned try/catch block for retweets to catch any _AttributeError_ and print the full tweet with the <code>full_text</code> key. This took trial and error, but I validated the results on various search queries in various languages.

Tweepy documentation mentions the <code>RateLimitError</code> exception, and I pre-emptively accounted for this potential issue by setting <code>wait_on_rate_limit</code> and <code>wait_on_rate_limit_notify</code> to True [[9]](#9).

To summarize the test programs, I was able to:

* Get the User object and associated screen name, followers count, and friends list
* Discover that the error message received when an incorrect Twitter handle is passed reads "tweepy.error.TweepError: [{'code': 50, 'message': 'User not found.'}]"
* Write code that catches the incorrect Twitter handle error and displays the message 'User handle <handle> does not exist.' (Can also be modified to request a new handle.)
* Retrieve tweets from my home timeline
* Retrieve tweets from a given Twitter handle
* Modify the number of tweets displayed, from how many pages, and whether the tweets should be truncated or not
* Use the Cursor object to process statuses (and catch Attribute errors)
* Search for specific query or hashtag, filter by language, timeframe, location, result type (recent or popular)
* Most importantly, I was able to retrieve tweets _in full_ according to my specifications, which will be useful for doing sentiment analysis for part 2 of this project
 

<a name="Google-NLP-API"></a>
## Google NLP API
To set up the Google Natural Language API, I relied primarily on the official Google Cloud documentation [[10]](#10),[[11]](#11). To begin, I created a Cloud project and enabled the Google Cloud Language API. I activated the project environment, added credentials to the Bash script, and installed the Cloud Client Library Google Cloud Natural Language for Python. I ran a modified "Analyze some text" example from the NLP API Quickstart documentation and compared the result to the online NLP API demo tool [[12]](#12), [[13]](#13). The results indicated that my setup was working properly. One additional test of the API was performed using <code>analyze_entities</code> to see if entities (proper names and common nouns) were identified correctly throughout various text examples, and this test was also successful [[14]](#14).

To summarize the test programs, I was able to:

* Determine the sentiment score and magnitude of example sentences and verify the results using the online NLP API demo
* Interpret the sentiment score and magnitude values as being "clearly positive", "clearly negative", "neutral", or "mixed", recognizing that some thresholds might have to be adjusted based on the specific details of the application
* Perform entity analysis on a variety of example sentences and verify the results using the online NLP API demo
* Recognize the limitations of sentiment analysis, especially when there is nuanced language used to describe tragic events (this will be important if I do a project related to COVID-19, for instance)

<a name="Future-Direction"></a>
## Future Direction
Now that I understand what an API is and how it works, as well as how to secure information like the API key and other credentials, I think my next step is to organize what I've learned into Python functions that can be called as part of a larger program for part 2 of this project. I am now thinking about the ways in which these APIs can be integrated in useful ways and the user impact that these different types of applications may have.

<a name="Product-Mission"></a>
## Product Mission

<a name="User-Story"></a>
## User Story

<a name="Software-Implementation-Results"></a>
## Software Implementation & Results

<a name="References"></a>
## References
<a id="1">[1]</a> https://developers.google.com/maps/api-key-best-practices

<a id="2">[2]</a> Meli, M., McNiece, M. R., & Reaves, B. (2019). How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories. In NDSS.

<a id="3">[3]</a> Blair. Message to BU EC601 \#class channel. _Slack_, 26 Sept. 2020.

<a id="4">[4]</a> https://cloud.google.com/docs/authentication/api-keys

<a id="5">[5]</a> https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#windows

<a id="6">[6]</a> http://docs.tweepy.org/en/latest/getting_started.html

<a id="7">[7]</a> http://docs.tweepy.org/en/latest/extended_tweets.html

<a id="8">[8]</a> http://docs.tweepy.org/en/v3.5.0/api.html

<a id="9">[9]</a> http://docs.tweepy.org/en/v3.5.0/api.html#tweepy-error-exceptions

<a id="10">[10]</a>https://cloud.google.com/natural-language/docs/quickstart#quickstart-analyze-entities-gcloud

<a id="11">[11]</a> https://cloud.google.com/python/setup

<a id="12">[12]</a> https://cloud.google.com/natural-language/docs/quickstart-client-libraries#client-libraries-usage-python

<a id="13">[13]</a> https://cloud.google.com/natural-language

<a id="14">[14]</a> https://cloud.google.com/natural-language/docs/reference/rest
