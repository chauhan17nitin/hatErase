from django.contrib import admin
from .models import Handlers, Info, Tweets

admin.site.register(Handlers)
admin.site.register(Info)
admin.site.register(Tweets)
