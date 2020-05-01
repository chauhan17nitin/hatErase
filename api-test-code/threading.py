import threading
import tweepy
import json
import credentials

username = "@narendramodi"         
auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret) 
auth.set_access_token(credentials.access_token, credentials.access_secret) 
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
tweets = api.user_timeline(screen_name=username) 

class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

listener = StdOutListener()
stream = Stream(auth, listener)
stream.filter(follow=['1063010159440490496'])




































###############################################################################
from datetime import date, datetime
from threading import Thread
import pandas as pd

def update_csv(p,c):
    
    df = pd.read_csv('track.csv', encoding='latin-1')
    
    dat = str(date.today())
    time = str(datetime.now().time())
    time = time.split('.')
    time = time[0]
    
update_csv(2,3)
df = pd.read_csv('track.csv', encoding='latin-1')






















