from django.conf.urls import url
from . import views

app_name = 'twitter'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^handler/$', views.handler_view, name='handler'),
    url(r'^(?P<info_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search_bar, name = 'search'),
    url(r'^add/(?P<screen_name>\w+)/$', views.add_track, name='add_track'),
    url(r'^(?P<info_id>[0-9]+)/delete_track/$', views.delete_track, name='delete'),

    # url(r'^create_handler/$', views.create_handler, name='create_handler'),
]

