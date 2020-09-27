# EC601-Project02
The purpose of this assignment is to explore the Twitter API and Google Cloud Natural Language ("NLP") API.

## Securing API Keys
There were a few options available to secure the API keys used in this demo. The most rudimentary method to _attempt_ to keep API keys secure is to remove them prior to pushing code to GitHub. This method is not at all technically challenging, but it's falliable and prone to human error; therefore, this method is not recommended[[1]](#1). In fact, this type of negligence is responsible for exposed keys in over 100,000 repositories with thousands of new instances every day[[2]](#2). Another potential method of securing API keys involves storing credentials in a separate file in the repository and adding that file to the .gitignore[[3]](#3). This is also a straightforward solution. However, Google best practices for securing API keys recommends that API keys should not be stored in files located inside the application's source tree[[4]](#4). Given these best practices and recommendations, I took a different approach.

## Twitter API: Tweepy


## Google NLP API
To set up the Google Natural Language API, I relied primarily on the official Google Cloud documentation.

## References
<a id="1">[1]</a> https://developers.google.com/maps/api-key-best-practices

<a id="2">[2]</a> Meli, M., McNiece, M. R., & Reaves, B. (2019). How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories. In NDSS.

<a id="3">[3]</a> Blair. Message to BU EC601 \#class channel. _Slack_, 26 Sept. 2020.

<a id="4">[4]</a> https://cloud.google.com/docs/authentication/api-keys
