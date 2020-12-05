from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import NotifyMe, Message, PrivateMessage, ChatRoom, Blog, Comments
from users.models import Profile
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=Blog)
def create_blog(sender, created, instance, **kwargs):
    title = "New Blog Post"
    message = f"{instance.user} added a new blog"

    my_profile = get_object_or_404(Profile, user=instance.user)
    followers = my_profile.followers.all()

    if created:
        for i in followers:
            NotifyMe.objects.create(user=i, notify_title=title, notify_alert=message, follower_sender=instance.user,
                                    blog_slug=instance.slug)


@receiver(post_save, sender=Comments)
def alert_tutorial_comment(sender, created, instance, **kwargs):
    title = "New Blog comment"
    blog_user = instance.blog.user
    message = f"{instance.user} commented on your blog '{instance.blog.title}'"

    if created:
        if not instance.user == instance.blog.user:
            NotifyMe.objects.create(user=blog_user, notify_title=title, notify_alert=message,
                                    follower_sender=instance.user, blog_slug=instance.blog.slug)
