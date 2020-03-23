from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator
from django.urls import reverse
# Create your models here.


class Controls(models.Model):
    user_name = models.ForeignKey(User, on_delete = models.CASCADE)
    twitter_handle = models.CharField(max_length=150)

    # class Meta:
        # unique_together = ('user_name', 'twitter_handle')

    def __str__(self):
        return self.twitter_handle

class user_info(models.Model):
    twitter_handle = models.ForeignKey(Controls, on_delete = models.CASCADE)
    name = models.CharField(max_length=200)
    url_image = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=500, default="")
    num_followers = models.PositiveIntegerField(validators = [MaxValueValidator(9999999999)])
    # num_following = models.PositiveIntegerField(validators = [MaxValueValidator(9999999999)])
    blue_ticked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class tweets(models.Model):
    twitter_handle = models.ForeignKey(Controls, on_delete=models.CASCADE)
    tweet_id = models.CharField(max_length=100)
    tweet_text = models.TextField(default=" ")
    hashtags = models.CharField(max_length=300)

    def __str__(self):
        return self.tweet_text
    