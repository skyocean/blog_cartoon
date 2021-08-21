from twarc import Twarc2, expansions
import json
import pickle
import pandas as pd


# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser

# set non scientific notation
pd.set_option('display.float_format', '{:.5f}'.format)

# Replace your bearer token below
client = Twarc2(bearer_token="xxxxxxxxx")

# Specify the start time in UTC of the time interval when targeted tweets were posted
start_time = datetime.datetime(2019, 5, 1, 0, 0, 0, 0, datetime.timezone.utc)

# Specify the end time in UTC of the time interval when targeted tweets were posted
end_time = datetime.datetime(2021, 7, 1, 0, 10, 0, 0, datetime.timezone.utc)

# This is where we specify our query
query = "(Totoro OR Walle OR\"Wall-E\") lang:en is:verified -is:retweet"

# The search_all method call the full-archive search endpoint to get Tweets based on the query, start and end time
search_results = client.search_all(query = query, start_time = start_time, end_time = end_time, max_results = 100)
# Build an empty list for later store the results
tweets_list = list()
# Twarc returns all Tweets for the criteria set above, so we page through the results
for page in search_results:
    # The Twitter API v2 returns the Tweet information and the user, media etc.,separately
    # so we use expansions.flatten to get all the information in a single JSON
    result = expansions.flatten(page)
    for tweets in result:
        # Here we are parsing tweets to json file
        tweets_list.append(tweets)

# save json and txt file, in case the json file is huge
with open("tweetscartoon.txt", 'wb') as txtfile:
    pickle.dump(tweets_list, txtfile)

with open("tweetscartoon.json", "w") as jsonfile:
    json.dump(tweets_list, jsonfile, indent = 4)

## In case the following parsing data cannot go through, we need to load those files
#with open("tweetscartoon.txt", 'rb') as txtfile:
    #tweets_list = pickle.load(txtfile)
#with open('tweetscartoon.json') as jsonfile:
    #tweets_list = json.load(jsonfile)

# Parse the data to a data frame
count = 0
tweet_list = list()
for tweet in tweets_list:
    # Create variables for each tweet
    # Some of the keys might not exist for some tweets, so we need to use try and except
    # Author properties
    author_id = tweet['author_id']
    author_account = tweet['author']['username']
    author_name = tweet['author']['name']
    author_description = tweet['author']['description']
    try:
        location = tweet['author']['location']
    except KeyError:
        location = " "
    author_followers = tweet['author']['public_metrics']['followers_count']
    author_followees = tweet['author']['public_metrics']['following_count']
    author_tweets_num = tweet['author']['public_metrics']['tweet_count']
    author_created = dateutil.parser.parse(tweet['author']['created_at'])

    # Tweet properties: Time created
    created_at = dateutil.parser.parse(tweet['created_at'])
    # Tweet ID
    tweet_id = tweet['id']
    # Language
    lang = tweet['lang']
    # Tweet metrics
    retweet_count = tweet['public_metrics']['retweet_count']
    reply_count = tweet['public_metrics']['reply_count']
    like_count = tweet['public_metrics']['like_count']
    quote_count = tweet['public_metrics']['quote_count']
    # source
    source = tweet['source']
    # Tweet text
    text = tweet['text']
    # hashtag
    try:
        hashtag = ' '.join(tags['tag'] for tags in tweet['entities']['hashtags'])
    except KeyError:
        hashtag = " "

    # Assemble all data in a list
    res = [author_id, author_account, author_name, author_description, author_followees, author_followers, author_tweets_num,
           author_created, text, created_at, tweet_id, lang, hashtag, like_count, quote_count, reply_count, retweet_count,
           source]
    tweet_list.append(res)
    count = count + 1

# Coverse the list to the data frame
tweetsdata = pd.DataFrame(tweet_list, columns = ['author_id', 'author_account', 'author_name', 'author_description', 'author_followees', 'author_followers', 'author_tweets_num', 'author_created', 'text', 'created_at', 'tweet_id', 'lang', 'hashtag', 'like_count', 'quote_count', 'reply_count','retweet_count', 'source'])

# save the data frame
tweetsdata.to_csv("tweetscartoon.csv", index = False, encoding="utf-8")
