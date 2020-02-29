from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from .models import Admin
from django.template import loader


# Create your views here.


def index(request):

    all_admin = Admin.objects.all()
    context = {
        'all_admin': all_admin,
    }
    return render(request, 'twitter/index.html', context) 

def detail(request, admin_id):
    # try:
    #     admin = Admin.objects.get(pk=admin_id)
    # except Admin.DoesNotExist:
    #     raise Http404("Aldmin does not exists")
    admin = get_object_or_404(Admin, pk=admin_id)
    return render(request, 'twitter/detail.html', {'admin': admin})
