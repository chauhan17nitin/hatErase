from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^twitter/', include('twitter.urls')),
    url(r'^', include('twitter.urls')),
]
