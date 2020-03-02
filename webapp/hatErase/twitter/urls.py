from django.conf.urls import url
from . import views

app_name = 'twitter'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name = 'detail'),
    url(r'admin/add/$', views.Admin.as_view(), name = 'album-add')
    # url(r'^signup/$', views.signup, name = 'signup')
]