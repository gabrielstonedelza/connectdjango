import pytz
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from .validator import validate_file_size


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=500,blank=True, default="Team work is all we need")
    room_logo = models.ImageField(upload_to="room_pics",blank=True, default='room.jpg')
    is_active = models.BooleanField(default=False)
    allowed_users = models.ManyToManyField(User, related_name="allowed",blank=True)
    pending_users = models.ManyToManyField(User, related_name="pending",blank=True)
    key = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, allow_unicode=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name

    def get_absolute_room_url(self):
        return reverse("room_detail", args={self.room_name})

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    love = models.ManyToManyField(User, related_name='love', blank=True)
    funny = models.ManyToManyField(User, related_name="funny", blank=True)

    def __str__(self):
        return f"{self.author.username} just sent a message to the group"

    def last_10_messages():
        return Message.objects.order_by('-date_posted')[:10]

class PrivateMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    love = models.ManyToManyField(User, related_name='love', blank=True)
    funny = models.ManyToManyField(User, related_name="funny", blank=True)

    def __str__(self):
        return f"{self.author.username} just sent a message to the group"

    def last_10_messages():
        return Message.objects.order_by('-date_posted')[:10]

class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=500, help_text="your suggestions are important,let us know. ")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} gave a feedback"



class NotifyMe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notify_title = models.CharField(max_length=100, default="New Notification")
    notify_alert = models.CharField(max_length=200)
    follower_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="who_started_following")
    read = models.BooleanField(default=False)
    blog_id = models.IntegerField(blank=True, default=0)
    tuto_id = models.IntegerField(blank=True, default=0)
    improvement_id = models.IntegerField(blank=True, default=0)
    date_notified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New {self.notify_title} notification sent to  {self.user}"

    def get_absolute_notification_url(self):
        return reverse("notify_detail", args=self.pk)
