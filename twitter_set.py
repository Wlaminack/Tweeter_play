#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tweepy
from tweepy import OAuthHandler


def twitter_api_set():
	#gets the twitter keys from the enviromental variables
	consumer_key = os.environ['TWITTER_KEY']
	consumer_secret =os.environ['TWITTER_SECRET']
	access_token =os.environ['TWITTER_ACCESS']
	access_secret =os.environ['TWITTER_ACCESS_SECRET']
	#sets up everthing
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	return api
