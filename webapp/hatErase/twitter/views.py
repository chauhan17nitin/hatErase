from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from .models import Admin
from django.template import loader


# Create your views here.


# def index(request):

#     all_admin = Admin.objects.all()
#     context = {
#         'all_admin': all_admin,
#     }
#     return render(request, 'twitter/index.html', context) 

# def detail(request, admin_id):
#     # try:
#     #     admin = Admin.objects.get(pk=admin_id)
#     # except Admin.DoesNotExist:
#     #     raise Http404("Aldmin does not exists")
#     admin = get_object_or_404(Admin, pk=admin_id)
#     return render(request, 'twitter/detail.html', {'admin': admin})

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View


from .models import Admin
from .forms import UserForm

class IndexView(generic.ListView):
    template_name = 'twitter/index.html'
    context_object_name = 'object_list'
    # By default it is object_list and we can change this name
    

    def get_queryset(self):
        return Admin.objects.all()

class DetailView(generic.DetailView):
    model = Admin
    template_name = 'twitter/detail.html'


class AdminCreate(CreateView):
    model = Admin
    fields = ['user_name', 'admin_name', 'email', 'address', 'city', 'state', 'mobile', 'occupation']
    
class AdminUpdate(UpdateView):
    model = Admin
    fields = ['user_name', 'admin_name', 'email', 'address', 'city', 'state', 'mobile', 'occupation']

class AdminDelete(DeleteView):
    model = Admin
    success_url = reverse_lazy('music:index')

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
            password = form.cleaned_data['passowrd']

            user.set_password(password)
            user.save()