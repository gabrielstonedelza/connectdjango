from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True, default="I am a django developer")
    name = models.CharField(max_length=150, default="New User")
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True, default='default.jpg')
    cover_pic = models.ImageField(upload_to="cover_pics", blank=True, default='cover-default.jpg')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    your_facebook = models.CharField(max_length=450, blank=True)
    your_instagram = models.CharField(max_length=450, blank=True)
    your_twitter = models.CharField(max_length=450, blank=True)
    your_youtube = models.CharField(max_length=450, blank=True)
    your_medium = models.CharField(max_length=450, blank=True)
    your_linkedin = models.CharField(max_length=450, blank=True)
    your_github = models.CharField(max_length=450, blank=True)
    date_followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    def my_following_count(self):
        return self.following.count

    def my_followers_count(self):
        return self.followers.count


class LastSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s last seen was {self.last_seen}"

