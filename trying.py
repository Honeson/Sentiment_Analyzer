from tweepy import API, OAuthHandler
import credentials_from_twitter
import csv
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client



class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials_from_twitter.CONSUMER_KEY, credentials_from_twitter.CONSUMER_SECRET)
        auth.set_access_token(credentials_from_twitter.ACCESS_TOKEN, credentials_from_twitter.ACCESS_TOKEN_SECRET)
        return auth


class TweetCollector():
    """
    Functionality to collect tweets and store it in a csv file specified.
    """
    def collect_tweets_and_store_as_csv_file(self, tweets):
        with open('trying8.csv', 'a+', encoding='utf-8-sig') as all_tweets:
            csv_writer = csv.writer(all_tweets)
            for line in tweets:
                row = [line.text, line.id, len(line.text), line.created_at, line.source, line.favorite_count, line.retweet_count, line.geo]
                csv_writer.writerow(row)



if __name__ == "__main__":
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    tweet_collector = TweetCollector()

    tweets = api.search(
        q='APC%20OR%20Buhari%20OR%20vote%20Buhari%20OR%20vote%20APC%20OR%20%23Buhari%20OR%20%40Buhari',
        max_id='1282693856644018176',
        count=100)
        #&geocode=6.465422, 3.406448, 1km'

    tweet_collector.collect_tweets_and_store_as_csv_file(tweets)