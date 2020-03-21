from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, RedirectView


from .models import Controls
from .forms import UserForm, UserLogin

class IndexView(generic.ListView):
    template_name = 'twitter/index.html'
    context_object_name = 'object_list'
    # By default it is object_list and we can change this name
    

    def get_queryset(self):
        return Controls.objects.all()

class DetailView(generic.DetailView):
    model = Controls
    template_name = 'twitter/detail.html'


class AdminCreate(CreateView):
    model = Controls
    fields = ['user_name', 'twitter_handle']
    success_url = reverse_lazy('twitter:index')
    
class AdminUpdate(UpdateView):
    model = Controls
    fields = ['user_name', 'admin_name', 'email', 'address', 'city', 'state', 'mobile', 'occupation']

class AdminDelete(DeleteView):
    model = Controls
    success_url = reverse_lazy('twitter:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'twitter/registration_form.html'
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
    template_name = 'twitter/login_form.html'

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
