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



class TweetAnalyzer():
    """
    Functionality to remove unwanted characters from collected tweets. This is where the data is preprocesses.
    """
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1




if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    #This is used to get the tweets from APC Handle
    tweets = api.user_timeline(screen_name="OfficialAPCNg", max_id=1070919575338920000, count=1000)

    #The following stores the collected tweets in a csv file
    with open('tweets_now13.csv', 'w+', encoding='utf-8-sig') as all_tweets:
        csv_writer = csv.writer(all_tweets)
        for line in tweets:
            row = [line.text, line.id, len(line.text), line.created_at, line.source, line.favorite_count, line.retweet_count]
            csv_writer.writerow(row)
    