from django.contrib.auth.models import Permission, User
from django.db import models


class Handlers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    handle = models.CharField(max_length=250)
    handler_name = models.CharField(max_length=500)

    def __str__(self):
        return self.handle + ' - ' + self.handler_name

class Tweets(models.Model):
    handle = models.ForeignKey(Handlers, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=250)

    def __str__(self):
        return self.tweet
