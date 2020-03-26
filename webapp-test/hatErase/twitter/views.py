from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import View, ListView
from django.contrib import messages

from .forms import UserForm
from .models import Handlers, Info, Tweets


import tweepy
import json
from twitter import credentials

# Authorization to consumer key and consumer secret 
auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret) 
# Access to user's access key and access secret 
auth.set_access_token(credentials.access_token, credentials.access_secret) 
# Calling api 
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'twitter/home.html')
    else:
        return render(request, 'twitter/index.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Handlers.objects.filter(user=request.user)
                return render(request, 'twitter/index.html') #{'albums': albums})
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
                # albums = Album.objects.filter(user=request.user)
                return render(request, 'twitter/index.html')#, {'albums': albums})
            else:
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


# def create_handler(request):
#     if not request.user.is_authenticated:
#         return render(request, 'twitter/login.html')
#     else:
#         form = HandlerForm(request.POST or None)
#         if form.is_valid():
#             handler = form.save(commit=False)
#             handler.user = request.user
#             handler.save()
#             return handler_view(request)
#         context = {
#             "form": form,
#         }

#         return render(request, 'twitter/create_handler.html', context)

def handler_view(request):

    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        
        users = Handlers.objects.filter(user=request.user)
        # print('ll')
        handlers = Info.objects.filter(handle__in = users)
        # print(handlers)
        # return index(request)
        return render(request, 'twitter/handler.html', {'handlers': handlers})

def detail(request, handle):
    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        # user = request.user
        handle = get_object_or_404(Handlers, pk=handle)
        handler = Info.objects.filter(name = handle)
        return render(request, 'twitter/detail.html', {'handler': handler})#, 'user': user})


def search_bar(request):

    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        query = request.GET.get("q","")
        if query:
            result = retreive_tweets(query)
            
            return render(request, 'twitter/searched.html', {'result': result})

def add_track(request, screen_name):

    if not request.user.is_authenticated:
        return render(request, 'twitter/login.html')
    else:
        if Handlers.objects.filter(user=request.user).exists():
            users = Handlers.objects.values('handle').filter(user=request.user).values()
            users = list(users)
            hl = [x['handle'] for x in users]
            print(hl)
            if screen_name in hl:
                messages.success(request, 'The handle is being tracked already')
                return handler_view(request)
            else:
                info = Handlers(user = request.user, handle = screen_name)
                info.save()
                user_ = api.get_user(str(screen_name))
                Info(handle=info, name=user_.name, url_img=user_.profile_image_url, description=user_.description, num_followers=user_.followers_count).save()
                
                return handler_view(request)
        else:
            info = Handlers(user = request.user, handle = screen_name)
            info.save()
            user_ = api.get_user(str(screen_name))
            Info(handle=info, name=user_.name, url_img=user_.profile_image_url, description=user_.description, num_followers=user_.followers_count).save()
            
            return handler_view(request)

def retreive_tweets(handle):

    tweets_rec = api.user_timeline(screen_name=handle, tweet_mode='extended') 
    list_tweets=[]
    # Extracting the json file of each tweet and appending it to the list
    for tweet in tweets_rec:
        list_tweets.append(tweet._json)
    name = list_tweets[0]['user']['name']
    screen_name = list_tweets[0]['user']['screen_name']
    profile_image = list_tweets[0]['user']['profile_image_url']
    result = {
        'tweets': list_tweets,
        'name': name,
        'screen_name': screen_name,
        'profile_image': profile_image,
    }

    return result