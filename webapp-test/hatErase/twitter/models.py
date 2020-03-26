from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator 


class Handlers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    handle = models.CharField(max_length=250)

    def __str__(self):
        return self.handle

class Info(models.Model):
    handle = models.ForeignKey(Handlers, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    url_img = models.CharField(max_length=1000)
    description = models.CharField(max_length=250)
    num_followers = models.PositiveIntegerField(validators = [MaxValueValidator(9999999999)])
    
    def __str__(self):
        return self.name


class Tweets(models.Model):
    handle = models.ForeignKey(Handlers, on_delete=models.CASCADE)
    tweet_id = models.CharField(max_length=100)
    tweet_text = models.TextField(default=" ")
    hashtags = models.CharField(max_length=300)

    def __str__(self):
        return self.tweet_id