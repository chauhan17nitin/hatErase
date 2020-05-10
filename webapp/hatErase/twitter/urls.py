from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'twitter'

urlpatterns = [
    url(r'^$', (views.IndexView.as_view()), name = 'index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name = 'detail'),

    url(r'^register/$', views.UserFormView.as_view(), name = 'register'),
    url(r'^login/$', views.UserLoginView.as_view(), name = 'login'),
    url(r'^accounts/login/$', views.UserLoginView.as_view(), name = 'login'),
    url(r'^logout/$', views.LogoutView.as_view(), name = 'logout'),
    # adding new admin user


    url(r'^search/$', views.SearchView.as_view(), name = 'search'),
    
    # url(r'^delete/$', views.deleteTrack.as_view(), name = 'delete-track'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.deleteTrack.as_view(), name = 'delete-track'),

       
    url(r'^add/(?P<screen_name>\w+)/$', views.addTrack.as_view(), name='add_track'),

    url(r'controls/add/$', views.ControlCreate.as_view(), name = 'control-add'),
    # /twitter/admin/2/
    # url(r'admin/(?P<pk>[0-9]+)/$', views.AdminUpdate.as_view(), name = 'admin-update'),
    # /twitter/admin/2/delete/
    # url(r'^(?P<pk>[0-9]+)/delete/$', views.AdminDelete.as_view(), name = 'admin-delete'),

    






    # url(r'^signup/$', views.signup, name = 'signup')
]