# models.py

from django.db import models
from django.contrib.auth.models import User


class Tier(models.Model):
    name = models.CharField(max_length=200)
    thumbnail_sizes = models.JSONField(default=list)
    has_original = models.BooleanField(default=True)
    can_expire = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ": " + str(self.created_at)
