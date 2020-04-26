from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, RedirectView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Controls, user_info, tweets
from .forms import UserForm, UserLogin, AddControlForm

import tweepy
import json
# import credentials

consumer_key = 'Hokk7a7NferS2H94YgpvXGGot'
consumer_secret = 'l1TEv0a8j9WAcnIqT4DUU6YDPjNQFihkXZIvQWYKLvCAecC1pw'
access_token = '1063010159440490496-2sm6UH8Plaeb7KcoO3FIHreqjFgGTp'
access_secret = 'AYiNlXA4tLz3WoLItHDI6hMnSJJDAMdb1xHCHZJnUUa1a'

# Authorization to consumer key and consumer secret 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
# Access to user's access key and access secret 
auth.set_access_token(access_token, access_secret) 
# Calling api 
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# @method_decorator(login_required, name = 'dispatch')
class IndexView(LoginRequiredMixin ,generic.ListView):

    template_name = 'twitter/index.html'
    context_object_name = 'object_list'
    # By default it is object_list and we can change this name

    # this is the testing phase for pull push issue
    
    def get_queryset(self):
        controller = Controls.objects.filter(user_name = self.request.user)
        return user_info.objects.filter(twitter_handle__in = controller)


class DetailView(generic.DetailView):
    model = user_info
    template_name = 'twitter/detail.html'

    def get_context_data(self, **kwargs):

        context = super(DetailView, self).get_context_data(**kwargs)
        context['tweets'] = tweets.objects.filter(twitter_handle = self.get_object().twitter_handle)
        return context

class deleteTrack(DeleteView):
    model = Controls
    success_url = reverse_lazy('twitter:index')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user_name=owner)

    def get(self, request, pk):
        return self.post(request)

class addTrack(View):
    model = Controls

    def get(self, request, screen_name):
        # twitter_handle = request.GET.get('name', '')
        twitter_handle = screen_name
        controler = Controls(user_name = self.request.user, twitter_handle = twitter_handle)
        controler.save()

        user_ = api.get_user(str(twitter_handle))

        user_info(twitter_handle=controler, name=user_.name, url_image=user_.profile_image_url, description=user_.description, num_followers=user_.followers_count, blue_ticked=user_.verified).save()
        return redirect('twitter:index')




class SearchView(TemplateView):
    template_name = 'twitter/search.html'
    context_object_name = 'object_list'

    def get(self, request):
        q = request.GET.get('q', '')
        try:
            tweets = api.user_timeline(screen_name=q, tweet_mode='extended')
            # Creating an Empty List so that multiple Jsonline strings can be appended to a same file 
            l=[]
            # Extracting the json file of each tweet and appending it to the list
            for tweet in tweets:
                l.append(tweet._json)

            name = l[0]['user']['name']
            if name == "Nitin Chauhan":
                messages.success(request, 'Specified Username does not Exist ')
                return redirect('twitter:index')
            screen_name = l[0]['user']['screen_name']
            profile_image = l[0]['user']['profile_image_url']
            self.results = {
                'tweets': l,
                'name': name,
                'screen_name': screen_name,
                'profile_image': profile_image,
                'length': "120deg"
            }
            return super().get(request)
        except:
            
            messages.success(request, 'Specified Username does not Exist ')
            print('aaya bhai yhan')

            return redirect('twitter:index')
            # return super().get(request)
        

    def get_context_data(self):
        # context = super().get_context_data(results=self.results)
 
        return super().get_context_data(data=self.results)
    
    def get_template_names(self):
        data = self.results
        if 'notification' in data:
            print('yes')
            template_name = 'twitter/index.html'
        else:
            template_name = 'twitter/search.html'
        return [template_name]


class ControlCreate(CreateView):
    form_class = AddControlForm
    model = Controls

    success_url = reverse_lazy('twitter:index')

    # def get_initial(self):
    #     return {
    #         "user_name": self.request.user
    #     }

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super(ControlCreate, self).form_valid(form)



class AdminUpdate(UpdateView):
    model = Controls
    fields = ['user_name', 'admin_name', 'email', 'address', 'city', 'state', 'mobile', 'occupation']





class UserFormView(View):
    form_class = UserForm
    template_name = 'twitter/authentication.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    
    # processing form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit = False)
            # cleaned(normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # returns user object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # we can access data related to user with request.user.username
                    return redirect('twitter:index')

        return render(request, self.template_name, {'form': form})

class UserLoginView(View):
    form_class = UserLogin
    template_name = 'twitter/authentication.html'

    # display login form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    
    # procecssing data from form
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('twitter:index')
                else:
                    return render(request, self.template_name, {'form': form, 'error_message': 'Your account has been disabled' })
            else:
                return render(request, self.template_name, {'form': form , 'error_message': 'Invalid login'})
        return render(request, self.template_name, {'form': form})

class LogoutView(RedirectView):

    def get(self, request):
        logout(request)
        return redirect('twitter:login')
