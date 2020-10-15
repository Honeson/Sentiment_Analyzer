from tweepy import API, Cursor, OAuthHandler, Stream
from tweepy.streaming import StreamListener
from textblob import TextBlob
import credentials_from_twitter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import re
import csv
import twint



# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client



# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials_from_twitter.CONSUMER_KEY, credentials_from_twitter.CONSUMER_SECRET)
        auth.set_access_token(credentials_from_twitter.ACCESS_TOKEN, credentials_from_twitter.ACCESS_TOKEN_SECRET)
        return auth



# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(locations=[2.69170169436, 4.24059418377, 14.5771777686, 13.8659239771])



# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                    tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)



class TweetCollector():
    """
    Functionality to collect tweets and store it in a csv file specified.
    """
    def collect_tweets_and_store_as_csv_file(self, tweets):
        with open('OfficialAPCNg3.csv', 'a+', encoding='utf-8-sig') as all_tweets:
            csv_writer = csv.writer(all_tweets)
            for line in tweets:
                row = [line.text, line.id, len(line.text), line.created_at, line.source, line.favorite_count, line.retweet_count]
                csv_writer.writerow(row)


   




if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_collector = TweetCollector()

    api = twitter_client.get_twitter_client_api()

    #This is used to get the tweets from APC Handle
    tweets = api.user_timeline(
        screen_name="OfficialAPCNg", 
        #since-_id=
        max_id=1069208235419280000,
        count=200,
        include_rts=1)


    c = twint.Config()
    c.Search = 'APC'
    c.Since = '2019-01-19'
    c.Until = '2019-02-19'
    #c.Custom["tweets"] = ["id", "created_at", "retweets", "source", "likes_count"]
    #c.Limit = 50
    #c.Output = "work2.csv"
    c.Store_object = True
    c.Store_csv = True
    twint.run.Search(c)
    #c.Limit = 50
    tweets_as_objects = twint.output.tweets_list
    #c.Output = tweets_as_objects
    
    #print(tweets_as_objects)

    #Using the class object to call the function that stores tweets in a csv file
    tweet_collector.collect_tweets_and_store_as_csv_file(tweets_as_objects)
    