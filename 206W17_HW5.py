import unittest
import tweepy
import requests
import json
import twitter_info
import codecs

## SI 206 - W17 - HW5
## Miguel Martinez



##code that uses the tweepy library to search for tweets with a phrase of the user's choice (should use the Python input function), and prints out the Tweet text and the created_at value (note that this will be in GMT time) of the first THREE tweets with at least 1 blank line in between each of them, e.g.

## TEXT: I'm an awesome Python programmer.
## CREATED AT: Sat Feb 11 04:28:19 +0000 2017

## TEXT: Go blue!
## CREATED AT: Sun Feb 12 12::35:19 +0000 2017


consumer_key = twitter_info.consumer_key 
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser()) 
# Set up library to grab stuff from twitter with authentication, and return it in a JSON-formatted way


CACHE_FNAME = "cached_data_socialmedia.json"
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


def get_tweets(search):
	unique_identifier = "{}".format(search)
	if unique_identifier in CACHE_DICTION:
		print('retrieving search term from cache: ', search)
		print('\n')
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting new data for search term: ', search)
		print('\n')
		twitter_results = api.search(q=search)
		CACHE_DICTION[unique_identifier] = twitter_results
		f = codecs.open(CACHE_FNAME, 'w', encoding = "utf-8")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	tweet_texts = []
	for tweet in twitter_results['statuses']:
		tweet_texts.append("TWEET TEXT: " + tweet['text'])
		tweet_texts.append("CREATED AT: " + tweet['created_at'])
		tweet_texts.append("\n")
	return tweet_texts[:9]

search_term = input("Enter a search term: ")
print("\n")
three_tweets = get_tweets(search_term)
for t in three_tweets:
	r =t.encode("utf-8")
	try:
		print(r.decode("utf-8"))
	except:
		print(r)










