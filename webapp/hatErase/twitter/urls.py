from django.conf.urls import url
from . import views

app_name = 'twitter'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name = 'detail'),
    # adding new admin user
    url(r'admin/add/$', views.AdminCreate.as_view(), name = 'admin-add'),
    # /twitter/admin/2/
    url(r'admin/(?P<pk>[0-9]+)/$', views.AdminUpdate.as_view(), name = 'admin-update'),
    # /twitter/admin/2/delete/
    url(r'^(?P<pk>[0-9]+)/delete/$', views.AdminDelete.as_view(), name = 'admin-delete'),






    # url(r'^signup/$', views.signup, name = 'signup')
]