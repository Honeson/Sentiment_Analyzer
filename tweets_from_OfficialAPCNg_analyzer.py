from textblob import TextBlob
import credentials_from_twitter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import re
import csv



class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
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
def sum_sentiments(df):
    positive_sentiments = negative_sentiments = neutral_sentiments = 0
    for sentiment in df['Sentiment']:
        if sentiment==1:
            positive_sentiments+=1
        elif sentiment==-1:
            negative_sentiments+=1
        else:
            neutral_sentiments+=1
    print("\n")
    print("The Total Positive Sentiments (Sentiments Supporting APC) in OffialAPCNg is ",positive_sentiments)
    print("The Total Negtative Sentiments (Sentiments Against APC) in OffialAPCNg is ",negative_sentiments)
    print("The Total Neutral Sentiments (Sentiments that is Neutral) in OffialAPCNg is ",neutral_sentiments)

class PlotLikesRetweetsPolarity():

    def plot_dist_of_likes_and_retweets(self, df):
        plt.style.use('ggplot')
        time_likes = pd.Series(data=df['Likes'].values, index=df['Date'])
        time_likes.plot(color='r', label="Likes")
        time_retweets = pd.Series(data=df['Retweets'].values, index=df['Date'])
        time_retweets.plot(color='b', label="Retweets")
        plt.title("Likes and Retweets for Tweets Analyzed From OfficailAPCNg", fontsize=15)
        plt.savefig('APC_LIKES_RETWEETS.png')
        plt.legend()
        plt.show()

    def plot_dist_of_APC_polarity(self, df):
        polarity = df['Sentiment']
        p = sns.distplot(polarity, color="r",)
        p.set_title("APC Tweet Polarity", fontsize=20)
        p.set_xlabel('← Negative — — — — Positive →', fontsize=15)
        plt.tight_layout()
        plt.savefig('distribution_plot_for_apc_polarity.png')
        plt.show()

    
if __name__ == '__main__':

    tweet_analyzer = TweetAnalyzer()
   

    all_tweets = 'OfficialAPCNg.csv'
    df = pd.read_csv(all_tweets, names=['Tweets', 'ID', 'Len', 'Date', 'Source', 'Likes', 'Retweets'])

    df['Sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['Tweets']])
    print(df.head(20))

    plot_likes_retweets_polarity = PlotLikesRetweetsPolarity()

    #Get the total of Positive, Negative and Neutral Sentiments for APC in OfficialAPCNg
    sum_sentiments(df)
    
    #Display the plots     
    plot_likes_retweets_polarity.plot_dist_of_likes_and_retweets(df)
    plot_likes_retweets_polarity.plot_dist_of_APC_polarity(df)

    print(df.head(40))