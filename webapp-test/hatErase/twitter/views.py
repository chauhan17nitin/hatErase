from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import View, ListView
from django.contrib import messages

from .forms import UserForm
from .models import Handlers, Info, Tweets

# twitter api
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler,Stream
from tweepy import TweepError

# mailing service
from django.core.mail import send_mail
from hatErase.settings import EMAIL_HOST_USER

# multithreading
from threading import Thread
import multiprocessing
from time import sleep

import json

from twitter import inference

from twitter import credentials

# Authorization to consumer key and consumer secret
auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
# Access to user's access key and access secret
auth.set_access_token(credentials.access_token, credentials.access_secret)
# Calling api
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

I = inference.Inference()

track_list = []

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'twitter/home.html')
    else:
        return render(request, 'twitter/index.html')


def signup_email(email_id, name):
    subject = "Welcome {} to hatErase".format(name)
    message = "Hi {}, Welcome to hatErase.\n A real-time solution for tracking any twitter account and stoping community hates. Just for making community better and cleaner.\n Enjoying Using hatErase \n Regards \nCo-Founders \n Nitin Chauhan & Srijan Singh".format(name)
    send_mail(subject, message, EMAIL_HOST_USER, [email_id], fail_silently = False)
    print('Mail Done Dude')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        signup_email(email, username)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'twitter/index.html')
    context = {
        "form": form,
    }
    return render(request, 'twitter/register.html', context)


def login_user(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'twitter/index.html')
                return render(request, 'twitter/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'twitter/login.html', {'error_message': 'Invalid login'})

    return render(request, 'twitter/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'twitter/login.html', context)


def handler_view(request):

    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        users = Handlers.objects.filter(user=request.user)
        handlers = Info.objects.filter(handle__in = users)
        return render(request, 'twitter/handler.html', {'handlers': handlers})

def detail(request, info_id):
    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        handler = get_object_or_404(Info, pk=info_id)
        return render(request, 'twitter/detail.html', {'handler': handler})


def search_bar(request):
    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        query = request.GET.get("q", False)
        if query:
            result = retreive_tweets(query)
            if result:
                return render(request, 'twitter/searched.html', {'result': result})
            else:
                result={'screen_name': query}
                return render(request, 'twitter/searched.html', {'none': 'The seached handle does not exist. Please check again.', 'result': result})
        else:
            # print('dd')
            result={'screen_name': 'dummy'}
            return render(request, 'twitter/searched.html', {'none': 'Please check you have searched something.', 'result': result})


def add_track(request, screen_name):
    global track_list, stream
    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        if Handlers.objects.filter(user=request.user).exists():
            users = Handlers.objects.values('handle').filter(user=request.user).values()
            users = list(users)
            hl = [x['handle'] for x in users]
            # print(hl)
            if screen_name in hl:
                messages.success(request, 'The handle is being tracked already')
                return handler_view(request)
            else:
                info = Handlers(user = request.user, handle = screen_name)
                info.save()
                user_ = api.get_user(str(screen_name))
                # print(user_.id_str)
                Info(handle=info, id_str=user_.id_str, name=user_.name, url_img=user_.profile_image_url, description=user_.description, num_followers=user_.followers_count).save()
                track_list.append(str(user_.id))

                stream.disconnect()
                stream = Start_stream()

                return handler_view(request)
        else:
            info = Handlers(user = request.user, handle = screen_name)
            info.save()
            user_ = api.get_user(str(screen_name))
            Info(handle=info, id_str=user_.id_str, name=user_.name, url_img=user_.profile_image_url, description=user_.description, num_followers=user_.followers_count).save()
            track_list.append(str(user_.id))
            # Starting thread for streaming
            # th = Thread(target=Start_stream)
            # th.start()
            stream.disconnect()
            stream = Start_stream()

            return handler_view(request)

def delete_track(request, info_id):
    global stream
    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        h = Handlers.objects.get(pk=info_id)
        handler = get_object_or_404(Info, pk=info_id)
        track_list.remove(handler.id_str)
        h.delete() # very important delete after otherwise details will be deleted from Info models
        stream.disconnect()
        stream = Start_stream()
        return handler_view(request)

def retreive_tweets(handle):

    try:
        tweets_rec = api.user_timeline(screen_name=handle, tweet_mode='extended')
        # print(tweets_rec)
        list_tweets=[]
        pred_tweets_list=[]
        if tweets_rec:
        # Extracting the json file of each tweet and appending it to the list
            for tweet in tweets_rec:
                tw = tweet._json
                text = tw['full_text']
                _,_,_,pro_text = I.preprocess_text(text)
                # print(text)
                tfidf_text = I.fit_transform(pro_text)
                pred = I.predict(tfidf_text)
                pred_tweets = {'text': text, 'pred': pred}
                pred_tweets_list.append(pred_tweets)
                list_tweets.append(tweet._json)


            name = list_tweets[0]['user']['name']
            id_str = list_tweets[0]['id_str']
            screen_name = list_tweets[0]['user']['screen_name']
            profile_image = list_tweets[0]['user']['profile_image_url']
            result = {
                'tweets': pred_tweets_list,
                'id': id_str,
                'name': name,
                'screen_name': screen_name,
                'profile_image': profile_image,
            }

            return result

        else:
            return None
    except TweepError:
        return None

def Start_stream():
    global track_list
    print(track_list)
    class StdOutListener(StreamListener):
        def on_data(self, data):
            if data:

                print(data)

            return True

        def on_error(self, status):
            print(status)


    listener = StdOutListener()
    stream = Stream(auth, listener)

    # to track users
    stream.filter(follow=track_list, is_async=True)
    return stream

stream = Start_stream()
