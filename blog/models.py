import pytz
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from .validator import validate_file_size
from django.utils.text import slugify
import random


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=150, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=500, blank=True, default="Team work is all we need")
    room_logo = models.ImageField(upload_to="room_pics", validators=[validate_file_size])
    is_active = models.BooleanField(default=False, help_text="Make your room active for communication or inactive for users")
    allowed_users = models.ManyToManyField(User, related_name="allowed", blank=True)
    pending_users = models.ManyToManyField(User, related_name="pending", blank=True)
    slug = models.SlugField(max_length=100, default='')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name

    def get_absolute_room_url(self):
        kwargs = {
            # 'pk': self.id,
            'slug': self.slug
        }
        return reverse('room_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.room_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

        if self.room_logo:
            img = Image.open(self.room_logo.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.room_logo.path)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    chat_id = models.CharField(max_length=400)
    date_posted = models.DateTimeField(auto_now_add=True)
    msg_file = models.FileField(upload_to='message_files', blank=True, validators=[validate_file_size])
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    love = models.ManyToManyField(User, related_name='love', blank=True)
    funny = models.ManyToManyField(User, related_name="funny", blank=True)

    def __str__(self):
        return f"{self.author.username} just sent a message to the group"


class PrivateMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    chat_id = models.CharField(max_length=400)
    date_posted = models.DateTimeField(auto_now_add=True)
    pmsg_file = models.FileField(upload_to='private_message_files', blank=True, validators=[validate_file_size])
    like = models.ManyToManyField(User, related_name='plikes', blank=True)
    love = models.ManyToManyField(User, related_name='plove', blank=True)
    funny = models.ManyToManyField(User, related_name="pfunny", blank=True)

    def __str__(self):
        return self.author.username


class Chatters(models.Model):
    chatter_users = models.CharField(max_length=200)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatter2")
    private_chat_id = models.CharField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.private_chat_id


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=150)
    blog_pic = models.ImageField(upload_to="blogpics", blank=True, validators=[validate_file_size])
    blog_content = models.TextField(default='')
    slug = models.SlugField(max_length=100, allow_unicode=True, default='')
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    views = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count

    def get_absolute_blog(self):
        kwargs = {
            # 'pk': self.id,
            'slug': self.slug
        }
        return reverse('blog_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

        if self.blog_pic:
            img = Image.open(self.blog_pic.path)

            if img.height > 600 or img.width > 900:
                output_size = (680, 400)
                img.thumbnail(output_size)
                img.save(self.blog_pic.path)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField(default='...')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has commented on {self.blog}"


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
    room_slug = models.CharField(max_length=200)
    blog_slug = models.CharField(max_length=100, blank=True)
    date_notified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New {self.notify_title} notification sent to  {self.user}"

    def get_absolute_notification_url(self):
        return reverse("notify_detail", args=self.pk)
