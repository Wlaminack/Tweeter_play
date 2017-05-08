#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime
import tweepy
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
from twitter_set import twitter_api_set
import Queue
from threading import Thread
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
#Complication from the sqlalchemy 
#that requires a creation of the base class
# for the sql model 
Base = declarative_base()

class Twitter(Base):
	#sqlalchemy base class model
	#table name
    __tablename__ = 'tweets'
    #list of column names
    #at the moment just four 

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    text = Column(String)
    time =Column(DateTime)


    def __repr__(self):
        return "<User(user_id='%s', text='%s', tweet_id='%s')>" % (
                           self.user_id, self.text, self.id)


class Tweeter_to_sql(Thread):
    def __init__(self,queue,Session,Twitter):
        Thread.__init__(self)
        #must pass in the object for the interaction
        self.queue = queue
        self.Twitter=Twitter
        self.session=Session()
    def add_tweet(self,tweet):
        #datetime.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S %z %Y')
        #this is how it should work but f****g 2.7 doesn't support timezones 
        #so we have to remove the time zone
        
        datestring=tweet["created_at"][:-10]+tweet["created_at"][-4:]
        # time zone removed from the text
        dateobject=datetime.datetime.strptime(datestring, '%a %b %d %H:%M:%S %Y')
        tweet_g = self.Twitter(id=tweet["id"], text=tweet["text"], time=dateobject,user_id=tweet["user"]["id"])
        self.session.add(tweet_g)
        self.session.commit()
    def run(self):
        while True:
            data= self.queue.get()
            try:
                #convert the raw data to a json
                tweet=json.loads(data)
                self.add_tweet(tweet)
            except:
                pass
            self.queue.task_done()


class Stream_To_sql(tweepy.StreamListener):
    def __init__(self,Session,Model,Worker_object):
        tweepy.StreamListener.__init__(self)
        self.queue_data=Queue.Queue()
        #use five threads
        for i in range(5):
            #This passes the sqlalchemy model
            worker =Worker_object(self.queue_data,Session,Model)
            worker.daemon = True
            worker.start()
    def on_data(self, data):
        try:
            self.queue_data.put(data)
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True 
    def on_error(self, status):
        print(status)
        return True

if __name__=="__main__":
	api = twitter_api_set()
	location="sqlite:///twitter.db"

	engine = create_engine(location)
	#make sure the tables are created
	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session=Session()
	#how many tweets do you want
	max_tweets=10000

	#starts up the 
	lines=0
	while lines<max_tweets:
		try:
			myStream = tweepy.Stream(auth = api.auth, listener=Stream_To_sql(Session,Twitter,Tweeter_to_sql))
			# trackes only english language posts and anything with "ts" and "i"
			#this is only a sample 
			myStream.filter(languages=['en'],track=["ts","i"])
		except:
			print("break")
		
		#at a break in the twitter issue count the number of rows in the db
		lines = session.query(Twitter).count()
