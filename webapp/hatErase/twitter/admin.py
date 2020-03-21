from django.contrib import admin
from .models import  Controls, user_info, tweets
# Register your models here.

admin.site.register(Controls)
admin.site.register(user_info)
admin.site.register(tweets)


