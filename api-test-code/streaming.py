from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import credentials



# if __name__ == '__main__':
def Start_stream():

    class StdOutListener(StreamListener):
        def on_data(self, data):
            if data:
                print(data)
            else:
                print('nhi aaya bsdk')
            return True

        def on_error(self, status):
            print(status)


    listener = StdOutListener()
    auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_secret)

    stream = Stream(auth, listener)

    # to track users
    s = stream.filter(follow=['1163025465423982592'])
