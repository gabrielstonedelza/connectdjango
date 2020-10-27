from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import NotifyMe, Tutorial, BlogPost
from users.models import Profile
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=Tutorial)
def create_tutorial(sender, created, instance, **kwargs):
    title = f"New Tutorial"
    message = f"{instance.user} added a new tutorial"

    my_profile = get_object_or_404(Profile, user=instance.user)
    followers = my_profile.followers.all()

    if created:
        for i in followers:
            NotifyMe.objects.create(user=i, notify_title=title, notify_alert=message, follower_sender=instance.user, tuto_id=instance.id)


@receiver(post_save, sender=BlogPost)
def create_blog(sender, created, instance, **kwargs):
    title = "New Post"
    message = f"{instance.user} added a new blog"

    my_profile = get_object_or_404(Profile, user=instance.user)
    followers = my_profile.followers.all()

    if created:
        for i in followers:
            NotifyMe.objects.create(user=i, notify_title=title, notify_alert=message, follower_sender=instance.user, blog_id=instance.id)


