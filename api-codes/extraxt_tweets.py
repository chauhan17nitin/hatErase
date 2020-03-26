
# Importing the required libraries for extracting and storing data
import tweepy 
import json

# API credentials required for using twitter data
consumer_key = 'F1BCRW0AXUlr0wjLE8L6Znm8a'
consumer_secret = 'HqRCnviPD8TmI05TSL47CA9eL6niFYtRu35CIP6J2F0fhjL9zz'
access_key = '1163025465423982592-WrNzWHSUZykiwRmYbexhkUa5BGudYZ'
access_secret = 'bZ0mWxWgFMClId9OoauDLQgT9IlwojmFS65OuGsy0E9QQ'

username = "ml intern"         
# Authorization to consumer key and consumer secret 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
# Access to user's access key and access secret 
auth.set_access_token(access_key, access_secret) 
  
# Calling api 
# used proxy due to college lan issue 
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
tweets = api.user_timeline(screen_name=username) 
        
# Creating an Empty List so that multiple Jsonline strings can be appended to a same file 
l=[]
# Extracting the json file of each tweet and appending it to the list
for tweet in tweets:
    l.append(tweet._json)
            
# saving the tweet data into a jsonline file having extension jsonl 
list_json=json.dumps(l, indent=4)
with open('modi.jsonl','w') as outfile:
    outfile.write(list_json)

import pandas as pd 
list_final = []        
with open('modi.jsonl') as json_file:  
    data = json.load(json_file)
    for datax in data:
        list2 = [datax['text'],datax['created_at'],datax['favorite_count'],datax['retweet_count']]
        list_final.append(list2)
df = pd.DataFrame(list_final, columns = ['text', 'time','likes','retweets'])
