#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime
import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class MyStreamListener(tweepy.StreamListener):
	def __init__(self,location):
		tweepy.StreamListener.__init__(self)
		self.location=location

	def on_data(self, data):
		try:
			with open(self.location, 'a') as f:
				f.write(data)
				return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self, status):
		print(status)
		return True

if __name__=="__main__":
	#gets the twitter keys from the enviromental variables
	consumer_key = os.environ['TWITTER_KEY']
	consumer_secret =os.environ['TWITTER_SECRET']
	access_token =os.environ['TWITTER_ACCESS']
	access_secret =os.environ['TWITTER_ACCESS_SECRET']
	#sets up everthing
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	##Location you want to write to
	location="tweeter_data.json"
	#how many tweets do you want
	max_tweets=10000

	#starts up the 
	lines=0
	while lines<max_tweets:
		try:
			myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener(location))
			#myStream.filter(track=['t'])
			myStream.filter(languages=['en'],track=["ts","i"])
		except:
			print("yep")
			pass
		#at a break in the twitter issue count the number of lines in the file
		lines=int(subprocess.check_output(['wc','-l',location]).split()[0])
