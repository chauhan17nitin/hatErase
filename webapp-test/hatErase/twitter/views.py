from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import View, ListView


from .forms import UserForm
from .models import Handlers, Tweets

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
    return render(request, 'twitter/home.html', context)
