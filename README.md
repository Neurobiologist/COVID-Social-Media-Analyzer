# EC601-Project02
The purpose of this assignment is to explore the Twitter API and Google Cloud Natural Language ("NLP") API.

## Securing API Keys
There were a few options available to secure the API keys used in this demo. The most rudimentary method to _attempt_ to keep API keys secure is to remove them prior to pushing code to GitHub. This method is not at all technically challenging, but it's falliable and prone to human error; therefore, this method is not recommended [[1]](#1). In fact, this type of negligence is responsible for exposed keys in over 100,000 repositories with thousands of new instances every day [[2]](#2). Another potential method of securing API keys involves storing credentials in a separate file in the repository and adding that file to the .gitignore [[3]](#3). This is also a straightforward solution. However, Google best practices for securing API keys recommends that API keys should not be stored in files located inside the application's source tree [[4]](#4). Given these best practices and recommendations, I took a different approach.

My setup includes Conda to manage virtual environments. The Conda documentation includes a section on how to save environment variables [[5]](#5). I used this information to write a Bash script that activates environment variables containing my Twitter API key, API secret, access token, access token secret, and the JSON path to my Google application credentials every time I activate the project environment. A separate Bash script was written to deactivate these environment variables. This way, none of this sensitive information is included in the source code or source tree, and it is not at risk of being uploaded to a GitHub repository. In addition, this method makes it easy to share and collaborate if other contributors use the same nomenclature for their respective API keys and save their personal keys to their own environment variables.

## Twitter API: Tweepy
To verify that I set up the Bash scripts and Tweepy API correctly, I ran a modified "Hello Tweepy" example given in the Tweepy API Introduction [[6]](#6). The example successfully downloads 20 tweets from my 'Home' timeline and prints them to the console. I further modified this code to print my screen name, followers count, and friends list. Twitter also has a useful Cursor object that handles pagination, or the process of iterating through information. I experimented with the Cursor object by iterating through 5 statuses in my timeline.

I noticed that all of my tweets were truncated when printed. As it turns out, there have been changes to the number of allowable characters in certain circumstances over time, and the standard Tweepy API methods allow for a 'compact' or 'extended' parameter, which contains either a truncated or untruncated version of the tweets, respectively [[7]](#7). If the aim is to use information on Twitter for sentiment analysis, we want to ensure that we have the full context of each tweet to be used. Even when applying this initial fix, I noticed that certain tweets were still truncated. As it turns out, retweets must be handled separately with a try/except block, and the code for the handling of this section has been adapted from the Tweepy documentation on Extended Tweets [[7]](#7).

The most useful Tweepy method to gather tweets for sentiment analysis is likely API.search, which "returns a collection of relevant Tweets matching a specified query" [[8]](#8). This method takes a search query and returns search results, with additional parameters to restrict this search to different geographical regions, languages, and type of results (recent vs. popular). Tweepy requires several modifications to return the untruncated version of tweets, starting with the <code>extended_tweet</code> parameter. Then, to access the full tweets, I modified the aforementioned try/catch block for retweets to catch any _AttributeError_ and print the full teet with the <code>full_text</code> key. This took trial and error, but I validated the results on various search queries in various languages.

## Google NLP API
To set up the Google Natural Language API, I relied primarily on the official Google Cloud documentation [[9]](#9),[[10]](#10). To begin, I created a Cloud project and enabled the Google Cloud Language API. I activated the project environment, added credentials to the Bash script, and installed the Cloud Client Library Google Cloud Natural Language for Python. I ran a modified "Analyze some text" example from the NLP API Quickstart documentation and compared the result to the online NLP API demo tool [[11]](#11), [[12]](#12). The results indicated that my setup was working properly. One additional test of the API was performed using <code>analyze_entities</code> to see if entities (proper names and common nouns) were identified correctly throughout various text examples, and this test was also successful [[13]](#13).

## References
<a id="1">[1]</a> https://developers.google.com/maps/api-key-best-practices

<a id="2">[2]</a> Meli, M., McNiece, M. R., & Reaves, B. (2019). How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories. In NDSS.

<a id="3">[3]</a> Blair. Message to BU EC601 \#class channel. _Slack_, 26 Sept. 2020.

<a id="4">[4]</a> https://cloud.google.com/docs/authentication/api-keys

<a id="5">[5]</a> https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#windows

<a id="6">[6]</a> http://docs.tweepy.org/en/latest/getting_started.html

<a id="7">[7]</a> http://docs.tweepy.org/en/latest/extended_tweets.html

<a id="8">[8]</a> http://docs.tweepy.org/en/v3.5.0/api.html

<a id="9">[9]</a> https://cloud.google.com/natural-language/docs/quickstart#quickstart-analyze-entities-gcloud

<a id="10">[10]</a> https://cloud.google.com/python/setup

<a id="11">[11]</a> https://cloud.google.com/natural-language/docs/quickstart-client-libraries#client-libraries-usage-python

<a id="12">[12]</a> https://cloud.google.com/natural-language

<a id="13">[13]</a> https://cloud.google.com/natural-language/docs/reference/rest
