import tweepy
import json
import pickle
import pandas as pd

# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser

# set non scientific notation
pd.set_option('display.float_format', '{:.5f}'.format)

# Replace keys and tokens
consumer_key = "xxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxx"

# attempt authentication
try:
    # create OAuthHandler object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # create tweepy API object to fetch tweets
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    print("Authentication Successfull")
except:
    print("Error: Authentication Failed")

# Specify the time of intervals when targeted tweets start collecting, (you can only get tweets in a week)
date_since = "2021-8-20"

# Specify other variables for pass the rate
maxTweets = 100000 # Some arbitrary large number, you can change it to 1000000000000000000000000, or even more
tweetsPerQry = 100  # this is the max the API permits

# This is where we specify our query
query = "Totoro OR Walle OR \'Wall E\'" + "-filter:retweet" + "-filter:replies" + "is:verified" #Unfortunatedly, is:verified does not work

# If results from a specific ID onwards are required, set since_id to that ID.
# Otherwise default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1
tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

# pull out the tweets

tweets_list = list()

while tweetCount < maxTweets:
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=query, lang="en", since=date_since, include_entities=True, count=tweetsPerQry)
            else:
                new_tweets = api.search(q=query, lang="en", since=date_since, include_entities=True,  count=tweetsPerQry, since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q=query, lang="en", since=date_since, include_entities=True, count=tweetsPerQry, max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q=query, lang="en", since=date_since, include_entities=True, count=tweetsPerQry, max_id=str(max_id - 1), since_id=sinceId)
        if not new_tweets:
            print("No more tweets found")
            break

        for tweets in new_tweets:
            tweets_list.append(tweets._json)

        tweetCount += len(new_tweets)
        print("Downloaded {0} tweets".format(tweetCount))
        max_id = new_tweets[-1].id

    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break

print("Downloaded {0} tweets, Saved to {1}")

# Here we are parsing tweets to json file
# save json and txt file, in case the json file is huge
with open("../sample output/tweetscartoonv1.txt", 'wb') as txtfile:
    pickle.dump(tweets_list, txtfile)

with open("../sample output/tweetscartoonv1.json", "w") as jsonfile:
    json.dump(tweets_list, jsonfile, indent=4)

## in case the following parsing data cannot go through, we need to load those files
# with open("../sample output/tweetscartoonv1.txt", 'rb') as txtfile:
# tweets_list = pickle.load(txtfile)
# with open('../sample output/tweetscartoonv1.json') as jsonfile:
# tweets_list = json.load(jsonfile)

# parse the data to a data frame
count = 0
tweet_list = list()
for tweet in tweets_list:
    # Create variables for each tweet
    # Some of the keys might not exist for some tweets, so we need to use try and except
    # Author properties
    author_id = tweet['user']["id"]
    author_account = tweet['user']['screen_name']
    author_name = tweet['user']['name']
    author_description = tweet['user']['description']
    try:
        location = tweet['user']['location']
    except KeyError:
        location = " "
    author_followers = tweet['user']['followers_count']
    author_friend = tweet['user']['friends_count']
    author_verified = tweet['user']["verified"]
    # author_tweets_num = tweet['user']['public_metrics']['tweet_count']
    author_created = dateutil.parser.parse(tweet['user']['created_at'])

    # Tweet properties: Time created
    created_at = dateutil.parser.parse(tweet['created_at'])
    # Tweet ID
    tweet_id = tweet['id']
    # Language
    lang = tweet['lang']
    # Tweet metrics
    retweet_count = tweet['retweet_count']
    # reply_count = tweet['reply_count']
    like_count = tweet['favorite_count']
    # quote_count = tweet['public_metrics']['quote_count']
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
    res = [author_id, author_account, author_name, author_description, location, author_friend, author_followers,
           author_verified,
           author_created, text, created_at, tweet_id, lang, hashtag, like_count, retweet_count, source]
    tweet_list.append(res)
    count = count + 1

tweetsdata = pd.DataFrame(tweet_list,
                          columns=['author_id', 'author_account', 'author_name', 'author_description', 'location',
                                   'author_friend', 'author_followers', 'author_verified', 'author_created', 'text',
                                   'created_at', 'tweet_id', 'lang', 'hashtag', 'like_count', 'retweet_count',
                                   'source'])

tweetsdata.to_csv("../sample output/tweetscartoonv1.csv", index=False, encoding="utf-8")
