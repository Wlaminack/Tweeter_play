# Tweeter_play
Playing around with the twitter stream
While the Tweepy gives a good base streaming class I have exanded it for two possiblities
The first is to write the tweets to a json file. This is the Twitter_Add_JSON.py file.
The second is to write the tweets to a relational db. This is done in the Twitter_Add_SQL.py file.
These are two simple files for downloading data from the twitter data stream.

# Documentation
In order to do use the programes, you have to setup 4 envromental variables
* ['TWITTER_KEY']
* ['TWITTER_SECRET']
* ['TWITTER_ACCESS']
* ['TWITTER_ACCESS_SECRET']

With the access keys provided by twitter for your application
If you really don't want to set up the evniromental variables you can just change the twitter_set.py, but this is not recomended.
