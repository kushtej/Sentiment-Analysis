import sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sent_mod
from twitter_credentials import *
import json

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]  
        sentiment,confidence_level = sent_mod.sentiment(tweet)
        
        if confidence_level*100 > 80:
            print(tweet," ",sentiment,confidence_level)
            file = open(".twitter_stream_data.txt","a")
            file.write(sentiment)
            file.write("\n")
            file.close()
            
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=[sys.argv[1]])
