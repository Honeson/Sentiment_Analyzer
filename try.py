import pandas as pd
import twint

all_tweets = 'work.csv'
df = pd.read_csv(all_tweets)


#print(df.head())

c = twint.Config()
c.Search = 'Buhari'
c.Since = '2019-01-19'
c.Until = '2019-02-19'
#c.Custom["tweets"] = ["id", "created_at", "retweets", "source", "likes_count"]
#c.Limit = 50
c.Output = "work2.csv"
c.Store_csv = True
twint.run.Search(c)
